# HydroOS-Agent：水网全生命周期多智能体智能决策平台

> **用途**：本文件是 Claude Code 的项目提示词（CLAUDE.md），指导开发以 HydroOS 为核心的多智能体平台 MVP。
> **最小对象**：单水箱（Single Tank）系统
> **目标**：用最小对象跑通完整架构，为后续扩展到任意水网工程奠定基础。

---

## 一、项目愿景与核心理念

### 1.1 双层架构思想（本项目的灵魂）

```
┌─────────────────────────────────────────────────────┐
│              灵活智能层 (Flexible AI Layer)           │
│                                                       │
│   主编排 Agent（Orchestrator）                        │
│     ├── 理解用户自然语言意图                          │
│     ├── 选择/组合下层核心工具                         │
│     ├── 临时生成分析脚本（优化、比选、可视化）        │
│     └── 汇总结果、生成报告、辅助决策                  │
│                                                       │
│   ← MCP 协议接入核心工具 | A2A 协议实现 Agent 间协作  │
├───────────────────────────────────────────────────────┤
│              固定工作流层 (Fixed Workflow Layer)       │
│                                                       │
│   仿真引擎 │ 辨识引擎 │ 数据清洗 │ 预测模型          │
│   调度优化 │ 控制器   │ ODD评估 │ 性能评价 │ 优化设计  │
│                                                       │
│   （精雕细琢、经过验证、不可随意替换的核心模块）      │
└─────────────────────────────────────────────────────────┘
```

**核心原则**：
- **下层固定**：仿真、控制、辨识、调度等核心模块是经过严格验证的确定性工具，如同邮箱服务器一样不需要重新开发，只需调用。
- **上层灵活**：大模型智能体只在与人交互时介入，负责理解意图、编排工具、临时开发辅助功能（如优化脚本、可视化报告），实现辅助决策。
- **不是替代，是辅助**：类似阿里"阿福"医疗助手的思路——不直接替代专家决策，而是提供备选方案、背景知识、工具组合，降低工作量、提高决策质量。

### 1.2 设计目标

1. **以水箱为最小对象**，演示仿真→辨识→预测→控制→ODD→评价的完整链路
2. **架构对标国际主流开源框架**，确保可扩展到任意机理/数据驱动模型
3. **MCP + A2A 双协议**：核心工具通过 MCP 暴露能力，Agent 之间通过 A2A 协作
4. **为 HydroOS 三层架构服务**：执行感知层 → 过程控制层 → 认知决策层

---

## 二、技术架构

### 2.1 总体架构（对标开源生态）

```
                        用户（调度员/研究员/规划师/设计师）
                                    │
                                    ▼
                    ┌───────────────────────────┐
                    │   认知决策层 (Cognitive)    │  ← HydroOS L3
                    │                             │
                    │  Orchestrator Agent          │  ← LangGraph 状态图编排
                    │    ├── Planning Agent        │     意图解析 + 任务规划
                    │    ├── Analysis Agent        │     临时开发分析/优化脚本
                    │    ├── Report Agent          │     报告生成 + 可视化
                    │    └── Safety Agent          │     ODD 边界校验
                    │                             │
                    │  通信协议: A2A (Agent间)     │
                    │  工具协议: MCP (Agent→Tool)  │
                    └──────────┬────────────────────┘
                               │ MCP Tool Calls
                    ┌──────────▼────────────────────┐
                    │   过程控制层 (Process Control)  │  ← HydroOS L2
                    │                                 │
                    │  MCP Server: Simulation Tool    │  仿真引擎 (圣维南/水箱ODE)
                    │  MCP Server: Identification     │  辨识引擎 (系统辨识)
                    │  MCP Server: DataClean          │  数据清洗
                    │  MCP Server: Prediction         │  预测模型 (LSTM/线性)
                    │  MCP Server: Scheduling         │  调度优化 (线性规划/MILP)
                    │  MCP Server: Controller         │  控制器 (PID/MPC)
                    │  MCP Server: ODD                │  运行设计域评估
                    │  MCP Server: Evaluation         │  性能评价
                    │  MCP Server: Design             │  优化设计
                    └──────────┬────────────────────┘
                               │ 读写数据
                    ┌──────────▼────────────────────┐
                    │   执行感知层 (Perception)       │  ← HydroOS L1
                    │                                 │
                    │  传感器数据 (模拟) │ 状态数据库   │
                    │  执行器指令 (模拟) │ 时序存储     │
                    └──────────────────────────────────┘
```

### 2.2 开源框架选型

| 组件 | 选型 | 理由 |
|------|------|------|
| Agent 编排 | **LangGraph** | 有向图架构，精确控制分支/并行/人机交互；状态持久化；故障恢复 |
| Agent 间通信 | **A2A 协议** | Google+Linux Foundation 主导，标准化 Agent 发现/任务委托/生命周期管理 |
| 工具暴露 | **MCP v2 协议** | Anthropic 主导的事实标准，Agent→Tool 的 "USB-C 接口" |
| LLM 后端 | **Claude Sonnet 4.5** | 通过 Anthropic API 调用，兼容 MCP 原生 |
| 数值计算 | **SciPy / NumPy** | Python 科学计算标准库 |
| 控制系统 | **python-control** | 开源控制系统工具箱 |
| 优化求解 | **PuLP / scipy.optimize** | 线性规划 + 非线性优化 |
| 时序数据 | **SQLite + Pandas** | 轻量级，MVP 阶段足够 |
| 可视化 | **Matplotlib / Plotly** | 科学绘图 + 交互式图表 |

### 2.3 目录结构

```
hydroos-agent/
├── CLAUDE.md                    # 本文件（Claude Code 项目提示词）
├── pyproject.toml               # Python 项目配置
├── README.md                    # 项目说明
│
├── core/                        # 固定工作流层——核心计算模块
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
│   │   ├── odd_definition.py    #   ODD 边界定义（水位上下限/流量/水质）
│   │   ├── odd_monitor.py       #   ODD 实时监测
│   │   └── mrc_handler.py       #   最小风险条件处理
│   ├── evaluation/              # 性能评价
│   │   ├── metrics.py           #   RMSE/MAE/NSE/响应时间等指标
│   │   └── wnal_assessor.py     #   WNAL 等级评估
│   └── design/                  # 优化设计
│       ├── sizing.py            #   水箱尺寸优化
│       └── sensitivity.py       #   敏感性分析
│
├── mcp_servers/                 # MCP 工具服务器——将 core 暴露为 MCP 接口
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
├── agents/                      # 灵活智能层——LangGraph Agent 定义
│   ├── __init__.py
│   ├── orchestrator.py          # 主编排 Agent（意图路由 + 工具选择）
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
├── workflows/                   # 固定工作流定义
│   ├── __init__.py
│   ├── sim_to_control.py        # 工作流：仿真→辨识→控制器设计→闭环验证
│   ├── data_to_predict.py       # 工作流：数据清洗→特征工程→预测→评价
│   ├── odd_assessment.py        # 工作流：ODD定义→仿真扫描→边界标定→报告
│   └── full_lifecycle.py        # 工作流：全生命周期闭环演示
│
├── data/                        # 数据目录
│   ├── tank_config.json         # 水箱参数配置
│   ├── sample_timeseries.csv    # 示例时序数据
│   └── odd_specs.json           # ODD 规格定义
│
├── tests/                       # 测试
│   ├── test_simulation.py
│   ├── test_control.py
│   ├── test_odd.py
│   └── test_mcp_servers.py
│
└── docs/                        # 文档
    ├── architecture.md          # 架构设计文档
    ├── mcp_api_reference.md     # MCP 接口文档
    └── user_guide.md            # 用户指南
```

---

## 三、核心模块详细设计（固定工作流层）

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

## 四、智能层详细设计（灵活 AI 层）

### 4.1 Orchestrator Agent（主编排）

**职责**：理解用户自然语言请求，路由到合适的工作流或 Agent 组合

**意图分类**：

| 用户说的话 | 路由 | 工具组合 |
|-----------|------|---------|
| "仿真一下水箱在入流阶跃下的响应" | 直接调用 | simulation |
| "帮我辨识水箱参数" | 直接调用 | identification |
| "清洗一下这组数据" | 直接调用 | dataclean |
| "设计一个PID控制器让水位稳定在1米" | 工作流 | simulation → identification → control → evaluation |
| "评估当前系统的ODD" | 工作流 | simulation(扫描) → odd → evaluation → report |
| "比较PID和MPC哪个控制效果更好" | 分析Agent | control(PID) + control(MPC) + evaluation + report(对比图) |
| "优化水箱尺寸使造价最低" | 设计Agent | design + simulation(验证) + evaluation |
| "帮我出一份系统性能报告" | 报告Agent | 全链路 → report |
| "当前水位安全吗" | 安全Agent | odd(check) → 判断 → 建议 |

**LangGraph 状态图**：

```
START → intent_classify
  ├── direct_tool_call → execute_tool → format_result → END
  ├── fixed_workflow → load_workflow → execute_steps → evaluate → END
  ├── flexible_analysis → planning_agent → [临时生成代码] → execute → END
  └── report_request → gather_data → report_agent → END

每个节点均可触发 safety_agent 进行 ODD 校验
```

### 4.2 Planning Agent（规划）

**职责**：将复杂请求拆解为子任务序列

**输入**：用户意图 + 当前系统状态
**输出**：任务DAG（有向无环图），每个节点标注所需工具和参数

### 4.3 Analysis Agent（分析）

**职责**：灵活组装分析能力，必要时**临时生成** Python 脚本

**关键能力**：
- 方案比选（A vs B，用统一指标评价）
- 敏感性分析（自动生成参数扫描代码）
- 优化求解（根据用户约束临时构建优化问题）
- 数据可视化（生成 matplotlib/plotly 代码）

**这是"灵活层"的核心体现**：核心工具不变，但分析方式可以千变万化。

### 4.4 Report Agent（报告）

**职责**：汇总分析结果，生成结构化报告

**输出格式**：Markdown / HTML / Word（python-docx）

### 4.5 Safety Agent（安全）

**职责**：全程守护 ODD 边界

**工作模式**：
- 被动模式：被 Orchestrator 调用，校验某次操作是否安全
- 主动模式：在仿真/控制过程中持续监测，发现越界立即中断并报告

---

## 五、开发计划（分阶段）

### Phase 1：核心模块 + 单元测试（Week 1-2）

```
目标：core/ 目录下所有模块可独立运行并通过测试
优先级：simulation > control > odd > identification > evaluation > dataclean > prediction > scheduling > design
每个模块必须：
  - 纯 Python 实现，无 LLM 依赖
  - 完整 docstring（中英双语）
  - pytest 测试覆盖率 ≥ 80%
  - 输入/输出类型用 Pydantic BaseModel 定义
```

### Phase 2：MCP Server 封装（Week 3）

```
目标：每个 core 模块封装为 MCP Server
技术：FastMCP (Python) 
每个 Server 必须：
  - 暴露 ≥ 1 个 tool
  - 定义清晰的 JSON Schema 输入/输出
  - 支持 stdio 和 SSE 两种传输方式
  - 包含 Agent Card（JSON 格式的能力描述）
```

### Phase 3：LangGraph Agent 编排（Week 4-5）

```
目标：Orchestrator + 4 个子 Agent 协同工作
技术：LangGraph + Claude Sonnet 4.5 API
关键功能：
  - 自然语言 → 意图分类 → 工具路由
  - 固定工作流执行（sim_to_control 等）
  - 临时脚本生成与执行（Analysis Agent）
  - ODD 安全守护（Safety Agent 全程在线）
```

### Phase 4：集成演示 + 文档（Week 6）

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

## 六、编码规范

### 6.1 Python 规范
- Python ≥ 3.11
- 类型注解全覆盖（Pydantic v2 用于数据模型）
- 格式化：ruff format
- 检查：ruff check
- 测试：pytest + pytest-asyncio

### 6.2 命名规范
- 模块：snake_case
- 类：PascalCase
- MCP Tool：snake_case 动词开头（simulate_tank, clean_timeseries）
- Agent：PascalCase + Agent 后缀（OrchestratorAgent, SafetyAgent）

### 6.3 文档规范
- 每个公开函数/类必须有 docstring
- docstring 格式：Google style
- 关键参数标注物理单位

### 6.4 Git 规范
- 分支：main (稳定) / dev (开发) / feature/xxx
- Commit 消息：`[模块] 描述`，如 `[simulation] 实现水箱RK4求解器`

---

## 七、CHS 术语对照表（开发时保持一致）

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

## 八、扩展路线图（MVP 之后）

### 8.1 模型扩展
- 水箱 → 串联水箱 → 明渠（圣维南方程）→ 管网（水锤方程）→ 梯级水电站
- 每种新模型只需：实现 core 模块 + 封装 MCP Server，Agent 层无需修改

### 8.2 工具扩展
- 接入 OpenModelica（Modelica 仿真）
- 接入 EPA-SWMM / EPANET（管网仿真）
- 接入 GPU 并行求解器

### 8.3 AI 能力扩展
- 接入瀚铎水网大模型（替代通用 LLM，领域知识更强）
- 知识图谱集成（水利规范、设计标准）
- 强化学习控制策略

### 8.4 部署扩展
- Docker 容器化
- Kubernetes 编排
- Web UI（Streamlit → React）
- 与实际 SCADA 系统对接

---

## 九、关键参考

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

## 十、注意事项

1. **核心模块必须可独立运行**：不依赖 LLM，纯数值计算，确保确定性和可测试性
2. **MCP 接口设计要通用**：输入/输出用 JSON Schema 严格定义，为将来替换模型预留空间
3. **安全第一**：任何涉及控制指令下达的操作，必须经过 ODD 校验
4. **不要过早优化**：MVP 阶段用最简单的实现（如欧拉法而非高阶求解器），跑通链路优先
5. **中英双语注释**：代码注释和文档保持中英双语，方便国际化推广
