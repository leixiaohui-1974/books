"""StdCNWriterAgent — 国内技术标准写作智能体"""
from hydroscribe.agents.base_writer import BaseWriterAgent
from hydroscribe.schema import SkillType, WritingTask


class StdCNWriterAgent(BaseWriterAgent):
    name: str = "writer-std-cn"
    description: str = "国内技术标准写作智能体，遵循 GB/T 1.1-2020 编写格式"
    skill_type: SkillType = SkillType.STD_CN

    def _build_system_prompt(self, task: WritingTask) -> str:
        base_prompt = super()._build_system_prompt(task)
        return base_prompt + """
## 国内标准特殊要求
- 严格遵循 GB/T 1.1-2020《标准化工作导则 第1部分：标准化文件的结构和起草规则》
- 条文格式：用"应""宜""可""不应"等规范性动词
- 包含：范围→规范性引用文件→术语和定义→技术要求→检验方法
- 附录分为规范性附录和资料性附录
"""
