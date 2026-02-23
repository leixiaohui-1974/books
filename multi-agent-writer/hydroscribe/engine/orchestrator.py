"""
Orchestrator — 多智能体编排器（系统大脑）
参考 OpenManus PlanningFlow，实现 Plan → Execute → Reflect 三阶段循环
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
from hydroscribe.agents.base_writer import BaseWriterAgent
from hydroscribe.agents.base_reviewer import BaseReviewerAgent

logger = logging.getLogger("hydroscribe.orchestrator")


class Orchestrator:
    """
    多智能体编排器 — 系统大脑

    职责：
    1. Plan  — 解析用户指令，读取书目规格，生成写作 DAG
    2. Execute — 按 DAG 调度 Writer/Reviewer/Utility Agent
    3. Reflect — 汇总评审结果，门控决策，更新进度
    """

    def __init__(
        self,
        books_root: str = "/home/user/books",
        gate_mode: str = "auto",
    ):
        self.books_root = books_root
        self.gate_mode = gate_mode
        self.event_bus = EventBus()

        # Agent 池
        self.writers: Dict[str, BaseWriterAgent] = {}
        self.reviewers: Dict[str, BaseReviewerAgent] = {}

        # 活跃任务
        self.active_tasks: Dict[str, WritingTask] = {}

        # 加载共享资源
        self._glossary = self._load_file("terminology/glossary_cn.md")
        self._symbols = self._load_file("terminology/symbols.md")

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
        # 尝试多种文件名模式
        for suffix in ["_final.md", "_v2.md", "_v1.md", ".md"]:
            path = os.path.join(self.books_root, "books", book_id, f"{prev_ch}{suffix}")
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                return content[-500:] if len(content) > 500 else content
        return ""

    def _get_style_guide(self, skill_type: SkillType, book_id: str) -> str:
        """根据文体和书目获取写作风格指南"""
        # 从 CLAUDE.md §8 加载
        if skill_type == SkillType.BK:
            if book_id.startswith("T1"):
                return "先导版风格：语气介于学术论文和科普读物之间，每章开头用真实场景引入，数学公式仅在绝对必要时出现。"
            elif book_id.startswith("T2"):
                return "研究生教材风格：每段200-400字，一段一个中心思想。首句为主题句。数学公式三段式呈现。"
            elif book_id.startswith("M8"):
                return "工程案例专著风格：叙事以工程为主线，理论为工具。大量使用实际运行数据。每个技术方案附实施要点和踩过的坑。"
            else:
                return "学术专著风格：理论推导完整，公式可供研究生自学。包含可复现的数值算例。"
        return ""

    # ── 主流程 ──────────────────────────────────────────────────

    async def start_book(self, book_id: str, skill_type: str = "BK") -> Dict[str, Any]:
        """
        启动一本书的写作 — 对应 "开始BK[X]" 指令

        流程：
        1. 读取书目规格
        2. 读取进度文件
        3. 定位下一待写章节
        4. 创建 WritingTask
        5. 执行 写作→评审→门控 循环
        """
        logger.info(f"启动书目 {book_id} 写作")
        skill = SkillType(skill_type)

        # 读取进度
        progress = self._load_progress(book_id)

        # 创建任务
        # (实际中应从 CLAUDE.md 解析，这里用简化版)
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

        # 执行写作→评审循环
        result = await self.execute_writing_cycle(task)
        return result

    async def execute_writing_cycle(self, task: WritingTask) -> Dict[str, Any]:
        """
        执行 写作→检查→评审→门控 循环

        这是系统的核心循环，对应设计文档中的 DAG 执行流程。
        """
        skill = task.skill_type
        threshold = SKILL_THRESHOLDS.get(skill, {"min_score": 8.0, "max_iterations": 6})

        for iteration in range(1, task.max_iterations + 1):
            task.current_iteration = iteration
            task.status = "in_progress"

            logger.info(f"[{task.book_id}/{task.chapter_id}] 第 {iteration} 轮写作")

            # ① 写作
            writer = self._get_or_create_writer(skill)
            writer.glossary = self._glossary
            writer.symbols = self._symbols
            writer.style_guide = self._get_style_guide(skill, task.book_id)
            writer.prev_chapter_tail = self._load_prev_chapter_tail(task.book_id, task.chapter_id)

            if iteration > 1:
                writer.review_feedback = task.status  # 传入上轮评审意见

            write_result = await writer.write_chapter(task)

            # ② 保存初稿
            output_path = self._save_draft(task, write_result["content"], iteration)

            # ③ 并行评审
            review_result = await self._parallel_review(
                content=write_result["content"],
                task=task,
                reviewer_roles=task.reviewers,
            )

            # ④ 门控决策
            passed = self._gate_check(review_result, threshold)

            if passed:
                # 通过 → 保存终稿 + 更新进度
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
                    }
                ))

                task.status = "completed"
                return {
                    "status": "completed",
                    "iterations": iteration,
                    "score": review_result.avg_score,
                    "file": final_path,
                    "word_count": write_result["word_count"],
                }
            else:
                # 未通过 → 准备修改意见
                await self.event_bus.publish(Event(
                    type=EventType.REVISION_NEEDED,
                    source_agent="orchestrator",
                    book_id=task.book_id,
                    chapter_id=task.chapter_id,
                    payload={
                        "iteration": iteration,
                        "avg_score": review_result.avg_score,
                        "recommendation": review_result.recommendation,
                    }
                ))

                # 收集所有评审意见作为下轮修改参考
                feedback_parts = []
                for review in review_result.reviews:
                    feedback_parts.append(f"[{review.reviewer_role}] 评分: {review.overall}/10")
                    for issue in review.issues_red:
                        feedback_parts.append(f"  🔴 {issue}")
                    for issue in review.issues_yellow:
                        feedback_parts.append(f"  🟡 {issue}")
                writer.review_feedback = "\n".join(feedback_parts)

        # 超过最大迭代次数
        task.status = "max_iterations_reached"
        return {
            "status": "max_iterations_reached",
            "iterations": task.max_iterations,
            "message": "建议人工审核",
        }

    async def _parallel_review(
        self,
        content: str,
        task: WritingTask,
        reviewer_roles: List[ReviewerRole],
    ) -> AggregatedReview:
        """并行评审 — 所有 Reviewer 同时工作"""

        async def _single_review(role: ReviewerRole) -> ReviewScore:
            reviewer = self._get_or_create_reviewer(role)
            return await reviewer.review(content, task.book_id, task.chapter_id)

        # 并行执行所有评审
        review_tasks = [_single_review(role) for role in reviewer_roles]
        scores = await asyncio.gather(*review_tasks, return_exceptions=True)

        # 收集有效结果
        valid_scores = []
        for s in scores:
            if isinstance(s, ReviewScore):
                valid_scores.append(s)
            elif isinstance(s, Exception):
                logger.error(f"评审失败: {s}")

        # 汇总
        avg_score = sum(s.overall for s in valid_scores) / max(len(valid_scores), 1)
        has_red = any(len(s.issues_red) > 0 for s in valid_scores)

        result = AggregatedReview(
            reviews=valid_scores,
            avg_score=round(avg_score, 1),
            has_red_issues=has_red,
        )

        # 发布评审完成事件
        await self.event_bus.publish(Event(
            type=EventType.REVIEW_DONE,
            source_agent="orchestrator",
            book_id=task.book_id,
            chapter_id=task.chapter_id,
            payload={
                "avg_score": result.avg_score,
                "has_red": result.has_red_issues,
                "reviewer_count": len(valid_scores),
                "scores": {s.reviewer_role: s.overall for s in valid_scores},
            }
        ))

        return result

    def _gate_check(self, review: AggregatedReview, threshold: dict) -> bool:
        """门控检查 — 决定是否通过"""
        min_score = threshold.get("min_score", 8.0)
        no_red = threshold.get("no_red", False)

        passed = review.avg_score >= min_score
        if no_red and review.has_red_issues:
            passed = False

        review.passed = passed
        review.recommendation = "approve" if passed else "revise"
        return passed

    # ── Agent 管理 ────────────────────────────────────────────

    def _get_or_create_writer(self, skill_type: SkillType) -> BaseWriterAgent:
        """获取或创建 Writer Agent"""
        key = skill_type.value
        if key not in self.writers:
            from hydroscribe.agents.writers import WRITER_REGISTRY
            agent_cls = WRITER_REGISTRY.get(key)
            if agent_cls:
                agent = agent_cls(name=f"writer-{key.lower()}")
                agent.event_bus = self.event_bus
                self.writers[key] = agent
            else:
                # fallback to base
                agent = BaseWriterAgent(name=f"writer-{key.lower()}", skill_type=skill_type)
                agent.event_bus = self.event_bus
                self.writers[key] = agent
        return self.writers[key]

    def _get_or_create_reviewer(self, role: ReviewerRole) -> BaseReviewerAgent:
        """获取或创建 Reviewer Agent"""
        key = role.value
        if key not in self.reviewers:
            # 加载对应的评审 prompt
            prompt_template = self._load_reviewer_prompt(role)
            agent = BaseReviewerAgent(
                name=f"reviewer-{key}",
                reviewer_role=role,
                reviewer_prompt_template=prompt_template,
            )
            agent.event_bus = self.event_bus
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
            ReviewerRole.PATENT_EXAMINER: "patent_reviewer.md",
            ReviewerRole.TECH_REVIEWER: "rpt_reviewer.md",
            ReviewerRole.STD_CN_STANDARD: "std_cn_reviewer.md",
            ReviewerRole.STD_INT_ISO: "std_int_reviewer.md",
            ReviewerRole.WX_READER: "wechat_reviewer.md",
            ReviewerRole.PPT_AUDIENCE: "ppt_reviewer.md",
        }

        filename = role_file_map.get(role, "book_reviewer.md")
        path = os.path.join(
            self.books_root,
            "writing-projects", "academic-writer-skill", "agents",
            filename,
        )
        return self._load_file(path) if os.path.exists(path) else ""

    # ── 文件操作 ──────────────────────────────────────────────

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

        # 计算整体进度
        completed = sum(1 for ch in progress.chapters.values() if ch.status == "completed")
        total = progress.total_chapters or 16
        progress.overall_progress = f"{completed / total * 100:.1f}%"

        self._save_progress(progress)

    # ── 状态查询 ──────────────────────────────────────────────

    def get_status(self) -> Dict[str, Any]:
        """获取系统当前状态（供 API 使用）"""
        return {
            "active_tasks": {k: v.model_dump() for k, v in self.active_tasks.items()},
            "writers": {k: {"name": v.name, "skill": v.skill_type.value} for k, v in self.writers.items()},
            "reviewers": {k: {"name": v.name, "role": v.reviewer_role.value} for k, v in self.reviewers.items()},
            "event_history_count": len(self.event_bus._history),
        }
