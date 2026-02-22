# OpenClaw Agent Core (OCAC)
# 类EvoAgentX/OpenManus架构的自主Agent系统

## 架构概述

```
┌─────────────────────────────────────────────────────────────┐
│                    OpenClaw Agent Core                      │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Workflow   │  │    Task      │  │   Optimizer  │     │
│  │   Engine     │──│  Decomposer  │──│              │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                   │                │             │
│         ▼                   ▼                ▼             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Parallel Executor                        │  │
│  │         (sessions_spawn + cron)                       │  │
│  └──────────────────────────────────────────────────────┘  │
│         │                   │                │             │
│         ▼                   ▼                ▼             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Evaluator   │  │    Memory    │  │   Output     │     │
│  │              │  │   Manager    │  │   Generator  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## 核心组件

### 1. Workflow Engine（工作流引擎）
- 自动解析任务描述
- 生成DAG（有向无环图）工作流
- 管理任务依赖关系

### 2. Task Decomposer（任务分解器）
- 将复杂任务分解为可执行子任务
- 估计每个子任务的资源需求
- 分配优先级

### 3. Parallel Executor（并行执行器）
- 使用sessions_spawn并行执行子任务
- 监控执行进度
- 处理失败重试

### 4. Evaluator（评估器）
- 评估子任务输出质量
- 计算性能指标
- 生成反馈信号

### 5. Optimizer（优化器）
- 基于反馈优化工作流
- 调整任务参数
- 迭代改进

### 6. Memory Manager（记忆管理器）
- 存储执行历史
- 检索相关经验
- 支持知识复用

## 工作流程

```
用户输入任务
    ↓
[Task Decomposer] → 分解为子任务列表
    ↓
[Workflow Engine] → 构建执行DAG
    ↓
[Parallel Executor] → 并行执行（sessions_spawn）
    ↓
[Evaluator] → 评估结果质量
    ↓
质量达标?
    ↓ 否
[Optimizer] → 调整参数/重试
    ↓
[Memory Manager] → 保存经验
    ↓
[Output Generator] → 整合输出
    ↓
返回结果给用户
```

## 使用示例

```bash
# 启动Agent执行复杂任务
python3 agent_core.py --task "生成25万字学术报告" --parallel 10

# 查看执行状态
python3 agent_core.py --status

# 查看历史记录
python3 agent_core.py --history
```

## 配置说明

配置文件：`config/agent_config.yaml`

```yaml
# 执行配置
execution:
  max_parallel: 10          # 最大并行子任务数
  timeout: 1800             # 子任务超时时间（秒）
  retry_count: 3            # 失败重试次数

# 优化配置
optimization:
  enable: true              # 启用优化
  iterations: 5             # 最大优化迭代次数
  threshold: 0.8            # 质量达标阈值

# 记忆配置
memory:
  storage: github           # 存储方式：github/local
  repo: books               # GitHub仓库名
  path: agent-memory/       # 存储路径

# 评估配置
evaluation:
  metrics:                  # 评估指标
    - accuracy
    - completeness
    - consistency
```

## 与EvoAgentX/OpenManus对比

| 功能 | EvoAgentX | OpenManus | OCAC (本系统) |
|------|-----------|-----------|---------------|
| 工作流生成 | ✅ | ✅ | ✅ |
| 并行执行 | ✅ | ✅ | ✅ (sessions_spawn) |
| 动态优化 | ✅ | ✅ | ✅ |
| 评估反馈 | ✅ | ✅ | ✅ |
| 记忆管理 | ✅ | ✅ | ✅ (GitHub存储) |
| 自进化 | ✅ | ⚠️ | ⚠️ (半自动) |
| 多智能体 | ✅ | ✅ | ✅ (子任务Agent) |
| 部署难度 | 高 | 中 | 低 (纯Python) |

## 优势

1. **无需额外部署**：基于现有OpenClaw工具链
2. **GitHub集成**：天然支持版本控制和协作
3. **灵活扩展**：易于添加新的Agent类型
4. **成本可控**：复用现有计算资源

## 下一步开发计划

- [ ] 实现Workflow Engine核心
- [ ] 实现Task Decomposer
- [ ] 集成Parallel Executor
- [ ] 实现Evaluator
- [ ] 实现Optimizer
- [ ] 完善Memory Manager
- [ ] 添加Web UI监控界面
