"""
HydroScribe - CHS 多智能体协同写作助手
基于 OpenManus + OpenClaw 架构，融合 9 大写作技能，支持阿里云百炼

Architecture:
  OpenManus (BaseAgent/PlanningFlow) → HydroScribe (CHS 领域定制)
  9 Writer Agents + 28 Reviewer Agents + 3 Utility Agents
  LLM Provider Layer → 百炼/OpenAI/Anthropic/Local
  Event Bus → WebSocket → Dashboard UI
  OpenClaw Skill Wrapper → 可被 OpenClaw 调度
"""

__version__ = "0.3.0"
__author__ = "CHS Writing System"
