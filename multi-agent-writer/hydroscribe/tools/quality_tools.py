"""
QualityTools — 质量检查工具集

将 Utility Agent 的检查能力封装为可被任意 Agent 调用的 Tool。
"""

import re
from typing import Any, Dict, List


class CheckGlossaryTool:
    """术语一致性检查工具（同步版，不依赖异步）"""

    name: str = "check_glossary"
    description: str = "检查内容中的术语是否符合CHS术语规范。返回禁止别名、缺失定义、符号问题。"

    # 禁止别名（CLAUDE.md §5.1）
    FORBIDDEN = {
        "水控制学": "水系统控制论", "水系统论": "水系统控制论", "水网控制学": "水系统控制论",
        "水网自动化等级": "水网自主等级", "水利自主等级": "水网自主等级",
        "操作设计域": "运行设计域", "运行设计范围": "运行设计域",
        "安全域": "安全包络", "物理引擎": "物理AI引擎", "机理模型引擎": "物理AI引擎",
        "知识引擎": "认知AI引擎", "决策引擎": "认知AI引擎",
        "分级控制": "分层分布式控制", "集散控制": "分层分布式控制",
        "多代理系统": "多智能体系统", "闭环测试": "在环测试",
        "水利操作系统": "水网操作系统", "水务OS": "水网操作系统",
        "翰铎": "瀚铎水网大模型", "瀚铎大模型": "瀚铎水网大模型",
        "预测控制": "模型预测控制", "传递矩阵": "传递函数", "简化模型": "降阶模型",
        "SCADA/MAS混合": "SCADA+MAS融合架构",
    }

    def execute(self, content: str) -> Dict[str, Any]:
        issues = []
        for alias, correct in self.FORBIDDEN.items():
            count = content.count(alias)
            if count > 0:
                issues.append({"alias": alias, "correct": correct, "count": count})

        score = max(0, 10 - len(issues) * 1.5)
        return {
            "passed": len(issues) == 0,
            "score": round(score, 1),
            "forbidden_aliases": issues,
            "total_issues": len(issues),
        }


class CheckConsistencyTool:
    """跨书一致性检查工具"""

    name: str = "check_consistency"
    description: str = "检查内容与CHS体系关键概念的一致性（八原理、WNAL、工程参数等）"

    EIGHT_PRINCIPLES = [
        "传递函数化", "可控可观性", "分层分布式", "安全包络",
        "在环验证", "认知增强", "人机共融", "自主演进",
    ]

    WNAL_LEVELS = ["L0", "L1", "L2", "L3", "L4", "L5"]

    def execute(self, content: str, book_id: str = "") -> Dict[str, Any]:
        issues = []

        # 检查八原理是否完整（如果提到了其中一个）
        mentioned = [p for p in self.EIGHT_PRINCIPLES if p in content]
        if 1 <= len(mentioned) < 8 and "八原理" in content:
            missing = [p for p in self.EIGHT_PRINCIPLES if p not in content]
            issues.append({
                "type": "incomplete_principles",
                "message": f"提到了'八原理'但只列出了{len(mentioned)}/8个: 缺少 {', '.join(missing)}",
                "severity": "yellow",
            })

        # 检查WNAL是否完整（如果提到了）
        wnal_mentioned = [l for l in self.WNAL_LEVELS if l in content]
        if 1 <= len(wnal_mentioned) < 6 and "WNAL" in content:
            missing = [l for l in self.WNAL_LEVELS if l not in content]
            issues.append({
                "type": "incomplete_wnal",
                "message": f"提到了WNAL但只列出了{len(wnal_mentioned)}/6级: 缺少 {', '.join(missing)}",
                "severity": "yellow",
            })

        # 检查工程混淆
        if "胶东" in content and "水电站" in content:
            # 胶东是调水工程，不是水电站
            context = content[max(0, content.index("胶东") - 50):content.index("胶东") + 100]
            if "水电站" in context or "发电" in context:
                issues.append({
                    "type": "project_confusion",
                    "message": "胶东调水是明渠调水工程(非水电站)，请检查是否混淆了胶东调水和沙坪水电站",
                    "severity": "red",
                })

        if "沙坪" in content and "调水" in content:
            context = content[max(0, content.index("沙坪") - 50):content.index("沙坪") + 100]
            if "调水" in context and "梯级" not in context:
                issues.append({
                    "type": "project_confusion",
                    "message": "沙坪是大渡河水电站(非调水工程)，请检查是否混淆",
                    "severity": "red",
                })

        red = [i for i in issues if i["severity"] == "red"]
        yellow = [i for i in issues if i["severity"] == "yellow"]
        score = max(0, 10 - len(red) * 3 - len(yellow) * 1)

        return {
            "passed": len(red) == 0,
            "score": round(score, 1),
            "issues": issues,
            "red_count": len(red),
            "yellow_count": len(yellow),
        }


class CheckReferenceTool:
    """参考文献检查工具"""

    name: str = "check_reference"
    description: str = "检查参考文献的数量、自引率、近5年占比、必引文献覆盖"

    MUST_CITE = ["Wiener", "钱学森", "Lei 2025"]

    def execute(self, content: str, skill_type: str = "BK") -> Dict[str, Any]:
        # 提取参考文献
        ref_section = re.search(
            r'(?:参考文献|References|Bibliography)\s*\n(.*?)(?:\n#|\Z)',
            content, re.DOTALL | re.IGNORECASE
        )
        refs = []
        if ref_section:
            for line in ref_section.group(1).strip().split("\n"):
                line = line.strip()
                if line and (re.match(r'^\[?\d+\]?', line) or re.match(r'^-\s', line)):
                    refs.append(line)

        total = len(refs)

        # 自引
        self_count = sum(1 for r in refs if any(m in r for m in ["Lei", "雷晓辉"]))
        self_rate = self_count / max(total, 1)

        # 近5年
        recent = sum(1 for r in refs if re.search(r'202[1-6]', r))
        recent_rate = recent / max(total, 1)

        # 必引
        missing = []
        for must in self.MUST_CITE:
            if not any(must in r for r in refs) and must not in content:
                missing.append(must)

        # 最低数量要求
        min_refs = {"BK": 10, "SCI": 30, "CN": 20, "PAT": 5, "RPT": 10}.get(skill_type, 10)

        score = 10.0
        if total < min_refs:
            score -= 2.0
        if recent_rate < 0.30:
            score -= 1.5
        score -= len(missing) * 0.5

        return {
            "passed": score >= 7.0,
            "score": round(max(0, score), 1),
            "total_references": total,
            "self_citation_rate": round(self_rate, 3),
            "recent_rate": round(recent_rate, 3),
            "must_cite_missing": missing,
            "min_required": min_refs,
        }


class CheckStructureTool:
    """章节结构完整性检查工具（CLAUDE.md §6.1）"""

    name: str = "check_structure"
    description: str = "检查教材章节的结构完整性：学习目标/小结/习题/拓展阅读/概念密度/图表"

    def execute(self, content: str, book_type: str = "textbook") -> Dict[str, Any]:
        checks = {}

        if book_type in ("textbook", "BK"):
            # 教材质量清单
            checks["has_learning_objectives"] = bool(re.search(r'学习目标|Learning Objectives', content, re.I))
            checks["has_summary"] = bool(re.search(r'本章小结|Chapter Summary|小结', content, re.I))
            checks["has_exercises"] = bool(re.search(r'习题|Exercises|Problems', content, re.I))
            checks["has_further_reading"] = bool(re.search(r'拓展阅读|Further Reading|References', content, re.I))

            # 概念密度
            bold_terms = re.findall(r'\*\*([^*]{2,20})\*\*', content)
            checks["concept_count"] = len(set(bold_terms))
            checks["concept_density_ok"] = checks["concept_count"] <= 10

            # 图表
            figures = len(re.findall(r'\[图\s*\d|Figure\s*\d', content, re.I))
            tables = len(re.findall(r'\[表\s*\d|Table\s*\d', content, re.I))
            checks["figures"] = figures
            checks["tables"] = tables
            checks["has_visuals"] = (figures + tables) >= 2

            # 例题
            examples = len(re.findall(r'【例\d|\[例\d', content))
            checks["examples"] = examples

            # 公式
            equations = len(re.findall(r'\$\$[^$]+\$\$', content))
            checks["equations"] = equations

        elif book_type == "T1":
            # 先导版特殊标准（无需习题）
            checks["has_opening_case"] = bool(re.search(r'^\d{4}年|某.*工程|案例', content[:2000]))
            checks["minimal_math"] = len(re.findall(r'\$\$[^$]+\$\$', content)) <= len(content) * 0.05
            checks["has_comparison_table"] = bool(re.search(r'\|.*\|.*\|', content))

        # 计算通过的检查项数
        bool_checks = {k: v for k, v in checks.items() if isinstance(v, bool)}
        passed_count = sum(1 for v in bool_checks.values() if v)
        total_checks = len(bool_checks)
        score = (passed_count / max(total_checks, 1)) * 10

        return {
            "passed": score >= 7.0,
            "score": round(score, 1),
            "checks": checks,
            "passed_count": passed_count,
            "total_checks": total_checks,
        }
