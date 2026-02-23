# 面向水网工程的基于模型定义（MBD）方法论（Ⅱ）：总体框架与工程验证

**摘要：** 姊妹篇上篇（Ⅰ）系统阐述了面向水网工程的MBD方法论内涵与四类模型协同体系。本文作为下篇，在此基础上提出"四层一闭环"总体框架：以运行设计域（ODD）分层表达为顶层约束，以多模型耦合仿真（SIM）为底座支撑，以分层分布式控制/多智能体系统（HDC/MAS）为决策内核，以模型在环（MIL）/软件在环（SIL）/硬件在环（HIL）分级验证为质量保障，以现场执行与数据回馈形成持续进化闭环。针对供水调度、防洪减灾和水资源综合利用三类典型水网功能场景，给出了框架的差异化适配方案。进而构建了从SIM仿真平台、ODD场景定义、MAS协同部署到SIL/HIL在环验证的关键技术工程链，提出了ODD驱动的五元组证据链形成机制。结合南水北调中线、胶东调水、大渡河瀑深枕梯级EDC及沙坪水电站发电泄洪智能控制等工程实践，验证了框架核心要素的技术可行性，揭示了"水位区间→运行域→控制策略"映射关系作为ODD与HDC协同设计在水网工程中的自然体现，并指出了从MIL向SIL/HIL系统化跨越的演进路径。

**关键词：** 水网工程；基于模型的定义（MBD）；运行设计域（ODD）；在环验证（SIL/HIL）；四层一闭环；多智能体系统（MAS）；证据链

**Abstract:** Part Ⅰ of this companion series established the MBD methodology connotation and four-category model taxonomy for water network engineering. This paper, as Part Ⅱ, proposes a "four-layer, one-loop" overall framework: ODD layered specification as the top-level constraint, multi-model coupled simulation (SIM) as the foundation, HDC/MAS as the decision-making core, MIL/SIL/HIL staged verification as quality assurance, and field execution with data feedback forming a continuous evolution loop. The framework is adapted to three typical water network scenarios. A key technology engineering chain from SIM platform, ODD scenario definition, MAS collaborative deployment to SIL/HIL verification is constructed, with an ODD-driven five-tuple evidence chain mechanism. Preliminary practices from the South-to-North Water Diversion Middle Route, Jiaodong Water Transfer, Shaping Hub, and Daduhe cascade projects verify the technical feasibility of core framework elements.

**Keywords:** water network engineering; Model-Based Definition (MBD); Operational Design Domain (ODD); in-the-loop verification (SIL/HIL); four-layer one-loop; Multi-Agent System (MAS); evidence chain

## 引言

姊妹篇上篇[1]以CPSS认知为基础，系统阐述了水网MBD方法论从"设计锁定效应"识别到"运行能力交付"的核心理念，构建了物理对象模型（PBM）、面向控制的简化模型（SM）、观测与状态估计模型（OSEM）及控制策略模型（HDC/MAS）四类模型协同体系与统一仿真验证平台。上篇回答了"水网MBD是什么"的问题；本文作为下篇，回答"水网MBD怎么做"的问题。

在工业领域，MBD的落地需要从方法论内涵走向系统化框架与工程化路径。航空航天行业通过V模型将需求定义、模型开发、在环验证和系统集成组织为标准化流程[2]；自动驾驶行业以ODD为核心，构建了场景驱动的安全论证体系[3]。水网工程具有不同于上述行业的独特特征：水力过程具有跨越数个数量级的时间尺度差异——单个渠池水位响应为分钟至小时量级（压力波传播），全线流量到达传播可达十余天量级（质量波传播）[4]；传感器稀疏且分布不均；执行机构受物理行程和安全约束限制；调度规程涉及多利益主体博弈。这些特征要求MBD框架进行针对性适配。

目前，水利行业在水动力仿真[5-7]、调度优化[8-10]及自动化控制[4,11-13]等环节已积累丰富实践，部分工程已在典型场景下开展MIL测试[14,18]，个别工程进行了局部SIL/HIL探索[16-17]，但整体而言，验证实践缺乏系统性——根本原因在于行业对ODD概念认识不足，不知道"应该验证什么场景"，因而无法建立ODD定义、模型仿真、控制部署与在环验证一体化闭环的系统方法。本文在上篇四类模型协同体系的基础上，提出"四层一闭环"总体框架，构建关键技术工程链，并结合国内外实践进行初步验证。

## 1　"四层一闭环"总体框架

### 1.1　总体架构设计

面向水网工程的MBD总体框架采用"四层一闭环"结构（表1），自顶向下分为ODD定义层、模型决策层、在环验证层和现场执行层，以数据回馈通道形成持续进化闭环：

表1　"四层一闭环"MBD总体架构

| 层次 | 核心功能 | 核心输出 |
|-----|---------|---------|
| ODD定义层 | 运行场景分类与边界约束 | ODD参数表与场景库 |
| 模型决策层 | 多模型耦合仿真与控制策略优化 | 控制策略方案与仿真验证报告 |
| 在环验证层 | MIL→SIL→HIL分级验证 | 五元组证据链 |
| 现场执行层 | 控制策略部署与实时运行 | 运行数据与偏差记录 |

a. ODD定义层。以"允许运行范围"为核心概念，将调度规程中隐含的运行边界显式化、参数化。ODD定义层的输出是分层结构化的场景库，为下游各层提供统一的测试输入和评估基准。ODD边界的变化（如新增工况、规程修订）可直接触发下游验证流程的增量更新，无需全系统重新验证。

b. 模型决策层。基于上篇构建的四类模型协同体系（PBM/SM/OSEM/HDC-MAS），在统一仿真平台上进行控制策略的开发、调参和性能评估。模型决策层同时承担设计空间探索功能——通过蒙特卡洛仿真或多目标优化，评估不同设计方案（如传感器布设、控制器参数、闸门调度规则）的运行效能，为设计决策提供量化依据。

c. 在环验证层。采用MIL→SIL→HIL分级递进策略：MIL阶段验证控制算法与PBM闭环交互的功能正确性；SIL阶段将控制算法编译为目标平台代码，验证软件实现与算法设计的一致性；HIL阶段将控制代码部署至真实PLC/RTU硬件，验证硬件环境下的时序特性、通信协议可靠性和故障响应能力。三个阶段逐级逼近真实运行条件，每一阶段的验证报告构成证据链的一环。

d. 现场执行层。经在环验证确认的控制策略部署至现场工程。运行数据通过标准化接口回馈至模型决策层和ODD定义层，驱动模型参数动态校正和ODD边界更新，形成"设计—验证—运行—再设计/再验证"的持续进化闭环。

### 1.2　框架在不同水网功能场景下的适用性

不同水网功能场景对MBD框架各层的技术需求存在差异化侧重：

a. 供水调度场景（如南水北调、胶东调水）。ODD侧重流量变化、用水需求波动和冰期运行等常态化场景组合，验证重点在控制策略的长期稳定性与节能优化效果，水力时间尺度横跨分钟级（闸门动作响应）到旬月级（水量分配计划），MAS协商机制需处理多用水主体利益协调。

b. 防洪减灾场景（如流域梯级调度）。ODD侧重极端来水、设备故障和通信中断等高风险场景，验证重点在系统的快速响应能力和安全降级机制，时间尺度以分钟至小时级为主，安全约束（最低安全余量、降级策略）在ODD和控制策略中均需显式建模。

c. 水资源综合利用场景（如多功能水库群联合调度）。ODD需覆盖发电、灌溉、生态、航运等多目标间的动态权衡，验证重点在多目标帕累托前沿的鲁棒性和目标切换策略的平滑性，时间尺度横跨日内调节到年际调度，社会层约束（如优先级规则、跨区域协调机制）比前两类场景更为突出。

## 2　ODD分层表达机制

运行设计域（ODD）是MBD框架的顶层约束。借鉴自动驾驶行业的ODD方法论[3]，本文将水网ODD定义为系统被设计为能够正常运行的外部条件、运行模式和约束边界的完整集合，并建立分层表达机制。

### 2.1　ODD三区间划分

ODD将连续的运行状态空间划分为三个区间：正常运行域（Normal Operating Envelope）、扩展运行域（Extended Operating Envelope）和最小风险条件域（Minimal Risk Condition，MRC）。正常运行域对应调度规程覆盖的常规工况，系统应实现设计性能指标；扩展运行域对应超出常规但仍可控的工况（如设备部分退化、非设计来水过程），系统性能允许适度降低但需保持安全运行；MRC对应系统应启动安全降级措施的极端工况边界，包括紧急停水、闸门全开泄洪等最后防线策略。

### 2.2　ODD参数化表达

ODD边界通过六维参数向量进行结构化表达：水文边界（来水过程、回归水量、区间入流等）、设备状态（闸门/泵站可用度、执行器行程约束等）、通信条件（测站在线率、延时上限、丢包率等）、环境因素（冰期、风浪、泥沙等）、社会约束（用水优先级、生态流量底线、通航要求等）及运行模式（正常输水、应急调度、检修工况等）。每一维参数均明确取值范围，不同维度的组合构成ODD场景库的生成空间。

### 2.3　与调度规程的映射

ODD分层表达机制为传统调度规程提供了形式化转译工具：将规程中的自然语言描述转化为可计算的参数约束集合，使"允许运行范围"从隐性经验变为显性规范。更重要的是，ODD的参数化表达使得"边界之外发生什么"成为可分析、可设计的工程问题——传统规程通常不回答这一问题，而MBD通过MRC策略显式设计系统在边界区域的安全退出路径。

传统调度规程与ODD的映射关系为：规程中"当来水流量超过X时，启动应急预案"对应ODD的水文边界参数跨区事件，规程中"设备检修期间降低输水流量至Y"对应ODD的设备状态参数降级场景。通过这一映射，调度规程的完备性可借助ODD的参数组合进行系统化审计——识别规程未覆盖的场景盲区。

## 3　关键技术工程链

从上篇的模型体系到实际工程部署，需要一条系统化的技术工程链将MBD各要素串联。该工程链包含四个核心环节（图1）：SIM仿真平台建设→ODD场景定义→MAS协同部署→SIL/HIL在环验证。

图1　CPSS框架下关键技术之间的工程逻辑关系

Fig.1　Engineering chain between key technologies under the CPSS framework

### 3.1　SIM仿真平台建设

SIM仿真平台是整个工程链的底座。平台需实现三项核心能力：（1）多模型异步耦合——PBM、SM、OSEM和控制策略模型以不同时间步长运行，通过统一调度器保障时间同步和数据一致性；（2）场景批量注入——接受ODD场景库生成的标准化测试用例，支持自动化批量仿真和结果归档；（3）软硬件接口预留——SIL阶段支持控制代码编译替换，HIL阶段支持工业通信协议（如OPC UA、Modbus）接入真实控制硬件。

### 3.2　ODD场景定义

ODD场景定义环节将六维参数空间的离散采样转化为结构化的测试场景库。场景生成策略兼顾覆盖性与经济性：首先以正交试验或拉丁超立方采样覆盖正常运行域的典型工况组合；其次以故障树分析和历史事件库补充扩展运行域的关键风险场景；最后以安全分析方法识别MRC边界的极端场景。场景库随工程运行经验积累持续扩充，形成"初始设计库→运行增量库→完整场景库"的递进发展路径。

### 3.3　HDC/MAS协同部署

HDC/MAS协同部署环节将控制策略从算法原型转化为可部署的工程实体。部署过程包括：（1）HDC三层架构参数化配置——明确战略层/战术层/现场层的决策周期、优化目标和约束传递接口；（2）MAS协商协议设计——定义智能体间的信息交换格式、协商轮次上限和收敛判据；（3）安全降级策略实现——当MAS协商超时或通信中断时，系统自动退回HDC层级指令模式或进入MRC状态。部署完成后，控制策略以可执行代码形式进入在环验证流程。

### 3.4　SIL/HIL在环验证与证据链

在环验证是MBD框架的质量保障核心。验证流程遵循ODD驱动的五元组证据链机制（图2）：

图2　ODD驱动的SIL/HIL在环验证与证据链形成示意

Fig.2　Schematic diagram of ODD-driven SIL/HIL in-loop verification and evidence chain formation

五元组 = {ODD场景标识, 验证级别(MIL/SIL/HIL), 性能指标, 通过/未通过判据, 时间戳与版本号}。每完成一项场景的某级别验证，即生成一条五元组记录。全部记录汇聚为完整的证据矩阵，其覆盖度（已验证场景数/ODD场景总数）和通过率（通过数/已验证数）构成MBD交付质量的定量评估指标。

SIL验证的核心关注点为：控制代码与算法设计的一致性、边界条件处理的正确性、异常输入的鲁棒性以及多线程/多进程环境下的时序安全性。HIL验证在SIL基础上增加：真实硬件的I/O响应延迟、工业通信协议的可靠性（如丢包重传、超时恢复）、控制器与仿真器之间的实时同步精度以及硬件故障（如PLC宕机、RTU通信中断）下的安全降级响应。

## 4　初步实践与验证

### 4.1　国际实践现状：MIL为主，ODD意识缺失

在国际范围内，水利领域的控制算法验证主要停留在MIL层级。ASCE灌溉渠道控制算法委员会建立了标准化基准渠道，对PI、LQR、MPC等控制算法进行了系统仿真测试[28,29]，但场景主要围绕典型用水需求变化工况。法国Litrico和Fromion建立了频域控制设计与验证方法论[33]，西班牙基于LMI方法完成了PI控制器优化验证[34]，荷兰van Overloop团队和Negenborn等分别将分布式预测控制应用于荷兰国家水网和灌溉渠道[32,35]，法国Calais运河完成了数字孪生MPC验证[30]。水电领域，美国NREL开发了兆瓦级实时硬件在环仿真平台（RTHEP），但聚焦于水电—电网并网控制[31]。

上述实践的共同特征是：验证以MIL或实验室渠道为主，缺乏类似自动驾驶行业的ODD概念——即未将"系统被设计为能够运行的完整条件集合"作为验证的顶层驱动；SIL/HIL测试在水利领域基本空白。

### 4.2　国内实践：从典型场景MIL到ODD探索

在南水北调中线、胶东调水及大渡河梯级水电站等工程中，研究团队构建了水力仿真模型（PBM）与面向控制的简化模型（SM），开展了MIL测试[4,18]。管光华等[36]针对南水北调中线构建了实时自校正数字孪生模型，其团队基于广义ID模型[25]和分布式MPC-ADMM方案[37]建立了树状渠系多区域协调控制的建模—仿真—验证链条。王忠静等[11,38]以积分时滞算法构建了多输入多输出渠系最优控制方法，全渠系智能控制系统已在新疆、内蒙古等灌区部署运行。胶东调水工程围绕570公里、13座泵站级联系统，开展了跳站优化调度[39]和泵站控制时间分析[40]等仿真研究，目前处于算法仿真验证阶段。

然而，现有MIL测试以典型场景为主，远未实现ODD驱动的全场景系统化覆盖。HIL测试平台已在引调水渠道控制[16]和船闸工控[17]等领域完成设计与搭建，雷晓辉等[14]提出了面向自主运行水网的MIL/SIL/HIL三级在环测试体系框架，但总体上仍处于单点平台建设阶段，尚未形成基于ODD场景库的标准化验证流程。

### 4.3　ODD与HDC深度实践：大渡河梯级水电站

大渡河梯级水电站提供了两个均已业务化运行的案例，集中体现了ODD与HDC（分层分布式控制）的协同设计思想[24,41,42]。

瀑深枕（瀑布沟—深溪沟—枕头坝）梯级联合调度的ODD核心在于：以反调节水库（深溪沟）水位区间为枢纽，划分不同运行域并匹配差异化的EDC（Economic Dispatch Control）策略。正常运行域内，梯级总负荷按蓄能最大原则在各站间优化分配，同时回避机组振动区；当深溪沟水位趋近上下限时，系统自动降级为单站独立保底模式；来水突变或事故切机时触发紧急安全响应。这一"水位区间→运行域→控制策略"的映射关系，恰是ODD分层定义与HDC分层控制在水电调度中的自然体现——不同ODD对应不同层级的控制架构与优化目标。该策略通过"电网—集控—电站"三层控制模式和改进动态规划算法实现了电网AGC实时考核要求[42]。

沙坪二级水电站作为枕头坝下游的径流式电站，库容极小（调节库容585万m³），面临上游来流频繁波动（汛期流量变化超100m³/s事件年均约3000次）的挑战。研究团队在发电控制基础上实现了泄洪闸门联动智能控制[41]：基于一维水动力模型和水位预测，按水位区间定义了"纯发电调节→发电泄洪协调→闸门应急"三级ODD，在各运行域内分别匹配负荷申报策略、闸门联动预测控制和应急分段优化策略，首次在径流式水电站中实现了发电与泄洪的一体化ODD驱动智能控制。

### 4.4　实际运行模式与瓶颈

上述各工程的智能化控制算法投运后，普遍采用"现场工程师在线值守+算法远程升级维护"的运行模式——研发工程师通过远程通信链路对运行算法进行参数调优和版本更新，现场运行人员负责监视系统状态并在必要时进行人工干预。这一模式表明：当前MBD框架的实践深度主要集中在典型场景MIL层级，且ODD意识的普遍缺失是制约验证深度的核心瓶颈。

需要特别指出的是，上述实践均属于MBD方法论在"运行验证"层面的应用——即在已建成工程上验证控制算法的有效性。而MBD方法论的更高层级应用——以运行仿真反哺工程设计优化，例如通过全场景ODD仿真评估渠道断面设计的冗余度、闸站布局对控制性能的影响、泵站选型与变频配置对节能效果的贡献等——在水利行业尚未开始。在制造业中，MBD驱动的"设计—仿真—验证"迭代已是成熟实践[2]；而水利工程的设计与运行长期脱节，设计阶段几乎不考虑运行控制需求，运行阶段则被迫在既有工程约束下"打补丁"。这一断裂恰恰是MBD方法论最有潜力弥合的缺口。

## 5　结论与展望

本文作为姊妹篇下篇，在上篇MBD方法论内涵与模型体系的基础上，给出了面向水网工程的MBD总体框架与工程验证路径，主要结论如下：

a. 提出了"四层一闭环"总体框架。ODD定义层→模型决策层→在环验证层→现场执行层，以数据回馈形成持续进化闭环。框架对供水调度、防洪减灾、水资源综合利用三类场景具有差异化适配能力。

b. 建立了ODD分层表达机制。将连续运行状态空间划分为正常运行域、扩展运行域和最小风险条件域（MRC），通过六维参数向量实现调度规程的形式化表达，为场景盲区识别和安全退出路径设计提供系统化工具。

c. 构建了关键技术工程链与证据链机制。SIM仿真平台→ODD场景定义→HDC/MAS协同部署→SIL/HIL在环验证四环节串联，以ODD驱动的五元组证据链实现验证质量的定量评估。

d. 国内外实践揭示了ODD意识缺失是核心瓶颈。大渡河梯级水电站两个业务化运行案例表明，"水位区间→运行域→控制策略"的映射关系是ODD与HDC协同设计在水网工程中的自然体现，为框架的ODD层提供了最具参考价值的工程范例。

展望未来，MBD方法论在水网工程中的深化应用需沿五步路径推进：（1）ODD意识建立与边界提取——在行业层面引入ODD概念体系，将现有调度规程、运行经验和历史事件库进行形式化表达；（2）ODD边界量化——建立覆盖主要水网类型的ODD参数标准库，实现从典型场景向完整运行域的系统化扩展；（3）验证体系结构化——形成ODD驱动的MIL/SIL/HIL分级验证行业规范与证据链标准；（4）运行能力动态化——基于运行数据驱动的模型校正与ODD边界动态更新机制；（5）设计优化闭环——将运行阶段积累的ODD覆盖数据和控制性能评估反馈至工程设计阶段，以MBD仿真评估驱动渠道断面、闸站布局和设备选型的优化迭代，实现"设计即考虑运行"的方法论跨越。

随着国家水网建设的推进，MBD方法论将成为水网工程从"建得好"向"管得好、运行得好"跨越的关键方法论基础设施。

## 参考文献

[1] 雷晓辉,等.面向水网工程的基于模型定义（MBD）方法论（Ⅰ）：内涵与模型体系[J].（姊妹篇上篇）

[2] 何绍民,杨欢,王海兵,等.电动汽车功率控制单元软件数字化设计研究综述及展望[J].电工技术学报,2021,36(24):5101-5114.

[3] BSI. PAS 1883: Operational Design Domain (ODD) taxonomy for an automated driving system (ADS) — Specification[S]. London: British Standards Institution, 2020.

[4] 孔令仲,雷晓辉,张召,等.多级串联明渠调水工程多目标水位预测控制模型研究[J].水利学报,2022,53(4):471-482.

[5] 周立,吴琼,姚仕明,等.江湖系统显式与隐式二维水动力模型比较[J].长江科学院院报,2021,38(12):12-18.

[6] 闫毓,袁赛瑜,唐洪武,等.上海蕰南水利控制片河网水动力再造[J].河海大学学报(自然科学版),2021,49(4):329-334,365.

[7] Yan P R, Zhang Z, Lei X H, et al. A multi-objective optimal control model of cascade pumping stations considering both cost and safety[J]. Journal of Cleaner Production, 2022, 345: 131171.

[8] Liu X L, Liu Z R, Hou X, et al. A parallel multi-objective optimization based on adaptive surrogate model for combined operation of multiple hydraulic facilities in water diversion project[J]. Journal of Hydroinformatics, 2024, 26: 1351-1369.

[9] 方国华,李智超,钟华昱,等.考虑供水均衡性的南水北调东线工程江苏段优化调度[J].河海大学学报(自然科学版),2023,51(3):10-18.

[10] Chen H T, Wang W C, Chau K W, et al. Flood control operation of reservoir group using yin-yang firefly algorithm[J]. Water Resources Management, 2021, 35: 5325-5345.

[11] 王忠静,郑志磊,徐国印,等.基于线性二次型的多级联输水渠道最优控制[J].水科学进展,2018,29(3):383-389.

[12] 郑大琼,任钟淳,米恩柏.长距离明渠输水工程实时控制研究[J].河海大学学报,1998,(5):53-59.

[13] Li X, Guan G, Tian X, et al. Hybrid feedforward-feedback LQR controller based on model prediction for open channel water level control[J]. Journal of Hydroinformatics, 2025, 27(1): 33-50.

[14] 雷晓辉,张峥,苏承国,等.自主运行智能水网的在环测试体系[J].南水北调与水利科技(中英文),2025,23(4):787-793.

[15] 蔡阳.数字孪生水网建设应着力解决的几个关键问题[J].中国水利,2024,(17):36-41.

[16] 何立新,史博阳,张峥,等.引调水渠道控制系统硬件在环测试平台设计与实现[J].南水北调与水利科技(中英文),2025,23(5):1036-1046.

[17] 王忠民,齐俊麟,李乐新.船闸工控系统硬件在环仿真平台设计与实现[J].水利水电技术(中英文),2024,55(S2):887-892.

[18] 何立新,曹辰宇,张峥,等.引黄济青明渠段输水控制系统的MIL测试系统设计与实现[J].南水北调与水利科技(中英文),2025,23(1):1-9,58.

[19] 雷晓辉,龙岩,许慧敏,等.水系统控制论：提出背景、技术框架与研究范式[J].南水北调与水利科技(中英文),2025,23(4):761-769,904.

[20] 雷晓辉,苏承国,龙岩,等.基于无人驾驶理念的下一代自主运行智慧水网架构与关键技术[J].南水北调与水利科技(中英文),2025,23(4):778-786.

[21] 雷晓辉,许慧敏,何中政,等.水资源系统分析学科展望：从静态平衡到动态控制[J].南水北调与水利科技(中英文),2025,23(4):770-777.

[22] Kong L, Li Y, Tang H, et al. Predictive control for the operation of cascade pumping stations in water supply canal systems considering energy consumption and costs[J]. Applied Energy, 2023, 341: 121103.

[23] 夏军,陈进,佘敦先,等.变化环境下中国现代水网建设的机遇与挑战[J].地理学报,2023,78(7):1608-1617.

[24] 涂扬举,梅亚东,曹辉,等.复杂环境下流域梯级水电站智慧运行关键技术与应用[R].国家能源集团大渡河流域水电开发有限公司,2021.（2021年水力发电科学技术奖一等奖）

[25] Zhu Z, Guan G, Tian X, et al. The Integrator dual-Delay model for advanced controller design of the open canal irrigation systems with multiple offtakes[J]. Computers and Electronics in Agriculture, 2023, 205: 107616.

[26] 王涛,杨开林.调水工程明渠水力控制线性化数学模型[J].南水北调与水利科技(中英文),2005,3(3):52-55.

[27] Asano R Jr, Ferreira F O, Gramulia J, et al. Integration of water transfers in hydropower operation planning[J]. Energies, 2024, 17: 5872.

[28] Clemmens A J, Kacerek T F, Grawitz B, et al. Test cases for canal control algorithms[J]. Journal of Irrigation and Drainage Engineering, 1998, 124(1): 23-30.

[29] Bautista E, Clemmens A J, Strand R J. Salt River Project canal automation pilot project: simulation tests[J]. Journal of Irrigation and Drainage Engineering, 2006, 132(2): 143-152.

[30] Ranjbar R, Segovia P, Duviella E, et al. Digital twin of Calais canal with model predictive controller: a simulation on a real database[J]. Journal of Water Resources Planning and Management, 2024, 150(5): 04024014.

[31] Poudel B, Panwar M, Hovsapian R. Data-driven scalable emulation of hydropower using real-time hardware-in-the-loop[C]. NREL/PO-5D00-86870, National Renewable Energy Laboratory, 2023.

[32] Negenborn R R, van Overloop P J, Keviczky T, et al. Distributed model predictive control for irrigation canals[J]. Networks and Heterogeneous Media, 2009, 4(2): 359-380.

[33] Litrico X, Fromion V. Modeling and control of hydrosystems[M]. Dordrecht: Springer, 2009.

[34] Arauz T, Maestre J M, Tian X, et al. Design of PI controllers for irrigation canals based on linear matrix inequalities[J]. Water, 2020, 12(3): 855.

[35] van Overloop P J, Negenborn R R, De Schutter B, et al. Predictive control for national water flow optimization in the Netherlands[C]//Intelligent Systems, Control and Automation: Science and Engineering. Dordrecht: Springer, 2010, 42: 439-461.

[36] Liu W J Y, Guan G H, Tian X, et al. Exploiting a real-time self-correcting digital twin model for the middle route of the South-to-North Water Diversion Project of China[J]. Journal of Water Resources Planning and Management, 2023, 149(7): 04023023.

[37] Zhu Z L, Guan G H, Wang K. Distributed model predictive control based on the alternating direction method of multipliers for branching open canal irrigation systems[J]. Agricultural Water Management, 2023, 285: 108384.

[38] 王忠静,贾仰文,甘泓,等.大中型自流灌区全渠系智能控制方法与系统[Z].清华大学,2023.

[39] Zhang Z, Lei X H, Tian Y, et al. Optimized scheduling of cascade pumping stations in open-channel water transfer systems based on station skipping[J]. Journal of Water Resources Planning and Management, 2019, 145(7): 05019011.

[40] Yan P R, Zhang Z, Lei X H, et al. A simple method for the control time of a pumping station to ensure a stable water level immediately upstream of the pumping station under a change of the discharge in an open channel[J]. Water, 2021, 13(3): 355.

[41] 雷晓辉,王孝群,龙岩,等.大渡河沙坪二级电站发电与泄洪多维决策管控模型研究应用[R].河北工程大学,2020.

[42] 涂扬举,梅亚东,张新明,等.大型梯级水电站间负荷实时智能调度技术[R].国电大渡河流域水电开发有限公司/四川大学/南瑞集团有限公司,2018.
