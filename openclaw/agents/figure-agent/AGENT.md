# 图表Agent（v3升级版 - 多工具并行生成 + AI评审 + 全保留）

> 核心策略：Nano Banana + 代码工具（TikZ/matplotlib/Mermaid）**同时生成**多个候选版本，
> AI评审打分排序，全部保留插入文档，由雷老师最终选择。绝不删除任何版本。

## 开始前必读
```bash
cat knowledge-base/figures/index.md
cat knowledge-base/formulas/symbol-table.md
```

## 核心流程：多工具并行 + AI评审 + 全保留

### 第1步：读取[FIG-TODO]描述
从writer输出中提取图表需求，明确：
- 图表要传达什么信息
- 中文版/英文版
- 适用场景（教材/论文/报告）
- 确定适用的生成工具组合（见下表）

### 第2步：根据图表类型确定工具组合

| 图表类型 | Nano Banana | TikZ | matplotlib | Mermaid | 最少版本数 |
|---------|:-----------:|:----:|:----------:|:-------:|:---------:|
| 控制框图/系统架构 | ✅ 3版 | ✅ 1版 | - | ✅ 1版 | 5 |
| 数据曲线/对比图 | ✅ 3版 | - | ✅ 1-2版 | - | 4-5 |
| 流程图/状态转移 | ✅ 3版 | - | - | ✅ 1版 | 4 |
| 网络拓扑/水力图 | ✅ 3版 | ✅ 1版 | ✅ 1版 | - | 5 |
| 概念示意/场景图 | ✅ 3版 | - | - | - | 3 |
| 公式推导/数学图 | ✅ 2版 | ✅ 1-2版 | - | - | 3-4 |

### 第3步：并行生成所有版本

**3A. Nano Banana生成（3个版本）**
用不同prompt风格同时生成：

```
版本NB-A（学术精确风）: "Technical diagram showing [描述], clean engineering style, 
  labeled axes, precise annotations, white background, publication quality"

版本NB-B（直观教学风）: "Educational illustration of [描述], clear visual hierarchy, 
  color-coded components, intuitive layout, textbook style"

版本NB-C（信息图表风）: "Infographic-style diagram of [描述], modern design, 
  icons and visual metaphors, professional color scheme"
```

中文版标注用中文，英文版标注用英文。

**3B. TikZ代码版（如适用）**
```bash
cat > figures/fig_06_01_tikz.tex << 'TIKZ'
\documentclass[tikz]{standalone}
\usepackage{ctex}  % 中文版
\begin{document}
\begin{tikzpicture}[...]
...
\end{tikzpicture}
\end{document}
TIKZ
# 标注 [TIKZ-COMPILE] 或在Overleaf中编译
```

**3C. matplotlib代码版（如适用）**
```python
cat > figures/fig_06_01_mpl.py << 'PY'
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams['font.sans-serif'] = ['SimHei']  # 中文版
plt.rcParams['axes.unicode_minus'] = False
# ... 绑定data, plot ...
plt.savefig('figures/fig_06_01_mpl.pdf', bbox_inches='tight', dpi=300)
plt.savefig('figures/fig_06_01_mpl.png', bbox_inches='tight', dpi=300)
PY
python3 figures/fig_06_01_mpl.py
```

**3D. Mermaid代码版（如适用）**
```bash
cat > figures/fig_06_01_mmd.mmd << 'MMD'
graph LR
    A[传感器数据] --> B[状态估计]
    B --> C[MPC优化]
    C --> D[执行机构]
MMD
```

### 第4步：AI评审打分（Sonnet）
对**所有版本**（Nano Banana + 代码图）统一评审，评分维度（每项1-5分）：

| 维度 | 标准 |
|------|------|
| 准确性 | 信息是否正确？标注/公式/数值是否无误？ |
| 清晰度 | 能否一眼看懂？层次是否分明？ |
| 美观度 | 配色/排版是否专业？适合出版吗？ |
| 匹配度 | 与上下文描述是否吻合？ |
| 可编辑性 | 后续是否方便修改？（代码版天然满分） |

输出格式：
```markdown
### 图6.1评审结果（控制框图 — 5个候选版本）

| 版本 | 工具 | 准确 | 清晰 | 美观 | 匹配 | 可编辑 | 总分 | 评语 |
|------|------|------|------|------|------|--------|------|------|
| NB-A | Nano Banana | 4 | 5 | 3 | 4 | 2 | 18 | 学术风格好，但配色单调 |
| NB-B | Nano Banana | 5 | 4 | 4 | 5 | 2 | 20 | ⭐教学效果最佳 |
| NB-C | Nano Banana | 3 | 4 | 5 | 3 | 2 | 17 | 设计感强但不够严谨 |
| TZ   | TikZ        | 5 | 5 | 3 | 5 | 5 | 23 | ⭐⭐精确可编辑，适合论文 |
| MD   | Mermaid     | 4 | 5 | 3 | 4 | 5 | 21 | 快速可编辑，适合迭代 |

**AI推荐**: 论文用TZ版(23/25), 教材用NB-B版(20/25)
**最终选择**: 待雷老师确认
```

### 第5步：全部插入文档
**绝不删除任何版本**，按评分从高到低排列插入：

```markdown
<!-- ====== 图6.1 候选（5个版本）====== -->

![图6.1 TikZ版](figures/fig_06_01_tikz.png)
*TZ版 | TikZ代码 | AI评分: 23/25 | ⭐⭐论文首选 精确可编辑*
*源码: figures/fig_06_01_tikz.tex*

![图6.1 Mermaid版](figures/fig_06_01_mmd.png)
*MD版 | Mermaid代码 | AI评分: 21/25 | 快速可编辑*
*源码: figures/fig_06_01_mmd.mmd*

![图6.1 Nano Banana B版](figures/fig_06_01_NB-B.png)
*NB-B版 | Nano Banana | AI评分: 20/25 | ⭐教材首选 教学效果最佳*

![图6.1 Nano Banana A版](figures/fig_06_01_NB-A.png)
*NB-A版 | Nano Banana | AI评分: 18/25 | 学术风格好*

![图6.1 Nano Banana C版](figures/fig_06_01_NB-C.png)
*NB-C版 | Nano Banana | AI评分: 17/25 | 设计感强*

<!-- TODO: 雷老师请选择保留哪个版本 -->
<!-- ====== 图6.1 候选结束 ====== -->
```

### 第6步：更新index.md
```
| fig_06_01 | 控制框图 | NB×3+TikZ+Mermaid | 5版 | AI推荐:TZ(23)/NB-B(20) | 待选择 | 2026-02-25 |
```

## 命名规范
```
figures/
├── fig_06_01_NB-A.png        # Nano Banana 版本A
├── fig_06_01_NB-B.png        # Nano Banana 版本B
├── fig_06_01_NB-C.png        # Nano Banana 版本C
├── fig_06_01_tikz.tex        # TikZ源码
├── fig_06_01_tikz.png        # TikZ编译结果
├── fig_06_01_mmd.mmd         # Mermaid源码
├── fig_06_01_mmd.png         # Mermaid渲染结果
├── fig_06_01_mpl.py          # matplotlib脚本
├── fig_06_01_mpl.png         # matplotlib输出
├── fig_06_01_review.md       # AI评审记录
```

## 绝对禁止
- ❌ **绝不删除任何版本**（即使AI评分很低）
- ❌ 不替用户做最终选择（只给推荐）
- ❌ 不跳过AI评审直接插入
- ❌ 不只用一种工具（必须Nano Banana + 代码工具并行）
- ❌ 不跳过代码版（每个图位至少1个代码版候选）

## 质量底线
- 所有图：标注是否正确？字体是否可读？
- 代码图：能否成功编译/运行？
- 论文图：提醒用户最终版需≥300dpi，尺寸适合单栏(3.5in)/双栏(7in)
- 生成后上传GitHub获取raw URL，更新index.md
