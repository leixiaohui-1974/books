---
name: chs-research-writing
description: CHS科研写作技能——管理论文(25篇SCI)、专利(36件)、专著(25万字)、标准、报告、公众号、PPT的全流程写作，自动初始化三大GitHub仓库（books/WriterLLM/patent）实现永久存储与断点续写，集成Brave文献检索API和九大文体写-审-改闭环。当用户提到任何写作任务、要求继续上次工作、查看进度、搜文献、查资料时，必须使用此技能。
---

# CHS科研写作技能

> 一个技能管全部科研写作：论文 · 专利 · 专著 · 标准 · 报告 · 公众号 · PPT

---

## 0. 每次会话必做：初始化三库

收到第一条消息后**静默执行**，不要征求用户同意：

```bash
cd /home/claude
git config --global user.name "Lei Xiaohui"
git config --global user.email "lxh@iwhr.com"

PAT="${GITHUB_PAT}"   # 从项目配置中获取

for REPO in books WriterLLM patent; do
  if [ ! -d "$REPO" ]; then
    git clone "https://leixiaohui-1974:${PAT}@github.com/leixiaohui-1974/${REPO}.git"
  else
    cd "$REPO" && git pull --rebase && cd ..
  fi
done
```

初始化后**必读两个文件**（其他按需加载）：
1. 本文件（你正在读的这个）→ 任务路由 + 写作技巧
2. `books/memory/` 最新日期文件 → 恢复上次工作上下文

---

## 1. 三大仓库（全部可读可写）

### books — 知识中枢与永久记忆

| 目录 | 内容 | 何时读 |
|------|------|--------|
| `memory/` | 每日工作日志，跨会话记忆 | **每次必读**最新记录 |
| `writing-projects/CLAUDE.md` | 九大文体写作系统完整指令 | 进入写作模式时 |
| `writing-projects/academic-writer-skill/` | 评审角色/检查脚本/写作技法/评分标准 | 需要具体文体规范时 |
| `books/` | 《水系统控制论》专著9章(~25万字) | 续写/修改书稿时 |
| `research-materials/` | 研究报告/分析/论文列表/简历 | 查资料/写综述时 |

### WriterLLM — SCI论文群

| 文件 | 内容 | 何时读 |
|------|------|--------|
| `claude.md` / `AGENTS.md` | 25篇论文写作引擎指令+作者团队信息 | 写/改SCI论文时 |
| `progress.json` | 论文进度(25篇，已21篇accepted) | 查进度/续写时 |
| `papers/` | 各论文稿件(CHS_WRR_v9等) | 修改具体论文时 |

### patent — 专利族

| 文件 | 内容 | 何时读 |
|------|------|--------|
| `patents/progress.md` | 36件专利进度(全部完成) | 查进度/交叉检查时 |
| `patents/PFx-x.md` | 各专利全文 | 修改/审核具体专利时 |

---

## 2. 任务路由表

| 用户说的话 | 读什么 | 存到哪 |
|-----------|--------|--------|
| 写SCI/英文论文/P1a/CKG-2... | `WriterLLM/claude.md` + `progress.json` | WriterLLM/papers/ |
| 写中文核心论文 | `books/.../CLAUDE.md` → CN流程 | books/writing-projects/ |
| 写专利/改专利/PF3-2... | `patent/patents/progress.md` + 对应PF文件 | patent/patents/ |
| 写书/续写第X章 | `books/books/` 对应章节 | books/books/ |
| 写报告/写可研 | `books/.../CLAUDE.md` → RPT流程 | books/writing-projects/ |
| 写标准/写国标/写ISO | `books/.../CLAUDE.md` → STD流程 | books/writing-projects/ |
| 写公众号/写推文 | `books/.../CLAUDE.md` → WX流程 | books/writing-projects/ |
| 做PPT/做汇报 | `books/.../CLAUDE.md` → PPT流程 | books/writing-projects/ |
| 审稿回复 | 上传的审稿意见+原论文 | books/writing-projects/ |
| 查文献/验证引用 | Brave API检索 | — |
| 继续/上次做什么了 | `books/memory/` 最新文件 | — |
| 论文进度 | `WriterLLM/progress.json` | — |
| 专利进度 | `patent/patents/progress.md` | — |
| 查资料/找XX | 三库 `grep -r` | — |

---

## 3. 科研写作技巧（实战沉淀）

### 一、流程类

**技巧1 写-审-改闭环**
所有正式文档必须多角色评审迭代。九大文体各有专属评审角色和达标标准（详见 `academic-writer-skill/SKILL.md`）。

**技巧2 三库持久化**
产出按类型存入对应仓库。commit规范：`[类型] 描述`。断点续传：说"继续"即可从memory恢复。

**技巧3 讨论→写作自然切换**
不急于动笔。先在讨论中理清要素（类型/创新点/目标读者/结构），信息足够后输出提纲，确认再动笔。

**技巧4 分层渐进**
长文档分模块：提纲→逐节撰写→组装→通检。25万字书稿用L4策略（50模块×5000字）。

### 二、质量类

**技巧5 质量关卡强制**
初稿必跑 `run_checks.py`。参考文献验证关卡不可跳过——编造文献整篇打回。

**技巧6 文献检索用Brave API**
验证真实性、查最新进展、确认标准有效。检索命令见本文件第4节。

**技巧7 跨文档一致性**
论文-专利-书稿间术语/参数/符号统一。创新点重叠<30%。用 `check_consistency.py` 检查。

**技巧8 ODD场景化思维**
水网问题从运行设计域切入：正常域→扩展域→MRC，六维参数向量结构化。这是CHS标志性方法。

### 三、工具类

**技巧9 python-docx生成Word**
避免JS的中文引号转义问题。内容写文本文件，Python脚本读取生成docx。

**技巧10 审稿回复要简练**
每条意见1-2段，说清"改了什么"。不堆砌不套话。不同意就说"我们的理解是……"。

**技巧11 多平台内容分发**
同一学术内容可适配：SCI论文→中文核心→公众号科普→PPT汇报→短视频脚本。

**技巧12 上下文高效利用**
按需加载文件，不一次读完。先看目录结构，按任务定位具体内容。

### 四、中文核心期刊专项技巧

**技巧13 字数规模与篇幅管理**
各期刊字数基准（正文+图表+参考文献折算）：

| 期刊 | 总字数 | 摘要 | 参考文献格式 | 特殊要求 |
|------|--------|------|-------------|---------|
| 中国科学：技术科学 | 15,000-20,000字 | 300字中+200词英 | GB/T 7714 | 中英摘要对应 |
| 水利学报 | 8,000-12,000字 | 300字 | GB/T 7714 | 基金项目声明 |
| 南水北调与水利科技 | 8,000-10,000字 | 200-300字 | GB/T 7714 | — |
| 水利水电技术 | 6,000-8,000字 | 200字 | GB/T 7714 | — |

**写作要点**：
- 用Python统计各节字数（`len(re.findall(r'[\u4e00-\u9fff]', text))`），识别<300字的"薄弱节"优先扩充
- 理论核心节（如六元架构、八原理）字数不应低于全文平均节字数
- 扩写优先级：理论框架 > 工程案例 > 路线图，先扩"论文灵魂"部分
- 中英文摘要必须语义对应（非逐字翻译），英文摘要可略简

**技巧14 学术插图AI生成提示词规范**

所有插图采用统一的提示词模板，中英双语标注，确保跨图件视觉一致性。

**提示词模板**（每张图必须包含以下要素）：
```
### 图X-Y: [中文图题]
**文件名**: fig_X_Y_english_name.png

**提示词**:
[用英文描述图件内容、布局、配色、标注、尺寸]

**技术规格**:
- 尺寸: [宽×高] px（最小1800×1200px，复杂图2400×1600px或更大）
- 背景: 白色(White background)
- 风格: Academic textbook quality / Clean academic infographic
- 标注: Chinese+English labels（中英双语）
- 分辨率: ≥300 DPI

**配色方案**（全文统一）:
```

**CHS论文/书稿统一配色**：

| 语义角色 | Hex | 用途 |
|---------|-----|------|
| Physical AI / 水力学 | #1565C0 (深蓝) | 蓝色系，水/机理/控制 |
| Safety / ODD | #4CAF50 (绿) | 安全边界 |
| Cognitive AI | #7B1FA2 (紫) | 智能/认知 |
| 扰动/警告 | #FF7043 (橙红) | 扰动/告警 |
| 信息块背景 | #E3F2FD/#FFF3E0/#E8F5E9/#F3E5F5 | 浅色填充 |
| 辅助线/网格 | #E0E0E0 (浅灰) | — |
| 正文文字 | #212121 (近黑) | — |

**图件类型与尺寸建议**：

| 图件类型 | 最小尺寸(px) | 典型用途 |
|---------|-------------|---------|
| 流程图/架构图 | 1800×2400 (竖版) | 控制架构、写作流程 |
| 时间线/路线图 | 2400×1200 (横版) | 发展历程、甘特图 |
| 概念关系图 | 2400×1600 (横版) | 理论框架、概念地图 |
| 散点图/对比图 | 1800×1500 (近方) | 跨行业定位、性能对比 |
| 全景总图 | 2800×1800 (横版) | 学科全景、系统总图 |

**实操建议**：
- 架构图信息层次复杂时，先用AI生成视觉风格参考，再在PPT/Illustrator中手动精修
- 中英文标注同时出现，中文在上或在前，英文在下或在后
- 每张图提示词末尾加 "Academic textbook quality. Chinese+English labels. Minimum [宽]×[高]px."
- SCI投稿用矢量格式(SVG/PDF)，审稿用PNG 300dpi

**技巧15 中文核心期刊参考文献铁律**

- 格式严格遵循 GB/T 7714-2015
- 每条参考文献必须用 Brave API 或 web_search 验证真实性
- 中文期刊：≥20篇参考文献，近5年占比≥40%
- 自引Lei 2025a-d系列：控制在自引率15-25%之间
- 标准引用（GB/T、SL/T）：必须web_search确认现行有效，废止标准不可引用
- 已发表中文基准文献（必引）：
  - Lei 2025a: 水系统控制论. 南水北调,23(04):761-769
  - Lei 2025b: 自主运行智慧水网架构. 南水北调,23(04):778-786
  - Lei 2025c: 在环测试体系. 南水北调,23(04):787-793
  - Lei 2025d: 学科展望. 南水北调,23(04):770-777

**技巧16 中文论文扩写方法论**

当审稿人或自检发现篇幅不足时：
1. **Python扫描各节字数**，生成`节名: 字数`列表，标记<300字的节为 `⚠薄`
2. **优先扩充顺序**：理论核心节 > 案例数据节 > 路线图节 > 文献综述节
3. **扩写手法**：
   - 理论节：增加公式的物理含义解释、与传统方法的对比、工程实例类比
   - 案例节：增加六元组对应关系、定量测试结果、经验教训总结
   - 路线图节：拆分为子节（理论完善/技术标准/推广应用/机制建设），每节配一段
4. **扩写后复查**：重新统计字数，确认薄弱节已达标，全文字数匹配目标期刊要求

**技巧17 长文拆分"姊妹篇"策略**

中文核心期刊单篇一般10-12页（含参考文献约13,000-15,000字）。当初稿超过20,000字时，拆分为上下篇（姊妹篇）：

- **拆分原则**：上篇建理论（"为什么"+"是什么"），下篇落工程（"怎么做"+"做得怎样"）
- **字数控制**：每篇正文6,000-8,000中文字 + 参考文献1,500字 + 摘要800字 ≈ 10页
- **关系设计**：下篇引用上篇的框架定义，但自身逻辑完整可独立审稿
- **投稿策略**：两篇同时投稿注明系列论文，或先投上篇录用后投下篇
- **必须产出拆分方案文档**（split_plan.md），包含：
  - 每篇的章节结构、内容来源（v原稿哪节）、预估字数
  - 图表分配（哪张图归哪篇）
  - 两篇关系图（ASCII框图即可）

**实战数据**（MBD论文）：v4全文23,600字正文 → 拆分为上篇6,955字+下篇7,478字，各配1-2张图。

**技巧18 中文期刊插图提示词规范（区别于SCI）**

中文核心期刊的插图要求与SCI英文期刊有显著差异：

| 要素 | 中文核心期刊 | SCI英文期刊 |
|------|-------------|------------|
| 标注语言 | **纯中文**，仅保留国际通用缩写(MBD/ODD/MPC等) | 全英文 |
| 分辨率 | **≥600dpi**（印刷要求高于电子版） | ≥300dpi |
| 配色 | **黑白灰+单色点缀**（蓝色最安全），适合黑白印刷 | 可用多色但需色盲友好 |
| 宽度 | 单栏~85mm，双栏~170mm | 单栏≤85mm，双栏≤180mm |
| 风格 | 矢量感线框图，无3D/阴影/渐变 | 允许适度渐变 |
| 输出格式 | PNG/SVG/TIFF | 矢量优先(SVG/EPS/PDF) |

**中文插图提示词模板**：
```
### 图X　[中文图题]
**文件名**: fig_X_english_name.png

**论文上下文**: [描述这张图在论文中的位置和要表达的信息]

**提示词**:
A technical [diagram type] for an academic journal paper showing [content].
White background, black/dark gray lines, minimal blue accent color.
Suitable for journal layout (~170mm width).
ALL TEXT LABELS IN CHINESE ONLY, no English translations.
Keep only standard abbreviations ([列举]).

[详细描述图件内容、布局、箭头方向、标注文字...]

Clean technical diagram suitable for academic journal printing.
Black/gray with minimal blue accent. No decorative elements, no 3D effects, no shadows.
```

**关键差异强调**：
- 提示词主体用英文（AI工具理解效果好），但**必须明确要求"ALL TEXT LABELS IN CHINESE ONLY"**
- 每张图的提示词前必须写清**论文上下文**（帮助AI理解信息层次）
- 概念图/架构图类用AI生成初稿+PPT精修；数据曲线类用matplotlib/plotly代码生成
- 一篇中文论文通常2-4张图（不宜过多，中文期刊版面有限）

**技巧19 审稿修改的参考文献全量复核流程**

审稿返修时参考文献容易出问题（占位符遗漏、编号错位、信息不全），必须执行：

```python
# 1. 提取全部参考文献
refs = re.findall(r'\[(\d+)\].*', text)

# 2. 检查编号连续性
nums = sorted([int(n) for n in re.findall(r'\[(\d+)\]', ref_section)])
expected = list(range(1, len(nums)+1))
assert nums == expected, f"编号缺漏: {set(expected)-set(nums)}"

# 3. 每条参考文献用Brave API验证
for ref in refs:
    query = extract_key_terms(ref)  # 作者+标题关键词+期刊
    result = brave_search(query)
    verify(result, ref)  # 比对DOI/卷期页码/年份

# 4. 正文中每个[N]都必须在参考文献列表中存在
cited_in_text = set(re.findall(r'\[(\d+)\]', body_text))
defined_in_refs = set(re.findall(r'^\[(\d+)\]', ref_section, re.M))
assert cited_in_text == defined_in_refs, "引用与文献列表不匹配"
```

---

## 4. 文献检索

```bash
curl -s "https://api.search.brave.com/res/v1/web/search?q=${QUERY}&count=10" \
  -H "X-Subscription-Token: ${BRAVE_API_KEY}" \
  -H "Accept: application/json"
```

**典型用途**：
- `q=DOI+10.1016/xxx` → 验证参考文献
- `q=water+network+autonomous+control+2024` → 检索最新进展
- `q=GB/T+50509+现行` → 确认标准有效性
- `q=发明专利+水网+分布式控制` → 查竞争专利
- `q=雷晓辉+基于无人驾驶+自主运行+南水北调` → 验证自引文献

---

## 5. 会话结束存档

```bash
cd /home/claude/books
cat >> memory/$(date +%Y-%m-%d).md << 'EOF'

## HH:MM 更新
- 完成：[产出]
- 决策：[关键决策]
- 待办：[下次做什么]
EOF
git add -A && git commit -m "[memory] $(date +%Y-%m-%d) 工作记录" && git push
```

如修改了其他仓库，也对应push：
```bash
cd /home/claude/WriterLLM && git add -A && git commit -m "[论文编号] 描述" && git push
cd /home/claude/patent && git add -A && git commit -m "[PFx-x] 描述" && git push
```
