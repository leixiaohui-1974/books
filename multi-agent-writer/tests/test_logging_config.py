"""
测试结构化日志系统
"""

import json
import logging
import os
import tempfile

import pytest

from hydroscribe.engine.logging_config import (
    JSONFormatter, ConsoleFormatter, LogContext, setup_logging
)


class TestJSONFormatter:
    def test_basic_format(self):
        fmt = JSONFormatter()
        record = logging.LogRecord(
            name="hydroscribe.test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="测试日志消息",
            args=(),
            exc_info=None,
        )
        output = fmt.format(record)
        data = json.loads(output)
        assert data["level"] == "INFO"
        assert data["logger"] == "hydroscribe.test"
        assert data["msg"] == "测试日志消息"
        assert "ts" in data

    def test_extra_fields(self):
        fmt = JSONFormatter()
        record = logging.LogRecord(
            name="hydroscribe.llm",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="LLM 调用",
            args=(),
            exc_info=None,
        )
        record.book_id = "T2a"
        record.tokens = 1500
        record.model = "qwen-plus"

        output = fmt.format(record)
        data = json.loads(output)
        assert data["book_id"] == "T2a"
        assert data["tokens"] == 1500
        assert data["model"] == "qwen-plus"

    def test_exception_format(self):
        fmt = JSONFormatter()
        try:
            raise ValueError("测试异常")
        except ValueError:
            import sys
            record = logging.LogRecord(
                name="test",
                level=logging.ERROR,
                pathname="",
                lineno=0,
                msg="出错了",
                args=(),
                exc_info=sys.exc_info(),
            )
        output = fmt.format(record)
        data = json.loads(output)
        assert "exception" in data
        assert "ValueError" in data["exception"]


class TestConsoleFormatter:
    def test_basic_format(self):
        fmt = ConsoleFormatter()
        record = logging.LogRecord(
            name="hydroscribe.orchestrator",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="启动写作",
            args=(),
            exc_info=None,
        )
        output = fmt.format(record)
        assert "hs.orchestrator" in output
        assert "启动写作" in output

    def test_with_extras(self):
        fmt = ConsoleFormatter()
        record = logging.LogRecord(
            name="hydroscribe.writer",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="写作中",
            args=(),
            exc_info=None,
        )
        record.book_id = "T1-CN"
        record.agent = "writer-bk"

        output = fmt.format(record)
        assert "book_id=T1-CN" in output
        assert "agent=writer-bk" in output


class TestSetupLogging:
    def test_setup_default(self):
        setup_logging(log_level="info")
        root = logging.getLogger()
        assert root.level == logging.INFO

    def test_setup_with_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            setup_logging(log_level="debug", log_dir=tmpdir)

            # 检查日志文件被创建
            logger = logging.getLogger("hydroscribe.test_file")
            logger.info("测试文件日志")

            log_file = os.path.join(tmpdir, "hydroscribe.log")
            assert os.path.exists(log_file)

    def test_setup_json_mode(self):
        setup_logging(log_level="info", json_format=True)
        root = logging.getLogger()
        # 应该有至少一个 handler 使用 JSONFormatter
        has_json = any(
            isinstance(h.formatter, JSONFormatter)
            for h in root.handlers
        )
        assert has_json

    def test_setup_quiet_mode(self):
        setup_logging(log_level="info", quiet=True)
        root = logging.getLogger()
        # quiet 模式不应该有 StreamHandler (除了文件 handler)
        stream_handlers = [
            h for h in root.handlers
            if isinstance(h, logging.StreamHandler)
            and not isinstance(h, logging.handlers.RotatingFileHandler)
        ]
        assert len(stream_handlers) == 0


class TestLogContext:
    def test_context_info(self):
        logger = logging.getLogger("hydroscribe.test_ctx")
        logger.setLevel(logging.DEBUG)

        # 添加一个捕获 handler
        records = []

        class CaptureHandler(logging.Handler):
            def emit(self, record):
                records.append(record)

        handler = CaptureHandler()
        logger.addHandler(handler)

        ctx = LogContext(logger, book_id="T2a", agent="writer-bk")
        ctx.info("开始写作")

        assert len(records) == 1
        assert records[0].book_id == "T2a"
        assert records[0].agent == "writer-bk"

        logger.removeHandler(handler)
