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
A vertical flowchart showing the four-stage policy gatekeeper check process in HydroOS. White background, blue (#0055A4) and red (#CC2222) color scheme. Overall layout approximately 1800×2400px portrait orientation.

Top entry point: a rounded rectangle (fill #E8F0FE, border #0055A4, 2px) "控制策略输入 Strategy Input" with three incoming arrows from above, each a different color: left arrow (blue) labeled "PAI-MPC自动策略", center arrow (teal) labeled "CAI协同编排建议", right arrow (gray) labeled "人工手动指令". These three arrows merge into one downward arrow entering the first check.

Four sequential diamond-shaped decision nodes (each diamond fill #F0F6FF, border #0055A4), connected by downward green (#22AA44) arrows on the PASS path, and leftward red (#CC2222) arrows on the FAIL path leading to rejection boxes (fill #FFF0F0, border #CC2222):

**Diamond 1**: "检查一: 安全包络合规 Safety Envelope". Right-side annotation box (light yellow callout): "调用PAI快速预测模块(计算<1秒), 模拟策略执行后未来1-6小时系统状态轨迹; 任一时刻进入红区→拒绝". FAIL box: "拒绝: 附拒绝原因(哪个变量/何时越界) + 建议修正方向".

**Diamond 2**: "检查二: 操作约束合规 Operational Constraints". Annotation: "闸门调整速度≤2%-5%开度/min; 泵站启停间隔≥15-30min冷却时间; 硬限制, 不可违反". FAIL box: "拒绝: 标注具体违反的约束参数及当前值".

**Diamond 3**: "检查三: 权限合规 Authorization". Annotation: "HotL模式下常规调整可自主执行; 跨区域大幅调整需调度主任批准; 根据当前WNAL等级+人机协同SOP(原理七)判定". FAIL box: "拒绝: 提示所需审批级别+推送审批请求".

**Diamond 4**: "检查四: 一致性检查 Consistency". Annotation: "检测当前策略与正在执行策略的物理矛盾; 如'增大1号闸'与'降低下游水位'冲突; 优先级裁决规则: 安全>保障>效率". FAIL box: "拒绝: 标注冲突策略ID及矛盾点".

All four PASS arrows converge to a wide green (#22AA44) rounded rectangle at bottom: "四项检查全部通过 → 策略放行 → DAL执行 All Passed → Approved → Execute", with a checkmark icon. A small chain-link icon to the right: "写入审计链 Audit Trail".

Right margin: a bordered statistics callout box (fill #FFFFF0): "胶东调水试运行统计 | 拦截率≈3.2% | 操作约束违规 70% | 安全包络触及 25% | 权限不足 5% | 每次拦截=避免一次潜在风险".

Clean flowchart, flat design, no 3D effects. Academic textbook quality. Chinese and English bilingual labels. High resolution, minimum 2400×2800px.

---

### 图5-3: HydroOS四态机状态转换图
**文件名**: fig_5_3_four_state_machine.png

**提示词**:
A state transition diagram showing four operating modes of the HydroOS system. White background with colored state nodes. Overall layout approximately 2400×1800px landscape orientation.

Four large rounded rectangle state nodes (each approximately 400×250px) arranged in a 2×2 grid with generous spacing:

**Top-left** (green fill #22AA44, white text): "正常态 Normal" — three subtitle lines: "所有变量绿区 | 最优策略运行", "CAI全功能服务", "日志级别: 标准". This is the default/initial state (marked with a small filled black circle and arrow at the top-left corner of this node).

**Top-right** (amber fill #DDAA00, dark text): "降级态 Degraded" — subtitles: "部分设备故障或通信中断", "保守策略 + 增大安全裕度 + 禁用故障回路", "CAI聚焦故障诊断 | 日志级别: 增强".

**Bottom-right** (red fill #CC2222, white text): "应急态 Emergency" — subtitles: "关键变量进入红区 / 重大设备故障(如主泵全停)", "预定义应急响应序列", "CAI应急编排+强制通知调度员 | 全量日志记录".

**Bottom-left** (gray fill #888888, white text): "检修态 Maintenance" — subtitles: "人工显式触发进入", "被检修设备从控制回路隔离 + 局部策略调整", "恢复上线需简化在环验证(≥MIL) | 检修日志".

Directed transition arrows between states, using curved Bezier paths to avoid crossing. Each arrow has a colored shaft matching the target state and a descriptive label:

- Normal → Degraded: amber arrow, label "异常检测自动触发: 部分设备故障/通信中断, 非核心功能受损" (solid line).
- Degraded → Normal: green dashed arrow, label "故障排除 + 状态连续稳定(如30min无新异常)".
- Normal → Emergency: red thick arrow, label "红区触发(自动) / 重大设备故障(自动)" (solid line, thicker than others).
- Degraded → Emergency: red arrow, label "状态持续恶化 / 变量进入红区 (自动升级)".
- Emergency → Degraded: amber dashed arrow, label "主要风险解除, 仍有次要故障未清".
- Emergency → Normal: green dotted arrow (longer path, arcing around), label "全部变量回绿区 + 人工确认 (罕见直接跳转)".
- Normal → Maintenance: gray arrow, label "调度员显式操作'进入检修'" (solid line).
- Maintenance → Normal: green dashed arrow, label "在环验证通过(≥MIL) + 人工确认上线".

**Center of the 2×2 grid**: a small shield icon (#003366) with text "核心原则: 预定义所有模式+转换规则, 避免紧急时临场判断".

**Bottom legend bar**: "━ 实线 = 自动触发(无需人工确认) | ┅ 虚线 = 需人工确认 | 箭头颜色 = 目标状态色".

Clean state machine diagram, UML-inspired but simplified. Flat design, no 3D effects, no shadows. Academic textbook quality. Chinese labels with English subtitles. High resolution, minimum 2400×1800px.

---

### 图5-4: SCADA+MAS+HydroOS融合架构图
**文件名**: fig_5_4_scada_mas_fusion_architecture.png

**提示词**:
A three-tier overlay architecture diagram showing how HydroOS integrates with existing SCADA systems. White background, blue scheme with clear layer delineation. Overall layout approximately 2800×1800px landscape orientation.

Three horizontal tiers, drawn as wide rounded rectangles stacked vertically with visible overlap/connection:

**Bottom tier** (gray background #E8E8E8, border #999999, representing legacy infrastructure): "既有SCADA层 Existing SCADA Layer (保留 Retained)". Inside: a row of five flat icons with labels — (1) RTU icon labeled "远程终端 RTU ×50-200", (2) PLC icon labeled "可编程控制器 PLC ×30-100", (3) radio tower icon labeled "通信网络 (串口/以太网/光纤)", (4) server rack icon labeled "SCADA服务器+数据库", (5) monitor screen icon labeled "HMI操作界面". A prominent italic label at top-right corner: "40年工程投资完整保留 — 硬件/网络/数据/团队". At the top edge of this tier: a narrow orange (#FF8800) interface bar labeled "OPC UA适配层 OPC UA Gateway" with bidirectional blue arrows pointing up. Inside this bar, three small tags: "语义映射: tag平面模型→UDSM对象模型", "吞吐: 3000条/秒@1-2Mbps", "延迟: +50-200ms". This is the key integration point, visually highlighted with a glowing border.

**Middle tier** (medium blue background #D4E8FC, border #0055A4): "HydroOS核心层 HydroOS Core (新增 New)". Inside, split into two sub-blocks side by side:

Left sub-block (fill #E0EEFF): "DAL 设备抽象层" with three mini-icons: UDSM semantic model icon, protocol adapter stack (Modbus/IEC 61850), edge protection shield. Right sub-block (fill #E0EEFF): "PAI 物理AI引擎" with four mini-icons: hydro model (wave), state estimator (EKF), MPC controller (horizon graph), safety envelope (three-zone). Below both sub-blocks, a wide dashed box (fill #F0F8FF): "MAS多智能体框架 Multi-Agent System" containing four agent types in a 2×2 grid — "设备智能体 Device Agent (×数百, 请求-应答模式)", "区域智能体 Zone Agent (×5-15, 协商-合同模式)", "协调智能体 Coordinator (×1-3, 事件广播模式)", "治理智能体 Governance (×1, 规则裁决)". Connection arrows between DAL/PAI and the agent grid.

**Top tier** (light blue background #EEF6FF, border #4499CC): "认知增强与治理层 Cognitive & Governance Layer (新增 New)". Inside left: "CAI 认知AI引擎" icon cluster (knowledge graph + 瀚铎LLM + causal diagnosis). Inside center: a red (#CC3333) horizontal bar "策略门禁+四态机+审计链 Runtime Governance". Inside right: "Web增强界面 Enhanced Web UI" showing a dashboard mockup with natural-language chat panel. A human silhouette icon (#003366) to the far right labeled "调度员 Dispatcher" with two arrows: one to the top tier Web UI (labeled "增强界面 New"), one directly down to the bottom tier HMI (labeled "传统界面 Legacy").

Key flow annotations on the sides:
- Left side, upward thick blue (#0055A4) arrow from bottom to middle: "实时数据上行: 3000+测点, 1s周期".
- Right side, downward thick orange (#FF6600) arrow from middle to bottom: "控制指令下行: 经门禁四项检查验证".
- A dashed red (#CC2222) "回退通道 Fallback" arrow arcing from middle tier back to bottom tier, with label: "HydroOS任何层故障 → 立即回退纯SCADA+人工模式, 零停机切换".

Bottom callout strip: three advantage badges in rounded pills — "🔒 低侵入性: 不改SCADA核心架构", "📈 渐进式: 先试点一个区段再推广", "💰 投资保护: 新增仅软件+服务器+网关".

Clean layered overlay diagram. Flat design, no 3D effects, no shadows. Academic textbook quality. Chinese and English bilingual labels. High resolution, minimum 2800×1800px.

---

### 图5-5: HydroOS分级部署路径与WNAL等级对应图
**文件名**: fig_5_5_staged_deployment_wnal.png

**提示词**:
A horizontal staged deployment roadmap diagram aligned with WNAL autonomy levels. White background, blue gradient (#B8D4F0 → #0055A4 → #003366) scheme. Overall layout approximately 2800×1600px landscape orientation.

Three main stages arranged left to right as ascending step blocks (staircase style), with a timeline arrow at the bottom:

**Stage 1** (lightest blue #B8D4F0, border #6699CC): "阶段一 Phase 1: L1→L2" — top banner "典型周期 6—12个月". Content inside the step face, listed with checkmark icons: "✓ DAL设备注册+UDSM建模", "✓ PAI核心(降阶模型+状态估计+基础MPC)", "✓ 策略门禁(四项检查)", "✓ 审计日志(基础)". Below the block, three metric badges in rounded pills: "人工干预: 基线100%(全部需人工确认)" (gray pill), "平均响应: 10-15min(人工模式)" (gray pill), "新增投资: SCADA投资的15-25%" (blue pill). A human figure icon prominently inside the control loop, labeled "人=执行者 Human-in-the-Loop | 机=辅助决策".

**Stage 2** (medium blue #4488BB, border #0055A4, taller step): "阶段二 Phase 2: L2→L3" — top banner "典型周期 12—24个月". Content additions (with "+" prefix): "+ MPC自动控制(常规工况自主执行)", "+ 完整四态机(四状态+全部转换规则)", "+ CAI基础功能(因果诊断+策略解释)". Metric badges: "人工干预: 降低60%-70%" (green pill), "平均响应: 30-60s(半自动)" (green pill), "累计新增: +20-30%" (blue pill). A bold red (#CC2222) dashed vertical line at the left boundary of this stage, with a prominent label: "⚠ 关键跃迁: 责任移交分水岭 — 在环验证从'推荐'升为'强制' — 从此系统承担实质性自主决策权". Human figure moves to supervisory position above the loop, labeled "人=监督者 Human-on-the-Loop | 机=执行者".

**Stage 3** (darkest blue #003366, white text, tallest step): "阶段三 Phase 3: L3→L4" — top banner "典型周期 24—36个月". Content additions: "+ CAI全功能(协同编排+知识图谱完整部署)", "+ MAS智能体框架(四类Agent协同)", "+ 灰度发布机制 + 自主演进三重闭环(数据/模型/策略)". Metric badges: "人工干预: 降低>90%" (bright green pill), "平均响应: <30s(全自动)" (bright green pill), "累计新增: +15-25%" (blue pill). Human figure far above, connected by thin policy line, labeled "人=策略制定者 Human-out-of-the-Loop | 机=自主运行".

**Bottom horizontal arrow** (spanning all three stages): left label "技术+治理成熟度 →" with small milestones "模型标定完成", "SIL/HIL验证通过", "连续达标运行".

**Bottom row** below the stages: a table strip showing three night-operation metrics: "夜间控制能力: L1→L2 严重退化 | L2→L3 不退化 | L3→L4 不退化" — highlighting that autonomous operation eliminates the human fatigue bottleneck.

**Top right callout box** (fill #FFFFF0, red border): "每阶段升级须通过WNAL等级准入评估(第四章): 技术门槛+验证门槛+治理门槛+运行门槛 四重门槛全部满足" with a gate icon.

Clean staircase/timeline diagram. Flat design, no 3D effects. Academic textbook quality. Chinese and English bilingual labels. High resolution, minimum 2800×1600px.

---

### 图5-6: PAI-CAI协作工作流（水位异常事件处置全过程）
**文件名**: fig_5_6_pai_cai_collaboration_workflow.png

**提示词**:
A horizontal four-phase swimlane workflow diagram showing PAI-CAI collaboration during a water level anomaly event. White background, blue scheme with phase-colored sections. Overall layout approximately 3000×1800px landscape orientation.

**Three horizontal swimlanes** (rows), each with a left-side label column (width ~120px) and colored background:

- Top lane (light blue fill #EEF6FF, border #4499CC): "CAI 认知AI引擎" with a brain/network icon.
- Middle lane (medium blue fill #D4E8FC, border #0055A4): "PAI 物理AI引擎" with a wave/equation icon.
- Bottom lane (dark blue fill #B8D4F0, border #003366): "DAL 设备抽象层" with a device/sensor icon.

**Four phase columns** (left to right), each with a colored header band spanning all three lanes:

**Phase 1** (green header #22AA44, text white): "阶段一: 感知与检测 Sensing & Detection | 14:00—14:02 (2min)".
- DAL lane: rounded box "数据质控 Data QC" with annotation "L3多源交叉验证: 超声波传感器≈雷达传感器读数一致 → 确认水位上升为真实工况, 非传感器故障". Arrow up to PAI.
- PAI lane: rounded box "状态估计 State Estimation" with annotation "当前水位4.25m | 上升速率0.5cm/min | EKF融合后精度±2cm | 按趋势预测: 25min后进入黄区(4.38m)". Output: thick upward arrow to CAI labeled "趋势预警信号 + MPC预测轨迹".
- CAI lane: small waiting icon (clock) — CAI尚未激活.

**Phase 2** (amber header #DDAA00, text dark): "阶段二: 诊断与解释 Diagnosis & Explanation | 14:02—14:03 (1min)".
- CAI lane (primary activity, large box): three sequential steps connected by small arrows: "(1) 知识图谱查询 KG Query" annotation "发现: 上游2号闸门13:55开度调整30%→45%" → "(2) 调用PAI水力模型验证" annotation "计算: 闸门调整→流量增幅18%, 水波传播至3号渠池需7min, 与观测14:02上升起始时间吻合" → "(3) 下游状态检查" annotation "发现: B泵站2号机组14:02自动停机(轴承温度报警), 出流减少12%". Final output box (amber fill): "综合诊断: '上游增流+下游减排'双重叠加 → 根因确认, 置信度92%". Arrow down to PAI: "诊断结果 + 更新的边界条件".
- PAI lane: dashed box "模型被调用(验证)" — CAI调用PAI水力模型进行因果验证.
- DAL lane: dashed box "持续数据采集" — 背景运行.

**Phase 3** (orange header #FF8800, text white): "阶段三: 策略生成与安全检查 Strategy Generation & Safety Check | 14:03—14:04 (1min)".
- PAI lane (primary activity): rounded box "MPC重新求解 Re-optimize" with annotation "更新边界: 上游入流+18%, 下游出流-12%. 输出控制方案: ① 2号闸门开度45%→32%(限速2%/min) ② 启动B泵站3号备用机组 ③ 4号闸门20%→28%分流". Arrow down to a red (#CC2222) checkpoint barrier icon spanning PAI-DAL boundary: "策略门禁 Policy Gate" with four green checkmarks in a row: "安全包络✓ 操作约束✓ 权限✓ 一致性✓ → 放行". Arrow from gate to DAL: "验证后控制指令".
- CAI lane: small box "等待门禁结果".
- DAL lane: small box "准备接收指令".

**Phase 4** (blue header #0055A4, text white): "阶段四: 执行与反馈 Execution & Feedback | 14:04—14:30 (26min)".
- DAL lane: rounded box "指令执行 Command Execution" with annotation "指令翻译: UDSM→PLC本地协议格式 → 下发执行 → 返回执行确认ACK". Arrow up to PAI.
- PAI lane: rounded box "效果监控 Performance Monitoring" with a small embedded curve chart showing water level: peak at 14:15 (4.38m) then declining to 4.20m at 14:30. Annotation: "14:15达峰值4.38m → 持续回落 → 14:30回到4.20m进入稳态 ✓ 事件解除". Arrow up to CAI.
- CAI lane: rounded box "事件总结 Event Summary" with annotation "生成处置报告推送调度员: 时间线 + 根因分析 + 处置措施 + 效果评估 + 优化建议(设置2号闸门大幅调整时的联动预警规则)".

**Right edge** (spanning all four phases): a vertical dark strip labeled "审计链 Audit Trail" with a chain-link icon (#003366), note: "全过程完整记录: 每个阶段的输入/输出/时间戳/决策依据".

**Timeline bar** at very bottom: a horizontal axis with labeled time markers at 14:00, 14:02, 14:03, 14:04, 14:15, 14:30, connected by a gradient line from green (start) to blue (end).

**Bottom summary strip** (fill #F8F8F0, border #CCCCCC): "全流程30分钟 (传统人工模式: 10-15min仅完成诊断协调, 30-60min完成恢复) | 核心优势: 数据可信(DAL) + 控制精确(PAI) + 决策可解释(CAI)".

Clean swimlane workflow diagram. Flat design, no 3D effects, no shadows. Academic textbook quality. Chinese labels with English phase names. High resolution, minimum 3000×1800px.

---

## 第六章 关键工程实践

### 图6-1: 胶东调水三级控制架构图
**文件名**: fig_6_1_jiaodong_three_level_control.png

**提示词**:
A layered control architecture diagram for the Jiaodong Water Transfer Project. White background, portrait orientation (1800×2400px). Three horizontal layers stacked vertically with clear boundaries:

**Top layer (L2, fill #E8F0FE, border #0055A4)**: "协调优化层 Coordination Layer — MPC" — central box labeled "模型预测控制器 MPC Controller" with inputs: "全线水力模型 Hydraulic Model", "SCADA实时数据", "安全约束集 Constraint Set". Output arrows going down to L1 labeled "优化控制指令 Optimal Commands". Key parameters in annotation box: "控制周期15min | 预测时域60min | 状态50维 | 约束200-500个".

**Middle layer (L1, fill #F0F8E0, border #4CAF50)**: "局部控制层 Local Control — PID" — three parallel boxes representing canal segments, each with "PID水位控制器" and "本段闸门/泵站" icons. Dashed lines showing "独立运行能力 Independent Operation" label.

**Bottom layer (L0, fill #FFF3E0, border #FF9800)**: "现场保护层 Field Protection — PLC Hardwired" — boxes for "闸门超限锁定", "泵站低水位停机", "电气过载保护". Label: "响应＜ms | 不依赖通信".

Left side vertical arrow: "控制精度提升 ↑" (bottom to top). Right side vertical arrow: "安全可靠性 ↑" (top to bottom). Annotation: "核心设计原则: 断连可活——任何上层失效, 下层独立维持安全运行".

Clean layered architecture diagram. Flat design, no 3D. Academic textbook quality. Chinese+English labels. Minimum 1800×2400px.

---

### 图6-2: 胶东调水WNAL等级跃迁路径
**文件名**: fig_6_2_jiaodong_wnal_progression.png

**提示词**:
A timeline-based progression diagram showing the WNAL level advancement of the Jiaodong Water Transfer Project. White background, landscape orientation (2400×1400px).

Horizontal timeline from left to right spanning 2016—2025+. Four ascending staircase blocks representing WNAL levels:

**Block 1 (L0→L1, ~2016-2018, fill #E0E0E0)**: "传统运行" — "SCADA监控 + 人工调度". Milestone marker: "全线SCADA建成".

**Block 2 (MIL/SIL/HIL, 2018-2020, fill #FFF9C4)**: "MPC研发与验证" — three verification icons stacked: MIL ✓, SIL ✓ (发现浮点截断), HIL ✓ (发现通信延迟). Label: "三级验证完整闭环".

**Block 3 (L2, 2020-2022, fill #C8E6C9)**: "条件辅助 — MPC建议+人工确认". Key metric: "水位偏差 ±15cm→±5cm". ODD annotation: "设计流量±10%".

**Block 4 (L3, 2022-2024+, fill #BBDEFB)**: "条件自主 — MPC自主+人工监督". Key metric: "水位偏差 ±3cm". ODD annotation: "设计流量±30%, 含常见扰动".

Between each block, upward transition arrows labeled with prerequisites: "技术前提: 12个月运行数据", "验证前提: SIL/HIL覆盖率≥98%", "管理前提: 四态机+审计链就绪".

Clean staircase timeline diagram. Academic textbook quality. Chinese+English labels. Minimum 2400×1400px.

---

### 图6-3: 沙坪水电站PAI-CAI协作决策流程
**文件名**: fig_6_3_shaping_pai_cai_workflow.png

**提示词**:
A workflow diagram showing the PAI-CAI collaborative decision process at Shaping Hydropower Station. White background, portrait orientation (1800×2200px).

Four-step vertical workflow with two parallel swim lanes: left lane "PAI 物理AI引擎" (fill #E3F2FD), right lane "CAI 认知AI引擎" (fill #FFF3E0).

**Step 1 — 情境感知 Situation Awareness** (CAI lane): CAI aggregates four input sources shown as feed-in arrows: "SCADA实时数据", "水情预报(3-6h)", "上级调度令", "机组检修计划". Output: "结构化态势报告".

**Step 2 — 方案生成 Option Generation** (spanning both lanes): CAI calls PAI for computation. PAI box: "调洪演算 + 机组特性曲线 → 帕累托前沿". Three output option cards: "方案A: 保守安全型", "方案B: 均衡型", "方案C: 经济优先型". Each card has mini-metrics: risk level, generation loss, flood margin.

**Step 3 — 决策解释 Decision Explanation** (CAI lane): CAI generates natural language explanation bubble: "方案A: 泄洪闸2→4孔, 下游+800m³/s(低于安全阈值), 发电损失8.5万kWh, 防洪库容+1200万m³".

**Step 4 — 执行跟踪 Execution Tracking** (spanning both lanes): Human operator icon selects plan → CAI coordinates PAI+DAL execution → monitoring loop with "偏差预警 Deviation Alert" feedback arrow back to Step 1.

Clean vertical workflow diagram. Flat design. Academic textbook quality. Chinese+English labels. Minimum 1800×2200px.

---

### 图6-4: 胶东调水与沙坪水电站技术方案对比
**文件名**: fig_6_4_jiaodong_vs_shaping_comparison.png

**提示词**:
A side-by-side comparison diagram of two engineering cases. White background, landscape orientation (2400×1600px).

Two vertical panels divided by a center line:

**Left panel — 胶东调水 Jiaodong Water Transfer** (header fill #BBDEFB): Icon: long canal with gates. "控制目标: 单一 (水位控制)". "核心技术: MPC". "人机模式: L3 系统自主+人工监督". "模型特点: IDZ降阶, 确定性强". "关键挑战: 长时滞, 多耦合, 冰期".

**Right panel — 沙坪水电站 Shaping Hydropower** (header fill #FFF3E0): Icon: dam with turbines. "控制目标: 多目标冲突 (发电/泄洪/生态)". "核心技术: PAI+CAI协作". "人机模式: L2 系统建议+人工决策". "模型特点: 多目标优化, 不确定性大". "关键挑战: 目标冲突, 来水不确定, 梯级耦合".

**Center shared box** (fill #F5F5F5): "共享CHS机制: 安全包络 | 四态机 | 策略门禁 | MIL/SIL/HIL | 审计链".

Bottom annotation: "CHS框架适应性: 控制策略因场景而异, 安全治理机制保持统一".

Clean comparison diagram. Academic textbook quality. Chinese+English labels. Minimum 2400×1600px.

---

### 图6-5: 中外典型案例WNAL等级对照
**文件名**: fig_6_5_global_wnal_comparison.png

**提示词**:
A horizontal bar chart comparing WNAL levels across six engineering cases. White background, landscape orientation (2400×1400px).

Vertical axis (left): six project names: "胶东调水 Jiaodong", "沙坪水电站 Shaping", "南水北调中线 SNWTP", "CAP (美国)", "Canal de Provence (法国)", "MWRA Boston (美国)".

Horizontal axis: WNAL levels L0 through L4 with colored zones: L0 (gray #E0E0E0), L1 (#FFF9C4), L2 (#C8E6C9), L3 (#BBDEFB), L4 (#E1BEE7).

Each project has a progress bar: solid fill = achieved level, hatched fill = target level. Jiaodong: solid to L3. Shaping: solid to L2, hatched to L3. SNWTP: solid to L1, hatched to L2. CAP: solid to L2, note "水权法规限制 Legal constraint". Canal de Provence: solid to L2. MWRA: solid to L1-L2.

Right annotation column: key limitation per project.

Clean academic comparison chart. Chinese+English labels. Minimum 2400×1400px.

---

### 图6-6: 三类典型失败模式与CHS防线对应关系
**文件名**: fig_6_6_failure_modes_vs_chs_defenses.png

**提示词**:
A mapping diagram showing three failure modes matched to CHS framework defenses. White background, portrait orientation (1800×2000px).

Left column — "失败模式 Failure Modes" (fill #FFEBEE, border #D32F2F): three red-bordered boxes: "ODD缺失 — 无定义区域事故", "验证不足 — 现场意外", "运维缺失 — 效果衰减".

Right column — "CHS防线 CHS Defenses" (fill #E8F5E9, border #388E3C): three green-bordered boxes: "ODD显式定义 + WNAL等级评估 (Ch4)", "MIL/SIL/HIL三级验证 (Ch3原理五)", "审计链 + 模型校正长效机制 (Ch5)".

Red-to-green horizontal arrows connecting each pair with labels: "防线一", "防线二", "防线三".

Bottom box (fill #FFF8E1, border #F57F17): "深层根源: 技术决策与工程管理脱节 → CHS对策: WNAL分级 + 四态机 + 审计链 = 制度性弥合工具".

Clean mapping diagram. Flat design. Academic textbook quality. Chinese+English labels. Minimum 1800×2000px.

---

### 图6-7: 水利工程智能化四阶段实施路线图
**文件名**: fig_6_7_four_stage_implementation_roadmap.png

**提示词**:
A four-stage implementation roadmap for water engineering intelligent transformation. White background, landscape orientation (2800×1600px).

Four horizontal blocks as ascending steps connected by forward arrows:

**Stage 1 (1-3个月, fill #E3F2FD)**: "基础评估 Foundation Assessment" — items: "可控可观核验", "传感器/执行器评估", "SCADA数据质量审计". Deliverable: "可控可观核验报告". Warning: "⚠ 重算法轻硬件".

**Stage 2 (3-6个月, fill #FFF3E0)**: "安全底线 Safety Baseline" — items: "MRC设计", "四态机降级机制", "审计链+SOP". Deliverable: "安全运行规程". Warning: "⚠ 规程停在纸面".

**Stage 3 (6-12个月, fill #E8F5E9)**: "控制建设 Control Capability" — items: "控制器设计", "MIL→SIL→HIL验证", "灰度上线". Deliverable: "通过验证的控制系统". Warning: "⚠ 跳过HIL".

**Stage 4 (持续, fill #F3E5F5)**: "运维演进 O&M Evolution" — items: "模型校正", "ODD扩展", "WNAL跃迁", "属地化建设". Deliverable: "年度评估报告". Warning: "⚠ 维护未属地化".

Top banner: "核心原则: 先安全后性能 | 先局部后全局 | 先验证后上线". Bottom timeline bar: months 0→3→6→12→ongoing.

Clean roadmap/staircase diagram. Flat design. Academic textbook quality. Chinese+English labels. Minimum 2800×1600px.

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
| Ch6 | 7 | 6-1, 6-2, 6-3, 6-4, 6-5, 6-6, 6-7 |
| Ch7 | 2 | 7-1, 7-2 |
| Ch8 | 2 | 8-1, 8-2 |
| **合计** | **35** | |
