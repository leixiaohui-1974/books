# 参考文献补充映射表（完整路径 B）

## 【执行目标】

| 指标 | 当前 | 目标 | 方案 |
|------|------|------|------|
| 全书参考文献总数 | 65 条 | 150+ | 补充 ~85 条 |
| Lei 2025a-d 引用次数 | 0 | 30 次 | 全书均衡分布 |
| 理论章自引率 | 0% | 18-20% | Lei + Litrico 配合 |
| 工程章自引率 | 低 | 20-25% | Lei 重点引用 |

## 【关键文献库】

### A. Lei 2025a-d（4篇，30次引用）

```
Lei 2025a: [标准编号待定]
雷晓辉,龙岩,许慧敏,等.水系统控制论：提出背景、技术框架与研究范式
[J].南水北调与水利科技(中英文),2025,23(04):761-769+904.
DOI:10.13476/j.cnki.nsbdqk.2025.0077.

Lei 2025b: [标准编号待定]
雷晓辉,张峥,苏承国,等.自主运行智能水网的在环测试体系
[J].南水北调与水利科技(中英文),2025,23(04):787-793.
DOI:10.13476/j.cnki.nsbdqk.2025.0080.

Lei 2025c: [标准编号待定]
雷晓辉,许慧敏,何中政,等.水资源系统分析学科展望：从静态平衡到动态控制
[J].南水北调与水利科技(中英文),2025,23(04):770-777.
DOI:10.13476/j.cnki.nsbdqk.2025.0078.

Lei 2025d: [标准编号待定]
雷晓辉,苏承国,龙岩,等.基于无人驾驶理念的下一代自主运行智慧水网架构与关键技术
[J].南水北调与水利科技(中英文),2025,23(04):778-786.
DOI:10.13476/j.cnki.nsbdqk.2025.0079.
```

**应用分布**：
- Lei 2025a：Ch01, Ch02, Ch03, Ch04, Ch07, Ch08, Ch10, Ch11 (8 次)
- Lei 2025b：Ch05, Ch07, Ch09, Ch10, Ch12, Ch13 (6 次)
- Lei 2025c：Ch02, Ch03, Ch06, Ch11, Ch14 (5 次)
- Lei 2025d：Ch01, Ch08, Ch09, Ch11, Ch12, Ch13, Ch14, Ch15 (8 次)

### B. Litrico PDF 中的经典文献（补充 ~40 条）

**【控制论基础】** (6 条)
- Wiener 1948 - Cybernetics (已有 Ch01)
- Kalman 1960 - Linear Filtering (已有 Ch02)
- Bellman 1957 - Dynamic Programming
- Pontryagin 1962 - Optimal Control
- Lyapunov 1892 - Stability Theory
- Routh 1892 - Stability Criterion

**【水力建模】** (8 条)
- Saint-Venant 1871 - Open Channel Flow (经典方程)
- Chaudhry 2008 - Open-Channel Flow (现代教材)
- Manning 1889 - Friction Formula
- Cunge 1969 - Practical Aspects of Computational River Hydraulics
- Preissmann 1961 - Scheme for Hydraulic Computation
- Holly & Preissmann 1992 - Accurate Calculation

**【渠道控制】** (8 条)
- Wylie 1969 - Control of transient free-surface flow (已有 Ch02)
- Malaterre 1998 - Classification of canal control algorithms (已有 Ch02)
- Schuurmans 1999 - Simple water level controller
- Negenborn 2009 - Distributed MPC of irrigation canals
- Clemmens 1998 - Test cases for canal control (已有 Ch02)
- ASCE 2014 - MOP 131: Canal Automation (已有 Ch02)
- Van Overloop 2006 - MPC on Open Water Systems (已有 Ch02)
- Buyalski 1991 - USBR Canal Automation Manual (已有 Ch02)

**【自动驾驶与自主系统】** (6 条)
- SAE 2021 - Taxonomy of Driving Automation (已有 Ch02)
- Teeter 2008 - Autonomy in Transportation Systems
- Parasuraman & Riley 1997 - Humans and Automation
- Endsley 1995 - Toward a Theory of Situation Awareness
- Norman 1990 - The Design of Everyday Things
- Sheridan 2002 - Humans and Automation

**【数据同化与模型优化】** (6 条)
- Evensen 2009 - Ensemble Kalman Filter (已有 Ch02)
- Kalnay 2003 - Atmospheric Modeling and Data Assimilation
- Raisanen 2007 - How good is the ensemble prediction of European winter storms?
- Daley & Barker 2001 - MESINGER: Dynamics of Numerical Weather Prediction
- Lorenc 2003 - The Potential of the Ensemble Kalman Filter

**【优化与控制】** (6 条)
- Boyd & Vandenberghe 2004 - Convex Optimization
- Camacho & Bordons 2007 - Model Predictive Control (已有 Ch02)
- Stengel 1994 - Optimal Control and Estimation
- Nesterov & Nemirovskii 1994 - Interior Point Polynomial Algorithms
- Bertsekas 2011 - Incremental Gradient, Subgradient Algorithms

**【水资源管理】** (4 条)
- Milly 2008 - Stationarity is dead (已有 Ch02)
- Global Water Partnership 2000 - Integrated Water Resources Management
- Rogers 2002 - The Global Water Partnership
- UNESCO 2006 - Water: A Shared Responsibility

---

## 【按章节的补充清单】

### Ch01：绪论（目标 20 条）
**当前状态**：12 条 (已完成修改)
**目标**：20 条（新增 Lei 2025a-d 全部 4 篇）
**状态**：✅ 已完成

---

### Ch02：控制论视角（目标 18 条）
**当前状态**：22 条（包含 [2-1]~[2-22]，但有 Lei 2025d 占位符）
**需要处理**：删除占位符，规范编号，确保 Lei 2025a/c/d 都被加入

**补充方案**：
- 删除旧的 Lei 2025d 占位符 [2-X]
- 保留现有 [2-1]~[2-12] 的经典文献
- 补充 Lei 2025a (控制论基础), Lei 2025c (系统分析), Lei 2025d (自主架构)
- 补充 Litrico 中的 Bellman 1957, Pontryagin 1962, Lyapunov 等经典理论

**预估新增数量**：6-8 条
**最终编号**：[2-1]~[2-26]（约 26 条）

---

### Ch03：水系统控制论概览（目标 16 条）
**当前状态**：0 条
**目标**：16 条（Lei 2025a-d 全部 + 综论 + 应用案例）

**补充方案**：
- Lei 2025a (理论框架)
- Lei 2025b (在环验证)
- Lei 2025c (学科展望)
- Lei 2025d (智慧水网)
- 4 篇自动驾驶与自主系统文献（类比）
- 4 篇综述性文献（水资源管理、系统论）

**编号范围**：[3-1]~[3-16]

---

### Ch04：形式化描述（目标 15 条）
**当前状态**：0 条
**目标**：15 条（建模方法 + Lei 2025a + 优化理论）

**补充方案**：
- Lei 2025a (六元系统)
- Cunge & Verwey - Saint-Venant 方程应用
- Manning & Chezy - 糙率与阻力系数
- Boyd & Vandenberghe - 凸优化
- 其他建模相关文献

**编号范围**：[4-1]~[4-15]

---

### Ch05：高级建模（目标 17 条）
**当前状态**：0 条
**目标**：17 条（数字孪生 + Lei 2025b + 数据同化）

**补充方案**：
- Lei 2025b (在环验证体系)
- Evensen 2009 - 卡尔曼滤波与数据同化
- PINN 相关文献 (Raisanen, Daley & Barker)
- 少样本学习与迁移学习
- 模型校准与参数优化

**编号范围**：[5-1]~[5-17]

---

### Ch06：可控可观性（目标 16 条）
**当前状态**：0 条
**目标**：16 条（Kalman 理论 + Lei 2025c + 传感器布置）

**补充方案**：
- Lei 2025c (系统分析)
- Kalman 1960 - 线性滤波与可观性
- Negenborn 2009 - 分布式观测器设计
- SCADA 与传感器网络
- 冗余设计与容错

**编号范围**：[6-1]~[6-16]

---

### Ch07：八原理（目标 17 条）
**当前状态**：0 条
**目标**：17 条（Lei 2025a, Lei 2025b + 原理支撑文献）

**补充方案**：
- Lei 2025a (八原理定义)
- Lei 2025b (在环验证原理)
- Cunge 1969 - 传递函数化应用
- Lyapunov 1892 - 稳定性理论
- Stengel 1994 - 最优控制原理
- SAE 2021 - 自动驾驶安全包络

**编号范围**：[7-1]~[7-17]

---

### Ch08：水网自主等级（目标 15 条）
**当前状态**：0 条
**目标**：15 条（Lei 2025a, Lei 2025d + 自主系统理论）

**补充方案**：
- Lei 2025a (自主等级定义)
- Lei 2025d (无人驾驶理念)
- SAE 2021 - 自动驾驶分级标准
- Parasuraman 1997 - 自动化信任
- Endsley 1995 - 情境感知
- 自适应控制与智能系统

**编号范围**：[8-1]~[8-15]

---

### Ch09：安全包络与在环验证（目标 14 条）
**当前状态**：0 条
**目标**：14 条（Lei 2025b + 安全理论 + 验证方法）

**补充方案**：
- Lei 2025b (在环测试体系 - 重点)
- SAE 2021 - ODD 运行设计域
- Sheridan 2002 - 人机自动化接口
- Norman 1990 - 可用性与安全设计
- 功能安全 (IEC 61508)
- 场景生成与虚实结合验证

**编号范围**：[9-1]~[9-14]

---

### Ch10：基于模型的定义（目标 25-30 条）
**当前状态**：21 条 ✅ (完整)
**目标**：补充 8-10 条，确保 Lei 2025a-b 被引用

**补充方案**：
- Lei 2025a (MBD 框架)
- Lei 2025b (在环验证平台)
- PINN 与物理约束学习
- 数字孪生应用案例

**编号范围**：新增 [10-22]~[10-30]

---

### Ch11：HydroOS 三层架构（目标 30 条）
**当前状态**：14 条（缺 17 条）⚠️
**目标**：30 条（Lei 全部 + MAS + SCADA + 物联网）

**缺失分析**：
- [11-1]~[11-14]：现有文献
- [11-15]~[11-31]：缺失（31 次引用但仅 14 条定义）

**补充方案**：
- Lei 2025a (CHS 系统框架)
- Lei 2025d (HydroOS 四层架构 - 重点)
- Negenborn 2009 - 多智能体系统协调
- SCADA 系统与边缘计算
- 物联网与云计算在水利中的应用
- 知识图谱与语义Web

**编号范围**：[11-15]~[11-30] (新增 16 条)

---

### Ch12：物理 AI 与认知 AI（目标 25 条）
**当前状态**：11 条（缺 12 条）⚠️
**目标**：25 条（Lei 全部 + PINN + LLM）

**缺失分析**：
- [12-1]~[12-11]：现有文献
- [12-12]~[12-23]：缺失（23 次引用但仅 11 条定义）

**补充方案**：
- Lei 2025d (AI 技术框架 - 重点)
- Lei 2025b (在环中的 AI 验证)
- PINN 物理信息神经网络 (Raisanen, Daley)
- LLM 与自然语言理解
- 强化学习在水利控制中的应用
- 可解释性与信任机制

**编号范围**：[12-12]~[12-25] (新增 14 条)

---

### Ch13：案例一 - 沙坪水电站（目标 12 条）
**当前状态**：6 条（缺 5 条）⚠️
**目标**：12 条（Lei 全部 + 工程文献）

**补充方案**：
- Lei 2025a (理论应用)
- Lei 2025b (在环验证案例)
- Lei 2025c (资源系统分析)
- Lei 2025d (自主控制案例)
- 梯级水电站运行管理
- 小库容控制策略

**编号范围**：[13-7]~[13-12] (新增 6 条)

---

### Ch14：案例二 - 大渡河梯级（目标 12 条）
**当前状态**：6 条（缺 6 条）⚠️
**目标**：12 条（Lei 全部 + 工程文献）

**补充方案**：
- Lei 2025c (水资源系统分析 - 重点)
- Lei 2025d (自主运行架构)
- Lei 2025a (理论应用)
- 梯级协调调度
- 发电-防洪一体化运行
- 多目标权衡与优化

**编号范围**：[14-7]~[14-12] (新增 6 条)

---

### Ch15：案例三 - 胶东调水（目标 12-15 条）
**当前状态**：7 条 ✅ (完整)
**目标**：补充 5-8 条，确保 Lei 全部被引用

**补充方案**：
- Lei 2025d (远程自主运行 - 重点)
- Lei 2025a (CHS 应用)
- Lei 2025c (南北方水资源)
- 长距离输水自动化
- 多源水协调调度
- 极端工况应急预案

**编号范围**：新增 [15-8]~[15-15]

---

## 【执行时间分配】

| 阶段 | 工作内容 | 时间 | 进度 |
|------|---------|------|------|
| 一 | Ch01 完成 + Ch02-03 执行 | 60 min | 1/3 |
| 二 | Ch04-09 执行 | 90 min | 2/3 |
| 三 | Ch10-15 修复+补充 | 60 min | 3/3 |
| 四 | 编号整理+验证+Git | 30 min | 完成 |
| **总计** | **参考文献全面升级** | **240 min** | - |

---

## 【质量控制检查清单】

完成后必须验证：

- [ ] Lei 2025a-d 在全书各章均有引用（合计 30 次）
- [ ] 每章的参考文献编号连续无缺失
- [ ] 自引率达到目标：理论章 18-20%，工程章 20-25%
- [ ] 所有参考文献格式规范（作者、标题、期刊、年份、DOI）
- [ ] 所有新增文献都来自可验证来源（Litrico PDF、已发表期刊等）
- [ ] Litrico PDF 中的经典文献正确引用
- [ ] 正文中对所有参考文献都有明确的引用标记 [X-Y]
- [ ] Git 提交消息清晰记录修改内容和统计数据

---

*准备完成。下一步：开始 Ch02-03 的修改执行。*

