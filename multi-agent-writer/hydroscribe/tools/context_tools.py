"""
ContextTools — 上下文管理工具集

让 Agent 可以主动调用上下文估算和压缩能力。
"""

from typing import Any, Dict, List, Optional

from hydroscribe.engine.context_manager import (
    ContextManager, TextCompressor, estimate_tokens, TokenBudget
)


class EstimateTokensTool:
    """Token 数量估算工具"""

    name: str = "estimate_tokens"
    description: str = "估算文本的 token 数量。参数: text(str)"

    def execute(self, text: str) -> Dict[str, Any]:
        tokens = estimate_tokens(text)
        chars = len(text)
        return {
            "tokens": tokens,
            "characters": chars,
            "ratio": round(tokens / max(chars, 1), 3),
            "fits_in_context": tokens < 120000,
        }


class CompressContentTool:
    """内容压缩工具"""

    name: str = "compress_content"
    description: str = "按优先级压缩文本到指定 token 数。参数: text(str), max_tokens(int), priority(str='smart')"

    def __init__(self):
        self.compressor = TextCompressor()

    def execute(
        self, text: str, max_tokens: int = 50000, priority: str = "smart"
    ) -> Dict[str, Any]:
        original_tokens = estimate_tokens(text)

        if original_tokens <= max_tokens:
            return {
                "compressed": False,
                "original_tokens": original_tokens,
                "content": text,
            }

        compressed = self.compressor.truncate_with_priority(text, max_tokens, priority)
        compressed_tokens = estimate_tokens(compressed)

        return {
            "compressed": True,
            "original_tokens": original_tokens,
            "compressed_tokens": compressed_tokens,
            "reduction_pct": round((1 - compressed_tokens / original_tokens) * 100, 1),
            "content": compressed,
        }


class PrepareReviewContextTool:
    """评审上下文准备工具"""

    name: str = "prepare_review_context"
    description: str = "为评审准备合适大小的内容。长文自动分段。参数: content(str), review_prompt(str)"

    def __init__(self):
        self.ctx = ContextManager()

    def execute(self, content: str, review_prompt: str = "") -> Dict[str, Any]:
        chunker = self.ctx.get_review_chunker()
        segments = chunker.prepare_review_content(content, review_prompt)

        return {
            "segment_count": len(segments),
            "segments": [
                {
                    "segment": seg["segment"],
                    "tokens": estimate_tokens(seg["content"]),
                    "is_summary": seg.get("is_summary", False),
                }
                for seg in segments
            ],
            "needs_segmentation": len(segments) > 1,
        }
