# OCAC (OpenClaw Agent Core) 使用指南 v2.0

> 集成9大学术写作技能的自动化任务执行系统

---

## 简介

OCAC是一个自动化任务执行系统，能够：
- 自动分解复杂任务为可执行子任务
- 并行执行（利用9大学术写作技能）
- 质量评估与迭代优化
- 输出管理与版本控制

---

## 9大学术写作技能集成

OCAC内置对接9大文体技能：

| 代号 | 文体 | 适用场景 | 评审角色 |
|------|------|---------|---------|
| `RPT` | 技术报告 | 项目报告、可研报告、技术方案 | 技术评审+管理评审 |
| `BK` | 书稿/专著 | 学术著作、教材章节 | 内容编辑+技术审校 |
| `SCI` | SCI英文论文 | WRR/Nature Water等国际顶刊 | 三角色评审(A/B/C) |
| `CN` | 中文核心期刊 | 水利学报/中国科学等 | 三角色评审 |
| `PAT` | 发明专利 | 中国发明专利申请 | 专利审查员模拟 |
| `STD-CN` | 国内标准 | GB/T、SL/T、行业标准 | 标准化专家 |
| `STD-INT` | 国际标准 | ISO、IEC、OGC等 | 国际标准专家 |
| `WX` | 微信公众号 | 科普/行业分析/观点输出 | 传播学专家+领域专家 |
| `PPT` | 演示文稿 | 学术汇报/项目答辩 | 设计专家+内容专家 |

---

## 快速开始

### 1. 基本用法

```bash
# 进入OCAC目录
cd /root/.openclaw/workspace/books/agent-core

# 查看帮助
python3 ocac_v2.py --help

# 列出所有任务
python3 ocac_v2.py list
```

### 2. 运行任务

#### 模式1：仅准备（不执行）
```bash
python3 ocac_v2.py run --task "生成5篇水系统控制论科普文章"
```

#### 模式2：实际执行
```bash
python3 ocac_v2.py run --task "生成5篇水系统控制论科普文章" --execute
```

#### 模式3：指定文体技能
```bash
# 使用微信公众号技能(WX)
python3 ocac_v2.py run --task "写10篇智慧水利科普文章" --skill WX --execute

# 使用书稿技能(BK)
python3 ocac_v2.py run --task "写水系统控制论第3章" --skill BK --execute

# 使用SCI论文技能
python3 ocac_v2.py run --task "写一篇关于MPC的SCI论文" --skill SCI --execute
```

---

## 典型应用场景

### 场景1：批量生成公众号文章

```bash
# 任务分解 → 并行生成 → 质量评估
python3 ocac_v2.py run \
  --task "生成50篇水系统控制论系列公众号文章，每篇1500字" \
  --skill WX \
  --execute \
  --batch-size 10
```

**执行流程**：
1. 分解为50个写作任务
2. 调用WX技能并行生成
3. 自动评估每篇文章质量
4. 不达标自动重写
5. 整合输出50篇成品

### 场景2：撰写学术书稿

```bash
# 整本书自动生成
python3 ocac_v2.py run \
  --task "撰写《水系统控制论》全书，共13章，25万字" \
  --skill BK \
  --execute
```

**执行流程**：
1. 分解为13个章节任务
2. 每章再分解为5-7个小节
3. 调用BK技能逐节撰写
4. 多轮评审迭代
5. 整合成完整书稿

### 场景3：撰写SCI论文

```bash
python3 ocac_v2.py run \
  --task "撰写一篇关于数字孪生水网的SCI论文，投稿WRR" \
  --skill SCI \
  --execute
```

**执行流程**：
1. 文献检索与综述
2. 方法论设计
3. 实验/案例分析
4. 三角色评审（Reviewer A/B/C）
5. 多轮修改直至达标

### 场景4：编写技术标准

```bash
# 国内标准
python3 ocac_v2.py run \
  --task "编写《智慧水网模型预测控制技术规范》行业标准" \
  --skill STD-CN \
  --execute

# 国际标准
python3 ocac_v2.py run \
  --task "编写ISO标准《Smart Water Network - MPC Guidelines》" \
  --skill STD-INT \
  --execute
```

---

## 高级功能

### 批量执行

```bash
# 分批执行大量任务
python3 ocac_v2.py batch \
  --id task_20260222_095444 \
  --batch-size 5
```

### 质量评估

```bash
# 评估已生成内容的quality
python3 ocac_v2.py eval --id task_20260222_095444
```

### 迭代优化

```bash
# 自动迭代直至达标
python3 ocac_v2.py run \
  --task "优化第3章内容至8分以上" \
  --skill BK \
  --execute \
  --max-iterations 6
```

---

## 输出目录结构

```
books/
├── agent-runs/           # 任务运行记录
│   ├── task_xxx_result.json
│   ├── task_xxx_workflow.json
│   └── task_xxx_subtask_N_script.py
├── agent-outputs/        # 生成的内容输出
│   ├── task_xxx_subtask_1_output.md
│   ├── task_xxx_subtask_2_output.md
│   └── ...
└── outputs/              # 最终整合输出
    ├── 书稿/
    ├── 论文/
    ├── 公众号/
    └── 标准/
```

---

## 与9大Skill的深度集成

### 写作流程

```
用户输入任务
    ↓
OCAC分解任务
    ↓
调用对应Skill（SCI/CN/WX等）
    ↓
Skill执行"写-审-改"闭环
    ↓
输出达标内容
    ↓
OCAC整合所有输出
```

### 质量保障

每个Skill内置：
- **写作技法**：参照 `references/writing_craft_guide.md`
- **金标准片段**：参照 `references/gold_standard_fragments.md`
- **评分锚点**：参照 `references/scoring_rubrics.md`

### 迭代优化

| 文体 | 最大迭代轮数 | 达标条件 |
|------|------------|---------|
| SCI/CN | 20轮 | 连续2轮"小修"或"接受" |
| PAT | 4轮 | 评分≥7.5/10 |
| BK | 6轮 | 评分≥8.0/10 |
| RPT | 3轮 | 评分≥7.0/10 |
| STD-CN/STD-INT | 4轮 | 评分≥8.0/10 + 100%合规 |
| WX | 5轮 | 评分≥7.5/10 |
| PPT | 4轮 | 评分≥7.5/10 |

---

## 实际案例

### 案例1：生成25万字书稿

```bash
$ python3 ocac_v2.py run \
    --task "撰写《水系统控制论》全书，13章，25万字" \
    --skill BK \
    --execute

🚀 OCAC 开始执行任务: task_20260222_100000
============================================================
任务: 撰写《水系统控制论》全书，13章，25万字
执行模式: 自动执行

📋 步骤1: 任务分解
   分解为 53 个子任务
   预计总时间: 3120 分钟
   预计并行时间: 3120 分钟

🔄 步骤2: 创建工作流
   工作流已保存

⚡ 步骤3: 生成执行脚本
   生成 53 个执行脚本

▶️  步骤4: 执行任务（调用BK Skill）
   ✅ 第1章绪论: success (评分: 8.5/10)
   ✅ 第2章基础理论: success (评分: 8.2/10)
   ...
   ✅ 第13章总结: success (评分: 8.0/10)

✅ 任务完成
输出: books/outputs/书稿/水系统控制论.md
字数: 253,000字
```

### 案例2：批量生成公众号文章

```bash
$ python3 ocac_v2.py run \
    --task "生成50篇水系统控制论科普文章" \
    --skill WX \
    --execute \
    --batch-size 10

📋 分解为 50 个写作任务
▶️  批次1/5: 10篇文章
   ✅ 文章1: 8.2分
   ✅ 文章2: 7.8分
   ...
▶️  批次2/5: 10篇文章
   ...
✅ 全部完成，平均评分: 7.9/10
```

---

## 注意事项

1. **执行时间**：大任务可能需要数小时，建议分批执行
2. **资源限制**：并行度受限于系统资源，默认max_workers=10
3. **质量检查**：务必运行 `eval` 检查输出质量
4. **版本控制**：所有输出自动保存到Git，方便追溯

---

## 下一步开发

- [ ] 集成真正的sessions_spawn调用（替代subprocess）
- [ ] 添加Web UI监控界面
- [ ] 支持更多数据源（数据库、API等）
- [ ] 添加任务调度功能（定时执行）

---

**最后更新**: 2026-02-22  
**版本**: v2.0  
**作者**: Kimi Claw
