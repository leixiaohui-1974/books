"""
9 大文体对应的专业评审智能体
"""
from hydroscribe.agents.reviewers.book_reviewers import (
    InstructorReviewer, ExpertReviewer, EngineerReviewer, InternationalReviewer,
)
from hydroscribe.agents.reviewers.sci_reviewers import (
    SCIReviewerA, SCIReviewerB, SCIReviewerC,
)
from hydroscribe.agents.reviewers.cn_reviewers import (
    CNReviewerA, CNReviewerB, CNReviewerC,
)
from hydroscribe.agents.reviewers.patent_reviewers import (
    PatentExaminerReviewer, PatentAgentReviewer, PatentTechReviewer,
)
from hydroscribe.agents.reviewers.report_reviewers import (
    TechReviewer, MgmtReviewer,
)
from hydroscribe.agents.reviewers.std_cn_reviewers import (
    StdCNStandardReviewer, StdCNTechReviewer, StdCNImplReviewer,
)
from hydroscribe.agents.reviewers.std_int_reviewers import (
    StdIntISOReviewer, StdIntHydroReviewer, StdIntIndustryReviewer,
)
from hydroscribe.agents.reviewers.wechat_reviewers import (
    WXReaderReviewer, WXEditorReviewer, WXDomainReviewer,
)
from hydroscribe.agents.reviewers.ppt_reviewers import (
    PPTAudienceReviewer, PPTDesignReviewer, PPTContentReviewer,
)
from hydroscribe.schema import ReviewerRole

REVIEWER_REGISTRY = {
    # BK (书稿) — 4 角色
    ReviewerRole.INSTRUCTOR: InstructorReviewer,
    ReviewerRole.EXPERT: ExpertReviewer,
    ReviewerRole.ENGINEER: EngineerReviewer,
    ReviewerRole.INTERNATIONAL: InternationalReviewer,
    # SCI — 3 角色
    ReviewerRole.REVIEWER_A: SCIReviewerA,
    ReviewerRole.REVIEWER_B: SCIReviewerB,
    ReviewerRole.REVIEWER_C: SCIReviewerC,
    # CN — 3 角色
    ReviewerRole.CN_REVIEWER_A: CNReviewerA,
    ReviewerRole.CN_REVIEWER_B: CNReviewerB,
    ReviewerRole.CN_REVIEWER_C: CNReviewerC,
    # PAT — 3 角色
    ReviewerRole.PATENT_EXAMINER: PatentExaminerReviewer,
    ReviewerRole.PATENT_AGENT: PatentAgentReviewer,
    ReviewerRole.PATENT_TECH: PatentTechReviewer,
    # RPT — 2 角色
    ReviewerRole.TECH_REVIEWER: TechReviewer,
    ReviewerRole.MGMT_REVIEWER: MgmtReviewer,
    # STD-CN — 3 角色
    ReviewerRole.STD_CN_STANDARD: StdCNStandardReviewer,
    ReviewerRole.STD_CN_TECH: StdCNTechReviewer,
    ReviewerRole.STD_CN_IMPL: StdCNImplReviewer,
    # STD-INT — 3 角色
    ReviewerRole.STD_INT_ISO: StdIntISOReviewer,
    ReviewerRole.STD_INT_HYDRO: StdIntHydroReviewer,
    ReviewerRole.STD_INT_INDUSTRY: StdIntIndustryReviewer,
    # WX — 3 角色
    ReviewerRole.WX_READER: WXReaderReviewer,
    ReviewerRole.WX_EDITOR: WXEditorReviewer,
    ReviewerRole.WX_DOMAIN: WXDomainReviewer,
    # PPT — 3 角色
    ReviewerRole.PPT_AUDIENCE: PPTAudienceReviewer,
    ReviewerRole.PPT_DESIGN: PPTDesignReviewer,
    ReviewerRole.PPT_CONTENT: PPTContentReviewer,
}
