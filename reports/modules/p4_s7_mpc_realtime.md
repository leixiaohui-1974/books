<ama-doc>
# 第四部分 模型预测控制

## 第7节 MPC实时计算优化

### 4.7.1 引言

模型预测控制的实时计算性能是其工程应用的关键瓶颈。MPC需要在每个采样周期内求解一个优化问题，对于快速动态系统或大规模问题，计算延迟可能限制MPC的应用范围。实时计算优化技术通过算法优化、硬件加速、问题结构利用等手段，显著降低MPC求解时间，使其能够满足微秒级到毫秒级的实时性要求[1]。

MPC计算优化的研究始于20世纪90年代，随着嵌入式系统和实时操作系统的发展，MPC的实时实现技术不断进步。近年来，GPU并行计算、FPGA硬件加速、专用求解器架构等技术的兴起，为MPC的实时性能提升开辟了新途径。在水系统控制中，大型供水管网的MPC优化可能涉及数千个变量和约束，实时计算优化技术对于工程实施至关重要。

实时计算优化的核心挑战在于：在保证求解精度和稳定性的前提下，最小化计算时间。这需要从算法选择、代码优化、硬件加速等多个层面进行系统优化。同时，还需考虑数值稳定性、内存占用、功耗等工程约束。

### 4.7.2 优化算法效率提升

#### 4.7.2.1 快速QP求解器

线性MPC的核心是二次规划求解，专用快速QP求解器显著提升了计算效率[2]。

**qpOASES：**

基于在线活跃集策略，利用相邻QP问题的解作为热启动：

```
输入: H, f, A, lb, ub, x_prev
1. 初始化活跃集 W = W_prev
2. 求解等式约束QP
3. 检查KKT条件
4. 更新活跃集
5. 重复2-4直到收敛
```

热启动使迭代次数从$O(n)$减少到$O(1)$（对于小扰动）。

**OSQP：**

基于ADMM的QP求解器，利用问题结构稀疏性：

$$\min_{x, z} \frac{1}{2}x^T P x + q^T x \tag{4.7.1}$$

$$\text{s.t.} \quad Ax + z = l, \quad z \in \mathcal{K} \tag{4.7.2}$$

ADMM迭代：

$$x^{k+1} = (P + \sigma I + A^T \rho A)^{-1}(\sigma x^k - q + A^T(\rho z^k - \lambda^k)) \tag{4.7.3}$$
$$z^{k+1} = \Pi_{\mathcal{K}}(Ax^{k+1} + \lambda^k/\rho) \tag{4.7.4}$$
$$\lambda^{k+1} = \lambda^k + \rho(Ax^{k+1} - z^{k+1}) \tag{4.7.5}$$

**PIQP：**

针对MPC结构优化的内点法实现，支持稠密和稀疏模式。

#### 4.7.2.2 实时迭代策略

对于非线性MPC，实时迭代（RTI）策略通过限制单步迭代次数保证实时性[3]。

标准SQP vs. RTI：

| 方法 | 单步计算 | 收敛性 | 适用场景 |
|------|----------|--------|----------|
| 标准SQP | 多次迭代 | 精确收敛 | 离线优化 |
| RTI | 1次迭代 | 渐进收敛 | 实时控制 |

RTI的稳定性条件：

$$\|x(k+1) - x^*(k+1)\| \leq \rho \|x(k) - x^*(k)\| + \epsilon \tag{4.7.6}$$

其中，$\rho < 1$，$\epsilon$为小量。

#### 4.7.2.3 灵敏度更新策略

Jacobian和Hessian的更新策略影响计算效率：

**精确更新：** 每次采样重新计算所有导数

**BFGS近似：** 利用梯度差分近似Hessian

$$H_{k+1} = H_k + \frac{y_k y_k^T}{y_k^T s_k} - \frac{H_k s_k s_k^T H_k}{s_k^T H_k s_k} \tag{4.7.7}$$

其中，$y_k = \nabla L_{k+1} - \nabla L_k$，$s_k = x_{k+1} - x_k$。

**固定更新：** 每隔$N$步重新计算Jacobian

**组合策略：** 根据收敛情况动态选择更新方式

### 4.7.3 问题结构利用

#### 4.7.3.1 MPC问题的稀疏结构

MPC优化问题具有特殊的稀疏结构，利用稀疏线性代数可大幅提升效率[4]。

约束Jacobian的块对角结构：

$$J = \begin{bmatrix}
I & & & & & & \\
-A & I & -B & & & & \\
& & & \ddots & & & \\
& & & & -A & I & -B
\end{bmatrix} \tag{4.7.8}$$

稀疏矩阵技术：
- 稀疏Cholesky分解
- 稀疏LU分解
- 共轭梯度法（CG）
- 预处理技术

#### 4.7.3.2 condensing技术

Condensing通过消去状态变量，将稀疏问题转化为小规模稠密问题[5]。

原始变量：$(x_0, u_0, x_1, u_1, \ldots, x_N)$，维数$Nn + Nm$

Condensed变量：$(u_0, u_1, \ldots, u_{N-1})$，维数$Nm$

状态表示为控制序列的函数：

$$x_i = A^i x_0 + \sum_{j=0}^{i-1} A^{i-1-j} B u_j \tag{4.7.9}$$

Condensing适合预测时域较长、控制变量较少的情况。

#### 4.7.3.3 部分condensing

部分condensing是完整condensing和稀疏方法的折中：

- 将预测时域划分为若干块
- 块内condensing，块间保持稀疏

平衡了问题规模和矩阵稀疏性。

### 4.7.4 代码优化技术

#### 4.7.4.1 代码生成

代码生成工具将高级MPC描述转化为高效C代码[6]。

**CasADi代码生成：**

```python
# 定义MPC问题
nlp = {'x': u, 'f': J, 'g': g}

# 生成求解器
solver = nlpsol('solver', 'ipopt', nlp)

# 生成C代码
solver.generate_dependencies('mpc.c')
```

**ACADO Toolkit：**

专为实时MPC设计的代码生成工具，生成自包含的C代码。

#### 4.7.4.2 定点运算

对于资源受限的嵌入式系统，定点运算替代浮点运算：

$$x_{fixed} = \lfloor x \cdot 2^Q \rceil \tag{4.7.10}$$

其中，$Q$为定点精度。

优点：
- 计算速度快
- 硬件成本低
- 功耗小

缺点：
- 数值精度受限
- 需要仔细的数值分析

#### 4.7.4.3 查表法

对于频繁计算的函数，采用查表法：

```c
// 预计算查找表
float sqrt_table[256];
for (int i = 0; i < 256; i++) {
    sqrt_table[i] = sqrt(i / 256.0);
}

// 运行时查表
float fast_sqrt(float x) {
    int idx = (int)(x * 256);
    return sqrt_table[idx];
}
```

### 4.7.5 硬件加速

#### 4.7.5.1 GPU并行计算

GPU的并行架构适合MPC中的矩阵运算和批量仿真[7]。

**MPCGPU：**

基于GPU的NMPC求解器，利用并行共轭梯度（PCG）求解线性系统。

并行策略：
- 矩阵-向量乘法并行化
- 多场景并行仿真
- 多起点优化并行

性能提升：相比CPU实现，求解速度提升10-100倍。

#### 4.7.5.2 FPGA加速

FPGA（现场可编程门阵列）提供定制化的硬件加速[8]。

FPGA实现优势：
- 确定性的低延迟
- 高并行度
- 低功耗

典型实现：
- 定制QP求解器IP核
- 流水线化的矩阵运算单元
- 专用内存架构

#### 4.7.5.3 嵌入式处理器优化

针对ARM Cortex-M/R系列等嵌入式处理器：

**NEON指令集：** SIMD并行处理

**CMSIS-DSP库：** 优化的DSP函数

**内存优化：** 缓存友好的数据布局

### 4.7.6 显式MPC与近似方法

#### 4.7.6.1 显式MPC的在线效率

显式MPC将优化问题离线求解，在线仅需查表[9]：

在线计算：
1. 确定当前状态所属区域：$H_i x \leq h_i$
2. 计算控制量：$u = F_i x + g_i$

计算复杂度：$O(N_r \cdot n)$，其中$N_r$为区域数。

#### 4.7.6.2 区域缩减技术

减少显式MPC存储和查询开销：

**区域合并：** 合并相邻且控制律相近的区域

**近似显式MPC：** 用神经网络或多项式拟合近似

$$u \approx f_{NN}(x; \theta) \tag{4.7.11}$$

**自适应分区：** 根据运行轨迹动态调整分区密度

#### 4.7.6.3 次优MPC

在计算资源受限时，接受次优解：

**提前终止：** 设置最大迭代次数

**简化模型：** 使用降阶模型近似

**收缩时域：** 动态调整预测时域长度

### 4.7.7 实时操作系统集成

#### 4.7.7.1 确定性执行

实时MPC需要确定性的执行时间：

**最坏情况执行时间（WCET）分析：**

$$T_{WCET} = T_{setup} + N_{iter,max} \cdot T_{iter} \tag{4.7.12}$$

**时间触发架构：**

```
采样周期 T_s
├── 传感器读取 (t1)
├── 状态估计 (t2)
├── MPC求解 (t3)
├── 控制输出 (t4)
└── 空闲等待
```

#### 4.7.7.2 多任务调度

在复杂系统中，MPC与其他任务共享计算资源：

**优先级调度：** MPC任务具有高优先级

**时间片轮转：** 保证各任务的执行时间

**自适应调度：** 根据系统状态动态调整MPC求解精度

### 4.7.8 水系统MPC实时实现案例

#### 4.7.8.1 小型供水系统

系统规模：10个节点，3个泵站

实现方案：
- 平台：ARM Cortex-M4 @ 100MHz
- 求解器：自定义主动集QP
- 采样周期：1秒
- 求解时间：< 50ms

#### 4.7.8.2 中型供水管网

系统规模：100个节点，20个泵站

实现方案：
- 平台：Intel i7 + NVIDIA GTX 1060
- 求解器：MPCGPU + OSQP
- 采样周期：15分钟
- 求解时间：< 2分钟

#### 4.7.8.3 大型跨流域系统

系统规模：1000+节点，多区域协调

实现方案：
- 平台：服务器集群
- 架构：分布式DMPC
- 采样周期：1小时
- 求解时间：< 10分钟

### 4.7.9 小结

MPC实时计算优化是连接理论研究与工程应用的桥梁。通过快速QP求解器、实时迭代策略、问题结构利用、代码优化和硬件加速等技术，MPC的计算效率已提升数个数量级，能够满足从微秒级到分钟级不同时间尺度的控制需求。

在水系统控制中，实时计算优化使MPC能够应用于大型供水管网、复杂污水处理过程等大规模系统。GPU并行计算和FPGA硬件加速为计算密集型应用提供了强大支撑，而显式MPC和近似方法则在资源受限场景下提供了实用解决方案。

随着边缘计算和物联网技术的发展，MPC的实时实现将更加分散化和智能化。未来发展方向包括：自适应精度调节、云-边协同计算、基于学习的快速近似求解，以及面向特定应用的专用MPC芯片。

## 参考文献

[1] FERREAU H J, KIRCHES C, POT SCHKA A, et al. qpOASES: A parametric active-set algorithm for quadratic programming[J]. Mathematical Programming Computation, 2014, 6(4): 327-363.

[2] STELLATO B, BANJAC G, GOULART P, et al. OSQP: An operator splitting solver for quadratic programs[J]. Mathematical Programming Computation, 2020, 12(4): 637-672.

[3] DIEHL M, BOCK H G, SCHLÖDER J P, et al. Real-time optimization and nonlinear model predictive control of processes governed by differential-algebraic equations[J]. Journal of Process Control, 2002, 12(4): 577-585.

[4] FRISON G, JØRGENSEN J B. A fast condensing method for solving linear-quadratic control problems[C]//Proceedings of the 52nd IEEE Conference on Decision and Control. Florence: IEEE, 2013: 7715-7720.

[5] KOUZOUPIS D, QUIRYNEN R, HOUSKA B, et al. A block based ALADIN scheme for highly parallelizable direct optimal control[C]//Proceedings of the 2015 ACM Symposium on Architecture for Networking and Communications Systems. Oakland: ACM, 2015: 1-6.

[6] ANDERSSON J A, GILLIS J, HORN G, et al. CasADi: A software framework for nonlinear optimization and optimal control[J]. Mathematical Programming Computation, 2019, 11(1): 1-36.

[7] ENGELMANN A, JIANG Y, BENNER H, et al. MPCGPU: Real-time nonlinear model predictive control through preconditioned iterative solvers[C]//Proceedings of the 2022 IEEE 61st Conference on Decision and Control (CDC). Cancun: IEEE, 2022: 2219-2226.

[8] JEREZ J L, GOULART P J, RICHTER S, et al. Embedded online optimization for model predictive control at megahertz rates[J]. IEEE Transactions on Automatic Control, 2014, 59(12): 3238-3251.

[9] BEMPORAD A, MORARI M, DUA V, et al. The explicit linear quadratic regulator for constrained systems[J]. Automatica, 2002, 38(1): 3-20.

[10] KOGEL M, FINDEISEN R. Fast predictive control for linear systems with disturbances and constraints[J]. IFAC-PapersOnLine, 2021, 54(6): 91-98.

[11] WANG Y, BOYD S. Fast model predictive control using online optimization[J]. IEEE Transactions on Control Systems Technology, 2010, 18(2): 267-278.

[12] PATRINOS P, BEMPORAD A. An accelerated dual gradient-projection algorithm for embedded linear model predictive control[J]. IEEE Transactions on Automatic Control, 2014, 59(1): 18-33.

</ama-doc>
