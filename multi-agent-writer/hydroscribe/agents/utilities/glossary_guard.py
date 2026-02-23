"""
GlossaryGuardAgent — 术语一致性守护者

职责：
- 检查写作内容中的术语是否与统一术语表(glossary_cn.md/glossary_en.md)一致
- 检测禁止别名的使用
- 检查数学符号是否与symbols.md一致
- 检查新术语是否需要添加到术语表
"""

import os
import re
import sys
from typing import Any, Dict, List, Optional

from pydantic import Field

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'openmanus'))

from app.agent.base import BaseAgent as OpenManusBaseAgent

from hydroscribe.schema import Event, EventType
from hydroscribe.engine.event_bus import EventBus


# 禁止别名映射表（从 CLAUDE.md §5.1）
FORBIDDEN_ALIASES = {
    "水控制学": "水系统控制论",
    "水系统论": "水系统控制论",
    "水网控制学": "水系统控制论",
    "水网自动化等级": "水网自主等级",
    "水利自主等级": "水网自主等级",
    "操作设计域": "运行设计域",
    "运行设计范围": "运行设计域",
    "安全域": "安全包络",
    "物理引擎": "物理AI引擎",
    "机理模型引擎": "物理AI引擎",
    "知识引擎": "认知AI引擎",
    "决策引擎": "认知AI引擎",
    "分级控制": "分层分布式控制",
    "集散控制": "分层分布式控制",
    "多代理系统": "多智能体系统",
    "闭环测试": "在环测试",
    "水利操作系统": "水网操作系统",
    "水务OS": "水网操作系统",
    "翰铎": "瀚铎水网大模型",
    "瀚铎大模型": "瀚铎水网大模型",
    "预测控制": "模型预测控制",
    "传递矩阵": "传递函数",
    "简化模型": "降阶模型",
    "SCADA/MAS混合": "SCADA+MAS融合架构",
}

# 核心术语 — 中英对照
CORE_TERMS = {
    "水系统控制论": "Cybernetics of Hydro Systems (CHS)",
    "水网自主等级": "Water Network Autonomy Levels (WNAL)",
    "运行设计域": "Operational Design Domain (ODD)",
    "安全包络": "Safety Envelope",
    "物理AI引擎": "Physical AI Engine",
    "认知AI引擎": "Cognitive AI Engine",
    "分层分布式控制": "Hierarchical Distributed Control (HDC)",
    "多智能体系统": "Multi-Agent System (MAS)",
    "在环测试": "In-the-Loop Testing",
    "水网操作系统": "Water Network Operating System (HydroOS)",
    "瀚铎水网大模型": "HanDuo Water Network Large Model",
    "模型预测控制": "Model Predictive Control (MPC)",
    "传递函数": "Transfer Function",
    "降阶模型": "Reduced-Order Model (ROM)",
    "SCADA+MAS融合架构": "SCADA+MAS Fusion Architecture",
}


class GlossaryGuardAgent(OpenManusBaseAgent):
    """术语一致性守护者"""

    name: str = "glossary-guard"
    description: str = "术语一致性检查智能体"

    event_bus: Optional[Any] = Field(default=None, exclude=True)
    glossary_content: str = Field(default="")
    symbols_content: str = Field(default="")

    max_steps: int = 1

    class Config:
        arbitrary_types_allowed = True
        extra = "allow"

    async def check(self, content: str, book_id: str, chapter_id: str) -> Dict[str, Any]:
        """
        检查内容中的术语一致性

        Returns:
            {
                "passed": bool,
                "forbidden_aliases_found": [...],
                "missing_definitions": [...],
                "symbol_issues": [...],
                "new_terms_suggested": [...],
                "score": float
            }
        """
        issues = {
            "forbidden_aliases_found": [],
            "missing_definitions": [],
            "symbol_issues": [],
            "new_terms_suggested": [],
        }

        # 1. 检查禁止别名
        for alias, correct in FORBIDDEN_ALIASES.items():
            if alias in content:
                count = content.count(alias)
                issues["forbidden_aliases_found"].append({
                    "alias": alias,
                    "correct_term": correct,
                    "count": count,
                })

        # 2. 检查核心术语首次出现是否有定义
        for cn_term, en_term in CORE_TERMS.items():
            if cn_term in content:
                first_pos = content.index(cn_term)
                # 检查首次出现附近是否有英文标注
                context_window = content[max(0, first_pos - 50):first_pos + len(cn_term) + 100]
                abbrev = en_term.split("(")[-1].rstrip(")") if "(" in en_term else ""
                if abbrev and abbrev not in context_window and en_term not in context_window:
                    issues["missing_definitions"].append({
                        "term": cn_term,
                        "expected_annotation": en_term,
                        "first_occurrence_pos": first_pos,
                    })

        # 3. 检查数学符号一致性
        symbol_checks = [
            (r'流量.*?(\w)\s*[=≈]', "Q", "流量应使用符号Q"),
            (r'水[位深].*?(\w)\s*[=≈]', "h", "水位/水深应使用符号h或y"),
            (r'断面面积.*?(\w)\s*[=≈]', "A", "断面面积应使用符号A"),
            (r'Manning.*?(\w)\s*[=≈]', "n", "Manning系数应使用符号n"),
        ]
        for pattern, expected, msg in symbol_checks:
            matches = re.findall(pattern, content)
            for m in matches:
                if m != expected and m not in (expected.lower(), expected.upper()):
                    issues["symbol_issues"].append({"message": msg, "found": m, "expected": expected})

        # 4. 检测可能的新术语（加粗的中文词组）
        bold_terms = re.findall(r'\*\*([^*]{2,20})\*\*', content)
        for term in set(bold_terms):
            if term not in CORE_TERMS and term not in FORBIDDEN_ALIASES.values():
                if re.search(r'[\u4e00-\u9fff]', term):  # 含中文
                    issues["new_terms_suggested"].append(term)

        # 计算分数
        total_issues = (
            len(issues["forbidden_aliases_found"]) * 3 +  # 禁止别名权重高
            len(issues["missing_definitions"]) * 1 +
            len(issues["symbol_issues"]) * 2
        )
        score = max(0, 10 - total_issues * 0.5)
        passed = len(issues["forbidden_aliases_found"]) == 0 and score >= 7.0

        # 发布检查事件
        if self.event_bus:
            await self.event_bus.publish(Event(
                type=EventType.CHECK_GLOSSARY,
                source_agent=self.name,
                book_id=book_id,
                chapter_id=chapter_id,
                payload={
                    "passed": passed,
                    "score": score,
                    "forbidden_count": len(issues["forbidden_aliases_found"]),
                    "missing_defs": len(issues["missing_definitions"]),
                    "symbol_issues": len(issues["symbol_issues"]),
                }
            ))

        return {
            "passed": passed,
            "score": round(score, 1),
            **issues,
        }

    async def step(self) -> str:
        return ""
