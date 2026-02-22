<ama-doc>

# 8.2 MIL测试（模型在环测试）

## 8.2.1 引言

模型在环测试（Model-in-the-Loop Testing，MIL）是XIL测试体系中的第一个环节，也是模型驱动开发流程中最基础的验证手段。MIL测试在控制算法的设计阶段即开始进行，通过在被控对象的仿真模型中验证控制器模型的行为，确保控制策略在投入实际实现之前满足设计需求。

MIL测试的核心特征在于其完全基于模型进行，不涉及任何实际代码或硬件。控制器模型和被控对象模型均在统一的仿真环境中运行，这种纯软件验证方式使得设计人员能够快速迭代、早期发现缺陷，并为后续的SIL和HIL测试奠定基础。

本章将深入探讨MIL测试的原理、方法、工具及实践要点，为水培控制系统等嵌入式应用的开发提供理论指导。

## 8.2.2 MIL测试的基本原理

### 8.2.2.1 MIL测试的定义与定位

MIL测试是指在系统开发的早期阶段，使用数学模型对控制算法进行验证的过程。在MIL测试中，控制器以数学模型的形式存在，通常在MATLAB/Simulink、Modelica或类似的建模环境中实现。被控对象同样以数学模型的形式表示，两个模型在仿真环境中闭环运行。

MIL测试在整个V型开发流程中的位置如图8.2-1所示：

```
需求分析 ────────────────────────────────► 系统测试
    │                                          ▲
    ▼                                          │
系统架构 ────────────────────────────────► 集成测试
    │                                          ▲
    ▼                                          │
详细设计 ────────────────────────────────► 单元测试
    │                                          ▲
    ▼                                          │
┌──────────────────────────────────────────────────┐
│               MIL测试（模型在环）                  │
│    控制器模型 ◄────► 被控对象模型                 │
│         ↑                                      │
│    代码生成                                    │
└──────────────────────────────────────────────────┘
```

MIL测试的主要目标是验证控制算法的功能正确性、动态性能和鲁棒性，而不涉及实现层面的问题（如数值精度、代码效率等）。

### 8.2.2.2 MIL测试的数学基础

MIL测试本质上是对控制系统数学模型的数值仿真。对于连续时间系统，其动态行为由微分方程描述：

$$\frac{dx}{dt} = f(x, u, t) \tag{8.2.1}$$

其中，$x \in \mathbb{R}^n$为状态向量，$u \in \mathbb{R}^m$为控制输入，$f: \mathbb{R}^n \times \mathbb{R}^m \times \mathbb{R} \rightarrow \mathbb{R}^n$为状态转移函数。

对于离散时间控制系统（如数字控制器），动态行为由差分方程描述：

$$x[k+1] = f_d(x[k], u[k], k) \tag{8.2.2}$$

MIL测试通过数值积分算法求解上述方程，常用的数值积分方法包括：

**欧拉法**：
$$x_{k+1} = x_k + h \cdot f(x_k, u_k, t_k) \tag{8.2.3}$$

**四阶龙格-库塔法（RK4）**：
$$x_{k+1} = x_k + \frac{h}{6}(k_1 + 2k_2 + 2k_3 + k_4) \tag{8.2.4}$$

其中：
$$k_1 = f(x_k, u_k, t_k) \tag{8.2.5}$$
$$k_2 = f(x_k + \frac{h}{2}k_1, u_k, t_k + \frac{h}{2}) \tag{8.2.6}$$
$$k_3 = f(x_k + \frac{h}{2}k_2, u_k, t_k + \frac{h}{2}) \tag{8.2.7}$$
$$k_4 = f(x_k + hk_3, u_k, t_k + h) \tag{8.2.8}$$

龙格-库塔法具有$O(h^4)$的截断误差，在相同步长下比欧拉法具有更高的精度。

### 8.2.2.3 控制器模型的表示形式

在MIL测试中，控制器模型可采用多种表示形式：

**传递函数模型**：适用于线性时不变系统，形式为：
$$G(s) = \frac{Y(s)}{U(s)} = \frac{b_ms^m + b_{m-1}s^{m-1} + \cdots + b_0}{s^n + a_{n-1}s^{n-1} + \cdots + a_0} \tag{8.2.9}$$

**状态空间模型**：适用于多输入多输出系统，形式为：
$$\dot{x}(t) = Ax(t) + Bu(t) \tag{8.2.10}$$
$$y(t) = Cx(t) + Du(t) \tag{8.2.11}$$

其中，$A \in \mathbb{R}^{n \times n}$为系统矩阵，$B \in \mathbb{R}^{n \times m}$为输入矩阵，$C \in \mathbb{R}^{p \times n}$为输出矩阵，$D \in \mathbb{R}^{p \times m}$为直接传递矩阵。

**框图模型**：基于图形化建模工具（如Simulink）构建，通过基本运算模块（积分、增益、求和等）的组合表示控制算法。

## 8.2.3 MIL测试环境构建

### 8.2.3.1 建模工具选择

当前主流的控制系统建模工具包括：

| 工具名称 | 开发商 | 主要特点 | 适用领域 |
|---------|-------|---------|---------|
| MATLAB/Simulink | MathWorks | 功能全面、生态丰富、代码生成 | 通用控制、汽车、航空 |
| Modelica/Dymola | Dassault | 面向对象、多物理域、符号处理 | 多物理场系统 |
| LabVIEW | National Instruments | 图形化编程、硬件集成 | 测试测量 |
| SCADE | Esterel Technologies | 形式化验证、安全关键 | 航空、轨道交通 |
| PLECS | Plexim | 电力电子专用、快速仿真 | 电力电子 |

对于水培控制系统这类嵌入式控制应用，MATLAB/Simulink是最常用的选择，其优势在于：

1. 丰富的控制算法库和仿真工具
2. 强大的代码生成能力（Embedded Coder）
3. 完善的SIL/HIL测试支持
4. 广泛的行业应用和文档资源

### 8.2.3.2 被控对象模型开发

被控对象模型的准确性直接影响MIL测试的有效性。对于水培控制系统，被控对象模型通常包括以下子系统：

**营养液循环模型**：描述营养液在管道中的流动特性，基于流体力学方程：
$$\rho \frac{\partial v}{\partial t} + \rho v \cdot \nabla v = -\nabla p + \mu \nabla^2 v + \rho g \tag{8.2.12}$$

对于简化的一维管道流动，可采用集总参数模型：
$$Q = \frac{\Delta P}{R_f} \tag{8.2.13}$$

其中，$Q$为流量，$\Delta P$为压差，$R_f$为流阻。

**温度动态模型**：描述营养液和环境的热交换过程：
$$C_p \frac{dT}{dt} = Q_{in} - Q_{out} - Q_{loss} \tag{8.2.14}$$

其中，$C_p$为热容，$Q_{in}$为加热功率，$Q_{out}$为冷却功率，$Q_{loss}$为热损失。

**pH动态模型**：描述营养液pH值的变化规律：
$$\frac{d[pH]}{dt} = -\frac{1}{V}(Q_{acid} \cdot C_{acid} - Q_{base} \cdot C_{base}) \tag{8.2.15}$$

其中，$V$为营养液体积，$Q_{acid}$和$Q_{base}$分别为酸碱液流量，$C_{acid}$和$C_{base}$为对应浓度。

### 8.2.3.3 仿真参数设置

MIL测试的仿真参数设置对结果准确性有重要影响：

**仿真步长选择**：仿真步长$h$需要满足数值稳定性要求。对于显式积分方法，步长应满足：
$$h < \frac{2}{|\lambda_{max}|} \tag{8.2.16}$$

其中，$\lambda_{max}$为系统矩阵$A$的最大特征值。对于刚性系统，建议采用隐式积分方法或变步长算法。

**求解器类型选择**：根据系统特性选择合适的求解器：
- 固定步长求解器：适用于实时仿真准备和代码生成
- 变步长求解器：适用于非实时精度验证
- 刚性求解器（ode15s）：适用于时间常数差异大的系统

**仿真时间设置**：仿真时间应覆盖系统的完整动态响应过程，包括瞬态和稳态阶段。对于闭环控制系统，建议仿真时间至少为系统调节时间的5~10倍。

## 8.2.4 MIL测试方法

### 8.2.4.1 功能测试

功能测试验证控制器是否按照规格说明正确实现各项功能。测试用例设计应覆盖：

**正常工作模式测试**：验证控制器在正常工况下的基本功能，包括：
- 设定值跟踪测试：验证控制器能否将系统输出调节至设定值
- 稳态精度测试：验证稳态误差是否满足要求
- 响应速度测试：验证上升时间和调节时间是否满足要求

**模式切换测试**：对于具有多种工作模式的控制器，验证模式切换的正确性：
- 自动/手动模式切换
- 正常运行/节能模式切换
- 故障模式切换

**边界条件测试**：验证控制器在边界条件下的行为：
- 输入信号限幅处理
- 输出饱和保护
- 积分抗饱和（Anti-windup）功能

### 8.2.4.2 性能测试

性能测试评估控制器的动态响应特性，主要指标包括：

**时域性能指标**：
- 超调量：$\sigma\% = \frac{y_{max} - y_{\infty}}{y_{\infty}} \times 100\%$
- 上升时间：$t_r$（从10%到90%稳态值的时间）
- 调节时间：$t_s$（进入并保持在±5%误差带内的时间）
- 稳态误差：$e_{ss} = \lim_{t \to \infty}(r(t) - y(t))$

**频域性能指标**：
- 相位裕度：$\gamma = 180° + \angle G(j\omega_c)$
- 增益裕度：$K_g = \frac{1}{|G(j\omega_g)|}$
- 带宽频率：$\omega_b$（幅值下降至-3dB时的频率）

性能测试通常采用阶跃响应、脉冲响应和频率扫描等方法进行。

### 8.2.4.3 鲁棒性测试

鲁棒性测试验证控制器在参数摄动和外部扰动下的性能保持能力：

**参数摄动测试**：在模型参数变化±20%~±50%的范围内，评估控制器性能的变化：
$$\Delta J = \frac{J(\theta + \Delta\theta) - J(\theta)}{J(\theta)} \times 100\% \tag{8.2.17}$$

其中，$J$为性能指标（如ISE、ITAE等），$\theta$为模型参数。

**外部扰动测试**：模拟实际运行中可能遇到的扰动：
- 负载扰动：模拟用水量变化对营养液循环系统的影响
- 环境扰动：模拟环境温度、光照强度的变化
- 测量噪声：在传感器信号上叠加高斯白噪声

**故障注入测试**：模拟传感器或执行器故障：
- 传感器卡死故障
- 传感器漂移故障
- 执行器失效故障

### 8.2.4.4 蒙特卡洛仿真

对于具有随机不确定性的系统，蒙特卡洛仿真是一种有效的统计验证方法。其基本流程为：

1. 定义不确定参数的概率分布：$\theta_i \sim p(\theta_i)$
2. 进行$N$次独立仿真，每次从分布中随机采样参数值
3. 统计分析输出结果：
   - 均值：$\bar{y} = \frac{1}{N}\sum_{i=1}^{N}y_i$
   - 方差：$\sigma_y^2 = \frac{1}{N-1}\sum_{i=1}^{N}(y_i - \bar{y})^2$
   - 置信区间：$\bar{y} \pm z_{\alpha/2}\frac{\sigma_y}{\sqrt{N}}$

蒙特卡洛仿真的样本数量$N$应满足精度要求：
$$N \geq \left(\frac{z_{\alpha/2}\sigma}{\epsilon}\right)^2 \tag{8.2.18}$$

其中，$\epsilon$为允许误差，$z_{\alpha/2}$为标准正态分布的分位数。

## 8.2.5 MIL测试案例分析

### 8.2.5.1 水培系统温度控制MIL测试

以营养液温度控制为例，说明MIL测试的具体实施过程。

**被控对象模型**：营养液温度动态可用一阶惯性加纯滞后模型近似：
$$G_p(s) = \frac{K}{Ts + 1}e^{-\tau s} \tag{8.2.19}$$

其中，$K$为增益系数，$T$为时间常数，$\tau$为纯滞后时间。

**控制器设计**：采用PI控制器：
$$G_c(s) = K_p\left(1 + \frac{1}{T_is}\right) \tag{8.2.20}$$

**测试用例**：
1. 设定值阶跃响应测试（从20°C阶跃至25°C）
2. 负载扰动测试（模拟环境温度下降5°C）
3. 参数摄动测试（时间常数变化±30%）

**测试结果分析**：

| 测试项目 | 性能指标 | 要求值 | 实测值 | 结果 |
|---------|---------|-------|-------|-----|
| 阶跃响应 | 超调量 | ≤10% | 8.2% | 通过 |
| 阶跃响应 | 调节时间 | ≤600s | 480s | 通过 |
| 阶跃响应 | 稳态误差 | ≤0.5°C | 0.2°C | 通过 |
| 负载扰动 | 最大偏差 | ≤2°C | 1.5°C | 通过 |
| 参数摄动 | 性能变化 | ≤20% | 15% | 通过 |

### 8.2.5.2 pH值控制MIL测试

pH值控制是水培系统中的关键控制回路，具有强非线性特性。

**被控对象模型**：pH值的动态与酸碱中和反应相关，呈现高度非线性：
$$\frac{d[pH]}{dt} = f([pH], Q_{acid}, Q_{base}) \tag{8.2.21}$$

**控制器设计**：采用增益调度PID或模糊PID控制器以适应不同pH区间的不同增益特性。

**测试要点**：
- 不同工作点（pH=5.5, 6.0, 6.5）的响应特性
- 酸碱液流量饱和限制的影响
- 测量延迟对控制性能的影响

## 8.2.6 MIL测试的局限性与注意事项

### 8.2.6.1 MIL测试的局限性

MIL测试虽然具有诸多优势，但也存在以下局限性：

1. **模型误差**：被控对象模型与实际物理系统之间存在差异，MIL测试结果只能作为参考
2. **未考虑实现因素**：MIL测试不涉及数值精度、计算延迟等实现层面的问题
3. **理想化假设**：MIL测试环境假设传感器和执行器是理想的，未考虑实际硬件的非理想特性
4. **实时性未验证**：MIL测试通常采用变步长求解器，不验证控制算法的实时执行能力

### 8.2.6.2 提高MIL测试有效性的措施

为提高MIL测试的有效性，建议采取以下措施：

1. **模型验证**：通过实验数据验证被控对象模型的准确性，确保模型能够反映实际系统的关键动态特性
2. **不确定性量化**：在模型中引入参数不确定性和未建模动态，进行鲁棒性分析
3. **逐步细化**：从简化模型开始，逐步增加模型复杂度，评估控制算法对模型精度的敏感性
4. **与SIL/HIL衔接**：MIL测试通过后，应及时进行SIL和HIL测试，验证实现层面的问题

## 8.2.7 本章小结

MIL测试是XIL测试体系的基础环节，在控制算法的设计阶段即开始进行验证。通过在被控对象的仿真模型中测试控制器模型，MIL测试能够在早期发现设计缺陷，降低后期修改成本。

本章系统介绍了MIL测试的基本原理、环境构建、测试方法和实践案例。MIL测试的核心在于建立准确的数学模型和选择合适的仿真参数，测试内容涵盖功能测试、性能测试和鲁棒性测试等多个方面。

尽管MIL测试存在模型误差和理想化假设等局限性，但通过与SIL和HIL测试的有机结合，能够构建完整的嵌入式系统验证体系，为水培控制系统等复杂嵌入式应用的开发提供可靠的质量保障。

## 参考文献

[1] MATHWORKS. Model-based design with MATLAB and Simulink[EB/OL]. (2023-01-01)[2024-12-01]. https://www.mathworks.com/solutions/model-based-design.html.

[2] CELLIER F E, KOFMAN E. Continuous system simulation[M]. New York: Springer Science & Business Media, 2006.

[3] ÅSTRÖM K J, HÄGGLUND T. Advanced PID control[M]. Research Triangle Park: ISA-The Instrumentation, Systems, and Automation Society, 2006.

[4] BRINGMANN E, KRÄMER A. Model-based testing of automotive systems[C]//2008 1st International Conference on Software Testing, Verification, and Validation. Lillehammer: IEEE, 2008: 485-493.

[5] WYNN A. Model-in-the-loop testing[M]//Automotive Model-Based Development. Berlin: Springer, 2017: 87-112.

[6] SCHÄFER W, WEHRHEIM H. Model-driven development with mechatronic UML[M]//Model-Driven Development of Reliable Automotive Services. Berlin: Springer, 2010: 131-148.

[7] BROY M, FEILKAS M, HERRMANNSDOERFER M, et al. Seamless model-based development: from isolated tools to integrated model engineering environments[J]. Proceedings of the IEEE, 2010, 98(4): 526-545.

[8] DUVALL P M, MATYAS S, GLOVER A. Continuous integration: improving software quality and reducing risk[M]. Boston: Addison-Wesley Professional, 2007.

[9] IEEE 1012-2016. IEEE Standard for System, Software, and Hardware Verification and Validation[S]. New York: IEEE, 2016.

[10] ISO 26262-6:2018. Road vehicles - Functional safety - Part 6: Product development at the software level[S]. Geneva: International Organization for Standardization, 2018.

</ama-doc>
