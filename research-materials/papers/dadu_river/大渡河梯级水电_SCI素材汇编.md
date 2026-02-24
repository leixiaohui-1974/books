# 大渡河梯级水电 SCI论文素材汇编

*整理时间：2026年2月*
*说明：四位目标研究者（张召、蒋志强、闻昕、谭乔凤）暂无以大渡河为主要案例的直接SCI论文，本汇编收录大渡河相关高质量SCI/EI论文及蒋志强课题组的相关调度系统背景，供书稿写作参考。*

---

## 大渡河流域概况

大渡河是岷江最大的支流，也是中国第五大水电基地：
- **水电潜力**：3459万千瓦
- **自然落差**：4175米
- **梯级规划**：28座梯级电站
- **核心梯级**：双江口（312m坝高，世界最高在建大坝）、猴子岩（223m，CFRD）、大岗山（210m拱坝）、瀑布沟（3.6GW，54亿m³库容）、深溪沟、珍珠坝、龚嘴
- **核心运行组合**：瀑布沟-深溪沟-珍珠坝（Pu-Shen-Zhen，总装机498万kW）

**运营主体**：国家能源集团大渡河能源有限公司（原国电大渡河水电开发有限公司）

**系统地位**：四川电网主要调峰调频电源，也是长江流域防洪的重要屏障。

---

## D1：大渡河流域智能运营管理（Tu等2023）

### 基本信息

**标题**：Intelligent Operation and Management in the Dadu River Basin

**期刊**：River (Wiley), 2023. DOI: 10.1002/rvr2.34

**作者**：Tu等（大渡河能源公司团队）

---

### 核心贡献

**背景**：记录大渡河公司构建"智能企业"的系统实践，是国内梯级水电智能化最系统的工程案例文献之一。

**智能调度关键里程碑**：
- **2013年起**：应用汛末分期蓄水技术，至2020年底累计多发干期电量约20.22亿kWh
- **2016年汛末**：分期蓄水多拦水量4.81亿m³，折合多发电3.36亿kWh，节约燃煤11.59万吨
- **2017年4月**：瀑布沟-深溪沟-珍珠坝实时智能"一键调度"系统投运

**"一键调度"系统**：
- 解决了AGC在传统电站层面无法协调三站水位的问题
- 深溪沟和珍珠坝库容极小（分别仅848万m³和1230万m³），受瀑布沟出力频繁变化影响严重
- 投运后实现梯级间实时、智能的负荷分配

**2019年6月背景**：西南电网与外部电网异步互联后，外部电网同步容量仅为原来的1/6，调峰调频需求急剧加大，对大渡河梯级调度提出更高要求。

---

### 书稿应用价值

- **自主运行典范**：大渡河"一键调度"是WNAL L3-L4的工程实证，可作为书稿中水电站自主运行演进案例。
- **数据**：具体指标（多蓄水量、多发电量、节煤量、减排量）可支撑CHS效益量化分析。

---

## D2：梯级水电高强度调峰下闸门联合优化运用（Zhang等2024）

### 基本信息

**标题**：Joint Optimal Use of Sluices of a Group of Cascade Hydropower Stations under High-Intensity Peak Shaving and Frequency Regulation

**期刊**：Water, 2024, 16(2): 275. DOI: 10.3390/w16020275 (MDPI开放获取)

**作者**：Zhang等（大渡河能源公司、相关高校合作）

**研究工程**：瀑布沟-深溪沟-珍珠坝（Pu-Shen-Zhen）

---

### 核心贡献

**问题背景**：高强度调峰调频使三座电站闸门操作极为频繁，水位大幅波动、"弃水"和"干库"风险并存。

**关键约束**（珍珠坝水力特点）：
- 水位须高于650m才能开闸
- 需避开闸门振动区
- 5个闸孔、每孔8.0×16m
- 低流量工况禁止不对称开启和单孔超大泄量

**方法**：
- "离线计算+在线搜索"组合模型
- **离线阶段**：为各站不同水位预算最优可行闸门开启组合，构建闸门操作策略表
- **在线阶段**：根据实时水位+调度需求，从策略表中快速检索最优方案

**验证时段**：2019年7月5日—8月5日（典型高调峰频率时期）

---

### 主要结论

- 三站闸门操作总次数从1195次降至675次，**减少43.5%**
- 主调站（瀑布沟）水位波动显著降低
- 下游两站水位稳定性明显改善

### CHS理论映射

| CHS概念 | 论文贡献 |
|---------|---------|
| 实时控制优化 | 离线预算+在线搜索实现毫秒级决策 |
| 设备保护约束 | 闸门振动区、非对称操作约束建模 |
| 梯级协同控制 | 三站统一考虑的闸门联合优化 |

---

## D3：深度强化学习梯级水库联合调度（Zhang等2024）

### 基本信息

**标题**：A Deep Reinforcement Learning Approach for Joint Scheduling of Cascade Reservoir System

**期刊**：Journal of Hydrology, 2024（12月）. DOI: 10.1016/j.jhydrol.2024.019115

**作者**：Zhang等（相关科研机构）

**研究工程**：瀑布沟-深溪沟-珍珠坝系统

---

### 核心贡献

**问题**：考虑来水预报不确定性、电网计划负荷不确定性以及蓄水任务约束的梯级调度。

**核心算法**：SAC（Soft Actor-Critic）+ EVHER（Enhanced Value Hindsight Experience Replay）采样框架

**创新点**：
- EVHER改进了传统HER（Hindsight Experience Replay）的采样策略
- 对比4种HER变体，在成功率和收敛速度均优
- 离线实时优化模型架构（Offline Real-Time Optimization）

**鲁棒性评估**：300次蒙特卡洛模拟（随机入流、负荷情景）

---

### 主要结论

- EVHER算法平均成功率达到**0.998**（接近完美）
- 相比HER四种变体策略，EVHER在收敛速度和解质量均更优
- 适用于带有终态水位约束的单目标短期调度场景

### CHS理论映射

| CHS概念 | 论文贡献 |
|---------|---------|
| WNAL L4自主决策 | RL实现无需人工干预的日内调度 |
| 终态控制 | 日终蓄水任务=水网过程状态目标控制 |
| 不确定鲁棒 | 300次MC验证的高稳健性决策 |

---

## D4：基于动态库容的短期水电调度优化（Zhang等2024）

### 基本信息

**标题**：Optimization of short-term hydropower scheduling with dynamic reservoir capacity

**期刊**：Journal of Hydrology, 2024

**作者**：Zhang Rongqi, Zhang Shanghong, Wen Xiaoxiong, Yue Ziqi, Zhou Yang

**研究工程**：瀑布沟-深溪沟-珍珠坝（大渡河梯级）

---

### 核心贡献

**问题**：传统调度模型假设水位-库容关系静态，忽略水下地形随时间的动态变化（淤积、冲刷等）。

**方法**：
- 动态库容（DRC: Dynamic Reservoir Capacity）模型
- 改进遗传算法（IGA: Improved Genetic Algorithm）
- 并行计算加速求解

**对比分析**：动态库容模型 vs. 传统静态模型

---

### 主要结论

- 动态库容修正后，发电量计算误差显著减小
- IGA结合并行计算，求解效率提升约60%
- 为长期运行的老坝（有淤积）调度提供更精确的基础模型

### CHS理论映射

| CHS概念 | 论文贡献 |
|---------|---------|
| 数字孪生精度 | 动态库容修正是数字孪生精确建模的组成部分 |
| 参数自适应 | 库容动态更新类似于CHS的模型参数在线辨识 |
| 计算效率 | 并行计算支撑实时优化的时效性要求 |

---

## D5/D6/D7/D8：大渡河工程建设与生态环境（综合背景文献）

### D5 流域水能高效开发（综述，中文）

**标题**：大型流域水能高效开发与利用关键技术

**期刊**：水电能源科学（核心期刊），2020年

**核心内容**：
- 大渡河全流域梯级规划：瀑布沟（主库，调节性最强）、大岗山、猴子岩、龚嘴、双江口
- "和谐水电"开发理念，多坝型并存（心墙堆石坝、混凝土面板堆石坝、拱坝、重力坝、闸坝）
- 统一流域调度，老站可持续挖潜（龚嘴、铜街子等老坝增效改造）

### D6 环境保护工程实践（英文SCI）

**标题**：Practices of environmental protection, technological innovation, economic promotion and social equity in hydropower development: a case study of cascade hydropower exploitation in China's Dadu River basin

**期刊**：Clean Technologies and Environmental Policy, 2021. DOI: 10.1007/s10098-021-02212-x

**核心数据**：
- 瀑布沟移民：约10.5万人（中国第二大水库移民，仅次于三峡约113万人）
- 主要移民集中地：汉源县（约9.3万人）
- 四维分析框架：环境保护、技术创新、经济促进、社会公平

### D7 流域开发关键技术早期示范（英文SCI）

**标题**：Early demonstration and research on the key technical issues of large-basin hydropower development under the concept of harmony

**期刊**：Clean Energy, 2020, 4(1): 67-80. DOI: 10.1093/ce/zkaa003

**关键技术突破**：
- 双江口：312m心墙堆石坝（当时世界最高在建大坝）
- 大岗山：210m拱坝，地震加速度0.557g（世界最高烈度拱坝）
- 瀑布沟（2010）：当时中国最高厚覆盖层堆石坝
- 猴子岩（2016）：狭谷高地震区第二高混凝土面板堆石坝
- 丹巴：国内最高门型坝，>100m厚覆盖层，软岩地质

### D8 大渡河智能工程建设（英文SCI）

**标题**：Exploration and practice of intelligent engineering in Dadu River hydropower construction

**期刊**：Clean Energy, 2020, 4(3): 288-302. DOI: 10.1093/ce/zkaa020

**智能化建设历程**：

| 阶段 | 项目 | 时间 |
|------|------|------|
| 探索期 | 数字大岗山（Digital Dagangshan） | 2011-2014 |
| 探索期 | 智能猴子岩（Intelligent Houziyan） | 2011-2014 |
| 试点期 | 沙坪二级（Shaping-II pilot） | 2014-2016 |
| 推广期 | 双江口（全面推广） | 2016至今 |

**五控体系**：安全、质量、进度、环保、投资（Five Controls）

**主要创新**：
- 智能大坝建造（温控、碾压监控）
- 地下工程智能化
- 混凝土温控智能化系统
- 双江口智能地下工程系统

---

## 蒋志强课题组与大渡河的联系

根据课题组室主任王超简介，**蒋志强所在的水资源调度研究室**研发的调度模型和软件平台已在**大渡河流域梯级水电站群**实现业务化运行。

具体联系：
- 调度优化模型（FLSS快速局部搜索策略）已在大渡河实际调度系统中得到应用
- 研究室为大渡河公司提供了短期-中期-长期多尺度的联合调度技术支持
- 但**蒋志强本人的SCI论文**案例工程主要为**雅砻江梯级**（两河口+7库系统），未见以大渡河为主要案例发表的英文SCI论文

---

## 四位目标研究者与大渡河的关系总结

| 研究者 | 大渡河直接SCI论文 | 关联说明 |
|--------|----------------|---------|
| 张召 | ❌ 无 | 研究领域为明渠调水（中线/胶东），非水库梯级 |
| 蒋志强 | ❌ 无直接论文 | 课题组研究成果在大渡河业务化运行；本人SCI以雅砻江为主 |
| 闻昕 | ❌ 无直接论文 | 研究以沅江、雅砻江、金沙江为主 |
| 谭乔凤 | ❌ 无直接论文 | 与闻昕合作，案例工程为沅江、雅砻江 |

**结论**：大渡河梯级调度SCI论文主要由大渡河能源公司内部技术团队和合作高校（华中科技大学其他团队、成都勘测设计研究院等）发表，四位目标研究者的案例工程以其他梯级水电或明渠调水为主。

---

## GB/T 7714 参考文献格式

```
[D1] TU, et al. Intelligent operation and management in the Dadu River Basin[J]. River, 2023. DOI: 10.1002/rvr2.34.

[D2] ZHANG, et al. Joint Optimal Use of Sluices of a Group of Cascade Hydropower Stations under High-Intensity Peak Shaving and Frequency Regulation[J]. Water, 2024, 16(2): 275. DOI: 10.3390/w16020275.

[D3] ZHANG, et al. A deep reinforcement learning approach for joint scheduling of cascade reservoir system[J]. Journal of Hydrology, 2024. DOI: 10.1016/j.jhydrol.2024.019115.

[D4] ZHANG R, ZHANG S, WEN X, et al. Optimization of short-term hydropower scheduling with dynamic reservoir capacity[J]. Journal of Hydrology, 2024.

[D6] FU, et al. Practices of environmental protection, technological innovation, economic promotion and social equity in hydropower development: a case study of cascade hydropower exploitation in China's Dadu River basin[J]. Clean Technologies and Environmental Policy, 2021. DOI: 10.1007/s10098-021-02212-x.

[D7] DUAN, et al. Early demonstration and research on the key technical issues of large-basin hydropower development under the concept of harmony[J]. Clean Energy, 2020, 4(1): 67-80. DOI: 10.1093/ce/zkaa003.

[D8] LI, et al. Exploration and practice of intelligent engineering in Dadu River hydropower construction[J]. Clean Energy, 2020, 4(3): 288-302. DOI: 10.1093/ce/zkaa020.
```
