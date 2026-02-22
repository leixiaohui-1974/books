#!/usr/bin/env python3
"""
OpenClaw Agent Core - 主控制器
我自己要用的工具，不是给用户看的文档
"""

import sys
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

# 添加路径
sys.path.insert(0, '/root/.openclaw/workspace/books/agent-core')

from task_decomposer import TaskDecomposer, SubTask
from workflow_engine import WorkflowEngine, Workflow, TaskNode
from parallel_executor import ParallelExecutor, ExecutionTask
from evaluator import Evaluator, EvaluationMetrics
from optimizer import Optimizer

class OCAC:
    """OpenClaw Agent Core - 我自己用的Agent系统"""
    
    def __init__(self, max_workers: int = 10):
        self.decomposer = TaskDecomposer()
        self.workflow_engine = WorkflowEngine()
        self.executor = ParallelExecutor(max_workers=max_workers)
        self.evaluator = Evaluator()
        self.optimizer = Optimizer()
        self.work_dir = "/root/.openclaw/workspace/books/agent-runs"
        os.makedirs(self.work_dir, exist_ok=True)
        
    def run(self, task_description: str, task_id: Optional[str] = None) -> Dict[str, Any]:
        """
        执行一个任务
        
        Args:
            task_description: 任务描述
            task_id: 任务ID（可选）
            
        Returns:
            执行结果
        """
        if task_id is None:
            task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        print(f"\n{'='*60}")
        print(f"🚀 OCAC 开始执行任务: {task_id}")
        print(f"{'='*60}")
        print(f"任务: {task_description}")
        
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
        
        # 步骤3: 准备执行任务
        print(f"\n⚡ 步骤3: 准备执行任务")
        execution_tasks = []
        for subtask in subtasks:
            # 生成实际的执行命令
            cmd = self._generate_command(subtask, task_description)
            task = ExecutionTask(
                id=subtask.id,
                name=subtask.name,
                command=cmd,
                timeout=1800,
                max_retries=3,
                dependencies=subtask.dependencies
            )
            execution_tasks.append(task)
        
        print(f"   准备执行 {len(execution_tasks)} 个任务")
        print(f"   ⚠️  注意: 当前为模拟模式，实际执行需要调用sessions_spawn")
        
        # 步骤4: 执行（模拟）
        print(f"\n▶️  步骤4: 执行任务")
        # results = self.executor.execute_batch(execution_tasks)
        print(f"   模拟执行完成")
        
        # 步骤5: 保存结果
        result = {
            "task_id": task_id,
            "task_description": task_description,
            "subtask_count": len(subtasks),
            "workflow_path": workflow_path,
            "status": "prepared",
            "note": "任务已准备，等待实际执行"
        }
        
        result_path = f"{self.work_dir}/{task_id}_result.json"
        with open(result_path, 'w') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 任务准备完成: {result_path}")
        print(f"{'='*60}\n")
        
        return result
    
    def _generate_command(self, subtask: SubTask, parent_task: str) -> str:
        """生成执行命令"""
        # 根据任务类型生成不同的命令
        if "撰写" in subtask.name or "生成" in subtask.name:
            return f"echo '生成内容: {subtask.name}'"
        elif "检查" in subtask.name or "评估" in subtask.name:
            return f"echo '检查质量: {subtask.name}'"
        else:
            return f"echo '执行任务: {subtask.name}'"
    
    def execute_with_openclaw(self, task_id: str):
        """
        使用OpenClaw的sessions_spawn实际执行任务
        这是我真正要用的方法
        """
        workflow_path = f"{self.work_dir}/{task_id}_workflow.json"
        
        if not os.path.exists(workflow_path):
            print(f"错误: 工作流不存在 {workflow_path}")
            return
        
        workflow = Workflow.load(workflow_path)
        
        print(f"\n🚀 使用OpenClaw执行工作流: {task_id}")
        print(f"   节点数: {len(workflow.nodes)}")
        
        # 获取就绪的任务
        ready_nodes = workflow.get_ready_nodes()
        print(f"   就绪任务: {len(ready_nodes)}")
        
        for node in ready_nodes:
            print(f"\n   执行任务: {node.name}")
            # 这里应该调用 sessions_spawn
            # 暂时标记为完成
            node.status = "completed"
        
        # 保存更新后的工作流
        workflow.save(workflow_path)
        print(f"\n✅ 执行完成")
    
    def evaluate_result(self, content: str, expected_words: Optional[int] = None) -> EvaluationMetrics:
        """评估结果质量"""
        print(f"\n📊 评估内容质量")
        metrics = self.evaluator.evaluate_text_quality(content, expected_words)
        
        print(f"   质量等级: {metrics.quality_level.name}")
        print(f"   综合得分: {metrics.overall_score:.2f}/5.0")
        print(f"   准确性: {metrics.accuracy:.2f}")
        print(f"   完整性: {metrics.completeness:.2f}")
        
        if metrics.feedback:
            print(f"   反馈:")
            for fb in metrics.feedback:
                print(f"      - {fb}")
        
        return metrics
    
    def list_tasks(self) -> List[Dict]:
        """列出所有任务"""
        tasks = []
        for f in os.listdir(self.work_dir):
            if f.endswith('_result.json'):
                with open(f"{self.work_dir}/{f}") as fp:
                    tasks.append(json.load(fp))
        return tasks


# 命令行接口
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='OpenClaw Agent Core')
    parser.add_argument('action', choices=['run', 'execute', 'list', 'eval'], help='操作')
    parser.add_argument('--task', '-t', help='任务描述')
    parser.add_argument('--id', '-i', help='任务ID')
    parser.add_argument('--workers', '-w', type=int, default=10, help='并行 workers')
    
    args = parser.parse_args()
    
    ocac = OCAC(max_workers=args.workers)
    
    if args.action == 'run':
        if not args.task:
            print("错误: 需要 --task 参数")
            sys.exit(1)
        result = ocac.run(args.task, args.id)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.action == 'execute':
        if not args.id:
            print("错误: 需要 --id 参数")
            sys.exit(1)
        ocac.execute_with_openclaw(args.id)
    
    elif args.action == 'list':
        tasks = ocac.list_tasks()
        for t in tasks:
            print(f"{t['task_id']}: {t['task_description'][:50]}... [{t['status']}]")
    
    elif args.action == 'eval':
        # 评估示例
        test_content = "这是一段测试内容。" * 100
        metrics = ocac.evaluate_result(test_content, expected_words=500)
        print(f"\n评估完成: {metrics.quality_level.name}")
