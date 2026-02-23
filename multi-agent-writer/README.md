# HydroScribe — CHS 多智能体协同写作助手

> 基于 OpenManus + OpenClaw 架构，融合 9 大写作技能，支持阿里云百炼/OpenAI/Anthropic/本地模型的多智能体学术写作系统

## 架构概览

```
┌─────────────────────────────────────────────────────┐
│          HydroScribe Dashboard (Web UI)              │
│  仪表盘 | 书架 | 写作面板 | 评审面板 | 事件流         │
└──────────────────────┬──────────────────────────────┘
                       │ WebSocket
┌──────────────────────┼──────────────────────────────┐
│           FastAPI + EventBus + Config                │
├──────────────────────┼──────────────────────────────┤
│  Orchestrator (Plan → Execute → Reflect)             │
│  ├ specialist 模式 (按技能路由)                       │
│  └ master_slave 模式 (多章并行)                       │
├──────────────────────┼──────────────────────────────┤
│  9 Writer + 28 Reviewer + 3 Utility Agents           │
│  (继承 OpenManus BaseAgent)                          │
├──────────────────────┼──────────────────────────────┤
│  LLM Provider Layer                                  │
│  百炼 | OpenAI | Anthropic | Local (Ollama/vLLM)     │
├──────────────────────┼──────────────────────────────┤
│  Shared Memory (Git + JSON + 术语库)                  │
│  Context Manager (三层防御: Token/压缩/分块)          │
└─────────────────────────────────────────────────────┘
         ↕ OpenClaw Skill Wrapper (可选)
┌─────────────────────────────────────────────────────┐
│  OpenClaw Gateway → 外部调度集成                      │
└─────────────────────────────────────────────────────┘
```

## 9 大写作技能 × 40 个 Agent

| 代号 | 文体 | Writer Agent | Reviewer Agents | 权重分配 |
|------|------|-------------|----------------|---------|
| BK | 书稿/教材 | `writer-bk` | 教师 + 专家 + 工程师 + 国际读者 | 30/30/20/20 |
| SCI | SCI论文 | `writer-sci` | Reviewer A + B + C | 40/30/30 |
| CN | 中文核心 | `writer-cn` | 审稿人 A + B + C | 40/30/30 |
| PAT | 发明专利 | `writer-pat` | 审查员 + 代理人 + 技术专家 | 40/30/30 |
| RPT | 技术报告 | `writer-rpt` | 技术审查 + 管理审查 | 60/40 |
| STD-CN | 国内标准 | `writer-std-cn` | 标准化 + 技术 + 实施方 | 40/30/30 |
| STD-INT | 国际标准 | `writer-std-int` | ISO + 水利 + 工业界 | 35/35/30 |
| WX | 微信公众号 | `writer-wx` | 读者 + 编辑 + 领域专家 | 40/30/30 |
| PPT | 演示文稿 | `writer-ppt` | 观众 + 设计 + 内容 | 35/30/35 |

**辅助 Agent**: GlossaryGuard (术语守卫) + ConsistencyChecker (一致性) + ReferenceManager (参考文献)

---

## 快速开始

### 方式一：pip 安装 (推荐)

```bash
# 1. 克隆仓库
git clone <your-repo-url> && cd multi-agent-writer

# 2. 安装
pip install -e ".[dev]"          # 核心 + 开发依赖
# 或: pip install -e ".[dev,bailian]"  # 含百炼 SDK

# 3. 初始化 (交互式向导)
hydroscribe init

# 4. 环境检查
hydroscribe doctor

# 5. 启动服务
hydroscribe serve
# 访问 http://localhost:8000
```

### 方式二：Docker 部署

```bash
# 1. 配置环境变量
cp .env.example .env
# 编辑 .env，设置 DASHSCOPE_API_KEY 或 OPENAI_API_KEY

# 2. 构建并启动
docker-compose up -d

# 3. 查看日志
docker-compose logs -f hydroscribe

# 访问 http://localhost:8000
```

### 方式三：阿里云 ECS 部署

```bash
# 1. 在 ECS 上克隆仓库
git clone <your-repo-url> && cd multi-agent-writer

# 2. 配置百炼 API Key
export DASHSCOPE_API_KEY="sk-your-key-here"

# 3. Docker 部署
docker-compose up -d

# 4. 验证
curl http://localhost:8000/api/status

# 提示: 阿里云 ECS 到百炼 API 为内网访问，延迟极低 (<10ms)
# 建议 ECS 区域选择与百炼相同的地域 (如 cn-hangzhou)
```

---

## CLI 命令参考

```bash
hydroscribe init              # 交互式初始化向导 (首次使用)
hydroscribe serve             # 启动 Web 服务器 + 仪表盘
hydroscribe serve --reload    # 开发模式 (热重载)
hydroscribe start T1-CN       # 开始写作
hydroscribe start T2a --chapters ch01,ch02,ch03  # 多章并行
hydroscribe status            # 查看所有书目进度
hydroscribe check file.md     # 四维质量检查 (术语/一致性/参考文献/结构)
hydroscribe agents            # 列出所有 Agent (40个)
hydroscribe doctor            # 环境自诊断
hydroscribe config            # 显示当前配置 (脱敏)
```

### Makefile 快捷命令

```bash
make help           # 查看所有命令
make install        # pip install -e .
make install-dev    # pip install -e ".[dev]"
make init           # 交互式初始化
make serve          # 启动服务
make serve-dev      # 开发模式 (热重载)
make start BOOK=T1-CN                       # 启动写作
make start BOOK=T2a CHAPTERS=ch01,ch02      # 多章并行
make test           # 运行测试
make test-cov       # 测试 + 覆盖率
make check FILE=books/T2a/ch01.md           # 质量检查
make doctor         # 环境自诊断
make docker-build   # 构建 Docker 镜像
make docker-up      # 启动容器
make docker-down    # 停止容器
make clean          # 清理缓存
```

---

## 配置

### 配置文件

运行 `hydroscribe init` 自动生成 `config/config.toml`:

```toml
books_root = "/home/user/books"
log_level = "info"

[server]
host = "0.0.0.0"
port = 8000

[orchestrator]
gate_mode = "auto"              # auto / human / hybrid
coordination_mode = "specialist" # specialist / master_slave
max_concurrent_writers = 3

[llm]
provider = "alibaba_bailian"    # alibaba_bailian / openai / anthropic / local
model = "qwen-plus"
api_key = "sk-..."
max_tokens = 4096
temperature = 0.3
fallback_model = "qwen-turbo"

# 角色特定配置 (可选，覆盖默认)
# [llm.writer]
# model = "qwen-max"
# [llm.reviewer]
# provider = "anthropic"
# model = "claude-sonnet-4-20250514"
```

### 环境变量优先级

环境变量 > config.toml > 默认值

| 环境变量 | 说明 |
|---------|------|
| `DASHSCOPE_API_KEY` | 百炼 API Key (自动设置 provider=alibaba_bailian) |
| `OPENAI_API_KEY` | OpenAI API Key |
| `ANTHROPIC_API_KEY` | Anthropic API Key |
| `HYDROSCRIBE_LLM_PROVIDER` | LLM 提供商 |
| `HYDROSCRIBE_LLM_MODEL` | LLM 模型名称 |
| `HYDROSCRIBE_BOOKS_ROOT` | 书稿数据根目录 |
| `HYDROSCRIBE_GATE_MODE` | 门控模式 (auto/human/hybrid) |

### LLM 提供商对比

| 提供商 | 推荐模型 | 特点 | 适用场景 |
|-------|---------|------|---------|
| 阿里云百炼 | qwen-plus / qwen-max | 国内低延迟、中文优化、成本低 | 国内服务器部署 |
| OpenAI | gpt-4o / gpt-4o-mini | 英文写作优秀 | 英文书稿 (T1-EN 等) |
| Anthropic | claude-sonnet-4-20250514 | 长文本、推理能力强 | 复杂推导章节 |
| Local | qwen2.5:14b (Ollama) | 无 API 费用、离线可用 | 开发测试 |

---

## 目录结构

```
multi-agent-writer/
├── DESIGN.md                   设计方案
├── README.md                   本文件
├── Makefile                    快捷命令
├── Dockerfile                  容器化构建
├── docker-compose.yml          编排配置
├── .env.example                环境变量模板
├── pyproject.toml              Python 打包配置
├── main.py                     兼容入口 (推荐用 hydroscribe serve)
├── config/
│   └── config.toml             配置文件 (hydroscribe init 生成)
├── hydroscribe/                核心代码
│   ├── __init__.py             版本信息
│   ├── cli.py                  CLI 入口 (init/serve/start/doctor...)
│   ├── schema.py               数据模型 (事件/任务/评审/技能)
│   ├── engine/
│   │   ├── event_bus.py        事件总线 + WebSocket 推送
│   │   ├── orchestrator.py     多智能体编排器
│   │   ├── context_manager.py  三层上下文管理
│   │   ├── llm_provider.py     LLM 提供商抽象层
│   │   └── config_loader.py    TOML 配置加载器
│   ├── agents/
│   │   ├── base_writer.py      Writer 基类 (继承 OpenManus)
│   │   ├── base_reviewer.py    Reviewer 基类 (加权评分)
│   │   └── writers/            9 个 Writer Agent
│   ├── tools/
│   │   └── quality_tools.py    四维质量检查工具
│   ├── prompts/
│   │   └── templates.py        Prompt 模板库
│   ├── api/
│   │   └── app.py              FastAPI 路由 + WebSocket
│   └── static/
│       └── index.html          单页面实时仪表盘
├── openclaw/                   OpenClaw 技能包装
│   └── skills/
│       └── hydroscribe_writer/
├── tests/                      测试
│   └── test_llm_provider.py
└── openmanus/                  OpenManus 源码
```

---

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/status` | 系统状态 (含 LLM 使用量) |
| GET | `/api/books` | 书目列表 |
| GET | `/api/books/{id}` | 书目详情 |
| POST | `/api/tasks/start` | 启动写作任务 |
| POST | `/api/tasks/master-slave` | 多章并行写作 |
| GET | `/api/events` | 事件历史 |
| POST | `/api/gate/{id}/approve` | 人工批准 |
| POST | `/api/gate/{id}/reject` | 人工驳回 |
| GET | `/api/llm/usage` | LLM Token 使用量统计 |
| GET | `/api/config` | 当前配置 (脱敏) |
| WS | `/ws` | 实时事件流 |

---

## 与 OpenManus / OpenClaw 的关系

**OpenManus 继承**:
- `BaseAgent` → `BaseWriterAgent` / `BaseReviewerAgent`
- `PlanningFlow` → `Orchestrator` (Plan-Execute-Reflect)
- `Memory` / `Message` / `AgentState` → 直接复用

**HydroScribe 扩展**:
- 9 种文体的专用 Writer + 28 个加权 Reviewer
- 事件总线 (EventBus) + WebSocket 实时推送
- 门控机制: 自动/人工/混合三种审批模式
- 三层上下文管理: TokenBudget / TextCompressor / ChunkWriter
- LLM 提供商抽象层 (百炼/OpenAI/Anthropic/Local)
- TOML 配置系统 (支持环境变量覆盖)

**OpenClaw 集成**:
- HydroScribe 可作为 OpenClaw Skill 被外部调度
- Shell 入口脚本 → HTTP API → 轮询完成
- 见 `openclaw/skills/hydroscribe_writer/`

---

## 开发

```bash
# 安装开发依赖
make install-dev

# 运行测试
make test

# 测试覆盖率
make test-cov

# 代码检查
make lint

# 格式化
make fmt
```

---

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| v0.3.0 | 2026-02 | LLM 提供商抽象、TOML 配置、Docker、CLI 升级、OpenClaw 集成 |
| v0.2.0 | 2026-02 | 9 Writer + 28 Reviewer + 3 Utility、四维质检、实时仪表盘 |
| v0.1.0 | 2026-02 | 基础架构: EventBus、Orchestrator、BaseAgent |
