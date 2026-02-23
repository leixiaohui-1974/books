---
name: lei-claude-workspace
description: 雷晓辉与Claude协作工作空间——自动初始化GitHub仓库(books)作为永久记忆、加载九大文体写作技能、配置文献检索API、执行写-审-改闭环。当用户提到任何写作任务（论文、专利、书稿、报告、标准、公众号、PPT、审稿回复）、要求继续上次工作、查看进度、或进行学术研究时，必须使用此技能。这是所有任务的入口技能。
---

# 雷晓辉 × Claude 协作工作空间

> 一个技能统管全局：初始化 → 读记忆 → 干活 → 存记忆

---

## 0. 每次会话必做：自动初始化

收到第一条消息后，**静默执行**以下脚本（不要问用户），然后再回应：

```bash
cd /home/claude
git config --global user.name "Lei Xiaohui"
git config --global user.email "lxh@iwhr.com"

if [ ! -d "books" ]; then
  git clone https://leixiaohui-1974:${GITHUB_PAT}@github.com/leixiaohui-1974/books.git
else
  cd books && git pull --rebase && cd ..
fi
```

**环境变量**（运行时注入，不硬编码到输出中）：
- `GITHUB_PAT`: GitHub Personal Access Token
- `BRAVE_API_KEY`: Brave Search API Key（用于文献检索）

初始化后读取：
1. `books/writing-projects/CLAUDE.md` → 写作系统完整指令
2. `books/writing-projects/academic-writer-skill/SKILL.md` → 九大文体规范
3. `books/memory/` → 最近工作记录

---

## 1. 永久记忆系统

### 记忆存放位置

```
books/
├── memory/                    ← 工作记忆（每次会话结束时更新）
│   ├── YYYY-MM-DD.md          ← 当日工作日志
│   └── skills/                ← 学到的新技能
├── writing-projects/          ← 所有写作产出
│   ├── CLAUDE.md              ← 写作系统主指令
│   ├── academic-writer-skill/ ← 九大文体技能包
│   └── [各项目目录]/
├── research-materials/        ← 研究素材
└── books/                     ← 已有书稿
```

### 会话结束前

如果本次会话产生了重要产出，自动追加到 `memory/YYYY-MM-DD.md` 并 git push：

```bash
cd /home/claude/books
# 追加今日工作记录
cat >> memory/$(date +%Y-%m-%d).md << 'EOF'
## HH:MM 更新
- 完成了什么
- 关键决策
- 待办事项
EOF
git add -A && git commit -m "[memory] $(date +%Y-%m-%d) 工作记录" && git push
```

---

## 2. 协作技巧清单（实战沉淀）

以下是我们长期协作中积累的核心技巧：

### 技巧1：写-审-改闭环
所有正式文档必须经过多角色评审迭代，不一次交付。九大文体各有专属评审角色和达标标准（详见 `academic-writer-skill/SKILL.md`）。

### 技巧2：GitHub持久化
所有产出存入 books 仓库，跨会话不丢失。commit message 规范：`[类型] 描述`。断点续传：新会话说"继续"即可从上次中断处恢复。

### 技巧3：分层渐进
长文档（>1万字）分模块写作：先提纲→逐节撰写→组装→通检。25万字书稿用L4策略（50模块×5000字）。

### 技巧4：python-docx生成Word
避免JS的docx-js（中文引号转义地狱）。用python-docx，中文内容写在单独的文本文件中，Python脚本读取生成docx，规避字符串嵌套问题。

### 技巧5：审稿回复要简练
每条意见回复1-2段，说清"改了什么"就行。不堆砌、不套话。不同意的意见用"关于此问题，我们的理解是……"委婉表达。

### 技巧6：文献检索用Brave API
```bash
curl -s "https://api.search.brave.com/res/v1/web/search?q=QUERY" \
  -H "X-Subscription-Token: ${BRAVE_API_KEY}" \
  -H "Accept: application/json" | python3 -m json.tool
```
用于验证参考文献真实性、检索最新研究进展、确认标准现行有效。

### 技巧7：跨文档一致性
同一计划内多篇文档共享术语表、工程参数、符号系统。用 `check_consistency.py` 自动检查。创新点重叠不超过30%。

### 技巧8：ODD场景化思维
任何水网相关写作，都从ODD（运行设计域）角度切入：正常域→扩展域→MRC，用六维参数向量结构化表达运行边界。这是CHS理论体系的标志性方法。

### 技巧9：讨论模式→写作模式自然切换
不急于动笔。先在讨论模式中理清要素（文档类型、创新点、目标读者、结构），信息足够后输出提纲，用户确认再进入写作模式。

### 技巧10：质量关卡强制执行
初稿完成后必须运行对应的检查脚本（`run_checks.py`），参考文献验证关卡不可跳过——发现编造文献整篇打回重写。

### 技巧11：多平台内容分发
同一学术内容可适配多平台：SCI论文→中文核心→公众号科普→PPT汇报→短视频脚本。核心观点不变，表达方式按平台调整。

### 技巧12：上下文高效利用
- 长文件先看目录结构，按需读取具体章节
- 多文件任务优先读取 CLAUDE.md 或 SKILL.md 获取全局指引
- 不要一次性读完所有文件，按任务需要分步加载

---

## 3. 任务路由

根据用户指令自动路由到对应工作流：

| 用户说的话 | 动作 |
|-----------|------|
| 写论文/写SCI/写期刊 | 读取 `academic-writer-skill/SKILL.md` → SCI/CN流程 |
| 写专利 | 读取 `academic-writer-skill/SKILL.md` → PAT流程 |
| 写书/写章节/继续书稿 | 读取 `academic-writer-skill/SKILL.md` → BK流程 |
| 写报告 | 读取 `academic-writer-skill/SKILL.md` → RPT流程 |
| 写标准 | 读取 `academic-writer-skill/SKILL.md` → STD流程 |
| 写公众号/写推文 | 读取 `academic-writer-skill/SKILL.md` → WX流程 |
| 做PPT/做汇报 | 读取 `academic-writer-skill/SKILL.md` → PPT流程 |
| 审稿回复/回复审稿人 | 用python-docx生成简练回复函 |
| 继续/上次到哪了 | git pull → 读取 memory/ 和 progress.json → 断点恢复 |
| 查文献/搜论文 | 用Brave API检索 |
| 状态/进度 | 读取所有 progress.json → 输出汇总表 |

---

## 4. 文献检索工作流

```
用户需求 → Brave API搜索 → 筛选高质量来源 → 结构化输出
```

支持的检索场景：
- 验证参考文献真实性（DOI/标题）
- 检索某主题近5年进展
- 确认GB/T、ISO标准现行有效
- 查找竞争专利

---

## 5. 快速参考

### 九大文体代号
RPT(报告) | BK(书稿) | SCI(英文论文) | CN(中文论文) | PAT(专利) | STD-CN(国标) | STD-INT(国际标准) | WX(公众号) | PPT(演示)

### 关键文件路径
- 写作主指令：`books/writing-projects/CLAUDE.md`
- 九大文体技能：`books/writing-projects/academic-writer-skill/SKILL.md`
- 写作技法库：`books/writing-projects/academic-writer-skill/references/writing_craft_guide.md`
- 评分标准：`books/writing-projects/academic-writer-skill/references/scoring_rubrics.md`
- 检查脚本：`books/writing-projects/academic-writer-skill/scripts/`
- 工作记忆：`books/memory/`
- 研究素材：`books/research-materials/`
