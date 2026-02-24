# T1-CN Gemini AI 图片生成专用提示词

> **生成策略**（根据 MULTI_ROUTE_STRATEGY.md）：
> - ✅ **纯 Gemini 生成**：6 幅（创意视觉/工程示意图）
> - ⚠️ **已改用 HTML/SVG**：7 幅（原定 Gemini，现改代码生成以提升精度）
> 
> **本文件仅包含纯 Gemini 生成的 6 幅图**

---

## 🎯 纯 Gemini 生成清单（6 幅）

根据 MULTI_ROUTE_STRATEGY.md 第二部分 D 节，以下图片适合用 Gemini 生成：

| 编号 | 标题 | 原因 | 文件 |
|------|------|------|------|
| 图1-1 | 五代演进信息图 | 需要图标/视觉隐喻 | ch01_figures.md |
| 图1-2 | 自动化 vs 自主运行 | 左右对比概念 | ch01_figures.md |
| 图1-3 | WNAL-SAE 对比阶梯 | 双阶梯视觉类比 | ch01_figures.md |
| 图5-1 | 可控可观性直觉图 | 水库+闸门直觉比喻 | ch03-06_figures.md |
| 图12-1 | 枕头坝—沙坪耦合 | 工程剖面图 | ch12-13_figures.md |
| 图13-1 | 梯级三站拓扑 | 工程拓扑+河流示意 | ch12-13_figures.md |

---

## 📋 详细提示词

### 图 1-1: 水利工程运行管理系统五代演进图

**文件名**: `fig_01_01_five_generations.png`

**上下文**: 第一章§1.2，概述水利工程运行管理从1950s人工到2020s自主运行的五代演进历程，是全书的时代背景铺垫。

**Gemini 提示词**:
```
A horizontal timeline infographic showing five generations of water system operation management evolution, designed for an academic textbook.

From left to right, five vertical cards connected by a bold progress arrow:
- Gen 1 (1950s-1970s): "人工运行 Manual Operation" — icon: person with clipboard at dam. Background color: gray (#BDBDBD).
- Gen 2 (1980s-1990s): "SCADA自动化 SCADA Automation" — icon: CRT monitor with alarm. Background color: light blue (#90CAF9).
- Gen 3 (2000s): "网络化调度 Networked Dispatch" — icon: network topology with database. Background color: blue (#42A5F5).
- Gen 4 (2010s): "数字孪生 Digital Twin" — icon: 3D water network model. Background color: deep blue (#1565C0).
- Gen 5 (2020s→): "自主运行 Autonomous Operation" — icon: AI brain with water network. Background color: gold (#FFB300), dashed border (ongoing).

Each card shows: decade range on top, Chinese+English name in center, brief description below, small icon.
Bottom axis: arrow labeled "智能化程度递增 Intelligence Level →".

White background. Clean academic infographic style. Chinese+English labels. No decorative elements.
Minimum 2400×1200 px. 300 DPI.
```

---

### 图 1-2: 自动化与自主运行对比示意图

**文件名**: `fig_01_02_auto_vs_autonomous.png`

**上下文**: §1.3，核心概念辨析——"自动化"(Automation)按预设规则执行 vs "自主运行"(Autonomous Operation)具备感知-决策-执行-学习闭环能力。

**Gemini 提示词**:
```
A split comparison diagram for an academic textbook, divided into left and right halves by a vertical dashed line.

LEFT side — "自动化 Automation" (blue background #E3F2FD):
- Top: "预设规则 Pre-set Rules" box
- Arrow down to "执行器 Actuator" box
- Arrow down to "水利系统 Hydro System" box
- Side label: "开环/固定规则 Open-loop / Fixed Rules"
- Characteristics listed: 规则固定 Fixed Rules, 无学习能力 No Learning, 异常依赖人工 Manual Fallback

RIGHT side — "自主运行 Autonomous Operation" (green background #E8F5E9):
- A closed loop: "感知 Perceive" → "决策 Decide" → "执行 Act" → "学习 Learn" → back to "感知"
- Center of loop: "水利系统 Hydro System"
- Characteristics listed: 自适应策略 Adaptive, 持续学习 Continuous Learning, 自动降级 Auto Degradation

Center dividing line labeled: "关键区别 Key Difference"
Bottom comparison bar: 自动化=被动响应 Reactive ↔ 自主运行=主动决策 Proactive

White background. Clean academic style. Chinese+English labels.
Minimum 2400×1600 px. 300 DPI.
```

---

### 图 1-3: WNAL L0-L5 与 SAE 自动驾驶等级对比图

**文件名**: `fig_01_03_wnal_sae_comparison.png`

**上下文**: §1.4，将水网自主等级WNAL类比自动驾驶SAE分级，帮助读者建立直觉理解。

**Gemini 提示词**:
```
A side-by-side staircase comparison diagram for an academic textbook.

LEFT staircase — "WNAL 水网自主等级" (blue color scheme #1565C0):
Six ascending steps from bottom: L0手动运行, L1规则自动化, L2模型优化, L3条件自主, L4高度自主, L5完全自主.
A red dashed line between L2 and L3 labeled "质变节点 Critical Threshold".

RIGHT staircase — "SAE 自动驾驶等级" (purple color scheme #7B1FA2):
Six ascending steps: L0无自动化, L1驾驶辅助, L2部分自动, L3条件自动, L4高度自动, L5完全自动.
A red dashed line between L2 and L3.

Between two staircases, horizontal dashed arrows connecting corresponding levels (L0↔L0, L1↔L1, ..., L5↔L5), showing the analogy.

Bottom label: "共同特征 Common Features: 渐进分级 Gradual Levels → L2/L3质变 Phase Transition → 安全约束 Safety Constraints"

White background. Academic comparison chart style. Chinese+English labels.
Minimum 2400×1600 px. 300 DPI.
```

---

### 图 5-1: 可控性与可观性的直觉解释

**文件名**: `fig_05_01_controllability_observability_intuition.png`

**上下文**: 第五章§5.1，用水库-闸门-传感器的直觉比喻，帮助非控制专业读者理解可控性与可观性。

**Gemini 提示词**:
```
A split intuitive diagram for an academic textbook explaining controllability and observability in water systems.

LEFT side — "可控性 Controllability":
A simplified side-view of a reservoir with an outlet gate (sluice gate).
- Reservoir labeled "水库 Reservoir" (water level shown)
- Outlet gate labeled "闸门 Gate" (red, partially open)
- Arrow from gate to water level labeled "能否控制? Can control?"
- Annotation: "闸门影响水位 Gate affects level → 可控 Controllable"
- Background color: light blue (#E3F2FD)

RIGHT side — "可观性 Observability":
The same reservoir with multiple sensors.
- Water level sensor at top (green) labeled "水位计 Level Sensor"
- Flow meter at outlet (green) labeled "流量计 Flow Meter"
- Arrow from sensors to "状态估计 State Estimation" box
- Annotation: "传感器反推状态 Sensors infer state → 可观 Observable"
- Background color: light green (#E8F5E9)

Center dividing line labeled: "控制双可 Dual Properties"
Bottom: "可控=能影响 Can Influence ↔ 可观=能观测 Can Observe"

White background. Clean schematic style. Chinese+English labels.
Minimum 2400×1600 px. 300 DPI.
```

---

### 图 12-1: 枕头坝—沙坪水力电力耦合示意图

**文件名**: `fig_12_01_zhentou_shaping_coupling.png`

**上下文**: 第十二章§12.1案例一，沙坪二级水电站"一键调"核心示意——枕头坝上游水库调节 + 沙坪下游发电消纳的耦合关系。

**Gemini 提示词**:
```
A side-view engineering diagram showing the hydraulic-electric coupling between two cascade hydropower stations, designed for an academic textbook.

From left to right:
1. **枕头坝 (Zhentou Dam)** - upstream regulating reservoir:
   - Dam structure (concrete gravity dam)
   - Reservoir water level labeled "调节库容 Regulating Storage"
   - Spillway labeled "泄洪闸 Spillway"
   
2. **连接渠道 (Connecting Channel)**:
   - Canal connecting the two stations (5.5 km)
   - Flow arrow labeled "流量 Q"
   
3. **沙坪 (Shaping Station)** - downstream power generation:
   - Powerhouse with turbine icon
   - Generator labeled "发电机组 Generator Units"
   - Power output arrow labeled "电力输出 Power Output"

Overlaid system annotations:
- Red dashed box around Zhentou: "水力控制 Hydraulic Control"
- Green dashed box around Shaping: "电力优化 Power Optimization"
- Blue bidirectional arrow connecting them: "耦合约束 Coupling Constraints"

Bottom legend:
- 上游调节 Upstream Regulation (water level, spillage)
- 下游消纳 Downstream Consumption (power generation)
- 耦合目标 Coupling Goal: 水力-电力协同 Hydro-Electric Synergy

White background. Engineering schematic style. Chinese+English labels.
Minimum 2400×1600 px. 300 DPI.
```

---

### 图 13-1: 瀑深枕梯级水力电力耦合拓扑

**文件名**: `fig_13_01_pfsz_cascade_topology.png`

**上下文**: 第十三章§13.1案例二，瀑深枕（瀑布沟-深溪沟-枕头坝）三级梯级联合调度的拓扑结构和耦合关系。

**Gemini 提示词**:
```
A top-down schematic topology diagram showing three cascade hydropower stations along a river, designed for an academic textbook.

From top to bottom along a stylized river (blue wavy line):

1. **瀑布沟 (Pubugou)** - uppermost station:
   - Large reservoir icon (blue)
   - Dam structure
   - Label: "调节库容 180亿m³ Regulating Storage 18B m³"
   - Label: "装机 3300MW Installed Capacity"

2. **深溪沟 (Shenxigou)** - middle station (30 km downstream):
   - Medium reservoir icon
   - Dam structure
   - Label: "日调节 Daily Regulation"
   - Label: "装机 660MW"

3. **枕头坝 (Zhentouба)** - lower station (20 km downstream):
   - Small reservoir icon
   - Dam structure
   - Label: "小时调节 Hourly Regulation"
   - Label: "装机 48MW"

Connecting elements:
- Blue arrows labeled "流量传递 Flow Cascade"
- Red dashed lines labeled "水力耦合 Hydraulic Coupling"
- Green dashed lines labeled "电力协同 Power Coordination"

Right side annotation box:
"三级耦合特征 Three-level Coupling:
- 时间尺度 Time Scales: 周/日/时 Weekly/Daily/Hourly
- 容量递减 Capacity Cascade: 180亿→日调→时调
- 协同目标 Synergy Goal: 梯级联合出力 Joint Power Output"

White background. Topological schematic style. Chinese+English labels.
Minimum 2400×1600 px. 300 DPI.
```

---

## ✅ 生成检查清单

生成每幅图后，请检查：
- [ ] 分辨率 ≥ 2400×1600 px（或 2400×1200 for 横版）
- [ ] 中英文双语标注清晰可读
- [ ] 配色符合规范（深蓝 #1565C0 / 绿 #4CAF50 / 紫 #7B1FA2）
- [ ] 无多余装饰元素（学术风格）
- [ ] 文件命名符合规范（`fig_XX_YY_description.png`）

---

## 📦 输出目录

生成的图片保存到：
```
/home/admin/.openclaw/workspace/books/books/T1-CN/figure-prompts/generated/
```

已生成的图片列表见：`generated/` 目录
