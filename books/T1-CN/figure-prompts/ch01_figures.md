# 第一章 插图（6幅）

> 生成方式分配：
> - 🎨 Gemini: 图1-1, 图1-2, 图1-3, 图1-5（概念图/信息图）
> - 🐍 matplotlib: 图1-4 → 见 `code_figures.py :: fig_01_04()`
> - 📐 Mermaid: 图1-6 → 见 `mermaid_figures.md :: 图1-6`

---

## 🎨 图 1-1: 水利工程运行管理系统五代演进图

**文件名**: fig_01_01_five_generations.png

**论文上下文**: 第一章§1.2，概述水利工程运行管理从1950s人工到2020s自主运行的五代演进历程，是全书的时代背景铺垫。

**提示词**:
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

---

## 🎨 图 1-2: 自动化与自主运行对比示意图

**文件名**: fig_01_02_auto_vs_autonomous.png

**论文上下文**: §1.3，核心概念辨析——"自动化"(Automation)按预设规则执行 vs "自主运行"(Autonomous Operation)具备感知-决策-执行-学习闭环能力。

**提示词**:
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

---

## 🎨 图 1-3: WNAL L0-L5 与 SAE 自动驾驶等级对比图

**文件名**: fig_01_03_wnal_sae_comparison.png

**论文上下文**: §1.4，将水网自主等级WNAL类比自动驾驶SAE分级，帮助读者建立直觉理解。

**提示词**:
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
Minimum 2400×1600 px.

---

## 🐍 图 1-4: CHS 八原理层次关系图

> **→ matplotlib 代码生成**: 见 `code_figures.py :: fig_01_04()`
> **已生成**: `generated/fig_01_04_eight_principles_hierarchy.png`

---

## 🎨 图 1-5: 本书结构导读图

**文件名**: fig_01_05_book_structure.png

**论文上下文**: §1.6，向读者展示全书五部分14章的组织逻辑，便于按需阅读。

**提示词**:
A book structure overview diagram for an academic textbook preface, showing five parts with chapters organized in a top-down flow.

Part I "导论 Introduction" (gray #BDBDBD): Chapter 1 绪论
Part II "理论基础 Theoretical Foundation" (blue #1565C0): Chapters 2-5, horizontal row
Part III "八原理与验证 Principles & Verification" (deep blue #0D47A1): Chapters 6-8, horizontal row
Part IV "系统架构 System Architecture" (purple #7B1FA2): Chapters 9-11, horizontal row
Part V "工程实践 Engineering Practice" (green #4CAF50): Chapters 12-14, horizontal row labeled "点Point → 链Chain → 网Network"

Parts connected by vertical arrows showing reading flow.
Side annotations: "理论读者建议路径" and "工程读者建议路径" with different colored arrows.

White background. Clean academic style. Chinese+English labels.
Minimum 2400×1600 px.

---

## 📐 图 1-6: 章节依赖关系图

> **→ Mermaid 代码生成**: 见 `mermaid_figures.md :: 图1-6`
