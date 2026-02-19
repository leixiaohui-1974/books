# 学术写作项目目录

本目录存放所有AI辅助学术写作的产出，由"学术写作助手"技能自动管理。

## 使用方式

### Claude Code
```bash
cd books/writing-projects
claude
# 然后自由对话，讨论思路 → 确认提纲 → 自动写作+评审+修改+推送
```

### claude.ai / ChatGPT
将 `CLAUDE.md` 的内容粘贴到对话开头，或上传为 Project Knowledge。

## 目录结构

```
writing-projects/
├── CLAUDE.md                          ← 主提示词（粘贴到任何AI即可使用）
├── academic-writer-skill/             ← 完整技能包（Claude Code专用）
│   ├── SKILL.md                       ← 详细技能规范
│   ├── agents/                        ← 各文体评审角色定义
│   │   ├── sci_reviewer.md
│   │   ├── cn_reviewer.md
│   │   ├── patent_reviewer.md
│   │   ├── book_reviewer.md
│   │   └── standard_report_reviewer.md
│   └── references/
│       └── workflow.md
├── 2026-MM-类型-项目名/               ← 各写作计划（自动创建）
│   ├── plan.md
│   ├── progress.json
│   └── 文档编号/
│       ├── draft_v01.md
│       ├── review_v01.md
│       ├── draft_v02.md
│       └── draft_final.md
└── README.md                          ← 本文件
```

## 支持的文档类型

| 类型 | 评审角色 | 达标条件 |
|------|---------|---------|
| SCI英文论文 | 理论+方法+工程 3审 | 连续2轮Minor/Accept |
| 中文核心论文 | 学科+工程+编辑 3审 | 连续2轮小修/录用 |
| 发明专利 | 审查员+代理人+技术专家 | 综合≥7.5/10 |
| 书稿/教材 | 教师+学者+工程师+国际读者 4审 | ≥8.0且无🔴 |
| 技术报告 | 技术审查+管理审查 2审 | ≥7.0/10 |
| 技术标准 | 标准化+技术+实施方 3审 | ≥8.0且合规100% |
