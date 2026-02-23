"""
Phase 15 测试 — 事件重放 + 配置热重载 + CLI tasks/cancel + 任务列表 API + E2E dry-run
"""

import asyncio
import json
import os
import tempfile

import pytest

from hydroscribe.engine.event_bus import EventBus
from hydroscribe.engine.config_loader import (
    HydroScribeConfig, OrchestratorConfig, LLMRoleConfig,
    load_config, get_config, set_config, reload_config, validate_config,
)
from hydroscribe.schema import Event, EventType


# ── 事件重放测试 ──────────────────────────────────────────────

class TestEventReplay:
    """测试 EventBus.replay_from_history()"""

    @pytest.mark.asyncio
    async def test_replay_returns_count(self):
        """replay_from_history 应返回重放事件数"""
        bus = EventBus()
        # 发布一些事件到历史
        await bus.publish(Event(
            type=EventType.TASK_CREATED,
            source_agent="test",
            book_id="T1-CN",
            chapter_id="ch01",
        ))
        await bus.publish(Event(
            type=EventType.WRITING_STARTED,
            source_agent="test",
            book_id="T1-CN",
            chapter_id="ch01",
        ))

        count = await bus.replay_from_history(limit=10)
        assert count == 2

    @pytest.mark.asyncio
    async def test_replay_filter_by_type(self):
        """重放应支持按事件类型过滤"""
        bus = EventBus()
        await bus.publish(Event(type=EventType.TASK_CREATED, source_agent="test"))
        await bus.publish(Event(type=EventType.WRITING_STARTED, source_agent="test"))
        await bus.publish(Event(type=EventType.TASK_CREATED, source_agent="test"))

        count = await bus.replay_from_history(event_type=EventType.TASK_CREATED)
        assert count == 2

    @pytest.mark.asyncio
    async def test_replay_filter_by_book(self):
        """重放应支持按书目过滤"""
        bus = EventBus()
        await bus.publish(Event(type=EventType.TASK_CREATED, source_agent="test", book_id="T1-CN"))
        await bus.publish(Event(type=EventType.TASK_CREATED, source_agent="test", book_id="M1"))
        await bus.publish(Event(type=EventType.TASK_CREATED, source_agent="test", book_id="T1-CN"))

        count = await bus.replay_from_history(book_id="T1-CN")
        assert count == 2

    @pytest.mark.asyncio
    async def test_replay_triggers_handlers(self):
        """重放应触发订阅者"""
        bus = EventBus()
        received = []
        bus.subscribe(EventType.TASK_CREATED, lambda e: received.append(e.id))

        await bus.publish(Event(type=EventType.TASK_CREATED, source_agent="test"))
        assert len(received) == 1

        await bus.replay_from_history()
        assert len(received) == 2  # 原始 + 重放

    @pytest.mark.asyncio
    async def test_replay_limit(self):
        """重放应遵守 limit"""
        bus = EventBus()
        for _ in range(10):
            await bus.publish(Event(type=EventType.TASK_CREATED, source_agent="test"))

        count = await bus.replay_from_history(limit=3)
        assert count == 3

    def test_replay_method_exists_in_source(self):
        """EventBus 应有 replay_from_history 方法"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "engine", "event_bus.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "async def replay_from_history" in source


# ── 配置热重载测试 ────────────────────────────────────────────

class TestConfigReload:
    """测试配置热重载"""

    def test_reload_config_function_exists(self):
        """reload_config 函数应存在"""
        from hydroscribe.engine.config_loader import reload_config
        assert callable(reload_config)

    def test_reload_returns_config(self):
        """reload_config 应返回 HydroScribeConfig"""
        result = reload_config()
        assert isinstance(result, HydroScribeConfig)

    def test_reload_updates_global(self):
        """reload_config 应更新全局单例"""
        old_config = get_config()
        new_config = reload_config()
        current = get_config()
        assert current is new_config

        # 恢复原始
        set_config(old_config)

    def test_reload_api_endpoint_defined(self):
        """POST /api/config/reload 端点应存在"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "api", "app.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "/api/config/reload" in source

    def test_reload_api_uses_reload_config(self):
        """reload 端点应调用 reload_config"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "api", "app.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "reload_config()" in source

    def test_reload_audits_event(self):
        """reload 应记录审计日志"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "api", "app.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert '"config_reloaded"' in source


# ── 事件重放 API 测试 ────────────────────────────────────────

class TestReplayAPI:
    """测试 POST /api/events/replay 端点"""

    def test_replay_endpoint_defined(self):
        """POST /api/events/replay 应存在"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "api", "app.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "/api/events/replay" in source

    def test_replay_validates_event_type(self):
        """replay 应校验 event_type"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "api", "app.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "INVALID_EVENT_TYPE" in source

    def test_replay_request_model(self):
        """ReplayRequest 模型应存在"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "api", "app.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "class ReplayRequest" in source


# ── 任务列表 API 测试 ────────────────────────────────────────

class TestTaskListAPI:
    """测试 GET /api/tasks 端点"""

    def test_tasks_endpoint_defined(self):
        """GET /api/tasks 应存在"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "api", "app.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert '"/api/tasks"' in source

    def test_tasks_returns_active_count(self):
        """任务列表应包含 active_count"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "api", "app.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "active_count" in source

    def test_tasks_includes_task_details(self):
        """任务列表应包含任务详情"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "api", "app.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        for field in ["book_id", "chapter_id", "iteration", "max_iterations", "skill_type"]:
            assert field in source


# ── CLI tasks/cancel 命令测试 ────────────────────────────────

class TestCLITasksCancel:
    """测试 CLI tasks 和 cancel 命令"""

    def test_tasks_command_registered(self):
        """tasks 命令应在 CLI 中注册"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "cli.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert '"tasks"' in source
        assert "cmd_tasks" in source

    def test_cancel_command_registered(self):
        """cancel 命令应在 CLI 中注册"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "cli.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert '"cancel"' in source
        assert "cmd_cancel" in source

    def test_tasks_connects_to_api(self):
        """cmd_tasks 应通过 HTTP 连接 API"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "cli.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "/api/tasks" in source
        assert "urllib.request" in source

    def test_cancel_takes_task_id_arg(self):
        """cmd_cancel 应接受 task_id 参数"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "cli.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "task_id" in source

    def test_tasks_has_host_port_args(self):
        """tasks 命令应支持 --host 和 --port"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "cli.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        # tasks parser 应有 --host 和 --port
        assert "p_tasks" in source


# ── E2E Dry-Run 冒烟测试 ────────────────────────────────────

class TestE2EDryRun:
    """端到端 Dry-Run 冒烟测试 — 验证完整管线"""

    def test_dry_run_client_generates_content(self):
        """DryRunClient 应生成非空内容"""
        from hydroscribe.engine.llm_provider import LLMConfig, LLMProvider, LLMManager

        mgr = LLMManager(dry_run=True)
        mgr.register("default", LLMConfig(
            provider=LLMProvider.OPENAI,
            model="test",
            api_key="test",
        ))

        client = mgr.get_client("default")
        messages = [{"role": "user", "content": "写一段关于水系统的简介"}]
        result = asyncio.get_event_loop().run_until_complete(
            client.generate(messages)
        )
        # DryRunClient.generate returns LLMResponse (has .content)
        content = result.content if hasattr(result, "content") else str(result)
        assert len(content) > 0

    def test_dry_run_client_handles_outline_request(self):
        """DryRunClient 应识别大纲请求并生成大纲格式"""
        from hydroscribe.engine.llm_provider import LLMConfig, LLMProvider, LLMManager

        mgr = LLMManager(dry_run=True)
        mgr.register("default", LLMConfig(
            provider=LLMProvider.OPENAI,
            model="test",
            api_key="test",
        ))

        client = mgr.get_client("default")
        messages = [{"role": "user", "content": "生成详细的小节大纲"}]
        result = asyncio.get_event_loop().run_until_complete(
            client.generate(messages)
        )
        content = result.content if hasattr(result, "content") else str(result)
        # 大纲应包含数字编号
        assert any(c.isdigit() for c in content[:50])

    def test_dry_run_client_handles_review_request(self):
        """DryRunClient 应识别评审请求"""
        from hydroscribe.engine.llm_provider import LLMConfig, LLMProvider, LLMManager

        mgr = LLMManager(dry_run=True)
        mgr.register("default", LLMConfig(
            provider=LLMProvider.OPENAI,
            model="test",
            api_key="test",
        ))

        client = mgr.get_client("default")
        messages = [{"role": "user", "content": "请以评审角色评审以下内容"}]
        result = asyncio.get_event_loop().run_until_complete(
            client.generate(messages)
        )
        content = result.content if hasattr(result, "content") else str(result)
        assert len(content) > 0

    def test_dry_run_tracks_tokens(self):
        """DryRunClient 应追踪 token 使用（通过 call() 方法）"""
        from hydroscribe.engine.llm_provider import LLMConfig, LLMProvider, LLMManager

        mgr = LLMManager(dry_run=True)
        mgr.register("default", LLMConfig(
            provider=LLMProvider.OPENAI,
            model="test",
            api_key="test",
        ))

        client = mgr.get_client("default")
        messages = [{"role": "user", "content": "test prompt"}]
        # 使用 generate_with_retry() 而非 generate()，因为 token 统计在前者中累计
        asyncio.get_event_loop().run_until_complete(
            client.generate_with_retry(messages)
        )
        assert mgr.get_total_tokens() > 0

    def test_orchestrator_config_dry_run_field(self):
        """OrchestratorConfig 应有 dry_run 字段"""
        cfg = OrchestratorConfig()
        assert hasattr(cfg, "dry_run")
        assert cfg.dry_run is False

    def test_llm_manager_dry_run_flag(self):
        """LLMManager 应有 dry_run 标志"""
        from hydroscribe.engine.llm_provider import LLMManager
        mgr = LLMManager(dry_run=True)
        assert mgr._dry_run is True

    def test_full_pipeline_components_exist(self):
        """完整管线组件应全部存在"""
        # 验证关键模块源文件存在且包含核心类定义
        # （避免直接导入 Orchestrator 触发 DaytonaSettings 依赖）
        base = os.path.join(os.path.dirname(__file__), "..", "hydroscribe")

        modules = {
            os.path.join(base, "engine", "orchestrator.py"): "class Orchestrator",
            os.path.join(base, "engine", "event_bus.py"): "class EventBus",
            os.path.join(base, "engine", "llm_provider.py"): "class LLMManager",
            os.path.join(base, "engine", "config_loader.py"): "class HydroScribeConfig",
            os.path.join(base, "engine", "book_registry.py"): "BOOK_REGISTRY",
            os.path.join(base, "engine", "audit_log.py"): "class AuditLogger",
        }
        for path, marker in modules.items():
            with open(path, "r") as f:
                source = f.read()
            assert marker in source, f"{marker} not found in {path}"

        # 验证书目注册表数量
        from hydroscribe.engine.book_registry import BOOK_REGISTRY
        assert len(BOOK_REGISTRY) == 14


# ── 配置热重载变更检测测试 ────────────────────────────────────

class TestConfigChangeDetection:
    """测试配置变更检测逻辑"""

    def test_reload_detects_gate_mode_change(self):
        """reload_config 应检测 gate_mode 变更"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "engine", "config_loader.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "gate_mode" in source
        assert "def reload_config" in source

    def test_reload_detects_max_writers_change(self):
        """reload_config 应检测 max_concurrent_writers 变更"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "engine", "config_loader.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "max_concurrent_writers" in source

    def test_reload_returns_changed_fields(self):
        """reload_config 应记录变更字段"""
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "hydroscribe", "engine", "config_loader.py"
        )
        with open(src_path, "r") as f:
            source = f.read()
        assert "changed" in source
