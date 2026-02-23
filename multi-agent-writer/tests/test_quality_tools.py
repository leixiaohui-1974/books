"""
测试 QualityTools — 术语检查 / 一致性检查 / 参考文献检查 / 结构检查
"""

import pytest
from hydroscribe.tools.quality_tools import (
    CheckGlossaryTool,
    CheckConsistencyTool,
    CheckReferenceTool,
    CheckStructureTool,
)


class TestCheckGlossaryTool:
    def setup_method(self):
        self.tool = CheckGlossaryTool()

    def test_clean_content(self):
        content = "水系统控制论(CHS)提出了安全包络的概念。"
        result = self.tool.execute(content)
        assert result["passed"] is True
        assert result["score"] == 10
        assert result["total_issues"] == 0

    def test_forbidden_alias_detected(self):
        content = "水控制学是一个新兴学科方向，它提出了安全域的概念。"
        result = self.tool.execute(content)
        assert result["passed"] is False
        assert result["total_issues"] >= 2
        aliases = [a["alias"] for a in result["forbidden_aliases"]]
        assert "水控制学" in aliases
        assert "安全域" in aliases

    def test_multiple_occurrences(self):
        content = "多代理系统是核心。多代理系统很重要。多代理系统不可或缺。"
        result = self.tool.execute(content)
        assert result["forbidden_aliases"][0]["count"] == 3

    def test_correct_alternatives(self):
        content = "多智能体系统是核心。安全包络是重要概念。"
        result = self.tool.execute(content)
        assert result["passed"] is True


class TestCheckConsistencyTool:
    def setup_method(self):
        self.tool = CheckConsistencyTool()

    def test_clean_content(self):
        content = "水系统控制论提出了八原理框架。"
        result = self.tool.execute(content)
        assert result["passed"] is True

    def test_incomplete_principles(self):
        content = "八原理包括：传递函数化、可控可观性、分层分布式。"
        result = self.tool.execute(content)
        assert len(result["issues"]) > 0
        assert result["issues"][0]["type"] == "incomplete_principles"

    def test_project_confusion_jiaodong(self):
        content = "胶东调水水电站的发电能力很强。"
        result = self.tool.execute(content)
        assert result["passed"] is False
        assert any(i["type"] == "project_confusion" for i in result["issues"])

    def test_project_confusion_shaoping(self):
        content = "沙坪调水工程是长距离明渠。"
        result = self.tool.execute(content)
        assert result["passed"] is False

    def test_correct_descriptions(self):
        content = "胶东调水是明渠SCADA+HDC控制的典范。沙坪水电站是大渡河梯级的重要枢纽。"
        result = self.tool.execute(content)
        assert result["passed"] is True


class TestCheckReferenceTool:
    def setup_method(self):
        self.tool = CheckReferenceTool()

    def test_no_references(self):
        content = "这是没有参考文献的文章。"
        result = self.tool.execute(content)
        assert result["total_references"] == 0
        assert result["score"] < 10

    def test_with_references(self):
        content = """
正文内容。

## 参考文献

[1] Wiener N. Cybernetics. MIT Press, 1948.
[2] Lei X, et al. CHS theory. Water Resources, 2025a.
[3] 钱学森. 工程控制论. 科学出版社, 1954.
[4] Van Overloop PJ. Model Predictive Control. PhD thesis, 2006.
[5] Litrico X. Modeling and Control. Springer, 2023.
[6] Zhang Y. Deep Learning for Water. Nature Water, 2024.
[7] Wang H. Smart Water Networks. JWRPM, 2024.
[8] Li M. Digital Twin. Advances in Water Resources, 2023.
[9] Chen X. PINN for Hydraulics. JHE, 2025.
[10] ASCE. MOP 131. ASCE, 2014.
"""
        result = self.tool.execute(content, "BK")
        assert result["total_references"] == 10
        assert result["must_cite_missing"] == []  # Wiener, 钱学森, Lei 2025 都有

    def test_missing_must_cite(self):
        content = """
## 参考文献

[1] Zhang Y. Some paper. 2024.
[2] Li M. Another paper. 2023.
"""
        result = self.tool.execute(content)
        assert len(result["must_cite_missing"]) > 0


class TestCheckStructureTool:
    def setup_method(self):
        self.tool = CheckStructureTool()

    def test_complete_structure(self):
        content = """
## 学习目标

1. 理解MPC基本原理
2. 掌握约束处理方法
3. 能够设计简单的MPC控制器

## 7.1 引言

**模型预测控制**(MPC)是一种先进的控制方法。

[图 7-1: MPC原理示意图]

[表 7-1: MPC参数对比]

【例7-1】某明渠渠段...

## 本章小结

本章介绍了MPC的基本理论。

## 习题

1. 基础题...
2. 应用题...
3. 思考题...

## 拓展阅读

- Rawlings (2017)
- Borrelli (2017)
"""
        result = self.tool.execute(content, "textbook")
        assert result["passed"] is True
        assert result["checks"]["has_learning_objectives"] is True
        assert result["checks"]["has_summary"] is True
        assert result["checks"]["has_exercises"] is True
        assert result["checks"]["has_further_reading"] is True

    def test_missing_structure(self):
        content = "这是一段没有结构的内容，缺少学习目标和小结。"
        result = self.tool.execute(content, "textbook")
        assert result["passed"] is False
        assert result["checks"]["has_learning_objectives"] is False

    def test_t1_style(self):
        content = """
2023年夏季，华北某调水工程面临了严峻的运行挑战...

| 对比项 | 传统 | CHS |
|--------|------|-----|
| 调度方式 | 人工 | 自主 |
"""
        result = self.tool.execute(content, "T1")
        assert result["checks"]["has_opening_case"] is True
        assert result["checks"]["has_comparison_table"] is True
