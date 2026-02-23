"""
BookWriterAgent (BK) — 书稿/教材/专著 写作智能体
对应 SKILL.md §2.4 和 CLAUDE.md §8.1
"""

from hydroscribe.agents.base_writer import BaseWriterAgent
from hydroscribe.schema import SkillType, WritingTask


class BookWriterAgent(BaseWriterAgent):
    """
    书稿写作智能体

    特殊能力：
    - 生成学习目标（3-5 条）
    - 生成例题（已知→求解→解题过程→结果讨论）
    - 生成分级习题（基础题≥3 + 应用题≥2 + 思考题≥1）
    - 生成章末小结 + 拓展阅读
    - 遵循 CLAUDE.md §6.1 质量清单
    """

    name: str = "writer-bk"
    description: str = "书稿/教材/专著写作智能体，遵循研究生教材写作规范"
    skill_type: SkillType = SkillType.BK

    def _build_system_prompt(self, task: WritingTask) -> str:
        """覆写：添加书稿特有的写作要求"""
        base_prompt = super()._build_system_prompt(task)

        book_specific = """
## 书稿写作特殊要求（必须遵循）

### 章节结构
1. **章首学习目标**：3-5 条，用"掌握/理解/了解/能够"开头
2. **正文**：每段 200-400 字，一段一个中心思想，首句为主题句
3. **例题**：格式为「【例X-Y】已知→求解→解题过程→结果讨论」
4. **章末小结**：500 字以内，总结本章要点
5. **习题**：基础题≥3 + 应用题≥2 + 思考题≥1
6. **拓展阅读**：3-5 篇核心文献

### 数学公式呈现（三段式）
```
[物理直觉] 先用直觉语言解释
[公式] $$...$$
[工程解释] 每个符号的工程含义
```

### 概念密度控制
- 每章新概念 ≤ 10 个
- 每个新概念首次出现时有明确定义
- 每个新概念至少配 1 个例题或案例

### 禁止写法
- 禁止 "众所周知..." "显然..." "容易证明..."
- 禁止整页公式推导没有一句话解释
- 禁止多于 3 个连续公式之间没有文字衔接
"""
        return base_prompt + book_specific
