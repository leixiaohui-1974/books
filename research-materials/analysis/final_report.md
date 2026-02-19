# 《水系统运行科学与工程及智慧水利：发展历程与未来展望》

## 报告定位

这是一份系统梳理“水系统运行科学与工程”（Hydro Systems Operation Science and Engineering）这一学科方向的发展历程，以及智慧水利的历史、现在和未来的综合性研究报告。本报告旨在从理论根基、学科演进、实践应用和未来展望等多个维度，深入剖析水系统运行科学与工程的内涵、价值和发展路径，并特别强调“水系统控制论”（Cybernetics of Hydro Systems, CHS）作为其核心理论框架的独特贡献。

---

## 第一部分：学科的理论根基

水系统运行科学与工程（Hydro Systems Operation Science and Engineering）作为一个新兴的交叉学科方向，其理论体系并非空中楼阁，而是深深植根于20世纪中叶以来蓬勃发展的若干基础学科的沃土之上。这些基础理论不仅为水系统运行的研究提供了世界观与方法论，更在不同发展阶段为其提供了直接的分析工具和技术手段。

### 1.1 系统科学：从整体观到复杂适应系统

系统科学为水系统运行研究提供了最底层的世界观和方法论，即“整体观”。水系统本质上是一个由众多相互关联、相互作用的组分构成的复杂整体。

#### 1.1.1 一般系统论的奠基
20世纪30至40年代，奥地利裔生物学家路德维希·冯·贝塔朗菲（Ludwig von Bertalanffy）创立了“一般系统论”（General System Theory）[1]。他在1937年首次提出该概念，并在1968年出版了集大成之作《一般系统论：基础、发展和应用》[2]。贝塔朗菲的核心洞见在于，不同学科领域中看似无关的系统其组织和行为规律遵循着某些共同的、普适性的原理。这一思想打破了传统学科壁垒，促使人们从“还原论”转向关注系统的**整体性、关联性、动态性和层级性**。

对于水系统而言，一般系统论的整体观带来了革命性的影响。一个大型流域或一个跨区域调水工程，不再被看作是水库、渠道、泵站、闸门等孤立设施的简单集合，而被视为一个具有特定结构和功能的有机整体。

#### 1.1.2 耗散结构与自组织
伊利亚·普里高津（Ilya Prigogine）在1969年正式提出“耗散结构”（Dissipative Structure）理论 [3]，并因此获得1977年诺贝尔化学奖。他揭示了开放系统如何通过与外界交换物质和能量，在远离平衡态的情况下自发形成有序结构。水系统作为一个典型的开放耗散系统，其河床演变、产汇流规律等都体现了这种从无序到有序的自组织过程。

#### 1.1.3 复杂适应系统（CAS）
20世纪80年代，以圣塔菲研究所（Santa Fe Institute）为中心兴起的复杂性科学进一步深化了系统观。约翰·霍兰（John H. Holland）在1995年出版《隐秩序》[4]，系统阐述了复杂适应系统（Complex Adaptive Systems, CAS）理论。CAS强调系统由大量具有适应性的主体（Agents）构成，宏观行为是从微观交互中“涌现”（Emergence）出来的。在水系统中，用水户、调度员、自动控制单元都是适应性主体，其决策行为与水的物理过程深度耦合。

### 1.2 控制论/控制科学：从反馈到自主

控制论（Cybernetics）是水系统运行的核心方法论。控制的本质是“驾驭不确定性”。

#### 1.2.1 控制论的诞生
1948年，诺伯特·维纳（Norbert Wiener）发表《控制论》[5]，正式宣告了该学科的诞生。维纳将“反馈”（Feedback）作为控制论的灵魂。反馈思想对于水系统运行具有奠基性意义。无论是古代都江堰的岁修，还是现代水库根据实测水位调整泄量，本质上都是“感知-决策-执行”的闭环反馈过程。

#### 1.2.2 经典控制与现代控制
- **经典控制（1940s-1950s）**：以传递函数和频域分析为核心，代表成果是PID控制器。1942年Ziegler和Nichols提出了著名的PID整定规则 [6]。PID至今仍是水利现场控制（如泵站恒压供水）的主力。
- **现代控制（1960s-1970s）**：以状态空间法为核心。1960年鲁道夫·卡尔曼（Rudolf E. Kálmán）发表了关于线性滤波和预测问题的论文（卡尔曼滤波）[7]，解决了线性系统状态估计问题。1957年理查德·贝尔曼（Richard Bellman）提出动态规划（Dynamic Programming）[8]，为最优控制奠定了数学基础。

#### 1.2.3 大系统控制理论
大型水系统（如南水北调）具有极高的维度。1970年Mesarovic等人出版《层次化多级系统理论》[9]，奠定了大系统理论基础。其核心思想是“分解-协调”（Decomposition-Coordination）。Siljak在1978年进一步发展了分散控制（Decentralized Control）理论 [10]。这些理论为水系统构建“总调-分调-站控”的分层分布式控制（HDC）架构提供了直接依据。

#### 1.2.4 模型预测控制（MPC）
1978年Richalet等人提出IDCOM [11]，1980年Cutler和Ramaker提出动态矩阵控制（DMC）[12]，标志着MPC的诞生。MPC通过“滚动优化”处理复杂约束和预测未来扰动，被认为是解决复杂水系统（如渠道、水库群）控制问题的最有效方法。Rawlings在2009年出版的《模型预测控制》是该领域的权威著作 [13]。

#### 1.2.5 智能控制与多智能体系统（MAS）
1965年Lotfi Zadeh提出模糊集合理论 [14]，开创了模糊控制。随着AI的发展，神经网络控制、强化学习控制逐渐兴起。Wooldridge在2009年系统论述了多智能体系统 [15]，为分布式水系统控制提供了新视角。

### 1.3 人工智能：从专家经验到大数据驱动

人工智能（AI）为水系统运行注入了“智慧”内涵。

1.  **专家系统（1970s-1980s）**：McCarthy和Minsky等先驱推动了早期AI发展。在水利领域，专家系统曾用于大坝安全诊断 [16]。
2.  **机器学习（1990s-2000s）**：1986年Rumelhart、Hinton等重新发现反向传播算法 [17]，使神经网络复兴。SVM、随机森林等被广泛用于水文预报。
3.  **深度学习（2010s-至今）**：2012年AlexNet突破，2017年Vaswani等提出Transformer [18]。LSTM等模型在长时序径流预报中取得当前最优性能。
4.  **强化学习（RL）**：Sutton和Barto在2018年系统论述了强化学习 [19]。RL非常适合解决水库调度等序贯决策问题。

### 1.4 信息-物理系统（CPS）：理论的融合

2006年，美国国家科学基金会（NSF）的Helen Gill提出信息-物理系统（Cyber-Physical Systems, CPS）概念 [20]。CPS将计算、通信与物理过程深度融合。智慧水利、数字孪生流域本质上都是水利领域的CPS。它强调“算、通、控”三者的内在统一，为水系统运行科学与工程提供了顶层设计框架。

---

## 第二部分：水系统运行的学科演进

### 2.1 早期实践：运行智慧的千年传承

- **都江堰（公元前256年）**：中国古代运行智慧的巅峰 [21]。通过鱼嘴、飞沙堰、宝瓶口的系统配合，实现了自动分流、排沙和流量控制。其“深淘滩，低作堰”的岁修制度是典型的闭环反馈管理。
- **古罗马水道（Aqueduct）**：通过标准尺寸的“卡里克斯”（Calix）进行流量计量和分配，体现了量化管理思想 [22]。

### 2.2 学科奠基：三大技术思潮的汇流

1.  **计算水力学（Computational Hydraulics）**：1871年圣维南（Saint-Venant）建立非恒定流方程组 [23]，1891年曼宁（Manning）提出经验公式 [24]。20世纪60年代起，Cunge等推动了数值模拟技术 [25]，解决了“算得准”的问题。
2.  **水信息学（Hydroinformatics）**：1991年迈克尔·阿伯特（Michael B. Abbott）正式提出该概念 [26]。他强调将ICT应用于水环境，核心是数据、模型与决策支持。IHE Delft成为其人才培养摇篮。
3.  **水资源系统工程（Water Resources Systems Engineering）**：20世纪60年代起，Yeh [27]、Labadie [28]、Loucks [29] 等学者将运筹学引入水利，解决了“管得好”的优化决策问题。

### 2.3 从“工程管理”到“系统运行”的范式升级

这是学科发展的根本性转换：
- **传统“工程管理”**：管理学范式，关注“人和组织”。核心是项目管理、合同管理、运维制度。
- **“水系统运行”**：控制科学范式，关注“水和设备”。核心是感知、建模、决策、执行、反馈的闭环控制。
CHS的提出，旨在将“运行”从管理学范式中解放出来，回归控制科学本质。

### 2.4 渠道自动化：控制理论的试验场

渠道系统的大时滞、非线性使其成为控制理论的绝佳试验场。
- **关键人物**：Charles Burt（ITRC创始人，推动灌溉现代化）[30]、Albert Clemmens（制定ASCE测试案例）[31]、Litrico与Fromion（出版经典教材）[32]、Malaterre（提出PILOTE算法）[33]、van Overloop（MPC应用先驱）[34]。
- **Rubicon Water**：通过“Total Channel Control”技术实现了基于MPC的商业化成功。

### 2.5 水控制学：理论框架的升华

**水系统控制论（Cybernetics of Hydro Systems, CHS）**由雷晓辉教授系统提出。
- **时间线**：2022年前后思想萌芽；2025年初雷晓辉教授全职加入河北工程大学；2025年正式命名CHS并发表论文 [35]。
- **核心内涵：六个统一**：
  1. **多类型统一**：调水、水电、灌区、城市供排水等均遵循相同控制规律。
  2. **多目标统一**：防洪、供水、发电、生态等整合为多目标优化控制。
  3. **多尺度统一**：秒级实时控制到年度水资源配置的层级衔接。
  4. **多域统一**：水量、水质、冰期、水力机械、工程安全耦合考虑。
  5. **分层分布式统一**：借鉴大系统理论，实现局部自主与全局协同。
  6. **全生命周期统一**：规划考虑可控性，设计嵌入控制需求，建设预留感知执行。

---

## 第三部分：智慧水利的历史、现状与挑战

### 3.1 演进阶段：从信息化到智能化
1. **水利信息化**：解决“看不见”，核心是SCADA和传感器。
2. **数字水利**：解决“看不懂”，核心是数学模型和GIS。
3. **智慧水利**：解决“管不好”，核心是AI、CHS和自主运行。

### 3.2 中国智慧水利现状
- **政策驱动**：2019年《智慧水利总体方案》[36]，2021年提出“数字孪生流域”，2023年《国家水网建设规划纲要》[37]。
- **重大工程**：南水北调中线自动化调度、三峡梯级联合调度。钮新强院士主持了南水北调中线设计，解决了大量关键技术难题 [38]。王浩院士提出“自然-社会”二元水循环理论，为智慧水利提供了水文学基础 [39]。

### 3.3 市场格局与挑战
- **四类玩家**：设计院/科研院所、传统IT集成商、新兴AI巨头、细分领域“小巨人”。
- **核心挑战**：数据孤岛、重建设轻运行、理论实践脱节、复合型人才稀缺。

### 3.4 国际视野
- **荷兰**：精细化管理，3Di模型应用 [40]。
- **新加坡**：PUB构建的全流程闭环智能水网 [41]。
- **以色列**：极致的水资源利用效率与市场化驱动。

---

## 第四部分：未来展望

### 4.1 从“辅助决策”到“自主运行”
未来目标是实现水系统的自主运行（Autonomous Operation）。

#### 4.1.1 水系统自主运行水平（WSAL）分级
参考自动驾驶，提出WSAL L0-L5分级：
- **L0-L2**：人工主导，系统辅助。
- **L3**：有条件自主（如正常工况下的渠道恒水位控制）。
- **L4**：高度自主（人类作为领航员，系统处理复杂扰动）。
- **L5**：完全自主（理想状态）。

#### 4.1.2 Physical AI 与 Cognitive AI 的融合
- **Cognitive AI**：负责感知、预测、自然语言交互（如LLM）。
- **Physical AI**：负责具身智能、闭环控制、改变物理状态。
两者的融合是迈向L4的关键。

### 4.2 学科建设方向
1. **课程体系**：涵盖系统科学、控制、AI、水力学。
2. **教材建设**：编写基于CHS框架的权威教材。
3. **实验平台**：建设虚实结合的“水系统运行”在环测试（HIL）平台。
4. **人才培养**：培养懂水利、懂IT、懂控制的“π”型人才。

---

## 参考文献

[1] Bertalanffy, L. von. (1945). Zu einer allgemeinen Systemlehre. *Blätter für deutsche Philosophie*, 18.
[2] Bertalanffy, L. von. (1968). *General System Theory: Foundations, Development, Applications*. George Braziller.
[3] Prigogine, I. (1978). Time, structure, and fluctuations. *Science*, 201(4358), 777-785.
[4] Holland, J. H. (1995). *Hidden Order: How Adaptation Builds Complexity*. Addison-Wesley.
[5] Wiener, N. (1948). *Cybernetics: Or Control and Communication in the Animal and the Machine*. MIT Press.
[6] Ziegler, J. G., & Nichols, N. B. (1942). Optimum settings for automatic controllers. *Transactions of the ASME*, 64, 759-768.
[7] Kalman, R. E. (1960). A New Approach to Linear Filtering and Prediction Problems. *Journal of Basic Engineering*, 82(1), 35-45.
[8] Bellman, R. (1957). *Dynamic Programming*. Princeton University Press.
[9] Mesarovic, M. D., Macko, D., & Takahara, Y. (1970). *Theory of Hierarchical, Multilevel, Systems*. Academic Press.
[10] Siljak, D. D. (1978). *Large-Scale Dynamic Systems: Stability and Structure*. North-Holland.
[11] Richalet, J., et al. (1978). Model predictive heuristic control: Applications to industrial processes. *Automatica*, 14(5), 413-428.
[12] Cutler, C. R., & Ramaker, B. L. (1980). Dynamic matrix control—a computer control algorithm. *Joint Automatic Control Conference*.
[13] Rawlings, J. B., & Mayne, D. Q. (2009). *Model Predictive Control: Theory, Computation, and Design*. Nob Hill Publishing.
[14] Zadeh, L. A. (1965). Fuzzy sets. *Information and Control*, 8(3), 338-353.
[15] Wooldridge, M. (2009). *An Introduction to MultiAgent Systems*. John Wiley & Sons.
[16] Shortliffe, E. H. (1976). *Computer-Based Medical Consultations: MYCIN*. Elsevier.
[17] Rumelhart, D. E., Hinton, G. E., & Williams, R. J. (1986). Learning representations by back-propagating errors. *Nature*, 323, 533-536.
[18] Vaswani, A., et al. (2017). Attention is all you need. *NIPS*.
[19] Sutton, R. S., & Barto, A. G. (2018). *Reinforcement Learning: An Introduction*. MIT Press.
[20] Lee, E. A. (2008). Cyber-Physical Systems: Design Challenges. *ISORC*.
[21] UNESCO. (2000). *Mount Qingcheng and the Dujiangyan Irrigation System*.
[22] Mays, L. W. (2010). *Ancient Water Technologies*. Springer.
[23] Saint-Venant, A. J. C. (1871). Théorie du mouvement non permanent des eaux. *Comptes Rendus*.
[24] Manning, R. (1891). On the flow of water in open channels and pipes. *Transactions of the ICEI*.
[25] Cunge, J. A., et al. (1980). *Practical Aspects of Computational River Hydraulics*. Pitman.
[26] Abbott, M. B. (1991). *Hydroinformatics: Information Technology and the Aquatic Environment*. Avebury Technical.
[27] Yeh, W. W.-G. (1985). Reservoir management and operations models: A state-of-the-art review. *Water Resources Research*.
[28] Labadie, J. W. (2004). Optimal operation of multireservoir systems: State-of-the-art review. *JWRPM*.
[29] Loucks, D. P., & van Beek, E. (2017). *Water Resources Systems Planning and Management*. Springer.
[30] Burt, C. M., & Styles, S. W. (1999). *Modern water control and management practices in irrigation*. FAO.
[31] Clemmens, A. J., & Kacerek, T. F. (1998). Test Cases for Canal Control Algorithms. *JIDE*.
[32] Litrico, X., & Fromion, V. (2009). *Modeling and Control of Hydrosystems*. Springer.
[33] Malaterre, P. O. (1998). PILOTE: Linear quadratic optimal controller for irrigation canals. *JIDE*.
[34] van Overloop, P. J. (2006). *Model Predictive Control on Open Water Systems*. IOS Press.
[35] 雷晓辉, 等. (2025). 水系统控制论：提出背景、技术框架与研究范式. *南水北调与水利科技*.
[36] 水利部. (2019). *智慧水利总体方案*.
[37] 中共中央, 国务院. (2023). *国家水网建设规划纲要*.
[38] Niu, X. (2022). The first stage of the middle-line south-to-north water-transfer project. *Engineering*.
[39] 王浩, 等. (2023). 流域“自然—社会”二元水循环与水资源研究. *地理学报*.
[40] Nelen & Schuurmans. (2020). *3Di Water Management Whitepaper*.
[41] PUB Singapore. (2021). *Smart Water Grid Roadmap*.
[42] Prigogine, I., & Stengers, I. (1984). *Order out of Chaos*. Bantam Books.
[43] Holland, J. H. (1975). *Adaptation in Natural and Artificial Systems*. University of Michigan Press.
[44] Anderson, P. W. (1972). More is different. *Science*.
[45] Mesarovic, M. D. (1960). *The Control of Multivariable Systems*. MIT Press.
[46] Åström, K. J., & Hägglund, T. (1995). *PID Controllers: Theory, Design, and Tuning*. ISA.
[47] Garcia, C. E., et al. (1989). Model predictive control: Theory and practice—a survey. *Automatica*.
[48] Minsky, M., & Papert, S. (1969). *Perceptrons*. MIT Press.
[49] LeCun, Y., et al. (1998). Gradient-based learning applied to document recognition. *Proc. IEEE*.
[50] Hochreiter, S., & Schmidhuber, J. (1997). Long short-term memory. *Neural Computation*.
[51] Jennings, N. R. (2000). On agent-based software engineering. *AI*.
[52] Shoham, Y., & Leyton-Brown, K. (2008). *Multiagent Systems*. Cambridge University Press.
[53] Price, R. K., & Vojinović, Z. (2011). *Urban Hydroinformatics*. IWA Publishing.
[54] Savic, D. A., & Walters, G. A. (1997). Genetic algorithms for least-cost design of water distribution networks. *JWRPM*.
[55] Farmani, R., et al. (2005). Evolutionary multi-objective optimization in water distribution network design. *Engineering Optimization*.
[56] Schuurmans, J., et al. (1999). Modeling of irrigation and drainage canals for controller design. *JIDE*.
[57] Nash, J. E. (1960). A unit hydrograph study. *Proc. ICE*.
[58] Wurbs, R. A. (1993). Reservoir-system simulation and optimization models. *JWRPM*.
[59] Celeste, A. B., & Billib, M. (2009). Evaluation of stochastic reservoir operation optimization models. *Advances in Water Resources*.
[60] 水利部. (2021). *关于大力推进智慧水利建设的指导意见*.
[61] 水利部. (2022). *数字孪生流域建设技术大纲（试行）*.
[62] 钱学森. (1954). *Engineering Cybernetics*. McGraw-Hill.
[63] Zames, G. (1981). Feedback and optimal sensitivity. *IEEE TAC*.
[64] Clarke, D. W., et al. (1987). Generalized predictive control. *Automatica*.
[65] McCarthy, J., et al. (1955). *A Proposal for the Dartmouth Summer Research Project on AI*.
[66] Abbott, M. B., & Minns, A. W. (1998). *Computational Hydraulics*. Ashgate.
[67] Yeh, W. W.-G. (1982). Optimization of real-time reservoir operation. *Water Resources Research*.
[68] Labadie, J. W. (1988). *Dynamic Programming with Applications in Water Resources*.
[69] Loucks, D. P., et al. (1981). *Water Resource Systems Planning and Analysis*. Prentice Hall.
[70] Burt, C. M. (1988). *Canal Control Training Manual*. ITRC.
[71] Clemmens, A. J. (1994). *Feedback Control for Canal Systems*. USDA.
[72] Litrico, X. (2002). *Modeling and Control of Irrigation Canals*. PhD Thesis.
[73] Malaterre, P. O. (1994). *PILOTE: A Linear Quadratic Optimal Controller for Irrigation Canals*. PhD Thesis.
[74] van Overloop, P. J., et al. (2010). Multiple-model predictive control on a canal. *Control Engineering Practice*.
[75] Rubicon Water. (2020). *Total Channel Control Technology Overview*.
[76] 王浩. (2014). *中国水问题与水战略*. 科学出版社.
[77] 雷晓辉. (2022). *自主运行水网：内涵、技术挑战与发展路径*. 水利水电技术.
[78] 雷晓辉. (2023). *从自动驾驶到自主运行水网：跨领域自主运行简史*.
[79] 雷晓辉. (2023). *水系统运行科学与工程：一个新学科的诞生*.
[80] 雷晓辉. (2023). *智慧水利市场的“四类玩家”与破局之路*.
[81] 雷晓辉. (2023). *水利行业体制机制改革：智慧水利发展的深层动力*.
[82] 雷晓辉. (2023). *水利信息化：从“看不见”到“看得懂”再到“管得好”*.
[83] Mesarovic, M. D., & Takahara, Y. (1975). *General Systems Theory: Mathematical Foundations*. Academic Press.
[84] Prigogine, I. (1980). *From Being to Becoming*. W. H. Freeman.
[85] Holland, J. H. (1998). *Emergence: From Chaos to Order*. Addison-Wesley.
[86] Wiener, N. (1950). *The Human Use of Human Beings*. Houghton Mifflin.
[87] Kalman, R. E. (1963). Mathematical description of linear dynamical systems. *SIAM Journal on Control*.
[88] Bellman, R. (1961). *Adaptive Control Processes: A Guided Tour*. Princeton University Press.
[89] Zadeh, L. A. (1973). Outline of a new approach to the analysis of complex systems. *IEEE TSMC*.
[90] Rumelhart, D. E., & McClelland, J. L. (1986). *Parallel Distributed Processing*. MIT Press.
[91] LeCun, Y., et al. (2015). Deep learning. *Nature*.
[92] Silver, D., et al. (2016). Mastering the game of Go with deep neural networks and tree search. *Nature*.
[93] Vaswani, A., et al. (2017). Attention is all you need. *Advances in Neural Information Processing Systems*.
[94] Abbott, M. B. (1999). Introducing hydroinformatics. *Journal of Hydroinformatics*.
[95] Savic, D. A. (2002). Hydroinformatics: the next generation. *Journal of Hydroinformatics*.
[96] Price, R. K. (2003). Hydroinformatics: a new discipline? *Journal of Hydroinformatics*.
[97] Yeh, W. W.-G. (1985). Reservoir management and operations models. *Water Resources Research*.
[98] Labadie, J. W. (2004). Optimal operation of multireservoir systems. *JWRPM*.
[99] Loucks, D. P. (2000). Sustainable water resources management. *Water International*.
[100] Burt, C. M., & Piao, X. (2002). *Advances in Canal Automation*. ITRC.
[101] Clemmens, A. J., et al. (2005). Canal automation for irrigation districts. *JIDE*.
[102] Litrico, X., et al. (2007). Modeling and control of an irrigation canal. *IEEE Control Systems Magazine*.
[103] Malaterre, P. O., et al. (2014). *Canal Control Algorithms*. INRAE.
[104] van Overloop, P. J. (2006). *Model Predictive Control on Open Water Systems*. IOS Press.
[105] Rubicon Water. (2022). *Case Study: Coleambally Irrigation District*.
[106] 雷晓辉. (2025). *水系统控制论：理论与实践*. 科学出版社 (待出版).
