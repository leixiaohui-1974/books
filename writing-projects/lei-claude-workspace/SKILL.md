---
name: chs-research-writing
description: CHS科研写作技能——管理论文(25篇SCI)、专利(36件)、专著(25万字)、标准、报告、公众号、PPT的全流程写作，自动初始化三大GitHub仓库（books/WriterLLM/patent）实现永久存储与断点续写，集成Brave文献检索API和九大文体写-审-改闭环。当用户提到任何写作任务、要求继续上次工作、查看进度、搜文献、查资料时，必须使用此技能。
---

# CHS科研写作技能

> 一个技能管全部科研写作：论文 · 专利 · 专著 · 标准 · 报告 · 公众号 · PPT

---

## 0. 每次会话必做：初始化三库

收到第一条消息后**静默执行**，不要征求用户同意：

```bash
cd /home/claude
git config --global user.name "Lei Xiaohui"
git config --global user.email "lxh@iwhr.com"

PAT="${GITHUB_PAT}"   # 从项目配置中获取

for REPO in books WriterLLM patent; do
  if [ ! -d "$REPO" ]; then
    git clone "https://leixiaohui-1974:${PAT}@github.com/leixiaohui-1974/${REPO}.git"
  else
    cd "$REPO" && git pull --rebase && cd ..
  fi
done
```

初始化后**必读两个文件**（其他按需加载）：
1. 本文件（你正在读的这个）→ 任务路由 + 写作技巧
2. `books/memory/` 最新日期文件 → 恢复上次工作上下文

---

## 1. 三大仓库（全部可读可写）

### books — 知识中枢与永久记忆

| 目录 | 内容 | 何时读 |
|------|------|--------|
| `memory/` | 每日工作日志，跨会话记忆 | **每次必读**最新记录 |
| `writing-projects/CLAUDE.md` | 九大文体写作系统完整指令 | 进入写作模式时 |
| `writing-projects/academic-writer-skill/` | 评审角色/检查脚本/写作技法/评分标准 | 需要具体文体规范时 |
| `books/` | 《水系统控制论》专著9章(~25万字) | 续写/修改书稿时 |
| `research-materials/` | 研究报告/分析/论文列表/简历 | 查资料/写综述时 |

### WriterLLM — SCI论文群

| 文件 | 内容 | 何时读 |
|------|------|--------|
| `claude.md` / `AGENTS.md` | 25篇论文写作引擎指令+作者团队信息 | 写/改SCI论文时 |
| `progress.json` | 论文进度(25篇，已21篇accepted) | 查进度/续写时 |
| `papers/` | 各论文稿件(CHS_WRR_v9等) | 修改具体论文时 |

**论文编号体系**：P1a/P1b/P1c/P2A-E(总论)、CKG-1/2/3(陈凯歌)、SC-1/2(苏超)、HZF-1/2/3(黄志锋)、WHM-1/2(吴辉明)、BAK-1/YBK-1(水槽)

### patent — 专利族

| 文件 | 内容 | 何时读 |
|------|------|--------|
| `patents/progress.md` | 36件专利进度(全部完成) | 查进度/交叉检查时 |
| `patents/PFx-x.md` | 各专利全文 | 修改/审核具体专利时 |

**专利族编号**：PF1(水力建模6件)、PF2(控制策略6件)、PF3(安全与ODD 5件)、PF4(MAS与数字孪生5件)、PF5(大模型5件)、PF6(在环测试5件)、PF7(HydroOS 4件)

---

## 2. 任务路由表

| 用户说的话 | 读什么 | 存到哪 |
|-----------|--------|--------|
| 写SCI/英文论文/P1a/CKG-2... | `WriterLLM/claude.md` + `progress.json` | WriterLLM/papers/ |
| 写中文核心论文 | `books/.../CLAUDE.md` → CN流程 | books/writing-projects/ |
| 写专利/改专利/PF3-2... | `patent/patents/progress.md` + 对应PF文件 | patent/patents/ |
| 写书/续写第X章 | `books/books/` 对应章节 | books/books/ |
| 写报告/写可研 | `books/.../CLAUDE.md` → RPT流程 | books/writing-projects/ |
| 写标准/写国标/写ISO | `books/.../CLAUDE.md` → STD流程 | books/writing-projects/ |
| 写公众号/写推文 | `books/.../CLAUDE.md` → WX流程 | books/writing-projects/ |
| 做PPT/做汇报 | `books/.../CLAUDE.md` → PPT流程 | books/writing-projects/ |
| 审稿回复 | 上传的审稿意见+原论文 | books/writing-projects/ |
| 查文献/验证引用 | Brave API检索 | — |
| 继续/上次做什么了 | `books/memory/` 最新文件 | — |
| 论文进度 | `WriterLLM/progress.json` | — |
| 专利进度 | `patent/patents/progress.md` | — |
| 查资料/找XX | 三库 `grep -r` | — |

---

## 3. 科研写作12条技巧

### 流程类

**技巧1 写-审-改闭环**
所有正式文档必须多角色评审迭代。九大文体各有专属评审角色和达标标准（详见 `academic-writer-skill/SKILL.md`）。

**技巧2 三库持久化**
产出按类型存入对应仓库。commit规范：`[类型] 描述`。断点续传：说"继续"即可从memory恢复。

**技巧3 讨论→写作自然切换**
不急于动笔。先在讨论中理清要素（类型/创新点/目标读者/结构），信息足够后输出提纲，确认再动笔。

**技巧4 分层渐进**
长文档分模块：提纲→逐节撰写→组装→通检。25万字书稿用L4策略（50模块×5000字）。

### 质量类

**技巧5 质量关卡强制**
初稿必跑 `run_checks.py`。参考文献验证关卡不可跳过——编造文献整篇打回。

**技巧6 文献检索用Brave API**
验证真实性、查最新进展、确认标准有效。检索命令见本文件第4节。

**技巧7 跨文档一致性**
论文-专利-书稿间术语/参数/符号统一。创新点重叠<30%。用 `check_consistency.py` 检查。

**技巧8 ODD场景化思维**
水网问题从运行设计域切入：正常域→扩展域→MRC，六维参数向量结构化。这是CHS标志性方法。

### 工具类

**技巧9 python-docx生成Word**
避免JS的中文引号转义问题。内容写文本文件，Python脚本读取生成docx。

**技巧10 审稿回复要简练**
每条意见1-2段，说清"改了什么"。不堆砌不套话。不同意就说"我们的理解是……"。

**技巧11 多平台内容分发**
同一学术内容可适配：SCI论文→中文核心→公众号科普→PPT汇报→短视频脚本。

**技巧12 上下文高效利用**
按需加载文件，不一次读完。先看目录结构，按任务定位具体内容。

---

## 4. 文献检索

```bash
curl -s "https://api.search.brave.com/res/v1/web/search?q=${QUERY}&count=10" \
  -H "X-Subscription-Token: ${BRAVE_API_KEY}" \
  -H "Accept: application/json"
```

**典型用途**：
- `q=DOI+10.1016/xxx` → 验证参考文献
- `q=water+network+autonomous+control+2024` → 检索最新进展
- `q=GB/T+50509+现行` → 确认标准有效性
- `q=发明专利+水网+分布式控制` → 查竞争专利

---

## 5. 会话结束存档

```bash
cd /home/claude/books
cat >> memory/$(date +%Y-%m-%d).md << 'EOF'

## HH:MM 更新
- 完成：[产出]
- 决策：[关键决策]
- 待办：[下次做什么]
EOF
git add -A && git commit -m "[memory] $(date +%Y-%m-%d) 工作记录" && git push
```

如修改了其他仓库，也对应push：
```bash
cd /home/claude/WriterLLM && git add -A && git commit -m "[论文编号] 描述" && git push
cd /home/claude/patent && git add -A && git commit -m "[PFx-x] 描述" && git push
```
