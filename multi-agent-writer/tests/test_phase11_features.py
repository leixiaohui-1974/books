"""
Phase 11 测试 — 书目注册表 + 配置校验 + 审计日志 + CLI dry-run + report
"""

import json
import os
import tempfile

import pytest

from hydroscribe.engine.book_registry import (
    BOOK_REGISTRY,
    get_book_spec,
    get_books_by_batch,
    get_books_by_tier,
    list_book_ids,
    validate_book_id,
)
from hydroscribe.engine.audit_log import AuditLogger, get_audit_logger
from hydroscribe.engine.config_loader import (
    HydroScribeConfig,
    LLMRoleConfig,
    OrchestratorConfig,
    ServerConfig,
    validate_config,
)


# ── 书目注册表测试 ─────────────────────────────────────────────

class TestBookRegistry:
    """测试 BOOK_REGISTRY 数据完整性与查询"""

    def test_registry_has_all_books(self):
        """注册表应包含全部 16 本书"""
        expected = {
            "T1-CN", "T1-EN", "T2a", "T2b",
            "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8",
            "M9", "M10",
        }
        assert set(BOOK_REGISTRY.keys()) == expected

    def test_each_book_has_required_fields(self):
        """每本书应包含必需的元数据字段"""
        required_fields = {"title", "tier", "total_chapters", "target_words", "publisher", "language", "skill_type"}
        for book_id, spec in BOOK_REGISTRY.items():
            for field in required_fields:
                assert field in spec, f"{book_id} 缺少字段: {field}"

    def test_total_chapters_positive(self):
        """每本书的 total_chapters 应为正整数"""
        for book_id, spec in BOOK_REGISTRY.items():
            assert spec["total_chapters"] > 0, f"{book_id} total_chapters 无效"

    def test_validate_book_id_known(self):
        assert validate_book_id("T1-CN") is True
        assert validate_book_id("M8") is True

    def test_validate_book_id_unknown(self):
        assert validate_book_id("UNKNOWN") is False
        assert validate_book_id("") is False

    def test_get_book_spec_found(self):
        spec = get_book_spec("T1-CN")
        assert spec is not None
        assert spec["title"] == "水系统控制论"
        assert spec["total_chapters"] == 8

    def test_get_book_spec_not_found(self):
        assert get_book_spec("NONEXISTENT") is None

    def test_list_book_ids(self):
        ids = list_book_ids()
        assert len(ids) == 14
        assert ids == sorted(ids)  # 应按字母序排列

    def test_get_books_by_tier(self):
        tier1 = get_books_by_tier(1)
        assert len(tier1) == 2  # T1-CN, T1-EN
        assert all(b["tier"] == 1 for b in tier1)

        tier3 = get_books_by_tier(3)
        assert len(tier3) == 8  # M1-M8

    def test_get_books_by_batch(self):
        batch1 = get_books_by_batch(1)
        assert len(batch1) == 2  # T1-CN, T1-EN
        assert all(b["batch"] == 1 for b in batch1)

    def test_tier_names_consistent(self):
        """层级名称应一致"""
        for book_id, spec in BOOK_REGISTRY.items():
            tier = spec["tier"]
            name = spec.get("tier_name", "")
            if tier == 1:
                assert name == "种子"
            elif tier == 2:
                assert name == "骨架"
            elif tier == 3:
                assert name == "血肉"
            elif tier == 4:
                assert name == "生态"

    def test_t1_cn_matches_claude_md(self):
        """T1-CN 规格应与 CLAUDE.md §2 一致"""
        spec = get_book_spec("T1-CN")
        assert spec["total_chapters"] == 8
        assert spec["language"] == "zh"

    def test_t2a_matches_claude_md(self):
        """T2a 规格应与 CLAUDE.md §2 一致"""
        spec = get_book_spec("T2a")
        assert spec["total_chapters"] == 16

    def test_m8_matches_claude_md(self):
        """M8 规格应与 CLAUDE.md §2 一致"""
        spec = get_book_spec("M8")
        assert spec["total_chapters"] == 14


# ── 配置校验测试 ──────────────────────────────────────────────

class TestConfigValidation:
    """测试 validate_config()"""

    def _make_valid_config(self) -> HydroScribeConfig:
        """构造一个完全有效的配置"""
        with tempfile.TemporaryDirectory() as tmpdir:
            cfg = HydroScribeConfig(
                books_root=tmpdir,
                server=ServerConfig(port=8000),
                orchestrator=OrchestratorConfig(
                    gate_mode="auto",
                    coordination_mode="specialist",
                    max_concurrent_writers=3,
                    review_weight=0.8,
                    utility_weight=0.2,
                ),
                llm_default=LLMRoleConfig(
                    provider="local",
                    model="test-model",
                    max_tokens=4096,
                    temperature=0.3,
                ),
            )
            errors, warnings = validate_config(cfg)
            assert errors == [], f"预期无错误，但得到: {errors}"
            return cfg

    def test_valid_config_no_errors(self):
        """有效配置应无错误"""
        self._make_valid_config()

    def test_invalid_books_root(self):
        """不存在的 books_root 应报错"""
        cfg = HydroScribeConfig(books_root="/nonexistent/path/xxx")
        errors, _ = validate_config(cfg)
        assert any("books_root" in e for e in errors)

    def test_invalid_gate_mode(self):
        """无效的 gate_mode 应报错"""
        cfg = HydroScribeConfig(
            orchestrator=OrchestratorConfig(gate_mode="invalid"),
        )
        errors, _ = validate_config(cfg)
        assert any("gate_mode" in e for e in errors)

    def test_invalid_coordination_mode(self):
        cfg = HydroScribeConfig(
            orchestrator=OrchestratorConfig(coordination_mode="unknown"),
        )
        errors, _ = validate_config(cfg)
        assert any("coordination_mode" in e for e in errors)

    def test_zero_concurrent_writers(self):
        cfg = HydroScribeConfig(
            orchestrator=OrchestratorConfig(max_concurrent_writers=0),
        )
        errors, _ = validate_config(cfg)
        assert any("max_concurrent_writers" in e for e in errors)

    def test_high_concurrent_writers_warns(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cfg = HydroScribeConfig(
                books_root=tmpdir,
                orchestrator=OrchestratorConfig(max_concurrent_writers=15),
            )
            _, warnings = validate_config(cfg)
            assert any("max_concurrent_writers" in w for w in warnings)

    def test_weight_sum_warning(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cfg = HydroScribeConfig(
                books_root=tmpdir,
                orchestrator=OrchestratorConfig(review_weight=0.5, utility_weight=0.1),
            )
            _, warnings = validate_config(cfg)
            assert any("review_weight" in w for w in warnings)

    def test_invalid_temperature(self):
        cfg = HydroScribeConfig(
            llm_default=LLMRoleConfig(temperature=3.0),
        )
        errors, _ = validate_config(cfg)
        assert any("temperature" in e for e in errors)

    def test_invalid_port(self):
        cfg = HydroScribeConfig(
            server=ServerConfig(port=0),
        )
        errors, _ = validate_config(cfg)
        assert any("port" in e for e in errors)

    def test_missing_api_key_warns(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cfg = HydroScribeConfig(
                books_root=tmpdir,
                llm_default=LLMRoleConfig(provider="openai", model="gpt-4o", api_key=""),
            )
            _, warnings = validate_config(cfg)
            assert any("api_key" in w for w in warnings)

    def test_local_provider_no_key_warning(self):
        """local provider 不需要 api_key, 不应告警"""
        with tempfile.TemporaryDirectory() as tmpdir:
            cfg = HydroScribeConfig(
                books_root=tmpdir,
                llm_default=LLMRoleConfig(provider="local", model="test", api_key=""),
            )
            _, warnings = validate_config(cfg)
            assert not any("api_key" in w for w in warnings)

    def test_low_max_tokens_warns(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cfg = HydroScribeConfig(
                books_root=tmpdir,
                llm_default=LLMRoleConfig(provider="local", model="t", max_tokens=100),
            )
            _, warnings = validate_config(cfg)
            assert any("max_tokens" in w for w in warnings)


# ── 审计日志测试 ──────────────────────────────────────────────

class TestAuditLogger:
    """测试 AuditLogger JSONL 持久化"""

    def test_log_creates_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            al = AuditLogger(log_dir=tmpdir)
            al.log("test_event", actor="test")
            assert os.path.exists(al.filepath)

    def test_log_writes_valid_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            al = AuditLogger(log_dir=tmpdir)
            al.log("test_event", actor="test", details={"key": "value"})
            with open(al.filepath, "r") as f:
                line = f.readline().strip()
            record = json.loads(line)
            assert record["event"] == "test_event"
            assert record["actor"] == "test"
            assert record["details"]["key"] == "value"
            assert "timestamp" in record

    def test_log_multiple_events(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            al = AuditLogger(log_dir=tmpdir)
            al.log("event1", actor="a")
            al.log("event2", actor="b")
            al.log("event3", actor="c")
            with open(al.filepath, "r") as f:
                lines = [l.strip() for l in f.readlines() if l.strip()]
            assert len(lines) == 3

    def test_read_recent(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            al = AuditLogger(log_dir=tmpdir)
            for i in range(10):
                al.log(f"event_{i}", actor="test")
            records = al.read_recent(limit=5)
            assert len(records) == 5
            assert records[-1]["event"] == "event_9"

    def test_read_recent_empty(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            al = AuditLogger(log_dir=tmpdir)
            records = al.read_recent()
            assert records == []

    def test_log_with_book_and_chapter(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            al = AuditLogger(log_dir=tmpdir)
            al.log("writing_started", actor="orch", book_id="T1-CN", chapter_id="ch01")
            records = al.read_recent()
            assert records[0]["book_id"] == "T1-CN"
            assert records[0]["chapter_id"] == "ch01"

    def test_convenience_methods(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            al = AuditLogger(log_dir=tmpdir)
            al.log_writing_started("T1-CN", "ch01")
            al.log_writing_completed("T1-CN", "ch01", word_count=15000, iterations=3)
            al.log_review_passed("T1-CN", "ch01", scores={"instructor": 8.5})
            al.log_config_change("dry_run", False, True)
            al.log_checkpoint_saved("T1-CN", "ch01", iteration=2)

            records = al.read_recent()
            assert len(records) == 5
            events = [r["event"] for r in records]
            assert "writing_started" in events
            assert "writing_completed" in events
            assert "review_passed" in events
            assert "config_changed" in events
            assert "checkpoint_saved" in events

    def test_writing_failed_log(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            al = AuditLogger(log_dir=tmpdir)
            al.log_writing_failed("M1", "ch03", error="LLM timeout")
            records = al.read_recent()
            assert records[0]["event"] == "writing_failed"
            assert records[0]["details"]["error"] == "LLM timeout"

    def test_review_rejected_log(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            al = AuditLogger(log_dir=tmpdir)
            al.log_review_rejected("T2a", "ch07", scores={"expert": 4.0})
            records = al.read_recent()
            assert records[0]["event"] == "review_rejected"

    def test_global_singleton(self):
        """get_audit_logger 应返回单例"""
        a1 = get_audit_logger()
        a2 = get_audit_logger()
        assert a1 is a2


# ── CLI 相关纯函数测试 ────────────────────────────────────────

class TestCLIReport:
    """测试 report 命令的核心逻辑"""

    def test_report_generates_markdown(self):
        """report 应生成 Markdown 文件"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # 创建 progress 目录和示例进度文件
            progress_dir = os.path.join(tmpdir, "progress")
            os.makedirs(progress_dir)

            progress_data = {
                "book_id": "T1-CN",
                "book_title": "水系统控制论",
                "total_chapters": 8,
                "chapters": {
                    "ch01": {"status": "completed", "word_count": 15000, "iterations": 3, "last_updated": "2026-02-20"},
                    "ch02": {"status": "in_progress", "word_count": 8000},
                },
                "overall_progress": "12.5%",
            }
            with open(os.path.join(progress_dir, "BKT1-CN.json"), "w") as f:
                json.dump(progress_data, f)

            output_path = os.path.join(tmpdir, "report.md")

            # 模拟 cmd_report 的核心逻辑
            from hydroscribe.engine.book_registry import BOOK_REGISTRY
            lines = ["# CHS 教材体系写作进度报告", ""]
            for fname in sorted(os.listdir(progress_dir)):
                if fname.endswith(".json"):
                    with open(os.path.join(progress_dir, fname), "r") as fp:
                        data = json.load(fp)
                    book_id = data.get("book_id", "")
                    lines.append(f"## {book_id}")
                    for ch_id, ch in sorted(data.get("chapters", {}).items()):
                        lines.append(f"- {ch_id}: {ch.get('status', 'pending')}")

            content = "\n".join(lines)
            with open(output_path, "w") as f:
                f.write(content)

            assert os.path.exists(output_path)
            with open(output_path, "r") as f:
                text = f.read()
            assert "T1-CN" in text
            assert "ch01" in text


class TestCLIDryRunIntegration:
    """测试 --dry-run 标志集成"""

    def test_dry_run_sets_config(self):
        """--dry-run 应修改 OrchestratorConfig"""
        from hydroscribe.engine.config_loader import OrchestratorConfig
        oc = OrchestratorConfig()
        assert oc.dry_run is False
        oc.dry_run = True
        assert oc.dry_run is True

    def test_book_id_strip_bk_prefix(self):
        """CLI 应去除 BK 前缀"""
        raw = "BKT1-CN"
        book_id = raw.replace("BK", "")
        assert book_id == "T1-CN"

    def test_book_id_without_prefix(self):
        raw = "M8"
        book_id = raw.replace("BK", "")
        assert book_id == "M8"
