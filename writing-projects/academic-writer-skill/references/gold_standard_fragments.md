# 金标准范文片段 (Gold Standard Fragments)

> 本文件提供各文体的优秀写作范例片段。这些片段展示"好的输出长什么样"。
> 写作引擎撰写初稿时对标这些范例的质量水准，评审时以此为隐性基准。
> 
> ⚠️ 以下片段均为CHS领域写作的参考范例，非完整论文。实际写作须根据具体主题调整内容。

---

## SCI论文 — Introduction Gap Statement 范例

```
Canal automation has advanced significantly over the past two decades, driven by
the integration of real-time sensing, model predictive control, and distributed
computing (Malaterre et al., 1998; van Overloop, 2006; Lemos et al., 2023).
However, the vast majority of existing control schemes operate under a critical
but rarely examined assumption: that the underlying hydraulic model remains
time-invariant during the control horizon. In practice, canal pool dynamics are
subject to continuous parameter drift due to sediment deposition, vegetation
growth, and structural aging — factors that can alter the effective Manning's
coefficient by 15–30% over a single irrigation season (Lei et al., 2025a).

This temporal non-stationarity poses a fundamental challenge that cannot be
resolved by simply re-calibrating model parameters at fixed intervals. What is
needed instead is a control framework that explicitly accounts for parametric
uncertainty as a first-class design element, rather than treating it as an
exogenous disturbance to be compensated ex post. To date, no such framework
has been established for open-channel hydraulic systems, despite mature
parallels in aerospace (Åström & Wittenmark, 2013) and power systems
(Morari & Lee, 1999).
```

**为什么这段好**：
- Gap从"假设"入手（不是"没人做过"的懒惰Gap）
- 用具体数据（15-30%）支撑问题的严重性
- "first-class design element" vs "exogenous disturbance"——用对比制造认知张力
- 类比航空/电力系统，暗示方法论的可借鉴性和通用性

---

## SCI论文 — Methodology 物理直觉解释范例

```
Theorem 1. (IDZ Frequency-Domain Equivalence) For a prismatic canal pool
operating under small perturbation conditions, the linearized Saint-Venant
equations admit a rational transfer function of the form:

    G(s) = e^{-τ_d s} · (1 + α·s) / (s · (1 + β·s))         (7)

where τ_d is the dominant delay, α captures the zero dynamics of the upstream
boundary, and β represents the effective inertial time constant.

Proof. Starting from the linearized momentum equation (3)...  □

Remark 1. The physical interpretation of Eq. (7) is instructive. The pure
integrator (1/s) reflects the mass-balance nature of the pool: water level
rises continuously under a sustained inflow imbalance. The delay e^{-τ_d s}
corresponds to the wave travel time from the upstream gate to the measurement
point — typically 5–15 minutes for pools of 5–20 km in the Middle Route of
SNWTP. The numerator zero (1 + α·s) captures the initial "inverse response"
phenomenon observed in long pools: when the upstream gate opens, the downstream
water level momentarily drops before rising, a behavior well-documented in
field observations (Schuurmans, 1997) but frequently overlooked in simplified
control models.
```

**为什么这段好**：
- 定理→证明→Remark的经典三段结构
- Remark不是重复公式，而是赋予每个参数物理意义
- 用真实工程数据（5-15分钟，5-20km）锚定抽象参数
- 提到"frequently overlooked"——暗示本文的精细程度优于前人

---

## 中文核心论文 — 摘要范例

```
针对长距离输水明渠冰期运行中水位波动大、安全裕度不足的问题，提出了一种融合
冰盖热力学模型与分布式模型预测控制（DMPC）的冰期水位协同调控方法。首先，
基于Stefan方程建立渠池冰盖生长-消融动态模型，与Saint-Venant方程耦合形成冰
水耦合水力模型；其次，将耦合模型嵌入DMPC框架，以各闸门调节量为决策变量，
以水位偏差最小化和冰盖安全约束为目标函数，实现多渠池协同优化；最后，以南水
北调中线工程安阳-邯郸段（4个渠池、全长87 km）为验证对象，开展了冬季典型工
况的数值实验。结果表明：与现行分散PID调控方案相比，所提方法将水位波动幅度
降低了47.3%，冰盖厚度预测误差控制在±2.1 cm以内，且在极端降温工况下仍能
维持安全水位裕度≥0.3 m。研究成果为北方寒区输水工程冰期智能调度提供了理论
依据和技术支撑。
```

**为什么这段好**：
- 严格的"目的—方法—结果—结论"四段结构浑然一体
- 三个量化指标（47.3%、±2.1cm、≥0.3m）让审稿人一眼看到价值
- 工程验证对象具体到段落名和长度（安阳-邯郸段，87km）
- 末句"理论依据和技术支撑"精准收束

---

## 发明专利 — 权利要求书范例

```
1. 一种基于IDZ模型的多渠池水位协同控制方法，包括实时采集各渠池
的水位数据和闸门开度数据，其特征在于，包括以下步骤：

步骤一，基于所述水位数据和闸门开度数据，采用递推最小二乘法在线
辨识各渠池的IDZ传递函数参数，所述IDZ传递函数参数包括积分增益、
延迟时间和零点时间常数；

步骤二，将辨识得到的所述IDZ传递函数参数输入分布式模型预测控制
器，所述分布式模型预测控制器以各闸门调节量为决策变量，以预测
时域内各渠池目标水位偏差的加权二范数最小为优化目标，并满足闸门
开度约束、闸门调节速率约束和水位安全包络约束；

步骤三，所述分布式模型预测控制器通过相邻渠池间的状态信息交换，
采用交替方向乘子法迭代求解所述优化目标，得到各闸门在当前控制
周期的最优调节量；

步骤四，将所述最优调节量下发至各闸门执行器执行，并在下一控制
周期返回步骤一。

2. 根据权利要求1所述的方法，其特征在于，所述步骤一中，递推最小
二乘法的遗忘因子设置为0.95至0.99，辨识窗口长度为所述延迟时间
的3至5倍。

3. 根据权利要求1所述的方法，其特征在于，所述步骤二中，所述水位
安全包络约束定义为：目标水位±ε，其中ε根据渠池的运行设计域
（ODD）等级确定，L3等级对应ε=0.10m，L4等级对应ε=0.05m。
```

**为什么这段好**：
- 独权4步骤形成完整闭环（辨识→优化→求解→执行→回到辨识）
- 每步用"所述"严格回指，法律语言规范
- 从权2开始逐层具体化（遗忘因子0.95-0.99→可实施的参数范围）
- 权3引入ODD分级与安全包络，扩展保护范围至安全域概念

---

## 书稿/教材 — 章首导言范例

```
第3章 渠池传递函数建模

想象你正在操控一条50公里长的输水渠道。你在上游开大了闸门，但下游的水位
传感器要过15分钟才能"感知到"这个变化——这段等待时间里，你完全是在"盲飞"。
更麻烦的是，当水位终于开始变化时，它的响应速度、超调量和最终稳定值都取决于
渠道的形状、粗糙度和当前水深——这些参数你可能并不精确知道。

这就是水利控制工程师每天面对的核心困境：如何在大延迟、强耦合、参数不确定
的系统中实现精准控制？

本章的目标是为这个困境提供一把数学钥匙——传递函数。我们将从描述明渠水流的
基本方程（Saint-Venant方程）出发，经过线性化和Laplace变换两个关键步骤，
最终得到一个结构简洁、物理意义清晰的IDZ传递函数模型。这个模型只有三个参数
（α, β, τ_d），却能捕捉渠池动态响应的本质特征。

在第2章中，我们已经建立了Saint-Venant方程的数值解法。本章将揭示：同样的
物理过程，换一个数学视角（频域而非时域），会带来怎样意想不到的简洁与深刻。
第4章将在此基础上，利用传递函数设计各类控制器。
```

**为什么这段好**：
- "盲飞"比喻让工科学生瞬间理解延迟控制的困难
- 三个递进的困难（延迟→耦合→不确定性）构建问题层次
- "数学钥匙"的比喻让学生期待解决方案
- 清晰的知识路径图（SV→线性化→Laplace→IDZ）
- 与前后章显式衔接

---

## 技术报告 — 执行摘要范例

```
一、项目概况
受水利部南水北调司委托，本项目针对中线工程冰期运行安全问题，研发了冰水
耦合智能调控系统。项目执行期2024年6月至2026年3月，合同金额1,200万元。

二、核心成果
1. 建立了国内首个渠池冰盖生长-消融实时预测模型，72小时预报精度达92.3%；
2. 研发了冰期DMPC协同调控算法，经安阳-邯郸段（87km）实测验证，水位控制
   精度较现行方案提升47.3%；
3. 完成了冰期调控决策支持系统（V2.1）的软件开发与部署，已在2025-2026年
   冰期正式投入试运行。

三、关键建议
1.【高优先级】建议将冰期调控系统的运行范围从安阳-邯郸段扩展至全线（北京段
  以北），预计需追加投资380万元，建议列入2027年度预算（责任单位：调度中心）。
2.【中优先级】建议在2026年夏季开展冰盖传感器加密布设（间距从20km缩短至
  10km），以提高空间分辨率（责任单位：维护处，预算约95万元）。
3.【低优先级】建议启动冰期运行规程修编，将DMPC调控策略纳入正式操作规程
  （责任单位：运行管理处，预计周期6个月）。
```

**为什么这段好**：
- 非技术人员2分钟读完即掌握全局
- 每个成果都有量化指标（92.3%、47.3%、V2.1）
- 建议按优先级排序，每条有：行动内容+预算+责任单位+时间
- 管理者读完可以直接批示"同意建议1，建议2待论证"

---

## 技术标准 — 条文范例 (STD-CN)

```
5 系统功能要求

5.1 总体要求

5.1.1 水网智能调控系统应具备数据采集、状态监测、预测预警、优化调度和
自主控制五项基本功能。

5.1.2 系统应根据水网自主运行等级（WNAL，见3.1）的要求，分级配置功能
模块。各等级的功能要求见表1。

表1 各WNAL等级功能配置要求
┌────────┬──────┬──────┬──────┬──────┬──────┐
│ 功能模块 │ L1   │ L2   │ L3   │ L4   │ L5   │
├────────┼──────┼──────┼──────┼──────┼──────┤
│ 数据采集 │ 应   │ 应   │ 应   │ 应   │ 应   │
│ 状态监测 │ 应   │ 应   │ 应   │ 应   │ 应   │
│ 预测预警 │ —    │ 应   │ 应   │ 应   │ 应   │
│ 优化调度 │ —    │ —    │ 应   │ 应   │ 应   │
│ 自主控制 │ —    │ —    │ —    │ 应   │ 应   │
│ 自主决策 │ —    │ —    │ —    │ —    │ 应   │
└────────┴──────┴──────┴──────┴──────┴──────┘

5.2 数据采集

5.2.1 系统应采集的水力参数至少包括：水位、流量、闸门开度。量测精度
应满足以下要求：
  a) 水位量测误差不应大于±1 cm；
  b) 流量量测误差不应大于量测值的±5%；
  c) 闸门开度量测误差不应大于±0.5 cm。

5.2.2 数据采集周期宜根据WNAL等级确定：
  a) L1至L2等级，采集周期不宜大于15 min；
  b) L3至L4等级，采集周期不宜大于5 min；
  c) L5等级，采集周期不宜大于1 min。
```

**为什么这段好**：
- "应/宜/不应"用语精确，无一处混用
- 表格将分级要求一目了然
- 每个量化指标都可检验（±1cm、±5%、±0.5cm）
- 条文编号连续，层次清晰（5→5.1→5.1.1→5.2→5.2.1）
- 使用a) b) c)子条目结构化展示

---

## 技术标准 — 条文范例 (STD-INT)

```
6 Control system requirements

6.1 General

6.1.1 The water network intelligent control system shall implement the
control functions corresponding to its designated WNAL level as specified
in Table 2.

6.1.2 The control system should support graceful degradation: if a
component failure reduces the achievable WNAL level, the system shall
automatically fall back to the next lower level and shall notify the
operator within 30 s.

6.2 Model predictive control

6.2.1 Where WNAL Level 3 or higher is required, the control system shall
implement a model predictive control (MPC) algorithm with the following
minimum capabilities:
  a) prediction horizon of not less than 3 times the dominant transport
     delay of the longest canal pool in the network;
  b) control update interval of not more than one-fifth of the dominant
     transport delay;
  c) constraint handling for both gate position limits and water level
     safety envelopes as defined in 6.4.

6.2.2 The MPC algorithm should use the IDZ (Integrator Delay Zero)
transfer function model as the internal prediction model. Alternative
models may be used provided that the prediction accuracy requirements
of 6.3 are met.

NOTE  The IDZ model offers a favourable trade-off between fidelity and
computational cost for real-time control applications. See Annex B for
a comparative evaluation.
```

**为什么这段好**：
- shall/should/may严格区分（shall=强制，should=推荐，may=允许）
- 6.1.2的"graceful degradation"条款体现工程安全思维
- 量化指标表述为与物理量的关系（≥3倍延迟、≤1/5延迟），而非绝对数值
- NOTE提供非规范性补充说明
- 交叉引用（6.3、6.4、Annex B）构建文档网络

---

## 微信公众号 — 开头范例

```
# 你的城市供水管道，正在用30年前的方式运转

2024年，中国新能源汽车渗透率突破50%，无人机送外卖在深圳成为日常，
ChatGPT已经能写论文、改代码、做PPT。

但如果你走进任何一座城市的供水调度中心，大概率会看到这样一幅画面——

三个调度员盯着六块大屏，屏幕上密密麻麻的数字每隔15分钟刷新一次。
其中一位正在打电话："老王，3号泵站出口压力偏低，你手动调一下阀门。"

这不是2004年的场景。这是2024年。

**中国管理着全球最复杂的水网系统——总长超过110万公里的供水管道、
7200多座水库、49万公里灌溉渠道——但调度方式，基本停留在"人盯屏幕+
电话调令"的阶段。**

这件事为什么重要？因为水和电不一样。
```

**为什么这段好**：
- 标题用"你的"制造关联感，"30年前"制造反差
- 三个科技进步（新能源车/无人机/ChatGPT）建立"技术已经很先进"的锚点
- "但如果你走进..."硬转折，场景画面感极强
- "这不是2004年。这是2024年。"短句制造震撼
- 加粗段用数据（110万公里、7200座、49万公里）建立规模感
- 结尾"水和电不一样"抛出钩子，让人想继续读

---

## 演示文稿(PPT) — Speaker Notes 范例

```
--- Slide 7: IDZ模型将计算时间缩短95% ---

[转场·2秒]
"前面我们看到了问题有多复杂。现在，让我展示一个让我们团队自己都吃惊的结果。"

[指图·左侧]
"左边是传统方法——直接求解Saint-Venant方程。对于中线工程1432公里、
63个渠池的规模，计算一次最优调度方案需要47分钟。这意味着什么？
意味着你算出方案的时候，水已经流到了下一个渠池。"

[停顿·1秒]

[指图·右侧]
"右边是IDZ模型。同样的63个渠池，同样的精度要求——2.3分钟。
快了20倍。而且，水位预测误差控制在±3厘米以内。"

[关键判断]
"这不是一个技术细节的改进。这是一个质变——它让实时控制从理论上
可行变成了工程上可行。没有这个速度，后面所有的自动化都无从谈起。"

[过渡]
"有了快速可靠的模型，接下来的问题是：如何让63个闸门协同工作？
这就是下一页要讲的分布式控制。"

[时间] 约1分40秒，累计约11分钟
```

**为什么这段好**：
- [转场]制造期待感（"让我们团队自己都吃惊"）
- 47分钟→2.3分钟的对比极具冲击力
- "水已经流到了下一个渠池"——用直觉而非技术语言解释为什么47分钟不行
- "质变"判断升华了技术数据的意义
- 过渡句自然引出下一页，听众不会断流
- 标注时间帮助控制节奏

---

## 使用方法

1. **写作时**: 查阅对应文体的金标准片段，模仿其结构和质量水准
2. **评审时**: 将初稿与金标准片段对比，差距即扣分依据
3. **修改时**: 参照"为什么这段好"的分析，针对性改进
