# HydroScribe 多智能体写作 Skill (阿里云百炼优化版)

## 功能描述

此 Skill 封装了 HydroScribe 多智能体协同写作系统，可自动完成学术文档的写作、评审和质量检查。

系统包含：
- **9 个 Writer Agent**: 教材(BK)、SCI论文(SCI)、中文论文(CN)、专利(PAT)、报告(RPT)、国标(STD-CN)、国际标准(STD-INT)、公众号(WX)、PPT(PPT)
- **28 个 Reviewer Agent**: 按文体匹配的多角色加权评审
- **3 个 Utility Agent**: 术语检查、跨书一致性、参考文献管理

## 使用场景

- 撰写 CHS 水系统控制论教材体系的各章节
- 生成学术论文（中英文）
- 撰写发明专利说明书
- 生成技术报告、标准文档
- 多书目协同写作，确保术语和内容一致性

## 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| book_id | string | 是 | 书目编号，如 "T2a", "M1", "T1-CN" |
| skill_type | string | 否 | 写作类型，默认 "BK"，可选 SCI/CN/PAT/RPT 等 |
| chapter_id | string | 否 | 章节编号，如 "ch07"，留空则自动选择下一章 |
| gate_mode | string | 否 | 审批模式，"auto"(自动) / "human"(人工) / "hybrid"(混合) |

## 输出结果

- **JSON 文件**: 包含写作状态、字数、评审分数、文件路径等信息
- **Markdown 文件**: 完成的章节内容保存在 books/{book_id}/ 目录

## 调用示例

用户可通过自然语言触发：

- "帮我写 T2a 第七章 模型预测控制"
- "用 SCI 论文格式写一篇关于明渠降阶建模的论文"
- "生成水系统控制论第三章的专利申请书"

## 技术架构

```
OpenClaw Gateway → run_hydroscribe_skill.sh
  → HydroScribe API (http://hydroscribe_api:8000)
    → Orchestrator
      → Writer Agent (百炼 qwen-plus/qwen-max)
      → 3× Utility Agent (并行质检)
      → N× Reviewer Agent (并行评审)
    → 评分 = 0.80 × 评审加权分 + 0.20 × 质检分
    → 门控决策 → 通过/驳回/人工审批
```

## 注意事项

- 需要配置阿里云百炼 API Key（环境变量 `DASHSCOPE_API_KEY`）
- 单章写作可能需要 5-30 分钟，取决于目标字数和模型速度
- 确保 ECS 安全组放行 `dashscope.aliyuncs.com:443` 出站
