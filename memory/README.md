# GitHub永久记忆存储配置

## 存储仓库
- **仓库**: https://github.com/leixiaohui-1974/books
- **本地路径**: /root/.openclaw/workspace/books
- **记忆目录**: /root/.openclaw/workspace/books/memory/

## 存储结构
```
books/
├── memory/                    # AI记忆存储
│   ├── conversations/         # 对话记录
│   ├── reports/              # 生成的报告
│   ├── skills/               # 技能学习记录
│   ├── workflows/            # 工作流设计
│   └── decisions/            # 重要决策记录
├── reports/                   # 已生成的报告
│   └── 25w-report/           # 25万字报告
└── ...                       # 原有内容
```

## 自动提交规则
1. 每次生成重要文档后，自动git add
2. 每天结束时自动commit和push
3. 重要决策立即commit

## 提交信息格式
- 报告: "Add report: [标题] ([字数]字)"
- 记忆: "Update memory: [类型] - [摘要]"
- 技能: "Add skill: [技能名]"

## 访问方式
- GitHub网页: https://github.com/leixiaohui-1974/books/tree/main/memory
- 本地: /root/.openclaw/workspace/books/memory/
