"""CNWriterAgent — 中文核心期刊论文写作智能体"""
from hydroscribe.agents.base_writer import BaseWriterAgent
from hydroscribe.schema import SkillType, WritingTask


class CNWriterAgent(BaseWriterAgent):
    name: str = "writer-cn"
    description: str = "中文核心期刊论文写作智能体，面向水利学报/中国科学等"
    skill_type: SkillType = SkillType.CN

    def _build_system_prompt(self, task: WritingTask) -> str:
        base_prompt = super()._build_system_prompt(task)
        return base_prompt + """
## 中文核心期刊论文特殊要求
- 语言：学术中文，参照 GB/T 7714-2015 引用格式
- 参考文献 ≥ 25 篇，英文文献占比 ≥ 30%
- 关键词：中英文各 3-8 个
- 摘要：中文 300-500 字 + 英文 Abstract
- 图表标题中英文对照
"""
