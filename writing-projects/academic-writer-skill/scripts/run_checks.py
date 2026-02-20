#!/usr/bin/env python3
"""run_checks.py — 统一质量检查调度器

自动识别文档类型，按正确顺序运行所有适用的检查脚本。

Usage:
    python3 run_checks.py <markdown_file> [--type TYPE] [--verbose]

Examples:
    python3 run_checks.py paper.md --type sci        # SCI论文全量检查
    python3 run_checks.py report.md --type bk         # BK专著全量检查
    python3 run_checks.py article.md                   # 自动检测类型
    python3 run_checks.py standard.md --type std-cn    # 国内标准全量检查
    python3 run_checks.py slides.md --type ppt         # PPT全量检查

支持类型: sci, cn, pat, bk, rpt, std-cn, std-int, wx, ppt
"""

import subprocess
import sys
import os
import re
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 文体→检查脚本映射（按执行顺序）
CHECK_MATRIX = {
    'sci': [
        ('check_quality.py', ['--type', 'sci'], '通用质量'),
        ('check_references.py', ['--type', 'sci'], '参考文献'),
        ('check_paper.py', ['--type', 'sci'], 'SCI论文专项'),
    ],
    'cn': [
        ('check_quality.py', ['--type', 'cn'], '通用质量'),
        ('check_references.py', ['--type', 'cn'], '参考文献'),
        ('check_paper.py', ['--type', 'cn'], 'CN论文专项'),
    ],
    'pat': [
        ('check_quality.py', ['--type', 'pat'], '通用质量'),
        ('check_patent.py', [], '发明专利专项'),
    ],
    'bk': [
        ('check_quality.py', ['--type', 'bk'], '通用质量'),
        ('check_references.py', ['--type', 'bk'], '参考文献'),
        ('check_readability.py', [], 'BK可读性专项'),
    ],
    'rpt': [
        ('check_quality.py', ['--type', 'rpt'], '通用质量'),
        ('check_references.py', ['--type', 'rpt'], '参考文献'),
    ],
    'std-cn': [
        ('check_quality.py', ['--type', 'std'], '通用质量'),
        ('check_references.py', ['--type', 'std'], '参考文献'),
        ('check_standard.py', ['--type', 'cn'], '国内标准合规'),
    ],
    'std-int': [
        ('check_quality.py', ['--type', 'std'], '通用质量'),
        ('check_references.py', ['--type', 'std'], '参考文献'),
        ('check_standard.py', ['--type', 'int'], '国际标准合规'),
    ],
    'wx': [
        ('check_article.py', [], '公众号文章专项'),
    ],
    'ppt': [
        ('check_ppt.py', [], 'PPT专项'),
    ],
}

# 文档类型自动检测关键词
TYPE_PATTERNS = {
    'sci': [r'\\begin\{abstract\}', r'Introduction.*Conclusion', r'References\b', r'(?i)abstract.*keywords'],
    'cn': [r'摘\s*要', r'关键词', r'参考文献', r'中图分类号'],
    'pat': [r'权利要求书', r'说明书摘要', r'技术领域', r'背景技术'],
    'bk': [r'第[一二三四五]部分', r'本节小结', r'思考与讨论', r'概念速览'],
    'rpt': [r'执行摘要', r'技术方案', r'验收报告', r'可研报告'],
    'std-cn': [r'GB/T\s+\d', r'SL/T\s+\d', r'规范性引用文件', r'本文件适用'],
    'std-int': [r'(?i)normative references', r'(?i)scope.*this document', r'(?i)terms and definitions', r'(?i)shall\b'],
    'wx': [r'#\s+[^\n]+\n\n>', r'点击.*关注', r'原创声明'],
    'ppt': [r'slide\s*\d', r'(?i)transition', r'演示文稿', r'备注'],
}


def detect_type(filepath):
    """自动检测文档类型。"""
    with open(filepath, encoding='utf-8') as f:
        text = f.read(10000)  # Read first 10k chars

    scores = {}
    for dtype, patterns in TYPE_PATTERNS.items():
        score = sum(1 for p in patterns if re.search(p, text))
        if score > 0:
            scores[dtype] = score

    if not scores:
        return None

    return max(scores, key=scores.get)


def run_script(script_name, filepath, extra_args, label, verbose=False):
    """运行单个检查脚本，返回 (success, output)。"""
    script_path = os.path.join(SCRIPT_DIR, script_name)
    if not os.path.exists(script_path):
        return None, f"⚠️ 脚本不存在: {script_name}"

    cmd = [sys.executable, script_path, filepath] + extra_args
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=60
        )
        output = result.stdout + result.stderr
        success = result.returncode == 0

        # Count issues
        red = output.count('❌') + output.count('🔴')
        yellow = output.count('🟡')
        green = output.count('✅') + output.count('🟢')

        return {
            'success': success,
            'red': red,
            'yellow': yellow,
            'green': green,
            'output': output if verbose else '',
            'returncode': result.returncode,
        }, None
    except subprocess.TimeoutExpired:
        return None, f"⏰ 超时: {script_name}"
    except Exception as e:
        return None, f"💥 错误: {script_name}: {e}"


def main():
    import argparse
    parser = argparse.ArgumentParser(description='统一质量检查调度器')
    parser.add_argument('file', help='待检查的文档文件')
    parser.add_argument('--type', dest='dtype', help='文档类型 (sci/cn/pat/bk/rpt/std-cn/std-int/wx/ppt)')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示每个脚本的详细输出')
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"❌ 文件不存在: {args.file}")
        sys.exit(1)

    # 检测或使用指定类型
    dtype = args.dtype
    if not dtype:
        dtype = detect_type(args.file)
        if not dtype:
            print("⚠️ 无法自动检测文档类型，请使用 --type 指定")
            print(f"   支持类型: {', '.join(CHECK_MATRIX.keys())}")
            sys.exit(1)

    dtype = dtype.lower()
    if dtype not in CHECK_MATRIX:
        print(f"❌ 不支持的文档类型: {dtype}")
        print(f"   支持类型: {', '.join(CHECK_MATRIX.keys())}")
        sys.exit(1)

    checks = CHECK_MATRIX[dtype]
    filesize = os.path.getsize(args.file)
    filename = os.path.basename(args.file)

    print(f"{'═' * 60}")
    print(f"  统一质量检查调度器 v1.0")
    print(f"  文件: {filename} ({filesize:,} bytes)")
    print(f"  类型: {dtype.upper()}")
    print(f"  检查脚本: {len(checks)}个")
    print(f"{'═' * 60}")

    total_red = 0
    total_yellow = 0
    total_green = 0
    results = []

    for script, extra_args, label in checks:
        print(f"\n{'─' * 40}")
        print(f"  ▶ {label} ({script})")
        print(f"{'─' * 40}")

        t0 = time.time()
        result, error = run_script(script, args.file, extra_args, label, args.verbose)
        elapsed = time.time() - t0

        if error:
            print(f"  {error}")
            results.append((label, 'error', 0, 0, 0))
        elif result:
            status = "✅ 通过" if result['red'] == 0 else f"❌ {result['red']}项问题"
            print(f"  {status} | 🟢{result['green']} 🟡{result['yellow']} 🔴{result['red']} | {elapsed:.1f}s")
            if args.verbose and result['output']:
                for line in result['output'].strip().split('\n'):
                    print(f"    {line}")
            total_red += result['red']
            total_yellow += result['yellow']
            total_green += result['green']
            results.append((label, 'ok', result['red'], result['yellow'], result['green']))

    # Summary
    print(f"\n{'═' * 60}")
    print(f"  汇总报告")
    print(f"{'═' * 60}")
    for label, status, red, yellow, green in results:
        icon = '✅' if red == 0 and status == 'ok' else '⚠️' if status == 'error' else '❌'
        print(f"  {icon} {label}: 🔴{red} 🟡{yellow} 🟢{green}")

    print(f"\n  总计: 🔴{total_red} 🟡{total_yellow} 🟢{total_green}")

    if total_red == 0:
        print(f"  ✅ 全部通过，可进入评审阶段")
    else:
        print(f"  ❌ 有{total_red}项🔴问题需修复后再评审")

    print(f"{'═' * 60}")
    sys.exit(0 if total_red == 0 else 1)


if __name__ == '__main__':
    main()
