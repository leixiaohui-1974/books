"""
ContextManager — 上下文长度管理与压缩

核心问题：
- 一章目标3万字，加术语表/评审意见/前序章节，远超LLM上下文窗口
- 评审时需要看完整内容，但评审prompt本身也很长
- 多轮修改时历史对话会不断膨胀

解决策略（三层防线）：
1. 预算分配 — 按角色预分配token预算，强制截断
2. 渐进式压缩 — 对话历史超限时，自动摘要压缩旧消息
3. 分段处理 — 长文本分段送入，每段独立处理后合并

设计原则：
- 不依赖LLM做压缩（避免递归调用和额外成本）
- 使用规则 + 启发式方法做确定性压缩
- 保证关键信息（术语、公式、评审意见）不被丢失
"""

import hashlib
import json
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


# ── Token 估算 ────────────────────────────────────────────────

def estimate_tokens(text: str) -> int:
    """
    估算文本的token数量（无需tiktoken依赖）

    规则：
    - 中文：约1.5-2 token/字
    - 英文：约1.3 token/word
    - 代码/公式：约1 token/4字符
    """
    if not text:
        return 0

    # 分别统计中文字符、英文单词、其他字符
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    english_words = len(re.findall(r'[a-zA-Z]+', text))
    special_chars = len(re.findall(r'[^a-zA-Z\u4e00-\u9fff\s]', text))

    tokens = int(chinese_chars * 1.8 + english_words * 1.3 + special_chars * 0.5)
    return max(tokens, len(text) // 4)  # 下限保护


# ── Token 预算 ────────────────────────────────────────────────

@dataclass
class TokenBudget:
    """各组件的token预算分配"""
    total: int = 120000              # 总预算（Claude约200K，留余量）
    system_prompt: int = 8000        # 系统prompt
    glossary: int = 3000             # 术语表
    symbols: int = 2000              # 符号表
    style_guide: int = 2000          # 写作风格
    prev_chapter: int = 2000         # 前序章节末尾
    review_feedback: int = 5000      # 评审意见
    conversation_history: int = 15000 # 对话历史
    current_content: int = 40000     # 当前正在写的内容
    output_reserve: int = 8000       # 留给输出的空间

    # 评审模式的特殊预算
    review_system_prompt: int = 6000  # 评审系统prompt
    review_content: int = 60000       # 待评审内容（更大份额）
    review_output: int = 4000         # 评审输出

    @property
    def writing_available(self) -> int:
        """写作时可用于内容的token数"""
        used = (self.system_prompt + self.glossary + self.symbols +
                self.style_guide + self.prev_chapter + self.review_feedback +
                self.output_reserve)
        return self.total - used

    @property
    def review_available(self) -> int:
        """评审时可用于内容的token数"""
        used = self.review_system_prompt + self.review_output
        return self.total - used


# ── 文本截断与压缩 ────────────────────────────────────────────

class TextCompressor:
    """文本压缩器 — 保留关键信息的智能截断"""

    @staticmethod
    def truncate_with_priority(text: str, max_tokens: int, priority: str = "tail") -> str:
        """
        按优先级截断文本

        priority:
        - "head": 保留开头（适合正文开头、引言）
        - "tail": 保留末尾（适合前序章节、对话历史）
        - "both": 保留首尾（适合术语表、概览性内容）
        - "smart": 智能截断（保留标题/公式/关键词，压缩普通段落）
        """
        current_tokens = estimate_tokens(text)
        if current_tokens <= max_tokens:
            return text

        # 按字符估算截断点（粗略：1 token ≈ 2-3 中文字符）
        char_limit = int(max_tokens * 2.5)

        if priority == "head":
            return text[:char_limit] + "\n\n[...内容已截断，保留前部...]"

        elif priority == "tail":
            return "[...内容已截断，保留后部...]\n\n" + text[-char_limit:]

        elif priority == "both":
            half = char_limit // 2
            return text[:half] + "\n\n[...中间内容已省略...]\n\n" + text[-half:]

        elif priority == "smart":
            return TextCompressor._smart_truncate(text, char_limit)

        return text[:char_limit]

    @staticmethod
    def _smart_truncate(text: str, char_limit: int) -> str:
        """
        智能截断：保留高信息密度的内容，压缩低密度段落

        优先保留：
        1. 标题行（# ## ### 等）
        2. 数学公式（$...$, $$...$$）
        3. 定义（**加粗术语**）
        4. 代码块
        5. 图表标记
        6. 参考文献
        """
        lines = text.split("\n")
        scored_lines: List[Tuple[float, int, str]] = []

        for i, line in enumerate(lines):
            score = TextCompressor._line_importance(line)
            scored_lines.append((score, i, line))

        # 按重要性排序，优先保留高分行
        scored_lines.sort(key=lambda x: -x[0])

        kept_chars = 0
        kept_indices = set()

        for score, idx, line in scored_lines:
            line_chars = len(line) + 1  # +1 for newline
            if kept_chars + line_chars > char_limit:
                break
            kept_indices.add(idx)
            kept_chars += line_chars

        # 按原始顺序输出
        result_lines = []
        prev_kept = -1
        for i, line in enumerate(lines):
            if i in kept_indices:
                if prev_kept >= 0 and i - prev_kept > 1:
                    result_lines.append("[...]")  # 省略标记
                result_lines.append(line)
                prev_kept = i

        return "\n".join(result_lines)

    @staticmethod
    def _line_importance(line: str) -> float:
        """计算单行的信息密度/重要性评分"""
        score = 1.0
        stripped = line.strip()

        if not stripped:
            return 0.1  # 空行

        # 标题
        if re.match(r'^#{1,6}\s', stripped):
            level = len(re.match(r'^(#+)', stripped).group(1))
            score += 10 - level  # h1=9, h2=8, ...

        # 数学公式
        if '$$' in stripped or re.search(r'\$[^$]+\$', stripped):
            score += 5
        if '\\begin{equation}' in stripped:
            score += 5

        # 定义/术语（加粗）
        if '**' in stripped:
            score += 3

        # 代码块
        if stripped.startswith('```'):
            score += 2

        # 图表标记
        if re.search(r'\[图\s*\d|Figure\s*\d|表\s*\d|Table\s*\d', stripped, re.I):
            score += 4

        # 例题
        if re.match(r'【例\d|^\[例\d', stripped):
            score += 4

        # 学习目标/小结
        if any(kw in stripped for kw in ["学习目标", "本章小结", "习题", "拓展阅读"]):
            score += 3

        # 参考文献
        if re.match(r'^\[\d+\]', stripped):
            score += 2

        # 评审意见标记
        if any(marker in stripped for marker in ["🔴", "🟡", "🟢", "致命", "重要"]):
            score += 6

        return score


# ── 对话历史压缩 ──────────────────────────────────────────────

class ConversationCompressor:
    """
    对话历史压缩器

    策略：
    1. 保留最近N轮完整对话
    2. 对更早的对话做摘要压缩
    3. 特殊消息（系统消息、评审结果）永远保留关键信息
    """

    def __init__(self, max_history_tokens: int = 15000, keep_recent: int = 3):
        self.max_history_tokens = max_history_tokens
        self.keep_recent = keep_recent

    def compress(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        压缩对话历史

        Args:
            messages: [{"role": "user"/"assistant", "content": "..."}]

        Returns:
            压缩后的消息列表
        """
        if not messages:
            return messages

        total_tokens = sum(estimate_tokens(m.get("content", "")) for m in messages)
        if total_tokens <= self.max_history_tokens:
            return messages

        # 分为三部分：系统消息 | 旧消息 | 近期消息
        system_msgs = [m for m in messages if m.get("role") == "system"]
        non_system = [m for m in messages if m.get("role") != "system"]

        # 保留最近N轮（1轮=user+assistant）
        recent_count = min(self.keep_recent * 2, len(non_system))
        recent = non_system[-recent_count:]
        old = non_system[:-recent_count] if recent_count < len(non_system) else []

        if not old:
            return messages

        # 对旧消息做摘要
        summary = self._summarize_old_messages(old)

        # 组合：系统消息 + 摘要 + 近期消息
        result = system_msgs.copy()
        if summary:
            result.append({
                "role": "user",
                "content": f"[对话历史摘要]\n{summary}\n[摘要结束，以下为最近的对话]",
            })
        result.extend(recent)

        return result

    def _summarize_old_messages(self, messages: List[Dict[str, str]]) -> str:
        """对旧消息做规则摘要（不调用LLM）"""
        summary_parts = []

        for msg in messages:
            role = msg.get("role", "")
            content = msg.get("content", "")

            if role == "user":
                # 提取用户请求的关键动作
                first_line = content.split("\n")[0][:200]
                summary_parts.append(f"- 用户请求: {first_line}")

            elif role == "assistant":
                # 提取助手回复的核心结果
                # 优先提取标题/结论
                headers = re.findall(r'^#{1,3}\s+(.+)', content, re.M)
                if headers:
                    summary_parts.append(f"- 完成: {', '.join(headers[:3])}")
                else:
                    first_line = content.split("\n")[0][:200]
                    summary_parts.append(f"- 回复: {first_line}")

        return "\n".join(summary_parts[-20:])  # 最多保留20条摘要


# ── 分段写作管理器 ────────────────────────────────────────────

class ChunkWriter:
    """
    分段写作管理器

    解决问题：单次LLM输出有长度限制（通常4K-8K token），
    但一章内容可能需要2万-5万字。

    策略：
    1. 按大纲分段：每个小节独立请求
    2. 滑动窗口：每段携带前文末尾（衔接）+ 后文提示（预告）
    3. 累积摘要：写完一段后更新摘要，下一段携带摘要而非全文
    """

    def __init__(self, budget: Optional[TokenBudget] = None):
        self.budget = budget or TokenBudget()
        self.compressor = TextCompressor()
        self.accumulated_summary = ""
        self.section_count = 0
        self.total_word_count = 0

    def prepare_section_context(
        self,
        outline: List[str],
        section_index: int,
        prev_content: str,
        system_prompt: str,
        glossary: str,
        symbols: str,
        style_guide: str,
        review_feedback: str = "",
    ) -> Dict[str, str]:
        """
        为每个小节准备上下文（在token预算内）

        Returns:
            {
                "system_prompt": str,   # 截断后的系统prompt
                "user_prompt": str,     # 写作请求
                "context_tokens": int,  # 已用token
            }
        """
        budget = self.budget

        # 1. 压缩各组件到预算内
        system_prompt = self.compressor.truncate_with_priority(
            system_prompt, budget.system_prompt, "head"
        )
        glossary = self.compressor.truncate_with_priority(
            glossary, budget.glossary, "smart"
        )
        symbols = self.compressor.truncate_with_priority(
            symbols, budget.symbols, "smart"
        )
        style_guide = self.compressor.truncate_with_priority(
            style_guide, budget.style_guide, "head"
        )

        # 2. 前文衔接（滑动窗口）
        if prev_content:
            tail_budget = budget.prev_chapter
            if self.accumulated_summary:
                # 有摘要时，前文窗口可以更小
                tail_budget = budget.prev_chapter // 2
            prev_tail = self.compressor.truncate_with_priority(
                prev_content, tail_budget, "tail"
            )
        else:
            prev_tail = ""

        # 3. 评审意见（如果是修改轮）
        if review_feedback:
            review_feedback = self.compressor.truncate_with_priority(
                review_feedback, budget.review_feedback, "smart"
            )

        # 4. 构建用户请求
        current_section = outline[section_index] if section_index < len(outline) else ""
        total_sections = len(outline)
        words_per_section = 30000 // max(total_sections, 1)  # 默认每章3万字

        user_parts = [
            f"现在请撰写「{current_section}」这一小节。",
            f"约 {words_per_section} 字。",
            f"进度: 第{section_index + 1}/{total_sections}节。",
        ]

        if section_index == 0:
            user_parts.append("这是本章第一小节，需包含引导性内容和学习目标。")
        if section_index == total_sections - 1:
            user_parts.append("这是本章最后一小节，需包含本章小结、习题和拓展阅读。")

        # 附加摘要（已写部分的概要）
        if self.accumulated_summary:
            user_parts.append(f"\n已写内容概要:\n{self.accumulated_summary}")

        # 附加前文末尾（衔接用）
        if prev_tail:
            user_parts.append(f"\n前文末尾（请衔接）:\n...{prev_tail}")

        # 附加下一节预告
        if section_index + 1 < total_sections:
            next_section = outline[section_index + 1]
            user_parts.append(f"\n下一节预告: {next_section}")

        # 组装系统prompt
        full_system = "\n\n".join(filter(None, [
            system_prompt,
            f"## 术语规范\n{glossary}" if glossary else "",
            f"## 符号规范\n{symbols}" if symbols else "",
            f"## 写作风格\n{style_guide}" if style_guide else "",
            f"## 评审修改意见\n{review_feedback}" if review_feedback else "",
        ]))

        user_prompt = "\n".join(user_parts)

        context_tokens = estimate_tokens(full_system) + estimate_tokens(user_prompt)

        return {
            "system_prompt": full_system,
            "user_prompt": user_prompt,
            "context_tokens": context_tokens,
            "available_output_tokens": budget.total - context_tokens,
        }

    def update_summary(self, section_title: str, section_content: str):
        """
        写完一个小节后，更新累积摘要（替代保留全文）

        用规则提取小节的关键信息：
        - 标题
        - 定义的概念
        - 关键公式
        - 结论/要点
        """
        summary_parts = [f"### {section_title}"]

        # 提取定义（加粗的术语）
        definitions = re.findall(r'\*\*([^*]{2,30})\*\*', section_content)
        if definitions:
            summary_parts.append(f"概念: {', '.join(definitions[:5])}")

        # 提取公式编号
        equations = re.findall(r'\((\d+-\d+)\)', section_content)
        if equations:
            summary_parts.append(f"公式: 式({'), 式('.join(equations[:5])})")

        # 提取结论性语句（含"因此"/"综上"/"可得"等）
        conclusions = re.findall(r'(?:因此|综上|可得|结论是|总之)[，,：:](.{10,80})', section_content)
        if conclusions:
            summary_parts.append(f"结论: {conclusions[0]}")

        # 字数统计
        word_count = len(section_content)
        summary_parts.append(f"({word_count}字)")

        self.section_count += 1
        self.total_word_count += word_count

        # 更新摘要（控制总长度）
        new_entry = " | ".join(summary_parts)
        if self.accumulated_summary:
            self.accumulated_summary += f"\n{new_entry}"
        else:
            self.accumulated_summary = new_entry

        # 如果摘要本身太长，压缩它
        if estimate_tokens(self.accumulated_summary) > 3000:
            lines = self.accumulated_summary.split("\n")
            # 保留最近10条，旧的只保留标题
            if len(lines) > 10:
                old_titles = [l.split("|")[0].strip() for l in lines[:-10]]
                self.accumulated_summary = (
                    "前文: " + " → ".join(old_titles) +
                    "\n" + "\n".join(lines[-10:])
                )


# ── 评审内容分段器 ────────────────────────────────────────────

class ReviewChunker:
    """
    评审内容分段器

    问题：一章3万字，评审prompt也2000字，加起来超限
    策略：
    1. 短内容（<15K字）：整体评审
    2. 中等内容（15K-30K字）：压缩后整体评审
    3. 长内容（>30K字）：分段评审后合并
    """

    def __init__(self, budget: Optional[TokenBudget] = None):
        self.budget = budget or TokenBudget()
        self.compressor = TextCompressor()

    def prepare_review_content(
        self,
        content: str,
        review_prompt: str,
    ) -> List[Dict[str, str]]:
        """
        准备评审内容（可能分段）

        Returns:
            [{"content": str, "segment": "1/3", "is_summary": False}, ...]
        """
        content_tokens = estimate_tokens(content)
        prompt_tokens = estimate_tokens(review_prompt)
        available = self.budget.review_available - prompt_tokens

        if content_tokens <= available:
            # 整体评审
            return [{"content": content, "segment": "1/1", "is_summary": False}]

        # 尝试智能压缩
        compressed = self.compressor.truncate_with_priority(content, available, "smart")
        compressed_tokens = estimate_tokens(compressed)

        if compressed_tokens <= available:
            return [{"content": compressed, "segment": "1/1", "is_summary": True}]

        # 分段评审
        segments = self._split_by_sections(content, available)
        result = []
        for i, seg in enumerate(segments):
            result.append({
                "content": seg,
                "segment": f"{i+1}/{len(segments)}",
                "is_summary": False,
            })
        return result

    def _split_by_sections(self, content: str, max_tokens_per_segment: int) -> List[str]:
        """按章节/小节边界分段"""
        # 按 ## 或 ### 标题分段
        sections = re.split(r'(?=^##\s)', content, flags=re.M)
        if len(sections) <= 1:
            # 没有明显分段，按字数强制切分
            char_limit = int(max_tokens_per_segment * 2.5)
            return [content[i:i+char_limit] for i in range(0, len(content), char_limit)]

        # 贪心合并：尽量多的小节放一个segment
        segments = []
        current = ""
        for section in sections:
            if estimate_tokens(current + section) > max_tokens_per_segment and current:
                segments.append(current)
                current = section
            else:
                current += section
        if current:
            segments.append(current)

        return segments

    def merge_segment_reviews(self, segment_reviews: List[Dict]) -> Dict:
        """合并分段评审结果"""
        if len(segment_reviews) == 1:
            return segment_reviews[0]

        # 合并各段的评审
        all_red = []
        all_yellow = []
        all_green = []
        scores = []
        comments = []

        for review in segment_reviews:
            all_red.extend(review.get("issues_red", []))
            all_yellow.extend(review.get("issues_yellow", []))
            all_green.extend(review.get("issues_green", []))
            if review.get("overall_score"):
                scores.append(review["overall_score"])
            if review.get("comments"):
                comments.append(review["comments"])

        avg_score = sum(scores) / max(len(scores), 1) if scores else 5.0

        return {
            "overall_score": round(avg_score, 1),
            "issues_red": all_red,
            "issues_yellow": all_yellow,
            "issues_green": all_green,
            "comments": " | ".join(comments[:3]),
            "decision": "major" if all_red else ("minor" if all_yellow else "accept"),
            "segments_reviewed": len(segment_reviews),
        }


# ── 全局上下文管理器 ──────────────────────────────────────────

class ContextManager:
    """
    全局上下文管理器 — 协调所有组件的token使用

    使用方式：
        ctx = ContextManager(model_context_limit=200000)

        # 写作时
        chunk_writer = ctx.get_chunk_writer()
        section_ctx = chunk_writer.prepare_section_context(...)

        # 评审时
        review_chunker = ctx.get_review_chunker()
        segments = review_chunker.prepare_review_content(...)

        # 对话压缩
        compressed = ctx.compress_conversation(messages)
    """

    def __init__(self, model_context_limit: int = 200000):
        # Claude 的实际限制约200K token，预留安全边际
        safe_limit = int(model_context_limit * 0.85)

        self.budget = TokenBudget(total=safe_limit)
        self.conversation_compressor = ConversationCompressor(
            max_history_tokens=self.budget.conversation_history
        )
        self._chunk_writers: Dict[str, ChunkWriter] = {}
        self._review_chunker = ReviewChunker(budget=self.budget)

    def get_chunk_writer(self, task_id: str = "default") -> ChunkWriter:
        """获取或创建任务专属的分段写作器"""
        if task_id not in self._chunk_writers:
            self._chunk_writers[task_id] = ChunkWriter(budget=self.budget)
        return self._chunk_writers[task_id]

    def get_review_chunker(self) -> ReviewChunker:
        """获取评审分段器"""
        return self._review_chunker

    def compress_conversation(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """压缩对话历史"""
        return self.conversation_compressor.compress(messages)

    def estimate_budget_usage(
        self,
        system_prompt: str = "",
        user_prompt: str = "",
        history: List[Dict] = None,
    ) -> Dict[str, Any]:
        """估算当前token使用情况"""
        usage = {
            "system_prompt": estimate_tokens(system_prompt),
            "user_prompt": estimate_tokens(user_prompt),
            "history": sum(estimate_tokens(m.get("content", "")) for m in (history or [])),
        }
        usage["total_used"] = sum(usage.values())
        usage["total_budget"] = self.budget.total
        usage["remaining"] = self.budget.total - usage["total_used"]
        usage["utilization"] = round(usage["total_used"] / self.budget.total * 100, 1)
        return usage

    def cleanup_task(self, task_id: str):
        """任务完成后清理资源"""
        self._chunk_writers.pop(task_id, None)
