# [E4] Multi-scale closed-loop coupled real-time water quantity optimization scheduling of cascade pumping station in water supply canal systems

**作者：** Haoshun Xia^a, Chao Wang^b*, Jiahui Sun^c, Xiaohui Lei^b, Hao Wang^b  
**期刊：** Journal of Hydrology, 2024, Vol. 641, Article 131802  
**DOI：** 10.1016/j.jhydrol.2024.131802  
**ScienceDirect：** https://www.sciencedirect.com/science/article/pii/S0022169424011983  
**发表：** 2024年8月

---

## 核心创新点（基于搜索结果）

1. **多尺度闭环耦合实时调度框架**：建立大小尺度相结合的多尺度闭环耦合实时调度框架
2. **双类扰动处理**：同时处理单点和连续水量分配扰动（Both single point and continuous water distribution disturbance）
3. **宏观引导优势**：多尺度相比单一尺度闭环具有宏观引导优势（Compared with a single scale closed loop has the advantage of macro guidance）
4. **综合效益提升**：多尺度滚动优化可提高供水和经济效益（Multi-scale rolling optimization can improve water supply and economic benefits）
5. **可扩展性**：可扩展至更长时间维度的不确定调度问题（It can be extended to solving uncertain scheduling problems with longer time dimensions）

---

## 研究背景

闭环控制是处理供水渠道系统（WSCS）不确定扰动的有效方法。然而，以往研究主要关注单一时间尺度的闭环控制，难以解决长时间维度的不确定性问题。本文提出多尺度闭环耦合实时调度框架，综合考虑大小尺度不确定性，以东线南水北调梯级泵站调度为背景。

---

## 工程背景（东线江苏水源）

南水北调东线工程采用梯级泵站提水输送，从江苏扬州提水北调，经洪泽湖、骆马湖、南四湖、东平湖等调节湖泊，逐级北调至山东、河北。江苏段共设13个梯级，大型泵站33座，设计总调水量148m³/s。

---

## 方法框架

### 多尺度时间嵌套结构

```
长尺度调度（日/旬）：宏观引导，确定总体供水目标
    ↓
中尺度调度（小时）：中层协调，分解供水任务
    ↓  
短尺度调度（分钟）：实时控制，泵站精细调节
    ↓
闭环反馈：状态观测→误差修正→重新滚动优化
```

### 闭环控制结构

- **前馈环节**：基于需水预测制定初始调度方案
- **反馈环节**：实测水位/流量→状态估计→误差补偿
- **滚动优化**：定期更新优化窗口，处理实时不确定性

---

## 书稿应用要点

**对应CHS理论框架：**

| CHS概念 | 论文对应 |
|:---|:---|
| 多尺度时间嵌套控制 | 多尺度闭环框架（大-中-短尺度嵌套） |
| 梯级系统协调控制 | 梯级泵站多尺度联合优化 |
| 闭环反馈自适应 | 基于实测的滚动状态修正 |
| 抗扰动能力 | 单点+连续扰动双重处理能力 |
| WNAL自主性 | 接近L3→L4的自主决策能力 |

**与其他论文的关联：**
- 与[J3] Jin2023的MPC方法互补：E4侧重多尺度协调，J3侧重扰动分类响应
- 与[E5] Yan2022的多目标控制共同构成东线泵站调度技术体系
- 多尺度思想是CHS理论中"时空层次化控制"的核心实证

**适用章节：**
- 东线梯级泵站优化调度技术
- 多尺度闭环控制系统设计
- 供水安全与经济运行协同优化

**引用格式（GB/T）：**
> XIA H, WANG C, SUN J, et al. Multi-scale closed-loop coupled real-time water quantity optimization scheduling of cascade pumping station in water supply canal systems[J]. Journal of Hydrology, 2024, 641: 131802.

---
*资料来源：ScienceDirect搜索结果摘要*  
*整理日期：2026年2月24日*
