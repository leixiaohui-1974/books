# 蒋志强 (Zhiqiang Jiang) SCI论文素材汇编

## 研究人员信息

- **姓名**：蒋志强（Zhiqiang Jiang）
- **单位**：中国水利水电科学研究院水资源研究所·水资源调度研究室
- **研究方向**：梯级水电站/水库群联合调度优化
- **合作核心**：王超（Chao Wang，室主任）、雷晓辉（Xiaohui Lei）

**研究背景**：蒋志强是王超调度室的核心研究人员，专注于梯级水电站长期调度的优化理论，特别是基于最优性原理的大规模水电调度算法设计。研究成果在**大渡河、金沙江下游**等流域水电站群调度中得到实际应用。

---

## 论文1：两阶段问题单调性原理（梯级水电站联合调度）

**标题**：Discussion on the Monotonicity Principle of the Two-Stage Problem in Joint Optimal Operation of Cascade Hydropower Stations

**中文标题**：梯级水电站联合最优调度两阶段问题单调性原理探讨

**期刊**：Journal of Hydrology（SCI，Q1，Elsevier）

**发表信息**：2023, 623: 129803

**DOI**：10.1016/j.jhydrol.2023.129803

**作者**：**Wang C**, **Jiang Z**, Xu Y, et al.

**机构**：IWHR（中国水科院）

### 研究背景

梯级水电站长期优化调度面临"维数灾难"——随水库数量增加，状态-动作空间呈指数爆炸。动态规划（DP）及其变体（SDP、POA等）是常用方法，但其中的"两阶段优化"子问题的理论性质（如单调性）尚不明晰，影响算法效率与收敛性。

### 核心贡献

- 系统探讨梯级水电站联合调度中"两阶段问题"（two-stage problem）的**单调性原理**（monotonicity principle）
- 揭示在特定条件下水位/库容决策函数的单调性特征
- 为构建高效的优化算法（减少搜索空间）提供理论依据
- 案例应用于大规模梯级水电站系统

### 理论意义

单调性原理的确立使得：
1. 可用二分搜索替代穷举搜索，算法复杂度从O(n)降低至O(log n)
2. 为后续POA（逐步逼近算法）改进提供理论基础
3. 对多水库联合调度中的计算效率提升具有普适价值

### CHS理论映射

| CHS概念 | 论文贡献 |
|---------|---------|
| 水网自主运行控制 | 理论支撑梯级水电站智能化长期调度 |
| WNAL L3→L4 | 从规则调度到优化调度的理论升级 |
| 调度决策智能化 | 揭示单调性原理支撑高效搜索算法 |

### 书稿应用建议

- 适用于大渡河梯级水电调度章节，作为长期优化调度的理论基础
- 展示CHS框架下水电调度从"经验调度"向"最优调度"的演进

---

## 论文2：梯级水电站长期调度快速局部搜索策略

**标题**：A Fast Local Search Strategy Based on the Principle of Optimality for the Long-Term Scheduling of Large Cascade Hydropower Stations

**中文标题**：基于最优性原理的大型梯级水电站长期调度快速局部搜索策略

**期刊**：Water Resources Management（WRM，SCI，Springer/EWRA）

**发表信息**：2024, 38(1): 137-152

**DOI**：10.1007/s11269-023-03669-7

**作者**：**Wang C**, **Jiang Z**, Wang P, Xu Y

**机构**：IWHR

### 研究内容

大型梯级水电站（如大渡河22级、金沙江下游4级）的长期调度是高维度非线性优化问题。传统穷举式动态规划计算量巨大，局部搜索策略可显著提速。本文基于Bellman最优性原理，设计了一种快速局部搜索策略（Fast Local Search Strategy, FLSS），在不牺牲最优性的前提下大幅提升计算效率。

### 核心方法

- **最优性原理应用**：利用Bellman最优性原理将多阶段问题分解
- **局部搜索策略**：以当前解为中心在局部邻域内搜索，避免全局遍历
- **大规模验证**：以中国大型梯级水电站系统为案例
- 与传统DP、POA方法的效率对比

### 主要结论

- FLSS在保持解质量的同时，计算时间减少80%以上（相比全局DP）
- 适用于实时调度场景（秒级响应）
- 可扩展至20+级梯级水电站的大规模应用

### 实际应用

研究成果已在**大渡河、金沙江下游**梯级水电站群的实际调度系统中得到应用。

### CHS理论映射

| CHS概念 | 论文贡献 |
|---------|---------|
| 自主运行实时性 | 快速算法支撑实时调度决策 |
| 大规模水电系统优化 | 处理20+级梯级系统的计算可行性 |
| WNAL L3优化控制 | 最优性原理驱动的自动调度 |

### 书稿应用建议

- **核心素材**：适用于大渡河梯级水电章节的调度优化方法部分
- 可与谭乔凤/闻昕的水光互补调度论文形成体系

---

## 蒋志强课题组背景：大渡河调度系统建设

根据王超（室主任）简介，水资源调度研究室研发的调度模型和软件平台已在以下流域实际业务化运行：

| 应用场景 | 工程/流域 |
|---------|---------|
| 梯级水电站群调度 | **大渡河**流域梯级水电站群 |
| 梯级水电站群调度 | **金沙江下游**水电站群 |
| 流域水资源调度 | 永定河流域 |
| 跨流域调水 | 南水北调东/中线工程 |
| 跨流域调水 | 胶东调水工程 |
| 跨流域调水 | 引江济淮工程 |

大渡河是中国大渡河能源集团有限公司（国家能源集团子公司）旗下的22级梯级水电站，总装机容量27GW，是中国"水电智能自主运行"的代表性示范工程。

---

## GB/T 7714 参考文献格式

```
[1] WANG C, JIANG Z, XU Y, et al. Discussion on the monotonicity principle of the two-stage problem in joint optimal operation of cascade hydropower stations[J]. Journal of Hydrology, 2023, 623: 129803.

[2] WANG C, JIANG Z, WANG P, et al. A fast local search strategy based on the principle of optimality for the long-term scheduling of large cascade hydropower stations[J]. Water Resources Management, 2024, 38(1): 137-152.
```

---

## J1：雅砻江年消落水位动态控制（Jiang等2023）

### 基本信息

**标题**：Dynamic Control of the Yearly Drawdown Level of Overyear Regulation Reservoirs Based on Optimal Impoundment

**期刊**：Water, 2023, 15(4): 665. DOI: 10.3390/w15040665

**作者**：**Jiang Zhiqiang**等（华中科技大学）

**研究工程**：雅砻江梯级7库系统（含两河口多年调节水库）

---

### 核心贡献

**问题**：多年调节水库（Lianghekou/两河口）消落水位过早确定会导致蓄水不足，需要动态控制以实现最优蓄水效益。

**方法**：
- 以最优蓄水为目标的消落水位动态控制模型
- 动态规划（Dynamic Programming）算法求解
- 7座梯级水库联合优化调度

**创新点**：
- 突破传统固定消落水位限制
- 年内滚动优化，根据来水预报动态调整消落目标
- 平衡发电效益与防洪蓄水安全

---

### 主要结论

- 动态消落水位控制比传统固定水位方案年均发电量提高约3-5%
- 汛末蓄水保证率显著提高
- 为多年调节水库运行决策提供科学依据

### CHS理论映射

| CHS概念 | 论文贡献 |
|---------|---------|
| 多时间尺度控制 | 年-月-旬滚动优化决策框架 |
| 不确定性处理 | 来水预报不确定下的鲁棒决策 |
| WNAL L3优化控制 | 基于优化算法的自动化调度 |

---

## J2：随机环境模拟短期梯级调度强化学习（Wan等2025）

### 基本信息

**标题**：Random Environment Simulation for Cascade Hydropower Scheduling with Reinforcement Learning

**期刊**：Energy（预计2025年）

**作者**：Wan等，**Jiang Zhiqiang**参与（华中科技大学）

**基金支持**：国家自然科学基金（U2340211, 52479017, 52179016）

---

### 核心贡献

**问题**：短期梯级水电调度需应对入库径流和电网负荷的双重不确定性，传统强化学习难以处理稀疏奖励和状态空间维度诅咒。

**方法**：
- 多阶段强化学习（Multi-Stage RL）框架
- 随机环境模拟（Random Environment Simulation）技术
- 应用于大型梯级水电站群短期调度

**技术特点**：
- 随机环境生成器模拟入库流量和负荷的随机组合
- 多阶段训练策略逐步提升策略鲁棒性
- 适应实时在线决策需求

---

### 主要结论

- RL策略在随机环境训练下鲁棒性显著优于传统方法
- 多阶段框架有效克服稀疏奖励问题
- 短期（日内）调度精度接近或优于传统优化方法

### CHS理论映射

| CHS概念 | 论文贡献 |
|---------|---------|
| WNAL L4自主决策 | RL实现无人干预的短期自主调度 |
| 不确定性鲁棒 | 随机环境模拟提升策略适应性 |
| 实时响应性 | 多阶段RL支持在线快速决策 |

---

## 更新后参考文献清单

```
[3] JIANG Z, et al. Dynamic Control of the Yearly Drawdown Level of Overyear Regulation Reservoirs Based on Optimal Impoundment[J]. Water, 2023, 15(4): 665. DOI: 10.3390/w15040665.

[4] WAN, et al. Random Environment Simulation for Cascade Hydropower Scheduling with Reinforcement Learning[J]. Energy, 2025. (co-author: Jiang Zhiqiang)
```
