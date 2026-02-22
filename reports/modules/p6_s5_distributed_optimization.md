<ama-doc>

# 22. 分布式优化

## 22.1 引言

水系统的优化控制涉及大量决策变量和复杂约束条件，传统集中式优化方法面临计算复杂度高、通信开销大、隐私保护难等问题。分布式优化（Distributed Optimization）通过将全局优化问题分解为多个子问题，在本地求解并通过邻居间信息交换协调，为大规模水系统的实时优化提供了有效途径。本章将系统介绍分布式优化的理论基础、核心算法及其在水系统控制中的应用。

## 22.2 分布式优化的数学基础

### 22.2.1 问题描述

考虑如下优化问题[1]：

$$\min_{x} \sum_{i=1}^{N} f_i(x) \quad \text{s.t.} \quad x \in \mathcal{X}$$

其中 $f_i: \mathbb{R}^n \rightarrow \mathbb{R}$ 是第 $i$ 个节点的局部目标函数，$\mathcal{X} \subseteq \mathbb{R}^n$ 是约束集合。

在集中式方法中，需要一个中心节点收集所有 $f_i$ 并求解整个问题。分布式方法中，每个节点 $i$ 仅知道 $f_i$，通过局部计算和邻居通信协作求解全局问题。

### 22.2.2 可分离问题结构

许多水系统优化问题具有可分离结构：

$$\min_{\{x_i\}} \sum_{i=1}^{N} f_i(x_i) \quad \text{s.t.} \quad \sum_{i=1}^{N} A_i x_i = b, \quad x_i \in \mathcal{X}_i$$

其中 $x_i$ 是节点 $i$ 的局部决策变量，耦合约束 $\sum_{i=1}^{N} A_i x_i = b$ 表示资源平衡或网络连接关系。

### 22.2.3 对偶分解

对偶分解是解决可分离优化问题的经典方法。构造拉格朗日函数：

$$L(x, \lambda) = \sum_{i=1}^{N} f_i(x_i) + \lambda^T(\sum_{i=1}^{N} A_i x_i - b)$$

其中 $\lambda$ 是拉格朗日乘子（对偶变量）。

对偶函数：

$$g(\lambda) = \inf_{x_i \in \mathcal{X}_i} L(x, \lambda) = \sum_{i=1}^{N} \inf_{x_i \in \mathcal{X}_i} [f_i(x_i) + \lambda^T A_i x_i] - \lambda^T b$$

对偶问题分解为 $N$ 个独立的子问题：

$$\min_{x_i \in \mathcal{X}_i} f_i(x_i) + \lambda^T A_i x_i, \quad i = 1, ..., N$$

通过对偶上升法更新乘子：

$$\lambda^{k+1} = \lambda^k + \alpha^k (\sum_{i=1}^{N} A_i x_i(\lambda^k) - b)$$

其中 $\alpha^k$ 是步长。

## 22.3 交替方向乘子法（ADMM）

### 22.3.1 ADMM基本原理

交替方向乘子法（Alternating Direction Method of Multipliers, ADMM）是求解分布式优化问题的强大工具，结合了对偶分解和增广拉格朗日方法的优点[2]。

考虑如下问题：

$$\min_{x,z} f(x) + g(z) \quad \text{s.t.} \quad Ax + Bz = c$$

增广拉格朗日函数：

$$L_{\rho}(x, z, \lambda) = f(x) + g(z) + \lambda^T(Ax + Bz - c) + \frac{\rho}{2}||Ax + Bz - c||^2$$

其中 $\rho > 0$ 是惩罚参数。

ADMM迭代步骤：

$$x^{k+1} = \arg\min_x L_{\rho}(x, z^k, \lambda^k)$$

$$z^{k+1} = \arg\min_z L_{\rho}(x^{k+1}, z, \lambda^k)$$

$$\lambda^{k+1} = \lambda^k + \rho(Ax^{k+1} + Bz^{k+1} - c)$$

### 22.3.2 共识ADMM

对于共识优化问题：

$$\min_{x} \sum_{i=1}^{N} f_i(x)$$

引入局部变量 $x_i$ 和一致性约束 $x_i = z$：

$$\min_{\{x_i\}, z} \sum_{i=1}^{N} f_i(x_i) \quad \text{s.t.} \quad x_i = z, \quad i = 1, ..., N$$

共识ADMM迭代[3]：

$$x_i^{k+1} = \arg\min_{x_i} f_i(x_i) + (\lambda_i^k)^T(x_i - \bar{x}^k) + \frac{\rho}{2}||x_i - \bar{x}^k||^2$$

$$\bar{x}^{k+1} = \frac{1}{N}\sum_{i=1}^{N} x_i^{k+1}$$

$$\lambda_i^{k+1} = \lambda_i^k + \rho(x_i^{k+1} - \bar{x}^{k+1})$$

其中 $\bar{x}$ 是共识变量。

### 22.3.3 分布式ADMM

在分布式网络中，每个节点只与邻居通信。共识约束变为 $x_i = x_j$ 对所有边 $(i,j) \in E$。

边共识ADMM[4]：

$$x_i^{k+1} = \arg\min_{x_i} f_i(x_i) + \sum_{j \in \mathcal{N}_i} [(\lambda_{ij}^k)^T x_i + \frac{\rho}{2}||x_i - (x_i^k + x_j^k)/2||^2]$$

$$\lambda_{ij}^{k+1} = \lambda_{ij}^k + \frac{\rho}{2}(x_i^{k+1} - x_j^{k+1})$$

分布式ADMM只需要邻居间通信，适合大规模网络应用。

## 22.4 分布式梯度方法

### 22.4.1 分布式梯度下降

对于无约束优化问题，分布式梯度下降（DGD）是一种简单的分布式算法[5]。

每个节点维护一个局部估计 $x_i^k$，迭代更新：

$$x_i^{k+1} = \sum_{j=1}^{N} w_{ij} x_j^k - \alpha^k \nabla f_i(x_i^k)$$

其中 $w_{ij}$ 是共识权重，$\alpha^k$ 是步长。

矩阵形式：

$$x^{k+1} = Wx^k - \alpha^k \nabla f(x^k)$$

其中 $W$ 是双随机权重矩阵。

**收敛条件**：当步长满足 $\sum_{k=0}^{\infty} \alpha^k = \infty$ 和 $\sum_{k=0}^{\infty} (\alpha^k)^2 < \infty$ 时，DGD收敛到最优解。

### 22.4.2 分布式随机梯度下降

当目标函数是期望形式 $f_i(x) = \mathbb{E}_{\xi}[F_i(x, \xi)]$ 或大规模求和形式时，采用随机梯度下降提高效率。

分布式SGD迭代：

$$x_i^{k+1} = \sum_{j \in \mathcal{N}_i} w_{ij} x_j^k - \alpha^k g_i(x_i^k, \xi_i^k)$$

其中 $g_i(x_i^k, \xi_i^k)$ 是随机梯度估计。

### 22.4.3 加速分布式算法

为提高收敛速度，发展了多种加速技术：

**EXTRA**：使用梯度差分校正共识误差[6]：

$$x^{k+1} = (I + W)x^k - \tilde{W}x^{k-1} - \alpha[\nabla f(x^k) - \nabla f(x^{k-1})]$$

**DIGing**：采用梯度跟踪技术：

$$y_i^{k+1} = \sum_{j=1}^{N} w_{ij} y_j^k + \nabla f_i(x_i^{k+1}) - \nabla f_i(x_i^k)$$

$$x_i^{k+1} = \sum_{j=1}^{N} w_{ij} x_j^k - \alpha y_i^k$$

**Nesterov加速**：引入动量项加速收敛：

$$v_i^{k+1} = \beta v_i^k + \sum_{j=1}^{N} w_{ij} x_j^k - x_i^k - \alpha \nabla f_i(x_i^k)$$

$$x_i^{k+1} = x_i^k + v_i^{k+1}$$

## 22.5 水系统分布式优化应用

### 22.5.1 供水管网压力优化

供水管网压力优化目标是最小化泵站能耗同时满足压力约束[7]：

$$\min_{h} \sum_{i \in \mathcal{P}} c_i q_i(h_i^{in} - h_i^{out})$$

$$\text{s.t.} \quad Aq = d$$

$$h_j^{min} \leq h_j \leq h_j^{max}, \quad \forall j \in \mathcal{J}$$

其中 $h$ 是节点水头，$q$ 是管段流量，$\mathcal{P}$ 是泵站集合，$\mathcal{J}$ 是节点集合，$d$ 是节点需水量。

**分布式求解**：
- 每个管网区域维护局部水头估计
- 区域间通过边界节点水头协调
- 采用ADMM迭代求解，邻居区域交换边界信息

### 22.5.2 多水源供水优化

多水源供水系统的成本优化问题：

$$\min_{\{q_i\}} \sum_{i=1}^{N} C_i(q_i)$$

$$\text{s.t.} \quad \sum_{i=1}^{N} q_i = D$$

$$q_i^{min} \leq q_i \leq q_i^{max}$$

其中 $C_i(q_i)$ 是水源 $i$ 的供水成本，$D$ 是总需求。

**分布式求解**：
- 各水源智能体维护对边际成本的估计 $\lambda_i$
- 通过共识协议协调边际成本趋于一致
- 根据协调后的边际成本确定供水量

迭代公式：

$$q_i^{k+1} = \arg\min_{q_i} C_i(q_i) - \lambda_i^k q_i$$

$$\lambda_i^{k+1} = \sum_{j \in \mathcal{N}_i} w_{ij} \lambda_j^k + \alpha(\sum_{i=1}^{N} q_i^k - D)$$

### 22.5.3 水质优化控制

水质优化控制需要协调消毒剂投加和管网水力条件：

$$\min_{u} \sum_{t=1}^{T} [\sum_{i \in \mathcal{S}} c_i u_i(t) + \sum_{j \in \mathcal{J}} w_j(c_j(t) - c^{target})^2]$$

$$\text{s.t.} \quad c(t+1) = f(c(t), u(t), q(t))$$

$$c^{min} \leq c_j(t) \leq c^{max}$$

其中 $u_i(t)$ 是水源 $i$ 的消毒剂投加量，$c_j(t)$ 是节点 $j$ 的余氯浓度。

**分布式模型预测控制**：
- 将管网划分为多个控制区域
- 各区域求解局部MPC问题
- 通过协调变量（边界浓度）实现区域间一致性

## 22.6 异步与在线分布式优化

### 22.6.1 异步分布式算法

实际系统中，各节点的计算和通信可能存在延迟。异步分布式算法允许节点以不同频率更新：

$$x_i^{k+1} = \sum_{j=1}^{N} w_{ij} \hat{x}_j^k - \alpha \nabla f_i(\hat{x}_i^k)$$

其中 $\hat{x}_j^k$ 是节点 $i$ 对节点 $j$ 状态的最新了解，可能滞后于当前迭代。

**收敛条件**：当延迟有界时，异步算法仍能收敛到最优解[8]。

### 22.6.2 在线分布式优化

当目标函数随时间变化时，需要在线分布式优化：

$$\min_{x} \sum_{t=1}^{T} \sum_{i=1}^{N} f_i^t(x)$$

在线梯度下降：

$$x_i^{t+1} = \sum_{j=1}^{N} w_{ij} x_j^t - \alpha \nabla f_i^t(x_i^t)$$

**遗憾界（Regret Bound）**：算法的性能通过遗憾衡量：

$$R_T = \sum_{t=1}^{T} \sum_{i=1}^{N} f_i^t(x_i^t) - \min_{x} \sum_{t=1}^{T} \sum_{i=1}^{N} f_i^t(x)$$

良好的在线算法具有次线性遗憾 $R_T = o(T)$。

### 22.6.3 事件触发分布式优化

为减少通信开销，采用事件触发机制：

$$||x_i^k - x_i^{last}|| > \epsilon \Rightarrow \text{广播更新}$$

只有当本地变量变化超过阈值时才与邻居通信，显著降低通信负担[9]。

## 22.7 隐私保护分布式优化

### 22.7.1 差分隐私

在分布式优化中，节点的目标函数可能包含敏感信息。差分隐私技术可以在保护隐私的同时实现优化[10]：

$$x_i^{k+1} = \sum_{j=1}^{N} w_{ij} x_j^k - \alpha(\nabla f_i(x_i^k) + \eta_i^k)$$

其中 $\eta_i^k$ 是精心设计的噪声，提供差分隐私保证。

### 22.7.2 安全多方计算

安全多方计算（SMC）允许多方在不泄露私有输入的情况下协作计算：

- 同态加密：在加密数据上直接计算
- 秘密共享：将数据分割为份额分发给多方
- 混淆电路：将计算表示为布尔电路进行安全求值

### 22.7.3 联邦学习框架

联邦学习是一种隐私保护的分布式机器学习框架，可应用于水系统数据驱动的优化：

- 各节点在本地数据上训练模型
- 只共享模型参数（而非原始数据）
- 聚合服务器协调全局模型更新

## 22.8 本章小结

本章系统阐述了分布式优化的理论基础和算法设计。分布式优化通过将全局问题分解为局部子问题，在保护隐私和降低通信开销的同时实现大规模系统的协同优化。对偶分解和ADMM提供了处理耦合约束的通用框架，分布式梯度方法适用于无约束和大规模问题。

在水系统应用中，分布式优化已成功应用于管网压力优化、多水源协调、水质控制等场景。异步、在线和事件触发算法提高了算法的实用性和效率。隐私保护技术确保了敏感数据的安全。

随着水系统规模的扩大和智能化需求的提升，分布式优化将成为水系统实时优化控制的核心技术。未来的发展方向包括与深度学习的结合、非凸问题的处理、以及更加高效的通信机制设计。

## 参考文献

[1] BERTSEKAS D P, TSITSIKLIS J N. Parallel and distributed computation: Numerical methods[M]. Prentice Hall, 1989.

[2] BOYD S, PARIKH N, CHU E, et al. Distributed optimization and statistical learning via the alternating direction method of multipliers[J]. Foundations and Trends in Machine Learning, 2011, 3(1): 1-122.

[3] SCHIZAS I D, RIBEIRO A, GIANNAKIS G B. Consensus in ad hoc WSNs with noisy links—Part I: Distributed estimation of deterministic signals[J]. IEEE Transactions on Signal Processing, 2008, 56(1): 350-364.

[4] WEI E, OZDAGLAR A. Distributed alternating direction method of multipliers[C]//2012 IEEE 51st IEEE Conference on Decision and Control (CDC). IEEE, 2012: 5445-5450.

[5] NEDIC A, OZDAGLAR A. Distributed subgradient methods for multi-agent optimization[J]. IEEE Transactions on Automatic Control, 2009, 54(1): 48-61.

[6] SHI W, LING Q, WU G, et al. EXTRA: An exact first-order algorithm for decentralized consensus optimization[J]. SIAM Journal on Optimization, 2015, 25(2): 944-966.

[7] PULEO V, et al. Optimal design of pressure-constrained water distribution networks using a multi-objective genetic algorithm[J]. Procedia Engineering, 2014, 70: 912-921.

[8] TSITSIKLIS J N, BERTSEKAS D P, ATHANS M. Distributed asynchronous deterministic and stochastic gradient optimization algorithms[J]. IEEE Transactions on Automatic Control, 1986, 31(9): 803-812.

[9] LIU Y, LI B. Event-triggered distributed optimization for multi-agent systems[J]. IEEE Transactions on Automatic Control, 2020, 65(12): 5362-5369.

[10] ZHANG T, ZHU Q. Dynamic differential privacy for ADMM-based distributed classification learning[J]. IEEE Transactions on Information Forensics and Security, 2022, 12(1): 172-187.

[11] NEDIC A, OLSHEVSKY A, SHI W. Achieving geometric convergence for distributed optimization over time-varying graphs[J]. SIAM Journal on Optimization, 2017, 27(4): 2597-2633.

[12] QU G, LI N. Harnessing smoothness to accelerate distributed optimization[J]. IEEE Transactions on Control of Network Systems, 2018, 5(3): 1245-1260.

</ama-doc>
