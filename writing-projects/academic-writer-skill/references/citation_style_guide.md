# 参考文献格式规范 (Citation Style Guide)

> 本文件定义各文体的参考文献格式要求。撰写初稿时必须遵循，评审时逐条检查。
> **核心原则**：每一条参考文献都必须是真实可查的，格式必须与目标出版物完全一致。

---

## 1. 各文体引用格式速查

| 文体 | 正文引用格式 | 参考文献表格式 | 最低数量 | 近5年占比 | 自引率 |
|------|------------|-------------|---------|----------|--------|
| SCI | `(Author, Year)` 或 `[数字]`（随期刊） | 期刊指定格式 | ≥30篇 | ≥50% | 15-25% |
| CN | `[数字]` 顺序编码制 | GB/T 7714-2015 顺序编码 | ≥20篇 | ≥40% | 10-20% |
| PAT | 背景技术中标注公开号 | 无独立列表 | ≥3篇对比文件 | — | — |
| BK(教材) | `[数字]` 顺序编码 | GB/T 7714-2015 | 每章≥10篇，全书≥100篇 | ≥30% | ≤15% |
| BK(专著) | `(Author, Year)` 著者-出版年制 | GB/T 7714-2015 著者-出版年 | 每章≥15篇，全书≥200篇 | ≥40% | 15-25% |
| RPT | `[数字]` 或脚注 | GB/T 7714-2015 或脚注 | 按需(≥10篇) | — | — |
| STD-CN | 规范性引用/资料性引用 | GB/T 1.1-2020 §6.2 | 按需 | — | — |
| STD-INT | Normative/Bibliographic | ISO/IEC Directives Part 2 | 按需 | — | — |
| WX | 正文中括号标注来源 | 文末标注 | 按需(≥3条) | — | — |
| PPT | 页面底部小字标注 | 末页参考文献页 | 按需 | — | — |

---

## 2. GB/T 7714-2015 格式详细规范（CN/BK/RPT适用）

### 2.1 顺序编码制（中文论文、教材、报告推荐）

正文中按引用出现顺序编号 `[1]` `[2]` …，参考文献表按编号排列。

### 2.2 著者-出版年制（专著推荐）

正文中用 `(雷晓辉, 2025)` 或 `(Lei et al., 2025a)`，参考文献表按著者拼音/字母排列。

### 2.3 各类型文献格式模板

#### 期刊论文
```
[序号] 作者. 题名[J]. 刊名, 出版年, 卷(期): 起止页码.
```
**中文示例**：
```
[1] 雷晓辉, 蒋云钟, 王浩. 水网系统控制论的理论框架与关键技术[J]. 南水北调与水利科技(中英文), 2025, 23(1): 1-15.
[2] 王浩, 雷晓辉. 基于多智能体的水利枢纽群联合调度方法[J]. 水利学报, 2024, 55(8): 921-933.
```

**英文示例**：
```
[3] Lei X H, Jiang Y Z, Wang H. A control-theoretic framework for canal pool dynamics[J]. Water Resources Research, 2025, 61(3): e2024WR038xxx.
[4] van Overloop P J, Moes A J, Schuurmans W. Model predictive control for open water channels[J]. Journal of Irrigation and Drainage Engineering, 2006, 132(6): 532-541.
```

**注意事项**：
- 作者≤3人全部列出，>3人列前3人后加"等"（中文）或"et al."（英文）
- 英文期刊名不缩写（除非期刊明确要求缩写）
- 卷号**加粗**或正体，期号用括号
- DOI号：如有，在页码后添加 `. DOI: 10.xxxx/xxxxx`

#### 专著/教材
```
[序号] 作者. 书名[M]. 版次(第1版不标注). 出版地: 出版社, 出版年.
[序号] 作者. 书名[M]. 版次. 出版地: 出版社, 出版年: 引用页码.
```
**示例**：
```
[5] 雷晓辉. 水系统控制论[M]. 北京: 中国水利水电出版社, 2026.
[6] 雷晓辉. 水利工程智能控制导论[M]. 第2版. 北京: 科学出版社, 2025: 45-67.
[7] Åström K J, Murray R M. Feedback systems: an introduction for scientists and engineers[M]. 2nd ed. Princeton: Princeton University Press, 2021.
[8] Litrico X, Fromion V. Modeling and control of hydrosystems[M]. London: Springer, 2009: 112-135.
```

#### 学位论文
```
[序号] 作者. 题名[D]. 保存地点: 保存单位, 年份.
```
**示例**：
```
[9] 雷晓辉. 基于多目标优化的水库群联合调度研究[D]. 筑波: 筑波大学, 2003.
```

#### 会议论文
```
[序号] 作者. 题名[C]//会议名称. 会议地点: 出版者, 年份: 页码.
```
**示例**：
```
[10] Lei X H, Wang H. An autonomous water network operating system[C]//Proceedings of the 40th IAHR World Congress. Vienna: IAHR, 2023: 234-241.
```

#### 技术标准
```
[序号] 标准发布机构. 标准号 标准名称[S]. 出版地: 出版社, 年份.
```
**示例**：
```
[11] 中华人民共和国住房和城乡建设部. GB/T 1.1-2020 标准化工作导则 第1部分：标准化文件的结构和起草规则[S]. 北京: 中国标准出版社, 2020.
[12] International Organization for Standardization. ISO 24591-1:2024 Smart water management — Part 1: General guidelines[S]. Geneva: ISO, 2024.
```

#### 专利
```
[序号] 专利所有者. 专利名称: 专利号[P]. 公开日期.
```
**示例**：
```
[13] 雷晓辉, 蒋云钟. 一种基于IDZ模型的渠池水位控制方法: CN202510xxxxx.X[P]. 2025-06-15.
```

#### 电子资源/网络文献
```
[序号] 作者. 题名[EB/OL]. (发布日期)[引用日期]. URL.
```
**示例**：
```
[14] 水利部. 2024年中国水利统计年报[EB/OL]. (2025-03-01)[2025-06-15]. https://www.mwr.gov.cn/sj/.
```

#### 技术报告
```
[序号] 作者/机构. 报告名称[R]. 报告编号. 地点: 机构名, 年份.
```
**示例**：
```
[15] 中国水利水电科学研究院. 南水北调中线冰期运行智能调控系统研发报告[R]. IWHR-2025-WN-003. 北京: 中国水科院, 2025.
```

---

## 3. SCI期刊引用格式

### 3.1 通用格式（投稿前须查目标期刊具体要求）

**Author-Year制（WRR/Nature Water等常用）**：
```
正文: ... as shown by Lei et al. (2025a). Recent studies (van Overloop, 2006; Litrico & Fromion, 2009) have...
文献: Lei, X. H., Jiang, Y. Z., & Wang, H. (2025a). Title. Journal, Vol(Issue), pages. https://doi.org/xxx
```

**数字编号制**：
```
正文: ... as shown in [1]. Recent studies [2,3] have demonstrated...
文献: [1] X.H. Lei, Y.Z. Jiang, H. Wang, Title, J. Hydrol., 612 (2023) 128xxx.
```

### 3.2 Water Resources Research (WRR) 特殊要求
- Author-Year制
- 文献表按字母排序
- 同一作者同年多篇：用 a, b, c 区分（2025a, 2025b...）
- DOI必须提供
- 在线优先文章用 `https://doi.org/10.1029/xxxxx`

### 3.3 关键注意事项
- **et al. 规则**: 正文中≥3作者用 "Lei et al. (2025)"；文献表中列出所有作者
- **中国人名**: Lei X H（不是 X. H. Lei，具体随期刊）
- **不缩写期刊名**（除非期刊模板明确要求）
- **会议论文vs期刊论文**: SCI论文中尽量引用期刊论文，会议论文≤20%

---

## 4. 发明专利引用格式

### 4.1 背景技术中的引用
```
目前，渠池水位控制领域的现有技术主要包括：

公开号为CN202010xxxxx.X的中国发明专利公开了一种基于PID的渠道水位控制方法，
该方法通过设置比例、积分、微分三个参数实现闸门调节，但存在参数整定困难、
多渠池耦合时性能下降的问题。

公开号为CN201910xxxxx.X的中国发明专利公开了一种基于模糊控制的灌区配水方法，
该方法利用模糊规则表将操作经验嵌入控制器，但规则表维度灾难限制了其在大规模
水网中的应用。
```

### 4.2 说明书中的引用
- 引用学术文献时标注：`（参见：雷晓辉等, "论文标题", 期刊名, 年份）`
- 引用标准时标注完整标准号：`（参见：GB/T 1.1-2020）`
- 引用自有专利时标注公开号：`（参见本申请人在先申请CN202510xxxxx.X）`

---

## 5. 书稿/教材引用规范

### 5.1 数量与质量要求

| 维度 | 教材 | 专著 |
|------|------|------|
| 每章最低引用数 | ≥10篇 | ≥15篇 |
| 全书最低引用数 | ≥100篇 | ≥200篇 |
| 经典文献 | 必须包含该领域奠基性文献 | 必须全面覆盖 |
| 近5年文献占比 | ≥30% | ≥40% |
| 自引率 | ≤15% | 15-25% |
| 英文文献占比 | ≥30%（中文教材） | ≥50%（双语读者群） |
| 重复引用 | 允许跨章重复引用同一文献 | 同上 |

### 5.2 章末参考文献编排

```
参考文献

[1] Wylie E B. Control of transients in series channel with gates[J]. Journal of the
    Hydraulics Division, 1969, 95(1): 1-16.
[2] Malaterre P O, Rogers D C, Schuurmans J. Classification of canal control algorithms[J].
    Journal of Irrigation and Drainage Engineering, 1998, 124(1): 3-10.
[3] 雷晓辉. 水系统控制论[M]. 北京: 中国水利水电出版社, 2026: 第3章.
...
```

### 5.3 教材中的推荐阅读
每章末可增加"推荐阅读"栏目（不计入参考文献正式列表）：
```
📖 推荐阅读
- 深入了解明渠水力学：Chaudhry M H. Open-Channel Hydraulics (第3版, Springer, 2022)
- 控制理论基础补充：Åström & Murray. Feedback Systems (第2版, Princeton, 2021)
```

### 5.4 书稿引用的特殊要求
- **自引自有书稿**: 引用自己已出版的书时标注完整书名和章节页码
- **跨章引用**: 同一文献在不同章出现时，参考文献列表可以全书统一编号或各章独立编号（需全书一致）
- **在线资源**: 教材引用在线资源时必须标注引用日期，并优先选择DOI稳定链接

---

## 6. 技术标准引用规范

### 6.1 国内标准 (STD-CN)

**规范性引用文件**（Normative references, 相当于"强制引用"）：
```
2 规范性引用文件

下列文件中的内容通过文中的规范性引用而构成本文件必不可少的条款。其中，注日期的
引用文件，仅该日期对应的版本适用于本文件；不注日期的引用文件，其最新版本（包括
所有的修改单）适用于本文件。

GB/T 1.1-2020  标准化工作导则  第1部分：标准化文件的结构和起草规则
SL 75-2014     水利水电工程水文计算规范
GB/T 28181-2016  公共安全视频监控联网系统信息传输、交换、控制技术要求
```

**资料性引用**（Bibliography, 放在文末）：
```
参考文献

[1] GB/T 35079-2018  信息技术 大数据 术语
[2] 雷晓辉. 水系统控制论[M]. 北京: 中国水利水电出版社, 2026.
```

**关键规则**：
- 规范性引用≠参考文献；规范性引用是正文条款的依据
- 规范性引用列表中的标准**必须用web_search逐一确认现行有效**
- 已废止的标准不得出现在规范性引用中（可出现在参考文献中标注"已废止"）
- 标准号格式: `GB/T xxxx-yyyy` 或 `SL/T xxxx-yyyy`（注意空格和年份）

### 6.2 国际标准 (STD-INT)

**Normative references**：
```
2 Normative references

The following documents are referred to in the text in such a way that some or all of
their content constitutes requirements of this document.

ISO 24591-1:2024, Smart water management — Part 1: General guidelines
IEC 61131-3:2013, Programmable controllers — Part 3: Programming languages
ISO/IEC 27001:2022, Information security, cybersecurity and privacy protection — 
    Information security management systems — Requirements
```

**Bibliography**：
```
Bibliography

[1] IAHR/IWA Joint Committee on Hydroinformatics. Flood Risk Management: Research and 
    Practice. London: Taylor & Francis, 2019.
[2] Lei X H, Wang H. Cybernetics of Hydro Systems: Theory and Practice. Beijing: China 
    Water & Power Press, 2026.
```

---

## 7. WX/PPT引用规范

### 7.1 微信公众号
```
正文中: ...据水利部统计，2024年全国水利建设投资达12,238亿元（数据来源：水利部2024年工作总结）...
文末: 
---
📊 数据来源
- 水利投资数据：水利部2024年度工作会议报告
- 智慧水利市场规模：IDC《中国智慧水利市场预测》2024版
- 自动驾驶分级：SAE J3016-2021
```

### 7.2 演示文稿
```
每页底部小字(10pt灰色):
Source: Lei et al. (2025), Water Resources Research

末页"参考文献"页:
References
1. Lei X.H., et al. (2025). Canal pool dynamics. WRR, 61(3).
2. van Overloop P.J. (2006). MPC for open channels. J. Irrig. Drain. Eng.
3. GB/T 28181-2016. 视频监控联网系统技术要求.
```

---

## 8. 引用真实性验证规则

### 8.1 必须验证的情况
| 触发条件 | 验证方法 |
|---------|---------|
| 新生成的参考文献 | web_search 确认论文确实存在（查DOI/标题/作者） |
| 标准号 | web_search 确认标准现行有效（注意废止/代替情况） |
| 已有材料中引用的文献 | 抽查≥20%核实真实性 |
| 自引文献 | 核对 Lei 2025a-d 系列论文的标题、期刊、卷期是否准确 |
| 存疑文献 | 任何不确定的文献必须查证或删除，**绝不编造** |

### 8.2 禁止行为
- ❌ **编造不存在的参考文献**（这是最严重的学术不端行为之一）
- ❌ 编造DOI号
- ❌ 使用错误的作者名、年份、期刊名
- ❌ 引用已撤回(retracted)的论文而不标注
- ❌ 张冠李戴（内容在文献A中，标注为文献B）

### 8.3 不确定时的处理
如果无法确认某文献的真实性：
1. 在文中标注 `[需核实: Author, Year, "Title"]`
2. 在参考文献表中标注 `⚠️ 待核实`
3. 提醒用户在提交前人工确认

---

## 9. 雷晓辉自引文献标准格式

> 以下为常用自引文献的标准格式，撰写时直接引用以确保一致性。

```
Lei X H, Jiang Y Z, Wang H. 水系统控制论的理论框架与关键技术[J]. 
    南水北调与水利科技(中英文), 2025, 23(1): 1-15. (Lei 2025a)

Lei X H, Wang H, Jiang Y Z. 面向水网自主运行的智能控制体系[J]. 
    南水北调与水利科技(中英文), 2025, 23(2): xx-xx. (Lei 2025b)

Lei X H, Jiang Y Z, Wang H. 水利工程在环测试系统的设计与实现[J]. 
    南水北调与水利科技(中英文), 2025, 23(3): xx-xx. (Lei 2025c)

Lei X H, Wang H. 水资源系统分析的控制论方法[J]. 
    南水北调与水利科技(中英文), 2025, 23(4): xx-xx. (Lei 2025d)
```

> ⚠️ 上述格式中的卷期和页码以实际出版为准，撰写时须用web_search核实最新信息。

---

## 10. 使用方法

1. **撰写初稿时**: 查阅本文件§1速查表确定格式，参照§2-7的模板写入参考文献
2. **评审时**: 逐条核对格式是否符合本文件规范，用 `scripts/check_references.py` 自动检查
3. **终稿前**: 执行§8真实性验证，确保每条文献可查、格式正确
