# HydroScribe — CHS 多智能体协同写作助手
# =========================================
# make help     显示所有命令
# make init     首次配置
# make serve    启动服务
# make test     运行测试

.PHONY: help init serve start test check doctor config clean \
        docker-build docker-up docker-down docker-logs lint fmt \
        install install-dev install-all

# ── 默认目标 ──────────────────────────────────────────
help:  ## 显示所有可用命令
	@echo ""
	@echo "  HydroScribe — CHS 多智能体协同写作助手"
	@echo "  ========================================"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'
	@echo ""

# ── 安装 ──────────────────────────────────────────────
install:  ## 安装核心依赖 (pip)
	pip install -e .

install-dev:  ## 安装开发依赖 (pytest, etc.)
	pip install -e ".[dev]"

install-all:  ## 安装全部依赖 (含百炼 SDK)
	pip install -e ".[dev,bailian]"

# ── 初始化与配置 ──────────────────────────────────────
init:  ## 交互式初始化向导 (首次使用)
	python -m hydroscribe.cli init

doctor:  ## 环境自诊断
	python -m hydroscribe.cli doctor

config:  ## 显示当前配置 (脱敏)
	python -m hydroscribe.cli config

# ── 启动服务 ──────────────────────────────────────────
serve:  ## 启动 Web 服务器 + 仪表盘 (http://localhost:8000)
	python -m hydroscribe.cli serve

serve-dev:  ## 启动开发服务器 (热重载)
	python -m hydroscribe.cli serve --reload

start:  ## 启动写作任务 (用法: make start BOOK=T1-CN)
	@if [ -z "$(BOOK)" ]; then \
		echo "用法: make start BOOK=T1-CN [SKILL=BK] [CHAPTERS=ch01,ch02]"; \
		exit 1; \
	fi
	python -m hydroscribe.cli start $(BOOK) \
		$(if $(SKILL),--skill $(SKILL)) \
		$(if $(CHAPTERS),--chapters $(CHAPTERS))

status:  ## 查看所有书目进度
	python -m hydroscribe.cli status

agents:  ## 列出所有 Agent (40个)
	python -m hydroscribe.cli agents

# ── 质量检查 ──────────────────────────────────────────
check:  ## 质量检查 (用法: make check FILE=books/T2a/ch01.md)
	@if [ -z "$(FILE)" ]; then \
		echo "用法: make check FILE=path/to/chapter.md [SKILL=BK]"; \
		exit 1; \
	fi
	python -m hydroscribe.cli check $(FILE) $(if $(SKILL),--skill $(SKILL))

# ── 测试 ──────────────────────────────────────────────
test:  ## 运行全部测试
	python -m pytest tests/ -v

test-cov:  ## 运行测试 + 覆盖率报告
	python -m pytest tests/ -v --cov=hydroscribe --cov-report=term-missing

test-quick:  ## 快速运行测试 (不含慢速标记)
	python -m pytest tests/ -v -m "not slow"

# ── 代码质量 ──────────────────────────────────────────
lint:  ## 代码检查 (ruff)
	python -m ruff check hydroscribe/ tests/

fmt:  ## 代码格式化 (ruff)
	python -m ruff format hydroscribe/ tests/

# ── Docker ────────────────────────────────────────────
docker-build:  ## 构建 Docker 镜像
	docker build -t hydroscribe:latest .

docker-up:  ## 启动 Docker 容器 (后台)
	docker-compose up -d

docker-down:  ## 停止 Docker 容器
	docker-compose down

docker-logs:  ## 查看容器日志
	docker-compose logs -f hydroscribe

docker-shell:  ## 进入容器 Shell
	docker-compose exec hydroscribe /bin/bash

# ── 清理 ──────────────────────────────────────────────
clean:  ## 清理生成的文件
	rm -rf __pycache__ .pytest_cache .ruff_cache htmlcov .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

clean-all: clean  ## 清理全部 (含 output/ 和 logs/)
	rm -rf output/ logs/
