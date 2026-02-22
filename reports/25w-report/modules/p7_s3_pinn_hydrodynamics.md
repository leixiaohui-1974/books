<ama-doc>

# 7.3 物理信息神经网络PINN

## 7.3.1 引言

物理信息神经网络（Physics-Informed Neural Networks, PINNs）是一种将物理定律嵌入神经网络架构的新型计算方法，由Raissi等人于2019年系统提出[1]。传统神经网络纯粹依赖数据进行训练，而PINNs通过在损失函数中引入物理方程约束，使网络解满足基本的物理守恒定律。这一方法在水系统科学中具有特殊价值，因为水循环过程受质量守恒、动量守恒和能量守恒等基本物理定律支配。

水系统建模长期面临数据稀缺与物理复杂性之间的矛盾。一方面，水文观测站点分布稀疏，难以支撑纯数据驱动模型的训练；另一方面，基于物理的数值模型（如SWE、Navier-Stokes方程）计算成本高昂，且需要精细的边界条件和参数标定。PINNs提供了一种融合数据与物理的混合建模框架，能够利用稀疏观测数据和已知物理定律，实现高效、物理一致的预测。本章系统介绍PINNs的理论基础、算法实现及其在水系统中的应用。

## 7.3.2 PINNs理论基础

### 7.3.2.1 问题定义

考虑一般形式的偏微分方程（PDE）：

$$\mathcal{F}[u(\mathbf{x}, t); \lambda] = 0, \quad \mathbf{x} \in \Omega, \quad t \in [0, T] \tag{7.3.1}$$

其中，$u(\mathbf{x}, t)$为待求解场变量，$\mathcal{F}$为微分算子，$\lambda$为物理参数，$\Omega$为空间域。边界条件和初始条件为：

$$\mathcal{B}[u] = g(\mathbf{x}, t), \quad \mathbf{x} \in \partial\Omega \tag{7.3.2}$$
$$u(\mathbf{x}, 0) = h(\mathbf{x}), \quad \mathbf{x} \in \Omega \tag{7.3.3}$$

PINNs使用深度神经网络$u_\theta(\mathbf{x}, t)$近似解，其中$\theta$为网络参数。网络的输入为时空坐标$(\mathbf{x}, t)$，输出为场变量$u$。

### 7.3.2.2 损失函数构造

PINNs的损失函数由三部分组成：

$$\mathcal{L}(\theta) = \mathcal{L}_{\text{PDE}} + \mathcal{L}_{\text{BC}} + \mathcal{L}_{\text{Data}} \tag{7.3.4}$$

**PDE残差损失**：强制网络满足控制方程

$$\mathcal{L}_{\text{PDE}} = \frac{1}{N_f} \sum_{i=1}^{N_f} \left| \mathcal{F}[u_\theta(\mathbf{x}_f^i, t_f^i); \lambda] \right|^2 \tag{7.3.5}$$

其中，$\{ (\mathbf{x}_f^i, t_f^i) \}_{i=1}^{N_f}$为配点（collocation points），均匀或自适应采样于计算域内。

**边界/初始条件损失**：强制满足边界和初始条件

$$\mathcal{L}_{\text{BC}} = \frac{1}{N_b} \sum_{i=1}^{N_b} \left| \mathcal{B}[u_\theta(\mathbf{x}_b^i, t_b^i)] - g(\mathbf{x}_b^i, t_b^i) \right|^2 + \frac{1}{N_0} \sum_{i=1}^{N_0} \left| u_\theta(\mathbf{x}_0^i, 0) - h(\mathbf{x}_0^i) \right|^2 \tag{7.3.6}$$

**数据拟合损失**：匹配观测数据

$$\mathcal{L}_{\text{Data}} = \frac{1}{N_d} \sum_{i=1}^{N_d} \left| u_\theta(\mathbf{x}_d^i, t_d^i) - u_{\text{obs}}^i \right|^2 \tag{7.3.7}$$

通过最小化总损失，网络学习同时满足物理方程和观测数据的解。

### 7.3.2.3 自动微分

PINNs的核心技术是自动微分（Automatic Differentiation, AD），用于精确计算PDE残差。现代深度学习框架（TensorFlow、PyTorch、JAX）提供自动微分功能，可高效计算高阶导数。

对于网络输出$u_\theta(\mathbf{x}, t)$，其一阶和二阶导数计算为：

$$\frac{\partial u}{\partial t} = \text{AD}(u_\theta, t), \quad \frac{\partial u}{\partial x} = \text{AD}(u_\theta, x) \tag{7.3.8}$$
$$\frac{\partial^2 u}{\partial x^2} = \text{AD}\left(\text{AD}(u_\theta, x), x\right) \tag{7.3.9}$$

自动微分的计算复杂度与函数评估相当，避免了传统数值微分的截断误差。

### 7.3.2.4 网络架构

PINNs通常采用全连接神经网络（FCNN），输入层接收时空坐标，输出层产生场变量。隐藏层常用激活函数包括：

- **tanh**：平滑可微，适合求解光滑解
- **sin**：适合周期性或波动问题
- **Swish**：平滑非单调，表达能力更强

网络深度和宽度影响表达能力，典型配置为5-10层隐藏层，每层20-256个神经元。近年来，傅里叶特征网络（Fourier Feature Networks）和注意力机制被引入PINNs，改善高频成分的表达能力。

## 7.3.3 水系统控制方程

### 7.3.3.1 浅水方程

浅水方程（Shallow Water Equations, SWE）描述自由表面流动，广泛应用于河流、洪水、潮汐模拟。一维SWE形式为：

**连续性方程**：
$$\frac{\partial h}{\partial t} + \frac{\partial (hu)}{\partial x} = 0 \tag{7.3.10}$$

**动量方程**：
$$\frac{\partial (hu)}{\partial t} + \frac{\partial}{\partial x}\left(hu^2 + \frac{1}{2}gh^2\right) = -gh\frac{\partial z_b}{\partial x} - ghS_f \tag{7.3.11}$$

其中，$h$为水深，$u$为流速，$g$为重力加速度，$z_b$为河床高程，$S_f$为摩擦坡降（Manning公式：$S_f = \frac{n^2 u |u|}{R^{4/3}}$，$n$为Manning粗糙系数）。

二维SWE扩展为：

$$\frac{\partial \mathbf{U}}{\partial t} + \frac{\partial \mathbf{F}}{\partial x} + \frac{\partial \mathbf{G}}{\partial y} = \mathbf{S} \tag{7.3.12}$$

其中：

$$\mathbf{U} = \begin{bmatrix} h \\ hu \\ hv \end{bmatrix}, \quad \mathbf{F} = \begin{bmatrix} hu \\ hu^2 + \frac{1}{2}gh^2 \\ huv \end{bmatrix}, \quad \mathbf{G} = \begin{bmatrix} hv \\ huv \\ hv^2 + \frac{1}{2}gh^2 \end{bmatrix} \tag{7.3.13}$$

$$\mathbf{S} = \begin{bmatrix} 0 \\ -gh\frac{\partial z_b}{\partial x} - ghS_{fx} \\ -gh\frac{\partial z_b}{\partial y} - ghS_{fy} \end{bmatrix} \tag{7.3.14}$$

### 7.3.3.2 地下水流动方程

饱和地下水流动遵循质量守恒和Darcy定律，控制方程为：

$$S_s \frac{\partial h}{\partial t} = \nabla \cdot (K \nabla h) + Q \tag{7.3.15}$$

其中，$h$为水头，$S_s$为储水系数，$K$为水力传导系数张量，$Q$为源汇项。对于各向同性介质，简化为：

$$S_s \frac{\partial h}{\partial t} = K \nabla^2 h + Q \tag{7.3.16}$$

### 7.3.3.3 对流-扩散方程

水质输运由对流-扩散方程描述：

$$\frac{\partial C}{\partial t} + \mathbf{u} \cdot \nabla C = \nabla \cdot (D \nabla C) + R(C) + S \tag{7.3.17}$$

其中，$C$为污染物浓度，$\mathbf{u}$为流速场，$D$为扩散系数张量，$R(C)$为反应项，$S$为源汇项。对于一维河流：

$$\frac{\partial C}{\partial t} + u \frac{\partial C}{\partial x} = D \frac{\partial^2 C}{\partial x^2} - kC \tag{7.3.18}$$

其中，$k$为一级衰减系数。

### 7.3.3.4 圣维南方程

圣维南方程（Saint-Venant Equations）是一维明渠流动的完整描述：

$$\frac{\partial A}{\partial t} + \frac{\partial Q}{\partial x} = q_l \tag{7.3.19}$$

$$\frac{\partial Q}{\partial t} + \frac{\partial}{\partial x}\left(\frac{Q^2}{A}\right) + gA\frac{\partial h}{\partial x} = gA(S_0 - S_f) + q_l v_l \tag{7.3.20}$$

其中，$A$为过水断面面积，$Q$为流量，$q_l$为侧向入流，$S_0$为底坡，$v_l$为侧向入流流速。

## 7.3.4 PINNs算法实现

### 7.3.4.1 训练策略

PINNs训练面临多任务学习挑战：同时优化PDE残差、边界条件和数据拟合。不同损失项的量纲和梯度尺度可能差异巨大，需要精心设计训练策略。

**损失加权**：为各损失项分配权重，平衡不同约束的重要性：

$$\mathcal{L} = \lambda_{\text{PDE}} \mathcal{L}_{\text{PDE}} + \lambda_{\text{BC}} \mathcal{L}_{\text{BC}} + \lambda_{\text{Data}} \mathcal{L}_{\text{Data}} \tag{7.3.21}$$

权重可通过网格搜索、学习率退火或自适应方法确定。

**学习率调度**：采用学习率衰减策略，如指数衰减、余弦退火：

$$\eta(t) = \eta_{\min} + \frac{1}{2}(\eta_{\max} - \eta_{\min})\left(1 + \cos\left(\frac{t}{T}\pi\right)\right) \tag{7.3.22}$$

**自适应配点**：在PDE残差较大的区域增加配点密度，提高局部精度。基于残差的几何自适应采样：

$$p(\mathbf{x}) \propto \epsilon(\mathbf{x})^\gamma \tag{7.3.23}$$

其中，$\epsilon(\mathbf{x})$为局部残差，$\gamma$为调节参数。

### 7.3.4.2 参数推断

PINNs可同时进行场变量求解和物理参数反演。将未知参数$\lambda$作为可训练变量，联合优化：

$$\min_{\theta, \lambda} \mathcal{L}(\theta, \lambda) \tag{7.3.24}$$

这对于水系统参数识别（如Manning系数、扩散系数）具有重要价值，避免了传统试错法的繁琐。

### 7.3.4.3 域分解与并行化

大规模水系统问题需要域分解策略。将计算域划分为子域，各子域训练独立PINN，在界面处施加连续性约束：

$$u_i = u_j, \quad \frac{\partial u_i}{\partial \mathbf{n}} = \frac{\partial u_j}{\partial \mathbf{n}}, \quad \text{on } \Gamma_{ij} \tag{7.3.25}$$

这扩展为XPINNs（Extended PINNs）方法，支持大规模并行计算。

### 7.3.4.4 时间域处理

长时间模拟面临梯度消失/爆炸和累积误差问题。常用策略包括：

**时间序列PINNs**：将时间划分为窗口，逐段求解，前一段的终值作为后一段的初值。

**因果训练**：引入因果权重，确保时间顺序上的物理一致性：

$$\mathcal{L}_{\text{causal}} = \sum_{i=1}^{N_t} w_i \mathcal{L}_i, \quad w_i = \exp\left(-\epsilon \sum_{j=1}^{i-1} \mathcal{L}_j\right) \tag{7.3.26}$$

## 7.3.5 水系统应用案例

### 7.3.5.1 明渠流动模拟

PINNs求解一维圣维南方程，模拟明渠非恒定流。研究表明，PINNs能够准确捕捉洪水波的传播和反射，与有限差分法结果高度一致[2]。相比传统数值方法，PINNs具有以下优势：

- **无网格需求**：避免复杂河网的网格生成
- **连续解**：获得时空连续的分析解，而非离散网格值
- **逆向求解**：自然支持参数反演和逆问题

对于包含激波（shock）的问题，需要引入熵条件或粘性正则化保证解的唯一性。

### 7.3.5.2 地下水流动与溶质运移

PINNs求解地下水流动方程和溶质运移方程，实现水头和浓度的联合预测。在异质介质中，PINNs通过学习空间变化的导水系数场，捕捉复杂的流动模式[3]。

对于多相流问题（如非饱和带水流），Richards方程的高度非线性给PINNs带来挑战。自适应激活函数和课程学习策略有助于改善收敛性。

### 7.3.5.3 溃坝洪水模拟

溃坝洪水涉及快速变化的自由表面和激波，是检验PINNs能力的经典问题。二维浅水方程的PINNs求解能够预测洪水淹没范围的时空演变。研究表明，结合WENO（Weighted Essentially Non-Oscillatory）思想的PINNs变体能够更好地处理间断解[4]。

### 7.3.5.4 河流温度模拟

河流水温影响水生生态系统和水质过程。能量平衡方程描述水温演变：

$$\frac{\partial T}{\partial t} + u \frac{\partial T}{\partial x} = \frac{1}{\rho c_p h}(Q_{\text{net}} - Q_{\text{out}}) \tag{7.3.27}$$

其中，$Q_{\text{net}}$为净热通量（太阳辐射、大气长波辐射等），$Q_{\text{out}}$为输出热通量（蒸发、长波辐射等）。PINNs整合水动力方程和能量方程，实现流场-温度场的耦合模拟。

### 7.3.5.5 数据同化与参数识别

PINNs天然支持数据同化，将观测数据作为软约束融入训练。对于稀疏观测场景，PINNs利用物理方程填补数据空白，实现全场估计。

参数识别是PINNs的重要应用。以Manning系数识别为例，将$n(x)$参数化为神经网络或查找表，通过最小化观测流量残差优化：

$$\min_n \sum_{i} |Q_{\text{PINN}}(x_i, t_i; n) - Q_{\text{obs}}(x_i, t_i)|^2 \tag{7.3.28}$$

这比传统试错法更高效，且提供不确定性量化能力。

## 7.3.6 挑战与前沿发展

### 7.3.6.1 当前挑战

**收敛困难**：复杂PDE（如湍流、多相流）的PINNs训练常面临收敛困难。损失景观的多尺度特性导致梯度冲突，不同损失项难以同时优化。

**高频成分**：标准PINNs难以捕捉解的高频振荡。傅里叶特征嵌入和多重网格方法部分缓解这一问题。

**长时间模拟**：累积误差和梯度消失限制PINNs的长时间预测能力。时间域分解和循环神经网络结合是潜在解决方案。

**高维问题**：维度灾难限制PINNs在高维参数空间的应用。稀疏网格和降维技术有助于扩展适用性。

### 7.3.6.2 前沿发展

**自适应激活函数**：可学习的激活函数（如KAN - Kolmogorov-Arnold Networks）提高网络表达能力和收敛速度。

**神经算子**：FNO（Fourier Neural Operator）和DeepONet学习函数空间之间的映射，实现不同分辨率/参数下的快速推理，支持实时模拟[5]。

**物理引导生成模型**：扩散模型和流模型生成满足物理约束的样本，用于不确定性量化和数据增强。

**多保真度PINNs**：整合高保真数值模拟和低保真观测，平衡精度与效率。

**数字孪生集成**：PINNs作为水系统数字孪生的核心求解器，实现实时状态估计和预测。

## 7.3.7 本章小结

物理信息神经网络为水系统建模提供了融合数据与物理的创新框架。通过在损失函数中嵌入控制方程，PINNs实现了物理一致的神经网络求解，在稀疏数据场景下展现出独特优势。从明渠流动到地下水运移，从参数识别到数据同化，PINNs在水系统的多个领域取得重要进展。尽管面临收敛困难、高频捕捉等挑战，但随着算法改进和计算能力提升，PINNs有望成为水系统科学计算的重要工具，推动水文学从数据驱动向物理-数据融合范式转变。

## 参考文献

[1] RAISSI M, PERDIKARIS P, KARNIADAKIS G E. Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations[J]. Journal of Computational Physics, 2019, 378: 686-707.

[2] TARTAKOVSKY A M, MARRERO C O, PERDIKARIS P, et al. Physics-informed deep neural networks for learning parameters and constitutive relationships in subsurface flow problems[J]. Water Resources Research, 2020, 56(5): e2019WR026731.

[3] HE Q, BARAJAS-SOLANO D, TARTAKOVSKY G, et al. Physics-informed neural networks for multiphysics data assimilation with application to subsurface transport[J]. Advances in Water Resources, 2020, 141: 103610.

[4] MAO Z, JAGTAP A D, KARNIADAKIS G E. Physics-informed neural networks for high-speed flows[J]. Computer Methods in Applied Mechanics and Engineering, 2020, 360: 112789.

[5] LI Z, KOVACHKI N, AZIZZADENESHELI K, et al. Fourier neural operator for parametric partial differential equations[C]//International Conference on Learning Representations. Virtual: OpenReview, 2021.

[6] KARNIADAKIS G E, KEVREKIDIS I G, LU L, et al. Physics-informed machine learning[J]. Nature Reviews Physics, 2021, 3(6): 422-440.

[7] CUOMO S, DI COLA V S, GIAMPAOLO F, et al. Scientific machine learning through physics-informed neural networks: Where we are and what's next[J]. Journal of Scientific Computing, 2022, 92(3): 88.

[8] FANG Z. A high-efficient hybrid physics-informed neural networks based on convolutional neural network[J]. IEEE Transactions on Neural Networks and Learning Systems, 2021, 33(10): 5514-5526.

[9] JAGTAP A D, KARNIADAKIS G E. Extended physics-informed neural networks (XPINNs): A generalized space-time domain decomposition based deep learning framework for nonlinear partial differential equations[J]. Communications in Computational Physics, 2020, 28(5): 2002-2041.

[10] WANG S, YU X, PERDIKARIS P. When and why PINNs fail to train: A neural tangent kernel perspective[J]. Journal of Computational Physics, 2022, 449: 110768.

</ama-doc>
