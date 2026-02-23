"""
HydroScribe Web API — FastAPI + WebSocket 实时推送
"""

import asyncio
import json
import logging
import os
import time
from collections import defaultdict
from typing import Optional

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from starlette.middleware.base import BaseHTTPMiddleware

from hydroscribe.engine.orchestrator import Orchestrator
from hydroscribe.engine.event_bus import EventBus
from hydroscribe.engine.config_loader import get_config
from hydroscribe.engine.logging_config import setup_logging
from hydroscribe.engine.book_registry import BOOK_REGISTRY, get_book_spec, validate_book_id
from hydroscribe.engine.audit_log import get_audit_logger
from hydroscribe.schema import EventType, Event, SkillType

logger = logging.getLogger("hydroscribe.api")

# 启动时间记录 (用于 uptime 计算)
_start_time = time.monotonic()


# ── 速率限制中间件 ────────────────────────────────────────────

class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    简单的滑动窗口速率限制器

    按客户端 IP 限制每分钟请求数。WebSocket 和健康检查端点豁免。
    """

    def __init__(self, app, max_requests: int = 120, window_seconds: int = 60):
        super().__init__(app)
        self._max_requests = max_requests
        self._window = window_seconds
        self._requests: dict = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        # 豁免路径
        path = request.url.path
        if path in ("/health", "/ready", "/ws") or path.startswith("/static"):
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"
        now = time.monotonic()

        # 清理过期记录
        timestamps = self._requests[client_ip]
        cutoff = now - self._window
        self._requests[client_ip] = [t for t in timestamps if t > cutoff]
        timestamps = self._requests[client_ip]

        if len(timestamps) >= self._max_requests:
            logger.warning(f"速率限制: {client_ip} 超过 {self._max_requests} req/{self._window}s")
            return JSONResponse(
                status_code=429,
                content={"error": "请求过于频繁", "retry_after_seconds": self._window},
            )

        timestamps.append(now)
        return await call_next(request)



# ── 初始化 ────────────────────────────────────────────────────

config = get_config()
BOOKS_ROOT = os.environ.get("BOOKS_ROOT", config.books_root)

app = FastAPI(
    title="HydroScribe — CHS 多智能体协同写作助手",
    description="基于 OpenManus+OpenClaw 架构，融合 9 大写作技能的多智能体系统 (阿里云百炼优化)",
    version="0.3.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.server.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RateLimitMiddleware, max_requests=120, window_seconds=60)

orchestrator = Orchestrator(books_root=BOOKS_ROOT, config=config)


@app.on_event("startup")
async def startup_event():
    """应用启动 — 启动 WebSocket 心跳"""
    orchestrator.event_bus.start_heartbeat()
    logger.info("HydroScribe API 已启动")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭 — 优雅停止所有资源"""
    logger.info("收到关闭信号，正在优雅停止...")
    await orchestrator.event_bus.shutdown()
    logger.info("HydroScribe API 已关闭")


# ── 请求模型 ──────────────────────────────────────────────────

class StartTaskRequest(BaseModel):
    book_id: str
    skill_type: str = "BK"
    gate_mode: str = "auto"


class GateRequest(BaseModel):
    reason: str = ""


# ── REST API ──────────────────────────────────────────────────

@app.get("/api/status")
async def get_status():
    """系统状态"""
    return {
        "status": "running",
        "version": "0.2.0",
        "books_root": BOOKS_ROOT,
        "skill_types": [s.value for s in SkillType],
        "orchestrator": orchestrator.get_status(),
    }


@app.get("/api/books")
async def list_books():
    """列出所有书目及进度"""
    books = []
    progress_dir = os.path.join(BOOKS_ROOT, "progress")
    if os.path.exists(progress_dir):
        for f in sorted(os.listdir(progress_dir)):
            if f.endswith(".json"):
                try:
                    with open(os.path.join(progress_dir, f), "r", encoding="utf-8") as fp:
                        data = json.load(fp)
                    books.append(data)
                except Exception:
                    pass
    return {"books": books}


@app.get("/api/books/{book_id}")
async def get_book(book_id: str):
    """获取单本书的详细进度"""
    progress = orchestrator._load_progress(book_id)
    return progress.model_dump()


@app.post("/api/tasks/start")
async def start_writing(req: StartTaskRequest):
    """启动写作任务"""
    if not validate_book_id(req.book_id):
        return JSONResponse(
            status_code=400,
            content={
                "error": f"未知书目: {req.book_id}",
                "valid_book_ids": sorted(BOOK_REGISTRY.keys()),
            },
        )
    asyncio.create_task(
        orchestrator.start_book(req.book_id, req.skill_type)
    )
    return {
        "status": "started",
        "book_id": req.book_id,
        "skill_type": req.skill_type,
        "gate_mode": req.gate_mode,
        "message": f"已启动 {req.book_id} 的写作任务，请通过 WebSocket 监控进度",
    }


@app.get("/api/events")
async def get_events(limit: int = 50, book_id: Optional[str] = None):
    """获取事件历史"""
    return {"events": orchestrator.event_bus.get_history(limit=limit, book_id=book_id)}


@app.get("/api/agents")
async def get_agents():
    """获取所有活跃的 Agent 状态"""
    writers = {k: {"name": v.name, "skill": v.skill_type.value} for k, v in orchestrator.writers.items()}
    reviewers = {k: {"name": v.name, "role": v.reviewer_role.value} for k, v in orchestrator.reviewers.items()}
    return {
        "writers": writers,
        "reviewers": reviewers,
        "agent_states": orchestrator.event_bus.get_agent_status_summary(),
    }


@app.get("/api/skills")
async def get_skills():
    """获取9大写作技能信息"""
    from hydroscribe.schema import SKILL_REVIEWERS, SKILL_THRESHOLDS
    skills = {}
    for skill in SkillType:
        reviewers = SKILL_REVIEWERS.get(skill, [])
        threshold = SKILL_THRESHOLDS.get(skill, {})
        skills[skill.value] = {
            "name": skill.value,
            "reviewer_count": len(reviewers),
            "reviewers": [r.value for r in reviewers],
            "threshold": threshold,
        }
    return {"skills": skills}


@app.post("/api/gate/{gate_id}/approve")
async def approve_gate(gate_id: str):
    """人工批准门控"""
    orchestrator.approve_gate(gate_id)
    await orchestrator.event_bus.publish(Event(
        type=EventType.GATE_APPROVED,
        source_agent="human",
        payload={"gate_id": gate_id},
    ))
    return {"status": "approved", "gate_id": gate_id}


@app.post("/api/gate/{gate_id}/reject")
async def reject_gate(gate_id: str, req: GateRequest):
    """人工驳回门控"""
    orchestrator.reject_gate(gate_id)
    await orchestrator.event_bus.publish(Event(
        type=EventType.GATE_REJECTED,
        source_agent="human",
        payload={"gate_id": gate_id, "reason": req.reason},
    ))
    return {"status": "rejected", "gate_id": gate_id}


@app.get("/api/gates/pending")
async def get_pending_gates():
    """获取待审批的门控列表"""
    return {"pending_gates": list(orchestrator._pending_gates.keys())}


class MasterSlaveRequest(BaseModel):
    book_id: str
    chapter_ids: list
    skill_type: str = "BK"


@app.post("/api/tasks/master-slave")
async def start_master_slave(req: MasterSlaveRequest):
    """主从模式 — 并行启动多章写作"""
    asyncio.create_task(
        orchestrator.execute_master_slave(req.book_id, req.chapter_ids, req.skill_type)
    )
    return {
        "status": "started",
        "mode": "master_slave",
        "book_id": req.book_id,
        "chapters": req.chapter_ids,
        "max_concurrent": orchestrator.config.orchestrator.max_concurrent_writers,
        "message": f"已启动 {len(req.chapter_ids)} 章并行写作",
    }


@app.get("/api/llm/usage")
async def get_llm_usage():
    """获取 LLM token 用量统计"""
    return {
        "usage": orchestrator.get_llm_usage(),
        "total_tokens": orchestrator.llm_manager.get_total_tokens(),
    }


@app.get("/api/config")
async def get_config_info():
    """获取当前配置（脱敏）"""
    cfg = orchestrator.config
    return {
        "books_root": cfg.books_root,
        "llm": {
            "provider": cfg.llm_default.provider,
            "model": cfg.llm_default.model,
            "base_url": cfg.llm_default.base_url,
            "max_tokens": cfg.llm_default.max_tokens,
            "temperature": cfg.llm_default.temperature,
            # api_key 脱敏
            "api_key_set": bool(cfg.llm_default.api_key),
        },
        "orchestrator": {
            "gate_mode": cfg.orchestrator.gate_mode,
            "coordination_mode": cfg.orchestrator.coordination_mode,
            "review_weight": cfg.orchestrator.review_weight,
            "utility_weight": cfg.orchestrator.utility_weight,
            "max_concurrent_writers": cfg.orchestrator.max_concurrent_writers,
        },
        "openclaw": {
            "enabled": cfg.openclaw_enabled,
            "gateway_url": cfg.openclaw_gateway_url if cfg.openclaw_enabled else "",
        },
    }


# ── 书目注册表 ────────────────────────────────────────────────

@app.get("/api/registry")
async def get_registry():
    """获取全部书目注册表"""
    return {
        "total_books": len(BOOK_REGISTRY),
        "books": {
            bid: {
                "title": spec["title"],
                "tier": spec["tier"],
                "tier_name": spec["tier_name"],
                "total_chapters": spec["total_chapters"],
                "target_words": spec["target_words"],
                "publisher": spec["publisher"],
                "language": spec["language"],
                "priority": spec["priority"],
                "batch": spec["batch"],
            }
            for bid, spec in BOOK_REGISTRY.items()
        },
    }


@app.get("/api/registry/{book_id}")
async def get_registry_book(book_id: str):
    """获取单本书的注册规格"""
    spec = get_book_spec(book_id)
    if not spec:
        return JSONResponse(
            status_code=404,
            content={"error": f"书目 {book_id} 不存在", "valid_book_ids": sorted(BOOK_REGISTRY.keys())},
        )
    return {"book_id": book_id, **spec}


# ── 审计日志 ──────────────────────────────────────────────────

@app.get("/api/audit")
async def get_audit_trail(limit: int = 50):
    """获取最近的审计日志"""
    audit = get_audit_logger()
    records = audit.read_recent(limit=limit)
    return {"total": len(records), "records": records}


# ── 死信队列 ──────────────────────────────────────────────────

@app.get("/api/dead-letters")
async def get_dead_letters(limit: int = 50):
    """获取事件总线死信队列（处理失败/超时的事件）"""
    entries = orchestrator.event_bus.get_dead_letters(limit=limit)
    return {"total": len(entries), "dead_letters": entries}


@app.delete("/api/dead-letters")
async def clear_dead_letters():
    """清空死信队列"""
    orchestrator.event_bus.clear_dead_letters()
    return {"status": "cleared"}


# ── 健康检查与监控 ────────────────────────────────────────────

@app.get("/health")
async def health_check():
    """健康检查 — 适配 Docker HEALTHCHECK / K8s liveness probe"""
    uptime_seconds = int(time.monotonic() - _start_time)

    # 检查文件系统可写性
    fs_ok = True
    try:
        test_path = os.path.join(orchestrator.books_root, ".health_check")
        with open(test_path, "w") as f:
            f.write("ok")
        os.unlink(test_path)
    except Exception:
        fs_ok = False

    # 检查事件总线
    event_bus_ok = orchestrator.event_bus is not None

    all_ok = fs_ok and event_bus_ok
    return {
        "status": "healthy" if all_ok else "degraded",
        "version": "0.3.0",
        "uptime_seconds": uptime_seconds,
        "checks": {
            "filesystem": "ok" if fs_ok else "error",
            "event_bus": "ok" if event_bus_ok else "error",
        },
    }


@app.get("/ready")
async def readiness_check():
    """就绪探针 — K8s readiness probe / 负载均衡器健康检查

    与 /health 区别: /health 检查进程存活，/ready 检查能否接受新任务
    """
    # 基本存活
    uptime_seconds = int(time.monotonic() - _start_time)

    # LLM 可用性 (检查是否有至少一个已配置的 provider)
    llm_configured = len(orchestrator.llm_manager._clients) > 0

    # 活跃任务是否过载
    max_tasks = orchestrator.config.orchestrator.max_concurrent_writers
    active_count = len(orchestrator.active_tasks)
    tasks_ok = active_count < max_tasks

    ready = llm_configured and tasks_ok

    return {
        "ready": ready,
        "uptime_seconds": uptime_seconds,
        "checks": {
            "llm_configured": llm_configured,
            "tasks_capacity": f"{active_count}/{max_tasks}",
            "accepting_tasks": tasks_ok,
        },
    }


@app.get("/api/metrics")
async def get_metrics():
    """系统指标 — 供监控面板使用"""
    uptime_seconds = int(time.monotonic() - _start_time)

    # LLM 用量
    llm_usage = orchestrator.get_llm_usage()
    total_tokens = orchestrator.llm_manager.get_total_tokens()

    # Agent 统计
    active_writers = len(orchestrator.writers)
    active_reviewers = len(orchestrator.reviewers)
    active_tasks = len(orchestrator.active_tasks)
    pending_gates = len(orchestrator._pending_gates)

    # 事件统计
    event_count = len(orchestrator.event_bus._history)
    ws_connections = len(orchestrator.event_bus._ws_connections)

    return {
        "uptime_seconds": uptime_seconds,
        "agents": {
            "writers_active": active_writers,
            "reviewers_active": active_reviewers,
            "tasks_active": active_tasks,
            "gates_pending": pending_gates,
        },
        "llm": {
            "total_tokens": total_tokens,
            "usage_by_role": {
                role: {
                    "prompt_tokens": u.get("prompt_tokens", 0),
                    "completion_tokens": u.get("completion_tokens", 0),
                    "total_tokens": u.get("total_tokens", 0),
                }
                for role, u in llm_usage.items()
            },
        },
        "events": {
            "total_count": event_count,
            "ws_connections": ws_connections,
        },
        "circuit_breakers": orchestrator.llm_manager.get_circuit_breaker_stats(),
        "llm_latency": orchestrator.llm_manager.get_latency_stats(),
        "task_stats": orchestrator.get_task_stats(),
        "coordination_mode": orchestrator.coordination_mode,
    }


# ── WebSocket 实时推送 ────────────────────────────────────────

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket 端点 — 实时推送所有事件到前端"""
    await websocket.accept()
    orchestrator.event_bus.register_ws(websocket)
    logger.info("WebSocket 客户端已连接")

    try:
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
            elif data.startswith("{"):
                try:
                    cmd = json.loads(data)
                    action = cmd.get("action")
                    if action == "start":
                        asyncio.create_task(
                            orchestrator.start_book(
                                cmd.get("book_id", "T1-CN"),
                                cmd.get("skill_type", "BK"),
                            )
                        )
                    elif action == "approve":
                        orchestrator.approve_gate(cmd.get("gate_id", ""))
                    elif action == "reject":
                        orchestrator.reject_gate(cmd.get("gate_id", ""))
                except json.JSONDecodeError:
                    pass
    except WebSocketDisconnect:
        orchestrator.event_bus.unregister_ws(websocket)
        logger.info("WebSocket 客户端已断开")
    except Exception as e:
        orchestrator.event_bus.unregister_ws(websocket)
        logger.warning(f"WebSocket 异常断开: {e}")


# ── 前端页面 ──────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    """主页 — 单页面实时仪表盘"""
    html_path = os.path.join(os.path.dirname(__file__), "..", "static", "index.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>HydroScribe Dashboard</h1><p>static/index.html not found</p>"
