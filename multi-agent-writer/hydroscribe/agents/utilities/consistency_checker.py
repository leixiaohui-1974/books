"""
ConsistencyCheckerAgent — 跨书一致性检查器

职责（来自 CLAUDE.md §11）：
- 检查跨书共享内容的一致性（八原理、WNAL、Saint-Venant方程等）
- 检查工程参数一致性（胶东调水、沙坪水电站等）
- 检查引用格式一致性
- 维护跨书引用图谱
"""

import json
import os
import re
import sys
from typing import Any, Dict, List, Optional

from pydantic import Field

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'openmanus'))

from app.agent.base import BaseAgent as OpenManusBaseAgent

from hydroscribe.schema import Event, EventType
from hydroscribe.engine.event_bus import EventBus


# 跨书必须一致的内容定义（CLAUDE.md §11.2）
CONSISTENCY_RULES = {
    "八原理": {
        "books": ["T1", "T2a", "M9"],
        "keywords": ["传递函数化", "可控可观性", "分层分布式", "安全包络",
                      "在环验证", "认知增强", "人机共融", "自主演进"],
        "description": "八原理名称和核心表述完全一致",
    },
    "WNAL_L0_L5": {
        "books": ["T1", "T2b", "M8"],
        "keywords": ["L0", "L1", "L2", "L3", "L4", "L5", "WNAL"],
        "description": "WNAL六级定义表完全一致",
    },
    "Saint_Venant": {
        "books": ["T2a", "M1", "M8"],
        "keywords": ["Saint-Venant", "连续方程", "动量方程"],
        "description": "Saint-Venant方程形式和符号完全一致",
    },
    "MPC_basic": {
        "books": ["T2a", "M2", "M8"],
        "keywords": ["MPC", "预测时域", "控制时域", "目标函数"],
        "description": "MPC标准表述一致",
    },
    "HydroOS_arch": {
        "books": ["T1", "T2b", "M7"],
        "keywords": ["HydroOS", "三层架构", "设备抽象层", "调度引擎"],
        "description": "HydroOS架构图和层级命名一致",
    },
    "Jiaodong_params": {
        "books": ["T2a", "T2b", "M1", "M8"],
        "keywords": ["胶东调水", "明渠", "SCADA", "HDC"],
        "description": "胶东调水工程参数完全一致",
    },
    "Shaoping_params": {
        "books": ["T2a", "T2b", "M8"],
        "keywords": ["沙坪", "大渡河", "发电", "泄洪", "梯级"],
        "description": "沙坪水电站工程参数完全一致",
    },
}

# 自引论文列表（必须保持引用格式一致）
SELF_CITATIONS = [
    {"key": "Lei 2025a", "doi": "10.13476/j.cnki.nsbdqk.2025.0077", "topic": "理论背景与研究范式"},
    {"key": "Lei 2025b", "doi": "10.13476/j.cnki.nsbdqk.2025.0079", "topic": "自主智能水网架构"},
    {"key": "Lei 2025c", "doi": "10.13476/j.cnki.nsbdqk.2025.0080", "topic": "在环测试系统"},
    {"key": "Lei 2025d", "doi": "10.13476/j.cnki.nsbdqk.2025.0078", "topic": "水资源系统分析展望"},
]


class ConsistencyCheckerAgent(OpenManusBaseAgent):
    """跨书一致性检查器"""

    name: str = "consistency-checker"
    description: str = "跨书一致性检查智能体"

    books_root: str = Field(default="/home/user/books")
    event_bus: Optional[Any] = Field(default=None, exclude=True)

    max_steps: int = 1

    class Config:
        arbitrary_types_allowed = True
        extra = "allow"

    def _load_chapter_content(self, book_id: str, chapter_id: str) -> str:
        """加载已完成章节的内容"""
        base = os.path.join(self.books_root, "books", book_id)
        for suffix in ["_final.md", "_v2.md", "_v1.md", ".md"]:
            path = os.path.join(base, f"{chapter_id}{suffix}")
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    return f.read()
        return ""

    async def check(
        self,
        content: str,
        book_id: str,
        chapter_id: str,
    ) -> Dict[str, Any]:
        """
        检查新内容与已有书目的一致性

        Returns:
            {
                "passed": bool,
                "consistency_issues": [...],
                "citation_issues": [...],
                "cross_ref_suggestions": [...],
                "score": float
            }
        """
        issues = {
            "consistency_issues": [],
            "citation_issues": [],
            "cross_ref_suggestions": [],
        }

        # 1. 检查跨书关键概念一致性
        for rule_name, rule in CONSISTENCY_RULES.items():
            if book_id not in rule["books"]:
                continue

            # 检查当前内容是否包含相关关键词
            relevant_keywords = [kw for kw in rule["keywords"] if kw in content]
            if not relevant_keywords:
                continue

            # 检查其他书中对应内容
            for other_book in rule["books"]:
                if other_book == book_id:
                    continue
                # 尝试加载其他书的相关章节
                other_content = self._scan_book_for_keywords(other_book, rule["keywords"])
                if other_content:
                    # 简单的一致性检测：关键词都出现
                    for kw in rule["keywords"]:
                        if kw in content and kw not in other_content:
                            issues["consistency_issues"].append({
                                "rule": rule_name,
                                "keyword": kw,
                                "message": f"'{kw}' 在 {book_id} 中出现但在 {other_book} 中未找到",
                                "severity": "yellow",
                            })

        # 2. 检查自引论文格式一致性
        for ref in SELF_CITATIONS:
            if ref["key"] in content:
                # 检查格式 "(Lei et al., 2025a)"
                expected_pattern = rf'Lei\s+et\s+al\.\s*,?\s*2025[a-d]'
                if not re.search(expected_pattern, content):
                    issues["citation_issues"].append({
                        "citation": ref["key"],
                        "message": f"自引 {ref['key']} 格式不符合规范 '(Lei et al., 2025x)'",
                    })

                # 检查DOI是否一致
                if ref["doi"] in content:
                    pass  # DOI正确
                # 不强制要求DOI出现

        # 3. 建议跨书引用
        cross_ref_map = {
            "MPC": ("M2", "《水网预测控制》"),
            "降阶模型": ("M1", "《明渠水动力降阶建模》"),
            "安全包络": ("M3", "《水网运行安全包络》"),
            "多智能体": ("M4", "《水网多智能体系统》"),
            "认知智能": ("M5", "《水利认知智能》"),
            "在环测试": ("M6", "《水网控制在环验证》"),
            "HydroOS": ("M7", "《水网操作系统》"),
        }
        for keyword, (ref_book, ref_title) in cross_ref_map.items():
            if keyword in content and ref_book != book_id:
                # 检查是否已有跨书引用
                ref_pattern = f"参见{ref_title}|See {ref_book}"
                if not re.search(ref_pattern, content):
                    issues["cross_ref_suggestions"].append({
                        "keyword": keyword,
                        "suggested_ref": f"参见{ref_title}",
                        "ref_book": ref_book,
                    })

        # 计算分数
        red_issues = [i for i in issues["consistency_issues"] if i.get("severity") == "red"]
        yellow_issues = [i for i in issues["consistency_issues"] if i.get("severity") == "yellow"]
        score = max(0, 10 - len(red_issues) * 2 - len(yellow_issues) * 0.5 - len(issues["citation_issues"]) * 0.5)
        passed = len(red_issues) == 0 and score >= 7.0

        if self.event_bus:
            await self.event_bus.publish(Event(
                type=EventType.CHECK_CONSISTENCY,
                source_agent=self.name,
                book_id=book_id,
                chapter_id=chapter_id,
                payload={
                    "passed": passed,
                    "score": round(score, 1),
                    "consistency_count": len(issues["consistency_issues"]),
                    "citation_count": len(issues["citation_issues"]),
                    "cross_ref_count": len(issues["cross_ref_suggestions"]),
                }
            ))

        return {
            "passed": passed,
            "score": round(score, 1),
            **issues,
        }

    def _scan_book_for_keywords(self, book_id: str, keywords: List[str]) -> str:
        """扫描一本书的所有章节，返回包含关键词的内容"""
        book_dir = os.path.join(self.books_root, "books", book_id)
        if not os.path.exists(book_dir):
            return ""

        combined = ""
        for fname in sorted(os.listdir(book_dir)):
            if fname.endswith(".md"):
                path = os.path.join(book_dir, fname)
                with open(path, "r", encoding="utf-8") as f:
                    text = f.read()
                if any(kw in text for kw in keywords):
                    combined += text + "\n"
        return combined

    async def step(self) -> str:
        return ""
