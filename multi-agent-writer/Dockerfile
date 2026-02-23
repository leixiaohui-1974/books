# HydroScribe — CHS 多智能体协同写作助手
# 多阶段构建，最终镜像基于 python:3.12-slim

# ── 第一阶段：安装依赖 ────────────────────────────────────────────
FROM python:3.12-slim-bookworm AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
COPY hydroscribe/ ./hydroscribe/
COPY openmanus/ ./openmanus/

RUN pip install --no-cache-dir --prefix=/install .

# ── 第二阶段：运行镜像 ────────────────────────────────────────────
FROM python:3.12-slim-bookworm

LABEL maintainer="CHS Writing System"
LABEL description="HydroScribe - CHS 多智能体协同写作助手 (OpenManus + OpenClaw)"

WORKDIR /app

COPY --from=builder /install /usr/local

COPY hydroscribe/ ./hydroscribe/
COPY openmanus/ ./openmanus/
COPY config/ ./config/
COPY main.py .

RUN mkdir -p /app/data /app/output /app/logs

ENV PYTHONPATH="/app:/app/openmanus" \
    PYTHONUNBUFFERED=1 \
    HYDROSCRIBE_SERVER_HOST="0.0.0.0" \
    HYDROSCRIBE_SERVER_PORT="8000" \
    BOOKS_ROOT="/data/books"

VOLUME ["/data/books", "/app/config", "/app/output"]

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import httpx; r = httpx.get('http://localhost:8000/api/status'); r.raise_for_status()" || exit 1

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "hydroscribe.api.app:app", \
     "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"]
