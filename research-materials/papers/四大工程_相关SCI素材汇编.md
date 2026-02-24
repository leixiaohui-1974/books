# 沙坪、胶东调水、中线、东线江苏水源 — 相关SCI/学术论文素材汇编

> 整理日期：2026年2月24日  
> 作者范围：雷晓辉、王超、王浩及合作者  
> 用途：为书稿相关章节提供文献素材

---

## 一、沙坪工程（大渡河梯级水电）

### 1.1 核心论文

**[S1] 沙坪二级电站水力调控方法研究**
- 作者：李谷涵, 张召, 孔令仲, 雷晓辉, 王艺霖, 颜培儒, 许珂
- 期刊：中国农村水利水电
- 年份：2022, 第(1)期, 页码：196-199,205
- 收稿：2021-04-06，发表：2022-01-15

**内容摘要（基于搜索结果）：**
沙坪二级电站位于四川省乐山市大渡河上，是大渡河22级梯级开发第20级的第二级，总装机348MW（6台×58MW灯泡贯流式机组）。研究背景：珍头坝I～沙坪II段坡陡流急，水力调控研究难度大，此前主要依靠人工经验。方法：采用一维非恒定流数值模拟模型，系统分析水流时滞特性，计算上游流量变化时下游边界的理想流量过程，提出快速计算方法。结果：所提水力调控方法经水动力学模拟验证，控制方法产生的最大水位波动约0.2m，可保障工程安全运行。

**关键词：** 沙坪二级电站、水力调控、一维非恒定流、时滞、大渡河

**书稿应用建议：**
- 可作为CHS理论框架中"梯级水电系统水力控制"的典型案例
- 时滞分析是CHS理论中"水力传播特性"的重要实证
- 体现了从经验调度向科学调控的转变，对应WNAL自主性提升的论述

---

## 二、胶东调水工程（引黄济青/南水北调东线山东段）

### 2.1 核心论文

**[J1] 引黄济青明渠段输水控制系统的MIL测试系统设计与实现**
- 作者：何立新, 曹辰宇, 张峥, 雷晓辉, 李翔
- 期刊：南水北调与水利科技（中英文）
- 年份：2025, 23(01): 1-9+58
- DOI：10.13476/j.cnki.nsbdqk.2025.0001

**内容概述：**
引黄济青（引黄河水济青岛）是胶东地区重要的跨流域调水工程，已运行30余年，是南水北调东线山东段末端的重要组成部分。本文研究引黄济青明渠段输水控制系统的硬件在环（MIL）测试技术，为控制系统的测试与验证提供科学方法。

**关键词：** 引黄济青、明渠调水、控制系统、MIL测试、胶东

---

**[J2] 明渠调水工程渠池自平衡特性及扰动阈值**
- 作者：龙岩, 高伟, 张召, 雷晓辉
- 期刊：南水北调与水利科技（中英文）
- 年份：2025, 23(01): 10-20
- DOI：10.13476/j.cnki.nsbdqk.2025.0002

**内容概述：**
研究明渠调水工程中渠池的自平衡特性，分析扰动条件下渠池水位的自恢复能力，量化扰动阈值，对引水渠道运行安全和自动控制具有重要理论意义。此研究直接支撑CHS理论中关于"渠系自律控制"的论述。

---

**[J3] Real-Time Control Operation Method of Water Diversion Project Based on River Diversion Disturbance**
- 作者：Pengyu Jin, Chao Wang, Jiahui Sun, Xiaohui Lei, Hao Wang
- 期刊：Water (MDPI), 2023, 15(15), 2793
- DOI：10.3390/w15152793
- 开放获取：是（CC BY）

**全文摘要（已获取）：**
研究以水分流（river diversion）扰动为核心问题，针对跨流域调水工程的实时控制运行，构建了五类典型分流扰动条件（C1~C5），设计了基于多渠池积分时延（ID）模型的离散状态空间方程作为预测模型，结合一维水动力模型实时修正系统状态。在不同典型扰动线型下建立模型预测控制（MPC）算法，制定控制闸门和泵站的控制策略。在江淮水资源综合利用工程历史调度数据上验证了方法有效性。**结果**：该方法能更好地应对不同程度的分流扰动，补偿广义模型精度不足带来的控制性能损失，提高水位控制和闸门调节效果。

**关键要点：**
- 五类分流扰动线型（C1增流后恢复、C2突增临时、C3频繁波动、C4减流、C5下游调峰）
- 多渠池积分时延模型：$\frac{dy(t)}{dt} = \frac{1}{A_s}[q_{fa}(t) - q_{out}(t) - q_d(t)]$
- 模型预测控制：滚动优化，仿真步长1h，控制步长2h，预见期72h
- 三层目标：①水位约束保证 ②水位波动最小化 ③梯级泵站高效区运行

**书稿应用建议：**
- 可引用作为"调水工程扰动识别与响应控制"的代表性成果
- 分流扰动分类体系可纳入CHS理论的扰动类型框架
- 多渠池ID模型+MPC控制器的结合，是CHS中"预测-反馈混合控制"的典型实现

---

**[J4] Roughness inversion of water transfer channels from a data-driven perspective**
- 作者：L Zhou, P Yan, Z Han, Z Zhang, X Lei, H Wang
- 期刊：Water, 2023, 15(15), 2822
- DOI：10.3390/w15152822

**内容概述：**
从数据驱动角度研究调水渠道糙率反演问题，对于建立调水渠道精确水力模型具有重要意义，可为胶东调水等工程运行模型参数识别提供支撑。

---

**[J5] A novel IBAS-ELM model for prediction of water levels in front of pumping stations**
- 作者：P Yan, Z Zhang, Q Hou, X Lei, Y Liu, H Wang
- 期刊：Journal of Hydrology, 2023, 616, 128810
- DOI：（J Hydrology 616卷）

**内容概述：**
提出基于改进算法（IBAS）优化的极限学习机（ELM）模型，用于泵站前池水位预测，对于胶东调水和东线泵站优化调度具有实际意义。

---

## 三、南水北调中线工程

### 3.1 核心论文

**[M1] Optimal allocation of water resources in the middle route of south-to-north water diversion project based on multi-regional input-output model**
- 作者：Y Long, Y Liu, T Zhao, Z Zhang, X Lei, Y Yang
- 期刊：Journal of Hydrology, 2024, 637, 131381
- DOI：10.1016/j.jhydrol.2024.131381

**内容概述：**
基于多区域投入产出模型，优化中线工程受水区的水资源配置，分析跨区域水资源分配的经济和社会效益。

---

**[M2] Assessment of the spatiotemporal water quality variations in the Middle Route of China's South-to-North Water Diversion Project**
- 作者：Y Xu, J Lin, X Lei, D Zhang, Q Peng, J Wang, B Zhu
- 期刊：Environmental Science and Pollution Research, 2023, 30(15), 44206-44222
- DOI：（ESPR 30卷）

**内容概述：**
系统评估中线工程水质的时空变化特征，分析影响因素，为水质管理提供科学依据。

---

**[M3] Ecological scheduling of the middle route of south-to-north water diversion project based on a reinforcement learning model**
- 作者（含雷晓辉）：Zhu J, Zhang Z, Lei X, Jing X, Wang H, Yan P
- 期刊：Journal of Hydrology, 2021, 596, 126107
- DOI：10.1016/j.jhydrol.2021.126107

**内容概述：**
将强化学习（RL）方法应用于中线工程生态调度，建立智能调度规则，平衡输水供水与生态流量需求。这是将AI方法引入水网自主运行的重要探索。

**书稿应用建议：**
- 体现了从规则调度到学习型调度的跨越，对应WNAL L3→L4的进化
- RL方法是HydroOS自主决策层的理论基础之一

---

**[M4] Sudden water pollution accidents and reservoir emergency operations: impact analysis at Danjiangkou Reservoir**
- 作者：Hezhen Zheng, Xiaohui Lei, Yizi Shang, Yang Duan, Lingzhong Kong, Yunzhong Jiang, Hao Wang
- 期刊：Environmental Science and Pollution Research（约2017年）
- PubMed ID：28355129

**内容概述：**
建立丹江口水库三维水动力和水质模型，分析突发水污染事故对中线水源地的影响，提出应急管理建议。这是雷晓辉在中线水源水质安全保障方面的重要成果。

---

**[M5] 南水北调中线工程智能调控与应急调度关键技术**
- 作者：王浩, 雷晓辉, 尚毅梓
- 期刊：南水北调与水利科技（中英文）
- 年份：2017, 15(2): 1-8
- 来源：网络搜索确认

**内容概述：**
系统总结中线工程智能调控与应急调度的关键技术，是王浩、雷晓辉团队在中线工程运行管理方面的综合性成果。

---

**[M6] 南水北调中线渠系蓄量补偿运行控制方式**
- 作者：吴辉明，雷晓辉，秦韬，等
- 期刊：南水北调与水利科技
- 年份：2015, 13(4): 788-792+802
- 来源：网络搜索确认

**内容概述：**
研究中线渠系基于蓄量补偿的运行控制方式，为渠系水量平衡和水位控制提供技术支撑。"蓄量补偿"是中线闸群联合控制的核心概念。

---

**[M7] 南水北调中线输水调度实时控制策略**
- 作者：孔令仲，王浩，雷晓辉，权锦，杨迁
- 期刊：水科学进展
- 来源：网络搜索确认

**内容概述：**
研究中线工程实时控制策略，包括前馈和反馈控制的综合运用，是CHS理论中"实时控制决策"的重要实证。

---

**[M8] 多级串联明渠调水工程多目标水位预测控制模型研究**
- 作者：孔令仲, 雷晓辉, 张召, 朱杰, 王浩
- 期刊：水利学报
- 年份：2022
- 来源：网络搜索确认

**内容概述：**
针对多级串联明渠工程建立多目标水位预测控制模型，综合考虑水位稳定性和输水效率，是中线渠系控制研究的代表性成果。

---

## 四、南水北调东线江苏水源工程

### 4.1 核心论文

**[E1] 南水北调东线江苏段典型泵站运行效率模拟模型**
- 作者：杨靖仁, 王超, 雷晓辉, 等
- 期刊：南水北调与水利科技(中英文)
- 年份：2024, 22(2): 388-398
- 来源：网络搜索确认

**内容概述：**
针对东线江苏段典型泵站（如淮安、睢宁、邳州等站），建立运行效率模拟模型，分析影响泵站效率的关键因素，为泵站优化调度提供依据。这是[E2]英文版的中文配套研究。

---

**[E2] Research on efficiency simulation model of pumping stations based on data-driven methods**
- 作者：Xiaohui Lei, Jingren Yang, Chao Wang, HE Zhongzheng, Qiaoyin Liu
- 期刊：Energy Reports, 2024, Vol.12, 2773-2785
- DOI：10.1016/j.egyr.2024.xx
- ScienceDirect URL：https://www.sciencedirect.com/science/article/pii/S2352484724005389

**详细内容（基于搜索结果）：**
研究背景：泵站机组运行效率受多因素影响，理论效率与实际效率存在显著差异。研究角度：从①模型算法、②特征输入、③响应输出三个维度研究基于数据驱动的泵站效率仿真模型。

**案例工程：** 南水北调东线**邳州站**（Pizhou Station）和**睢宁二站**（Suining 2nd Station）的8台机组历史数据。

**主要方法：** 引入8种机器学习模型（含高斯过程回归GPR、随机森林、XGBoost等）与传统多项式回归对比。创新提出用"上游水位+下游水位"(UWL+DWL)替代传统"扬程"(H)作为特征输入。

**主要结论：**
1. GPR模型综合性能最优，R²接近0.92
2. 使用UWL+DWL训练后，GPR模型所有指标提升，EMA指标从平均0.39%降至0.26%
3. 直接拟合效率优于拟合功率再换算效率，但R²指标相反
4. 以UWL+DWL训练GPR模型模拟效率精度最高：邳州站4号机组EMA和EMI分别从16.49%/20.40%降至0.18%/1.55%

**关键词：** 机器学习、高斯过程回归、泵站效率预测、数据驱动、东线南水北调

**书稿应用建议：**
- 数据驱动泵站效率模型是HydroOS中"泵站数字孪生"的核心技术
- UWL+DWL替代扬程H的创新体现了CHS理论中"物理量选择优化"
- 案例工程（邳州、睢宁）是东线江苏水源的典型控制断面

---

**[E3] Spatiotemporal characteristics and potential pollution factors of water quality in the eastern route of the South-to-North Water Diversion Project in China**
- 作者：Lingjiang Lu, Yongcan Chen, Manjie Li, Xiaohui Lei, Qingwei Ni, Zhaowei Liu
- 期刊：Journal of Hydrology, 2024, Vol.638, Article 131523
- DOI：10.1016/j.jhydrol.2024.131523
- ScienceDirect：https://www.sciencedirect.com/science/article/abs/pii/S0022169424009193

**详细内容（基于搜索结果）：**
应用水质综合指数（WQII）和多元统计方法（MSTs）对东线工程水质进行时空特征评估和潜在污染因子识别。

**主要结论：**
- 总体水质达到III类标准，说明过去10年污染控制有效
- 总氮（TN）污染仍然严峻，达到V类甚至劣V类，是首要关注问题
- 分流期与非分流期水质存在明显差异

**研究范围：** 覆盖东线从江苏扬州到山东的各调节湖（洪泽湖、骆马湖、南四湖、东平湖）及干线监测断面。

---

**[E4] Multi-scale closed-loop coupled real-time water quantity optimization scheduling of cascade pumping station in water supply canal systems**
- 作者：Haoshun Xia, Chao Wang, Jiahui Sun, Xiaohui Lei, Hao Wang
- 期刊：Journal of Hydrology, 2024, Vol.641, 131802
- DOI：10.1016/j.jhydrol.2024.131802
- ScienceDirect：https://www.sciencedirect.com/science/article/pii/S0022169424011983

**详细内容（基于搜索结果）：**
创新点：建立多尺度闭环耦合的梯级泵站实时调度框架，解决单一时间尺度闭环控制难以处理长时间维度不确定性问题。

**研究亮点：**
- 基于多尺度滚动优化的梯级泵站实时调度
- 同时处理单点和连续水量分配扰动
- 多尺度闭环相比单一尺度具有宏观引导优势
- 多尺度滚动优化可提高供水和经济效益
- 可扩展至更长时间维度的不确定调度问题

**书稿应用建议：**
- 东线梯级泵站多尺度优化调度是CHS"多尺度时间嵌套控制"的核心应用
- 闭环控制框架是CHS控制论在工程调度中的直接实现
- 与[J3]的MPC方法形成互补，共同构建调水工程智能控制体系

---

**[E5] A multi-objective optimal control model of cascade pumping stations considering both cost and safety**
- 作者：P Yan, Z Zhang, X Lei, Q Hou, H Wang
- 期刊：Journal of Cleaner Production, 2022, 345, 131171
- DOI：10.1016/j.jclepro.2022.131171

**内容概述：**
建立同时考虑成本和安全的梯级泵站多目标优化控制模型，在经济运行和安全运行之间取得平衡，应用于东线梯级泵站调度。

---

**[E6] Self-balancing of an open–close pumping station based on the second-order integrator-delay model**
- 作者：L Zhou, H Li, Z Lu, Z Zhang, X Lei, H Wang
- 期刊：Journal of Water Resources Planning and Management, 2025, 151(5), 04025005

**内容概述：**
基于二阶积分时延模型研究开-闭式泵站的自平衡特性，提出泵站自动控制新方法，对于泵站自动化运行（对应WNAL）具有重要意义。

---

## 五、跨主题综合论文

**[C1] Real-time reservoir flood control operation enhanced by data assimilation**
- 作者：J Zhang, X Cai, X Lei
- 期刊：Journal of Hydrology, 2021, 598, 126426

**[C2] An ecologically oriented operation strategy for a multi-reservoir system: A case study of the middle and lower Han River Basin, China**
- 作者：H Wang, X Lei, D Yan, X Wang, S Wu, Z Yin, W Wan
- 期刊：Engineering, 2018, 4(5), 627-634（王浩院士第一作者，体现中线水源水库群生态调度）

**[C3] Inter-basin water transfer-supply model and risk analysis with consideration of rainfall forecast information**
- 作者：X Lei, Y Jiang, H Wang, Y Tian
- 期刊：Science China Technological Sciences, 2010, 53(S1), 35-44（雷晓辉早期跨流域调水奠基性工作）

---

## 六、重点论文获取状态

| 编号 | 论文标题（简） | 获取状态 | 来源 |
|:---:|:---|:---:|:---|
| S1 | 沙坪二级电站水力调控 | ⚠️ 仅摘要 | 中国农村水利水电 |
| J1 | 引黄济青MIL测试 | ⚠️ 已知元数据 | 南水北调与水利科技 |
| J3 | 分流扰动实时控制（Jin 2023）| ✅ 全文获取 | MDPI开放访问 |
| M3 | 中线RL生态调度 | ⚠️ 摘要/关键信息 | J Hydrology |
| M4 | 丹江口突发污染 | ⚠️ 摘要 | PubMed |
| E1 | 东线江苏泵站效率中文 | ⚠️ 已知元数据 | 南水北调与水利科技 |
| E2 | 泵站效率数据驱动（英文）| ✅ 详细结果 | Energy Reports+SSRN |
| E3 | 东线水质时空特征 | ✅ 主要结论 | J Hydrology |
| E4 | 梯级泵站多尺度调度 | ✅ 主要创新点 | J Hydrology |

---

## 七、书稿素材整合建议

### 对应书稿章节

**第X章 水系统控制论在跨流域调水工程中的应用：**

1. **沙坪工程** → 梯级水电系统水力控制，时滞分析，从经验到模型
2. **胶东调水** → 渠系自平衡特性，MIL在环测试，现代控制方法在引水工程的应用
3. **中线工程** → 综合控制体系（蓄量补偿→预测控制→RL），水质安全，生态调度
4. **东线江苏** → 梯级泵站优化（效率模拟→多目标控制→多尺度闭环），水质监测

**叙述框架建议：**
- 从单工程单目标（如沙坪水力调控）→ 到网络级多目标（如东线梯级泵站多尺度调度）
- 从物理规律驱动（ID模型、MPC）→ 到数据驱动（GPR效率模型、RL生态调度）
- 从人工经验 → 辅助决策 → 自动控制 → 自主运行（对应WNAL L0→L5）

---

*整理人：Claude（基于网络搜索、MDPI全文、搜索结果摘要）*  
*注：带⚠️的论文建议通过CNKI、Web of Science或Sci-Hub补充全文*
