# 第七至十一章 插图（13幅）

> 生成方式分配：
> - 🎨 Gemini: 图9-1, 图10-1, 图10-4, 图10-5（概念图/架构图）
> - 🐍 matplotlib: 图7-1, 图7-3, 图11-1 → 见 `code_figures.py`
> - 📐 Mermaid: 图7-2, 图9-2, 图10-2, 图10-3 → 见 `mermaid_figures.md`
> - ♻️ 复用: 图8-1≈图6-3, 图8-2=图6-4

---

## 🐍 图 7-1: WNAL L0-L5 阶梯图

> **→ matplotlib 代码生成**: 见 `code_figures.py :: fig_07_01()`
> **已生成**: `generated/fig_07_01_wnal_ladder.png`
> 六级递增条形+L2/L3红色质变分界线。

---

## 📐 图 7-2: WNAL 等级跃迁四重门槛

> **→ Mermaid 代码生成**: 见 `mermaid_figures.md :: 图7-2`
> 四个门槛（技术/验证/治理/运行）汇入决策菱形的结构化流程。

---

## 🐍 图 7-3: 八原理与 WNAL 等级映射图

> **→ matplotlib 代码生成**: 见 `code_figures.py :: fig_07_03()`
> **已生成**: `generated/fig_07_03_principle_wnal_mapping.png`
> 8×6热力矩阵(P1-P8 × L0-L5)。

---

## ♻️ 图 8-1: 安全包络红黄绿三区示意图

> **复用图6-3**，增加ODD阈值标定说明注释。
> 源文件: `generated/fig_06_03_safety_envelope.png`

---

## ♻️ 图 8-2: 在环验证深度与 WNAL 等级对应图

> **复用图6-4**，仅更改图号。
> 源文件: `generated/fig_06_04_xil_wnal_matrix.png`

---

## 🎨 图 9-1（新增）: 水系统 CPSS 三层认知框架

**文件名**: fig_09_01_cpss_framework.png

**论文上下文**: 第九章§9.1，展示水系统作为信息-物理-社会系统(CPSS)的三层认知框架，是MBD方法论的顶层视角。

**提示词**:
A three-layer nested framework diagram showing water system as a Cyber-Physical-Social System (CPSS), designed for an academic textbook.

Three concentric rounded rectangles (or three interlocking circles in Venn diagram style):

OUTER layer — "社会层 Social Layer" (purple #7B1FA2 tint):
- Elements: 运行规程 SOP, 法规标准 Regulations, 利益相关者 Stakeholders, 公众参与 Public Engagement
- Label: "S — 社会系统 Social System"

MIDDLE layer — "信息层 Cyber Layer" (blue #1565C0 tint):
- Elements: 数字孪生 Digital Twin, 模型库 Model Repository, AI决策 AI Decision, 通信网络 Network
- Label: "C — 信息系统 Cyber System"

INNER layer — "物理层 Physical Layer" (green #4CAF50 tint):
- Elements: 水库 Reservoir, 渠道 Canal, 闸门 Gate, 泵站 Pump, 传感器 Sensor
- Label: "P — 物理系统 Physical System"

Arrows between layers:
- Physical→Cyber: "数据采集 Data Acquisition" (upward)
- Cyber→Physical: "控制指令 Control Commands" (downward)
- Cyber→Social: "决策支持 Decision Support" (upward)
- Social→Cyber: "目标约束 Objectives & Constraints" (downward)

Bottom annotation: "MBD关注焦点: C层模型如何精确映射P层行为 MBD Focus: How C-layer models map P-layer behaviors"

White background. Academic diagram style. Chinese+English labels.
Minimum 2400×1800 px. 300 DPI.

---

## 📐 图 9-2（新增）: MBD"四层一闭环"总体框架（详细版）

> **→ Mermaid 代码生成**: 见 `mermaid_figures.md :: 图9-2`
> 扩展版图3-2，展示每层内部子模块（ODD六维、四类模型、三级验证、SCADA+PLC）。

---

## 🎨 图 10-1: HydroOS 三层架构图

**文件名**: fig_10_01_hydroos_architecture.png

**论文上下文**: 第十章§10.2，HydroOS核心架构，展示设备抽象层(DAL)—物理AI层(PAI)—认知AI层(CAI)三层及其关键组件。

**提示词**:
A three-layer software architecture diagram for HydroOS (Hydro Operating System), designed for an academic textbook. Vertical stack layout.

TOP layer — "CAI 认知AI层 Cognitive AI Engine" (purple #7B1FA2):
- Components in boxes: 瀚铎大模型 Hando LLM, 知识图谱 Knowledge Graph, 多智能体协商 Multi-Agent Negotiation, 认知推理 Reasoning
- Interface label at bottom: "CAI-API"

MIDDLE layer — "PAI 物理AI层 Physical AI Engine" (blue #1565C0):
- Components: MPC控制器 MPC Controller, 安全包络引擎 Safety Envelope, 模型库管理 Model Mgr (PBM/SM/OSEM), 状态估计器 State Estimator
- Interface labels: top "PAI-API (接收CAI建议)", bottom "PAI-DAL接口"

BOTTOM layer — "DAL 设备抽象层 Device Abstraction Layer" (gray #757575):
- Components: 协议适配器 Protocol Adapter, 设备驱动 Device Driver, SCADA桥接 SCADA Bridge, 数据归一化 Data Normalization
- Bottom: physical devices icons (gate, pump, sensor)

Between layers: bidirectional arrows.
Left side annotation: "自主程度 ↑ Autonomy", Right side: "物理接近度 ↑ Physical Proximity"

White background. Clean software architecture style. Chinese+English labels. No 3D.
Minimum 2400×1800 px. 300 DPI.

---

## 📐 图 10-2: 策略门禁四项检查流程图

> **→ Mermaid 代码生成**: 见 `mermaid_figures.md :: 图10-2`
> 四项串行检查（安全/约束/权限/一致性），通过才放行。

---

## 📐 图 10-3: HydroOS 四态机状态转换图

> **→ Mermaid 代码生成**: 见 `mermaid_figures.md :: 图10-3`
> 四态（正常/降级/应急/检修）+迁移条件。

---

## 🎨 图 10-4: SCADA+MAS+HydroOS 融合架构图

**文件名**: fig_10_04_scada_mas_hydroos.png

**论文上下文**: §10.5，展示HydroOS如何在现有SCADA+多智能体(MAS)基础上叠加，而非替代。

**提示词**:
A three-layer overlay architecture diagram showing the evolution from SCADA to HydroOS, designed for an academic textbook.

Three overlapping horizontal layers (semi-transparent, showing the "additive" nature):

BOTTOM layer (gray, solid) — "SCADA层 SCADA Layer (已有 Existing)":
- Components: RTU/PLC, 组态软件 HMI, 历史数据库 Historian, 报警系统 Alarm
- Era label: "1990s~"

MIDDLE layer (blue, semi-transparent overlay) — "MAS层 Multi-Agent Layer (扩展 Extended)":
- Components: 区域Agent Regional Agent, 协商协议 Negotiation Protocol, 分布式决策 Distributed Decision
- Era label: "2010s~"

TOP layer (gradient blue-purple, semi-transparent) — "HydroOS层 (融合 Integrated)":
- Components: PAI物理AI, CAI认知AI, 安全包络 Safety Envelope, 统一API Unified API
- Era label: "2020s~"

Arrows: SCADA data feeds upward to MAS and HydroOS. HydroOS controls down through SCADA actuators. MAS agents communicate laterally within their layer.

Key message annotation: "HydroOS = 在SCADA+MAS上叠加AI层，不替代底层 HydroOS adds AI layers on top, does not replace SCADA"

White background. Layered architecture with transparency. Chinese+English labels.
Minimum 2400×1600 px. 300 DPI.

---

## 🎨 图 10-5: HydroOS 分级部署路径与 WNAL 等级对应

**文件名**: fig_10_05_hydroos_deployment.png

**论文上下文**: §10.6，展示从WNAL L1到L4，HydroOS各层模块如何逐步部署激活。

**提示词**:
A deployment roadmap diagram showing how HydroOS modules activate at each WNAL level, designed for an academic textbook.

Horizontal axis: WNAL levels L1 → L2 → L3 → L4 (left to right, ascending steps).
Vertical axis: three HydroOS layers (DAL bottom, PAI middle, CAI top).

At each WNAL level, show which modules are activated (filled box) vs not yet deployed (dashed box):

L1: DAL basic (filled), PAI basic rules (filled), CAI none (dashed)
L2: DAL full (filled), PAI MPC+model (filled), CAI none (dashed)  
L3: DAL full, PAI full + safety envelope (filled), CAI basic LLM advisor (filled)
L4: DAL full, PAI full + self-diagnosis (filled), CAI full multi-agent (filled)

Use progressive color fill from light to dark as capabilities increase.
Red dashed vertical line between L2 and L3: "质变: CAI上线 Phase Change: CAI Online"

White background. Roadmap/deployment matrix style. Chinese+English labels.
Minimum 2400×1200 px. 300 DPI.

---

## 🐍 图 11-1: PAI-CAI 协作工作流

> **→ matplotlib 代码生成**: 见 `code_figures.py :: fig_11_01()`（待补充）
> 双泳道时序图：PAI泳道（蓝）和CAI泳道（紫），四阶段协作流程。
