"""
HydroScribe 结构化日志系统

特性：
- JSON 格式输出（生产环境）或 Rich 彩色输出（开发环境）
- 自动日志轮转（10MB × 5 文件）
- 按模块分级别控制
- LLM 调用专用日志（token 用量追踪）
"""

import json
import logging
import logging.handlers
import os
import sys
from datetime import datetime
from typing import Optional


class JSONFormatter(logging.Formatter):
    """JSON 格式化器 — 生产环境使用"""

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "ts": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }

        if record.exc_info and record.exc_info[0]:
            log_data["exception"] = self.formatException(record.exc_info)

        # 附加上下文字段
        for key in ("book_id", "chapter_id", "agent", "task_id",
                     "tokens", "model", "duration_ms"):
            if hasattr(record, key):
                log_data[key] = getattr(record, key)

        return json.dumps(log_data, ensure_ascii=False, default=str)


class ConsoleFormatter(logging.Formatter):
    """彩色控制台格式化器 — 开发环境使用"""

    COLORS = {
        "DEBUG": "\033[36m",     # cyan
        "INFO": "\033[32m",      # green
        "WARNING": "\033[33m",   # yellow
        "ERROR": "\033[31m",     # red
        "CRITICAL": "\033[35m",  # magenta
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, "")
        timestamp = datetime.fromtimestamp(record.created).strftime("%H:%M:%S")
        name_short = record.name.replace("hydroscribe.", "hs.")

        msg = f"{color}{timestamp} [{name_short}] {record.levelname}: {record.getMessage()}{self.RESET}"

        # 附加上下文
        extras = []
        for key in ("book_id", "chapter_id", "agent", "tokens"):
            if hasattr(record, key):
                extras.append(f"{key}={getattr(record, key)}")
        if extras:
            msg += f" ({', '.join(extras)})"

        if record.exc_info and record.exc_info[0]:
            msg += "\n" + self.formatException(record.exc_info)

        return msg


def setup_logging(
    log_level: str = "info",
    log_dir: Optional[str] = None,
    json_format: bool = False,
    quiet: bool = False,
):
    """
    配置 HydroScribe 日志系统

    Args:
        log_level: 日志级别 (debug/info/warning/error)
        log_dir: 日志文件目录（None 则不写文件）
        json_format: 是否使用 JSON 格式（生产环境推荐）
        quiet: 是否静默控制台输出
    """
    level = getattr(logging, log_level.upper(), logging.INFO)

    # 根 logger
    root = logging.getLogger()
    root.setLevel(level)

    # 清除已有 handler
    root.handlers.clear()

    # 控制台输出
    if not quiet:
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setLevel(level)

        if json_format:
            console_handler.setFormatter(JSONFormatter())
        else:
            console_handler.setFormatter(ConsoleFormatter())

        root.addHandler(console_handler)

    # 文件输出（带轮转）
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

        # 主日志文件
        main_handler = logging.handlers.RotatingFileHandler(
            os.path.join(log_dir, "hydroscribe.log"),
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding="utf-8",
        )
        main_handler.setLevel(level)
        main_handler.setFormatter(JSONFormatter())
        root.addHandler(main_handler)

        # 错误日志单独文件
        error_handler = logging.handlers.RotatingFileHandler(
            os.path.join(log_dir, "error.log"),
            maxBytes=5 * 1024 * 1024,
            backupCount=3,
            encoding="utf-8",
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(JSONFormatter())
        root.addHandler(error_handler)

        # LLM 调用日志
        llm_handler = logging.handlers.RotatingFileHandler(
            os.path.join(log_dir, "llm_calls.log"),
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8",
        )
        llm_handler.setLevel(logging.DEBUG)
        llm_handler.setFormatter(JSONFormatter())
        llm_logger = logging.getLogger("hydroscribe.llm")
        llm_logger.addHandler(llm_handler)

    # 第三方库日志级别调低
    for lib in ("uvicorn", "uvicorn.access", "fastapi", "httpx", "httpcore", "openai"):
        logging.getLogger(lib).setLevel(max(level, logging.WARNING))


class LogContext:
    """日志上下文管理器 — 为日志记录附加额外字段"""

    def __init__(self, logger: logging.Logger, **kwargs):
        self.logger = logger
        self.extra = kwargs

    def _log(self, level: int, msg: str, **extra):
        merged = {**self.extra, **extra}
        self.logger.log(level, msg, extra=merged)

    def debug(self, msg: str, **extra):
        record = self.logger.makeRecord(
            self.logger.name, logging.DEBUG, "", 0, msg, (), None
        )
        for k, v in {**self.extra, **extra}.items():
            setattr(record, k, v)
        self.logger.handle(record)

    def info(self, msg: str, **extra):
        record = self.logger.makeRecord(
            self.logger.name, logging.INFO, "", 0, msg, (), None
        )
        for k, v in {**self.extra, **extra}.items():
            setattr(record, k, v)
        self.logger.handle(record)

    def warning(self, msg: str, **extra):
        record = self.logger.makeRecord(
            self.logger.name, logging.WARNING, "", 0, msg, (), None
        )
        for k, v in {**self.extra, **extra}.items():
            setattr(record, k, v)
        self.logger.handle(record)

    def error(self, msg: str, **extra):
        record = self.logger.makeRecord(
            self.logger.name, logging.ERROR, "", 0, msg, (), None
        )
        for k, v in {**self.extra, **extra}.items():
            setattr(record, k, v)
        self.logger.handle(record)
