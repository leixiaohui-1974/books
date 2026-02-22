#!/usr/bin/env python3
"""
OpenClaw Agent Core - Task Decomposer
任务分解器 - 将复杂任务分解为可执行子任务
"""

import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

@dataclass
class SubTask:
    """子任务"""
    id: str
    name: str
    description: str
    estimated_time: int  # 估计执行时间（分钟）
    dependencies: List[str] = field(default_factory=list)
    required_skills: List[str] = field(default_factory=list)
    output_format: str = "text"  # text, json, markdown, etc.


class TaskDecomposer:
    """任务分解器"""
    
    # 任务类型模板
    TASK_TEMPLATES = {
        "report_generation": {
            "name": "报告生成",
            "subtasks": [
                {"name": "文献调研", "time": 30, "skills": ["search"]},
                {"name": "大纲设计", "time": 20, "skills": ["writing"]},
                {"name": "内容撰写", "time": 120, "skills": ["writing"]},
                {"name": "质量检查", "time": 30, "skills": ["review"]},
                {"name": "格式整理", "time": 20, "skills": ["formatting"]}
            ]
        },
        "code_development": {
            "name": "代码开发",
            "subtasks": [
                {"name": "需求分析", "time": 30, "skills": ["analysis"]},
                {"name": "架构设计", "time": 40, "skills": ["design"]},
                {"name": "编码实现", "time": 120, "skills": ["coding"]},
                {"name": "单元测试", "time": 60, "skills": ["testing"]},
                {"name": "代码审查", "time": 30, "skills": ["review"]}
            ]
        },
        "data_analysis": {
            "name": "数据分析",
            "subtasks": [
                {"name": "数据收集", "time": 40, "skills": ["collection"]},
                {"name": "数据清洗", "time": 60, "skills": ["cleaning"]},
                {"name": "探索性分析", "time": 60, "skills": ["analysis"]},
                {"name": "建模分析", "time": 90, "skills": ["modeling"]},
                {"name": "结果可视化", "time": 40, "skills": ["visualization"]}
            ]
        },
        "research_survey": {
            "name": "研究综述",
            "subtasks": [
                {"name": "文献检索", "time": 60, "skills": ["search"]},
                {"name": "文献筛选", "time": 40, "skills": ["review"]},
                {"name": "内容提取", "time": 90, "skills": ["analysis"]},
                {"name": "综述撰写", "time": 120, "skills": ["writing"]},
                {"name": "引用整理", "time": 30, "skills": ["formatting"]}
            ]
        }
    }
    
    def __init__(self):
        self.decomposition_history = []
    
    def analyze_task_type(self, task_description: str) -> str:
        """
        分析任务类型
        
        Args:
            task_description: 任务描述
            
        Returns:
            任务类型标识
        """
        task_lower = task_description.lower()
        
        # 关键词匹配
        if any(kw in task_lower for kw in ["报告", "report", "论文", "paper", "文档", "document"]):
            if "万" in task_description or "万字" in task_description:
                return "large_report_generation"
            return "report_generation"
        
        if any(kw in task_lower for kw in ["代码", "code", "程序", "program", "开发", "develop"]):
            return "code_development"
        
        if any(kw in task_lower for kw in ["数据", "data", "分析", "analysis", "统计", "statistics"]):
            return "data_analysis"
        
        if any(kw in task_lower for kw in ["综述", "survey", "回顾", "review", "文献", "literature"]):
            return "research_survey"
        
        return "general_task"
    
    def decompose(self, task_description: str, task_id: Optional[str] = None) -> List[SubTask]:
        """
        分解任务为子任务
        
        Args:
            task_description: 任务描述
            task_id: 任务ID
            
        Returns:
            子任务列表
        """
        task_type = self.analyze_task_type(task_description)
        
        # 特殊处理：大型报告生成
        if task_type == "large_report_generation":
            return self._decompose_large_report(task_description, task_id)
        
        # 使用模板
        template = self.TASK_TEMPLATES.get(task_type, self.TASK_TEMPLATES["report_generation"])
        
        subtasks = []
        for i, subtask_template in enumerate(template["subtasks"]):
            subtask = SubTask(
                id=f"{task_id}_subtask_{i+1}" if task_id else f"subtask_{i+1}",
                name=subtask_template["name"],
                description=f"{subtask_template['name']} for: {task_description[:50]}...",
                estimated_time=subtask_template["time"],
                dependencies=[f"{task_id}_subtask_{i}"] if i > 0 else [],
                required_skills=subtask_template["skills"]
            )
            subtasks.append(subtask)
        
        # 记录分解历史
        self.decomposition_history.append({
            "task": task_description,
            "type": task_type,
            "subtasks": len(subtasks)
        })
        
        return subtasks
    
    def _decompose_large_report(self, task_description: str, task_id: Optional[str]) -> List[SubTask]:
        """
        分解大型报告生成任务
        
        例如：25万字报告 → 50个5000字模块
        """
        # 提取字数要求
        word_match = re.search(r'(\d+)万', task_description)
        if word_match:
            target_words = int(word_match.group(1)) * 10000
        else:
            target_words = 250000  # 默认25万字
        
        # 计算模块数（每模块5000字）
        module_size = 5000
        num_modules = target_words // module_size
        
        subtasks = []
        
        # 1. 规划阶段
        subtasks.append(SubTask(
            id=f"{task_id}_plan" if task_id else "plan",
            name="报告规划",
            description=f"设计{target_words}字报告的整体架构和章节安排",
            estimated_time=30,
            dependencies=[],
            required_skills=["planning", "writing"]
        ))
        
        # 2. 模块撰写阶段（并行）
        for i in range(num_modules):
            subtasks.append(SubTask(
                id=f"{task_id}_module_{i+1}" if task_id else f"module_{i+1}",
                name=f"模块{i+1}撰写",
                description=f"撰写第{i+1}个模块（{module_size}字）",
                estimated_time=60,
                dependencies=[f"{task_id}_plan"] if task_id else ["plan"],
                required_skills=["writing", "research"]
            ))
        
        # 3. 整合阶段
        module_ids = [f"{task_id}_module_{i+1}" if task_id else f"module_{i+1}" 
                      for i in range(num_modules)]
        subtasks.append(SubTask(
            id=f"{task_id}_integrate" if task_id else "integrate",
            name="报告整合",
            description=f"整合所有{num_modules}个模块为完整报告",
            estimated_time=30,
            dependencies=module_ids,
            required_skills=["editing", "formatting"]
        ))
        
        # 4. 质量检查阶段
        subtasks.append(SubTask(
            id=f"{task_id}_review" if task_id else "review",
            name="质量检查",
            description="检查报告质量、引用准确性、格式规范性",
            estimated_time=60,
            dependencies=[f"{task_id}_integrate"] if task_id else ["integrate"],
            required_skills=["review", "verification"]
        ))
        
        return subtasks
    
    def estimate_resources(self, subtasks: List[SubTask]) -> Dict[str, Any]:
        """
        估计资源需求
        
        Args:
            subtasks: 子任务列表
            
        Returns:
            资源估计
        """
        total_time = sum(st.estimated_time for st in subtasks)
        max_parallel = len([st for st in subtasks if not st.dependencies])
        
        skill_counts = {}
        for st in subtasks:
            for skill in st.required_skills:
                skill_counts[skill] = skill_counts.get(skill, 0) + 1
        
        return {
            "total_tasks": len(subtasks),
            "total_time_minutes": total_time,
            "estimated_wall_time": total_time / max(1, max_parallel),
            "max_parallel": max_parallel,
            "skill_requirements": skill_counts
        }


if __name__ == "__main__":
    # 测试
    decomposer = TaskDecomposer()
    
    # 测试大型报告分解
    task = "生成25万字水系统控制论学术报告"
    subtasks = decomposer.decompose(task, "report_001")
    
    print(f"Task: {task}")
    print(f"Decomposed into {len(subtasks)} subtasks:")
    for st in subtasks[:5]:  # 只显示前5个
        print(f"  - {st.name} ({st.estimated_time}min)")
    if len(subtasks) > 5:
        print(f"  ... and {len(subtasks)-5} more")
    
    resources = decomposer.estimate_resources(subtasks)
    print(f"\nResource estimation:")
    print(f"  Total time: {resources['total_time_minutes']} minutes")
    print(f"  Wall time: {resources['estimated_wall_time']:.0f} minutes")
    print(f"  Max parallel: {resources['max_parallel']}")
