#!/usr/bin/env python3
"""
HydroScribe — CHS 多智能体协同写作助手
入口文件：启动 FastAPI 服务

用法：
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
    parser = argparse.ArgumentParser(description="HydroScribe — CHS 多智能体协同写作助手")
    parser.add_argument("--port", "-p", type=int, default=8000, help="服务端口 (默认: 8000)")
    parser.add_argument("--host", "-H", type=str, default="0.0.0.0", help="绑定地址 (默认: 0.0.0.0)")
    parser.add_argument("--dev", action="store_true", help="开发模式（热重载）")
    args = parser.parse_args()

    import uvicorn

    print(f"""
    ╔═══════════════════════════════════════════════════════╗
    ║         HydroScribe — CHS 多智能体协同写作助手        ║
    ║                                                       ║
    ║  前端仪表盘: http://localhost:{args.port}                ║
    ║  API  文档:  http://localhost:{args.port}/docs            ║
    ║  WebSocket:  ws://localhost:{args.port}/ws                ║
    ║                                                       ║
    ║  基于 OpenManus 架构 | 融合 9 大写作技能              ║
    ║  9 Writer + N Reviewer + EventBus + 实时 UI           ║
    ╚═══════════════════════════════════════════════════════╝
    """)

    uvicorn.run(
        "hydroscribe.api.app:app",
        host=args.host,
        port=args.port,
        reload=args.dev,
        log_level="info",
    )


if __name__ == "__main__":
    main()
