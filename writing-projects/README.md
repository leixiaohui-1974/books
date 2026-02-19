# 学术写作助手 (Academic Writer)

统一的"写—审—改—迭代"引擎，覆盖 **九大文体**，所有产出自动持久化到 GitHub。

## 支持的文档类型

| 代号 | 文体 | 说明 |
|------|------|------|
| `SCI` | SCI英文论文 | 针对WRR/Nature Water等国际顶刊 |
| `CN` | 中文核心期刊论文 | 针对水利学报/中国科学等 |
| `PAT` | 发明专利 | 中国发明专利申请文件 |
| `BK` | 书稿/专著/教材 | 章节制，逐章写作评审 |
| `RPT` | 技术报告/研究报告 | 项目报告、可研报告、技术方案 |
| `STD-CN` | 国内技术标准 | GB/T、SL/T、DB、T/ 行业标准/团体标准 |
| `STD-INT` | 国际技术标准 | ISO、IEC、OGC、IWA、IAHR技术报告 |
| `WX` | 微信公众号文章 | 科普/行业分析/观点输出，手机阅读优化 |
| `PPT` | 演示文稿 | 学术汇报/项目答辩/产品发布/国际会议演讲 |

## 目录结构

```
writing-projects/
├── CLAUDE.md                          # 主提示词（讨论模式+写作模式+GitHub持久化）
├── README.md                          # 本文件
├── academic-writer-skill/
│   ├── SKILL.md                       # 核心技能文件（九大文体完整规范）
│   ├── agents/                        # 各文体评审代理
│   │   ├── sci_reviewer.md            # SCI论文三角色评审
│   │   ├── cn_reviewer.md             # 中文核心期刊三角色评审
│   │   ├── patent_reviewer.md         # 发明专利三角色评审
│   │   ├── book_reviewer.md           # 书稿/教材四角色评审
│   │   ├── standard_report_reviewer.md # 技术报告评审
│   │   ├── std_cn_reviewer.md         # 国内标准三角色评审(GB/T 1.1)
│   │   ├── std_int_reviewer.md        # 国际标准三角色评审(ISO/IEC Directives)
│   │   ├── wechat_reviewer.md         # 微信公众号文章三角色评审
│   │   └── ppt_reviewer.md            # 演示文稿三角色评审
│   ├── references/
│   │   ├── workflow.md                # 工作流程参考（含九文体速查表）
│   │   └── ppt_style_guide.md         # PPT风格指南（配色/字体/排版/素材）
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
> 做个PPT
> 写个标准
> 继续
```

### 核心指令
- `开始[类型][编号]` — 启动写作（如 `开始SCI-P1a`、`开始专利PF2-3`）
- `写篇公众号` — 启动公众号文章写作（WX模式）
- `做个PPT` / `做个汇报` — 启动演示文稿制作（PPT模式，遵循风格指南）
- `写个标准` / `写行标` — 启动国内标准编写（STD-CN模式，GB/T 1.1规范）
- `write ISO standard` — 启动国际标准编写（STD-INT模式，ISO Directives）
- `继续` — 从断点恢复
- `状态` — 查看进度

## 特殊工具

```bash
# 公众号文章自动质量检查
python3 scripts/check_article.py article.md

# PPT生成（使用pptxgenjs）
node create_ppt.js
```

## 版本记录

- v3.0 (2026-02-19): 拆分STD为STD-CN+STD-INT，新增PPT文体+风格指南，九大文体体系
- v2.0 (2026-02-19): 整合公众号文章(WX)为第七文体
- v1.0 (2026-02-19): 初始版本，6文体写审改闭环 + GitHub自动持久化
