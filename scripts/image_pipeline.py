#!/usr/bin/env python3
"""
图片自动化流水线 v1.0
====================
供 Claude Code 调用的统一图片管理工具。
支持：状态检查、生成、评审清单、插入文档。

用法:
  # 查看所有图片状态
  python scripts/image_pipeline.py status --book T2-CN

  # 查看指定章节状态
  python scripts/image_pipeline.py status --book T2-CN --chapter 09

  # 只生成缺失的图片
  python scripts/image_pipeline.py generate --book T2-CN --missing

  # 生成指定章节（覆盖模式，旧图备份为_old）
  python scripts/image_pipeline.py generate --book T2-CN --chapter 09 --overwrite

  # 生成指定图片
  python scripts/image_pipeline.py generate --book T2-CN --keys fig_ch09_1 fig_ch09_2

  # 预览（不实际生成）
  python scripts/image_pipeline.py generate --book T2-CN --all --dry-run

  # 生成评审清单（供 Claude 逐张查看）
  python scripts/image_pipeline.py review --book T2-CN

  # 插入图片引用到 Markdown
  python scripts/image_pipeline.py insert --book T2-CN

  # 全流程: 生成缺失 → 评审清单
  python scripts/image_pipeline.py full --book T2-CN
"""

import os, sys, json, argparse
from pathlib import Path
from datetime import datetime


REPO_ROOT = Path(__file__).parent.parent.resolve()

BOOK_DIRS = {
    "T1-CN": REPO_ROOT / "books" / "T1-CN",
    "T2-CN": REPO_ROOT / "books" / "T2-CN",
}


def get_book_dir(book_id):
    d = BOOK_DIRS.get(book_id)
    if not d or not d.exists():
        print(f"❌ 未知书目: {book_id}")
        print(f"   可选: {', '.join(BOOK_DIRS.keys())}")
        sys.exit(1)
    return d


def load_manifests(book_dir):
    """加载图片清单"""
    data = {}
    for fname in ["image_manifest.json", "chapter_openers.json"]:
        fp = book_dir / fname
        if fp.exists():
            try:
                data.update(json.load(open(fp, encoding="utf-8")))
            except Exception as e:
                print(f"⚠️  加载 {fname} 失败: {e}")
    return data


def get_image_info(book_dir, item):
    """获取单张图片的状态信息"""
    fp = book_dir / item["file"]
    if not fp.exists():
        return {"status": "missing", "size": 0, "path": str(fp)}
    sz = fp.stat().st_size
    if sz > 20 * 1024:
        return {"status": "ok", "size": sz, "path": str(fp)}
    elif sz > 0:
        return {"status": "placeholder", "size": sz, "path": str(fp)}
    return {"status": "empty", "size": 0, "path": str(fp)}


# ═══════════════════════════════════════════════════════════════════════
# 命令: status
# ═══════════════════════════════════════════════════════════════════════
def cmd_status(args):
    book_dir = get_book_dir(args.book)
    manifest = load_manifests(book_dir)

    if not manifest:
        print(f"❌ 未找到图片清单文件")
        return

    # 按章节分组
    by_ch = {}
    for k, v in sorted(manifest.items()):
        ch = v.get("chapter", "??")
        by_ch.setdefault(ch, []).append((k, v))

    # 过滤章节
    if args.chapter:
        ch_filter = args.chapter.zfill(2)
        by_ch = {k: v for k, v in by_ch.items() if k == ch_filter}

    stats = {"ok": 0, "missing": 0, "placeholder": 0, "empty": 0}
    total = 0

    print(f"\n📁 {args.book} 图片状态")
    print(f"{'=' * 70}")

    for ch in sorted(by_ch):
        items = by_ch[ch]
        ch_label = f"第{int(ch)}章" if ch.isdigit() and int(ch) > 0 else f"ch{ch}"
        print(f"\n  ── {ch_label} ({len(items)} 张) ──")
        for k, v in items:
            info = get_image_info(book_dir, v)
            stats[info["status"]] += 1
            total += 1

            if info["status"] == "ok":
                st = f"✅ {info['size'] // 1024:>4d}KB"
            elif info["status"] == "placeholder":
                st = "📄 占位符"
            elif info["status"] == "missing":
                st = "❌ 缺 失"
            else:
                st = "⚫ 空文件"

            type_tag = f"[{v.get('type', '?'):7s}]"
            print(f"    {st}  {type_tag}  {k:30s}  {v.get('title', '')[:24]}")

    print(f"\n{'=' * 70}")
    print(f"  合计: {total} 张")
    print(f"  ✅ 完成: {stats['ok']}  ❌ 缺失: {stats['missing']}  📄 占位: {stats['placeholder']}  ⚫ 空: {stats['empty']}")

    if stats["missing"] + stats["placeholder"] > 0:
        print(f"\n  💡 生成缺失图片:")
        print(f"     python scripts/image_pipeline.py generate --book {args.book} --missing")


# ═══════════════════════════════════════════════════════════════════════
# 命令: generate
# ═══════════════════════════════════════════════════════════════════════
def _ensure_env(book_dir):
    """确保 API 配置可用：统一使用 T2-CN/.env 作为共享密钥源"""
    shared_env = REPO_ROOT / "books" / "T2-CN" / ".env"
    local_env = book_dir / ".env"
    if not local_env.exists() and shared_env.exists():
        # 将 T2-CN 的 .env 加载到环境变量
        for line in shared_env.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                k, v = k.strip(), v.strip().strip('"').strip("'")
                os.environ[k] = v
        print(f"  📎 API 配置来自: {shared_env}")


def cmd_generate(args):
    book_dir = get_book_dir(args.book)

    # 确保 API 密钥可用
    _ensure_env(book_dir)

    # 构建 generate_images_api.py 的命令行参数
    api_script = book_dir / "generate_images_api.py"
    if not api_script.exists():
        # 尝试从 T2-CN 复制
        src = REPO_ROOT / "books" / "T2-CN" / "generate_images_api.py"
        if src.exists():
            import shutil
            shutil.copy2(src, api_script)
            print(f"  📋 已从 T2-CN 复制 generate_images_api.py")
        else:
            print(f"❌ 未找到 {api_script}")
            sys.exit(1)

    cmd_parts = [sys.executable, str(api_script), f"--project-dir", str(book_dir)]

    # 范围选择
    if args.keys:
        cmd_parts.extend(["--keys"] + args.keys)
    elif args.chapter:
        cmd_parts.extend(["--chapter", args.chapter.zfill(2)])
    else:
        cmd_parts.append("--all")

    # 模式
    if args.overwrite:
        cmd_parts.extend(["--mode", "overwrite"])
    else:
        cmd_parts.extend(["--mode", "skip"])

    # 过滤: --missing 表示生成 missing + placeholder（skip模式自动跳过ok图片）
    # 不传 --status 过滤，让 skip 模式处理

    if args.type:
        cmd_parts.extend(["--type", args.type])

    # 选项
    if args.dry_run:
        cmd_parts.append("--dry-run")

    if args.update_md:
        cmd_parts.append("--update-md")

    print(f"🚀 执行: {' '.join(cmd_parts)}")
    print()

    os.execvp(sys.executable, cmd_parts)


# ═══════════════════════════════════════════════════════════════════════
# 命令: review — 生成供 Claude Code 审查的检查清单
# ═══════════════════════════════════════════════════════════════════════
def cmd_review(args):
    book_dir = get_book_dir(args.book)
    manifest = load_manifests(book_dir)

    if args.chapter:
        ch_filter = args.chapter.zfill(2)
        manifest = {k: v for k, v in manifest.items() if v.get("chapter") == ch_filter}

    # 只检查已有图片（ok 或 placeholder）
    review_items = []
    for k, v in sorted(manifest.items()):
        info = get_image_info(book_dir, v)
        if info["status"] in ("ok", "placeholder"):
            review_items.append({
                "key": k,
                "title": v.get("title", ""),
                "fig_id": v.get("fig_id", ""),
                "type": v.get("type", ""),
                "chapter": v.get("chapter", ""),
                "path": info["path"],
                "size_kb": info["size"] // 1024,
                "status": info["status"],
                "prompt_preview": (v.get("prompt_en", "") or v.get("prompt_zh", ""))[:100],
            })

    if not review_items:
        print("没有需要评审的图片。")
        return

    # 输出评审清单
    review_file = book_dir / "H" / "review_checklist.json"
    review_file.parent.mkdir(exist_ok=True)

    review_data = {
        "generated": datetime.now().isoformat(),
        "book": args.book,
        "total": len(review_items),
        "items": review_items,
        "review_criteria": {
            "1_content_accuracy": "图片内容是否准确反映提示词要求",
            "2_text_readability": "图片中的文字（如有）是否清晰可读",
            "3_color_scheme": "配色是否符合科技蓝+水元素风格",
            "4_print_quality": "分辨率和清晰度是否满足A4印刷要求",
            "5_no_artifacts": "是否有AI生成的明显瑕疵（多余肢体、文字乱码等）",
            "6_consistency": "与同章其他图片风格是否一致"
        }
    }

    with open(review_file, "w", encoding="utf-8") as f:
        json.dump(review_data, f, ensure_ascii=False, indent=2)

    print(f"\n📋 评审清单: {review_file}")
    print(f"   共 {len(review_items)} 张图片待评审")
    print()

    # 输出供 Claude Code 直接使用的路径列表
    print("📸 图片路径（供 Claude Code Read 工具查看）:")
    print("-" * 60)
    for item in review_items:
        flag = "📄" if item["status"] == "placeholder" else "✅"
        print(f"  {flag} {item['key']:30s} {item['size_kb']:>4d}KB  {item['path']}")

    print()
    print("💡 Claude Code 可用 Read 工具逐张查看图片进行评审")
    print("   评审标准: 内容准确性 / 文字可读性 / 配色风格 / 印刷质量 / AI瑕疵 / 一致性")


# ═══════════════════════════════════════════════════════════════════════
# 命令: insert — 将图片引用插入 Markdown 文件
# ═══════════════════════════════════════════════════════════════════════
def cmd_insert(args):
    book_dir = get_book_dir(args.book)
    manifest = load_manifests(book_dir)

    if args.chapter:
        ch_filter = args.chapter.zfill(2)
        manifest = {k: v for k, v in manifest.items() if v.get("chapter") == ch_filter}

    # 读取项目配置中的 github_raw_base
    github_raw_base = ""
    config_file = book_dir / "image_project.json"
    if config_file.exists():
        try:
            cfg = json.load(open(config_file, encoding="utf-8"))
            github_raw_base = cfg.get("github_raw_base", "")
        except:
            pass

    # 按章节分组
    by_ch = {}
    for k, v in sorted(manifest.items()):
        ch = v.get("chapter", "??")
        by_ch.setdefault(ch, []).append((k, v))

    updated = 0
    for ch, items in sorted(by_ch.items()):
        # 查找对应的 markdown 文件
        md_files = list(book_dir.glob(f"ch{ch}*.md"))
        md_files = [f for f in md_files if not any(x in f.name for x in ["_v1", "_backup", "_old", "_images"])]

        if not md_files:
            continue

        md_file = md_files[0]
        text = md_file.read_text(encoding="utf-8")
        changed = False

        for k, v in items:
            info = get_image_info(book_dir, v)
            if info["status"] not in ("ok",):
                continue

            fig_id = v.get("fig_id", k)
            title = v["title"]
            filename = Path(v["file"]).name

            if github_raw_base:
                img_ref = f"{github_raw_base.rstrip('/')}/{filename}"
            else:
                img_ref = f"H/{filename}"

            # 检查是否已存在引用
            if filename in text:
                continue

            # 尝试在适当位置插入（这里简单追加到文末配图区域）
            new_ref = f"\n![{fig_id} {title}]({img_ref})\n"

            if "## 配图" in text:
                text = text.replace("## 配图", f"## 配图\n{new_ref}", 1)
                changed = True
            # 否则不自动插入，留给用户手动处理

        if changed:
            md_file.write_text(text, encoding="utf-8")
            print(f"  💾 更新 {md_file.name}")
            updated += 1

    print(f"\n更新了 {updated} 个文件")


# ═══════════════════════════════════════════════════════════════════════
# 命令: full — 完整流水线
# ═══════════════════════════════════════════════════════════════════════
def cmd_full(args):
    book_dir = get_book_dir(args.book)

    print("=" * 60)
    print(f"  📦 {args.book} 完整图片流水线")
    print("=" * 60)

    # Step 1: 状态检查
    print("\n📊 Step 1: 状态检查")
    print("-" * 40)
    manifest = load_manifests(book_dir)
    stats = {"ok": 0, "missing": 0, "placeholder": 0}
    for k, v in manifest.items():
        info = get_image_info(book_dir, v)
        stats[info["status"]] = stats.get(info["status"], 0) + 1

    print(f"  ✅ 已有: {stats['ok']}  ❌ 缺失: {stats['missing']}  📄 占位: {stats.get('placeholder', 0)}")

    need_generate = stats["missing"] + stats.get("placeholder", 0)
    if need_generate == 0:
        print("  所有图片已就绪!")
    else:
        print(f"\n  需要生成: {need_generate} 张")
        print(f"  执行: python scripts/image_pipeline.py generate --book {args.book} --missing")

    # Step 2: 评审清单
    print(f"\n📋 Step 2: 评审清单")
    print("-" * 40)
    review_items = []
    for k, v in sorted(manifest.items()):
        info = get_image_info(book_dir, v)
        if info["status"] == "ok":
            review_items.append(info["path"])

    print(f"  {len(review_items)} 张图片可供评审")
    if review_items:
        print(f"  执行: python scripts/image_pipeline.py review --book {args.book}")

    # Step 3: 插入建议
    print(f"\n📝 Step 3: 文档插入")
    print("-" * 40)
    print(f"  执行: python scripts/image_pipeline.py insert --book {args.book}")

    print(f"\n{'=' * 60}")
    print("  流水线概览完成")
    print(f"{'=' * 60}")


# ═══════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════
def main():
    p = argparse.ArgumentParser(
        description="图片自动化流水线 v1.0 — Claude Code 专用",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = p.add_subparsers(dest="command", required=True)

    # status
    s = sub.add_parser("status", help="查看图片状态")
    s.add_argument("--book", required=True, choices=list(BOOK_DIRS.keys()))
    s.add_argument("--chapter", help="章节号（如 09）")

    # generate
    g = sub.add_parser("generate", help="生成图片")
    g.add_argument("--book", required=True, choices=list(BOOK_DIRS.keys()))
    g.add_argument("--chapter", help="章节号")
    g.add_argument("--keys", nargs="+", help="指定图片 key")
    g.add_argument("--all", action="store_true", help="全部")
    g.add_argument("--missing", action="store_true", help="只生成缺失的")
    g.add_argument("--overwrite", action="store_true", help="覆盖模式（旧图备份为_old）")
    g.add_argument("--type", choices=["opener", "inline", "all"], help="图片类型")
    g.add_argument("--dry-run", action="store_true", help="预览模式")
    g.add_argument("--update-md", action="store_true", help="生成后更新Markdown")

    # review
    r = sub.add_parser("review", help="生成评审清单")
    r.add_argument("--book", required=True, choices=list(BOOK_DIRS.keys()))
    r.add_argument("--chapter", help="章节号")

    # insert
    i = sub.add_parser("insert", help="插入图片到Markdown")
    i.add_argument("--book", required=True, choices=list(BOOK_DIRS.keys()))
    i.add_argument("--chapter", help="章节号")

    # full
    f = sub.add_parser("full", help="完整流水线概览")
    f.add_argument("--book", required=True, choices=list(BOOK_DIRS.keys()))

    args = p.parse_args()

    dispatch = {
        "status": cmd_status,
        "generate": cmd_generate,
        "review": cmd_review,
        "insert": cmd_insert,
        "full": cmd_full,
    }
    dispatch[args.command](args)


if __name__ == "__main__":
    main()
