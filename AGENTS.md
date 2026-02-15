# CHS教材与专著体系 — AI辅助持续写作系统 (CLAUDE.md)

> **版本**: 1.0  
> **创建**: 2026-02  
> **维护**: 雷晓辉  
> **定位**: 本文件是Claude Code / Claude Web协助CHS教材写作的**主控提示词**

---

## 0. 快速启动

### 两个核心命令

| 命令 | 作用 | 示例 |
|------|------|------|
| `开始BK[编号]` | 启动某本书的写作/续写 | `开始BKT2a` `开始BKM1` |
| `继续` | 在当前书的当前章继续写作 | `继续` |

### 启动时Claude必须执行的动作

收到 `开始BK[X]` 后：
1. 定位§2中该书的完整规格
2. 检查 `progress/BK[X].json` 确认已完成章节
3. 定位下一个待写章节
4. 读取§5术语表、§6质量标准
5. 如有前序章节，读取最后500字用于衔接
6. 开始写作，完成后自动进入四角色评审（§7）
7. 评审通过后更新进度文件，提示"输入`继续`进入下一章"

收到 `继续` 后：
1. 读取当前书的进度文件
2. 定位下一待写章节
3. 执行写作→评审→更新循环

---

## 1. 项目总览

### 1.1 体系架构

CHS教材体系共16本书 + 2套配套教辅，分四个层级：

| 层级 | 书目 | 数量 |
|------|------|------|
| 第一层·种子 | T1-CN, T1-EN | 2本 |
| 第二层·骨架 | T2a-CN, T2a-EN, T2b-CN, T2b-EN | 4本 |
| 第三层·血肉 | M1-M8 (各含中英文版) | 8本 |
| 第四层·生态 | M9, M10 | 2本 |

### 1.2 与论文/专利体系的映射

| 书目 | 对应CHS论文族群 | 对应专利族群 |
|------|----------------|-------------|
| T2a (建模与控制) | P1a-P1c 理论基础线 | PF1-PF3 |
| T2b (智能与自主) | P2a-P5c 实验与算法线 | PF4-PF7 |
| M1 明渠降阶建模 | P1a, P2a | PF1 |
| M2 水网预测控制 | P2b, P3a | PF2 |
| M3 水网运行安全包络 | P2c, P3b | PF3 |
| M4 水网多智能体系统 | P3c, P4a | PF4 |
| M5 水利认知智能 | P4b, P4c | PF5 |
| M6 水网控制在环验证 | P5a, P5b | PF6 |
| M7 HydroOS设计与实现 | P5c | PF7 |
| M8 胶东调水与沙坪水电站 | P5a-P5c (工程应用) | PF1-PF7综合 |

### 1.3 GitHub仓库结构

```
CHS-Books/
├── CLAUDE.md                  ← 本文件
├── progress/                  ← 各书进度追踪
│   ├── BKT1-CN.json
│   ├── BKT2a.json
│   ├── BKM1.json
│   └── ...
├── terminology/               ← 术语规范
│   ├── glossary_cn.md         ← 中文术语表
│   ├── glossary_en.md         ← 英文术语表
│   └── symbols.md             ← 统一符号表
├── books/                     ← 各书稿件
│   ├── T1-CN/
│   │   ├── ch01.md
│   │   ├── ch02.md
│   │   └── ...
│   ├── T2a/
│   ├── M1/
│   └── ...
├── figures/                   ← 统一图库
│   ├── fig_specs.md           ← 图表规格清单
│   └── generated/
├── references/                ← 参考文献
│   ├── master_bib.bib         ← 全体系主文献库
│   └── self_citations.md      ← 自引文献清单
└── reviews/                   ← 评审记录
    ├── BKT1-CN_ch01_r1.md
    └── ...
```

---

## 2. 全部书目规格

### T1-CN 《水系统控制论》（中文先导版）

- **出版社**: 中国水利水电出版社
- **页数**: 150-200页（约12-15万字）
- **读者**: 水利行业工程师、管理者、研究生入门
- **语言**: 中文
- **章节结构** (8章):

| 章 | 标题 | 字数 | 核心内容 |
|----|------|------|---------|
| ch01 | 绪论：水系统面临的控制挑战 | 1.5万 | 全球水利基础设施现状；从人工调度到自主运行的范式转变；CHS学科定位 |
| ch02 | 控制论视角下的水系统 | 2万 | 水系统作为被控对象的特性；反馈、前馈、多变量；与经典控制论的关系；钱学森《工程控制论》传承 |
| ch03 | 水系统控制论八原理 | 2万 | 八原理的逐一阐述：传递函数化、可控可观性、分层分布式、安全包络、在环验证、认知增强、人机共融、自主演进 |
| ch04 | 水网自主等级（WNAL L0-L5） | 1.5万 | 六级自主分级体系；与自动驾驶SAE分级的类比和差异；ODD定义 |
| ch05 | 核心技术架构概览 | 2万 | HydroOS三层架构；物理AI引擎与认知AI引擎；SCADA+MAS融合架构；瀚铎水网大模型 |
| ch06 | 关键工程实践 | 2万 | 胶东调水SCADA+HDC实践；沙坪水电站发电-泄洪一体化智能控制；国际案例简述 |
| ch07 | 学科前景与人才培养 | 1万 | CHS作为新学科方向；四支柱课程体系；国际合作与IAHR平台 |
| ch08 | 结语与展望 | 0.5万 | 从SCADA到自主的十年路线图 |

- **写作风格**: 面向行业的科普+学术混合体，每章开头有引导性案例，数学公式控制在最低限度，多用示意图和对比表。

---

### T1-EN *Cybernetics of Hydro Systems: Principles and Perspectives*

- **出版社**: IAHR Water Monograph (CRC Press/Balkema), Open Access
- **页数**: 100-150页（约5-8万词）
- **读者**: 国际水利/控制/AI交叉领域学者
- **语言**: English
- **章节结构** (6章):

| Ch | Title | Words | Core Content |
|----|-------|-------|-------------|
| ch01 | Introduction: The Control Challenge in Water Systems | 8k | Global water infrastructure; paradigm shift from manual to autonomous; CHS positioning |
| ch02 | Theoretical Foundations | 12k | Eight Principles of CHS; transfer-function formulation; controllability/observability for hydraulic systems; safety envelope concept |
| ch03 | Architecture of Autonomous Water Networks | 12k | WNAL L0-L5; HydroOS three-tier architecture; SCADA+MAS fusion; Physical AI & Cognitive AI engines |
| ch04 | Verification and Validation Framework | 10k | SIM-SIL-HIL pipeline; ODD-based testing; runtime monitoring |
| ch05 | Case Studies | 8k | Jiaodong Water Transfer (open-channel HDC); Shaoping Hydropower (generation-flood integrated control); international benchmarks |
| ch06 | Perspectives and Research Agenda | 5k | Open problems; IAHR community building; curriculum framework |

- **写作风格**: Academic English, formal but accessible; follow IAHR Monograph formatting guidelines; each chapter opens with a key insight box; equations formatted in LaTeX.

---

### T2a 《水系统控制论：建模与控制》（研究生核心教材·上册）

- **出版社**: CN=高等教育出版社 / EN=Springer (Advances in Industrial Control)
- **页数**: 400-500页（约40-50万字）
- **读者**: 水利/控制/计算机方向研究生
- **语言**: 中文为主，英文版独立编写
- **章节结构** (16章):

| 章 | 标题 | 字数 | 核心内容 | 对应论文/专利 |
|----|------|------|---------|-------------|
| ch01 | 导论 | 2万 | CHS学科框架；八原理概述；本书结构导读 | P1a §1-2 |
| ch02 | 明渠水动力学基础 | 3万 | Saint-Venant方程推导；特征线法；线性化；传递函数 | P1a §3, PF1-1 |
| ch03 | 管网水力学基础 | 3万 | 管网稳态方程；水锤瞬变流；传递矩阵法 | P1a §4, PF1-2 |
| ch04 | 水系统降阶建模 | 3万 | Muskingum-Cunge; IDZ模型; 频率域辨识; 数据驱动降阶 | M1全书, PF1-3/4/5 |
| ch05 | 经典控制方法 | 3万 | PID/PI; 前馈-反馈; 解耦控制; 频域设计; Bode/Nyquist应用 | P2a §3 |
| ch06 | 现代控制方法 | 3.5万 | 状态空间; LQR/LQG; 鲁棒控制(H∞); 自适应控制 | P2a §4 |
| ch07 | 模型预测控制（MPC） | 4万 | MPC原理; 约束处理; 线性MPC; 非线性MPC; 分布式MPC | M2全书, PF2-1/2/3 |
| ch08 | 优化理论与方法 | 3万 | 线性/非线性规划; 多目标优化; 随机优化; 进化算法 | P2b §3-4 |
| ch09 | 水系统可控性与可观性 | 2.5万 | 可控性分析; 可观性分析; 传感器/执行器布局优化 | P1a §5, PF1-6 |
| ch10 | 安全约束与安全包络 | 3万 | 安全包络形式化; 红/黄/绿三区间; 运行设计域(ODD); 安全联锁 | M3全书, PF3-1/2/3 |
| ch11 | 水系统状态估计与数据融合 | 2.5万 | Kalman滤波; 扩展/无迹KF; 粒子滤波; 传感器故障检测 | P2c §3, PF3-4 |
| ch12 | 分层分布式控制架构 | 3万 | 分层控制(L0/L1/L2); 协调机制; 信息流设计; HDC实现 | P3c §3, PF4-1/2 |
| ch13 | 数字孪生与仿真平台 | 2.5万 | 数字孪生概念; FMI/FMU封装; 实时仿真; 在线校正 | PF6-1/2, M6 ch1-3 |
| ch14 | 胶东调水工程案例 | 2万 | 工程概况; 水力模型建立; SCADA+HDC控制系统; MIL验证结果 | M8 Part I, PF1-PF3综合 |
| ch15 | 沙坪水电站工程案例 | 2万 | 工程概况; 发电-泄洪一体化; 认知智能+ODD+HDC; 蒲布-深溪沟-镇头-沙坪梯级一键调 | M8 Part II, PF2-PF5综合 |
| ch16 | 总结与展望 | 1万 | 本册回顾; 与下册的衔接; 开放问题 | — |

- **写作规范**: 研究生教材体，每章含学习目标→正文→例题→小结→习题→拓展阅读。数学推导完整但附物理直觉。每章新概念≤10个，每个概念至少配1个例题。

---

### T2b 《水系统控制论：智能与自主》（研究生核心教材·下册）

- **出版社**: CN=高等教育出版社 / EN=Springer (Advances in Industrial Control)
- **页数**: 400-500页（约40-50万字）
- **读者**: 水利/控制/计算机方向研究生
- **章节结构** (14章):

| 章 | 标题 | 字数 | 核心内容 | 对应论文/专利 |
|----|------|------|---------|-------------|
| ch01 | 从控制到智能：下册导论 | 1.5万 | 上册回顾; 从模型驱动到数据驱动; AI在水系统中的角色 | — |
| ch02 | 机器学习基础 | 3万 | 监督/无监督/半监督; SVM/RF/GBDT; 交叉验证; 特征工程 | P4a §2-3 |
| ch03 | 深度学习与水系统 | 3.5万 | CNN/RNN/LSTM/Transformer; 时间序列预测; 空间建模; 迁移学习 | P4a §4, PF5-1 |
| ch04 | 物理信息神经网络（PINN） | 3万 | PINN原理; PDE约束; 水动力学PINN; 反问题求解 | P4b §3-4, PF5-2 |
| ch05 | 强化学习与水系统控制 | 3万 | MDP框架; Q-learning/DQN/PPO/SAC; 水网调度RL; 安全强化学习 | P4c §3-4, PF5-3 |
| ch06 | 大语言模型与认知AI | 3万 | LLM架构; RAG; 水利知识图谱; 认知AI引擎; 人机对话调度 | M5全书, PF5-4/5 |
| ch07 | 多智能体系统理论 | 3万 | MAS基础; 共识协议; 博弈论; SCADA+MAS融合架构 | M4全书, PF4-3/4/5 |
| ch08 | 水网自主等级（WNAL） | 2.5万 | L0-L5详细定义; ODD; 最小风险状态; 等级跃迁条件 | P1b §3-4 |
| ch09 | HydroOS水网操作系统 | 3.5万 | 三层架构; 设备抽象层; 调度引擎; API设计; 微服务 | M7全书, PF7-1/2/3/4/5 |
| ch10 | 在环测试与验证 | 3万 | MIL/SIL/HIL; 测试用例设计; 覆盖度度量; 回归测试 | M6全书, PF6-3/4/5 |
| ch11 | 水网信息安全 | 2万 | SCADA安全威胁; 入侵检测; 安全通信; 韧性设计 | P3b §4 |
| ch12 | 胶东调水智能化案例 | 2万 | 在T2a ch14基础上的智能化升级; MAS部署; 在环测试 | M8 Part I续 |
| ch13 | 沙坪水电站智能化案例 | 2万 | 在T2a ch15基础上的认知智能部署; 大模型辅助决策 | M8 Part II续 |
| ch14 | CHS学科展望 | 1.5万 | 水系统运行工程作为新学科; 国际标准化; 十年路线图 | P1c |

---

### M1 《明渠水动力降阶建模》/ *Reduced-Order Modeling of Open-Channel Hydraulics*

- **出版社**: CN=科学出版社 / EN=Springer
- **页数**: 300页（约25万字）
- **章节结构** (10章):

| 章 | 标题 | 字数 |
|----|------|------|
| ch01 | 绪论：为什么需要降阶模型 | 2万 |
| ch02 | Saint-Venant方程与特征线分析 | 3万 |
| ch03 | 传递函数模型 | 3万 |
| ch04 | IDZ (Integrator Delay Zero) 模型 | 2.5万 |
| ch05 | Muskingum类模型及其推广 | 2.5万 |
| ch06 | 频率域辨识方法 | 2.5万 |
| ch07 | 数据驱动降阶方法 | 2.5万 |
| ch08 | 冰期工况降阶建模 | 2万 |
| ch09 | 模型验证与比较框架 | 2万 |
| ch10 | 胶东调水降阶建模实践 | 2.5万 |

---

### M2 《水网预测控制》/ *Predictive Control of Water Networks*

- **出版社**: CN=科学出版社 / EN=Springer AIC
- **页数**: 350页（约30万字）
- **章节结构** (12章):

| 章 | 标题 | 字数 |
|----|------|------|
| ch01 | 绪论 | 2万 |
| ch02 | MPC基本理论 | 3万 |
| ch03 | 线性MPC与明渠控制 | 3万 |
| ch04 | 非线性MPC与管网控制 | 2.5万 |
| ch05 | 分布式MPC架构 | 3万 |
| ch06 | 鲁棒MPC与不确定性处理 | 2.5万 |
| ch07 | 经济型MPC | 2万 |
| ch08 | 自适应MPC与在线学习 | 2.5万 |
| ch09 | MPC与安全约束集成 | 2万 |
| ch10 | MPC实时计算优化 | 2万 |
| ch11 | 胶东调水MPC实践 | 2.5万 |
| ch12 | 沙坪梯级MPC实践 | 2万 |

---

### M3 《水网运行安全包络》/ *Safety Envelope for Water Network Operations*

- **页数**: 250页 | **出版社**: CN=水利水电 / EN=CRC Press

### M4 《水网多智能体系统》/ *Multi-Agent Systems for Water Networks*

- **页数**: 300页 | **出版社**: CN=电子工业 / EN=Springer

### M5 《水利认知智能》/ *Cognitive Intelligence for Water Systems*

- **页数**: 280页 | **出版社**: CN=机械工业 / EN=CRC Press

### M6 《水网控制在环验证》/ *In-the-Loop Verification of Water Network Control*

- **页数**: 250页 | **出版社**: CN=水利水电 / EN=IAHR Book Series

### M7 《水网操作系统：HydroOS设计与实现》/ *HydroOS: Design and Implementation of a Water Network Operating System*

- **页数**: 350页 | **出版社**: CN=科学出版社 / EN=IWA Publishing

### M8 《水利工程自主运行实践——胶东调水与沙坪水电站》/ *Autonomous Operation of Hydraulic Infrastructure: Jiaodong Water Transfer and Shaoping Hydropower Station*

- **出版社**: CN=水利水电 / EN=Springer WSTL
- **页数**: 400页（约35万字）
- **章节结构** (14章):

| 章 | 标题 | 字数 |
|----|------|------|
| ch01 | 绪论：水利工程自主运行的挑战 | 2万 |
| **Part I 胶东调水工程** | | |
| ch02 | 胶东调水工程概况 | 2万 |
| ch03 | 输水明渠水力建模 | 3万 |
| ch04 | SCADA+HDC控制系统设计 | 3万 |
| ch05 | MPC在线优化调度 | 2.5万 |
| ch06 | 在环测试与验证 | 2.5万 |
| ch07 | 运行效果评估 | 2万 |
| **Part II 沙坪水电站** | | |
| ch08 | 大渡河沙坪水电站概况 | 2万 |
| ch09 | 发电-泄洪一体化建模 | 3万 |
| ch10 | 认知智能+ODD+HDC控制设计 | 3万 |
| ch11 | 蒲布-深溪沟-镇头-沙坪梯级一键调 | 3万 |
| ch12 | 认知AI辅助决策系统 | 2.5万 |
| ch13 | 综合效益分析 | 2万 |
| ch14 | 结论与推广前景 | 1.5万 |

**特别注意**：
- 胶东调水是长距离明渠调水工程，核心是明渠SCADA+HDC自主控制
- 沙坪水电站是大渡河梯级水电枢纽，核心是发电和泄洪一体化智能控制
- 两者不可混淆——前者是调水工程，后者是水电站
- 沙坪的"一键调"指蒲布-深溪沟-镇头-沙坪梯级联合调度，不是沙坪单站

---

### M9 《水系统运行工程导论》/ *Introduction to Water Systems Operations Engineering*

- **出版社**: CN=高等教育出版社 / EN=Cambridge UP
- **页数**: 300页
- **读者**: 本科高年级（门户教材）
- **特殊要求**: 前置知识仅要求大学物理+高等数学+流体力学基础；数学推导最少化；大量案例和图表

### M10 《水网智能控制实验》/ *Laboratory Manual for Intelligent Water Network Control*

- **出版社**: CN=高等教育出版社
- **页数**: 200页
- **特殊要求**: 配合M9使用；每个实验含目的→原理→步骤→数据记录表→思考题；基于HydroOS教学版

---

## 3. 写作优先级与批次

### 第一批（2026Q2-2027Q2）：立旗

| 优先级 | 书目 | 目标完稿 | 说明 |
|--------|------|---------|------|
| ★★★★★ | T1-CN | 2026Q4 | 中文先导版，最先启动 |
| ★★★★★ | T1-EN | 2026Q4 | IAHR Monograph，同步启动 |

### 第二批（2027Q1-2028Q4）：骨架

| 优先级 | 书目 | 目标完稿 |
|--------|------|---------|
| ★★★★☆ | T2a-CN/EN | 2028Q2 |
| ★★★★☆ | M9 | 2028Q1 |
| ★★★☆☆ | T2b-CN/EN | 2028Q4 |

### 第三批（2028-2030）：血肉

| 优先级 | 书目 | 目标完稿 |
|--------|------|---------|
| ★★★☆☆ | M1 → M2 → M7 → M8 | 每6个月1-2本 |
| ★★☆☆☆ | M3 → M4 → M5 → M6 | 2030年底前 |
| ★★☆☆☆ | M10 | 2030 |

---

## 4. 作者信息

### 第一作者/主编

**雷晓辉** 教授  
- 河北工程大学学术副校长  
- IAHR Water Systems Operation Working Group 创始主席  
- 二级教授，国家万人计划  
- 清华大学水利水电工程学士（1993-1998），中国水科院硕士（导师王浩院士），日本筑波大学博士（导师前川孝昭教授）
- 200+论文（150篇SCI），60件专利，10部专著，30+软著  
- 主持两项国家重点研发计划（南水北调东线/中线）

### 核心概念署名

- **水系统控制论（CHS）**: 雷晓辉原创理论框架
- **HydroOS**: 雷晓辉原创水网操作系统
- **瀚铎水网大模型**: 雷晓辉主持开发
- **WNAL (Water Network Autonomy Levels)**: 雷晓辉原创分级体系
- **EMS五代框架**: 雷晓辉提出

---

## 5. 术语规范

### 5.1 核心术语表（中英文严格对应）

| 中文规范 | English Standard | 禁止别名 |
|---------|-----------------|---------|
| 水系统控制论 | Cybernetics of Hydro Systems (CHS) | ❌水控制学、水系统论、水网控制学 |
| 水网自主等级 | Water Network Autonomy Levels (WNAL) | ❌水网自动化等级、水利自主等级 |
| 运行设计域 | Operational Design Domain (ODD) | ❌操作设计域、运行设计范围 |
| 安全包络 | Safety Envelope | ❌安全边界（可用但不作术语）、安全域 |
| 物理AI引擎 | Physical AI Engine | ❌物理引擎（歧义）、机理模型引擎 |
| 认知AI引擎 | Cognitive AI Engine | ❌知识引擎、决策引擎 |
| 分层分布式控制 | Hierarchical Distributed Control (HDC) | ❌分级控制、集散控制 |
| 多智能体系统 | Multi-Agent System (MAS) | ❌多代理系统（在水利语境中） |
| 在环测试 | In-the-Loop Testing | ❌闭环测试（歧义） |
| 水网操作系统 | Water Network Operating System (HydroOS) | ❌水利操作系统、水务OS |
| 瀚铎水网大模型 | HanDuo Water Network Large Model | ❌翰铎（错别字）、瀚铎大模型（缺"水网"） |
| 模型预测控制 | Model Predictive Control (MPC) | ❌预测控制（不完整） |
| 传递函数 | Transfer Function | ❌传递矩阵（不同概念） |
| 降阶模型 | Reduced-Order Model (ROM) | ❌简化模型（不准确） |
| SCADA+MAS融合架构 | SCADA+MAS Fusion Architecture | ❌SCADA/MAS混合（不准确） |

### 5.2 数学符号统一规范

| 符号 | 含义 | 单位 |
|------|------|------|
| $Q$ | 流量 | m³/s |
| $h$ (或 $y$) | 水位/水深 | m |
| $A$ | 过水断面面积 | m² |
| $B$ | 水面宽度 | m |
| $S_0$ | 底坡 | - |
| $S_f$ | 摩阻坡降 | - |
| $n$ | Manning粗糙系数 | s/m^{1/3} |
| $c$ | 波速 | m/s |
| $\tau$ | 传输延时 | s |
| $T_p$ | 预测时域 | s |
| $T_c$ | 控制时域 | s |
| $\mathbf{x}$ | 状态向量 | — |
| $\mathbf{u}$ | 控制输入向量 | — |
| $\mathbf{y}$ | 输出向量 | — |
| $\mathbf{A, B, C, D}$ | 状态空间矩阵 | — |
| $G(s)$ | 传递函数 | — |
| $J$ | 目标函数/代价函数 | — |

### 5.3 全体系交叉引用规范

- 引用本体系其他书目时使用：「参见《水网预测控制》第5章」或「See M2 Ch.5」
- 引用CHS论文时使用：「(Lei et al., 2025a)」格式
- 引用专利时使用：「（专利PF2-3"分布式MPC在线协调方法"）」

---

## 6. 质量标准

### 6.1 教材章节质量清单

每章完成后，Claude必须对照以下检查项逐一验证：

**【结构完整性】**
- [ ] 章首含"学习目标"（3-5条）
- [ ] 章末含"本章小结"（500字以内）
- [ ] 章末含"习题"（基础题≥3 + 应用题≥2 + 思考题≥1）
- [ ] 章末含"拓展阅读"（3-5篇核心文献）
- [ ] 章首回顾前一章关键结论（如非首章）
- [ ] 章末预告下一章内容（如非末章）

**【概念密度】**
- [ ] 本章引入的新概念 ≤ 10个
- [ ] 每个新概念首次出现时有明确定义
- [ ] 每个新概念至少配1个例题或案例
- [ ] 新概念的中英文术语严格遵循§5

**【数学-直觉平衡】**
- [ ] 每个公式推导前有物理直觉说明
- [ ] 每个公式推导后有工程意义解释
- [ ] 复杂推导拆分为可独立理解的步骤
- [ ] 数学符号全部使用§5.2统一规范

**【习题梯度】**
- [ ] 基础题：验证概念理解，有标准答案
- [ ] 应用题：工程计算，需要建模+计算
- [ ] 思考题：开放式探究，无唯一答案

**【图表质量】**
- [ ] 每章至少2张图表
- [ ] 图表编号连续（图X-Y / 表X-Y）
- [ ] 图表有完整标题和说明文字
- [ ] 图表可独立理解（不看正文也能看懂大意）

### 6.2 专著章节质量清单

专著（M1-M8）的质量标准在教材标准基础上增加：

- [ ] 包含最新参考文献（近5年占比≥40%）
- [ ] 包含与国际同类工作的系统对比
- [ ] 包含可复现的数值算例或实验结果
- [ ] 公式推导完整，可供研究生自学

### 6.3 T1系列（先导版）特殊质量标准

- [ ] 无需习题
- [ ] 数学公式最少化（必要公式不超过全文的5%）
- [ ] 每章开头有引导性案例（500字以内）
- [ ] 面向行业读者可独立阅读，无需预备知识

---

## 7. 四角色评审机制

每章初稿完成后，Claude须依次扮演四个角色进行评审：

### Role A：学科教师（Instructor Reviewer）

**评审视角**: 教学可用性  
**检查重点**:
- 知识点覆盖是否完整？与大纲一致？
- 难度梯度是否从易到难？
- 例题质量：是否典型、是否有解题过程、是否与习题衔接？
- 习题难度分布是否合理？
- 一个研究生每周能否消化一章？
- 前后章衔接是否自然？

**输出格式**:
```
[教师评审] BK[X] ch[Y]
- 覆盖度: ★★★★☆ (说明缺失内容)
- 难度梯度: ★★★☆☆ (指出跳跃点)
- 例题质量: ★★★★★
- 习题质量: ★★★☆☆ (建议补充)
- 可教性评分: X/10
- 修改建议: (按优先级列出)
```

### Role B：学科专家（Domain Expert Reviewer）

**评审视角**: 学术准确性  
**检查重点**:
- 理论表述是否准确？有无错误？
- 公式推导是否正确？量纲是否一致？
- 与国际前沿是否对齐？是否遗漏重要文献？
- 自引是否合理？（自引率控制在7-10%）
- 是否有原创性贡献？与已有教材的差异何在？
- 论断是否有文献支撑？

**输出格式**:
```
[专家评审] BK[X] ch[Y]
- 准确性: ★★★★☆ (列出错误/疑问)
- 文献覆盖: ★★★☆☆ (缺失的关键文献)
- 前沿性: ★★★★★
- 原创性: ★★★★☆
- 学术评分: X/10
- 修改建议: (按严重性排序)
```

### Role C：行业工程师（Industry Engineer Reviewer）

**评审视角**: 工程实用性  
**检查重点**:
- 案例是否来自真实工程？参数是否符合实际？
- 技术方案是否可落地？有无工程实施障碍？
- 是否考虑了实际工况的复杂性（如冰期、检修、突发事件）？
- 行业工程师是否看得懂？
- 计算结果是否在工程合理范围？
- 是否有可以直接拿来用的计算公式/参数表/流程图？

**输出格式**:
```
[工程师评审] BK[X] ch[Y]
- 工程真实性: ★★★★☆
- 可落地性: ★★★☆☆ (指出脱离实际之处)
- 可读性: ★★★★★
- 实用性评分: X/10
- 修改建议: (面向工程应用)
```

### Role D：国际读者（International Reader Reviewer）

**评审视角**: 跨文化可达性（仅英文版适用，中文版跳过此角色）  
**检查重点**:
- 术语翻译是否准确、是否符合国际惯例？
- 案例是否具有国际通用性？
- 是否避免了中国特有语境的表达障碍？
- 英文是否流畅、地道？
- 是否符合目标出版社的Style Guide？
- 引用的文献是否以国际文献为主？

**输出格式**:
```
[国际评审] BK[X] ch[Y]
- 术语准确性: ★★★★☆
- 国际通用性: ★★★☆☆
- 英文质量: ★★★★☆
- 国际评分: X/10
- 修改建议: (面向国际读者)
```

### 评审后的修改流程

1. 四角色评审完成后，汇总所有修改建议
2. 按严重性分级：🔴致命（必须修改）→ 🟡重要（应当修改）→ 🟢建议（可选修改）
3. 执行🔴和🟡级修改
4. 再次运行质量检查清单（§6）
5. 通过后更新进度文件

---

## 8. 写作风格指南

### 8.1 教材（T2a/T2b/M9）通用风格

**段落结构**: 每段200-400字，一段一个中心思想。首句为主题句。

**数学公式呈现**:
```
[物理直觉] 水位变化的速度取决于来水量与出水量之差——这正是质量守恒的体现。
[公式] $$\frac{\partial A}{\partial t} + \frac{\partial Q}{\partial x} = q_l$$
[工程解释] 其中左侧第一项是断面面积的时间变化率，第二项是流量沿程变化率，
右侧 $q_l$ 为旁侧入流（如支渠汇入或泵站取水）。对于无旁侧入流的简单渠段，$q_l=0$。
```

**例题格式**:
```
【例X-Y】某明渠渠段长L=10km，设计流量Q₀=50m³/s，底宽B=8m，底坡S₀=0.0001...
[已知] ...
[求解] ...
[解题过程] 分步展示，每步有物理含义说明
[结果讨论] 计算结果是否符合工程经验？物理意义是什么？
```

**避免的写法**:
- ❌ "众所周知..."（读者可能真的不知道）
- ❌ "显然..."（如果显然就不需要教材了）
- ❌ "容易证明..."（容易的话请写出来）
- ❌ 整页公式推导没有一句话解释
- ❌ 多于3个连续公式之间没有文字衔接

### 8.2 先导版（T1-CN/T1-EN）风格

- 语气介于学术论文和科普读物之间
- 每章开头用一个真实场景引入（如："2023年夏季，华北某调水工程面临......"）
- 数学公式仅在绝对必要时出现，且附白话解释
- 大量使用对比表、流程图、架构图

### 8.3 工程案例专著（M8）风格

- 叙事以工程为主线，理论为工具
- 大量使用实际运行数据、截图、照片描述
- 每个技术方案附"实施要点"和"踩过的坑"
- 语气可以略微口语化，接近工程总结报告

---

## 9. 参考文献规范

### 9.1 自引策略

| 场景 | 自引率目标 | 说明 |
|------|-----------|------|
| T1-CN/T1-EN | 10-15% | 先导版需要多引自己的系统性工作 |
| T2a/T2b | 7-10% | 核心教材需要平衡自引和广泛引用 |
| M1-M8 | 5-8% | 专著聚焦特定方向，自引自然偏低 |
| M9 | 3-5% | 本科教材以经典文献为主 |

### 9.2 必引文献（所有书目共享的基础文献库）

**控制论奠基**:
- Wiener, N. (1948). *Cybernetics*
- 钱学森 (1954). *Engineering Cybernetics* / 《工程控制论》

**明渠控制经典**:
- Wylie, E.B. (1969). "Control of transient free-surface flow"
- Buyalski, C.P. (1991). *Canal Systems Automation Manual*
- Litrico, X. & Fromion, V. (2009). *Modeling and Control of Hydrosystems*
- Van Overloop, P.J. (2006). *Model Predictive Control on Open Water Systems*
- ASCE (2014). *MOP 131: Canal Automation for Irrigation Systems*

**CHS核心论文（雷晓辉发表）**:
- Lei 2025a: 理论背景与研究范式 (DOI: 10.13476/j.cnki.nsbdqk.2025.0077)
- Lei 2025b: 自主智能水网架构 (DOI: 10.13476/j.cnki.nsbdqk.2025.0079)
- Lei 2025c: 在环测试系统 (DOI: 10.13476/j.cnki.nsbdqk.2025.0080)
- Lei 2025d: 水资源系统分析学科展望 (DOI: 10.13476/j.cnki.nsbdqk.2025.0078)

**EMS五代框架参考文献** (共93篇，自引7篇=7.5%，国际引用82篇=88%):
- 第一代: Wylie 1969 (最早期)
- 第二代: Buyalski 1991 (SCADA时代)
- 第三代: Van Overloop 2006 (HDC时代)
- 完整文献清单见 `references/master_bib.bib`

---

## 10. 进度追踪

### 进度文件格式

每本书对应一个JSON文件 `progress/BK[X].json`:

```json
{
  "book_id": "T2a",
  "book_title": "水系统控制论：建模与控制",
  "total_chapters": 16,
  "chapters": {
    "ch01": {
      "status": "completed",
      "word_count": 19500,
      "review_passed": true,
      "review_scores": {"A": 8, "B": 9, "C": 7, "D": null},
      "last_updated": "2027-03-15",
      "issues": []
    },
    "ch02": {
      "status": "in_progress",
      "word_count": 15000,
      "review_passed": false,
      "issues": ["缺少IDZ模型例题", "Manning公式推导不完整"]
    },
    "ch03": {
      "status": "pending"
    }
  },
  "overall_progress": "12.5%"
}
```

### 状态定义

| 状态 | 含义 |
|------|------|
| `pending` | 未开始 |
| `in_progress` | 正在写作 |
| `review` | 初稿完成，评审中 |
| `revision` | 评审后修改中 |
| `completed` | 评审通过，定稿 |

---

## 11. 跨书一致性检查

### 11.1 术语一致性

每完成一本书的某章后，Claude需检查：
- 本章使用的所有术语是否与§5.1完全一致
- 本章使用的所有数学符号是否与§5.2完全一致
- 如有新术语/符号引入，是否已更新到统一术语表和符号表

### 11.2 内容一致性

以下内容在多本书中出现，必须保持一致：

| 内容 | 出现在 | 一致性要求 |
|------|--------|-----------|
| 八原理表述 | T1, T2a ch01, M9 ch01 | 原理名称和核心表述完全一致，详略可不同 |
| WNAL L0-L5定义 | T1 ch04, T2b ch08, M8 ch01 | 定义表完全一致 |
| Saint-Venant方程 | T2a ch02, M1 ch02, M8 ch03 | 公式形式和符号完全一致 |
| MPC基本原理 | T2a ch07, M2 ch02, M8 ch05 | 标准表述一致，深度可不同 |
| HydroOS架构 | T1 ch05, T2b ch09, M7 ch02 | 架构图和层级命名一致 |
| 胶东调水概况 | T2a ch14, T2b ch12, M1 ch10, M8 ch02 | 工程参数完全一致 |
| 沙坪水电站概况 | T2a ch15, T2b ch13, M8 ch08 | 工程参数完全一致 |

### 11.3 引用一致性

- 同一参考文献在不同书目中的引用格式完全一致
- 同一自引论文的年份、DOI完全一致
- 跨书引用使用统一格式：「参见《水网预测控制》第5章」

---

## 12. 特殊场景处理

### 12.1 知识超出AI能力范围时

如Claude无法确定某个技术细节的准确性（如特定工程参数、实测数据、专利细节），须：
1. 在正文中标注 `[TODO: 需补充XXX]`
2. 不要编造具体数值
3. 继续写作后续内容，不要因一个TODO停下来

### 12.2 中英文版本差异处理

- 中文版和英文版是**独立写作**，不是逐句翻译
- 英文版可适当增加对中国水利体制的背景解释
- 中文版可适当增加对国际案例的介绍
- 两个版本的核心技术内容必须一致，但案例详略可以不同

### 12.3 与论文写作的协同

- 如某章内容与CHS Full Paper Plan中某篇论文高度重叠，优先引用论文而非重复论文内容
- 教材内容应比论文更详细（含推导过程、例题、习题），但理论主张必须一致
- 如论文尚未发表，教材中的引用格式使用「(Lei et al., forthcoming)」

---

## 13. 图表生成规范

### 13.1 图表编号

- 章内连续编号：图X-1, 图X-2... / 表X-1, 表X-2...
- X = 章号

### 13.2 核心架构图（跨书共享）

以下架构图在多本书中使用，必须保持一致（可有详略差异）：

| 图号 | 名称 | 使用书目 |
|------|------|---------|
| ARCH-01 | CHS八原理关系图 | T1, T2a, M9 |
| ARCH-02 | WNAL L0-L5阶梯图 | T1, T2b, M8 |
| ARCH-03 | HydroOS三层架构图 | T1, T2b, M7 |
| ARCH-04 | SCADA+MAS融合架构图 | T2a, T2b, M4 |
| ARCH-05 | 物理AI+认知AI双引擎图 | T1, T2a, T2b |
| ARCH-06 | SIM-SIL-HIL在环测试管线图 | T2b, M6 |
| ARCH-07 | 安全包络红/黄/绿三区间图 | T2a, M3 |
| ARCH-08 | 胶东调水工程布置图 | T2a, M1, M8 |
| ARCH-09 | 沙坪梯级系统布置图 | T2a, M8 |

### 13.3 图表描述格式

在Markdown中用以下格式标注需要生成的图表：

```
[图X-Y: 标题]
{描述: 详细描述图表内容、布局、标注要求}
{尺寸: 半页/全页}
{颜色方案: 蓝色系/灰度/自定义}
{对应ARCH编号: ARCH-XX（如有）}
```

---

## 14. 版本控制与协作

### 14.1 文件命名

- 初稿: `books/T2a/ch07_v1.md`
- 评审后修改: `books/T2a/ch07_v2.md`
- 定稿: `books/T2a/ch07_final.md`

### 14.2 变更日志

每次重大修改在文件头部记录：

```markdown
<!-- 变更日志
v2 2027-06-15: 补充分布式MPC例题；修正式(7-12)量纲错误
v1 2027-05-20: 初稿
-->
```

---

## 附录A：完整书目一览表

| 编号 | 中文书名 | English Title | 页数 | 出版社 |
|------|---------|--------------|------|--------|
| T1-CN | 《水系统控制论》 | — | 150-200 | 水利水电 |
| T1-EN | — | *Cybernetics of Hydro Systems: Principles and Perspectives* | 100-150 | IAHR/CRC |
| T2a-CN | 《水系统控制论：建模与控制》 | — | 400-500 | 高教社 |
| T2a-EN | — | *Cybernetics of Hydro Systems: Modeling and Control* | 400-500 | Springer AIC |
| T2b-CN | 《水系统控制论：智能与自主》 | — | 400-500 | 高教社 |
| T2b-EN | — | *Cybernetics of Hydro Systems: Intelligence and Autonomy* | 400-500 | Springer AIC |
| M1 | 《明渠水动力降阶建模》 | *Reduced-Order Modeling of Open-Channel Hydraulics* | 300 | 科学/Springer |
| M2 | 《水网预测控制》 | *Predictive Control of Water Networks* | 350 | 科学/Springer AIC |
| M3 | 《水网运行安全包络》 | *Safety Envelope for Water Network Operations* | 250 | 水利水电/CRC |
| M4 | 《水网多智能体系统》 | *Multi-Agent Systems for Water Networks* | 300 | 电子工业/Springer |
| M5 | 《水利认知智能》 | *Cognitive Intelligence for Water Systems* | 280 | 机械工业/CRC |
| M6 | 《水网控制在环验证》 | *In-the-Loop Verification of Water Network Control* | 250 | 水利水电/IAHR |
| M7 | 《水网操作系统：HydroOS设计与实现》 | *HydroOS: Design and Implementation of a Water Network OS* | 350 | 科学/IWA |
| M8 | 《水利工程自主运行实践——胶东调水与沙坪水电站》 | *Autonomous Operation of Hydraulic Infrastructure* | 400 | 水利水电/Springer WSTL |
| M9 | 《水系统运行工程导论》 | *Introduction to Water Systems Operations Engineering* | 300 | 高教/Cambridge UP |
| M10 | 《水网智能控制实验》 | *Lab Manual for Intelligent Water Network Control* | 200 | 高教社 |
