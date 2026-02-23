# HydroScribe — CHS 多智能体协同写作助手

> 基于 OpenManus 架构，融合 9 大写作技能，带实时 UI 仪表盘的多智能体学术写作系统

## 架构概览

```
┌─────────────────────────────────────────────┐
│            HydroScribe UI (React)            │
│  仪表盘 | 书架 | 写作面板 | 评审面板 | 事件流  │
└──────────────────┬──────────────────────────┘
                   │ WebSocket
┌──────────────────┼──────────────────────────┐
│           FastAPI + EventBus                 │
├──────────────────┼──────────────────────────┤
│  Orchestrator (Plan → Execute → Reflect)     │
├──────────────────┼──────────────────────────┤
│  9 Writer Agents + N Reviewer Agents         │
│  (继承 OpenManus BaseAgent)                  │
├──────────────────┼──────────────────────────┤
│  Shared Memory (Git + JSON + 术语库)         │
└──────────────────────────────────────────────┘
```

## 9 大写作技能

| 代号 | 文体 | Writer Agent | Reviewer Agents |
|------|------|-------------|----------------|
| BK | 书稿/教材 | `writer-bk` | 教师 + 专家 + 工程师 + 国际读者 |
| SCI | SCI论文 | `writer-sci` | Reviewer A + B + C |
| CN | 中文核心 | `writer-cn` | 审稿人 A + B + C |
| PAT | 发明专利 | `writer-pat` | 审查员 + 代理人 + 技术专家 |
| RPT | 技术报告 | `writer-rpt` | 技术审查 + 管理审查 |
| STD-CN | 国内标准 | `writer-std-cn` | 标准化 + 技术 + 实施方 |
| STD-INT | 国际标准 | `writer-std-int` | ISO + 水利 + 工业界 |
| WX | 微信公众号 | `writer-wx` | 读者 + 编辑 + 领域专家 |
| PPT | 演示文稿 | `writer-ppt` | 观众 + 设计 + 内容 |

## 快速启动

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务
python main.py

# 访问
# 前端: http://localhost:8000
# API:  http://localhost:8000/docs
# WS:   ws://localhost:8000/ws

# Docker 部署
docker-compose up -d
```

## 目录结构

```
multi-agent-writer/
├── DESIGN.md              ← 完整设计方案 (10 章)
├── README.md              ← 本文件
├── main.py                ← 入口文件
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── openmanus/             ← OpenManus 源码 (git clone)
├── hydroscribe/           ← HydroScribe 核心代码
│   ├── schema.py          ← 数据模型 (事件/任务/评审)
│   ├── engine/
│   │   ├── event_bus.py   ← 事件总线 + WebSocket 推送
│   │   └── orchestrator.py← 多智能体编排器
│   ├── agents/
│   │   ├── base_writer.py ← Writer 基类 (继承 OpenManus)
│   │   ├── base_reviewer.py ← Reviewer 基类
│   │   └── writers/       ← 9 个 Writer Agent
│   ├── api/
│   │   └── app.py         ← FastAPI 路由 + WebSocket
│   └── static/
│       └── index.html     ← 单页面实时仪表盘
```

## 与 OpenManus 的关系

HydroScribe 继承了 OpenManus 的核心架构：
- `BaseAgent` → `BaseWriterAgent` / `BaseReviewerAgent`
- `PlanningFlow` → `Orchestrator` (Plan-Execute-Reflect)
- `Memory` / `Message` / `AgentState` → 直接复用

在此基础上增加了：
- **领域专业化**: 9 种文体的专用 Writer + 对应 Reviewer
- **事件总线**: Agent 间异步通信 + WebSocket 实时推送
- **门控机制**: 自动/人工/混合三种审批模式
- **一致性保障**: 术语库 + 跨书引用图谱
- **实时 UI**: 仪表盘 + 写作面板 + 评审面板

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/status` | 系统状态 |
| GET | `/api/books` | 书目列表 |
| GET | `/api/books/{id}` | 书目详情 |
| POST | `/api/tasks/start` | 启动写作任务 |
| GET | `/api/events` | 事件历史 |
| POST | `/api/gate/{id}/approve` | 人工批准 |
| POST | `/api/gate/{id}/reject` | 人工驳回 |
| WS | `/ws` | 实时事件流 |
