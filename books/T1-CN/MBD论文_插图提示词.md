# MBD论文（上下篇）插图生成提示词

> **使用说明**: 本文件为MBD论文上下篇共3张插图的生成提示词。
> **风格统一要求**: 学术期刊风格，蓝色系主色调，白色背景，清晰中文标注（附英文），矢量感/扁平化设计，无过度装饰。
> **输出格式**: PNG，分辨率≥300dpi，宽度≥2000px
> **目标期刊**: 《水利学报》/ Journal of Hydraulic Engineering（中文核心期刊，单栏图宽≤80mm，双栏图宽≤170mm）

---

## 上篇（Ⅰ）：MBD内涵与模型体系

### 图1：多学科模型独立+系统级统一仿真验证的底座能力示意

**文件名**: fig_paperA_1_unified_simulation_platform.png

**论文上下文**: §5"多模型耦合集成与统一仿真平台"。四类模型（PBM、SM、OSEM、HDC/MAS）通过标准化接口协同工作，构成统一仿真验证平台。PBM与SM构成"校准—验证"循环；OSEM驱动SM预测和控制决策；控制策略经PBM闭环验证。SIL阶段控制代码与SM/OSEM运行于软件环境、PBM提供虚拟被控对象；HIL阶段控制策略运行于真实PLC/RTU硬件。模型耦合遵循三项原则：单向数据流、时间同步、故障隔离。场景与环境模型由ODD边界库生成标准化测试输入。

**提示词**:

A professional academic diagram showing a unified simulation and verification platform for water network MBD (Model-Based Definition). White background, blue color scheme (#003366 to #4499CC gradient). Landscape orientation, approximately 2400×1600px.

**Central area — Four Model Components arranged in a 2×2 grid, each as a rounded rectangle card:**

Top-left card (fill #E3F2FD, border #0055A4): "PBM 物理对象模型" with a small icon of Saint-Venant equations / wave propagation. Subtitle: "高保真水力仿真 | 虚拟被控对象". Annotation: "Saint-Venant方程 / 有限差分".

Top-right card (fill #E8F5E9, border #388E3C): "SM 面向控制的简化模型" with a small icon of transfer function block. Subtitle: "实时预测与优化 | 预测控制内核". Annotation: "IDZ传递函数 / Muskingum / MPC".

Bottom-left card (fill #FFF3E0, border #FF9800): "OSEM 观测与状态估计模型" with a small icon of Kalman filter / data fusion. Subtitle: "状态重构与融合 | 感知-决策桥梁". Annotation: "EKF / UKF / 数据同化".

Bottom-right card (fill #F3E5F5, border #7B1FA2): "HDC/MAS 控制策略模型" with a small icon of hierarchical agents. Subtitle: "协同控制与决策 | 待验证控制逻辑". Annotation: "分层MPC / BDI智能体".

**Interaction arrows between cards (curved Bezier paths, colored by data type):**

- PBM ↔ SM: blue bidirectional arrow labeled "校准—验证循环" (SM从PBM降阶, PBM标定SM误差边界)
- OSEM → SM: orange arrow labeled "状态估计驱动预测"
- OSEM → HDC/MAS: orange arrow labeled "状态估计驱动决策"
- HDC/MAS → PBM: green arrow labeled "控制指令 → 闭环验证"

**Bottom foundation bar (dark blue #003366, spanning full width):**

"ODD场景库 / 场景与环境模型" with three small icons: hydrological process icon, equipment fault icon, communication interference icon. Label: "标准化测试输入 → MIL/SIL/HIL各阶段一致场景激励". Upward arrows from this bar feeding into all four model cards.

**Right side — Verification progression column (three stacked boxes):**

Box 1 (lightest, top): "MIL 模型在环" — "PBM + SM + OSEM + HDC/MAS 全软件闭环"
Box 2 (medium): "SIL 软件在环" — "控制代码编译 + SM/OSEM软件环境 + PBM虚拟对象"
Box 3 (darkest, bottom): "HIL 硬件在环" — "真实PLC/RTU硬件 + 工业通信 + PBM实时仿真器"

Downward arrow through three boxes labeled "逐级逼近真实运行条件".

**Top annotation strip (three interface design principles in rounded pills):**

"① 单向数据流" | "② 时间同步" | "③ 故障隔离(MRC降级)"

**Bottom-right feedback loop:**

A dashed curved arrow from "现场运行数据" back up to PBM and ODD bar, labeled "参数动态校正 + ODD边界更新 → 持续进化闭环".

Clean academic diagram. Flat design, no 3D effects. Chinese labels with English subtitles in parentheses. Suitable for Journal of Hydraulic Engineering single-page width figure.

---

## 下篇（Ⅱ）：总体框架与工程验证

### 图1：CPSS框架下关键技术之间的工程逻辑关系

**文件名**: fig_paperB_1_engineering_chain.png

**论文上下文**: §3"关键技术工程链"。从上篇模型体系到实际工程部署，需要四个核心环节串联：SIM仿真平台建设→ODD场景定义→MAS协同部署→SIL/HIL在环验证。SIM平台需实现多模型异步耦合、场景批量注入、软硬件接口预留；ODD场景生成兼顾覆盖性与经济性（正交试验→故障树→极端场景）；MAS部署包括HDC三层参数化配置、协商协议设计、安全降级策略实现；在环验证基于五元组证据链。上方是"四层一闭环"总体框架（ODD定义层→模型决策层→在环验证层→现场执行层），下方是三类适用场景（供水调度、防洪减灾、水资源综合利用）。

**提示词**:

A professional academic diagram showing the engineering chain between key technologies under the CPSS (Cyber-Physical-Social Systems) framework for water network MBD. White background, blue color scheme. Landscape orientation, approximately 2400×1800px.

**Top banner — "四层一闭环" Framework Overview (horizontal flow with feedback):**

Four layer boxes arranged left to right, each a wide rounded rectangle:

Layer 1 (fill #E3F2FD): "ODD定义层" — "运行场景分类与边界约束 → ODD参数表与场景库"
Layer 2 (fill #BBDEFB): "模型决策层" — "多模型耦合仿真与控制策略优化 → 仿真验证报告"
Layer 3 (fill #90CAF9): "在环验证层" — "MIL→SIL→HIL分级验证 → 五元组证据链"
Layer 4 (fill #64B5F6): "现场执行层" — "控制策略部署与实时运行 → 运行数据"

Forward arrows between layers (solid blue). A long dashed feedback arrow from Layer 4 back to Layer 1, arcing above all layers, labeled "数据回馈 → 持续进化闭环".

**Central area — Engineering Chain (four nodes connected by thick forward arrows):**

Node 1 (large rounded rectangle, fill #E8F5E9, border #4CAF50): "SIM 仿真平台建设" with three sub-items stacked vertically: "多模型异步耦合", "场景批量注入", "软硬件接口预留". Icon: simulation dashboard.

→ thick arrow →

Node 2 (fill #FFF3E0, border #FF9800): "ODD 场景定义" with three sub-items: "正交试验/拉丁超立方(正常域)", "故障树+历史事件(扩展域)", "安全分析(MRC边界)". Icon: parameter space grid. Annotation: "六维参数向量: 水文/设备/通信/环境/社会/运行模式".

→ thick arrow →

Node 3 (fill #F3E5F5, border #7B1FA2): "HDC/MAS 协同部署" with three sub-items: "HDC三层参数化配置", "MAS协商协议设计", "安全降级策略(MRC)". Icon: hierarchical agent network.

→ thick arrow →

Node 4 (fill #FFEBEE, border #D32F2F): "SIL/HIL 在环验证" with three sub-items: "五元组证据链", "覆盖度与通过率", "增量验证机制". Icon: test report with checkmarks.

Between each pair of nodes: a small diamond gate icon labeled "质量门禁".

**Bottom strip — Three Scenario Adaptations (three columns):**

Column A (fill #E3F2FD): "供水调度" — "ODD侧重: 流量变化/用水波动/冰期" | "时间尺度: 分钟→旬月" | "典型工程: 南水北调/胶东调水"

Column B (fill #FFF3E0): "防洪减灾" — "ODD侧重: 极端来水/设备故障/通信中断" | "时间尺度: 分钟→小时" | "典型工程: 流域梯级水电站"

Column C (fill #F3E5F5): "水资源综合利用" — "ODD侧重: 多目标权衡/社会约束" | "时间尺度: 日内→年际" | "典型工程: 多功能水库群"

Dashed upward arrows from each column to the Engineering Chain, labeled "差异化适配".

Clean academic diagram. Flat design, no 3D. Chinese labels with English in parentheses. Suitable for journal two-column width figure.

---

### 图2：ODD驱动的SIL/HIL在环验证与证据链形成示意

**文件名**: fig_paperB_2_odd_driven_verification_evidence_chain.png

**论文上下文**: §3.4"SIL/HIL在环验证与证据链"。验证流程遵循ODD驱动的五元组证据链机制：五元组 = {ODD场景标识, 验证级别(MIL/SIL/HIL), 性能指标, 通过/未通过判据, 时间戳与版本号}。每完成一项场景的某级别验证，即生成一条五元组记录，全部记录汇聚为证据矩阵，覆盖度和通过率构成定量评估指标。SIL关注：代码与算法一致性、边界条件、异常输入鲁棒性、多线程时序安全。HIL在SIL基础上增加：I/O响应延迟、通信协议可靠性、实时同步精度、硬件故障下安全降级。

**提示词**:

A professional academic diagram showing the ODD-driven SIL/HIL verification and evidence chain formation process. White background, blue color scheme. Landscape orientation, approximately 2400×1600px.

**Left side — ODD Scene Library (vertical stack):**

A tall rounded rectangle (fill #E3F2FD, border #0055A4) labeled "ODD场景库" at top. Inside, three stacked sections representing three ODD zones:

Top section (green tint): "正常运行域 Normal" — "典型工况组合 (正交试验/拉丁超立方)"
Middle section (yellow tint): "扩展运行域 Extended" — "关键风险场景 (故障树+历史事件)"
Bottom section (red tint): "MRC边界域" — "极端场景 (安全分析)"

Six dimension icons along the left edge: 水文, 设备, 通信, 环境, 社会, 运行模式.

Rightward arrows from the scene library, labeled "场景注入", pointing to the verification stages.

**Center — Three-Stage Verification Pipeline (horizontal flow):**

Three large stage boxes arranged left to right, connected by thick forward arrows with gate checkpoints:

Stage 1 (fill #E8F5E9): "MIL 模型在环" — inside: "算法 + PBM闭环". Focus items: "功能正确性验证". Small icon of mathematical model loop.

Stage 2 (fill #FFF3E0): "SIL 软件在环" — inside: "编译代码 + 软件环境". Focus items in a small list: "代码-算法一致性", "边界条件处理", "异常输入鲁棒性", "多线程时序安全". Small icon of code compilation.

Stage 3 (fill #FFEBEE): "HIL 硬件在环" — inside: "真实PLC/RTU + 工业通信". Focus items in a small list: "I/O响应延迟", "通信协议可靠性(丢包/超时)", "实时同步精度", "硬件故障安全降级". Small icon of hardware board.

Between stages: diamond gate icons. A reject/rework loop arrow arcs backward from each gate back to the previous stage, labeled "未通过 → 修正重验".

**Right side — Evidence Chain Formation (vertical assembly):**

A wide rounded rectangle (fill #F5F5F5, border #333333) labeled "五元组证据链" at top.

Inside, a small table/matrix representation:

Header row: "ODD场景ID | 验证级别 | 性能指标 | 通过/未通过 | 时间戳+版本"

Three example rows (abbreviated), each with a colored status dot (green = pass, red = fail).

Below the table: two metric badges:

Badge 1 (blue pill): "覆盖度 = 已验证场景数 / ODD场景总数"
Badge 2 (green pill): "通过率 = 通过数 / 已验证数"

**Bottom feedback arrow:**

A dashed curved arrow from the evidence chain back to the ODD scene library, labeled "运行数据回馈 → ODD边界更新 + 场景库增量扩充".

**Top annotation:**

A thin banner: "ODD驱动原则: 场景定义先于验证执行 → 验证什么由ODD决定，而非由算法开发者选择"

Clean academic diagram. Flat design, no 3D effects. Chinese labels with English in parentheses. Suitable for journal two-column width figure.

---

## 统计

| 论文 | 图数 | 图号与标题 |
|------|------|-----------|
| 上篇(Ⅰ) | 1 | 图1 多学科模型独立+系统级统一仿真验证的底座能力示意 |
| 下篇(Ⅱ) | 2 | 图1 CPSS框架下关键技术之间的工程逻辑关系 |
|  |  | 图2 ODD驱动的SIL/HIL在环验证与证据链形成示意 |
| **合计** | **3** | |
