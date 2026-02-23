"""
ReferenceManagerAgent — 参考文献管理器

职责：
- 检查参考文献格式一致性（GB/T 7714-2015 / APA / IEEE）
- 检查自引率是否在目标范围内
- 验证参考文献计数（总数、近5年占比）
- 检查必引文献是否被引用
- 管理master_bib.bib与各章引用的同步
"""

import os
import re
import sys
from typing import Any, Dict, List, Optional

from pydantic import Field

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'openmanus'))

from app.agent.base import BaseAgent as OpenManusBaseAgent

from hydroscribe.schema import Event, EventType, SkillType
from hydroscribe.engine.event_bus import EventBus


# 自引率目标（CLAUDE.md §9.1）
SELF_CITATION_TARGETS = {
    "T1": (0.10, 0.15),   # 10-15%
    "T2": (0.07, 0.10),   # 7-10%
    "M": (0.05, 0.08),    # 5-8%  (M1-M8)
    "M9": (0.03, 0.05),   # 3-5%
}

# 必引文献（CLAUDE.md §9.2）
MUST_CITE = [
    "Wiener, 1948",       # Cybernetics
    "钱学森, 1954",        # Engineering Cybernetics
    "Lei 2025a",          # CHS 理论背景
    "Lei 2025b",          # 自主智能水网架构
]

# 领域经典文献
CLASSIC_REFERENCES = [
    "Wylie, 1969",        # Control of transient free-surface flow
    "Buyalski, 1991",     # Canal Systems Automation Manual
    "Litrico, 2009",      # Modeling and Control of Hydrosystems
    "Van Overloop, 2006", # Model Predictive Control on Open Water Systems
    "ASCE, 2014",         # MOP 131
]

# 自引论文关键词
SELF_CITATION_MARKERS = [
    "Lei et al.",
    "Lei,",
    "雷晓辉",
    "Lei 2025",
]


class ReferenceManagerAgent(OpenManusBaseAgent):
    """参考文献管理器"""

    name: str = "reference-manager"
    description: str = "参考文献格式与一致性检查"

    event_bus: Optional[Any] = Field(default=None, exclude=True)

    max_steps: int = 1

    class Config:
        arbitrary_types_allowed = True
        extra = "allow"

    async def check(
        self,
        content: str,
        book_id: str,
        chapter_id: str,
        skill_type: SkillType = SkillType.BK,
    ) -> Dict[str, Any]:
        """
        检查参考文献质量

        Returns:
            {
                "passed": bool,
                "total_references": int,
                "self_citation_rate": float,
                "self_citation_target": tuple,
                "recent_ratio": float,
                "must_cite_missing": [...],
                "format_issues": [...],
                "score": float
            }
        """
        issues = {
            "must_cite_missing": [],
            "format_issues": [],
        }

        # 1. 提取参考文献
        refs = self._extract_references(content)
        total_refs = len(refs)

        # 2. 计算自引率
        self_count = sum(1 for r in refs if any(m in r for m in SELF_CITATION_MARKERS))
        self_rate = self_count / max(total_refs, 1)

        # 确定自引率目标
        target = (0.07, 0.10)  # 默认
        for prefix, rate_range in SELF_CITATION_TARGETS.items():
            if book_id.startswith(prefix):
                target = rate_range
                break

        # 3. 检查近5年文献占比
        current_year = 2026
        recent_count = 0
        for ref in refs:
            years = re.findall(r'(20[2-3]\d|202[1-6])', ref)
            if years:
                for y in years:
                    if current_year - int(y) <= 5:
                        recent_count += 1
                        break
        recent_ratio = recent_count / max(total_refs, 1)

        # 4. 检查必引文献
        for must_ref in MUST_CITE:
            found = False
            for ref in refs:
                if must_ref in ref or must_ref.lower() in ref.lower():
                    found = True
                    break
            # 也检查正文
            if not found and must_ref in content:
                found = True
            if not found:
                issues["must_cite_missing"].append(must_ref)

        # 5. 检查引用格式
        if skill_type == SkillType.CN:
            # GB/T 7714-2015 格式检查
            for ref in refs:
                if not re.search(r'\[(J|M|C|D|R|S|P|DB|CP|EB)\]', ref):
                    issues["format_issues"].append({
                        "reference": ref[:80],
                        "issue": "缺少文献类型标识[J][M][C]等（GB/T 7714-2015要求）",
                    })
        elif skill_type == SkillType.SCI:
            # 检查是否有足够引用
            if total_refs < 30:
                issues["format_issues"].append({
                    "reference": "全文",
                    "issue": f"SCI论文参考文献数量不足：{total_refs}篇 < 30篇最低要求",
                })

        # 6. 计算总分
        score = 10.0
        if total_refs < 10:
            score -= 2.0
        if self_rate < target[0]:
            score -= 1.0  # 自引偏低
        elif self_rate > target[1]:
            score -= 1.5  # 自引偏高
        if recent_ratio < 0.30:
            score -= 1.5  # 近期文献不足
        score -= len(issues["must_cite_missing"]) * 0.5
        score -= min(len(issues["format_issues"]) * 0.3, 2.0)
        score = max(0, round(score, 1))

        passed = score >= 7.0 and len(issues["must_cite_missing"]) <= 1

        if self.event_bus:
            await self.event_bus.publish(Event(
                type=EventType.CHECK_REFERENCE,
                source_agent=self.name,
                book_id=book_id,
                chapter_id=chapter_id,
                payload={
                    "passed": passed,
                    "score": score,
                    "total_refs": total_refs,
                    "self_rate": round(self_rate, 3),
                    "recent_ratio": round(recent_ratio, 3),
                    "missing_must_cite": len(issues["must_cite_missing"]),
                }
            ))

        return {
            "passed": passed,
            "total_references": total_refs,
            "self_citation_rate": round(self_rate, 3),
            "self_citation_target": target,
            "recent_ratio": round(recent_ratio, 3),
            "score": score,
            **issues,
        }

    def _extract_references(self, content: str) -> List[str]:
        """从内容中提取参考文献列表"""
        refs = []

        # 方法1：查找参考文献/References节
        ref_section = re.search(
            r'(?:参考文献|References|Bibliography)\s*\n(.*?)(?:\n#|\Z)',
            content, re.DOTALL | re.IGNORECASE
        )
        if ref_section:
            lines = ref_section.group(1).strip().split("\n")
            for line in lines:
                line = line.strip()
                if line and (re.match(r'^\[?\d+\]?', line) or re.match(r'^-\s', line)):
                    refs.append(line)

        # 方法2：查找内联引用 [1], [2] 等
        if not refs:
            inline_refs = re.findall(r'\[(\d+)\]', content)
            refs = [f"[{r}]" for r in sorted(set(inline_refs), key=int)]

        # 方法3：查找 (Author, Year) 格式
        if not refs:
            author_year = re.findall(r'\(([A-Z][a-z]+(?:\s+et\s+al\.)?,\s*\d{4}[a-z]?)\)', content)
            refs = list(set(author_year))

        return refs

    async def step(self) -> str:
        return ""
