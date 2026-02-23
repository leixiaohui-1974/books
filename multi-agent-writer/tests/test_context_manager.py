"""
测试 ContextManager — 上下文长度管理

覆盖：
- Token 估算
- 文本压缩（head/tail/both/smart）
- 对话历史压缩
- 分段写作器
- 评审内容分段器
"""

import pytest
from hydroscribe.engine.context_manager import (
    estimate_tokens,
    TextCompressor,
    ConversationCompressor,
    ChunkWriter,
    ReviewChunker,
    ContextManager,
    TokenBudget,
)


class TestEstimateTokens:
    def test_empty_string(self):
        assert estimate_tokens("") == 0

    def test_chinese_text(self):
        text = "水系统控制论是一个新兴的交叉学科方向"
        tokens = estimate_tokens(text)
        assert tokens > 0
        assert tokens > len(text) // 5  # 中文token密度高

    def test_english_text(self):
        text = "Cybernetics of Hydro Systems is a new interdisciplinary field"
        tokens = estimate_tokens(text)
        assert tokens > 0

    def test_mixed_text(self):
        text = "水系统控制论(CHS)提出了八原理框架，包括Transfer Function等"
        tokens = estimate_tokens(text)
        assert tokens > 0

    def test_formula_text(self):
        text = "$$\\frac{\\partial A}{\\partial t} + \\frac{\\partial Q}{\\partial x} = q_l$$"
        tokens = estimate_tokens(text)
        assert tokens > 0


class TestTextCompressor:
    def setup_method(self):
        self.compressor = TextCompressor()

    def test_no_truncation_needed(self):
        text = "短文本"
        result = self.compressor.truncate_with_priority(text, 100000, "head")
        assert result == text

    def test_head_truncation(self):
        text = "A" * 10000
        result = self.compressor.truncate_with_priority(text, 100, "head")
        assert len(result) < len(text)
        assert result.startswith("A")
        assert "截断" in result or "..." in result

    def test_tail_truncation(self):
        text = "A" * 10000
        result = self.compressor.truncate_with_priority(text, 100, "tail")
        assert len(result) < len(text)
        assert result.endswith("A" * 10) or "A" in result[-20:]

    def test_both_truncation(self):
        text = "A" * 5000 + "B" * 5000
        result = self.compressor.truncate_with_priority(text, 100, "both")
        assert len(result) < len(text)
        assert "A" in result
        assert "B" in result

    def test_smart_truncation_preserves_headers(self):
        lines = ["# 重要标题", "普通段落" * 50, "## 次级标题", "普通段落" * 50]
        text = "\n".join(lines)
        result = self.compressor.truncate_with_priority(text, 200, "smart")
        assert "重要标题" in result

    def test_line_importance_header(self):
        score = TextCompressor._line_importance("# 第一章 绪论")
        assert score > 5

    def test_line_importance_formula(self):
        score = TextCompressor._line_importance("$$E = mc^2$$")
        assert score > 3

    def test_line_importance_empty(self):
        score = TextCompressor._line_importance("")
        assert score < 1

    def test_line_importance_definition(self):
        score = TextCompressor._line_importance("**水系统控制论**是一个新兴学科")
        assert score > 2

    def test_line_importance_review_marker(self):
        score = TextCompressor._line_importance("🔴 致命问题：公式推导有误")
        assert score > 5


class TestConversationCompressor:
    def setup_method(self):
        self.compressor = ConversationCompressor(max_history_tokens=500, keep_recent=2)

    def test_no_compression_needed(self):
        messages = [
            {"role": "user", "content": "写一段"},
            {"role": "assistant", "content": "好的"},
        ]
        result = self.compressor.compress(messages)
        assert len(result) == 2

    def test_compression_with_many_messages(self):
        messages = []
        for i in range(20):
            messages.append({"role": "user", "content": f"请求 {i} " + "x" * 200})
            messages.append({"role": "assistant", "content": f"回复 {i} " + "y" * 200})

        result = self.compressor.compress(messages)
        # 应该压缩了旧消息
        assert len(result) < len(messages)

    def test_system_messages_preserved(self):
        messages = [
            {"role": "system", "content": "你是写作助手"},
            {"role": "user", "content": "x" * 1000},
            {"role": "assistant", "content": "y" * 1000},
            {"role": "user", "content": "最近的请求"},
            {"role": "assistant", "content": "最近的回复"},
        ]
        result = self.compressor.compress(messages)
        system_msgs = [m for m in result if m["role"] == "system"]
        assert len(system_msgs) >= 1

    def test_empty_messages(self):
        result = self.compressor.compress([])
        assert result == []


class TestChunkWriter:
    def setup_method(self):
        self.writer = ChunkWriter()

    def test_prepare_section_context(self):
        outline = ["1.1 引言", "1.2 基本概念", "1.3 小结"]
        result = self.writer.prepare_section_context(
            outline=outline,
            section_index=0,
            prev_content="",
            system_prompt="你是写作助手",
            glossary="术语表",
            symbols="符号表",
            style_guide="写作风格",
        )
        assert "system_prompt" in result
        assert "user_prompt" in result
        assert result["context_tokens"] > 0
        assert "引言" in result["user_prompt"]
        assert "第一小节" in result["user_prompt"]

    def test_prepare_last_section(self):
        outline = ["1.1 引言", "1.2 小结"]
        result = self.writer.prepare_section_context(
            outline=outline,
            section_index=1,
            prev_content="前文内容",
            system_prompt="",
            glossary="",
            symbols="",
            style_guide="",
        )
        assert "最后一小节" in result["user_prompt"]

    def test_update_summary(self):
        self.writer.update_summary(
            "1.1 引言",
            "**水系统控制论**(CHS)是由雷晓辉教授提出的理论框架。因此，CHS是水利工程的未来方向。"
        )
        assert self.writer.section_count == 1
        assert self.writer.total_word_count > 0
        assert "引言" in self.writer.accumulated_summary

    def test_summary_compression(self):
        # 模拟大量小节，验证摘要不会无限增长
        for i in range(30):
            self.writer.update_summary(f"1.{i} 小节{i}", f"内容{'很长' * 100}")
        summary_tokens = estimate_tokens(self.writer.accumulated_summary)
        assert summary_tokens < 5000  # 应被压缩控制


class TestReviewChunker:
    def setup_method(self):
        self.chunker = ReviewChunker()

    def test_short_content_no_split(self):
        content = "短内容" * 100
        prompt = "评审指南"
        segments = self.chunker.prepare_review_content(content, prompt)
        assert len(segments) == 1
        assert segments[0]["segment"] == "1/1"

    def test_merge_single(self):
        reviews = [{"overall_score": 8.0, "issues_red": [], "issues_yellow": [], "comments": "好"}]
        result = self.chunker.merge_segment_reviews(reviews)
        assert result == reviews[0]

    def test_merge_multiple(self):
        reviews = [
            {"overall_score": 8.0, "issues_red": ["问题1"], "issues_yellow": [], "issues_green": [], "comments": "第1段"},
            {"overall_score": 7.0, "issues_red": [], "issues_yellow": ["建议1"], "issues_green": [], "comments": "第2段"},
        ]
        result = self.chunker.merge_segment_reviews(reviews)
        assert result["overall_score"] == 7.5
        assert len(result["issues_red"]) == 1
        assert len(result["issues_yellow"]) == 1
        assert result["segments_reviewed"] == 2


class TestContextManager:
    def test_init(self):
        ctx = ContextManager()
        assert ctx.budget.total > 0

    def test_get_chunk_writer(self):
        ctx = ContextManager()
        w1 = ctx.get_chunk_writer("task1")
        w2 = ctx.get_chunk_writer("task1")
        assert w1 is w2  # 同一任务返回同一实例

        w3 = ctx.get_chunk_writer("task2")
        assert w3 is not w1

    def test_estimate_budget_usage(self):
        ctx = ContextManager()
        usage = ctx.estimate_budget_usage(
            system_prompt="你是助手" * 100,
            user_prompt="请写一章" * 50,
        )
        assert usage["total_used"] > 0
        assert usage["remaining"] > 0
        assert 0 < usage["utilization"] < 100

    def test_cleanup_task(self):
        ctx = ContextManager()
        ctx.get_chunk_writer("temp_task")
        assert "temp_task" in ctx._chunk_writers
        ctx.cleanup_task("temp_task")
        assert "temp_task" not in ctx._chunk_writers
