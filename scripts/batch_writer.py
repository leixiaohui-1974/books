#!/usr/bin/env python3
"""
CHS 批量写作调度器 (batch_writer.py)

为多智能体协同写作生成优化的 prompt，最大化复用共享上下文，减少 token 浪费。

命令:
  plan     <书目>                      生成写作计划（哪些章需写/扩写/精编）
  prompt   <书目> <章号范围> [--role]   生成批量写作/评审 prompt
  cost     <书目>                      估算 token 成本
  progress <书目>                      查看写作进度

用法:
  python3 batch_writer.py plan T2a
  python3 batch_writer.py prompt T2a ch01-ch05 --role writer
  python3 batch_writer.py prompt T2a ch01-ch05 --role reviewer-b
  python3 batch_writer.py cost T2a
  python3 batch_writer.py progress T2a

设计理念:
  - 不直接调用 AI API，而是生成优化的 prompt 文本
  - 主控 Agent (Opus) 读取 prompt 后通过 Task 工具分发给 Sonnet/Haiku
  - 共享上下文只加载一次，连续处理多章
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
BOOKS_DIR = REPO_ROOT / "books"

# CLAUDE.md 中的目标字数（字符数，1中文字≈1字符）
TARGET_CHARS = {
    "T1-CN": {"total": 150000, "per_ch": 15000},
    "T1-EN": {"total": 400000, "per_ch": 50000},  # 英文字符
    "T2-CN": {"total": 100000, "per_ch": 8000},
    "T2a":   {"total": 450000, "per_ch": 28000},
    "T2b":   {"total": 450000, "per_ch": 32000},
    "M1":    {"total": 250000, "per_ch": 25000},
    "M2":    {"total": 300000, "per_ch": 25000},
    "M3":    {"total": 200000, "per_ch": 20000},
    "M4":    {"total": 250000, "per_ch": 25000},
    "M5":    {"total": 250000, "per_ch": 25000},
    "M6":    {"total": 200000, "per_ch": 20000},
    "M7":    {"total": 300000, "per_ch": 30000},
    "M8":    {"total": 350000, "per_ch": 25000},
    "M9":    {"total": 250000, "per_ch": 21000},
    "M10":   {"total": 150000, "per_ch": 15000},
}

# 模型定价 ($/M tokens)
PRICING = {
    "opus":   {"input": 15.0, "output": 75.0},
    "sonnet": {"input": 3.0,  "output": 15.0},
    "haiku":  {"input": 0.8,  "output": 4.0},
}

# 每万字中文 ≈ 的 token 数（估算）
CHARS_PER_10K_TOKENS = 6000  # 1万token ≈ 6000中文字符


def resolve_book(name):
    d = BOOKS_DIR / name
    if not d.is_dir():
        print(f"错误: 找不到 {d}", file=sys.stderr)
        sys.exit(1)
    return d


def get_chapters(book_dir):
    """获取当前章节文件及字符数"""
    manifest = book_dir / "book_manifest.json"
    if manifest.exists():
        data = json.loads(manifest.read_text(encoding="utf-8"))
        files = data.get("current_files", [])
    else:
        files = sorted([f.name for f in book_dir.glob("ch*.md")
                        if "_archive" not in str(f.parent)
                        and not any(p in f.stem for p in
                                    ["_v1","_v2","_v3","_v4","_v5","_backup","_OLD","_temp"])])

    chapters = []
    for fname in files:
        fpath = book_dir / fname
        if fpath.exists():
            content = fpath.read_text(encoding="utf-8", errors="ignore")
            chars = len(content)
            # 提取标题
            title = ""
            for line in content.split("\n"):
                if line.strip().startswith("# "):
                    title = line.strip()[2:].strip()
                    break
            ch_match = re.match(r"ch(\d+)", fname)
            ch_num = int(ch_match.group(1)) if ch_match else 0
            chapters.append({
                "file": fname,
                "ch_num": ch_num,
                "title": title,
                "chars": chars,
            })
    return chapters


def classify_chapter(ch, target_per_ch):
    """分类章节状态"""
    ratio = ch["chars"] / max(target_per_ch, 1)
    if ratio >= 0.85:
        return "done", "精编"      # 已接近目标，只需精编
    elif ratio >= 0.4:
        return "expand", "扩写"    # 有基础，需扩写
    elif ch["chars"] > 5000:
        return "rewrite", "大幅扩写"  # 有框架但内容很少
    else:
        return "new", "新写"       # 基本空白


# ============================================================
# 命令实现
# ============================================================

def cmd_plan(args):
    """生成写作计划"""
    book_dir = resolve_book(args.book)
    chapters = get_chapters(book_dir)
    target = TARGET_CHARS.get(args.book, {"total": 200000, "per_ch": 20000})

    total_chars = sum(ch["chars"] for ch in chapters)
    total_target = target["total"]

    print(f"📖 {args.book} 写作计划")
    print(f"   当前: {total_chars:,} 字符 / 目标: {total_target:,} 字符 "
          f"({total_chars/total_target*100:.0f}%)")
    print()

    categories = {"done": [], "expand": [], "rewrite": [], "new": []}
    gap_total = 0

    print(f"  {'章节':<30} {'当前':>8} {'目标':>8} {'缺口':>8} {'状态':<8}")
    print(f"  {'-'*30} {'-'*8} {'-'*8} {'-'*8} {'-'*8}")

    for ch in chapters:
        status, label = classify_chapter(ch, target["per_ch"])
        gap = max(0, target["per_ch"] - ch["chars"])
        gap_total += gap
        categories[status].append(ch)

        marker = {"done": "✅", "expand": "📝", "rewrite": "📄", "new": "🆕"}[status]
        print(f"  {marker} {ch['file']:<28} {ch['chars']:>7,} {target['per_ch']:>7,} "
              f"{gap:>7,} {label}")

    print()
    print(f"  总缺口: {gap_total:,} 字符")
    print()
    print(f"  ✅ 已完成(精编): {len(categories['done'])} 章")
    print(f"  📝 需扩写:       {len(categories['expand'])} 章")
    print(f"  📄 大幅扩写:     {len(categories['rewrite'])} 章")
    print(f"  🆕 需新写:       {len(categories['new'])} 章")

    # 推荐批次
    print()
    print(f"  💡 推荐执行顺序:")
    if categories["done"]:
        print(f"     1. 精编 {len(categories['done'])} 章 (Haiku评审 → Sonnet微调)")
    if categories["expand"]:
        print(f"     2. 扩写 {len(categories['expand'])} 章 (Sonnet批量写, 3-5章/批)")
    if categories["rewrite"]:
        print(f"     3. 大幅扩写 {len(categories['rewrite'])} 章 (Sonnet写 + Opus终审)")
    if categories["new"]:
        print(f"     4. 新写 {len(categories['new'])} 章 (Sonnet写 + Opus终审)")


def cmd_prompt(args):
    """生成批量 prompt"""
    book_dir = resolve_book(args.book)
    chapters = get_chapters(book_dir)
    target = TARGET_CHARS.get(args.book, {"total": 200000, "per_ch": 20000})

    # 解析章号范围
    ch_range = parse_range(args.range)
    selected = [ch for ch in chapters if ch["ch_num"] in ch_range]

    if not selected:
        print(f"错误: 未找到章节 {args.range}", file=sys.stderr)
        sys.exit(1)

    role = args.role.lower()

    if role in ("writer", "draft", "draftwriter"):
        prompt = gen_writer_prompt(args.book, selected, target, book_dir)
    elif role in ("reviewer-a", "a"):
        prompt = gen_reviewer_prompt(args.book, selected, "A", "理论严谨型",
            "公式推导正确性、符号一致性、定理逻辑链、LaTeX语法、学术引用准确性")
    elif role in ("reviewer-b", "b"):
        prompt = gen_reviewer_prompt(args.book, selected, "B", "工程实践型",
            "工程参数量级、SCADA/PLC可行性、案例数据真实性、方案可操作性")
    elif role in ("reviewer-c", "c"):
        prompt = gen_reviewer_prompt(args.book, selected, "C", "学科交叉型",
            "跨学科准确性、创新性、术语翻译、可读性和教学价值")
    elif role in ("final", "finalreviewer"):
        prompt = gen_final_prompt(args.book, selected)
    else:
        print(f"可用角色: writer, reviewer-a, reviewer-b, reviewer-c, final")
        sys.exit(1)

    # 输出
    if args.output:
        Path(args.output).write_text(prompt, encoding="utf-8")
        print(f"✅ prompt 已保存到 {args.output}")
        print(f"   字符数: {len(prompt):,}, 约 {len(prompt)//4:,} tokens")
    else:
        print(prompt)


def cmd_cost(args):
    """估算 token 成本"""
    book_dir = resolve_book(args.book)
    chapters = get_chapters(book_dir)
    target = TARGET_CHARS.get(args.book, {"total": 200000, "per_ch": 20000})

    total_gap = 0
    ch_counts = {"done": 0, "expand": 0, "rewrite": 0, "new": 0}
    for ch in chapters:
        status, _ = classify_chapter(ch, target["per_ch"])
        ch_counts[status] += 1
        total_gap += max(0, target["per_ch"] - ch["chars"])

    # 每章的 token 消耗估算
    costs = {
        "done":    {"input": 15000, "output": 3000,  "model": "haiku"},   # 精编：haiku评审
        "expand":  {"input": 40000, "output": 15000, "model": "sonnet"},  # 扩写
        "rewrite": {"input": 50000, "output": 20000, "model": "sonnet"},  # 大幅扩写
        "new":     {"input": 50000, "output": 25000, "model": "sonnet"},  # 新写
    }

    total_cost = 0
    print(f"💰 {args.book} 成本估算")
    print()
    print(f"  {'类型':<10} {'章数':>4} {'模型':<8} {'input/章':>10} {'output/章':>10} {'小计':>8}")
    print(f"  {'-'*10} {'-'*4} {'-'*8} {'-'*10} {'-'*10} {'-'*8}")

    for status, count in ch_counts.items():
        if count == 0:
            continue
        c = costs[status]
        p = PRICING[c["model"]]
        # 写作成本
        write_cost = count * (c["input"] * p["input"] / 1e6 + c["output"] * p["output"] / 1e6)
        total_cost += write_cost
        label = {"done": "精编", "expand": "扩写", "rewrite": "大幅扩写", "new": "新写"}[status]
        print(f"  {label:<10} {count:>4} {c['model']:<8} {c['input']:>10,} {c['output']:>10,} ${write_cost:>6.2f}")

    # 评审成本（每章 haiku 评审 2 轮）
    review_count = sum(ch_counts.values()) - ch_counts["done"]
    review_cost = review_count * 2 * (20000 * 0.8 / 1e6 + 5000 * 4.0 / 1e6)
    total_cost += review_cost
    print(f"  {'评审':<10} {review_count*2:>4} {'haiku':<8} {'20,000':>10} {'5,000':>10} ${review_cost:>6.2f}")

    # Opus 终审（每章 1 次）
    opus_count = sum(ch_counts.values())
    opus_cost = opus_count * (20000 * 15.0 / 1e6 + 5000 * 75.0 / 1e6)
    total_cost += opus_cost
    print(f"  {'终审':<10} {opus_count:>4} {'opus':<8} {'20,000':>10} {'5,000':>10} ${opus_cost:>6.2f}")

    print(f"  {'-'*60}")
    print(f"  {'合计':<10} {sum(ch_counts.values()):>4} {'':8} {'':>10} {'':>10} ${total_cost:>6.2f}")
    print()
    print(f"  缺口: {total_gap:,} 字符")
    print(f"  单价: ${total_cost/max(total_gap,1)*10000:.2f} / 万字")

    # 对比全 Opus 方案
    opus_all = sum(ch_counts.values()) * (110000 * 15.0 / 1e6 + 37000 * 75.0 / 1e6)
    print(f"\n  💡 对比全 Opus 方案: ${opus_all:.2f} → 节省 {(1-total_cost/opus_all)*100:.0f}%")


def cmd_progress(args):
    """查看写作进度"""
    book_dir = resolve_book(args.book)
    chapters = get_chapters(book_dir)
    target = TARGET_CHARS.get(args.book, {"total": 200000, "per_ch": 20000})

    total = sum(ch["chars"] for ch in chapters)
    done = sum(1 for ch in chapters
               if classify_chapter(ch, target["per_ch"])[0] == "done")

    bar_width = 40
    ratio = total / max(target["total"], 1)
    filled = int(bar_width * min(ratio, 1.0))
    bar = "█" * filled + "░" * (bar_width - filled)

    print(f"📊 {args.book} 进度")
    print(f"   [{bar}] {ratio*100:.1f}%")
    print(f"   {total:,} / {target['total']:,} 字符")
    print(f"   {done}/{len(chapters)} 章达标")


# ============================================================
# Prompt 生成器
# ============================================================

def gen_writer_prompt(book, chapters, target, book_dir):
    """生成批量写作 prompt"""
    lines = [
        f"# 批量写作任务: {book}",
        "",
        "你是CHS教材写作助手，以雷晓辉教授的视角写作。",
        "请依次完成以下章节的扩写/新写。",
        "",
        "## 写作规范",
        "- 术语严格遵循 CLAUDE.md §5 术语表",
        "- 数学符号遵循 CLAUDE.md §5.2 符号表",
        "- 每章结构: 学习目标 → 正文 → 例题 → 小结 → 习题 → 拓展阅读",
        "- 公式推导前有物理直觉，推导后有工程意义",
        "- 每章新概念 ≤ 10 个，每个概念至少1个例题",
        "",
        "## 任务清单",
        "",
    ]

    for ch in chapters:
        gap = max(0, target["per_ch"] - ch["chars"])
        status, label = classify_chapter(ch, target["per_ch"])
        lines.append(f"### {ch['file']} ({label})")
        lines.append(f"- 当前: {ch['chars']:,} 字符 → 目标: {target['per_ch']:,} 字符 (缺 {gap:,})")
        lines.append(f"- 标题: {ch['title']}")
        if status == "done":
            lines.append(f"- 操作: 精编（检查术语、补充例题、润色文字）")
        elif status == "expand":
            lines.append(f"- 操作: 在现有内容基础上扩写至目标字数")
        else:
            lines.append(f"- 操作: 大幅扩写或新写，需覆盖章节大纲所有要点")
        lines.append(f"- 文件: books/{book}/{ch['file']}")
        lines.append("")

    lines.extend([
        "## 执行方式",
        "每章写完后用 Write 工具保存。",
        "章节之间注意衔接：开头回顾上章结论，结尾预告下章。",
        "写完全部章节后运行 termcheck_v2.py 检查。",
    ])

    return "\n".join(lines)


def gen_reviewer_prompt(book, chapters, role_id, role_name, dimensions):
    """生成批量评审 prompt"""
    lines = [
        f"# 批量评审任务: {book} (Reviewer{role_id} — {role_name})",
        "",
        f"你是{role_name}评审专家。请依次评审以下章节。",
        "",
        f"## 评审维度: {dimensions}",
        "",
        "## 输出格式",
        "每章输出一个 JSON 数组，格式:",
        '```json',
        '[{"id":"CR-{book}-ch{N}-{seq}","location":"§X.Y 第N行","type":"...","severity":"Critical|Major|Minor","description":"...","suggested_fix":"..."}]',
        '```',
        "",
        "## 任务清单",
        "",
    ]

    for ch in chapters:
        lines.append(f"### {ch['file']}")
        lines.append(f"- 读取 books/{book}/{ch['file']}")
        lines.append(f"- 输出评审清单")
        lines.append("")

    return "\n".join(lines)


def gen_final_prompt(book, chapters):
    """生成终审 prompt"""
    lines = [
        f"# 终审任务: {book} (FinalReviewer — Opus)",
        "",
        "你是CHS理论体系的最终把关者。请对以下章节做终审。",
        "",
        "## 终审标准",
        "1. 理论深度: 与 P1a (WRR) 论文的一致性",
        "2. 论证严密性: 逻辑链条完整、无跳跃",
        "3. 全书叙事连贯性: 章间衔接自然",
        "4. 创新性: 是否有超越现有教材的独到见解",
        "",
        "## 输出",
        "每章: Accept / Minor Revision / Major Revision + 理由",
        "",
        "## 章节列表",
        "",
    ]

    for ch in chapters:
        lines.append(f"- books/{book}/{ch['file']}: {ch['title']}")

    return "\n".join(lines)


# ============================================================
# 辅助函数
# ============================================================

def parse_range(range_str):
    """解析 ch01-ch05 或 ch03 或 ch01,ch03,ch05 格式"""
    nums = set()
    for part in range_str.split(","):
        part = part.strip()
        m = re.match(r"ch(\d+)\s*-\s*ch(\d+)", part)
        if m:
            for i in range(int(m.group(1)), int(m.group(2)) + 1):
                nums.add(i)
        else:
            m = re.match(r"ch(\d+)", part)
            if m:
                nums.add(int(m.group(1)))
    return nums


def main():
    parser = argparse.ArgumentParser(description="CHS 批量写作调度器")
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("plan", help="生成写作计划")
    p.add_argument("book")

    p = sub.add_parser("prompt", help="生成批量 prompt")
    p.add_argument("book")
    p.add_argument("range", help="章号范围: ch01-ch05 或 ch03 或 ch01,ch03,ch05")
    p.add_argument("--role", default="writer",
                   help="角色: writer, reviewer-a/b/c, final")
    p.add_argument("--output", "-o", help="保存到文件")

    p = sub.add_parser("cost", help="估算 token 成本")
    p.add_argument("book")

    p = sub.add_parser("progress", help="查看写作进度")
    p.add_argument("book")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    {"plan": cmd_plan, "prompt": cmd_prompt, "cost": cmd_cost,
     "progress": cmd_progress}[args.command](args)


if __name__ == "__main__":
    main()
