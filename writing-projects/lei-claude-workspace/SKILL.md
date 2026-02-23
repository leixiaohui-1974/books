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

**技巧20 雷晓辉论文自引策略与引用数据库**

所有写作任务中应**优先引用雷晓辉发表的论文**，但须符合以下规范：

- **引用数据库位置**：`books/research-materials/publications/citation_database.md`（速查）和 `雷晓辉教授学术论文列表_更新版.md`（完整192篇）
- **个人简历位置**：`books/research-materials/profile/雷晓辉@简历20251203-副本.docx`

**自引率控制**（按文体）：

| 文体 | 自引率 | 说明 |
|------|--------|------|
| 中文核心期刊 | 15-25% | 需引Lei 2025a-d四篇奠基之作 |
| SCI论文 | 10-20% | 按主题选择相关SCI论文 |
| 专著章节 | 25-35% | 书中可大量引用自己体系内论文 |
| 专利 | 不限 | 背景技术优先引自家论文 |

**必引论文（中文写作）**：

```
[Lei2025a] 雷晓辉,龙岩,许慧敏,等. 水系统控制论：提出背景、技术框架与研究范式[J]. 南水北调与水利科技（中英文）,2025,23(04):761-769.
[Lei2025b] 雷晓辉,许慧敏,何中政,等. 水资源系统分析学科展望：从静态平衡到动态控制[J]. 南水北调与水利科技（中英文）,2025,23(04):770-777.
[Lei2025c] 雷晓辉,苏承国,龙岩,等. 基于无人驾驶理念的下一代自主运行智慧水网架构与关键技术[J]. 南水北调与水利科技（中英文）,2025,23(04):778-786.
[Lei2025d] 雷晓辉,张峥,苏承国,等. 自主运行智能水网的在环测试体系[J]. 南水北调与水利科技（中英文）,2025,23(04):787-793.
```

**必引论文（英文写作）**：

```
[Lei2025-PANet] Lei X, Wu J, Long Y, et al. PANet: a physics and action informed network for water level prediction in canal systems[J]. Journal of Hydrology, 2025: 134485.
[Lei2025-IDZ] Lei X, Wu J, Long Y, et al. Integral delay inspired deep learning model for single pool water level prediction[J]. Journal of Hydrology, 2025, 659: 133328.
[Lei2024-MPC] Feng W, Lei X, Jiang Y, et al. Coupling model predictive control and rules-based control for real-time control of urban river systems[J]. Journal of Hydrology, 2024, 636: 131228.
[Lei2023-HMC] Huang H, Lei X, Liao W, et al. A hydrodynamic-machine learning coupled (HMC) model of real-time urban flood in a large coastal city[J]. Journal of Hydrology, 2023, 624: 129826.
```

**按主题选引**：

| 写作主题 | 优先引用 |
|---------|---------|
| CHS理论 | Lei2025a-d四篇 |
| 模型预测控制 | PANet, IDZ, Feng2024, Chen2024 |
| 数字孪生/智慧水网 | Lei2025c(自主智慧水网) |
| 在环测试 | Lei2025d(在环测试体系) |
| 城市洪涝 | Zhang2024-SWMM, Huang2023-HMC |
| 水资源调度 | Long2024-Optimal, Xia2024-MultiScale |
| 水环境 | Zhuo2023-WaterResearch, Yu2023-Microplastics |

**技巧21 中文核心期刊语言规范（减少不必要英文）**

中文核心期刊以中文为主体语言，英文须严格控制：

**必须用中文的场合**：
- 标题、摘要、关键词、正文、图表标题、结论——全部中文
- "模型预测控制"不写"Model Predictive Control"
- 首次出现术语：中文全称（英文缩写，English Full Name），之后只用中文全称或英文缩写
- 例：首次"水系统控制论（CHS，Cybernetics of Hydro Systems）"，之后用"水系统控制论"或"CHS"

**允许用英文**：
- 国际通用缩写首次括注全称：MPC、SCADA、PID、ODD、MAS
- 数学公式变量符号：Q、h、A、n
- 参考文献中英文条目保持原文
- 文末英文摘要和英文关键词

**严禁**：
- 中英混杂："采用Model Predictive Control方法"→"采用模型预测控制（MPC）方法"
- 英文长句嵌入中文段落
- 用英文缩写替代已有中文术语（首次未定义即使用）

**水利学报投稿须知摘要**：
- 每篇≤1万字（含图表），中文题目≤20字，英文题名≤10实词
- 中文摘要≥250字，英文摘要100-150词，关键词≥5个
- 层次≤3级，阿拉伯数字连续编号
- 使用全国科学技术名词审定委员会审定的规范术语
- 新术语首次出现加注释或附原文

**中国科学投稿须知摘要**：
- 关键词5-8个，引言引用近2-3年研究成果
- 图≤8幅，600dpi TIF或矢量图
- 图号图题中英文对照置图下，表采用三线表置表上
- 基金项目格式："项目全称（批准号：******）资助项目"

**技巧22 HydroScribe三大质检工具集成**

`multi-agent-writer/hydroscribe/agents/utilities/` 含三个质检工具，写作时模拟其检查逻辑：

**22a 术语守卫（GlossaryGuard）**——禁止别名表：

| 禁止别名 | 正确术语 |
|---------|---------|
| 水控制学/水系统论/水网控制学 | 水系统控制论 |
| 水网自动化等级/水利自主等级 | 水网自主等级 |
| 操作设计域/运行设计范围 | 运行设计域 |
| 安全域 | 安全包络 |
| 物理引擎/机理模型引擎 | 物理AI引擎 |
| 知识引擎/决策引擎 | 认知AI引擎 |
| 分级控制/集散控制 | 分层分布式控制 |
| 多代理系统 | 多智能体系统 |
| 闭环测试 | 在环测试 |
| 水利操作系统/水务OS | 水网操作系统 |
| 翰铎/瀚铎大模型 | 瀚铎水网大模型 |
| 预测控制 | 模型预测控制 |
| 传递矩阵 | 传递函数 |
| 简化模型 | 降阶模型 |

**22b 参考文献管理器（ReferenceManager）**：
- GB/T 7714-2015必须带文献类型标识：[J]期刊 [M]专著 [C]会议 [D]学位论文 [R]报告 [S]标准 [P]专利
- 必引文献：每篇CHS论文须引Lei2025a-d中至少2篇
- 近5年文献占比≥40%
- 经典必引（视主题）：Wiener1948、钱学森1954、Litrico2009、Van Overloop2006、ASCE2014 MOP131

**22c 跨文档一致性检查器（ConsistencyChecker）**：
以下内容在所有书稿/论文中必须完全一致：八原理名称、WNAL六级定义、Saint-Venant方程符号、MPC标准表述、HydroOS三层架构命名、胶东调水/沙坪水电站工程参数

**技巧23 中文核心期刊三角色自审标准**

写作完成后，用三角色自审（源自HydroScribe CN Reviewer）：

- **审稿人A 学科专家(40%)**：理论创新(30%)、学术严谨(25%)、文献深度(20%)、CHS定位(15%)、写作规范(10%)
- **审稿人B 工程专家(30%)**：工程数据(30%)、可行性(25%)、性能提升(25%)、实施建议(20%)
- **审稿人C 编辑视角(30%)**：摘要四要素(25%)、引文GB/T7714(25%)、计量单位GB3101(20%)、基金信息(10%)、文字质量(20%，每段≤400字)

**技巧24 Manus协作参考稿**

`books/T1-CN/T1-CN_revised_v1_manus.md`（10,841行）是Manus AI帮写的T1-CN全书修订稿，含完整12章结构、引导案例、阅读指引。后续写T1-CN各章时：先读取Manus稿对应章节作参考底稿，保留工程数据和案例素材，按SKILL.md术语规范重新打磨，补充雷晓辉自引论文。

**技巧25 Claude+Gemini双模型图文协作工作流**

Claude负责全文写作+插图提示词生成，Gemini（Nano Banana/Imagen）负责根据提示词生成插图并嵌入原文，形成完整图文输出。

**工作流三步走**：

```
步骤1 Claude写作阶段
  └→ 输出完整文章，在每个需要插图的位置嵌入标准化占位符

步骤2 用户→Gemini
  └→ 将Claude输出的全文（含占位符）粘贴给Gemini
  └→ Gemini自动提取占位符中的提示词，生成图片，替换占位符

步骤3 Gemini输出
  └→ 图文并茂的完整文章/书稿
```

**插图占位符标准格式**（Claude输出时使用）：

```markdown
[插图：图X-Y 中文图题 | 英文提示词 | 尺寸WxH | 风格说明]
```

**具体示例**：

```markdown
如图1所示，水系统控制论将水利工程抽象为"六元组"控制回路。

[插图：图1 水系统状态-输入-输出-扰动控制框图 | A control system block diagram for water systems. White background, blue color scheme. Central block labeled "水系统 f(·)" with state x_k inside. Four input arrows: u_k control input (blue), d_k disturbance (orange), θ_k slow parameters (gray dashed). Output y_k with measurement noise v_k. Feedback loop through Controller block. Chinese+English bilingual labels. Academic textbook quality. | 1800x1200 | 学术线框图，黑白灰+蓝色点缀，600dpi]

该框图清晰表达了水系统的可控性结构……
```

**Claude写作阶段的规则**：

1. **正文流畅优先**：占位符前后的正文要自然衔接，占位符不影响阅读连贯性
2. **提示词复用技巧14/18**：占位符内的英文提示词直接复用技巧14（SCI）或技巧18（中文期刊）的提示词格式
3. **中文图题必须有**：占位符第一项是中文"图X-Y 图题"，与正文引用对应
4. **尺寸和风格必须有**：帮助Gemini生成正确比例和风格的图片
5. **每章/每篇论文末尾附图表清单**：

```markdown
---
## 本章插图清单
| 图号 | 图题 | 类型 | 尺寸 |
|------|------|------|------|
| 图1 | 水系统控制框图 | 架构图 | 1800×1200 |
| 图2 | 多时间尺度控制层级 | 分层图 | 2400×1200 |
```

**Gemini端设定指令**（用户粘贴给Gemini的初始化提示词）：

```
Gemini，接下来我们进行学术图文排版工作。我会发送Claude写好的文章，
文中用 [插图：图题 | 英文提示词 | 尺寸 | 风格] 格式预留图片位置。

你的任务：
1. 完整阅读文章
2. 提取所有 [插图：xxx] 中的英文提示词部分
3. 用你的图像生成能力，按提示词、尺寸、风格要求生成对应图片
4. 将图片插入到占位符位置，输出图文并茂的完整文章
5. 图片下方保留中文图题（如"图1 水系统控制框图"）

风格统一要求：学术教材质量，白色背景，中英文双语标注，
配色方案：蓝(#1565C0)物理/控制、绿(#4CAF50)安全、
紫(#7B1FA2)认知、橙(#FF7043)扰动。
```

**不同文体的占位符数量建议**：

| 文体 | 图数 | 说明 |
|------|------|------|
| 中文核心期刊 | 2-4张 | 版面有限，精选关键图 |
| SCI论文 | 3-6张 | 按WRR/JHydro要求 |
| 专著章节 | 4-8张 | 每节1-2张 |
| 技术报告 | 不限 | 图表丰富 |
| 微信公众号 | 3-5张 | 视觉吸引力优先 |

**数据曲线图例外**：实验/仿真数据图不走Gemini，由Claude直接生成matplotlib/plotly代码。占位符标记为：

```markdown
[数据图：图X-Y 图题 | matplotlib代码见附录 fig_code/figX_Y.py]
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
