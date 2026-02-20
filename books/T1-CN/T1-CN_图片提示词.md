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
A control system block diagram for water systems. White background, blue color scheme. Central block labeled "水系统 f(·)" (Water System). Input arrows: u_k "控制输入" (gate opening, pump frequency) from left; d_k "外部扰动" (rainfall, demand) from top; θ_k "慢变参数" (roughness, degradation) from bottom-left. Output arrow: y_k "可测输出" (water level, flow) to right, with v_k "测量噪声" added. State x_k shown inside the block. Feedback loop from output back to controller block on the left. Clean signal flow diagram style, standard control engineering notation, academic textbook quality.

---

### 图2-2: 三类约束层次图
**文件名**: fig_2_2_three_constraint_layers.png

**提示词**:
A concentric circles diagram showing three layers of constraints in water system control. White background, blue color scheme. Innermost circle (light blue): "物理约束 Physical" - water level limits, flow velocity bounds, capacity bounds. Middle ring (medium blue): "操作约束 Operational" - minimum start-stop intervals, maintenance windows, ramp rate limits. Outermost ring (dark blue): "治理约束 Governance" - ecological flow red lines, supply agreements, authority boundaries. Arrows pointing inward showing "all three must be modeled together". Chinese and English labels. Clean academic diagram, flat design.

---

### 图2-3: 多时间尺度分层控制链
**文件名**: fig_2_3_multi_timescale_control_hierarchy.png

**提示词**:
A vertical hierarchy diagram showing four control layers with their time scales. White background, blue gradient. Top layer (lightest): "规划层 Planning" - "日/周级 Days/Weeks" - water resource allocation. Second layer: "协调层 Coordination" - "小时级 Hours" - cross-zone flow distribution. Third layer: "调节层 Regulation" - "分钟级 Minutes" - local section stability. Bottom layer (darkest): "执行层 Execution" - "秒级 Seconds" - device closed-loop control. Bidirectional arrows between layers. Time scale bar on the right side. Clock icons showing different time scales. Clean hierarchical diagram, academic textbook style.

---

### 图2-4: 异常工况四态机状态迁移图
**文件名**: fig_2_4_four_state_machine.png

**提示词**:
A state machine diagram with four states and transitions. White background. Four rounded rectangles arranged in a diamond/square pattern: "正常态 Normal" (green), "受限态 Restricted" (yellow), "降级态 Degraded" (orange), "接管态 Takeover" (red). Arrows between states showing transitions with trigger conditions labeled: "预测可信度下降" (Normal→Restricted), "黄区/红区边界" (Restricted→Degraded), "重大故障/越界" (Degraded→Takeover), and recovery paths back. Each state box contains 2-3 key actions. Clean state diagram style, colored states with Chinese labels, academic textbook quality.

---

## 第三章 水系统控制论八原理

### 图3-1: CHS八原理依赖导图
**文件名**: fig_3_1_eight_principles_dependency.png

**提示词**:
A horizontal flow diagram showing dependencies between CHS eight principles in five stages. White background, blue color scheme. Left to right: Stage 1 "建模层 Modeling" (Principle 1 Transfer Function + Principle 2 Controllability/Observability) → Stage 2 "架构层 Architecture" (Principle 3 Hierarchical Distributed + Principle 4 Safety Envelope) → Stage 3 "验证层 Verification" (Principle 5 In-the-Loop) → Stage 4 "协同智能层 Collaborative Intelligence" (Principle 6 Cognitive + Principle 7 Human-Machine) → Stage 5 "演进层 Evolution" (Principle 8 Autonomous Evolution). Forward arrows between stages. A feedback arrow from Principle 4 back to Principle 8 labeled "安全约束回边" (safety constraint feedback). Each principle in a rounded box with number and name. Clean dependency graph, academic style.

---

### 图3-2: 安全包络红黄绿三区示意图
**文件名**: fig_3_2_safety_envelope_zones.png

**提示词**:
A diagram showing safety envelope concept with three zones for water level control. White background. A vertical axis labeled "水位 Water Level" with a time series curve. Three horizontal bands: Green zone (center, green-tinted) labeled "绿区：性能优先运行" - normal operating range; Yellow zone (above and below green, yellow-tinted) labeled "黄区：保守策略，收缩控制域" - caution range; Red zone (outermost, red-tinted) labeled "红区：强制保护，接管" - emergency range. The water level curve oscillates mostly in green zone, briefly touching yellow zone. Upper and lower limit lines clearly marked. Clean technical diagram with Chinese labels, suitable for academic textbook.

---

### 图3-3: MIL-SIL-HIL在环验证管线图
**文件名**: fig_3_3_mil_sil_hil_pipeline.png

**提示词**:
A three-stage verification pipeline diagram. White background, blue color scheme. Three stages left to right, each in a large rounded rectangle: Stage 1 "MIL 模型在环" - contains icons of mathematical model + control logic, labeled "检验逻辑正确性"; Stage 2 "SIL 软件在环" - contains icons of code + numerical simulation, labeled "检验实现一致性"; Stage 3 "HIL 硬件在环" - contains icons of hardware + real-time interface, labeled "检验时序与接口可靠性". Arrows between stages with gate/checkpoint symbols labeled "门禁 Gate". Final arrow to "上线运行 Go-Live". A reject path loops back from each gate. Clean pipeline diagram, academic textbook style, Chinese and English bilingual.

---

## 第四章 水网自主等级

### 图4-1: WNAL L0-L5阶梯图
**文件名**: fig_4_1_wnal_staircase.png

**提示词**:
A staircase/step diagram showing six levels of water network autonomy (WNAL L0-L5). White background, blue gradient from light to dark ascending left to right. Six steps: L0 "手动运行 Manual" (lightest) → L1 "规则自动化 Rule-based" → L2 "条件自动化 Conditional Automation" → L3 "条件自主 Conditional Autonomy" (highlighted with a star) → L4 "高度自主 High Autonomy" → L5 "完全自主 Full Autonomy" (darkest, marked as "理论目标 Theoretical Target"). Each step has three labels below: machine capability, human role, ODD scope. L3 step has a callout box "降级与接管机制". L4 has callout "自诊断与灰度发布". Ascending arrow on the right. Clean infographic staircase, academic textbook quality.

---

### 图4-2: 等级跃迁四类门槛图
**文件名**: fig_4_2_level_transition_gates.png

**提示词**:
A diagram showing four mandatory gates for WNAL level transition. White background, blue scheme. Central arrow from "Lk" to "Lk+1" passing through four vertical gate barriers. Gate 1 (技术门槛 Technical): model, control, monitoring, computing. Gate 2 (验证门槛 Verification): MIL/SIL/HIL pass, scenario coverage. Gate 3 (治理门槛 Governance): responsibility matrix, takeover mechanism, audit chain. Gate 4 (运行门槛 Operational): sustained performance metrics. All four gates must be passed (AND logic). A "reject" path below loops back to Lk. Clean gate/barrier diagram, academic style, Chinese labels.

---

## 第五章 核心技术架构概览

### 图5-1: HydroOS三层架构图
**文件名**: fig_5_1_hydroos_architecture.png

**提示词**:
A layered architecture diagram for HydroOS water network operating system. White background, blue color scheme. Three main horizontal layers stacked bottom to top: Bottom layer (dark blue) "设备抽象层 Device Abstraction Layer" - icons for gates, pumps, sensors, SCADA. Middle layer (medium blue) "物理AI引擎 Physical AI Engine" - icons for hydrodynamic model, MPC optimizer, safety envelope, state estimator. Top layer (light blue) "认知AI引擎 Cognitive AI Engine" - icons for knowledge graph, LLM interpreter, multi-agent system, review engine. Left side: upward arrow labeled "数据上行 Data Upflow" from SCADA. Right side: downward arrow labeled "指令下行 Command Downflow". Above the three layers: "人机协同与治理审计 Human-Machine Collaboration & Governance Audit" module. Between middle and top layers: "策略门禁+四态机 Strategy Gate + State Machine" marker. Clean layered architecture diagram, academic textbook style.

---

### 图5-2: SCADA+MAS融合流程图
**文件名**: fig_5_2_scada_mas_fusion.png

**提示词**:
A horizontal flow diagram showing the SCADA+MAS fusion process. White background, blue scheme. Five steps left to right connected by arrows: Step 1 "SCADA上报状态" (sensor icons) → Step 2 "物理AI生成候选策略" (model icon with multiple options) → Step 3 "MAS多角色协商" (multiple agent icons discussing) → Step 4 "认知AI生成可执行指令" (LLM icon producing commands) → Step 5 "执行并回写日志" (actuator + log icons). A feedback loop from Step 5 back to Step 1. Above the flow: "人工监督层" with a human icon observing the process. Clean process flow diagram, academic textbook style, Chinese labels.

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
| Ch3 | 3 | 3-1, 3-2, 3-3 |
| Ch4 | 2 | 4-1, 4-2 |
| Ch5 | 2 | 5-1, 5-2 |
| Ch6 | 3 | 6-1, 6-2, 6-3 |
| Ch7 | 2 | 7-1, 7-2 |
| Ch8 | 2 | 8-1, 8-2 |
| **合计** | **23** | |
