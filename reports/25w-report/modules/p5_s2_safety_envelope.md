<ama-doc>

# 5.2 安全包络概念

## 5.2.1 引言

安全包络（Safety Envelope）是安全关键控制系统中的核心概念，它定义了系统在不违反安全约束的前提下可以运行的状态空间区域[1]。与简单的安全边界不同，安全包络是一个动态演化的概念，综合考虑了系统当前状态、动态特性、控制能力和外部扰动等因素，为实时安全决策提供了量化依据。

在水系统控制领域，安全包络的概念具有特别重要的意义。水系统通常具有大惯性、强耦合、多约束的特点，传统的基于固定阈值的安全监控方法难以适应复杂多变的运行工况。安全包络方法通过建立状态相关的动态安全边界，能够在保障安全的同时最大化系统的运行效率和灵活性。

## 5.2.2 安全包络的基本定义

### 5.2.2.1 数学定义

**定义5.3（安全包络）**：对于动态系统 $\dot{\mathbf{x}} = \mathbf{f}(\mathbf{x}, \mathbf{u}, \mathbf{d})$，其中 $\mathbf{x} \in \mathbb{R}^n$ 是状态，$\mathbf{u} \in \mathcal{U}$ 是控制输入，$\mathbf{d} \in \mathcal{D}$ 是有界扰动，安全包络 $\mathcal{E}(t)$ 是状态空间中的一个时变集合，满足：

1. **可行性**：对于任意 $\mathbf{x} \in \mathcal{E}(t)$，存在控制策略 $\mathbf{u}(\tau) \in \mathcal{U}, \tau \geq t$，使得对所有容许扰动 $\mathbf{d}(\tau) \in \mathcal{D}$，系统轨迹满足 $\mathbf{x}(\tau) \in \mathcal{S}$（安全集合）。

2. **不变性**：若 $\mathbf{x}(t) \in \mathcal{E}(t)$，则通过适当控制，可以维持 $\mathbf{x}(\tau) \in \mathcal{E}(\tau)$ 对所有 $\tau \geq t$ 成立。

3. **最大性**：$\mathcal{E}(t)$ 是满足上述条件的最大集合。

安全包络 $\mathcal{E}(t)$ 与固定安全集合 $\mathcal{S}$ 的关系为 $\mathcal{E}(t) \subseteq \mathcal{S}$，且通常 $\mathcal{E}(t) \subset \mathcal{S}$，即在安全集合内部存在一个"安全裕度"区域。

### 5.2.2.2 安全包络的物理意义

安全包络的物理意义可以从多个维度理解：

**可控性维度**：安全包络内的任何状态都可以通过适当的控制动作避免进入危险区域。这要求系统具有足够的控制权限来抵消扰动的影响。

**可达性维度**：从安全包络内的状态出发，存在至少一条轨迹可以永远保持在安全集合内。这与微分博弈中的" discriminating kernel"概念相关[2]。

**鲁棒性维度**：安全包络考虑了最坏情况下的扰动，确保即使在不利条件下也能维持安全。

## 5.2.3 安全包络的计算方法

### 5.2.3.1 基于水平集的方法

水平集方法通过求解Hamilton-Jacobi偏微分方程计算安全包络的边界[3]。设价值函数 $V(\mathbf{x}, t)$ 表示从状态 $\mathbf{x}$ 出发能够维持安全的"代价"，则安全包络边界对应于 $V(\mathbf{x}, t) = 0$ 的等值面。

价值函数满足Hamilton-Jacobi-Isaacs方程：

$$\frac{\partial V}{\partial t} + \min\left\{0, \max_{\mathbf{u} \in \mathcal{U}} \min_{\mathbf{d} \in \mathcal{D}} \nabla V \cdot \mathbf{f}(\mathbf{x}, \mathbf{u}, \mathbf{d})\right\} = 0$$

边界条件为：

$$V(\mathbf{x}, T) = l(\mathbf{x})$$

其中 $l(\mathbf{x})$ 是终端代价函数，在危险区域取正值，在安全区域取负值。

安全包络定义为：

$$\mathcal{E}(t) = \{\mathbf{x} : V(\mathbf{x}, t) \leq 0\}$$

水平集方法的优点是可以处理非线性动态和复杂约束，缺点是计算复杂度高，通常仅限于低维系统。

### 5.2.3.2 基于障碍函数的方法

控制障碍函数方法提供了计算安全包络的替代途径。若 $B(\mathbf{x})$ 是有效的控制障碍函数，则其子水平集定义了一个安全区域：

$$\mathcal{E}_c = \{\mathbf{x} : B(\mathbf{x}) \leq c\}$$

对于给定的 $c > 0$，只要系统初始状态满足 $B(\mathbf{x}_0) \leq c$，且控制输入满足CBF条件，则系统将永远保持在 $\mathcal{E}_c$ 内。

通过选择不同的 $c$ 值，可以得到一族嵌套的安全包络：

$$\mathcal{E}_{c_1} \subset \mathcal{E}_{c_2} \subset \cdots \subset \mathcal{E}_{c_n}, \quad c_1 < c_2 < \cdots \u003c c_n$$

这提供了安全裕度的分级描述，支持渐进式的安全干预策略。

### 5.2.3.3 基于可达集的方法

可达集方法通过计算系统在给定时间 horizon 内的可达状态集合来确定安全包络[4]。

**后向可达集**：从目标集合 $\mathcal{T}$ 出发，计算能够到达 $\mathcal{T}$ 的初始状态集合：

$$\text{Reach}_{\text{bwd}}(\mathcal{T}, [0, T]) = \{\mathbf{x}_0 : \exists \mathbf{u}, \mathbf{d}, \mathbf{x}(T) \in \mathcal{T}\}$$

**前向可达集**：从初始状态 $\mathbf{x}_0$ 出发，计算系统可能到达的状态集合：

$$\text{Reach}_{\text{fwd}}(\mathbf{x}_0, [0, T]) = \{\mathbf{x}(T) : \exists \mathbf{u}, \mathbf{d}\}$$

安全包络可以表征为不与危险集合相交的最大可控不变集：

$$\mathcal{E} = \{\mathbf{x}_0 : \text{Reach}_{\text{fwd}}(\mathbf{x}_0, [0, \infty)) \cap \mathcal{X}_{\text{danger}} = \emptyset\}$$

### 5.2.3.4 基于数据驱动的方法

对于复杂水系统，基于模型的安全包络计算可能面临模型不准确的问题。数据驱动方法通过学习大量运行数据来估计安全包络[5]。

**支持向量机方法**：将安全/不安全运行数据作为训练样本，学习安全包络的分类边界：

$$\mathcal{E} = \{\mathbf{x} : \sum_{i} \alpha_i y_i K(\mathbf{x}_i, \mathbf{x}) + b \geq 0\}$$

其中 $K(\cdot, \cdot)$ 是核函数，$\alpha_i$ 和 $b$ 是训练得到的参数。

**高斯过程方法**：通过高斯过程回归学习安全裕度的概率分布：

$$p(B(\mathbf{x}) | \mathcal{D}) = \mathcal{N}(\mu(\mathbf{x}), \sigma^2(\mathbf{x}))$$

其中 $\mathcal{D}$ 是观测数据，$\mu(\mathbf{x})$ 和 $\sigma(\mathbf{x})$ 分别是均值和标准差。

## 5.2.4 水系统的安全包络建模

### 5.2.4.1 水库安全包络

水库的安全包络需要综合考虑防洪、供水、生态等多重约束。设水库状态为 $\mathbf{x} = [V, Q_{\text{in}}]^T$，其中 $V$ 是库容，$Q_{\text{in}}$ 是入流。

**防洪安全包络**：考虑下游河道安全泄量 $Q_{\text{safe}}$ 和最大库容 $V_{\max}$：

$$\mathcal{E}_{\text{flood}} = \{(V, Q_{\text{in}}) : V \leq V_{\max} - \Delta V(Q_{\text{in}})\}$$

其中 $\Delta V(Q_{\text{in}})$ 是考虑入流不确定性的安全裕度：

$$\Delta V(Q_{\text{in}}) = \int_0^{T_{\text{resp}}} \max(0, Q_{\text{in}}(t) - Q_{\text{safe}}) dt$$

$T_{\text{resp}}$ 是系统响应时间。

**供水安全包络**：考虑供水保证率和死库容：

$$\mathcal{E}_{\text{supply}} = \{(V, D) : V \geq V_{\text{dead}} + \int_0^{T_{\text{drought}}} D(t) dt\}$$

其中 $D$ 是需水量，$T_{\text{drought}}$ 是设计干旱期长度。

### 5.2.4.2 渠道系统安全包络

明渠水流的安全包络需要考虑水力稳定性约束。基于圣维南方程，渠道状态由水位和流量描述。

**稳定流安全包络**：确保弗劳德数处于亚临界范围：

$$\mathcal{E}_{\text{stable}} = \{(h, Q) : Fr = \frac{Q}{A\sqrt{gD_h}} \leq Fr_{\text{crit}} - \Delta Fr\}$$

其中 $A$ 是过水断面面积，$D_h$ 是水力直径，$\Delta Fr$ 是安全裕度。

**溢流安全包络**：防止渠道漫顶：

$$\mathcal{E}_{\text{freeboard}} = \{(h, Q) : h \leq h_{\text{max}} - \Delta h(Q)\}$$

$\Delta h(Q)$ 考虑了流量波动引起的水面波动。

### 5.2.4.3 供水管网安全包络

供水管网的安全包络涉及节点压力和管段流速的多维约束。

**压力安全包络**：

$$\mathcal{E}_{\text{pressure}} = \{\mathbf{P} : P_i^{\min} + \Delta P_i \leq P_i \leq P_i^{\max} - \Delta P_i, \forall i\}$$

其中 $\Delta P_i$ 是压力波动裕度，与系统水力特性相关。

**水锤安全包络**：考虑瞬态压力波动：

$$\mathcal{E}_{\text{hammer}} = \{(\mathbf{P}, \mathbf{Q}) : P_i + \Delta P_{\text{hammer}}(\mathbf{Q}, \dot{\mathbf{Q}}) \leq P_i^{\max}\}$$

## 5.2.5 安全包络的动态更新

### 5.2.5.1 基于预测的包络更新

安全包络应根据系统状态和环境变化动态更新。基于模型预测的方法利用预测信息调整安全包络：

$$\mathcal{E}(t) = f(\mathbf{x}(t), \hat{\mathbf{d}}_{t:t+T}, \mathcal{M})$$

其中 $\hat{\mathbf{d}}_{t:t+T}$ 是未来扰动的预测，$\mathcal{M}$ 是系统模型。

### 5.2.5.2 自适应安全包络

自适应方法根据观测数据在线调整安全包络参数。设安全包络由参数向量 $\boldsymbol{\theta}$ 描述：

$$\mathcal{E}(\boldsymbol{\theta}) = \{\mathbf{x} : g(\mathbf{x}, \boldsymbol{\theta}) \geq 0\}$$

参数更新律可以设计为：

$$\dot{\boldsymbol{\theta}} = \Gamma \phi(\mathbf{x}, \mathbf{u}) e$$

其中 $e$ 是安全裕度误差，$\phi$ 是回归向量，$\Gamma$ 是学习率矩阵。

## 5.2.6 安全包络在控制中的应用

### 5.2.6.1 包络保持控制

包络保持控制的目标是维持系统状态在安全包络内。这可以表述为约束优化问题：

$$\begin{aligned}
\min_{\mathbf{u}} \quad & J(\mathbf{x}, \mathbf{u}) \\
\text{s.t.} \quad & \mathbf{x}(t) \in \mathcal{E}(t) \\
& \dot{\mathbf{x}} = \mathbf{f}(\mathbf{x}, \mathbf{u}, \mathbf{d}) \\
& \mathbf{u} \in \mathcal{U}
\end{aligned}$$

### 5.2.6.2 包络恢复控制

当系统状态接近或超出安全包络边界时，需要启动包络恢复控制：

$$\mathbf{u}_{\text{recovery}} = \arg\min_{\mathbf{u}} \text{dist}(\mathbf{x}(t+\Delta t), \mathcal{E}(t+\Delta t))$$

### 5.2.6.3 多级安全干预

基于嵌套安全包络结构，可以设计多级安全干预策略：

| 层级 | 包络 | 干预措施 |
|------|------|----------|
| 正常 | $\mathcal{E}_1$ | 正常控制 |
| 警戒 | $\mathcal{E}_2 \setminus \mathcal{E}_1$ | 增强监控 |
| 警告 | $\mathcal{E}_3 \setminus \mathcal{E}_2$ | 限制操作 |
| 紧急 | $\mathcal{S} \setminus \mathcal{E}_3$ | 紧急处置 |

## 5.2.7 本章小结

安全包络概念为水系统安全控制提供了动态、量化的分析框架。本章主要贡献包括：

1. **理论定义**：给出了安全包络的严格数学定义，阐明了可行性、不变性和最大性三个核心性质。

2. **计算方法**：系统介绍了水平集方法、障碍函数方法、可达集方法和数据驱动方法，为不同应用场景提供了工具选择。

3. **水系统应用**：针对水库、渠道、管网等典型水系统，建立了具体的安全包络模型。

4. **动态更新**：讨论了基于预测和自适应的安全包络更新机制，支持时变环境下的安全控制。

5. **控制应用**：阐述了安全包络在包络保持、包络恢复和多级干预中的应用方式。

安全包络概念是连接安全理论与控制实践的桥梁，是实现水系统自主安全运行的关键技术。

---

## 参考文献

[1] ALTHOFF M, DOLAN J M. Online verification of automated road vehicles using reachability analysis[J]. IEEE Transactions on Robotics, 2014, 30(4): 903-918.

[2] AUBIN J P. Viability theory[M]. Boston: Birkhäuser, 1991.

[3] MITCHELL I M, BAYEN A M, TOMLIN C J. A time-dependent Hamilton-Jacobi formulation of reachable sets for continuous dynamic games[J]. IEEE Transactions on Automatic Control, 2005, 50(7): 947-957.

[4] CHEN M, HERBERT S L, VASHISHTHA M, et al. Decomposition of reachable sets and tubes for a class of nonlinear systems[J]. IEEE Transactions on Automatic Control, 2021, 66(11): 5379-5394.

[5] FISAC J F, AKAMETALU A K, ZEILINGER M N, et al. A general safety framework for learning-based control in uncertain robotic systems[J]. IEEE Transactions on Automatic Control, 2019, 64(7): 2737-2752.

[6] KAYNAMA S, MITCHELL I M, OISHI M, et al. Computing the viability kernel using maximal reachable sets[C]//International Conference on Hybrid Systems: Computation and Control. ACM, 2012: 55-64.

[7] BANSAL S, CHEN M, HERBERT S L, et al. Hamilton-Jacobi reachability: A brief overview and recent advances[C]//2017 IEEE 56th Annual Conference on Decision and Control (CDC). IEEE, 2017: 2242-2253.

[8] GIRARD A. Reachability of uncertain linear systems using zonotopes[C]//International Conference on Hybrid Systems: Computation and Control. Springer, 2005: 291-305.

[9] KURZHANSKI A B, VARAIYA P. Ellipsoidal techniques for reachability analysis[C]//International Conference on Hybrid Systems: Computation and Control. Springer, 2000: 202-214.

[10] BLANCHINI F, MIANI S. Set-theoretic methods in control[M]. Boston: Birkhäuser, 2008.

[11] RUNGER M, ZAMANI M. Accurate reachability analysis of uncertain nonlinear systems[C]//2019 IEEE 58th Conference on Decision and Control (CDC). IEEE, 2019: 4305-4311.

[12] ALTHOFF M. An introduction to CORA 2015[C]//Proc. of the Workshop on Applied Verification for Continuous and Hybrid Systems. 2015: 120-151.

</ama-doc>
