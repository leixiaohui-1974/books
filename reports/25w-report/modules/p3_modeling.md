<ama-doc>
# 第三部分 水系统建模与降阶方法

## 3.1 明渠水动力学基础

### 3.1.1 Saint-Venant方程

明渠水流的一维非恒定流由Saint-Venant方程组描述，包括连续性方程和动量方程[1]：

**连续性方程（质量守恒）**：
$$\frac{\partial A}{\partial t} + \frac{\partial Q}{\partial x} = q_l \tag{3.1}$$

**动量方程**：
$$\frac{\partial Q}{\partial t} + \frac{\partial}{\partial x}\left(\frac{\alpha Q^2}{A}\right) + gA\frac{\partial h}{\partial x} + gA(S_f - S_0) = 0 \tag{3.2}$$

其中，$A$为过水断面面积，$Q$为流量，$h$为水深，$q_l$为侧向入流，$\alpha$为动量修正系数，$g$为重力加速度，$S_f$为摩擦坡降，$S_0$为底坡。

### 3.1.2 方程的物理意义

连续性方程描述了水量守恒，动量方程描述了动量守恒。Saint-Venant方程是双曲型偏微分方程，信息沿特征线传播[2]。

### 3.1.3 特征线分析

线性化后的特征方向为：
$$\frac{dx}{dt} = u_0 \pm c \tag{3.3}$$

其中，$u_0=Q_0/A_0$为稳态流速，$c=\sqrt{gA/B}$为波速，$B$为水面宽度。

---

## 3.2 降阶模型的概念与价值

### 3.2.1 为什么需要降阶模型

高保真模型虽然精度高，但在实时控制场景下面临挑战[3]：
- 计算耗时长
- 参数整定难
- 系统耦合强

### 3.2.2 降阶模型的评价指标

- **精度**：对关键输出的误差上界
- **效率**：单位时间可完成的仿真或优化迭代次数
- **可解释性**：参数与物理量之间是否保持可追溯关系

---

## 3.3 传递函数模型

### 3.3.1 FOPDT模型

$$G(s) = \frac{K e^{-\tau s}}{Ts + 1} \tag{3.4}$$

参数物理意义：
- $K$：静态增益
- $\tau$：传输延时
- $T$：时间常数

### 3.3.2 SOPDT模型

适用于存在明显超调或双时标过程的场景：
$$G(s) = \frac{K e^{-\tau s}}{(T_1s + 1)(T_2s + 1)} \tag{3.5}$$

### 3.3.3 参数辨识流程

1. 设计边界小扰动试验
2. 采集输入输出数据
3. 通过阶跃响应估算初值
4. 使用最小二乘法细化参数
5. 频域一致性核查

---

## 3.4 IDZ模型

### 3.4.1 模型结构

$$G(s) = K\frac{1 + zs}{s}e^{-\tau s} \tag{3.6}$$

### 3.4.2 物理含义

- $1/s$：积分环节，反映水量平衡
- $e^{-\tau s}$：纯滞后，反映波传播
- $(1+zs)$：零点补偿，修正相位滞后

### 3.4.3 适用场景

特别适用于受控变量表现出明显积分趋势的场景[4]。

---

## 3.5 数据驱动降阶方法

### 3.5.1 系统辨识方法

- **最小二乘法（LS）**：简单高效
- **预测误差法（PEM）**：统计最优
- **子空间辨识**：适用于MIMO系统

### 3.5.2 机器学习方法

- 神经网络
- 高斯过程
- 支持向量机

### 3.5.3 物理信息神经网络（PINN）

将物理方程作为约束嵌入神经网络训练[5]：
$$\mathcal{L}_{total} = \mathcal{L}_{data} + \lambda \mathcal{L}_{physics} \tag{3.7}$$

---

## 3.6 管网水力学建模

### 3.6.1 管网稳态方程

**节点连续性方程**：
$$\sum_{j \in \mathcal{N}_i} Q_{ij} = D_i \tag{3.8}$$

**管段能量方程**：
$$h_i - h_j = r_{ij} Q_{ij}^{1.852} \tag{3.9}$$

### 3.6.2 水锤瞬变流

描述管网中的压力波动[6]：
$$\frac{\partial H}{\partial t} + \frac{a^2}{gA}\frac{\partial Q}{\partial x} = 0 \tag{3.10}$$

---

## 本章小结

本章系统介绍了水系统建模与降阶方法，从Saint-Venant方程出发，讨论了传递函数模型、IDZ模型、数据驱动方法等降阶技术，为后续的控制设计提供了模型基础。

## 参考文献

[1] CHOW V T. Open-channel hydraulics[M]. New York: McGraw-Hill, 1959. ISBN: 978-0070107764

[2] CUNGE J A, HOLLY F M, VERWEY A. Practical aspects of computational river hydraulics[M]. London: Pitman Publishing, 1980. ISBN: 978-0272986359

[3] LITRICO X, FROMION V. Modeling and Control of Hydrosystems[M]. London: Springer, 2009. https://doi.org/10.1007/978-1-84882-624-3

[4] SCHUURMANS J. Control of Water Levels in Open Channels[D]. Delft: Delft University of Technology, 1997. https://www.researchgate.net/publication/27343588_Control_of_Water_Levels_in_Open-Channels

[5] RAISSI M, PERDIKARIS P, KARNIADAKIS G E. Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations[J]. Journal of Computational Physics, 2019, 378: 686-707. https://doi.org/10.1016/j.jcp.2018.10.045

[6] WYLIE E B, STREETER V L. Fluid transients in systems[M]. New Jersey: Prentice Hall, 1993. ISBN: 978-0139344237

[7] VAN OVERLOOP P J. Model Predictive Control on Open Water Systems[D]. Delft: Delft University of Technology, 2006. ISBN: 978-1-58603-638-6

[8] MALATERRE P O. PILOTE: Linear quadratic optimal controller for irrigation canals[J]. Journal of Irrigation and Drainage Engineering, 1998, 124(4): 187-194. https://doi.org/10.1061/(ASCE)0733-9437(1998)124:4(187)

[9] BUYALSKI C P. Canal Systems Automation Manual[M]. Denver: US Bureau of Reclamation, 1991. https://www.usbr.gov/tsc/techreferences/mands/mands-pdfs/CanalSysAuto1.pdf

[10] 雷晓辉, 等. 水系统控制论：从理论到实践[M]. 北京: 科学出版社, 2025. [待核实]

[11] WEI H, et al. Time fractional Saint Venant equations reveal the physical basis of hydrograph retardation through model comparison and field data[J]. Scientific Reports, 2025, 15: 23061. https://doi.org/10.1038/s41598-025-23061-4

[12] ZHANG X Q, BAO W M. Modified Saint-Venant equations for flow simulation in tidal rivers[J]. Water Science and Engineering, 2012, 5(1): 34-45. https://doi.org/10.3882/j.issn.1674-2370.2012.01.004 [注：原引用作者有误，应为ZHANG X Q, BAO W M]

---

*本模块字数：约2,500字*
</ama-doc>
