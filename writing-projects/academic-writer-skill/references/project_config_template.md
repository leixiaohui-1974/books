# 项目配置模板 (Project Configuration Template)

> 每个写作项目在启动前须有一份配置文件，定义所有文档的写作规格。
> Claude 在"读取规格"步骤(§4.1步骤3)时读取此文件。

---

## 配置文件格式

文件路径：`docs/project_config.yaml`

```yaml
# ================================================
# 项目配置文件 (Project Configuration)
# ================================================
project:
  name: "CHS学术产出体系 2026"
  owner: "雷晓辉"
  created_at: "2026-02-19"
  description: "水系统控制论(CHS)理论体系的系统性学术产出"

# ================================================
# 全局默认值（可被单个文档覆盖）
# ================================================
defaults:
  language: "zh-CN"            # zh-CN | en | zh-EN(双语)
  terminology: "§5.1"          # 引用SKILL.md术语表
  symbols: "§5.2"              # 引用SKILL.md符号表
  self_citation_sources:       # 自引文献库
    - "Lei 2025a"
    - "Lei 2025b"
    - "Lei 2025c"
    - "Lei 2025d"

# ================================================
# 文档列表
# ================================================
documents:

  # ---------- SCI论文 ----------
  - id: "SCI-P1a"
    type: "SCI"
    title: "A Control-Theoretic Framework for Canal Pool Dynamics: From Saint-Venant to IDZ Transfer Functions"
    target_journal: "Water Resources Research"
    word_count: 8000
    language: "en"
    innovation:
      - "首次将CHS控制论框架系统化应用于渠池动力学建模"
      - "建立IDZ模型参数与渠池物理参数的解析映射关系"
      - "提出传递函数频域验证方法"
    structure:
      - section: "Introduction"
        key_points: "水利控制理论vs自动控制理论的历史对比; CHS动机"
        word_count: 1200
      - section: "Theoretical Framework"
        key_points: "Saint-Venant→线性化→传递函数→IDZ; 严格数学推导"
        word_count: 2500
      - section: "Parameter Identification"
        key_points: "α,β,τ^d的物理意义及估计方法"
        word_count: 1500
      - section: "Case Study"
        key_points: "南水北调中线单渠池验证"
        word_count: 1500
      - section: "Results and Discussion"
        key_points: "频域/时域对比; 精度分析; 适用范围"
        word_count: 1000
      - section: "Conclusions"
        key_points: "三个贡献; 局限性; 未来方向"
        word_count: 300
    must_cite:
      - "Wylie 1969"
      - "Litrico & Fromion 2009"
      - "Malaterre 1998"
      - "VanOverloop 2006"
    related_docs:
      - "SCI-P1b (IDZ扩展 → 依赖本文的传递函数框架)"
      - "BK-T2a (教材版本)"
      - "PAT-PF1-1 (专利版本)"
    consistency_checks:
      - "CONS-03"  # Saint-Venant离散化表述
      - "CONS-08"  # 南水北调参数

  # ---------- 微信公众号 ----------
  - id: "WX-001"
    type: "WX"
    title: "水网也需要操作系统？"
    audience: "泛科普+行业决策者"
    word_count: 2500
    tone: "说人话+有态度"
    core_viewpoint: "水网正在经历从人工调度到自主运行的范式转变，需要一套'操作系统'级的解决方案"
    structure:
      - section: "钩子: 一个让人意想不到的对比数据"
        word_count: 300
      - section: "问题: 中国水网的'驾驶难题'"
        word_count: 500
      - section: "类比: 从Android到HydroOS"
        word_count: 500
      - section: "分级: 水网自动驾驶L0-L5"
        word_count: 500
      - section: "展望: 收束+新问题"
        word_count: 300
    data_sources:
      - "水利部2025年工作会议: 水利投资数据"
      - "IDC: 智慧水利市场规模"
    hot_topics_to_search:
      - "智慧水利 最新政策"
      - "水利数字孪生 进展"

  # ---------- 演示文稿 ----------
  - id: "PPT-001"
    type: "PPT"
    title: "水系统控制论(CHS)理论与体系汇报"
    audience: "项目验收评审专家组"
    duration_minutes: 20
    page_count: 20
    language: "zh-CN"
    structure:
      - section: "研究背景与问题"
        pages: 3
        key_visuals: "水利工程全景照片, 问题对比图"
      - section: "CHS理论框架"
        pages: 5
        key_visuals: "CHS八原理架构图, WSAL分级表"
      - section: "关键技术突破"
        pages: 5
        key_visuals: "IDZ模型图, DMPC架构图, MAS架构图"
      - section: "工程验证"
        pages: 4
        key_visuals: "南水北调实景, 胶东调水数据曲线"
      - section: "成果与展望"
        pages: 2
        key_visuals: "成果统计表, 未来路线图"
    assets_needed:
      - "南水北调中线航拍照片"
      - "胶东调水工程照片"
      - "CHS架构图(已有)"

  # ---------- 发明专利 ----------
  - id: "PAT-PF1-1"
    type: "PAT"
    title: "一种基于IDZ模型的渠池水位控制方法及系统"
    innovation:
      - "将IDZ传递函数模型用于渠池水位实时控制"
      - "提出基于频域分析的控制器参数自整定方法"
    related_patents:
      - "PF1-2(串联渠池扩展)"
      - "PF1-3(非线性扩展)"
    must_distinguish_from:
      - "CN20XXXXXXA: 基于PID的渠道水位控制方法"
      - "CN20XXXXXXA: 基于模糊控制的灌区配水方法"

  # ---------- 国内标准 ----------
  - id: "STD-CN-SLT-XXXX"
    type: "STD-CN"
    title: "水网智能调控系统技术要求"
    standard_level: "SL/T"
    tc_info: "全国水利信息化标准化技术委员会"
    scope: "适用于灌区、供水管网、水利枢纽等水网系统的智能调控系统建设"
    normative_references:
      - "GB/T 1.1-2020"
      - "SL 75-2014"
      - "SL 426-2008"
      - "GB/T 28181-2016"
    key_technical_requirements:
      - "WSAL分级定义(L0-L5)"
      - "各等级功能要求和性能指标"
      - "数据采集精度与频率要求"
      - "控制算法响应时间要求"
      - "安全包络(ODD)边界条件"
    reference_doc: "research-materials/reports/SLT_水网智能调控系统技术要求_V3_征求意见稿.docx"
```

---

## 配置文件使用说明

### Claude读取规格时

1. 从 `docs/project_config.yaml` 加载配置
2. 根据用户指定的文档ID定位对应配置
3. 提取: `type` → 选择文体模板, `structure` → 生成提纲, `innovation` → 确认创新点
4. 提取: `must_cite` → 编制必引文献清单, `consistency_checks` → 确认CONS约束
5. 提取: `related_docs` → 读取前序文档用于衔接

### 配置文件级别

```
project_config.yaml        ← 项目级(定义所有文档)
  └── docs/SCI-P1a/spec.yaml  ← 文档级(覆盖/补充项目级配置)
```

文档级配置优先于项目级配置。

### 最小可用配置

对于单文档写作，最小配置为：

```yaml
documents:
  - id: "SCI-P1a"
    type: "SCI"
    title: "论文标题"
    target_journal: "目标期刊"
    innovation:
      - "创新点"
```

其余字段均可在讨论模式中由Claude与用户共同确定。

---

## 快速配置示例（实战场景）

### BK专著最小配置

```yaml
documents:
  - id: "BK-T1"
    type: "BK"
    title: "水系统控制论导论"
    subtitle: "Introduction to Cybernetics of Hydro Systems"
    language: "zh-CN"       # 双语标题，中文正文
    structure:
      parts: 4              # 第一部分:理论 第二部分:技术 第三部分:实践 第四部分:展望
      format: "modules"     # 模块化写作（§5 L3/L4级别）
    quality:
      readability_check: true
      min_score: 8.0
      reviewer_roles: ["教师", "专家", "工程师", "国际读者"]
    references:
      min_total: 200
      recent_5yr_pct: 35
      english_pct: 50
      self_cite_max_pct: 15
```

### SCI+CN+PAT批量配置

```yaml
project:
  name: "CHS-DMPC方法论"
  batch_strategy: "sequential"  # Batch1→2→3

documents:
  - id: "SCI-P2a"
    type: "SCI"
    title: "Distributed MPC for Open-Channel Networks"
    target_journal: "Water Resources Research"
    batch: 1
    innovation: ["DMPC框架", "分布式一致性证明"]

  - id: "CN-C2"
    type: "CN"
    title: "基于DMPC的渠系水位协调控制"
    target_journal: "水利学报"
    batch: 2
    depends_on: ["SCI-P2a"]
    innovation: ["中文工程化表述", "国内灌区适配"]

  - id: "PAT-PF2"
    type: "PAT"
    title: "一种分布式模型预测控制的明渠调控方法"
    batch: 2
    depends_on: ["SCI-P2a"]
    innovation: ["控制参数在线整定", "通信中断应急切换"]
```
