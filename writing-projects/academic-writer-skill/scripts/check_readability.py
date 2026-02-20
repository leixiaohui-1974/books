#!/usr/bin/env python3
"""check_readability.py — BK专著可读性自动检查（v04经验总结）

Usage:
    python3 check_readability.py report_full_assembled.md

检查项:
  1. 超长段落（>400字，含位置定位）
  2. 跨学科术语首次释义率
  3. 概念速览框数量
  4. 章末小结格式（### §x.x + ---分隔线）
  5. 思考题覆盖率（每节L1-L4）
  6. 图表前后空行
  7. 参考文献统计（总数/近5年/英文/自引）
  8. 各部分字数平衡
"""

import re
import sys
import os


def check_long_paragraphs(text, threshold=400):
    """检查超长段落。"""
    lines = text.split('\n')
    issues = []
    buf = ""
    buf_start = 0
    for i, line in enumerate(lines):
        s = line.strip()
        if s == '':
            if len(buf) > threshold and not buf.startswith('>') and not buf.startswith('|') and not buf.startswith('#') and not buf.startswith('['):
                issues.append((buf_start + 1, i + 1, len(buf), buf[:60]))
            buf = ""
            buf_start = i + 1
        else:
            if not buf:
                buf_start = i
            buf += s
    return issues


def check_term_annotations(text):
    """检查跨学科术语是否有首次释义。"""
    TERMS = [
        '圣维南方程', '贝叶斯', '鲁棒', '过拟合', '拉格朗日',
        '状态空间', '传递函数', '遗传算法', '粒子群', '知识图谱',
        '自编码器', '闭环', '开环', '稳态误差', '相位裕度',
        '凸优化', '启发式', '卡尔曼', '李雅普诺夫', '马尔可夫',
    ]
    annotated = 0
    missing = []
    for term in TERMS:
        idx = text.find(term)
        if idx >= 0:
            context = text[idx:idx + len(term) + 50]
            if '（' in context[:len(term) + 10] or re.search(r'[a-zA-Z]', context[:len(term) + 20]):
                annotated += 1
            else:
                missing.append(term)
    return annotated, missing


def check_concept_boxes(text):
    """检查概念速览框。"""
    return re.findall(r'📖.*?速览', text)


def check_section_summaries(text):
    """检查章末小结格式。"""
    proper = len(re.findall(r'### §[\d.]+ 本节小结', text))
    with_sep = len(re.findall(r'---\s*\n\s*### §[\d.]+ 本节小结', text))
    legacy = len(re.findall(r'\*\*§[\d.]+ 本节小结\*\*', text))
    return proper, with_sep, legacy


def check_questions(text):
    """检查思考题。"""
    q_count = len(re.findall(r'^\d+\.\s*（', text, re.M))
    q_sections = len(re.findall(r'\*\*思考与讨论\*\*', text))
    levels = {
        'L1概念': len(re.findall(r'（概念理解）', text)),
        'L2计算': len(re.findall(r'（计算练习）', text)),
        'L3分析': len(re.findall(r'（分析[比较|应用]）', text)),
        'L4综合': len(re.findall(r'（综合[设计|应用|思考]）', text)),
        'L3批判': len(re.findall(r'（批判思考）', text)),
        'L4开放': len(re.findall(r'（开放讨论）', text)),
        'L3数据': len(re.findall(r'（数据分析）', text)),
    }
    return q_count, q_sections, levels


def check_figure_spacing(text):
    """检查图表引用块前后空行。"""
    issues = 0
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('> **图 ') or line.startswith('> **表 ') or line.startswith('> **概念辨析'):
            if i > 0 and lines[i - 1].strip() != '' and not lines[i - 1].startswith('>'):
                issues += 1
    return issues


def check_references(text):
    """检查参考文献统计。"""
    refs = re.findall(r'^\[\d+\](.+)', text, re.M)
    total = len(refs)
    recent = sum(1 for r in refs if re.search(r'\((\d{4})\)', r) and int(re.search(r'\((\d{4})\)', r).group(1)) >= 2021)
    en = sum(1 for r in refs if len(re.findall(r'[\u4e00-\u9fff]', r)) < 5)
    self_cite = sum(1 for r in refs if 'Lei' in r)
    return total, recent, en, self_cite


def check_part_balance(text):
    """检查各部分字数平衡。"""
    parts = {}
    markers = [
        (r'# 第一部分', r'# 第二部分', '第一部分'),
        (r'# 第二部分', r'# 第三部分', '第二部分'),
        (r'# 第三部分', r'# 第四部分', '第三部分'),
        (r'# 第四部分', r'## 术语表|## Glossary', '第四部分'),
    ]
    for sp, ep, name in markers:
        s = re.search(sp, text)
        e = re.search(ep, text)
        if s and e:
            parts[name] = len(text[s.start():e.start()])
    return parts


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 check_readability.py <markdown_file>")
        sys.exit(1)

    filepath = sys.argv[1]
    with open(filepath, encoding='utf-8') as f:
        text = f.read()

    chars = len(text)
    print(f"{'═' * 60}")
    print(f"  BK专著可读性自动检查报告")
    print(f"  文件: {os.path.basename(filepath)} ({chars:,}字符)")
    print(f"{'═' * 60}")

    # 1. 超长段落
    long_paras = check_long_paragraphs(text)
    status = "✅" if len(long_paras) == 0 else "❌"
    print(f"\n{status} 1. 超长段落(>400字): {len(long_paras)}处")
    for start, end, length, preview in long_paras[:5]:
        print(f"     L{start}-{end}: {length}字 | {preview}...")

    # 2. 术语释义
    annotated, missing = check_term_annotations(text)
    status = "✅" if len(missing) <= 3 else "🟡" if len(missing) <= 8 else "❌"
    print(f"\n{status} 2. 术语首次释义: {annotated}个已标注, {len(missing)}个缺失")
    if missing:
        print(f"     缺失: {', '.join(missing[:10])}")

    # 3. 概念速览框
    boxes = check_concept_boxes(text)
    status = "✅" if len(boxes) >= 5 else "🟡" if len(boxes) >= 3 else "❌"
    print(f"\n{status} 3. 概念速览框: {len(boxes)}个")

    # 4. 章末小结
    proper, with_sep, legacy = check_section_summaries(text)
    total_summaries = proper + legacy
    status = "✅" if proper >= 15 and with_sep >= 15 else "🟡"
    print(f"\n{status} 4. 章末小结: {proper}处(###格式) + {legacy}处(旧格式), {with_sep}处有分隔线")

    # 5. 思考题
    q_count, q_sections, levels = check_questions(text)
    status = "✅" if q_count >= 40 else "🟡" if q_count >= 20 else "❌"
    print(f"\n{status} 5. 思考题: {q_count}道, 覆盖{q_sections}节")
    for k, v in levels.items():
        if v > 0:
            print(f"     {k}: {v}道")

    # 6. 图表间距
    spacing_issues = check_figure_spacing(text)
    status = "✅" if spacing_issues == 0 else "🟡"
    print(f"\n{status} 6. 图表前缺空行: {spacing_issues}处")

    # 7. 参考文献
    total, recent, en, self_cite = check_references(text)
    r_pct = recent / total * 100 if total else 0
    e_pct = en / total * 100 if total else 0
    s_pct = self_cite / total * 100 if total else 0
    print(f"\n{'✅' if total >= 200 else '❌'} 7. 参考文献: {total}条")
    print(f"   {'✅' if r_pct >= 35 else '🟡'} 近5年: {recent}条 ({r_pct:.0f}%) [目标≥35%]")
    print(f"   {'✅' if e_pct >= 50 else '🟡'} 英文: {en}条 ({e_pct:.0f}%) [目标≥50%]")
    print(f"   {'✅' if s_pct <= 15 else '🟡'} 自引: {self_cite}条 ({s_pct:.0f}%) [上限15%]")

    # 8. 部分平衡
    parts = check_part_balance(text)
    print(f"\n📊 8. 各部分平衡:")
    for name, c in parts.items():
        pct = c / chars * 100
        flag = "🟡" if pct < 12 or pct > 35 else "✅"
        print(f"   {flag} {name}: {c:,}字符 ({pct:.1f}%)")

    # Summary
    score = 10
    if len(long_paras) > 0:
        score -= min(2, len(long_paras) * 0.2)
    if len(missing) > 5:
        score -= 1
    if len(boxes) < 3:
        score -= 1
    if q_count < 20:
        score -= 1
    if total < 200:
        score -= 1
    if r_pct < 35:
        score -= 0.5

    print(f"\n{'═' * 60}")
    print(f"  可读性评估: {score:.1f}/10")
    print(f"{'═' * 60}")


if __name__ == '__main__':
    main()
