"""
HydroScribe Agent Tools — OpenManus 风格的工具注册

每个 Tool 继承 OpenManus BaseTool，可被 Writer/Reviewer/Utility Agent 调用。
工具分三类：
1. FileTools — 读写书稿、进度、术语表
2. QualityTools — 术语检查、一致性检查、参考文献检查
3. ContextTools — 上下文估算、分段准备
"""

from hydroscribe.tools.file_tools import (
    ReadChapterTool,
    WriteChapterTool,
    ReadProgressTool,
    UpdateProgressTool,
    ReadGlossaryTool,
)
from hydroscribe.tools.quality_tools import (
    CheckGlossaryTool,
    CheckConsistencyTool,
    CheckReferenceTool,
    CheckStructureTool,
)
from hydroscribe.tools.context_tools import (
    EstimateTokensTool,
    CompressContentTool,
    PrepareReviewContextTool,
)

__all__ = [
    "ReadChapterTool",
    "WriteChapterTool",
    "ReadProgressTool",
    "UpdateProgressTool",
    "ReadGlossaryTool",
    "CheckGlossaryTool",
    "CheckConsistencyTool",
    "CheckReferenceTool",
    "CheckStructureTool",
    "EstimateTokensTool",
    "CompressContentTool",
    "PrepareReviewContextTool",
]
