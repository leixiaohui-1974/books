# 学术写作完全指南

> 创建时间：2026-02-22  
> 适用范围：SCI 论文/中文核心/发明专利/书稿/技术报告  
> 目标：掌握所有学术写作技能和标准规范

---

## 一、文献检索与管理

### 1.1 文献检索数据库

#### 英文文献

| 数据库 | 网址 | 特点 | 适用领域 |
|--------|------|------|---------|
| Web of Science | webofscience.com | 最权威，SCI/SSCI 收录 | 全学科 |
| Scopus | scopus.com | 覆盖广，引用分析强 | 全学科 |
| Google Scholar | scholar.google.com | 免费，覆盖最全 | 全学科 |
| IEEE Xplore | ieeexplore.ieee.org | 工程/计算机 | 工程技术 |
| ScienceDirect | sciencedirect.com | Elsevier 期刊 | 理工医 |
| SpringerLink | link.springer.com | Springer 期刊/图书 | 理工 |
| Wiley Online | onlinelibrary.wiley.com | Wiley 期刊 | 全学科 |
| PubMed | pubmed.ncbi.nlm.nih.gov | 生物医学 | 医学/生物 |
| arXiv | arxiv.org | 预印本 | 物理/CS/数学 |

#### 中文文献

| 数据库 | 网址 | 特点 |
|--------|------|------|
| 中国知网 (CNKI) | cnki.net | 最全面，期刊/学位论文 |
| 万方数据 | wanfangdata.com.cn | 期刊/会议/专利 |
| 维普网 | cqvip.com | 期刊为主 |
| 超星发现 | chaoxing.com | 图书/期刊 |

### 1.2 检索策略

#### 布尔逻辑检索

```
# 基本运算符
AND - 与 (缩小范围)
OR - 或 (扩大范围)
NOT - 非 (排除)

# 示例
("water system" OR "hydraulic system") AND ("control" OR "automation")
"model predictive control" NOT "chemical"
```

#### 高级检索技巧

```
# 精确匹配（短语检索）
"cyber-physical systems"

# 通配符
control*  # control, controls, controlled, controlling
wom?n     # woman, women

# 字段限定
TI="water network"    # 标题
AB="optimization"     # 摘要
AU="Smith J"          # 作者
SO="Water Resources Research"  # 期刊名
PY=2023               # 出版年份

# 组合检索
TI=("smart water" OR "intelligent water") AND AB=(optimization OR control)
```

### 1.3 文献管理软件

#### EndNote

```
# 安装
https://endnote.com/

# 基本用法
1. 创建文献库 (.enl 文件)
2. 导入文献（支持 PDF 自动识别）
3. 在 Word 中插入引用（Cite While You Write 插件）
4. 选择期刊格式，自动生成参考文献

# 批量导入
File → Import → File/Online Search
```

#### Zotero（免费推荐）

```bash
# 安装
# 访问 zotero.org 下载客户端
# 安装浏览器插件（Chrome/Firefox）

# 基本用法
1. 浏览器插件一键保存网页/PDF
2. 自动抓取元数据
3. Word/LibreOffice 插件插入引用
4. 支持 10000+ 引用格式

# 命令行同步
zotero --sync
```

#### Mendeley

```
# 特点
- 免费（2GB 云存储）
- PDF 管理和标注
- 社交功能（发现相关研究）
- Word 插件

# 安装
https://www.mendeley.com/download-reference-manager/
```

### 1.4 文献阅读笔记模板

```markdown
# 文献笔记

## 基本信息
- **标题**: 
- **作者**: 
- **期刊/会议**: 
- **年份**: 
- **DOI**: 
- **链接**: 

## 研究问题
- 核心问题是什么？
- 为什么重要？

## 方法
- 使用了什么方法？
- 创新点在哪里？

## 主要发现
- 关键结论是什么？
- 数据支持是否充分？

## 局限性
- 作者承认的局限？
- 我发现的不足？

## 启发与应用
- 对我的研究有什么启发？
- 可以引用到论文的哪个部分？
- 可以扩展的方向？

## 金句摘录
> （原文引用，标注页码）

## 关联文献
- 与哪些文献相关？
- 支持/反驳了哪些研究？
```

---

## 二、SCI 论文写作

### 2.1 SCI 论文结构（IMRaD）

```
Title (标题)
Abstract (摘要)
Keywords (关键词)

1. Introduction (引言)
2. Methods (方法)
3. Results (结果)
4. and Discussion (讨论)

5. Conclusion (结论)
Acknowledgements (致谢)
References (参考文献)
Supplementary Material (补充材料)
```

### 2.2 各部分写作要点

#### 标题 (Title)

**要求**：
- 准确反映研究内容
- 简洁（15-20 词）
- 包含关键词
- 避免缩写和行话

**模板**：
```
- [方法] for [问题] in [领域]: A Case Study of [案例]
- A Novel [方法] Approach to [问题]
- [因素 1] and [因素 2] Affect [结果] in [系统]
- Machine Learning-Based [任务] for [应用]

示例:
"Model Predictive Control for Water Distribution Networks: 
A Case Study of the Jiaodong Water Transfer Project"
```

#### 摘要 (Abstract)

**结构**（150-250 词）：
```
1. 背景 (1-2 句): 研究领域和重要性
2. 问题 (1 句): 现有研究的不足
3. 方法 (2-3 句): 本文提出的方法
4. 结果 (2-3 句): 主要发现和量化指标
5. 结论 (1 句): 意义和贡献
```

**示例**：
```
Background: Water distribution networks face increasing challenges 
in efficient operation under multi-constraint conditions.

Problem: Existing control strategies often fail to handle the 
coupled hydraulic and power constraints in cascade hydropower stations.

Methods: This study proposes a bi-level dynamic programming 
successive approximation (BDPSA) algorithm for economic dispatch 
of the Pubugou-Shenxigou-Zhentou cascade.

Results: The proposed method reduced computation time by 67% 
compared to traditional approaches, while maintaining 99.2% 
load tracking accuracy.

Conclusion: The BDPSA algorithm provides an effective solution 
for real-time optimal operation of cascade hydropower stations.
```

#### 引言 (Introduction)

**结构**（3-5 段）：
```
段落 1: 研究背景和大环境
段落 2: 文献综述（现有研究）
段落 3: 研究空白（Gap）
段落 4: 本文贡献
段落 5: 论文结构（可选）
```

**常用句型**：
```
- Recent advances in [领域] have led to...
- However, existing methods suffer from...
- To address this gap, we propose...
- The main contributions of this paper are:
  1) ...
  2) ...
  3) ...
- The remainder of this paper is organized as follows...
```

#### 方法 (Methods)

**内容**：
```
- 研究区域/对象描述
- 数据来源和预处理
- 理论框架/模型
- 算法步骤（伪代码）
- 实验设计
- 评估指标
```

**写作技巧**：
- 使用公式编号
- 提供算法伪代码
- 包含流程图
- 说明参数设置依据

#### 结果 (Results)

**要求**：
- 客观描述，不解释
- 使用图表展示
- 突出关键发现
- 包含统计显著性

**常用句型**：
```
- Figure X shows that...
- As can be seen from Table Y...
- The results indicate/demonstrate/reveal...
- Compared with [基线], our method achieved...
- The improvement was statistically significant (p < 0.05)
```

#### 讨论 (Discussion)

**内容**：
```
- 结果的含义
- 与前人研究的对比
- 可能的解释
- 局限性
- 实际应用价值
```

**常用句型**：
```
- Our findings are consistent with [文献]...
- In contrast to [文献], we observed...
- This discrepancy may be attributed to...
- The practical implications of these findings are...
- Several limitations should be noted...
```

#### 结论 (Conclusion)

**结构**：
```
1. 重申主要发现（不重复摘要）
2. 强调贡献和创新
3. 指出局限性
4. 展望未来研究
```

**避免**：
- ❌ 引入新信息
- ❌ 过度夸大
- ❌ 简单复制摘要

### 2.3 图表制作规范

#### 图 (Figures)

**要求**：
- 分辨率 ≥ 300 DPI
- 格式：TIFF/EPS/PDF
- 尺寸：单栏 8.5cm，双栏 17cm
- 字体：Arial/Helvetica 8-10pt

**配色方案**：
```
# 推荐色盲友好配色
蓝色系：#1f77b4, #7f7f7f, #bcbd22, #17becf
橙色系：#ff7f0e, #2ca02c, #d62728, #9467bd

# 避免
红绿对比（色盲无法区分）
```

#### 表 (Tables)

**规范**：
```
- 使用三线表（顶线、底线粗，栏目线细）
- 表头清晰，单位标注
- 数据对齐（数字右对齐，文字左对齐）
- 显著性标记（* p<0.05, ** p<0.01, *** p<0.001）
```

**LaTeX 示例**：
```latex
\begin{table}[htbp]
  \centering
  \caption{实验结果对比}
  \begin{tabular}{lccc}
    \toprule
    方法 & 精度 (\%) & 召回率 (\%) & F1 分数 \\
    \midrule
    基线 & 75.2 & 68.5 & 71.7 \\
    方法 A & 82.1* & 79.3* & 80.7* \\
    本文方法 & \textbf{89.4} & \textbf{86.2} & \textbf{87.8} \\
    \bottomrule
  \end{tabular}
  \label{tab:results}
\end{table}
```

### 2.4 参考文献格式

#### GB/T 7714-2015（中国标准）

```
# 期刊论文
[序号] 作者。题名 [J]. 期刊名，年，卷 (期): 起止页码.

示例:
[1] 雷晓辉，龙岩，许慧敏，等。水系统控制论：提出背景、技术框架与研究范式 [J]. 
    南水北调与水利科技 (中英文), 2025, 23(04): 761-769.

# 专著
[序号] 作者。书名 [M]. 版本。出版地：出版者，出版年.

示例:
[2] 钱学森。工程控制论 [M]. 北京：科学出版社，1954.

# 学位论文
[序号] 作者。题名 [D]. 保存地：保存单位，年份.

示例:
[3] 张三。智能水网优化控制研究 [D]. 北京：清华大学，2023.

# 会议论文
[序号] 作者。题名 [C]//会议录名。出版地：出版者，年份：起止页码.

# 专利
[序号] 申请者。专利名：专利号 [P]. 公告日期.

# 标准
[序号] 标准编号，标准名称 [S].

# 电子资源
[序号] 作者。题名 [EB/OL]. (更新日期)[引用日期]. 网址.
```

#### APA 格式（第 7 版）

```
# 期刊论文
Author, A. A., & Author, B. B. (Year). Title of article. 
Title of Journal, volume(issue), pages. DOI

示例:
Lei, X., Long, Y., & Xu, H. (2025). Cybernetics of Hydro Systems: 
Background, framework, and research paradigm. 
South-to-North Water Transfers and Water Science & Technology, 
23(4), 761-769. https://doi.org/10.13476/j.cnki.nsbdqk.2025.0077

# 专著
Author, A. A. (Year). Title of work. Publisher.

# 学位论文
Author, A. A. (Year). Title of dissertation [Doctoral dissertation, 
University Name]. Database Name.
```

#### IEEE 格式

```
# 期刊论文
[1] A. A. Author and B. B. Author, "Title of article," 
    Abbrev. Title of Period., vol. x, no. x, pp. xxx-xxx, Abbrev. Month, Year.

# 会议论文
[2] A. A. Author, "Title of paper," in Abbreviated Name of Conf., City of Conf., 
    Abbrev. State (if given), Country, Year, pp. xxxx-xxxx.

# 专著
[3] A. A. Author, Title of Book. xth ed. City of Publisher: Publisher, Year.
```

### 2.5 投稿流程

#### 选刊策略

```
# 考虑因素
1. 研究领域匹配度
2. 影响因子 (IF) 和分区 (Q1-Q4)
3. 审稿周期
4. 版面费 (OA 期刊)
5. 录用率

# 选刊工具
- Web of Science Journal Citation Reports (JCR)
- Elsevier Journal Finder
- Springer Journal Suggester
- LetPub (中文)
```

#### 投稿材料

```
1. 主文稿 (Manuscript)
2. 封面信 (Cover Letter)
3. 亮点说明 (Highlights)
4. 图表文件 (Figures/Tables)
5. 补充材料 (Supplementary Material)
6. 推荐审稿人 (3-5 人)
7. 利益冲突声明
```

#### 封面信模板

```
[日期]

Dear Editor [编辑姓名],

We are pleased to submit our manuscript entitled "[论文标题]" 
for consideration for publication in [期刊名].

[研究重要性 - 2-3 句]
Our study addresses [研究问题], which is critical for [领域].

[主要发现 - 2-3 句]
We demonstrate that [主要发现 1]. Furthermore, [主要发现 2].

[创新点 - 1-2 句]
This work is novel because [创新点].

We confirm that this manuscript has not been published elsewhere 
and is not under consideration by another journal.

All authors have approved the manuscript and agree with its submission.

Thank you for your consideration.

Sincerely,
[通讯作者姓名]
[单位]
[邮箱]
```

#### 审稿意见回复

```
# 回复信结构
1. 感谢编辑和审稿人
2. 逐条回复意见
3. 标注修改位置

# 回复模板
Response to Reviewer #1:

Comment 1: [复制审稿人意见]

Response: We thank the reviewer for this insightful comment. 
We have [说明修改]. This change can be found on page X, line Y.

[如有不同意见，礼貌解释]
We respectfully disagree with this point because [理由]. 
However, to clarify, we have [折中方案].
```

---

## 三、中文核心期刊写作

### 3.1 中文论文结构

```
标题 (≤20 字)
作者姓名，单位
摘要 (200-300 字)
关键词 (3-8 个)

0 引言
1 一级标题
  1.1 二级标题
    1.1.1 三级标题
2 研究方法
3 结果与分析
4 讨论
5 结论

参考文献
```

### 3.2 中文写作规范

#### 数字用法

```
# 使用阿拉伯数字
- 公历世纪、年代、年、月、日、时
- 计数和计量
- 型号、编号

示例:
20 世纪 90 年代
2026 年 2 月 22 日
3 次实验
图 1、表 2、式 (3)

# 使用汉字数字
- 定型的词、词组、成语
- 相邻两个数字连用表示概数
- 带有"几"字的数字

示例:
一方面、三叶草、星期五
三四天、几十、几百
```

#### 量和单位

```
# 使用法定计量单位
长度：m, km, cm, mm
质量：kg, g, mg
时间：s, min, h, d
体积：m³, L, mL
压力：Pa, kPa, MPa
流量：m³/s, L/s

# 错误示例
❌ 5 公斤 → ✅ 5 kg
❌ 100 公里 → ✅ 100 km
❌ 30 秒 → ✅ 30 s
```

#### 图表规范

```
# 图
- 图序、图题居中置于图下方
- 坐标轴标注：物理量/单位
- 图例清晰

示例:
图 1 系统架构图
水位/m
流量/(m³·s⁻¹)

# 表
- 表序、表题居中置于表上方
- 使用三线表
- 同一栏数据位数对齐

示例:
表 1 实验参数设置
```

### 3.3 中文核心期刊推荐

#### 水利类

| 期刊名 | 影响因子 | 分区 | 审稿周期 |
|--------|---------|------|---------|
| 水利学报 | 2.5+ | EI | 3-6 月 |
| 水科学进展 | 2.3+ | EI | 3-6 月 |
| 水力发电学报 | 1.8+ | EI | 2-4 月 |
| 水利水电科技进展 | 1.5+ | 核心 | 2-3 月 |
| 南水北调与水利科技 | 1.6+ | 核心 | 1-3 月 |

#### 自动化类

| 期刊名 | 影响因子 | 分区 | 审稿周期 |
|--------|---------|------|---------|
| 自动化学报 | 3.0+ | EI | 4-8 月 |
| 控制与决策 | 2.2+ | EI | 3-6 月 |
| 控制工程 | 1.5+ | 核心 | 2-4 月 |

---

## 四、发明专利撰写

### 4.1 专利类型

| 类型 | 保护对象 | 保护期 | 审查周期 |
|------|---------|--------|---------|
| 发明专利 | 方法、产品、改进 | 20 年 | 18-36 月 |
| 实用新型 | 产品形状、构造 | 10 年 | 6-12 月 |
| 外观设计 | 产品外观 | 15 年 | 4-6 月 |

### 4.2 发明专利结构

```
1. 发明名称
2. 技术领域
3. 背景技术
4. 发明内容
   - 要解决的技术问题
   - 技术方案
   - 有益效果
5. 附图说明
6. 具体实施方式
7. 权利要求书
8. 摘要
9. 摘要附图
```

### 4.3 各部分写作要点

#### 发明名称

**要求**：
- 准确、简明（≤25 字）
- 体现发明主题
- 避免广告用语

**示例**：
```
❌ 一种世界领先的智能水网控制系统
✅ 一种基于模型预测控制的水网优化调度方法
```

#### 技术领域

**模板**：
```
本发明涉及 [技术领域]，具体涉及 [具体方向]。

示例:
本发明涉及水利工程自动化技术领域，
具体涉及一种基于模型预测控制的水网优化调度方法。
```

#### 背景技术

**内容**：
```
1. 介绍相关技术现状
2. 指出现有技术的不足
3. 引证相关专利/文献

写作技巧:
- 客观描述，不贬低
- 明确指出技术问题
- 为发明内容做铺垫
```

#### 发明内容

**结构**：
```
【要解决的技术问题】
本发明要解决的技术问题是 [问题描述]。

【技术方案】
为解决上述技术问题，本发明采用如下技术方案：

[独立权利要求 1]
一种 [产品名称/方法名称]，其特征在于，包括：
- 部件/步骤 A
- 部件/步骤 B
- 部件/步骤 C

[从属权利要求 2-N]
根据权利要求 1 所述的 [产品名称/方法名称]，
其特征在于，所述 [部件 A] 进一步包括 [细节]。

【有益效果】
与现有技术相比，本发明具有以下有益效果：
1) [效果 1，最好量化]
2) [效果 2]
3) [效果 3]
```

#### 附图说明

```
图 1 为本发明实施例 1 的系统架构图；
图 2 为本发明实施例 1 的流程图；
图 3 为本发明实施例 2 的 [具体名称]；
...
```

#### 具体实施方式

**要求**：
- 详细、完整
- 本领域技术人员可实现
- 提供多个实施例
- 包含实验数据

**模板**：
```
实施例 1

[系统/设备组成]
如图 1 所示，本实施例提供一种 [系统名称]，包括：
- 模块 A，用于 [功能]
- 模块 B，用于 [功能]
- 模块 C，用于 [功能]

[工作流程]
本实施例的工作流程如下：
步骤 S1: [详细描述]
步骤 S2: [详细描述]
...

[实验验证]
为验证本发明效果，进行了以下实验：
[实验设计]
[实验结果，包含数据对比]
[结论]
```

#### 权利要求书（最重要！）

**结构**：
```
1. 一种 [产品名称/方法名称]，其特征在于，包括：
   [必要技术特征 A]；
   [必要技术特征 B]；
   [必要技术特征 C]。

2. 根据权利要求 1 所述的 [产品名称/方法名称]，
   其特征在于，所述 [特征 A] 进一步包括 [细节]。

3. 根据权利要求 1 所述的 [产品名称/方法名称]，
   其特征在于，还包括 [可选特征 D]。
...
```

**撰写技巧**：
- 独立权利要求 1：范围尽可能宽
- 从属权利要求：逐步细化，形成保护梯度
- 使用"其特征在于"区分前序和特征部分
- 避免使用"约"、"左右"等模糊词汇

#### 摘要

**要求**：
- ≤300 字
- 包含技术问题、方案要点、主要用途
- 不写入权利要求

**模板**：
```
本发明公开了一种 [产品名称/方法名称]，
包括 [主要部件/步骤 A、B、C]。
本发明通过 [技术手段]，实现了 [技术效果]。
实验表明，[量化指标]。
本发明适用于 [应用领域]。
```

### 4.4 专利检索

#### 检索数据库

| 数据库 | 网址 | 特点 |
|--------|------|------|
| 中国专利公布公告 | cpquery.cnipa.gov.cn | 中国专利 |
| 国家知识产权局 | pss-system.cnipa.gov.cn | 检索分析 |
| Google Patents | patents.google.com | 全球专利 |
| USPTO | uspto.gov | 美国专利 |
| EPO | epo.org | 欧洲专利 |
| WIPO | wipo.int | PCT 国际专利 |

#### 检索策略

```
# 关键词检索
("水网" OR "水系统") AND ("控制" OR "调度") AND "预测"

# IPC 分类号检索
IPC = E03B  (供水工程)
IPC = G05B  (控制系统)
IPC = G06Q  (管理系统)

# 组合检索
(TI="模型预测" OR AB="MPC") AND IPC=G05B
```

### 4.5 专利答复审查意见

#### 常见审查意见

```
1. 新颖性问题
   - 找到区别技术特征
   - 强调技术效果差异

2. 创造性问题
   - 论证非显而易见性
   - 提供实验数据支持
   - 强调技术偏见

3. 清楚性问题
   - 修改模糊表述
   - 增加具体实施细节
```

#### 答复模板

```
关于权利要求 1 的创造性

审查员认为权利要求 1 相对于对比文件 1 不具备创造性。

申请人 respectfully disagree，理由如下：

1. 区别技术特征
权利要求 1 包含 [特征 X]，而对比文件 1 未公开该特征。

2. 技术效果
[特征 X] 带来了 [效果 Y]，如实施例数据所示（表 1）。

3. 非显而易见性
[特征 X] 并非本领域公知常识，对比文件 2 也未给出技术启示。

综上，权利要求 1 具备专利法第 22 条第 3 款规定的创造性。
```

---

## 五、技术书稿写作

### 5.1 书稿结构

```
前言/序言
目录

第 1 部分 基础理论
  第 1 章 绪论
    - 引导案例
    - 本章目标
    - 正文内容
    - 本章小结
    - 思考题
    - 参考文献

第 2 部分 技术方法
  ...

第 3 部分 工程实践
  ...

第 4 部分 展望
  ...

附录
术语表
索引
```

### 5.2 章节写作规范

#### 章节长度

```
- 单章：1.5-2.5 万字
- 单节：3000-5000 字
- 单小节：1000-2000 字
```

#### 图表配置

```
- 每章：图 5-8 幅，表 3-5 个
- 图表比：约 2:1
- 图表位置：紧跟首次引用处
```

#### 写作风格

```
# 教材类
- 语言通俗易懂
- 多举例、多类比
- 循序渐进

# 专著类
- 专业术语准确
- 理论推导严谨
- 创新点突出

# 科普类
- 故事化叙述
- 避免公式
- 图文并茂
```

### 5.3 出版流程

```
1. 选题申报（1-2 月）
2. 大纲评审（1 月）
3. 书稿撰写（3-6 月）
4. 三审三校（2-3 月）
5. 排版设计（1 月）
6. 印刷出版（1 月）

总计：9-15 月
```

---

## 六、技术报告写作

### 6.1 报告类型

| 类型 | 用途 | 篇幅 | 特点 |
|------|------|------|------|
| 可行性研究报告 | 立项决策 | 50-100 页 | 数据详实、论证充分 |
| 技术方案报告 | 方案比选 | 30-50 页 | 多方案对比 |
| 测试报告 | 性能验证 | 20-40 页 | 数据为主 |
| 验收报告 | 项目结题 | 40-80 页 | 全面总结 |
| 调研报告 | 现状分析 | 20-50 页 | 问题导向 |

### 6.2 报告结构

```
封面
摘要
目录

1 概述
  1.1 项目背景
  1.2 报告目的
  1.3 研究范围
  1.4 技术路线

2 现状分析
  2.1 国内外现状
  2.2 存在问题
  2.3 需求分析

3 技术方案
  3.1 方案一
  3.2 方案二
  3.3 方案比选

4 实施计划
  4.1 进度安排
  4.2 资源配置
  4.3 风险分析

5 投资估算
  5.1 估算依据
  5.2 费用构成
  5.3 效益分析

6 结论与建议

参考文献
附录
```

---

## 七、写作工具推荐

### 7.1 文献管理

- **EndNote**: 功能最强，收费
- **Zotero**: 免费，开源，推荐
- **Mendeley**: 免费，社交功能
- **NoteExpress**: 中文支持好

### 7.2 写作工具

- **LaTeX**: 科技论文首选
- **Overleaf**: 在线 LaTeX 编辑器
- **Word**: 通用，配合 EndNote
- **Markdown**: 书稿/报告，轻量级
- **Typora**: Markdown 编辑器

### 7.3 语法检查

- **Grammarly**: 英文语法检查
- **Hemingway**: 英文可读性
- **秘塔写作猫**: 中文语法检查
- **CNKI 写作助手**: 学术规范检查

### 7.4 图表工具

- **Origin**: 科研绘图
- **MATLAB**: 数据可视化
- **Python (Matplotlib/Seaborn)**: 编程绘图
- **Visio**: 流程图
- **Draw.io**: 免费在线绘图
- **Adobe Illustrator**: 专业矢量图

---

## 八、学术道德与规范

### 8.1 学术不端行为

```
❌ 抄袭/剽窃
❌ 伪造数据
❌ 篡改数据
❌ 一稿多投
❌ 不当署名
❌ 自我抄袭
```

### 8.2 引用规范

```
# 必须引用的情况
- 使用他人观点、方法、数据
- 转述他人论述
- 使用他人图表

# 引用格式
直接引用：加引号，标注页码
间接引用：改写，标注来源
图表引用：获得许可，注明来源
```

### 8.3 查重标准

```
# 期刊论文
- 总重复率：< 15%
- 单篇引用：< 3%

# 学位论文
- 本科：< 30%
- 硕士：< 15%
- 博士：< 10%

# 查重系统
- 中国知网 CNKI
- 万方数据
- Turnitin (英文)
```

---

## 九、技能检查清单

### 文献检索
- [ ] 掌握 Web of Science/Scopus 检索
- [ ] 掌握 CNKI/万方检索
- [ ] 熟练使用布尔逻辑
- [ ] 会使用字段限定检索

### 文献管理
- [ ] 安装并配置 Zotero/EndNote
- [ ] 会导入 PDF 和元数据
- [ ] 会在 Word 中插入引用
- [ ] 会切换引用格式

### SCI 论文写作
- [ ] 掌握 IMRaD 结构
- [ ] 会写英文摘要
- [ ] 会制作三线表
- [ ] 熟悉目标期刊格式
- [ ] 会写 Cover Letter
- [ ] 会回复审稿意见

### 中文论文写作
- [ ] 掌握中文论文结构
- [ ] 熟悉量和单位规范
- [ ] 会制作中文图表
- [ ] 了解核心期刊要求

### 专利撰写
- [ ] 掌握专利结构
- [ ] 会写权利要求书
- [ ] 会进行专利检索
- [ ] 会答复审查意见

### 书稿写作
- [ ] 掌握章节结构
- [ ] 控制章节篇幅
- [ ] 图表配置合理
- [ ] 了解出版流程

---

**最后更新**: 2026-02-22  
**维护者**: AI Assistant  
**适用仓库**: books / WriterLLM / patent
