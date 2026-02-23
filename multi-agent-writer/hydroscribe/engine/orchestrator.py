"""
Orchestrator — 多智能体编排器（系统大脑）
参考 OpenManus PlanningFlow，实现 Plan → Execute → Reflect 三阶段循环

协同模式：
- specialist (专家分工): 不同 OpenManus 实例按文体特化，Orchestrator 按技能路由
- master_slave (主从): Orchestrator 分解任务为子任务，分配给多个并行 Writer

集成层：
- LLM Provider: 多提供商抽象 (百炼/OpenAI/Anthropic/本地)
- Config Loader: TOML 配置 + 环境变量覆盖
- OpenClaw Skill: 可被 OpenClaw 网关作为 Skill 调度
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from hydroscribe.schema import (
    AggregatedReview, BookProgress, ChapterProgress, ChapterSpec,
    Event, EventType, ReviewScore, ReviewerRole,
    SKILL_REVIEWERS, SKILL_THRESHOLDS,
    SkillType, WritingTask
)
from hydroscribe.engine.event_bus import EventBus
from hydroscribe.engine.config_loader import (
    HydroScribeConfig, get_config, LLMRoleConfig
)
from hydroscribe.engine.llm_provider import (
    LLMManager, LLMConfig, LLMProvider, LLMUsage, create_llm_client
)
from hydroscribe.engine.llm_bridge import (
    LLMBridge, create_writer_bridge, create_reviewer_bridge, create_utility_bridge
)
from hydroscribe.agents.base_writer import BaseWriterAgent
from hydroscribe.agents.base_reviewer import BaseReviewerAgent

logger = logging.getLogger("hydroscribe.orchestrator")

# 每种文体的评审角色权重（来自 skill 文件定义）
REVIEWER_WEIGHTS: Dict[SkillType, Dict[ReviewerRole, float]] = {
    SkillType.BK: {
        ReviewerRole.INSTRUCTOR: 0.25,
        ReviewerRole.EXPERT: 0.25,
        ReviewerRole.ENGINEER: 0.25,
        ReviewerRole.INTERNATIONAL: 0.25,
    },
    SkillType.SCI: {
        ReviewerRole.REVIEWER_A: 0.34,
        ReviewerRole.REVIEWER_B: 0.33,
        ReviewerRole.REVIEWER_C: 0.33,
    },
    SkillType.CN: {
        ReviewerRole.CN_REVIEWER_A: 0.40,
        ReviewerRole.CN_REVIEWER_B: 0.30,
        ReviewerRole.CN_REVIEWER_C: 0.30,
    },
    SkillType.PAT: {
        ReviewerRole.PATENT_EXAMINER: 0.40,
        ReviewerRole.PATENT_AGENT: 0.30,
        ReviewerRole.PATENT_TECH: 0.30,
    },
    SkillType.RPT: {
        ReviewerRole.TECH_REVIEWER: 0.60,
        ReviewerRole.MGMT_REVIEWER: 0.40,
    },
    SkillType.STD_CN: {
        ReviewerRole.STD_CN_STANDARD: 0.40,
        ReviewerRole.STD_CN_TECH: 0.35,
        ReviewerRole.STD_CN_IMPL: 0.25,
    },
    SkillType.STD_INT: {
        ReviewerRole.STD_INT_ISO: 0.40,
        ReviewerRole.STD_INT_HYDRO: 0.35,
        ReviewerRole.STD_INT_INDUSTRY: 0.25,
    },
    SkillType.WX: {
        ReviewerRole.WX_READER: 0.40,
        ReviewerRole.WX_EDITOR: 0.30,
        ReviewerRole.WX_DOMAIN: 0.30,
    },
    SkillType.PPT: {
        ReviewerRole.PPT_AUDIENCE: 0.35,
        ReviewerRole.PPT_DESIGN: 0.30,
        ReviewerRole.PPT_CONTENT: 0.35,
    },
}


class Orchestrator:
    """
    多智能体编排器 — 系统大脑

    职责：
    1. Plan  — 解析用户指令，读取书目规格，生成写作 DAG
    2. Execute — 按 DAG 调度 Writer/Reviewer/Utility Agent
    3. Reflect — 汇总评审结果（加权），门控决策，Utility检查，更新进度

    协同模式（由 config.orchestrator.coordination_mode 控制）：
    - specialist: 按文体路由到专用 Agent（默认，低并发场景）
    - master_slave: 分解大任务为子任务，多 Writer 并行执行
    """

    def __init__(
        self,
        books_root: str = "/home/user/books",
        gate_mode: str = "auto",
        config: Optional[HydroScribeConfig] = None,
    ):
        # 加载配置
        self.config = config or get_config()
        self.books_root = books_root or self.config.books_root
        self.gate_mode = gate_mode or self.config.orchestrator.gate_mode
        self.coordination_mode = self.config.orchestrator.coordination_mode

        self.event_bus = EventBus()

        # LLM Manager — 多提供商管理
        self.llm_manager = LLMManager()
        self._init_llm_manager()

        # Agent 池
        self.writers: Dict[str, BaseWriterAgent] = {}
        self.reviewers: Dict[str, BaseReviewerAgent] = {}

        # Utility Agents（延迟初始化）
        self._glossary_guard = None
        self._consistency_checker = None
        self._reference_manager = None

        # 活跃任务
        self.active_tasks: Dict[str, WritingTask] = {}

        # 待人工审批的门控
        self._pending_gates: Dict[str, asyncio.Event] = {}
        self._gate_decisions: Dict[str, bool] = {}

        # 加载共享资源
        self._glossary = self._load_file("terminology/glossary_cn.md")
        self._symbols = self._load_file("terminology/symbols.md")

    def _init_llm_manager(self):
        """根据配置初始化 LLM Manager"""
        for role in ("default", "writer", "reviewer", "utility"):
            role_config = self.config.get_llm_config(role)
            if role_config.model:
                try:
                    provider = LLMProvider(role_config.provider)
                except ValueError:
                    provider = LLMProvider.OPENAI

                llm_config = LLMConfig(
                    provider=provider,
                    model=role_config.model,
                    api_key=role_config.api_key,
                    base_url=role_config.base_url,
                    max_tokens=role_config.max_tokens,
                    temperature=role_config.temperature,
                    top_p=role_config.top_p,
                    timeout=role_config.timeout,
                    max_retries=role_config.max_retries,
                    retry_delay=role_config.retry_delay,
                    fallback_model=role_config.fallback_model,
                    fallback_provider=role_config.fallback_provider,
                )
                self.llm_manager.register(role, llm_config)
                logger.info(
                    f"LLM [{role}]: {role_config.provider}/{role_config.model}"
                )

    # ── Utility Agent 惰性加载 ────────────────────────────────

    def _get_glossary_guard(self):
        if self._glossary_guard is None:
            from hydroscribe.agents.utilities.glossary_guard import GlossaryGuardAgent
            self._glossary_guard = GlossaryGuardAgent(name="glossary-guard")
            self._glossary_guard.event_bus = self.event_bus
            self._glossary_guard.glossary_content = self._glossary
            self._glossary_guard.symbols_content = self._symbols
            self._glossary_guard.llm = create_utility_bridge(self.llm_manager)
        return self._glossary_guard

    def _get_consistency_checker(self):
        if self._consistency_checker is None:
            from hydroscribe.agents.utilities.consistency_checker import ConsistencyCheckerAgent
            self._consistency_checker = ConsistencyCheckerAgent(
                name="consistency-checker", books_root=self.books_root
            )
            self._consistency_checker.event_bus = self.event_bus
            self._consistency_checker.llm = create_utility_bridge(self.llm_manager)
        return self._consistency_checker

    def _get_reference_manager(self):
        if self._reference_manager is None:
            from hydroscribe.agents.utilities.reference_manager import ReferenceManagerAgent
            self._reference_manager = ReferenceManagerAgent(name="reference-manager")
            self._reference_manager.event_bus = self.event_bus
            self._reference_manager.llm = create_utility_bridge(self.llm_manager)
        return self._reference_manager

    # ── 文件操作 ──────────────────────────────────────────────

    def _load_file(self, rel_path: str) -> str:
        """加载项目中的文件"""
        full_path = os.path.join(self.books_root, rel_path)
        if os.path.exists(full_path):
            with open(full_path, "r", encoding="utf-8") as f:
                return f.read()
        return ""

    def _load_progress(self, book_id: str) -> BookProgress:
        """读取 progress/BK[X].json"""
        progress_path = os.path.join(self.books_root, "progress", f"BK{book_id}.json")
        if os.path.exists(progress_path):
            with open(progress_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return BookProgress(**data)
        return BookProgress(book_id=book_id, book_title="", total_chapters=0)

    def _save_progress(self, progress: BookProgress):
        """保存进度文件"""
        progress_path = os.path.join(self.books_root, "progress", f"BK{progress.book_id}.json")
        os.makedirs(os.path.dirname(progress_path), exist_ok=True)
        with open(progress_path, "w", encoding="utf-8") as f:
            json.dump(progress.model_dump(), f, ensure_ascii=False, indent=2)

    def _find_next_chapter(self, progress: BookProgress, total_chapters: int) -> Optional[str]:
        """找到下一个待写章节"""
        for i in range(1, total_chapters + 1):
            ch_id = f"ch{i:02d}"
            ch_progress = progress.chapters.get(ch_id)
            if ch_progress is None or ch_progress.status in ("pending", "in_progress"):
                return ch_id
        return None

    def _load_prev_chapter_tail(self, book_id: str, chapter_id: str) -> str:
        """读取前序章节末尾 500 字"""
        ch_num = int(chapter_id.replace("ch", ""))
        if ch_num <= 1:
            return ""

        prev_ch = f"ch{ch_num - 1:02d}"
        for suffix in ["_final.md", "_v2.md", "_v1.md", ".md"]:
            path = os.path.join(self.books_root, "books", book_id, f"{prev_ch}{suffix}")
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                return content[-500:] if len(content) > 500 else content
        return ""

    def _get_style_guide(self, skill_type: SkillType, book_id: str) -> str:
        """根据文体和书目获取写作风格指南"""
        if skill_type == SkillType.BK:
            if book_id.startswith("T1"):
                return "先导版风格：语气介于学术论文和科普读物之间，每章开头用真实场景引入，数学公式仅在绝对必要时出现。"
            elif book_id.startswith("T2"):
                return "研究生教材风格：每段200-400字，一段一个中心思想。首句为主题句。数学公式三段式呈现（直觉→公式→解释）。"
            elif book_id == "M8":
                return "工程案例专著风格：叙事以工程为主线，理论为工具。大量使用实际运行数据。每个技术方案附实施要点和踩过的坑。"
            elif book_id == "M9":
                return "本科教材风格：前置知识仅要求大学物理+高等数学+流体力学。数学推导最少化，大量案例和图表。"
            else:
                return "学术专著风格：理论推导完整，公式可供研究生自学。包含可复现的数值算例。近5年文献≥40%。"
        elif skill_type == SkillType.SCI:
            return "SCI英文论文风格：Academic English, formal but precise. Follow target journal guidelines. ≥30 references."
        elif skill_type == SkillType.CN:
            return "中文核心期刊风格：摘要含目的-方法-结果-结论四要素。引文格式GB/T 7714-2015。每段≤400字。"
        elif skill_type == SkillType.PAT:
            return "发明专利风格：七部分结构（技术领域→背景→发明内容→附图→实施方式→权利要求→摘要）。权利要求8-15项。"
        elif skill_type == SkillType.RPT:
            return "技术报告风格：执行摘要独立可读。所有数据标注来源。建议附时间线/预算/责任分工。"
        elif skill_type == SkillType.STD_CN:
            return "国内标准风格：严格遵循GB/T 1.1-2020。条件用语（应/宜/可/不应/不宜）100%准确。法定计量单位。"
        elif skill_type == SkillType.STD_INT:
            return "国际标准风格：Follow ISO/IEC Directives Part 2. Use shall/should/may consistently. SI units only."
        elif skill_type == SkillType.WX:
            return "微信公众号风格：标题15-25字。段落≤150字。1500-2500字。每300字配图占位。结尾引导互动。"
        elif skill_type == SkillType.PPT:
            return "PPT演示风格：每页≤50字。15-25页。封面→目录→引言→核心→案例→总结→致谢→Q&A。每页附Speaker Notes。"
        return ""

    # ── 主流程 ──────────────────────────────────────────────────

    async def start_book(self, book_id: str, skill_type: str = "BK") -> Dict[str, Any]:
        """
        启动一本书的写作 — 对应 "开始BK[X]" 指令
        """
        logger.info(f"启动书目 {book_id} 写作")
        skill = SkillType(skill_type)

        progress = self._load_progress(book_id)

        next_ch = self._find_next_chapter(progress, progress.total_chapters or 16)
        if not next_ch:
            return {"status": "completed", "message": f"{book_id} 所有章节已完成"}

        task = WritingTask(
            book_id=book_id,
            chapter_id=next_ch,
            skill_type=skill,
            spec=ChapterSpec(
                chapter_id=next_ch,
                title=f"{book_id} {next_ch}",
                target_words=30000,
            ),
            reviewers=list(SKILL_REVIEWERS.get(skill, [])),
            max_iterations=SKILL_THRESHOLDS.get(skill, {}).get("max_iterations", 6),
            gate_mode=self.gate_mode,
        )

        self.active_tasks[task.id] = task

        await self.event_bus.publish(Event(
            type=EventType.TASK_CREATED,
            source_agent="orchestrator",
            book_id=book_id,
            chapter_id=next_ch,
            payload={"task_id": task.id, "skill": skill_type, "target_words": task.spec.target_words}
        ))

        result = await self.execute_writing_cycle(task)
        return result

    async def execute_writing_cycle(self, task: WritingTask) -> Dict[str, Any]:
        """
        执行 写作→质检→评审→门控 循环

        完整 DAG：
        write → [glossary_check, consistency_check, reference_check] → review → gate
        """
        skill = task.skill_type
        threshold = SKILL_THRESHOLDS.get(skill, {"min_score": 8.0, "max_iterations": 6})

        for iteration in range(1, task.max_iterations + 1):
            task.current_iteration = iteration
            task.status = "in_progress"

            logger.info(f"[{task.book_id}/{task.chapter_id}] 第 {iteration} 轮写作")

            await self.event_bus.publish(Event(
                type=EventType.REVISION_ROUND,
                source_agent="orchestrator",
                book_id=task.book_id,
                chapter_id=task.chapter_id,
                payload={"iteration": iteration, "max_iterations": task.max_iterations}
            ))

            # ① 写作
            writer = self._get_or_create_writer(skill)
            writer.glossary = self._glossary
            writer.symbols = self._symbols
            writer.style_guide = self._get_style_guide(skill, task.book_id)
            writer.prev_chapter_tail = self._load_prev_chapter_tail(task.book_id, task.chapter_id)

            try:
                write_result = await writer.write_chapter(task)
            except Exception as e:
                logger.error(
                    f"[{task.book_id}/{task.chapter_id}] 第 {iteration} 轮写作异常: {e}",
                    exc_info=True,
                )
                await self.event_bus.publish(Event(
                    type=EventType.TASK_FAILED,
                    source_agent="orchestrator",
                    book_id=task.book_id,
                    chapter_id=task.chapter_id,
                    payload={"iteration": iteration, "error": str(e)},
                ))
                task.status = "error"
                self._cleanup_task(task)
                return {
                    "status": "error",
                    "iterations": iteration,
                    "error": str(e),
                }

            # ② 保存初稿
            output_path = self._save_draft(task, write_result["content"], iteration)

            # ③ 并行质检（术语 + 一致性 + 参考文献 同时执行）
            utility_results = await self._parallel_utility_checks(
                content=write_result["content"],
                task=task,
            )

            # ④ 并行评审（加权）
            review_result = await self._parallel_review(
                content=write_result["content"],
                task=task,
                reviewer_roles=task.reviewers,
            )

            # ⑤ 综合评分（评审加权 + Utility检查）
            final_score = self._compute_final_score(review_result, utility_results, skill)
            review_result.avg_score = final_score

            # ⑥ 门控决策
            passed = self._gate_check(review_result, threshold)

            if passed:
                # 人工门控模式
                if task.gate_mode == "human":
                    passed = await self._wait_for_human_gate(task)
                elif task.gate_mode == "hybrid" and review_result.avg_score < threshold.get("min_score", 8.0) + 0.5:
                    passed = await self._wait_for_human_gate(task)

            if passed:
                final_path = self._save_final(task, write_result["content"])
                self._update_progress(task, write_result, review_result)

                await self.event_bus.publish(Event(
                    type=EventType.CHAPTER_COMPLETED,
                    source_agent="orchestrator",
                    book_id=task.book_id,
                    chapter_id=task.chapter_id,
                    payload={
                        "iterations": iteration,
                        "avg_score": review_result.avg_score,
                        "word_count": write_result["word_count"],
                        "file_path": final_path,
                        "utility_scores": {
                            k: v.get("score", 0) for k, v in utility_results.items()
                        },
                    }
                ))

                task.status = "completed"
                self._cleanup_task(task)
                return {
                    "status": "completed",
                    "iterations": iteration,
                    "score": review_result.avg_score,
                    "file": final_path,
                    "word_count": write_result["word_count"],
                    "utility_checks": utility_results,
                }
            else:
                await self.event_bus.publish(Event(
                    type=EventType.REVISION_NEEDED,
                    source_agent="orchestrator",
                    book_id=task.book_id,
                    chapter_id=task.chapter_id,
                    payload={
                        "iteration": iteration,
                        "avg_score": review_result.avg_score,
                        "recommendation": review_result.recommendation,
                        "utility_issues": {
                            k: v.get("passed", True) for k, v in utility_results.items()
                        },
                    }
                ))

                # 收集所有评审+质检意见
                feedback_parts = []
                for review in review_result.reviews:
                    feedback_parts.append(f"[{review.reviewer_role}] 评分: {review.overall}/10")
                    for issue in review.issues_red:
                        feedback_parts.append(f"  🔴 {issue}")
                    for issue in review.issues_yellow:
                        feedback_parts.append(f"  🟡 {issue}")

                # 附加 utility 反馈
                for check_name, check_result in utility_results.items():
                    if not check_result.get("passed", True):
                        feedback_parts.append(f"\n[{check_name}] 未通过 (分数: {check_result.get('score', 0)})")
                        if "forbidden_aliases_found" in check_result:
                            for alias in check_result["forbidden_aliases_found"][:5]:
                                feedback_parts.append(f"  🔴 禁止别名: '{alias['alias']}' → 应为 '{alias['correct_term']}'")
                        if "must_cite_missing" in check_result:
                            for ref in check_result["must_cite_missing"][:3]:
                                feedback_parts.append(f"  🟡 缺少必引文献: {ref}")

                writer.review_feedback = "\n".join(feedback_parts)

        task.status = "max_iterations_reached"
        self._cleanup_task(task)
        return {
            "status": "max_iterations_reached",
            "iterations": task.max_iterations,
            "message": "建议人工审核",
        }

    # ── 任务清理 ──────────────────────────────────────────────

    def _cleanup_task(self, task: WritingTask):
        """清理已完成任务的资源 — 防止内存泄漏"""
        # 从 active_tasks 移除
        self.active_tasks.pop(task.id, None)

        # 清理相关 gate
        gate_ids_to_remove = [
            gid for gid in self._pending_gates
            if gid.startswith(f"{task.book_id}_{task.chapter_id}")
        ]
        for gid in gate_ids_to_remove:
            self._pending_gates.pop(gid, None)

        logger.info(
            f"[{task.book_id}/{task.chapter_id}] 任务清理完成 "
            f"(active_tasks={len(self.active_tasks)}, gates={len(self._pending_gates)})"
        )

    # ── 并行质检 ──────────────────────────────────────────────

    async def _parallel_utility_checks(
        self,
        content: str,
        task: WritingTask,
    ) -> Dict[str, Dict[str, Any]]:
        """并行执行三项质检：术语 + 一致性 + 参考文献"""
        results = {}

        async def _glossary_check():
            guard = self._get_glossary_guard()
            return await guard.check(content, task.book_id, task.chapter_id)

        async def _consistency_check():
            checker = self._get_consistency_checker()
            return await checker.check(content, task.book_id, task.chapter_id)

        async def _reference_check():
            mgr = self._get_reference_manager()
            return await mgr.check(content, task.book_id, task.chapter_id, task.skill_type)

        checks = await asyncio.gather(
            _glossary_check(),
            _consistency_check(),
            _reference_check(),
            return_exceptions=True,
        )

        names = ["glossary", "consistency", "reference"]
        for name, result in zip(names, checks):
            if isinstance(result, dict):
                results[name] = result
            elif isinstance(result, Exception):
                logger.error(f"质检 {name} 失败: {result}")
                results[name] = {"passed": True, "score": 10.0, "error": str(result)}

        return results

    # ── 并行评审（加权）──────────────────────────────────────

    async def _parallel_review(
        self,
        content: str,
        task: WritingTask,
        reviewer_roles: List[ReviewerRole],
    ) -> AggregatedReview:
        """并行评审 — 所有 Reviewer 同时工作，按角色权重计算加权分"""

        async def _single_review(role: ReviewerRole) -> ReviewScore:
            reviewer = self._get_or_create_reviewer(role)
            return await reviewer.review(content, task.book_id, task.chapter_id)

        review_tasks = [_single_review(role) for role in reviewer_roles]
        scores = await asyncio.gather(*review_tasks, return_exceptions=True)

        valid_scores = []
        for s in scores:
            if isinstance(s, ReviewScore):
                valid_scores.append(s)
            elif isinstance(s, Exception):
                logger.error(f"评审失败: {s}")

        # 加权评分
        skill = task.skill_type
        weights = REVIEWER_WEIGHTS.get(skill, {})

        weighted_sum = 0.0
        weight_total = 0.0
        for score in valid_scores:
            role_enum = None
            for r in ReviewerRole:
                if r.value == score.reviewer_role:
                    role_enum = r
                    break
            w = weights.get(role_enum, 1.0 / max(len(valid_scores), 1))
            weighted_sum += score.overall * w
            weight_total += w

        avg_score = weighted_sum / max(weight_total, 0.01)
        has_red = any(len(s.issues_red) > 0 for s in valid_scores)

        result = AggregatedReview(
            reviews=valid_scores,
            avg_score=round(avg_score, 1),
            has_red_issues=has_red,
        )

        await self.event_bus.publish(Event(
            type=EventType.REVIEW_DONE,
            source_agent="orchestrator",
            book_id=task.book_id,
            chapter_id=task.chapter_id,
            payload={
                "avg_score": result.avg_score,
                "weighted": True,
                "has_red": result.has_red_issues,
                "reviewer_count": len(valid_scores),
                "scores": {s.reviewer_role: s.overall for s in valid_scores},
            }
        ))

        return result

    # ── 综合评分 ──────────────────────────────────────────────

    def _compute_final_score(
        self,
        review: AggregatedReview,
        utility: Dict[str, Dict],
        skill: SkillType,
    ) -> float:
        """
        综合评分 = 评审加权分 × 0.80 + Utility质检分 × 0.20
        """
        review_score = review.avg_score

        # Utility 平均分
        utility_scores = [v.get("score", 10.0) for v in utility.values()]
        utility_avg = sum(utility_scores) / max(len(utility_scores), 1)

        final = review_score * 0.80 + utility_avg * 0.20
        return round(final, 1)

    # ── 门控 ──────────────────────────────────────────────────

    def _gate_check(self, review: AggregatedReview, threshold: dict) -> bool:
        """门控检查 — 自动模式"""
        min_score = threshold.get("min_score", 8.0)
        no_red = threshold.get("no_red", False)
        compliance = threshold.get("compliance", False)

        passed = review.avg_score >= min_score
        if no_red and review.has_red_issues:
            passed = False
        if compliance:
            # 标准类文体要求100%合规
            all_accept = all(
                r.decision in ("accept", "minor") for r in review.reviews
            )
            if not all_accept:
                passed = False

        review.passed = passed
        review.recommendation = "approve" if passed else "revise"
        return passed

    async def _wait_for_human_gate(self, task: WritingTask) -> bool:
        """等待人工审批"""
        gate_id = f"{task.book_id}_{task.chapter_id}_v{task.current_iteration}"

        await self.event_bus.publish(Event(
            type=EventType.GATE_WAITING,
            source_agent="orchestrator",
            book_id=task.book_id,
            chapter_id=task.chapter_id,
            payload={"gate_id": gate_id, "message": "等待人工审批"}
        ))

        gate_event = asyncio.Event()
        self._pending_gates[gate_id] = gate_event

        # 等待（最多30分钟）
        try:
            await asyncio.wait_for(gate_event.wait(), timeout=1800)
        except asyncio.TimeoutError:
            logger.warning(f"门控 {gate_id} 超时，自动通过")
            return True

        return self._gate_decisions.get(gate_id, True)

    def approve_gate(self, gate_id: str):
        """外部调用 — 批准门控"""
        self._gate_decisions[gate_id] = True
        if gate_id in self._pending_gates:
            self._pending_gates[gate_id].set()

    def reject_gate(self, gate_id: str):
        """外部调用 — 驳回门控"""
        self._gate_decisions[gate_id] = False
        if gate_id in self._pending_gates:
            self._pending_gates[gate_id].set()

    # ── Agent 管理 ────────────────────────────────────────────

    def _get_or_create_writer(self, skill_type: SkillType) -> BaseWriterAgent:
        """获取或创建 Writer Agent（优先使用专业Writer注册表）"""
        key = skill_type.value
        if key not in self.writers:
            from hydroscribe.agents.writers import WRITER_REGISTRY
            agent_cls = WRITER_REGISTRY.get(key)
            if agent_cls:
                agent = agent_cls(name=f"writer-{key.lower()}")
            else:
                agent = BaseWriterAgent(name=f"writer-{key.lower()}", skill_type=skill_type)
            agent.event_bus = self.event_bus
            # 注入 LLM Bridge — 让 Agent.step() 使用 HydroScribe LLMManager
            agent.llm = create_writer_bridge(self.llm_manager)
            self.writers[key] = agent
        return self.writers[key]

    def _get_or_create_reviewer(self, role: ReviewerRole) -> BaseReviewerAgent:
        """获取或创建 Reviewer Agent（优先使用专业Reviewer注册表）"""
        key = role.value
        if key not in self.reviewers:
            agent = None
            # 优先从 REVIEWER_REGISTRY 加载专业评审
            try:
                from hydroscribe.agents.reviewers import REVIEWER_REGISTRY
                agent_cls = REVIEWER_REGISTRY.get(role)
                if agent_cls:
                    agent = agent_cls(name=f"reviewer-{key}")
            except ImportError:
                pass

            if agent is None:
                # 回退：使用基类 + 外部prompt文件
                prompt_template = self._load_reviewer_prompt(role)
                agent = BaseReviewerAgent(
                    name=f"reviewer-{key}",
                    reviewer_role=role,
                    reviewer_prompt_template=prompt_template,
                )
            agent.event_bus = self.event_bus
            # 注入 LLM Bridge — 让 Agent.step() 使用 HydroScribe LLMManager
            agent.llm = create_reviewer_bridge(self.llm_manager)
            self.reviewers[key] = agent
        return self.reviewers[key]

    def _load_reviewer_prompt(self, role: ReviewerRole) -> str:
        """从 writing-projects/academic-writer-skill/agents/ 加载评审提示词"""
        role_file_map = {
            ReviewerRole.INSTRUCTOR: "book_reviewer.md",
            ReviewerRole.EXPERT: "book_reviewer.md",
            ReviewerRole.ENGINEER: "book_reviewer.md",
            ReviewerRole.INTERNATIONAL: "book_reviewer.md",
            ReviewerRole.REVIEWER_A: "sci_reviewer.md",
            ReviewerRole.REVIEWER_B: "sci_reviewer.md",
            ReviewerRole.REVIEWER_C: "sci_reviewer.md",
            ReviewerRole.CN_REVIEWER_A: "cn_reviewer.md",
            ReviewerRole.CN_REVIEWER_B: "cn_reviewer.md",
            ReviewerRole.CN_REVIEWER_C: "cn_reviewer.md",
            ReviewerRole.PATENT_EXAMINER: "patent_reviewer.md",
            ReviewerRole.PATENT_AGENT: "patent_reviewer.md",
            ReviewerRole.PATENT_TECH: "patent_reviewer.md",
            ReviewerRole.TECH_REVIEWER: "rpt_reviewer.md",
            ReviewerRole.MGMT_REVIEWER: "rpt_reviewer.md",
            ReviewerRole.STD_CN_STANDARD: "std_cn_reviewer.md",
            ReviewerRole.STD_CN_TECH: "std_cn_reviewer.md",
            ReviewerRole.STD_CN_IMPL: "std_cn_reviewer.md",
            ReviewerRole.STD_INT_ISO: "std_int_reviewer.md",
            ReviewerRole.STD_INT_HYDRO: "std_int_reviewer.md",
            ReviewerRole.STD_INT_INDUSTRY: "std_int_reviewer.md",
            ReviewerRole.WX_READER: "wechat_reviewer.md",
            ReviewerRole.WX_EDITOR: "wechat_reviewer.md",
            ReviewerRole.WX_DOMAIN: "wechat_reviewer.md",
            ReviewerRole.PPT_AUDIENCE: "ppt_reviewer.md",
            ReviewerRole.PPT_DESIGN: "ppt_reviewer.md",
            ReviewerRole.PPT_CONTENT: "ppt_reviewer.md",
        }

        filename = role_file_map.get(role, "book_reviewer.md")
        path = os.path.join(
            self.books_root,
            "writing-projects", "academic-writer-skill", "agents",
            filename,
        )
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        return ""

    # ── 文件保存 ──────────────────────────────────────────────

    def _save_draft(self, task: WritingTask, content: str, iteration: int) -> str:
        """保存初稿"""
        dir_path = os.path.join(self.books_root, "books", task.book_id)
        os.makedirs(dir_path, exist_ok=True)
        filename = f"{task.chapter_id}_v{iteration}.md"
        path = os.path.join(dir_path, filename)

        header = f"<!-- 变更日志\nv{iteration} {datetime.now().strftime('%Y-%m-%d')}: {'初稿' if iteration == 1 else f'第{iteration}轮修改'}\n-->\n\n"
        with open(path, "w", encoding="utf-8") as f:
            f.write(header + content)
        return path

    def _save_final(self, task: WritingTask, content: str) -> str:
        """保存终稿"""
        dir_path = os.path.join(self.books_root, "books", task.book_id)
        os.makedirs(dir_path, exist_ok=True)
        path = os.path.join(dir_path, f"{task.chapter_id}_final.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def _update_progress(self, task: WritingTask, write_result: dict, review: AggregatedReview):
        """更新进度文件"""
        progress = self._load_progress(task.book_id)

        progress.chapters[task.chapter_id] = ChapterProgress(
            status="completed",
            word_count=write_result["word_count"],
            review_passed=True,
            review_scores={s.reviewer_role: s.overall for s in review.reviews},
            last_updated=datetime.now().strftime("%Y-%m-%d"),
            iterations=task.current_iteration,
        )

        completed = sum(1 for ch in progress.chapters.values() if ch.status == "completed")
        total = progress.total_chapters or 16
        progress.overall_progress = f"{completed / total * 100:.1f}%"

        self._save_progress(progress)

    # ── 评审记录保存 ──────────────────────────────────────────

    def _save_review_record(self, task: WritingTask, review: AggregatedReview, iteration: int):
        """保存评审记录到 reviews/ 目录"""
        reviews_dir = os.path.join(self.books_root, "reviews")
        os.makedirs(reviews_dir, exist_ok=True)

        filename = f"BK{task.book_id}_{task.chapter_id}_r{iteration}.md"
        path = os.path.join(reviews_dir, filename)

        lines = [
            f"# 评审记录 — {task.book_id} {task.chapter_id} 第{iteration}轮",
            f"",
            f"- 日期: {datetime.now().strftime('%Y-%m-%d')}",
            f"- 加权综合分: {review.avg_score}/10",
            f"- 通过: {'是' if review.passed else '否'}",
            f"",
        ]

        for r in review.reviews:
            lines.append(f"## [{r.reviewer_role}] 评分: {r.overall}/10 | 决定: {r.decision}")
            if r.issues_red:
                lines.append("### 🔴 致命问题")
                for issue in r.issues_red:
                    lines.append(f"- {issue}")
            if r.issues_yellow:
                lines.append("### 🟡 重要问题")
                for issue in r.issues_yellow:
                    lines.append(f"- {issue}")
            if r.issues_green:
                lines.append("### 🟢 建议")
                for issue in r.issues_green:
                    lines.append(f"- {issue}")
            if r.comments:
                lines.append(f"\n> {r.comments[:500]}")
            lines.append("")

        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    # ── 多Agent协同模式 ────────────────────────────────────────

    async def execute_master_slave(
        self, book_id: str, chapter_ids: List[str], skill_type: str = "BK"
    ) -> Dict[str, Any]:
        """
        主从模式 — Orchestrator 作为 Master 分配多章写作给并行 Writer

        适用场景：需要同时推进多个章节（如赶工期）
        限制：并行数受 config.orchestrator.max_concurrent_writers 控制
        """
        skill = SkillType(skill_type)
        max_concurrent = self.config.orchestrator.max_concurrent_writers
        results = {}

        semaphore = asyncio.Semaphore(max_concurrent)

        async def _write_chapter(ch_id: str):
            async with semaphore:
                logger.info(f"[master_slave] 分配 {book_id}/{ch_id} 给并行 Writer")
                return await self.start_book_chapter(book_id, ch_id, skill_type)

        tasks_list = [_write_chapter(ch_id) for ch_id in chapter_ids]
        completed = await asyncio.gather(*tasks_list, return_exceptions=True)

        for ch_id, result in zip(chapter_ids, completed):
            if isinstance(result, Exception):
                results[ch_id] = {"status": "error", "error": str(result)}
            else:
                results[ch_id] = result

        return {
            "mode": "master_slave",
            "book_id": book_id,
            "chapters_requested": len(chapter_ids),
            "results": results,
        }

    async def start_book_chapter(
        self, book_id: str, chapter_id: str, skill_type: str = "BK"
    ) -> Dict[str, Any]:
        """启动指定章节的写作"""
        skill = SkillType(skill_type)

        task = WritingTask(
            book_id=book_id,
            chapter_id=chapter_id,
            skill_type=skill,
            spec=ChapterSpec(
                chapter_id=chapter_id,
                title=f"{book_id} {chapter_id}",
                target_words=30000,
            ),
            reviewers=list(SKILL_REVIEWERS.get(skill, [])),
            max_iterations=SKILL_THRESHOLDS.get(skill, {}).get("max_iterations", 6),
            gate_mode=self.gate_mode,
        )

        self.active_tasks[task.id] = task

        await self.event_bus.publish(Event(
            type=EventType.TASK_CREATED,
            source_agent="orchestrator",
            book_id=book_id,
            chapter_id=chapter_id,
            payload={"task_id": task.id, "skill": skill_type, "mode": self.coordination_mode}
        ))

        return await self.execute_writing_cycle(task)

    # ── LLM 用量查询 ────────────────────────────────────────────

    def get_llm_usage(self) -> Dict[str, Any]:
        """获取所有角色的 LLM token 用量"""
        usage = self.llm_manager.get_all_usage()
        return {
            role: {
                "prompt_tokens": u.prompt_tokens,
                "completion_tokens": u.completion_tokens,
                "total_tokens": u.total_tokens,
                "model": u.model,
                "provider": u.provider,
            }
            for role, u in usage.items()
        }

    # ── 状态查询 ──────────────────────────────────────────────

    def get_status(self) -> Dict[str, Any]:
        """获取系统当前状态（供 API 使用）"""
        return {
            "active_tasks": {k: v.model_dump() for k, v in self.active_tasks.items()},
            "writers": {k: {"name": v.name, "skill": v.skill_type.value} for k, v in self.writers.items()},
            "reviewers": {k: {"name": v.name, "role": v.reviewer_role.value} for k, v in self.reviewers.items()},
            "utility_agents": {
                "glossary_guard": self._glossary_guard is not None,
                "consistency_checker": self._consistency_checker is not None,
                "reference_manager": self._reference_manager is not None,
            },
            "pending_gates": list(self._pending_gates.keys()),
            "event_history_count": len(self.event_bus._history),
            "coordination_mode": self.coordination_mode,
            "llm_config": {
                "provider": self.config.llm_default.provider,
                "model": self.config.llm_default.model,
            },
            "llm_usage": self.get_llm_usage(),
        }
