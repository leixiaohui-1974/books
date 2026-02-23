"""
审计日志 — 关键事件持久化到 JSONL 文件

记录写作启动/完成/失败、评审通过/拒绝、配置变更等关键操作，
用于事后追溯和合规审计。
"""

import json
import logging
import os
import threading
from datetime import datetime, timezone
from typing import Any, Dict, Optional

logger = logging.getLogger("hydroscribe.audit")


class AuditLogger:
    """
    JSONL 审计日志记录器

    每条审计记录为一行 JSON，包含:
    - timestamp: ISO 8601 时间戳
    - event: 事件类型
    - actor: 操作者 (agent 名称 / "cli" / "api")
    - book_id: 相关书目 (可选)
    - chapter_id: 相关章节 (可选)
    - details: 事件详情字典
    """

    def __init__(self, log_dir: str = "logs", filename: str = "audit.jsonl"):
        self._log_dir = log_dir
        self._filepath = os.path.join(log_dir, filename)
        self._lock = threading.Lock()
        os.makedirs(log_dir, exist_ok=True)

    @property
    def filepath(self) -> str:
        return self._filepath

    def log(
        self,
        event: str,
        actor: str = "system",
        book_id: Optional[str] = None,
        chapter_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        """写入一条审计记录"""
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": event,
            "actor": actor,
        }
        if book_id:
            record["book_id"] = book_id
        if chapter_id:
            record["chapter_id"] = chapter_id
        if details:
            record["details"] = details

        line = json.dumps(record, ensure_ascii=False, default=str)

        with self._lock:
            try:
                with open(self._filepath, "a", encoding="utf-8") as f:
                    f.write(line + "\n")
            except Exception as e:
                logger.error(f"审计日志写入失败: {e}")

    def read_recent(self, limit: int = 50) -> list:
        """读取最近 N 条审计记录"""
        if not os.path.exists(self._filepath):
            return []
        try:
            with open(self._filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()
            records = []
            for line in lines[-limit:]:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
            return records
        except Exception as e:
            logger.error(f"审计日志读取失败: {e}")
            return []

    # ── 便捷方法 ──

    def log_writing_started(self, book_id: str, chapter_id: str, actor: str = "orchestrator"):
        self.log("writing_started", actor=actor, book_id=book_id, chapter_id=chapter_id)

    def log_writing_completed(self, book_id: str, chapter_id: str, word_count: int = 0, iterations: int = 0):
        self.log(
            "writing_completed",
            actor="orchestrator",
            book_id=book_id,
            chapter_id=chapter_id,
            details={"word_count": word_count, "iterations": iterations},
        )

    def log_writing_failed(self, book_id: str, chapter_id: str, error: str = ""):
        self.log(
            "writing_failed",
            actor="orchestrator",
            book_id=book_id,
            chapter_id=chapter_id,
            details={"error": error},
        )

    def log_review_passed(self, book_id: str, chapter_id: str, scores: Optional[Dict] = None):
        self.log(
            "review_passed",
            actor="orchestrator",
            book_id=book_id,
            chapter_id=chapter_id,
            details={"scores": scores or {}},
        )

    def log_review_rejected(self, book_id: str, chapter_id: str, scores: Optional[Dict] = None):
        self.log(
            "review_rejected",
            actor="orchestrator",
            book_id=book_id,
            chapter_id=chapter_id,
            details={"scores": scores or {}},
        )

    def log_config_change(self, field: str, old_value: Any, new_value: Any, actor: str = "cli"):
        self.log(
            "config_changed",
            actor=actor,
            details={"field": field, "old": old_value, "new": new_value},
        )

    def log_checkpoint_saved(self, book_id: str, chapter_id: str, iteration: int):
        self.log(
            "checkpoint_saved",
            actor="orchestrator",
            book_id=book_id,
            chapter_id=chapter_id,
            details={"iteration": iteration},
        )


# ── 全局单例 ──

_global_audit: Optional[AuditLogger] = None


def get_audit_logger(log_dir: str = "logs") -> AuditLogger:
    """获取全局审计日志单例"""
    global _global_audit
    if _global_audit is None:
        _global_audit = AuditLogger(log_dir=log_dir)
    return _global_audit
