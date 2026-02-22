# OpenClaw Agent Core (OCAC) 使用指南

## 快速开始

### 1. 基础使用

```python
# 导入核心组件
from agent_core.task_decomposer import TaskDecomposer
from agent_core.workflow_engine import WorkflowEngine, TaskNode
from agent_core.parallel_executor import ParallelExecutor, ExecutionTask
from agent_core.evaluator import Evaluator
from agent_core.optimizer import Optimizer

# 创建任务分解器
decomposer = TaskDecomposer()

# 分解任务
task_description = "生成25万字水系统控制论学术报告"
subtasks = decomposer.decompose(task_description, "report_001")

print(f"任务已分解为 {len(subtasks)} 个子任务")
for st in subtasks[:5]:
    print(f"  - {st.name} ({st.estimated_time}分钟)")
```

### 2. 创建工作流

```python
# 创建工作流引擎
workflow_engine = WorkflowEngine()

# 根据子任务创建工作流
workflow = workflow_engine.create_workflow(task_description, "wf_001")

# 添加任务节点
for i, subtask in enumerate(subtasks):
    node = TaskNode(
        id=subtask.id,
        name=subtask.name,
        description=subtask.description,
        dependencies=subtask.dependencies
    )
    workflow.add_node(node)

# 保存工作流
workflow.save("workflow.json")
```

### 3. 并行执行

```python
# 创建并行执行器
executor = ParallelExecutor(max_workers=10)

# 将子任务转换为执行任务
execution_tasks = []
for subtask in subtasks:
    task = ExecutionTask(
        id=subtask.id,
        name=subtask.name,
        command=f"python3 generate_content.py --task '{subtask.name}'",
        timeout=1800,
        dependencies=subtask.dependencies
    )
    execution_tasks.append(task)

# 批量执行
results = executor.execute_batch(execution_tasks)

# 查看结果
for task_id, result in results.items():
    print(f"{task_id}: {result.status} ({result.execution_time:.2f}s)")
```

### 4. 质量评估

```python
# 创建评估器
evaluator = Evaluator()

# 评估生成的内容
with open("generated_content.md", "r") as f:
    content = f.read()

metrics = evaluator.evaluate_text_quality(content, expected_words=5000)

print(f"质量等级: {metrics.quality_level.name}")
print(f"综合得分: {metrics.overall_score:.2f}/5.0")
print(f"准确性: {metrics.accuracy:.2f}")
print(f"完整性: {metrics.completeness:.2f}")
print(f"一致性: {metrics.consistency:.2f}")
print(f"可读性: {metrics.readability:.2f}")

if metrics.feedback:
    print("\n改进建议:")
    for fb in metrics.feedback:
        print(f"  - {fb}")
```

### 5. 迭代优化

```python
# 创建优化器
optimizer = Optimizer(config={"max_iterations": 5})

# 准备评估结果
evaluation_results = {
    "results": {
        task_id: {
            "status": result.status,
            "quality": {
                "score": metrics.overall_score,
                "level": metrics.quality_level.name
            }
        }
        for task_id, result in results.items()
    }
}

# 优化工作流
optimized_workflow = optimizer.optimize(
    workflow.to_dict(),
    evaluation_results,
    iteration=1
)

# 检查是否需要重试
if optimizer.should_retry(metrics):
    print("质量不达标，需要重试优化")
```

## 完整示例：生成25万字报告

```python
#!/usr/bin/env python3
"""
使用OCAC生成25万字学术报告
"""

import os
import sys
sys.path.insert(0, '/root/.openclaw/workspace/books/agent-core')

from task_decomposer import TaskDecomposer
from workflow_engine import WorkflowEngine, TaskNode
from parallel_executor import ParallelExecutor, ExecutionTask
from evaluator import Evaluator
from optimizer import Optimizer

def main():
    # 步骤1: 任务分解
    print("=" * 50)
    print("步骤1: 任务分解")
    print("=" * 50)
    
    decomposer = TaskDecomposer()
    task = "生成25万字水系统控制论学术报告"
    subtasks = decomposer.decompose(task, "chs_report_25w")
    
    print(f"任务已分解为 {len(subtasks)} 个子任务")
    resources = decomposer.estimate_resources(subtasks)
    print(f"预计总时间: {resources['total_time_minutes']} 分钟")
    print(f"预计并行时间: {resources['estimated_wall_time']:.0f} 分钟")
    print(f"最大并行度: {resources['max_parallel']}")
    
    # 步骤2: 创建工作流
    print("\n" + "=" * 50)
    print("步骤2: 创建工作流")
    print("=" * 50)
    
    workflow_engine = WorkflowEngine()
    workflow = workflow_engine.create_workflow(task, "wf_chs_25w")
    
    for subtask in subtasks:
        node = TaskNode(
            id=subtask.id,
            name=subtask.name,
            description=subtask.description,
            dependencies=subtask.dependencies
        )
        workflow.add_node(node)
    
    workflow.save("/tmp/workflow_chs_25w.json")
    print(f"工作流已保存，共 {len(workflow.nodes)} 个节点")
    
    # 步骤3: 并行执行
    print("\n" + "=" * 50)
    print("步骤3: 并行执行")
    print("=" * 50)
    
    executor = ParallelExecutor(max_workers=10)
    
    # 创建执行任务（这里使用echo模拟，实际应该调用生成脚本）
    execution_tasks = []
    for subtask in subtasks:
        task = ExecutionTask(
            id=subtask.id,
            name=subtask.name,
            command=f"echo 'Generating: {subtask.name}'",
            timeout=1800,
            dependencies=subtask.dependencies
        )
        execution_tasks.append(task)
    
    print(f"开始执行 {len(execution_tasks)} 个任务...")
    # results = executor.execute_batch(execution_tasks)
    print("执行完成（模拟）")
    
    # 步骤4: 质量评估
    print("\n" + "=" * 50)
    print("步骤4: 质量评估")
    print("=" * 50)
    
    evaluator = Evaluator()
    # 这里应该评估实际生成的内容
    print("质量评估完成（模拟）")
    
    # 步骤5: 迭代优化
    print("\n" + "=" * 50)
    print("步骤5: 迭代优化")
    print("=" * 50)
    
    optimizer = Optimizer(config={"max_iterations": 3})
    print("优化器已创建")
    
    print("\n" + "=" * 50)
    print("OCAC工作流演示完成!")
    print("=" * 50)

if __name__ == "__main__":
    main()
```

## 命令行使用

```bash
# 进入agent-core目录
cd /root/.openclaw/workspace/books/agent-core

# 运行测试
python3 task_decomposer.py
python3 workflow_engine.py
python3 parallel_executor.py
python3 evaluator.py
python3 optimizer.py

# 运行完整示例
python3 example_usage.py
```

## 配置文件

创建 `config.yaml`:

```yaml
execution:
  max_workers: 10
  timeout: 1800
  retry_count: 3

optimization:
  max_iterations: 5
  threshold: 3.0  # 质量达标阈值

evaluation:
  metrics:
    - accuracy
    - completeness
    - consistency
    - readability

memory:
  storage: github
  repo: books
  path: agent-memory/
```

## 实际应用场景

### 场景1：生成学术报告
```python
task = "生成25万字水系统控制论学术报告"
# → 自动分解为50个5000字模块
# → 并行生成
# → 质量检查
# → 迭代优化
```

### 场景2：代码开发
```python
task = "开发水系统控制仿真软件"
# → 分解为需求分析、架构设计、编码、测试
# → 并行开发各模块
# → 代码审查
# → 集成优化
```

### 场景3：数据分析
```python
task = "分析南水北调工程运行数据"
# → 分解为数据收集、清洗、分析、可视化
# → 并行处理
# → 结果验证
# → 报告生成
```

## 注意事项

1. **实际执行**：示例中使用的是模拟执行，实际应该调用`sessions_spawn`或其他执行方式
2. **错误处理**：生产环境需要添加完善的错误处理和日志记录
3. **资源管理**：大规模并行时注意系统资源限制
4. **结果保存**：重要结果及时保存到GitHub或其他持久化存储

## 下一步

- 集成到OpenClaw工作流中
- 添加Web UI监控界面
- 实现真正的sessions_spawn调用
- 添加更多优化策略
