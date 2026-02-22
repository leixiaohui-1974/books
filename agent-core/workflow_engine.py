#!/usr/bin/env python3
"""
OpenClaw Agent Core - Workflow Engine
工作流引擎 - 自动生成和管理执行DAG
"""

import json
import yaml
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class TaskNode:
    """任务节点"""
    id: str
    name: str
    description: str
    dependencies: List[str] = field(default_factory=list)
    status: str = "pending"  # pending, running, completed, failed
    output: Any = None
    retry_count: int = 0
    max_retries: int = 3
    
@dataclass
class Workflow:
    """工作流"""
    id: str
    name: str
    description: str
    nodes: Dict[str, TaskNode] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    status: str = "pending"
    
    def add_node(self, node: TaskNode):
        """添加任务节点"""
        self.nodes[node.id] = node
        
    def get_ready_nodes(self) -> List[TaskNode]:
        """获取可以执行的任务（依赖已完成）"""
        ready = []
        for node in self.nodes.values():
            if node.status == "pending":
                deps_satisfied = all(
                    self.nodes[dep].status == "completed"
                    for dep in node.dependencies
                )
                if deps_satisfied:
                    ready.append(node)
        return ready
    
    def is_completed(self) -> bool:
        """检查工作流是否完成"""
        return all(
            node.status in ["completed", "failed"]
            for node in self.nodes.values()
        )
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "nodes": {
                nid: {
                    "id": node.id,
                    "name": node.name,
                    "description": node.description,
                    "dependencies": node.dependencies,
                    "status": node.status,
                    "retry_count": node.retry_count,
                    "max_retries": node.max_retries
                }
                for nid, node in self.nodes.items()
            }
        }
    
    def save(self, filepath: str):
        """保存工作流到文件"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
    
    @classmethod
    def load(cls, filepath: str) -> 'Workflow':
        """从文件加载工作流"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        workflow = cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            status=data["status"],
            created_at=datetime.fromisoformat(data["created_at"])
        )
        
        for nid, node_data in data["nodes"].items():
            node = TaskNode(
                id=node_data["id"],
                name=node_data["name"],
                description=node_data["description"],
                dependencies=node_data["dependencies"],
                status=node_data["status"],
                retry_count=node_data["retry_count"],
                max_retries=node_data["max_retries"]
            )
            workflow.add_node(node)
        
        return workflow


class WorkflowEngine:
    """工作流引擎"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_config(config_path)
        self.workflows: Dict[str, Workflow] = {}
        
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """加载配置"""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        return {
            "execution": {
                "max_parallel": 10,
                "timeout": 1800,
                "retry_count": 3
            }
        }
    
    def create_workflow(self, task_description: str, workflow_id: Optional[str] = None) -> Workflow:
        """
        根据任务描述创建工作流
        
        Args:
            task_description: 任务描述
            workflow_id: 工作流ID（可选）
            
        Returns:
            Workflow对象
        """
        if workflow_id is None:
            workflow_id = f"wf_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # 这里应该调用Task Decomposer来分解任务
        # 简化版本：创建一个示例工作流
        workflow = Workflow(
            id=workflow_id,
            name=f"Workflow for: {task_description[:50]}...",
            description=task_description
        )
        
        # 保存工作流
        self.workflows[workflow_id] = workflow
        
        return workflow
    
    def execute_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """
        执行工作流
        
        Args:
            workflow_id: 工作流ID
            
        Returns:
            执行结果
        """
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        workflow.status = "running"
        
        while not workflow.is_completed():
            ready_nodes = workflow.get_ready_nodes()
            
            if not ready_nodes:
                # 检查是否有失败的任务需要重试
                failed_nodes = [
                    n for n in workflow.nodes.values()
                    if n.status == "failed" and n.retry_count < n.max_retries
                ]
                if failed_nodes:
                    for node in failed_nodes:
                        node.status = "pending"
                        node.retry_count += 1
                    continue
                else:
                    break
            
            # 并行执行就绪的任务
            # 这里应该调用Parallel Executor
            for node in ready_nodes[:self.config["execution"]["max_parallel"]]:
                node.status = "running"
                # 模拟执行
                print(f"Executing task: {node.name}")
                # 实际应该调用sessions_spawn
        
        workflow.status = "completed" if all(
            n.status == "completed" for n in workflow.nodes.values()
        ) else "failed"
        
        return workflow.to_dict()
    
    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """获取工作流状态"""
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")
        return workflow.to_dict()


if __name__ == "__main__":
    # 测试
    engine = WorkflowEngine()
    workflow = engine.create_workflow("生成25万字学术报告")
    print(f"Created workflow: {workflow.id}")
    print(f"Status: {workflow.status}")
