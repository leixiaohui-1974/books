<ama-doc>
# 第四部分 模型预测控制

## 第5节 鲁棒模型预测控制

### 4.5.1 引言

鲁棒模型预测控制（Robust Model Predictive Control, RMPC）是针对系统不确定性和外部扰动的MPC扩展方法。在实际水系统控制中，模型误差、参数不确定性、未建模动态、需水量预测误差等不确定性因素普遍存在，标准MPC基于名义模型的优化策略可能导致约束违反或性能恶化。RMPC通过在控制设计中显式考虑不确定性边界，保证在最坏情况下仍能满足约束并实现可接受的控制性能[1]。

RMPC的研究始于20世纪90年代，Kothare、Balakrishnan、Morari等学者提出了基于线性矩阵不等式（LMI）的鲁棒MPC方法[2]。随后，Tube MPC、Min-max MPC、随机MPC等方法相继发展，形成了较为完整的理论体系。在水系统控制中，RMPC被用于处理需水量不确定性、管网参数不确定性、突发事件等场景。

RMPC的核心思想是在预测和优化中考虑不确定性的影响，确保控制策略对所有可能的不确定性实现都具有可行性和稳定性。这种保守性设计虽然可能牺牲部分名义性能，但显著提高了系统的可靠性和安全性，对于保障水系统的安全运行至关重要。

### 4.5.2 不确定性的建模与分类

#### 4.5.2.1 不确定性来源

水系统中的不确定性主要来源于以下方面[3]：

**模型不确定性：**
- 管道粗糙系数估计误差
- 泵站特性曲线拟合误差
- 水箱容积标定误差
- 简化模型引入的结构性误差

**参数不确定性：**
- 需水量预测误差
- 电价波动
- 水质参数变化
- 环境温度影响

**外部扰动：**
- 突发漏损
- 管道爆裂
- 极端天气事件
- 用户行为变化

**测量噪声：**
- 传感器精度限制
- 通信延迟和丢包
- 数据预处理误差

#### 4.5.2.2 不确定性表征

根据可用信息的不同，不确定性可采用以下方式表征：

**范数有界不确定性：**

$$w \in \mathbb{W} = \{w : \|w\| \leq \bar{w}\} \tag{4.5.1}$$

其中，$\bar{w}$为不确定性上界。

**多面体不确定性：**

$$w \in \mathbb{W} = \text{Co}\{w_1, w_2, \ldots, w_L\} \tag{4.5.2}$$

其中，$\text{Co}$表示凸包，$w_i$为不确定性顶点。

**概率不确定性：**

$$w \sim \mathcal{N}(\mu, \Sigma) \tag{4.5.3}$$

或更一般的概率分布$P(w)$。

### 4.5.3 Tube-based MPC

#### 4.5.3.1 基本思想

Tube MPC是最具代表性的RMPC方法之一，其核心思想是将状态轨迹分解为标称轨迹和误差轨迹两部分[4]：

$$x(k) = z(k) + e(k) \tag{4.5.4}$$

其中，$z(k)$为标称状态（无扰动时的轨迹），$e(k)$为误差状态。

标称系统：
$$z(k+1) = Az(k) + Bv(k) \tag{4.5.5}$$

误差系统：
$$e(k+1) = (A + BK)e(k) + w(k) \tag{4.5.6}$$

其中，$u(k) = v(k) + Ke(k)$，$K$为误差反馈增益。

#### 4.5.3.2 不变集计算

Tube MPC的关键是计算误差的不变集（Invariant Set），即满足以下条件的集合$\mathbb{S}$：

$$(A + BK)\mathbb{S} \oplus \mathbb{W} \subseteq \mathbb{S} \tag{4.5.7}$$

其中，$\oplus$表示Minkowski和。

最小鲁棒正不变集（mRPI）的计算方法：

**近似方法：**

$$\mathbb{S} \approx \sum_{i=0}^{N_s} (A + BK)^i \mathbb{W} \tag{4.5.8}$$

其中，$N_s$为足够大的整数。

**精确方法：** 利用线性规划或几何算法计算多面体不变集。

#### 4.5.3.3 约束紧缩

为保证实际状态满足约束，标称约束需紧缩：

$$z(k) \in \mathbb{Z} = \mathbb{X} \ominus \mathbb{S} \tag{4.5.9}$$
$$v(k) \in \mathbb{V} = \mathbb{U} \ominus K\mathbb{S} \tag{4.5.10}$$

其中，$\ominus$表示Pontryagin差。

Tube MPC优化问题：

$$\min_{\mathbf{v}} \sum_{i=0}^{N-1} l(z_{k+i|k}, v_{k+i|k}) + V_f(z_{k+N|k}) \tag{4.5.11}$$

$$\text{s.t.} \quad z_{i+1} = Az_i + Bv_i \tag{4.5.12}$$
$$z_i \in \mathbb{Z}, \quad v_i \in \mathbb{V} \tag{4.5.13}$$
$$z_N \in \mathbb{Z}_f \tag{4.5.14}$$

实际应用的控制量：

$$u(k) = v^*(k) + K(x(k) - z^*(k)) \tag{4.5.15}$$

### 4.5.4 Min-max MPC

#### 4.5.4.1 优化问题 formulation

Min-max MPC优化最坏情况下的性能[5]：

$$\min_{\mathbf{u}} \max_{\mathbf{w} \in \mathbb{W}} J(x, \mathbf{u}, \mathbf{w}) \tag{4.5.16}$$

$$\text{s.t.} \quad x_{i+1} = f(x_i, u_i, w_i) \tag{4.5.17}$$
$$x_i \in \mathbb{X}, \quad u_i \in \mathbb{U}, \quad \forall \mathbf{w} \in \mathbb{W} \tag{4.5.18}$$

对于线性系统和多面体不确定性，min-max问题可转化为单一优化问题。

#### 4.5.4.2 开环与反馈Min-max

**开环Min-max：** 控制序列在优化时固定，不考虑未来信息

$$\min_{\mathbf{u}} \max_{\mathbf{w}} J \tag{4.5.19}$$

**反馈Min-max：** 控制策略为状态的函数$u_i = \pi_i(x_i)$

$$\min_{\pi} \max_{\mathbf{w}} J \tag{4.5.20}$$

反馈Min-max保守性更低，但计算更复杂。

#### 4.5.4.3 场景优化

对于大规模不确定性，可采用场景法近似：

$$\min_{\mathbf{u}} \sum_{s=1}^{N_s} p_s J(x, \mathbf{u}, \mathbf{w}_s) \tag{4.5.21}$$

其中，$\{w_1, \ldots, w_{N_s}\}$为不确定性样本，$p_s$为场景概率。

### 4.5.5 随机MPC

#### 4.5.5.1 机会约束

当不确定性具有概率分布时，可采用机会约束（Chance Constraints）[6]：

$$\mathbb{P}(x \in \mathbb{X}) \geq 1 - \epsilon \tag{4.5.22}$$

其中，$\epsilon$为违反概率上界。

对于高斯不确定性，机会约束可转化为确定性约束：

若$x \sim \mathcal{N}(\mu, \Sigma)$，则：

$$\mathbb{P}(a^T x \leq b) \geq 1 - \epsilon \Leftrightarrow a^T \mu + \Phi^{-1}(1-\epsilon)\sqrt{a^T \Sigma a} \leq b \tag{4.5.23}$$

其中，$\Phi^{-1}$为标准正态分布的逆CDF。

#### 4.5.5.2 期望代价优化

随机MPC优化期望性能：

$$\min_{\mathbf{u}} \mathbb{E}[J(x, \mathbf{u}, \mathbf{w})] \tag{4.5.24}$$

对于二次代价和高斯扰动：

$$\mathbb{E}[x^T Q x] = \mu^T Q \mu + \text{tr}(Q\Sigma) \tag{4.5.25}$$

#### 4.5.5.3 场景树MPC

场景树方法通过树状结构表示不确定性的演化[7]：

- 根节点：当前已知状态
- 分支：不确定性实现的不同可能
- 叶节点：预测时域末端的场景

优化问题在整棵树上进行，决策变量满足非预期约束（non-anticipativity constraints）。

### 4.5.6 自适应鲁棒MPC

#### 4.5.6.1 在线参数估计

自适应RMPC结合参数估计和控制设计，逐步减小不确定性[8]：

参数估计（递推最小二乘）：

$$\hat{\theta}(k) = \hat{\theta}(k-1) + L(k)(y(k) - \phi^T(k)\hat{\theta}(k-1)) \tag{4.5.26}$$

其中，$\theta$为未知参数，$L(k)$为增益矩阵。

#### 4.5.6.2 双重控制

双重控制（Dual Control）在优化控制性能的同时考虑参数学习价值：

$$\min_{u} [J_{control} + \alpha J_{learning}] \tag{4.5.27}$$

其中，$J_{learning}$衡量控制动作对参数估计精度的改善。

#### 4.5.6.3 学习 Tube MPC

结合机器学习的Tube MPC利用历史数据学习不确定性边界和误差反馈策略：

$$\mathbb{S}_{learned} = \{e : f_{ML}(e) \leq 0\} \tag{4.5.28}$$

其中，$f_{ML}$为机器学习模型（如支持向量机、神经网络）。

### 4.5.7 RMPC在水系统中的应用

#### 4.5.7.1 需水量不确定性处理

供水管网面临显著的需水量预测不确定性[9]：

$$d(k) = \hat{d}(k) + w_d(k), \quad w_d \in \mathbb{W}_d \tag{4.5.29}$$

Tube MPC设计：
- 基于预测需水量计算标称轨迹
- 考虑预测误差范围设计Tube
- 约束紧缩确保实际水位安全

#### 4.5.7.2 管网参数不确定性

管道粗糙系数等参数随时间变化且难以精确测量：

$$C_{HW} \in [C_{min}, C_{max}] \tag{4.5.30}$$

鲁棒优化保证在所有可能参数下满足压力约束。

#### 4.5.7.3 突发事件应对

针对管道爆裂等突发事件，采用多场景RMPC：

- 正常场景
- 单点故障场景
- 多点故障场景

优化控制策略在所有场景下都具有可行性和可接受的性能。

### 4.5.8 小结

鲁棒模型预测控制为不确定性环境下的水系统安全运行提供了理论保障和技术手段。通过显式考虑模型误差、参数不确定性和外部扰动，RMPC确保控制策略在最坏情况下仍能满足约束并实现可接受的性能。

Tube MPC通过标称轨迹与误差轨迹的分离，将鲁棒控制问题转化为紧缩约束的标准MPC问题，计算效率高且易于实现。Min-max MPC直接优化最坏情况性能，保守性较强但保证明确。随机MPC利用不确定性的概率信息，在风险与性能之间取得平衡。

在水系统控制中，需水量预测误差、管网参数不确定性、突发事件等是RMPC的主要应用场景。随着自适应控制和学习控制技术的发展，RMPC正从固定不确定性边界向数据驱动的自适应边界演进，为智慧水务的不确定性管理提供了更灵活的解决方案。

未来发展方向包括：基于深度学习的端到端鲁棒MPC、考虑多源不确定性的综合鲁棒框架、面向网络攻击的安全MPC，以及实时性更强的近似RMPC算法。

## 参考文献

[1] KOUVARITAKIS B, CANNON M. Model Predictive Control: Classical, Robust and Stochastic[M]. Cham: Springer International Publishing, 2016.

[2] KOTHARE M V, BALAKRISHNAN V, MORARI M. Robust constrained model predictive control using linear matrix inequalities[J]. Automatica, 1996, 32(10): 1361-1379.

[3] PASCUAL J, BARREIRO A, LÓPEZ P. Multivariable control of a water supply system with a risk management approach[J]. Water Resources Management, 2013, 27(14): 4911-4926.

[4] MAYNE D Q, SERON M M, RAKOVIĆ S V. Robust model predictive control of constrained linear systems with bounded disturbances[J]. Automatica, 2005, 41(2): 219-224.

[5] SCOKAERT P O, MAYNE D Q. Min-max feedback model predictive control for constrained linear systems[J]. IEEE Transactions on Automatic Control, 1998, 43(8): 1136-1142.

[6] MESBAH A. Stochastic model predictive control: An overview and perspectives for future research[J]. IEEE Control Systems Magazine, 2016, 36(6): 30-44.

[7] BERNARDINI D, BEMPORAD A. Stabilizing model predictive control of stochastic constrained linear systems[J]. IEEE Transactions on Automatic Control, 2012, 57(6): 1468-1480.

[8] ADETOLA V, GUAY M, LEHRER D. Adaptive estimation in model predictive control of constrained uncertain systems[J]. International Journal of Adaptive Control and Signal Processing, 2014, 28(6): 536-549.

[9] WANG H, LIU S. Robust model predictive control for water distribution networks: A review[J]. Water Resources Management, 2021, 35(4): 1107-1125.

[10] GROSSO J M, OCAMPO-MARTINEZ C, PUIG V. Robust model predictive control for water management[M]//Real-time Monitoring and Control of Water Distribution Systems. London: IWA Publishing, 2017: 145-168.

[11] LIMON D, ALAMO T, RAIMONDO D M, et al. Input-to-state stability: A unifying framework for robust model predictive control[M]//Nonlinear Model Predictive Control. Berlin: Springer, 2009: 1-26.

[12] FARINA M, GIULIONI L, MAGNI L, et al. An approach to output-feedback MPC of stochastic linear discrete-time systems[J]. Automatica, 2016, 65: 140-149.

</ama-doc>
