# HydroScribe 多智能体评审系统 v2.0 — 详细设计

> **版本**: 2.0-draft
> **日期**: 2026-02-26
> **设计者**: 雷晓辉 + Claude
> **定位**: HydroScribe 评审子系统的全面升级，从"角色轴"扩展为"角色×维度"二维矩阵
> **适用范围**: T1-CN, T2-CN, T2a, T2b 及全部书稿/论文项目

---

## 0. 设计动机与问题分析

### 0.1 现有系统的不足

HydroScribe v0.3.0 的评审系统按**角色**划分 Reviewer：

```
BK文体: 教师 + 专家 + 工程师 + 国际读者 (4个角色)
```

这种设计的问题：
- **粒度不足**：每个角色评审"整章内容"，容易遗漏公式错误、编号跳号等细节
- **维度混合**：教师同时评内容质量、教学设计、逻辑流、图表质量——超出单一视角能力
- **无法批量修复**：发现的问题混杂在自然语言评价中，无法自动化处理
- **T1-CN实测**：80处问题中，62%是编号/引用/术语表等机械性错误，角色型Reviewer无法有效捕获

### 0.2 目标架构

```
现有: 1维 = 角色轴 (WHO)
      教师 → 评全章 → 混合反馈

升级: 2维 = 角色轴 (WHO) × 维度轴 (WHAT)
      教师 → 只评教学设计
      公式审核员 → 只审公式
      编号扫描器 → 只扫编号
      ...
```

### 0.3 设计原则

1. **维度正交**：每个维度Agent只关注一个方面，避免注意力分散
2. **机械性先行**：先用Utility Agent扫描可自动化的问题（编号/引用/格式），再用Role Agent评判需要理解力的问题（内容/逻辑/教学）
3. **模型匹配**：机械检查用haiku（快+准），内容评审用opus（深+慎），工程判断用sonnet（平衡）
4. **结构化输出**：每个Agent输出标准JSON，可直接驱动自动修复脚本
5. **参考最佳实践**：融合IEEE/Nature评审标准、ISO 9001质量管理、GB/T 33190教材标准

---

## 1. 二维评审矩阵

### 1.1 维度轴定义（12个维度）

按自动化程度从高到低排列：

| # | 维度ID | 中文名 | 英文名 | 自动化程度 | 推荐模型 | 权重 |
|---|--------|--------|--------|-----------|---------|------|
| D1 | `numbering` | 编号连续性 | Numbering Continuity | ★★★★★ | haiku | 10% |
| D2 | `cross-ref` | 交叉引用 | Cross-Reference | ★★★★★ | haiku | 12% |
| D3 | `terminology` | 术语一致性 | Terminology Consistency | ★★★★☆ | haiku | 8% |
| D4 | `bibliography` | 参考文献 | Bibliography | ★★★★☆ | haiku | 5% |
| D5 | `formatting` | 排版格式 | Layout & Formatting | ★★★★☆ | haiku | 5% |
| D6 | `formula` | 公式验证 | Formula Validation | ★★★☆☆ | opus | 12% |
| D7 | `figure` | 图片质量 | Figure Quality | ★★★☆☆ | sonnet | 8% |
| D8 | `table` | 表格质量 | Table Quality | ★★★☆☆ | sonnet | 5% |
| D9 | `content` | 内容准确性 | Content Accuracy | ★★☆☆☆ | opus | 15% |
| D10 | `logic` | 逻辑完整性 | Logic & Coherence | ★★☆☆☆ | opus | 10% |
| D11 | `pedagogy` | 教学设计 | Pedagogical Design | ★☆☆☆☆ | sonnet | 5% |
| D12 | `innovation` | 创新价值 | Innovation & Impact | ★☆☆☆☆ | opus | 5% |

### 1.2 角色轴定义（6个角色，继承HydroScribe BK文体）

| # | 角色ID | 中文名 | 视角描述 | 主要关注维度 | 推荐模型 |
|---|--------|--------|---------|------------|---------|
| R1 | `theorist` | 理论严谨型 | 欧洲控制论教授，40年学术经验 | D6,D9,D10,D12 | opus |
| R2 | `engineer` | 工程实践型 | 美国水利CTO，20年SCADA/MPC经验 | D7,D8,D9,D11 | sonnet |
| R3 | `cross-domain` | 学科交叉型 | 亚洲AI+水利带头人 | D9,D10,D12 | sonnet |
| R4 | `editor` | 出版编辑型 | 资深出版社编辑 | D1-D5 | haiku |
| R5 | `writer` | 作者修改型 | 雷晓辉教授视角 | 全维度 | opus |
| R6 | `auditor` | 一致性审核 | 全书质量总控 | D2,D3,D6 | sonnet |

### 1.3 交叉矩阵

```
             D1编号  D2引用  D3术语  D4文献  D5排版  D6公式  D7图片  D8表格  D9内容  D10逻辑  D11教学  D12创新
R1理论型      ·       ·       ·       ●       ·       ●●      ·       ·       ●●      ●●       ·       ●●
R2工程型      ·       ·       ·       ·       ·       ●       ●●      ●●      ●●      ●        ●●      ·
R3交叉型      ·       ·       ●       ·       ·       ·       ●       ·       ●●      ●●       ·       ●●
R4编辑型      ●●      ●●      ●●      ●●      ●●      ·       ●       ●       ·       ·        ·       ·
R5作者型      ●       ●       ●       ●       ●       ●       ●       ●       ●       ●        ●       ●
R6审核型      ●       ●●      ●●      ·       ·       ●       ·       ·       ·       ·        ·       ·

●● = 主要职责    ● = 辅助检查    · = 不关注
```

---

## 2. 维度Agent详细设计

### D1: 编号连续性审查员 (`numbering-auditor`)

**角色设定**: 强迫症级别的编号检查专家
**推荐模型**: haiku（快速、精确、低成本）
**输入**: 章节Markdown全文
**检查项**:

```yaml
checklist:
  section_numbers:
    - 章号X必须等于文件名中的章号（ch05→§5.X）
    - 子节号必须连续（§5.1→§5.2→§5.3，不可跳号）
    - 层级不超过4级（§5.2.3.1）
  equation_numbers:
    - 公式编号(X-Y)中X必须等于章号
    - Y必须在本章内连续递增
    - 正文中对公式的引用必须存在对应编号
  figure_numbers:
    - 图X-Y中X必须等于章号
    - Y在本章内连续
    - 正文中每处"图X-Y"必须有对应图片
  table_numbers:
    - 表X-Y中X必须等于章号
    - Y在本章内连续
    - 正文中每处"表X-Y"必须有对应表格
  reference_numbers:
    - [X-Y]格式引用在本章参考文献列表中必须有对应条目
    - 编号连续，无跳号
```

**输出格式**:
```json
{
  "dimension": "numbering",
  "chapter": "ch05",
  "score": 4,
  "issues": [
    {
      "id": "NUM-05-001",
      "severity": "critical",
      "type": "section_jump",
      "location": "line 42",
      "current": "§4.11b.1",
      "expected": "§5.2.1",
      "fix_command": "sed -i 's/§4\\.11b\\.1/§5.2.1/g' ch05_final.md",
      "auto_fixable": true
    }
  ],
  "summary": {
    "total_sections": 28,
    "total_equations": 15,
    "total_figures": 8,
    "total_tables": 3,
    "errors_found": 6
  }
}
```

---

### D2: 交叉引用验证器 (`crossref-validator`)

**角色设定**: 全书链接完整性专家
**推荐模型**: haiku
**输入**: 当前章节 + 全书目录结构（章号→标题映射）
**检查项**:

```yaml
checklist:
  internal_refs:
    - "见第X章"中X必须是有效章号（1-15）
    - "§X.Y"中X必须等于被引章号，§X.Y必须在目标章中存在
    - "见图X-Y"/"见表X-Y"/"见式(X-Y)"必须指向存在的元素
  cross_chapter_refs:
    - 章节间引用方向正确（不可引用尚未写的后续章）
    - 术语首次定义章与引用章的关系正确
  reading_guide:
    - 阅读指引中的§编号必须属于本章
    - "可略读"/"必读"段落的§编号有效
  glossary:
    - 术语表中§编号必须指向本章（关键红线）
```

**特别规则（来自T1-CN实测教训）**:
```
红线1: 术语表§编号章号偏移 — ch09术语表写§10.X是系统性bug
红线2: "第十一章"万能引用 — 章节重组后遗留的幽灵引用
红线3: 阅读指引§编号跨章 — ch05阅读指引写§6.X
```

---

### D3: 术语一致性守卫 (`terminology-guard`)

**角色设定**: CHS术语标准化执法官
**推荐模型**: haiku
**输入**: 章节全文 + `glossary_cn.md` + `symbols.md`
**检查项**:

```yaml
checklist:
  defined_terms:
    - 核心缩写首次出现必须给出全称+中文（如 "MPC, Model Predictive Control, 模型预测控制"）
    - 全书禁止别名（"安全边界"→必须用"安全包络"，"水网操作系统"→必须用"HydroOS"）
  cross_language:
    - 中英文术语对照一致（CHS=水系统控制论，不是"水系统控制学"）
    - 英文缩写全书统一（WNAL不可写成WNA或W-NAL）
  symbol_consistency:
    - 同一物理量符号全书统一（流量用Q不用q）
    - 上下标规范一致
  forbidden_aliases:
    CHS: ["水系统控制学", "水系控制论", "水力系统控制论"]
    HydroOS: ["水网操作系统", "水OS"]
    安全包络: ["安全边界", "安全域", "安全范围"]
    瀚铎: ["天河", "瀚朵"]
```

---

### D4: 参考文献审查员 (`bibliography-checker`)

**角色设定**: 学术诚信监督员
**推荐模型**: haiku
**输入**: 章节全文 + 全书参考文献数据库
**检查项**:

```yaml
checklist:
  completeness:
    - 正文中[X-Y]引用必须在参考文献列表中有对应条目
    - 参考文献列表中每条至少在正文被引用一次
  format:
    - GB/T 7714-2015格式统一
    - 作者名格式一致（Lei X H vs Xiaohui Lei）
    - DOI/URL有效性（可选，需联网）
  self_citation:
    - 计算本章自引率（Lei等/雷晓辉等的引用占比）
    - 自引率建议控制在20-30%（CHS项目特殊，可适当放宽）
  deduplication:
    - 同一文献在不同章节是否有不同引用格式
    - Litrico & Fromion等高频引用是否全书格式统一
```

---

### D5: 排版格式检查员 (`formatting-inspector`)

**角色设定**: Markdown排版规范专家
**推荐模型**: haiku
**检查项**:

```yaml
checklist:
  markdown_syntax:
    - 标题层级正确（# → ## → ### → ####，不可跳级）
    - 列表缩进一致
    - 代码块语言标注
    - 表格对齐
  image_links:
    - 所有![alt](url)链接可达
    - 图片替代文字有意义（不是"image1"）
  typography:
    - 中英文之间有空格
    - 标点符号全角/半角统一
    - 数字与单位之间有空格（如"100 km"）
  structure:
    - 每章有统一的结构（概述→正文→小结→习题→参考文献）
    - 术语表格式统一
    - 阅读指引格式统一
```

---

### D6: 公式验证专家 (`formula-validator`)

**角色设定**: 数学物理双栖审稿人
**推荐模型**: opus（需要深度数学推理）
**输入**: 章节中所有公式及上下文
**检查项**:

```yaml
checklist:
  mathematical_correctness:
    - LaTeX/Markdown公式语法正确
    - 数学推导步骤完整，无跳步
    - 矩阵维度匹配
    - 积分/求和上下限正确
  dimensional_analysis:
    - 等式两边量纲一致
    - 物理单位正确（SI制为主）
    - 无量纲数正确标注
  notation_consistency:
    - 向量/矩阵粗体标记统一
    - 转置符号统一（T vs ⊤）
    - 下标/上标含义前后一致
  engineering_validity:
    - 控制论公式参数在合理范围（增益、时延、阻尼比等）
    - Saint-Venant方程参数物理意义正确
    - 数值示例可重现
  boundary_conditions:
    - 特殊情况是否讨论（零输入/满载/极限工况）
    - 稳定性条件是否给出
```

**验证工具链**:
```
LLM审查 → SymPy符号验证(可选) → 量纲分析 → 数值验证
```

---

### D7: 图片质量评审员 (`figure-reviewer`)

**角色设定**: Nature级图表设计顾问
**推荐模型**: sonnet（需要视觉理解和审美判断）
**检查项**:

```yaml
checklist:
  relevance:
    - 图片与上下文论述密切相关
    - 不存在"装饰性"无意义配图
  clarity:
    - 图片清晰度足够（非模糊截图）
    - 文字标注可读
    - 坐标轴标签完整（含单位）
  consistency:
    - 全书图片风格统一（线宽/颜色/字体）
    - 示意图与实物照片区分清晰
    - 流程图方向统一（左→右或上→下）
  caption:
    - 图注完整、自包含（不看正文也能理解）
    - 图注与正文描述一致
  placement:
    - 图片紧跟首次引用的段落
    - 图片大小适中（不过大不过小）
  source:
    - 引用他人图片注明来源
    - AI生成图片标注生成方法
```

---

### D8: 表格质量评审员 (`table-reviewer`)

**角色设定**: 数据可视化专家
**推荐模型**: sonnet
**检查项**:

```yaml
checklist:
  data_accuracy:
    - 表格数据与正文描述一致
    - 同一参数在不同表格中数值一致
    - 单位标注清晰
  structure:
    - 表头信息完整
    - 行列对齐
    - 合并单元格使用合理
  format:
    - 数值精度统一（小数位数）
    - 大数字使用千分位（可选）
    - 空值处理方式一致（"—" vs "N/A"）
  cross_chapter:
    - 同一工程参数表在不同章节一致
    - 沙坪电站装机容量、胶东调水设计流量等关键参数统一
```

---

### D9: 内容准确性专家 (`content-expert`)

**角色设定**: CHS领域资深教授
**推荐模型**: opus（需要最深度的领域理解）
**检查项**:

```yaml
checklist:
  factual_accuracy:
    - 工程案例数据真实可查（沙坪/大渡河/胶东）
    - 历史事件时间线正确
    - 技术参数在工程合理范围
  theoretical_soundness:
    - CHS八原理表述完整准确
    - WNAL L0-L5定义与原始论文一致
    - ODD/MRC/HDC等核心概念准确
  completeness:
    - 每节覆盖了大纲要求的知识点
    - 关键定理/定义无遗漏
    - 重要假设条件已说明
  currency:
    - 引用的技术标准为现行有效版本
    - 不使用过时术语或淘汰技术
  originality:
    - 正确区分本书原创内容与引用内容
    - 创新点陈述准确（不夸大不缩小）
```

---

### D10: 逻辑完整性审查员 (`logic-reviewer`)

**角色设定**: 哲学逻辑训练的科学家
**推荐模型**: opus
**检查项**:

```yaml
checklist:
  argument_chain:
    - 每节的论证链完整（前提→推理→结论）
    - 无逻辑跳跃（"因此"之前有充分论据）
    - 反例和边界情况已讨论
  chapter_flow:
    - 章内节间过渡自然
    - 概念引入顺序合理（先简后繁，先定义后应用）
    - 前置知识已在前文覆盖
  cross_chapter_coherence:
    - 章间衔接语自然
    - 前后章内容无矛盾
    - 全书叙事线清晰（问题→理论→方法→应用）
  prerequisite_chain:
    - 引用的概念已在前文定义
    - 不存在循环定义
    - 读者知识假设一致
```

---

### D11: 教学设计评审员 (`pedagogy-reviewer`)

**角色设定**: 985高校教学名师
**推荐模型**: sonnet
**检查项**:

```yaml
checklist:
  learning_objectives:
    - 每章有明确的学习目标
    - 目标可测量（Bloom分类法）
    - 目标与内容匹配
  scaffolding:
    - 难度梯度合理（渐进式）
    - 有"物理直觉"段帮助理解
    - 抽象概念有具体类比
  examples:
    - 例题覆盖关键知识点
    - 例题难度递增
    - 工程案例与理论对应
  exercises:
    - 习题覆盖不同Bloom层次
    - 有开放性思考题
    - 难度标注（基础/提高/挑战）
  reading_guide:
    - 阅读指引实用（标注必读/选读/略读）
    - 不同读者路径清晰（研究生/工程师/自学者）
```

---

### D12: 创新价值评估员 (`innovation-assessor`)

**角色设定**: Nature/Science编委
**推荐模型**: opus
**检查项**:

```yaml
checklist:
  novelty:
    - 原创概念清晰标注（CHS八原理、WNAL、ODD-MRC等）
    - 与现有文献的差异明确
  significance:
    - 对领域的潜在影响评估
    - 实际应用价值
  international_context:
    - 与国际前沿的对标
    - 中英文术语翻译的学术准确性
  readability:
    - 面向国际读者的可理解性
    - 概念表达的普适性
```

---

## 3. 三阶段评审工作流

### 3.1 阶段概览

```
阶段一: 机械扫描 (Mechanical Scan)
  ├─ D1 编号连续性    ──→ haiku ──→ 自动修复脚本
  ├─ D2 交叉引用      ──→ haiku ──→ 自动修复脚本
  ├─ D3 术语一致性    ──→ haiku ──→ 自动修复脚本
  ├─ D4 参考文献      ──→ haiku ──→ 问题清单
  └─ D5 排版格式      ──→ haiku ──→ 自动修复脚本
  [5个Agent并行，预计2-5分钟/章]
  [产出: 机械问题清单 + 批量修复脚本]

       ↓ 执行自动修复后

阶段二: 专业评审 (Expert Review)
  ├─ D6 公式验证      ──→ opus  ──→ 公式问题清单
  ├─ D7 图片质量      ──→ sonnet ──→ 图片改进建议
  ├─ D8 表格质量      ──→ sonnet ──→ 表格改进建议
  ├─ D9 内容准确性    ──→ opus  ──→ 内容问题清单
  ├─ D10 逻辑完整性   ──→ opus  ──→ 逻辑问题清单
  ├─ D11 教学设计     ──→ sonnet ──→ 教学改进建议
  └─ D12 创新价值     ──→ opus  ──→ 创新评估报告
  [7个Agent并行，预计5-15分钟/章]
  [产出: 专业评审报告]

       ↓

阶段三: 综合研判 (Synthesis & Judgment)
  ├─ 角色综合评审 (R1-R3各一个Agent)
  │   ├─ R1 理论型 → opus  → 侧重D6+D9+D10+D12
  │   ├─ R2 工程型 → sonnet → 侧重D7+D8+D9+D11
  │   └─ R3 交叉型 → sonnet → 侧重D9+D10+D12
  ├─ 一致性审核 (R6)
  │   └─ R6 审核型 → sonnet → 跨章D2+D3+D6
  └─ 最终报告生成
      └─ 12维雷达图 + 优先级排序 + 修复计划
```

### 3.2 阶段一: 机械扫描详细流程

```python
# 伪代码: 阶段一并行执行
async def phase1_mechanical_scan(chapter_content, chapter_id, book_structure):
    """5个haiku Agent并行扫描，产出结构化问题清单"""

    agents = [
        NumberingAuditor(model="haiku"),      # D1
        CrossRefValidator(model="haiku"),      # D2
        TerminologyGuard(model="haiku"),       # D3
        BibliographyChecker(model="haiku"),    # D4
        FormattingInspector(model="haiku"),     # D5
    ]

    # 并行执行
    results = await asyncio.gather(*[
        agent.scan(chapter_content, chapter_id, book_structure)
        for agent in agents
    ])

    # 汇总
    mechanical_report = MechanicalReport(
        auto_fixable=[i for r in results for i in r.issues if i.auto_fixable],
        manual_review=[i for r in results for i in r.issues if not i.auto_fixable],
    )

    # 生成修复脚本
    fix_script = generate_fix_script(mechanical_report.auto_fixable)

    return mechanical_report, fix_script
```

### 3.3 阶段二: 专业评审详细流程

```python
async def phase2_expert_review(chapter_content, chapter_id, phase1_report):
    """7个专业Agent并行评审，使用不同模型"""

    agents = [
        FormulaValidator(model="opus"),        # D6 - 需要深度数学推理
        FigureReviewer(model="sonnet"),         # D7 - 需要视觉理解
        TableReviewer(model="sonnet"),          # D8 - 需要数据分析
        ContentExpert(model="opus"),            # D9 - 需要领域深度
        LogicReviewer(model="opus"),            # D10 - 需要推理能力
        PedagogyReviewer(model="sonnet"),       # D11 - 需要教学理解
        InnovationAssessor(model="opus"),       # D12 - 需要学术视野
    ]

    # 注入阶段一已修复信息，避免重复报告
    context = {"phase1_fixed": phase1_report.auto_fixed_items}

    results = await asyncio.gather(*[
        agent.review(chapter_content, chapter_id, context)
        for agent in agents
    ])

    return ExpertReport(dimension_scores={r.dimension: r.score for r in results},
                        all_issues=[i for r in results for i in r.issues])
```

### 3.4 阶段三: 综合研判

```python
async def phase3_synthesis(chapter_content, phase1_report, phase2_report):
    """角色型Agent综合研判 + 最终报告"""

    # 角色型Reviewer只关注各自擅长的维度
    role_reviews = await asyncio.gather(
        theorist_review(chapter_content,
                       focus_dims=[D6, D9, D10, D12],
                       model="opus"),
        engineer_review(chapter_content,
                       focus_dims=[D7, D8, D9, D11],
                       model="sonnet"),
        cross_domain_review(chapter_content,
                           focus_dims=[D9, D10, D12],
                           model="sonnet"),
    )

    # 一致性审核（需要跨章信息）
    consistency = await auditor_review(
        all_chapters, focus_dims=[D2, D3, D6], model="sonnet"
    )

    # 生成最终报告
    return FinalReport(
        mechanical=phase1_report,
        expert=phase2_report,
        role_reviews=role_reviews,
        consistency=consistency,
        radar_chart=compute_12d_radar(phase2_report),
        priority_ranking=rank_issues_by_severity(all_issues),
    )
```

---

## 4. Claude Projects 调用模板

### 4.1 启动全书评审

```
请对 T1-CN 执行三阶段多智能体评审。

阶段一（机械扫描，5个haiku Agent并行）：
  Agent 1 (haiku): D1编号连续性审查 — 扫描全书15章
  Agent 2 (haiku): D2交叉引用验证 — 扫描全书15章
  Agent 3 (haiku): D3术语一致性 — 扫描全书15章
  Agent 4 (haiku): D4参考文献检查 — 扫描全书15章
  Agent 5 (haiku): D5排版格式检查 — 扫描全书15章

  产出: 机械问题清单 + 自动修复脚本
  执行修复脚本后进入阶段二。

阶段二（专业评审，7个Agent并行，按章分批）：
  Agent 6 (opus): D6公式验证 — ch01-ch05（理论章，公式密集）
  Agent 7 (sonnet): D7+D8图表质量 — 全书
  Agent 8 (opus): D9内容准确性 — ch01-ch05
  Agent 9 (opus): D9内容准确性 — ch06-ch10
  Agent 10 (sonnet): D9内容准确性 — ch11-ch15
  Agent 11 (opus): D10逻辑完整性 — 全书（侧重章间衔接）
  Agent 12 (sonnet): D11+D12教学设计与创新评估 — 全书

阶段三（综合研判）：
  Agent 13 (opus): R1理论型综合评审
  Agent 14 (sonnet): R2+R3工程+交叉型综合评审
  Agent 15 (sonnet): R6跨章一致性审核
  Agent 16 (opus): 最终报告生成（12维雷达图+修复优先级）
```

### 4.2 单章深度评审

```
请对 ch05 执行12维深度评审：

并行启动以下Agent：
  Agent D1 (haiku): 编号连续性 — 重点检查§5.X编号
  Agent D2 (haiku): 交叉引用 — 重点检查阅读指引
  Agent D3 (haiku): 术语一致性 — 对照glossary_cn.md
  Agent D6 (opus): 公式验证 — 逐条验证所有公式
  Agent D9 (opus): 内容准确性 — CHS相关概念
  Agent D10 (opus): 逻辑完整性 — 论证链分析

产出12维评分雷达图和问题清单。
```

### 4.3 修改指定章节

```
根据评审报告中 ch05 的问题清单，执行分层修改：

Layer 1 (haiku): 执行自动修复脚本
  - §编号修正
  - 术语替换
  - 引用格式统一

Layer 2 (opus, 作者角色R5): 内容修改
  - 逐条处理D6/D9/D10维度的专家建议
  - 保持作者风格
  - 标注 [REVISED] / [ENHANCED]

Layer 3 (haiku): 修改后格式复查
  - 确认修复未引入新问题
  - 输出修改日志（diff格式）
```

---

## 5. 评审输出规范

### 5.1 单维度报告格式

```json
{
  "dimension": "formula",
  "dimension_name": "公式验证",
  "chapter": "ch05",
  "reviewer_model": "opus",
  "score": 7,
  "max_score": 10,
  "issues": [
    {
      "id": "FML-05-001",
      "severity": "critical",
      "location": "§5.3.2, 式(5-12)",
      "description": "RLS递推公式增益矩阵K(k)维度不匹配",
      "current_text": "K(k) = P(k-1)φ(k)[φᵀ(k)P(k-1)φ(k) + λ]⁻¹",
      "suggested_fix": "增益分子应为P(k-1)φ(k)，分母为标量，结果为列向量。检查φ(k)维度定义。",
      "auto_fixable": false,
      "requires_expertise": "control_theory"
    }
  ],
  "positive_findings": [
    "Saint-Venant方程推导步骤完整，物理意义清晰"
  ]
}
```

### 5.2 章节12维雷达图数据

```json
{
  "chapter": "ch05",
  "radar": {
    "numbering": 4,
    "cross_ref": 3,
    "terminology": 7,
    "bibliography": 6,
    "formatting": 6,
    "formula": 7,
    "figure": 8,
    "table": 7,
    "content": 8,
    "logic": 7,
    "pedagogy": 6,
    "innovation": 8
  },
  "weighted_score": 6.3,
  "critical_count": 3,
  "major_count": 5,
  "minor_count": 8,
  "verdict": "Major Revision"
}
```

### 5.3 全书总报告格式

```
MULTI_AGENT_REVIEW_REPORT_V2.md

一、执行摘要
  - 总评分
  - 12维平均分
  - 各阶段发现的问题数

二、12维雷达图（全书平均 + 各章）
  - ASCII雷达图或表格
  - 最强维度 / 最弱维度

三、系统性问题根因分析
  - 按维度分类
  - 自动可修复 vs 需人工处理

四、各章详细评审
  - 每章12维评分表
  - Critical问题列表

五、修复计划
  - P0: 阶段一可自动修复的问题（含脚本）
  - P1: 阶段二专业建议（需作者判断）
  - P2: 阶段三角色建议（提升性）

六、修复后预期评分

七、各Agent评审概要
  - 每个Agent的核心发现
  - Agent间分歧点
```

---

## 6. 与HydroScribe代码集成

### 6.1 新增维度Agent基类

```python
# hydroscribe/agents/base_dimension_reviewer.py

class BaseDimensionReviewer(BaseReviewerAgent):
    """维度型评审Agent基类 — 只关注一个评审维度"""

    dimension_id: str = ""        # "numbering", "formula", etc.
    dimension_name: str = ""      # "编号连续性", "公式验证", etc.
    checklist: list = []          # 检查项列表
    auto_fixable: bool = False    # 是否可生成自动修复脚本

    def _build_review_prompt(self, content, book_id, chapter_id):
        """覆盖基类方法，构建维度专用prompt"""
        return f"""你是{self.dimension_name}专项审查员。

你只需要检查以下方面，忽略其他所有问题：
{self._format_checklist()}

请严格按JSON格式输出，每个问题必须包含：
- location: 精确到行号或§编号
- severity: critical/major/minor
- auto_fixable: true/false
- fix_command: 如果auto_fixable=true，给出sed/python修复命令
"""
```

### 6.2 扩展config.toml

```toml
# 维度Agent专用配置
[review]
phases = ["mechanical", "expert", "synthesis"]
parallel_chapters = 3           # 并行评审章数
max_concurrent_dimension_agents = 12  # 最大并行维度Agent数

# 维度→模型映射
[review.model_map]
numbering = "haiku"
cross_ref = "haiku"
terminology = "haiku"
bibliography = "haiku"
formatting = "haiku"
formula = "opus"
figure = "sonnet"
table = "sonnet"
content = "opus"
logic = "opus"
pedagogy = "sonnet"
innovation = "opus"

# 维度→权重
[review.weights]
numbering = 0.10
cross_ref = 0.12
terminology = 0.08
bibliography = 0.05
formatting = 0.05
formula = 0.12
figure = 0.08
table = 0.05
content = 0.15
logic = 0.10
pedagogy = 0.05
innovation = 0.05
```

### 6.3 新增CLI命令

```bash
# 三阶段全书评审
hydroscribe review T1-CN --full

# 单阶段执行
hydroscribe review T1-CN --phase mechanical
hydroscribe review T1-CN --phase expert
hydroscribe review T1-CN --phase synthesis

# 单维度评审
hydroscribe review T1-CN --dimension formula --chapters ch01,ch02,ch03

# 执行自动修复
hydroscribe fix T1-CN --auto       # 执行P0自动修复脚本
hydroscribe fix T1-CN --interactive # 交互式修复（逐条确认）

# 查看评审报告
hydroscribe report T1-CN --format radar    # 12维雷达图
hydroscribe report T1-CN --format summary  # 执行摘要
hydroscribe report T1-CN --format full     # 完整报告
```

---

## 7. 参考标准与最佳实践

### 7.1 学术出版标准

| 标准 | 应用点 | 对应维度 |
|------|--------|---------|
| GB/T 33190-2016 高等教育教材 | 整体质量要求 | D9,D11 |
| GB/T 7714-2015 参考文献著录规则 | 文献格式 | D4 |
| ISO 9001:2015 质量管理体系 | PDCA循环、过程方法 | 全流程 |
| IEEE Peer Review Standards | 评审角色与流程 | R1-R3 |
| Nature Editorial Criteria | 创新性与影响力评估 | D12 |
| Bloom's Taxonomy | 教学目标分层 | D11 |
| WCAG 2.1 AA | 可访问性 | D5,D7 |

### 7.2 多Agent系统研究参考

| 来源 | 关键洞察 | 应用点 |
|------|---------|--------|
| Anthropic Multi-Agent Research (2025) | 15×token但覆盖更广 | 并行Agent比单Agent更全面 |
| HERMES (2025, arXiv:2511.18760) | LLM→形式化→求解器→反馈 | D6公式验证的verify链 |
| MATH-VF (2025) | CAS+SMT验证数学正确性 | D6的SymPy验证 |
| OpenManus PlanningFlow | Plan→Execute→Reflect | 三阶段流程 |

### 7.3 T1-CN实测数据支撑

v1.0评审发现的80处问题分布（支持维度权重设计）：

```
D1 编号连续性:  12处 (15%) — 节号跳号/继承错误
D2 交叉引用:   22处 (28%) — "第十一章"万能引用、术语表偏移 ← 最大痛点
D3 术语一致性:  8处 (10%) — MBD翻译不统一
D4 参考文献:    4处 (5%)
D5 排版格式:    6处 (8%)
D6 公式验证:    3处 (4%)
D7 图片质量:    5处 (6%)
D8 表格质量:    2处 (3%)
D9 内容准确性:  8处 (10%) — 工程参数
D10 逻辑完整性: 6处 (8%)
D11 教学设计:   2处 (3%)
D12 创新价值:   2处 (3%)
```

**关键发现**: D1+D2+D3+D5 四个可自动化维度占61%的问题。机械扫描优先策略正确。

---

## 8. 迭代计划

### Phase 1 (1周): 维度Agent基类 + D1-D5机械扫描
- 实现 `BaseDimensionReviewer`
- 实现 5个haiku Agent
- T1-CN全书测试

### Phase 2 (2周): D6-D12专业评审
- 实现 7个专业Agent
- 公式验证工具链（SymPy集成）
- T1-CN单章测试

### Phase 3 (1周): 三阶段编排 + 报告生成
- Orchestrator集成
- 12维雷达图生成
- 修复脚本自动化

### Phase 4 (持续): 优化与扩展
- 各维度Agent prompt迭代优化
- 扩展到SCI/CN/PAT文体
- 基于T1-CN结果的评审准确率baseline

---

## 9. 质量红线（不可妥协）

沿用HydroScribe v0.3.0，新增维度专项红线：

| # | 红线 | 对应维度 | 自动检测 |
|---|------|---------|---------|
| 1 | §编号章号必须等于文件名章号 | D1 | ✅ |
| 2 | 术语表§编号必须指向本章 | D2 | ✅ |
| 3 | 正文引用[X-Y]必须在参考文献中有条目 | D4 | ✅ |
| 4 | 公式编号(X-Y)的X必须等于章号 | D1 | ✅ |
| 5 | 图表编号X-Y的X必须等于章号 | D1 | ✅ |
| 6 | 同一工程参数跨章必须一致 | D8,D9 | ⚠️ 半自动 |
| 7 | 参考文献不可编造 | D4 | ⚠️ 需Brave验证 |
| 8 | CHS/HydroOS/WNAL等禁止使用别名 | D3 | ✅ |
| 9 | "见第X章"的X必须指向有效且正确的章节 | D2 | ✅ |
| 10 | 公式两边量纲必须一致 | D6 | ⚠️ 需SymPy |

---

**版本**: 2.0-draft
**状态**: 待讨论
**下一步**: 雷老师审阅后确定维度划分和权重，然后开始Phase 1实现
