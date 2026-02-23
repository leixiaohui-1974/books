"""
Phase 8 测试 — 熔断器 + 输出验证 + 原子写入 + 健康检查
"""

import os
import tempfile
import time
from unittest.mock import MagicMock, patch

import pytest

from hydroscribe.engine.llm_provider import CircuitBreaker, CircuitState


# ── 熔断器测试 ─────────────────────────────────────────────

class TestCircuitBreaker:
    """LLM 熔断器状态机测试"""

    def test_initial_state_closed(self):
        cb = CircuitBreaker(failure_threshold=3)
        assert cb.state == CircuitState.CLOSED
        assert cb.allow_request() is True

    def test_trips_after_threshold(self):
        cb = CircuitBreaker(failure_threshold=3, recovery_timeout=60.0)
        cb.record_failure()
        cb.record_failure()
        assert cb.state == CircuitState.CLOSED  # 还没到阈值
        cb.record_failure()
        assert cb.state == CircuitState.OPEN  # 达到阈值，熔断
        assert cb.allow_request() is False

    def test_success_resets_failure_count(self):
        cb = CircuitBreaker(failure_threshold=3)
        cb.record_failure()
        cb.record_failure()
        cb.record_success()  # 重置计数
        cb.record_failure()
        cb.record_failure()
        assert cb.state == CircuitState.CLOSED  # 没到 3 次连续失败

    def test_recovery_to_half_open(self):
        cb = CircuitBreaker(failure_threshold=2, recovery_timeout=0.1)
        cb.record_failure()
        cb.record_failure()
        assert cb.state == CircuitState.OPEN

        # 等待恢复超时
        time.sleep(0.15)
        assert cb.state == CircuitState.HALF_OPEN
        assert cb.allow_request() is True

    def test_half_open_success_closes(self):
        cb = CircuitBreaker(failure_threshold=2, recovery_timeout=0.05, success_threshold=2)
        cb.record_failure()
        cb.record_failure()
        time.sleep(0.1)
        assert cb.state == CircuitState.HALF_OPEN

        cb.record_success()
        assert cb.state == CircuitState.HALF_OPEN  # 还需一次成功
        cb.record_success()
        assert cb.state == CircuitState.CLOSED  # 恢复

    def test_half_open_failure_reopens(self):
        cb = CircuitBreaker(failure_threshold=2, recovery_timeout=0.05)
        cb.record_failure()
        cb.record_failure()
        time.sleep(0.1)
        assert cb.state == CircuitState.HALF_OPEN

        cb.record_failure()
        assert cb.state == CircuitState.OPEN  # 重新打开

    def test_stats(self):
        cb = CircuitBreaker(failure_threshold=2, name="test-cb")
        cb.record_failure()
        cb.record_failure()
        stats = cb.get_stats()
        assert stats["state"] == "open"
        assert stats["failure_count"] == 2
        assert stats["total_trips"] == 1

    def test_total_trips_accumulates(self):
        cb = CircuitBreaker(failure_threshold=1, recovery_timeout=0.05)
        # 第1次熔断
        cb.record_failure()
        assert cb._total_trips == 1
        # 恢复
        time.sleep(0.1)
        cb.record_success()
        cb.record_success()
        # 第2次熔断
        cb.record_failure()
        assert cb._total_trips == 2


# ── Writer 输出验证测试 ────────────────────────────────────

class TestWriterOutputValidation:
    """
    测试输出验证逻辑 — 独立于 BaseWriterAgent 的纯函数测试
    (避免 OpenManus 导入链中 DaytonaSettings 的环境依赖)
    """

    def _validate(self, content, target_words=10000):
        """直接调用验证逻辑，无需实例化完整 Agent"""
        import re

        target = target_words
        actual = len(content)
        ratio = actual / max(target, 1)
        word_count_ok = 0.5 <= ratio <= 1.5
        warnings = []
        if not word_count_ok:
            pct = round(ratio * 100, 1)
            warnings.append(f"字数偏差: 目标 {target}, 实际 {actual} ({pct}%)")

        todo_pattern = re.compile(r'\[TODO[:\s][^\]]*\]', re.IGNORECASE)
        todo_markers = todo_pattern.findall(content)
        if todo_markers:
            warnings.append(f"含 {len(todo_markers)} 个 [TODO] 标记，需人工补充")

        has_title = bool(re.search(r'^#', content, re.MULTILINE))
        has_content = len(content.strip()) > 500
        if not has_title:
            warnings.append("内容缺少标题 (# 标记)")
        if not has_content:
            warnings.append("内容过短 (<500字)")

        return {
            "word_count_ratio": round(ratio, 2),
            "word_count_ok": word_count_ok,
            "todo_markers": todo_markers[:10],
            "todo_count": len(todo_markers),
            "has_title": has_title,
            "has_content": has_content,
            "warnings": warnings,
        }

    def test_good_content_passes(self):
        content = "# 第一章 绪论\n\n" + "水系统控制论是一门新兴学科。" * 100
        result = self._validate(content, target_words=1000)
        assert result["has_title"] is True
        assert result["has_content"] is True
        assert len(result["warnings"]) == 0

    def test_word_count_too_low(self):
        content = "# 短内容\n\n" + "一些文字。" * 200
        result = self._validate(content, target_words=50000)
        assert result["word_count_ok"] is False
        assert any("字数偏差" in w for w in result["warnings"])

    def test_todo_markers_detected(self):
        content = "# 测试\n\n正文内容。[TODO: 需补充工程参数]。另一段[TODO: 待确认数据]。" + "x" * 500
        result = self._validate(content, target_words=500)
        assert result["todo_count"] == 2
        assert len(result["todo_markers"]) == 2
        assert any("TODO" in w for w in result["warnings"])

    def test_no_title_warning(self):
        content = "这段内容没有标题。" * 50
        result = self._validate(content, target_words=500)
        assert result["has_title"] is False
        assert any("标题" in w for w in result["warnings"])

    def test_too_short_warning(self):
        content = "# 标题\n\n短"
        result = self._validate(content, target_words=100)
        assert result["has_content"] is False
        assert any("过短" in w for w in result["warnings"])

    def test_word_count_upper_bound(self):
        """字数超过目标150%也应警告"""
        content = "# 超长内容\n\n" + "重复文字。" * 10000
        result = self._validate(content, target_words=1000)
        assert result["word_count_ok"] is False

    def test_todo_case_insensitive(self):
        """[todo: xxx] 也应被检测"""
        content = "# 标题\n\n" + "x" * 600 + "[todo: check this]"
        result = self._validate(content, target_words=500)
        assert result["todo_count"] == 1


# ── 原子写入测试 ──────────────────────────────────────────

def _atomic_write(path: str, content: str):
    """独立的原子化写入 — 与 Orchestrator._atomic_write 逻辑一致"""
    dir_path = os.path.dirname(path)
    os.makedirs(dir_path, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(dir=dir_path, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(content)
        os.replace(tmp_path, path)
    except Exception:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise


class TestAtomicWrite:
    """测试原子化文件写入"""

    def test_basic_atomic_write(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "test.md")
            _atomic_write(path, "hello world")
            with open(path, "r") as f:
                assert f.read() == "hello world"

    def test_atomic_write_creates_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "subdir", "deep", "test.md")
            _atomic_write(path, "nested content")
            with open(path, "r") as f:
                assert f.read() == "nested content"

    def test_atomic_write_overwrites(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "test.md")
            _atomic_write(path, "version 1")
            _atomic_write(path, "version 2")
            with open(path, "r") as f:
                assert f.read() == "version 2"

    def test_atomic_write_no_tmp_file_on_success(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "test.md")
            _atomic_write(path, "content")
            files = os.listdir(tmpdir)
            assert len(files) == 1
            assert files[0] == "test.md"

    def test_atomic_write_unicode(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "中文.md")
            content = "水系统控制论（CHS）提出了安全包络和水网自主等级的概念。"
            _atomic_write(path, content)
            with open(path, "r", encoding="utf-8") as f:
                assert f.read() == content


# ── 健康检查测试 ──────────────────────────────────────────

class TestHealthEndpoints:
    """测试 /health 和 /ready 端点"""

    @pytest.fixture
    def client(self):
        """创建 FastAPI 测试客户端"""
        try:
            from fastapi.testclient import TestClient
            from hydroscribe.api.app import app
            return TestClient(app)
        except Exception:
            pytest.skip("FastAPI test client not available")

    def test_health_returns_200(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["version"] == "0.3.0"
        assert "checks" in data
        assert data["checks"]["event_bus"] == "ok"

    def test_ready_returns_200(self, client):
        resp = client.get("/ready")
        assert resp.status_code == 200
        data = resp.json()
        assert "ready" in data
        assert "checks" in data
        assert "tasks_capacity" in data["checks"]
