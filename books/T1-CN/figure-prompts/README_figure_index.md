# T1-CN 全书插图总表 — 分类生成方案

> 更新日期：2026-02-24
> 依据 SKILL.md 技巧14/18 规范：
> - **概念图/架构图** → Gemini AI 生成 + PPT精修
> - **数据曲线/矩阵/时序图** → matplotlib/plotly 代码生成
> - **流程图/状态机/DAG** → Mermaid 代码生成 或 matplotlib
> 
> 统一配色：#1565C0(深蓝/水力) #4CAF50(绿/安全) #7B1FA2(紫/认知) #FF7043(橙红/扰动)
> 标注：中英双语（中文在前，英文在后）
> 尺寸：最小 1800×1200px，复杂图 2400×1600px

---

## 生成方式分类汇总

### 🎨 Gemini AI 生成（13幅）— 概念图/比喻图/视觉丰富的示意图

| 编号 | 标题 | 类型 | 提示词文件 |
|---|---|---|---|
| 图1-1 | 五代演进图 | 时间轴信息图 | ch01_figures.md |
| 图1-2 | 自动化与自主运行对比 | 左右对比概念图 | ch01_figures.md |
| 图1-3 | WNAL与SAE对比 | 阶梯对比概念图 | ch01_figures.md |
| 图1-5 | 本书结构导读图 | 结构导读概念图 | ch01_figures.md |
| 图5-1 | 可控性与可观性直觉解释 | 直觉概念图 | ch03-06_figures.md |
| 图5-2 | 传感器优化布局概念图 | 网络拓扑概念图 | ch03-06_figures.md |
| 图6-2 | CHS四层分布式控制架构 | 架构图 | ch03-06_figures.md |
| 图9-1 | CPSS三层认知框架 | 嵌套概念图 | ch07-11_figures.md |
| 图10-1 | HydroOS三层架构 | 架构图 | ch07-11_figures.md |
| 图10-4 | SCADA+MAS+HydroOS融合 | 融合架构图 | ch07-11_figures.md |
| 图10-5 | HydroOS分级部署路径 | 路线图 | ch07-11_figures.md |
| 图12-1 | 枕头坝—沙坪水力电力耦合 | 工程示意图 | ch12-13_figures.md |
| 图13-1 | 瀑深枕梯级拓扑 | 工程拓扑图 | ch12-13_figures.md |

### 🐍 matplotlib 代码生成（11幅）— 矩阵/时序/数据/层次图

| 编号 | 标题 | 图表类型 | 代码文件 |
|---|---|---|---|
| 图1-4 | CHS八原理层次关系 | 层次结构+回边 | code_figures.py |
| 图2-2 | 可控模型族三层体系 | 金字塔图 | code_figures.py |
| 图2-3 | 多时间尺度分层控制链 | 四层带状图 | code_figures.py |
| 图3-1 | CHS八原理依赖导图 | 五层DAG | code_figures.py |
| 图6-3 | 安全包络红黄绿三区 | 时序曲线+色带 | code_figures.py |
| 图6-4 | 在环验证×WNAL矩阵 | 热力矩阵 | code_figures.py |
| 图6-5 | 自主演进三重闭环 | 嵌套环形图 | code_figures.py |
| 图7-1 | WNAL L0-L5阶梯图 | 阶梯条形图 | code_figures.py |
| 图7-3 | 八原理×WNAL映射 | 热力矩阵 | code_figures.py |
| 图11-1 | PAI-CAI协作工作流 | 双泳道时序图 | code_figures.py |
| 图12-2 | 沙坪ODD六维+三区 | 雷达图+色带 | code_figures.py |

### 📐 Mermaid 代码生成（8幅）— 流程图/状态机

| 编号 | 标题 | 图表类型 | 代码文件 |
|---|---|---|---|
| 图1-6 | 章节依赖关系 | 有向无环图 | mermaid_figures.md |
| 图2-1 | 水系统控制框图 | 控制框图 | mermaid_figures.md |
| 图2-4 | 异常工况四态机 | 状态机 | mermaid_figures.md |
| 图3-2 | MBD四层一闭环 | 层次+闭环 | mermaid_figures.md |
| 图7-2 | WNAL四重门槛 | 结构化流程 | mermaid_figures.md |
| 图9-2 | MBD四层一闭环(详) | 层次+闭环 | mermaid_figures.md |
| 图10-2 | 策略门禁四项检查 | 串行流程 | mermaid_figures.md |
| 图10-3 | HydroOS四态机 | 状态机 | mermaid_figures.md |
| 图12-3 | MPC滚动优化流程 | 循环流程 | mermaid_figures.md |
| 图13-2 | 梯级EDC两级架构 | 架构+流程 | mermaid_figures.md |

### ♻️ 复用（4幅）

| 编号 | 复用来源 | 说明 |
|---|---|---|
| 图4-1 | = 图2-2 | 仅改标题 |
| 图6-1 | = 图3-1 | 仅改标题 |
| 图8-1 | ≈ 图6-3 | 微调阈值标注 |
| 图8-2 | = 图6-4 | 仅改标题 |

---

## 去重后实际工作量

| 方式 | 数量 | 状态 |
|---|---|---|
| Gemini AI 提示词 | 13 | ✅ 已完成（figure-prompts/*.md） |
| matplotlib 代码 | 11 | 🔧 code_figures.py |
| Mermaid 代码 | 10 | 🔧 mermaid_figures.md |
| 复用 | 4 | ✅ 无需生成 |
| **合计独立图** | **28** | — |
