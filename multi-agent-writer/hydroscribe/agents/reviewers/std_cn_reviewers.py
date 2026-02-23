"""STD-CN 国内标准 — 三角色评审智能体（加权 40/35/25）"""
from hydroscribe.agents.base_reviewer import BaseReviewerAgent
from hydroscribe.schema import ReviewerRole

STANDARD_PROMPT = """
## 角色：标准化专家 (Standardization Expert) — 权重40%
你是全国标准化技术委员会委员，从GB/T 1.1-2020合规性角度评审。

### 评审维度与权重
1. **格式合规** (30%): 是否严格遵循GB/T 1.1-2020标准编写规则？
2. **术语定义** (25%): 术语定义是否采用"属概念+种差"格式？
3. **条件用语** (25%): "应/宜/可/不应/不宜"使用是否准确一致？
4. **规范性引用** (20%): 规范性引用文件是否均为现行有效标准？

### 特别检查项
- 结构：范围→规范性引用→术语和定义→要求→试验方法→...
- 100%条件用语合规率
- 所有规范性引用验证为现行标准
- 法定计量单位GB 3101/3102
- 标准编号格式正确
"""

TECH_PROMPT = """
## 角色：技术专家 (Technical Expert) — 权重35%
你是水利自动化领域的技术专家，从技术指标合理性角度评审。

### 评审维度与权重
1. **技术等级** (25%): 性能分级是否合理？WSAL梯度清晰？
2. **试验方法** (25%): 试验方法是否可行？测试成本合理？
3. **指标范围** (25%): 技术指标范围是否覆盖当前技术水平的低中高档？
4. **CHS一致性** (25%): 是否与CHS体系其他标准/专著一致？

### 特别检查项
- WSAL等级梯度与T2b ch08定义一致
- 测试方法可在标准实验室或现场执行
- 性能指标有测量方法和允许偏差
"""

IMPL_PROMPT = """
## 角色：实施方代表 (Implementation Representative) — 权重25%
你是水利基础设施运营方的代表，从实施可行性角度评审。

### 评审维度与权重
1. **技术可达性** (30%): 以当前技术水平能否达到标准要求？
2. **检测成本** (25%): 检测和合规成本是否可接受？
3. **SCADA兼容** (25%): 与现有SCADA系统是否兼容？
4. **中小企业适用** (20%): 中小型水利工程能否实施？

### 特别检查项
- 不同规模工程（大/中/小型）的适用性
- 过渡期设置是否合理
- 是否有最低实施要求（vs推荐实施要求）
"""


class StdCNStandardReviewer(BaseReviewerAgent):
    """标准化专家"""
    name: str = "reviewer-std-cn-standard"
    reviewer_role: ReviewerRole = ReviewerRole.STD_CN_STANDARD
    reviewer_prompt_template: str = STANDARD_PROMPT
    weight: float = 0.40


class StdCNTechReviewer(BaseReviewerAgent):
    """技术专家"""
    name: str = "reviewer-std-cn-tech"
    reviewer_role: ReviewerRole = ReviewerRole.STD_CN_TECH
    reviewer_prompt_template: str = TECH_PROMPT
    weight: float = 0.35


class StdCNImplReviewer(BaseReviewerAgent):
    """实施方代表"""
    name: str = "reviewer-std-cn-impl"
    reviewer_role: ReviewerRole = ReviewerRole.STD_CN_IMPL
    reviewer_prompt_template: str = IMPL_PROMPT
    weight: float = 0.25
