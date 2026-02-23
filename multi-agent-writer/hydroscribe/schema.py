"""
HydroScribe 数据模型 — 扩展 OpenManus schema
"""

import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# ── 写作技能类型（9大文体）──────────────────────────────────────────

class SkillType(str, Enum):
    """9 大写作技能类型，对应 academic-writer-skill 的 9 种文体"""
    BK = "BK"           # 书稿/教材/专著
    SCI = "SCI"         # SCI 英文论文
    CN = "CN"           # 中文核心期刊论文
    PAT = "PAT"         # 发明专利
    RPT = "RPT"         # 技术报告
    STD_CN = "STD-CN"   # 国内标准
    STD_INT = "STD-INT" # 国际标准
    WX = "WX"           # 微信公众号
    PPT = "PPT"         # 演示文稿


# ── 评审角色 ──────────────────────────────────────────────────────

class ReviewerRole(str, Enum):
    """评审角色，来自 CLAUDE.md §7 和 SKILL.md §2"""
    # BK (书稿) 四角色
    INSTRUCTOR = "instructor"       # 学科教师
    EXPERT = "expert"               # 学科专家
    ENGINEER = "engineer"           # 行业工程师
    INTERNATIONAL = "international" # 国际读者
    # SCI 三角色
    REVIEWER_A = "reviewer_a"       # 理论与创新性
    REVIEWER_B = "reviewer_b"       # 方法论与可重复性
    REVIEWER_C = "reviewer_c"       # 工程应用
    # CN 三角色
    CN_REVIEWER_A = "cn_reviewer_a"
    CN_REVIEWER_B = "cn_reviewer_b"
    CN_REVIEWER_C = "cn_reviewer_c"
    # PAT 三角色
    PATENT_EXAMINER = "patent_examiner"
    PATENT_AGENT = "patent_agent"
    PATENT_TECH = "patent_tech"
    # RPT 二角色
    TECH_REVIEWER = "tech_reviewer"
    MGMT_REVIEWER = "mgmt_reviewer"
    # STD-CN 三角色
    STD_CN_STANDARD = "std_cn_standard"
    STD_CN_TECH = "std_cn_tech"
    STD_CN_IMPL = "std_cn_impl"
    # STD-INT 三角色
    STD_INT_ISO = "std_int_iso"
    STD_INT_HYDRO = "std_int_hydro"
    STD_INT_INDUSTRY = "std_int_industry"
    # WX 三角色
    WX_READER = "wx_reader"
    WX_EDITOR = "wx_editor"
    WX_DOMAIN = "wx_domain"
    # PPT 三角色
    PPT_AUDIENCE = "ppt_audience"
    PPT_DESIGN = "ppt_design"
    PPT_CONTENT = "ppt_content"


# 每种文体对应的评审角色列表
SKILL_REVIEWERS: Dict[SkillType, List[ReviewerRole]] = {
    SkillType.BK: [ReviewerRole.INSTRUCTOR, ReviewerRole.EXPERT, ReviewerRole.ENGINEER, ReviewerRole.INTERNATIONAL],
    SkillType.SCI: [ReviewerRole.REVIEWER_A, ReviewerRole.REVIEWER_B, ReviewerRole.REVIEWER_C],
    SkillType.CN: [ReviewerRole.CN_REVIEWER_A, ReviewerRole.CN_REVIEWER_B, ReviewerRole.CN_REVIEWER_C],
    SkillType.PAT: [ReviewerRole.PATENT_EXAMINER, ReviewerRole.PATENT_AGENT, ReviewerRole.PATENT_TECH],
    SkillType.RPT: [ReviewerRole.TECH_REVIEWER, ReviewerRole.MGMT_REVIEWER],
    SkillType.STD_CN: [ReviewerRole.STD_CN_STANDARD, ReviewerRole.STD_CN_TECH, ReviewerRole.STD_CN_IMPL],
    SkillType.STD_INT: [ReviewerRole.STD_INT_ISO, ReviewerRole.STD_INT_HYDRO, ReviewerRole.STD_INT_INDUSTRY],
    SkillType.WX: [ReviewerRole.WX_READER, ReviewerRole.WX_EDITOR, ReviewerRole.WX_DOMAIN],
    SkillType.PPT: [ReviewerRole.PPT_AUDIENCE, ReviewerRole.PPT_DESIGN, ReviewerRole.PPT_CONTENT],
}

# 每种文体的达标条件
SKILL_THRESHOLDS: Dict[SkillType, Dict[str, Any]] = {
    SkillType.BK: {"min_score": 8.0, "max_iterations": 6, "no_red": True},
    SkillType.SCI: {"consecutive_minor": 2, "max_iterations": 20},
    SkillType.CN: {"consecutive_minor": 2, "max_iterations": 20},
    SkillType.PAT: {"min_score": 7.5, "max_iterations": 4},
    SkillType.RPT: {"min_score": 7.0, "max_iterations": 3},
    SkillType.STD_CN: {"min_score": 8.0, "max_iterations": 4, "compliance": True},
    SkillType.STD_INT: {"min_score": 8.0, "max_iterations": 4, "compliance": True},
    SkillType.WX: {"min_score": 7.5, "max_iterations": 5, "no_red": True},
    SkillType.PPT: {"min_score": 7.5, "max_iterations": 4, "no_red": True},
}


# ── Agent 状态 ────────────────────────────────────────────────────

class AgentStatus(str, Enum):
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"


# ── 事件系统 ──────────────────────────────────────────────────────

class EventType(str, Enum):
    # 任务生命周期
    TASK_CREATED = "task.created"
    TASK_STARTED = "task.started"
    TASK_COMPLETED = "task.completed"
    TASK_FAILED = "task.failed"
    # 写作过程
    WRITING_STARTED = "writing.started"
    WRITING_CHUNK = "writing.chunk"
    WRITING_DONE = "writing.done"
    # 评审过程
    REVIEW_STARTED = "review.started"
    REVIEW_SCORE = "review.score"
    REVIEW_DONE = "review.done"
    # 质量检查
    CHECK_GLOSSARY = "check.glossary"
    CHECK_CONSISTENCY = "check.consistency"
    CHECK_REFERENCE = "check.reference"
    # 门控
    GATE_WAITING = "gate.waiting"
    GATE_APPROVED = "gate.approved"
    GATE_REJECTED = "gate.rejected"
    # 迭代
    REVISION_NEEDED = "revision.needed"
    REVISION_ROUND = "revision.round"
    # 里程碑
    CHAPTER_COMPLETED = "chapter.completed"
    BOOK_COMPLETED = "book.completed"


class Event(BaseModel):
    """事件数据结构 — 所有 Agent 间通信的载体"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    type: EventType
    timestamp: datetime = Field(default_factory=datetime.now)
    source_agent: str
    target_agent: Optional[str] = None
    book_id: Optional[str] = None
    chapter_id: Optional[str] = None
    payload: Dict[str, Any] = Field(default_factory=dict)


# ── 写作任务 ──────────────────────────────────────────────────────

class ChapterSpec(BaseModel):
    """章节规格（从 CLAUDE.md 解析）"""
    chapter_id: str           # "ch07"
    title: str                # "模型预测控制（MPC）"
    target_words: int         # 40000
    core_content: str = ""    # 核心内容描述
    related_papers: str = ""  # 对应论文/专利


class WritingTask(BaseModel):
    """写作任务"""
    id: str = Field(default_factory=lambda: f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    book_id: str              # "T2a"
    chapter_id: str           # "ch07"
    skill_type: SkillType     # BK
    spec: ChapterSpec
    dependencies: List[str] = Field(default_factory=list)  # ["ch06"]
    reviewers: List[ReviewerRole] = Field(default_factory=list)
    max_iterations: int = 6
    gate_mode: str = "auto"   # "auto" | "human" | "hybrid"
    current_iteration: int = 0
    status: str = "pending"


# ── 评审结果 ──────────────────────────────────────────────────────

class ReviewScore(BaseModel):
    """单个评审角色的评分"""
    reviewer_role: str
    scores: Dict[str, float] = Field(default_factory=dict)  # {"coverage": 4, "difficulty": 3}
    overall: float = 0.0
    issues_red: List[str] = Field(default_factory=list)
    issues_yellow: List[str] = Field(default_factory=list)
    issues_green: List[str] = Field(default_factory=list)
    decision: str = ""  # "accept" | "minor" | "major" | "reject"
    comments: str = ""


class AggregatedReview(BaseModel):
    """汇总的评审结果"""
    reviews: List[ReviewScore] = Field(default_factory=list)
    avg_score: float = 0.0
    has_red_issues: bool = False
    passed: bool = False
    recommendation: str = ""  # "approve" | "revise" | "human_review"


# ── 进度追踪 ──────────────────────────────────────────────────────

class ChapterProgress(BaseModel):
    """章节进度（兼容 progress/BK[X].json 格式）"""
    status: str = "pending"  # pending | in_progress | review | revision | completed
    word_count: int = 0
    review_passed: bool = False
    review_scores: Dict[str, Optional[float]] = Field(default_factory=dict)
    last_updated: str = ""
    issues: List[str] = Field(default_factory=list)
    iterations: int = 0
    # Phase 9: 扩展元数据
    file_path: str = ""                                    # 终稿文件路径
    metadata: Dict[str, Any] = Field(default_factory=dict) # 公式/例题/图表/概念计数
    todo_count: int = 0                                    # [TODO] 标记数量
    validation_warnings: List[str] = Field(default_factory=list)  # 输出验证警告


class BookProgress(BaseModel):
    """整本书的进度"""
    book_id: str
    book_title: str
    total_chapters: int
    chapters: Dict[str, ChapterProgress] = Field(default_factory=dict)
    overall_progress: str = "0%"
