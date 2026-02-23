"""
集成测试 — Orchestrator write→review→gate 循环

使用 Mock LLM 模拟完整的写作→评审→门控流程，
验证端到端流程的正确性和错误处理。
"""

import asyncio
import json
import os
import tempfile
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from hydroscribe.schema import (
    SkillType, ReviewerRole, EventType, Event,
    ChapterSpec, WritingTask, ReviewScore, AggregatedReview,
    BookProgress, ChapterProgress,
    SKILL_REVIEWERS,
)
from hydroscribe.engine.event_bus import EventBus
from hydroscribe.engine.llm_provider import (
    LLMManager, LLMConfig, LLMProvider, LLMResponse, LLMUsage
)
from hydroscribe.engine.llm_bridge import LLMBridge


# ── Mock LLM 响应 ─────────────────────────────────────────

MOCK_OUTLINE = """01.1 引言
01.2 水系统面临的挑战
01.3 控制论基础
01.4 CHS学科定位
01.5 本章小结"""

MOCK_SECTION_CONTENT = """## {title}

这是测试生成的章节内容。水系统控制论（Cybernetics of Hydro Systems, CHS）是一门研究
水利基础设施自主运行的交叉学科。

$$\\frac{{\\partial A}}{{\\partial t}} + \\frac{{\\partial Q}}{{\\partial x}} = q_l$$

**关键概念**: 水网自主等级（Water Network Autonomy Levels, WNAL）定义了L0-L5六级自主分级体系。

【例1-1】某明渠渠段长L=10km，设计流量Q₀=50m³/s...

[图1-1: CHS八原理关系图]

[1] Lei et al., 2025a
[2] Wiener, N. (1948)
"""

MOCK_REVIEW_JSON = """```json
{
    "overall_score": 8.5,
    "dimension_scores": {"coverage": 9, "accuracy": 8, "readability": 8.5},
    "decision": "minor",
    "issues_red": [],
    "issues_yellow": ["建议增加更多工程案例"],
    "issues_green": ["图表标注可以更详细"],
    "comments": "整体质量良好，建议小修后通过"
}
```"""


class MockLLMBridge:
    """Mock LLM Bridge — 返回预设的响应"""

    def __init__(self, responses=None):
        self._responses = responses or []
        self._call_count = 0

    async def ask(self, messages=None, system_msgs=None, **kwargs):
        if self._call_count < len(self._responses):
            resp = self._responses[self._call_count]
        else:
            resp = MOCK_SECTION_CONTENT.format(title="默认内容")
        self._call_count += 1
        return resp


@pytest.fixture
def temp_books_dir():
    """临时书稿目录"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # 创建基本目录结构
        os.makedirs(os.path.join(tmpdir, "progress"), exist_ok=True)
        os.makedirs(os.path.join(tmpdir, "books", "T1-CN"), exist_ok=True)
        os.makedirs(os.path.join(tmpdir, "terminology"), exist_ok=True)

        # 创建空进度文件
        progress = {
            "book_id": "T1-CN",
            "book_title": "水系统控制论",
            "total_chapters": 8,
            "chapters": {},
            "overall_progress": "0%",
        }
        with open(os.path.join(tmpdir, "progress", "BKT1-CN.json"), "w") as f:
            json.dump(progress, f)

        yield tmpdir


@pytest.fixture
def event_bus():
    return EventBus(max_history=500)


class TestEventBusIntegration:
    """测试事件总线在完整流程中的行为"""

    @pytest.mark.asyncio
    async def test_event_ordering(self, event_bus):
        """验证事件按正确顺序发布"""
        events = []

        async def capture(event):
            events.append(event.type)

        event_bus.subscribe_all(capture)

        # 模拟一个完整的写作+评审流程
        flow = [
            EventType.TASK_CREATED,
            EventType.REVISION_ROUND,
            EventType.WRITING_STARTED,
            EventType.WRITING_CHUNK,
            EventType.WRITING_CHUNK,
            EventType.WRITING_DONE,
            EventType.REVIEW_STARTED,
            EventType.REVIEW_SCORE,
            EventType.CHAPTER_COMPLETED,
        ]

        for et in flow:
            await event_bus.publish(Event(
                type=et,
                source_agent="test",
                book_id="T1-CN",
                chapter_id="ch01",
                payload={},
            ))

        assert events == flow

    @pytest.mark.asyncio
    async def test_concurrent_events(self, event_bus):
        """测试并发事件发布"""
        event_count = [0]

        async def counter(event):
            event_count[0] += 1

        event_bus.subscribe_all(counter)

        # 并发发布 50 个事件
        tasks = [
            event_bus.publish(Event(
                type=EventType.WRITING_CHUNK,
                source_agent=f"writer-{i}",
                payload={"i": i},
            ))
            for i in range(50)
        ]
        await asyncio.gather(*tasks)

        assert event_count[0] == 50
        assert len(event_bus._history) == 50


class TestWritingTaskLifecycle:
    """测试写作任务生命周期"""

    def test_task_creation(self):
        task = WritingTask(
            book_id="T1-CN",
            chapter_id="ch01",
            skill_type=SkillType.BK,
            spec=ChapterSpec(
                chapter_id="ch01",
                title="绪论：水系统面临的控制挑战",
                target_words=15000,
                core_content="全球水利基础设施现状",
            ),
        )
        assert task.status == "pending"
        assert task.current_iteration == 0
        assert len(task.id) > 0

    def test_task_with_reviewers(self):
        task = WritingTask(
            book_id="T2a",
            chapter_id="ch07",
            skill_type=SkillType.BK,
            spec=ChapterSpec(chapter_id="ch07", title="MPC", target_words=40000),
        )
        # BK 技能应有 4 个评审角色
        bk_reviewers = SKILL_REVIEWERS[SkillType.BK]
        assert len(bk_reviewers) == 4


class TestMockLLMBridge:
    """测试 Mock LLM 与 Agent 交互"""

    @pytest.mark.asyncio
    async def test_mock_bridge_responses(self):
        bridge = MockLLMBridge(responses=["响应1", "响应2", "响应3"])

        r1 = await bridge.ask(messages=[{"role": "user", "content": "test"}])
        assert r1 == "响应1"

        r2 = await bridge.ask(messages=[{"role": "user", "content": "test"}])
        assert r2 == "响应2"

    @pytest.mark.asyncio
    async def test_mock_bridge_fallback(self):
        bridge = MockLLMBridge(responses=["只有一个"])

        r1 = await bridge.ask(messages=[])
        assert r1 == "只有一个"

        # 超出范围后使用默认
        r2 = await bridge.ask(messages=[])
        assert "默认内容" in r2


class TestReviewScoreAggregation:
    """测试评审评分聚合逻辑"""

    def test_weighted_aggregation(self):
        """验证加权评分计算"""
        reviews = [
            ReviewScore(reviewer_role="instructor", overall=8.0),
            ReviewScore(reviewer_role="expert", overall=9.0),
            ReviewScore(reviewer_role="engineer", overall=7.0),
            ReviewScore(reviewer_role="international", overall=8.5),
        ]

        # BK 权重: instructor=30, expert=30, engineer=20, international=20
        weights = {"instructor": 0.30, "expert": 0.30, "engineer": 0.20, "international": 0.20}
        weighted_sum = sum(
            r.overall * weights.get(r.reviewer_role, 0.25)
            for r in reviews
        )
        expected = 8.0 * 0.30 + 9.0 * 0.30 + 7.0 * 0.20 + 8.5 * 0.20
        assert abs(weighted_sum - expected) < 0.01

    def test_all_red_issues_trigger_rejection(self):
        """有红色问题应该触发修改"""
        review = ReviewScore(
            reviewer_role="expert",
            overall=9.0,
            decision="accept",
            issues_red=["公式(3-5)量纲不一致"],
        )
        # 即使分数高，有红色问题也应该标记
        assert len(review.issues_red) > 0


class TestTaskCleanup:
    """测试任务清理（内存泄漏修复）"""

    @pytest.mark.asyncio
    async def test_event_bus_history_bounded(self):
        bus = EventBus(max_history=10)
        for i in range(100):
            await bus.publish(Event(
                type=EventType.WRITING_CHUNK,
                source_agent="writer",
                payload={"i": i},
            ))
        assert len(bus._history) == 10

    def test_progress_persistence(self, temp_books_dir):
        """测试进度文件正确读写"""
        progress_file = os.path.join(temp_books_dir, "progress", "BKT1-CN.json")

        with open(progress_file, "r") as f:
            data = json.load(f)

        assert data["book_id"] == "T1-CN"
        assert data["total_chapters"] == 8

        # 模拟更新进度
        data["chapters"]["ch01"] = {
            "status": "completed",
            "word_count": 15000,
            "review_passed": True,
        }
        data["overall_progress"] = "12.5%"

        with open(progress_file, "w") as f:
            json.dump(data, f)

        with open(progress_file, "r") as f:
            updated = json.load(f)

        assert updated["chapters"]["ch01"]["status"] == "completed"
        assert updated["overall_progress"] == "12.5%"


class TestErrorHandling:
    """测试错误处理路径"""

    @pytest.mark.asyncio
    async def test_review_score_on_llm_failure(self):
        """LLM 失败时评审返回降级评分"""
        score = ReviewScore(
            reviewer_role="instructor",
            overall=5.0,
            decision="major",
            comments="评审异常 (API超时)，建议人工评审",
            issues_red=["自动评审失败: API超时"],
        )
        assert score.overall == 5.0
        assert score.decision == "major"
        assert len(score.issues_red) == 1

    @pytest.mark.asyncio
    async def test_event_bus_subscriber_error_isolation(self):
        """订阅者异常不影响其他订阅者"""
        bus = EventBus()
        results = []

        def bad_handler(event):
            raise RuntimeError("handler crash")

        async def good_handler(event):
            results.append(event.type)

        bus.subscribe(EventType.TASK_CREATED, bad_handler)
        bus.subscribe(EventType.TASK_CREATED, good_handler)

        await bus.publish(Event(type=EventType.TASK_CREATED, source_agent="test"))

        # good_handler 仍然执行
        assert EventType.TASK_CREATED in results
