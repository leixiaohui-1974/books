<ama-doc>

# 8.3 SIL测试（软件在环测试）

## 8.3.1 引言

软件在环测试（Software-in-the-Loop Testing，SIL）是XIL测试体系中的第二个关键环节，承接MIL测试并为其后的HIL测试奠定基础。SIL测试的核心目标是在宿主机（Host PC）上验证自动生成的或手写的目标代码的正确性，确保代码实现与原始模型或设计规格的一致性。

与MIL测试相比，SIL测试引入了实现层面的因素，包括数值精度、数据类型、代码结构和执行效率等。通过SIL测试，可以在实际硬件部署之前发现并修复代码层面的缺陷，显著提高开发效率和代码质量。

本章将系统介绍SIL测试的原理、方法、工具链及最佳实践，为水培控制系统等嵌入式应用的软件开发提供指导。

## 8.3.2 SIL测试的基本原理

### 8.3.2.1 SIL测试的定义与目标

SIL测试是指在宿主机（通常是PC）上执行目标代码，并将其与仿真环境（被控对象模型）连接进行闭环测试的过程。在SIL测试中，控制器不再以数学模型的形式存在，而是以可执行代码的形式运行。

SIL测试的主要目标包括：

1. **代码正确性验证**：验证自动生成的代码或手写代码是否正确地实现了控制算法
2. **数值精度评估**：评估定点运算或浮点运算引入的数值误差是否在可接受范围内
3. **代码覆盖率分析**：评估测试用例对代码的覆盖程度，识别未测试的代码路径
4. **性能预估**：评估代码的执行时间和内存占用，为硬件选型提供参考

SIL测试在整个开发流程中的位置如图8.3-1所示：

```
┌─────────────────────────────────────────────────────────────┐
│                     MIL测试阶段                              │
│              控制器模型 + 被控对象模型                        │
│                      ↓ 代码生成                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     SIL测试阶段                              │
│              控制器代码 + 被控对象模型                        │
│                      ↓ 交叉编译                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     PIL/HIL测试阶段                          │
│              控制器代码 + 实时仿真器/实际硬件                  │
└─────────────────────────────────────────────────────────────┘
```

### 8.3.2.2 SIL测试与MIL测试的关系

SIL测试与MIL测试之间存在密切的继承关系。理想情况下，SIL测试应使用与MIL测试相同的测试用例和评估标准，以便进行结果对比。这种对比是SIL测试的核心价值所在。

SIL测试与MIL测试的主要差异包括：

| 比较维度 | MIL测试 | SIL测试 |
|---------|--------|--------|
| 控制器形式 | 数学模型 | 可执行代码 |
| 数值精度 | 双精度浮点 | 单精度/定点 |
| 执行环境 | 仿真器 | 宿主机/模拟器 |
| 代码覆盖率 | 不适用 | 可测量 |
| 执行时间 | 仿真时间 | 实际时间 |

SIL测试通过比较其与MIL测试的输出差异，量化代码实现引入的误差：

$$e_{SIL/MIL}[k] = y_{SIL}[k] - y_{MIL}[k] \tag{8.3.1}$$

其中，$y_{SIL}[k]$为SIL测试输出，$y_{MIL}[k]$为MIL测试输出。通常要求：

$$|e_{SIL/MIL}[k]| \leq \epsilon_{max}, \quad \forall k \tag{8.3.2}$$

$\epsilon_{max}$为允许的最大偏差，通常根据应用场景设定为$10^{-3}$~$10^{-6}$量级。

### 8.3.2.3 代码生成技术

SIL测试的前提是将控制器模型转换为可执行代码。现代建模工具（如MATLAB/Simulink）提供了自动代码生成功能，主要技术包括：

**Embedded Coder**：MathWorks提供的专业代码生成工具，可生成高效、可移植的C/C++代码。其特点包括：
- 支持浮点和定点代码生成
- 可配置代码优化级别
- 支持代码追溯（Traceability）
- 符合MISRA C等编码规范

**代码生成配置选项**：
- 求解器类型：固定步长/变步长
- 数据类型：单精度/双精度浮点，定点
- 代码优化：执行速度 vs 代码体积
- 接口配置：函数原型、数据存储类

**定点代码生成**：对于资源受限的嵌入式系统，定点运算可显著提高执行效率。定点数的表示为：

$$x_{fixed} = x_{real} \times 2^{Q} \tag{8.3.3}$$

其中，$Q$为定标因子（Q值），决定了小数部分的位数。定点运算需要特别注意溢出问题：

$$y = \frac{a \times b}{2^Q} \tag{8.3.4}$$

## 8.3.3 SIL测试环境构建

### 8.3.3.1 测试平台架构

典型的SIL测试平台包括以下组件：

1. **被测代码（SUT）**：控制器实现代码
2. **测试桩（Test Harness）**：提供输入激励和记录输出的测试框架
3. **被控对象模型**：与MIL测试相同的仿真模型
4. **比较器**：比较SIL与MIL的输出结果
5. **覆盖率分析工具**：测量代码覆盖率

```
┌─────────────────────────────────────────────────────────────┐
│                      测试管理平台                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  测试用例库   │  │  结果比较器   │  │  覆盖率分析   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                           │
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
    ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
    │  测试桩      │  │  被测代码    │  │  被控对象模型 │
    │ (Test       │  │  (SUT)      │  │             │
    │  Harness)   │  │             │  │             │
    └─────────────┘  └─────────────┘  └─────────────┘
```

### 8.3.3.2 测试桩设计

测试桩是SIL测试的关键组件，负责：
- 初始化被测代码
- 提供输入信号（来自测试用例或仿真模型）
- 调用被测代码的执行函数
- 收集输出数据
- 与仿真模型同步执行

测试桩的设计需要考虑以下因素：

**接口定义**：明确定义被测代码的输入/输出接口：
```c
/* 控制器初始化 */
void Controller_Init(void);

/* 控制器单步执行 */
void Controller_Step(
    const float32_T *ref,      /* 参考输入 */
    const float32_T *feedback, /* 反馈输入 */
    float32_T *output          /* 控制输出 */
);
```

**数据类型映射**：确保测试桩与被测代码之间的数据类型一致：
| Simulink类型 | C类型 | 描述 |
|-------------|-------|-----|
| double | float64_T | 双精度浮点 |
| single | float32_T | 单精度浮点 |
| int32 | int32_T | 32位有符号整数 |
| uint16 | uint16_T | 16位无符号整数 |
| boolean | boolean_T | 布尔类型 |

**执行同步**：对于闭环测试，需要确保被测代码与仿真模型的同步执行。通常采用以下同步策略：
- 时间驱动：按固定周期调用Controller_Step()
- 事件驱动：基于仿真模型的事件触发执行

### 8.3.3.3 代码覆盖率分析

代码覆盖率是衡量测试完整性的重要指标。常用的覆盖率度量包括：

**语句覆盖率（Statement Coverage）**：
$$C_{stmt} = \frac{\text{已执行语句数}}{\text{总语句数}} \times 100\% \tag{8.3.5}$$

**分支覆盖率（Branch Coverage）**：
$$C_{branch} = \frac{\text{已执行分支数}}{\text{总分支数}} \times 100\% \tag{8.3.6}$$

**条件覆盖率（Condition Coverage）**：
$$C_{cond} = \frac{\text{已评估条件结果数}}{\text{总条件结果数}} \times 100\% \tag{8.3.7}$$

**MC/DC覆盖率（Modified Condition/Decision Coverage）**：
用于安全关键系统（如DO-178C标准），要求每个条件的独立影响都被验证。

对于嵌入式控制系统，通常要求达到以下覆盖率目标：
- 语句覆盖率：≥95%
- 分支覆盖率：≥90%
- MC/DC覆盖率：≥100%（安全关键代码）

## 8.3.4 SIL测试方法

### 8.3.4.1 背靠背测试（Back-to-Back Testing）

背靠背测试是SIL测试的核心方法，通过比较SIL与MIL的输出结果来验证代码实现的正确性。

**测试流程**：
1. 执行MIL测试，记录参考输出$y_{MIL}[k]$
2. 执行SIL测试，记录实际输出$y_{SIL}[k]$
3. 计算偏差：$e[k] = y_{SIL}[k] - y_{MIL}[k]$
4. 评估偏差是否满足容差要求

**偏差评估方法**：

**绝对误差**：
$$e_{abs}[k] = |y_{SIL}[k] - y_{MIL}[k]| \tag{8.3.8}$$

**相对误差**：
$$e_{rel}[k] = \frac{|y_{SIL}[k] - y_{MIL}[k]|}{|y_{MIL}[k]|} \times 100\% \tag{8.3.9}$$

**均方根误差（RMSE）**：
$$RMSE = \sqrt{\frac{1}{N}\sum_{k=1}^{N}(y_{SIL}[k] - y_{MIL}[k])^2} \tag{8.3.10}$$

**容差判定准则**：
$$|e[k]| \leq \epsilon_{abs} + \epsilon_{rel} \cdot |y_{MIL}[k]| \tag{8.3.11}$$

其中，$\epsilon_{abs}$为绝对容差，$\epsilon_{rel}$为相对容差。

### 8.3.4.2 数值精度测试

数值精度测试评估定点或单精度浮点实现引入的量化误差。

**量化误差分析**：

对于定点数，量化误差为：
$$e_q = x_{real} - \frac{x_{fixed}}{2^Q} \tag{8.3.12}$$

量化误差的范围为：
$$-\frac{1}{2^{Q+1}} \leq e_q \leq \frac{1}{2^{Q+1}} \tag{8.3.13}$$

**溢出检测**：

定点运算可能发生溢出，需要检测和防护：
$$y = \text{sat}(a + b, y_{min}, y_{max}) \tag{8.3.14}$$

其中，$\text{sat}(\cdot)$为饱和函数：
$$\text{sat}(x, x_{min}, x_{max}) = \begin{cases} x_{max} & x > x_{max} \\ x_{min} & x < x_{min} \\ x & \text{otherwise} \end{cases} \tag{8.3.15}$$

**数值稳定性测试**：
- 长时间运行的数值漂移
- 积分环节的累积误差
- 除零和非法运算检测

### 8.3.4.3 边界条件测试

边界条件测试验证代码在极端输入和边界状态下的行为。

**输入边界测试**：
- 输入信号的最大/最小值
- 输入信号的突变（阶跃、脉冲）
- 输入信号的噪声叠加

**状态边界测试**：
- 积分器的饱和状态
- 状态变量的限幅
- 模式切换的边界条件

**异常处理测试**：
- 无效输入的处理
- 除零保护
- 数组越界防护

### 8.3.4.4 回归测试

回归测试确保代码修改不会引入新的缺陷。每次代码变更后，应重新执行全部或关键测试用例。

**回归测试策略**：
- 全量回归：执行所有测试用例（适用于重大变更）
- 选择性回归：仅执行受影响的测试用例（适用于局部修改）
- 自动化回归：集成到CI/CD流程中

## 8.3.5 SIL测试工具链

### 8.3.5.1 MATLAB/Simulink SIL测试

MATLAB/Simulink提供了完整的SIL测试支持：

**SIL仿真模式**：
在Simulink中，可通过配置将控制器模型切换为SIL模式：
```
Simulation > Model Configuration Parameters > Code Generation > Verification
> Enable SIL simulation
```

在SIL模式下，控制器模型被替换为自动生成的代码，而被控对象模型仍在Simulink中运行。

**代码生成配置**：
```matlab
% 配置代码生成
set_param(model, 'SystemTargetFile', 'ert.tlc');
set_param(model, 'SolverType', 'Fixed-step');
set_param(model, 'FixedStep', '0.01');
set_param(model, 'ProdEqTarget', 'on');
```

**结果比较**：
Simulink自动比较SIL与MIL的输出结果，生成偏差报告。

### 8.3.5.2 第三方SIL测试工具

**VectorCAST**：专业的嵌入式软件测试工具，支持SIL测试和代码覆盖率分析。

**LDRA Testbed**：符合DO-178C、ISO 26262等安全标准的测试工具。

**Cantata**：专注于C/C++代码的单元测试和集成测试。

**Google Test**：开源C++测试框架，适用于手写代码的SIL测试。

## 8.3.6 SIL测试案例分析

### 8.3.6.1 PID控制器SIL测试

以营养液温度PID控制器为例，说明SIL测试的实施过程。

**控制器参数**：
- 比例增益：$K_p = 2.5$
- 积分时间：$T_i = 120$ s
- 微分时间：$T_d = 10$ s
- 采样周期：$T_s = 1$ s

**代码生成配置**：
- 目标：32位ARM Cortex-M
- 数据类型：单精度浮点
- 求解器：离散（固定步长）

**背靠背测试结果**：

| 测试项目 | MIL输出 | SIL输出 | 绝对误差 | 相对误差 | 结果 |
|---------|--------|--------|---------|---------|-----|
| 稳态值 | 25.00 | 25.00 | 0.00 | 0.00% | 通过 |
| 峰值 | 26.85 | 26.84 | 0.01 | 0.04% | 通过 |
| 调节时间 | 485s | 485s | 0s | 0.00% | 通过 |
| 超调量 | 7.4% | 7.36% | 0.04% | 0.54% | 通过 |

**代码覆盖率结果**：
- 语句覆盖率：100%
- 分支覆盖率：98.5%
- 未覆盖分支：异常处理路径（需补充测试用例）

### 8.3.6.2 状态机控制器SIL测试

对于具有多模式切换的控制器，SIL测试需要验证状态转换的正确性。

**测试要点**：
- 各状态的入口/出口动作
- 状态转换条件的正确性
- 历史状态的恢复
- 并发状态的处理

## 8.3.7 SIL测试的最佳实践

### 8.3.7.1 测试用例设计原则

1. **继承MIL测试用例**：SIL测试应首先复用MIL测试的全部用例，确保测试的一致性
2. **补充边界测试**：针对代码实现补充边界条件和异常处理测试
3. **覆盖所有代码路径**：设计测试用例以达到目标覆盖率
4. **自动化测试**：建立自动化测试框架，支持回归测试

### 8.3.7.2 常见问题与对策

**问题1：SIL与MIL结果偏差过大**
- 原因：数据类型不匹配、算法实现差异
- 对策：检查数据类型配置，验证算法等价性

**问题2：代码覆盖率不达标**
- 原因：测试用例设计不足、存在死代码
- 对策：补充测试用例，清理或注释死代码

**问题3：执行时间过长**
- 原因：代码效率低、测试用例过多
- 对策：优化代码，采用选择性回归测试

## 8.3.8 本章小结

SIL测试是连接模型设计与代码实现的关键环节，通过在宿主机上验证目标代码的正确性，确保代码实现与原始设计的一致性。

本章系统介绍了SIL测试的原理、环境构建、测试方法和工具链。SIL测试的核心在于背靠背测试方法，通过比较SIL与MIL的输出结果来量化代码实现引入的误差。代码覆盖率分析是SIL测试的重要组成部分，有助于评估测试的完整性。

对于水培控制系统等嵌入式应用，SIL测试能够有效地发现代码层面的缺陷，为后续的HIL测试和系统部署奠定坚实基础。

## 参考文献

[1] MATHWORKS. Software-in-the-loop (SIL) simulation[EB/OL]. (2023-01-01)[2024-12-01]. https://www.mathworks.com/help/ecoder/software-in-the-loop-sil-simulation.html.

[2] CONRAD M, FEY I, SÖDING S. Development and introduction of a test process for MATLAB/Simulink models[C]//2006 IEEE International Conference on Industrial Technology. Mumbai: IEEE, 2006: 2579-2584.

[3] WACHENFELD W, WINNER H. The release of autonomous vehicles[M]//Autonomous Driving. Berlin: Springer, 2016: 425-449.

[4] ISO 26262-6:2018. Road vehicles - Functional safety - Part 6: Product development at the software level[S]. Geneva: International Organization for Standardization, 2018.

[5] MATHWORKS. Code generation verification and validation[EB/OL]. (2023-01-01)[2024-12-01]. https://www.mathworks.com/help/ecoder/code-verification-and-validation.html.

[6] VECTOR. Software-in-the-loop tests - one platform for all scenarios[EB/OL]. (2024-01-01)[2024-12-01]. https://cdn.vector.com/cms/content/know-how/_technical-articles/CANoe4SW_SIL_Tests_SQ_Magazin_202409_PressArticle_EN.pdf.

[7] SYNOPSYS. What is software-in-the-loop (SiL) testing?[EB/OL]. (2021-12-01)[2024-12-01]. https://www.synopsys.com/blogs/chip-design/what-is-software-in-the-loop-testing.html.

[8] OPAL-RT. What is software-in-the-loop (SIL)?[EB/OL]. (2025-01-01)[2024-12-01]. https://www.opal-rt.com/blog/what-is-software-in-the-loop/.

[9] BROY M, FEILKAS M, HERRMANNSDOERFER M, et al. Seamless model-based development: from isolated tools to integrated model engineering environments[J]. Proceedings of the IEEE, 2010, 98(4): 526-545.

[10] IEEE 1012-2016. IEEE Standard for System, Software, and Hardware Verification and Validation[S]. New York: IEEE, 2016.

</ama-doc>
