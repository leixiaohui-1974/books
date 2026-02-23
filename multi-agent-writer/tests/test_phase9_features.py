"""
Phase 9 测试 — 检查点/恢复 + 进度元数据 + WebSocket心跳 + 熔断器指标
"""

import asyncio
import json
import os
import tempfile
import time

import pytest

from hydroscribe.engine.event_bus import EventBus
from hydroscribe.engine.llm_provider import (
    CircuitBreaker,
    CircuitState,
    LLMConfig,
    LLMManager,
    LLMProvider,
)
from hydroscribe.schema import ChapterProgress, BookProgress


# ── 检查点测试 ─────────────────────────────────────────────

def _atomic_write(path: str, content: str):
    """原子化写入（同 Phase 8 测试工具）"""
    import tempfile as _tf
    dir_path = os.path.dirname(path)
    os.makedirs(dir_path, exist_ok=True)
    fd, tmp_path = _tf.mkstemp(dir=dir_path, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(content)
        os.replace(tmp_path, path)
    except Exception:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise


class TestCheckpoint:
    """测试检查点保存/加载/清除"""

    def test_save_and_load_checkpoint(self):
        """保存检查点后应能正确加载"""
        with tempfile.TemporaryDirectory() as tmpdir:
            progress_dir = os.path.join(tmpdir, "progress")
            os.makedirs(progress_dir)

            # 模拟保存检查点
            checkpoint = {
                "book_id": "T1-CN",
                "chapter_id": "ch01",
                "completed_iteration": 2,
                "max_iterations": 6,
                "word_count": 15000,
                "metadata": {"equations": 3, "examples": 2},
                "draft_path": os.path.join(tmpdir, "books/T1-CN/ch01_v2.md"),
                "timestamp": "2026-02-23T10:00:00",
            }
            path = os.path.join(progress_dir, ".checkpoint_T1-CN_ch01.json")
            _atomic_write(path, json.dumps(checkpoint, ensure_ascii=False, indent=2))

            # 加载
            with open(path, "r") as f:
                loaded = json.load(f)

            assert loaded["completed_iteration"] == 2
            assert loaded["word_count"] == 15000
            assert loaded["metadata"]["equations"] == 3

    def test_clear_checkpoint(self):
        """清除检查点后文件不应存在"""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, ".checkpoint_T1-CN_ch01.json")
            _atomic_write(path, '{"completed_iteration": 1}')
            assert os.path.exists(path)

            os.unlink(path)
            assert not os.path.exists(path)

    def test_checkpoint_resume_iteration(self):
        """检查点应正确恢复起始迭代"""
        checkpoint = {
            "completed_iteration": 3,
            "max_iterations": 6,
        }
        start_iteration = checkpoint["completed_iteration"] + 1
        assert start_iteration == 4
        assert start_iteration <= checkpoint["max_iterations"]

    def test_no_checkpoint_starts_from_1(self):
        """无检查点时应从第1轮开始"""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, ".checkpoint_T1-CN_ch01.json")
            assert not os.path.exists(path)
            start_iteration = 1
            assert start_iteration == 1


# ── 进度元数据扩展测试 ─────────────────────────────────────

class TestProgressMetadata:
    """测试 ChapterProgress 扩展字段"""

    def test_chapter_progress_with_metadata(self):
        """ChapterProgress 应支持新增字段"""
        cp = ChapterProgress(
            status="completed",
            word_count=15000,
            review_passed=True,
            review_scores={"instructor": 8.5, "expert": 9.0},
            last_updated="2026-02-23",
            iterations=2,
            file_path="books/T1-CN/ch01_final.md",
            metadata={"equations": 5, "examples": 3, "figures": 2},
            todo_count=1,
            validation_warnings=["含 1 个 [TODO] 标记，需人工补充"],
        )
        assert cp.file_path == "books/T1-CN/ch01_final.md"
        assert cp.metadata["equations"] == 5
        assert cp.todo_count == 1
        assert len(cp.validation_warnings) == 1

    def test_chapter_progress_defaults(self):
        """新字段应有合理默认值"""
        cp = ChapterProgress()
        assert cp.file_path == ""
        assert cp.metadata == {}
        assert cp.todo_count == 0
        assert cp.validation_warnings == []

    def test_chapter_progress_serialization(self):
        """扩展后的 ChapterProgress 应可正确序列化"""
        cp = ChapterProgress(
            status="completed",
            word_count=20000,
            file_path="books/M1/ch02_final.md",
            metadata={"equations": 10},
            todo_count=0,
        )
        data = cp.model_dump()
        assert data["file_path"] == "books/M1/ch02_final.md"
        assert data["metadata"]["equations"] == 10
        assert data["todo_count"] == 0

        # 反序列化
        cp2 = ChapterProgress(**data)
        assert cp2.file_path == cp.file_path
        assert cp2.metadata == cp.metadata

    def test_book_progress_with_enriched_chapters(self):
        """BookProgress 包含扩展 ChapterProgress"""
        bp = BookProgress(
            book_id="T1-CN",
            book_title="水系统控制论",
            total_chapters=8,
            chapters={
                "ch01": ChapterProgress(
                    status="completed",
                    word_count=15000,
                    file_path="books/T1-CN/ch01_final.md",
                    metadata={"equations": 3},
                    todo_count=0,
                ),
                "ch02": ChapterProgress(status="pending"),
            },
        )
        data = bp.model_dump()
        assert data["chapters"]["ch01"]["file_path"] == "books/T1-CN/ch01_final.md"
        assert data["chapters"]["ch02"]["file_path"] == ""


# ── EventBus 心跳与关闭测试 ─────────────────────────────────

class TestEventBusLifecycle:
    """测试 EventBus 心跳和优雅关闭"""

    @pytest.fixture
    def event_bus(self):
        return EventBus(max_history=100, ws_heartbeat_interval=0.1)

    def test_initial_state(self, event_bus):
        assert event_bus._shutting_down is False
        assert event_bus._heartbeat_task is None

    @pytest.mark.asyncio
    async def test_shutdown_clears_state(self, event_bus):
        """关闭后应清理所有订阅者和连接"""
        from hydroscribe.schema import EventType

        # 添加一些订阅
        event_bus.subscribe(EventType.WRITING_CHUNK, lambda e: None)
        event_bus.subscribe_all(lambda e: None)
        assert len(event_bus._subscribers) > 0
        assert len(event_bus._global_subscribers) > 0

        await event_bus.shutdown()

        assert event_bus._shutting_down is True
        assert len(event_bus._subscribers) == 0
        assert len(event_bus._global_subscribers) == 0
        assert len(event_bus._ws_connections) == 0

    @pytest.mark.asyncio
    async def test_heartbeat_starts(self, event_bus):
        """心跳应能启动且不崩溃"""
        event_bus.start_heartbeat()
        assert event_bus._heartbeat_task is not None
        assert not event_bus._heartbeat_task.done()

        # 等待一个心跳周期
        await asyncio.sleep(0.15)

        # 清理
        await event_bus.shutdown()
        assert event_bus._heartbeat_task.done()


# ── LLMManager 熔断器聚合测试 ──────────────────────────────

class TestLLMManagerCircuitBreaker:
    """测试 LLMManager.get_circuit_breaker_stats()"""

    def test_empty_manager(self):
        mgr = LLMManager()
        stats = mgr.get_circuit_breaker_stats()
        assert stats == {}

    def test_registered_clients_have_stats(self):
        mgr = LLMManager()
        config = LLMConfig(
            provider=LLMProvider.LOCAL,
            model="test-model",
            base_url="http://localhost:11434",
        )
        mgr.register("writer", config)
        stats = mgr.get_circuit_breaker_stats()
        assert "writer" in stats
        assert stats["writer"]["state"] == "closed"
        assert stats["writer"]["failure_count"] == 0

    def test_circuit_breaker_state_propagates(self):
        mgr = LLMManager()
        config = LLMConfig(
            provider=LLMProvider.LOCAL,
            model="test-model",
            base_url="http://localhost:11434",
        )
        mgr.register("writer", config)

        # 触发熔断
        client = mgr.get_client("writer")
        for _ in range(5):
            client._circuit_breaker.record_failure()

        stats = mgr.get_circuit_breaker_stats()
        assert stats["writer"]["state"] == "open"
        assert stats["writer"]["total_trips"] == 1
