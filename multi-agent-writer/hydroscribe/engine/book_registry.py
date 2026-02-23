"""
书目注册表 — CHS 教材体系全部书目的规格数据

提供 book_id 验证、规格查询、层级信息等。
"""

from typing import Any, Dict, List, Optional


# ── 全部书目规格 ─────────────────────────────────────────────

BOOK_REGISTRY: Dict[str, Dict[str, Any]] = {
    # ── 第一层·种子 ──
    "T1-CN": {
        "title": "水系统控制论",
        "title_en": "",
        "tier": 1,
        "tier_name": "种子",
        "total_chapters": 8,
        "target_words": 150_000,
        "publisher": "中国水利水电出版社",
        "language": "zh",
        "skill_type": "BK",
        "priority": 5,
        "batch": 1,
    },
    "T1-EN": {
        "title": "Cybernetics of Hydro Systems: Principles and Perspectives",
        "title_en": "Cybernetics of Hydro Systems: Principles and Perspectives",
        "tier": 1,
        "tier_name": "种子",
        "total_chapters": 6,
        "target_words": 80_000,
        "publisher": "IAHR/CRC Press",
        "language": "en",
        "skill_type": "BK",
        "priority": 5,
        "batch": 1,
    },
    # ── 第二层·骨架 ──
    "T2a": {
        "title": "水系统控制论：建模与控制",
        "title_en": "Cybernetics of Hydro Systems: Modeling and Control",
        "tier": 2,
        "tier_name": "骨架",
        "total_chapters": 16,
        "target_words": 500_000,
        "publisher": "高等教育出版社 / Springer AIC",
        "language": "zh+en",
        "skill_type": "BK",
        "priority": 4,
        "batch": 2,
    },
    "T2b": {
        "title": "水系统控制论：智能与自主",
        "title_en": "Cybernetics of Hydro Systems: Intelligence and Autonomy",
        "tier": 2,
        "tier_name": "骨架",
        "total_chapters": 14,
        "target_words": 500_000,
        "publisher": "高等教育出版社 / Springer AIC",
        "language": "zh+en",
        "skill_type": "BK",
        "priority": 3,
        "batch": 2,
    },
    # ── 第三层·血肉 ──
    "M1": {
        "title": "明渠水动力降阶建模",
        "title_en": "Reduced-Order Modeling of Open-Channel Hydraulics",
        "tier": 3,
        "tier_name": "血肉",
        "total_chapters": 10,
        "target_words": 250_000,
        "publisher": "科学出版社 / Springer",
        "language": "zh+en",
        "skill_type": "SCI",
        "priority": 3,
        "batch": 3,
    },
    "M2": {
        "title": "水网预测控制",
        "title_en": "Predictive Control of Water Networks",
        "tier": 3,
        "tier_name": "血肉",
        "total_chapters": 12,
        "target_words": 300_000,
        "publisher": "科学出版社 / Springer AIC",
        "language": "zh+en",
        "skill_type": "SCI",
        "priority": 3,
        "batch": 3,
    },
    "M3": {
        "title": "水网运行安全包络",
        "title_en": "Safety Envelope for Water Network Operations",
        "tier": 3,
        "tier_name": "血肉",
        "total_chapters": 10,
        "target_words": 200_000,
        "publisher": "水利水电出版社 / CRC Press",
        "language": "zh+en",
        "skill_type": "SCI",
        "priority": 2,
        "batch": 3,
    },
    "M4": {
        "title": "水网多智能体系统",
        "title_en": "Multi-Agent Systems for Water Networks",
        "tier": 3,
        "tier_name": "血肉",
        "total_chapters": 10,
        "target_words": 250_000,
        "publisher": "电子工业出版社 / Springer",
        "language": "zh+en",
        "skill_type": "SCI",
        "priority": 2,
        "batch": 3,
    },
    "M5": {
        "title": "水利认知智能",
        "title_en": "Cognitive Intelligence for Water Systems",
        "tier": 3,
        "tier_name": "血肉",
        "total_chapters": 10,
        "target_words": 220_000,
        "publisher": "机械工业出版社 / CRC Press",
        "language": "zh+en",
        "skill_type": "SCI",
        "priority": 2,
        "batch": 3,
    },
    "M6": {
        "title": "水网控制在环验证",
        "title_en": "In-the-Loop Verification of Water Network Control",
        "tier": 3,
        "tier_name": "血肉",
        "total_chapters": 10,
        "target_words": 200_000,
        "publisher": "水利水电出版社 / IAHR",
        "language": "zh+en",
        "skill_type": "SCI",
        "priority": 2,
        "batch": 3,
    },
    "M7": {
        "title": "水网操作系统：HydroOS设计与实现",
        "title_en": "HydroOS: Design and Implementation of a Water Network Operating System",
        "tier": 3,
        "tier_name": "血肉",
        "total_chapters": 12,
        "target_words": 300_000,
        "publisher": "科学出版社 / IWA Publishing",
        "language": "zh+en",
        "skill_type": "SCI",
        "priority": 3,
        "batch": 3,
    },
    "M8": {
        "title": "水利工程自主运行实践——胶东调水与沙坪水电站",
        "title_en": "Autonomous Operation of Hydraulic Infrastructure",
        "tier": 3,
        "tier_name": "血肉",
        "total_chapters": 14,
        "target_words": 350_000,
        "publisher": "水利水电出版社 / Springer WSTL",
        "language": "zh+en",
        "skill_type": "SCI",
        "priority": 3,
        "batch": 3,
    },
    # ── 第四层·生态 ──
    "M9": {
        "title": "水系统运行工程导论",
        "title_en": "Introduction to Water Systems Operations Engineering",
        "tier": 4,
        "tier_name": "生态",
        "total_chapters": 12,
        "target_words": 250_000,
        "publisher": "高等教育出版社 / Cambridge UP",
        "language": "zh+en",
        "skill_type": "BK",
        "priority": 4,
        "batch": 2,
    },
    "M10": {
        "title": "水网智能控制实验",
        "title_en": "Laboratory Manual for Intelligent Water Network Control",
        "tier": 4,
        "tier_name": "生态",
        "total_chapters": 10,
        "target_words": 150_000,
        "publisher": "高等教育出版社",
        "language": "zh",
        "skill_type": "BK",
        "priority": 2,
        "batch": 3,
    },
}


def get_book_spec(book_id: str) -> Optional[Dict[str, Any]]:
    """获取指定书目的完整规格，不存在返回 None"""
    return BOOK_REGISTRY.get(book_id)


def validate_book_id(book_id: str) -> bool:
    """校验 book_id 是否存在于注册表"""
    return book_id in BOOK_REGISTRY


def list_book_ids() -> List[str]:
    """返回所有注册的 book_id 列表"""
    return sorted(BOOK_REGISTRY.keys())


def get_books_by_tier(tier: int) -> List[Dict[str, Any]]:
    """按层级获取书目列表"""
    return [
        {"book_id": bid, **spec}
        for bid, spec in BOOK_REGISTRY.items()
        if spec["tier"] == tier
    ]


def get_books_by_batch(batch: int) -> List[Dict[str, Any]]:
    """按批次获取书目列表"""
    return [
        {"book_id": bid, **spec}
        for bid, spec in BOOK_REGISTRY.items()
        if spec["batch"] == batch
    ]
