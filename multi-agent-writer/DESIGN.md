# CHS 多智能体协同写作助手 — 系统设计方案

> **版本**: 1.0
> **日期**: 2026-02-23
> **代号**: HydroScribe (水笔)
> **定位**: 参考 Manus/OpenManus 架构，基于 9 大协作 Skill，构建带实时 UI 的多智能体写作系统

---

## 0. 设计目标

### 0.1 核心问题

当前 OCAC 原型存在的不足：

| 问题 | 现状 | 目标 |
|------|------|------|
| 无真正并行 | `subprocess` 模拟，未实际调用 LLM | 真正的多 Agent 并行写作 |
| 无实时 UI | 仅有简陋的 HTTP 轮询页面 | WebSocket 实时推送 + 可视化仪表盘 |
| Agent 职责模糊 | 单一 Agent 串行执行所有步骤 | 9 种 Writer + 对应 Reviewer + Orchestrator 分工明确 |
| 无记忆共享 | 每次执行独立，无跨会话记忆 | 共享术语库 / 一致性检查 / 跨书引用图谱 |
| 无人机协同 | 纯自动或纯手动 | 人在环（Human-in-the-Loop）审批门控 |

### 0.2 设计原则

1. **Agent 即角色** — 每个 Agent 对应一个明确的人类角色（作者/教师/专家/工程师/国际读者）
2. **DAG 即工作流** — 任务依赖关系用有向无环图表达，支持并行分支
3. **事件即通信** — Agent 间通过事件总线（Event Bus）异步通信
4. **UI 即窗口** — 所有 Agent 状态实时映射到前端仪表盘
5. **Git 即版本** — 每个写作产物自动版本控制

---

## 1. 系统架构总览

```
┌─────────────────────────────────────────────────────────────────────┐
│                        HydroScribe UI (React)                       │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │ 仪表盘   │ │ 书目总览 │ │ 写作面板 │ │ 评审面板 │ │ 一致性   │ │
│  │Dashboard │ │BookShelf │ │ Editor   │ │ Review   │ │Checker   │ │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ │
│       └─────────────┴────────────┴─────────────┴────────────┘       │
│                              WebSocket                               │
└──────────────────────────────────┬──────────────────────────────────┘
                                   │
┌──────────────────────────────────┼──────────────────────────────────┐
│                          API Gateway (FastAPI)                       │
│  /api/tasks  /api/agents  /api/books  /api/ws  /api/reviews         │
└──────────────────────────────────┬──────────────────────────────────┘
                                   │
┌──────────────────────────────────┼──────────────────────────────────┐
│                      Orchestrator (编排层)                           │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐        │
│  │  Task Planner  │  │  DAG Scheduler │  │  Gate Keeper   │        │
│  │  任务规划器    │  │  DAG 调度器    │  │  门控审批器    │        │
│  └───────┬────────┘  └───────┬────────┘  └───────┬────────┘        │
│          └───────────────────┼───────────────────┘                  │
│                              │                                      │
│  ┌───────────────────────────┼──────────────────────────────────┐   │
│  │                    Event Bus (事件总线)                        │   │
│  │  topic: writing.started / writing.chunk / review.score /     │   │
│  │         revision.needed / chapter.completed / gate.approve   │   │
│  └───────────────────────────┬──────────────────────────────────┘   │
└──────────────────────────────┼──────────────────────────────────────┘
                               │
┌──────────────────────────────┼──────────────────────────────────────┐
│                       Agent Pool (智能体池)                          │
│                                                                      │
│  ┌─── Writer Agents (写作智能体) ───────────────────────────────┐   │
│  │ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐  │   │
│  │ │ BK  │ │ SCI │ │ CN  │ │ PAT │ │ RPT │ │ WX  │ │ PPT │  │   │
│  │ │书稿 │ │论文 │ │中文 │ │专利 │ │报告 │ │公众号│ │PPT │  │   │
│  │ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘  │   │
│  │ ┌─────────┐ ┌─────────┐                                    │   │
│  │ │ STD-CN  │ │ STD-INT │                                    │   │
│  │ │国内标准 │ │国际标准 │                                    │   │
│  │ └─────────┘ └─────────┘                                    │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌─── Reviewer Agents (评审智能体) ────────────────────────────┐   │
│  │  每个 Writer 对应 2-4 个 Reviewer（详见§2.3）                │   │
│  │  BK: 教师 + 专家 + 工程师 + 国际读者                        │   │
│  │  SCI: Reviewer A + B + C                                    │   │
│  │  CN: 审稿人 A + B + C                                       │   │
│  │  PAT: 审查员 + 代理人 + 技术专家                            │   │
│  │  ...                                                        │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌─── Utility Agents (工具智能体) ─────────────────────────────┐   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │   │
│  │  │Glossary  │ │Consistency│ │Reference │ │ Figure   │       │   │
│  │  │术语守卫  │ │一致性检查 │ │文献管理  │ │ 图表生成 │       │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │   │
│  └─────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────┘
                               │
┌──────────────────────────────┼──────────────────────────────────────┐
│                       Shared Memory (共享记忆层)                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐              │
│  │ Git Repo │ │ Progress │ │ Glossary │ │ Cross-Ref│              │
│  │ 版本控制 │ │ JSON进度 │ │ 术语库   │ │ 引用图谱 │              │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘              │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 2. Agent 设计详解

### 2.1 Orchestrator — 编排层

Orchestrator 是整个系统的大脑，不直接写作，只负责规划、调度和门控。参考 Manus 的 Planning → Execution → Reflection 三阶段循环。

```
┌────────────────────────────────────────────────┐
│               Orchestrator 生命周期             │
│                                                │
│   ① Plan (规划)                                │
│      ├─ 解析用户指令 ("开始BKT2a")             │
│      ├─ 读取 CLAUDE.md §2 获取书目规格          │
│      ├─ 读取 progress/BK[X].json 确认进度       │
│      └─ 生成 DAG 工作流                         │
│                                                │
│   ② Execute (执行)                             │
│      ├─ 按 DAG 拓扑序调度 Agent                 │
│      ├─ 并行分派无依赖的子任务                   │
│      ├─ 监听事件总线上的进度和产出               │
│      └─ 流式推送状态到 UI                       │
│                                                │
│   ③ Reflect (反思)                             │
│      ├─ 汇总所有 Reviewer 评分                  │
│      ├─ 决定: 通过 / 修改 / 人工审批             │
│      ├─ 更新 progress JSON                      │
│      └─ 决定下一步: 继续下一章 or 修改当前章      │
└────────────────────────────────────────────────┘
```

#### Task Planner（任务规划器）

```python
# 核心数据结构
@dataclass
class WritingTask:
    book_id: str          # "T2a"
    chapter_id: str       # "ch07"
    skill_type: str       # "BK"
    spec: ChapterSpec     # 从 CLAUDE.md 解析的章节规格
    dependencies: list    # ["ch06"] 前序章节
    target_words: int     # 40000
    reviewers: list       # ["instructor", "expert", "engineer", "international"]
    max_iterations: int   # 6
    gate_type: str        # "auto" | "human"  门控类型
```

#### DAG Scheduler（DAG 调度器）

将一个章节的完整写作流程编排为 DAG：

```
                    ┌──────────┐
                    │ 加载规格  │
                    └────┬─────┘
                         │
                    ┌────┴─────┐
                    │ 读前序章 │
                    └────┬─────┘
                         │
                    ┌────┴─────┐
                    │ 撰写初稿 │  ← Writer Agent (BK)
                    └────┬─────┘
                         │
              ┌──────────┼──────────┐
              │          │          │
         ┌────┴────┐┌───┴────┐┌───┴────┐
         │术语检查 ││引用检查││一致性  │  ← Utility Agents (并行)
         └────┬────┘└───┬────┘└───┬────┘
              │          │          │
              └──────────┼──────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
    ┌────┴────┐    ┌────┴────┐    ┌────┴────┐
    │教师评审 │    │专家评审 │    │工程师   │  ← Reviewer Agents (并行)
    └────┬────┘    └────┬────┘    │评审     │
         │               │        └────┬────┘
         └───────────────┼─────────────┘
                         │
                    ┌────┴─────┐
                    │ 汇总评审  │
                    │ 决定门控  │  ← Orchestrator
                    └────┬─────┘
                    ┌────┴─────┐
                ┌───┤ 达标？   ├───┐
                │   └──────────┘   │
             否 │                  │ 是
                ▼                  ▼
          ┌──────────┐      ┌──────────┐
          │ 修改迭代  │      │ 保存终稿  │
          │ → 回到   │      │ 更新进度  │
          │   撰写   │      │ git commit│
          └──────────┘      └──────────┘
```

#### Gate Keeper（门控审批器）

支持三种门控模式：

| 模式 | 触发条件 | 行为 |
|------|---------|------|
| `auto` | 评分 ≥ 阈值且无 🔴 | 自动通过，继续下一章 |
| `human` | 每章完成后 | 暂停，推送通知，等待用户在 UI 上审批 |
| `hybrid` | 首章 human，后续 auto | 首章人工确认风格基调后，后续自动 |

### 2.2 Writer Agents — 9 大写作智能体

每个 Writer Agent 是一个**专业化的写作者**，内置对应文体的提示词模板、写作技法和金标准参考。

```
┌────────────────────────────────────────┐
│         Writer Agent 内部结构           │
│                                        │
│  ┌──────────────────────────────────┐  │
│  │ System Prompt                    │  │
│  │ ├─ SKILL.md 对应文体段落          │  │
│  │ ├─ writing_craft_guide.md        │  │
│  │ ├─ gold_standard_fragments.md    │  │
│  │ └─ 章节规格 (字数/大纲/风格)      │  │
│  └──────────────────────────────────┘  │
│                                        │
│  ┌──────────────────────────────────┐  │
│  │ Context Window                   │  │
│  │ ├─ 前序章节末尾 500 字            │  │
│  │ ├─ 术语表 (glossary_cn.md)       │  │
│  │ ├─ 符号表 (symbols.md)           │  │
│  │ └─ 上轮评审意见 (如修改轮)        │  │
│  └──────────────────────────────────┘  │
│                                        │
│  ┌──────────────────────────────────┐  │
│  │ Output                           │  │
│  │ ├─ 章节 Markdown 正文             │  │
│  │ ├─ 图表描述占位符                 │  │
│  │ └─ 元数据 (字数/概念数/公式数)     │  │
│  └──────────────────────────────────┘  │
└────────────────────────────────────────┘
```

**9 大 Writer Agent 配置：**

| Agent ID | 文体 | System Prompt 来源 | 特殊能力 |
|----------|------|-------------------|---------|
| `writer-bk` | 书稿/教材 | SKILL.md §2.4 + CLAUDE.md §8 | 学习目标/例题/习题生成 |
| `writer-sci` | SCI 论文 | SKILL.md §2.1 | LaTeX 公式 / 英文学术写作 |
| `writer-cn` | 中文核心 | SKILL.md §2.2 | 中文学术规范 / GB/T 7714 |
| `writer-pat` | 发明专利 | SKILL.md §2.3 | 权利要求书 / 说明书撰写 |
| `writer-rpt` | 技术报告 | SKILL.md §2.5 | 数据表格 / 技术方案 |
| `writer-std-cn` | 国内标准 | SKILL.md §2.6 | GB/T 1.1 条文格式 |
| `writer-std-int` | 国际标准 | SKILL.md §2.7 | ISO Directives Part 2 |
| `writer-wx` | 微信公众号 | SKILL.md §2.8 | 手机排版 / 传播力优化 |
| `writer-ppt` | 演示文稿 | SKILL.md §2.9 | 幻灯片结构 / 视觉设计 |

### 2.3 Reviewer Agents — 评审智能体矩阵

```
              Writer                Reviewers
            ┌────────┐
            │writer-bk│──→ 教师 + 专家 + 工程师 + 国际读者 (4角色)
            ├────────┤
            │writer-sci│──→ Reviewer A + B + C (3角色)
            ├────────┤
            │writer-cn│──→ 审稿人 A + B + C (3角色)
            ├────────┤
            │writer-pat│──→ 审查员 + 代理人 + 技术专家 (3角色)
            ├────────┤
            │writer-rpt│──→ 技术审查 + 管理审查 (2角色)
            ├────────┤
            │writer-std-cn│──→ 标准化专家 + 技术专家 + 实施方 (3角色)
            ├────────┤
            │writer-std-int│──→ ISO标准化 + 国际水利 + 工业界 (3角色)
            ├────────┤
            │writer-wx│──→ 读者 + 编辑 + 领域专家 (3角色)
            ├────────┤
            │writer-ppt│──→ 观众 + 设计 + 内容 (3角色)
            └────────┘
```

**关键设计：Reviewer 并行执行**

所有 Reviewer Agent 对同一份初稿**并行**评审，互不干扰。这是与当前串行评审最大的架构差异，可将评审耗时从 O(n) 降至 O(1)。

### 2.4 Utility Agents — 工具智能体

| Agent ID | 职责 | 触发时机 |
|----------|------|---------|
| `glossary-guard` | 术语一致性检查 | 每章写完后自动触发 |
| `consistency-checker` | 跨书内容一致性检查 | 涉及共享内容时触发（八原理/WNAL/Saint-Venant等） |
| `reference-manager` | 文献格式检查 + 自引率计算 | 每章写完后自动触发 |
| `figure-generator` | 图表描述 → 图表生成 | 终稿确认后触发 |

---

## 3. 事件总线设计

Agent 间通过 Event Bus 异步通信，所有事件同时推送到 UI 用于实时展示。

### 3.1 事件类型

```python
class EventType(Enum):
    # 任务生命周期
    TASK_CREATED    = "task.created"       # Orchestrator 创建任务
    TASK_STARTED    = "task.started"       # Agent 开始执行
    TASK_COMPLETED  = "task.completed"     # Agent 完成任务
    TASK_FAILED     = "task.failed"        # Agent 执行失败

    # 写作过程
    WRITING_STARTED = "writing.started"    # Writer 开始写作
    WRITING_CHUNK   = "writing.chunk"      # Writer 产出一个片段（流式）
    WRITING_DONE    = "writing.done"       # Writer 初稿完成

    # 评审过程
    REVIEW_STARTED  = "review.started"     # Reviewer 开始评审
    REVIEW_SCORE    = "review.score"       # Reviewer 给出评分
    REVIEW_DONE     = "review.done"        # 所有 Reviewer 评审完成

    # 质量检查
    CHECK_GLOSSARY  = "check.glossary"     # 术语检查结果
    CHECK_CONSISTENCY = "check.consistency" # 一致性检查结果
    CHECK_REFERENCE = "check.reference"    # 文献检查结果

    # 门控
    GATE_WAITING    = "gate.waiting"       # 等待人工审批
    GATE_APPROVED   = "gate.approved"      # 审批通过
    GATE_REJECTED   = "gate.rejected"      # 审批驳回

    # 迭代
    REVISION_NEEDED = "revision.needed"    # 需要修改
    REVISION_ROUND  = "revision.round"     # 第 N 轮修改

    # 里程碑
    CHAPTER_COMPLETED = "chapter.completed" # 一章完成
    BOOK_COMPLETED    = "book.completed"    # 一本书完成
```

### 3.2 事件数据结构

```python
@dataclass
class Event:
    id: str                  # UUID
    type: EventType
    timestamp: datetime
    source_agent: str        # 发出事件的 Agent ID
    target_agent: str | None # 目标 Agent（None = 广播）
    payload: dict            # 事件数据
    book_id: str             # "T2a"
    chapter_id: str          # "ch07"

# 示例事件
Event(
    type=EventType.REVIEW_SCORE,
    source_agent="reviewer-instructor",
    payload={
        "scores": {"coverage": 4, "difficulty_gradient": 3, "example_quality": 5},
        "overall": 8.2,
        "issues_red": [],
        "issues_yellow": ["建议补充MPC约束处理例题"],
        "issues_green": ["可增加国际案例对比"]
    },
    book_id="T2a",
    chapter_id="ch07"
)
```

---

## 4. UI 设计

### 4.1 技术栈

| 层 | 技术选型 | 理由 |
|----|---------|------|
| 前端框架 | **React 18 + TypeScript** | 组件化、生态丰富、SSE/WS 支持好 |
| UI 组件库 | **Shadcn/ui + Tailwind CSS** | 现代美观、轻量、高度可定制 |
| 实时通信 | **WebSocket (Socket.IO)** | 双向实时通信，支持断线重连 |
| 状态管理 | **Zustand** | 轻量级，适合实时数据流 |
| 图表 | **Recharts** | React 原生图表库 |
| 后端 | **FastAPI + uvicorn** | Python 异步框架，与 Agent 层天然集成 |
| 构建 | **Vite** | 开发体验好，构建速度快 |

### 4.2 页面结构

```
┌─────────────────────────────────────────────────────────────┐
│  HydroScribe                                     👤 雷晓辉  │
├────────┬────────────────────────────────────────────────────┤
│        │                                                    │
│ 📊 仪表盘│  ┌─ 仪表盘 ─────────────────────────────────┐   │
│ 📚 书架  │  │                                           │   │
│ ✍️ 写作  │  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐    │   │
│ 📝 评审  │  │  │16 本  │ │ 3 本  │ │ 47%  │ │ 2 个  │    │   │
│ 🔍 一致性│  │  │总书目 │ │进行中 │ │总进度 │ │待审批 │    │   │
│ 📖 术语  │  │  └──────┘ └──────┘ └──────┘ └──────┘    │   │
│ 📈 统计  │  │                                           │   │
│ ⚙️ 设置  │  │  ┌─ 当前活跃任务 ───────────────────────┐ │   │
│        │  │  │                                       │ │   │
│        │  │  │  📗 T2a ch07 模型预测控制              │ │   │
│        │  │  │  ██████████░░░░░░░░  62% 写作中       │ │   │
│        │  │  │  Writer-BK → 已写 24,800/40,000 字    │ │   │
│        │  │  │                                       │ │   │
│        │  │  │  📕 T1-EN ch03 Architecture           │ │   │
│        │  │  │  ████████████████░░  85% 评审中       │ │   │
│        │  │  │  Reviewer A: ✅  B: ✅  C: 🔄         │ │   │
│        │  │  │                                       │ │   │
│        │  │  └───────────────────────────────────────┘ │   │
│        │  │                                           │   │
│        │  │  ┌─ Agent 状态面板 ─────────────────────┐  │   │
│        │  │  │ 🟢 Orchestrator   调度中              │  │   │
│        │  │  │ 🟢 Writer-BK      ch07 撰写中        │  │   │
│        │  │  │ 🟡 Writer-SCI     空闲               │  │   │
│        │  │  │ 🔵 Reviewer-Inst  ch06 评审中        │  │   │
│        │  │  │ 🔵 Reviewer-Expert ch06 评审中       │  │   │
│        │  │  │ 🟢 Glossary-Guard  检查中            │  │   │
│        │  │  │ ⚪ Figure-Gen      待命              │  │   │
│        │  │  └──────────────────────────────────────┘  │   │
│        │  │                                           │   │
│        │  │  ┌─ 实时事件流 (最近 20 条) ─────────────┐ │   │
│        │  │  │ 14:32:05 📝 Writer-BK 产出§7.3 (2100字)│ │   │
│        │  │  │ 14:31:42 ✅ Glossary 术语检查通过      │ │   │
│        │  │  │ 14:30:18 ⭐ Reviewer-Expert 评分 8.5   │ │   │
│        │  │  │ 14:29:55 ⭐ Reviewer-Instructor 8.2   │ │   │
│        │  │  │ 14:25:00 📝 Writer-BK 完成 ch06 初稿   │ │   │
│        │  │  └──────────────────────────────────────┘  │   │
│        │  └─────────────────────────────────────────────┘   │
└────────┴────────────────────────────────────────────────────┘
```

### 4.3 核心页面设计

#### 页面 1：仪表盘 (Dashboard)

实时展示系统全局状态。

```
┌─────────────────────────────────────────────────┐
│  统计卡片行                                       │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐   │
│  │总书目 16│ │已完成 1 │ │进行中 3 │ │总字数   │   │
│  │本       │ │本       │ │本       │ │152万   │   │
│  └────────┘ └────────┘ └────────┘ └────────┘   │
│                                                  │
│  ┌─ 书目进度热力图 ────────────────────────────┐ │
│  │ T1-CN  ████████████████████ 100%            │ │
│  │ T1-EN  ██████░░░░░░░░░░░░░  35%            │ │
│  │ T2a    ████░░░░░░░░░░░░░░░  25%            │ │
│  │ T2b    ░░░░░░░░░░░░░░░░░░░   0%            │ │
│  │ M1     ░░░░░░░░░░░░░░░░░░░   0%            │ │
│  │ ...                                         │ │
│  └──────────────────────────────────────────────┘ │
│                                                  │
│  ┌─ 活跃 Agent ──┐  ┌─ 今日产出 ─────────────┐ │
│  │ (Agent状态列表) │  │ 📊 字数趋势折线图      │ │
│  │ (含CPU/内存)   │  │ 📊 章节完成甘特图      │ │
│  └────────────────┘  └────────────────────────┘ │
└─────────────────────────────────────────────────┘
```

#### 页面 2：书架 (BookShelf)

16 本书的总览视图，每本书显示为一张卡片。

```
┌─────────────────────────────────────────────────┐
│  🏗️ 第一层·种子                                   │
│  ┌──────────────────┐ ┌──────────────────┐      │
│  │ 📗 T1-CN         │ │ 📘 T1-EN         │      │
│  │ 水系统控制论      │ │ Cybernetics of   │      │
│  │ ████████████ 100% │ │ Hydro Systems    │      │
│  │ 9/9 章 ✅         │ │ ████░░░░  35%    │      │
│  │ 152,000 字        │ │ 2/6 章           │      │
│  └──────────────────┘ └──────────────────┘      │
│                                                  │
│  🏗️ 第二层·骨架                                   │
│  ┌──────────────────┐ ┌──────────────────┐      │
│  │ 📙 T2a           │ │ 📕 T2b           │      │
│  │ 建模与控制        │ │ 智能与自主        │      │
│  │ ████░░░░  25%     │ │ ░░░░░░░░   0%    │      │
│  │ 4/16 章           │ │ 0/14 章           │      │
│  └──────────────────┘ └──────────────────┘      │
│  ...                                             │
└─────────────────────────────────────────────────┘
```

点击某本书进入章节详情：

```
┌─────────────────────────────────────────────────┐
│  📙 T2a 《水系统控制论：建模与控制》               │
│  进度: 4/16 章  |  总字数: 112,000/450,000       │
│                                                  │
│  章节列表                                        │
│  ┌────┬──────────────┬────────┬──────┬────────┐ │
│  │ 章 │ 标题          │ 状态   │ 字数  │ 评审   │ │
│  ├────┼──────────────┼────────┼──────┼────────┤ │
│  │ 01 │ 导论          │ ✅完成  │ 19.5k│ 8/9/7  │ │
│  │ 02 │ 明渠水动力学  │ ✅完成  │ 30.2k│ 9/8/8  │ │
│  │ 03 │ 管网水力学    │ ✅完成  │ 28.8k│ 8/8/7  │ │
│  │ 04 │ 降阶建模      │ ✅完成  │ 31.0k│ 9/9/8  │ │
│  │ 05 │ 经典控制方法  │ 🔄写作中│ 18.2k│ —     │ │
│  │ 06 │ 现代控制方法  │ ⏳待写  │ —    │ —     │ │
│  │ .. │ ...          │ ⏳待写  │ —    │ —     │ │
│  └────┴──────────────┴────────┴──────┴────────┘ │
│                                                  │
│  [▶ 开始写下一章]  [🔄 重写选定章]  [📊 导出]    │
└─────────────────────────────────────────────────┘
```

#### 页面 3：写作面板 (Writing Panel)

实时展示 Writer Agent 的写作过程（流式输出）。

```
┌─────────────────────────────────────────────────────────┐
│  ✍️ T2a ch07 — 模型预测控制（MPC）                        │
│  Writer: writer-bk | 迭代: 第1轮 | 目标: 40,000字        │
│                                                          │
│  ┌─ 大纲导航 ──┐  ┌─ 实时写作内容 ─────────────────────┐│
│  │ 7.1 MPC原理 │  │                                    ││
│  │  ✅ 7.1.1   │  │ ## 7.3 线性MPC                     ││
│  │  ✅ 7.1.2   │  │                                    ││
│  │ 7.2 约束处理│  │ 线性MPC是模型预测控制中最基础也是  ││
│  │  ✅ 7.2.1   │  │ 应用最广泛的形式。当被控对象可以   ││
│  │  ✅ 7.2.2   │  │ 用线性模型充分描述时，MPC的在线    ││
│  │ 7.3 线性MPC │  │ 优化问题退化为一个二次规划（QP）   ││
│  │  🔄 7.3.1   │  │ 问题，具有成熟高效的求解算法。     ││
│  │  ⏳ 7.3.2   │  │                                    ││
│  │ 7.4 非线性  │  │ [物理直觉] 线性MPC就像一个棋手...  ││
│  │ 7.5 分布式  │  │ ████████████████░░░░ 正在生成...   ││
│  │ ...         │  │                                    ││
│  └──────────────┘  └────────────────────────────────────┘│
│                                                          │
│  ┌─ 元数据 ─────────────────────────────────────────────┐│
│  │ 字数: 24,800/40,000 | 新概念: 6/10 | 公式: 18       ││
│  │ 例题: 3 | 图表: 5 | 参考文献: 23                     ││
│  └───────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────┘
```

#### 页面 4：评审面板 (Review Panel)

多角色评审的并行状态和结果展示。

```
┌─────────────────────────────────────────────────────────┐
│  📝 评审: T2a ch07 — 第2轮                               │
│                                                          │
│  ┌─ 教师评审 ─────────┐  ┌─ 专家评审 ─────────┐        │
│  │ 状态: ✅ 已完成      │  │ 状态: ✅ 已完成      │        │
│  │ 覆盖度:    ★★★★☆   │  │ 准确性:    ★★★★★   │        │
│  │ 难度梯度:  ★★★★☆   │  │ 文献覆盖:  ★★★★☆   │        │
│  │ 例题质量:  ★★★★★   │  │ 前沿性:    ★★★★★   │        │
│  │ 可教性:    8.5/10   │  │ 学术评分:  9.0/10   │        │
│  │                     │  │                     │        │
│  │ 🔴 无               │  │ 🔴 无               │        │
│  │ 🟡 建议补充约束处理  │  │ 🟡 式(7-12)需检查   │        │
│  │    例题             │  │    量纲一致性       │        │
│  │ 🟢 可增加国际对比   │  │ 🟢 建议引用最新综述  │        │
│  └─────────────────────┘  └─────────────────────┘        │
│                                                          │
│  ┌─ 工程师评审 ────────┐  ┌─ 综合判定 ─────────┐        │
│  │ 状态: 🔄 评审中...   │  │                     │        │
│  │ ██████████░░ 75%    │  │ 教师:   8.5         │        │
│  │                     │  │ 专家:   9.0         │        │
│  │                     │  │ 工程师: (评审中)     │        │
│  │                     │  │ 国际:   (待启动)     │        │
│  │                     │  │ ───────────         │        │
│  │                     │  │ 综合:   待定         │        │
│  │                     │  │ 阈值:   8.0         │        │
│  └─────────────────────┘  └─────────────────────┘        │
│                                                          │
│  ┌─ 修改建议汇总 ───────────────────────────────────────┐│
│  │ 🔴 致命 (0)                                          ││
│  │ 🟡 重要 (2)                                          ││
│  │   1. 补充约束处理例题 (教师)                          ││
│  │   2. 检查式(7-12)量纲 (专家)                          ││
│  │ 🟢 建议 (2)                                          ││
│  │   3. 增加国际对比 (教师)                              ││
│  │   4. 引用最新MPC综述 (专家)                           ││
│  └───────────────────────────────────────────────────────┘│
│                                                          │
│  [✅ 批准通过]  [🔄 要求修改]  [👤 人工审阅]             │
└─────────────────────────────────────────────────────────┘
```

#### 页面 5：一致性检查器 (Consistency Checker)

跨书一致性的可视化。

```
┌─────────────────────────────────────────────────────────┐
│  🔍 跨书一致性检查                                       │
│                                                          │
│  ┌─ 共享内容一致性矩阵 ─────────────────────────────────┐│
│  │                                                      ││
│  │  内容             │ T1  │ T2a │ T2b │ M1  │ M8     ││
│  │  ─────────────────┼─────┼─────┼─────┼─────┼────    ││
│  │  八原理表述        │ ✅  │ ✅  │ ⏳  │ —   │ —      ││
│  │  WNAL L0-L5       │ ✅  │ —   │ ⏳  │ —   │ ⏳     ││
│  │  Saint-Venant方程 │ —   │ ✅  │ —   │ ⏳  │ ⏳     ││
│  │  MPC基本原理      │ —   │ ✅  │ —   │ —   │ ⏳     ││
│  │  HydroOS架构      │ ✅  │ —   │ ⏳  │ —   │ —      ││
│  │  胶东调水参数      │ —   │ ✅  │ ⏳  │ ✅  │ ⏳     ││
│  │  沙坪参数         │ —   │ ✅  │ ⏳  │ —   │ ⏳     ││
│  │                                                      ││
│  │  ✅ = 已检查一致  ⏳ = 未写/待检查  ⚠️ = 不一致      ││
│  └──────────────────────────────────────────────────────┘│
│                                                          │
│  ┌─ 术语使用频率 ──────────────────────────────────────┐ │
│  │ "水系统控制论" : 342 次 (全部正确)                   │ │
│  │ "安全包络"     : 89 次 (全部正确)                    │ │
│  │ ⚠️ "安全边界"  : 3 次 (T2a ch10 第42行, ...)        │ │
│  │    → 建议改为 "安全包络"                             │ │
│  └──────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## 5. 后端架构

### 5.1 目录结构

```
multi-agent-writer/
├── DESIGN.md                    ← 本文件
├── backend/
│   ├── main.py                  ← FastAPI 入口
│   ├── config.py                ← 配置管理
│   ├── models/                  ← 数据模型
│   │   ├── task.py
│   │   ├── event.py
│   │   └── agent.py
│   ├── agents/                  ← Agent 实现
│   │   ├── base_agent.py        ← Agent 基类
│   │   ├── orchestrator.py      ← 编排器
│   │   ├── writers/             ← 9 大 Writer Agent
│   │   │   ├── base_writer.py
│   │   │   ├── book_writer.py
│   │   │   ├── sci_writer.py
│   │   │   ├── cn_writer.py
│   │   │   ├── patent_writer.py
│   │   │   ├── report_writer.py
│   │   │   ├── std_cn_writer.py
│   │   │   ├── std_int_writer.py
│   │   │   ├── wechat_writer.py
│   │   │   └── ppt_writer.py
│   │   ├── reviewers/           ← 评审 Agent
│   │   │   ├── base_reviewer.py
│   │   │   ├── instructor_reviewer.py
│   │   │   ├── expert_reviewer.py
│   │   │   ├── engineer_reviewer.py
│   │   │   ├── international_reviewer.py
│   │   │   └── ...
│   │   └── utilities/           ← 工具 Agent
│   │       ├── glossary_guard.py
│   │       ├── consistency_checker.py
│   │       ├── reference_manager.py
│   │       └── figure_generator.py
│   ├── engine/                  ← 核心引擎
│   │   ├── event_bus.py         ← 事件总线
│   │   ├── dag_scheduler.py     ← DAG 调度器
│   │   ├── task_planner.py      ← 任务规划器
│   │   └── gate_keeper.py       ← 门控审批器
│   ├── llm/                     ← LLM 对接
│   │   ├── claude_client.py     ← Anthropic Claude API
│   │   └── prompt_builder.py   ← 提示词构建器
│   ├── storage/                 ← 存储层
│   │   ├── git_manager.py       ← Git 操作
│   │   ├── progress_tracker.py  ← 进度管理
│   │   └── file_manager.py      ← 文件操作
│   ├── api/                     ← API 路由
│   │   ├── tasks.py
│   │   ├── agents.py
│   │   ├── books.py
│   │   ├── reviews.py
│   │   └── websocket.py
│   └── requirements.txt
├── frontend/
│   ├── package.json
│   ├── src/
│   │   ├── App.tsx
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── BookShelf.tsx
│   │   │   ├── BookDetail.tsx
│   │   │   ├── WritingPanel.tsx
│   │   │   ├── ReviewPanel.tsx
│   │   │   ├── ConsistencyChecker.tsx
│   │   │   ├── GlossaryView.tsx
│   │   │   └── Settings.tsx
│   │   ├── components/
│   │   │   ├── AgentStatusCard.tsx
│   │   │   ├── ProgressBar.tsx
│   │   │   ├── EventStream.tsx
│   │   │   ├── ReviewScoreCard.tsx
│   │   │   ├── DAGVisualizer.tsx
│   │   │   └── BookCard.tsx
│   │   ├── hooks/
│   │   │   ├── useWebSocket.ts
│   │   │   └── useAgentStatus.ts
│   │   └── stores/
│   │       ├── taskStore.ts
│   │       └── agentStore.ts
│   └── vite.config.ts
└── docker-compose.yml           ← 一键部署
```

### 5.2 核心类设计

#### BaseAgent — Agent 基类

```python
class BaseAgent(ABC):
    """所有 Agent 的基类"""

    def __init__(self, agent_id: str, agent_type: str, event_bus: EventBus):
        self.agent_id = agent_id
        self.agent_type = agent_type     # "writer" | "reviewer" | "utility"
        self.event_bus = event_bus
        self.status = AgentStatus.IDLE   # IDLE | BUSY | ERROR
        self.current_task: Optional[str] = None

    @abstractmethod
    async def execute(self, task: WritingTask, context: dict) -> AgentResult:
        """执行任务的核心方法"""
        pass

    async def emit(self, event_type: EventType, payload: dict):
        """发送事件"""
        event = Event(
            type=event_type,
            source_agent=self.agent_id,
            payload=payload
        )
        await self.event_bus.publish(event)

    async def stream_output(self, chunk: str):
        """流式输出写作内容"""
        await self.emit(EventType.WRITING_CHUNK, {"chunk": chunk})
```

#### Orchestrator — 编排器

```python
class Orchestrator:
    """多智能体编排器 — 系统大脑"""

    def __init__(self, config: Config):
        self.event_bus = EventBus()
        self.planner = TaskPlanner(config)
        self.scheduler = DAGScheduler()
        self.gate_keeper = GateKeeper(config.gate_mode)
        self.agent_pool = AgentPool()      # 管理所有 Agent 实例
        self.progress = ProgressTracker()

    async def start_book(self, book_id: str):
        """启动一本书的写作"""
        # 1. 规划
        spec = self.planner.load_book_spec(book_id)
        progress = self.progress.load(book_id)
        next_chapter = self.planner.find_next_chapter(spec, progress)

        # 2. 创建 DAG
        dag = self.scheduler.create_chapter_dag(
            book_id=book_id,
            chapter=next_chapter,
            skill_type=spec.skill_type,
            reviewers=spec.reviewers
        )

        # 3. 执行
        await self.execute_dag(dag)

    async def execute_dag(self, dag: DAG):
        """按 DAG 调度执行"""
        while not dag.is_complete():
            ready_nodes = dag.get_ready_nodes()

            # 并行启动所有就绪节点
            tasks = []
            for node in ready_nodes:
                agent = self.agent_pool.get_agent(node.agent_type)
                tasks.append(self._run_node(agent, node))

            # 等待本批完成
            results = await asyncio.gather(*tasks)

            # 更新 DAG 状态
            for node, result in zip(ready_nodes, results):
                dag.mark_completed(node.id, result)

            # 检查门控
            if dag.at_gate():
                approved = await self.gate_keeper.check(dag.gate_data())
                if not approved:
                    dag.trigger_revision()

    async def _run_node(self, agent: BaseAgent, node: DAGNode):
        """执行单个 DAG 节点"""
        await self.event_bus.publish(Event(
            type=EventType.TASK_STARTED,
            source_agent=agent.agent_id,
            payload={"node": node.id, "name": node.name}
        ))

        result = await agent.execute(node.task, node.context)

        await self.event_bus.publish(Event(
            type=EventType.TASK_COMPLETED,
            source_agent=agent.agent_id,
            payload={"node": node.id, "result_summary": result.summary}
        ))

        return result
```

### 5.3 LLM 调用策略

```python
class ClaudeClient:
    """Claude API 客户端 — 支持流式输出"""

    MODEL_MAP = {
        "writer":   "claude-sonnet-4-6",     # 写作用 Sonnet（性价比）
        "reviewer": "claude-sonnet-4-6",     # 评审用 Sonnet
        "planner":  "claude-opus-4-6",       # 规划用 Opus（最强推理）
        "utility":  "claude-haiku-4-5-20251001",  # 工具检查用 Haiku（快）
    }

    async def stream_generate(self, prompt: str, role: str) -> AsyncIterator[str]:
        """流式生成，实时推送每个 chunk 到前端"""
        model = self.MODEL_MAP[role]
        async with self.client.messages.stream(
            model=model,
            max_tokens=16384,
            messages=[{"role": "user", "content": prompt}]
        ) as stream:
            async for text in stream.text_stream:
                yield text
```

**模型选择策略：**

| 角色 | 模型 | 理由 |
|------|------|------|
| Orchestrator / Planner | Opus 4.6 | 需要最强规划和推理能力 |
| Writer Agents | Sonnet 4.6 | 写作质量好，性价比高，支持长输出 |
| Reviewer Agents | Sonnet 4.6 | 评审需要好的分析能力 |
| Utility Agents | Haiku 4.5 | 术语/格式检查不需强推理，要快 |

### 5.4 WebSocket 实时通信

```python
# backend/api/websocket.py

class ConnectionManager:
    """WebSocket 连接管理器"""

    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def broadcast(self, event: Event):
        """广播事件到所有连接的前端"""
        message = {
            "type": event.type.value,
            "timestamp": event.timestamp.isoformat(),
            "agent": event.source_agent,
            "book": event.book_id,
            "chapter": event.chapter_id,
            "payload": event.payload
        }
        for connection in self.active_connections:
            await connection.send_json(message)

# 在 EventBus 中集成
class EventBus:
    def __init__(self):
        self.subscribers: dict[EventType, list[Callable]] = {}
        self.ws_manager = ConnectionManager()

    async def publish(self, event: Event):
        # 通知内部订阅者
        for handler in self.subscribers.get(event.type, []):
            await handler(event)
        # 同步推送到前端
        await self.ws_manager.broadcast(event)
```

---

## 6. 关键流程详解

### 6.1 完整写作流程（以 "开始BKT2a" 为例）

```
用户输入: "开始BKT2a"
        │
        ▼
[Orchestrator.start_book("T2a")]
        │
        ├─① 读取 CLAUDE.md §2 → T2a 规格 (16章, 400-500页)
        ├─② 读取 progress/BKT2a.json → ch01-ch04 已完成
        ├─③ 确定下一章: ch05 "经典控制方法" (30,000字)
        │
        ▼
[TaskPlanner.create_chapter_plan()]
        │
        ├─ 生成章节大纲 (Opus 规划)
        │   §5.1 PID/PI控制器
        │   §5.2 前馈-反馈控制
        │   §5.3 解耦控制
        │   §5.4 频域设计
        │   §5.5 Bode/Nyquist应用
        │   + 学习目标 + 例题 + 习题
        │
        ▼
[DAGScheduler.create_chapter_dag()]
        │
        ├─ Node 1: load_spec (加载规格)
        ├─ Node 2: read_prev_chapter (读ch04末尾500字)
        ├─ Node 3: write_draft (Writer-BK 撰写, ~30min)
        ├─ Node 4: check_glossary (术语检查, 并行)
        ├─ Node 5: check_references (文献检查, 并行)
        ├─ Node 6: check_consistency (一致性检查, 并行)
        ├─ Node 7: review_instructor (教师评审, 并行)
        ├─ Node 8: review_expert (专家评审, 并行)
        ├─ Node 9: review_engineer (工程师评审, 并行)
        ├─ Node 10: aggregate_reviews (汇总评审)
        └─ Node 11: gate (门控决定)
            │
            ├─ 通过 → save_final + update_progress + git_commit
            └─ 未通过 → revision (回到 Node 3, 携带评审意见)
```

### 6.2 并行评审时序

```
时间线 ──────────────────────────────────────────────────────→

Writer-BK:    ████████████████████ (撰写初稿)
              │完成
              ▼
Glossary:     ██ (检查) ─────────────────────────┐
Reference:    ███ (检查) ────────────────────────┤
Consistency:  ██ (检查) ─────────────────────────┤
              │                                   │
              │ 所有检查通过                        │
              ▼                                   │
Reviewer-教师: ████████ (评审) ──────────────┐   │
Reviewer-专家: █████████ (评审) ─────────────┤   │
Reviewer-工程师:██████████ (评审) ────────────┤   │
Reviewer-国际: ████████ (评审) ──────────────┤   │
              │                              │   │
              │ 所有评审完成                    │   │
              ▼                              │   │
Orchestrator: ██ (汇总+门控) ────────────────┘   │
              │                                   │
              ├─ 通过 → 保存                       │
              └─ 不通过 → Writer-BK 修改 → 再评审   │
```

**关键优化：评审并行后，4个 Reviewer 同时工作，时间 = max(单个评审时间) 而非 sum。**

### 6.3 人在环（Human-in-the-Loop）流程

```
┌──────────────┐         ┌──────────────┐
│  自动写作     │         │   UI 界面    │
│  + 评审完成   │────→────│              │
│              │         │  🔔 通知:     │
│              │         │  "T2a ch05   │
│              │         │   评审完成    │
│              │         │   综合 8.3分" │
│              │         │              │
│              │         │  [✅ 批准]    │
│              │←───←────│  [🔄 修改]    │
│              │         │  [📝 批注]    │
│              │         │              │
│  继续下一章   │         │  用户选择     │
│  或修改      │         │  "批准"      │
└──────────────┘         └──────────────┘
```

---

## 7. 与现有系统的集成

### 7.1 复用现有资产

| 现有资产 | 位置 | 集成方式 |
|---------|------|---------|
| 9 大 Writer Agent 提示词 | `writing-projects/academic-writer-skill/SKILL.md` | 直接作为 Writer System Prompt |
| 9 大 Reviewer Agent 定义 | `writing-projects/academic-writer-skill/agents/*.md` | 直接作为 Reviewer System Prompt |
| 评分锚点 | `references/scoring_rubrics.md` | 注入 Reviewer Context |
| 金标准片段 | `references/gold_standard_fragments.md` | 注入 Writer Context |
| 写作技法 | `references/writing_craft_guide.md` | 注入 Writer Context |
| 引用规范 | `references/citation_style_guide.md` | 注入 Reference Manager |
| 术语表 | `terminology/glossary_cn.md` + `glossary_en.md` | Glossary Guard 数据源 |
| 符号表 | `terminology/symbols.md` | Writer/Reviewer Context |
| 进度文件 | `progress/BK[X].json` | ProgressTracker 读写 |
| 已有书稿 | `books/T1-CN/*.md` 等 | 跨书一致性检查参考 |
| OCAC 核心逻辑 | `agent-core/*.py` | 迁移 TaskDecomposer/Evaluator |

### 7.2 与 CLAUDE.md 的关系

CLAUDE.md 继续作为**主控提示词**，HydroScribe 系统自动解析其中的：
- §2 书目规格 → 自动生成 WritingTask
- §5 术语规范 → Glossary Guard 规则库
- §6 质量标准 → Reviewer 评分标准
- §7 四角色评审 → Reviewer Agent 配置
- §8 写作风格 → Writer Agent 风格约束
- §10 进度追踪 → ProgressTracker 格式
- §11 一致性检查 → Consistency Checker 规则

### 7.3 迁移路径

```
Phase 1 (2周)   → 后端核心: EventBus + BaseAgent + Orchestrator
Phase 2 (2周)   → Writer-BK + 4个 Book Reviewer → 打通单章写作流程
Phase 3 (1周)   → 前端: Dashboard + BookShelf + WritingPanel
Phase 4 (1周)   → 前端: ReviewPanel + WebSocket 实时推送
Phase 5 (2周)   → 其余 8 个 Writer + 对应 Reviewer
Phase 6 (1周)   → Utility Agents + 一致性检查
Phase 7 (1周)   → Docker 化 + 部署 + 文档
```

---

## 8. 与 Manus/OpenManus 的对比

| 维度 | Manus | OpenManus | HydroScribe (本系统) |
|------|-------|-----------|---------------------|
| **定位** | 通用 AI Agent | 开源通用 Agent 框架 | CHS 学术写作专用 |
| **Agent 编排** | Plan-Execute-Reflect 循环 | DAG 工作流 + 动态规划 | DAG + 门控 + 人在环 |
| **并行策略** | 浏览器多标签页并行 | asyncio 并行 | Writer 串行 + Reviewer 并行 |
| **UI** | 内置 Web 界面 | 终端为主 | 专业写作仪表盘 |
| **记忆** | 长期记忆 + 向量检索 | 文件系统 | Git + JSON 进度 + 术语库 |
| **工具调用** | 浏览器/代码/文件 | 多工具链 | LLM 写作 + 术语/一致性检查 |
| **质量保证** | 自我反思 | 评估器 | 多角色并行评审 + 门控 |
| **领域知识** | 无 | 无 | CHS 术语表 + 符号表 + 引用库 |
| **部署** | 云端 SaaS | Docker 自部署 | Docker 自部署 |

**HydroScribe 的独特优势：**

1. **领域深度** — 内置 CHS 全套领域知识（术语/符号/引用/架构图）
2. **质量体系** — 9 种文体 × 多角色评审 = 27+ 种评审视角
3. **跨书一致性** — 16 本书共享术语、符号、工程参数的一致性保障
4. **人在环门控** — 关键节点可插入人工审批，不是纯自动化

---

## 9. 技术风险与对策

| 风险 | 影响 | 对策 |
|------|------|------|
| LLM 单次输出长度受限 | 无法一次写完 3 万字章节 | 按小节分片写作，Orchestrator 自动拼接 |
| LLM 幻觉/编造工程参数 | 技术内容不准确 | `[TODO]` 标记 + 工程师评审角色专项检查 |
| 多 Agent 并行成本高 | API 费用 | Haiku 用于检查，Sonnet 用于写作，Opus 仅用于规划 |
| Context Window 溢出 | 长章节上下文丢失 | 分段写作 + 摘要传递 + RAG 检索 |
| 前后章不衔接 | 阅读体验差 | 前序章末尾 500 字 + 章节衔接检查 Agent |
| 术语漂移 | 同概念不同表述 | Glossary Guard 实时检查 + 禁止别名库 |

---

## 10. 一键启动

```bash
# 开发模式
cd multi-agent-writer
docker-compose up -d

# 访问
# 前端:  http://localhost:3000
# API:   http://localhost:8000/docs
# WS:    ws://localhost:8000/ws

# 或者分别启动
cd backend && uvicorn main:app --reload --port 8000
cd frontend && npm run dev
```

```yaml
# docker-compose.yml
version: "3.9"
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ../books:/app/books          # 挂载书稿目录
      - ../progress:/app/progress    # 挂载进度目录
      - ../terminology:/app/terminology
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - GIT_REPO_PATH=/app/books

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
```

---

## 附录 A：与 CLAUDE.md "开始BK" 指令的兼容

HydroScribe 完全兼容现有的 `开始BK[X]` 和 `继续` 指令。用户既可以：

1. **通过 UI** — 在书架页面点击 "开始写下一章" 按钮
2. **通过 CLI** — 在终端输入 `开始BKT2a`，系统自动启动并在 UI 上显示进度
3. **通过 API** — `POST /api/tasks {"command": "开始BKT2a"}`

三种入口最终都调用同一个 `Orchestrator.start_book()` 方法。

---

## 附录 B：Agent 通信协议示例

```json
// Writer 完成初稿事件
{
  "type": "writing.done",
  "timestamp": "2026-03-15T14:25:00Z",
  "agent": "writer-bk",
  "book": "T2a",
  "chapter": "ch07",
  "payload": {
    "word_count": 41200,
    "sections": ["7.1", "7.2", "7.3", "7.4", "7.5"],
    "new_concepts": 8,
    "equations": 24,
    "examples": 5,
    "figures": 7,
    "file_path": "books/T2a/ch07_v1.md"
  }
}

// Reviewer 评分事件
{
  "type": "review.score",
  "timestamp": "2026-03-15T14:55:00Z",
  "agent": "reviewer-instructor",
  "book": "T2a",
  "chapter": "ch07",
  "payload": {
    "role": "教师",
    "scores": {
      "coverage": 4,
      "difficulty_gradient": 4,
      "example_quality": 5,
      "exercise_quality": 3,
      "teachability": 8.2
    },
    "issues": {
      "red": [],
      "yellow": ["建议补充约束处理例题"],
      "green": ["可增加国际案例对比"]
    },
    "overall": 8.2
  }
}

// 门控等待事件
{
  "type": "gate.waiting",
  "timestamp": "2026-03-15T15:10:00Z",
  "agent": "orchestrator",
  "book": "T2a",
  "chapter": "ch07",
  "payload": {
    "round": 2,
    "aggregate_score": 8.5,
    "threshold": 8.0,
    "recommendation": "auto_approve",
    "reviewer_scores": {
      "instructor": 8.2,
      "expert": 9.0,
      "engineer": 8.3
    }
  }
}
```
