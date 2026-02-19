# 学术写作助手 (Academic Writer)

统一的"写—审—改—迭代"引擎，覆盖 **七大文体**，所有产出自动持久化到 GitHub。

## 支持的文档类型

| 代号 | 文体 | 说明 |
|------|------|------|
| `SCI` | SCI英文论文 | 针对WRR/Nature Water等国际顶刊 |
| `CN` | 中文核心期刊论文 | 针对水利学报/中国科学等 |
| `PAT` | 发明专利 | 中国发明专利申请文件 |
| `BK` | 书稿/专著/教材 | 章节制，逐章写作评审 |
| `RPT` | 技术报告/研究报告 | 项目报告、可研报告、技术方案 |
| `STD` | 技术标准 | 行业标准/团体标准/企业标准 |
| `WX` | 微信公众号文章 | 科普/行业分析/观点输出，手机阅读优化 |

## 目录结构

```
writing-projects/
├── CLAUDE.md                          # 主提示词（讨论模式+写作模式+GitHub持久化）
├── README.md                          # 本文件
├── academic-writer-skill/
│   ├── SKILL.md                       # 核心技能文件（七大文体完整规范）
│   ├── agents/                        # 各文体评审代理
│   │   ├── sci_reviewer.md            # SCI论文三角色评审
│   │   ├── cn_reviewer.md             # 中文核心期刊三角色评审
│   │   ├── patent_reviewer.md         # 发明专利三角色评审
│   │   ├── book_reviewer.md           # 书稿/教材四角色评审
│   │   ├── standard_report_reviewer.md # 技术标准+技术报告评审
│   │   └── wechat_reviewer.md         # 微信公众号文章三角色评审
│   ├── references/
│   │   └── workflow.md                # 工作流程参考（含七文体速查表）
│   └── scripts/
│       └── check_article.py           # 公众号文章自动质量检查（12项）
```

## 使用方式

### Claude.ai / ChatGPT
新对话开头粘贴 `CLAUDE.md` 全部内容，然后自由对话。

### Claude Code
将本目录放入工作目录：
```bash
cd ~/my-project
claude
> 开始SCI-P1a
> 写篇公众号
> 继续
```

### 核心指令
- `开始[类型][编号]` — 启动写作（如 `开始SCI-P1a`、`开始专利PF2-3`）
- `写篇公众号` — 启动公众号文章写作（进入WX模式）
- `继续` — 从断点恢复
- `状态` — 查看进度

## 公众号文章特殊工具

```bash
# 自动质量检查（12项检测，含段落长度、禁用词、错别字等）
python3 scripts/check_article.py article.md
```

## 版本记录

- v2.0 (2026-02-19): 整合公众号文章(WX)为第七文体，新增wechat_reviewer.md、check_article.py
- v1.0 (2026-02-19): 初始版本，6文体写审改闭环 + GitHub自动持久化
