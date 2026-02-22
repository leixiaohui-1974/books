# CHS Full Paper Plan v5 — 25篇论文写作系统概要

> 来源：Claude对话产出 | 原始对话：https://claude.ai/chat/fa8df027-5510-40de-9149-2cb9706ca1f1
> 编制日期：2026年2月
> 说明：完整的CLAUDE.md项目记忆文件及迭代写作提示词见原始对话

---

## 一、项目总览

共25篇论文（21篇英文 + 4篇已发表中文），分5条研究线、4个批次推进。

## 二、五条研究线

| 研究线 | 名称 | 论文数 | 领衔 |
|:---|:---|:---|:---|
| 理论奠基线 | CHS统一理论 + 学科建设 | 5 | 雷晓辉 |
| 实验线A | 双水箱MBD/xIL平台 | 4 | 陈凯歌 |
| 实验线B | 水槽DMPC实验验证 | 4 | 苏超 |
| 算法线 | GPU并行+降阶算法 | 4 | 黄志锋 |
| 工程线 | 沙坪/胶东/密云实际工程 | 8 | 叶尚君/张雷/杨明晗/吴辉明 |

## 三、P1三篇核心论文（理论基座）

| 编号 | 期刊 | 标题 | 篇幅 | 状态 |
|:---|:---|:---|:---|:---|
| P1a | Water Resources Research (AGU) | Cybernetics of Hydro Systems: A Unified Control-Theoretic Framework | ~15,000词 | v9完成 |
| P1b | Nature Water | Towards Autonomous Water Networks | ~4,300词 | 初稿完成 |
| P1c | 中国科学：技术科学 | 从水资源配置到水网自主运行 | ~17,000字 | v2完成 |

### P1三篇差异化策略

| 维度 | P1a (WRR) | P1b (Nature Water) | P1c (中国科学) |
|:---|:---|:---|:---|
| 定位 | 完整技术论文 | 远景展望短文 | 学科传承综述 |
| 读者 | 水资源+控制论专家 | 广义水科学研究者 | 中国水利学界 |
| 数学深度 | 完整推导含证明 | 无公式 | 关键公式+物理意义 |
| 独有内容 | Muskingum-IDZ对偶证明 | 范式转移论述 | 王浩WRSA→CHS学术传承 |

## 四、25篇完整论文规格表

### 理论奠基线（5篇，Batch 1）

| 编号 | 标题 | 期刊 | 作者 |
|:---|:---|:---|:---|
| P1a | CHS Unified Theory | WRR | Lei (独著) |
| P1b | Towards Autonomous Water Networks | Nature Water | Lei/Ji/Wang C/Wang H |
| P1c | 水系统控制论学科基础与工程范式 | 中国科学 | Lei/Ji/Wang C/Wang H |
| P2A | MAS Architecture + WSAL Classification | JWRPM (ASCE) | Lei et al. |
| P-DC | Discipline Construction Framework | EMS | Lei/Wang/Long/Liu |

### 实验线A（4篇）
- P3a: 双水箱MBD框架 + xIL验证
- P3b: Simulink快速原型
- P3c: OpenModelica组件化建模
- P3d: 多工况xIL覆盖度分析

### 实验线B（4篇）
- P4a: 水槽DMPC实验验证
- P4b: 通信延迟/丢包鲁棒性
- P4c: 多目标权衡实验
- P4d: 水槽→工程尺度迁移分析

### 算法线（4篇）
- P5a: GPU并行Saint-Venant求解器
- P5b: IDZ传递函数在线辨识
- P5c: 分布式MPC快速求解
- P5d: 模型降阶与精度-效率权衡

### 工程线（8篇）
- P6a/P6b: 沙坪水电站SiL+ODD
- P7a/P7b: 胶东调水HDMPC+多时间尺度
- P8a: 密云水库MAS/MBD
- P8b: 冰期运行控制
- P9a: 跨工程对比分析
- P9b: WSAL评估方法论

## 五、核心术语约定

- 全文使用"Cybernetics of Hydro Systems (CHS)"
- "分层分布式控制"(HDC) 而非简单"分布式控制"
- 南水北调中线不作为成功案例（L2辅助决策），仅作为背景
- 沙坪和胶东定位为"前期探索"而非成熟应用
- 所有论文中不使用"State Key Laboratory"
- P1三篇之间文字重复率控制在10%以内

## 六、四个批次推进计划

| 批次 | 论文 | 时间 |
|:---|:---|:---|
| B1 | P1a, P1b, P1c, P2A, P-DC | 2026 Q1-Q2 |
| B2 | P3a-d, P4a-b | 2026 Q2-Q3 |
| B3 | P4c-d, P5a-d, P6a-b | 2026 Q3-Q4 |
| B4 | P7a-b, P8a-b, P9a-b | 2027 Q1-Q2 |
