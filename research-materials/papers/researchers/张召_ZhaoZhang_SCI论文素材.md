# 张召 (Zhao Zhang) SCI论文素材汇编

## 研究人员信息

- **姓名**：张召（Zhao Zhang）
- **单位**：中国水利水电科学研究院水资源研究所·水资源调度研究室
- **职务**：高级工程师
- **学历**：2020年河海大学博士（水力学及河流动力学），导师系列
- **邮箱**：zhangzhao@iwhr.com
- **兼职**：中国水利学会调水专委会副秘书长；中国水力发电工程学会水工水力学专委会委员；《南水北调与水利科技》青年编委；《三峡大学学报（自然科学版）》青年编委
- **研究方向**：调水系统水力调控与智能运行
- **科研成果**：论文70余篇（SCI/EI 30篇），发明专利10余项，专著3部（一作），参编4部

---

## 论文1：梯级泵站群最优调度（胶东调水）

**标题**：Optimized Scheduling of Cascade Pumping Stations in Open-Channel Water Transfer Systems Based on Station Skipping

**中文标题**：基于跨站调度的开放渠道调水系统梯级泵站群优化调度

**期刊**：Journal of Water Resources Planning and Management（JWRPM，ASCE，SCI）

**发表信息**：2019, 145(7): 05019011

**DOI**：10.1061/(ASCE)WR.1943-5452.0001086

**作者**：**Zhang Z**, Lei X, Tian Y, Wang H, Wang C

**机构**：IWHR（中国水科院）

### 研究内容

针对开放明渠调水系统中梯级泵站群的实时调度问题，提出基于"跨站调度"（station skipping）策略的优化调度方法。传统调度每次调节需要所有泵站联动响应，效率低、调控繁琐。跨站策略允许部分泵站不参与某次调节，从而减少闸站操作次数，提升系统整体运行效率。

### 核心方法

- 建立以能耗最小化和水位稳定性为目标的优化调度模型
- 跨站调度策略：识别关键泵站与非关键泵站，动态确定参与调节的泵站集合
- 胶东调水工程验证（宋庄闸至惠薄泵站段）
- 结合一维水动力模型进行水力响应预测

### 主要结论

- 跨站调度策略可减少泵站操作次数20%-30%
- 水位波动控制在允许范围内
- 为长距离调水泵站群实时控制提供了新思路

### CHS理论映射

| CHS概念 | 论文贡献 |
|---------|---------|
| 泵站群协同控制 | 跨站调度策略实现多泵站协调 |
| 调度自动化 | WNAL L2→L3演进（规则优化→参数优化调度） |
| 实时控制 | 实时调度决策框架 |

### 书稿应用建议

适用于书稿**胶东调水**章节，展示泵站群智能调度方法；也适用于东线泵站群调度对比。

---

## 论文2：集合卡尔曼滤波校正泵站参数

**标题**：Correction of Pumping Station Parameters in a One-Dimensional Hydrodynamic Model Using the Ensemble Kalman Filter

**中文标题**：基于集合卡尔曼滤波的一维水动力模型泵站参数校正

**期刊**：Journal of Hydrology（SCI，Q1）

**发表信息**：2019, 568: 108-118

**DOI**：10.1016/j.jhydrol.2018.10.063

**作者**：**Lei X**, Tian Y, **Zhang Z**, Wang H, Wang C

**机构**：IWHR

### 研究内容

一维水动力模型中泵站特性曲线参数（扬程-流量关系曲线系数）的率定与校正问题。泵站参数误差会导致水力仿真精度下降，影响调度决策。本文引入集合卡尔曼滤波（EnKF）数据同化方法，实现泵站参数的动态校正。

### 核心方法

- 集合卡尔曼滤波（Ensemble Kalman Filter, EnKF）
- 泵站特性曲线参数辨识：扬程-流量关系多项式系数
- 状态变量：渠池水位；观测变量：实测水位
- 以胶东调水工程泵站为案例

### 主要结论

- EnKF可有效校正泵站Q-H曲线参数
- 参数校正后水动力模型精度显著提升
- 适用于运行状态监测与数字孪生参数更新

### CHS理论映射

| CHS概念 | 论文贡献 |
|---------|---------|
| 数字孪生参数识别 | EnKF实时数据同化更新模型参数 |
| 水力模型精确化 | 泵站参数校正提升物理模型保真度 |
| CHS感知层 | 实测数据驱动的参数动态更新 |

---

## 论文3：泵站控制时间简单方法（胶东）

**标题**：A Simple Method for the Control Time of a Pumping Station to Ensure a Stable Water Level Immediately Upstream of the Pumping Station under a Change of the Discharge in an Open Channel

**中文标题**：开放渠道流量变化下保证泵站上游水位稳定的控制时间简单方法

**期刊**：Water（MDPI，SCI）

**发表信息**：2021, 13(3): 355

**DOI**：10.3390/w13030355

**作者**：Yan P, **Zhang Z**, **Lei X**, Zheng Y, Zhu J, Wang H, Tan Q

**机构**：天津大学/IWHR/山东省调水运行维护中心/北京工业大学/河海大学

### 研究内容

梯级泵站开放渠道中，当上游流量发生变化时，如何确定泵站最优控制时刻，使泵站上游水位保持稳定。提出基于等效水量变化的逆向分析方法，快速确定控制时间。

### 核心方法

- 逆向分析法（reverse analysis）：以固定水位为下游边界，变流量为上游边界，求解泵站最优出流过程
- 等效水量变化法：以渠池蓄水量变化作为控制时间判断依据
- 案例：胶东调水工程G1–P1段（宋庄闸至惠薄泵站）
- 分析初始流量、变化流量、下游水位对控制时间的影响

### 主要结论

- 等效水量法提供了简便可靠的控制时间计算公式
- 控制时间随初始流量和变化幅度增大而延长
- 方法简单实用，可用于现场调度决策

### CHS理论映射

| CHS概念 | 论文贡献 |
|---------|---------|
| 水力响应时间 | 量化渠道水力传播的时延效应 |
| 泵站自动控制 | 基于水量平衡的前馈控制时刻确定 |
| 胶东工程运行 | 直接案例验证 |

---

## 论文4：梯级泵站多目标最优控制（成本+安全）

**标题**：A Multi-Objective Optimal Control Model of Cascade Pumping Stations Considering Both Cost and Safety

**中文标题**：综合考虑费用和安全的梯级泵站多目标最优控制模型

**期刊**：Journal of Cleaner Production（SCI，Q1）

**发表信息**：2022, 345: 131171

**DOI**：10.1016/j.jclepro.2022.131171

**作者**：Yan P, **Zhang Z**, **Lei X**, Zhu J, Wang H

**机构**：IWHR/天津大学等

### 研究内容

针对梯级泵站群调水的多目标优化问题，同时考虑运行成本最小化和安全约束（水位约束、流量约束），建立多目标最优控制模型。

### 核心方法

- 多目标优化框架：运行成本（能耗）最小 + 安全约束（水位上下限、衬砌安全）
- 结合一维水动力模型模拟渠道水力响应
- 帕累托最优解集生成与决策者选择
- 案例：胶东调水工程梯级泵站

### 主要结论

- 多目标框架能在成本节约与安全保障之间找到平衡
- 提供帕累托解集供决策者选择
- 对比单目标模型，多目标方案在安全性方面有显著提升

### CHS理论映射

| CHS概念 | 论文贡献 |
|---------|---------|
| 多目标调度决策 | 经济-安全帕累托权衡框架 |
| WNAL L3控制 | 基于优化的自动调度，非规则驱动 |
| 清洁生产视角 | 节能减排与安全约束融合 |

### 书稿应用建议

适用于东线、胶东章节讨论泵站群调度优化。

---

## 论文5：未知分水口识别模型

**标题**：A New Model for Rapid Identification of Unknown Water Diversion Discharge and Location

**中文标题**：未知分水流量与位置快速识别新模型

**期刊**：Hydrological Sciences Journal（SCI）

**发表信息**：2025, 70(9): 1454-1463（2025年5月14日在线发表）

**DOI**：10.1080/02626667.2025.2492231

**作者**：**Zhang Z**（通讯）, **Lei X**, Ping Xue（许平，河海大学）

**机构**：IWHR/河海大学

### 研究内容

调水工程安全运行的关键需求之一是快速识别非授权分水（未知分水）的流量和位置。提出基于仿真优化的新模型，通过分析流量与水位之间的相关性，缩小优化搜索范围，实现快速准确识别。

### 核心方法

- 仿真优化框架（simulation-optimization）
- 相关性分析缩减优化搜索范围
- 一维水动力仿真 + 优化算法
- 基金：山东省自然科学基金 ZR2024QE367；国家重点研发计划 2022YFC3204604

### 主要结论

- 可快速定位未知分水口位置并估算分水量
- 相关性预筛选显著减少优化计算量
- 对调水工程安全监控具有重要实用价值

### CHS理论映射

| CHS概念 | 论文贡献 |
|---------|---------|
| 调水安全异常检测 | 自动识别未授权分水 |
| 感知-诊断-决策链 | 基于观测数据的异常源定位 |
| 数字孪生支撑 | 仿真模型驱动的逆向推断 |

---

## 张召相关的其他重要论文

### ZZ-关联：泵站群实时模型预测控制（径流式水电站）

**标题**：Real-Time Model Predictive Control Study of Run-of-River Hydropower Plants with Data-Driven and Physics-Based Coupled Model

**期刊**：Journal of Hydrology, 2023, 617: 128942 (SCI)

**作者**：Ye S, **Wang C**, Wang Y, et al.（王超等，IWHR团队）

**注**：张召所在课题组同期相关成果，方法体系与张召论文一脉相承。

---

## 主要应用工程

张召参与了以下重大调水工程的调控系统建设：
- 南水北调中线工程（水力调控模型）
- 引江济淮工程（调度系统）
- **胶东调水工程**（数字孪生建设，主力成员）
- 珠三角水资源配置工程
- 其他调水工程（10余项）

其中"数字孪生胶东调水"是国内首个具备"无人运行、智能调度"能力的大型调水工程，入选数字孪生水利建设典型案例。

---

## GB/T 7714 参考文献格式

```
[1] ZHANG Z, LEI X, TIAN Y, et al. Optimized scheduling of cascade pumping stations in open-channel water transfer systems based on station skipping[J]. Journal of Water Resources Planning and Management, 2019, 145(7): 05019011.

[2] LEI X, TIAN Y, ZHANG Z, et al. Correction of pumping station parameters in a one-dimensional hydrodynamic model using the Ensemble Kalman filter[J]. Journal of Hydrology, 2019, 568: 108-118.

[3] YAN P, ZHANG Z, LEI X, et al. A simple method for the control time of a pumping station to ensure a stable water level immediately upstream of the pumping station under a change of the discharge in an open channel[J]. Water, 2021, 13(3): 355.

[4] YAN P, ZHANG Z, LEI X, et al. A multi-objective optimal control model of cascade pumping stations considering both cost and safety[J]. Journal of Cleaner Production, 2022, 345: 131171.

[5] ZHANG Z, LEI X, XUE P. A new model for rapid identification of unknown water diversion discharge and location[J]. Hydrological Sciences Journal, 2025, 70(9): 1454-1463.
```

---

## Z4：中线应急工况液压优化控制（Li等2023）

### 基本信息

**标题**：Hydraulic Optimization Control of a Water Diversion Canal System under Emergency Scenarios

**期刊**：Journal of Water Resources Planning and Management, 2023, 149(7). DOI: 10.1061/JWRMD5.WRENG-5881

**作者**：Li Yueqiang, **Zhang Zhao**, Kong Lingzhong, **Lei Xiaohui**, Zhu Jie

**研究工程**：南水北调中线工程（Gangtou Gate—Beijuma Gate段，GB段）

---

### 核心贡献

**问题背景**：中线明渠供水突发中断（下游水源紧急短缺），需要迅速制定应急闸群联控方案。

**方法体系**：
- 模拟优化框架（Simulation-Optimization Framework）
- 多目标粒子群算法（MOPSO：Multi-Objective Particle Swarm Optimization）
- 与一维非稳态水动力模型耦合

**优化目标**：
1. 最大化应急供水量（保障下游用水安全）
2. 最小化输水渠水位偏差（保障渠道运行安全）
3. 最小化闸门操作次数（减少实际操作工作量）

**约束条件**：水位安全约束、流量约束、闸门操作约束

---

### 主要结论

- 应急方案相比无优化调度，下游供水量显著提升
- MOPSO给出Pareto前沿，支持管理者根据实际紧急程度选择方案
- 供水量与水位稳定性之间存在权衡：应急时优先保供水

### CHS理论映射

| CHS概念 | 论文贡献 |
|---------|---------|
| 应急响应机制 | 突发中断下的快速优化控制 |
| 多目标协调 | 安全性与效益的Pareto权衡 |
| WNAL L4级 | 闸群自主应急决策能力雏形 |

---

## Z6：时间序列相似性实时水位预测（Zhou等2022）

### 基本信息

**标题**：Real-Time Water Level Prediction in Open Channel Water Transfer Projects Based on Time Series Similarity

**期刊**：Water, 2022, 14(13): 2070. DOI: 10.3390/w14132070

**作者**：Zhou Luyan, **Zhang Zhao**, Zhang Weijie, An Kaijun, **Lei Xiaohui**, He Ming

**研究机构**：中国水科院、山东省水利科学研究院、华能西藏水电

---

### 核心贡献

**问题**：明渠调水工程的实时水位预测需要处理多种水力结构相互作用带来的复杂性。

**方法**：基于时间序列相似性的实时水位预测模型（Time Series Similarity-based, TSS）

**技术特点**：
- 利用历史时间序列的相似模式匹配当前工况
- 无需建立复杂的数学模型或神经网络训练
- 可快速适应不同的工况条件

**应用案例**：胶东调水工程（明渠段实时水位预报）

---

### 主要结论

- TSS方法计算简便，预测精度满足实时调控要求
- 对比多种模型（LSTM等），TSS在计算效率上具有明显优势
- 适用于实时在线运行的快速预报场景

### CHS理论映射

| CHS概念 | 论文贡献 |
|---------|---------|
| 状态感知快速性 | 无需训练的实时预报，降低计算延迟 |
| 数字孪生轻量化 | 数据驱动替代物理模型，降低部署门槛 |
| 工程适用性 | 胶东调水实际工程验证 |

---

## 更新后参考文献清单（GB/T 7714）

```
[6] LI Y, ZHANG Z, KONG L, et al. Hydraulic Optimization Control of a Water Diversion Canal System under Emergency Scenarios[J]. Journal of Water Resources Planning and Management, 2023, 149(7). DOI: 10.1061/JWRMD5.WRENG-5881.

[7] ZHOU L, ZHANG Z, ZHANG W, et al. Real-Time Water Level Prediction in Open Channel Water Transfer Projects Based on Time Series Similarity[J]. Water, 2022, 14(13): 2070. DOI: 10.3390/w14132070.
```
