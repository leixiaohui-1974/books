"""
HydroScribe Web API — FastAPI + WebSocket 实时推送
"""

import asyncio
import json
import logging
import os
from typing import Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from hydroscribe.engine.orchestrator import Orchestrator
from hydroscribe.engine.event_bus import EventBus
from hydroscribe.schema import EventType

logger = logging.getLogger("hydroscribe.api")

# ── 初始化 ────────────────────────────────────────────────────

BOOKS_ROOT = os.environ.get("BOOKS_ROOT", "/home/user/books")

app = FastAPI(
    title="HydroScribe — CHS 多智能体协同写作助手",
    description="基于 OpenManus 架构，融合 9 大写作技能的多智能体系统",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = Orchestrator(books_root=BOOKS_ROOT)


# ── REST API ──────────────────────────────────────────────────

@app.get("/api/status")
async def get_status():
    """系统状态"""
    return {
        "status": "running",
        "version": "0.1.0",
        "books_root": BOOKS_ROOT,
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
async def start_writing(book_id: str, skill_type: str = "BK"):
    """启动写作任务"""
    # 后台执行，不阻塞 API
    task = asyncio.create_task(orchestrator.start_book(book_id, skill_type))
    return {
        "status": "started",
        "book_id": book_id,
        "skill_type": skill_type,
        "message": f"已启动 {book_id} 的写作任务，请通过 WebSocket 监控进度",
    }


@app.get("/api/events")
async def get_events(limit: int = 50, book_id: Optional[str] = None):
    """获取事件历史"""
    return {"events": orchestrator.event_bus.get_history(limit=limit, book_id=book_id)}


@app.post("/api/gate/{task_id}/approve")
async def approve_gate(task_id: str):
    """人工批准门控"""
    await orchestrator.event_bus.publish(
        __import__("hydroscribe.schema", fromlist=["Event"]).Event(
            type=EventType.GATE_APPROVED,
            source_agent="human",
            payload={"task_id": task_id},
        )
    )
    return {"status": "approved"}


@app.post("/api/gate/{task_id}/reject")
async def reject_gate(task_id: str, reason: str = ""):
    """人工驳回门控"""
    await orchestrator.event_bus.publish(
        __import__("hydroscribe.schema", fromlist=["Event"]).Event(
            type=EventType.GATE_REJECTED,
            source_agent="human",
            payload={"task_id": task_id, "reason": reason},
        )
    )
    return {"status": "rejected"}


# ── WebSocket 实时推送 ────────────────────────────────────────

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket 端点 — 实时推送所有事件到前端"""
    await websocket.accept()
    orchestrator.event_bus.register_ws(websocket)
    logger.info("WebSocket 客户端已连接")

    try:
        while True:
            # 保持连接（接收客户端心跳或指令）
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        orchestrator.event_bus.unregister_ws(websocket)
        logger.info("WebSocket 客户端已断开")


# ── 前端页面 ──────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    """主页 — 单页面实时仪表盘"""
    html_path = os.path.join(os.path.dirname(__file__), "..", "static", "index.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>HydroScribe Dashboard</h1><p>static/index.html not found</p>"
