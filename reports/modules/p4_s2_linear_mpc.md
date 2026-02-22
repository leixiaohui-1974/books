<ama-doc>
# 第四部分 模型预测控制

## 第2节 线性模型预测控制

### 4.2.1 引言

线性模型预测控制（Linear Model Predictive Control, LMPC）是MPC技术家族中最成熟、应用最广泛的分支。LMPC基于线性系统模型，在每个采样时刻求解一个凸优化问题（通常为二次规划），具有计算效率高、理论分析完备、工程实施便捷等显著优势[1]。在水系统控制领域，尽管水力过程本身具有非线性特征，但在工作点附近线性化或采用分段线性近似，LMPC仍能有效处理大多数实际控制问题。

LMPC的理论基础可追溯至20世纪60年代的最优控制理论，但其大规模工业应用始于20世纪80年代。Shell Oil公司的动态矩阵控制（DMC）和IDCOM（Identification and Command）是早期LMPC的代表性算法[2]。经过四十余年的发展，LMPC已形成包括无约束LQR、约束MPC、显式MPC等在内的完整技术体系，并催生了大量商业化软件产品。

在水系统控制中，LMPC的应用涵盖供水管网压力控制、水库优化调度、污水处理过程控制等多个方面。其成功应用的关键在于：水系统在工作点附近的小信号动态可近似为线性；约束条件（如水位上下限、泵站流量限制）可线性表示；优化目标（如能耗最小化）常具有二次形式[3]。

### 4.2.2 线性MPC的数学描述

#### 4.2.2.1 线性状态空间模型

考虑离散时间线性时不变系统：

$$x(k+1) = Ax(k) + Bu(k) \tag{4.2.1}$$
$$y(k) = Cx(k) + Du(k) \tag{4.2.2}$$

其中，$x \in \mathbb{R}^n$为状态向量，$u \in \mathbb{R}^m$为控制输入，$y \in \mathbb{R}^p$为输出向量，$A \in \mathbb{R}^{n \times n}$、$B \in \mathbb{R}^{n \times m}$、$C \in \mathbb{R}^{p \times n}$、$D \in \mathbb{R}^{p \times m}$为系统矩阵。

对于水系统，状态变量通常包括水库/水箱水位、管道流量、节点压力等；控制输入包括泵站转速、阀门开度等；输出变量为需要调节或监测的量。

#### 4.2.2.2 带约束的优化问题

线性MPC在每个采样时刻求解以下约束优化问题：

$$\min_{\mathbf{u}} J = \sum_{i=0}^{N-1} \left[ \|y_{k+i|k} - r_{k+i}\|_Q^2 + \|\Delta u_{k+i|k}\|_R^2 \right] + \|y_{k+N|k} - r_{k+N}\|_P^2 \tag{4.2.3}$$

其中，$r$为参考轨迹，$\Delta u(k) = u(k) - u(k-1)$为控制增量，$Q, R, P$为权重矩阵。

约束条件包括：

**输入约束：**
$$u_{min} \leq u_{k+i|k} \leq u_{max}, \quad i = 0, 1, \ldots, N-1 \tag{4.2.4}$$

**输入变化率约束：**
$$\Delta u_{min} \leq \Delta u_{k+i|k} \leq \Delta u_{max}, \quad i = 0, 1, \ldots, N-1 \tag{4.2.5}$$

**输出约束：**
$$y_{min} \leq y_{k+i|k} \leq y_{max}, \quad i = 1, 2, \ldots, N \tag{4.2.6}$$

**状态约束：**
$$x_{min} \leq x_{k+i|k} \leq x_{max}, \quad i = 1, 2, \ldots, N \tag{4.2.7}$$

### 4.2.3 二次规划问题 formulation

#### 4.2.3.1 预测方程推导

基于状态空间模型，未来状态的预测可表示为：

$$x_{k+1|k} = Ax_k + Bu_{k|k} \tag{4.2.8}$$
$$x_{k+2|k} = A^2x_k + ABu_{k|k} + Bu_{k+1|k} \tag{4.2.9}$$
$$\vdots$$
$$x_{k+N|k} = A^Nx_k + A^{N-1}Bu_{k|k} + \cdots + Bu_{k+N-1|k} \tag{4.2.10}$$

定义预测向量：

$$\mathbf{X} = \begin{bmatrix} x_{k+1|k} \\ x_{k+2|k} \\ \vdots \\ x_{k+N|k} \end{bmatrix}, \quad \mathbf{U} = \begin{bmatrix} u_{k|k} \\ u_{k+1|k} \\ \vdots \\ u_{k+N-1|k} \end{bmatrix} \tag{4.2.11}$$

则预测方程可紧凑表示为：

$$\mathbf{X} = \mathcal{A}x_k + \mathcal{B}\mathbf{U} \tag{4.2.12}$$

其中：

$$\mathcal{A} = \begin{bmatrix} A \\ A^2 \\ \vdots \\ A^N \end{bmatrix}, \quad \mathcal{B} = \begin{bmatrix} B & 0 & \cdots & 0 \\ AB & B & \cdots & 0 \\ \vdots & \vdots & \ddots & \vdots \\ A^{N-1}B & A^{N-2}B & \cdots & B \end{bmatrix} \tag{4.2.13}$$

#### 4.2.3.2 目标函数的二次形式

将预测方程代入目标函数，可得标准二次规划形式：

$$\min_{\mathbf{U}} \frac{1}{2}\mathbf{U}^T H \mathbf{U} + f^T \mathbf{U} \tag{4.2.14}$$

其中，Hessian矩阵$H$和梯度向量$f$为：

$$H = 2(\mathcal{B}^T \bar{Q} \mathcal{B} + \bar{R}) \tag{4.2.15}$$
$$f = 2\mathcal{B}^T \bar{Q}(\mathcal{A}x_k - \bar{r}) \tag{4.2.16}$$

这里，$\bar{Q}$和$\bar{R}$为扩展权重矩阵，$\bar{r}$为扩展参考向量。

#### 4.2.3.3 约束的矩阵表示

所有约束可统一表示为线性不等式形式：

$$G\mathbf{U} \leq w \tag{4.2.17}$$

其中，$G$和$w$由输入约束、状态约束和输出约束组合而成。对于输入变化率约束，需引入差分矩阵进行转换。

### 4.2.4 二次规划求解算法

#### 4.2.4.1 活跃集法

活跃集法（Active Set Method）是求解凸二次规划的经典算法[4]。其基本思想是在每次迭代中识别活跃约束集，将原问题转化为等式约束问题求解。

算法流程：

1. **初始化**：选择可行初始点$\mathbf{U}_0$，确定活跃约束集$\mathcal{W}_0$

2. **等式QP求解**：在当前活跃集下求解等式约束QP：
   $$\min_{\mathbf{U}} \frac{1}{2}\mathbf{U}^T H \mathbf{U} + f^T \mathbf{U}$$
   $$\text{s.t.} \quad g_i^T \mathbf{U} = w_i, \quad i \in \mathcal{W}_k$$

3. **约束检查**：若解满足所有非活跃约束，则接受；否则沿搜索方向进行线搜索，确定新的活跃约束

4. **收敛判断**：若KKT条件满足，算法终止；否则更新活跃集，返回步骤2

活跃集法的优点是解的精度高，适合中小规模问题；缺点是活跃集变化时计算量较大。

#### 4.2.4.2 内点法

内点法（Interior Point Method）通过引入障碍函数将不等式约束转化为等式约束，利用牛顿法迭代求解[5]。

原始-对偶内点法的KKT条件：

$$\begin{bmatrix} H & G^T & 0 \\ G & 0 & -I \\ 0 & S & \Lambda \end{bmatrix} \begin{bmatrix} \Delta \mathbf{U} \\ \Delta \lambda \\ \Delta s \end{bmatrix} = -\begin{bmatrix} r_H \\ r_G \\ r_{S\Lambda} \end{bmatrix} \tag{4.2.18}$$

其中，$S = \text{diag}(s)$，$\Lambda = \text{diag}(\lambda)$，$s$为松弛变量，$\lambda$为拉格朗日乘子。

内点法的优点是迭代次数对问题规模不敏感，适合大规模问题；缺点是每次迭代需求解大型线性方程组。

#### 4.2.4.3 快速QP求解器

对于MPC的实时应用，需采用专门的快速QP求解器[6]：

**qpOASES：** 基于在线活跃集策略，利用相邻QP问题的解作为热启动，显著减少迭代次数。

**OSQP：** 基于交替方向乘子法（ADMM），将QP问题分解为更简单的子问题并行求解。

**ECOS/PIQP：** 针对稀疏结构优化的内点法实现，适合大规模MPC问题。

**GPU加速求解：** 利用GPU并行计算能力加速矩阵运算，实现微秒级QP求解。

### 4.2.5 显式MPC

#### 4.2.5.1 多面体分区概念

显式MPC（Explicit MPC）通过离线计算将状态空间划分为多个多面体区域，在每个区域内控制律为状态的分段线性函数[7]：

$$u^*(x) = F_i x + g_i, \quad \text{if } x \in \mathcal{R}_i \tag{4.2.19}$$

其中，$\mathcal{R}_i = \{x : H_i x \leq h_i\}$为多面体区域。

在线运行时，只需确定当前状态所属区域，通过查表获得控制量，无需实时求解优化问题。

#### 4.2.5.2 离线计算与在线查表

离线阶段通过多参数规划（Multi-Parametric Programming）求解：

1. 将状态$x$视为参数，求解参数化QP
2. 识别临界区域（Critical Regions），即具有相同活跃约束集的状态集合
3. 计算每个区域内的最优控制律$u^*(x) = F_i x + g_i$

在线阶段：

1. 确定当前状态$x$所属区域：$H_i x \leq h_i$
2. 计算控制量：$u = F_i x + g_i$

#### 4.2.5.3 复杂度与存储优化

显式MPC的主要挑战在于区域数量随预测时域和约束数指数增长。优化策略包括：

**区域合并：** 合并相邻且控制律相近的区域，减少存储需求

**近似显式MPC：** 采用神经网络或多项式拟合近似最优控制律

**自适应分区：** 根据系统运行轨迹动态调整分区密度

### 4.2.6 线性MPC在水系统中的应用

#### 4.2.6.1 供水管网压力控制

供水管网的压力控制是LMPC的典型应用场景[8]。控制目标为：

- 维持关键节点压力在服务压力范围内
- 最小化泵站能耗
- 减少压力波动和水锤效应

系统模型：

$$h(k+1) = Ah(k) + Bq(k) + Ed(k) \tag{4.2.20}$$

其中，$h$为节点压力头，$q$为泵站流量，$d$为节点需水量。

优化目标：

$$\min \sum_{i=0}^{N-1} \left[ \|h_{k+i|k} - h_{ref}\|_Q^2 + \|q_{k+i|k}\|_R^2 \right] \tag{4.2.21}$$

约束包括泵站流量限制、压力上下限、水箱容量限制等。

#### 4.2.6.2 水库优化调度

水库调度需平衡防洪、供水、发电等多目标需求。LMPC通过滚动优化实现实时调度：

$$V(k+1) = V(k) + T_s(Q_{in}(k) - Q_{out}(k)) \tag{4.2.22}$$

其中，$V$为水库蓄水量，$Q_{in}$为入库流量，$Q_{out}$为出库流量。

优化目标包括：
- 跟踪目标水位曲线
- 最小化泄洪损失
- 最大化发电效益

#### 4.2.6.3 污水处理过程控制

污水处理过程包含多个生物化学反应单元，LMPC用于优化曝气量和污泥回流比[9]：

$$\min \sum_{i=0}^{N-1} \left[ \alpha_1 \|DO_{k+i|k} - DO_{set}\|^2 + \alpha_2 \|Q_{air,k+i|k}\|^2 \right] \tag{4.2.23}$$

其中，$DO$为溶解氧浓度，$Q_{air}$为曝气量。

### 4.2.7 稳定性与鲁棒性分析

#### 4.2.7.1 稳定性条件

对于线性MPC，稳定性可通过终端代价和终端约束保证。设终端代价$V_f(x) = x^T P x$，其中$P$满足Riccati方程：

$$P = Q + A^T P A - A^T P B(R + B^T P B)^{-1} B^T P A \tag{4.2.24}$$

终端约束集$\mathbb{X}_f$为不变集：

$$(A - BK_{LQR})x \in \mathbb{X}_f, \quad \forall x \in \mathbb{X}_f \tag{4.2.25}$$

其中，$K_{LQR} = (R + B^T P B)^{-1} B^T P A$为LQR增益。

#### 4.2.7.2 无限时域保证

通过适当选择终端代价，有限时域MPC可等价于无限时域LQR：

$$J_N^*(x) = J_\infty^*(x), \quad \forall x \in \mathbb{X}_N \tag{4.2.26}$$

这保证了闭环系统的渐近稳定性。

#### 4.2.7.3 鲁棒性考虑

实际系统存在模型误差和扰动。线性MPC的鲁棒性可通过以下方式增强：

**反馈校正：** 利用测量值修正模型预测误差

**Tube MPC：** 在预测中考虑扰动边界，确保约束满足

**Min-max MPC：** 优化最坏情况下的性能

### 4.2.8 数值示例

考虑简单供水系统，状态方程为：

$$h(k+1) = 0.95h(k) + 0.1u(k) - 0.05d(k) \tag{4.2.27}$$

其中，$h$为水箱水位（m），$u$为泵站流量（L/s），$d$为需水量（L/s）。

参数设置：
- 预测时域$N = 10$
- 权重$Q = 1, R = 0.1$
- 约束：$0 \leq h \leq 10$，$0 \leq u \leq 50$

仿真结果显示，LMPC能有效跟踪水位设定值，同时满足所有约束条件，在需水量变化时快速调整控制策略。

### 4.2.9 小结

线性模型预测控制是MPC技术的基础和核心，其将控制问题转化为凸二次规划求解，具有理论完备、计算高效、实施便捷等优势。通过状态空间模型、预测方程和优化求解，LMPC能够系统性地处理多变量耦合、约束条件和多目标优化问题。

在水系统控制中，LMPC已成功应用于供水管网压力管理、水库调度、污水处理等多个领域。其关键在于将复杂水力过程在工作点附近线性化，同时保留约束处理和多目标优化能力。

随着快速QP求解器和显式MPC技术的发展，LMPC的实时性不断提升，为大规模水系统的在线优化控制提供了可行方案。未来发展方向包括与机器学习结合的数据驱动LMPC、面向不确定性的鲁棒LMPC，以及分布式LMPC架构等。

## 参考文献

[1] CAMACHO E F, BORDONS C. Model Predictive Control[M]. 2nd ed. London: Springer, 2007.

[2] CUTLER C R, RAMAKER B L. Dynamic matrix control-a computer control algorithm[C]//Proceedings of AIChE National Meeting. Houston, 1980.

[3] OCAMPO-MARTINEZ C, PUIG V, CEMBRANO G, et al. Application of predictive control strategies to the management of complex networks in the urban water cycle[J]. IEEE Control Systems Magazine, 2013, 33(1): 15-41.

[4] NOCEDAL J, WRIGHT S J. Numerical Optimization[M]. 2nd ed. New York: Springer, 2006.

[5] WRIGHT S J. Primal-Dual Interior-Point Methods[M]. Philadelphia: SIAM, 1997.

[6] FERREAU H J, KIRCHES C, POT SCHKA A, et al. qpOASES: A parametric active-set algorithm for quadratic programming[J]. Mathematical Programming Computation, 2014, 6(4): 327-363.

[7] BEMPORAD A, MORARI M, DUA V, et al. The explicit linear quadratic regulator for constrained systems[J]. Automatica, 2002, 38(1): 3-20.

[8] PASCUAL J, BARREIRO A, LÓPEZ P. Multivariable control of a water supply system with a risk management approach[J]. Water Resources Management, 2013, 27(14): 4911-4926.

[9] HOLENDA B, DOMOKOS E, RÉDEY A, et al. Dissolved oxygen control of the activated sludge wastewater treatment process using model predictive control[J]. Computers & Chemical Engineering, 2008, 32(6): 1270-1278.

[10] STELLATO B, BANJAC G, GOULART P, et al. OSQP: An operator splitting solver for quadratic programs[J]. Mathematical Programming Computation, 2020, 12(4): 637-672.

</ama-doc>
