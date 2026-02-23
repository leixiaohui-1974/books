"""
测试 EventBus — 事件发布/订阅/历史
"""

import asyncio
import pytest

from hydroscribe.schema import Event, EventType
from hydroscribe.engine.event_bus import EventBus


@pytest.fixture
def bus():
    return EventBus(max_history=100)


class TestEventBusPublish:
    @pytest.mark.asyncio
    async def test_publish_records_history(self, bus):
        event = Event(
            type=EventType.TASK_CREATED,
            source_agent="test-agent",
            book_id="T1-CN",
            chapter_id="ch01",
            payload={"test": True},
        )
        await bus.publish(event)
        assert len(bus._history) == 1
        assert bus._history[0].type == EventType.TASK_CREATED

    @pytest.mark.asyncio
    async def test_publish_multiple_events(self, bus):
        for i in range(5):
            await bus.publish(Event(
                type=EventType.WRITING_CHUNK,
                source_agent="writer",
                payload={"section": i},
            ))
        assert len(bus._history) == 5

    @pytest.mark.asyncio
    async def test_history_truncation(self):
        bus = EventBus(max_history=3)
        for i in range(10):
            await bus.publish(Event(
                type=EventType.WRITING_CHUNK,
                source_agent="writer",
                payload={"i": i},
            ))
        assert len(bus._history) == 3
        # 只保留最近的3个
        assert bus._history[0].payload["i"] == 7


class TestEventBusSubscription:
    @pytest.mark.asyncio
    async def test_subscribe_specific_type(self, bus):
        received = []

        async def handler(event):
            received.append(event)

        bus.subscribe(EventType.REVIEW_DONE, handler)

        # 发布匹配事件
        await bus.publish(Event(type=EventType.REVIEW_DONE, source_agent="r"))
        # 发布不匹配事件
        await bus.publish(Event(type=EventType.WRITING_DONE, source_agent="w"))

        assert len(received) == 1
        assert received[0].type == EventType.REVIEW_DONE

    @pytest.mark.asyncio
    async def test_subscribe_all(self, bus):
        received = []

        async def handler(event):
            received.append(event)

        bus.subscribe_all(handler)

        await bus.publish(Event(type=EventType.TASK_CREATED, source_agent="o"))
        await bus.publish(Event(type=EventType.WRITING_DONE, source_agent="w"))

        assert len(received) == 2

    @pytest.mark.asyncio
    async def test_handler_error_doesnt_crash(self, bus):
        """Handler 异常不应该影响事件发布"""

        def bad_handler(event):
            raise ValueError("boom")

        bus.subscribe(EventType.TASK_CREATED, bad_handler)
        # 不应抛出异常
        await bus.publish(Event(type=EventType.TASK_CREATED, source_agent="o"))
        assert len(bus._history) == 1


class TestEventBusHistory:
    @pytest.mark.asyncio
    async def test_get_history_with_limit(self, bus):
        for i in range(20):
            await bus.publish(Event(
                type=EventType.WRITING_CHUNK,
                source_agent="w",
                payload={"i": i},
            ))

        history = bus.get_history(limit=5)
        assert len(history) == 5

    @pytest.mark.asyncio
    async def test_get_history_filter_by_book(self, bus):
        await bus.publish(Event(type=EventType.TASK_CREATED, source_agent="o", book_id="T1-CN"))
        await bus.publish(Event(type=EventType.TASK_CREATED, source_agent="o", book_id="T2a"))
        await bus.publish(Event(type=EventType.TASK_CREATED, source_agent="o", book_id="T1-CN"))

        history = bus.get_history(book_id="T1-CN")
        assert len(history) == 2
        assert all(e["book"] == "T1-CN" for e in history)

    @pytest.mark.asyncio
    async def test_history_format(self, bus):
        await bus.publish(Event(
            type=EventType.CHAPTER_COMPLETED,
            source_agent="orchestrator",
            book_id="T2a",
            chapter_id="ch07",
            payload={"score": 8.5},
        ))

        history = bus.get_history()
        assert len(history) == 1
        entry = history[0]
        assert "id" in entry
        assert entry["type"] == EventType.CHAPTER_COMPLETED.value
        assert entry["agent"] == "orchestrator"
        assert entry["book"] == "T2a"
        assert entry["chapter"] == "ch07"
        assert entry["payload"]["score"] == 8.5
