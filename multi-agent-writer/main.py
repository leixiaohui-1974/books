#!/usr/bin/env python3
"""
HydroScribe — CHS 多智能体协同写作助手
入口文件：启动 FastAPI 服务 (v0.3.0)

推荐用法：
    hydroscribe serve             # 使用 CLI (推荐)
    hydroscribe init              # 首次配置向导

兼容用法：
    python main.py                # 默认 8000 端口
    python main.py --port 3000    # 自定义端口
    python main.py --dev          # 开发模式（热重载）

访问：
    前端仪表盘: http://localhost:8000
    API 文档:    http://localhost:8000/docs
    WebSocket:   ws://localhost:8000/ws
"""

import argparse
import logging
import sys
import os

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)


def main():
    parser = argparse.ArgumentParser(description="HydroScribe — CHS 多智能体协同写作助手 v0.3.0")
    parser.add_argument("--port", "-p", type=int, default=None, help="服务端口 (默认: 8000)")
    parser.add_argument("--host", "-H", type=str, default=None, help="绑定地址 (默认: 0.0.0.0)")
    parser.add_argument("--dev", action="store_true", help="开发模式（热重载）")
    args = parser.parse_args()

    # 使用配置系统加载设置
    from hydroscribe.engine.config_loader import get_config
    cfg = get_config()

    host = args.host or cfg.server.host
    port = args.port or cfg.server.port

    import uvicorn

    print(f"""
    ╔═══════════════════════════════════════════════════════╗
    ║    HydroScribe v0.3.0 — CHS 多智能体协同写作助手     ║
    ║                                                       ║
    ║  前端仪表盘: http://localhost:{port:<5}                 ║
    ║  API  文档:  http://localhost:{port:<5}/docs             ║
    ║  WebSocket:  ws://localhost:{port:<5}/ws                 ║
    ║                                                       ║
    ║  LLM:  {cfg.llm_default.provider + '/' + cfg.llm_default.model:<46}║
    ║  Gate: {cfg.orchestrator.gate_mode:<46}║
    ║                                                       ║
    ║  推荐使用 CLI: hydroscribe serve                      ║
    ╚═══════════════════════════════════════════════════════╝
    """)

    uvicorn.run(
        "hydroscribe.api.app:app",
        host=host,
        port=port,
        reload=args.dev,
        log_level=cfg.server.log_level,
    )


if __name__ == "__main__":
    main()
