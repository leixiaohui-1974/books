"""
Phase 10 测试 — 处理器超时 + 延迟追踪 + 任务统计 + Dry-run
"""

import asyncio
import time

import pytest

from hydroscribe.engine.event_bus import EventBus
from hydroscribe.engine.llm_provider import (
    DryRunClient,
    LatencyTracker,
    LLMConfig,
    LLMManager,
    LLMProvider,
)
from hydroscribe.schema import Event, EventType


# ── EventBus 处理器超时测试 ────────────────────────────────

class TestEventBusHandlerTimeout:
    """测试 publish() 的处理器超时保护"""

    @pytest.fixture
    def event_bus(self):
        return EventBus(max_history=100)

    def _make_event(self):
        return Event(
            type=EventType.WRITING_CHUNK,
            source_agent="test",
            payload={"test": True},
        )

    @pytest.mark.asyncio
    async def test_normal_handler_executes(self, event_bus):
        """正常处理器应被执行"""
        results = []
        event_bus.subscribe(EventType.WRITING_CHUNK, lambda e: results.append("ok"))
        await event_bus.publish(self._make_event())
        assert results == ["ok"]

    @pytest.mark.asyncio
    async def test_slow_handler_times_out(self, event_bus):
        """慢处理器应被超时跳过，不阻塞后续处理器"""
        results = []

        async def slow_handler(e):
            await asyncio.sleep(5.0)  # 超过 handler_timeout
            results.append("slow")

        def fast_handler(e):
            results.append("fast")

        event_bus.subscribe(EventType.WRITING_CHUNK, slow_handler)
        event_bus.subscribe(EventType.WRITING_CHUNK, fast_handler)

        start = time.monotonic()
        await event_bus.publish(self._make_event(), handler_timeout=0.1)
        elapsed = time.monotonic() - start

        # 快处理器应已执行
        assert "fast" in results
        # 慢处理器应被跳过
        assert "slow" not in results
        # 总耗时应远小于 5 秒
        assert elapsed < 1.0

    @pytest.mark.asyncio
    async def test_handler_exception_doesnt_block(self, event_bus):
        """抛异常的处理器不应阻塞后续处理器"""
        results = []

        def bad_handler(e):
            raise ValueError("boom")

        def good_handler(e):
            results.append("ok")

        event_bus.subscribe(EventType.WRITING_CHUNK, bad_handler)
        event_bus.subscribe(EventType.WRITING_CHUNK, good_handler)
        await event_bus.publish(self._make_event())

        assert results == ["ok"]

    @pytest.mark.asyncio
    async def test_global_handler_timeout(self, event_bus):
        """全局处理器也应受超时保护"""
        results = []

        async def slow_global(e):
            await asyncio.sleep(5.0)
            results.append("slow_global")

        def fast_global(e):
            results.append("fast_global")

        event_bus.subscribe_all(slow_global)
        event_bus.subscribe_all(fast_global)

        await event_bus.publish(self._make_event(), handler_timeout=0.1)
        assert "fast_global" in results
        assert "slow_global" not in results


# ── 延迟追踪器测试 ─────────────────────────────────────────

class TestLatencyTracker:
    """测试 LLM 延迟统计"""

    def test_empty_stats(self):
        tracker = LatencyTracker()
        stats = tracker.get_stats()
        assert stats["total_calls"] == 0
        assert stats["min_ms"] == 0

    def test_single_sample(self):
        tracker = LatencyTracker()
        tracker.record(100.0)
        stats = tracker.get_stats()
        assert stats["total_calls"] == 1
        assert stats["min_ms"] == 100.0
        assert stats["max_ms"] == 100.0
        assert stats["avg_ms"] == 100.0

    def test_multiple_samples(self):
        tracker = LatencyTracker()
        for v in [50, 100, 150, 200, 250]:
            tracker.record(float(v))
        stats = tracker.get_stats()
        assert stats["total_calls"] == 5
        assert stats["min_ms"] == 50.0
        assert stats["max_ms"] == 250.0
        assert stats["avg_ms"] == 150.0
        assert stats["p50_ms"] == 150.0  # 中位数
        assert stats["p95_ms"] == 250.0  # 第95百分位

    def test_max_samples_cap(self):
        tracker = LatencyTracker(max_samples=5)
        for i in range(20):
            tracker.record(float(i * 10))
        stats = tracker.get_stats()
        assert stats["total_calls"] == 20
        # 只保留最近 5 个样本 (150, 160, 170, 180, 190)
        assert stats["min_ms"] == 150.0
        assert stats["max_ms"] == 190.0


# ── Dry-run 客户端测试 ─────────────────────────────────────

class TestDryRunClient:
    """测试 DryRunClient 占位内容生成"""

    @pytest.fixture
    def client(self):
        config = LLMConfig(
            provider=LLMProvider.LOCAL,
            model="dry-run",
        )
        return DryRunClient(config)

    @pytest.mark.asyncio
    async def test_generate_returns_content(self, client):
        """dry-run 应返回非空内容"""
        response = await client.generate(
            messages=[{"role": "user", "content": "写一些内容"}]
        )
        assert len(response.content) > 0
        assert response.model == "dry-run"
        assert response.usage is not None
        assert response.usage.total_tokens > 0

    @pytest.mark.asyncio
    async def test_outline_detection(self, client):
        """请求大纲时应返回大纲格式"""
        response = await client.generate(
            messages=[{"role": "user", "content": "请生成大纲"}]
        )
        assert "1.1" in response.content

    @pytest.mark.asyncio
    async def test_review_detection(self, client):
        """请求评审时应返回评审格式"""
        response = await client.generate(
            messages=[{"role": "user", "content": "请进行评审"}]
        )
        assert "评审" in response.content

    @pytest.mark.asyncio
    async def test_dry_run_latency_tracked(self, client):
        """dry-run 也应记录延迟"""
        await client.generate_with_retry(
            messages=[{"role": "user", "content": "test"}]
        )
        stats = client.latency_stats
        assert stats["total_calls"] == 1
        assert stats["min_ms"] > 0  # 至少有 10ms 模拟延迟


# ── LLMManager dry_run 模式测试 ────────────────────────────

class TestLLMManagerDryRun:
    """测试 LLMManager 的 dry-run 模式"""

    def test_dry_run_creates_dry_clients(self):
        mgr = LLMManager(dry_run=True)
        config = LLMConfig(
            provider=LLMProvider.OPENAI,
            model="gpt-4o",
            api_key="fake-key",
        )
        mgr.register("writer", config)
        client = mgr.get_client("writer")
        assert isinstance(client, DryRunClient)

    def test_normal_mode_creates_real_clients(self):
        mgr = LLMManager(dry_run=False)
        config = LLMConfig(
            provider=LLMProvider.LOCAL,
            model="test",
            base_url="http://localhost:11434",
        )
        mgr.register("writer", config)
        client = mgr.get_client("writer")
        assert not isinstance(client, DryRunClient)

    @pytest.mark.asyncio
    async def test_dry_run_generate(self):
        """LLMManager.generate() 在 dry-run 模式下应返回占位内容"""
        mgr = LLMManager(dry_run=True)
        config = LLMConfig(
            provider=LLMProvider.LOCAL,
            model="test",
        )
        mgr.register("writer", config)
        response = await mgr.generate(
            role="writer",
            messages=[{"role": "user", "content": "test"}],
        )
        assert response.provider == "dry-run"
        assert len(response.content) > 0

    def test_latency_stats_aggregation(self):
        mgr = LLMManager(dry_run=False)
        config = LLMConfig(
            provider=LLMProvider.LOCAL,
            model="test",
            base_url="http://localhost:11434",
        )
        mgr.register("writer", config)
        stats = mgr.get_latency_stats()
        assert "writer" in stats
        assert stats["writer"]["total_calls"] == 0


# ── Config dry_run 测试 ─────────────────────────────────────

class TestConfigDryRun:
    def test_default_dry_run_off(self):
        from hydroscribe.engine.config_loader import OrchestratorConfig
        oc = OrchestratorConfig()
        assert oc.dry_run is False

    def test_dry_run_configurable(self):
        from hydroscribe.engine.config_loader import OrchestratorConfig
        oc = OrchestratorConfig(dry_run=True)
        assert oc.dry_run is True
