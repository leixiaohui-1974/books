"""
BaseReviewerAgent — 评审智能体基类
继承 OpenManus BaseAgent，专用于多角色评审
"""

import os
import re
import sys
from typing import Any, Dict, List, Optional

from pydantic import Field

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'openmanus'))

from app.agent.base import BaseAgent as OpenManusBaseAgent
from app.schema import AgentState, Message

from hydroscribe.schema import (
    Event, EventType, ReviewScore, ReviewerRole, SkillType
)
from hydroscribe.engine.event_bus import EventBus


class BaseReviewerAgent(OpenManusBaseAgent):
    """
    评审智能体基类

    每个 Reviewer Agent 对应一个评审角色（教师/专家/工程师/国际读者等），
    内置该角色的评审 System Prompt 和评分标准。

    核心流程：
    1. 接收待审内容（Markdown）
    2. 构建角色化的 System Prompt
    3. 执行评审，输出结构化评分
    4. 通过 EventBus 推送评审结果
    """

    # 评审角色
    reviewer_role: ReviewerRole = Field(default=ReviewerRole.EXPERT)

    # 评审 prompt（从 agents/*.md 加载）
    reviewer_prompt_template: str = Field(default="")

    # 评分锚点（从 scoring_rubrics.md 加载）
    scoring_rubrics: str = Field(default="")

    # 事件总线
    event_bus: Optional[Any] = Field(default=None, exclude=True)

    max_steps: int = 5

    class Config:
        arbitrary_types_allowed = True
        extra = "allow"

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
        执行评审 — 主入口

        Args:
            content: 待评审的 Markdown 内容
            book_id: 书目 ID
            chapter_id: 章节 ID

        Returns:
            ReviewScore 评审结果
        """
        # 发布评审开始事件
        if self.event_bus:
            await self.event_bus.publish(Event(
                type=EventType.REVIEW_STARTED,
                source_agent=self.name,
                book_id=book_id,
                chapter_id=chapter_id,
                payload={"role": self.reviewer_role.value}
            ))

        # 构建 prompt
        self.system_prompt = self._build_review_prompt(content, book_id, chapter_id)

        # 发送待审内容
        review_request = (
            f"请评审以下 {book_id} {chapter_id} 的内容：\n\n"
            f"---\n{content[:15000]}\n---\n"  # 截断到 15000 字以控制 token
        )

        if len(content) > 15000:
            review_request += f"\n（注：原文共 {len(content)} 字，此处展示前 15000 字用于评审）"

        self.update_memory("user", review_request)

        # 调用 LLM 评审
        result = await self.step()

        # 解析评审结果
        score = self._parse_review_result(result)
        score.reviewer_role = self.reviewer_role.value

        # 发布评审评分事件
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
                    "issues_red": score.issues_red,
                    "issues_yellow": score.issues_yellow,
                    "issues_green": score.issues_green,
                    "scores": score.scores,
                }
            ))

        return score

    def _parse_review_result(self, result: str) -> ReviewScore:
        """解析 LLM 返回的评审结果（JSON 格式）"""
        import json

        score = ReviewScore()

        if not result:
            score.comments = "评审未返回结果"
            return score

        # 尝试提取 JSON 块
        json_match = re.search(r'```json\s*(.*?)\s*```', result, re.DOTALL)
        if json_match:
            try:
                data = json.loads(json_match.group(1))
                score.overall = float(data.get("overall_score", 0))
                score.scores = data.get("dimension_scores", {})
                score.decision = data.get("decision", "major")
                score.issues_red = data.get("issues_red", [])
                score.issues_yellow = data.get("issues_yellow", [])
                score.issues_green = data.get("issues_green", [])
                score.comments = data.get("comments", "")
                return score
            except (json.JSONDecodeError, ValueError):
                pass

        # JSON 解析失败，尝试从文本中提取评分
        score_match = re.search(r'(\d+\.?\d*)\s*/\s*10', result)
        if score_match:
            score.overall = float(score_match.group(1))

        score.comments = result[:1000]
        score.decision = "major"  # 默认需要大修
        return score

    async def step(self) -> str:
        """执行一步 — 调用 LLM"""
        if not self.memory.messages:
            return ""

        try:
            response = await self.llm.ask(
                messages=self.memory.messages,
                system_msgs=[Message.system_message(self.system_prompt)] if self.system_prompt else None,
            )
            if response:
                self.update_memory("assistant", response)
            return response or ""
        except Exception as e:
            return f"[ERROR: {str(e)}]"
