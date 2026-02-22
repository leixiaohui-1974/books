<ama-doc>

# 5.3 运行设计域ODD

## 5.3.1 引言

运行设计域（Operational Design Domain, ODD）是自动驾驶和自主系统安全领域的关键概念，它定义了系统被设计为能够安全运行的特定条件和环境范围[1]。ODD概念源于对复杂自主系统安全边界的认识：没有任何自主系统能够在所有可能的条件下安全运行，因此必须明确界定其能力边界，并确保系统仅在能力范围内运行。

在水系统控制领域，ODD概念同样具有重要的理论和实践价值。水系统面临的环境条件（如来水、降雨、需水）、系统状态（设备健康状况、水质状况）和外部约束（法规要求、社会需求）具有高度的时空变异性。通过明确定义水系统控制系统的ODD，可以建立系统能力与运行条件之间的明确映射关系，为安全决策提供依据。

## 5.3.2 ODD的理论基础

### 5.3.2.1 ODD的定义与构成

根据SAE J3016标准，ODD被定义为"给定驾驶自动化系统或其功能被设计为运行的特定运行条件，包括但不限于环境、地理和时间限制，以及交通或道路特征的必要存在或缺失"[2]。这一定义可以推广到一般自主系统：

**定义5.4（运行设计域）**：运行设计域 $\mathcal{O}$ 是系统能够安全运行的所有条件和参数的集合：

$$\mathcal{O} = \{(e, g, t, tr, r, s) : \text{Safety}(e, g, t, tr, r, s) = \text{True}\}$$

其中各维度含义为：
- $e$：环境条件（天气、光照、能见度等）
- $g$：地理条件（地形、地貌、基础设施等）
- $t$：时间条件（时段、季节、特殊日期等）
- $tr$：交通/运行条件（负荷水平、干扰程度等）
- $r$：法规条件（操作限制、合规要求等）
- $s$：系统状态（设备健康、资源可用性等）

### 5.3.2.2 ODD的层次结构

ODD可以组织为层次化结构，从宏观到微观逐步细化[3]：

**战略层ODD**：定义系统部署的宏观场景，如"城市供水系统"、"流域防洪调度"等。

**战术层ODD**：定义特定场景下的运行模式，如"正常供水模式"、"干旱应急模式"、"洪水调度模式"等。

**操作层ODD**：定义具体控制动作的执行条件，如"泵组启动条件"、"阀门调节允许范围"等。

### 5.3.2.3 ODD与系统能力的关系

ODD与系统能力之间存在双向约束关系：

$$\mathcal{O} = \{\mathbf{c} : \text{Capability}(\mathbf{c}) \geq \text{Requirement}(\mathbf{c})\}$$

其中 $\mathbf{c}$ 是条件向量，$\text{Capability}$ 是系统能力函数，$\text{Requirement}$ 是条件需求函数。

这一关系表明，ODD边界由系统能力与任务需求之间的匹配程度决定。当环境需求超过系统能力时，系统应退出自主运行模式或请求人工干预。

## 5.3.3 ODD的形式化描述

### 5.3.3.1 基于本体的ODD建模

本体（Ontology）为ODD提供了结构化的知识表示框架[4]。ODD本体定义了概念、属性和关系的层次结构：

```
ODD
├── EnvironmentalConditions
│   ├── Weather
│   │   ├── Precipitation
│   │   ├── Temperature
│   │   └── Wind
│   ├── HydrologicalConditions
│   │   ├── Inflow
│   │   ├── WaterLevel
│   │   └── WaterQuality
│   └── Visibility
├── GeographicalConditions
│   ├── Terrain
│   ├── Infrastructure
│   └── NetworkTopology
├── TemporalConditions
│   ├── TimeOfDay
│   ├── Season
│   └── SpecialEvents
├── OperationalConditions
│   ├── LoadLevel
│   ├── EquipmentStatus
│   └── EmergencyLevel
└── RegulatoryConditions
    ├── OperatingLimits
    └── ComplianceRequirements
```

### 5.3.3.2 基于逻辑的ODD规范

ODD约束可以用逻辑公式形式化描述。对于水系统调度系统，ODD规范示例：

**环境条件约束**：

$$\text{ODD}_{\text{env}} = (P_{\text{rain}} \leq P_{max}) \wedge (T_{\text{air}} \geq T_{\min}) \wedge (Q_{\text{in}}^{\text{forecast}} \in [Q_{\min}, Q_{\max}])$$

**系统状态约束**：

$$\text{ODD}_{\text{sys}} = (\text{Pump}_1 = \text{OK}) \vee (\text{Pump}_2 = \text{OK}) \wedge (\text{SCADA} = \text{Online})$$

**时间约束**：

$$\text{ODD}_{\text{time}} = (T_{\text{current}} \in \text{BusinessHours}) \vee (\text{EmergencyMode} = \text{True})$$

完整ODD是各维度约束的合取：

$$\text{ODD} = \text{ODD}_{\text{env}} \wedge \text{ODD}_{\text{sys}} \wedge \text{ODD}_{\text{time}} \wedge \ldots$$

### 5.3.3.3 基于集合的ODD表示

ODD可以表示为多维参数空间中的超矩形或更复杂的几何形状：

$$\mathcal{O} = \{\mathbf{p} \in \mathbb{R}^n : \mathbf{p}_{\min} \leq \mathbf{p} \leq \mathbf{p}_{\max}, \mathbf{g}(\mathbf{p}) \leq \mathbf{0}\}$$

其中 $\mathbf{p}$ 是ODD参数向量，$\mathbf{g}(\cdot)$ 是非线性约束函数。

## 5.3.4 水系统ODD的具体维度

### 5.3.4.1 水文气象维度

水文气象条件是影响水系统运行的首要外部因素。

**降雨条件**：
- 降雨强度：$I \in [0, I_{\max}]$ (mm/h)
- 降雨持续时间：$D_{\text{rain}} \in [0, D_{\max}]$ (h)
- 降雨空间分布：均匀/局部/流域分布

**径流条件**：
- 入库流量：$Q_{\text{in}} \in [Q_{\text{base}}, Q_{\text{flood}}]$ (m³/s)
- 流量变化率：$|\dot{Q}_{\text{in}}| \leq \dot{Q}_{\max}$ (m³/s²)
- 洪水预见期：$T_{\text{lead}} \geq T_{\min}$ (h)

### 5.3.4.2 系统设备维度

设备健康状态决定了控制系统的执行能力。

**执行器状态**：
- 闸门：开度精度、响应时间、故障状态
- 泵站：可用台数、单机容量、效率曲线
- 阀门：调节范围、泄漏率、故障模式

**传感器状态**：
- 水位计：测量精度、采样频率、通信状态
- 流量计：量程范围、校准状态、冗余配置
- 水质监测：监测参数、检测限、响应时间

**通信与计算**：
- 通信链路：带宽、延迟、丢包率
- 计算资源：处理能力、存储容量、实时性

### 5.3.4.3 运行需求维度

运行需求定义了系统需要满足的服务目标。

**供水需求**：
- 需水量：$D(t) \in [D_{\min}, D_{\max}]$ (m³/s)
- 需水模式：日变化系数、季节变化
- 优先级：居民生活 > 工业生产 > 农业灌溉 > 生态

**防洪需求**：
- 防洪标准：设计洪水频率
- 安全泄量：下游河道承载能力
- 预警时间：人员转移所需时间

**生态需求**：
- 生态流量：$Q_{\text{eco}}^{\min}$ (m³/s)
- 水质标准：各指标浓度限值
- 水位波动：日变幅限制

### 5.3.4.4 法规与社会维度

外部约束条件影响控制决策的合法性。

**法规约束**：
- 水资源调度规程
- 防洪预案要求
- 环境保护法规

**社会约束**：
- 公众接受度
- 经济影响评估
- 应急响应要求

## 5.3.5 ODD边界的确定方法

### 5.3.5.1 基于能力分析的边界确定

ODD边界应基于系统能力的定量分析确定。对于每个ODD维度，需要评估系统在该维度上的能力范围。

**能力评估框架**：

1. **识别关键场景**：确定影响系统安全的关键运行场景
2. **能力建模**：建立系统在各场景下的能力模型
3. **边界测试**：通过仿真或测试确定能力边界
4. **安全裕度**：在能力边界内保留适当安全裕度

### 5.3.5.2 基于风险评估的边界确定

风险评估方法可以量化不同ODD边界选择的安全影响[5]。

**风险函数**：

$$R(\mathcal{O}) = \int_{\mathbf{c} \notin \mathcal{O}} P(\mathbf{c}) \cdot I(\mathbf{c}) \cdot S(\mathbf{c}) d\mathbf{c}$$

其中 $P(\mathbf{c})$ 是条件 $\mathbf{c}$ 发生的概率，$I(\mathbf{c})$ 是系统在该条件下失效的概率，$S(\mathbf{c})$ 是失效后果的严重度。

ODD边界优化问题：

$$\max_{\mathcal{O}} \text{Coverage}(\mathcal{O}) \quad \text{s.t.} \quad R(\mathcal{O}) \leq R_{\max}$$

### 5.3.5.3 基于验证的边界确定

通过系统性验证活动确定ODD边界：

**仿真验证**：在仿真环境中测试系统在各种边界条件下的表现

**场地测试**：在实际系统中进行受控测试

**运行数据**：分析历史运行数据，识别系统成功/失败的边界条件

## 5.3.6 ODD监控与管理

### 5.3.6.1 ODD合规性监控

实时监控系统运行条件是否在ODD范围内：

$$\text{InODD}(t) = \mathbb{1}_{\mathbf{c}(t) \in \mathcal{O}}$$

当 $\text{InODD}(t) = 0$ 时，系统应触发退出策略。

### 5.3.6.2 ODD退出策略

当系统即将或已经超出ODD时，需要执行退出策略：

**最小风险状态**：将系统引导至安全状态

$$\mathbf{x}_{\text{MRC}} = \arg\min_{\mathbf{x}} \text{Risk}(\mathbf{x}, \mathbf{c}(t))$$

**控制权限移交**：将控制权移交给人工操作员或备用系统

**系统降级**：降低自主级别，限制功能范围

### 5.3.6.3 ODD动态调整

在运行过程中，ODD可以根据系统学习或环境变化动态调整：

**ODD扩展**：通过验证和测试，逐步扩展ODD范围

$$\mathcal{O}_{\text{new}} = \mathcal{O}_{\text{current}} \cup \Delta\mathcal{O}$$

**ODD收缩**：当发现新的安全风险时，收缩ODD范围

$$\mathcal{O}_{\text{new}} = \mathcal{O}_{\text{current}} \setminus \mathcal{O}_{\text{risk}}$$

## 5.3.7 ODD在水系统中的应用实例

### 5.3.7.1 水库调度ODD

某水库调度系统的ODD定义示例：

| ODD维度 | 参数范围 | 说明 |
|---------|----------|------|
| 入库流量 | 10-5000 m³/s | 超设计洪水需人工介入 |
| 预报精度 | ≥85% (24h) | 预报精度不足时保守调度 |
| 闸门可用 | ≥2台 | 确保泄洪能力冗余 |
| 通信状态 | 主备链路正常 | 单链路故障时降级运行 |
| 下游安全 | 预警系统正常 | 确保人员安全转移 |

### 5.3.7.2 供水管网ODD

城市供水管网控制系统的ODD：

| ODD维度 | 参数范围 | 说明 |
|---------|----------|------|
| 需水量变化 | ±30%日预测 | 超出范围启动应急预案 |
| 泵站可用 | ≥80%容量 | 备用泵组可投入 |
| 水质指标 | 达标率≥95% | 超标时切换水源 |
| 管网压力 | 0.15-0.6 MPa | 超压/欠压告警 |

## 5.3.8 本章小结

运行设计域ODD为自主水系统控制提供了明确的运行边界定义框架。本章主要内容包括：

1. **理论基础**：阐述了ODD的定义、层次结构和与系统能力的关系，建立了ODD的理论框架。

2. **形式化描述**：介绍了基于本体、逻辑和集合的ODD建模方法，支持不同抽象层次的ODD规范。

3. **水系统维度**：系统分析了水文气象、设备状态、运行需求和法规社会四个维度的ODD参数。

4. **边界确定**：讨论了基于能力分析、风险评估和验证测试的ODD边界确定方法。

5. **监控管理**：介绍了ODD合规性监控、退出策略和动态调整机制。

ODD概念是水系统自主控制安全的关键使能技术，为系统能力边界的明确界定和安全运行提供了系统方法论。

---

## 参考文献

[1] KOOPMAN P, WAGNER M. Autonomous vehicle safety: An interdisciplinary challenge[J]. IEEE Intelligent Transportation Systems Magazine, 2017, 9(1): 90-96.

[2] SAE INTERNATIONAL. Taxonomy and definitions for terms related to driving automation systems for on-road motor vehicles: SAE J3016_202104[S]. SAE International, 2021.

[3] GEYER S, BALTZER M, FRANZ B, et al. Concept and development of a unified ontology for generating test and use-case catalogues for assisted and automated vehicle guidance[J]. IET Intelligent Transport Systems, 2014, 8(3): 183-189.

[4] BATSCH F, BAGHERI A, RIEDMAIER S, et al. Ontology-based ODD description for the safety assessment of automated vehicles[C]//2021 IEEE International Conference on Omni-layer Intelligent Systems (COINS). IEEE, 2021: 1-6.

[5] RIEDMAIER S, PONN T, LUDWIG D, et al. Survey on scenario-based safety assessment of automated vehicles[J]. IEEE Access, 2020, 8: 87456-87477.

[6] BSI. PAS 1883:2020 Operational design domain (ODD) taxonomy for an automated driving system (ADS)[S]. British Standards Institution, 2020.

[7] GYLLENHAMMAR M, WARG F, CHEN D, et al. Towards an operational design domain that supports the safety argumentation of automated driving systems[C]//2020 IEEE Intelligent Vehicles Symposium (IV). IEEE, 2020: 1187-1194.

[8] ULBRICH S, MENZEL T, RESCHKA A, et al. Defining and substantiating the terms scene, situation, and scenario for automated driving[C]//2015 IEEE 18th International Conference on Intelligent Transportation Systems. IEEE, 2015: 982-988.

[9] CZARNECKI K. Operational world model ontology for automated driving systems[R]. Waterloo Intelligent Systems Engineering (WISE) Lab Report, 2018.

[10] BOLTE J, BAR A, LÜTTING J, et al. Towards a comprehensive operational design domain for automated driving[C]//2020 IEEE 23rd International Conference on Intelligent Transportation Systems (ITSC). IEEE, 2020: 1-8.

[11] BAGHERI A, RIEDMAIER S, BATSCH F, et al. An ontology for the operational design domain of automated driving[C]//2021 IEEE International Conference on Omni-layer Intelligent Systems (COINS). IEEE, 2021: 1-6.

[12] WOOD M, BROWN D, BHARATHI M C R, et al. Operational design domain (ODD) framework for autonomous driving systems[C]//2021 IEEE International Conference on Omni-layer Intelligent Systems (COINS). IEEE, 2021: 1-6.

</ama-doc>
