# MBD论文（上下篇）插图生成提示词

> **使用说明**: 本文件为MBD两篇论文共3张图的生成提示词，供图片生成工具使用。
> **风格统一要求**: 学术期刊论文插图风格，黑白灰+蓝色点缀，白色背景，**纯中文标注**，矢量感线框图，适合单栏/双栏排版印刷。
> **输出格式**: PNG或SVG，分辨率≥600dpi，宽度适合期刊单栏（~85mm）或双栏（~170mm）排版。
> **重要**: 图中所有文字标注均使用中文，不加英文翻译。仅保留国际通用缩写（MBD、ODD、MPC、PBM、SM等）。

---

## 上篇（Ⅰ）：1张图

### 图1　"多学科模型独立+系统级统一仿真验证"的底座能力示意

**文件名**: MBD_A_fig1_unified_simulation_platform.png

**论文上下文**: 四类模型（PBM高保真物理模型、SM简化模型、OSEM在线状态估计模型、HDC/MAS控制策略模型）通过标准化接口协同工作，构成统一仿真验证平台。PBM与SM构成"校准—验证"循环；OSEM输出驱动SM预测和控制策略决策；控制策略指令经PBM闭环验证。SIL阶段控制代码与SM/OSEM运行于软件环境、PBM提供虚拟被控对象；HIL阶段控制策略运行于真实PLC/RTU硬件。底层由ODD场景库驱动标准化测试输入。设计阶段模型资产交付运行期数字孪生，运行数据回馈仿真平台形成持续进化闭环。

**提示词**:
A technical block diagram for an academic journal paper showing a unified multi-model simulation and verification platform for water network engineering. White background, black/dark gray lines, minimal blue accent color. Suitable for journal layout (~170mm width). ALL TEXT LABELS IN CHINESE ONLY, no English translations. Keep only standard abbreviations (PBM, SM, OSEM, HDC/MAS, MIL, SIL, HIL, ODD, MRC, MPC).

Central area contains four model blocks arranged in a 2×2 grid, each as a rounded rectangle with thin black border:
- Top-left: "PBM 物理对象模型" (dark gray fill) with subtitle "圣维南方程 / 水动力学"
- Top-right: "SM 简化控制模型" (light gray fill) with subtitle "IDZ传递函数 / Muskingum"
- Bottom-left: "OSEM 状态估计模型" (light gray fill) with subtitle "EKF / UKF / 数据同化"
- Bottom-right: "HDC/MAS 控制策略模型" (light gray fill) with subtitle "分层MPC / 智能体"

Directed arrows between model blocks showing data flow:
- PBM → SM: labeled "降阶/标定" (dashed arrow)
- SM ↔ OSEM: bidirectional, labeled "状态驱动/预测反馈"
- OSEM → HDC/MAS: labeled "状态估计值"
- HDC/MAS → PBM: labeled "控制指令（闭环验证）"
- PBM → SM: labeled "误差边界标定"

Below the 4-model grid: a wide horizontal bar (blue accent fill) labeled "ODD场景库" with upward arrows to all four models, labeled "标准化测试输入（水文/设备故障/通信干扰）"

Right side: a vertical bracket grouping three verification stages:
- "MIL：算法+模型纯软件环境"
- "SIL：控制代码+虚拟对象"
- "HIL：真实PLC/RTU+实时仿真器"
Each stage connected by downward arrow showing progression labeled "逐级逼近".

Top: a horizontal feedback loop spanning the full width: left label "设计阶段" → center "模型资产交付" → right "运行阶段" → bottom return arrow "实测数据回馈/参数校正", forming a "设计—运行—再验证" evolution loop.

Three interface design principles noted in a small annotation box (bottom-right corner): "①单向数据流 ②时间同步 ③故障隔离（MRC）"

Clean technical block diagram suitable for academic journal printing. Black/gray lines, minimal decoration, no 3D effects, no shadows.

---

## 下篇（Ⅱ）：2张图

### 图1　CPSS框架下关键技术之间的工程逻辑关系

**文件名**: MBD_B_fig1_engineering_chain.png

**论文上下文**: 从上篇模型体系到实际工程部署的四环节技术工程链：SIM仿真平台建设→ODD场景定义→MAS协同部署→SIL/HIL在环验证。SIM平台需实现多模型异步耦合、场景批量注入、软硬件接口预留。ODD将水文、设备、通信、管理四维参数正交组合定义运行域边界。MAS部署包括HDC三层架构参数化配置、协商协议设计、安全降级策略。在环验证遵循五元组证据链机制。整体嵌入CPSS框架，现场执行与数据回馈形成持续进化闭环。

**提示词**:
A horizontal engineering chain diagram for an academic journal paper showing four key technology stages under the CPSS framework. White background, black/dark gray lines, blue accent. Suitable for double-column journal layout (~170mm width). ALL TEXT LABELS IN CHINESE ONLY, no English translations.

Four main stages arranged left-to-right as rectangular blocks connected by thick forward arrows:

**Stage 1** (leftmost, thin black border): "SIM 仿真平台" — three items inside: "多模型异步耦合", "场景批量注入", "软硬件接口预留"

**Stage 2**: "ODD 场景定义" — inside: "六维参数正交组合" with sub-items: "水文 | 设备 | 通信 | 环境 | 社会 | 运行模式", plus "运行域边界划分"

**Stage 3**: "HDC/MAS 协同部署" — inside: "三层架构参数化配置", "协商协议设计", "安全降级→MRC"

**Stage 4** (rightmost): "SIL/HIL 在环验证" — inside: "五元组证据链", "覆盖度×通过率"

Above all four stages: a horizontal banner labeled "CPSS框架" spanning the full width, with three sub-labels: "信息层：模型与算法", "物理层：设备与通信", "社会层：管理与规程"

Below all four stages: a wide return arrow from Stage 4 back to Stage 1, labeled "现场执行→数据回馈→模型校正→持续进化闭环"

Between stages, the forward arrows are labeled:
- Stage 1→2: "场景激励"
- Stage 2→3: "ODD约束"
- Stage 3→4: "可执行代码"

A dashed upward arrow from "ODD场景定义" to the CPSS banner, labeled "调度规程映射→场景盲区审计"

Clean horizontal flow diagram. Black/gray with minimal blue accent. No decorative elements.

---

### 图2　ODD驱动的SIL/HIL在环验证与证据链形成示意

**文件名**: MBD_B_fig2_verification_evidence_chain.png

**论文上下文**: 验证流程遵循ODD驱动的五元组证据链机制：五元组 = {ODD场景标识, 验证级别(MIL/SIL/HIL), 性能指标, 通过/未通过判据, 时间戳与版本号}。每完成一项场景的某级别验证即生成一条五元组记录，全部记录汇聚为证据矩阵，其覆盖度和通过率构成MBD交付质量的定量评估指标。SIL关注：代码与算法一致性、边界条件、异常鲁棒性、多线程时序安全。HIL在SIL基础上增加：I/O响应延迟、工业通信可靠性、实时同步精度、硬件故障安全降级。

**提示词**:
A verification workflow and evidence chain diagram for an academic journal paper. White background, black/dark gray lines, blue and green accents. Suitable for double-column journal layout (~170mm width). ALL TEXT LABELS IN CHINESE ONLY, no English translations.

**Left portion — 验证流程（自上而下）:**

Top: rounded rectangle "ODD场景库" (blue border) with annotation "N个标准化场景". Three downward arrows fanning out to three verification level boxes arranged vertically:

Level 1 box: "MIL 模型在环" (lightest gray fill) — right annotation: "算法+模型 纯软件"
Level 2 box: "SIL 软件在环" (medium gray fill) — right annotation: "控制代码+虚拟对象", sub-items: "代码一致性 | 边界条件 | 异常鲁棒性 | 时序安全"
Level 3 box: "HIL 硬件在环" (darker gray fill) — right annotation: "真实PLC/RTU+实时仿真", sub-items: "I/O延迟 | 通信可靠性 | 同步精度 | 故障降级"

Downward arrows between levels labeled "逐级递进". Each level has a small output arrow to the right pointing to...

**Right portion — 证据链矩阵:**

A matrix/table structure:
- Rows: ODD场景（S₁, S₂, ... Sₙ）
- Columns: MIL, SIL, HIL
- Each cell contains a five-tuple record icon: "{场景ID, 级别, 指标, 判据, 时间戳}"
- Cells filled with checkmark (✓ 通过, green) or cross (✗ 未通过, red) or dash (— 待验证, gray)

Below the matrix: two metric bars:
- "覆盖度 = 已验证场景数 / ODD场景总数" with a horizontal progress bar
- "通过率 = 通过数 / 已验证数" with a horizontal progress bar

Bottom: a wide box labeled "MBD交付质量定量评估" receiving inputs from both metrics.

A feedback arrow from the bottom back up to "ODD场景库", labeled "未覆盖场景→补充测试 | 未通过场景→算法修正→重新验证"

Clean technical diagram combining flowchart and matrix. Black/gray with blue/green accents. No decorative elements, suitable for print.

---

## 统计

| 论文 | 图数 | 图号与名称 |
|------|------|-----------|
| 上篇（Ⅰ） | 1 | 图1 "多学科模型独立+系统级统一仿真验证"的底座能力示意 |
| 下篇（Ⅱ） | 2 | 图1 CPSS框架下关键技术之间的工程逻辑关系 |
|  |  | 图2 ODD驱动的SIL/HIL在环验证与证据链形成示意 |
| **合计** | **3** | |
