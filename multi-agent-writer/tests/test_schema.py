"""
测试 Schema — 数据模型完整性
"""

import pytest
from hydroscribe.schema import (
    SkillType, ReviewerRole, EventType, Event,
    ChapterSpec, WritingTask, ReviewScore, AggregatedReview,
    BookProgress, ChapterProgress,
    SKILL_REVIEWERS, SKILL_THRESHOLDS,
)


class TestSkillType:
    def test_all_9_skills(self):
        assert len(SkillType) == 9
        expected = {"BK", "SCI", "CN", "PAT", "RPT", "STD-CN", "STD-INT", "WX", "PPT"}
        actual = {s.value for s in SkillType}
        assert actual == expected


class TestReviewerRole:
    def test_all_28_roles(self):
        assert len(ReviewerRole) == 28

    def test_bk_roles(self):
        bk_roles = {ReviewerRole.INSTRUCTOR, ReviewerRole.EXPERT,
                     ReviewerRole.ENGINEER, ReviewerRole.INTERNATIONAL}
        assert all(r in ReviewerRole for r in bk_roles)

    def test_sci_roles(self):
        assert ReviewerRole.REVIEWER_A.value == "reviewer_a"
        assert ReviewerRole.REVIEWER_B.value == "reviewer_b"
        assert ReviewerRole.REVIEWER_C.value == "reviewer_c"


class TestEventType:
    def test_event_types_exist(self):
        critical_types = [
            EventType.TASK_CREATED, EventType.WRITING_STARTED,
            EventType.WRITING_CHUNK, EventType.WRITING_DONE,
            EventType.REVIEW_STARTED, EventType.REVIEW_SCORE,
            EventType.REVIEW_DONE, EventType.CHECK_GLOSSARY,
            EventType.CHECK_CONSISTENCY, EventType.CHECK_REFERENCE,
            EventType.GATE_WAITING, EventType.GATE_APPROVED,
            EventType.CHAPTER_COMPLETED,
        ]
        for et in critical_types:
            assert et is not None


class TestSkillReviewerMapping:
    def test_all_skills_have_reviewers(self):
        for skill in SkillType:
            assert skill in SKILL_REVIEWERS, f"{skill} missing from SKILL_REVIEWERS"
            assert len(SKILL_REVIEWERS[skill]) >= 2

    def test_bk_has_4_reviewers(self):
        assert len(SKILL_REVIEWERS[SkillType.BK]) == 4

    def test_rpt_has_2_reviewers(self):
        assert len(SKILL_REVIEWERS[SkillType.RPT]) == 2

    def test_all_skills_have_thresholds(self):
        for skill in SkillType:
            assert skill in SKILL_THRESHOLDS


class TestWritingTask:
    def test_create_task(self):
        task = WritingTask(
            book_id="T2a",
            chapter_id="ch07",
            skill_type=SkillType.BK,
            spec=ChapterSpec(chapter_id="ch07", title="MPC", target_words=40000),
        )
        assert task.book_id == "T2a"
        assert task.status == "pending"
        assert task.max_iterations == 6


class TestReviewScore:
    def test_create_score(self):
        score = ReviewScore(
            reviewer_role="instructor",
            overall=8.5,
            decision="minor",
            issues_red=["致命问题"],
            issues_yellow=["重要问题"],
        )
        assert score.overall == 8.5
        assert len(score.issues_red) == 1

    def test_aggregated_review(self):
        reviews = [
            ReviewScore(reviewer_role="instructor", overall=8.0),
            ReviewScore(reviewer_role="expert", overall=9.0),
        ]
        agg = AggregatedReview(
            reviews=reviews,
            avg_score=8.5,
        )
        assert agg.avg_score == 8.5
        assert len(agg.reviews) == 2


class TestBookProgress:
    def test_create_progress(self):
        progress = BookProgress(
            book_id="T2a",
            book_title="建模与控制",
            total_chapters=16,
        )
        assert progress.overall_progress == "0%"

    def test_with_chapters(self):
        progress = BookProgress(
            book_id="T1-CN",
            book_title="水系统控制论",
            total_chapters=8,
            chapters={
                "ch01": ChapterProgress(status="completed", word_count=15000),
                "ch02": ChapterProgress(status="in_progress", word_count=8000),
            }
        )
        assert progress.chapters["ch01"].status == "completed"
        assert progress.chapters["ch02"].word_count == 8000
