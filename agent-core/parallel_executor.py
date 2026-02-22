#!/usr/bin/env python3
"""
OpenClaw Agent Core - Parallel Executor
并行执行器 - 使用sessions_spawn并行执行子任务
"""

import json
import time
import subprocess
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

@dataclass
class ExecutionResult:
    """执行结果"""
    task_id: str
    status: str  # success, failed, timeout
    output: Any = None
    error: Optional[str] = None
    execution_time: float = 0.0
    retry_count: int = 0

@dataclass
class ExecutionTask:
    """执行任务"""
    id: str
    name: str
    command: str  # 要执行的命令或脚本
    timeout: int = 1800  # 超时时间（秒）
    retry_count: int = 0
    max_retries: int = 3
    dependencies: List[str] = field(default_factory=list)
    callback: Optional[Callable] = None


class ParallelExecutor:
    """并行执行器"""
    
    def __init__(self, max_workers: int = 10, config: Optional[Dict] = None):
        self.max_workers = max_workers
        self.config = config or {}
        self.execution_history: List[Dict] = []
        self._lock = threading.Lock()
        
    def execute_single(self, task: ExecutionTask) -> ExecutionResult:
        """
        执行单个任务
        
        Args:
            task: 执行任务
            
        Returns:
            执行结果
        """
        start_time = time.time()
        
        try:
            # 使用subprocess执行命令
            # 实际应该调用sessions_spawn，这里模拟
            result = subprocess.run(
                task.command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=task.timeout
            )
            
            execution_time = time.time() - start_time
            
            if result.returncode == 0:
                return ExecutionResult(
                    task_id=task.id,
                    status="success",
                    output=result.stdout,
                    execution_time=execution_time,
                    retry_count=task.retry_count
                )
            else:
                return ExecutionResult(
                    task_id=task.id,
                    status="failed",
                    error=result.stderr,
                    execution_time=execution_time,
                    retry_count=task.retry_count
                )
                
        except subprocess.TimeoutExpired:
            return ExecutionResult(
                task_id=task.id,
                status="timeout",
                error=f"Task timed out after {task.timeout} seconds",
                execution_time=task.timeout,
                retry_count=task.retry_count
            )
        except Exception as e:
            return ExecutionResult(
                task_id=task.id,
                status="failed",
                error=str(e),
                execution_time=time.time() - start_time,
                retry_count=task.retry_count
            )
    
    def execute_batch(self, tasks: List[ExecutionTask]) -> Dict[str, ExecutionResult]:
        """
        批量并行执行任务
        
        Args:
            tasks: 任务列表
            
        Returns:
            任务ID到结果的映射
        """
        results = {}
        completed_tasks = set()
        pending_tasks = {t.id: t for t in tasks}
        
        while pending_tasks:
            # 找出可以执行的任务（依赖已完成）
            ready_tasks = []
            for task_id, task in list(pending_tasks.items()):
                deps_satisfied = all(
                    dep in completed_tasks and results.get(dep, ExecutionResult("", "")).status == "success"
                    for dep in task.dependencies
                )
                if deps_satisfied:
                    ready_tasks.append(task)
            
            if not ready_tasks:
                # 检查是否有失败的任务需要重试
                failed_tasks = [
                    results[tid] for tid in completed_tasks
                    if results[tid].status == "failed" and results[tid].retry_count < tasks[0].max_retries
                ]
                if failed_tasks:
                    for result in failed_tasks:
                        # 重置为pending状态，增加重试计数
                        task = next(t for t in tasks if t.id == result.task_id)
                        task.retry_count = result.retry_count + 1
                        pending_tasks[result.task_id] = task
                        del results[result.task_id]
                        completed_tasks.remove(result.task_id)
                    continue
                else:
                    break
            
            # 并行执行就绪的任务
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                future_to_task = {
                    executor.submit(self.execute_single, task): task
                    for task in ready_tasks[:self.max_workers]
                }
                
                for future in as_completed(future_to_task):
                    task = future_to_task[future]
                    try:
                        result = future.result()
                        results[task.id] = result
                        completed_tasks.add(task.id)
                        del pending_tasks[task.id]
                        
                        # 记录执行历史
                        with self._lock:
                            self.execution_history.append({
                                "task_id": task.id,
                                "status": result.status,
                                "execution_time": result.execution_time,
                                "timestamp": datetime.now().isoformat()
                            })
                        
                        # 调用回调函数
                        if task.callback:
                            task.callback(result)
                            
                    except Exception as e:
                        results[task.id] = ExecutionResult(
                            task_id=task.id,
                            status="failed",
                            error=str(e)
                        )
                        completed_tasks.add(task.id)
                        del pending_tasks[task.id]
        
        return results
    
    def execute_with_sessions_spawn(self, tasks: List[ExecutionTask]) -> Dict[str, ExecutionResult]:
        """
        使用sessions_spawn执行（OpenClaw原生方式）
        
        这是推荐的执行方式，可以真正利用OpenClaw的并行能力
        """
        results = {}
        
        # 这里应该调用OpenClaw的sessions_spawn工具
        # 简化版本：记录任务信息，实际执行由调用方处理
        for task in tasks:
            results[task.id] = ExecutionResult(
                task_id=task.id,
                status="pending",
                output=f"Task queued for sessions_spawn: {task.name}"
            )
        
        return results
    
    def get_execution_stats(self) -> Dict[str, Any]:
        """获取执行统计信息"""
        if not self.execution_history:
            return {}
        
        total_tasks = len(self.execution_history)
        success_count = sum(1 for h in self.execution_history if h["status"] == "success")
        failed_count = sum(1 for h in self.execution_history if h["status"] == "failed")
        timeout_count = sum(1 for h in self.execution_history if h["status"] == "timeout")
        
        avg_time = sum(h["execution_time"] for h in self.execution_history) / total_tasks if total_tasks > 0 else 0
        
        return {
            "total_tasks": total_tasks,
            "success_count": success_count,
            "failed_count": failed_count,
            "timeout_count": timeout_count,
            "success_rate": success_count / total_tasks if total_tasks > 0 else 0,
            "average_execution_time": avg_time
        }
    
    def save_execution_log(self, filepath: str):
        """保存执行日志"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                "execution_history": self.execution_history,
                "stats": self.get_execution_stats()
            }, f, ensure_ascii=False, indent=2)


# 与Workflow Engine集成的执行器
class WorkflowExecutor:
    """工作流执行器 - 集成Workflow Engine和Parallel Executor"""
    
    def __init__(self, workflow_engine, parallel_executor: ParallelExecutor):
        self.workflow_engine = workflow_engine
        self.parallel_executor = parallel_executor
        
    def execute_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """
        执行工作流
        
        Args:
            workflow_id: 工作流ID
            
        Returns:
            执行结果
        """
        from workflow_engine import Workflow
        
        workflow = self.workflow_engine.workflows.get(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        # 将Workflow节点转换为ExecutionTask
        tasks = []
        for node_id, node in workflow.nodes.items():
            task = ExecutionTask(
                id=node_id,
                name=node.name,
                command=f"echo 'Executing {node.name}'",  # 实际应该根据节点类型生成命令
                timeout=1800,
                max_retries=node.max_retries,
                dependencies=node.dependencies
            )
            tasks.append(task)
        
        # 并行执行
        results = self.parallel_executor.execute_batch(tasks)
        
        # 更新工作流状态
        for node_id, result in results.items():
            workflow.nodes[node_id].status = (
                "completed" if result.status == "success" else "failed"
            )
            workflow.nodes[node_id].output = result.output
        
        workflow.status = "completed" if all(
            n.status == "completed" for n in workflow.nodes.values()
        ) else "failed"
        
        return {
            "workflow_id": workflow_id,
            "status": workflow.status,
            "results": {
                task_id: {
                    "status": result.status,
                    "execution_time": result.execution_time,
                    "error": result.error
                }
                for task_id, result in results.items()
            }
        }


if __name__ == "__main__":
    # 测试
    executor = ParallelExecutor(max_workers=5)
    
    # 创建测试任务
    tasks = [
        ExecutionTask(id=f"task_{i}", name=f"Task {i}", command=f"echo 'Hello from task {i}'")
        for i in range(10)
    ]
    
    # 执行
    results = executor.execute_batch(tasks)
    
    # 输出结果
    for task_id, result in results.items():
        print(f"{task_id}: {result.status} ({result.execution_time:.2f}s)")
    
    # 统计
    stats = executor.get_execution_stats()
    print(f"\nStats: {stats}")
