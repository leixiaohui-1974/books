"""
Phase 12 测试 — 审计集成 + API 注册表/审计端点 + 死信队列 + 速率限制
"""

import asyncio
import json
import os
import tempfile
import time

import pytest

from hydroscribe.engine.event_bus import EventBus
from hydroscribe.schema import Event, EventType


# ── 死信队列测试 ──────────────────────────────────────────────

class TestDeadLetterQueue:
    """测试 EventBus 死信队列功能"""

    def test_initial_empty(self):
        bus = EventBus()
        assert bus.get_dead_letters() == []

    @pytest.mark.asyncio
    async def test_timeout_handler_enters_dead_letter(self):
        """超时的处理器应进入死信队列"""
        bus = EventBus()

        async def slow_handler(event):
            await asyncio.sleep(10)

        bus.subscribe(EventType.TASK_CREATED, slow_handler)

        event = Event(
            type=EventType.TASK_CREATED,
            source_agent="test",
            payload={"test": True},
        )
        await bus.publish(event, handler_timeout=0.05)

        dead = bus.get_dead_letters()
        assert len(dead) == 1
        assert dead[0]["reason"] == "timeout"
        assert dead[0]["handler"] == "slow_handler"
        assert dead[0]["event_type"] == "task.created"

    @pytest.mark.asyncio
    async def test_error_handler_enters_dead_letter(self):
        """异常的处理器应进入死信队列"""
        bus = EventBus()

        def bad_handler(event):
            raise ValueError("test error")

        bus.subscribe(EventType.TASK_CREATED, bad_handler)

        event = Event(
            type=EventType.TASK_CREATED,
            source_agent="test",
            payload={},
        )
        await bus.publish(event, handler_timeout=5.0)

        dead = bus.get_dead_letters()
        assert len(dead) == 1
        assert dead[0]["reason"] == "error"
        assert "test error" in dead[0]["detail"]

    @pytest.mark.asyncio
    async def test_successful_handler_no_dead_letter(self):
        """成功的处理器不应进入死信队列"""
        bus = EventBus()
        calls = []

        def good_handler(event):
            calls.append(1)

        bus.subscribe(EventType.TASK_CREATED, good_handler)

        event = Event(type=EventType.TASK_CREATED, source_agent="test", payload={})
        await bus.publish(event)

        assert len(calls) == 1
        assert bus.get_dead_letters() == []

    def test_dead_letter_limit(self):
        """死信队列应遵守最大容量限制"""
        bus = EventBus(max_dead_letters=5)
        for i in range(10):
            bus._record_dead_letter(
                Event(type=EventType.TASK_CREATED, source_agent="test", payload={}),
                f"handler_{i}", "error", f"err_{i}"
            )
        assert len(bus.get_dead_letters()) == 5
        # 保留的是最近5条
        assert bus.get_dead_letters()[0]["handler"] == "handler_5"

    def test_clear_dead_letters(self):
        bus = EventBus()
        bus._record_dead_letter(
            Event(type=EventType.TASK_CREATED, source_agent="test", payload={}),
            "h", "error", "e"
        )
        assert len(bus.get_dead_letters()) == 1
        bus.clear_dead_letters()
        assert bus.get_dead_letters() == []

    def test_dead_letter_fields(self):
        """死信记录应包含完整字段"""
        bus = EventBus()
        event = Event(
            type=EventType.CHAPTER_COMPLETED,
            source_agent="orch",
            book_id="T1-CN",
            chapter_id="ch01",
            payload={"score": 9.0},
        )
        bus._record_dead_letter(event, "my_handler", "error", "some detail")
        dl = bus.get_dead_letters()[0]
        assert dl["event_id"] == event.id
        assert dl["event_type"] == "chapter.completed"
        assert dl["handler"] == "my_handler"
        assert dl["reason"] == "error"
        assert dl["detail"] == "some detail"
        assert dl["book_id"] == "T1-CN"
        assert dl["chapter_id"] == "ch01"
        assert "timestamp" in dl


# ── 速率限制测试 ─────────────────────────────────────────────

class TestRateLimitMiddleware:
    """测试速率限制中间件（源码验证，避免触发 OpenManus 导入链）"""

    def test_rate_limiter_in_source(self):
        """app.py 应包含 RateLimitMiddleware 定义"""
        app_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "api", "app.py"
        )
        with open(app_path, "r") as f:
            source = f.read()
        assert "class RateLimitMiddleware" in source
        assert "max_requests" in source
        assert "429" in source  # HTTP 429 Too Many Requests

    def test_rate_limiter_exempts_health(self):
        """速率限制应豁免 /health 和 /ready"""
        app_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "api", "app.py"
        )
        with open(app_path, "r") as f:
            source = f.read()
        assert '"/health"' in source
        assert '"/ready"' in source
        assert '"/ws"' in source

    def test_rate_limiter_wired_to_app(self):
        """速率限制中间件应被注册到 FastAPI app"""
        app_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "api", "app.py"
        )
        with open(app_path, "r") as f:
            source = f.read()
        assert "app.add_middleware(RateLimitMiddleware" in source


# ── 书目注册表 API 端点测试 ───────────────────────────────────

class TestBookRegistryAPI:
    """测试 /api/registry 端点的数据完整性"""

    def test_registry_data_structure(self):
        """注册表数据结构应正确"""
        from hydroscribe.engine.book_registry import BOOK_REGISTRY
        for bid, spec in BOOK_REGISTRY.items():
            assert isinstance(spec["title"], str)
            assert isinstance(spec["tier"], int)
            assert isinstance(spec["total_chapters"], int)
            assert isinstance(spec["target_words"], int)
            assert spec["target_words"] > 0

    def test_validate_rejects_bad_id(self):
        from hydroscribe.engine.book_registry import validate_book_id
        assert validate_book_id("FAKE-BOOK") is False

    def test_validate_accepts_good_id(self):
        from hydroscribe.engine.book_registry import validate_book_id
        assert validate_book_id("T1-CN") is True
        assert validate_book_id("M8") is True

    def test_api_registry_endpoint_defined(self):
        """app.py 应包含 /api/registry 端点"""
        app_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "api", "app.py"
        )
        with open(app_path, "r") as f:
            source = f.read()
        assert '"/api/registry"' in source
        assert '"/api/registry/{book_id}"' in source

    def test_api_validates_book_id_on_start(self):
        """app.py 的 /api/tasks/start 应校验 book_id"""
        app_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "api", "app.py"
        )
        with open(app_path, "r") as f:
            source = f.read()
        assert "validate_book_id" in source


# ── 审计日志集成测试 ─────────────────────────────────────────

class TestAuditIntegration:
    """测试审计日志与编排器的集成"""

    def test_audit_logger_creates_file(self):
        """审计日志应创建 JSONL 文件"""
        with tempfile.TemporaryDirectory() as tmpdir:
            from hydroscribe.engine.audit_log import AuditLogger
            al = AuditLogger(log_dir=tmpdir)
            al.log_writing_started("T1-CN", "ch01")
            al.log_writing_completed("T1-CN", "ch01", word_count=15000, iterations=3)
            al.log_review_passed("T1-CN", "ch01", scores={"instructor": 8.5})
            al.log_review_rejected("T2a", "ch07", scores={"expert": 5.0})

            records = al.read_recent(limit=10)
            assert len(records) == 4

            events = [r["event"] for r in records]
            assert "writing_started" in events
            assert "writing_completed" in events
            assert "review_passed" in events
            assert "review_rejected" in events

    def test_audit_record_contains_details(self):
        """审计记录应包含完整的详情"""
        with tempfile.TemporaryDirectory() as tmpdir:
            from hydroscribe.engine.audit_log import AuditLogger
            al = AuditLogger(log_dir=tmpdir)
            al.log_writing_completed("M1", "ch03", word_count=25000, iterations=5)

            records = al.read_recent()
            r = records[0]
            assert r["book_id"] == "M1"
            assert r["chapter_id"] == "ch03"
            assert r["details"]["word_count"] == 25000
            assert r["details"]["iterations"] == 5


# ── 编排器审计集成验证（源码检查，避免 OpenManus 导入链）────

class TestOrchestratorAuditWiring:
    """验证 orchestrator 正确导入并使用审计日志"""

    def _read_orchestrator_source(self):
        orch_path = os.path.join(
            os.path.dirname(__file__), "..",
            "hydroscribe", "engine", "orchestrator.py"
        )
        with open(orch_path, "r") as f:
            return f.read()

    def test_orchestrator_imports_audit(self):
        """Orchestrator 应导入 get_audit_logger"""
        source = self._read_orchestrator_source()
        assert "from hydroscribe.engine.audit_log import get_audit_logger" in source

    def test_orchestrator_calls_audit_methods(self):
        """Orchestrator 应在关键路径调用审计方法"""
        source = self._read_orchestrator_source()
        assert "self._audit.log_writing_started" in source
        assert "self._audit.log_writing_completed" in source
        assert "self._audit.log_writing_failed" in source
        assert "self._audit.log_review_passed" in source
        assert "self._audit.log_review_rejected" in source
        assert "self._audit.log_checkpoint_saved" in source

    def test_orchestrator_creates_audit_instance(self):
        """Orchestrator.__init__ 应创建 _audit 实例"""
        source = self._read_orchestrator_source()
        assert "self._audit = get_audit_logger()" in source


# ── EventBus 死信 + 正常事件隔离测试 ─────────────────────────

class TestEventBusIsolation:
    """确认死信队列不影响正常事件处理"""

    @pytest.mark.asyncio
    async def test_bad_handler_does_not_block_good_handler(self):
        """一个失败的处理器不应阻止其他处理器执行"""
        bus = EventBus()
        results = []

        def bad_handler(event):
            raise RuntimeError("boom")

        def good_handler(event):
            results.append("ok")

        bus.subscribe(EventType.TASK_CREATED, bad_handler)
        bus.subscribe(EventType.TASK_CREATED, good_handler)

        event = Event(type=EventType.TASK_CREATED, source_agent="test", payload={})
        await bus.publish(event)

        assert results == ["ok"]
        assert len(bus.get_dead_letters()) == 1

    @pytest.mark.asyncio
    async def test_dead_letter_preserves_event_history(self):
        """死信事件仍应出现在正常事件历史中"""
        bus = EventBus()

        def bad_handler(event):
            raise RuntimeError("boom")

        bus.subscribe(EventType.TASK_CREATED, bad_handler)

        event = Event(type=EventType.TASK_CREATED, source_agent="test", payload={})
        await bus.publish(event)

        history = bus.get_history()
        assert len(history) == 1
        assert history[0]["type"] == "task.created"


# ── API 新端点源码验证 ───────────────────────────────────────

class TestAPINewEndpoints:
    """验证 app.py 包含所有 Phase 12 新端点"""

    def _read_app_source(self):
        app_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "api", "app.py"
        )
        with open(app_path, "r") as f:
            return f.read()

    def test_audit_endpoint(self):
        source = self._read_app_source()
        assert '"/api/audit"' in source

    def test_dead_letters_endpoint(self):
        source = self._read_app_source()
        assert '"/api/dead-letters"' in source

    def test_book_id_validation_on_task_start(self):
        """POST /api/tasks/start 应返回 400 for unknown book_id"""
        source = self._read_app_source()
        assert "INVALID_BOOK_ID" in source
        assert "validate_book_id" in source
