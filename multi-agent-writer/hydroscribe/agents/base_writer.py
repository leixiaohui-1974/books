"""
BaseWriterAgent — 写作智能体基类
继承 OpenManus 的 BaseAgent 架构，专用于 CHS 学术写作

上下文管理策略：
- 每个小节独立生成，避免单次请求过长
- 使用 ChunkWriter 做滑动窗口+累积摘要（不保留全文在对话中）
- 写完每节后清理对话历史，只保留摘要
"""

import asyncio
import os
import re
from typing import Any, Dict, List, Optional

from pydantic import Field

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'openmanus'))

from app.agent.base import BaseAgent as OpenManusBaseAgent
from app.schema import AgentState, Memory, Message

from hydroscribe.schema import (
    ChapterSpec, Event, EventType, ReviewScore,
    SkillType, WritingTask
)
from hydroscribe.engine.event_bus import EventBus
from hydroscribe.engine.context_manager import (
    ContextManager, ChunkWriter, ConversationCompressor, estimate_tokens
)


class BaseWriterAgent(OpenManusBaseAgent):
    """
    写作智能体基类 — 继承 OpenManus BaseAgent

    上下文管理关键设计：
    1. 每个小节独立 LLM 请求（不累积全文到对话历史）
    2. 使用累积摘要替代全文回顾（降低token消耗90%+）
    3. 写完一节后主动清理对话，只保留最近3轮+摘要
    4. 系统prompt中的术语/符号做智能截断
    """

    skill_type: SkillType = Field(default=SkillType.BK)
    event_bus: Optional[Any] = Field(default=None, exclude=True)

    glossary: str = Field(default="", description="术语表内容")
    symbols: str = Field(default="", description="符号表内容")
    style_guide: str = Field(default="", description="写作风格指南")
    prev_chapter_tail: str = Field(default="", description="前序章节末尾 500 字")
    review_feedback: str = Field(default="", description="上一轮评审意见（修改轮）")

    current_task: Optional[WritingTask] = Field(default=None, exclude=True)
    output_buffer: str = Field(default="", exclude=True)
    word_count: int = Field(default=0, exclude=True)

    # 上下文管理
    _context_manager: Optional[Any] = None
    _chunk_writer: Optional[Any] = None

    max_steps: int = 30

    class Config:
        arbitrary_types_allowed = True
        extra = "allow"

    def _get_context_manager(self) -> ContextManager:
        if self._context_manager is None:
            self._context_manager = ContextManager()
        return self._context_manager

    def _get_chunk_writer(self, task_id: str) -> ChunkWriter:
        ctx = self._get_context_manager()
        return ctx.get_chunk_writer(task_id)

    def _build_system_prompt(self, task: WritingTask) -> str:
        """
        构建 System Prompt：合并文体模板 + 章节规格 + 术语 + 风格
        子类可覆写以添加文体特定内容

        注意：术语和符号使用 ContextManager 做截断
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

        # 术语和符号由 ContextManager 控制截断
        if self.glossary:
            prompt_parts.append("## 术语规范（严格遵循，不得使用禁止别名）")
            prompt_parts.append(self.glossary[:3000])
            prompt_parts.append("")

        if self.symbols:
            prompt_parts.append("## 数学符号规范")
            prompt_parts.append(self.symbols[:2000])
            prompt_parts.append("")

        if self.prev_chapter_tail:
            prompt_parts.append("## 前序章节末尾（用于衔接）")
            prompt_parts.append(self.prev_chapter_tail[-1000:])
            prompt_parts.append("")

        if self.review_feedback:
            prompt_parts.append("## 上一轮评审意见（本次修改必须回应）")
            # 评审意见做智能截断，优先保留🔴和🟡
            feedback = self.review_feedback
            if estimate_tokens(feedback) > 5000:
                # 优先保留致命和重要问题
                lines = feedback.split("\n")
                priority_lines = [l for l in lines if "🔴" in l or "🟡" in l or l.startswith("[")]
                other_lines = [l for l in lines if l not in priority_lines]
                feedback = "\n".join(priority_lines[:50] + other_lines[:10])
            prompt_parts.append(feedback)
            prompt_parts.append("")

        return "\n".join(prompt_parts)

    async def write_chapter(self, task: WritingTask) -> Dict[str, Any]:
        """
        写一个完整章节 — 主入口

        上下文管理策略：
        1. 大纲生成：独立请求，完成后清理对话
        2. 每个小节：使用 ChunkWriter 准备上下文（滑动窗口+累积摘要）
        3. 写完一节后：更新摘要 + 清理对话历史
        """
        self.current_task = task
        self.output_buffer = ""
        self.word_count = 0

        # 初始化上下文管理
        chunk_writer = self._get_chunk_writer(task.id)
        chunk_writer.accumulated_summary = ""
        chunk_writer.section_count = 0
        chunk_writer.total_word_count = 0

        self.system_prompt = self._build_system_prompt(task)

        if self.event_bus:
            await self.event_bus.publish(Event(
                type=EventType.WRITING_STARTED,
                source_agent=self.name,
                book_id=task.book_id,
                chapter_id=task.chapter_id,
                payload={
                    "target_words": task.spec.target_words,
                    "title": task.spec.title,
                    "context_budget": self._get_context_manager().budget.total,
                }
            ))

        # ① 生成大纲（独立请求）
        outline = await self._generate_outline(task)

        # 清理大纲生成的对话历史
        self._reset_memory()

        # ② 按小节分段写作
        full_content = ""
        sections = []

        for i, section in enumerate(outline):
            # 用 ChunkWriter 准备上下文
            section_ctx = chunk_writer.prepare_section_context(
                outline=outline,
                section_index=i,
                prev_content=full_content,
                system_prompt=self._build_system_prompt(task),
                glossary=self.glossary,
                symbols=self.symbols,
                style_guide=self.style_guide,
                review_feedback=self.review_feedback if i == 0 else "",  # 评审意见只在第一节传
            )

            # 设置系统prompt（已截断）
            self.system_prompt = section_ctx["system_prompt"]

            # 写入小节
            section_content = await self._write_section_managed(
                task, section, i, len(outline), section_ctx["user_prompt"]
            )

            full_content += section_content + "\n\n"
            sections.append(section)

            # 更新累积摘要
            chunk_writer.update_summary(section, section_content)

            # 清理对话历史（关键！防止对话膨胀）
            self._reset_memory()

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
                        "progress": round(self.word_count / max(task.spec.target_words, 1) * 100, 1),
                        "context_tokens_used": section_ctx["context_tokens"],
                        "accumulated_summary_tokens": estimate_tokens(chunk_writer.accumulated_summary),
                    }
                ))

        self.output_buffer = full_content

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

        # 清理任务资源
        self._get_context_manager().cleanup_task(task.id)

        return result

    def _reset_memory(self):
        """重置对话历史 — 防止上下文膨胀"""
        try:
            self.memory = Memory()
        except Exception:
            pass

    async def _write_section_managed(
        self,
        task: WritingTask,
        section_title: str,
        section_index: int,
        total_sections: int,
        user_prompt: str,
    ) -> str:
        """使用上下文管理器写一个小节"""
        self.update_memory("user", user_prompt)
        result = await self.step()
        return result if result else ""

    async def _generate_outline(self, task: WritingTask) -> List[str]:
        """生成章节大纲"""
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

        lines = step_result.strip().split("\n") if step_result else []
        outline = [line.strip() for line in lines if line.strip() and any(c.isdigit() for c in line[:5])]

        if not outline:
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

    def _extract_metadata(self, content: str) -> Dict[str, Any]:
        """从写作内容中提取元数据"""
        equations = len(re.findall(r'\$\$[^$]+\$\$', content)) + len(re.findall(r'\\begin\{equation\}', content))
        examples = len(re.findall(r'【例\d', content)) + len(re.findall(r'\[例\d', content))
        figures = len(re.findall(r'\[图\s*\d', content)) + len(re.findall(r'Figure\s*\d', content, re.I))
        tables = len(re.findall(r'\[表\s*\d', content)) + len(re.findall(r'Table\s*\d', content, re.I))
        concepts = len(re.findall(r'\*\*[^*]{2,20}\*\*', content))
        references = len(re.findall(r'\[\d+\]', content))

        return {
            "equations": equations,
            "examples": examples,
            "figures": figures,
            "tables": tables,
            "concepts": min(concepts, 30),
            "references": references,
        }

    async def step(self) -> str:
        """执行一步 — 调用 LLM 生成内容"""
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
