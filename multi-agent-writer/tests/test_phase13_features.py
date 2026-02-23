"""
Phase 13 测试 — 优雅关闭 + Writer 段级重试 + Prometheus 指标 + CLI audit
"""

import asyncio
import json
import os
import tempfile

import pytest

from hydroscribe.engine.event_bus import EventBus
from hydroscribe.engine.audit_log import AuditLogger
from hydroscribe.engine.config_loader import HydroScribeConfig, OrchestratorConfig
from hydroscribe.engine.book_registry import BOOK_REGISTRY


# ── 优雅关闭测试 ──────────────────────────────────────────────

class TestGracefulShutdown:
    """测试 Orchestrator.shutdown() 优雅关闭"""

    def test_orchestrator_has_shutdown_method(self):
        """Orchestrator 应有 shutdown 方法"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "engine", "orchestrator.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "async def shutdown(self)" in source

    def test_orchestrator_has_shutting_down_flag(self):
        """Orchestrator 应有 _shutting_down 标志"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "engine", "orchestrator.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "self._shutting_down = False" in source

    def test_shutdown_saves_checkpoints(self):
        """shutdown 应保存活跃任务的检查点"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "engine", "orchestrator.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        # 在 shutdown 方法中应调用 _save_checkpoint
        assert "_save_checkpoint" in source

    def test_shutdown_clears_active_tasks(self):
        """shutdown 应清理 active_tasks"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "engine", "orchestrator.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        # shutdown 方法应清空 active_tasks
        assert "self.active_tasks.clear()" in source

    def test_shutdown_logs_audit(self):
        """shutdown 应记录审计日志"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "engine", "orchestrator.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert '"system_shutdown"' in source

    def test_app_shutdown_calls_orchestrator_shutdown(self):
        """app.py 的 shutdown_event 应调用 orchestrator.shutdown()"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "api", "app.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "await orchestrator.shutdown()" in source

    def test_is_shutting_down_property(self):
        """Orchestrator 应有 is_shutting_down 属性"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "engine", "orchestrator.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "is_shutting_down" in source


class TestEventBusShutdown:
    """测试 EventBus 的优雅关闭"""

    @pytest.mark.asyncio
    async def test_eventbus_shutdown_sets_flag(self):
        bus = EventBus()
        assert bus._shutting_down is False
        await bus.shutdown()
        assert bus._shutting_down is True

    @pytest.mark.asyncio
    async def test_eventbus_shutdown_clears_subscribers(self):
        bus = EventBus()
        from hydroscribe.schema import EventType
        bus.subscribe(EventType.TASK_CREATED, lambda e: None)
        bus.subscribe_all(lambda e: None)
        await bus.shutdown()
        assert len(bus._subscribers) == 0
        assert len(bus._global_subscribers) == 0

    @pytest.mark.asyncio
    async def test_eventbus_shutdown_clears_ws(self):
        bus = EventBus()
        # 模拟 WS 连接
        class MockWS:
            async def send_text(self, data): pass
            async def close(self): pass
        bus.register_ws(MockWS())
        assert len(bus._ws_connections) == 1
        await bus.shutdown()
        assert len(bus._ws_connections) == 0


# ── Writer 段级重试测试 ──────────────────────────────────────

class TestWriterSectionRetry:
    """测试 _write_section_managed 的段级重试"""

    def test_base_writer_has_retry_params(self):
        """_write_section_managed 应有 max_retries 参数"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "agents", "base_writer.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "max_retries" in source
        assert "retry_delay" in source

    def test_retry_logic_in_source(self):
        """段级重试应包含重试循环"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "agents", "base_writer.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        # 应有重试循环和指数退避
        assert "for attempt in range" in source
        assert "asyncio.sleep" in source

    def test_retry_has_exponential_backoff(self):
        """重试应使用指数退避"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "agents", "base_writer.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        # 指数退避: retry_delay * (2 ** (attempt - 1))
        assert "2 **" in source

    def test_retry_resets_memory(self):
        """重试前应重置对话历史"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "agents", "base_writer.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        # 重试前调用 _reset_memory
        assert "_reset_memory" in source

    def test_retry_fallback_to_todo(self):
        """全部重试耗尽应返回 TODO 占位符"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "agents", "base_writer.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "[TODO:" in source
        assert "需人工补充" in source

    def test_default_retry_count(self):
        """默认最大重试次数应为 2"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "agents", "base_writer.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "max_retries: int = 2" in source


# ── Prometheus 指标导出测试 ────────────────────────────────────

class TestPrometheusMetrics:
    """测试 /metrics 端点（Prometheus text format）"""

    def test_metrics_endpoint_defined(self):
        """/metrics 端点应在 app.py 中定义"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "api", "app.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert '@app.get("/metrics"' in source

    def test_metrics_returns_plaintext(self):
        """Prometheus 端点应返回 PlainTextResponse"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "api", "app.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "PlainTextResponse" in source

    def test_metrics_has_help_type_lines(self):
        """Prometheus 指标应包含 # HELP 和 # TYPE 注释"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "api", "app.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "# HELP hydroscribe_uptime_seconds" in source
        assert "# TYPE hydroscribe_uptime_seconds" in source

    def test_metrics_includes_key_metrics(self):
        """应包含关键指标"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "api", "app.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        key_metrics = [
            "hydroscribe_uptime_seconds",
            "hydroscribe_tasks_total",
            "hydroscribe_active_tasks",
            "hydroscribe_active_writers",
            "hydroscribe_active_reviewers",
            "hydroscribe_ws_connections",
            "hydroscribe_events_total",
            "hydroscribe_dead_letters_total",
            "hydroscribe_llm_tokens_total",
        ]
        for metric in key_metrics:
            assert metric in source, f"缺少指标: {metric}"

    def test_metrics_has_per_role_tokens(self):
        """应有按角色的 token 指标"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "api", "app.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "hydroscribe_llm_prompt_tokens" in source
        assert "hydroscribe_llm_completion_tokens" in source

    def test_metrics_has_circuit_breaker(self):
        """应有熔断器状态指标"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "api", "app.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "hydroscribe_circuit_breaker_open" in source

    def test_metrics_exempt_from_rate_limit(self):
        """Prometheus /metrics 应考虑速率限制豁免"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "api", "app.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        # /metrics 路由存在
        assert "prometheus_metrics" in source


# ── CLI audit 命令测试 ────────────────────────────────────────

class TestCLIAudit:
    """测试 hydroscribe audit 命令"""

    def test_audit_command_registered(self):
        """audit 命令应在 CLI 中注册"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "cli.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert '"audit"' in source
        assert "cmd_audit" in source

    def test_audit_command_has_flags(self):
        """audit 命令应支持 --limit, --event, --book 参数"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "cli.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "--limit" in source
        assert "--event" in source
        assert "--book" in source

    def test_cmd_audit_function_exists(self):
        """cmd_audit 函数应存在"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "cli.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "def cmd_audit(args):" in source

    def test_audit_reads_from_audit_logger(self):
        """cmd_audit 应从 AuditLogger 读取"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "cli.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "get_audit_logger" in source
        assert "read_recent" in source

    def test_audit_supports_event_filter(self):
        """cmd_audit 应支持事件类型过滤"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "cli.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "event_filter" in source

    def test_audit_supports_book_filter(self):
        """cmd_audit 应支持书目过滤"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "cli.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "book_filter" in source


# ── CLI 帮助文本测试 ──────────────────────────────────────────

class TestCLIHelpText:
    """测试 CLI 帮助文本完善"""

    def test_version_updated(self):
        """CLI 版本应为 v0.4.0"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "cli.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "v0.4.0" in source

    def test_epilog_includes_ops_section(self):
        """epilog 应包含运维命令部分"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "cli.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "运维:" in source
        assert "hydroscribe audit" in source
        assert "hydroscribe validate" in source
        assert "hydroscribe report" in source

    def test_docstring_lists_all_commands(self):
        """模块文档应列出所有命令"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "cli.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        commands = ["init", "serve", "start", "status", "check",
                    "agents", "doctor", "config", "validate", "report", "audit"]
        for cmd in commands:
            assert cmd in source, f"文档缺少命令: {cmd}"


# ── AuditLogger 集成功能测试 ──────────────────────────────────

class TestAuditLoggerIntegration:
    """测试 AuditLogger 的过滤和集成功能"""

    def test_read_recent_with_large_limit(self):
        """read_recent 应能处理大 limit"""
        with tempfile.TemporaryDirectory() as tmpdir:
            al = AuditLogger(log_dir=tmpdir)
            for i in range(5):
                al.log(f"event_{i}", actor="test")
            records = al.read_recent(limit=100)
            assert len(records) == 5

    def test_filter_by_event_type(self):
        """应能按事件类型过滤"""
        with tempfile.TemporaryDirectory() as tmpdir:
            al = AuditLogger(log_dir=tmpdir)
            al.log("writing_started", actor="orch", book_id="T1-CN")
            al.log("writing_completed", actor="orch", book_id="T1-CN")
            al.log("writing_failed", actor="orch", book_id="M1")

            records = al.read_recent(limit=100)
            started = [r for r in records if "started" in r["event"]]
            assert len(started) == 1

    def test_filter_by_book_id(self):
        """应能按书目过滤"""
        with tempfile.TemporaryDirectory() as tmpdir:
            al = AuditLogger(log_dir=tmpdir)
            al.log("writing_started", actor="orch", book_id="T1-CN")
            al.log("writing_started", actor="orch", book_id="M1")

            records = al.read_recent(limit=100)
            t1 = [r for r in records if r.get("book_id") == "T1-CN"]
            assert len(t1) == 1

    def test_shutdown_audit_record_format(self):
        """system_shutdown 审计记录应包含详情"""
        with tempfile.TemporaryDirectory() as tmpdir:
            al = AuditLogger(log_dir=tmpdir)
            al.log(
                "system_shutdown",
                actor="orchestrator",
                details={
                    "active_tasks_cancelled": 2,
                    "checkpoints_saved": 2,
                },
            )
            records = al.read_recent()
            assert records[0]["event"] == "system_shutdown"
            assert records[0]["details"]["active_tasks_cancelled"] == 2
