"""SCIWriterAgent — SCI 英文论文写作智能体"""
from hydroscribe.agents.base_writer import BaseWriterAgent
from hydroscribe.schema import SkillType, WritingTask


class SCIWriterAgent(BaseWriterAgent):
    name: str = "writer-sci"
    description: str = "SCI英文论文写作智能体，面向WRR/Nature Water等国际顶刊"
    skill_type: SkillType = SkillType.SCI

    def _build_system_prompt(self, task: WritingTask) -> str:
        base_prompt = super()._build_system_prompt(task)
        return base_prompt + """
## SCI 论文特殊要求
- 语言：Academic English，正式但可读
- 参考文献 ≥ 30 篇，近 5 年占比 ≥ 50%
- 自引率 15-25%（含 Lei 2025a-d 系列）
- 所有公式必须编号，关键公式需推导过程
- 包含 Data Availability Statement
- Gap Statement 需精确指出现有方法的假设缺陷 + 量化影响
- Contribution 需显式编号列出 3 个贡献点（动词+对象+效果）
"""
