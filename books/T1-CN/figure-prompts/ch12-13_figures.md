# 第十二至十三章 插图（5幅，全部新增）

> 生成方式分配：
> - 🎨 Gemini: 图12-1, 图13-1（工程示意图/拓扑图）
> - 🐍 matplotlib: 图12-2 → 见 `code_figures.py`
> - 📐 Mermaid: 图12-3, 图13-2 → 见 `mermaid_figures.md`

---

## 🎨 图 12-1（新增）: 枕头坝—沙坪水力电力耦合示意图

**文件名**: fig_12_01_zhentou_shaping_coupling.png

**论文上下文**: 第十二章§12.1，展示枕头坝一级电站尾水直供沙坪二级电站的水力-电力耦合关系，是沙坪案例的工程背景图。

**提示词**:
A hydraulic-power coupling schematic diagram showing the Zhentou Dam - Shaping hydropower cascade, designed for an academic textbook.

Layout (left to right, following river flow):

LEFT — Zhentou Dam (枕头坝一级 760MW):
- Dam cross-section icon with reservoir behind it
- 3 turbine-generator units shown schematically
- Labels: 枕头坝水库 Reservoir, 水轮机 Turbine ×3, 出力 P_枕

CENTER — Connecting channel/tailrace (尾水渠):
- Short river/canal segment (~4.5km, 15min delay)
- Arrow showing flow direction
- Label: 尾水渠 Tailrace, L≈4.5km, τ≈15min

RIGHT — Shaping Dam (沙坪二级 360MW):
- Smaller dam with reservoir (较小库容 limited storage)
- 4 turbine-generator units
- Labels: 沙坪水库 Reservoir (V小), 水轮机 Turbine ×4, 出力 P_沙

ABOVE the schematic — Power grid connection:
- Both stations connected to 500kV grid via transmission lines
- AGC dispatch arrows from grid to both stations
- Label: 四川电网 Sichuan Grid, AGC指令

KEY coupling relationships highlighted with colored arrows:
- Blue arrow: 水力耦合 Hydraulic Coupling (枕头坝出库 = 沙坪入库 + 时延)
- Red arrow: 电力耦合 Power Coupling (AGC同时调度两站)
- Orange annotation: "核心难点: 枕头坝调节引起沙坪15min后水位剧烈波动"

White background. Clean engineering schematic style. Chinese+English labels. No 3D.
Minimum 2400×1200 px. 300 DPI.

---

## 🐍 图 12-2（新增）: 沙坪 ODD 六维参数与三区运行规则

> **→ matplotlib 代码生成**: 见 `code_figures.py :: fig_12_02()`
> **已生成**: `generated/fig_12_02_shaping_odd_radar.png`
> 左：六维雷达图，右：水位三区色带。

---

## 📐 图 12-3（新增）: 沙坪 MPC 滚动优化控制流程

> **→ Mermaid 代码生成**: 见 `mermaid_figures.md :: 图12-3`
> MPC循环：数据采集→状态估计→来流预测→ODD检查→优化→安全检查→执行→滚动。

---

## 🎨 图 13-1（新增）: 瀑深枕梯级水力电力耦合拓扑

**文件名**: fig_13_01_cascade_topology.png

**论文上下文**: 第十三章§13.1，展示大渡河瀑布沟—深溪沟—枕头坝三站串联的水力电力耦合拓扑，是梯级案例的工程背景图。

**提示词**:
A cascade hydropower topology diagram showing three stations in series along the Dadu River, designed for an academic textbook.

Layout (top to bottom, following river flow downstream):

STATION 1 (top) — "瀑布沟 Pubugou" (largest):
- Large dam icon with reservoir
- 6 turbine units, total capacity 3600 MW
- Labels: 瀑布沟水库 (V=53.4亿m³), 装机3600MW
- Color: deep blue #0D47A1

Connecting river segment: arrow down, "大渡河 Dadu River, L≈42km"

STATION 2 (middle) — "深溪沟 Shenxigou":
- Medium dam with limited reservoir
- 4 turbine units, 660 MW
- Labels: 深溪沟水库 (V=0.6亿m³), 装机660MW
- Color: blue #1565C0

Connecting river segment: arrow down, "L≈28km"

STATION 3 (bottom) — "枕头坝一级 Zhentou-I":
- Medium dam with limited reservoir
- 3 turbine units, 760 MW
- Labels: 枕头坝水库 (V=0.3亿m³), 装机760MW
- Color: blue #42A5F5

Further downstream (dashed): 沙坪二级 Shaping-II (360MW, 第12章对象)

RIGHT side — Grid connection:
- All three stations connect to 四川500kV电网 Sichuan Grid
- AGC指令 dispatches to all stations
- Total cascade capacity: 5020MW

LEFT side — Key coupling annotations:
- 瀑布沟调蓄能力强 (大库容) — strong regulation
- 深溪沟/枕头坝库容小 — weak regulation, sensitive to upstream
- 水力时延: 瀑→深 约3h, 深→枕 约2h

White background. Engineering topology style. Chinese+English labels.
Minimum 2400×1800 px. 300 DPI.

---

## 📐 图 13-2（新增）: 梯级 EDC 两级架构与负荷分配流程

> **→ Mermaid 代码生成**: 见 `mermaid_figures.md :: 图13-2`
> 两级架构：集控层（AGC接口+BDPSA优化+五种策略模式）→ 三个厂控层。
