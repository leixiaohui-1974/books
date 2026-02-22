<ama-doc>

# 5.6 故障诊断与容错

## 5.6.1 引言

故障诊断与容错控制是确保水系统长期可靠运行的关键技术。水系统作为关键基础设施，其故障可能导致严重的经济损失、社会影响甚至人员伤亡。故障诊断技术通过监测系统运行状态，及时识别和定位故障；容错控制技术则在故障发生后，通过重构控制策略，维持系统的基本功能或安全状态[1]。

随着水系统自动化程度的提高，故障诊断与容错控制面临着新的挑战：系统规模日益庞大，组件数量众多，故障模式复杂多样；系统间耦合紧密，局部故障可能传播放大；运行环境多变，正常运行与故障状态的边界模糊。这些挑战要求故障诊断与容错控制技术具备高灵敏度、高准确性和强适应性。

## 5.6.2 故障诊断方法分类

### 5.6.2.1 基于模型的方法

基于模型的故障诊断利用系统的数学模型生成残差信号，通过分析残差特性检测和隔离故障[2]。

**残差生成**：

$$\mathbf{r}(t) = \mathbf{y}(t) - \hat{\mathbf{y}}(t) = \mathbf{y}(t) - \mathbf{h}(\hat{\mathbf{x}}(t))$$

其中 $\mathbf{y}(t)$ 是实际测量，$\hat{\mathbf{y}}(t)$ 是模型预测输出。

**残差评价**：

$$J = \|\mathbf{r}\|_W = \sqrt{\mathbf{r}^T \mathbf{W} \mathbf{r}}$$

$$\text{Decision} = \begin{cases} H_0 \text{ (无故障)}, & J \leq J_{th} \\ H_1 \text{ (有故障)}, & J > J_{th} \end{cases}$$

**故障隔离**：通过结构化残差设计，使不同故障在残差空间中产生可区分的模式。

### 5.6.2.2 基于数据的方法

基于数据的方法不依赖精确的数学模型，而是从历史数据中学习正常和故障模式的特征[3]。

**主成分分析（PCA）**：

$$\mathbf{T} = \mathbf{X}\mathbf{P}$$

其中 $\mathbf{P}$ 是主成分载荷矩阵，$\mathbf{T}$ 是得分矩阵。故障检测统计量：

$$T^2 = \mathbf{t}^T \mathbf{\Lambda}^{-1} \mathbf{t}, \quad Q = \|\mathbf{x} - \hat{\mathbf{x}}\|^2$$

**支持向量机（SVM）**：

寻找最优分类超平面：

$$\min_{\mathbf{w}, b} \frac{1}{2}\|\mathbf{w}\|^2 + C\sum_{i=1}^N \xi_i$$
$$\text{s.t.} \quad y_i(\mathbf{w}^T\phi(\mathbf{x}_i) + b) \geq 1 - \xi_i$$

**深度学习方法**：

- 自动编码器：学习正常数据的低维表示
- 卷积神经网络：提取时序数据的特征
- 循环神经网络：建模动态序列

### 5.6.2.3 基于知识的方法

基于知识的方法利用专家经验和领域知识进行故障诊断[4]。

**专家系统**：

基于规则的推理：

$$\text{IF } (P_1 \wedge P_2 \wedge \cdots \wedge P_n) \text{ THEN } F_i$$

其中 $P_j$ 是症状，$F_i$ 是故障结论。

**模糊逻辑**：

处理诊断中的不确定性和模糊性：

$$\mu_F(x) = \text{隶属度函数}$$

**故障树分析**：

从顶事件（系统故障）向下分解，识别基本事件（组件故障）及其逻辑关系。

## 5.6.3 故障诊断的定量方法

### 5.6.3.1 参数估计方法

当故障表现为系统参数变化时，可通过在线参数估计检测故障。

**递推最小二乘（RLS）**：

$$\hat{\boldsymbol{\theta}}_k = \hat{\boldsymbol{\theta}}_{k-1} + \mathbf{K}_k(y_k - \boldsymbol{\phi}_k^T \hat{\boldsymbol{\theta}}_{k-1})$$
$$\mathbf{K}_k = \frac{\mathbf{P}_{k-1}\boldsymbol{\phi}_k}{\lambda + \boldsymbol{\phi}_k^T \mathbf{P}_{k-1}\boldsymbol{\phi}_k}$$

**故障决策**：

$$|\hat{\theta}_i - \theta_{i0}| > \delta_{th} \Rightarrow \text{Fault detected}$$

### 5.6.3.2 观测器组方法

通过设计多个观测器，每个观测器对特定故障敏感或鲁棒，实现故障隔离[5]。

**专用观测器方案**：

为每个可能的故障设计专用观测器，使其对该故障敏感而对其他故障鲁棒。

**广义观测器方案**：

设计观测器组，使得残差空间具有特定的方向性特征。

**故障隔离矩阵**：

$$\mathbf{S} = \begin{bmatrix} s_{11} & s_{12} & \cdots & s_{1n_f} \\ s_{21} & s_{22} & \cdots & s_{2n_f} \\ \vdots & \vdots & \ddots & \vdots \\ s_{n_r1} & s_{n_r2} & \cdots & s_{n_rn_f} \end{bmatrix}$$

其中 $s_{ij} = 1$ 表示第 $i$ 个残差对第 $j$ 个故障敏感。

### 5.6.3.3 奇偶空间方法

奇偶空间方法通过代数冗余关系生成残差：

$$\mathbf{V}_s \mathbf{Y}_s = \mathbf{V}_s (\mathbf{H}_s \mathbf{x} + \mathbf{E}_s \mathbf{f} + \mathbf{N}_s \mathbf{n}) = \mathbf{V}_s \mathbf{E}_s \mathbf{f} + \mathbf{V}_s \mathbf{N}_s \mathbf{n}$$

其中 $\mathbf{V}_s$ 是奇偶向量，满足 $\mathbf{V}_s \mathbf{H}_s = 0$。

## 5.6.4 容错控制基础

### 5.6.4.1 容错控制定义与分类

**定义5.6（容错控制）**：容错控制（Fault-Tolerant Control, FTC）是使系统在组件故障情况下仍能保持稳定性或 acceptable 性能的控制技术[6]。

**被动容错控制（PFTC）**：

- 固定控制器结构
- 对预设故障集具有鲁棒性
- 不需要在线故障信息

**主动容错控制（AFTC）**：

- 在线故障检测与诊断
- 根据故障信息重构控制
- 自适应或切换控制策略

### 5.6.4.2 被动容错控制设计

**可靠镇定**：

设计控制器使得闭环系统对特定故障集保持稳定：

$$\dot{\mathbf{x}} = (\mathbf{A} + \mathbf{B}\mathbf{K}\mathbf{F}_i)\mathbf{x}, \quad \forall \mathbf{F}_i \in \mathcal{F}$$

其中 $\mathbf{F}_i$ 表示第 $i$ 种执行器故障模式。

**同时镇定**：

寻找单一控制器同时镇定多个故障模型：

$$\exists \mathbf{K}: \lambda(\mathbf{A}_i + \mathbf{B}_i\mathbf{K}) \subset \mathbb{C}^-, \quad i = 1, \ldots, N$$

**鲁棒H∞设计**：

$$\min_{\mathbf{K}} \max_{\mathbf{F} \in \mathcal{F}} \|T_{zw}(\mathbf{K}, \mathbf{F})\|_\infty$$

### 5.6.4.3 主动容错控制设计

**控制重构**：

根据故障信息重新设计控制器：

$$\mathbf{u} = \mathbf{K}(\hat{\mathbf{f}})\mathbf{x}$$

**伪逆方法**：

当执行器故障时，重新分配控制作用：

$$\mathbf{u}_{\text{new}} = \mathbf{B}_{\text{fault}}^+ \mathbf{B}_{\text{nom}} \mathbf{u}_{\text{nom}}$$

其中 $\mathbf{B}_{\text{fault}}^+$ 是故障后输入矩阵的伪逆。

**模型参考自适应**：

$$\dot{\hat{\mathbf{x}}} = \mathbf{A}_m \hat{\mathbf{x}} + \mathbf{B}_m \mathbf{r} + \mathbf{L}(\mathbf{y} - \hat{\mathbf{y}})$$
$$\mathbf{u} = \boldsymbol{\theta}_1^T \boldsymbol{\phi}_1(\mathbf{x}) + \boldsymbol{\theta}_2^T \boldsymbol{\phi}_2(\mathbf{r})$$

自适应律根据跟踪误差更新参数。

## 5.6.5 水系统故障诊断应用

### 5.6.5.1 泵站故障诊断

**常见故障模式**：

| 故障类型 | 症状 | 诊断方法 |
|----------|------|----------|
| 轴承磨损 | 振动增大、温度升高 | 振动频谱分析 |
| 叶轮损坏 | 流量-扬程曲线变化 | 参数估计 |
| 密封泄漏 | 流量异常、压力波动 | 观测器残差 |
| 电机故障 | 电流异常、温升 | 电气特征分析 |

**振动诊断**：

频谱特征提取：

$$X(f) = \text{FFT}(x(t))$$

特征频率：
- 轴承故障：BPFO、BPFI、BSF、FTF
- 叶轮故障：叶片通过频率
- 不对中：2倍转频

### 5.6.5.2 管网泄漏检测

**基于水力模型的方法**：

夜间最小流量分析：

$$Q_{\min} = \sum_{i} Q_{\text{base},i} + Q_{\text{leak}}$$

压力变化分析：

$$\Delta P = f(Q_{\text{leak}}, \text{location})$$

**基于信号处理的方法**：

负压波检测：

$$\Delta P(t) = \Delta P_0 e^{-\alpha t} \cos(\omega t + \phi)$$

相关分析：

$$R_{12}(\tau) = \int x_1(t) x_2(t+\tau) dt$$

泄漏位置：

$$L_1 = \frac{L + v \cdot \tau_{\max}}{2}$$

### 5.6.5.3 水质异常检测

**统计过程控制**：

$$\text{UCL} = \mu + 3\sigma, \quad \text{LCL} = \mu - 3\sigma$$

**多变量监测**：

$$T^2 = (\mathbf{x} - \boldsymbol{\mu})^T \mathbf{\Sigma}^{-1} (\mathbf{x} - \boldsymbol{\mu})$$

**事件识别**：

- 余氯异常：加氯设备故障或污染源入侵
- 浊度异常：滤池穿透或原水恶化
- pH异常：化学投加系统故障

## 5.6.6 水系统容错控制

### 5.6.6.1 泵组容错控制

**冗余配置**：

- N+1冗余：N台运行，1台备用
- N+2冗余：N台运行，2台备用
- 轮换运行：均衡磨损

**故障重构**：

当一台泵故障时，启动备用泵并重新分配负荷：

$$Q_{\text{total}} = \sum_{i \in \text{healthy}} Q_i$$

优化调度：

$$\min \sum_{i} P_i(Q_i) \quad \text{s.t.} \quad \sum_{i} Q_i = D$$

### 5.6.6.2 阀门容错控制

**故障模式**：
- 卡死在当前位置
- 卡死在全开/全关
- 响应迟缓

**重构策略**：

- 利用冗余阀门调节
- 调整其他控制手段补偿
- 切换运行模式

### 5.6.6.3 传感器容错

**传感器融合**：

多传感器数据融合提高可靠性：

$$\hat{x} = \sum_{i} w_i y_i, \quad w_i = \frac{\sigma_i^{-2}}{\sum_j \sigma_j^{-2}}$$

**软测量技术**：

当传感器故障时，用模型估计替代：

$$y_{\text{soft}} = f(u_1, u_2, \ldots, y_{\text{other}})$$

## 5.6.7 故障诊断与容错的集成

### 5.6.7.1 集成架构

故障诊断与容错控制的集成架构包括：

1. **监测层**：数据采集与预处理
2. **诊断层**：故障检测、隔离与辨识
3. **决策层**：故障评估与响应决策
4. **执行层**：控制重构与执行

### 5.6.7.2 实时性考虑

故障诊断与容错控制需要满足实时性要求：

**检测时间**：从故障发生到检测的时间 $T_d$

**隔离时间**：从检测到隔离的时间 $T_i$

**重构时间**：从隔离到控制重构的时间 $T_r$

总响应时间：$T_{\text{total}} = T_d + T_i + T_r$

### 5.6.7.3 可靠性分析

容错控制系统的可靠性：

$$R_{\text{FTC}}(t) = R_{\text{plant}}(t) \cdot R_{\text{FDI}}(t) \cdot R_{\text{controller}}(t)$$

考虑诊断误差的可靠性：

$$R_{\text{actual}} = (1 - P_{\text{MD}}) R_{\text{nom}} + P_{\text{FA}} R_{\text{degraded}}$$

其中 $P_{\text{MD}}$ 是漏检概率，$P_{\text{FA}}$ 是虚警概率。

## 5.6.8 本章小结

故障诊断与容错控制是保障水系统安全可靠运行的核心技术。本章系统介绍了：

1. **诊断方法分类**：基于模型、数据和知识的故障诊断方法，为不同应用场景提供了方法选择。

2. **定量诊断方法**：详细阐述了参数估计、观测器组和奇偶空间等定量故障诊断技术。

3. **容错控制基础**：介绍了被动容错和主动容错的设计原理和方法。

4. **水系统应用**：针对泵站、管网、水质等典型应用场景进行了具体分析。

5. **集成架构**：讨论了故障诊断与容错控制的集成架构、实时性考虑和可靠性分析。

故障诊断与容错控制技术的发展，将显著提升水系统应对异常工况的能力，为自主安全运行提供坚实保障。

---

## 参考文献

[1] BLANKE M, KINNAERT M, LUNZE J, et al. Diagnosis and fault-tolerant control[M]. Springer Science & Business Media, 2006.

[2] CHEN J, PATTON R J. Robust model-based fault diagnosis for dynamic systems[M]. Springer Science & Business Media, 1999.

[3] YIN S, DING S X, XIE X, et al. A review on basic data-driven approaches for industrial process monitoring[J]. IEEE Transactions on Industrial Electronics, 2014, 61(11): 6418-6428.

[4] VENKATASUBRAMANIAN V, RENGASWAMY R, YIN K, et al. A review of process fault detection and diagnosis: Part I: Quantitative model-based methods[J]. Computers & Chemical Engineering, 2003, 27(3): 293-311.

[5] FRANK P M. Fault diagnosis in dynamic systems using analytical and knowledge-based redundancy: A survey and some new results[J]. Automatica, 1990, 26(3): 459-474.

[6] NOURA H, THEILLIOL D, PONSART J C, et al. Fault-tolerant control systems: Design and practical applications[M]. Springer Science & Business Media, 2009.

[7] BLANKE M, SCHRÖDER J, LUNZE J, et al. Fault-tolerant safe control for water networks[J]. Control Engineering Practice, 2024, 145: 105789.

[8] PUUST R, KAPELAN Z, SAVIC D A, et al. A review of methods for leakage management in pipe networks[J]. Urban Water Journal, 2010, 7(1): 25-45.

[9] COLOMBANO G, ALLEN M, PREIS A, et al. Fault-tolerant safe control for water networks[C]//IFAC-PapersOnLine. 2024, 57(6): 123-130.

[10] FANG T, LAU A. Sensor fault diagnosis for water distribution networks using machine learning[C]//Proceedings of the World Environmental and Water Resources Congress. 2019: 234-245.

[11] GERTLER J. Fault detection and diagnosis in engineering systems[M]. CRC Press, 1998.

[12] ISERMANN R. Fault-diagnosis systems: An introduction from fault detection to fault tolerance[M]. Springer, 2006.

</ama-doc>
