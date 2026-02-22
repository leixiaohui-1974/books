<ama-doc>

# 24. 运行设计域与自主等级

## 24.1 引言

运行设计域（Operational Design Domain, ODD）是自主系统领域的核心概念，定义了系统被设计为可以安全运行的特定条件和环境范围。对于水系统自主控制而言，ODD的明确界定是确保系统安全、确定人机责任边界的基础。本章将系统阐述ODD的概念框架、构建方法及其与WNAL的关联，为水系统自主控制的安全部署提供理论指导。

## 24.2 ODD概念框架

### 24.2.1 ODD的定义与起源

运行设计域（ODD）最初源于自动驾驶汽车领域，用于定义自动驾驶系统能够安全运行的操作条件[1]。SAE J3016标准将ODD定义为"给定驾驶自动化系统或其功能被设计为运行的特定运行条件，包括但不限于环境、地理和时间限制，以及交通流量、道路特征等必要特性"。

将ODD概念引入水系统控制领域，可以定义为：

**水系统运行设计域（ODD）**：水系统自主控制系统被设计为可以安全、有效运行的特定条件和环境范围，包括水力条件、水质参数、设备状态、外部需求等约束。

### 24.2.2 ODD的核心要素

水系统ODD包含以下核心要素：

**水力条件**：
- 流量范围：管道流量、泵站流量的可接受区间
- 压力范围：管网压力的安全上下限
- 水位范围：水库、水池水位的运行区间

**水质参数**：
- 原水水质：浊度、有机物含量、氨氮等指标范围
- 过程水质：各工艺单元的关键水质参数
- 出厂水质：满足饮用水标准的参数范围

**设备状态**：
- 可用设备：当前可投入运行的设备集合
- 设备健康度：关键设备的运行状态评估
- 维护状态：计划内和计划外维护的影响

**外部条件**：
- 用水需求：日用水量、时用水量变化范围
- 气象条件：降雨、气温等对水源和用水的影响
- 能源供应：电力供应的稳定性和价格

**系统配置**：
- 网络拓扑：管网连接方式和阀门状态
- 控制模式：当前生效的控制策略和参数
- 通信状态：监控通信链路的可用性

### 24.2.3 ODD的层级结构

ODD可以按层级进行组织：

**系统级ODD**：定义整个水系统的运行边界，由最高等级自主系统管理。

**子系统级ODD**：定义各子系统（水厂、管网区域）的运行边界。

**功能级ODD**：定义特定功能（如压力控制、水质调节）的运行边界。

**场景级ODD**：定义特定场景（如高峰供水、应急调度）的运行条件。

层级之间可以存在包含关系，也可以存在交集关系，形成复杂的ODD空间。

## 24.3 ODD构建方法

### 24.3.1 基于风险的ODD定义

ODD的边界应基于风险评估确定，确保在ODD内系统能够以可接受的风险水平运行[2]。

**风险识别**：识别系统运行中可能面临的危险源，包括：
- 水力风险：压力过高/过低、水锤、气蚀等
- 水质风险：超标出水、交叉污染等
- 设备风险：设备故障、连锁停机等
- 供应风险：供水中断、水质恶化等

**风险评估**：评估各危险源的发生概率和后果严重程度，确定风险等级。

**ODD边界确定**：将风险控制在可接受范围内的运行条件集合即为ODD。

### 24.3.2 基于能力的ODD定义

ODD也可以基于系统能力进行定义，明确系统能够可靠处理的运行条件范围。

**感知能力边界**：
- 传感器测量范围和精度限制
- 状态估计算法的有效范围
- 异常检测算法的灵敏度边界

**决策能力边界**：
- 控制算法的稳定运行区域
- 优化算法的收敛条件
- 应急策略的覆盖范围

**执行能力边界**：
- 执行器的调节范围和响应速度
- 设备的安全运行区间
- 控制动作的约束条件

### 24.3.3 ODD的形式化描述

ODD可以用约束集合的形式化方式描述：

$$ODD = \{x \in \mathcal{X} : g_i(x) \leq 0, i = 1, ..., m; h_j(x) = 0, j = 1, ..., p\}$$

其中 $x$ 是系统状态变量，$g_i$ 是不等式约束，$h_j$ 是等式约束。

对于时变系统，ODD可以是时变的：

$$ODD(t) = \{x(t) \in \mathcal{X}(t) : g_i(x(t), t) \leq 0, h_j(x(t), t) = 0\}$$

## 24.4 ODD监控与边界管理

### 24.4.1 ODD监控机制

实时监控系统是否处于ODD内是确保安全的关键。

**状态监测**：
- 实时采集关键状态变量
- 估计不可直接测量的状态
- 评估状态变量的不确定性

**边界检测**：
- 计算当前状态到ODD边界的距离
- 预测未来状态是否将超出ODD
- 评估边界穿越的风险

**预警机制**：
- 当接近ODD边界时发出预警
- 提供预警的原因和建议措施
- 根据风险等级分级预警

### 24.4.2 ODD退出处理

当系统即将或已经退出ODD时，需要启动相应的处理程序。

**预防性措施**：
- 调整控制策略避免边界穿越
- 启动备用设备扩大运行能力
- 请求人工干预

**退出响应**：
- 立即降低自主等级
- 启动安全模式或降级模式
- 通知操作员并请求接管

**恢复程序**：
- 当条件恢复后重新评估ODD状态
- 逐步恢复自主运行
- 记录和分析退出事件

### 24.4.3 ODD动态调整

在某些情况下，ODD可以根据实际需要进行动态调整。

**ODD扩展**：
- 通过设备增投或策略调整扩大运行能力
- 基于实时风险评估临时放宽某些约束
- 在人工监督下进入扩展ODD

**ODD收缩**：
- 设备故障时缩小可用运行范围
- 高风险时期收紧安全边界
- 维护期间限制运行模式

## 24.5 ODD与WNAL的关联

### 24.5.1 不同等级的ODD特征

不同WNAL等级对应不同的ODD特征：

| WNAL等级 | ODD特征 | 边界管理 |
|----------|---------|----------|
| WNAL-0 | 无ODD概念 | 人工判断 |
| WNAL-1 | 信息ODD | 系统提示 |
| WNAL-2 | 固定ODD | 自动限制 |
| WNAL-3 | 动态ODD | 自动监控+预警 |
| WNAL-4 | 自适应ODD | 智能调整+人工确认 |
| WNAL-5 | 全场景ODD | 自主管理 |

### 24.5.2 ODD复杂度与自主等级

随着自主等级的提升，ODD的复杂度通常也相应增加：

**WNAL-2**：ODD由固定的参数范围定义，如压力上下限、流量范围等。

**WNAL-3**：ODD可能包含多个子域，系统根据当前状态选择适用的子域。

**WNAL-4**：ODD可以动态调整，系统根据风险评估和性能反馈优化ODD边界。

**WNAL-5**：ODD接近全覆盖，系统能够处理几乎所有可预见的运行条件。

### 24.5.3 ODD验证与等级认证

ODD的定义和验证是WNAL等级认证的重要组成部分。

**ODD文档化**：
- 明确记录各等级的ODD定义
- 说明ODD边界的确定依据
- 描述ODD监控和退出处理机制

**ODD验证测试**：
- 在ODD边界附近进行测试
- 验证ODD退出检测的可靠性
- 测试降级和接管机制

**ODD更新管理**：
- 建立ODD变更的控制流程
- 评估ODD变更对安全的影响
- 更新相关文档和培训材料

## 24.6 水系统ODD应用案例

### 24.6.1 供水管网压力控制ODD

**ODD定义**：
- 流量范围：各泵站流量在额定流量的30%-100%
- 压力范围：管网压力在0.2-0.6 MPa
- 设备可用：至少2台主泵可用
- 通信正常：与调度中心通信延迟<5秒

**边界监控**：
- 实时计算各节点压力裕度
- 预测未来1小时的压力趋势
- 当裕度低于10%时发出预警

**退出处理**：
- 压力低于0.15 MPa：启动应急增压泵
- 压力高于0.65 MPa：自动开启泄压阀
- 通信中断：切换至本地自动控制

### 24.6.2 水厂工艺控制ODD

**ODD定义**：
- 原水浊度：<50 NTU
- 水温：5-30°C
- 氨氮：<2 mg/L
- 设备状态：关键设备无故障

**边界监控**：
- 连续监测原水水质参数
- 评估工艺单元的处理能力裕度
- 预测出水水质达标概率

**退出处理**：
- 原水浊度超标：增加混凝剂投加，必要时降低处理量
- 设备故障：切换备用设备，调整工艺参数
- 水质风险：加强检测频率，准备应急投加

### 24.6.3 多水源调度ODD

**ODD定义**：
- 总需求：不超过各水源可用产能之和的90%
- 水质兼容：混合后水质满足标准
- 能源价格：在预测范围内
- 应急储备：至少维持4小时应急供水

**边界监控**：
- 实时跟踪需求与产能平衡
- 监控各水源水质变化
- 评估应急储备消耗速度

**退出处理**：
- 需求超预期：启动需求响应，请求用户节水
- 水质冲突：调整混合比例，必要时隔离部分水源
- 储备不足：启动应急供水预案

## 24.7 ODD标准与规范

### 24.7.1 ODD文档标准

建立标准化的ODD文档模板，包括：

**基本信息**：
- ODD名称和版本
- 适用的系统/功能/等级
- 编制和审核信息

**ODD定义**：
- 运行条件约束（参数范围）
- 环境条件约束
- 设备状态要求
- 外部依赖条件

**边界管理**：
- 监控参数和方法
- 预警条件和级别
- 退出处理程序
- 恢复条件

**验证信息**：
- ODD确定依据
- 验证测试结果
- 已知限制和假设

### 24.7.2 ODD工程实践指南

制定ODD工程实践指南，包括：

**ODD开发流程**：
- 需求分析和场景识别
- 风险评估和边界确定
- ODD文档编制
- 验证测试和评审

**ODD管理流程**：
- 变更控制和影响评估
- 定期评审和更新
- 培训和信息发布

**ODD工具支持**：
- ODD建模和可视化工具
- ODD监控和预警系统
- ODD文档管理系统

## 24.8 本章小结

本章系统阐述了运行设计域（ODD）的概念框架及其在水系统自主控制中的应用。ODD定义了自主系统被设计为可以安全运行的条件范围，是确保系统安全、明确人机责任边界的基础。

ODD的构建可以基于风险评估或系统能力，包含水力条件、水质参数、设备状态、外部条件等多维要素。ODD监控机制实时跟踪系统状态，在接近或超出边界时启动预警和退出处理程序。

ODD与WNAL密切相关，不同自主等级对应不同的ODD特征和管理复杂度。随着自主等级的提升，ODD从固定范围发展到动态自适应，系统对运行条件的处理能力不断增强。

通过标准化的ODD文档和管理流程，可以确保水系统自主控制的安全部署和可靠运行。ODD框架为水系统智能化升级提供了重要的安全保障机制。

## 参考文献

[1] SAE INTERNATIONAL. Taxonomy and definitions for terms related to driving automation systems for on-road motor vehicles: SAE J3016_202104[S]. SAE International, 2021.

[2] BSI. PAS 1883:2020 Operational design domain (ODD) taxonomy for an automated driving system (ADS)[S]. British Standards Institution, 2020.

[3] GYLLENHAMMAR M, WARG F, CHEN D, et al. Towards an operational design domain that supports the safety argumentation of automated driving systems[C]//2020 IEEE Intelligent Vehicles Symposium (IV). IEEE, 2020: 1187-1194.

[4] ULBRICH S, MENZEL T, RESCHKA A, et al. Defining and substantiating the terms scene, situation, and scenario for automated driving[C]//2015 IEEE 18th International Conference on Intelligent Transportation Systems. IEEE, 2015: 982-988.

[5] CZARNECKI K. Operational world model ontology for automated driving systems[R]. Waterloo Intelligent Systems Engineering (WISE) Lab Report, 2018.

[6] KOOPMAN P, WAGNER M. Autonomous vehicle safety: An interdisciplinary challenge[J]. IEEE Intelligent Transportation Systems Magazine, 2017, 9(1): 90-96.

[7] RIEDMAIER S, PONN T, LUDWIG D, et al. Survey on scenario-based safety assessment of automated vehicles[J]. IEEE Access, 2020, 8: 87456-87477.

[8] BATSCH F, BAGHERI A, RIEDMAIER S, et al. Ontology-based ODD description for the safety assessment of automated vehicles[C]//2021 IEEE International Conference on Omni-layer Intelligent Systems (COINS). IEEE, 2021: 1-6.

[9] SALAY R, QUEIROZ R, CZARNECKI K. An analysis of ISO 26262: Using machine learning safely in automotive software[J]. arXiv preprint arXiv:1709.02435, 2017.

[10] BURTON S, GÄNSBERGER M, SÖTTINGER J. Making the case for safety of machine learning in highly automated driving[C]//International Conference on Computer Safety, Reliability, and Security. Springer, 2017: 5-16.

[11] AMANN J, BENZ M, HÄRTSCHEN M, et al. Operational design domain for automated driving systems: Taxonomy of terms and definitions[C]//2020 IEEE International Conference on Omni-layer Intelligent Systems (COINS). IEEE, 2020: 1-6.

[12] WOOD M, BROWN D, BHARATHI M C R, et al. Operational design domain (ODD) framework for autonomous driving systems[C]//2021 IEEE International Conference on Omni-layer Intelligent Systems (COINS). IEEE, 2021: 1-6.

</ama-doc>
