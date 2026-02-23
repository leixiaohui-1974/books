"""
HydroScribe Prompt Templates — 集中管理所有写作和评审提示词

设计原则：
- 每种文体(skill_type)一个模板文件
- 模板支持变量替换: {book_id}, {chapter_id}, {title}, {target_words}
- 提示词分层: 系统prompt → 文体prompt → 质量标准 → 写作指南
"""

import os
from typing import Dict, Optional

_TEMPLATES_DIR = os.path.dirname(__file__)


def load_template(name: str) -> str:
    """加载模板文件"""
    path = os.path.join(_TEMPLATES_DIR, f"{name}.md")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""


def render_template(name: str, **kwargs) -> str:
    """加载并渲染模板（变量替换）"""
    template = load_template(name)
    for key, value in kwargs.items():
        template = template.replace(f"{{{key}}}", str(value))
    return template


# 预定义模板名称
TEMPLATE_NAMES = {
    "system": "system_base",           # 基础系统prompt
    "quality_bk": "quality_textbook",  # 教材质量标准
    "quality_t1": "quality_t1",        # 先导版质量标准
    "quality_mono": "quality_monograph", # 专著质量标准
    "style_guide": "style_guide",      # 写作风格指南
    "review_format": "review_format",  # 评审输出格式
}
