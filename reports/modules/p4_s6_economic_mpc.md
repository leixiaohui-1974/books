<ama-doc>
# 第四部分 模型预测控制

## 第6节 经济型模型预测控制

### 4.6.1 引言

经济型模型预测控制（Economic Model Predictive Control, EMPC）是MPC技术在经济优化目标下的扩展形式。与传统跟踪型MPC不同，EMPC直接优化与经济性能相关的目标函数，如运行成本、能源消耗、资源利用效率等，而非跟踪预设的设定值或参考轨迹[1]。在水系统控制中，EMPC能够实现能源成本最小化、碳排放降低、设备寿命延长等多重经济目标，对于提升水系统的可持续性和经济性具有重要意义。

EMPC的理论研究始于21世纪初，Rawlings、Angeli、Amrit等学者建立了其稳定性理论和收敛性分析框架[2]。与传统MPC相比，EMPC面临的主要挑战在于：经济目标通常不是正定的，难以直接应用标准Lyapunov稳定性理论；最优操作点可能不是稳态，而是周期性或更复杂的轨迹；多目标权衡需要更精细的设计。

在水系统领域，泵站和污水处理是能源消耗的主要环节，占水系统运行成本的60%以上。EMPC通过优化设备运行策略、利用电价分时差异、协调多能源使用等方式，可显著降低运行成本。同时，EMPC还可整合碳排放目标，支持水系统的绿色转型。

### 4.6.2 经济型MPC的数学框架

#### 4.6.2.1 经济目标函数

EMPC的一般形式为：

$$\min_{\mathbf{u}} \sum_{i=0}^{N-1} l_e(x_{k+i|k}, u_{k+i|k}) \tag{4.6.1}$$

其中，$l_e(\cdot)$为经济阶段代价，通常具有以下形式：

**能源成本：**

$$l_e(x, u) = p_e \cdot P(x, u) \tag{4.6.2}$$

其中，$p_e$为电价，$P(x, u)$为功率消耗。

**多目标加权：**

$$l_e(x, u) = \alpha_1 J_{energy} + \alpha_2 J_{maintenance} + \alpha_3 J_{quality} \tag{4.6.3}$$

**经济-跟踪混合：**

$$l_e(x, u) = l_{economic}(x, u) + \rho \cdot l_{tracking}(x, u) \tag{4.6.4}$$

#### 4.6.2.2 稳态优化

EMPC通常与稳态优化层结合使用[3]。稳态优化问题：

$$(x_s, u_s) = \arg\min_{x, u} l_e(x, u) \tag{4.6.5}$$

$$\text{s.t.} \quad x = f(x, u) \tag{4.6.6}$$
$$x \in \mathbb{X}, \quad u \in \mathbb{U} \tag{4.6.7}$$

稳态解$(x_s, u_s)$为最优操作点，EMPC在此基础上进行动态优化。

#### 4.6.2.3 动态优化问题

EMPC动态优化：

$$\min_{\mathbf{u}} \sum_{i=0}^{N-1} l_e(x_{k+i|k}, u_{k+i|k}) \tag{4.6.8}$$

$$\text{s.t.} \quad x_{i+1} = f(x_i, u_i) \tag{4.6.9}$$
$$x_i \in \mathbb{X}, \quad u_i \in \mathbb{U} \tag{4.6.10}$$
$$x_N = x_s \text{ (或 } x_N \in \mathbb{X}_f \text{)} \tag{4.6.11}$$

### 4.6.3 稳定性与收敛性理论

#### 4.6.3.1 严格耗散性条件

EMPC的稳定性依赖于系统的严格耗散性（Strict Dissipativity）[4]。

定义：系统关于供给率$s(x, u) = l_e(x, u) - l_e(x_s, u_s)$是严格耗散的，若存在存储函数$\lambda(x)$和正定函数$\rho(x)$使得：

$$\lambda(f(x, u)) - \lambda(x) \leq s(x, u) - \rho(x - x_s) \tag{4.6.12}$$

严格耗散性保证了经济最优轨迹的稳定性。

#### 4.6.3.2 旋转代价函数

通过旋转代价（Rotated Cost）可将EMPC转化为标准跟踪型MPC：

$$\tilde{l}(x, u) = l_e(x, u) - l_e(x_s, u_s) + \lambda(x) - \lambda(f(x, u)) \tag{4.6.13}$$

旋转后的代价满足：

$$\tilde{l}(x, u) \geq \rho(x - x_s) \tag{4.6.14}$$

即具有正定形式，可应用标准MPC稳定性理论。

#### 4.6.3.3 平均性能分析

对于非稳态最优操作（如周期性操作），EMPC保证渐近平均性能：

$$\lim_{T \to \infty} \frac{1}{T} \sum_{k=0}^{T-1} l_e(x(k), u(k)) \leq l_e(x_s, u_s) + \epsilon \tag{4.6.15}$$

即长期平均经济性能接近最优。

### 4.6.4 周期性操作优化

#### 4.6.4.1 周期性最优解

某些系统的经济最优操作是周期性的而非稳态的[5]。典型例子包括：

- 利用电价峰谷差异的周期性储能
- 周期性反冲洗以维持过滤性能
- 季节性水资源调配

周期$T$的最优轨迹：

$$(x_p^*(0), \ldots, x_p^*(T-1)), \quad (u_p^*(0), \ldots, u_p^*(T-1)) \tag{4.6.16}$$

满足：

$$x_p^*(k+1) = f(x_p^*(k), u_p^*(k)), \quad x_p^*(T) = x_p^*(0) \tag{4.6.17}$$

#### 4.6.4.2 周期性EMPC

周期性EMPC优化问题：

$$\min_{\mathbf{u}} \sum_{i=0}^{N-1} l_e(x_{k+i|k}, u_{k+i|k}) \tag{4.6.18}$$

$$\text{s.t.} \quad x_{i+1} = f(x_i, u_i) \tag{4.6.19}$$
$$x_N = x_p^*((k+N) \mod T) \tag{4.6.20}$$

终端约束引导系统趋向周期性最优轨迹。

### 4.6.5 多目标经济优化

#### 4.6.5.1 帕累托最优

水系统通常涉及多个冲突的经济目标[6]：

- 能源成本 vs. 水质保障
- 运行成本 vs. 设备寿命
- 短期成本 vs. 长期可持续性

帕累托最优集定义为：

$$\mathcal{P} = \{(x, u) : \nexists (x', u') \text{ s.t. } J_i(x', u') \leq J_i(x, u), \forall i, \text{ with strict for some } i\} \tag{4.6.21}$$

#### 4.6.5.2 加权和法

通过权重调节实现多目标权衡：

$$l_e(x, u) = \sum_{i=1}^{m} w_i J_i(x, u) \tag{4.6.22}$$

不同权重组合产生帕累托前沿上的不同解。

#### 4.6.5.3 约束法

将次要目标转化为约束：

$$\min J_1(x, u) \tag{4.6.23}$$

$$\text{s.t.} \quad J_i(x, u) \leq \bar{J}_i, \quad i = 2, \ldots, m \tag{4.6.24}$$

通过调节约束边界$\bar{J}_i$探索帕累托前沿。

### 4.6.6 EMPC在水系统中的应用

#### 4.6.6.1 泵站能耗优化

泵站是供水系统的主要能耗设备，EMPC通过以下策略优化运行[7]：

**分时电价利用：**

$$l_e = \sum_{t} p_e(t) \cdot P(u_t) \tag{4.6.25}$$

其中，$p_e(t)$为时变电价，$P(u)$为泵站功率。

优化策略：
- 低谷时段多抽水、蓄满水箱
- 高峰时段减少抽水、利用水箱供水
- 优化泵站组合，使各泵运行在高效区

**变频调速优化：**

$$P = \frac{\rho g Q H}{\eta(Q, n)} \tag{4.6.26}$$

其中，$n$为转速，$\eta$为效率。EMPC优化转速使效率最大化。

#### 4.6.6.2 污水处理成本控制

污水处理过程能耗占运行成本的50%以上，EMPC优化曝气、污泥处理等环节[8]：

**曝气优化：**

$$\min \sum_{t} [p_e(t) \cdot P_{aer}(t) + c_{sludge} \cdot Q_{waste}(t)] \tag{4.6.27}$$

约束包括：
- 出水水质达标（BOD、氨氮、总氮等）
- 污泥龄限制
- 曝气池溶解氧范围

**碳源投加优化：**

在反硝化过程中，优化外部碳源投加量平衡脱氮效率与成本。

#### 4.6.6.3 多水源经济调度

对于具有多个水源（地表水、地下水、海水淡化等）的系统，EMPC优化水源配置[9]：

$$\min \sum_{t} \sum_{i} [c_i^{water} \cdot Q_{i,t} + c_i^{energy} \cdot P_{i,t}] \tag{4.6.28}$$

其中，$c_i^{water}$为水源$i$的水资源费，$c_i^{energy}$为取水能耗成本。

约束包括：
- 各水源取水量限制
- 水质混合要求
- 供水可靠性要求

### 4.6.7 实时经济优化

#### 4.6.7.1 稳态目标计算

双层MPC架构中，上层稳态优化计算最优设定值：

$$\min_{x_s, u_s} l_e(x_s, u_s) \tag{4.6.29}$$

$$\text{s.t.} \quad x_s = f(x_s, u_s) \tag{4.6.30}$$
$$y_s = h(x_s, u_s) = r \tag{4.6.31}$$
$$x_s \in \mathbb{X}, \quad u_s \in \mathbb{U} \tag{4.6.32}$$

下层动态MPC跟踪稳态目标。

#### 4.6.7.2 动态层优化

动态层考虑过渡过程优化：

$$\min_{\mathbf{u}} \sum_{i=0}^{N-1} [l_e(x_i, u_i) + \|y_i - y_s\|_Q^2] \tag{4.6.33}$$

经济项与跟踪项的结合确保快速收敛到经济最优。

#### 4.6.7.3 自适应经济优化

当经济参数（如电价、水价）变化时，实时更新优化目标：

$$l_e^{new}(x, u) = p_e^{new} \cdot P(x, u) \tag{4.6.34}$$

自适应EMPC快速响应市场变化。

### 4.6.8 小结

经济型模型预测控制将经济优化目标直接纳入控制设计，实现了从"跟踪设定值"到"优化经济性"的范式转变。通过严格耗散性理论和旋转代价函数，EMPC建立了完整的稳定性分析框架，保证了经济优化与系统稳定的统一。

在水系统控制中，EMPC在泵站能耗优化、污水处理成本控制、多水源经济调度等场景展现出显著的经济效益。利用分时电价差异、优化设备运行效率、协调多水源配置等策略，EMPC可降低运行成本10-30%，同时保障供水安全和水质达标。

周期性操作优化和多目标优化进一步扩展了EMPC的应用范围，使其能够处理更复杂的经济场景。随着电力市场改革和碳交易机制的推进，EMPC在水系统经济运营中的作用将更加重要。

未来发展方向包括：考虑碳排放约束的绿色EMPC、整合需求响应的交互式EMPC、基于市场信号的实时经济优化，以及与机器学习结合的数据驱动经济优化。

## 参考文献

[1] ELLIS M, DURAND H, CHRISTOFIDES P D. A tutorial review of economic model predictive control methods[J]. Journal of Process Control, 2014, 24(8): 1156-1178.

[2] RAWLINGS J B, AMRIT R. Optimizing process economic performance using model predictive control[M]//Nonlinear Model Predictive Control. Berlin: Springer, 2009: 119-138.

[3] RAWLINGS J B, BONNÉ D, JØRGENSEN J B, et al. Unreachable setpoints in model predictive control[J]. IEEE Transactions on Automatic Control, 2008, 53(9): 2209-2215.

[4] ANGELI D, AMRIT R, RAWLINGS J B. On average performance and stability of economic model predictive control[J]. IEEE Transactions on Automatic Control, 2012, 57(7): 1615-1626.

[5] ANGELI D, AMRIT R, RAWLINGS J B. Receding horizon cost optimization for overly constrained nonlinear plants[C]//Proceedings of the 48th IEEE Conference on Decision and Control. Shanghai: IEEE, 2009: 7972-7977.

[6] ZAVALA V M, FLORES-TLACUAHUAC A. Stability of multiobjective predictive control: A utopia-tracking approach[J]. Automatica, 2012, 48(10): 2627-2632.

[7] MENKE R, ABRAHAM E, PARPAS P, et al. Exploring optimal pump scheduling in water distribution networks with branch and bound methods[J]. Water Resources Research, 2016, 52(12): 9540-9552.

[8] VEGA D, REVOLLAR S, FRANCISCO M, et al. Economic optimization of the wastewater treatment plant by means of a flexible cost function[C]//Proceedings of the 10th IFAC Symposium on Advanced Control of Chemical Processes. Kyoto: IFAC, 2018: 187-192.

[9] MENKE R, ABRAHAM E, PARPAS P, et al. Demonstrating demand response from water distribution system through pump scheduling[J]. Applied Energy, 2016, 170: 377-387.

[10] FAULWASSER T, KORDA M, JONES C N, et al. Turnpike and dissipativity properties in dynamic real-time optimization and economic MPC[C]//Proceedings of the 2017 IEEE 56th Annual Conference on Decision and Control (CDC). Melbourne: IEEE, 2017: 6337-6342.

[11] MÜLLER M A, ANGELI D, ALLGÖWER F. On necessity and robustness of dissipativity in economic model predictive control[J]. IEEE Transactions on Automatic Control, 2015, 60(6): 1671-1676.

[12] HEIDARINEJAD M, LIU J, CHRISTOFIDES P D. Economic model predictive control of nonlinear process systems using Lyapunov techniques[J]. AIChE Journal, 2012, 58(3): 855-870.

</ama-doc>
