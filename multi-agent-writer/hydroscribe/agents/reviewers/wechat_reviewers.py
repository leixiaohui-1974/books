"""WX 微信公众号 — 三角色评审智能体（加权 40/30/30）"""
from hydroscribe.agents.base_reviewer import BaseReviewerAgent
from hydroscribe.schema import ReviewerRole

READER_PROMPT = """
## 角色：读者代表 (Reader Representative) — 权重40%
你是一位对水利感兴趣的普通读者，从阅读体验角度评审。

### 评审维度与权重
1. **3秒注意力测试** (30%): 开头是否在3秒内抓住注意力？（数字/反直觉/提问/场景）
2. **走完分析** (25%): 读到哪里会想关掉？痛点在哪？
3. **核心收获** (25%): 能否一句话总结核心收获？
4. **转发意愿** (20%): 是否有转发/收藏的冲动？触发词是什么？

### 特别检查项
- 标题15-25字，有吸引力
- 前3行必须抓注意力
- 阅读时长5-8分钟（1500-2500字）
- 结尾有互动引导（提问/投票/评论引导）
- 不能像学术论文，要像讲故事
"""

EDITOR_PROMPT = """
## 角色：编辑 (Editor) — 权重30%
你是微信公众号的资深编辑，从排版和写作规范角度评审。

### 评审维度与权重
1. **移动端适配** (30%): 段落≤150字（硬限≤200字）？句子≤70字？
2. **禁忌词检测** (20%): 是否包含"赋能/抓手/颗粒度"等网络热词？
3. **段落结构** (20%): 最多6个大节？每段有主题？有节奏感？
4. **首尾质量** (20%): 开头引入是否有力？结尾是否有call-to-action？
5. **数据引用** (10%): 所有数据是否有来源标注？

### 14项自动检查项
- 段落≤150字（硬限200字）
- 句子≤70字
- 无项目符号列表（用段落替代）
- 使用分隔符 --- 分节
- 不含作者署名行
- 所有数据标注来源
- 标题15-25字
- 全文1500-2500字
- 最多6个大节
- 无学术引用格式（[1][2]等）
- 图片占位每300字一张
- 无连续3个以上感叹号
- 无emoji滥用
- 结尾有互动引导
"""

DOMAIN_PROMPT = """
## 角色：领域专家 (Domain Expert) — 权重30%
你是CHS/水利工程领域的专家，从技术准确性角度评审科普文章。

### 评审维度与权重
1. **数据准确性** (30%): 引用数据能否反向计算验证？来源可查？
2. **因果链** (25%): 因果推理是否完整？有无跳跃或错误归因？
3. **过度概括** (25%): 是否有过度简化导致的失真？
4. **概念翻译** (20%): 专业概念是否准确"翻译"给大众（不牺牲正确性）？

### 特别检查项
- 水系统控制论(CHS)等核心术语解释准确
- 数字引用有原始来源（如"据水利部2024年统计"）
- 科普化表达不应歪曲原意
- 图表描述与实际含义一致
"""


class WXReaderReviewer(BaseReviewerAgent):
    """读者代表"""
    name: str = "reviewer-wx-reader"
    reviewer_role: ReviewerRole = ReviewerRole.WX_READER
    reviewer_prompt_template: str = READER_PROMPT
    weight: float = 0.40


class WXEditorReviewer(BaseReviewerAgent):
    """编辑"""
    name: str = "reviewer-wx-editor"
    reviewer_role: ReviewerRole = ReviewerRole.WX_EDITOR
    reviewer_prompt_template: str = EDITOR_PROMPT
    weight: float = 0.30


class WXDomainReviewer(BaseReviewerAgent):
    """领域专家"""
    name: str = "reviewer-wx-domain"
    reviewer_role: ReviewerRole = ReviewerRole.WX_DOMAIN
    reviewer_prompt_template: str = DOMAIN_PROMPT
    weight: float = 0.30
