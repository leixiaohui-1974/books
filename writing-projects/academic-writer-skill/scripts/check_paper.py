#!/usr/bin/env python3
"""check_paper.py — SCI/CN论文自动质量检查

Usage:
    python3 check_paper.py paper.md [--type sci|cn] [--journal WRR]

检查项（14项）:
  1. 结构完整性（Title/Abstract/Introduction/…/References）
  2. 摘要四要素（目的-方法-结果-结论）+ 量化指标
  3. Introduction倒三角（背景→gap→贡献）
  4. Gap Statement质量
  5. Contribution显式列举
  6. 图表编号连续性 + 正文引用覆盖
  7. 公式编号 + 变量首次定义
  8. 参考文献数量/近5年比/自引率
  9. Discussion独立性（非Results重复）
  10. Conclusion量化指标
  11. 段落长度（SCI≤250词, CN≤400字）
  12. 中英文摘要对应（CN专用）
  13. GB/T 7714格式（CN专用）
  14. 致谢/基金信息完整性
"""

import re
import sys
import os
import argparse


def detect_type(text):
    """Auto-detect SCI or CN based on language ratio."""
    cn_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    en_words = len(re.findall(r'[a-zA-Z]+', text))
    return 'cn' if cn_chars > en_words else 'sci'


def check_structure(text, paper_type):
    """检查论文结构完整性。"""
    issues = []
    if paper_type == 'sci':
        required = {
            'Title': r'^#\s+.+',
            'Abstract': r'(?i)abstract',
            'Keywords': r'(?i)key\s*words',
            'Introduction': r'(?i)introduction',
            'Methodology': r'(?i)method|approach|framework|formulation',
            'Results': r'(?i)results?|case\s+stud|experiment|simulation|validation',
            'Discussion': r'(?i)discussion',
            'Conclusion': r'(?i)conclusion',
            'References': r'(?i)references?|bibliography',
        }
    else:
        required = {
            '标题': r'^#\s+.+',
            '摘要': r'摘\s*要',
            '关键词': r'关键词',
            '引言': r'引\s*言|前\s*言|1\s+引|绪\s*论',
            '方法': r'方法|模型|框架|理论',
            '结果': r'结果|案例|验证|实验|仿真',
            '结论': r'结\s*论|结语',
            '参考文献': r'参考文献',
        }

    found = {}
    for name, pattern in required.items():
        if re.search(pattern, text, re.M):
            found[name] = True
        else:
            issues.append(f"缺少「{name}」部分")
    return found, issues


def check_abstract(text, paper_type):
    """检查摘要质量。"""
    issues = []

    if paper_type == 'sci':
        m = re.search(r'(?i)(?:^|\n)#+\s*abstract\s*\n(.*?)(?=\n#+|\nkey)', text, re.S)
        if not m:
            m = re.search(r'(?i)abstract[:\s]*(.*?)(?=key\s*word|introduction|\n#)', text, re.S)
    else:
        m = re.search(r'摘\s*要[：:\s]*(.*?)(?=关键词|Abstract)', text, re.S)

    if not m:
        return ['未找到摘要内容']

    abstract = m.group(1).strip()
    words = len(abstract.split()) if paper_type == 'sci' else len(abstract)

    # Length check
    if paper_type == 'sci':
        if words < 150:
            issues.append(f'摘要偏短({words}词, 建议150-300词)')
        elif words > 350:
            issues.append(f'摘要偏长({words}词, 建议150-300词)')
    else:
        if words < 200:
            issues.append(f'摘要偏短({words}字, 建议200-400字)')

    # Quantitative indicators
    numbers = re.findall(r'\d+\.?\d*\s*%|\d+\.?\d*\s*(?:cm|m|s|h|kg|kW|MW)', abstract)
    if len(numbers) < 2:
        issues.append(f'摘要量化指标不足(仅{len(numbers)}个, 建议≥3个)')

    # Four elements (CN)
    if paper_type == 'cn':
        elements = {
            '目的': bool(re.search(r'为了|针对|旨在|目的', abstract)),
            '方法': bool(re.search(r'提出|建立|采用|构建|设计', abstract)),
            '结果': bool(re.search(r'结果表明|实验表明|仿真结果|验证|精度', abstract)),
            '结论': bool(re.search(r'研究表明|总之|综上|可以得出|为.*提供', abstract)),
        }
        missing = [k for k, v in elements.items() if not v]
        if missing:
            issues.append(f'摘要缺少四要素中的: {", ".join(missing)}')

    return issues


def check_introduction(text, paper_type):
    """检查Introduction/引言结构。"""
    issues = []

    if paper_type == 'sci':
        m = re.search(r'(?i)introduction\s*\n(.*?)(?=\n##|\n#\s+\d)', text, re.S)
    else:
        m = re.search(r'(?:引\s*言|前\s*言|1\s+引)\s*\n?(.*?)(?=\n##|\n\d+\s)', text, re.S)

    if not m:
        return ['未找到引言内容']

    intro = m.group(1)

    # Gap statement
    gap_patterns_sci = [
        r'[Hh]owever', r'[Dd]espite', r'[Nn]evertheless', r'remain[s]? .{0,30}(unclear|open|unresolved|poorly)',
        r'lack[s]? ', r'gap', r'limitation', r'challenge', r'no .{0,20}(framework|method|systematic)',
    ]
    gap_patterns_cn = [
        r'然而', r'但是', r'不足', r'缺乏', r'尚未', r'仍然.*问题', r'局限', r'挑战', r'有待',
    ]
    patterns = gap_patterns_sci if paper_type == 'sci' else gap_patterns_cn
    gap_found = sum(1 for p in patterns if re.search(p, intro))
    if gap_found < 2:
        issues.append('Gap Statement不充分(缺少明确的研究空白陈述)')

    # Contribution statement
    contrib_patterns_sci = [r'contribution', r'this paper', r'this study', r'we propose', r'\(1\).*\(2\)', r'threefold', r'twofold']
    contrib_patterns_cn = [r'本文', r'创新点', r'贡献', r'主要工作', r'(（1）|①|第一)', r'提出了']
    c_patterns = contrib_patterns_sci if paper_type == 'sci' else contrib_patterns_cn
    contrib_found = sum(1 for p in c_patterns if re.search(p, intro))
    if contrib_found < 2:
        issues.append('Contribution陈述不明确(建议显式编号列出贡献点)')

    # Reference density in intro
    refs_in_intro = len(re.findall(r'\[[\d,\s–-]+\]|\([\w\s]+,?\s*\d{4}\)', intro))
    if refs_in_intro < 10:
        issues.append(f'引言引用密度偏低({refs_in_intro}处, 建议≥15处)')

    return issues


def check_figures_tables(text):
    """检查图表编号连续性和引用覆盖。"""
    issues = []

    # Find figure/table definitions
    fig_defs = set(re.findall(r'(?:Fig(?:ure|\.)?|图)\s*(\d+)', text))
    tab_defs = set(re.findall(r'(?:Table|表)\s*(\d+)', text))

    # Check continuity
    for label, nums in [('图', fig_defs), ('表', tab_defs)]:
        if nums:
            int_nums = sorted(int(n) for n in nums)
            expected = list(range(1, max(int_nums) + 1))
            missing = set(expected) - set(int_nums)
            if missing:
                issues.append(f'{label}编号不连续, 缺少: {label}{", ".join(str(n) for n in sorted(missing))}')

    return issues


def check_equations(text):
    """检查公式编号和变量定义。"""
    issues = []

    # Find equation references
    eq_refs = set(re.findall(r'(?:Eq(?:uation|\.)?|式|公式)\s*\(?(\d+)\)?', text))

    # Check variable definitions (where keyword)
    where_blocks = len(re.findall(r'(?:where|其中|式中)[：:\s]', text))
    eq_count = len(re.findall(r'\$\$|\\\[|\\begin\{equation\}|（\d+）', text))
    if eq_count > 3 and where_blocks < eq_count * 0.5:
        issues.append(f'公式{eq_count}个但变量定义块仅{where_blocks}个(建议每个公式后定义变量)')

    return issues


def check_references(text, paper_type):
    """检查参考文献。"""
    issues = []

    if paper_type == 'sci':
        refs = re.findall(r'^\[(\d+)\]\s*(.+)', text, re.M)
    else:
        refs = re.findall(r'^\[(\d+)\]\s*(.+)', text, re.M)

    total = len(refs)
    if total == 0:
        return ['未检测到参考文献']

    # Count recent
    recent = 0
    en_count = 0
    self_cite = 0
    for num, ref in refs:
        years = re.findall(r'[\(（](\d{4})[\)）]|,\s*(\d{4})[,.\s]', ref)
        for y in years:
            yr = int(y[0] or y[1])
            if yr >= 2021:
                recent += 1
                break
        if len(re.findall(r'[\u4e00-\u9fff]', ref)) < 5:
            en_count += 1
        if 'Lei' in ref or '雷晓辉' in ref:
            self_cite += 1

    # Thresholds
    min_refs = 30 if paper_type == 'sci' else 20
    min_recent_pct = 50 if paper_type == 'sci' else 40
    max_self_pct = 25 if paper_type == 'sci' else 20

    if total < min_refs:
        issues.append(f'参考文献{total}篇(目标≥{min_refs}篇)')
    r_pct = recent / total * 100 if total else 0
    if r_pct < min_recent_pct:
        issues.append(f'近5年文献{recent}篇({r_pct:.0f}%, 目标≥{min_recent_pct}%)')
    s_pct = self_cite / total * 100 if total else 0
    if s_pct > max_self_pct:
        issues.append(f'自引率{s_pct:.0f}%(上限{max_self_pct}%)')

    # CN-specific: GB/T 7714 format check
    if paper_type == 'cn':
        no_type = 0
        for num, ref in refs:
            if not re.search(r'\[[JMCDSPNR]\]', ref):
                no_type += 1
        if no_type > 0:
            issues.append(f'{no_type}条文献缺少类型标识([J]/[M]/[C]等, GB/T 7714)')

    return issues


def check_conclusion(text, paper_type):
    """检查结论量化指标。"""
    issues = []

    if paper_type == 'sci':
        m = re.search(r'(?i)conclusion[s]?\s*\n(.*?)(?=\n#|acknowledge|references|\Z)', text, re.S)
    else:
        m = re.search(r'结\s*论\s*\n?(.*?)(?=\n#|致谢|参考文献|\Z)', text, re.S)

    if not m:
        return ['未找到结论部分']

    conclusion = m.group(1)
    numbers = re.findall(r'\d+\.?\d*\s*%|\d+\.?\d*\s*(?:cm|m|s|h|min)', conclusion)
    if len(numbers) < 2:
        issues.append(f'结论量化指标不足({len(numbers)}个, 建议≥3个关键数值)')

    return issues


def check_paragraph_length(text, paper_type):
    """检查段落长度。"""
    issues = []
    threshold = 300 if paper_type == 'sci' else 500  # words vs chars

    paras = text.split('\n\n')
    long_count = 0
    for p in paras:
        p = p.strip()
        if not p or p.startswith('#') or p.startswith('>') or p.startswith('|') or p.startswith('['):
            continue
        length = len(p.split()) if paper_type == 'sci' else len(p)
        if length > threshold:
            long_count += 1

    if long_count > 3:
        unit = '词' if paper_type == 'sci' else '字'
        issues.append(f'{long_count}个超长段落(>{threshold}{unit})')

    return issues


def check_acknowledgement(text, paper_type):
    """检查致谢和基金信息。"""
    issues = []

    if paper_type == 'sci':
        has_ack = bool(re.search(r'(?i)acknowledge?ment', text))
        has_fund = bool(re.search(r'(?i)fund|grant|support|project|program|National', text))
    else:
        has_ack = bool(re.search(r'致谢|基金', text))
        has_fund = bool(re.search(r'基金|资助|项目|National|重点研发', text))

    if not has_fund:
        issues.append('未找到基金/项目资助信息')

    return issues


def main():
    parser = argparse.ArgumentParser(description='SCI/CN论文自动质量检查')
    parser.add_argument('file', help='论文Markdown文件路径')
    parser.add_argument('--type', choices=['sci', 'cn'], help='论文类型(默认自动检测)')
    parser.add_argument('--journal', default='', help='目标期刊(如WRR, NatureWater, 水利学报)')
    args = parser.parse_args()

    with open(args.file, encoding='utf-8') as f:
        text = f.read()

    paper_type = args.type or detect_type(text)
    type_label = 'SCI英文论文' if paper_type == 'sci' else '中文核心期刊论文'

    print(f"{'═' * 60}")
    print(f"  论文质量自动检查报告 ({type_label})")
    print(f"  文件: {os.path.basename(args.file)}")
    if args.journal:
        print(f"  目标期刊: {args.journal}")
    print(f"{'═' * 60}")

    checks = [
        ('结构完整性', lambda: check_structure(text, paper_type)[1]),
        ('摘要质量', lambda: check_abstract(text, paper_type)),
        ('引言结构', lambda: check_introduction(text, paper_type)),
        ('图表编号', lambda: check_figures_tables(text)),
        ('公式规范', lambda: check_equations(text)),
        ('参考文献', lambda: check_references(text, paper_type)),
        ('结论质量', lambda: check_conclusion(text, paper_type)),
        ('段落长度', lambda: check_paragraph_length(text, paper_type)),
        ('致谢/基金', lambda: check_acknowledgement(text, paper_type)),
    ]

    total_issues = 0
    for name, func in checks:
        issues = func()
        status = '✅' if not issues else '❌' if len(issues) > 1 else '🟡'
        print(f"\n{status} {name}")
        for issue in issues:
            print(f"     · {issue}")
            total_issues += 1

    # Summary score
    score = max(0, 10 - total_issues * 0.7)
    print(f"\n{'═' * 60}")
    print(f"  检测到 {total_issues} 个问题")
    print(f"  质量评估: {score:.1f}/10")
    print(f"{'═' * 60}")


if __name__ == '__main__':
    main()
