# 第二章 插图（4幅）

> 生成方式分配：
> - 🐍 matplotlib: 图2-2, 图2-3 → 见 `code_figures.py`
> - 📐 Mermaid: 图2-1, 图2-4 → 见 `mermaid_figures.md`
> 
> ⚠️ 本章无 Gemini 生成图——全部为结构化图表/框图/状态机，适合代码生成。

---

## 📐 图 2-1: 水系统状态—输入—输出—扰动框图

> **→ Mermaid 代码生成**: 见 `mermaid_figures.md :: 图2-1`
> 控制论经典框图，含反馈回路，Mermaid graph LR 最合适。

---

## 🐍 图 2-2: 可控模型族的三层体系（PBM→SM→OSEM金字塔）

> **→ matplotlib 代码生成**: 见 `code_figures.py :: fig_02_02()`
> **已生成**: `generated/fig_02_02_model_family.png`
> 三层梯形金字塔+双向箭头，需要精确控制几何形状。
> ⚠️ 图4-1复用本图。

---

## 🐍 图 2-3: 多时间尺度分层控制链

> **→ matplotlib 代码生成**: 见 `code_figures.py :: fig_02_03()`（待补充）
> 四层横向带状图，从秒级→日级→月级→年级，需精确对齐。

**视觉规格**:
四层水平带，从上到下：
- 第一层（浅蓝 #E3F2FD）：年/季度 — 水资源规划层 "Water Resources Planning"
- 第二层（蓝 #90CAF9）：月/旬 — 调度决策层 "Dispatch Decision"  
- 第三层（深蓝 #42A5F5）：日/时 — 实时优化层 "Real-time Optimization"
- 第四层（最深蓝 #1565C0）：分/秒 — 闭环控制层 "Closed-loop Control"

左侧纵轴：时间尺度 ↓（年→秒）
右侧纵轴：空间尺度 ↓（流域→设备）
层间有双向箭头：上层下发目标，下层反馈状态。

---

## 📐 图 2-4: 异常工况四态机状态迁移图

> **→ Mermaid 代码生成**: 见 `mermaid_figures.md :: 图2-4`
> 经典状态机，四态+迁移条件标注，stateDiagram-v2 最合适。
