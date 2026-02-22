## 术语表 Glossary

> 本表收录全书核心术语的中英文对照和简要定义，按英文字母排序。正文中术语首次出现时已标注英文。
> *This glossary lists core terms used throughout the book in Chinese-English bilingual format, sorted alphabetically by English. Terms are annotated in English at their first occurrence in the main text.*

| 序号 | 英文 | 中文 | 定义 |
|:----:|:-----|:-----|:-----|
| 1 | CBF (Control Barrier Function) | 控制障碍函数 | 一种通过构造安全集不变性来保证系统状态始终不超出安全约束的控制方法 |
| 2 | CHS (Cybernetics of Hydro Systems) | 水系统控制论 | 以控制论为核心、系统科学为认识论、AI为赋能的水系统运行理论框架 |
| 3 | CPS (Cyber-Physical System) | 信息-物理系统 | 计算、通信和物理过程深度融合的工程系统 |
| 4 | Digital Twin | 数字孪生 | 物理系统的高保真虚拟映射，实时同步、双向交互、持续演化 |
| 5 | DMA (District Metered Area) | 独立计量分区 | 将供水管网划分为可独立计量的区域以进行漏损管理 |
| 6 | DMPC (Distributed MPC) | 分布式模型预测控制 | 将大规模系统分解为子系统，各子系统的MPC控制器通过信息交互实现协调优化 |
| 7 | EMS (Engineering Management System) | 工程管理系统 | 水利工程运行管理系统，按代际从第一代（人工）到第五代（自主）演进 |
| 8 | Hando Model (瀚铎水网大模型) | 瀚铎水网大模型 | 基于大语言模型技术构建的水网领域专用认知AI系统 |
| 9 | HIL (Hardware-in-the-Loop) | 硬件在环测试 | 将真实控制器硬件接入仿真环境进行集成测试 |
| 10 | HydroOS | 水网操作系统 | 水网领域的通用软件平台，提供数据/模型/控制/智能/验证五大核心服务 |
| 11 | IDZ (Integrator Delay Zero) | 积分-延迟-零点模型 | 渠池传递函数（transfer function，描述系统输入-输出关系的数学模型，如闸门开度变化到下游水位响应之间的关系）的三参数简化模型，兼顾精度与实时性 |
| 12 | MAS (Multi-Agent System) | 多智能体系统 | 多个自主智能体通过交互协作完成复杂任务的系统架构 |
| 13 | MIL (Model-in-the-Loop) | 模型在环测试 | 在纯软件仿真环境中验证控制算法的正确性 |
| 14 | MPC (Model Predictive Control) | 模型预测控制 | 基于系统模型预测未来状态、在线优化控制输入的闭环（closed-loop，控制系统通过传感器实时获取输出反馈、自动调整控制动作的运行方式——与人工凭经验调度的开环（open-loop，控制系统不利用输出反馈、仅按预设规则执行的方式，如按固定调度图操作闸门）方式相对）控制方法 |
| 15 | MRC (Minimal Risk Condition) | 最小风险状态 | 系统在超出ODD或检测到故障时应自动进入的安全状态 |
| 16 | ODD (Operational Design Domain) | 运行设计域 | 自主系统正常工作的环境和工况条件边界 |
| 17 | PIL (Plant-in-the-Loop) | 实体在环测试 | 在真实工程环境中以"影子模式"或受控模式验证控制系统 |
| 18 | Safety Envelope | 安全包络 | 多维状态约束的在线监测和保护机制，确保系统状态不超出安全域 |
| 19 | Saint-Venant Equations | 圣维南方程（Saint-Venant equations，描述明渠水流运动的基本方程，由连续性方程和动量方程组成）组 | 描述明渠非恒定流的基本偏微分方程组（连续性+动量守恒） |
| 20 | SCADA | 数据采集与监控系统 | Supervisory Control And Data Acquisition的缩写，工业过程监控的标准系统 |
| 21 | SIL (Software-in-the-Loop) | 软件在环测试 | 在真实软件栈上验证控制算法的运行时序和异常处理 |
| 22 | SNWDP | 南水北调工程 | South-to-North Water Diversion Project，中国最大的跨流域调水工程 |
| 23 | TCC (Total Channel Control) | 全面渠道控制 | 澳大利亚Rubicon Water公司的灌区自动化解决方案 |
| 24 | WSAL (Water-network Self-driving Autonomy Level) | 水网自主等级 | L0-L5六级分级体系，描述水网从人工操控到完全自主的能力等级 |
| 25 | xIL (X-in-the-Loop) | 在回路测试 | MIL/SIL/HIL/PIL四层渐进验证体系的统称 |

> **中国水利特有概念补注** *Notes on China-specific Water Engineering Concepts*
>
> | 中文名称 | 英文 | 说明 |
> |:---------|:-----|:-----|
> | 南水北调 | South-to-North Water Diversion Project (SNWDP) | 世界最大跨流域调水工程，含东线（运河提水）、中线（自流渠道1432km）和规划中的西线 |
> | 胶东调水 | Jiaodong Water Diversion Project | 山东省大型跨流域调水工程，向青岛、烟台、威海等城市供水 |
> | 引江济淮 | Yangtze-to-Huai River Water Diversion | 安徽省大型调水工程，引长江水补给淮河流域 |
> | 重建轻管（emphasis on construction over operation, a structural problem in China's water sector where investment heavily favors new infrastructure over operational management） | "Emphasis on construction over operation" | 中国水利行业的结构性问题——大量投资用于新建工程，运行管理投入严重不足 |
> | 数字孪生流域 | Digital Twin River Basin | 中国水利部推动的水利信息化战略，要求重要流域建立数字孪生 |
> | 水利部 | Ministry of Water Resources (MWR) | 中国政府负责水利行政管理的部级机构 |
