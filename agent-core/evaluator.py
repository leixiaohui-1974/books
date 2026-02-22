#!/usr/bin/env python3
"""
OpenClaw Agent Core - Evaluator
评估器 - 评估任务输出质量
"""

import re
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum

class QualityLevel(Enum):
    """质量等级"""
    EXCELLENT = 5  # 优秀
    GOOD = 4       # 良好
    ACCEPTABLE = 3 # 可接受
    POOR = 2       # 较差
    UNACCEPTABLE = 1 # 不可接受

@dataclass
class EvaluationMetrics:
    """评估指标"""
    accuracy: float = 0.0      # 准确性 (0-1)
    completeness: float = 0.0  # 完整性 (0-1)
    consistency: float = 0.0   # 一致性 (0-1)
    readability: float = 0.0   # 可读性 (0-1)
    overall_score: float = 0.0 # 综合得分 (0-5)
    quality_level: QualityLevel = QualityLevel.UNACCEPTABLE
    feedback: List[str] = None
    
    def __post_init__(self):
        if self.feedback is None:
            self.feedback = []


class Evaluator:
    """评估器"""
    
    # 质量阈值
    THRESHOLDS = {
        "excellent": 4.5,
        "good": 3.5,
        "acceptable": 2.5,
        "poor": 1.5
    }
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.evaluation_history = []
    
    def evaluate_text_quality(self, text: str, expected_words: Optional[int] = None) -> EvaluationMetrics:
        """
        评估文本质量
        
        Args:
            text: 待评估文本
            expected_words: 预期字数
            
        Returns:
            评估指标
        """
        metrics = EvaluationMetrics()
        feedback = []
        
        # 1. 完整性检查
        word_count = len(text)
        if expected_words:
            completeness = min(1.0, word_count / expected_words)
            metrics.completeness = completeness
            if completeness < 0.8:
                feedback.append(f"字数不足: {word_count}/{expected_words} ({completeness*100:.1f}%)")
        else:
            metrics.completeness = 1.0 if word_count > 100 else word_count / 100
        
        # 2. 结构完整性检查
        has_structure = self._check_structure(text)
        if not has_structure:
            feedback.append("缺少必要的结构（标题、段落等）")
            metrics.completeness *= 0.8
        
        # 3. 可读性检查
        metrics.readability = self._evaluate_readability(text)
        if metrics.readability < 0.6:
            feedback.append("可读性较差，建议改进语言表达")
        
        # 4. 一致性检查
        metrics.consistency = self._evaluate_consistency(text)
        if metrics.consistency < 0.7:
            feedback.append("内容一致性存在问题")
        
        # 5. 准确性检查（简化版本）
        metrics.accuracy = self._evaluate_accuracy(text)
        
        # 计算综合得分
        metrics.overall_score = (
            metrics.accuracy * 1.2 +
            metrics.completeness * 1.2 +
            metrics.consistency * 1.0 +
            metrics.readability * 0.6
        )
        
        # 确定质量等级
        metrics.quality_level = self._determine_quality_level(metrics.overall_score)
        metrics.feedback = feedback
        
        return metrics
    
    def evaluate_code_quality(self, code: str, language: str = "python") -> EvaluationMetrics:
        """
        评估代码质量
        
        Args:
            code: 代码字符串
            language: 编程语言
            
        Returns:
            评估指标
        """
        metrics = EvaluationMetrics()
        feedback = []
        
        # 1. 语法检查（简化）
        if language == "python":
            try:
                compile(code, '<string>', 'exec')
                metrics.accuracy = 1.0
            except SyntaxError as e:
                metrics.accuracy = 0.0
                feedback.append(f"语法错误: {e}")
        
        # 2. 代码结构检查
        has_functions = 'def ' in code
        has_comments = '#' in code or '"""' in code
        
        if not has_functions:
            feedback.append("建议将代码组织为函数")
        if not has_comments:
            feedback.append("建议添加注释说明")
        
        metrics.completeness = 0.8 if has_functions else 0.5
        metrics.readability = 0.7 if has_comments else 0.4
        
        # 3. 一致性检查
        metrics.consistency = self._check_code_consistency(code, language)
        
        # 计算综合得分
        metrics.overall_score = (
            metrics.accuracy * 1.5 +
            metrics.completeness * 1.0 +
            metrics.consistency * 0.8 +
            metrics.readability * 0.7
        ) / 4 * 5  # 归一化到0-5
        
        metrics.quality_level = self._determine_quality_level(metrics.overall_score)
        metrics.feedback = feedback
        
        return metrics
    
    def evaluate_references(self, text: str) -> Dict[str, Any]:
        """
        评估参考文献质量
        
        Args:
            text: 包含参考文献的文本
            
        Returns:
            参考文献评估结果
        """
        # 提取引用标记
        citations = re.findall(r'\[(\d+)\]', text)
        unique_citations = set(citations)
        
        # 检查是否有待核实标记
        unverified = len(re.findall(r'\[待核实\]', text))
        
        # 统计
        total_refs = len(unique_citations)
        
        return {
            "total_citations": len(citations),
            "unique_references": total_refs,
            "unverified_count": unverified,
            "citation_density": len(citations) / len(text.split()) * 1000 if text else 0,
            "has_unverified": unverified > 0,
            "quality": "good" if unverified == 0 else "needs_verification"
        }
    
    def _check_structure(self, text: str) -> bool:
        """检查文本结构"""
        has_headers = bool(re.search(r'^#{1,6} ', text, re.MULTILINE))
        has_paragraphs = len(text.split('\n\n')) > 2
        return has_headers or has_paragraphs
    
    def _evaluate_readability(self, text: str) -> float:
        """评估可读性"""
        sentences = re.split(r'[。！？.!?]', text)
        if not sentences:
            return 0.0
        
        # 平均句子长度
        avg_sentence_length = sum(len(s) for s in sentences) / len(sentences)
        
        # 句子长度适中（20-50字）为最佳
        if 20 <= avg_sentence_length <= 50:
            return 0.8
        elif avg_sentence_length < 100:
            return 0.6
        else:
            return 0.4
    
    def _evaluate_consistency(self, text: str) -> float:
        """评估一致性"""
        # 检查术语一致性（简化）
        # 实际应该检查术语表
        return 0.8  # 默认较高
    
    def _evaluate_accuracy(self, text: str) -> float:
        """评估准确性"""
        # 检查是否有明显的错误标记
        if '[ERROR]' in text or '[待核实]' in text:
            return 0.6
        return 0.9  # 默认较高
    
    def _check_code_consistency(self, code: str, language: str) -> float:
        """检查代码一致性"""
        # 检查命名风格一致性
        snake_case = len(re.findall(r'\b[a-z]+_[a-z_]+\b', code))
        camelCase = len(re.findall(r'\b[a-z]+[A-Z][a-zA-Z]*\b', code))
        
        if snake_case > 0 and camelCase > 0:
            return 0.6  # 混合命名风格
        return 0.9
    
    def _determine_quality_level(self, score: float) -> QualityLevel:
        """确定质量等级"""
        if score >= self.THRESHOLDS["excellent"]:
            return QualityLevel.EXCELLENT
        elif score >= self.THRESHOLDS["good"]:
            return QualityLevel.GOOD
        elif score >= self.THRESHOLDS["acceptable"]:
            return QualityLevel.ACCEPTABLE
        elif score >= self.THRESHOLDS["poor"]:
            return QualityLevel.POOR
        else:
            return QualityLevel.UNACCEPTABLE
    
    def should_retry(self, metrics: EvaluationMetrics, max_retries: int = 3) -> bool:
        """判断是否应重试"""
        return (
            metrics.quality_level in [QualityLevel.POOR, QualityLevel.UNACCEPTABLE]
            and len(self.evaluation_history) < max_retries
        )
    
    def record_evaluation(self, task_id: str, metrics: EvaluationMetrics):
        """记录评估结果"""
        self.evaluation_history.append({
            "task_id": task_id,
            "metrics": {
                "accuracy": metrics.accuracy,
                "completeness": metrics.completeness,
                "consistency": metrics.consistency,
                "readability": metrics.readability,
                "overall_score": metrics.overall_score,
                "quality_level": metrics.quality_level.name
            },
            "feedback": metrics.feedback
        })


if __name__ == "__main__":
    # 测试
    evaluator = Evaluator()
    
    # 测试文本评估
    test_text = """
# 测试标题

这是一段测试文本。它包含了一些基本信息。

## 子标题

更多的内容在这里。
"""
    
    metrics = evaluator.evaluate_text_quality(test_text, expected_words=100)
    print(f"Text Quality: {metrics.quality_level.name}")
    print(f"Overall Score: {metrics.overall_score:.2f}")
    print(f"Feedback: {metrics.feedback}")
