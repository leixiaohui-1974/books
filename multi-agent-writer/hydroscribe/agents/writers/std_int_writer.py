"""StdIntWriterAgent — 国际技术标准写作智能体"""
from hydroscribe.agents.base_writer import BaseWriterAgent
from hydroscribe.schema import SkillType, WritingTask


class StdIntWriterAgent(BaseWriterAgent):
    name: str = "writer-std-int"
    description: str = "国际技术标准写作智能体，遵循 ISO/IEC Directives Part 2"
    skill_type: SkillType = SkillType.STD_INT

    def _build_system_prompt(self, task: WritingTask) -> str:
        base_prompt = super()._build_system_prompt(task)
        return base_prompt + """
## International Standard Requirements
- Follow ISO/IEC Directives Part 2 formatting rules
- Use "shall" / "should" / "may" / "shall not" normative verbs
- Structure: Scope → Normative references → Terms → Requirements → Test methods
- Language: English (formal, precise)
- Annexes classified as normative or informative
"""
