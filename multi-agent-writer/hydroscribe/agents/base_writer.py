"""
BaseWriterAgent — 写作智能体基类
继承 OpenManus 的 BaseAgent 架构，专用于 CHS 学术写作
"""

import asyncio
import os
from abc import abstractmethod
from typing import Any, Dict, List, Optional

from pydantic import Field

# OpenManus imports (路径适配)
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'openmanus'))

from app.agent.base import BaseAgent as OpenManusBaseAgent
from app.schema import AgentState, Memory, Message

from hydroscribe.schema import (
    ChapterSpec, Event, EventType, ReviewScore,
    SkillType, WritingTask
)
from hydroscribe.engine.event_bus import EventBus


class BaseWriterAgent(OpenManusBaseAgent):
    """
    写作智能体基类 — 继承 OpenManus BaseAgent

    每个 Writer Agent 对应一种文体（BK/SCI/CN/PAT/RPT/STD-CN/STD-INT/WX/PPT），
    内置该文体的 System Prompt、写作技法和金标准参考。

    核心流程：
    1. 接收 WritingTask（含章节规格、前序章节、评审意见）
    2. 构建上下文（术语表、符号表、写作风格指南）
    3. 分段写作（大章节按小节分片，防止单次输出过长）
    4. 通过 EventBus 流式推送写作进度
    5. 输出完整章节 Markdown + 元数据
    """

    # 文体类型
    skill_type: SkillType = Field(default=SkillType.BK)

    # 事件总线（运行时注入）
    event_bus: Optional[Any] = Field(default=None, exclude=True)

    # 写作上下文
    glossary: str = Field(default="", description="术语表内容")
    symbols: str = Field(default="", description="符号表内容")
    style_guide: str = Field(default="", description="写作风格指南")
    prev_chapter_tail: str = Field(default="", description="前序章节末尾 500 字")
    review_feedback: str = Field(default="", description="上一轮评审意见（修改轮）")

    # 当前任务
    current_task: Optional[WritingTask] = Field(default=None, exclude=True)

    # 输出缓冲
    output_buffer: str = Field(default="", exclude=True)
    word_count: int = Field(default=0, exclude=True)

    max_steps: int = 30

    class Config:
        arbitrary_types_allowed = True
        extra = "allow"

    def _build_system_prompt(self, task: WritingTask) -> str:
        """
        构建 System Prompt：合并文体模板 + 章节规格 + 术语 + 风格
        子类可覆写以添加文体特定内容
        """
        spec = task.spec
        prompt_parts = [
            f"你是一位专业的学术写作助手，当前正在撰写《{task.book_id}》的 {spec.chapter_id}：{spec.title}。",
            f"目标字数：{spec.target_words} 字。",
            "",
            "## 写作要求",
            f"核心内容：{spec.core_content}" if spec.core_content else "",
            "",
        ]

        if self.style_guide:
            prompt_parts.append("## 写作风格指南")
            prompt_parts.append(self.style_guide)
            prompt_parts.append("")

        if self.glossary:
            prompt_parts.append("## 术语规范（严格遵循，不得使用禁止别名）")
            prompt_parts.append(self.glossary[:3000])  # 截断以节省 token
            prompt_parts.append("")

        if self.symbols:
            prompt_parts.append("## 数学符号规范")
            prompt_parts.append(self.symbols[:2000])
            prompt_parts.append("")

        if self.prev_chapter_tail:
            prompt_parts.append("## 前序章节末尾（用于衔接）")
            prompt_parts.append(self.prev_chapter_tail)
            prompt_parts.append("")

        if self.review_feedback:
            prompt_parts.append("## 上一轮评审意见（本次修改必须回应）")
            prompt_parts.append(self.review_feedback)
            prompt_parts.append("")

        return "\n".join(prompt_parts)

    async def write_chapter(self, task: WritingTask) -> Dict[str, Any]:
        """
        写一个完整章节 — 主入口

        Returns:
            {
                "content": str,      # Markdown 正文
                "word_count": int,
                "sections": list,    # 小节列表
                "metadata": dict     # 概念数/公式数/例题数等
            }
        """
        self.current_task = task
        self.output_buffer = ""
        self.word_count = 0

        # 构建 System Prompt
        self.system_prompt = self._build_system_prompt(task)

        # 发布写作开始事件
        if self.event_bus:
            await self.event_bus.publish(Event(
                type=EventType.WRITING_STARTED,
                source_agent=self.name,
                book_id=task.book_id,
                chapter_id=task.chapter_id,
                payload={"target_words": task.spec.target_words, "title": task.spec.title}
            ))

        # 生成章节大纲
        outline = await self._generate_outline(task)

        # 按小节分段写作
        full_content = ""
        sections = []

        for i, section in enumerate(outline):
            section_content = await self._write_section(task, section, i, len(outline), full_content)
            full_content += section_content + "\n\n"
            sections.append(section)

            # 流式推送进度
            self.word_count = len(full_content)
            if self.event_bus:
                await self.event_bus.publish(Event(
                    type=EventType.WRITING_CHUNK,
                    source_agent=self.name,
                    book_id=task.book_id,
                    chapter_id=task.chapter_id,
                    payload={
                        "section": section,
                        "section_index": i + 1,
                        "total_sections": len(outline),
                        "word_count": self.word_count,
                        "target_words": task.spec.target_words,
                        "progress": round(self.word_count / max(task.spec.target_words, 1) * 100, 1)
                    }
                ))

        self.output_buffer = full_content

        # 发布写作完成事件
        result = {
            "content": full_content,
            "word_count": self.word_count,
            "sections": sections,
            "metadata": self._extract_metadata(full_content)
        }

        if self.event_bus:
            await self.event_bus.publish(Event(
                type=EventType.WRITING_DONE,
                source_agent=self.name,
                book_id=task.book_id,
                chapter_id=task.chapter_id,
                payload={
                    "word_count": result["word_count"],
                    "sections": result["sections"],
                    "metadata": result["metadata"],
                }
            ))

        return result

    async def _generate_outline(self, task: WritingTask) -> List[str]:
        """
        生成章节大纲（小节列表）
        子类可覆写以使用 LLM 动态生成
        """
        # 默认实现：从 spec 中解析
        spec = task.spec
        prompt = (
            f"为《{task.book_id}》的 {spec.chapter_id}「{spec.title}」生成详细的小节大纲。\n"
            f"目标字数：{spec.target_words} 字。\n"
            f"核心内容：{spec.core_content}\n\n"
            f"请返回小节标题列表，每行一个，格式如：\n"
            f"{spec.chapter_id[2:]}.1 小节标题\n"
            f"{spec.chapter_id[2:]}.2 小节标题\n"
            f"..."
        )

        self.update_memory("user", prompt)
        step_result = await self.step()

        # 解析返回的大纲
        lines = step_result.strip().split("\n") if step_result else []
        outline = [line.strip() for line in lines if line.strip() and any(c.isdigit() for c in line[:5])]

        if not outline:
            # fallback：生成默认大纲
            ch_num = spec.chapter_id.replace("ch", "")
            outline = [
                f"{ch_num}.1 引言",
                f"{ch_num}.2 基本概念",
                f"{ch_num}.3 核心理论",
                f"{ch_num}.4 方法与算法",
                f"{ch_num}.5 案例分析",
                f"{ch_num}.6 本章小结",
            ]

        return outline

    async def _write_section(
        self,
        task: WritingTask,
        section_title: str,
        section_index: int,
        total_sections: int,
        prev_content: str
    ) -> str:
        """
        写一个小节
        """
        spec = task.spec
        words_per_section = spec.target_words // max(total_sections, 1)

        prompt = (
            f"现在请撰写「{section_title}」这一小节。\n"
            f"约 {words_per_section} 字。\n"
        )

        if section_index == 0:
            prompt += "这是本章的第一小节，需要包含引导性内容。\n"
        if section_index == total_sections - 1:
            prompt += "这是本章最后一小节，需要包含本章小结。\n"

        if prev_content:
            # 传入前文末尾用于衔接
            tail = prev_content[-500:] if len(prev_content) > 500 else prev_content
            prompt += f"\n前文末尾（用于衔接）：\n...{tail}\n"

        self.update_memory("user", prompt)
        result = await self.step()
        return result if result else ""

    def _extract_metadata(self, content: str) -> Dict[str, Any]:
        """从写作内容中提取元数据"""
        import re

        # 统计公式数量
        equations = len(re.findall(r'\$\$[^$]+\$\$', content)) + len(re.findall(r'\\begin\{equation\}', content))

        # 统计例题数量
        examples = len(re.findall(r'【例\d', content)) + len(re.findall(r'\[例\d', content))

        # 统计图表数量
        figures = len(re.findall(r'\[图\s*\d', content)) + len(re.findall(r'Figure\s*\d', content, re.I))
        tables = len(re.findall(r'\[表\s*\d', content)) + len(re.findall(r'Table\s*\d', content, re.I))

        # 统计新概念（粗略：加粗的术语）
        concepts = len(re.findall(r'\*\*[^*]{2,20}\*\*', content))

        # 统计参考文献
        references = len(re.findall(r'\[\d+\]', content))

        return {
            "equations": equations,
            "examples": examples,
            "figures": figures,
            "tables": tables,
            "concepts": min(concepts, 30),  # 限制合理范围
            "references": references,
        }

    async def step(self) -> str:
        """
        执行一步 — 调用 LLM 生成内容
        继承自 OpenManus BaseAgent
        """
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
