"""PatentWriterAgent — 发明专利写作智能体"""
from hydroscribe.agents.base_writer import BaseWriterAgent
from hydroscribe.schema import SkillType, WritingTask


class PatentWriterAgent(BaseWriterAgent):
    name: str = "writer-pat"
    description: str = "中国发明专利申请文件写作智能体"
    skill_type: SkillType = SkillType.PAT

    def _build_system_prompt(self, task: WritingTask) -> str:
        base_prompt = super()._build_system_prompt(task)
        return base_prompt + """
## 发明专利特殊要求
- 权利要求书：独立权利要求 + 从属权利要求
- 说明书：技术领域→背景技术→发明内容→附图说明→具体实施方式
- 摘要：≤ 300 字
- 权利要求书措辞严谨，避免使用"等"等模糊用语
- 需要突出与现有技术的区别特征
"""
