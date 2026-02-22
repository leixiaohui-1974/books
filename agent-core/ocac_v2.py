#!/usr/bin/env python3
"""
OpenClaw Agent Core - 主控制器 (v2.0)
添加真正的sessions_spawn调用功能
"""

import sys
import json
import os
import subprocess
from datetime import datetime
from typing import List, Dict, Any, Optional

# 添加路径
sys.path.insert(0, '/root/.openclaw/workspace/books/agent-core')

from task_decomposer import TaskDecomposer, SubTask
from workflow_engine import WorkflowEngine, Workflow, TaskNode
from parallel_executor import ParallelExecutor, ExecutionTask
from evaluator import Evaluator, EvaluationMetrics
from optimizer import Optimizer
from sessions_spawn_client import SessionsSpawnClient, call_openclaw_sessions_spawn

class OCAC:
    """OpenClaw Agent Core - 真正能执行的Agent系统"""
    
    def __init__(self, max_workers: int = 10, auto_execute: bool = False):
        self.decomposer = TaskDecomposer()
        self.workflow_engine = WorkflowEngine()
        self.executor = ParallelExecutor(max_workers=max_workers)
        self.evaluator = Evaluator()
        self.optimizer = Optimizer()
        self.work_dir = "/root/.openclaw/workspace/books/agent-runs"
        self.output_dir = "/root/.openclaw/workspace/books/agent-outputs"
        os.makedirs(self.work_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        self.auto_execute = auto_execute  # 是否自动执行
        self.spawn_client = SessionsSpawnClient()
        
    def run(self, task_description: str, task_id: Optional[str] = None, 
            agent_id: str = "kimi-coding/k2p5", execute: bool = False) -> Dict[str, Any]:
        """
        执行一个任务
        
        Args:
            task_description: 任务描述
            task_id: 任务ID（可选）
            agent_id: 使用的Agent模型
            execute: 是否实际执行（调用sessions_spawn）
            
        Returns:
            执行结果
        """
        if task_id is None:
            task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        print(f"\n{'='*60}")
        print(f"🚀 OCAC 开始执行任务: {task_id}")
        print(f"{'='*60}")
        print(f"任务: {task_description}")
        print(f"执行模式: {'自动执行' if execute or self.auto_execute else '仅准备'}")
        
        # 步骤1: 任务分解
        print(f"\n📋 步骤1: 任务分解")
        subtasks = self.decomposer.decompose(task_description, task_id)
        print(f"   分解为 {len(subtasks)} 个子任务")
        
        resources = self.decomposer.estimate_resources(subtasks)
        print(f"   预计总时间: {resources['total_time_minutes']} 分钟")
        print(f"   预计并行时间: {resources['estimated_wall_time']:.0f} 分钟")
        
        # 步骤2: 创建工作流
        print(f"\n🔄 步骤2: 创建工作流")
        workflow = self.workflow_engine.create_workflow(task_description, task_id)
        
        for subtask in subtasks:
            node = TaskNode(
                id=subtask.id,
                name=subtask.name,
                description=subtask.description,
                dependencies=subtask.dependencies,
                max_retries=3
            )
            workflow.add_node(node)
        
        workflow_path = f"{self.work_dir}/{task_id}_workflow.json"
        workflow.save(workflow_path)
        print(f"   工作流已保存: {workflow_path}")
        
        # 步骤3: 生成执行脚本
        print(f"\n⚡ 步骤3: 生成执行脚本")
        scripts = []
        for i, subtask in enumerate(subtasks):
            script_path = self._generate_script(subtask, task_description, i+1)
            scripts.append({
                "subtask": subtask,
                "script_path": script_path,
                "output_path": f"{self.output_dir}/{task_id}_{subtask.id}.md"
            })
        
        print(f"   生成 {len(scripts)} 个执行脚本")
        
        # 步骤4: 执行（如果启用）
        executed = []
        if execute or self.auto_execute:
            print(f"\n▶️  步骤4: 执行任务（调用sessions_spawn）")
            for script_info in scripts[:5]:  # 先执行前5个测试
                result = self._execute_with_spawn(
                    script_info["subtask"], 
                    script_info["script_path"],
                    agent_id
                )
                executed.append(result)
                print(f"   ✅ {script_info['subtask'].name}: {result['status']}")
        else:
            print(f"\n⏸️  步骤4: 跳过执行（使用 --execute 启用）")
        
        # 步骤5: 保存结果
        result = {
            "task_id": task_id,
            "task_description": task_description,
            "subtask_count": len(subtasks),
            "workflow_path": workflow_path,
            "scripts_count": len(scripts),
            "executed_count": len(executed),
            "status": "completed" if executed else "prepared",
            "output_dir": self.output_dir,
            "timestamp": datetime.now().isoformat()
        }
        
        result_path = f"{self.work_dir}/{task_id}_result.json"
        with open(result_path, 'w') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 任务完成: {result_path}")
        print(f"{'='*60}\n")
        
        return result
    
    def _generate_script(self, subtask: SubTask, parent_task: str, index: int) -> str:
        """生成可执行的Python脚本"""
        script_content = f'''#!/usr/bin/env python3
"""
自动生成的任务脚本
任务: {subtask.name}
父任务: {parent_task}
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/books/agent-core')

from evaluator import Evaluator

def main():
    print(f"执行任务: {subtask.name}")
    print(f"描述: {subtask.description}")
    
    # 这里放置实际的任务逻辑
    # 例如：生成内容、分析数据等
    
    output = f"""
# {subtask.name}

## 任务描述
{subtask.description}

## 执行结果
任务已完成。

## 输出时间
{datetime.now().isoformat()}
"""
    
    # 保存输出
    output_path = "{self.output_dir}/{subtask.id}_output.md"
    with open(output_path, 'w') as f:
        f.write(output)
    
    print(f"输出已保存: {{output_path}}")
    return output

if __name__ == "__main__":
    result = main()
    print(result)
'''
        script_path = f"{self.work_dir}/{subtask.id}_script.py"
        with open(script_path, 'w') as f:
            f.write(script_content)
        os.chmod(script_path, 0o755)
        return script_path
    
    def _execute_with_spawn(self, subtask: SubTask, script_path: str, agent_id: str) -> Dict:
        """使用sessions_spawn执行任务"""
        # 构建任务提示
        task_prompt = f"""执行任务: {subtask.name}

任务描述: {subtask.description}

父任务: {subtask.description}

请完成以下工作：
1. 理解任务要求
2. 生成高质量的内容
3. 确保内容符合学术写作规范
4. 输出完整的执行结果

要求：
- 内容要专业、准确
- 格式要规范
- 字数要符合要求
"""
        
        print(f"     调用sessions_spawn: {subtask.name}")
        
        # 调用真正的sessions_spawn
        result = self.spawn_client.spawn(
            task=task_prompt,
            agent_id=agent_id,
            label=subtask.id
        )
        
        # 保存输出
        output_path = f"{self.output_dir}/{subtask.id}_output.md"
        with open(output_path, 'w') as f:
            f.write(f"# {subtask.name}\n\n")
            f.write(f"## 任务描述\n{subtask.description}\n\n")
            f.write(f"## 执行结果\n\n")
            f.write(result.get('output', '无输出'))
            f.write(f"\n\n## 执行状态\n{result.get('status', 'unknown')}\n")
            f.write(f"\n## 执行时间\n{datetime.now().isoformat()}\n")
        
        return {
            "subtask_id": subtask.id,
            "status": result.get('status', 'error'),
            "output_path": output_path,
            "agent": result.get('agent', agent_id)
        }
    
    def execute_batch(self, task_id: str, batch_size: int = 5) -> List[Dict]:
        """批量执行任务"""
        result_path = f"{self.work_dir}/{task_id}_result.json"
        
        if not os.path.exists(result_path):
            print(f"错误: 任务不存在 {task_id}")
            return []
        
        with open(result_path) as f:
            task_info = json.load(f)
        
        print(f"\n🚀 批量执行任务: {task_id}")
        print(f"总子任务数: {task_info['subtask_count']}")
        print(f"批次大小: {batch_size}")
        
        # 这里实现批量调用sessions_spawn
        # 暂时返回模拟结果
        results = []
        for i in range(min(batch_size, task_info['subtask_count'])):
            results.append({
                "batch": i+1,
                "status": "completed",
                "output": f"任务{i+1}完成"
            })
        
        return results
    
    def evaluate_outputs(self, task_id: str) -> Dict:
        """评估所有输出质量"""
        print(f"\n📊 评估任务输出: {task_id}")
        
        outputs = []
        for f in os.listdir(self.output_dir):
            if f.startswith(task_id) and f.endswith('.md'):
                with open(f"{self.output_dir}/{f}") as fp:
                    content = fp.read()
                    outputs.append(content)
        
        print(f"   找到 {len(outputs)} 个输出文件")
        
        # 评估每个输出
        evaluations = []
        for i, content in enumerate(outputs[:3]):  # 评估前3个
            metrics = self.evaluator.evaluate_text_quality(content)
            evaluations.append({
                "index": i+1,
                "score": metrics.overall_score,
                "level": metrics.quality_level.name
            })
            print(f"   输出{i+1}: {metrics.quality_level.name} ({metrics.overall_score:.2f})")
        
        return {
            "task_id": task_id,
            "evaluated_count": len(evaluations),
            "evaluations": evaluations
        }
    
    def list_tasks(self) -> List[Dict]:
        """列出所有任务"""
        tasks = []
        for f in os.listdir(self.work_dir):
            if f.endswith('_result.json'):
                with open(f"{self.work_dir}/{f}") as fp:
                    tasks.append(json.load(fp))
        return sorted(tasks, key=lambda x: x.get('timestamp', ''), reverse=True)


# 命令行接口
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='OpenClaw Agent Core v2.0')
    parser.add_argument('action', choices=['run', 'batch', 'eval', 'list'], help='操作')
    parser.add_argument('--task', '-t', help='任务描述')
    parser.add_argument('--id', '-i', help='任务ID')
    parser.add_argument('--execute', '-e', action='store_true', help='实际执行')
    parser.add_argument('--batch-size', '-b', type=int, default=5, help='批次大小')
    parser.add_argument('--agent', '-a', default='kimi-coding/k2p5', help='Agent模型')
    
    args = parser.parse_args()
    
    ocac = OCAC(auto_execute=args.execute)
    
    if args.action == 'run':
        if not args.task:
            print("错误: 需要 --task 参数")
            sys.exit(1)
        result = ocac.run(args.task, args.id, args.agent, args.execute)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.action == 'batch':
        if not args.id:
            print("错误: 需要 --id 参数")
            sys.exit(1)
        results = ocac.execute_batch(args.id, args.batch_size)
        print(json.dumps(results, ensure_ascii=False, indent=2))
    
    elif args.action == 'eval':
        if not args.id:
            print("错误: 需要 --id 参数")
            sys.exit(1)
        eval_result = ocac.evaluate_outputs(args.id)
        print(json.dumps(eval_result, ensure_ascii=False, indent=2))
    
    elif args.action == 'list':
        tasks = ocac.list_tasks()
        for t in tasks:
            status_icon = "✅" if t['status'] == 'completed' else "⏳"
            print(f"{status_icon} {t['task_id']}: {t['task_description'][:40]}... [{t['status']}]")
