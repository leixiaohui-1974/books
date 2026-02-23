"""
LLM Bridge — 将 HydroScribe LLMManager 桥接到 OpenManus BaseAgent 的 LLM 接口

问题：
  BaseAgent.step() 调用 self.llm.ask()，但 self.llm 是 OpenManus 自带的 LLM 接口。
  HydroScribe 有自己的 LLMManager (支持百炼/OpenAI/Anthropic/Local)。

解决：
  创建一个适配器类 LLMBridge，实现 OpenManus LLM 接口 (ask 方法)，
  内部委托给 HydroScribe 的 LLMManager。
  Orchestrator 在创建 Agent 时注入 bridge 实例。
"""

import logging
from typing import Any, Dict, List, Optional

from hydroscribe.engine.llm_provider import LLMManager, LLMResponse

logger = logging.getLogger("hydroscribe.llm_bridge")


class LLMBridge:
    """
    适配器：将 HydroScribe LLMManager 包装为 OpenManus 期望的 LLM 接口

    OpenManus BaseAgent 调用 self.llm.ask(messages, system_msgs)
    本类实现该接口，委托给 LLMManager.generate()
    """

    def __init__(self, llm_manager: LLMManager, role: str = "default"):
        """
        Args:
            llm_manager: HydroScribe 的 LLM 管理器
            role: 角色名 (writer/reviewer/utility/default)
        """
        self.llm_manager = llm_manager
        self.role = role

    async def ask(
        self,
        messages: List[Any],
        system_msgs: Optional[List[Any]] = None,
        **kwargs,
    ) -> str:
        """
        兼容 OpenManus LLM 接口

        Args:
            messages: OpenManus Message 对象列表
            system_msgs: OpenManus 系统消息列表
        Returns:
            生成的文本内容
        """
        # 将 OpenManus Message 对象转换为标准字典格式
        api_messages = []
        for msg in messages:
            if hasattr(msg, "role") and hasattr(msg, "content"):
                api_messages.append({
                    "role": msg.role if isinstance(msg.role, str) else str(msg.role),
                    "content": msg.content or "",
                })
            elif isinstance(msg, dict):
                api_messages.append(msg)

        # 提取系统提示
        system_prompt = ""
        if system_msgs:
            sys_parts = []
            for sm in system_msgs:
                if hasattr(sm, "content") and sm.content:
                    sys_parts.append(sm.content)
                elif isinstance(sm, dict) and sm.get("content"):
                    sys_parts.append(sm["content"])
            system_prompt = "\n".join(sys_parts)

        # 委托给 LLMManager
        try:
            response: LLMResponse = await self.llm_manager.generate(
                role=self.role,
                messages=api_messages,
                system_prompt=system_prompt,
                **kwargs,
            )

            logger.debug(
                f"LLM [{self.role}] 响应: {len(response.content)}字, "
                f"tokens={response.usage.total_tokens if response.usage else '?'}"
            )

            return response.content

        except Exception as e:
            logger.error(f"LLM [{self.role}] 调用失败: {e}")
            raise


def create_writer_bridge(llm_manager: LLMManager) -> LLMBridge:
    """创建 Writer Agent 用的 LLM 桥接"""
    return LLMBridge(llm_manager, role="writer")


def create_reviewer_bridge(llm_manager: LLMManager) -> LLMBridge:
    """创建 Reviewer Agent 用的 LLM 桥接"""
    return LLMBridge(llm_manager, role="reviewer")


def create_utility_bridge(llm_manager: LLMManager) -> LLMBridge:
    """创建 Utility Agent 用的 LLM 桥接"""
    return LLMBridge(llm_manager, role="utility")
