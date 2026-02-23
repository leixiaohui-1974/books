"""PPTWriterAgent — 演示文稿写作智能体"""
from hydroscribe.agents.base_writer import BaseWriterAgent
from hydroscribe.schema import SkillType, WritingTask


class PPTWriterAgent(BaseWriterAgent):
    name: str = "writer-ppt"
    description: str = "演示文稿写作智能体，学术汇报/项目答辩/产品发布"
    skill_type: SkillType = SkillType.PPT

    def _build_system_prompt(self, task: WritingTask) -> str:
        base_prompt = super()._build_system_prompt(task)
        return base_prompt + """
## PPT 演示文稿特殊要求
- 每页幻灯片：标题 + 3-5 个要点 + 备注（演讲词）
- 总页数：15-25 页（20 分钟演讲）
- 结构：封面→目录→引言→核心内容→案例→总结→致谢→Q&A
- 每页文字 ≤ 50 字，核心观点用关键词而非长句
- 图表描述：每张图表附详细的内容描述和配色建议
- 过渡页：每个主要部分之间有过渡页
"""
