# 第三至六章 插图（10幅）

> 生成方式分配：
> - 🎨 Gemini: 图5-1, 图5-2, 图6-2（概念图/架构图）
> - 🐍 matplotlib: 图3-1, 图6-3, 图6-4, 图6-5 → 见 `code_figures.py`
> - 📐 Mermaid: 图3-2 → 见 `mermaid_figures.md`
> - ♻️ 复用: 图4-1=图2-2, 图6-1=图3-1

---

## 🐍 图 3-1: CHS 八原理依赖导图

> **→ matplotlib 代码生成**: 见 `code_figures.py :: fig_03_01()`（待补充，与fig_01_04()同源但更详细）
> 五层DAG，含P4→P8红色约束回边。
> ⚠️ 图6-1复用本图。

---

## 📐 图 3-2: MBD 四层一闭环架构

> **→ Mermaid 代码生成**: 见 `mermaid_figures.md :: 图3-2`
> 四层纵向结构+底层到顶层的闭环回边。

---

## ♻️ 图 4-1: 可控模型族的三层体系

> **复用图2-2**，仅更改图号。
> 源文件: `generated/fig_02_02_model_family.png`

---

## 🎨 图 5-1（新增）: 可控性与可观性的直觉解释

**文件名**: fig_05_01_controllability_observability.png

**论文上下文**: 第五章§5.1，用直觉图示解释控制论中可控性和可观性的物理含义，帮助水利读者理解抽象概念。

**提示词**:
A side-by-side conceptual diagram explaining controllability and observability for a water engineering textbook.

LEFT panel — "可控性 Controllability" (blue #1565C0 background tint):
- A water reservoir with an adjustable gate at the outlet
- Arrows showing: control input u → gate opening → water level changes
- Metaphor: "能否通过闸门控制水位到达任意目标？ Can the gate drive water level to any target?"
- Green checkmark for controllable state, red X for uncontrollable state
- Example: gate fully controls downstream level ✓; upstream inflow uncontrollable ✗

RIGHT panel — "可观性 Observability" (green #4CAF50 background tint):
- Same reservoir with sensors at different locations
- Arrows showing: water level → sensor readings → estimated state
- Metaphor: "能否通过传感器推断全部内部状态？ Can sensors reveal all internal states?"
- Green checkmark where sensors cover well, red X for blind spots
- Example: water level measured ✓; sediment concentration unobserved ✗

Center dividing line. Bottom summary: "可控性+可观性 = 闭环控制的前提条件 Prerequisites for Closed-loop Control"

White background. Academic illustration style. Chinese+English labels. No 3D effects.
Minimum 2400×1600 px. 300 DPI.

---

## 🎨 图 5-2（新增）: 传感器优化布局概念图

**文件名**: fig_05_02_sensor_layout.png

**论文上下文**: §5.3，展示在管网/渠道系统中如何通过优化传感器布局来保障系统可观性。

**提示词**:
A network topology diagram showing sensor placement optimization for a water distribution system, designed for an academic textbook.

A simplified water network with: 1 reservoir (top, blue filled), 3 junction nodes (circles), 5 pipe segments (lines with arrows for flow direction), 2 demand points (bottom, green).

Sensor placement shown in two scenarios:
- LEFT scenario "冗余布局 Redundant": every node has a sensor (yellow triangle icon) — 7 sensors total, some redundant
- RIGHT scenario "优化布局 Optimized": only 4 sensors at key nodes — determined by observability Gramian analysis

Color coding: nodes with sensors = solid yellow triangle marker; nodes without = hollow circle; critical nodes (where sensor is essential) = red border.

A small observability index bar chart at bottom comparing: redundant layout (score 0.95) vs optimized layout (score 0.92) — nearly equal observability with fewer sensors.

White background. Clean network diagram style. Chinese+English labels.
Minimum 2400×1600 px. 300 DPI.

---

## ♻️ 图 6-1: CHS 八原理依赖导图

> **复用图3-1**，仅更改图号。

---

## 🎨 图 6-2: CHS 四层分布式控制架构图

**文件名**: fig_06_02_four_layer_architecture.png

**论文上下文**: 第六章§6.2 P3分层分布式控制原理详述，展示治理—全局—区域—执行四层结构及信息流。

**提示词**:
A four-layer hierarchical and distributed control architecture diagram for water systems, designed for an academic textbook.

Four horizontal layers stacked vertically (top to bottom):

Layer 1 (top, purple #7B1FA2 tint): "治理层 Governance Layer"
- Contains: 政策目标 Policy Goals, 长期规划 Long-term Planning, 公共安全约束 Safety Constraints
- Timescale: 年/季 Year/Season

Layer 2 (deep blue #1565C0): "全局优化层 Global Optimization Layer"  
- Contains: 水资源分配 Resource Allocation, 多目标优化 Multi-Obj Optimization, 冲突协调 Conflict Resolution
- Timescale: 月/旬 Month/Dekad

Layer 3 (blue #42A5F5): "区域协调层 Regional Coordination Layer"
- Contains: 子系统协调 Subsystem Coordination, 分布式MPC, Agent协商 Agent Negotiation
- Timescale: 日/时 Day/Hour

Layer 4 (bottom, gray #757575): "执行控制层 Execution Control Layer"
- Contains: PID/MPC本地控制, SCADA数据采集, 执行器动作 Actuator Commands
- Timescale: 分/秒 Min/Sec

Between layers: downward solid arrows (目标下达 Target Dispatch) and upward dashed arrows (状态反馈 State Feedback).
Between nodes in same layer: horizontal bidirectional arrows (对等协商 Peer Negotiation).

Left axis label: "时间尺度递减 ↓ Timescale". Right axis label: "空间粒度递减 ↓ Spatial Scale"

White background. Clean layered architecture style. Chinese+English labels. No 3D.
Minimum 2400×1800 px. 300 DPI.

---

## 🐍 图 6-3: 安全包络红黄绿三区示意图

> **→ matplotlib 代码生成**: 见 `code_figures.py :: fig_06_03()`
> **已生成**: `generated/fig_06_03_safety_envelope.png`
> 时序曲线+三色区间+切换逻辑流程图。
> ⚠️ 图8-1复用本图（微调阈值标注）。

---

## 🐍 图 6-4: 在环验证深度与 WNAL 等级对应图

> **→ matplotlib 代码生成**: 见 `code_figures.py :: fig_06_04()`
> **已生成**: `generated/fig_06_04_xil_wnal_matrix.png`
> 3×6热力矩阵(MIL/SIL/HIL × L0-L5)。
> ⚠️ 图8-2复用本图。

---

## 🐍 图 6-5: 自主演进三重闭环示意图

> **→ matplotlib 代码生成**: 见 `code_figures.py :: fig_06_05()`（待补充）
> 三重嵌套环形：数据闭环（内）→ 模型闭环（中）→ 策略闭环（外），原编号图6-6。
