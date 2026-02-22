<ama-doc>

# 5.1 安全约束的形式化

## 5.1.1 引言

安全约束的形式化是确保自主水系统控制可靠运行的理论基础。在水系统控制论中，安全约束不仅涉及物理边界条件，还包括操作限制、环境约束和性能要求等多维度限制。传统的安全约束通常以经验规则或定性描述的形式存在，难以在自动化控制系统中精确实施和验证。形式化方法通过数学语言和逻辑框架，将安全约束转化为可计算、可验证的规范，为安全关键控制系统的设计、分析和验证提供了严格的理论支撑。

形式化安全约束的核心目标在于建立一套完整的数学描述体系，使得系统在任何运行状态下都能够明确判断其行为是否满足安全要求。这种形式化描述不仅需要涵盖系统的物理约束，如水位上下限、流量限制、压力边界等，还需要考虑操作约束、时间约束和逻辑约束等复杂条件。通过形式化方法，可以将这些多样化的约束统一到一个连贯的数学框架中，便于进行系统性的安全分析和控制器设计。

## 5.1.2 安全约束的数学描述

### 5.1.2.1 状态空间约束

在水系统控制中，系统的状态通常由水位、流量、压力等物理量描述。设系统状态向量为 $\mathbf{x} \in \mathbb{R}^n$，则状态空间约束可以表示为状态空间中的一个安全集合 $\mathcal{S}$：

$$\mathcal{S} = \{\mathbf{x} \in \mathbb{R}^n : h_i(\mathbf{x}) \geq 0, \quad i = 1, 2, \ldots, m\}$$

其中 $h_i: \mathbb{R}^n \rightarrow \mathbb{R}$ 是连续可微的约束函数。安全集合 $\mathcal{S}$ 定义了系统允许运行的状态空间区域。对于水系统而言，典型的状态约束包括：

**水位约束**：对于水库或调蓄池，水位必须保持在安全范围内：

$$h_{\min} \leq h(t) \leq h_{\max}$$

这可以转化为两个约束函数：

$$h_1(\mathbf{x}) = h(t) - h_{\min} \geq 0$$
$$h_2(\mathbf{x}) = h_{\max} - h(t) \geq 0$$

**流量约束**：管道或渠道中的流量受限于物理容量：

$$Q_{\min} \leq Q(t) \leq Q_{\max}$$

**压力约束**：供水管网中的压力必须满足服务要求和设备限制：

$$P_{\min} \leq P(t) \leq P_{\max}$$

### 5.1.2.2 输入约束

控制输入（如阀门开度、泵速等）同样受到物理限制。设控制输入为 $\mathbf{u} \in \mathcal{U} \subset \mathbb{R}^p$，其中 $\mathcal{U}$ 是允许的控制输入集合：

$$\mathcal{U} = \{\mathbf{u} \in \mathbb{R}^p : u_{j,\min} \leq u_j \leq u_{j,\max}, \quad j = 1, 2, \ldots, p\}$$

输入约束通常以箱型约束的形式出现，反映了执行器的物理限制。例如，阀门开度 $\alpha$ 满足 $0 \leq \alpha \leq 100\%$，泵速 $n$ 满足 $n_{\min} \leq n \leq n_{\max}$。

### 5.1.2.3 混合约束

实际水系统中存在大量涉及状态和输入的耦合约束。例如，为防止水锤效应，阀门关闭速度需要与当前流量相关联：

$$\left|\frac{d\alpha}{dt}\right| \leq k_1 + k_2 Q(t)$$

这类混合约束可以统一表示为：

$$g(\mathbf{x}, \mathbf{u}, \dot{\mathbf{u}}) \geq 0$$

## 5.1.3 控制障碍函数方法

控制障碍函数（Control Barrier Functions, CBF）是近年来安全关键控制领域的重要理论工具，为安全约束的形式化提供了一种系统性的方法[1]。CBF方法通过构造一个标量函数 $B(\mathbf{x})$，将高维状态空间中的安全集合边界转化为函数值的约束条件。

### 5.1.3.1 CBF的定义与性质

**定义5.1（控制障碍函数）**：对于系统 $\dot{\mathbf{x}} = \mathbf{f}(\mathbf{x}) + \mathbf{g}(\mathbf{x})\mathbf{u}$ 和安全集合 $\mathcal{S} = \{\mathbf{x} : h(\mathbf{x}) \geq 0\}$，若存在连续可微函数 $B: \mathbb{R}^n \rightarrow \mathbb{R}$ 满足：

1. **边界条件**：$B(\mathbf{x}) \rightarrow \infty$ 当 $h(\mathbf{x}) \rightarrow 0^+$
2. **控制条件**：$\forall \mathbf{x} \in \text{int}(\mathcal{S}), \exists \mathbf{u} \in \mathcal{U}$ 使得

$$\dot{B}(\mathbf{x}, \mathbf{u}) = L_f B(\mathbf{x}) + L_g B(\mathbf{x})\mathbf{u} \leq \frac{\gamma}{B(\mathbf{x})}$$

其中 $\gamma > 0$ 是设计参数，$L_f B$ 和 $L_g B$ 分别表示 $B$ 沿向量场 $\mathbf{f}$ 和 $\mathbf{g}$ 的李导数。

则称 $B(\mathbf{x})$ 为安全集合 $\mathcal{S}$ 的一个控制障碍函数。

CBF的核心价值在于将集合不变性问题转化为一个可计算的优化问题。若存在有效的CBF，则可以通过二次规划（QP）实时求解安全控制输入：

$$\begin{aligned}
\min_{\mathbf{u}} \quad & \|\mathbf{u} - \mathbf{u}_{\text{nom}}\|^2 \\
\text{s.t.} \quad & L_f B(\mathbf{x}) + L_g B(\mathbf{x})\mathbf{u} \leq \frac{\gamma}{B(\mathbf{x})} \\
& \mathbf{u} \in \mathcal{U}
\end{aligned}$$

其中 $\mathbf{u}_{\text{nom}}$ 是名义控制器（如跟踪控制器）的输出。该优化问题寻找最接近名义控制输入的安全控制动作。

### 5.1.3.2 高阶控制障碍函数

对于相对阶大于1的约束，标准CBF方法需要扩展。高阶控制障碍函数（High-Order CBF, HOCBF）通过引入辅助函数处理高阶动态约束[2]。

**定义5.2（高阶控制障碍函数）**：设 $h(\mathbf{x})$ 的相对阶为 $r$，定义函数序列：

$$\psi_0(\mathbf{x}) = h(\mathbf{x})$$
$$\psi_1(\mathbf{x}) = \dot{\psi}_0(\mathbf{x}) + \alpha_1(\psi_0(\mathbf{x}))$$
$$\vdots$$
$$\psi_r(\mathbf{x}) = \dot{\psi}_{r-1}(\mathbf{x}) + \alpha_r(\psi_{r-1}(\mathbf{x}))$$

其中 $\alpha_i(\cdot)$ 是类$\mathcal{K}$函数。若 $\psi_r(\mathbf{x})$ 满足CBF条件，则称 $h(\mathbf{x})$ 具有有效的HOCBF。

### 5.1.3.3 指数控制障碍函数

指数控制障碍函数（Exponential CBF, ECBF）提供了一种更灵活的安全约束形式化方法[3]。ECBF要求：

$$\dot{B}(\mathbf{x}, \mathbf{u}) \leq -\lambda B(\mathbf{x})$$

其中 $\lambda > 0$ 是衰减率参数。该条件保证了安全集合的指数级不变性，即系统状态以指数速度收敛到安全区域内部。

## 5.1.4 安全约束的时序逻辑描述

对于涉及时间演化的复杂安全要求，线性时序逻辑（Linear Temporal Logic, LTL）和信号时序逻辑（Signal Temporal Logic, STL）提供了强大的形式化工具[4]。

### 5.1.4.1 线性时序逻辑基础

LTL通过时序算子描述系统行为的时序特性：

- **$\bigcirc \phi$**（Next）：下一时刻$\phi$成立
- **$\phi \, \mathcal{U} \, \psi$**（Until）：$\phi$持续成立直到$\psi$成立
- **$\square \phi$**（Always）：$\phi$永远成立
- **$\Diamond \phi$**（Eventually）：$\phi$最终成立

**示例**：水库水位安全要求"水位永远不会低于最低安全水位"可以表示为：

$$\square (h(t) \geq h_{\min})$$

**示例**：紧急泄洪要求"当水位超过警戒值时，必须在10分钟内开始泄洪"可以表示为：

$$\square \left( (h(t) > h_{\text{alert}}) \rightarrow \Diamond_{[0,10]} (Q_{\text{out}} > Q_{\text{emergency}}) \right)$$

### 5.1.4.2 信号时序逻辑

STL扩展了LTL，支持连续信号和实时约束。STL的语义定义在实值信号上，通过鲁棒性度量（robustness degree）量化公式满足程度[5]。

对于谓词 $\mu: h(\mathbf{x}) \geq 0$，其鲁棒性度量为：

$$\rho(\mu, \mathbf{x}, t) = h(\mathbf{x}(t))$$

时序算子的鲁棒性递归定义为：

$$\rho(\neg \phi, \mathbf{x}, t) = -\rho(\phi, \mathbf{x}, t)$$
$$\rho(\phi_1 \wedge \phi_2, \mathbf{x}, t) = \min(\rho(\phi_1, \mathbf{x}, t), \rho(\phi_2, \mathbf{x}, t))$$
$$\rho(\Diamond_{[a,b]} \phi, \mathbf{x}, t) = \sup_{\tau \in [t+a, t+b]} \rho(\phi, \mathbf{x}, \tau)$$

正鲁棒性表示公式被满足，负鲁棒性表示被违反，绝对值表示满足/违反的程度。

## 5.1.5 水系统安全约束的形式化实例

### 5.1.5.1 水库调度安全约束

考虑具有防洪、供水双重功能的水库，其安全约束包括：

**防洪安全约束**：

$$\square \left( V(t) \leq V_{\text{flood}} \right) \wedge \square \left( Q_{\text{out}}(t) \leq Q_{\text{downstream}}^{\max} \right)$$

**供水安全约束**：

$$\square \left( V(t) \geq V_{\text{dead}} \right) \wedge \square_{\text{day}} \left( Q_{\text{supply}}(t) \geq D(t) \right)$$

其中 $\square_{\text{day}}$ 表示在每日供水时段内始终成立，$D(t)$ 是时变需水量。

### 5.1.5.2 供水管网压力约束

供水管网需要维持足够的压力以服务用户，同时避免过高压力导致爆管。形式化约束为：

$$\square \left( \forall i \in \mathcal{N}: P_i^{\min} \leq P_i(t) \leq P_i^{\max} \right)$$

其中 $\mathcal{N}$ 是管网节点集合，$P_i$ 是节点 $i$ 的压力。

### 5.1.5.3 水质安全约束

对于涉及水质控制的水系统，需要形式化描述水质指标约束：

$$\square \left( C_i(t) \leq C_i^{\text{std}} \right) \wedge \square \left( \text{RT}(t) \leq \text{RT}^{\max} \right)$$

其中 $C_i$ 是污染物浓度，$\text{RT}$ 是水力停留时间。

## 5.1.6 安全约束的验证与综合

### 5.1.6.1 形式化验证方法

形式化验证通过数学证明确认系统满足安全规范。主要方法包括：

**模型检验**：对有限状态抽象模型进行穷举分析，验证所有可能执行轨迹满足安全性质。对于水系统，通常需要对连续动态进行离散化抽象。

**定理证明**：使用交互式或自动定理证明器，基于系统模型和安全规范构造形式化证明。适用于复杂无限状态系统。

**可达性分析**：计算系统从初始状态集合出发的可达状态集合，验证其与不安全集合的交集为空：

$$\text{Reach}(\mathcal{X}_0) \cap \mathcal{X}_{\text{unsafe}} = \emptyset$$

### 5.1.6.2 安全控制器综合

安全控制器综合旨在自动构造满足安全规范的控制器。基于CBF的综合方法通过求解优化问题实时生成安全控制输入。基于博弈的方法将控制器设计建模为与环境的博弈，寻找必胜策略[6]。

对于水系统，安全控制器综合需要考虑：
- 系统模型的不确定性
- 外部扰动（如来水、需水）的预测
- 多目标权衡（安全与效率）
- 计算实时性要求

## 5.1.7 本章小结

安全约束的形式化是水系统安全控制的理论基础。本章系统介绍了：

1. **数学描述框架**：通过状态空间、输入空间和混合约束的统一描述，建立了安全约束的数学基础。

2. **控制障碍函数方法**：CBF及其扩展（HOCBF、ECBF）提供了将安全约束嵌入控制设计的系统方法，通过二次规划实现实时安全控制。

3. **时序逻辑方法**：LTL和STL为表达复杂时序安全要求提供了形式化语言，鲁棒性度量支持定量安全分析。

4. **验证与综合**：形式化验证方法确保系统设计满足安全规范，安全控制器综合方法自动生成满足约束的控制策略。

这些方法为水系统控制的安全保障提供了严格的数学工具，是实现自主安全运行的关键支撑技术。

---

## 参考文献

[1] AMES A D, COOGAN S, EGERSTEDT M, et al. Control barrier functions: Theory and applications[C]//2019 18th European Control Conference (ECC). IEEE, 2019: 3420-3431.

[2] XIAO W, BELTA C. Control barrier functions for systems with high relative degree[C]//2019 IEEE 58th Conference on Decision and Control (CDC). IEEE, 2019: 474-479.

[3] NGUYEN Q, SREENATH K. Exponential control barrier functions for enforcing high relative-degree safety-critical constraints[C]//2016 American Control Conference (ACC). IEEE, 2016: 322-328.

[4] BELTA C, BICCHI A, EGERSTEDT M, et al. Symbolic planning and control of robot motion[J]. IEEE Robotics & Automation Magazine, 2007, 14(1): 61-70.

[5] DONZÉ A, MALER O. Robust satisfaction of temporal logic over real-valued signals[C]//International Conference on Formal Modeling and Analysis of Timed Systems. Springer, 2010: 92-106.

[6] TABUADA P. Verification and control of hybrid systems: A symbolic approach[M]. Springer Science & Business Media, 2009.

[7] WIELAND P, ALLGÖWER F. Constructive safety using control barrier functions[C]//2007 7th IFAC Symposium on Nonlinear Control Systems. IFAC, 2007: 462-467.

[8] ROMDLONY M Z, JAYAWARDHANA B. Stabilization with guaranteed safety using control Lyapunov-barrier function[J]. Automatica, 2016, 66: 39-47.

[9] AGRAWAL D R, PETERS S, TOMLIN C J, et al. Discrete control barrier functions for safety-critical control of discrete systems with application to bipedal robot navigation[C]//Robotics: Science and Systems. 2017.

[10] CHEN X, ABRAHÁM E, SANKARANARAYANAN S. Flow*: An analyzer for non-linear hybrid systems[C]//International Conference on Computer Aided Verification. Springer, 2013: 258-263.

[11] PRAINA S, JADBABAIE A, PAPPAS G J. A framework for worst-case and stochastic safety verification using barrier certificates[J]. IEEE Transactions on Automatic Control, 2007, 52(8): 1415-1428.

[12] MAGHENEM M, SANFELICE R G. Sufficient conditions for forward invariance and contractivity in hybrid inclusions using barrier certificates[J]. Automatica, 2022, 135: 109984.

</ama-doc>
