<ama-doc>

# 5.5 状态估计与故障检测

## 5.5.1 引言

状态估计与故障检测是自主水系统控制的核心技术支撑。由于传感器数量限制、测量噪声、通信延迟等因素，水系统的完整状态往往无法直接测量获得。状态估计技术通过融合多源信息，重构系统的内部状态，为控制决策提供准确的状态反馈[1]。故障检测技术则通过分析系统行为的异常模式，及时发现传感器、执行器或过程本身的故障，为容错控制和安全保护提供依据。

在水系统控制中，状态估计面临独特的挑战：系统动态通常由复杂的偏微分方程描述（如圣维南方程），具有分布式、非线性、时变的特点；测量数据稀疏且采样频率不一；外部扰动（降雨、需水）具有高度不确定性。这些特点要求状态估计方法既要保证估计精度，又要满足实时性要求。

## 5.5.2 状态估计基础理论

### 5.5.2.1 状态估计问题描述

考虑离散时间动态系统：

$$\mathbf{x}_{k+1} = \mathbf{f}(\mathbf{x}_k, \mathbf{u}_k, \mathbf{w}_k)$$
$$\mathbf{y}_k = \mathbf{h}(\mathbf{x}_k, \mathbf{v}_k)$$

其中 $\mathbf{x}_k \in \mathbb{R}^n$ 是状态向量，$\mathbf{u}_k$ 是控制输入，$\mathbf{y}_k \in \mathbb{R}^m$ 是测量输出，$\mathbf{w}_k$ 和 $\mathbf{v}_k$ 分别是过程噪声和测量噪声。

状态估计的目标是：给定测量序列 $\mathbf{y}_{0:k} = \{\mathbf{y}_0, \mathbf{y}_1, \ldots, \mathbf{y}_k\}$ 和控制序列 $\mathbf{u}_{0:k-1}$，估计当前状态 $\mathbf{x}_k$ 或状态序列 $\mathbf{x}_{0:k}$。

### 5.5.2.2 估计器性能指标

**无偏性**：估计误差的期望为零

$$E[\tilde{\mathbf{x}}_k] = E[\mathbf{x}_k - \hat{\mathbf{x}}_k] = 0$$

**一致性**：估计误差协方差与实际误差匹配

$$E[\tilde{\mathbf{x}}_k \tilde{\mathbf{x}}_k^T] = \mathbf{P}_k$$

**收敛性**：随着时间推移，估计误差趋于零

$$\lim_{k \to \infty} E[\|\tilde{\mathbf{x}}_k\|^2] = 0$$

**鲁棒性**：对模型不确定性和噪声统计特性变化不敏感

## 5.5.3 卡尔曼滤波及其扩展

### 5.5.3.1 标准卡尔曼滤波

对于线性系统：

$$\mathbf{x}_{k+1} = \mathbf{A}\mathbf{x}_k + \mathbf{B}\mathbf{u}_k + \mathbf{w}_k$$
$$\mathbf{y}_k = \mathbf{C}\mathbf{x}_k + \mathbf{v}_k$$

其中 $\mathbf{w}_k \sim \mathcal{N}(0, \mathbf{Q})$，$\mathbf{v}_k \sim \mathcal{N}(0, \mathbf{R})$，卡尔曼滤波提供最优线性无偏估计[2]。

**预测步骤**：

$$\hat{\mathbf{x}}_{k|k-1} = \mathbf{A}\hat{\mathbf{x}}_{k-1|k-1} + \mathbf{B}\mathbf{u}_{k-1}$$
$$\mathbf{P}_{k|k-1} = \mathbf{A}\mathbf{P}_{k-1|k-1}\mathbf{A}^T + \mathbf{Q}$$

**更新步骤**：

$$\mathbf{K}_k = \mathbf{P}_{k|k-1}\mathbf{C}^T(\mathbf{C}\mathbf{P}_{k|k-1}\mathbf{C}^T + \mathbf{R})^{-1}$$
$$\hat{\mathbf{x}}_{k|k} = \hat{\mathbf{x}}_{k|k-1} + \mathbf{K}_k(\mathbf{y}_k - \mathbf{C}\hat{\mathbf{x}}_{k|k-1})$$
$$\mathbf{P}_{k|k} = (\mathbf{I} - \mathbf{K}_k\mathbf{C})\mathbf{P}_{k|k-1}$$

### 5.5.3.2 扩展卡尔曼滤波（EKF）

对于非线性系统，扩展卡尔曼滤波通过局部线性化处理[3]：

$$\mathbf{A}_k = \left.\frac{\partial \mathbf{f}}{\partial \mathbf{x}}\right|_{\hat{\mathbf{x}}_{k|k}, \mathbf{u}_k}, \quad \mathbf{C}_k = \left.\frac{\partial \mathbf{h}}{\partial \mathbf{x}}\right|_{\hat{\mathbf{x}}_{k|k-1}}$$

**预测**：

$$\hat{\mathbf{x}}_{k|k-1} = \mathbf{f}(\hat{\mathbf{x}}_{k-1|k-1}, \mathbf{u}_{k-1})$$
$$\mathbf{P}_{k|k-1} = \mathbf{A}_{k-1}\mathbf{P}_{k-1|k-1}\mathbf{A}_{k-1}^T + \mathbf{Q}$$

**更新**：

$$\mathbf{K}_k = \mathbf{P}_{k|k-1}\mathbf{C}_k^T(\mathbf{C}_k\mathbf{P}_{k|k-1}\mathbf{C}_k^T + \mathbf{R})^{-1}$$
$$\hat{\mathbf{x}}_{k|k} = \hat{\mathbf{x}}_{k|k-1} + \mathbf{K}_k(\mathbf{y}_k - \mathbf{h}(\hat{\mathbf{x}}_{k|k-1}))$$

EKF适用于弱非线性系统，对于强非线性系统可能发散。

### 5.5.3.3 无迹卡尔曼滤波（UKF）

无迹卡尔曼滤波通过无迹变换（Unscented Transform）更准确地传播均值和协方差[4]。

**Sigma点生成**：

$$\mathcal{X}_0 = \hat{\mathbf{x}}, \quad W_0 = \frac{\kappa}{n+\kappa}$$
$$\mathcal{X}_i = \hat{\mathbf{x}} + (\sqrt{(n+\kappa)\mathbf{P}})_i, \quad W_i = \frac{1}{2(n+\kappa)}$$
$$\mathcal{X}_{i+n} = \hat{\mathbf{x}} - (\sqrt{(n+\kappa)\mathbf{P}})_i, \quad W_{i+n} = \frac{1}{2(n+\kappa)}$$

**预测**：

$$\mathcal{X}_{k|k-1}^* = \mathbf{f}(\mathcal{X}_{k-1}, \mathbf{u}_{k-1})$$
$$\hat{\mathbf{x}}_{k|k-1} = \sum_{i=0}^{2n} W_i \mathcal{X}_{i,k|k-1}^*$$
$$\mathbf{P}_{k|k-1} = \sum_{i=0}^{2n} W_i (\mathcal{X}_{i,k|k-1}^* - \hat{\mathbf{x}}_{k|k-1})(\cdot)^T + \mathbf{Q}$$

UKF避免了雅可比矩阵计算，对于非线性系统通常比EKF更精确。

### 5.5.3.4 集合卡尔曼滤波（EnKF）

集合卡尔曼滤波通过蒙特卡洛集合表示概率分布，适用于高维系统[5]：

**集合预测**：

$$\mathbf{x}_{k|k-1}^{(i)} = \mathbf{f}(\mathbf{x}_{k-1|k-1}^{(i)}, \mathbf{u}_{k-1}) + \mathbf{w}_k^{(i)}, \quad i = 1, \ldots, N_e$$

**集合更新**：

$$\bar{\mathbf{x}}_{k|k-1} = \frac{1}{N_e}\sum_{i=1}^{N_e} \mathbf{x}_{k|k-1}^{(i)}$$
$$\mathbf{P}_{k|k-1} = \frac{1}{N_e-1}\sum_{i=1}^{N_e}(\mathbf{x}_{k|k-1}^{(i)} - \bar{\mathbf{x}}_{k|k-1})(\cdot)^T$$

EnKF广泛应用于气象和水文数据同化，适合处理分布式水系统的高维状态估计问题。

## 5.5.4 粒子滤波

### 5.5.4.1 基本原理

粒子滤波通过一组带权粒子近似后验分布[6]：

$$p(\mathbf{x}_k | \mathbf{y}_{0:k}) \approx \sum_{i=1}^{N_p} w_k^{(i)} \delta(\mathbf{x}_k - \mathbf{x}_k^{(i)})$$

**重要性采样**：

从提议分布 $q(\mathbf{x}_k | \mathbf{x}_{k-1}, \mathbf{y}_k)$ 采样，权重更新：

$$w_k^{(i)} \propto w_{k-1}^{(i)} \frac{p(\mathbf{y}_k | \mathbf{x}_k^{(i)}) p(\mathbf{x}_k^{(i)} | \mathbf{x}_{k-1}^{(i)})}{q(\mathbf{x}_k^{(i)} | \mathbf{x}_{k-1}^{(i)}, \mathbf{y}_k)}$$

**重采样**：当有效粒子数 $N_{\text{eff}} = 1/\sum (w^{(i)})^2$ 低于阈值时进行重采样。

### 5.5.4.2 粒子滤波在水系统中的应用

粒子滤波适用于强非线性、非高斯噪声的水系统状态估计：
- 洪水演进估计
- 水质参数估计
- 极端事件状态跟踪

## 5.5.5 分布式状态估计

### 5.5.5.1 分布式估计架构

大型水系统通常采用分布式估计架构：

**集中式估计**：所有测量汇聚到中心节点进行全局估计
- 优点：全局最优
- 缺点：通信负担大、单点故障风险

**分散式估计**：各子系统独立进行本地估计
- 优点：通信简单、容错性好
- 缺点：忽略子系统间耦合

**分布式估计**：子系统本地估计+信息交换
- 平衡了最优性和可扩展性

### 5.5.5.2 分布式卡尔曼滤波

**一致性卡尔曼滤波**：各节点通过一致性协议交换信息

$$\hat{\mathbf{x}}_{k|k}^{(i)} = \hat{\mathbf{x}}_{k|k-1}^{(i)} + \mathbf{K}_k^{(i)}(\mathbf{y}_k^{(i)} - \mathbf{C}^{(i)}\hat{\mathbf{x}}_{k|k-1}^{(i)}) + \gamma \sum_{j \in \mathcal{N}_i}(\hat{\mathbf{x}}_{k|k}^{(j)} - \hat{\mathbf{x}}_{k|k}^{(i)})$$

## 5.5.6 故障检测原理

### 5.5.6.1 故障类型与建模

**传感器故障**：
- 偏差故障：$y_{\text{fault}} = y_{\text{true}} + b$
- 漂移故障：$y_{\text{fault}} = y_{\text{true}} + \alpha t$
- 精度退化：噪声方差增大
- 完全失效：$y_{\text{fault}} = \text{constant}$ 或随机值

**执行器故障**：
- 卡死故障：$u_{\text{fault}} = u_{\text{stuck}}$
- 增益变化：$u_{\text{fault}} = \alpha u_{\text{cmd}}$
- 部分失效：$u_{\text{fault}} = \alpha u_{\text{cmd}}, \alpha \in (0,1)$

**过程故障**：
- 泄漏：$Q_{\text{leak}} = C_d A \sqrt{2gH}$
- 堵塞：流量系数变化
- 结构损坏：系统参数变化

### 5.5.6.2 基于模型的故障检测

**残差生成**：

$$\mathbf{r}_k = \mathbf{y}_k - \mathbf{h}(\hat{\mathbf{x}}_{k|k-1})$$

无故障时，残差应接近零均值白噪声；故障时，残差呈现异常模式。

**检测逻辑**：

$$J = \mathbf{r}_k^T \mathbf{\Sigma}^{-1} \mathbf{r}_k \underset{H_0}{\overset{H_1}{\gtrless}} \eta$$

其中 $H_0$ 是无故障假设，$H_1$ 是有故障假设，$\eta$ 是检测阈值。

### 5.5.6.3 基于观测器的故障检测

**龙伯格观测器**：

$$\dot{\hat{\mathbf{x}}} = \mathbf{A}\hat{\mathbf{x}} + \mathbf{B}\mathbf{u} + \mathbf{L}(\mathbf{y} - \mathbf{C}\hat{\mathbf{x}})$$

残差动态：

$$\dot{\tilde{\mathbf{x}}} = (\mathbf{A} - \mathbf{L}\mathbf{C})\tilde{\mathbf{x}} + \mathbf{E}\mathbf{f}$$

通过适当设计 $\mathbf{L}$，使残差对特定故障敏感。

**未知输入观测器**：

设计观测器使残差对未知干扰解耦，仅对故障敏感：

$$\mathbf{T}\mathbf{E}_d = 0, \quad \mathbf{T}\mathbf{E}_f \neq 0$$

## 5.5.7 水系统状态估计应用

### 5.5.7.1 明渠水流状态估计

基于圣维南方程的明渠系统状态估计：

$$\frac{\partial A}{\partial t} + \frac{\partial Q}{\partial x} = 0$$
$$\frac{\partial Q}{\partial t} + \frac{\partial}{\partial x}\left(\frac{Q^2}{A}\right) + gA\frac{\partial h}{\partial x} = gA(S_0 - S_f)$$

采用集总参数模型或有限差分/有限元离散化，结合稀疏水位测量进行状态估计。

### 5.5.7.2 供水管网状态估计

供水管网状态估计问题：

**测量方程**：

$$\mathbf{z} = \mathbf{h}(\mathbf{x}) + \boldsymbol{\epsilon}$$

其中 $\mathbf{x}$ 包括节点压力、管段流量，$\mathbf{z}$ 包括压力测量、流量测量。

**加权最小二乘估计**：

$$\min_{\mathbf{x}} J = [\mathbf{z} - \mathbf{h}(\mathbf{x})]^T \mathbf{W} [\mathbf{z} - \mathbf{h}(\mathbf{x})]$$

### 5.5.7.3 水质状态估计

水质参数（余氯、浊度等）的时空分布估计：

**对流-扩散方程**：

$$\frac{\partial C}{\partial t} + \mathbf{v} \cdot \nabla C = \nabla \cdot (D \nabla C) - kC + S$$

结合有限的水质监测点数据，通过数据同化技术估计全网水质分布。

## 5.5.8 本章小结

状态估计与故障检测是自主水系统控制的关键支撑技术。本章主要内容包括：

1. **基础理论**：建立了状态估计问题的数学描述和性能评价体系。

2. **卡尔曼滤波**：系统介绍了标准KF、EKF、UKF和EnKF，为不同特性的水系统提供了估计工具选择。

3. **粒子滤波**：讨论了非线性非高斯情况下的状态估计方法。

4. **分布式估计**：介绍了大规模水系统的分布式状态估计架构和算法。

5. **故障检测**：阐述了基于模型和观测器的故障检测原理和方法。

6. **水系统应用**：针对明渠、管网、水质等典型应用场景进行了具体分析。

准确的状态估计和及时的故障检测是实现水系统高级控制功能的前提条件，对于提升系统安全性、可靠性和效率具有重要意义。

---

## 参考文献

[1] SIMON D. Optimal state estimation: Kalman, H infinity, and nonlinear approaches[M]. John Wiley & Sons, 2006.

[2] KALMAN R E. A new approach to linear filtering and prediction problems[J]. Journal of Basic Engineering, 1960, 82(1): 35-45.

[3] GELB A. Applied optimal estimation[M]. MIT Press, 1974.

[4] JULIER S J, UHLMANN J K. New extension of the Kalman filter to nonlinear systems[C]//Signal Processing, Sensor Fusion, and Target Recognition VI. SPIE, 1997, 3068: 182-193.

[5] EVENSEN G. Data assimilation: The ensemble Kalman filter[M]. Springer Science & Business Media, 2009.

[6] ARULAMPALAM M S, MASKELL S, GORDON N, et al. A tutorial on particle filters for online nonlinear/non-Gaussian Bayesian tracking[J]. IEEE Transactions on Signal Processing, 2002, 50(2): 174-188.

[7] KHAN A, MOAYED V. Employing extended Kalman filter for faulty sensor detection in water distribution systems[J]. Engineering Proceedings, 2024, 69(1): 28.

[8] PREIS A, OSTFELD A. A coupled model tree - genetic algorithm scheme for flow and water quality predictions in water distribution networks[J]. Water Resources Research, 2008, 44(9): W09408.

[9] SANDBERG C, BREKKE E, LUND E. Online state estimation in water distribution systems via sparse dictionary learning[J]. Water Research, 2024, 249: 120876.

[10] HUTTON C J, KAPELAN Z, VAMVAKERIDOU-LYROUDIA L, et al. Dealing with uncertainty in water distribution system models: A framework for real-time modeling and data assimilation[J]. Journal of Water Resources Planning and Management, 2014, 140(2): 169-183.

[11] ANDERSON B D O, MOORE J B. Optimal filtering[M]. Englewood Cliffs: Prentice-Hall, 1979.

[12] WAN E A, VAN DER MERWE R. The unscented Kalman filter for nonlinear estimation[C]//Proceedings of the IEEE 2000 Adaptive Systems for Signal Processing, Communications, and Control Symposium. IEEE, 2000: 153-158.

</ama-doc>
