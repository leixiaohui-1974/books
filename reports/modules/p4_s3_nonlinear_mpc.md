<ama-doc>
# 第四部分 模型预测控制

## 第3节 非线性模型预测控制

### 4.3.1 引言

非线性模型预测控制（Nonlinear Model Predictive Control, NMPC）是MPC技术在处理本质非线性系统时的自然扩展。与线性MPC相比，NMPC采用非线性系统模型，在每个采样时刻求解非凸非线性规划（Nonlinear Programming, NLP）问题，能够更准确地描述复杂动态过程[1]。在水系统控制中，管网水力方程、水质传输模型、泵站特性曲线等均呈现显著非线性，NMPC的应用对于提升控制精度和系统性能具有重要意义。

NMPC的理论研究始于20世纪90年代，Mayne、Rawlings等学者奠定了其稳定性理论基础[2]。随着计算能力的提升和优化算法的发展，NMPC已从学术研究走向工程应用，在化工过程、机器人控制、航空航天等领域展现出强大能力。在水系统领域，NMPC被用于处理管网水力非线性、水质反应动力学、多相流等复杂过程。

NMPC面临的主要挑战包括：非凸优化问题的计算复杂度、局部最优解问题、实时性保证等。近年来，实时迭代（Real-Time Iteration, RTI）策略、高效NLP求解器、并行计算等技术的发展，显著提升了NMPC的实用性和可扩展性[3]。

### 4.3.2 非线性MPC的数学框架

#### 4.3.2.1 非线性系统模型

考虑离散时间非线性系统：

$$x(k+1) = f(x(k), u(k)) \tag{4.3.1}$$
$$y(k) = h(x(k), u(k)) \tag{4.3.2}$$

其中，$f: \mathbb{R}^n \times \mathbb{R}^m \to \mathbb{R}^n$为状态转移函数，$h: \mathbb{R}^n \times \mathbb{R}^m \to \mathbb{R}^p$为输出函数。假设$f$和$h$关于$(x, u)$连续可微。

在水系统中，典型的非线性模型包括：

**管网水力模型：**

管道水头损失采用Hazen-Williams或Darcy-Weisbach公式：

$$\Delta h = k \cdot Q^{1.852} \quad \text{(Hazen-Williams)} \tag{4.3.3}$$

或

$$\Delta h = f \cdot \frac{L}{D} \cdot \frac{Q^2}{2gA^2} \quad \text{(Darcy-Weisbach)} \tag{4.3.4}$$

其中，$Q$为流量，$k$为管道阻力系数，$f$为摩擦系数，$L$为管长，$D$为管径。

**水质传输模型：**

污染物浓度变化遵循对流-扩散-反应方程：

$$\frac{\partial C}{\partial t} + v \frac{\partial C}{\partial x} = D \frac{\partial^2 C}{\partial x^2} - kC \tag{4.3.5}$$

其中，$C$为浓度，$v$为流速，$D$为扩散系数，$k$为反应速率常数。

**泵站特性：**

泵站扬程-流量关系通常表示为二次函数：

$$H = H_0 - aQ^2 \tag{4.3.6}$$

其中，$H_0$为零流量扬程，$a$为特性系数。

#### 4.3.2.2 NMPC优化问题

NMPC在每个采样时刻求解以下非线性规划问题：

$$\min_{\mathbf{u}} J = \sum_{i=0}^{N-1} l(x_{k+i|k}, u_{k+i|k}) + V_f(x_{k+N|k}) \tag{4.3.7}$$

约束条件：

$$x_{k+i+1|k} = f(x_{k+i|k}, u_{k+i|k}), \quad i = 0, \ldots, N-1 \tag{4.3.8}$$
$$x_{k|k} = x(k) \tag{4.3.9}$$
$$x_{k+i|k} \in \mathbb{X}, \quad u_{k+i|k} \in \mathbb{U} \tag{4.3.10}$$
$$x_{k+N|k} \in \mathbb{X}_f \tag{4.3.11}$$

其中，阶段代价$l(\cdot)$和终端代价$V_f(\cdot)$通常取二次形式或经济型代价。

### 4.3.3 非线性规划求解方法

#### 4.3.3.1 序列二次规划（SQP）

序列二次规划是求解NLP问题的主流算法，通过迭代求解一系列QP子问题逼近最优解[4]。

在第$j$次迭代，在当前点$(\mathbf{x}^j, \mathbf{u}^j)$处线性化约束，二次近似目标函数：

$$\min_{\Delta \mathbf{u}} \frac{1}{2}\Delta \mathbf{u}^T H^j \Delta \mathbf{u} + (\nabla J^j)^T \Delta \mathbf{u} \tag{4.3.12}$$

$$\text{s.t.} \quad c^j + A^j \Delta \mathbf{u} = 0 \tag{4.3.13}$$
$$d^j + B^j \Delta \mathbf{u} \leq 0 \tag{4.3.14}$$

其中，$H^j$为Lagrange函数的Hessian近似，$A^j$和$B^j$为约束的Jacobian矩阵。

SQP算法流程：

1. **初始化**：选择初始点$\mathbf{u}^0$，设置收敛容差$\epsilon$

2. **QP求解**：在当前点求解QP子问题，获得搜索方向$\Delta \mathbf{u}^j$

3. **线搜索**：沿搜索方向进行线搜索，确定步长$\alpha^j$

4. **更新**：$\mathbf{u}^{j+1} = \mathbf{u}^j + \alpha^j \Delta \mathbf{u}^j$

5. **收敛判断**：若$\|\Delta \mathbf{u}^j\| < \epsilon$，停止；否则返回步骤2

#### 4.3.3.2 内点法

内点法通过引入障碍函数处理不等式约束，将NLP转化为一系列等式约束问题[5]。

障碍函数形式：

$$\min_{\mathbf{u}, s} J(\mathbf{u}) - \mu \sum_{i} \ln(s_i) \tag{4.3.15}$$

$$\text{s.t.} \quad c(\mathbf{u}) = 0 \tag{4.3.16}$$
$$d(\mathbf{u}) + s = 0 \tag{4.3.17}$$
$$s \geq 0 \tag{4.3.18}$$

其中，$\mu > 0$为障碍参数，$s$为松弛变量。

内点法的优点是对初始点要求较低，适合大规模问题；缺点是参数$\mu$的选择影响收敛速度。

#### 4.3.3.3 直接多重打靶法

直接多重打靶法（Direct Multiple Shooting）将预测时域划分为多个区间，在每个区间内独立积分系统动态，通过连续性约束保证轨迹光滑[6]。

优化变量包括各区间起点的控制输入和状态：

$$\mathbf{z} = (u_0, x_1, u_1, x_2, \ldots, u_{N-1}, x_N) \tag{4.3.19}$$

连续性约束：

$$x_{i+1} - \phi(x_i, u_i) = 0, \quad i = 0, \ldots, N-1 \tag{4.3.20}$$

其中，$\phi(\cdot)$为数值积分算子。

多重打靶法的优点是优化问题结构稀疏，便于利用稀疏线性代数求解器；缺点是变量维数增加。

### 4.3.4 实时迭代策略

#### 4.3.4.1 实时迭代概念

实时迭代（Real-Time Iteration, RTI）策略针对NMPC的实时性要求，通过利用相邻采样时刻优化问题的相似性，大幅减少单步计算时间[7]。

RTI的核心思想：

- 每个采样时刻仅执行有限次（通常1次）SQP迭代
- 利用上一时刻的解作为热启动
- 在系统运行过程中逐步收敛到最优解

#### 4.3.4.2 初始值嵌入

初始值嵌入（Initial Value Embedding）是RTI的关键技术，将当前状态测量显式嵌入优化问题：

$$\min_{\mathbf{u}} J(x(k), \mathbf{u}) \tag{4.3.21}$$

通过将$x(k)$作为参数，优化问题的结构保持不变，便于利用前一时刻的因子分解结果。

#### 4.3.4.3 灵敏度更新

RTI中，Jacobian和Hessian矩阵的更新策略影响计算效率：

**精确更新：** 每次迭代重新计算所有导数，精度高但计算量大

**BFGS近似：** 利用梯度信息近似Hessian，减少计算量

**固定Jacobian：** 在若干采样周期内保持Jacobian不变，适用于变化缓慢的系统

### 4.3.5 稳定性与收敛性分析

#### 4.3.5.1 终端条件设计

与线性MPC类似，NMPC的稳定性依赖于终端代价$V_f$和终端约束集$\mathbb{X}_f$的适当选择[8]。

终端代价需满足：

$$V_f(f(x, \kappa_f(x))) - V_f(x) \leq -l(x, \kappa_f(x)), \quad \forall x \in \mathbb{X}_f \tag{4.3.22}$$

其中，$\kappa_f(x)$为局部稳定控制器，通常通过线性化系统设计和LQR方法获得。

#### 4.3.5.2 子最优稳定性

由于实时性限制，NMPC可能只能获得次优解。子最优MPC的稳定性条件[9]：

设$\tilde{J}(x)$为实际实现的代价值，$J^*(x)$为最优值，若满足：

$$\tilde{J}(x) \leq J^*(x) + \epsilon \tag{4.3.23}$$
$$\tilde{J}(x^+) - \tilde{J}(x) \leq -l(x, u) + \delta \tag{4.3.24}$$

其中，$\epsilon, \delta$为适当小的正数，则闭环系统实用稳定。

#### 4.3.5.3 收敛性分析

NMPC优化问题的收敛性依赖于：

- 目标函数的凸性（或局部凸性）
- 约束规范（如LICQ、MFCQ）
- 初始点的选择

对于非凸问题，SQP可能收敛到局部最优。全局优化策略包括多起点、模拟退火、遗传算法等，但计算成本较高。

### 4.3.6 NMPC在水系统中的应用

#### 4.3.6.1 非线性管网水力控制

供水管网的水力方程本质非线性，NMPC可实现更精确的压力和流量控制[10]。

节点压力方程（基于图论）：

$$A_p Q_p + A_0 Q_0 = q_d \tag{4.3.25}$$
$$A_p^T H = \Delta h_p(Q_p) \tag{4.3.26}$$

其中，$A_p$为管网关联矩阵，$Q_p$为管道流量，$H$为节点压力头，$\Delta h_p$为管道水头损失函数。

NMPC优化问题：

$$\min \sum_{i=0}^{N-1} \left[ \|H_{k+i|k} - H_{ref}\|_Q^2 + \|Q_{pump,k+i|k}\|_R^2 \right] \tag{4.3.27}$$

约束包括水力方程、泵站特性、压力限制等。

#### 4.3.6.2 水质优化控制

水质控制涉及消毒剂传输和衰减的非线性动力学[11]：

$$\frac{\partial C}{\partial t} = -v \frac{\partial C}{\partial x} - kC^n \tag{4.3.28}$$

其中，$n$为反应级数（通常为1或2）。

NMPC通过优化消毒剂投加策略，在保证水质达标的前提下最小化投加成本：

$$\min \sum_{i=0}^{N-1} \left[ \alpha_1 \|C_{min} - C_{k+i|k}\|_+ + \alpha_2 \|u_{dose,k+i|k}\|^2 \right] \tag{4.3.29}$$

其中，$\|\cdot\|_+$为正部函数，惩罚浓度低于下限的情况。

#### 4.3.6.3 泵站组合优化

大型供水系统包含多个泵站，NMPC可优化泵站启停和转速组合：

$$\min \sum_{i=0}^{N-1} \sum_{j} \left[ P_j(u_{j,k+i|k}) + c_j \cdot \delta_{j,k+i|k} \right] \tag{4.3.30}$$

其中，$P_j$为泵站$j$的功率消耗，$\delta_j \in \{0, 1\}$为启停状态，$c_j$为启停成本。

此类问题为混合整数非线性规划（MINLP），求解难度更大，通常采用松弛-舍入或分支定界方法。

### 4.3.7 高效实现技术

#### 4.3.7.1 自动微分

自动微分（Automatic Differentiation, AD）可精确高效地计算导数，是NMPC实现的关键技术[12]。

前向模式AD：

$$\dot{y} = \frac{\partial f}{\partial x} \dot{x} + \frac{\partial f}{\partial u} \dot{u} \tag{4.3.31}$$

反向模式AD：

$$\bar{x} = \left(\frac{\partial f}{\partial x}\right)^T \bar{y}, \quad \bar{u} = \left(\frac{\partial f}{\partial u}\right)^T \bar{y} \tag{4.3.32}$$

常用AD工具：CasADi、ADOL-C、CppAD等。

#### 4.3.7.2 稀疏结构利用

NMPC优化问题的Jacobian和Hessian矩阵具有高度稀疏结构，利用稀疏线性代数可大幅提升求解效率。

稀疏模式分析：

- 系统动态约束仅连接相邻时刻变量
- 多重打靶法的连续性约束形成块对角结构
- 利用稀疏Cholesky分解或稀疏LU分解

#### 4.3.7.3 并行计算

NMPC的计算可并行化加速：

**预测并行：** 各预测时刻的动态仿真并行执行

**多场景并行：** 对不确定性场景并行求解

**GPU加速：** 利用GPU的并行计算能力加速矩阵运算和仿真

### 4.3.8 小结

非线性模型预测控制是处理本质非线性系统的强大工具，通过在每个采样时刻求解非线性规划问题，实现了对复杂动态过程的精确控制。在水系统控制中，NMPC能够直接处理管网水力非线性、水质反应动力学等复杂模型，显著提升控制精度和系统性能。

NMPC的核心挑战在于非凸优化问题的实时求解。序列二次规划、内点法、多重打靶法等算法为NLP求解提供了有效途径。实时迭代策略通过利用相邻优化问题的相似性，大幅降低了单步计算时间，使NMPC的在线应用成为可能。

随着自动微分、稀疏线性代数、并行计算等技术的发展，NMPC的计算效率不断提升。在水系统领域，NMPC正从理论研究走向工程实践，为供水管网优化运行、水质安全保障、能源效率提升等提供了先进技术手段。

未来发展方向包括：数据驱动的NMPC、与深度学习结合的近似NMPC、面向大规模系统的分布式NMPC，以及考虑不确定性的随机NMPC等。

## 参考文献

[1] GRÜNE L, PANNEK J. Nonlinear Model Predictive Control: Theory and Algorithms[M]. 2nd ed. Cham: Springer, 2017.

[2] MAYNE D Q, RAWLINGS J B, RAO C V, et al. Constrained model predictive control: Stability and optimality[J]. Automatica, 2000, 36(6): 789-814.

[3] DIEHL M, FERREAU H J, HAVERBEKE N. Efficient numerical methods for nonlinear MPC and moving horizon estimation[M]//Nonlinear Model Predictive Control. Berlin: Springer, 2009: 391-417.

[4] BOGGS P T, TOLLE J W. Sequential quadratic programming[J]. Acta Numerica, 1995, 4: 1-51.

[5] NOCEDAL J, WRIGHT S J. Numerical Optimization[M]. 2nd ed. New York: Springer, 2006.

[6] BOCK H G, PLITT K J. A multiple shooting algorithm for direct solution of optimal control problems[C]//IFAC Proceedings Volumes. 1984, 17(2): 1603-1608.

[7] DIEHL M, BOCK H G, SCHLÖDER J P, et al. Real-time optimization and nonlinear model predictive control of processes governed by differential-algebraic equations[J]. Journal of Process Control, 2002, 12(4): 577-585.

[8] CHEN H, ALLGÖWER F. A quasi-infinite horizon nonlinear model predictive control scheme with guaranteed stability[J]. Automatica, 1998, 34(10): 1205-1217.

[9] SCOKAERT P O, MAYNE D Q, RAWLINGS J B. Suboptimal model predictive control (feasibility implies stability)[J]. IEEE Transactions on Automatic Control, 1999, 44(3): 648-654.

[10] WANG H, LIU S. Nonlinear model predictive control for water distribution networks: A review[J]. Water Resources Management, 2021, 35(4): 1087-1105.

[11] WANG Y, GUO H. Nonlinear model predictive control for chlorine dosing in water distribution systems[J]. Journal of Water Resources Planning and Management, 2018, 144(8): 04018064.

[12] ANDERSSON J A, GILLIS J, HORN G, et al. CasADi: A software framework for nonlinear optimization and optimal control[J]. Mathematical Programming Computation, 2019, 11(1): 1-36.

</ama-doc>
