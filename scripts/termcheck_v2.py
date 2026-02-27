#!/usr/bin/env python3
"""
CHS 术语与质量检查脚本 v2 (termcheck_v2)

功能升级（vs v1）:
  - 批量扫描: 支持目录参数，递归处理所有 .md 文件
  - 交叉引用验证: 检查"见第X章§Y.Z"是否指向实际存在的章节
  - 参考文献编号连续性: [X-Y] 编号无缺失/重复
  - 图表编号一致性: 图X-Y/表X-Y 中 X 必须等于章号
  - 公式编号一致性: (X-Y) 中 X 必须等于章号
  - JSON 输出: 支持 --json 参数输出 JSON 格式报告
  - 完整术语表: 全量 CHS 术语检查

用法:
  python3 termcheck_v2.py <文件或目录>              # 人类可读输出
  python3 termcheck_v2.py <文件或目录> --json        # JSON 输出
  python3 termcheck_v2.py <目录> --book T2-CN        # 指定书名前缀
  python3 termcheck_v2.py <文件> --verbose           # 显示详细行号
"""

import re
import sys
import json
import os
from pathlib import Path
from collections import defaultdict

# ============================================================
# 术语规范定义 (来自 CLAUDE.md §5.1 + §H)
# ============================================================

STANDARD_TERMS = {
    '水系统控制论': {
        'english': 'Cybernetics of Hydro Systems (CHS)',
        'forbidden': ['水控制学', '水系统论', '水网控制学'],
    },
    '水网自主等级': {
        'english': 'Water Network Autonomy Levels (WNAL)',
        'forbidden': ['水网自动化等级', '水利自主等级', '水网自动驾驶等级'],
    },
    '运行设计域': {
        'english': 'Operational Design Domain (ODD)',
        'forbidden': ['操作设计域', '运行设计范围'],
    },
    '安全包络': {
        'english': 'Safety Envelope',
        'forbidden': ['安全域'],
    },
    '物理AI引擎': {
        'english': 'Physical AI Engine',
        'forbidden': ['物理引擎', '机理模型引擎'],
    },
    '认知AI引擎': {
        'english': 'Cognitive AI Engine',
        'forbidden': ['知识引擎', '决策引擎'],
    },
    '分层分布式控制': {
        'english': 'Hierarchical Distributed Control (HDC)',
        'forbidden': ['分级控制', '集散控制'],
    },
    '多智能体系统': {
        'english': 'Multi-Agent System (MAS)',
        'forbidden': ['多代理系统'],
    },
    '在环测试': {
        'english': 'In-the-Loop Testing',
        'forbidden': ['闭环测试'],
    },
    '水网操作系统': {
        'english': 'Water Network Operating System (HydroOS)',
        'forbidden': ['水利操作系统', '水务OS'],
    },
    '瀚铎水网大模型': {
        'english': 'HanDuo Water Network Large Model',
        'forbidden': ['翰铎', 'HanDo'],
    },
    '模型预测控制': {
        'english': 'Model Predictive Control (MPC)',
        'forbidden': [],
    },
    '传递函数': {
        'english': 'Transfer Function',
        'forbidden': ['传递矩阵'],
    },
    '降阶模型': {
        'english': 'Reduced-Order Model (ROM)',
        'forbidden': ['简化模型'],
    },
    'SCADA+MAS融合架构': {
        'english': 'SCADA+MAS Fusion Architecture',
        'forbidden': ['SCADA/MAS混合'],
    },
}

# WNAL 错误表述
WNAL_WRONG = {
    'WSAL': '应使用 WNAL (Water Network Autonomy Levels)',
    '水网自动驾驶等级': '应使用"水网自主等级 (WNAL)"',
    '水网自动化等级': '应使用"水网自主等级 (WNAL)"',
}

# 工程名称一致性
ENGINEERING_TERMS = {
    '沙坪水电站': ['沙坪电站', '沙坪水电厂'],
    '胶东调水': ['胶东调水工程', '胶东工程'],
    '大渡河': [],
}

# ============================================================
# 章号提取
# ============================================================

def extract_chapter_num(filepath):
    """从文件名提取章号数字，如 ch05_final.md -> 5, ch10_大渡河接力赛.md -> 10"""
    fname = Path(filepath).stem
    m = re.match(r'ch(\d+)', fname)
    if m:
        return int(m.group(1))
    return None


def find_all_chapters(directory):
    """找到目录下所有章节文件，返回章号集合"""
    chapters = set()
    p = Path(directory)
    for f in p.glob('ch*.md'):
        # 排除 _v1, _backup 等版本文件
        if '_v1' in f.name or '_backup' in f.name:
            continue
        ch = extract_chapter_num(f)
        if ch is not None:
            chapters.add(ch)
    return chapters


# ============================================================
# 检查函数
# ============================================================

def check_terminology(content, filepath):
    """检查术语使用规范性"""
    issues = []
    lines = content.split('\n')

    # 1. 检查禁止别名
    for correct, info in STANDARD_TERMS.items():
        for wrong in info['forbidden']:
            for i, line in enumerate(lines, 1):
                if wrong in line:
                    issues.append({
                        'type': '术语',
                        'severity': 'Critical' if correct in ['水系统控制论', '水网自主等级', '瀚铎水网大模型'] else 'Major',
                        'location': f'第{i}行',
                        'description': f'检测到禁止别名「{wrong}」',
                        'current_text': line.strip()[:100],
                        'suggested_fix': f'应使用「{correct}」({info["english"]})',
                    })

    # 2. WNAL 错误表述
    for wrong, suggestion in WNAL_WRONG.items():
        for i, line in enumerate(lines, 1):
            if wrong in line:
                issues.append({
                    'type': '术语',
                    'severity': 'Major',
                    'location': f'第{i}行',
                    'description': f'检测到错误表述「{wrong}」',
                    'current_text': line.strip()[:100],
                    'suggested_fix': suggestion,
                })

    # 3. 工程名称一致性
    for standard, variants in ENGINEERING_TERMS.items():
        for variant in variants:
            for i, line in enumerate(lines, 1):
                if variant in line and standard not in line:
                    issues.append({
                        'type': '术语',
                        'severity': 'Minor',
                        'location': f'第{i}行',
                        'description': f'工程名称不统一：「{variant}」',
                        'current_text': line.strip()[:100],
                        'suggested_fix': f'建议统一使用「{standard}」',
                    })

    return issues


def check_cross_references(content, filepath, available_chapters):
    """检查交叉引用的正确性"""
    issues = []
    lines = content.split('\n')
    ch_num = extract_chapter_num(filepath)

    # 跨书引用书名模式（引用其他书时不按本书章节校验）
    cross_book_names = [
        '《水系统控制论》', '《水网觉醒》', '《建模与控制》', '《智能与自主》',
        '《明渠水动力降阶建模》', '《水网预测控制》', '《水网运行安全包络》',
        '《水网多智能体系统》', '《水利认知智能》', '《水网控制在环验证》',
    ]

    # 模式1: "见第X章" / "第X章" / "参见第X章"
    pattern_cn = re.compile(r'(?:见|参见|详见)?第([一二三四五六七八九十百零\d]+)章')
    cn_num_map = {
        '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
        '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
        '十一': 11, '十二': 12, '十三': 13, '十四': 14, '十五': 15,
    }

    in_code_block = False
    for i, line in enumerate(lines, 1):
        # 跟踪代码块
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue
        if in_code_block or line.strip().startswith('<!--'):
            continue

        for m in pattern_cn.finditer(line):
            ref_text = m.group(1)
            # 转换中文数字
            ref_num = cn_num_map.get(ref_text)
            if ref_num is None:
                try:
                    ref_num = int(ref_text)
                except ValueError:
                    continue

            # 检查是否为跨书引用（引用前30个字符内出现其他书名）
            start_ctx = max(0, m.start() - 50)
            context_before = line[start_ctx:m.start()]
            is_cross_book = any(bname in context_before for bname in cross_book_names)

            if is_cross_book:
                # 跨书引用，仅记录为 Info（不校验本书章节）
                continue

            if available_chapters and ref_num not in available_chapters:
                issues.append({
                    'type': '交叉引用',
                    'severity': 'Critical',
                    'location': f'第{i}行',
                    'description': f'引用"第{ref_text}章"但该章不存在（可用章节: {sorted(available_chapters)}）',
                    'current_text': line.strip()[:100],
                    'suggested_fix': '修正章号引用或确认目标章节存在',
                })

    # 模式2: §X.Y 格式
    pattern_section = re.compile(r'§(\d+)\.(\d+)')
    in_code_block = False
    in_cross_book_block = False  # 追踪引用块是否提到了其他书名
    for i, line in enumerate(lines, 1):
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        # 追踪 blockquote 块中的跨书上下文
        if line.strip().startswith('>'):
            if any(bname in line for bname in cross_book_names):
                in_cross_book_block = True
        else:
            # 离开 blockquote 块时重置
            in_cross_book_block = False

        for m in pattern_section.finditer(line):
            ref_ch = int(m.group(1))
            # 检查是否为跨书引用（同行或同块中已提到其他书名）
            start_ctx = max(0, m.start() - 50)
            context_before = line[start_ctx:m.start()]
            is_cross_book = any(bname in context_before for bname in cross_book_names)
            if is_cross_book or in_cross_book_block:
                continue

            if available_chapters and ref_ch not in available_chapters:
                issues.append({
                    'type': '交叉引用',
                    'severity': 'Major',
                    'location': f'第{i}行',
                    'description': f'引用 §{ref_ch}.{m.group(2)} 但第{ref_ch}章不存在',
                    'current_text': line.strip()[:100],
                    'suggested_fix': '修正节号引用',
                })

    return issues


def check_reference_numbering(content, filepath):
    """检查参考文献编号的连续性和唯一性"""
    issues = []
    ch_num = extract_chapter_num(filepath)
    if ch_num is None:
        return issues

    lines = content.split('\n')

    # 查找 [X-Y] 格式的参考文献引用
    ref_pattern = re.compile(r'\[(\d+)-(\d+)\]')
    ref_numbers = defaultdict(list)  # {chapter: [(seq, line_num), ...]}

    for i, line in enumerate(lines, 1):
        for m in ref_pattern.finditer(line):
            ref_ch = int(m.group(1))
            ref_seq = int(m.group(2))
            ref_numbers[ref_ch].append((ref_seq, i))

    # 检查引用的章号是否匹配当前章
    for ref_ch, refs in ref_numbers.items():
        if ref_ch != ch_num:
            # 可能是跨章引用，标记为 Minor
            for seq, line_num in refs:
                issues.append({
                    'type': '参考文献',
                    'severity': 'Minor',
                    'location': f'第{line_num}行',
                    'description': f'参考文献 [{ref_ch}-{seq}] 章号({ref_ch})与当前章号({ch_num})不匹配',
                    'current_text': '',
                    'suggested_fix': f'如果是本章参考文献，章号应为 [{ch_num}-{seq}]',
                })

    # 检查本章参考文献编号连续性
    if ch_num in ref_numbers:
        seqs = sorted(set(s for s, _ in ref_numbers[ch_num]))
        if seqs:
            max_seq = max(seqs)
            missing = set(range(1, max_seq + 1)) - set(seqs)
            if missing:
                issues.append({
                    'type': '参考文献',
                    'severity': 'Major',
                    'location': '全章',
                    'description': f'参考文献编号不连续，缺失: [{ch_num}-{sorted(missing)}]',
                    'current_text': f'已使用编号: {seqs}',
                    'suggested_fix': '补充缺失的参考文献编号或重新编号',
                })

            # 检查重复引用定义（在参考文献列表中）
            # 仅计算以 [X-Y] 开头的行作为定义行（排除文本中的引用）
            ref_def_pattern = re.compile(rf'^\s*\[{ch_num}-(\d+)\]')
            in_ref_section = False
            ref_defs = defaultdict(list)
            for i, line in enumerate(lines, 1):
                if re.match(r'^#+\s*参考文献', line) or re.match(r'^#+\s*References', line):
                    in_ref_section = True
                if in_ref_section:
                    m = ref_def_pattern.match(line)
                    if m:
                        ref_defs[int(m.group(1))].append(i)

            for seq, def_lines in ref_defs.items():
                if len(def_lines) > 1:
                    issues.append({
                        'type': '参考文献',
                        'severity': 'Critical',
                        'location': f'第{def_lines}行',
                        'description': f'参考文献 [{ch_num}-{seq}] 重复定义（出现在第{def_lines}行）',
                        'current_text': '',
                        'suggested_fix': '删除重复的参考文献定义或重新编号',
                    })

    return issues


def check_figure_table_numbering(content, filepath):
    """检查图表编号一致性"""
    issues = []
    ch_num = extract_chapter_num(filepath)
    if ch_num is None:
        return issues

    lines = content.split('\n')

    # 跨书引用书名模式
    cross_book_names = [
        '《水系统控制论》', '《水网觉醒》', '《建模与控制》', '《智能与自主》',
        '《明渠水动力降阶建模》', '《水网预测控制》', '《水网运行安全包络》',
    ]

    # 图编号: 图X-Y
    fig_pattern = re.compile(r'图(\d+)-(\d+)')
    # 表编号: 表X-Y
    table_pattern = re.compile(r'表(\d+)-(\d+)')

    fig_nums = []
    table_nums = []

    for i, line in enumerate(lines, 1):
        # 检测是否为跨书引用行（含其他书名，或在 > 深入阅读块中）
        is_cross_book_line = any(bname in line for bname in cross_book_names)

        # 图编号
        for m in fig_pattern.finditer(line):
            fig_ch = int(m.group(1))
            fig_seq = int(m.group(2))
            if fig_ch == ch_num:
                fig_nums.append(fig_seq)
            elif not is_cross_book_line:
                issues.append({
                    'type': '编号',
                    'severity': 'Critical',
                    'location': f'第{i}行',
                    'description': f'图{fig_ch}-{fig_seq} 的章号({fig_ch})与当前章号({ch_num})不匹配',
                    'current_text': line.strip()[:100],
                    'suggested_fix': f'应为 图{ch_num}-{fig_seq}',
                })

        # 表编号
        for m in table_pattern.finditer(line):
            tbl_ch = int(m.group(1))
            tbl_seq = int(m.group(2))
            if tbl_ch == ch_num:
                table_nums.append(tbl_seq)
            elif not is_cross_book_line:
                issues.append({
                    'type': '编号',
                    'severity': 'Critical',
                    'location': f'第{i}行',
                    'description': f'表{tbl_ch}-{tbl_seq} 的章号({tbl_ch})与当前章号({ch_num})不匹配',
                    'current_text': line.strip()[:100],
                    'suggested_fix': f'应为 表{ch_num}-{tbl_seq}',
                })

    # 检查图编号连续性
    if fig_nums:
        unique_figs = sorted(set(fig_nums))
        max_fig = max(unique_figs)
        missing_figs = set(range(1, max_fig + 1)) - set(unique_figs)
        if missing_figs:
            issues.append({
                'type': '编号',
                'severity': 'Major',
                'location': '全章',
                'description': f'图编号不连续，缺失: 图{ch_num}-{sorted(missing_figs)}',
                'current_text': f'已使用: {unique_figs}',
                'suggested_fix': '补充或重新编号',
            })

    # 检查表编号连续性
    if table_nums:
        unique_tables = sorted(set(table_nums))
        max_tbl = max(unique_tables)
        missing_tables = set(range(1, max_tbl + 1)) - set(unique_tables)
        if missing_tables:
            issues.append({
                'type': '编号',
                'severity': 'Major',
                'location': '全章',
                'description': f'表编号不连续，缺失: 表{ch_num}-{sorted(missing_tables)}',
                'current_text': f'已使用: {unique_tables}',
                'suggested_fix': '补充或重新编号',
            })

    return issues


def check_image_links(content, filepath):
    """检查图片链接有效性"""
    issues = []
    lines = content.split('\n')
    file_dir = Path(filepath).parent

    # Markdown 图片: ![alt](path)
    img_pattern = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')

    for i, line in enumerate(lines, 1):
        for m in img_pattern.finditer(line):
            alt_text = m.group(1)
            img_path = m.group(2)

            # 跳过 URL
            if img_path.startswith('http'):
                continue

            # 检查本地文件
            full_path = file_dir / img_path
            if not full_path.exists():
                # 也检查相对于 books/ 目录
                alt_path = file_dir.parent / img_path
                if not alt_path.exists():
                    issues.append({
                        'type': '格式',
                        'severity': 'Major',
                        'location': f'第{i}行',
                        'description': f'图片文件不存在: {img_path}',
                        'current_text': line.strip()[:100],
                        'suggested_fix': f'确认图片路径正确，或生成缺失图片',
                    })

    return issues


def check_markdown_format(content, filepath):
    """检查 Markdown 格式规范"""
    issues = []
    lines = content.split('\n')

    heading_levels = []
    in_code_block = False

    for i, line in enumerate(lines, 1):
        # 跟踪代码块
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue

        if in_code_block:
            continue

        # 检查标题层级跳跃 (h1 -> h3 跳过 h2)
        heading_match = re.match(r'^(#{1,6})\s+', line)
        if heading_match:
            level = len(heading_match.group(1))
            if heading_levels and level > heading_levels[-1] + 1:
                issues.append({
                    'type': '格式',
                    'severity': 'Minor',
                    'location': f'第{i}行',
                    'description': f'标题层级跳跃: 从 h{heading_levels[-1]} 跳到 h{level}',
                    'current_text': line.strip()[:80],
                    'suggested_fix': f'建议使用 h{heading_levels[-1]+1}',
                })
            heading_levels.append(level)

    return issues


def compute_stats(content, filepath):
    """计算文档统计信息"""
    lines = content.split('\n')
    char_count = len(content)
    line_count = len(lines)

    # 中文字数（粗略）
    cn_chars = len(re.findall(r'[\u4e00-\u9fff]', content))

    # 公式数
    formula_count = len(re.findall(r'\$\$', content)) // 2  # 双 $$ 对
    inline_formula = len(re.findall(r'(?<!\$)\$(?!\$)', content)) // 2

    # 图表数
    fig_count = len(re.findall(r'图\d+-\d+', content))
    table_count = len(re.findall(r'表\d+-\d+', content))
    img_count = len(re.findall(r'!\[[^\]]*\]\([^)]+\)', content))

    # 参考文献数
    ch_num = extract_chapter_num(filepath)
    ref_count = 0
    if ch_num:
        ref_count = len(set(re.findall(rf'\[{ch_num}-(\d+)\]', content)))

    return {
        'char_count': char_count,
        'line_count': line_count,
        'cn_char_count': cn_chars,
        'word_count_approx': cn_chars,  # 中文按字数计
        'formula_count': formula_count + inline_formula,
        'display_formula_count': formula_count,
        'figure_refs': fig_count,
        'table_refs': table_count,
        'image_links': img_count,
        'reference_count': ref_count,
    }


# ============================================================
# 主检查流程
# ============================================================

def check_single_file(filepath, available_chapters=None, book_name=''):
    """对单个文件执行全部检查"""
    filepath = str(filepath)
    content = Path(filepath).read_text(encoding='utf-8')
    ch_num = extract_chapter_num(filepath)

    all_issues = []

    # 1. 术语检查
    all_issues.extend(check_terminology(content, filepath))

    # 2. 交叉引用检查
    all_issues.extend(check_cross_references(content, filepath, available_chapters))

    # 3. 参考文献编号检查
    all_issues.extend(check_reference_numbering(content, filepath))

    # 4. 图表编号检查
    all_issues.extend(check_figure_table_numbering(content, filepath))

    # 5. 图片链接检查
    all_issues.extend(check_image_links(content, filepath))

    # 6. Markdown 格式检查
    all_issues.extend(check_markdown_format(content, filepath))

    # 统计信息
    stats = compute_stats(content, filepath)

    # 为每个 issue 添加文件信息和 ID
    for idx, issue in enumerate(all_issues, 1):
        issue['file'] = Path(filepath).name
        issue['chapter'] = f'ch{ch_num:02d}' if ch_num is not None else Path(filepath).stem
        if book_name:
            issue['id'] = f'CR-{book_name}-{issue["chapter"]}-{idx:03d}'
        else:
            issue['id'] = f'CR-{issue["chapter"]}-{idx:03d}'

    return {
        'file': filepath,
        'filename': Path(filepath).name,
        'chapter': ch_num,
        'stats': stats,
        'issues': all_issues,
        'summary': {
            'critical': len([i for i in all_issues if i['severity'] == 'Critical']),
            'major': len([i for i in all_issues if i['severity'] == 'Major']),
            'minor': len([i for i in all_issues if i['severity'] == 'Minor']),
            'total': len(all_issues),
        }
    }


def check_directory(dirpath, book_name='', file_pattern=None):
    """对目录中所有 .md 文件执行批量检查"""
    dirpath = Path(dirpath)

    # 找到所有章节文件
    if file_pattern:
        md_files = sorted(dirpath.glob(file_pattern))
    else:
        md_files = sorted(dirpath.glob('ch*.md'))

    # 排除备份和版本文件
    md_files = [f for f in md_files if '_v1' not in f.name and '_backup' not in f.name]

    if not md_files:
        print(f"WARNING: 在 {dirpath} 中未找到匹配的章节文件", file=sys.stderr)
        return {'files': [], 'overall': {}}

    # 获取可用章节列表
    available_chapters = find_all_chapters(dirpath)

    results = []
    for f in md_files:
        result = check_single_file(f, available_chapters, book_name)
        results.append(result)

    # 汇总统计
    overall = {
        'book': book_name,
        'directory': str(dirpath),
        'file_count': len(results),
        'total_issues': sum(r['summary']['total'] for r in results),
        'total_critical': sum(r['summary']['critical'] for r in results),
        'total_major': sum(r['summary']['major'] for r in results),
        'total_minor': sum(r['summary']['minor'] for r in results),
        'total_cn_chars': sum(r['stats']['cn_char_count'] for r in results),
        'total_formulas': sum(r['stats']['formula_count'] for r in results),
        'total_images': sum(r['stats']['image_links'] for r in results),
        'verdict': 'PASS' if sum(r['summary']['critical'] for r in results) == 0 else 'FAIL',
    }

    return {
        'files': results,
        'overall': overall,
    }


# ============================================================
# 输出格式化
# ============================================================

def print_human_report(report, verbose=False):
    """输出人类可读报告"""
    overall = report.get('overall', {})
    files = report.get('files', [])

    print(f"\n{'='*70}")
    print(f"  CHS 术语与质量检查报告 v2 (termcheck_v2)")
    print(f"{'='*70}")

    if overall:
        print(f"\n  书名: {overall.get('book', 'N/A')}")
        print(f"  目录: {overall.get('directory', 'N/A')}")
        print(f"  文件数: {overall.get('file_count', 0)}")
        print(f"  总字数: {overall.get('total_cn_chars', 0):,} 中文字")
        print(f"  总公式数: {overall.get('total_formulas', 0)}")
        print(f"  总图片数: {overall.get('total_images', 0)}")

    print(f"\n{'─'*70}")
    print(f"  问题汇总")
    print(f"{'─'*70}")

    if overall:
        crit = overall.get('total_critical', 0)
        major = overall.get('total_major', 0)
        minor = overall.get('total_minor', 0)
        print(f"  [Critical] {crit}  [Major] {major}  [Minor] {minor}  总计: {crit+major+minor}")
        print(f"  判定: {'FAIL - 存在Critical问题' if crit > 0 else 'PASS - 无Critical问题'}")

    for result in files:
        fname = result['filename']
        s = result['summary']
        st = result['stats']

        print(f"\n{'─'*70}")
        print(f"  {fname}  |  {st['cn_char_count']:,}字  |  C:{s['critical']} M:{s['major']} m:{s['minor']}")
        print(f"{'─'*70}")

        if not result['issues']:
            print(f"  (无问题)")
            continue

        # 按 severity 分组
        for severity in ['Critical', 'Major', 'Minor']:
            sev_issues = [i for i in result['issues'] if i['severity'] == severity]
            if not sev_issues:
                continue

            tag = {'Critical': '[!]', 'Major': '[*]', 'Minor': '[-]'}[severity]
            for issue in sev_issues:
                print(f"  {tag} {issue['id']} [{issue['type']}] {issue['location']}")
                print(f"      {issue['description']}")
                if verbose and issue.get('current_text'):
                    print(f"      > {issue['current_text'][:80]}")
                print(f"      -> {issue['suggested_fix']}")

    print(f"\n{'='*70}")
    if overall.get('verdict') == 'PASS':
        print(f"  PASS: 无 Critical 问题，可进入下一步")
    else:
        print(f"  FAIL: 存在 Critical 问题，须修复后再继续")
    print(f"{'='*70}\n")


def output_json(report):
    """输出 JSON 报告"""
    print(json.dumps(report, ensure_ascii=False, indent=2))


# ============================================================
# CLI
# ============================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='CHS 术语与质量检查工具 v2',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 termcheck_v2.py books/T2-CN/                    # 检查T2-CN全部章节
  python3 termcheck_v2.py books/T1-CN/ --book T1-CN       # 指定书名
  python3 termcheck_v2.py books/T2-CN/ch06_安全第一.md     # 检查单文件
  python3 termcheck_v2.py books/T2-CN/ --json              # JSON输出
  python3 termcheck_v2.py books/T2-CN/ --json -o report.json  # 输出到文件
        """
    )
    parser.add_argument('path', help='要检查的文件或目录路径')
    parser.add_argument('--book', '-b', default='', help='书名前缀 (如 T1-CN, T2-CN)')
    parser.add_argument('--json', '-j', action='store_true', help='输出 JSON 格式')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细信息（含问题行原文）')
    parser.add_argument('--output', '-o', default='', help='输出到文件（默认标准输出）')
    parser.add_argument('--pattern', '-p', default='', help='文件匹配模式（如 ch*_final.md）')

    args = parser.parse_args()

    target = Path(args.path)
    if not target.exists():
        print(f"ERROR: 路径不存在: {args.path}", file=sys.stderr)
        sys.exit(1)

    # 自动推断书名
    book_name = args.book
    if not book_name:
        if 'T1-CN' in str(target):
            book_name = 'T1-CN'
        elif 'T2-CN' in str(target):
            book_name = 'T2-CN'
        elif 'T2a' in str(target):
            book_name = 'T2a'
        elif 'T2b' in str(target):
            book_name = 'T2b'

    if target.is_file():
        # 单文件模式
        parent_dir = target.parent
        available_chapters = find_all_chapters(parent_dir)
        result = check_single_file(target, available_chapters, book_name)
        report = {
            'files': [result],
            'overall': {
                'book': book_name,
                'directory': str(parent_dir),
                'file_count': 1,
                'total_issues': result['summary']['total'],
                'total_critical': result['summary']['critical'],
                'total_major': result['summary']['major'],
                'total_minor': result['summary']['minor'],
                'total_cn_chars': result['stats']['cn_char_count'],
                'total_formulas': result['stats']['formula_count'],
                'total_images': result['stats']['image_links'],
                'verdict': 'PASS' if result['summary']['critical'] == 0 else 'FAIL',
            }
        }
    elif target.is_dir():
        # 目录模式
        file_pattern = args.pattern if args.pattern else None
        report = check_directory(target, book_name, file_pattern)
    else:
        print(f"ERROR: {args.path} 既不是文件也不是目录", file=sys.stderr)
        sys.exit(1)

    # 输出
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            if args.json:
                json.dump(report, f, ensure_ascii=False, indent=2)
            else:
                # 重定向 stdout 到文件
                import io
                old_stdout = sys.stdout
                sys.stdout = f
                print_human_report(report, args.verbose)
                sys.stdout = old_stdout
        print(f"报告已保存到: {args.output}", file=sys.stderr)
    else:
        if args.json:
            output_json(report)
        else:
            print_human_report(report, args.verbose)

    # 退出码
    verdict = report.get('overall', {}).get('verdict', 'PASS')
    sys.exit(0 if verdict == 'PASS' else 1)


if __name__ == '__main__':
    main()
