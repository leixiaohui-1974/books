"""
HydroScribe - CHS 多智能体协同写作助手
基于 OpenManus 架构，融合 9 大写作技能，支持实时 UI 追踪

Architecture:
  OpenManus (BaseAgent/PlanningFlow) → HydroScribe (CHS 领域定制)
  9 Writer Agents + N Reviewer Agents + Utility Agents
  Event Bus → WebSocket → React UI
"""

__version__ = "0.1.0"
__author__ = "CHS Writing System"
