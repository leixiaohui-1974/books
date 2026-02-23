"""ReportWriterAgent — 技术报告写作智能体"""
from hydroscribe.agents.base_writer import BaseWriterAgent
from hydroscribe.schema import SkillType, WritingTask


class ReportWriterAgent(BaseWriterAgent):
    name: str = "writer-rpt"
    description: str = "技术报告/可研报告/技术方案写作智能体"
    skill_type: SkillType = SkillType.RPT

    def _build_system_prompt(self, task: WritingTask) -> str:
        base_prompt = super()._build_system_prompt(task)
        return base_prompt + """
## 技术报告特殊要求
- 结构：摘要→项目背景→技术方案→实施计划→预期成果→经费预算
- 语言：专业但不晦涩，面向项目评审专家和管理者
- 大量使用数据表格、甘特图描述、技术路线图
- 每个技术方案需附可行性分析
"""
