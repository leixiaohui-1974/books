"""
BaseReviewerAgent — 评审智能体基类
继承 OpenManus BaseAgent，专用于多角色评审

上下文管理策略：
- 短文（<15K字）：整体评审
- 中文（15K-30K字）：智能压缩后评审（保留标题/公式/定义，压缩段落）
- 长文（>30K字）：分段评审后合并结果
- 每次评审后清理对话历史
"""

import os
import re
import json
import sys
from typing import Any, Dict, List, Optional

from pydantic import Field

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'openmanus'))

from app.agent.base import BaseAgent as OpenManusBaseAgent
from app.schema import AgentState, Memory, Message

from hydroscribe.schema import (
    Event, EventType, ReviewScore, ReviewerRole, SkillType
)
from hydroscribe.engine.event_bus import EventBus
from hydroscribe.engine.context_manager import (
    ContextManager, ReviewChunker, estimate_tokens
)


class BaseReviewerAgent(OpenManusBaseAgent):
    """
    评审智能体基类

    上下文管理关键设计：
    1. 评审prompt固定（2-6K token），内容占比可控
    2. 长内容自动分段评审，合并结果
    3. 每次评审完毕清理对话，无状态设计
    4. 评审结果强制JSON格式，方便解析
    """

    reviewer_role: ReviewerRole = Field(default=ReviewerRole.EXPERT)
    reviewer_prompt_template: str = Field(default="")
    scoring_rubrics: str = Field(default="")
    weight: float = Field(default=1.0, description="评审角色权重")

    event_bus: Optional[Any] = Field(default=None, exclude=True)

    _context_manager: Optional[Any] = None

    max_steps: int = 5

    class Config:
        arbitrary_types_allowed = True
        extra = "allow"

    def _get_context_manager(self) -> ContextManager:
        if self._context_manager is None:
            self._context_manager = ContextManager()
        return self._context_manager

    def _build_review_prompt(self, content: str, book_id: str, chapter_id: str) -> str:
        """构建评审 System Prompt"""
        parts = [
            f"你正在以「{self.reviewer_role.value}」的角色评审 {book_id} {chapter_id} 的章节内容。",
            "",
        ]

        if self.reviewer_prompt_template:
            parts.append("## 评审指南")
            parts.append(self.reviewer_prompt_template)
            parts.append("")

        if self.scoring_rubrics:
            parts.append("## 评分锚点标准")
            parts.append(self.scoring_rubrics[:3000])
            parts.append("")

        parts.append("## 评审输出格式要求")
        parts.append("""
请严格按以下 JSON 格式输出评审结果（用 ```json 包裹）：
```json
{
  "overall_score": 8.5,
  "dimension_scores": {
    "维度1": 4,
    "维度2": 5
  },
  "decision": "minor",
  "issues_red": ["致命问题列表"],
  "issues_yellow": ["重要问题列表"],
  "issues_green": ["建议列表"],
  "comments": "总体评价文字"
}
```
- overall_score: 0-10 分
- decision: "accept" / "minor" / "major" / "reject"
- issues_red: 必须修改的致命问题
- issues_yellow: 应当修改的重要问题
- issues_green: 可选的建议
""")

        return "\n".join(parts)

    async def review(self, content: str, book_id: str, chapter_id: str) -> ReviewScore:
        """
        执行评审 — 主入口，自动处理上下文长度
        """
        if self.event_bus:
            await self.event_bus.publish(Event(
                type=EventType.REVIEW_STARTED,
                source_agent=self.name,
                book_id=book_id,
                chapter_id=chapter_id,
                payload={
                    "role": self.reviewer_role.value,
                    "content_tokens": estimate_tokens(content),
                }
            ))

        review_prompt = self._build_review_prompt(content, book_id, chapter_id)

        # 检查是否需要分段
        ctx = self._get_context_manager()
        chunker = ctx.get_review_chunker()
        segments = chunker.prepare_review_content(content, review_prompt)

        if len(segments) == 1:
            score = await self._review_single(
                segments[0]["content"], book_id, chapter_id, review_prompt,
                is_summary=segments[0].get("is_summary", False),
            )
        else:
            segment_results = []
            for seg in segments:
                seg_prompt = review_prompt + f"\n\n[注意: 这是第{seg['segment']}段内容，请只评审此段]"
                result_text = await self._call_llm(seg["content"], seg_prompt, book_id, chapter_id)
                parsed = self._parse_review_json(result_text)
                segment_results.append(parsed)
                self._reset_memory()

            merged = chunker.merge_segment_reviews(segment_results)
            score = ReviewScore(
                reviewer_role=self.reviewer_role.value,
                overall=merged.get("overall_score", 5.0),
                scores=merged.get("dimension_scores", {}),
                decision=merged.get("decision", "major"),
                issues_red=merged.get("issues_red", []),
                issues_yellow=merged.get("issues_yellow", []),
                issues_green=merged.get("issues_green", []),
                comments=merged.get("comments", "分段评审合并结果"),
            )

        score.reviewer_role = self.reviewer_role.value

        if self.event_bus:
            await self.event_bus.publish(Event(
                type=EventType.REVIEW_SCORE,
                source_agent=self.name,
                book_id=book_id,
                chapter_id=chapter_id,
                payload={
                    "role": self.reviewer_role.value,
                    "overall": score.overall,
                    "decision": score.decision,
                    "issues_red": score.issues_red[:5],
                    "issues_yellow": score.issues_yellow[:5],
                }
            ))

        self._reset_memory()
        return score

    async def _review_single(
        self, content: str, book_id: str, chapter_id: str,
        review_prompt: str, is_summary: bool = False,
    ) -> ReviewScore:
        """单次评审 — 异常时返回降级评分"""
        import logging
        logger = logging.getLogger("hydroscribe.reviewer")

        note = ""
        if is_summary:
            note = "\n（注：内容经过智能压缩，保留了标题/公式/定义等关键信息）"

        try:
            result_text = await self._call_llm(content, review_prompt + note, book_id, chapter_id)
            return self._parse_review_result(result_text)
        except Exception as e:
            logger.error(f"[{self.name}] 评审 {book_id}/{chapter_id} 失败: {e}")
            return ReviewScore(
                reviewer_role=self.reviewer_role.value,
                overall=5.0,
                decision="major",
                comments=f"评审异常 ({e})，建议人工评审",
                issues_red=[f"自动评审失败: {e}"],
            )

    async def _call_llm(
        self, content: str, system_prompt: str,
        book_id: str, chapter_id: str,
    ) -> str:
        """调用LLM执行评审 — 异常向上传播到 _review_single"""
        self.system_prompt = system_prompt
        review_request = (
            f"请评审以下 {book_id} {chapter_id} 的内容：\n\n"
            f"---\n{content}\n---\n"
        )
        self.update_memory("user", review_request)
        result = await self.step()
        return result

    def _reset_memory(self):
        """重置对话历史"""
        try:
            self.memory = Memory()
        except Exception:
            pass

    def _parse_review_result(self, result: str) -> ReviewScore:
        """解析 LLM 返回的评审结果"""
        score = ReviewScore()

        if not result:
            score.comments = "评审未返回结果"
            return score

        parsed = self._parse_review_json(result)
        score.overall = float(parsed.get("overall_score", 0))
        score.scores = parsed.get("dimension_scores", {})
        score.decision = parsed.get("decision", "major")
        score.issues_red = parsed.get("issues_red", [])
        score.issues_yellow = parsed.get("issues_yellow", [])
        score.issues_green = parsed.get("issues_green", [])
        score.comments = parsed.get("comments", "")

        if score.overall == 0:
            score_match = re.search(r'(\d+\.?\d*)\s*/\s*10', result)
            if score_match:
                score.overall = float(score_match.group(1))
            score.comments = result[:1000]
            score.decision = "major"

        return score

    def _parse_review_json(self, result: str) -> Dict:
        """从LLM输出中提取JSON评审结果"""
        if not result:
            return {}

        json_match = re.search(r'```json\s*(.*?)\s*```', result, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except (json.JSONDecodeError, ValueError):
                pass

        json_match = re.search(r'\{[^{}]*"overall_score"[^{}]*\}', result, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except (json.JSONDecodeError, ValueError):
                pass

        return {}

    async def step(self) -> str:
        """执行一步 — 调用 LLM

        异常处理策略：
        - LLM 调用失败时向上传播异常
        - review() 方法负责捕获并返回降级的 ReviewScore
        """
        if not self.memory.messages:
            return ""

        import logging
        logger = logging.getLogger("hydroscribe.reviewer")

        try:
            logger.debug(
                f"[{self.name}] step() 调用 LLM, "
                f"messages={len(self.memory.messages)}, "
                f"role={self.reviewer_role.value}"
            )

            response = await self.llm.ask(
                messages=self.memory.messages,
                system_msgs=[Message.system_message(self.system_prompt)] if self.system_prompt else None,
            )

            content = response or ""
            if content:
                self.update_memory("assistant", content)

            logger.debug(f"[{self.name}] step() 返回 {len(content)} 字")
            return content

        except Exception as e:
            logger.error(f"[{self.name}] step() LLM 调用失败: {e}", exc_info=True)
            raise
