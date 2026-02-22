#!/usr/bin/env python3
"""
OpenClaw Agent Core - Optimizer
优化器 - 基于反馈迭代优化工作流和任务
"""

import json
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class OptimizationStrategy:
    """优化策略"""
    name: str
    description: str
    apply_func: Callable  # 应用优化的函数
    priority: int = 1

@dataclass
class OptimizationRecord:
    """优化记录"""
    iteration: int
    strategy: str
    changes: Dict[str, Any]
    improvement: float  # 改进幅度
    timestamp: datetime = field(default_factory=datetime.now)


class Optimizer:
    """优化器"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.optimization_history: List[OptimizationRecord] = []
        self.strategies: Dict[str, OptimizationStrategy] = {}
        self._register_default_strategies()
    
    def _register_default_strategies(self):
        """注册默认优化策略"""
        self.strategies = {
            "retry_failed": OptimizationStrategy(
                name="retry_failed",
                description="重试失败的任务",
                apply_func=self._retry_failed_tasks,
                priority=1
            ),
            "increase_timeout": OptimizationStrategy(
                name="increase_timeout",
                description="增加超时时间",
                apply_func=self._increase_timeout,
                priority=2
            ),
            "adjust_parallel": OptimizationStrategy(
                name="adjust_parallel",
                description="调整并行度",
                apply_func=self._adjust_parallel,
                priority=3
            ),
            "refine_decomposition": OptimizationStrategy(
                name="refine_decomposition",
                description="细化任务分解",
                apply_func=self._refine_decomposition,
                priority=4
            ),
            "improve_prompt": OptimizationStrategy(
                name="improve_prompt",
                description="改进提示词",
                apply_func=self._improve_prompt,
                priority=5
            )
        }
    
    def optimize(self, workflow: Dict[str, Any], evaluation_results: Dict[str, Any], 
                 iteration: int = 1) -> Dict[str, Any]:
        """
        优化工作流
        
        Args:
            workflow: 当前工作流
            evaluation_results: 评估结果
            iteration: 当前迭代次数
            
        Returns:
            优化后的工作流
        """
        if iteration > self.config.get("max_iterations", 5):
            print(f"Reached max iterations ({self.config.get('max_iterations', 5)}), stopping optimization.")
            return workflow
        
        optimized_workflow = workflow.copy()
        improvements = []
        
        # 分析评估结果，确定需要优化的方面
        issues = self._analyze_issues(evaluation_results)
        
        # 按优先级应用优化策略
        for strategy_name, strategy in sorted(self.strategies.items(), key=lambda x: x[1].priority):
            if strategy_name in issues:
                print(f"Applying optimization strategy: {strategy.name}")
                changes = strategy.apply_func(optimized_workflow, evaluation_results)
                
                if changes:
                    improvements.append({
                        "strategy": strategy_name,
                        "changes": changes
                    })
                    
                    # 记录优化
                    record = OptimizationRecord(
                        iteration=iteration,
                        strategy=strategy_name,
                        changes=changes,
                        improvement=self._estimate_improvement(changes)
                    )
                    self.optimization_history.append(record)
        
        return optimized_workflow
    
    def _analyze_issues(self, evaluation_results: Dict[str, Any]) -> List[str]:
        """分析问题"""
        issues = []
        
        for task_id, result in evaluation_results.get("results", {}).items():
            if result.get("status") == "failed":
                issues.append("retry_failed")
            elif result.get("status") == "timeout":
                issues.append("increase_timeout")
            
            # 检查质量
            quality = result.get("quality", {})
            if quality.get("score", 0) < 3.0:
                issues.append("improve_prompt")
        
        # 去重
        return list(set(issues))
    
    def _retry_failed_tasks(self, workflow: Dict[str, Any], evaluation_results: Dict[str, Any]) -> Dict[str, Any]:
        """重试失败的任务"""
        changes = {}
        
        for task_id, result in evaluation_results.get("results", {}).items():
            if result.get("status") == "failed":
                # 找到对应的任务节点
                if task_id in workflow.get("nodes", {}):
                    node = workflow["nodes"][task_id]
                    if node.get("retry_count", 0) < node.get("max_retries", 3):
                        node["status"] = "pending"
                        node["retry_count"] = node.get("retry_count", 0) + 1
                        changes[task_id] = f"Retry count: {node['retry_count']}"
        
        return changes
    
    def _increase_timeout(self, workflow: Dict[str, Any], evaluation_results: Dict[str, Any]) -> Dict[str, Any]:
        """增加超时时间"""
        changes = {}
        
        for task_id, result in evaluation_results.get("results", {}).items():
            if result.get("status") == "timeout":
                if task_id in workflow.get("nodes", {}):
                    node = workflow["nodes"][task_id]
                    old_timeout = node.get("timeout", 1800)
                    new_timeout = int(old_timeout * 1.5)
                    node["timeout"] = new_timeout
                    changes[task_id] = f"Timeout: {old_timeout}s -> {new_timeout}s"
        
        return changes
    
    def _adjust_parallel(self, workflow: Dict[str, Any], evaluation_results: Dict[str, Any]) -> Dict[str, Any]:
        """调整并行度"""
        changes = {}
        
        # 如果有大量任务失败，减少并行度
        failed_count = sum(1 for r in evaluation_results.get("results", {}).values() if r.get("status") == "failed")
        total_count = len(evaluation_results.get("results", {}))
        
        if failed_count / total_count > 0.3:  # 失败率超过30%
            current_parallel = workflow.get("max_parallel", 10)
            new_parallel = max(1, current_parallel // 2)
            workflow["max_parallel"] = new_parallel
            changes["global"] = f"Max parallel: {current_parallel} -> {new_parallel}"
        
        return changes
    
    def _refine_decomposition(self, workflow: Dict[str, Any], evaluation_results: Dict[str, Any]) -> Dict[str, Any]:
        """细化任务分解"""
        changes = {}
        
        # 对于执行时间过长的任务，建议进一步分解
        for task_id, result in evaluation_results.get("results", {}).items():
            execution_time = result.get("execution_time", 0)
            if execution_time > 3600:  # 超过1小时
                changes[task_id] = "Suggest further decomposition (execution > 1h)"
        
        return changes
    
    def _improve_prompt(self, workflow: Dict[str, Any], evaluation_results: Dict[str, Any]) -> Dict[str, Any]:
        """改进提示词"""
        changes = {}
        
        # 对于质量较低的任务，添加提示词改进标记
        for task_id, result in evaluation_results.get("results", {}).items():
            quality = result.get("quality", {})
            if quality.get("score", 0) < 3.0:
                if task_id in workflow.get("nodes", {}):
                    node = workflow["nodes"][task_id]
                    node["needs_prompt_improvement"] = True
                    changes[task_id] = "Marked for prompt improvement"
        
        return changes
    
    def _estimate_improvement(self, changes: Dict[str, Any]) -> float:
        """估计改进幅度"""
        # 简化版本：根据修改数量估计
        return min(1.0, len(changes) * 0.2)
    
    def get_optimization_summary(self) -> Dict[str, Any]:
        """获取优化摘要"""
        if not self.optimization_history:
            return {}
        
        total_iterations = max(r.iteration for r in self.optimization_history)
        strategy_usage = {}
        total_improvement = 0.0
        
        for record in self.optimization_history:
            strategy_usage[record.strategy] = strategy_usage.get(record.strategy, 0) + 1
            total_improvement += record.improvement
        
        return {
            "total_iterations": total_iterations,
            "total_optimizations": len(self.optimization_history),
            "strategy_usage": strategy_usage,
            "average_improvement": total_improvement / len(self.optimization_history) if self.optimization_history else 0,
            "total_improvement": total_improvement
        }
    
    def save_history(self, filepath: str):
        """保存优化历史"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                "history": [
                    {
                        "iteration": r.iteration,
                        "strategy": r.strategy,
                        "changes": r.changes,
                        "improvement": r.improvement,
                        "timestamp": r.timestamp.isoformat()
                    }
                    for r in self.optimization_history
                ],
                "summary": self.get_optimization_summary()
            }, f, ensure_ascii=False, indent=2)


# 与Evaluator集成的优化器
class FeedbackDrivenOptimizer(Optimizer):
    """反馈驱动的优化器"""
    
    def __init__(self, evaluator, config: Optional[Dict] = None):
        super().__init__(config)
        self.evaluator = evaluator
    
    def optimize_with_feedback(self, workflow: Dict[str, Any], 
                               task_outputs: Dict[str, str]) -> Dict[str, Any]:
        """
        基于反馈优化
        
        Args:
            workflow: 工作流
            task_outputs: 任务输出
            
        Returns:
            优化后的工作流
        """
        # 评估所有任务输出
        evaluation_results = {"results": {}}
        
        for task_id, output in task_outputs.items():
            metrics = self.evaluator.evaluate_text_quality(output)
            evaluation_results["results"][task_id] = {
                "status": "completed",
                "quality": {
                    "score": metrics.overall_score,
                    "level": metrics.quality_level.name
                }
            }
        
        # 调用优化
        return self.optimize(workflow, evaluation_results)


if __name__ == "__main__":
    # 测试
    optimizer = Optimizer(config={"max_iterations": 3})
    
    # 模拟工作流
    workflow = {
        "id": "test_workflow",
        "nodes": {
            "task_1": {"status": "completed", "retry_count": 0, "timeout": 1800},
            "task_2": {"status": "failed", "retry_count": 0, "timeout": 1800},
            "task_3": {"status": "timeout", "retry_count": 0, "timeout": 1800}
        },
        "max_parallel": 10
    }
    
    # 模拟评估结果
    evaluation_results = {
        "results": {
            "task_1": {"status": "completed", "quality": {"score": 4.5}},
            "task_2": {"status": "failed"},
            "task_3": {"status": "timeout"}
        }
    }
    
    # 优化
    optimized = optimizer.optimize(workflow, evaluation_results, iteration=1)
    
    print("Optimization applied!")
    print(f"History: {len(optimizer.optimization_history)} records")
    print(f"Summary: {optimizer.get_optimization_summary()}")
