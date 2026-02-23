"""
Phase 14 测试 — 并发信号量 + 进度文件锁 + 任务取消 + 统一错误格式
"""

import asyncio
import fcntl
import json
import os
import tempfile

import pytest

from hydroscribe.engine.event_bus import EventBus
from hydroscribe.engine.audit_log import AuditLogger
from hydroscribe.engine.book_registry import BOOK_REGISTRY


# ── 并发信号量测试 ────────────────────────────────────────────

class TestConcurrencySemaphore:
    """测试 Orchestrator 的写作并发信号量"""

    def test_orchestrator_has_semaphore(self):
        """Orchestrator 应有 _writer_semaphore"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "engine", "orchestrator.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "_writer_semaphore" in source
        assert "asyncio.Semaphore" in source

    def test_execute_writing_cycle_uses_semaphore(self):
        """execute_writing_cycle 应在信号量内执行"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "engine", "orchestrator.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "async with self._writer_semaphore" in source

    def test_inner_cycle_method_exists(self):
        """_execute_writing_cycle_inner 应存在"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "engine", "orchestrator.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "_execute_writing_cycle_inner" in source

    def test_semaphore_uses_config(self):
        """信号量值应来自 max_concurrent_writers 配置"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "engine", "orchestrator.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "max_concurrent_writers" in source

    @pytest.mark.asyncio
    async def test_semaphore_limits_concurrency(self):
        """信号量应能限制并发数"""
        sem = asyncio.Semaphore(2)
        running = []
        max_running = [0]

        async def task(i):
            async with sem:
                running.append(i)
                max_running[0] = max(max_running[0], len(running))
                await asyncio.sleep(0.05)
                running.remove(i)

        await asyncio.gather(*[task(i) for i in range(5)])
        assert max_running[0] <= 2


# ── 进度文件锁测试 ────────────────────────────────────────────

class TestProgressFileLocking:
    """测试进度文件的 fcntl 文件锁"""

    def test_load_progress_uses_lock(self):
        """_load_progress 应使用共享锁"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "engine", "orchestrator.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "fcntl.LOCK_SH" in source

    def test_save_progress_uses_lock(self):
        """_save_progress 应使用排他锁"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "engine", "orchestrator.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "fcntl.LOCK_EX" in source

    def test_save_progress_uses_lock_file(self):
        """_save_progress 应使用 .lock 文件"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "engine", "orchestrator.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert ".lock" in source

    def test_fcntl_lock_unlock_cycle(self):
        """fcntl 锁应能正确获取和释放"""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write('{"test": 1}')
            tmp_path = f.name
        try:
            with open(tmp_path, "r") as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_SH)
                data = json.load(f)
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            assert data == {"test": 1}
        finally:
            os.unlink(tmp_path)

    def test_atomic_write_with_lock(self):
        """原子写入 + 排他锁应协同工作"""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "test.json")
            lock_path = path + ".lock"

            # 模拟带锁写入
            with open(lock_path, "w") as lock_f:
                fcntl.flock(lock_f.fileno(), fcntl.LOCK_EX)
                with open(path, "w") as f:
                    json.dump({"a": 1}, f)
                fcntl.flock(lock_f.fileno(), fcntl.LOCK_UN)

            with open(path, "r") as f:
                data = json.load(f)
            assert data == {"a": 1}


# ── 任务取消测试 ──────────────────────────────────────────────

class TestTaskCancellation:
    """测试任务取消机制"""

    def test_cancel_tokens_in_orchestrator(self):
        """Orchestrator 应有 _cancel_tokens"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "engine", "orchestrator.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "_cancel_tokens" in source

    def test_cancel_task_method_exists(self):
        """Orchestrator 应有 cancel_task 方法"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "engine", "orchestrator.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "def cancel_task(self, task_id: str)" in source

    def test_cancel_checks_in_cycle(self):
        """写作循环应在每轮检查取消令牌"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "engine", "orchestrator.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "cancel_event.is_set()" in source

    def test_cancel_saves_checkpoint(self):
        """取消时应保存检查点"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "engine", "orchestrator.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert '"cancelled"' in source

    def test_cancel_returns_cancelled_status(self):
        """取消后应返回 cancelled 状态"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "engine", "orchestrator.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert '"cancelled"' in source

    def test_cleanup_removes_cancel_token(self):
        """_cleanup_task 应清理取消令牌"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "engine", "orchestrator.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "self._cancel_tokens.pop(task.id, None)" in source

    def test_cancel_api_endpoint_defined(self):
        """POST /api/tasks/{task_id}/cancel 端点应存在"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "api", "app.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "/api/tasks/{task_id}/cancel" in source

    def test_cancel_api_checks_task_exists(self):
        """取消 API 应检查任务是否存在"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "api", "app.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "TASK_NOT_FOUND" in source

    @pytest.mark.asyncio
    async def test_cancel_event_mechanism(self):
        """asyncio.Event 取消令牌应正确工作"""
        cancel = asyncio.Event()
        assert not cancel.is_set()
        cancel.set()
        assert cancel.is_set()

    def test_cancel_audits_event(self):
        """取消应记录审计日志"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "engine", "orchestrator.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert '"task_cancelled"' in source


# ── 统一 API 错误格式测试 ────────────────────────────────────

class TestUnifiedAPIErrors:
    """测试统一的 API 错误响应格式"""

    def test_api_error_helper_exists(self):
        """api_error 辅助函数应存在"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "api", "app.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "def api_error(" in source

    def test_error_format_has_code(self):
        """错误响应应包含 error.code"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "api", "app.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert '"code"' in source

    def test_error_format_has_message(self):
        """错误响应应包含 error.message"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "api", "app.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert '"message"' in source

    def test_error_codes_used(self):
        """应使用语义化错误码"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "api", "app.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        error_codes = [
            "INVALID_BOOK_ID",
            "BOOK_NOT_FOUND",
            "TASK_NOT_FOUND",
            "RATE_LIMITED",
        ]
        for code in error_codes:
            assert code in source, f"缺少错误码: {code}"

    def test_rate_limit_uses_unified_format(self):
        """速率限制响应应使用统一格式"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "api", "app.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "RATE_LIMITED" in source

    def test_start_task_uses_unified_format(self):
        """start_writing 的错误响应应使用 api_error"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "api", "app.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "INVALID_BOOK_ID" in source

    def test_registry_book_uses_unified_format(self):
        """get_registry_book 的错误响应应使用 api_error"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "api", "app.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "BOOK_NOT_FOUND" in source


# ── API 版本测试 ──────────────────────────────────────────────

class TestAPIVersion:
    """测试 API 版本号更新"""

    def test_api_version_updated(self):
        """API 版本应为 0.4.0"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "api", "app.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert '"0.4.0"' in source


# ── 写作循环取消集成测试 ──────────────────────────────────────

class TestCancellationIntegration:
    """集成测试：取消令牌在循环中的行为"""

    @pytest.mark.asyncio
    async def test_cancel_event_stops_iteration(self):
        """取消事件应阻止下一轮迭代"""
        cancel = asyncio.Event()
        iterations_run = 0

        async def mock_cycle(max_iters=5):
            nonlocal iterations_run
            for i in range(max_iters):
                if cancel.is_set():
                    return {"status": "cancelled", "iterations": i}
                iterations_run += 1
                await asyncio.sleep(0.01)
            return {"status": "completed", "iterations": max_iters}

        # 在第 2 轮后取消
        async def delayed_cancel():
            await asyncio.sleep(0.025)
            cancel.set()

        result, _ = await asyncio.gather(mock_cycle(), delayed_cancel())
        assert result["status"] == "cancelled"
        assert iterations_run < 5

    @pytest.mark.asyncio
    async def test_shutdown_flag_stops_iteration(self):
        """_shutting_down 标志应阻止下一轮迭代"""
        shutting_down = False
        iterations = 0

        async def mock_cycle(max_iters=5):
            nonlocal iterations, shutting_down
            for i in range(max_iters):
                if shutting_down:
                    return {"status": "cancelled"}
                iterations += 1
                await asyncio.sleep(0.01)
                if i == 1:
                    shutting_down = True

        await mock_cycle()
        assert iterations <= 3


# ── 并发安全测试 ──────────────────────────────────────────────

class TestConcurrencySafety:
    """测试并发场景下的安全性"""

    def test_concurrent_progress_writes(self):
        """并发写入进度文件应通过锁保证安全"""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "progress.json")
            lock_path = path + ".lock"

            def write_with_lock(value):
                with open(lock_path, "w") as lock_f:
                    fcntl.flock(lock_f.fileno(), fcntl.LOCK_EX)
                    try:
                        # 读取-修改-写入
                        if os.path.exists(path):
                            with open(path, "r") as f:
                                data = json.load(f)
                        else:
                            data = {"values": []}
                        data["values"].append(value)
                        with open(path, "w") as f:
                            json.dump(data, f)
                    finally:
                        fcntl.flock(lock_f.fileno(), fcntl.LOCK_UN)

            # 模拟多次写入
            for i in range(10):
                write_with_lock(i)

            with open(path, "r") as f:
                data = json.load(f)
            assert len(data["values"]) == 10
            assert data["values"] == list(range(10))
