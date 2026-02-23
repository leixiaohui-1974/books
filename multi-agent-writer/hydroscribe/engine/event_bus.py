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
    - 支持 WebSocket 广播到前端
    - 保存事件历史（用于 UI 回放）
    """

    def __init__(self, max_history: int = 1000):
        self._subscribers: Dict[EventType, List[Callable]] = defaultdict(list)
        self._global_subscribers: List[Callable] = []
        self._ws_connections: Set[Any] = set()
        self._history: List[Event] = []
        self._max_history = max_history
        self._lock = asyncio.Lock()

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

    async def publish(self, event: Event):
        """发布事件"""
        async with self._lock:
            # 保存到历史
            self._history.append(event)
            if len(self._history) > self._max_history:
                self._history = self._history[-self._max_history:]

        logger.info(f"[Event] {event.type.value} from {event.source_agent}: {json.dumps(event.payload, ensure_ascii=False, default=str)[:200]}")

        # 通知特定订阅者
        for handler in self._subscribers.get(event.type, []):
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(event)
                else:
                    handler(event)
            except Exception as e:
                logger.error(f"Event handler error: {e}")

        # 通知全局订阅者
        for handler in self._global_subscribers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(event)
                else:
                    handler(event)
            except Exception as e:
                logger.error(f"Global handler error: {e}")

        # 广播到所有 WebSocket 连接
        await self._broadcast_ws(event)

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
