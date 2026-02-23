"""
HydroScribe CLI — 命令行入口

用法:
    hydroscribe serve              # 启动 Web 服务器 + 仪表盘
    hydroscribe start BKT1-CN      # 启动 T1-CN 的写作
    hydroscribe status             # 查看所有书目进度
    hydroscribe check <file>       # 对文件执行术语/一致性/参考文献检查
    hydroscribe agents             # 列出所有 Agent
"""

import argparse
import asyncio
import json
import os
import sys
from typing import Optional

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def cmd_serve(args):
    """启动 Web 服务器"""
    import uvicorn

    host = args.host or "0.0.0.0"
    port = args.port or 8000

    console.print(Panel(
        f"[bold blue]HydroScribe[/] v0.2.0\n"
        f"Starting server at http://{host}:{port}\n"
        f"Dashboard: http://{host}:{port}/\n"
        f"API docs:  http://{host}:{port}/docs",
        title="HydroScribe Server",
    ))

    uvicorn.run(
        "hydroscribe.api.app:app",
        host=host,
        port=port,
        reload=args.reload,
        log_level="info",
    )


def cmd_start(args):
    """启动写作任务"""
    from hydroscribe.engine.orchestrator import Orchestrator

    book_id = args.book_id.replace("BK", "")
    skill_type = args.skill or "BK"
    books_root = args.books_root or os.environ.get("BOOKS_ROOT", "/home/user/books")

    console.print(f"[bold]启动写作[/]: {book_id} (技能: {skill_type})")

    orch = Orchestrator(books_root=books_root)
    result = asyncio.run(orch.start_book(book_id, skill_type))

    if result["status"] == "completed":
        console.print(f"[green]完成![/] {result.get('word_count', 0)}字, {result.get('iterations', 0)}轮, 评分{result.get('score', 0)}")
        console.print(f"文件: {result.get('file', '')}")
    else:
        console.print(f"[yellow]状态: {result['status']}[/]")
        console.print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_status(args):
    """查看所有书目进度"""
    books_root = args.books_root or os.environ.get("BOOKS_ROOT", "/home/user/books")
    progress_dir = os.path.join(books_root, "progress")

    table = Table(title="CHS 教材体系写作进度")
    table.add_column("书目", style="bold")
    table.add_column("进度", justify="right")
    table.add_column("已完成章节", justify="center")
    table.add_column("总章节", justify="center")
    table.add_column("最后更新")

    if os.path.exists(progress_dir):
        for f in sorted(os.listdir(progress_dir)):
            if f.endswith(".json"):
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

                style = "green" if progress == "100%" else ("yellow" if completed > 0 else "dim")
                table.add_row(book_id, progress, str(completed), str(total), last_update, style=style)

    console.print(table)


def cmd_check(args):
    """对文件执行质量检查"""
    filepath = args.file
    if not os.path.exists(filepath):
        console.print(f"[red]文件不存在: {filepath}[/]")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    console.print(f"[bold]检查文件[/]: {filepath} ({len(content)}字)")

    from hydroscribe.tools.quality_tools import (
        CheckGlossaryTool, CheckConsistencyTool, CheckReferenceTool, CheckStructureTool
    )

    # 术语检查
    glossary_result = CheckGlossaryTool().execute(content)
    status = "[green]PASS[/]" if glossary_result["passed"] else "[red]FAIL[/]"
    console.print(f"\n术语检查: {status} (分数: {glossary_result['score']})")
    for alias in glossary_result.get("forbidden_aliases", []):
        console.print(f"  [red]禁止别名[/]: '{alias['alias']}' -> '{alias['correct']}' (x{alias['count']})")

    # 一致性检查
    consistency_result = CheckConsistencyTool().execute(content)
    status = "[green]PASS[/]" if consistency_result["passed"] else "[red]FAIL[/]"
    console.print(f"\n一致性检查: {status} (分数: {consistency_result['score']})")
    for issue in consistency_result.get("issues", []):
        color = "red" if issue["severity"] == "red" else "yellow"
        console.print(f"  [{color}]{issue['message']}[/]")

    # 参考文献检查
    ref_result = CheckReferenceTool().execute(content, args.skill or "BK")
    status = "[green]PASS[/]" if ref_result["passed"] else "[red]FAIL[/]"
    console.print(f"\n参考文献检查: {status} (分数: {ref_result['score']})")
    console.print(f"  总引用: {ref_result['total_references']}篇, 自引率: {ref_result['self_citation_rate']:.1%}, 近5年: {ref_result['recent_rate']:.1%}")
    for missing in ref_result.get("must_cite_missing", []):
        console.print(f"  [yellow]缺少必引[/]: {missing}")

    # 结构检查
    struct_result = CheckStructureTool().execute(content, args.book_type or "textbook")
    status = "[green]PASS[/]" if struct_result["passed"] else "[red]FAIL[/]"
    console.print(f"\n结构检查: {status} (分数: {struct_result['score']}, 通过: {struct_result['passed_count']}/{struct_result['total_checks']})")
    for name, val in struct_result.get("checks", {}).items():
        if isinstance(val, bool):
            icon = "[green]✓[/]" if val else "[red]✗[/]"
            console.print(f"  {icon} {name}")

    # 总分
    avg = (glossary_result["score"] + consistency_result["score"] +
           ref_result["score"] + struct_result["score"]) / 4
    console.print(f"\n[bold]综合质检分: {avg:.1f}/10[/]")


def cmd_agents(args):
    """列出所有 Agent"""
    from hydroscribe.agents.writers import WRITER_REGISTRY
    from hydroscribe.schema import SKILL_REVIEWERS, ReviewerRole

    table = Table(title="HydroScribe Agent 清单")
    table.add_column("类型", style="bold")
    table.add_column("技能/角色")
    table.add_column("Agent 类名")
    table.add_column("权重", justify="right")

    for skill, cls in WRITER_REGISTRY.items():
        table.add_row("Writer", skill, cls.__name__, "-")

    table.add_section()

    for skill, roles in SKILL_REVIEWERS.items():
        for role in roles:
            from hydroscribe.engine.orchestrator import REVIEWER_WEIGHTS
            weight = REVIEWER_WEIGHTS.get(skill, {}).get(role, 0)
            table.add_row("Reviewer", f"{skill.value}/{role.value}", role.value, f"{weight:.0%}")

    table.add_section()
    table.add_row("Utility", "glossary", "GlossaryGuardAgent", "-")
    table.add_row("Utility", "consistency", "ConsistencyCheckerAgent", "-")
    table.add_row("Utility", "reference", "ReferenceManagerAgent", "-")

    console.print(table)


def main():
    parser = argparse.ArgumentParser(
        prog="hydroscribe",
        description="HydroScribe — CHS 多智能体协同写作助手 CLI",
    )
    parser.add_argument("--books-root", default=None, help="书目根目录")
    sub = parser.add_subparsers(dest="command")

    # serve
    p_serve = sub.add_parser("serve", help="启动 Web 服务器")
    p_serve.add_argument("--host", default="0.0.0.0")
    p_serve.add_argument("--port", type=int, default=8000)
    p_serve.add_argument("--reload", action="store_true")

    # start
    p_start = sub.add_parser("start", help="启动写作任务")
    p_start.add_argument("book_id", help="书目ID (如 T1-CN, T2a, M1)")
    p_start.add_argument("--skill", default="BK", help="写作技能类型")

    # status
    sub.add_parser("status", help="查看写作进度")

    # check
    p_check = sub.add_parser("check", help="质量检查")
    p_check.add_argument("file", help="要检查的 Markdown 文件")
    p_check.add_argument("--skill", default="BK")
    p_check.add_argument("--book-type", default="textbook")

    # agents
    sub.add_parser("agents", help="列出所有 Agent")

    args = parser.parse_args()

    if args.command == "serve":
        cmd_serve(args)
    elif args.command == "start":
        cmd_start(args)
    elif args.command == "status":
        cmd_status(args)
    elif args.command == "check":
        cmd_check(args)
    elif args.command == "agents":
        cmd_agents(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
