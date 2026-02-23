"""
测试 LLM Bridge — LLMManager 到 Agent 的适配器
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from hydroscribe.engine.llm_provider import (
    LLMManager, LLMConfig, LLMProvider, LLMResponse, LLMUsage
)
from hydroscribe.engine.llm_bridge import (
    LLMBridge, create_writer_bridge, create_reviewer_bridge, create_utility_bridge
)


@pytest.fixture
def mock_manager():
    """创建一个 mock 的 LLMManager"""
    manager = LLMManager()
    config = LLMConfig(
        provider=LLMProvider.OPENAI,
        model="gpt-4o-mini",
        api_key="test-key",
    )
    manager.register("default", config)
    manager.register("writer", config)
    manager.register("reviewer", config)
    manager.register("utility", config)
    return manager


class TestLLMBridge:
    def test_create_bridge(self, mock_manager):
        bridge = LLMBridge(mock_manager, role="writer")
        assert bridge.role == "writer"
        assert bridge.llm_manager is mock_manager

    @pytest.mark.asyncio
    async def test_ask_with_dict_messages(self, mock_manager):
        """测试字典格式消息"""
        bridge = LLMBridge(mock_manager, role="writer")

        # Mock generate 方法
        mock_response = LLMResponse(
            content="测试响应内容",
            usage=LLMUsage(prompt_tokens=10, completion_tokens=20, total_tokens=30),
        )
        mock_manager.generate = AsyncMock(return_value=mock_response)

        result = await bridge.ask(
            messages=[{"role": "user", "content": "测试"}],
            system_msgs=[{"role": "system", "content": "你是写作助手"}],
        )

        assert result == "测试响应内容"
        mock_manager.generate.assert_called_once()
        call_kwargs = mock_manager.generate.call_args
        assert call_kwargs.kwargs["role"] == "writer"
        assert call_kwargs.kwargs["system_prompt"] == "你是写作助手"

    @pytest.mark.asyncio
    async def test_ask_with_message_objects(self, mock_manager):
        """测试 OpenManus Message 对象格式"""
        bridge = LLMBridge(mock_manager, role="reviewer")

        mock_response = LLMResponse(content="评审结果")
        mock_manager.generate = AsyncMock(return_value=mock_response)

        # 模拟 OpenManus Message 对象
        msg = MagicMock()
        msg.role = "user"
        msg.content = "请评审以下内容"

        sys_msg = MagicMock()
        sys_msg.content = "你是评审专家"

        result = await bridge.ask(messages=[msg], system_msgs=[sys_msg])

        assert result == "评审结果"
        call_kwargs = mock_manager.generate.call_args
        assert call_kwargs.kwargs["role"] == "reviewer"

    @pytest.mark.asyncio
    async def test_ask_error_propagation(self, mock_manager):
        """测试 LLM 调用失败时的错误传播"""
        bridge = LLMBridge(mock_manager, role="writer")
        mock_manager.generate = AsyncMock(side_effect=RuntimeError("API 调用失败"))

        with pytest.raises(RuntimeError, match="API 调用失败"):
            await bridge.ask(messages=[{"role": "user", "content": "test"}])

    @pytest.mark.asyncio
    async def test_ask_empty_messages(self, mock_manager):
        """测试空消息列表"""
        bridge = LLMBridge(mock_manager, role="writer")
        mock_response = LLMResponse(content="")
        mock_manager.generate = AsyncMock(return_value=mock_response)

        result = await bridge.ask(messages=[])
        assert result == ""

    @pytest.mark.asyncio
    async def test_ask_no_system_msgs(self, mock_manager):
        """测试无系统消息"""
        bridge = LLMBridge(mock_manager, role="utility")
        mock_response = LLMResponse(content="检查完成")
        mock_manager.generate = AsyncMock(return_value=mock_response)

        result = await bridge.ask(
            messages=[{"role": "user", "content": "检查术语"}],
            system_msgs=None,
        )
        assert result == "检查完成"
        call_kwargs = mock_manager.generate.call_args
        assert call_kwargs.kwargs["system_prompt"] == ""


class TestBridgeFactories:
    def test_create_writer_bridge(self, mock_manager):
        bridge = create_writer_bridge(mock_manager)
        assert isinstance(bridge, LLMBridge)
        assert bridge.role == "writer"

    def test_create_reviewer_bridge(self, mock_manager):
        bridge = create_reviewer_bridge(mock_manager)
        assert isinstance(bridge, LLMBridge)
        assert bridge.role == "reviewer"

    def test_create_utility_bridge(self, mock_manager):
        bridge = create_utility_bridge(mock_manager)
        assert isinstance(bridge, LLMBridge)
        assert bridge.role == "utility"
