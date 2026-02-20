# T1-CN《水系统控制论》图片生成提示词

> **使用说明**: 本文件为全书图片的生成提示词，供 Google 图片生成工具使用。
> **风格统一要求**: 学术教材风格，蓝色系主色调，白色背景，清晰中文标注，矢量感/扁平化设计，无过度装饰。
> **输出格式**: PNG，分辨率≥300dpi，宽度≥2000px

---

## 第一章 绪论

### 图1-1: CHS八原理层次关系图
**文件名**: fig_1_1_chs_eight_principles_pyramid.png

**提示词**:
A clean academic diagram showing a four-layer pyramid structure, viewed from the front. White background, blue color scheme. Bottom layer (foundation, dark blue): "Principle 1: Transfer Function" and "Principle 2: Controllability & Observability". Second layer (architecture, medium blue): "Principle 3: Hierarchical Distributed" and "Principle 4: Safety Envelope". Third layer (intelligence, light blue): "Principle 5: In-the-Loop Verification", "Principle 6: Cognitive Enhancement", "Principle 7: Human-Machine Collaboration". Top layer (evolution, accent blue): "Principle 8: Autonomous Evolution". Upward arrows between layers showing support relationships. Each layer labeled in both Chinese and English. Professional textbook illustration style, flat design, no 3D effects. Chinese labels: 基础层, 架构层, 智能层, 演进层.

---

### 图1-2: 水利工程运行管理系统五代演进图
**文件名**: fig_1_2_five_generations_evolution.png

**提示词**:
A horizontal timeline infographic showing five generations of water engineering operation management systems. White background, blue gradient color scheme. Left to right: Generation 1 (1960s, gray-blue): icon of manual gauge + "人工观测与经验调度"; Generation 2 (1970-1990s, light blue): icon of computer screen + "SCADA遥测遥控"; Generation 3 (1990-2010s, medium blue): icon of mathematical model + "模型驱动控制HDC"; Generation 4 (2010-2020s, blue): icon of AI brain + "数据驱动智慧水利"; Generation 5 (2020s+, deep blue): icon of autonomous system + "自主运行 CHS+HydroOS". A rising arrow across all five stages indicating capability accumulation ("能力逐层叠加"). Each generation box contains a small representative icon and 2-3 keyword labels. Note: this is a general industry evolution summary, not attributed to any single author. Clean flat design, academic textbook style. Timeline arrow at bottom.

---

### 图1-3: 自动化与自主运行对比示意图
**文件名**: fig_1_3_automation_vs_autonomy.png

**提示词**:
A side-by-side comparison diagram with two panels. White background, blue color scheme. Left panel labeled "自动化 Automation": shows a simple linear flow "预设规则 → 执行 → 固定响应", with a human figure at the top making all decisions, arrows pointing down to machines. Right panel labeled "自主运行 Autonomous Operation": shows a closed loop "感知 → 理解 → 决策 → 执行 → 学习", with a human figure at the side in supervisory role, the loop is self-contained. Key differences highlighted with icons: decision-making (human vs machine), adaptability (fixed vs learning), safety (interlock vs safety envelope). Clean academic diagram style, flat design, Chinese and English bilingual labels.

---

### 图1-4: WNAL L0-L5与SAE自动驾驶等级对比图
**文件名**: fig_1_4_wnal_vs_sae_comparison.png

**提示词**:
A dual-column comparison chart showing WNAL L0-L5 water network autonomy levels alongside SAE L0-L5 driving automation levels. White background. Left column (blue): WNAL levels from L0 "人工运行" to L5 "完全自主", each with a water/dam icon. Right column (gray): SAE levels from L0 "No Automation" to L5 "Full Automation", each with a car icon. Horizontal lines connecting corresponding levels. Key differences highlighted in the middle: "公共安全 vs 个体安全", "连续服务 vs 行程结束", "治理责任 vs 产品责任". Arrow on left showing increasing water system autonomy. Clean infographic style, academic textbook quality, flat design.

---

### 图1-5: 本书结构导读图
**文件名**: fig_1_5_book_structure_roadmap.png

**提示词**:
A book structure roadmap diagram showing 8 chapters in a logical flow. White background, blue color scheme. Layout: Chapter 1-2 at left labeled "为什么 Why" (problem and theory basis); Chapter 3-4 in center-left labeled "是什么 What" (principles and classification); Chapter 5 in center labeled "怎么做 How" (technology architecture); Chapter 6 in center-right labeled "做了什么 Practice" (engineering cases); Chapter 7-8 at right labeled "走向哪里 Future" (outlook). Chapters connected by directional arrows showing reading flow. Each chapter box contains its number and short title in Chinese. Clean flowchart style, rounded rectangles, academic textbook illustration.

---

## 第二章 控制论视角下的水系统

### 图2-1: 水系统状态-输入-输出-扰动框图
**文件名**: fig_2_1_system_block_diagram.png

**提示词**:
A control system block diagram for water systems. White background, blue color scheme. Central large rounded rectangle labeled "水利系统 f(·)" with state x_k shown inside. Four input arrows: (1) from left, u_k labeled "控制输入：闸门开度/泵站频率" in blue; (2) from top, d_k labeled "外部扰动：降雨/取水变化" in orange; (3) from bottom-left as dashed arrow, θ_k labeled "慢变参数：糙率/设备效率" in gray. One output arrow to the right: y_k labeled "可测输出：水位/流量观测", with a small circle at output adding v_k "测量噪声". A feedback loop from output goes down and left to a second rounded rectangle labeled "控制器 Controller", then back to the input u_k. Standard control engineering block diagram notation. Clean flat academic style, no decorative elements. All labels in Chinese with mathematical symbols.

---

### 图2-2: 可控模型族的三层体系
**文件名**: fig_2_2_model_hierarchy_pyramid.png

**提示词**:
A pyramid diagram showing three tiers of water system models. White background, blue gradient scheme. Viewed from front, three horizontal layers stacked vertically. Bottom layer (largest, dark blue): "高保真PDE模型 High-Fidelity PDE" with annotation "离线仿真 / 数字孪生, 维度 ~10³". Middle layer (medium, blue): "降阶传递函数模型 Reduced-Order TF (IDZ)" with annotation "在线MPC控制, 维度 ~10¹". Top layer (smallest, light blue): "数据增强模型 Data-Enhanced" with annotation "参数校正 / 软测量". Left side: downward arrow labeled "降阶方法 Model Reduction" connecting bottom to middle. Right side: downward arrow labeled "数据同化 Data Assimilation" connecting top to middle. Far left vertical annotation: "物理保真度↑" pointing down. Far right vertical annotation: "在线计算效率↑" pointing up. Clean pyramid/tiered diagram, academic textbook style, flat design, Chinese and English bilingual labels.

---

### 图2-3: 多时间尺度分层控制链
**文件名**: fig_2_3_multi_timescale_control_hierarchy.png

**提示词**:
A four-layer horizontal band diagram showing multi-timescale hierarchical control for water systems. White background, blue gradient from light (top) to dark (bottom). Four horizontal bands stacked vertically: Top band (lightest blue) "规划层 Planning" — "日/周级" — right side: "优化调度 / 随机规划"; Second band (light blue) "协调层 Coordination" — "小时级" — right side: "集中/分布式MPC"; Third band (medium blue) "调节层 Regulation" — "分钟级" — right side: "PI/PID + 前馈"; Bottom band (dark blue) "执行层 Execution" — "秒级" — right side: "PID + 联锁保护". Between each pair of bands: upward arrow labeled "状态报告↑" and downward arrow labeled "目标约束↓". Left side: vertical time axis from "秒 Seconds" at bottom to "周 Weeks" at top. Far right column shows a concrete engineering mapping example: "PLC" (execution), "管理处控制系统" (regulation), "调度中心MPC" (coordination), "水资源调度系统" (planning). Clean layered diagram, academic textbook quality, Chinese labels.

---

### 图2-4: 异常工况四态机状态迁移图
**文件名**: fig_2_4_four_state_machine.png

**提示词**:
A state machine diagram with four states and bidirectional transitions. White background. Four large rounded rectangles arranged in a horizontal row (or slight arc): leftmost "正常态 Normal" (green fill), second "受限态 Restricted" (yellow fill), third "降级态 Degraded" (orange fill), rightmost "接管态 Takeover" (red fill). Forward transition arrows (solid, above): Normal→Restricted labeled "预测可信度下降 / 通信质量变差"; Restricted→Degraded labeled "关键状态逼近黄区 / 多传感器离线"; Degraded→Takeover labeled "红区触及 / 执行器故障 / 人工主动接管". Recovery arrows (dashed, below): Takeover→Degraded→Restricted→Normal, each labeled with recovery conditions. Inside each state box, two lines: top line = control strategy (性能优化 / 保守策略 / 固定流量带 / 人工控制); bottom line = human-machine role (自动 / 监督 / 请求接管 / 人工主导). Clean state diagram, colored states, academic textbook quality, Chinese labels with clear legibility.

---

## 第三章 水系统控制论八原理

### 图3-1: CHS八原理依赖导图
**文件名**: fig_3_1_eight_principles_dependency.png

**提示词**:
A horizontal dependency flow diagram of CHS eight principles organized in five layers. White background, blue color scheme. Five groups left to right, each in a rounded-corner card: Layer 1 "建模基础层" (dark blue) contains P1 "传递函数化" and P2 "可控可观性", side by side. Layer 2 "架构组织层" (blue) contains P3 "分层分布式" and P4 "安全包络", side by side. Layer 3 "验证保障层" (medium blue) contains P5 "在环验证" alone. Layer 4 "协同智能层" (light blue) contains P6 "认知增强" and P7 "人机共融", side by side. Layer 5 "演进能力层" (lightest blue) contains P8 "自主演进" alone. Thick forward arrows connect each layer to the next. A curved red feedback arrow from P4 (Safety Envelope) arcs back to P8 (Autonomous Evolution), labeled "安全约束回边 Safety Constraint Feedback". Each principle box has its number circled. Clean dependency graph, flat design, academic textbook style, Chinese and English labels.

---

### 图3-2: CHS四层分布式控制架构图（配合§3.4）
**文件名**: fig_3_2_four_layer_distributed_architecture.png

**提示词**:
A vertical hierarchy diagram showing the CHS four-layer distributed control architecture. White background, blue gradient color scheme. Four layers stacked bottom to top: Bottom layer (darkest blue) "执行层 L0 Execution" with small icons for individual gates, pumps, valves — right-side label "秒级 | 设备闭环+安全联锁". Second layer (dark blue) "区域层 L1 Regional" with an icon for a canal section controller — label "分钟级 | 局部MPC+约束协调". Third layer (medium blue) "全局层 L2 Global" with an icon for a coordinator — label "小时级 | 跨区域分配+冲突消解". Top layer (light blue) "治理层 L3 Governance" with an icon for human decision-maker — label "日/政策级 | 策略审批+审计闭环". Bidirectional arrows between adjacent layers. Right-side column lists three coordination mechanisms with small connector icons: "① 目标分解与约束传递", "② 信息共享与一致性协议", "③ 冲突裁决与优先级规则". Clean hierarchical diagram, flat design, academic textbook style.

---

### 图3-3: 安全包络红黄绿三区示意图（配合§3.5）
**文件名**: fig_3_3_safety_envelope_zones.png

**提示词**:
A technical diagram illustrating the safety envelope three-zone concept for water level control. White background. Left portion: a vertical axis labeled "水位 h (m)" with a realistic-looking time-series curve plotted against time axis "t (h)". Three horizontal bands around a target water level line: Green zone (center, light green tint) labeled "绿区 Green: 性能优先" with note "优化算法自由度最大"; Yellow zone (above and below green, light yellow tint) labeled "黄区 Yellow: 保守策略" with note "收缩控制域, 降低目标"; Red zone (outermost, light red tint) labeled "红区 Red: 强制保护" with note "确定性指令, 不经优化". The curve oscillates mostly in the green zone, briefly dips into yellow zone once, showing the system self-correcting back to green. Right portion: a small flowchart showing zone transition logic — "进入黄区 → 切换保守策略 → 恢复绿区" and "进入红区 → 触发联锁保护 → 通知调度员". Red and yellow threshold lines clearly marked with values like "h_max", "h_warn_upper". Clean technical diagram, academic textbook style.

---

### 图3-4: 在环验证深度与WNAL等级对应图（配合§3.6）
**文件名**: fig_3_4_verification_wnal_matrix.png

**提示词**:
A matrix diagram mapping verification stages to WNAL autonomy levels. White background, blue scheme. Horizontal axis (6 columns): WNAL levels L0 through L5, with column width increasing slightly left to right. Vertical axis (3 rows): MIL (模型在环), SIL (软件在环), HIL (硬件在环). Cell fills: L0-L1 columns all light gray with dash mark "—"; L2 column has light blue MIL cell "基本工况", light blue SIL cell "推荐", gray HIL "—"; L3 column all solid blue "必须" with notes "全工况+异常" for MIL, "必须" for SIL, "关键回路" for HIL; L4 column deep blue with "极端+对抗" for MIL, "必须" for SIL/HIL with "全部回路"; L5 column deepest blue with "生成式测试" for MIL, "形式化验证" for SIL, "长期耐久" for HIL. A bold dashed red vertical line between L2 and L3 columns labeled "关键门槛". Clean matrix/heatmap style, academic textbook quality.

---

### 图3-5: 人机关系三种模式与WNAL等级对应图（配合§3.8）
**文件名**: fig_3_5_human_machine_modes.png

**提示词**:
A three-panel comparison diagram showing three human-machine collaboration modes. White background, blue scheme. Panel 1 (left, labeled "HitL 人在回路中 | L0-L1"): a human stick figure centered inside a circular control loop, making all decisions, machine icons (gate, pump) as passive tools below. Panel 2 (center, labeled "HotL 人在回路上 | L2-L3"): a machine/computer icon centered in the control loop executing decisions autonomously, human figure positioned above the loop on a "监督 Supervisory" platform, with a downward "接管 Override" arrow. Panel 3 (right, labeled "HootL 人在回路外 | L4-L5"): fully autonomous machine loop running independently, human figure far above setting "策略 Policy" via a thin connection line. Below all three panels: a horizontal gradient arrow labeled "自主程度递增 →". Three badge icons at bottom: "🔍 可追踪 Traceable", "🔄 可接管 Overridable", "📋 优先级规则 Priority Rules". Clean comparison diagram, flat design, academic textbook style.

---

### 图3-6: 自主演进三重闭环示意图（配合§3.9）
**文件名**: fig_3_6_triple_loop_evolution.png

**提示词**:
A nested concentric loop diagram showing three feedback loops for autonomous water network evolution. White background, blue scheme. Three concentric rounded rectangles (not circles): Innermost (lightest blue, smallest) "数据闭环 Data Loop" with four nodes along the loop: "采集 Collect → 清洗 Clean → 标注 Label → 回灌 Feed-back". Middle loop (medium blue) "模型闭环 Model Loop" with three nodes: "离线训练 Offline Train → 灰度验证 Shadow Test → 在线监控 Online Monitor". Outermost loop (darkest blue, largest) "策略闭环 Strategy Loop" with three nodes: "版本管理 Version Ctrl → 回滚机制 Rollback → 效果评估 Evaluation". A thick constraint bracket on the right side from outside, colored red, labeled "安全包络约束 Safety Envelope Constraint" with an inward-pointing arrow, indicating the envelope constrains all three loops. Bottom row shows three principle badges: "可回滚 Rollback-able", "可解释 Explainable", "可审计 Auditable". Clean nested loop diagram, flat design, academic textbook quality.

---

## 第四章 水网自主等级

### 图4-1: WNAL L0-L5阶梯图
**文件名**: fig_4_1_wnal_staircase.png

**提示词**:
A staircase diagram showing six ascending levels of water network autonomy. White background. Six steps rising left to right: L0 (gray) "手动运行 Manual", L1 (pale blue) "规则自动化 Rule-Based", L2 (light blue) "条件自动化 Conditional Automation", L3 (blue) "条件自主 Conditional Autonomy", L4 (dark blue) "高度自主 High Autonomy", L5 (gold dashed outline) "完全自主 Full Autonomy (Theoretical)". On each step face, three keyword labels: "机器能力 Machine Capability", "人工角色 Human Role", "ODD范围 ODD Scope". A prominent red dashed line between L2 and L3 labeled "责任移交分水岭 Responsibility Transition Watershed". Inside L3 step: "四态机+安全包络". L5 step has dashed border to indicate unreachable. Left vertical axis: "自主能力↑ Autonomy". Bottom horizontal axis: "技术+治理成熟度→ Tech + Governance Maturity". Clean academic staircase diagram, flat design, Chinese and English bilingual labels.

---

### 图4-2: WNAL等级跃迁四重门槛
**文件名**: fig_4_2_level_transition_gates.png

**提示词**:
A diagram showing four mandatory gates for WNAL level transition. White background, blue scheme. Central thick arrow from "Lk" on left to "Lk+1" on right, passing through four vertical gate barriers evenly spaced. Gate 1 (blue) "技术门槛 Technical": labels inside "模型精度/控制能力/传感器覆盖/算力保障". Gate 2 (green) "验证门槛 Verification": labels "MIL通过/SIL通过/HIL通过/场景覆盖≥95%". Gate 3 (orange) "治理门槛 Governance": labels "责任矩阵/接管SOP/审计链/合规性". Gate 4 (red) "运行门槛 Operational": labels "连续达标/无安全事件/KPI持续满足". Above all four gates: "AND (全部通过)" in bold. Below the arrow: a dashed return loop from Lk+1 back to Lk labeled "任一门槛不满足→退回或降级". Clean gate/barrier diagram, academic textbook style, Chinese labels with clear legibility.

---

### 图4-3: 八原理与WNAL等级映射图
**文件名**: fig_4_3_principles_wnal_mapping.png

**提示词**:
A matrix mapping diagram showing the relationship between CHS Eight Principles (vertical axis) and WNAL levels (horizontal axis). White background. Left column lists eight principles vertically: P1 传递函数化 through P8 自主演进, grouped into layers (基础/架构/验证/智能/演进). Top row shows L0 through L5 horizontally. Colored blocks fill the intersection cells to show which principles are required for which levels: P1/P2 cover L1-L5 (light blue fill); P3/P4 cover L3-L5 (medium blue fill); P5 covers L3-L5 (green fill with label "L3准入强制"); P6/P7 cover L4-L5 (orange fill); P8 covers L4-L5 (light red fill with label "受P4约束"). A bold vertical line at L2-L3 boundary labeled "最小原理集: 1+2+3+4+5". Clean matrix heat-map style, academic textbook quality, Chinese labels.

---

## 第五章 核心技术架构：HydroOS

### 图5-1: HydroOS三层架构图
**文件名**: fig_5_1_hydroos_three_layer_architecture.png

**提示词**:
A professional layered architecture diagram for the HydroOS water network operating system. White background, blue color scheme with clear layer separation.

Three main horizontal layers stacked bottom to top, each a wide rounded rectangle with distinct color:

**Bottom layer** (darkest blue, #003366): "设备抽象层 DAL — Device Abstraction Layer". Inside the layer, five small flat icons in a row: (1) a sluice gate icon labeled "闸门 Gate", (2) a pump icon labeled "泵站 Pump", (3) a water level sensor icon labeled "水位计 Level Sensor", (4) a water quality probe icon labeled "水质站 WQ Station", (5) a generic PLC/RTU icon labeled "PLC/RTU". Below these icons, a thin sub-bar labeled "UDSM统一设备语义模型 + 协议适配器(Modbus/OPC UA/IEC 61850)". Right-side annotation: "毫秒—秒级 | 边缘保护+断连自治".

**Middle layer** (medium blue, #0055A4): "物理AI引擎 PAI — Physical AI Engine". Inside, four module boxes in a row: (1) "水力模型 Hydro Model" with a small wave equation icon, (2) "状态估计 State Estimator" with a Kalman filter icon, (3) "MPC优化器 MPC Optimizer" with a rolling horizon icon, (4) "安全包络 Safety Envelope" with a red-yellow-green zone mini icon. Right-side annotation: "秒—分钟级 | 机理驱动+约束优化".

**Top layer** (light blue, #4499CC): "认知AI引擎 CAI — Cognitive AI Engine". Inside, four module boxes: (1) "知识图谱 Knowledge Graph" with a network/node icon, (2) "因果诊断 Causal Diagnosis" with a magnifying glass icon, (3) "策略解释 Strategy Explainer" with a speech bubble icon, (4) "协同编排 Orchestrator" with a conductor baton icon. Right-side annotation: "分钟—小时级 | 语义理解+人机协同".

Between middle and top layers: a horizontal red bar spanning the full width labeled "策略门禁 + 四态机 + 审计链 | Policy Gate + State Machine + Audit Trail".

Left side: a thick upward arrow (green) labeled "数据上行 Data Upflow (感知链)".
Right side: a thick downward arrow (orange) labeled "指令下行 Command Downflow (执行链)".

Above the top layer: a horizontal bar with a human silhouette icon, labeled "调度员 / 管理层 Operator / Management".

Three small callout badges at the very bottom: "断连可活 Fail-Safe", "安全内生 Safety by Design", "可解释 Explainable".

Clean layered architecture diagram. Flat design, no 3D effects. Academic textbook quality. All text in both Chinese and English. High resolution, minimum 2400×1600px.

---

### 图5-2: 策略门禁四项检查流程图
**文件名**: fig_5_2_policy_gatekeeper_flowchart.png

**提示词**:
A vertical flowchart showing the four-stage policy gatekeeper check process in HydroOS. White background, blue and red scheme.

Top entry point: a rounded rectangle "控制策略输入 Strategy Input" with three incoming arrows labeled "PAI自动策略", "CAI协同建议", "人工手动指令".

Four sequential diamond-shaped decision nodes, connected by downward arrows, each with a PASS path (right, green arrow) continuing down and a FAIL path (left, red arrow) leading to a rejection box:

**Diamond 1** (blue): "检查一: 安全包络合规 Safety Envelope Compliance" — annotation: "PAI快速预测<1s, 轨迹不入红区". FAIL box: "拒绝 + 附原因 + 建议修正方向".

**Diamond 2** (blue): "检查二: 操作约束合规 Operational Constraint Compliance" — annotation: "闸门限速≤3%/min, 泵站冷却间隔≥15min". FAIL box: "拒绝 + 标注违反的约束".

**Diamond 3** (blue): "检查三: 权限合规 Authorization Check" — annotation: "当前WNAL等级+人机SOP判定". FAIL box: "拒绝 + 提示需要更高权限审批".

**Diamond 4** (blue): "检查四: 一致性检查 Consistency Check" — annotation: "与同期策略无物理矛盾, 安全>保障>效率". FAIL box: "拒绝 + 标注冲突策略".

All four PASS arrows converge to a green rounded rectangle at bottom: "策略放行 → DAL执行 Strategy Approved → Execute". A small audit log icon attached: "审计记录 Audit Log".

Right margin: a statistics callout box — "工程统计: 拦截率≈3.2%, 其中操作约束70%, 安全包络25%, 权限5%".

Clean flowchart, flat design, academic textbook quality. Chinese and English labels. High resolution.

---

### 图5-3: HydroOS四态机状态转换图
**文件名**: fig_5_3_four_state_machine.png

**提示词**:
A state transition diagram showing four operating modes of the HydroOS system. White background with colored state nodes.

Four large rounded rectangle state nodes arranged in a diamond/square layout:

**Top-left** (green fill, #22AA44): "正常态 Normal" — subtitle: "最优策略 | CAI全功能 | 标准日志". This is the default/initial state (marked with a small black dot entry arrow).

**Top-right** (yellow fill, #DDAA00): "降级态 Degraded" — subtitle: "保守策略 | CAI聚焦故障 | 增强日志".

**Bottom-right** (red fill, #CC2222, white text): "应急态 Emergency" — subtitle: "预定义序列 | CAI应急编排 | 全量记录".

**Bottom-left** (gray fill, #888888, white text): "检修态 Maintenance" — subtitle: "隔离+局部控制 | 维护辅助 | 检修日志".

Directed arrows between states with trigger conditions:

- Normal → Degraded: "设备故障/通信部分中断 (自动触发)"
- Degraded → Normal: "故障排除 + 状态稳定 (自动+确认)"
- Normal → Emergency: "红区触发/重大故障 (自动)"
- Degraded → Emergency: "状态恶化/红区 (自动)"
- Emergency → Normal: "全部变量回绿区 + 人工确认"
- Emergency → Degraded: "主要风险解除, 仍有次要故障"
- Normal → Maintenance: "人工显式触发"
- Maintenance → Normal: "在环验证通过 + 人工确认"

Each arrow has a small label on it with the trigger condition. Arrows use curved paths to avoid crossing.

A small legend box in the corner: "实线=自动触发, 虚线=需人工确认".

Clean state diagram, UML-style but simplified. Flat design, academic textbook quality. Chinese labels with English subtitles. High resolution.

---

### 图5-4: SCADA+MAS+HydroOS融合架构图
**文件名**: fig_5_4_scada_mas_fusion_architecture.png

**提示词**:
A three-tier overlay architecture diagram showing how HydroOS integrates with existing SCADA systems. White background, blue scheme with clear layer delineation.

Three horizontal tiers, drawn as wide rounded rectangles stacked vertically with visible overlap/connection:

**Bottom tier** (gray background, representing legacy infrastructure): "既有SCADA层 Existing SCADA Layer (保留)". Inside: a row of icons — RTU, PLC, communication network (radio tower), SCADA server, HMI screen. A prominent label: "40年工程投资 保护既有资产". A thin blue interface bar at the top edge of this tier labeled "OPC UA适配层 OPC UA Gateway" with bidirectional arrows.

**Middle tier** (medium blue background): "HydroOS智能决策层 HydroOS Intelligent Layer (新增)". Inside left half: "DAL 设备抽象" with UDSM icon + "PAI 物理AI" with MPC/model icons. Inside right half: four small agent icons arranged in a 2×2 grid — "设备智能体 Device Agent (×数百)", "区域智能体 Zone Agent (×5-15)", "协调智能体 Coordinator (×1-3)", "治理智能体 Governance (×1)". A label at the center: "MAS多智能体框架". Connection arrows between DAL/PAI and the agent grid.

**Top tier** (light blue background): "认知增强与治理层 Cognitive & Governance Layer (新增)". Inside: "CAI 认知AI引擎" icon, "策略门禁+四态机+审计链" bar, and "Web交互界面" icon showing a dashboard. A human silhouette labeled "调度员 Operator".

Key annotations on the right side:
- Arrow from bottom tier to middle: "实时数据 (3000+测点/秒)"
- Arrow from middle to bottom: "控制指令 (经门禁验证)"
- A dashed red "回退通道" arrow from middle tier back to bottom: "HydroOS故障 → 回退纯SCADA+人工模式"

Bottom callout: three advantage badges — "低侵入性 Low Intrusion", "渐进式升级 Incremental", "投资保护 Investment Protection".

Clean layered overlay diagram. Flat design, academic textbook quality. Chinese and English bilingual labels. High resolution, minimum 2400×1600px.

---

### 图5-5: HydroOS分级部署路径与WNAL等级对应图
**文件名**: fig_5_5_staged_deployment_wnal.png

**提示词**:
A horizontal staged deployment roadmap diagram aligned with WNAL autonomy levels. White background, blue gradient scheme.

Three main stages arranged left to right as ascending step blocks (staircase style), with a timeline arrow at the bottom:

**Stage 1** (lightest blue block): "阶段一 Phase 1: L1→L2" — timeline "6—12个月". Content inside: "DAL + PAI核心 + 策略门禁 + 审计日志". Below the block, key metrics in a mini table: "人工干预: 基线(100%) → 人工确认全部指令" and "主要目标: 帮人看得更清楚". A small human icon actively operating controls.

**Stage 2** (medium blue block, taller): "阶段二 Phase 2: L2→L3" — timeline "12—24个月". Content: "MPC自动控制 + 完整四态机 + CAI基础(诊断+解释)". Key metrics: "人工干预降低60-70%, 响应30-60s". A red dashed line at the boundary between Stage 1 and 2 labeled "关键跃迁: 责任移交 Critical Transition". Human icon now in supervisory position above.

**Stage 3** (darkest blue block, tallest): "阶段三 Phase 3: L3→L4" — timeline "24—36个月". Content: "CAI全功能 + MAS + 灰度发布 + 自主演进". Key metrics: "人工干预降低>90%, 响应<30s". Human icon far above, setting policy only.

Below the three stages, a horizontal bar showing cumulative investment: "SCADA投资15-25% → +20-30% → +15-25%".

Right side: a vertical bar showing corresponding WNAL levels L1 through L4, with arrows connecting each stage to its target level.

A callout at the top: "每阶段升级须通过WNAL准入评估 (第四章)" with a gate icon.

Clean staged roadmap diagram. Flat design, academic textbook style. Chinese and English labels. High resolution.

---

### 图5-6: PAI-CAI协作工作流（水位异常事件处置全过程）
**文件名**: fig_5_6_pai_cai_collaboration_workflow.png

**提示词**:
A horizontal four-phase workflow diagram showing PAI-CAI collaboration during a water level anomaly event. White background, blue scheme with phase-colored sections.

A horizontal swimlane diagram with three lanes (rows) and four phase columns:

**Three swimlanes** (top to bottom):
- Top lane (light blue): "CAI 认知AI引擎"
- Middle lane (medium blue): "PAI 物理AI引擎"
- Bottom lane (dark blue): "DAL 设备抽象层"

**Four phase columns** (left to right), each with a colored header band:

**Phase 1** (green header): "感知与检测 Detect | 14:00-14:02". In DAL lane: "数据质控: 多源交叉验证 → 确认非传感器故障". In PAI lane: "状态估计: 水位4.25m, 上升0.5cm/min → 预测25min后入黄区". Arrow from PAI upward to CAI: "趋势预警信号".

**Phase 2** (yellow header): "诊断与解释 Diagnose | 14:02-14:03". In CAI lane (main activity): three sequential action boxes — "(1) 知识图谱查询: 上游闸门13:55调整30%→45%" → "(2) 水力模型验证: 流量+18%, 传播7min, 时间吻合" → "(3) 下游检查: B泵站2号机停机, 出流-12%". Output: "根因报告: 上游增流+下游减排, 置信度92%". Arrow from CAI downward to PAI: "诊断结果+边界条件更新".

**Phase 3** (orange header): "策略生成 Optimize | 14:03-14:04". In PAI lane: "MPC重新求解 → 方案: ①2号闸32% ②启B泵3号 ③4号闸28%". Below PAI, a red gate icon: "策略门禁四项检查 → 全部通过 ✓". Arrow down to DAL: "验证后指令".

**Phase 4** (blue header): "执行与反馈 Execute | 14:04-14:30". In DAL lane: "指令翻译 → PLC下发 → 执行确认". In PAI lane: "持续监控: 14:15峰值4.38m → 14:30回落至4.20m ✓". In CAI lane: "生成事件总结报告 → 推送调度员 → 建议联动预警规则". A small audit log icon spanning all lanes at the right edge: "审计日志完整记录".

A timeline bar at the very bottom: markers at 14:00, 14:02, 14:03, 14:04, 14:15, 14:30. Total handling: "全流程约30分钟 (人工模式需60-90分钟)".

Clean swimlane workflow diagram. Flat design, academic textbook quality. Chinese labels with English phase names. High resolution, minimum 2800×1600px.

---

## 第六章 关键工程实践

### 图6-1: 工程实践闭环模板图
**文件名**: fig_6_1_practice_loop_template.png

**提示词**:
A circular/closed-loop diagram showing the engineering practice template. White background, blue scheme. Six stages in a circle: "场景目标 Scenario Goals" → "ODD定义 ODD Definition" → "控制策略 Control Strategy" → "在环验证 In-Loop Verification" → "上线运行 Go-Live Operation" → "复盘改进 Review & Improve" → back to "场景目标". Center of circle: "CHS工程实践闭环". Two callout boxes pointing to interfaces: one to "Ch4 WNAL分级" and another to "Ch5 HydroOS架构". Clean circular flow diagram, academic textbook quality, Chinese labels.

---

### 图6-2: 胶东调水工程示意图
**文件名**: fig_6_2_jiaodong_water_transfer.png

**提示词**:
A simplified schematic map of the Jiaodong Water Transfer Project in Shandong Province, China. White background with light gray landmass outline. A long canal line (blue) running from west to east across the Shandong Peninsula, with key nodes marked: source intake (Yellow River), cascaded pumping stations (triangle icons, emphasizing the cascade pump-canal topology), control gates (rectangle icons), branch offtakes, and terminal reservoir. Key locations labeled in Chinese: 引黄济青, 胶东调水干线, 主要泵站与控制节点. MPC (Model Predictive Control) signals shown as dashed feedback loops at pumping stations. Total length annotation "~500km". Clean engineering schematic style, not a realistic map but a simplified topology diagram showing the cascade pump-open canal system structure, academic textbook quality.

---

### 图6-3: 沙坪水电站梯级调度示意图
**文件名**: fig_6_3_shaping_cascade_control.png

**提示词**:
A simplified cascade hydropower station diagram showing the Pubu-Shenxigou-Zhentou-Shaping cascade system. White background, blue scheme. Four stations arranged along a river (top to bottom or left to right): "蒲布 Pubu" → "深溪沟 Shenxigou" → "镇头 Zhentou" → "沙坪 Shaping". Each station has a dam icon with turbine and spillway symbols. Arrows showing water flow direction. Control signals shown as dashed lines connecting all stations to a central "一键调 One-Click Dispatch" control hub. Three constraint labels: "发电 Generation", "泄洪 Flood Discharge", "生态 Ecology" shown as competing objectives. Clean engineering schematic, academic textbook quality.

---

## 第七章 学科前景与人才培养

### 图7-1: CHS人才与学科建设十年路线图
**文件名**: fig_7_1_ten_year_roadmap_talent.png

**提示词**:
A timeline roadmap diagram for CHS talent and discipline development from 2026 to 2035. White background, blue gradient. Three phases along a horizontal timeline: Phase I (2026-2028, light blue) "先导与试点 Pilot", Phase II (2029-2031, medium blue) "规模化与认证 Scale & Certification", Phase III (2032-2035, dark blue) "生态化与国际协同 Ecosystem & Global Collaboration". Four horizontal swim lanes below the timeline: "课程 Curriculum", "平台 Platform", "标准化 Standards", "产业协同 Industry". Milestone markers in each lane at each phase. Clean Gantt-chart-like timeline, academic textbook quality, Chinese labels.

---

### 图7-2: 四支柱课程体系结构图
**文件名**: fig_7_2_four_pillar_curriculum.png

**提示词**:
A structural diagram showing the four-pillar curriculum system for CHS education. White background, blue scheme. Four pillars (vertical columns) standing on a common base: Pillar A "水系统建模与控制 Modeling & Control" (courses: hydrodynamics, system identification, MPC); Pillar B "智能算法与认知增强 AI & Cognition" (courses: ML, RL, PINN, cognitive AI); Pillar C "系统工程与软件平台 System Engineering" (courses: SCADA+MAS, microservices, in-loop testing); Pillar D "运行治理与行业规范 Governance & Standards" (courses: risk management, cybersecurity, regulation). A roof/beam across all four pillars labeled "CHS复合型人才 CHS Compound Talent". Base labeled "工程实践平台 Engineering Practice Platform". Clean architectural pillar diagram, academic style.

---

## 第八章 结语与展望

### 图8-1: 从SCADA到自主运行生态的十年路线图
**文件名**: fig_8_1_ten_year_roadmap_industry.png

**提示词**:
A comprehensive roadmap diagram showing the water industry evolution from SCADA to autonomous operation ecosystem, 2026-2035. White background, blue gradient. Three phases: Phase I (2026-2028) "标准化与试点 Standardization & Pilot" - milestones: unified terminology, WNAL classification standard, demonstration projects. Phase II (2029-2031) "规模化与认证 Scale-up & Certification" - milestones: cross-basin deployment, industry certification, replicable templates. Phase III (2032-2035) "生态化与国际协同 Ecosystem & Global" - milestones: platform interoperability, standard mutual recognition, talent mobility. Three parallel tracks at bottom: "技术 Technology", "组织 Organization", "治理 Governance", each with specific milestones per phase. Full-page width diagram, clean academic infographic style, Chinese labels.

---

### 图8-2: CHS核心概念关系总图
**文件名**: fig_8_2_chs_concept_map.png

**提示词**:
A concept map showing the relationships between all core CHS concepts as a summary for the entire book. White background, blue scheme. Central node: "CHS 水系统控制论". Connected major nodes: "八原理 8 Principles" (with 8 sub-nodes), "WNAL L0-L5" (with level progression), "HydroOS" (with three layers), "SCADA+MAS" (fusion architecture), "ODD" (operational design domain), "Safety Envelope" (三区). Relationship arrows labeled with connections: "理论框架 provides theory", "实现载体 implemented by", "分级评价 evaluated by", "安全保障 ensured by". Clean mind-map/concept-map style, academic textbook quality, not too crowded, clear hierarchy.

---

## 统计

| 章 | 图数 | 图号列表 |
|----|------|----------|
| Ch1 | 5 | 1-1, 1-2, 1-3, 1-4, 1-5 |
| Ch2 | 4 | 2-1, 2-2, 2-3, 2-4 |
| Ch3 | 6 | 3-1, 3-2, 3-3, 3-4, 3-5, 3-6 |
| Ch4 | 3 | 4-1, 4-2, 4-3 |
| Ch5 | 6 | 5-1, 5-2, 5-3, 5-4, 5-5, 5-6 |
| Ch6 | 3 | 6-1, 6-2, 6-3 |
| Ch7 | 2 | 7-1, 7-2 |
| Ch8 | 2 | 8-1, 8-2 |
| **合计** | **31** | |
