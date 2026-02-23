"""
HydroScribe CLI — 命令行入口 (v0.3.0)

用法:
    hydroscribe init                # 交互式初始化向导
    hydroscribe serve               # 启动 Web 服务器 + 仪表盘
    hydroscribe start T2a           # 启动 T2a 的写作
    hydroscribe start T2a --chapters ch01,ch02,ch03  # 并行写多章
    hydroscribe status              # 查看所有书目进度
    hydroscribe check <file>        # 对文件执行术语/一致性/参考文献检查
    hydroscribe agents              # 列出所有 Agent
    hydroscribe doctor              # 环境自诊断
    hydroscribe config              # 显示当前配置
"""

import argparse
import asyncio
import json
import os
import shutil
import sys
from typing import Optional

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.tree import Tree
from rich.text import Text
from rich import box

console = Console()

BANNER = """[bold blue]
 ╦ ╦┬ ┬┌┬┐┬─┐┌─┐╔═╗┌─┐┬─┐┬┌┐ ┌─┐
 ╠═╣└┬┘ ││├┬┘│ │╚═╗│  ├┬┘│├┴┐├┤
 ╩ ╩ ┴ ─┴┘┴└─└─┘╚═╝└─┘┴└─┴└─┘└─┘[/]
[dim]CHS 多智能体协同写作助手 v0.3.0[/]
[dim]OpenManus + OpenClaw | 百炼/OpenAI/Anthropic/Local[/]
"""


# ── init — 交互式初始化向导 ─────────────────────────────────────

def cmd_init(args):
    """交互式初始化向导 — 引导用户完成首次配置"""
    console.print(BANNER)
    console.print(Panel(
        "[bold]欢迎使用 HydroScribe 初始化向导[/]\n"
        "本向导将帮助您完成配置，只需 3 步：\n"
        "  1. 选择 LLM 提供商并配置 API Key\n"
        "  2. 设置数据目录\n"
        "  3. 生成配置文件",
        title="Step 0/3",
        border_style="blue",
    ))

    # Step 1: LLM 提供商
    console.print("\n[bold]Step 1/3: 选择 LLM 提供商[/]")
    console.print("  [1] 阿里云百炼 (推荐，国内低延迟)")
    console.print("  [2] OpenAI (GPT-4o)")
    console.print("  [3] Anthropic Claude")
    console.print("  [4] 本地模型 (Ollama/vLLM)")

    choice = Prompt.ask("请选择", choices=["1", "2", "3", "4"], default="1")

    provider_map = {
        "1": ("alibaba_bailian", "qwen-plus", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
        "2": ("openai", "gpt-4o", ""),
        "3": ("anthropic", "claude-sonnet-4-20250514", ""),
        "4": ("local", "qwen2.5:14b", "http://localhost:11434/v1"),
    }
    provider, default_model, default_url = provider_map[choice]

    model = Prompt.ask("模型名称", default=default_model)

    api_key = ""
    if choice != "4":
        key_env = {
            "1": "DASHSCOPE_API_KEY",
            "2": "OPENAI_API_KEY",
            "3": "ANTHROPIC_API_KEY",
        }.get(choice, "")

        existing_key = os.environ.get(key_env, "")
        if existing_key:
            console.print(f"  [green]已检测到环境变量 {key_env}[/]")
            api_key = existing_key
        else:
            api_key = Prompt.ask(f"API Key (或稍后设置环境变量 {key_env})", default="", password=True)

    base_url = default_url
    if choice == "4":
        base_url = Prompt.ask("本地模型 API 地址", default=default_url)

    # Step 2: 数据目录
    console.print("\n[bold]Step 2/3: 数据目录配置[/]")
    default_books_root = os.environ.get("BOOKS_ROOT", "/home/user/books")
    books_root = Prompt.ask("书稿数据根目录", default=default_books_root)

    # Step 3: 生成配置
    console.print("\n[bold]Step 3/3: 生成配置文件[/]")

    config_dir = os.path.join(os.getcwd(), "config")
    os.makedirs(config_dir, exist_ok=True)
    config_path = os.path.join(config_dir, "config.toml")

    # 如果已存在，询问是否覆盖
    if os.path.exists(config_path):
        if not Confirm.ask(f"  配置文件 {config_path} 已存在，是否覆盖?", default=False):
            console.print("  [yellow]跳过配置文件生成[/]")
            _init_directories(books_root)
            _print_init_summary(provider, model, books_root, config_path)
            return

    config_content = f'''# HydroScribe 配置文件 (自动生成)
# 生成时间: {__import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M")}

books_root = "{books_root}"
log_level = "info"

[server]
host = "0.0.0.0"
port = 8000

[orchestrator]
gate_mode = "auto"
coordination_mode = "specialist"
max_concurrent_writers = 3

[llm]
provider = "{provider}"
model = "{model}"
api_key = "{api_key}"
base_url = "{base_url}"
max_tokens = 4096
temperature = 0.3
max_retries = 3
fallback_model = "{_get_fallback_model(provider, model)}"

[openclaw]
enabled = false
'''

    with open(config_path, "w", encoding="utf-8") as f:
        f.write(config_content)
    console.print(f"  [green]配置文件已生成: {config_path}[/]")

    # 生成 .env
    env_path = os.path.join(os.getcwd(), ".env")
    if not os.path.exists(env_path):
        env_var = {"alibaba_bailian": "DASHSCOPE_API_KEY", "openai": "LLM_API_KEY", "anthropic": "LLM_API_KEY"}.get(provider, "LLM_API_KEY")
        with open(env_path, "w") as f:
            f.write(f"# HydroScribe 环境变量\n{env_var}={api_key}\nLLM_PROVIDER={provider}\nLLM_MODEL={model}\n")
        console.print(f"  [green].env 文件已生成: {env_path}[/]")

    _init_directories(books_root)
    _print_init_summary(provider, model, books_root, config_path)


def _get_fallback_model(provider: str, model: str) -> str:
    fallbacks = {
        "alibaba_bailian": "qwen-turbo",
        "openai": "gpt-4o-mini",
        "anthropic": "claude-haiku-4-5-20251001",
        "local": model,
    }
    return fallbacks.get(provider, "")


def _init_directories(books_root: str):
    """确保必要的目录结构存在"""
    dirs = [
        os.path.join(books_root, "progress"),
        os.path.join(books_root, "books"),
        os.path.join(books_root, "terminology"),
        os.path.join(books_root, "reviews"),
        os.path.join(books_root, "references"),
        os.path.join(books_root, "figures", "generated"),
        "output",
        "logs",
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    console.print("  [green]目录结构已就绪[/]")


def _print_init_summary(provider, model, books_root, config_path):
    console.print(Panel(
        f"[bold green]初始化完成![/]\n\n"
        f"  LLM 提供商: [bold]{provider}[/]\n"
        f"  模型:       [bold]{model}[/]\n"
        f"  数据目录:   [bold]{books_root}[/]\n"
        f"  配置文件:   [bold]{config_path}[/]\n\n"
        f"[bold]下一步:[/]\n"
        f"  [cyan]hydroscribe serve[/]        启动服务 (浏览器访问 http://localhost:8000)\n"
        f"  [cyan]hydroscribe doctor[/]       检查环境是否就绪\n"
        f"  [cyan]hydroscribe start T1-CN[/]  开始写作第一本书",
        title="Ready!",
        border_style="green",
    ))


# ── doctor — 环境自诊断 ────────────────────────────────────────

def cmd_doctor(args):
    """环境自诊断 — 检查所有依赖和配置"""
    console.print(BANNER)
    console.print("[bold]Running HydroScribe Doctor...[/]\n")

    checks_passed = 0
    checks_total = 0

    def _check(name: str, test_fn, fix_hint: str = ""):
        nonlocal checks_passed, checks_total
        checks_total += 1
        try:
            result = test_fn()
            if result:
                console.print(f"  [green]PASS[/] {name}")
                checks_passed += 1
                return True
            else:
                console.print(f"  [red]FAIL[/] {name}")
                if fix_hint:
                    console.print(f"        [dim]{fix_hint}[/]")
                return False
        except Exception as e:
            console.print(f"  [red]FAIL[/] {name}: {e}")
            if fix_hint:
                console.print(f"        [dim]{fix_hint}[/]")
            return False

    # Python 版本
    _check(
        f"Python >= 3.10 (当前 {sys.version.split()[0]})",
        lambda: sys.version_info >= (3, 10),
        "需要 Python 3.10+: https://python.org",
    )

    # 核心依赖
    for pkg, name in [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("pydantic", "Pydantic"),
        ("rich", "Rich"),
        ("openai", "OpenAI SDK"),
        ("httpx", "HTTPX"),
    ]:
        _check(
            f"{name} 已安装",
            lambda p=pkg: __import__(p),
            f"pip install {pkg}",
        )

    # 可选依赖
    console.print()
    _check(
        "Anthropic SDK 已安装 (可选)",
        lambda: __import__("anthropic"),
        "pip install anthropic  (如需使用 Claude)",
    )

    # TOML 解析
    _check(
        "TOML 解析可用",
        lambda: __import__("tomllib") if sys.version_info >= (3, 11) else __import__("tomli"),
        "pip install tomli  (Python < 3.11)",
    )

    # 配置文件
    console.print()
    config_path = os.path.join(os.getcwd(), "config", "config.toml")
    _check(
        f"配置文件存在 ({config_path})",
        lambda: os.path.exists(config_path),
        "运行 hydroscribe init 生成配置",
    )

    # LLM API Key
    has_key = False
    for env_var in ("DASHSCOPE_API_KEY", "HYDROSCRIBE_LLM_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY"):
        if os.environ.get(env_var):
            has_key = True
            break
    if not has_key and os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                content = f.read()
            if 'api_key = "sk-' in content or "api_key = 'sk-" in content:
                has_key = True
        except Exception:
            pass

    _check(
        "LLM API Key 已配置",
        lambda: has_key,
        "设置环境变量 DASHSCOPE_API_KEY 或在 config.toml 中配置 api_key",
    )

    # 数据目录
    books_root = os.environ.get("BOOKS_ROOT", "/home/user/books")
    _check(
        f"数据目录可访问 ({books_root})",
        lambda: os.path.isdir(books_root),
        f"mkdir -p {books_root}  或修改 BOOKS_ROOT 环境变量",
    )

    for subdir in ("progress", "books", "terminology"):
        path = os.path.join(books_root, subdir)
        _check(
            f"  子目录 {subdir}/",
            lambda p=path: os.path.isdir(p),
            f"mkdir -p {path}",
        )

    # OpenManus
    console.print()
    openmanus_path = os.path.join(os.path.dirname(__file__), "..", "openmanus")
    _check(
        "OpenManus 源码存在",
        lambda: os.path.isdir(openmanus_path),
        "git clone https://github.com/mannaandpoem/OpenManus.git openmanus",
    )

    # Docker (可选)
    _check(
        "Docker 可用 (可选，容器化部署)",
        lambda: shutil.which("docker") is not None,
        "https://docs.docker.com/get-docker/",
    )

    # 端口检查
    import socket
    def _port_available(port=8000):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.bind(("0.0.0.0", port))
            return True
        except OSError:
            return False

    _check(
        "端口 8000 可用",
        _port_available,
        "其他进程占用了 8000 端口，使用 --port 参数指定其他端口",
    )

    # 汇总
    console.print()
    if checks_passed == checks_total:
        console.print(Panel(
            f"[bold green]全部 {checks_total} 项检查通过![/]\n"
            f"运行 [cyan]hydroscribe serve[/] 启动服务",
            border_style="green",
        ))
    else:
        failed = checks_total - checks_passed
        console.print(Panel(
            f"[yellow]{checks_passed}/{checks_total} 项通过，{failed} 项需要修复[/]\n"
            f"请根据上方提示修复后重新运行 [cyan]hydroscribe doctor[/]",
            border_style="yellow",
        ))


# ── config — 显示当前配置 ──────────────────────────────────────

def cmd_config(args):
    """显示当前配置（脱敏）"""
    from hydroscribe.engine.config_loader import get_config
    cfg = get_config()

    tree = Tree("[bold]HydroScribe 配置[/]")

    # 基础
    basic = tree.add("[bold]基础[/]")
    basic.add(f"books_root: [cyan]{cfg.books_root}[/]")
    basic.add(f"log_level: {cfg.log_level}")

    # Server
    server = tree.add("[bold]服务[/]")
    server.add(f"host: {cfg.server.host}")
    server.add(f"port: [cyan]{cfg.server.port}[/]")

    # LLM
    llm = tree.add("[bold]LLM 配置[/]")
    llm.add(f"provider: [cyan]{cfg.llm_default.provider}[/]")
    llm.add(f"model: [cyan]{cfg.llm_default.model}[/]")
    key_display = "***" + cfg.llm_default.api_key[-4:] if len(cfg.llm_default.api_key) > 4 else ("(未设置)" if not cfg.llm_default.api_key else "***")
    llm.add(f"api_key: {key_display}")
    if cfg.llm_default.base_url:
        llm.add(f"base_url: {cfg.llm_default.base_url}")
    llm.add(f"max_tokens: {cfg.llm_default.max_tokens}")
    llm.add(f"temperature: {cfg.llm_default.temperature}")
    if cfg.llm_default.fallback_model:
        llm.add(f"fallback: {cfg.llm_default.fallback_model}")

    # 角色特定 LLM
    for role, role_cfg in [("writer", cfg.llm_writer), ("reviewer", cfg.llm_reviewer), ("utility", cfg.llm_utility)]:
        if role_cfg and role_cfg.model:
            r = llm.add(f"[dim]{role}:[/] {role_cfg.provider}/{role_cfg.model}")

    # Orchestrator
    orch = tree.add("[bold]编排器[/]")
    orch.add(f"gate_mode: {cfg.orchestrator.gate_mode}")
    orch.add(f"coordination_mode: [cyan]{cfg.orchestrator.coordination_mode}[/]")
    orch.add(f"review_weight: {cfg.orchestrator.review_weight}")
    orch.add(f"utility_weight: {cfg.orchestrator.utility_weight}")
    orch.add(f"max_concurrent_writers: {cfg.orchestrator.max_concurrent_writers}")

    # OpenClaw
    oc = tree.add("[bold]OpenClaw[/]")
    oc.add(f"enabled: {'[green]Yes[/]' if cfg.openclaw_enabled else '[dim]No[/]'}")
    if cfg.openclaw_enabled:
        oc.add(f"gateway: {cfg.openclaw_gateway_url}")

    console.print(tree)


# ── serve — 启动服务 ───────────────────────────────────────────

def cmd_serve(args):
    """启动 Web 服务器"""
    import uvicorn
    from hydroscribe.engine.config_loader import get_config

    cfg = get_config()
    host = args.host or cfg.server.host
    port = args.port or cfg.server.port

    console.print(BANNER)
    console.print(Panel(
        f"  Dashboard:  [bold cyan]http://{host}:{port}/[/]\n"
        f"  API Docs:   [bold cyan]http://{host}:{port}/docs[/]\n"
        f"  WebSocket:  [bold cyan]ws://{host}:{port}/ws[/]\n\n"
        f"  LLM:        [dim]{cfg.llm_default.provider}/{cfg.llm_default.model}[/]\n"
        f"  Gate Mode:  [dim]{cfg.orchestrator.gate_mode}[/]\n"
        f"  Coord Mode: [dim]{cfg.orchestrator.coordination_mode}[/]",
        title="[bold]HydroScribe Server[/]",
        border_style="blue",
    ))

    uvicorn.run(
        "hydroscribe.api.app:app",
        host=host,
        port=port,
        reload=args.reload,
        log_level=cfg.server.log_level,
    )


# ── start — 启动写作 ──────────────────────────────────────────

def cmd_start(args):
    """启动写作任务"""
    from hydroscribe.engine.orchestrator import Orchestrator
    from hydroscribe.engine.config_loader import get_config

    cfg = get_config()
    book_id = args.book_id.replace("BK", "")
    skill_type = args.skill or "BK"
    books_root = args.books_root or cfg.books_root

    console.print(BANNER)

    orch = Orchestrator(books_root=books_root, config=cfg)

    # 并行多章模式
    if args.chapters:
        chapter_ids = [ch.strip() for ch in args.chapters.split(",")]
        console.print(Panel(
            f"  书目: [bold]{book_id}[/]\n"
            f"  技能: [bold]{skill_type}[/]\n"
            f"  模式: [bold cyan]主从并行[/] ({len(chapter_ids)} 章)\n"
            f"  章节: {', '.join(chapter_ids)}\n"
            f"  并发: {cfg.orchestrator.max_concurrent_writers}",
            title="多章并行写作",
            border_style="cyan",
        ))

        if not Confirm.ask("确认启动?", default=True):
            return

        result = asyncio.run(orch.execute_master_slave(book_id, chapter_ids, skill_type))
        _print_results(result)
        return

    # 单章模式
    console.print(Panel(
        f"  书目: [bold]{book_id}[/]\n"
        f"  技能: [bold]{skill_type}[/]\n"
        f"  模式: [bold]{cfg.orchestrator.coordination_mode}[/]\n"
        f"  LLM:  [dim]{cfg.llm_default.provider}/{cfg.llm_default.model}[/]",
        title="启动写作",
        border_style="blue",
    ))

    result = asyncio.run(orch.start_book(book_id, skill_type))
    _print_results(result)


def _print_results(result):
    if isinstance(result, dict) and result.get("status") == "completed":
        console.print(Panel(
            f"  [bold green]写作完成![/]\n"
            f"  字数: {result.get('word_count', 0)}\n"
            f"  轮次: {result.get('iterations', 0)}\n"
            f"  评分: {result.get('score', 0)}\n"
            f"  文件: {result.get('file', '')}",
            border_style="green",
        ))
    elif isinstance(result, dict) and "results" in result:
        # master_slave 模式
        table = Table(title="多章写作结果")
        table.add_column("章节")
        table.add_column("状态")
        table.add_column("字数", justify="right")
        table.add_column("评分", justify="right")
        for ch_id, ch_result in result["results"].items():
            status = ch_result.get("status", "unknown")
            style = "green" if status == "completed" else "yellow"
            table.add_row(
                ch_id,
                status,
                str(ch_result.get("word_count", "-")),
                str(ch_result.get("score", "-")),
                style=style,
            )
        console.print(table)
    else:
        console.print(f"[yellow]状态: {result.get('status', 'unknown')}[/]")
        if result.get("message"):
            console.print(f"  {result['message']}")


# ── status — 进度查看 ─────────────────────────────────────────

def cmd_status(args):
    """查看所有书目进度"""
    books_root = args.books_root or os.environ.get("BOOKS_ROOT", "/home/user/books")
    progress_dir = os.path.join(books_root, "progress")

    console.print(BANNER)

    table = Table(
        title="CHS 教材体系写作进度",
        box=box.ROUNDED,
        show_lines=True,
    )
    table.add_column("书目", style="bold", min_width=8)
    table.add_column("书名", min_width=15)
    table.add_column("进度", justify="center", min_width=8)
    table.add_column("章节", justify="center")
    table.add_column("最后更新", justify="center")

    book_titles = {
        "T1-CN": "水系统控制论",
        "T1-EN": "Cybernetics of Hydro Systems",
        "T2a": "建模与控制",
        "T2b": "智能与自主",
        "M1": "明渠水动力降阶建模",
        "M2": "水网预测控制",
        "M3": "水网运行安全包络",
        "M4": "水网多智能体系统",
        "M5": "水利认知智能",
        "M6": "水网控制在环验证",
        "M7": "HydroOS设计与实现",
        "M8": "胶东调水与沙坪水电站",
        "M9": "水系统运行工程导论",
        "M10": "水网智能控制实验",
    }

    found = False
    if os.path.exists(progress_dir):
        for f in sorted(os.listdir(progress_dir)):
            if f.endswith(".json"):
                found = True
                with open(os.path.join(progress_dir, f), "r", encoding="utf-8") as fp:
                    data = json.load(fp)

                book_id = data.get("book_id", f.replace("BK", "").replace(".json", ""))
                total = data.get("total_chapters", 0)
                chapters = data.get("chapters", {})
                completed = sum(1 for ch in chapters.values() if ch.get("status") == "completed")
                progress = data.get("overall_progress", "0%")

                last_update = ""
                for ch in chapters.values():
                    lu = ch.get("last_updated", "")
                    if lu > last_update:
                        last_update = lu

                # 进度条样式
                pct = float(progress.replace("%", "")) if "%" in progress else 0
                if pct >= 100:
                    bar = f"[bold green]{progress}[/]"
                elif pct > 0:
                    filled = int(pct / 10)
                    bar = f"[blue]{'█' * filled}{'░' * (10 - filled)}[/] {progress}"
                else:
                    bar = f"[dim]{'░' * 10} {progress}[/]"

                title = book_titles.get(book_id, data.get("book_title", ""))
                table.add_row(book_id, title, bar, f"{completed}/{total}", last_update or "-")

    if not found:
        table.add_row("[dim]暂无进度数据[/]", "", "", "", "")
        console.print(table)
        console.print("\n[dim]提示: 使用 hydroscribe start T1-CN 开始写作第一本书[/]")
    else:
        console.print(table)


# ── check — 质量检查 ──────────────────────────────────────────

def cmd_check(args):
    """对文件执行质量检查"""
    filepath = args.file
    if not os.path.exists(filepath):
        console.print(f"[red]文件不存在: {filepath}[/]")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    console.print(f"[bold]检查文件[/]: {filepath} ({len(content)}字)\n")

    from hydroscribe.tools.quality_tools import (
        CheckGlossaryTool, CheckConsistencyTool, CheckReferenceTool, CheckStructureTool
    )

    results = []

    # 术语检查
    with console.status("[bold]检查术语一致性...[/]"):
        glossary_result = CheckGlossaryTool().execute(content)
    status = "[green]PASS[/]" if glossary_result["passed"] else "[red]FAIL[/]"
    console.print(f"  {status}  术语一致性  ({glossary_result['score']}/10)")
    for alias in glossary_result.get("forbidden_aliases", [])[:5]:
        console.print(f"       [red]禁止[/]: '{alias['alias']}' -> '{alias['correct']}' (x{alias['count']})")
    results.append(glossary_result["score"])

    # 一致性检查
    with console.status("[bold]检查跨书一致性...[/]"):
        consistency_result = CheckConsistencyTool().execute(content)
    status = "[green]PASS[/]" if consistency_result["passed"] else "[red]FAIL[/]"
    console.print(f"  {status}  跨书一致性  ({consistency_result['score']}/10)")
    for issue in consistency_result.get("issues", [])[:3]:
        color = "red" if issue["severity"] == "red" else "yellow"
        console.print(f"       [{color}]{issue['message']}[/]")
    results.append(consistency_result["score"])

    # 参考文献检查
    with console.status("[bold]检查参考文献...[/]"):
        ref_result = CheckReferenceTool().execute(content, args.skill or "BK")
    status = "[green]PASS[/]" if ref_result["passed"] else "[red]FAIL[/]"
    console.print(f"  {status}  参考文献    ({ref_result['score']}/10)")
    console.print(f"       总引用: {ref_result['total_references']}篇  自引率: {ref_result['self_citation_rate']:.1%}  近5年: {ref_result['recent_rate']:.1%}")
    results.append(ref_result["score"])

    # 结构检查
    with console.status("[bold]检查结构完整性...[/]"):
        struct_result = CheckStructureTool().execute(content, args.book_type or "textbook")
    status = "[green]PASS[/]" if struct_result["passed"] else "[red]FAIL[/]"
    console.print(f"  {status}  结构完整性  ({struct_result['score']}/10  通过: {struct_result['passed_count']}/{struct_result['total_checks']})")
    results.append(struct_result["score"])

    # 总分
    avg = sum(results) / len(results)
    color = "green" if avg >= 8 else "yellow" if avg >= 6 else "red"
    console.print(f"\n  [{color}]综合质检分: {avg:.1f}/10[/]")


# ── agents — Agent 清单 ───────────────────────────────────────

def cmd_agents(args):
    """列出所有 Agent"""
    from hydroscribe.agents.writers import WRITER_REGISTRY
    from hydroscribe.schema import SKILL_REVIEWERS
    from hydroscribe.engine.orchestrator import REVIEWER_WEIGHTS

    console.print(BANNER)

    table = Table(
        title="HydroScribe Agent Registry",
        box=box.ROUNDED,
    )
    table.add_column("类型", style="bold", min_width=8)
    table.add_column("技能", min_width=8)
    table.add_column("角色/名称", min_width=16)
    table.add_column("权重", justify="right", min_width=6)

    for skill, cls in WRITER_REGISTRY.items():
        table.add_row("[blue]Writer[/]", skill, cls.__name__, "-")

    table.add_section()

    for skill, roles in SKILL_REVIEWERS.items():
        for role in roles:
            weight = REVIEWER_WEIGHTS.get(skill, {}).get(role, 0)
            table.add_row("[yellow]Reviewer[/]", skill.value, role.value, f"{weight:.0%}")

    table.add_section()
    table.add_row("[green]Utility[/]", "-", "GlossaryGuard", "-")
    table.add_row("[green]Utility[/]", "-", "ConsistencyChecker", "-")
    table.add_row("[green]Utility[/]", "-", "ReferenceManager", "-")

    console.print(table)
    console.print(f"\n  [dim]总计: {len(WRITER_REGISTRY)} Writers + 28 Reviewers + 3 Utilities = 40 Agents[/]")


# ── main — CLI 入口 ───────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="hydroscribe",
        description="HydroScribe — CHS 多智能体协同写作助手",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
快速开始:
  hydroscribe init              首次配置向导
  hydroscribe serve             启动 Web 服务器 + 仪表盘
  hydroscribe start T1-CN       开始写作
  hydroscribe doctor            环境自诊断

更多信息: https://github.com/your-repo/hydroscribe
        """,
    )
    parser.add_argument("--books-root", default=None, help="书目根目录 (覆盖配置)")
    sub = parser.add_subparsers(dest="command")

    # init
    sub.add_parser("init", help="交互式初始化向导 (首次使用)")

    # serve
    p_serve = sub.add_parser("serve", help="启动 Web 服务器 + 仪表盘")
    p_serve.add_argument("--host", default=None)
    p_serve.add_argument("--port", type=int, default=None)
    p_serve.add_argument("--reload", action="store_true", help="开发模式 (热重载)")

    # start
    p_start = sub.add_parser("start", help="启动写作任务")
    p_start.add_argument("book_id", help="书目ID (如 T1-CN, T2a, M1)")
    p_start.add_argument("--skill", default="BK", help="写作技能: BK/SCI/CN/PAT/RPT/STD-CN/STD-INT/WX/PPT")
    p_start.add_argument("--chapters", default=None, help="并行多章: ch01,ch02,ch03")

    # status
    sub.add_parser("status", help="查看所有书目进度")

    # check
    p_check = sub.add_parser("check", help="对 Markdown 文件执行四维质量检查")
    p_check.add_argument("file", help="要检查的文件路径")
    p_check.add_argument("--skill", default="BK")
    p_check.add_argument("--book-type", default="textbook")

    # agents
    sub.add_parser("agents", help="列出所有 Agent (40个)")

    # doctor
    sub.add_parser("doctor", help="环境自诊断")

    # config
    sub.add_parser("config", help="显示当前配置 (脱敏)")

    args = parser.parse_args()

    cmd_map = {
        "init": cmd_init,
        "serve": cmd_serve,
        "start": cmd_start,
        "status": cmd_status,
        "check": cmd_check,
        "agents": cmd_agents,
        "doctor": cmd_doctor,
        "config": cmd_config,
    }

    handler = cmd_map.get(args.command)
    if handler:
        handler(args)
    else:
        console.print(BANNER)
        parser.print_help()


if __name__ == "__main__":
    main()
