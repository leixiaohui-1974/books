<ama-doc>
# 第四部分 模型预测控制

## 第4节 分布式模型预测控制

### 4.4.1 引言

分布式模型预测控制（Distributed Model Predictive Control, DMPC）是应对大规模系统控制挑战的重要方法。随着水系统规模的不断扩大和复杂性的日益增加，集中式MPC面临着计算复杂度爆炸、通信负担沉重、可靠性降低等瓶颈问题。DMPC通过将大规模系统分解为若干子系统，由各子系统基于局部信息并行求解优化问题，并通过协调机制实现全局优化，为大规模水系统的实时控制提供了可行方案[1]。

DMPC的研究始于21世纪初，由Jia、Krogh、Camponogara等学者奠定了理论基础[2]。经过二十余年的发展，DMPC已形成包括非合作式、合作式、基于纳什均衡、基于价格协调等多种架构的完整体系。在水系统控制中，DMPC被广泛应用于多区域供水管网、跨流域调水系统、分布式污水处理等场景。

DMPC的核心优势在于：计算任务分布化，降低单点计算负担；通信需求局部化，减少网络带宽占用；系统模块化，便于扩展和维护；容错能力强，单点故障不影响全局。这些特性使其特别适合地理分布广泛、子系统众多的水系统控制应用。

### 4.4.2 分布式系统建模

#### 4.4.2.1 系统分解与耦合结构

考虑由$M$个子系统组成的大规模系统，每个子系统$i$的动态为：

$$x_i(k+1) = f_i(x_i(k), u_i(k), w_i(k)) \tag{4.4.1}$$
$$y_i(k) = h_i(x_i(k), u_i(k)) \tag{4.4.2}$$

其中，$x_i \in \mathbb{R}^{n_i}$、$u_i \in \mathbb{R}^{m_i}$、$y_i \in \mathbb{R}^{p_i}$分别为子系统$i$的状态、输入和输出，$w_i$为来自其他子系统的耦合变量。

耦合关系可表示为：

$$w_i(k) = \sum_{j \in \mathcal{N}_i} g_{ij}(x_j(k), u_j(k)) \tag{4.4.3}$$

其中，$\mathcal{N}_i$为子系统$i$的邻居集合，$g_{ij}$为耦合函数。

在水系统中，典型的耦合形式包括：

**流量耦合：** 相邻区域通过管道连接，流量相互影响
$$Q_{ij} = f(H_i, H_j, R_{ij}) \tag{4.4.4}$$

**水质耦合：** 上游区域出水影响下游区域水质
$$C_{down} = \frac{Q_{up}C_{up} + Q_{local}C_{local}}{Q_{up} + Q_{local}} \tag{4.4.5}$$

**水力耦合：** 共享水源或水库的多个区域需协调取水

#### 4.4.2.2 图论表示

分布式系统的拓扑结构可用图$\mathcal{G} = (\mathcal{V}, \mathcal{E})$表示，其中：

- 顶点集$\mathcal{V} = \{1, 2, \ldots, M\}$代表子系统
- 边集$\mathcal{E} \subseteq \mathcal{V} \times \mathcal{V}$代表子系统间的耦合关系

邻接矩阵$A \in \mathbb{R}^{M \times M}$定义为：

$$A_{ij} = \begin{cases} 1, & \text{if } (i, j) \in \mathcal{E} \\ 0, & \text{otherwise} \end{cases} \tag{4.4.6}$$

拉普拉斯矩阵$L = D - A$，其中$D$为度矩阵。

### 4.4.3 分布式MPC架构

#### 4.4.3.1 非合作式DMPC

非合作式DMPC（Non-cooperative DMPC）中，各子系统独立优化自身目标，不考虑对其他子系统的影响[3]。

子系统$i$的局部优化问题：

$$\min_{\mathbf{u}_i} J_i = \sum_{t=0}^{N-1} l_i(x_{i,t}, u_{i,t}) + V_{f,i}(x_{i,N}) \tag{4.4.7}$$

$$\text{s.t.} \quad x_{i,t+1} = f_i(x_{i,t}, u_{i,t}, w_{i,t}) \tag{4.4.8}$$
$$x_{i,t} \in \mathbb{X}_i, \quad u_{i,t} \in \mathbb{U}_i \tag{4.4.9}$$

其中，耦合变量$w_{i,t}$假设为已知（通常采用前一迭代或前一时刻的值）。

非合作式DMPC的优点是计算简单、通信量小；缺点是可能产生冲突控制，全局性能次优。

#### 4.4.3.2 合作式DMPC

合作式DMPC（Cooperative DMPC）中，各子系统优化全局目标函数，通过协调实现整体最优[4]。

全局目标函数：

$$J = \sum_{i=1}^{M} J_i \tag{4.4.10}$$

各子系统求解：

$$\min_{\mathbf{u}_i} J_i + \sum_{j \in \mathcal{N}_i} \lambda_{ij}^T (w_{ij} - g_{ij}(x_j, u_j)) \tag{4.4.11}$$

其中，$\lambda_{ij}$为拉格朗日乘子，用于协调子系统间的耦合约束。

#### 4.4.3.3 基于纳什均衡的DMPC

纳什均衡DMPC将各子系统的交互建模为非合作博弈，寻求纳什均衡解[5]。

定义子系统$i$的最优响应映射：

$$\mathcal{R}_i(\mathbf{u}_{-i}) = \arg\min_{\mathbf{u}_i} J_i(\mathbf{u}_i, \mathbf{u}_{-i}) \tag{4.4.12}$$

其中，$\mathbf{u}_{-i}$表示除子系统$i$外其他子系统的控制序列。

纳什均衡满足：

$$\mathbf{u}_i^* = \mathcal{R}_i(\mathbf{u}_{-i}^*), \quad \forall i = 1, \ldots, M \tag{4.4.13}$$

即任何子系统单独改变策略都无法进一步降低自身代价。

### 4.4.4 协调算法

#### 4.4.4.1 对偶分解与次梯度法

对偶分解通过引入拉格朗日乘子将耦合约束分解到各子系统[6]。

耦合约束：

$$\sum_{i=1}^{M} A_i x_i = b \tag{4.4.14}$$

拉格朗日函数：

$$L(\mathbf{x}, \lambda) = \sum_{i=1}^{M} f_i(x_i) + \lambda^T (\sum_{i=1}^{M} A_i x_i - b) \tag{4.4.15}$$

对偶问题：

$$\max_{\lambda} \quad q(\lambda) = \sum_{i=1}^{M} q_i(\lambda) \tag{4.4.16}$$

其中，$q_i(\lambda) = \min_{x_i} [f_i(x_i) + \lambda^T A_i x_i]$。

次梯度法更新乘子：

$$\lambda^{k+1} = \lambda^k + \alpha_k (\sum_{i=1}^{M} A_i x_i(\lambda^k) - b) \tag{4.4.17}$$

#### 4.4.4.2 交替方向乘子法（ADMM）

ADMM结合对偶分解和增广拉格朗日方法，具有更好的收敛性[7]。

增广拉格朗日函数：

$$L_\rho(x, z, \lambda) = f(x) + g(z) + \lambda^T (Ax + Bz - c) + \frac{\rho}{2}\|Ax + Bz - c\|^2 \tag{4.4.18}$$

ADMM迭代：

$$x^{k+1} = \arg\min_x L_\rho(x, z^k, \lambda^k) \tag{4.4.19}$$
$$z^{k+1} = \arg\min_z L_\rho(x^{k+1}, z, \lambda^k) \tag{4.4.20}$$
$$\lambda^{k+1} = \lambda^k + \rho(Ax^{k+1} + Bz^{k+1} - c) \tag{4.4.21}$$

ADMM的优势在于分解后的子问题通常更易求解，且收敛速度较快。

#### 4.4.4.3 预测协调法

预测协调法（Prediction-Driven Coordination）通过交换预测轨迹实现协调[8]。

算法流程：

1. **初始化**：各子系统独立求解局部MPC，获得初始预测轨迹

2. **信息交换**：子系统间交换预测的状态和控制轨迹

3. **耦合更新**：基于接收的邻居预测，更新耦合变量估计

4. **局部优化**：各子系统重新求解局部MPC

5. **收敛判断**：若预测轨迹变化小于阈值，停止；否则返回步骤2

### 4.4.5 稳定性与收敛性分析

#### 4.4.5.1 稳定性条件

DMPC的稳定性分析需考虑子系统间的耦合影响[9]。

假设各子系统满足局部稳定性条件：存在Lyapunov函数$V_i$使得：

$$V_i(x_i^+) - V_i(x_i) \leq -l_i(x_i, u_i) + \sum_{j \in \mathcal{N}_i} \gamma_{ij} V_j(x_j) \tag{4.4.22}$$

其中，$\gamma_{ij}$为耦合强度系数。

全局稳定性要求耦合矩阵$\Gamma = [\gamma_{ij}]$满足稳定性条件（如谱半径小于1）。

#### 4.4.5.2 迭代收敛性

协调算法的收敛性取决于：

- 目标函数的凸性
- 耦合约束的结构
- 步长或惩罚参数的选择

对于凸问题，次梯度法和ADMM保证收敛到最优解；对于非凸问题，通常只能保证收敛到局部最优或稳定点。

#### 4.4.5.3 可行性保证

DMPC需确保各子系统优化问题的可行性。常用策略包括：

**终端集设计：** 各子系统的终端集需考虑耦合影响

**约束紧缩：** 预留裕度以容纳邻居子系统的影响

**可行性恢复：** 当局部问题不可行时，采用松弛或备用策略

### 4.4.6 DMPC在水系统中的应用

#### 4.4.6.1 多区域供水管网控制

大型城市供水管网通常划分为多个压力区或DMA（District Metered Area），各区域通过DMPC协调控制[10]。

区域$i$的局部模型：

$$h_i(k+1) = A_i h_i(k) + B_i u_i(k) + E_i d_i(k) + \sum_{j \in \mathcal{N}_i} F_{ij} h_j(k) \tag{4.4.23}$$

其中，$h_i$为区域$i$的关键节点压力，$u_i$为区域泵站控制，$F_{ij}$为区域间耦合矩阵。

协调目标：
- 维持各区域压力在服务范围内
- 最小化全局能耗
- 平衡区域间负荷

#### 4.4.6.2 跨流域调水系统

跨流域调水系统涉及多个水源、多个受水区，需协调各水库和泵站的运行[11]。

系统结构：
- 水源水库：$\{R_1, R_2, \ldots, R_{M_s}\}$
- 受水区：$\{D_1, D_2, \ldots, D_{M_d}\}$
- 输水线路：连接水源和受水区的管网

DMPC架构：
- 各水源水库作为独立子系统
- 各受水区作为独立子系统
- 通过协调算法优化全局水资源配置

#### 4.4.6.3 分布式污水处理系统

分布式污水处理系统包含多个处理厂，各厂处理能力和排放要求不同，需协调运行[12]。

子系统模型（处理厂$i$）：

$$x_{i,bio}(k+1) = f_{bio}(x_{i,bio}(k), Q_{i,in}(k), u_{i,aer}(k)) \tag{4.4.24}$$

协调变量：
- 进水流量分配$Q_{i,in}$
- 污泥交换量
- 出水水质指标

### 4.4.7 通信与同步机制

#### 4.4.7.1 通信拓扑

DMPC的通信拓扑可分为：

**全连接：** 所有子系统直接通信，信息传递快但通信量大

**邻居通信：** 仅相邻子系统通信，通信量小但信息传递慢

**分层通信：** 引入协调层，子系统与协调器通信

#### 4.4.7.2 同步与异步更新

**同步DMPC：** 所有子系统在同一时刻完成计算并交换信息，便于理论分析但可能产生等待

**异步DMPC：** 各子系统按自身节奏更新，提高资源利用率但分析更复杂

异步更新规则：

$$x_i(k+1) = \begin{cases} \mathcal{R}_i(x_{\mathcal{N}_i}(\tau_{j}^i(k))), & \text{if } i \in \mathcal{S}(k) \\ x_i(k), & \text{otherwise} \end{cases} \tag{4.4.25}$$

其中，$\mathcal{S}(k)$为时刻$k$更新的子系统集合，$\tau_{j}^i(k)$为子系统$i$获取子系统$j$信息的时刻。

### 4.4.8 小结

分布式模型预测控制为大规模水系统的实时优化控制提供了有效的技术途径。通过系统分解、并行优化和协调机制，DMPC在保持MPC约束处理和多目标优化能力的同时，克服了集中式架构的计算和通信瓶颈。

DMPC的核心在于平衡局部自主性与全局协调性。非合作式、合作式、纳什均衡等不同架构代表了不同的权衡策略，适用于不同的应用场景。对偶分解、ADMM、预测协调等算法为子系统间的协调提供了数学工具。

在水系统控制中，DMPC已成功应用于多区域供水管网、跨流域调水、分布式污水处理等场景。其分布式特性与水系统的地理分布特征高度契合，为智慧水务的建设提供了重要支撑。

未来发展方向包括：考虑通信延迟和丢包的鲁棒DMPC、基于事件触发的异步DMPC、与机器学习结合的数据驱动DMPC，以及面向网络攻击的安全DMPC等。

## 参考文献

[1] SCATTOLINI R. Architectures for distributed and hierarchical model predictive control—A review[J]. Journal of Process Control, 2009, 19(5): 723-731.

[2] CAMPONOGARA E, JIA D, KROGH B H, et al. Distributed model predictive control[J]. IEEE Control Systems Magazine, 2002, 22(1): 44-52.

[3] DUNBAR W B. Distributed receding horizon control of dynamically coupled nonlinear systems[J]. IEEE Transactions on Automatic Control, 2007, 52(7): 1249-1263.

[4] STEWART B T, VENKAT A N, RAWLINGS J B, et al. Cooperative distributed model predictive control[J]. Systems & Control Letters, 2010, 59(8): 460-469.

[5] MAESTRE J M, MUÑOZ DE LA PEÑA D, CAMACHO E F. Distributed model predictive control based on a cooperative game[J]. Optimal Control Applications and Methods, 2011, 32(2): 153-176.

[6] BOYD S, PARIKH N, CHU E, et al. Distributed optimization and statistical learning via the alternating direction method of multipliers[J]. Foundations and Trends in Machine Learning, 2011, 3(1): 1-122.

[7] BOYD S, VANDENBERGHE L. Convex Optimization[M]. Cambridge: Cambridge University Press, 2004.

[8] TRODDEN P, RICHARDS A. Distributed model predictive control of linear systems with persistent disturbances[J]. International Journal of Control, 2010, 83(8): 1653-1663.

[9] RAIMONDO D M, MAGNI L, SCATTOLINI R. Decentralized MPC of nonlinear systems: An input-to-state stability approach[J]. International Journal of Robust and Nonlinear Control, 2007, 17(17): 1651-1667.

[10] OCAMPO-MARTINEZ C, BARCELLI D, PUIG V. Partitioning approach oriented to the decentralised predictive control of large-scale systems[J]. Journal of Process Control, 2012, 22(8): 1356-1368.

[11] ZHENG X, LI H. Distributed model predictive control for multi-interconnected-basin water resources systems[J]. Water Resources Management, 2018, 32(14): 4589-4605.

[12] ZENG J, LIU J. Distributed model predictive control for wastewater systems with adaptive cooperation[J]. Water Research, 2015, 83: 120-133.

</ama-doc>
