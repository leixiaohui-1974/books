# Real-Time Control Operation Method of Water Diversion Project Based on River Diversion Disturbance

**论文信息**
- 作者：Pengyu Jin¹, Chao Wang²*, Jiahui Sun³, Xiaohui Lei², Hao Wang²
- 期刊：Water (MDPI), 2023, 15(15), 2793
- DOI：10.3390/w15152793
- 开放获取：CC BY
- ¹ Hohai University; ² IWHR; ³ Shandong University

---

## Abstract

Changes in water diversion flow are the major disturbance sources in the daily operation of water diversion projects. Ensuring efficient and safe project operation while dealing with different degrees of water diversion disturbance is crucial for real-time control operation. Based on the historical water diversion projects in China and abroad, this study constructs the water diversion disturbance conditions, selects the typical disturbance lines, and constructs the control objectives for different water diversion disturbance lines. The discrete state space equation of the multi-channel pool integral time-delay model is introduced and used as the system prediction model. Concurrently, the simulation results of the river channel hydrodynamic model are used to correct the system state. The model predictive control algorithm is established according to the objective functions of different typical water distribution disturbance lines, and the control strategy of the control gate and pump station along the water diversion project is formulated to assist in the decision making of the project scheduling operation scheme. The proposed method can better cope with different degrees of river diversion disturbance, compensate for the loss of control performance caused by the low accuracy of the generalized model simulation, and improve water level control and sluice regulation.

**Keywords:** predictive control algorithm; water diversion disturbance; multi-channel pool integral time-delay model; discrete state space equation

---

## 1. Introduction

研究背景：
- 调水工程规模扩大、调水线路复杂化，调度运行难度增加
- 传统调度高度依赖人工，控制精度低、管理成本高
- 分水口流量变化是日常运行的主要扰动源，可导致梯级泵站运行失效、不稳定等问题

研究现状：
- 早期：基于圣维南方程逆解的闸门行程算法（gate-stroking），受工程约束限制
- 体积补偿算法（volume compensation）：处理两稳态间流量补偿
- PID控制：成功应用于伊朗Dez灌渠和澳大利亚新南威尔士灌渠
- 模型预测控制（MPC）：处理复杂工程拓扑和扰动，效果显著提升
- Hashemy等：MPC+输水线蓄水策略应对分流扰动
- Zheng等：大系统分解协调模型+分时电价，实现梯级泵站经济运行

研究空白：现有研究多针对灌渠或纯控制闸门系统，跨流域调水工程中控制闸+泵站混合系统的MPC设计及分水扰动策略研究不足。

---

## 2. 五类典型分流扰动条件

基于国内外历史调水工程水分配规律分析，分流扰动分五类（C1~C5）：

| 类型 | 描述 | 扰动强度 | 扰动频率 |
|:---:|:---|:---:|:---:|
| C1 | 按计划增大分流量，满足后恢复稳态 | 中 | 低 |
| C2 | 城市用水高峰期临时突增，满足后恢复 | **高（突变）** | **低** |
| C3 | 闸门频繁调节导致分流波动，降低调节频次恢复 | 低 | **高** |
| C4 | 需求减少，减小分流量，恢复稳态 | 中 | 低 |
| C5 | 下游用水高峰，渠池减少分流以平衡，高峰后恢复 | 中 | 低 |

C2（突变高强度低频）和C3（渐变低强度高频）是最具代表性的两种扰动线型。

---

## 3. 方法

### 3.1 积分时延模型（ID Model）

圣维南方程作为MPC内部预测模型计算太慢，采用积分时延（Integrator-Delay）模型代替：

**单渠池ID模型：**
$$q_{fa}(t) = q_{in}(t - \tau)$$
$$\frac{dy(t)}{dt} = \frac{1}{A_s}[q_{fa}(t) - q_{out}(t) - q_d(t)]$$

其中：y为下游控制点水位，τ为均匀流区时延，$A_s$为回水区水面面积

**多渠池离散状态空间方程：**
$$x(k+1) = A \cdot x(k) + B_u \cdot u(k) + B_d \cdot d(k)$$

状态变量：水位y(k)、水位变幅Δy(k)、超前控制入流变幅序列
控制变量：入流变幅Δq_in(k)、出流变幅Δq_out(k)、分流变幅Δq_d(k)

### 3.2 目标函数（三层次结构）

**针对C2（高强度突变扰动）：**
- 第1层（最高优先）：保证水位约束和末端水量需求
- 第2层：最小化渠池水位每小时变幅（促进扰动后快速恢复稳态）
- 第3层：最大化梯级泵站运行效率（高效区过渡）

**针对C3（低强度高频扰动）：**
- 第1层：最大化初末段水位稳定时长
- 第2层：增大稳定运行效率及稳定时长

### 3.3 模型预测控制算法

- 模拟步长：1h；控制步长：2h；预见期：72h
- 将相邻泵站、闸门站及其间渠道视为一个渠池
- 广义倒虹吸、坡降段、分水口等内部建筑物用SV方程耦合
- 一维水动力模型计算结果用于在线系统状态修正
- 基于MPC框架求解最优控制策略

---

## 4. 案例验证

**案例工程：** 引江济淮（Yangtze River to Huai River）工程历史调度数据

验证了方法对不同程度分流扰动的适应性，证明相较于单纯广义模型方法，提高了水位控制稳定性和闸门调节效果。

---

## 关键引用文献（部分）

- Hashemy et al. (2013): Inline storage + MPC, Irrig Drain
- Zheng et al.: Large-scale system decomposition for cascade pump stations
- Malaterre et al. (1998): Canal control algorithm classification
- Clemmens et al. (1998): Test cases for canal control

---

## 书稿应用要点

1. **调水工程扰动分类体系（C1-C5）** 可直接引用或参考，纳入CHS理论的扰动分类框架
2. **ID模型+MPC** 是CHS中"预测反馈混合控制"的经典实现案例
3. **三层次目标函数** 体现了调水工程调度中约束-稳定性-经济性的优先级关系
4. **案例为引江济淮**，可与胶东调水案例形成对比，展示CHS方法的普适性

*全文来源：MDPI Water, 开放获取，CC BY 4.0*
