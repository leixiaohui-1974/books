# 多智能体协同写作系统 v4.0

> CHS 教材/专著体系的 AI 协同写作全流程规范。
> 覆盖：模型分配、写作流程、评审机制、版本管理、成本控制。

---

## 一、模型分配策略（省 token 模式）

### 1.1 三级模型定位

| 级别 | 模型 | 定价(input/output) | 定位 | 使用占比 |
|------|------|-------------------|------|---------|
| **L1 精锐** | Opus | $15/$75 per M | 仅终审、复杂理论、关键修复 | ≤10% |
| **L2 主力** | Sonnet | $3/$15 per M | 初稿写作、扩写、评审修改 | ~60% |
| **L3 批量** | Haiku | $0.8/$4 per M | 格式检查、术语扫描、轻量评审 | ~30% |
| **L0 免费** | 本地脚本 | $0 | termcheck、book_admin、image_pipeline | 尽量多用 |

### 1.2 角色-模型映射（优化后）

| 角色 | 旧模型 | **新模型** | 理由 |
|------|--------|-----------|------|
| **DraftWriter** (初稿写作) | opus | **sonnet** | 初稿不需要最高质量，后续会评审修改 |
| **ReviewerA** (理论严谨) | opus | **sonnet** | 公式检查 sonnet 足够，真正复杂的由 Opus 终审 |
| **ReviewerB** (工程实践) | sonnet | **haiku** | 参数量级检查不需要强推理 |
| **ReviewerC** (学科交叉) | haiku | **haiku** | 保持不变 |
| **FormatChecker** (格式规范) | haiku | **本地脚本优先** | termcheck_v2 覆盖80%格式检查，剩余用 haiku |
| **Writer** (评审后修改) | opus | **sonnet** | 按评审清单修改，sonnet 够用 |
| **ConsistencyAuditor** (一致性) | sonnet | **haiku** | 跨章对比是模式匹配，haiku 可胜任 |
| **FinalReviewer** (终审) | — | **opus** | 新增角色，仅在章节定稿前调用一次 |

### 1.3 Opus 使用红线

**Opus 仅在以下场景使用**（其余一律 Sonnet/Haiku）：

1. **终审定稿** — 章节通过 Sonnet 评审后，Opus 做最终一轮检查
2. **复杂理论推导** — 涉及 CHS 八原理证明、传递函数族推导、DMPC 收敛性等
3. **跨书一致性仲裁** — 多本书之间出现概念矛盾时，Opus 裁定
4. **新理论内容创作** — 从无到有构建全新章节框架（非扩写）

**Opus 不用于**：
- ❌ 扩写已有内容（Sonnet 做）
- ❌ 格式修复、编号修复（Haiku/脚本做）
- ❌ 评审第一轮（Sonnet+Haiku 做）
- ❌ 参考文献整理（Haiku 做）

---

## 二、角色详细定义

### DraftWriter — 初稿写作
- **模型**: sonnet
- **人设**: 雷晓辉教授视角，熟悉 CHS 理论体系
- **输入**: 章节大纲 + 素材文件 + 前后章衔接段
- **输出**: 完整章节 .md 文件
- **质量要求**: 结构完整、术语正确、内容覆盖大纲要点。允许细节粗糙（后续评审修改）
- **批量模式**: 一次加载全书素材，连续写 3-5 章

### ReviewerA — 理论严谨型
- **模型**: sonnet
- **人设**: 欧洲控制论教授，40年学术经验
- **审查维度**: 公式推导、符号一致性、定理逻辑链、LaTeX 语法、学术引用
- **输出**: JSON 问题清单

### ReviewerB — 工程实践型
- **模型**: haiku
- **人设**: 美国水利工程CTO，20年SCADA/MPC经验
- **审查维度**: 工程参数量级、SCADA可行性、案例数据真实性、方案可操作性
- **输出**: JSON 问题清单

### ReviewerC — 学科交叉型
- **模型**: haiku
- **人设**: 亚洲AI+水利带头人，Nature编委
- **审查维度**: 跨学科准确性、创新性、术语翻译、可读性
- **输出**: JSON 问题清单

### FormatChecker — 格式规范型
- **模型**: 本地脚本(termcheck_v2.py) + haiku(补充)
- **工作流**:
  1. 先运行 `termcheck_v2.py --json` （0 token）
  2. termcheck 无法覆盖的项（如图表描述质量、段落衔接）用 haiku 补充
- **输出**: JSON 问题清单

### Writer — 评审修改型
- **模型**: sonnet
- **输入**: 原文 + 评审问题清单
- **工作模式**: 逐条修改，Critical 全部解决，Major 实质回应，Minor 全部修正
- **输出**: 修改后的完整 .md 文件

### FinalReviewer — 终审定稿（新增）
- **模型**: opus
- **触发条件**: 章节已通过 Sonnet 评审 + termcheck PASS
- **审查重点**: 理论深度、论证严密性、与 P1a 论文的一致性、全书叙事连贯性
- **输出**: Accept / Minor Revision / Major Revision
- **规则**: 一章只调用一次 Opus 终审。Minor 问题由 Sonnet 修改，不再回 Opus

### ConsistencyAuditor — 一致性审核
- **模型**: haiku
- **工作模式**: 跨章术语、工程数据、概念定义对比
- **输出**: 不一致项清单

---

## 三、写作流水线（单章完整流程）

```
Phase 1: 准备（0 token）
  ├─ book_admin.py status {BOOK} → 确认文件状态
  ├─ termcheck_v2.py → 基线检查
  └─ 读取 book_manifest.json → 确定目标文件

Phase 2: 初稿（Sonnet, ~20k output tokens/万字）
  └─ DraftWriter(sonnet): 素材 + 大纲 → ch_draft.md

Phase 3: 并行评审（Haiku×2 + Sonnet×1, ~12k input + ~6k output）
  ├─ ReviewerA(sonnet): 理论检查 → issues_A.json
  ├─ ReviewerB(haiku):  工程检查 → issues_B.json
  └─ ReviewerC(haiku):  交叉检查 → issues_C.json

Phase 4: 修改（Sonnet, ~15k output tokens）
  ├─ Writer(sonnet): 合并问题清单 → 逐条修改
  └─ termcheck_v2.py: 格式复查（0 token）

Phase 5: 终审（Opus, ~5k output tokens）— 仅一次
  └─ FinalReviewer(opus): 最终把关 → Accept/Revision

Phase 6: 收尾（0 token）
  ├─ book_admin.py promote → 版本管理
  ├─ termcheck_v2.py → 终验
  └─ book_manifest.json 自动更新
```

**单章 token 消耗估算（1万字章节）**:

| 阶段 | 模型 | 输入 | 输出 | 成本 |
|------|------|------|------|------|
| 初稿 | Sonnet | 30k | 15k | $0.31 |
| 评审×3 | S+H+H | 45k | 9k | $0.21 |
| 修改 | Sonnet | 20k | 10k | $0.21 |
| 终审 | Opus | 15k | 3k | $0.45 |
| **单章合计** | | **110k** | **37k** | **~$1.18** |

**对比旧方案（全 Opus）: ~$3.60/章 → 节省 67%**

---

## 四、批量写作协议（减少上下文浪费）

### 4.1 核心原则：一次加载，连续输出

传统做法每写一章都要重新加载上下文（CLAUDE.md + 术语表 + 素材），浪费大量 input token。
批量模式下，一个 Sonnet agent 一次性加载共享上下文，连续写 3-5 章。

### 4.2 批量写作模板

```
启动 DraftWriter Agent (sonnet, max_turns=30):

你是CHS教材写作助手。请依次完成以下章节的初稿写作。

【共享上下文】
- 书目: {BOOK_ID}
- 术语表: （附上核心术语20条）
- 符号表: （附上核心符号15个）
- 写作风格: （附上该书的风格要求）
- 前序章节尾段: （附上上一章最后500字）

【任务清单】
1. 写 ch{N}.md: 标题={title}, 目标字数={target}, 大纲={outline}
2. 写 ch{N+1}.md: ...
3. 写 ch{N+2}.md: ...

每章写完后，用 Write 工具保存到 books/{BOOK_ID}/ 目录。
章节之间注意衔接：每章开头回顾上章结论，结尾预告下章。
```

### 4.3 批量评审模板

```
启动 ReviewerB Agent (haiku, max_turns=20):

你是工程实践型评审专家。请依次评审以下章节。

【评审标准】（附上评审维度）

【任务清单】
1. 读取 books/{BOOK_ID}/ch{N}.md → 输出 issues_B_ch{N}.json
2. 读取 books/{BOOK_ID}/ch{N+1}.md → 输出 issues_B_ch{N+1}.json
3. ...

每章输出独立的 JSON 问题清单，格式如下：
{标准格式}
```

### 4.4 token 节省估算

| 场景 | 单章模式 | 批量模式(5章) | 节省 |
|------|---------|-------------|------|
| 共享上下文加载 | 5×30k = 150k | 1×30k = 30k | 80% input |
| 评审上下文加载 | 5×15k = 75k | 1×15k = 15k | 80% input |
| **5章总 input** | **~550k** | **~280k** | **~50%** |

---

## 五、标准化输出格式

### 问题清单条目
```json
{
  "id": "CR-{书名}-{章号}-{序号}",
  "chapter": "ch05",
  "location": "§5.2 第43行",
  "type": "交叉引用|术语|编号|内容|逻辑|格式|公式|数据",
  "severity": "Critical|Major|Minor",
  "description": "具体问题描述",
  "current_text": "当前文本（问题段落）",
  "suggested_fix": "建议修改",
  "reviewer": "A|B|C|F"
}
```

### 章节评分
```json
{
  "chapter": "ch05",
  "reviewer": "A",
  "scores": {"accuracy": 8, "completeness": 7, "consistency": 6, "readability": 8, "innovation": 7},
  "overall": 7.2,
  "critical_count": 1,
  "major_count": 3,
  "minor_count": 5,
  "verdict": "Major Revision"
}
```

---

## 六、质量红线（不可妥协）

1. **交叉引用**: "见第X章§Y.Z"必须指向实际存在的章节
2. **术语表**: 每章术语§编号必须指向本章
3. **参考文献**: [X-Y]必须在本章参考文献列表有对应条目
4. **公式编号**: (X-Y)中X必须等于章号
5. **图表编号**: 图X-Y/表X-Y中X必须等于章号
6. **数据一致性**: 同一工程参数跨章必须一致
7. **符号一致性**: 以P1a论文符号表为准

---

## 七、版本管理协议（book_admin 工作流）

### 7.1 目录规范

```
books/{BOOK_ID}/
├── ch01_final.md          ← 当前版本（根目录只放当前版本）
├── ch02_final.md
├── ...
├── book_manifest.json     ← AI agent 的权威文件清单
├── _archive/              ← 旧版归档（隔离区）
│   ├── ch01_v1.md
│   └── ...
└── H/                     ← 图片目录
```

### 7.2 工具链

```bash
python3 scripts/book_admin.py status   {BOOK}          # 查看状态
python3 scripts/book_admin.py archive  {BOOK}          # 归档旧版
python3 scripts/book_admin.py promote  {BOOK} file.md  # 提升新版
python3 scripts/book_admin.py manifest {BOOK}          # 重建清单
python3 scripts/book_admin.py list     {BOOK} --json   # 当前文件列表
python3 scripts/book_admin.py check-all                # 全局总览
python3 scripts/book_admin.py clean    {BOOK} --dry-run # 预览清理
```

### 7.3 Agent 启动前置检查（强制）

```
Step 1: 读取 book_manifest.json → 只操作 current_files
Step 2: book_admin.py status → 确认 stale=0
Step 3: termcheck_v2.py --json → 记录基线
```

### 7.4 防误操作规则

| 规则 | 说明 |
|------|------|
| 只改根目录文件 | 不得修改 `_archive/` 中的文件 |
| 先读 manifest | 不确定版本时，读 `book_manifest.json` |
| 归档不删除 | `archive` 只移动，`clean` 需 `--confirm` |
| promote 自动归档 | 新版提升时旧版自动归档 |
| termcheck 前后对比 | 修改前后都运行，确保不引入新问题 |

---

## 八、成本控制与监控

### 8.1 每批预算规划

| 批次 | 书目 | 预估章数 | 预估成本 | 策略 |
|------|------|---------|---------|------|
| 第1批 | M5精编+M6精编+M4扩写 | 30 | ~$30 | 已有大量内容，以修改为主 |
| 第2批 | T2a 16章扩写 | 16 | ~$80 | 素材充分，Sonnet 批量写 |
| 第3批 | T2b 14章扩写 | 14 | ~$70 | 同上 |
| 第4批 | M1+M2+M3 | 32 | ~$60 | 理论章节，需适量 Opus |
| 第5批 | M7+M8+M9+M10 | 46 | ~$80 | M8有工程素材可复用 |
| 第6批 | T1-EN 扩写 | 6 | ~$30 | 基于T1-CN翻译+改写 |
| **总计** | | **~144章** | **~$350** | |

### 8.2 token 优化检查清单

每次启动写作前确认：
- [ ] 使用批量模式（3-5章/agent）？
- [ ] 初稿用 Sonnet（非 Opus）？
- [ ] 评审用 Haiku（非 Sonnet）？
- [ ] 格式检查先跑本地脚本（termcheck）？
- [ ] Opus 仅用于终审（每章最多1次）？
- [ ] 共享上下文已精简（<5k tokens）？

### 8.3 各模型 token 上限建议

| 操作 | 模型 | 单次 input 上限 | 单次 output 上限 |
|------|------|----------------|-----------------|
| 写初稿 | Sonnet | 40k | 20k |
| 评审 | Haiku | 20k | 5k |
| 修改 | Sonnet | 30k | 15k |
| 终审 | Opus | 20k | 5k |

---

## 九、评审维度权重

| 维度 | 权重 | 检查项 | 主要承担者 |
|------|------|--------|-----------|
| 内容准确性 | 25% | 工程数据、公式推导、技术参数 | ReviewerA(sonnet) |
| 交叉引用 | 20% | §X.Y指向、章间关系 | termcheck(本地) |
| 术语一致性 | 15% | 核心术语全书统一 | termcheck(本地) |
| 编号连续性 | 15% | 图/表/公式/参考文献编号 | termcheck(本地) |
| 逻辑完整性 | 15% | 论证链条、章间衔接 | ReviewerA(sonnet) |
| 格式规范 | 10% | Markdown、图片链接、表格 | FormatChecker(haiku) |

**注意**: 交叉引用+术语+编号（共50%权重）由本地脚本覆盖，0 token。

---

**版本**: 4.0
**更新日期**: 2026-02-27
**变更记录**:
- v4.0: 重构模型分配（省token模式）、新增批量写作协议、成本控制框架
- v3.0: 新增版本管理协议（book_admin）
- v2.0: 初版多角色评审定义
