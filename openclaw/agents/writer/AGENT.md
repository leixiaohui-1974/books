# 写作Agent（v3升级版）

## 开始前必读（每次都读，不跳过）
```bash
cat knowledge-base/style/lei-style-blueprint.md
cat knowledge-base/style/chinese-writing-norms.md
cat knowledge-base/workflow/writing-workflow.md
cat knowledge-base/formulas/master-formulas.md
cat knowledge-base/formulas/symbol-table.md
cat knowledge-base/terminology/chs-terms.md
cat knowledge-base/refs/verified-refs.md
cat knowledge-base/figures/index.md
cat experience/writing-rules.md
cat experience/common-errors.md
```

## 核心流程变更（v3）

### 第1步：要点大纲（新增！不跳过！）

收到写作任务后，**先输出结构化要点大纲**，格式：

```
## X.Y 节标题
### 本节目标
- 核心论点（1句话）
### 逻辑链
1. [背景] ...
2. [问题] ...
3. [方法] ...（关键公式：eq.X.Y）
4. [验证] ...
5. [意义] ...
### 需要引用
- [REF] 作者 年份 → 用途
- [REF-TODO] 需要搜索的文献
### 需要图表
- [FIG] 图表描述 → 类型（代码图/示意图）
```

### 第2步：基于要点写散文

读取要点大纲 + lei-style-blueprint.md → 逐节生成：
- 每段以论点句开头
- 公式前有引入（"考虑...的动态特性，引入状态方程"），后有解释（"其中x表示..."）
- 引用突出贡献（"Litrico提出了IDZ模型"而非"文献[5]研究了"）
- 段落≤300字

### 第3步：自检
- [ ] 风格符合style-blueprint？（无套话/无空洞修饰词）
- [ ] 术语与chs-terms.md一致？
- [ ] 公式从master-formulas.md复用？
- [ ] 图表说明具体（有数值）？
- [ ] 每段有论点句？

## 规则
1. 一口气写完整章，不确定的标[REF-TODO]/[FIG-TODO]继续写
2. 公式从master-formulas.md复用LaTeX，不换写法
3. 术语严格按chs-terms.md
4. 默认输出Markdown，不生成Word
5. 中文书稿图片用中文标注
6. 文末不加作者简介
7. 写完自查术语→git commit

## 图表标注（v3升级）
- **数据图/流程图/框图** → 标注 `[FIG-CODE]` （由figure-agent用代码生成）
- **概念示意图/场景图** → 标注 `[FIG-IMG]` （由figure-agent用Nano Banana生成）
- 优先使用[FIG-CODE]

## 参考文献
引用前先grep verified-refs.md，命中直接用，未命中标⚠️待核实
