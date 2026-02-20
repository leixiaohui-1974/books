# 工作流程参考 (Workflow Reference)

## 1. 总体工作流

```
┌──────────────────────────────────────────────────────────┐
│                     用户指令入口                           │
│  "开始SCI-P1a" / "开始专利PF2-3" / "做个PPT" / "写篇公众号"  │
│  / "写个标准" / "write ISO standard" / "继续" / "状态"       │
└──────────────────┬───────────────────────────────────────┘
                   ↓
┌──────────────────┴──────────────────┐
│          指令解析器                    │
│  识别: 文体 + 编号 + 当前进度          │
│  文体: SCI/CN/PAT/BK/RPT/           │
│        STD-CN/STD-INT/WX/PPT        │
└──────────────────┬──────────────────┘
                   ↓
┌──────────────────┴──────────────────┐
│         规格加载器                    │
│  读取: 提纲/字数/格式/目标期刊         │
│  加载: 项目配置 + 前序版本(如有)       │
└──────────────────┬──────────────────┘
                   ↓
┌──────────────────┴──────────────────┐
│         写作引擎                      │
│  参照: writing_craft_guide.md        │
│  + gold_standard_fragments.md        │
│  + 文体模板(SKILL.md §9)             │
│  长文档: §5 L1-L4分级策略             │
└──────────────────┬──────────────────┘
                   ↓
┌──────────────────┴──────────────────┐
│         自动预检(统一调度器)          │
│  run_checks.py --type {文体}        │
│  (自动运行所有适用脚本,§3矩阵)      │
└──────────────────┬──────────────────┘
                   ↓
┌──────────────────┴──────────────────┐
│         多角色评审                    │
│  加载: agents/{文体}_reviewer.md     │
│  + scoring_rubrics.md 锚点标准       │
│  + citation_style_guide.md 引用规范  │
└──────────────────┬──────────────────┘
                   ↓
              ┌────┴────┐
              │ 达标？   │
              └────┬────┘
          否 ←─────┼─────→ 是
          ↓                 ↓
    ┌─────┴─────┐    ┌─────┴─────┐
    │  修改      │    │  终稿保存   │
    │  逐条回应  │    │  更新进度   │
    │  新版本    │    │  git commit │
    └─────┬─────┘    │  提示"继续" │
          │          └───────────┘
          └→ 回到"自动预检"
```

---

## 2. 九大文体速查表

| 文体 | 评审角色 | 达标条件 | 预检脚本 | 最大迭代 |
|:----:|:---------|:---------|:---------|:--------:|
| **SCI** | Reviewer A/B/C | 连续2轮Minor/Accept | `check_paper.py --type sci` + `check_references.py` | 20 |
| **CN** | 审稿人A/B/C | 连续2轮小修/录用 | `check_paper.py --type cn` + `check_references.py` | 20 |
| **PAT** | 审查员+代理人+技术专家 | 综合≥7.5/10 | `check_patent.py` | 4 |
| **BK** | 教师+专家+工程师+国际读者 | ≥8.0且🔴=0 | `check_readability.py` + `check_references.py` | 6 |
| **RPT** | 技术审查+管理审查 | ≥7.0/10 | `check_quality.py` + `check_references.py` | 3 |
| **STD-CN** | 标准化+技术+实施方 | ≥8.0+合规100% | `check_standard.py` | 4 |
| **STD-INT** | ISO标准化+国际水利+工业界 | ≥8.0+合规100% | `check_standard.py --type int` | 4 |
| **WX** | 读者+编辑+领域专家 | ≥7.5且🔴=0 | `check_article.py` | 5 |
| **PPT** | 观众+设计+内容 | ≥7.5且🔴=0 | `check_ppt.py` | 4 |

---

## 3. 质量检查脚本矩阵

### 3.1 文体专属脚本

| 脚本 | 适用文体 | 检查项数 | 核心检查内容 |
|:-----|:---------|:--------:|:-------------|
| `check_paper.py` | SCI, CN | 14 | 结构/摘要四要素/Gap/Contribution/图表/公式/文献/结论/段落/基金 |
| `check_patent.py` | PAT | 12 | 结构/权利要求/独权/背景引用/效果/实施例/回指/术语 |
| `check_readability.py` | BK | 8 | 段落≤400字/术语释义/速览框/小结/思考题/图表间距/文献/平衡 |
| `check_article.py` | WX | 12 | 段落≤150字/句子≤70字/禁用词/标题/中英间距/加粗密度/钩子 |
| `check_ppt.py` | PPT | 10 | 每页字数/配色/字体/对比度/动画/时间分配/备注 |
| `check_standard.py` | STD-CN, STD-INT | 11 | 条文用语/引用标准现行/GB 3101-3102/术语/编号/附录 |

### 3.2 通用脚本（所有文体适用）

| 脚本 | 核心功能 |
|:-----|:---------|
| **`run_checks.py`** | **统一调度器**——自动识别文体，按正确顺序运行所有适用检查，汇总🔴/🟡/🟢 |
| `check_references.py` | 文献真实性验证/格式检查/正文-文献表交叉/自引率/近5年比 |
| `check_quality.py` | 通用质量检查(术语一致/段落/引用格式) |
| `check_consistency.py` | 跨文档一致性(CHS/WSAL/HydroOS定义一致性) |

### 3.3 推荐执行顺序

```
# 推荐方式: 统一调度器（自动识别文体+按顺序运行所有检查）
python3 scripts/run_checks.py document.md --type [sci|cn|pat|bk|rpt|std-cn|std-int|wx|ppt]

# 等价手动方式:
1. 通用检查:    check_quality.py → check_references.py
2. 文体专属:    check_{paper|patent|readability|article|ppt|standard}.py
3. 跨文档检查:  check_consistency.py (批量写作时)
```

---

## 4. 长文档工作流（BK/RPT >5万字）

```
步骤1: 估算字数 → 选择L1-L4级别(SKILL.md §5)
步骤2: 创建 modules/ 目录，按节拆分
步骤3: 逐模块生成 → 即时check_readability.py
步骤4: 组装 report_full_assembled.md
步骤5: 全文统计(字符/文献/图表/段落)
步骤6: 四角色评审
步骤7: 修改 → git commit + tag → 回到步骤3
步骤8: 达标 → docx生成(§5.5防失败协议)
```

---

## 5. 批量写作工作流

```
步骤1: 规划文档依赖图
  Batch 1: 基础理论(无依赖) → SCI-P1a, CN-C1
  Batch 2: 方法论(依赖B1) → SCI-P2, PAT-1
  Batch 3: 验证(依赖B1+B2) → SCI-P3, CN-C2
  Batch 4: 应用(依赖B1-3) → BK-ch05, RPT-01

步骤2: 按批次顺序写作
  每篇: 写初稿 → 预检脚本 → 多角色评审 → 迭代

步骤3: 批次完成后跨文档审计
  · check_consistency.py 一致性
  · 创新点重叠度检查(≤30%重叠)
  · 引用网络完整性
  · 术语一致性
```

---

## 6. GitHub持久化流程

```
每轮修改:
  git add -A && git commit -m "[{文体}-{编号}] {版本} {摘要}"

重大版本:
  git tag {版本号}  (如 v04)
  git push origin main --tags

commit message规范:
  [SCI-P1a] v03 Reviewer A/B Minor, C Accept, 综合8.2/10
  [BK-report] v04 可读性修复: 38→0超长段落, +5概念框
  [PAT-PF1] v02 独权精简12→8特征, 审查员7.8/10
```
