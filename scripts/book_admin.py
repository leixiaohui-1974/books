#!/usr/bin/env python3
"""
CHS 书稿版本管理工具 (book_admin.py)

多智能体协同写作的版本管理基础设施。
解决新旧版本混存导致 AI agent 误读/误改/误报的问题。

命令:
  status   <书目>             查看当前版本 vs 归档文件统计
  archive  <书目>             将旧版文件移入 _archive/
  promote  <书目> <文件>       将新写文件提升为当前版本（旧版自动归档）
  manifest <书目>             重建 book_manifest.json
  list     <书目>             列出当前文件清单（供其他脚本/agent读取）
  clean    <书目> --dry-run   预览可清理的归档文件（不实际删除）
  clean    <书目> --confirm   实际删除归档文件（不可恢复）

用法:
  python3 book_admin.py status T1-CN
  python3 book_admin.py archive T2-CN
  python3 book_admin.py promote T1-CN ch04_v3.md
  python3 book_admin.py manifest T1-CN
  python3 book_admin.py list T2-CN --json

设计原则:
  1. 每本书的根目录只保留「当前版本」文件
  2. 旧版/备份/临时文件全部在 _archive/ 子目录中
  3. book_manifest.json 是 AI agent 的权威文件清单
  4. 所有操作幂等，重复运行不会破坏状态
"""

import argparse
import json
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
BOOKS_DIR = REPO_ROOT / "books"

# 旧版文件的识别模式
ARCHIVE_PATTERNS = [
    '_v1', '_v2', '_v3', '_v4', '_v5', '_v6', '_v7', '_v8', '_v9',
    '_backup', '_OLD', '_old', '_temp', '_restructured',
    '_archive', '_draft', '_wip',
]


def resolve_book(book_name: str) -> Path:
    """解析书目名称为目录路径"""
    book_dir = BOOKS_DIR / book_name
    if not book_dir.is_dir():
        print(f"错误: 找不到书目目录 {book_dir}", file=sys.stderr)
        sys.exit(1)
    return book_dir


def is_archive_file(filename: str) -> bool:
    """判断文件名是否匹配旧版模式"""
    stem = Path(filename).stem
    return any(pat in stem for pat in ARCHIVE_PATTERNS)


def get_chapter_files(book_dir: Path) -> dict:
    """扫描书目目录，分类为 current / archive / orphan"""
    archive_dir = book_dir / "_archive"

    current = []   # 根目录下的当前版本
    stale = []     # 根目录下应该被归档的旧版
    archived = []  # 已在 _archive/ 中的文件
    other = []     # 非章节文件

    for f in sorted(book_dir.glob("ch*.md")):
        if is_archive_file(f.name):
            stale.append(f)
        else:
            current.append(f)

    if archive_dir.is_dir():
        for f in sorted(archive_dir.glob("*.md")):
            archived.append(f)

    return {
        "current": current,
        "stale": stale,
        "archived": archived,
    }


# ============================================================
# 命令实现
# ============================================================

def cmd_status(args):
    """查看版本状态"""
    book_dir = resolve_book(args.book)
    files = get_chapter_files(book_dir)

    print(f"📖 {args.book} 版本状态")
    print(f"   目录: {book_dir}")
    print()

    print(f"  ✅ 当前版本: {len(files['current'])} 个")
    for f in files['current']:
        size = f.stat().st_size
        print(f"     {f.name}  ({size // 1024}KB)")

    if files['stale']:
        print(f"\n  ⚠️  待归档: {len(files['stale'])} 个")
        for f in files['stale']:
            print(f"     {f.name}")
        print(f"\n  💡 运行: python3 book_admin.py archive {args.book}")
    else:
        print(f"\n  ✅ 根目录无旧版文件")

    print(f"\n  📦 已归档: {len(files['archived'])} 个")
    if files['archived'] and args.verbose:
        for f in files['archived']:
            print(f"     {f.name}")

    # 检查 manifest
    manifest = book_dir / "book_manifest.json"
    if manifest.exists():
        data = json.loads(manifest.read_text(encoding="utf-8"))
        manifest_files = set(data.get("current_files", []))
        actual_files = {f.name for f in files['current']}
        if manifest_files == actual_files:
            print(f"\n  ✅ book_manifest.json 与实际文件一致")
        else:
            added = actual_files - manifest_files
            removed = manifest_files - actual_files
            print(f"\n  ⚠️  book_manifest.json 不一致:")
            if added:
                print(f"     新增(未在manifest): {added}")
            if removed:
                print(f"     缺失(manifest中有): {removed}")
            print(f"  💡 运行: python3 book_admin.py manifest {args.book}")
    else:
        print(f"\n  ⚠️  缺少 book_manifest.json")
        print(f"  💡 运行: python3 book_admin.py manifest {args.book}")


def cmd_archive(args):
    """将旧版文件移入 _archive/"""
    book_dir = resolve_book(args.book)
    archive_dir = book_dir / "_archive"
    files = get_chapter_files(book_dir)

    if not files['stale']:
        print(f"✅ {args.book}: 根目录无旧版文件，无需归档")
        return

    archive_dir.mkdir(exist_ok=True)
    moved = 0
    for f in files['stale']:
        dest = archive_dir / f.name
        if dest.exists():
            # 同名冲突：加时间戳
            stem = f.stem
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            dest = archive_dir / f"{stem}_{ts}{f.suffix}"
        shutil.move(str(f), str(dest))
        print(f"  → _archive/{dest.name}")
        moved += 1

    print(f"\n✅ 已归档 {moved} 个文件")

    # 自动更新 manifest
    print(f"\n📋 自动更新 book_manifest.json ...")
    args_copy = argparse.Namespace(book=args.book)
    cmd_manifest(args_copy)


def cmd_promote(args):
    """将新文件提升为当前版本，旧版自动归档

    使用场景：AI agent 写了 ch04_v3.md，要替换 ch04_final.md
    """
    book_dir = resolve_book(args.book)
    archive_dir = book_dir / "_archive"
    new_file = book_dir / args.file

    if not new_file.exists():
        # 也检查 _archive/ 中
        alt = archive_dir / args.file
        if alt.exists():
            new_file = alt
        else:
            print(f"错误: 找不到文件 {args.file}", file=sys.stderr)
            sys.exit(1)

    # 从文件名推断章号
    ch_match = re.match(r'ch(\d+)', args.file)
    if not ch_match:
        print(f"错误: 无法从 {args.file} 中提取章号", file=sys.stderr)
        sys.exit(1)

    ch_num = ch_match.group(1)

    # 找到当前的同章文件
    current_files = list(book_dir.glob(f"ch{ch_num}*.md"))
    current_files = [f for f in current_files if f.name != args.file
                     and not is_archive_file(f.name)]

    archive_dir.mkdir(exist_ok=True)

    # 归档当前版本
    for old in current_files:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        dest = archive_dir / f"{old.stem}_archived_{ts}{old.suffix}"
        shutil.move(str(old), str(dest))
        print(f"  📦 归档: {old.name} → _archive/{dest.name}")

    # 确定新文件的目标名
    # T1-CN 用 ch{NN}_final.md 命名
    # T2-CN 用 ch{NN}_{标题}.md 命名
    manifest = book_dir / "book_manifest.json"
    target_name = None
    if manifest.exists():
        data = json.loads(manifest.read_text(encoding="utf-8"))
        ch_key = f"ch{ch_num}"
        if ch_key in data.get("chapter_map", {}):
            target_name = data["chapter_map"][ch_key].get("file")

    if not target_name:
        # 默认：ch{NN}_final.md
        target_name = f"ch{ch_num}_final.md"

    # 移动/重命名新文件
    dest = book_dir / target_name
    if new_file != dest:
        shutil.move(str(new_file), str(dest))
        print(f"  ✅ 提升: {args.file} → {target_name}")
    else:
        print(f"  ✅ {target_name} 已就位")

    # 更新 manifest
    print(f"\n📋 自动更新 book_manifest.json ...")
    args_copy = argparse.Namespace(book=args.book)
    cmd_manifest(args_copy)


def cmd_manifest(args):
    """重建 book_manifest.json"""
    book_dir = resolve_book(args.book)
    files = get_chapter_files(book_dir)

    # 读取已有 manifest 保留元数据
    manifest_path = book_dir / "book_manifest.json"
    existing = {}
    if manifest_path.exists():
        existing = json.loads(manifest_path.read_text(encoding="utf-8"))

    current_files = sorted([f.name for f in files['current']])

    # 构建 chapter_map
    chapter_map = existing.get("chapter_map", {})
    for f in files['current']:
        ch_match = re.match(r'ch(\d+)', f.name)
        if not ch_match:
            continue
        ch_key = f"ch{ch_match.group(1)}"
        if ch_key not in chapter_map:
            # 尝试从文件内容读取标题
            title = _extract_title(f)
            chapter_map[ch_key] = {"file": f.name, "title": title}
        else:
            chapter_map[ch_key]["file"] = f.name

    data = {
        "book_id": existing.get("book_id", args.book),
        "book_title": existing.get("book_title", args.book),
        "language": existing.get("language", "zh-CN"),
        "archive_dir": "_archive",
        "image_dir": existing.get("image_dir", "H"),
        "current_files": current_files,
        "chapter_map": dict(sorted(chapter_map.items())),
        "naming_convention": existing.get("naming_convention", ""),
        "image_url_base": existing.get("image_url_base", ""),
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    manifest_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )
    print(f"  ✅ {manifest_path.name}: {len(current_files)} 个当前文件")


def cmd_list(args):
    """列出当前文件（供脚本/agent调用）"""
    book_dir = resolve_book(args.book)

    manifest = book_dir / "book_manifest.json"
    if manifest.exists():
        data = json.loads(manifest.read_text(encoding="utf-8"))
        files = data.get("current_files", [])
    else:
        files_obj = get_chapter_files(book_dir)
        files = sorted([f.name for f in files_obj['current']])

    if args.json:
        print(json.dumps(files, ensure_ascii=False))
    else:
        for f in files:
            print(f)


def cmd_clean(args):
    """清理归档文件"""
    book_dir = resolve_book(args.book)
    archive_dir = book_dir / "_archive"

    if not archive_dir.is_dir():
        print(f"✅ {args.book}: 无归档目录")
        return

    archived = list(archive_dir.glob("*.md"))
    if not archived:
        print(f"✅ {args.book}: 归档目录为空")
        return

    total_size = sum(f.stat().st_size for f in archived)

    if args.dry_run:
        print(f"🔍 {args.book} 归档预览（--dry-run，不实际删除）:")
        for f in sorted(archived):
            print(f"   {f.name}  ({f.stat().st_size // 1024}KB)")
        print(f"\n   共 {len(archived)} 个文件，{total_size // 1024}KB")
        print(f"   💡 确认删除: python3 book_admin.py clean {args.book} --confirm")
    elif args.confirm:
        for f in archived:
            f.unlink()
        print(f"🗑️  已删除 {len(archived)} 个归档文件 ({total_size // 1024}KB)")
        # 删除空目录
        if not any(archive_dir.iterdir()):
            archive_dir.rmdir()
            print(f"   已移除空目录 _archive/")
    else:
        print("需要指定 --dry-run 或 --confirm")


def cmd_check_all(args):
    """检查所有书目的版本状态（全局视图）"""
    if not BOOKS_DIR.is_dir():
        print(f"错误: 找不到 books/ 目录", file=sys.stderr)
        sys.exit(1)

    books = sorted([d.name for d in BOOKS_DIR.iterdir()
                    if d.is_dir() and not d.name.startswith('.')])

    print(f"📚 全部书目版本状态\n")
    print(f"{'书目':<12} {'当前':>4} {'待归档':>6} {'已归档':>6} {'manifest':>10}")
    print(f"{'-'*12} {'-'*4} {'-'*6} {'-'*6} {'-'*10}")

    for book_name in books:
        book_dir = BOOKS_DIR / book_name
        files = get_chapter_files(book_dir)
        manifest = book_dir / "book_manifest.json"

        m_status = "✅" if manifest.exists() else "❌"
        stale_mark = f"⚠️ {len(files['stale'])}" if files['stale'] else "0"

        print(f"{book_name:<12} {len(files['current']):>4} {stale_mark:>6} "
              f"{len(files['archived']):>6} {m_status:>10}")

    print()


# ============================================================
# 辅助函数
# ============================================================

def _extract_title(filepath: Path) -> str:
    """从 .md 文件的第一个 # 标题行提取标题"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('# '):
                    return line[2:].strip()
                if line and not line.startswith(('---', '<!--', '>')):
                    break
    except Exception:
        pass
    return ""


# ============================================================
# CLI 入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="CHS 书稿版本管理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
命令示例:
  python3 book_admin.py status T1-CN          # 查看版本状态
  python3 book_admin.py archive T2-CN         # 归档旧版文件
  python3 book_admin.py promote T1-CN ch04_v3.md  # 提升新版本
  python3 book_admin.py manifest T1-CN        # 重建清单
  python3 book_admin.py list T2-CN --json     # JSON 输出当前文件列表
  python3 book_admin.py check-all             # 全局状态总览
  python3 book_admin.py clean T1-CN --dry-run # 预览可清理的归档
        """
    )

    sub = parser.add_subparsers(dest="command")

    # status
    p = sub.add_parser("status", help="查看版本状态")
    p.add_argument("book", help="书目名称（如 T1-CN）")
    p.add_argument("--verbose", "-v", action="store_true")

    # archive
    p = sub.add_parser("archive", help="归档旧版文件")
    p.add_argument("book", help="书目名称")

    # promote
    p = sub.add_parser("promote", help="提升新文件为当前版本")
    p.add_argument("book", help="书目名称")
    p.add_argument("file", help="要提升的文件名")

    # manifest
    p = sub.add_parser("manifest", help="重建 book_manifest.json")
    p.add_argument("book", help="书目名称")

    # list
    p = sub.add_parser("list", help="列出当前文件")
    p.add_argument("book", help="书目名称")
    p.add_argument("--json", action="store_true")

    # clean
    p = sub.add_parser("clean", help="清理归档文件")
    p.add_argument("book", help="书目名称")
    p.add_argument("--dry-run", action="store_true", help="仅预览，不删除")
    p.add_argument("--confirm", action="store_true", help="确认删除")

    # check-all
    sub.add_parser("check-all", help="全局状态总览")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    commands = {
        "status": cmd_status,
        "archive": cmd_archive,
        "promote": cmd_promote,
        "manifest": cmd_manifest,
        "list": cmd_list,
        "clean": cmd_clean,
        "check-all": cmd_check_all,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
