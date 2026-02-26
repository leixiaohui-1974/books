# HydroOS-Agent：水网全生命周期多智能体智能决策平台

> **用途**：本文件是 Claude Code 的项目提示词（CLAUDE.md），指导开发以 HydroOS 为核心的多智能体平台 MVP。
> **最小对象**：单水箱（Single Tank）系统
> **目标**：用最小对象跑通完整架构，为后续扩展到任意水网工程奠定基础。

---

## 一、项目愿景与核心理念

### 1.1 双层架构思想（本项目的灵魂）

```
┌───────────────────────────────────────────────────────────┐
│  L4  灵活智能层 (Flexible AI Layer) — Agent              │
│                                                           │
│  主编排 Agent（Orchestrator）                             │
│    ├── 理解用户自然语言意图                               │
│    ├── 选择/组合 Skill                                    │
│    ├── 临时生成分析脚本（优化、比选、可视化）             │
│    └── 汇总结果、生成报告、辅助决策                       │
│                                                           │
│  通信协议: A2A (Agent间) | 调用协议: Skill → MCP Tool    │
├───────────────────────────────────────────────────────────┤
│  L3  技能编排层 (Skill Layer) — 固定工作流封装            │
│                                                           │
│  Skill: 控制系统设计   = 仿真→辨识→控制→闭环验证→评价    │
│  Skill: 数据分析预测   = 清洗→特征工程→预测→评价          │
│  Skill: ODD安全评估    = ODD定义→仿真扫描→边界标定→报告   │
│  Skill: 优化设计       = 设计空间→仿真验证→敏感性→比选    │
│  Skill: 全生命周期闭环 = 上述 Skill 的有序组合            │
│                                                           │
│  每个 Skill = 带描述/触发条件/参数模板的固定 Tool 编排    │
│  不可随意修改（精雕细琢后固化），Agent 只能选择和调用     │
├───────────────────────────────────────────────────────────┤
│  L2  核心工具层 (MCP Tool Layer) — 原子计算能力           │
│                                                           │
│  MCP Tool: simulate │ identify │ clean │ predict          │
│  MCP Tool: schedule │ control  │ odd   │ evaluate │ design│
│                                                           │
│  每个 Tool 是一个 MCP Server 暴露的原子函数               │
│  纯数值计算，无 LLM 依赖，确定性、可测试                 │
├───────────────────────────────────────────────────────────┤
│  L1  分布式计算层 (Compute Layer) — Ray                   │
│                                                           │
│  Ray Core: @ray.remote 装饰核心计算函数                   │
│  Ray Actor: 有状态的仿真环境 / 控制器实例                 │
│  Ray Data: 大规模时序数据并行处理                         │
│  单机模式 (MVP) → 集群模式 (扩展后)                       │
│                                                           │
│  水箱单机即可；管网/梯级电站需要集群并行                  │
├───────────────────────────────────────────────────────────┤
│  L0  数据与感知层 (Data & Perception Layer)               │
│                                                           │
│  传感器数据 (模拟/实际) │ 时序数据库 │ 配置存储           │
│  执行器指令接口 │ SCADA 适配器 (扩展)                     │
└───────────────────────────────────────────────────────────┘
```

**核心原则**：
- **L1-L2 固定**：核心计算模块和分布式运行时是经过严格验证的确定性工具，如同邮箱服务器一样不需要重新开发，只需调用。
- **L3 固化**：Skill 是经过验证的固定工作流封装。Agent 不能修改 Skill 内部逻辑，只能选择和调用——这是"固定工作流"的体现。
- **L4 灵活**：大模型智能体只在与人交互时介入，负责理解意图、选择 Skill、临时开发辅助功能（优化脚本、可视化报告），实现辅助决策。
- **不是替代，是辅助**：类似阿里"阿福"医疗助手的思路——不直接替代专家决策，而是提供备选方案、背景知识、工具组合，降低工作量、提高决策质量。

### 1.2 Tool → Skill → Agent 三级概念辨析

| 层级 | 概念 | 类比 | 示例 | 谁创建 | 可否临时修改 |
|------|------|------|------|--------|-------------|
| MCP Tool | 原子操作 | 一把螺丝刀 | `simulate_tank()` | 开发者 | 否（代码级变更） |
| Skill | 固定工作流 | 一套标准化操作规程 | "控制系统设计"流程 | 领域专家+开发者 | 否（验证后固化） |
| Agent | 智能角色 | 一个工程师 | Orchestrator Agent | AI 编排 | 是（灵活组合 Skill） |

Agent 选择哪些 Skill 来组合——这是"灵活"的部分。
每个 Skill 内部怎么调 Tool——这是"固定"的部分。

### 1.3 设计目标

1. **以水箱为最小对象**，演示仿真→辨识→预测→控制→ODD→评价的完整链路
2. **架构对标国际主流开源框架**，确保可扩展到任意机理/数据驱动模型
3. **MCP + A2A 双协议**：核心工具通过 MCP 暴露能力，Agent 之间通过 A2A 协作
4. **五层架构对齐 HydroOS**：数据感知 → 分布式计算 → MCP 工具 → Skill 编排 → 认知决策
5. **计算可伸缩**：MVP 阶段 Ray 单机模式，扩展时无缝切换到 Ray 集群

---

## 二、技术架构

### 2.1 总体架构（五层，对标开源生态）

```
                        用户（调度员/研究员/规划师/设计师）
                                    │
                                    ▼
                    ┌───────────────────────────┐
                    │  L4 认知决策层 (Cognitive)  │  ← HydroOS 认知决策层
                    │                             │
                    │  Orchestrator Agent          │  ← LangGraph 状态图编排
                    │    ├── Planning Agent        │     意图解析 + 任务规划
                    │    ├── Analysis Agent        │     临时开发分析/优化脚本
                    │    ├── Report Agent          │     报告生成 + 可视化
                    │    └── Safety Agent          │     ODD 边界校验
                    │                             │
                    │  A2A (Agent间) + MCP (调Skill)│
                    └──────────┬────────────────────┘
                               │ 选择 Skill
                    ┌──────────▼────────────────────┐
                    │  L3 技能编排层 (Skill Layer)    │  ← 固定工作流封装
                    │                                 │
                    │  Skill: control_system_design   │  仿真→辨识→控制→验证→评价
                    │  Skill: data_analysis_predict   │  清洗→特征→预测→评价
                    │  Skill: odd_assessment          │  ODD定义→扫描→标定→报告
                    │  Skill: optimization_design     │  设计空间→仿真→敏感性→比选
                    │  Skill: full_lifecycle          │  全链路闭环
                    └──────────┬────────────────────┘
                               │ 调用 MCP Tool
                    ┌──────────▼────────────────────┐
                    │  L2 核心工具层 (MCP Tool Layer) │  ← HydroOS 过程控制层
                    │                                 │
                    │  MCP: simulate │ identify │clean│
                    │  MCP: predict │ schedule │ctrl  │
                    │  MCP: odd │ evaluate │ design   │
                    └──────────┬────────────────────┘
                               │ 提交计算任务
                    ┌──────────▼────────────────────┐
                    │  L1 分布式计算层 (Ray Compute)  │  ← 可伸缩运行时
                    │                                 │
                    │  ray.remote(仿真) │ Ray Actor   │
                    │  Ray Data(批处理) │ Ray Serve   │
                    └──────────┬────────────────────┘
                               │ 读写数据
                    ┌──────────▼────────────────────┐
                    │  L0 数据感知层 (Perception)     │  ← HydroOS 执行感知层
                    │                                 │
                    │  传感器数据 │ 状态数据库 │ 配置  │
                    │  执行器接口 │ 时序存储 │ SCADA  │
                    └──────────────────────────────────┘
```

### 2.2 开源框架选型

| 层级 | 组件 | 选型 | 理由 |
|------|------|------|------|
| L4 Agent | Agent 编排 | **LangGraph** | 有向图架构，精确控制分支/并行/人机交互；状态持久化；故障恢复 |
| L4 Agent | Agent 间通信 | **A2A 协议** | Google+Linux Foundation 主导，标准化 Agent 发现/任务委托/生命周期管理 |
| L4 Agent | LLM 后端 | **Claude Sonnet 4.5** | 通过 Anthropic API，兼容 MCP 原生 |
| L3 Skill | 工作流定义 | **YAML + Python** | Skill 用 YAML 声明元数据+触发条件，Python 实现编排逻辑 |
| L2 Tool | 工具暴露 | **MCP v2 (FastMCP)** | Anthropic 主导的事实标准，Agent→Tool 的"USB-C 接口" |
| L2 Tool | 数值计算 | **SciPy / NumPy** | Python 科学计算标准库 |
| L2 Tool | 控制系统 | **python-control** | 开源控制系统工具箱 |
| L2 Tool | 优化求解 | **PuLP / scipy.optimize** | 线性规划 + 非线性优化 |
| L1 Compute | 分布式运行时 | **Ray** | Python 原生分布式框架；OpenAI/Uber 生产验证；Linux Foundation 项目；单机→集群无缝切换 |
| L1 Compute | GPU 并行 | **Ray + CuPy**（扩展期） | 大规模管网/梯级电站圣维南方程并行求解 |
| L0 Data | 时序数据 | **SQLite + Pandas**（MVP）→ **TimescaleDB**（扩展） | 轻量级起步，后期可切换 |
| L0 Data | 可视化 | **Matplotlib / Plotly** | 科学绘图 + 交互式图表 |

### 2.3 目录结构

```
hydroos-agent/
├── CLAUDE.md                    # 本文件（Claude Code 项目提示词）
├── pyproject.toml               # Python 项目配置
├── README.md                    # 项目说明
│
├── core/                        # L2 核心工具层——原子计算模块
│   ├── __init__.py
│   ├── simulation/              # 仿真引擎
│   │   ├── tank_model.py        #   水箱 ODE 模型 (dh/dt = Qin/A - Cd*a*sqrt(2gh)/A)
│   │   └── simulator.py         #   仿真运行器（欧拉/RK4/odeint）
│   ├── identification/          # 系统辨识
│   │   ├── least_squares.py     #   最小二乘辨识
│   │   └── arx_model.py         #   ARX 模型辨识
│   ├── data_clean/              # 数据清洗
│   │   ├── outlier_detect.py    #   异常值检测（3σ/IQR/孤立森林）
│   │   └── interpolation.py     #   缺失值插补
│   ├── prediction/              # 预测模型
│   │   ├── linear_predictor.py  #   线性预测器
│   │   └── lstm_predictor.py    #   LSTM 预测器（可选）
│   ├── scheduling/              # 调度优化
│   │   ├── lp_scheduler.py      #   线性规划调度
│   │   └── rule_based.py        #   规则调度
│   ├── control/                 # 控制器
│   │   ├── pid_controller.py    #   PID 控制器
│   │   └── mpc_controller.py    #   模型预测控制
│   ├── odd/                     # 运行设计域
│   │   ├── odd_definition.py    #   ODD 边界定义
│   │   ├── odd_monitor.py       #   ODD 实时监测
│   │   └── mrc_handler.py       #   最小风险条件处理
│   ├── evaluation/              # 性能评价
│   │   ├── metrics.py           #   RMSE/MAE/NSE 等指标
│   │   └── wnal_assessor.py     #   WNAL 等级评估
│   └── design/                  # 优化设计
│       ├── sizing.py            #   水箱尺寸优化
│       └── sensitivity.py       #   敏感性分析
│
├── compute/                     # L1 分布式计算层——Ray 封装
│   ├── __init__.py
│   ├── ray_config.py            # Ray 初始化（单机/集群自动检测）
│   ├── distributed_sim.py       # @ray.remote 仿真任务（批量参数扫描/蒙特卡洛）
│   ├── distributed_optim.py     # @ray.remote 优化任务（并行多目标/敏感性）
│   ├── parallel_data.py         # Ray Data 大规模时序数据并行清洗/预处理
│   └── actor_controller.py      # Ray Actor 有状态控制器（MPC 滚动优化）
│
├── mcp_servers/                 # L2 MCP 工具服务器——将 core 暴露为 MCP 接口
│   ├── __init__.py
│   ├── simulation_server.py     # MCP Server: 仿真工具
│   ├── identification_server.py # MCP Server: 辨识工具
│   ├── dataclean_server.py      # MCP Server: 数据清洗
│   ├── prediction_server.py     # MCP Server: 预测工具
│   ├── scheduling_server.py     # MCP Server: 调度工具
│   ├── control_server.py        # MCP Server: 控制工具
│   ├── odd_server.py            # MCP Server: ODD 工具
│   ├── evaluation_server.py     # MCP Server: 评价工具
│   └── design_server.py         # MCP Server: 设计工具
│
├── skills/                      # L3 技能编排层——固定工作流封装
│   ├── __init__.py
│   ├── base_skill.py            # Skill 基类（描述/触发条件/参数模板/Tool 链）
│   ├── control_system_design.py # Skill: 控制系统设计（仿真→辨识→控制→验证→评价）
│   ├── control_system_design.yaml  # 元数据：名称/描述/触发词/输入输出 Schema
│   ├── data_analysis_predict.py # Skill: 数据分析预测（清洗→特征→预测→评价）
│   ├── data_analysis_predict.yaml
│   ├── odd_assessment.py        # Skill: ODD 安全评估（定义→扫描→标定→报告）
│   ├── odd_assessment.yaml
│   ├── optimization_design.py   # Skill: 优化设计（设计空间→仿真→敏感性→比选）
│   ├── optimization_design.yaml
│   ├── full_lifecycle.py        # Skill: 全生命周期闭环（组合以上 Skill）
│   └── full_lifecycle.yaml
│
├── agents/                      # L4 灵活智能层——LangGraph Agent 定义
│   ├── __init__.py
│   ├── orchestrator.py          # 主编排 Agent（意图路由 + Skill 选择）
│   ├── planning_agent.py        # 规划 Agent（任务分解 + 方案比选）
│   ├── analysis_agent.py        # 分析 Agent（临时生成脚本 + 数据分析）
│   ├── report_agent.py          # 报告 Agent（可视化 + 文档生成）
│   ├── safety_agent.py          # 安全 Agent（ODD 校验 + MRC 触发）
│   └── agent_cards/             # A2A Agent Card 定义
│       ├── orchestrator.json
│       ├── planning.json
│       ├── analysis.json
│       ├── report.json
│       └── safety.json
│
├── data/                        # 数据目录
│   ├── tank_config.json         # 水箱参数配置
│   ├── sample_timeseries.csv    # 示例时序数据
│   └── odd_specs.json           # ODD 规格定义
│
├── tests/                       # 测试
│   ├── test_core/               # core 模块单元测试
│   ├── test_compute/            # Ray 分布式测试
│   ├── test_mcp_servers/        # MCP 接口测试
│   ├── test_skills/             # Skill 集成测试
│   └── test_agents/             # Agent 端到端测试
│
└── docs/                        # 文档
    ├── architecture.md          # 五层架构设计文档
    ├── skill_authoring_guide.md # Skill 开发指南（如何新增 Skill）
    ├── mcp_api_reference.md     # MCP 接口文档
    ├── ray_deployment.md        # Ray 部署指南（单机/集群）
    └── user_guide.md            # 用户指南
```

---

## 三、L2 核心工具层详细设计（MCP Tool）

### 3.1 水箱模型 (Simulation)

**物理方程**：

```
dh/dt = (Q_in - Q_out) / A
Q_out = Cd * a * sqrt(2 * g * h)
```

其中：
- `h`：水位 (m)
- `A`：水箱截面积 (m²)
- `Q_in`：入流量 (m³/s)
- `Q_out`：出流量 (m³/s)
- `Cd`：流量系数 (无量纲)
- `a`：出口面积 (m²)
- `g`：重力加速度 (9.81 m/s²)

**MCP Tool 接口设计**：

```python
@mcp_tool(name="simulate_tank")
def simulate_tank(
    duration: float,        # 仿真时长 (s)
    dt: float = 1.0,        # 时间步长 (s)
    q_in_profile: list,     # 入流时序 [(t, Q_in), ...]
    initial_h: float = 0.5, # 初始水位 (m)
    tank_params: dict = None # 水箱参数（A, Cd, a, 默认从配置读取）
) -> dict:
    """运行水箱仿真，返回水位/流量时序"""
    return {
        "time": [...],
        "water_level": [...],
        "outflow": [...],
        "metadata": {"solver": "RK4", "steps": N}
    }
```

### 3.2 系统辨识 (Identification)

**功能**：从观测数据反演水箱参数（Cd, a 等）

**方法**：
- 最小二乘法拟合
- ARX 模型辨识（线性化后的离散传递函数）

**MCP Tool**: `identify_parameters(observed_data, model_type="nonlinear|ARX")`

### 3.3 数据清洗 (DataClean)

**功能**：处理传感器噪声、缺失值、异常值

**方法**：
- 3σ 规则 / IQR 方法检测异常值
- 线性/样条插值补缺
- 中值滤波降噪

**MCP Tool**: `clean_timeseries(raw_data, methods=["outlier_3sigma", "interpolate_linear", "median_filter"])`

### 3.4 预测 (Prediction)

**功能**：基于历史数据预测未来水位/流量

**方法**：
- 线性回归（基线）
- LSTM（可选，需 torch）

**MCP Tool**: `predict_future(historical_data, horizon=60, model="linear|lstm")`

### 3.5 调度优化 (Scheduling)

**功能**：在约束条件下优化入流分配

**方法**：
- 线性规划（PuLP）
- 规则调度（if-else 逻辑）

**MCP Tool**: `optimize_schedule(demand_forecast, constraints, objective="minimize_cost|maximize_supply")`

### 3.6 控制器 (Control)

**功能**：实时水位控制

**方法**：
- PID 控制器（Kp, Ki, Kd 可调）
- MPC 控制器（基于线性化模型，滚动优化）

**MCP Tool**: `run_controller(setpoint, current_state, controller_type="PID|MPC", params={})`

### 3.7 运行设计域 ODD (Operational Design Domain)

**功能**：定义和监测系统安全运行边界

**ODD 六维向量**（水箱简化版）：
```json
{
  "water_level": {"min": 0.1, "max": 1.8, "unit": "m"},
  "inflow_rate": {"min": 0.0, "max": 0.05, "unit": "m³/s"},
  "outflow_rate": {"min": 0.0, "max": 0.03, "unit": "m³/s"},
  "water_quality": {"turbidity_max": 10, "unit": "NTU"},
  "temperature": {"min": 0, "max": 40, "unit": "°C"},
  "structural": {"pressure_max": 50, "unit": "kPa"}
}
```

**三区域判定**：
- 正常域（Normal）：所有参数在 ODD 内 → 自主运行
- 扩展域（Extended）：部分参数接近边界 → 预警 + 人工确认
- MRC 域：超出 ODD → 触发最小风险条件（关闸/排水/报警）

**MCP Tool**: `check_odd(current_state) → {"zone": "normal|extended|mrc", "violations": [...]}`

### 3.8 性能评价 (Evaluation)

**功能**：评估控制/预测/仿真的性能

**指标**：RMSE, MAE, NSE (Nash-Sutcliffe), 响应时间, 超调量, 稳态误差

**MCP Tool**: `evaluate_performance(observed, predicted, metrics=["RMSE","NSE","settling_time"])`

### 3.9 WNAL 等级评估

**功能**：基于系统能力评估自主运行等级（L0-L5）

**MCP Tool**: `assess_wnal(system_capabilities) → {"level": "L3", "score": 72, "gaps": [...]}`

### 3.10 优化设计 (Design)

**功能**：水箱参数优化设计

**方法**：
- 参数敏感性分析（Morris / Sobol）
- 尺寸优化（目标：满足需求+最小造价）

**MCP Tool**: `optimize_design(requirements, design_space, objective="minimize_cost")`

---

## 四、L3 技能编排层详细设计（Skill）

### 4.1 Skill 基类设计

每个 Skill 由两个文件组成：

**YAML 元数据**（声明式，描述 Skill 的"身份证"）：
```yaml
# skills/control_system_design.yaml
name: control_system_design
display_name: "控制系统设计"
description: "从仿真建模到闭环验证的完整控制系统设计流程"
trigger_phrases:
  - "设计控制器"
  - "PID调参"
  - "控制系统"
  - "闭环验证"
input_schema:
  plant_type: { type: string, default: "tank", enum: ["tank", "canal", "network"] }
  controller_type: { type: string, default: "PID", enum: ["PID", "MPC"] }
  setpoint: { type: number, description: "目标水位 (m)" }
output_schema:
  controller_params: { type: object }
  performance_metrics: { type: object }
  plots: { type: array, items: { type: string } }
tools_required:            # 这个 Skill 内部调用的 MCP Tool 序列
  - simulate_tank
  - identify_parameters
  - run_controller
  - evaluate_performance
max_execution_time: 120    # 秒
```

**Python 实现**（编排逻辑，固定不变）：
```python
# skills/control_system_design.py
class ControlSystemDesignSkill(BaseSkill):
    """控制系统设计 Skill——固定工作流，不可被 Agent 修改"""

    async def execute(self, params: dict) -> SkillResult:
        # Step 1: 仿真建模——获取开环响应
        sim_result = await self.call_tool("simulate_tank", {...})

        # Step 2: 系统辨识——从仿真数据反演模型参数
        id_result = await self.call_tool("identify_parameters", {...})

        # Step 3: 控制器设计+闭环仿真
        ctrl_result = await self.call_tool("run_controller", {...})

        # Step 4: 性能评价
        eval_result = await self.call_tool("evaluate_performance", {...})

        return SkillResult(
            controller_params=ctrl_result.params,
            performance_metrics=eval_result.metrics,
            plots=eval_result.plots
        )
```

### 4.2 已定义 Skill 清单

| Skill 名称 | 内部 Tool 链 | 典型触发场景 |
|------------|-------------|-------------|
| control_system_design | simulate→identify→control→evaluate | "设计一个PID控制器" |
| data_analysis_predict | clean→predict→evaluate | "清洗数据并预测水位" |
| odd_assessment | odd_define→simulate(扫描)→odd_check→report | "评估系统ODD" |
| optimization_design | design→simulate(验证)→sensitivity→evaluate | "优化水箱尺寸" |
| full_lifecycle | 以上Skill有序组合 | "从零开始设计一个水箱系统" |

### 4.3 新增 Skill 的流程

1. 创建 `skills/new_skill.yaml`（元数据）
2. 创建 `skills/new_skill.py`（继承 BaseSkill，实现 execute）
3. 编写集成测试 `tests/test_skills/test_new_skill.py`
4. Orchestrator 自动发现新 Skill（通过扫描 skills/ 目录的 YAML 文件）

---

## 五、L1 分布式计算层详细设计（Ray）

### 5.1 设计原则

- **MVP 阶段用 Ray 单机模式**：`ray.init()` 自动检测本地资源，无需集群配置
- **core/ 模块不感知 Ray**：核心计算函数保持纯 Python，由 compute/ 层包装为 Ray 任务
- **渐进式并行**：只对计算密集型操作加 `@ray.remote`，不过度分布式化

### 5.2 哪些操作需要分布式

| 操作 | 水箱阶段 | 管网/梯级阶段 | Ray 组件 |
|------|---------|-------------|---------|
| 参数扫描（蒙特卡洛） | 有用（100+次仿真） | 必须（10000+次） | ray.remote Task |
| 敏感性分析（Morris/Sobol） | 有用 | 必须 | ray.remote Task |
| MPC 滚动优化 | 单机足够 | 需要状态持久化 | Ray Actor |
| 大规模数据清洗 | 单机 | 需要并行 | Ray Data |
| 多目标优化（NSGA-II） | 有用 | 必须 | ray.remote Task |
| 模型训练（LSTM） | 单机 GPU | 多 GPU 分布式 | Ray Train |

### 5.3 代码模式

```python
# compute/distributed_sim.py
import ray
from core.simulation.simulator import run_simulation

@ray.remote
def simulate_remote(params: dict) -> dict:
    """将仿真任务提交到 Ray 集群"""
    return run_simulation(**params)

async def parameter_sweep(param_grid: list[dict]) -> list[dict]:
    """参数扫描——自动并行化"""
    futures = [simulate_remote.remote(p) for p in param_grid]
    return ray.get(futures)  # 并行执行，收集结果
```

```python
# compute/actor_controller.py
@ray.remote
class MPCControllerActor:
    """有状态的 MPC 控制器——作为 Ray Actor 持久运行"""
    def __init__(self, model_params, horizon=10):
        self.controller = MPCController(model_params, horizon)
        self.state_history = []

    def step(self, current_state, setpoint):
        action = self.controller.compute(current_state, setpoint)
        self.state_history.append((current_state, action))
        return action
```

### 5.4 Ray 配置策略

```python
# compute/ray_config.py
import ray

def init_ray():
    """智能初始化 Ray：自动检测单机/集群模式"""
    if ray.is_initialized():
        return

    # 检查是否存在 Ray 集群
    cluster_address = os.environ.get("RAY_ADDRESS")
    if cluster_address:
        ray.init(address=cluster_address)  # 连接已有集群
    else:
        ray.init()  # 单机模式，自动使用本地所有 CPU 核心
```

---

## 六、L4 灵活智能层详细设计（Agent）

### 6.1 Orchestrator Agent（主编排）

**职责**：理解用户自然语言请求，路由到合适的 Skill 或临时组装 Tool

**路由逻辑（三级优先）**：

| 优先级 | 匹配方式 | 动作 | 示例 |
|--------|---------|------|------|
| 1 | 精确匹配某个 Skill 的触发词 | 调用该 Skill | "设计PID控制器" → control_system_design Skill |
| 2 | 匹配单个 MCP Tool | 直接调用 Tool | "仿真一下水箱阶跃响应" → simulate_tank Tool |
| 3 | 无精确匹配 | 交给 Planning Agent 分解 | "比较三种方案的性价比" → Planning→Analysis→Report |

**意图分类表**：

| 用户说的话 | 路由层级 | 目标 |
|-----------|---------|------|
| "设计一个PID控制器让水位稳定在1米" | Skill | control_system_design |
| "评估当前系统的ODD" | Skill | odd_assessment |
| "从零开始设计一个水箱系统" | Skill | full_lifecycle |
| "清洗数据并预测未来1小时水位" | Skill | data_analysis_predict |
| "仿真一下水箱在入流阶跃下的响应" | Tool | simulate_tank |
| "帮我辨识水箱参数" | Tool | identify_parameters |
| "比较PID和MPC哪个控制效果更好" | Agent | Planning→Analysis→Report |
| "帮我出一份系统性能报告" | Agent | Report Agent |
| "当前水位安全吗" | Agent | Safety Agent |

**LangGraph 状态图**：

```
START → intent_classify
  ├── direct_tool_call → execute_tool → format_result → END
  ├── fixed_workflow → load_workflow → execute_steps → evaluate → END
  ├── flexible_analysis → planning_agent → [临时生成代码] → execute → END
  └── report_request → gather_data → report_agent → END

每个节点均可触发 safety_agent 进行 ODD 校验
```

### 6.2 Planning Agent（规划）

**职责**：将复杂请求拆解为子任务序列

**输入**：用户意图 + 当前系统状态
**输出**：任务DAG（有向无环图），每个节点标注所需工具和参数

### 6.3 Analysis Agent（分析）

**职责**：灵活组装分析能力，必要时**临时生成** Python 脚本

**关键能力**：
- 方案比选（A vs B，用统一指标评价）
- 敏感性分析（自动生成参数扫描代码）
- 优化求解（根据用户约束临时构建优化问题）
- 数据可视化（生成 matplotlib/plotly 代码）

**这是"灵活层"的核心体现**：核心工具不变，但分析方式可以千变万化。

### 6.4 Report Agent（报告）

**职责**：汇总分析结果，生成结构化报告

**输出格式**：Markdown / HTML / Word（python-docx）

### 6.5 Safety Agent（安全）

**职责**：全程守护 ODD 边界

**工作模式**：
- 被动模式：被 Orchestrator 调用，校验某次操作是否安全
- 主动模式：在仿真/控制过程中持续监测，发现越界立即中断并报告

---

## 七、开发计划（分阶段）

### Phase 1：L2 核心模块 + 单元测试（Week 1-2）

```
目标：core/ 目录下所有模块可独立运行并通过测试
优先级：simulation > control > odd > identification > evaluation > dataclean > prediction > scheduling > design
每个模块必须：
  - 纯 Python 实现，无 LLM 依赖，无 Ray 依赖
  - 完整 docstring（中英双语）
  - pytest 测试覆盖率 ≥ 80%
  - 输入/输出类型用 Pydantic BaseModel 定义
```

### Phase 2：L1 Ray 计算层（Week 2-3，与 Phase 1 并行）

```
目标：compute/ 封装，单机 Ray 跑通参数扫描和批量仿真
关键任务：
  - ray_config.py 智能初始化（单机/集群自动检测）
  - distributed_sim.py 参数扫描（100次蒙特卡洛仿真 < 10秒）
  - actor_controller.py MPC Actor（有状态控制器持久运行）
  - 验证：core/ 模块单独调用 vs Ray 调用结果一致
```

### Phase 3：L2 MCP Server 封装（Week 3）

```
目标：每个 core 模块封装为 MCP Server
技术：FastMCP (Python)
每个 Server 必须：
  - 暴露 ≥ 1 个 tool
  - 定义清晰的 JSON Schema 输入/输出
  - 支持 stdio 和 SSE 两种传输方式
  - 包含 Agent Card（JSON 格式的能力描述）
  - 计算密集型操作内部自动走 Ray
```

### Phase 4：L3 Skill 层封装（Week 4）

```
目标：5 个 Skill 各有 YAML 元数据 + Python 实现 + 集成测试
关键任务：
  - base_skill.py 基类（统一接口：描述/触发/参数/Tool链/超时）
  - 每个 Skill 的 YAML 触发词要覆盖用户的自然语言表达习惯
  - 集成测试：Skill 调用 MCP Tool → Tool 调用 core → core 可选走 Ray
  - Skill 注册机制：Orchestrator 启动时自动扫描 skills/*.yaml
```

### Phase 5：L4 LangGraph Agent 编排（Week 5-6）

```
目标：Orchestrator + 4 个子 Agent 协同工作
技术：LangGraph + Claude Sonnet 4.5 API
关键功能：
  - 自然语言 → 意图分类 → Skill/Tool/Agent 三级路由
  - Skill 执行（固定工作流）
  - 临时脚本生成与执行（Analysis Agent，灵活层核心）
  - ODD 安全守护（Safety Agent 全程在线）
```

### Phase 6：集成演示 + 文档（Week 7）

```
目标：完整演示全生命周期工作流
演示场景：
  1. 用户："帮我从零开始设计一个水箱控制系统"
     → 仿真建模 → 参数辨识 → PID设计 → MPC对比 → ODD评估 → 性能报告
  2. 用户："这组传感器数据有问题，帮我清洗后预测未来1小时水位"
     → 数据清洗 → 预测 → ODD校验 → 预警
  3. 用户："比较三种水箱尺寸方案的性价比"
     → 设计优化 → 仿真验证 → 评价 → 对比报告
```

---

## 八、编码规范

### 8.1 Python 规范
- Python ≥ 3.11
- 类型注解全覆盖（Pydantic v2 用于数据模型）
- 格式化：ruff format
- 检查：ruff check
- 测试：pytest + pytest-asyncio

### 8.2 命名规范
- 模块：snake_case
- 类：PascalCase
- MCP Tool：snake_case 动词开头（simulate_tank, clean_timeseries）
- Agent：PascalCase + Agent 后缀（OrchestratorAgent, SafetyAgent）

### 8.3 文档规范
- 每个公开函数/类必须有 docstring
- docstring 格式：Google style
- 关键参数标注物理单位

### 8.4 Git 规范
- 分支：main (稳定) / dev (开发) / feature/xxx
- Commit 消息：`[模块] 描述`，如 `[simulation] 实现水箱RK4求解器`

---

## 九、CHS 术语对照表（开发时保持一致）

| 代码中的名称 | CHS 术语 | 说明 |
|-------------|---------|------|
| `ODD` | 运行设计域 (Operational Design Domain) | 系统安全运行的参数边界 |
| `MRC` | 最小风险条件 (Minimal Risk Condition) | ODD 越界时的安全降级模式 |
| `WNAL` | 水网自主运行等级 (Water Network Autonomy Level) | L0-L5 分级 |
| `HydroOS` | 水网操作系统 (Hydro Operating System) | 三层架构：感知→控制→认知 |
| `PBM` | 物理对象模型 (Physics-Based Model) | 基于机理方程的模型 |
| `SM` | 简化模型 (Simplified Model) | 面向控制的降阶模型 |
| `IDZ` | 积分延迟零 (Integrator-Delay-Zero) | 明渠简化模型 |
| `HDC` | 分层分布式控制 (Hierarchical Distributed Control) | 多层级控制架构 |
| `MAS` | 多智能体系统 (Multi-Agent System) | 分布式协同控制 |

---

## 十、扩展路线图（MVP 之后）

### 10.1 模型扩展
- 水箱 → 串联水箱 → 明渠（圣维南方程）→ 管网（水锤方程）→ 梯级水电站
- 每种新模型只需：实现 core 模块 + 封装 MCP Server，Agent 层无需修改

### 10.2 工具扩展
- 接入 OpenModelica（Modelica 仿真）
- 接入 EPA-SWMM / EPANET（管网仿真）
- 接入 GPU 并行求解器

### 10.3 AI 能力扩展
- 接入瀚铎水网大模型（替代通用 LLM，领域知识更强）
- 知识图谱集成（水利规范、设计标准）
- 强化学习控制策略

### 10.4 部署扩展
- Docker 容器化
- Kubernetes 编排
- Web UI（Streamlit → React）
- 与实际 SCADA 系统对接

---

## 十一、关键参考

### 学术基础
- Lei 2025a: 水系统控制论:提出背景、技术框架与研究范式. 南水北调,23(04):761-769
- Lei 2025b: 基于无人驾驶理念的自主运行智慧水网架构. 南水北调,23(04):778-786
- Lei 2025c: 自主运行智能水网的在环测试体系. 南水北调,23(04):787-793

### 开源框架
- LangGraph: https://github.com/langchain-ai/langgraph （Agent 编排）
- FastMCP: https://github.com/jlowin/fastmcp （Python MCP Server）
- A2A Protocol: https://github.com/google/a2a-protocol （Agent 间通信）
- MCP Specification: https://modelcontextprotocol.io （MCP v2 规范）
- python-control: https://python-control.readthedocs.io （控制系统工具箱）

---

## 十二、注意事项

1. **core 模块必须可独立运行**：不依赖 LLM，不依赖 Ray，纯数值计算，确保确定性和可测试性
2. **compute 层是可选加速层**：core/ 不感知 Ray 的存在，compute/ 是透明包装；Ray 挂了，core 照样跑
3. **Skill 不可被 Agent 修改**：Skill 是固化的工作流，Agent 只能选择调用哪个 Skill 以及传什么参数
4. **MCP 接口设计要通用**：输入/输出用 JSON Schema 严格定义，为将来替换模型预留空间
5. **安全第一**：任何涉及控制指令下达的操作，必须经过 ODD 校验
6. **不要过早优化**：MVP 阶段用最简单的实现（如欧拉法而非高阶求解器），跑通链路优先
7. **中英双语注释**：代码注释和文档保持中英双语，方便国际化推广
8. **Ray 单机起步**：MVP 用 `ray.init()` 单机模式，不要一开始就搭集群
