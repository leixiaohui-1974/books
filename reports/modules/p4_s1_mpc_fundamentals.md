<ama-doc>
# 第四部分 模型预测控制

## 第1节 模型预测控制基本原理

### 4.1.1 引言

模型预测控制（Model Predictive Control, MPC）作为一种先进的控制策略，在过去四十年间经历了从工业过程控制到现代智能系统的广泛应用拓展。MPC的核心思想源于对系统未来行为的预测能力，通过在每个采样时刻求解一个开环最优控制问题，并将所得控制序列的第一个元素应用于系统，从而实现闭环控制[1]。这种"滚动优化、反馈校正"的控制范式，使其在处理多输入多输出系统、约束条件以及多目标优化问题时展现出独特的优势。

MPC的发展可追溯至20世纪70年代末80年代初，由法国ADERSA公司的Richalet等人提出的模型预测启发控制（Model Predictive Heuristic Control, MPHC）以及Shell Oil公司的Cutler和Ramaker提出的动态矩阵控制（Dynamic Matrix Control, DMC）[2]。这些早期方法主要应用于石油精炼和化工过程，其成功实践奠定了MPC作为工业标准控制技术的地位。随着计算能力的飞速提升和优化理论的不断完善，MPC已从最初的线性约束二次规划问题扩展到涵盖非线性、鲁棒、分布式和经济型等多种变体[3]。

在水系统控制领域，MPC的应用日益广泛。供水管网、污水处理、灌溉调度和洪水管理等水系统具有强耦合性、大滞后性、多约束条件和不确定性的特点，传统PID控制难以满足日益复杂的控制需求。MPC通过显式处理系统约束、预测未来需求和优化资源配置，为水系统的高效、安全、经济运行提供了强有力的技术支撑[4]。

### 4.1.2 MPC的核心原理

#### 4.1.2.1 滚动优化机制

MPC区别于传统控制方法的根本特征在于其滚动优化机制。在每个采样时刻$k$，控制器基于当前系统状态$x(k)$，求解一个有限时域的开环最优控制问题：

$$\min_{\mathbf{u}} J(x(k), \mathbf{u}) = \sum_{i=0}^{N-1} l(x_{k+i|k}, u_{k+i|k}) + V_f(x_{k+N|k}) \tag{4.1.1}$$

其中，$N$为预测时域长度，$l(\cdot, \cdot)$为阶段代价函数，$V_f(\cdot)$为终端代价函数，$\mathbf{u} = \{u_{k|k}, u_{k+1|k}, \ldots, u_{k+N-1|k}\}$为待优化的控制序列，$x_{k+i|k}$表示在时刻$k$对时刻$k+i$的状态预测。

上述优化问题需满足以下约束条件：

**系统动态约束：**
$$x_{k+i+1|k} = f(x_{k+i|k}, u_{k+i|k}), \quad i = 0, 1, \ldots, N-1 \tag{4.1.2}$$

**状态约束：**
$$x_{k+i|k} \in \mathbb{X}, \quad i = 1, 2, \ldots, N \tag{4.1.3}$$

**控制约束：**
$$u_{k+i|k} \in \mathbb{U}, \quad i = 0, 1, \ldots, N-1 \tag{4.1.4}$$

**终端约束（可选）：**
$$x_{k+N|k} \in \mathbb{X}_f \tag{4.1.5}$$

优化完成后，仅将控制序列的第一个元素$u_{k|k}^*$应用于实际系统：

$$u(k) = u_{k|k}^* \tag{4.1.6}$$

在下一采样时刻$k+1$，基于新的状态测量$x(k+1)$，重复上述优化过程。这种滚动时域策略使MPC能够持续适应系统变化，处理模型不确定性和外部扰动。

#### 4.1.2.2 预测模型

预测模型是MPC的核心组件，决定了控制器对未来系统行为的预测精度。根据系统特性和应用需求，预测模型可分为以下几类：

**状态空间模型：**

对于线性时不变系统，状态空间表示为：

$$x(k+1) = Ax(k) + Bu(k) \tag{4.1.7}$$
$$y(k) = Cx(k) + Du(k) \tag{4.1.8}$$

其中，$x \in \mathbb{R}^n$为状态向量，$u \in \mathbb{R}^m$为控制输入，$y \in \mathbb{R}^p$为输出向量，$A, B, C, D$为适当维数的系统矩阵。

**输入输出模型：**

对于无法直接测量状态的系统，可采用输入输出模型，如阶跃响应模型或脉冲响应模型。DMC采用的阶跃响应模型形式为：

$$y(k) = \sum_{i=1}^{N_s} a_i \Delta u(k-i) \tag{4.1.9}$$

其中，$a_i$为阶跃响应系数，$N_s$为模型时域长度，$\Delta u(k) = u(k) - u(k-1)$为控制增量。

**非线性模型：**

对于本质非线性系统，需采用非线性状态空间模型：

$$x(k+1) = f(x(k), u(k)) \tag{4.1.10}$$
$$y(k) = h(x(k), u(k)) \tag{4.1.11}$$

其中，$f(\cdot)$和$h(\cdot)$为非线性函数。在水系统中，管网水力模型、水质传输模型通常呈现强非线性特征。

#### 4.1.2.3 反馈校正机制

MPC通过反馈校正机制补偿模型误差和外部扰动。在每个采样时刻，利用实际测量值与模型预测值的偏差修正未来预测：

$$\tilde{y}(k+i|k) = y(k+i|k) + d(k) \tag{4.1.12}$$

其中，$d(k) = y_m(k) - y(k|k-1)$为当前时刻的预测误差，$y_m(k)$为实际测量输出。这种误差补偿机制确保了控制的鲁棒性。

### 4.1.3 MPC的数学框架

#### 4.1.3.1 标准MPC问题表述

考虑离散时间非线性系统：

$$x_{k+1} = f(x_k, u_k), \quad x_0 = x(0) \tag{4.1.13}$$

其中，$x_k \in \mathbb{R}^n$，$u_k \in \mathbb{R}^m$。约束集定义为：

$$\mathbb{X} = \{x \in \mathbb{R}^n : g_x(x) \leq 0\} \tag{4.1.14}$$
$$\mathbb{U} = \{u \in \mathbb{R}^m : g_u(u) \leq 0\} \tag{4.1.15}$$

标准MPC优化问题可表述为：

$$\begin{aligned}
\min_{\mathbf{u}} \quad & J_N(x, \mathbf{u}) = \sum_{i=0}^{N-1} l(x_i, u_i) + V_f(x_N) \\
\text{s.t.} \quad & x_{i+1} = f(x_i, u_i), \quad i = 0, \ldots, N-1 \\
& x_0 = x \\
& x_i \in \mathbb{X}, \quad i = 1, \ldots, N \\
& u_i \in \mathbb{U}, \quad i = 0, \ldots, N-1 \\
& x_N \in \mathbb{X}_f
\end{aligned} \tag{4.1.16}$$

#### 4.1.3.2 稳定性分析

MPC的稳定性分析是理论研究的焦点。Mayne等人提出了保证MPC闭环稳定性的三个关键要素[5]：

**终端代价函数$V_f(x)$：** 作为最优值函数在无限时域上的近似，需满足：

$$V_f(f(x, \kappa_f(x))) - V_f(x) \leq -l(x, \kappa_f(x)), \quad \forall x \in \mathbb{X}_f \tag{4.1.17}$$

其中，$\kappa_f(x)$为局部稳定控制器。

**终端约束集$\mathbb{X}_f$：** 需满足正不变性条件：

$$f(x, \kappa_f(x)) \in \mathbb{X}_f, \quad \forall x \in \mathbb{X}_f \tag{4.1.18}$$

**局部控制器$\kappa_f(x)$：** 在终端集内稳定系统。

满足上述条件时，闭环系统渐近稳定，且吸引域为可行集：

$$\mathbb{X}_N = \{x \in \mathbb{X} : \exists \mathbf{u} \text{ 使得约束满足}\} \tag{4.1.19}$$

#### 4.1.3.3 最优性条件

对于无约束线性二次型MPC，问题存在解析解。考虑系统$x_{k+1} = Ax_k + Bu_k$，代价函数：

$$J = \sum_{i=0}^{N-1} (x_i^T Q x_i + u_i^T R u_i) + x_N^T P x_N \tag{4.1.20}$$

通过动态规划或批量优化方法，可得最优控制律：

$$u_k^* = -K_k x_k \tag{4.1.21}$$

其中，$K_k$为时变反馈增益矩阵。当$N \to \infty$且$(A, B)$可稳、$(Q^{1/2}, A)$可检测时，MPC收敛至LQR控制器。

### 4.1.4 MPC的关键设计参数

#### 4.1.4.1 预测时域$N$

预测时域决定了控制器向前预测的时间范围。较大的$N$可捕获更多系统动态，提高控制性能，但增加计算负担。一般原则为：

- $N$应覆盖系统的主要动态响应时间
- 对于具有大时滞的系统，$N$需大于时滞时间
- 在满足性能要求的前提下，选择最小的$N$以保证实时性

#### 4.1.4.2 采样周期$T_s$

采样周期影响离散化精度和控制响应速度：

- $T_s$过小：计算负担增加，数值问题加剧
- $T_s$过大：离散化误差增大，可能丢失关键动态

经验法则：$T_s$应小于系统最小时间常数的1/10。

#### 4.1.4.3 权重矩阵$Q, R$

权重矩阵调节状态调节与控制能量之间的权衡：

- $Q$增大：状态跟踪精度提高，但控制动作增大
- $R$增大：控制动作平滑，但响应速度降低

调参方法包括试凑法、基于频域分析的方法和基于优化的自动调参。

### 4.1.5 MPC在水系统中的应用特点

#### 4.1.5.1 水系统的控制挑战

水系统控制面临以下独特挑战[6]：

**强耦合性：** 供水管网中各节点压力、流量相互影响，形成复杂的多变量耦合关系。

**大时滞性：** 水质传输、长距离输水过程存在显著的时间延迟，传统控制难以处理。

**多约束条件：** 包括物理约束（管道承压能力、泵站工作范围）、安全约束（水质标准、水位限制）和经济约束（运行成本）。

**不确定性：** 需水量预测误差、设备故障、突发事件等不确定性因素普遍存在。

#### 4.1.5.2 MPC的优势

MPC为水系统控制提供了系统性解决方案：

**约束处理能力：** MPC通过优化问题的显式约束处理，确保控制动作始终满足物理和安全限制。

**多目标优化：** 可同时优化能耗、水质、服务水平等多个目标，通过权重调节实现不同目标间的权衡。

**预测能力：** 基于需水量预测模型，MPC可提前调整控制策略，应对未来变化。

**协调控制：** 对于大规模水系统，MPC可实现多泵站、多水库的协调优化调度。

#### 4.1.5.3 典型应用场景

**供水管网压力管理：** 通过优化泵站运行和阀门调节，维持管网压力在合理范围，同时降低能耗[7]。

**水库调度：** 优化水库蓄放水策略，平衡防洪、供水、发电等多目标需求。

**污水处理过程控制：** 优化曝气、污泥回流等操作，在保证出水水质的同时降低运行成本。

**灌溉系统调度：** 根据作物需水和气象预报，优化灌溉时间和水量分配。

### 4.1.6 MPC的算法实现流程

MPC的实时实现涉及以下关键步骤：

**步骤1：状态估计**

基于传感器测量，利用状态观测器（如卡尔曼滤波器）估计当前系统状态：

$$\hat{x}(k) = \text{Observer}(y_m(k), u(k-1), \hat{x}(k-1))$$

**步骤2：预测生成**

基于预测模型，生成未来状态和输出轨迹：

$$\mathbf{x}_{pred} = \{x_{k+1|k}, x_{k+2|k}, \ldots, x_{k+N|k}\}$$

**步骤3：优化求解**

求解有限时域最优控制问题，获得最优控制序列：

$$\mathbf{u}^* = \arg\min_{\mathbf{u}} J(\hat{x}(k), \mathbf{u})$$

**步骤4：控制实施**

将优化所得控制序列的第一个元素应用于系统：

$$u(k) = u_{k|k}^*$$

**步骤5：等待下一周期**

等待下一采样时刻，返回步骤1。

### 4.1.7 小结

模型预测控制作为一种基于优化的先进控制策略，通过滚动优化、预测模型和反馈校正三大核心机制，为复杂约束系统的控制提供了系统性解决方案。其显式处理约束的能力、多目标优化的灵活性以及预测未来变化的特性，使其在水系统控制领域展现出巨大潜力。

MPC的理论基础包括最优控制、滚动时域控制和稳定性理论。终端代价、终端约束和局部控制器是保证闭环稳定性的三个关键要素。在实际应用中，预测时域、采样周期、权重矩阵等设计参数的选择对控制性能具有重要影响。

随着计算能力的提升和优化算法的发展，MPC已从最初的工业过程控制扩展到智能交通、能源管理、机器人控制等广泛领域。在水系统控制中，MPC正逐步从理论研究走向工程实践，为水资源的高效利用和可持续管理提供技术支撑。

## 参考文献

[1] RAWLINGS J B, MAYNE D Q. Model Predictive Control: Theory and Design[M]. Madison: Nob Hill Publishing, 2009.

[2] QIN S J, BADGWELL T A. A survey of industrial model predictive control technology[J]. Control Engineering Practice, 2003, 11(7): 733-764.

[3] MAYNE D Q. Model predictive control: Recent developments and future promise[J]. Automatica, 2014, 50(12): 2967-2986.

[4] WANG Y, BOYD S. Fast model predictive control using online optimization[J]. IEEE Transactions on Control Systems Technology, 2010, 18(2): 267-278.

[5] MAYNE D Q, RAWLINGS J B, RAO C V, et al. Constrained model predictive control: Stability and optimality[J]. Automatica, 2000, 36(6): 789-814.

[6] OCAMPO-MARTINEZ C, PUIG V, CEMBRANO G, et al. Application of predictive control strategies to the management of complex networks in the urban water cycle[J]. IEEE Control Systems Magazine, 2013, 33(1): 15-41.

[7] PASCUAL J, BARREIRO A, LÓPEZ P. Multivariable control of a water supply system with a risk management approach[J]. Water Resources Management, 2013, 27(14): 4911-4926.

[8] GARCIA C E, PRETT D M, MORARI M. Model predictive control: Theory and practice—A survey[J]. Automatica, 1989, 25(3): 335-348.

[9] LEE J H. Model predictive control: Review of the three decades of development[J]. International Journal of Control, Automation and Systems, 2011, 9(3): 415-424.

[10] KOUVARITAKIS B, CANNON M. Model Predictive Control: Classical, Robust and Stochastic[M]. Cham: Springer International Publishing, 2016.

</ama-doc>
