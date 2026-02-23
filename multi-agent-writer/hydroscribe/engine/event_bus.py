"""
事件总线 — Agent 间异步通信 + WebSocket 实时推送
"""

import asyncio
import json
import logging
from collections import defaultdict
from typing import Any, Callable, Coroutine, Dict, List, Optional, Set

from hydroscribe.schema import Event, EventType

logger = logging.getLogger("hydroscribe.event_bus")


class EventBus:
    """
    事件总线：所有 Agent 的通信中枢
    - 支持事件订阅/发布
    - 支持 WebSocket 广播到前端（含心跳检测）
    - 保存事件历史（用于 UI 回放）
    - 支持优雅关闭
    """

    def __init__(self, max_history: int = 1000, ws_heartbeat_interval: float = 30.0, max_dead_letters: int = 200):
        self._subscribers: Dict[EventType, List[Callable]] = defaultdict(list)
        self._global_subscribers: List[Callable] = []
        self._ws_connections: Set[Any] = set()
        self._history: List[Event] = []
        self._max_history = max_history
        self._lock = asyncio.Lock()
        self._shutting_down = False
        self._ws_heartbeat_interval = ws_heartbeat_interval
        self._heartbeat_task: Optional[asyncio.Task] = None
        # 死信队列 — 记录处理失败/超时的事件
        self._dead_letters: List[Dict] = []
        self._max_dead_letters = max_dead_letters

    def subscribe(self, event_type: EventType, handler: Callable):
        """订阅特定事件类型"""
        self._subscribers[event_type].append(handler)

    def subscribe_all(self, handler: Callable):
        """订阅所有事件（用于 UI 推送）"""
        self._global_subscribers.append(handler)

    def register_ws(self, ws):
        """注册 WebSocket 连接"""
        self._ws_connections.add(ws)

    def unregister_ws(self, ws):
        """注销 WebSocket 连接"""
        self._ws_connections.discard(ws)

    def start_heartbeat(self):
        """启动 WebSocket 心跳任务 — 定期 ping 检测断连"""
        if self._heartbeat_task is None or self._heartbeat_task.done():
            self._heartbeat_task = asyncio.ensure_future(self._heartbeat_loop())
            logger.info(f"WebSocket 心跳已启动 (间隔 {self._ws_heartbeat_interval}s)")

    async def _heartbeat_loop(self):
        """心跳循环 — 向所有 WS 连接发送 ping，清理断连"""
        while not self._shutting_down:
            try:
                await asyncio.sleep(self._ws_heartbeat_interval)
            except asyncio.CancelledError:
                break

            if not self._ws_connections:
                continue

            dead = set()
            for ws in list(self._ws_connections):
                try:
                    await ws.send_text('{"type":"heartbeat"}')
                except Exception:
                    dead.add(ws)

            if dead:
                self._ws_connections -= dead
                logger.info(f"心跳清理 {len(dead)} 个断连 WebSocket")

    async def shutdown(self):
        """优雅关闭 — 通知所有 WS 连接并清理资源"""
        self._shutting_down = True
        logger.info("EventBus 正在关闭...")

        # 取消心跳
        if self._heartbeat_task and not self._heartbeat_task.done():
            self._heartbeat_task.cancel()
            try:
                await self._heartbeat_task
            except asyncio.CancelledError:
                pass

        # 通知所有 WS 连接
        for ws in list(self._ws_connections):
            try:
                await ws.send_text('{"type":"shutdown","message":"服务器正在关闭"}')
                await ws.close()
            except Exception:
                pass
        self._ws_connections.clear()

        # 清理订阅者
        self._subscribers.clear()
        self._global_subscribers.clear()
        logger.info("EventBus 已关闭")

    async def publish(self, event: Event, handler_timeout: float = 10.0):
        """
        发布事件（带处理器超时保护）

        Args:
            event: 待发布的事件
            handler_timeout: 单个处理器的最大执行时间（秒），超时则跳过
        """
        async with self._lock:
            # 保存到历史
            self._history.append(event)
            if len(self._history) > self._max_history:
                self._history = self._history[-self._max_history:]

        logger.info(f"[Event] {event.type.value} from {event.source_agent}: {json.dumps(event.payload, ensure_ascii=False, default=str)[:200]}")

        # 通知特定订阅者（带超时保护）
        for handler in self._subscribers.get(event.type, []):
            await self._invoke_handler(handler, event, handler_timeout)

        # 通知全局订阅者（带超时保护）
        for handler in self._global_subscribers:
            await self._invoke_handler(handler, event, handler_timeout)

        # 广播到所有 WebSocket 连接
        await self._broadcast_ws(event)

    async def _invoke_handler(self, handler: Callable, event: Event, timeout: float):
        """调用单个处理器（带超时保护 + 死信记录）"""
        handler_name = getattr(handler, "__name__", str(handler))
        try:
            if asyncio.iscoroutinefunction(handler):
                await asyncio.wait_for(handler(event), timeout=timeout)
            else:
                handler(event)
        except asyncio.TimeoutError:
            logger.warning(
                f"事件处理器超时 [{handler_name}] "
                f"(>{timeout}s, event={event.type.value})"
            )
            self._record_dead_letter(event, handler_name, "timeout", f"超时 >{timeout}s")
        except Exception as e:
            logger.error(f"事件处理器错误 [{handler_name}]: {e}")
            self._record_dead_letter(event, handler_name, "error", str(e))

    def _record_dead_letter(self, event: Event, handler_name: str, reason: str, detail: str):
        """记录失败事件到死信队列"""
        from datetime import datetime, timezone
        entry = {
            "event_id": event.id,
            "event_type": event.type.value,
            "handler": handler_name,
            "reason": reason,
            "detail": detail,
            "book_id": event.book_id,
            "chapter_id": event.chapter_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self._dead_letters.append(entry)
        if len(self._dead_letters) > self._max_dead_letters:
            self._dead_letters = self._dead_letters[-self._max_dead_letters:]

    def get_dead_letters(self, limit: int = 50) -> List[Dict]:
        """查询死信队列（最近 N 条）"""
        return self._dead_letters[-limit:]

    def clear_dead_letters(self):
        """清空死信队列"""
        self._dead_letters.clear()

    async def _broadcast_ws(self, event: Event):
        """广播事件到所有 WebSocket 客户端"""
        if not self._ws_connections:
            return

        message = {
            "id": event.id,
            "type": event.type.value,
            "timestamp": event.timestamp.isoformat(),
            "agent": event.source_agent,
            "book": event.book_id,
            "chapter": event.chapter_id,
            "payload": event.payload,
        }
        data = json.dumps(message, ensure_ascii=False, default=str)

        dead_connections = set()
        for ws in self._ws_connections:
            try:
                await ws.send_text(data)
            except Exception:
                dead_connections.add(ws)

        # 清理断开的连接
        self._ws_connections -= dead_connections

    def get_history(self, limit: int = 50, book_id: Optional[str] = None) -> List[Dict]:
        """获取事件历史"""
        events = self._history
        if book_id:
            events = [e for e in events if e.book_id == book_id]
        return [
            {
                "id": e.id,
                "type": e.type.value,
                "timestamp": e.timestamp.isoformat(),
                "agent": e.source_agent,
                "book": e.book_id,
                "chapter": e.chapter_id,
                "payload": e.payload,
            }
            for e in events[-limit:]
        ]

    def get_agent_status_summary(self) -> Dict[str, str]:
        """从事件历史推断各 Agent 当前状态"""
        agent_states: Dict[str, str] = {}
        for event in self._history:
            if event.type == EventType.TASK_STARTED:
                agent_states[event.source_agent] = "busy"
            elif event.type in (EventType.TASK_COMPLETED, EventType.TASK_FAILED):
                agent_states[event.source_agent] = "idle"
        return agent_states
