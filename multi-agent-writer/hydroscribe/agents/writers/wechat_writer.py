"""WeChatWriterAgent — 微信公众号文章写作智能体"""
from hydroscribe.agents.base_writer import BaseWriterAgent
from hydroscribe.schema import SkillType, WritingTask


class WeChatWriterAgent(BaseWriterAgent):
    name: str = "writer-wx"
    description: str = "微信公众号文章写作智能体，科普/行业分析/观点输出"
    skill_type: SkillType = SkillType.WX

    def _build_system_prompt(self, task: WritingTask) -> str:
        base_prompt = super()._build_system_prompt(task)
        return base_prompt + """
## 微信公众号特殊要求
- 标题：吸引力优先，15-25 字
- 开头：前 3 行必须抓住注意力（数据/故事/提问）
- 段落：每段 2-4 行（手机屏幕适配）
- 配图：每 300 字配一张图的描述占位
- 结尾：引导互动（提问/投票/评论引导）
- 阅读时长：控制在 5-8 分钟（1500-2500 字）
- 语气：专业但亲切，避免过于学术化
"""
