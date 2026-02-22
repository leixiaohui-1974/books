#!/usr/bin/env python3
"""
参考文献格式自动检查脚本
用法: python3 check_references.py <文件路径> [--type SCI|CN|BK|RPT|STD-CN|STD-INT|WX|PPT]
配合 references/citation_style_guide.md 使用

检查项:
1. 参考文献数量是否达标
2. GB/T 7714 格式规范(中文)
3. 正文引用与文献表的交叉一致性
4. 近5年文献占比
5. 自引率
6. 常见格式错误
7. 疑似编造文献检测
"""
import re
import sys
import argparse
from collections import Counter, defaultdict
from datetime import datetime

CURRENT_YEAR = datetime.now().year

# ============================================================
# 各文体的参考文献要求
# ============================================================
REF_REQUIREMENTS = {
    'SCI': {'min_count': 30, 'recent_5yr_ratio': 0.50, 'self_cite_range': (0.15, 0.25)},
    'CN':  {'min_count': 20, 'recent_5yr_ratio': 0.40, 'self_cite_range': (0.10, 0.20)},
    'BK':  {'min_count': 100, 'recent_5yr_ratio': 0.30, 'self_cite_range': (0.0, 0.15)},
    'RPT': {'min_count': 10, 'recent_5yr_ratio': None, 'self_cite_range': None},
    'STD-CN': {'min_count': 0, 'recent_5yr_ratio': None, 'self_cite_range': None},
    'STD-INT': {'min_count': 0, 'recent_5yr_ratio': None, 'self_cite_range': None},
    'WX':  {'min_count': 3, 'recent_5yr_ratio': None, 'self_cite_range': None},
    'PPT': {'min_count': 0, 'recent_5yr_ratio': None, 'self_cite_range': None},
    'PAT': {'min_count': 3, 'recent_5yr_ratio': None, 'self_cite_range': None},
}

# 自引作者关键词
SELF_CITE_AUTHORS = ['雷晓辉', 'Lei X', 'Lei, X', 'Xiaohui Lei']

# ============================================================
# 参考文献提取
# ============================================================

def extract_references_numbered(content):
    """提取顺序编码制参考文献 [1] [2] ..."""
    refs = []
    # 匹配 [数字] 开头的行（可能跨行）
    ref_section = re.search(r'(?:参考文献|References|Bibliography)(.*)', content, re.DOTALL | re.IGNORECASE)
    if not ref_section:
        return refs
    
    ref_text = ref_section.group(1)
    # 按 [数字] 切分
    entries = re.split(r'\n\s*\[(\d+)\]\s*', ref_text)
    
    for i in range(1, len(entries), 2):
        if i + 1 < len(entries):
            num = int(entries[i])
            text = entries[i + 1].strip().split('\n')[0]  # 取第一行
            if len(text) > 10:  # 过滤掉太短的
                refs.append({'num': num, 'text': text})
    
    return refs

def extract_references_author_year(content):
    """提取著者-出版年制参考文献"""
    refs = []
    ref_section = re.search(r'(?:参考文献|References|Bibliography)(.*)', content, re.DOTALL | re.IGNORECASE)
    if not ref_section:
        return refs
    
    ref_text = ref_section.group(1)
    lines = ref_text.strip().split('\n')
    current_ref = ''
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if current_ref:
                refs.append({'text': current_ref.strip()})
                current_ref = ''
            continue
        
        # 检查是否是新条目（以作者名开头）
        if re.match(r'^[A-Z\u4e00-\u9fff]', stripped) and not stripped.startswith(('http', 'doi', 'DOI')):
            if current_ref:
                refs.append({'text': current_ref.strip()})
            current_ref = stripped
        else:
            current_ref += ' ' + stripped
    
    if current_ref:
        refs.append({'text': current_ref.strip()})
    
    return refs

def extract_inline_citations_numbered(content):
    """提取正文中的顺序编码引用 [1] [2,3] [1-5]"""
    citations = set()
    # 单个引用
    for m in re.finditer(r'\[(\d+)\]', content):
        citations.add(int(m.group(1)))
    # 范围引用 [1-5]
    for m in re.finditer(r'\[(\d+)-(\d+)\]', content):
        for n in range(int(m.group(1)), int(m.group(2)) + 1):
            citations.add(n)
    # 多引用 [1,3,5]
    for m in re.finditer(r'\[([\d,\s]+)\]', content):
        for n in re.findall(r'\d+', m.group(1)):
            citations.add(int(n))
    return citations

def extract_inline_citations_author_year(content):
    """提取正文中的著者-出版年引用"""
    citations = set()
    # (Author, Year) 或 Author (Year)
    for m in re.finditer(r'[\(（]([^)）]+,\s*\d{4}[a-z]?)[\)）]', content):
        citations.add(m.group(1).strip())
    for m in re.finditer(r'(\w+)\s+\((\d{4}[a-z]?)\)', content):
        citations.add(f"{m.group(1)}, {m.group(2)}")
    return citations

# ============================================================
# 格式检查
# ============================================================

def extract_year(ref_text):
    """从参考文献条目中提取年份"""
    years = re.findall(r'(?:19|20)\d{2}', ref_text)
    if years:
        return int(years[-1])  # 取最后一个年份（通常是出版年）
    return None

def check_gbt7714_format(ref_text, ref_num=None):
    """检查单条参考文献是否符合GB/T 7714基本格式"""
    issues = []
    prefix = f'[{ref_num}] ' if ref_num else ''
    
    # 1. 检查文献类型标识 [J] [M] [C] [D] [P] [S] [R] [EB/OL]
    type_markers = re.findall(r'\[([A-Z/]+)\]', ref_text)
    if not type_markers:
        issues.append(f'{prefix}缺少文献类型标识（如[J]期刊/[M]专著/[C]会议/[D]学位论文/[S]标准/[R]报告）')
    
    # 2. 检查作者格式（中文：姓名逗号分隔；英文：姓在前）
    # 简单检查是否有作者部分
    first_period = ref_text.find('.')
    if first_period < 3:
        issues.append(f'{prefix}作者部分可能缺失或格式异常')
    
    # 3. 检查年份
    year = extract_year(ref_text)
    if not year:
        issues.append(f'{prefix}未检测到出版年份')
    elif year > CURRENT_YEAR + 1:
        issues.append(f'{prefix}年份异常({year})，超过当前年份')
    elif year < 1950:
        issues.append(f'{prefix}年份偏早({year})，请确认')
    
    # 4. 期刊论文检查
    if '[J]' in ref_text:
        # 检查是否有卷期页码
        if not re.search(r'\d+\(\d+\)|\d+:\s*\d+', ref_text):
            issues.append(f'{prefix}期刊论文缺少卷(期): 页码信息')
    
    # 5. 专著检查
    if '[M]' in ref_text:
        if '出版社' not in ref_text and 'Press' not in ref_text and 'Springer' not in ref_text and 'Elsevier' not in ref_text and 'Wiley' not in ref_text:
            issues.append(f'{prefix}专著缺少出版社信息')
    
    # 6. 标准检查
    if '[S]' in ref_text:
        if not re.search(r'GB|SL|ISO|IEC|IEEE', ref_text):
            issues.append(f'{prefix}标准文献缺少标准号')
    
    # 7. 标点检查
    if ref_text.count('..') > 0:
        issues.append(f'{prefix}出现连续句点(..)')
    
    return issues

def check_numbering_continuity(refs):
    """检查编号连续性"""
    issues = []
    if not refs:
        return issues
    
    nums = sorted(set(r.get('num', 0) for r in refs if r.get('num')))
    if nums and nums[0] != 1:
        issues.append(f'参考文献编号未从[1]开始（起始为[{nums[0]}]）')
    
    for i in range(len(nums) - 1):
        if nums[i + 1] - nums[i] > 1:
            issues.append(f'编号不连续: [{nums[i]}]后跳至[{nums[i+1]}]')
    
    return issues

def check_cross_consistency(inline_citations, ref_nums):
    """检查正文引用与文献表的交叉一致性"""
    issues = []
    
    # 正文中引用了但文献表中没有
    cited_not_listed = inline_citations - ref_nums
    if cited_not_listed:
        issues.append(f'正文引用了但文献表中不存在: {sorted(cited_not_listed)[:10]}')
    
    # 文献表中有但正文未引用
    listed_not_cited = ref_nums - inline_citations
    if listed_not_cited:
        issues.append(f'文献表中存在但正文未引用: {sorted(listed_not_cited)[:10]}')
    
    return issues

def check_self_citation_rate(refs):
    """计算自引率"""
    total = len(refs)
    if total == 0:
        return 0.0, 0
    
    self_count = 0
    for ref in refs:
        text = ref.get('text', '')
        if any(author in text for author in SELF_CITE_AUTHORS):
            self_count += 1
    
    return self_count / total, self_count

def check_recent_ratio(refs, years_back=5):
    """计算近N年文献占比"""
    total = len(refs)
    if total == 0:
        return 0.0, 0
    
    cutoff = CURRENT_YEAR - years_back
    recent = 0
    for ref in refs:
        year = extract_year(ref.get('text', ''))
        if year and year >= cutoff:
            recent += 1
    
    return recent / total, recent

def check_suspicious_refs(refs):
    """检测疑似编造的参考文献"""
    issues = []
    
    for ref in refs:
        text = ref.get('text', '')
        num = ref.get('num', '?')
        
        # 1. 过于模糊的条目
        if len(text) < 30:
            issues.append(f'[{num}] 条目过短({len(text)}字)，可能不完整')
        
        # 2. 含有占位符
        placeholders = ['xxx', 'XXX', '待补充', 'TODO', 'TBD', '需核实']
        for ph in placeholders:
            if ph in text:
                issues.append(f'[{num}] 含有占位符"{ph}"')
        
        # 3. 重复条目检测
        # (简单的文本相似度)
    
    # 检查重复
    texts = [ref.get('text', '')[:50] for ref in refs]
    text_counts = Counter(texts)
    for text, count in text_counts.items():
        if count > 1 and text:
            issues.append(f'疑似重复条目({count}次): "{text}..."')
    
    return issues

# ============================================================
# 标准引用专项检查
# ============================================================

def check_normative_references(content, std_type='cn'):
    """检查标准文件的规范性引用"""
    issues = []
    
    if std_type == 'cn':
        section_match = re.search(r'(?:2\s+)?规范性引用文件(.*?)(?=^3\s|\Z)', content, re.DOTALL | re.MULTILINE)
    else:
        section_match = re.search(r'(?:2\s+)?Normative references(.*?)(?=^3\s|\Z)', content, re.DOTALL | re.MULTILINE)
    
    if not section_match:
        issues.append('未找到规范性引用文件章节')
        return issues
    
    norm_text = section_match.group(1)
    
    # 提取标准号
    if std_type == 'cn':
        standards = re.findall(r'((?:GB|SL|DL|HJ|JGJ|CJJ)[/T]*\s*[\d.]+-\d{4})', norm_text)
    else:
        standards = re.findall(r'(ISO[/IEC]*\s*[\d.]+-?\d{0,4})', norm_text)
    
    if not standards:
        issues.append('规范性引用文件章节中未检测到标准号')
    else:
        for std in standards:
            # 检查是否有年份
            if not re.search(r'\d{4}', std):
                issues.append(f'标准"{std}"未注明年份——需确认是注日期引用还是不注日期引用')
    
    # 检查导语
    if std_type == 'cn':
        if '通过文中的规范性引用' not in norm_text and '构成本文件必不可少的条款' not in norm_text:
            issues.append('规范性引用文件章节缺少GB/T 1.1规定的标准导语')
    else:
        if 'referred to in the text' not in norm_text:
            issues.append('Normative references section missing standard introductory text per ISO/IEC Directives')
    
    return issues

# ============================================================
# 主函数
# ============================================================

def run_checks(filepath, doc_type):
    """执行完整参考文献检查"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ 无法读取文件: {e}")
        return False
    
    all_issues = {'SEVERE': [], 'WARNING': [], 'CHECK': []}
    reqs = REF_REQUIREMENTS.get(doc_type, {})
    
    # 提取参考文献
    refs = extract_references_numbered(content)
    is_numbered = len(refs) > 0
    if not is_numbered:
        refs = extract_references_author_year(content)
    
    ref_count = len(refs)
    
    # 统计
    stats = {
        '文档类型': doc_type,
        '引用格式': '顺序编码制' if is_numbered else '著者-出版年制',
        '参考文献数': ref_count,
    }
    
    # 1. 数量检查
    min_count = reqs.get('min_count', 0)
    if min_count and ref_count < min_count:
        all_issues['SEVERE'].append(f'参考文献仅{ref_count}篇，{doc_type}要求≥{min_count}篇')
    
    # 2. 格式检查 (GB/T 7714)
    if doc_type in ('CN', 'BK', 'RPT') and refs:
        for ref in refs:
            fmt_issues = check_gbt7714_format(ref.get('text', ''), ref.get('num'))
            for issue in fmt_issues:
                all_issues['WARNING'].append(f'格式: {issue}')
    
    # 3. 编号连续性
    if is_numbered:
        num_issues = check_numbering_continuity(refs)
        for issue in num_issues:
            all_issues['WARNING'].append(f'编号: {issue}')
    
    # 4. 正文-文献表交叉一致性
    if is_numbered:
        inline_cites = extract_inline_citations_numbered(content)
        ref_nums = set(r.get('num', 0) for r in refs)
        cross_issues = check_cross_consistency(inline_cites, ref_nums)
        for issue in cross_issues:
            all_issues['SEVERE'].append(f'交叉引用: {issue}')
        stats['正文引用数'] = len(inline_cites)
    
    # 5. 近5年文献占比
    if refs:
        recent_ratio, recent_count = check_recent_ratio(refs)
        stats['近5年占比'] = f'{recent_ratio:.0%} ({recent_count}/{ref_count})'
        req_ratio = reqs.get('recent_5yr_ratio')
        if req_ratio and recent_ratio < req_ratio:
            all_issues['WARNING'].append(f'近5年文献占比{recent_ratio:.0%}，要求≥{req_ratio:.0%}')
    
    # 6. 自引率
    if refs:
        self_ratio, self_count = check_self_citation_rate(refs)
        stats['自引率'] = f'{self_ratio:.0%} ({self_count}/{ref_count})'
        cite_range = reqs.get('self_cite_range')
        if cite_range:
            if self_ratio < cite_range[0]:
                all_issues['CHECK'].append(f'自引率{self_ratio:.0%}偏低(目标{cite_range[0]:.0%}-{cite_range[1]:.0%})')
            elif self_ratio > cite_range[1]:
                all_issues['WARNING'].append(f'自引率{self_ratio:.0%}偏高(目标≤{cite_range[1]:.0%})')
    
    # 7. 疑似编造检测
    if refs:
        suspicious = check_suspicious_refs(refs)
        for issue in suspicious:
            all_issues['CHECK'].append(f'疑似问题: {issue}')
    
    # 8. 标准特殊检查
    if doc_type in ('STD-CN', 'STD-INT'):
        std_type = 'cn' if doc_type == 'STD-CN' else 'int'
        norm_issues = check_normative_references(content, std_type)
        for issue in norm_issues:
            all_issues['WARNING'].append(f'规范性引用: {issue}')
    
    # 输出报告
    print(f"\n{'='*65}")
    print(f" 📚 参考文献质量检查报告")
    print(f"{'='*65}")
    
    print(f"\n📊 基本统计:")
    for k, v in stats.items():
        print(f"   {k}: {v}")
    
    severe = all_issues['SEVERE']
    warning = all_issues['WARNING']
    check = all_issues['CHECK']
    total = len(severe) + len(warning) + len(check)
    
    print(f"\n共发现 {total} 个问题 "
          f"(🔴严重:{len(severe)} 🟡警告:{len(warning)} ⚪待确认:{len(check)})")
    
    if severe:
        print(f"\n🔴 严重问题（必须修正）:")
        print(f"{'—'*55}")
        for i, issue in enumerate(severe, 1):
            print(f"  {i}. {issue}")
    
    if warning:
        print(f"\n🟡 警告（建议修正）:")
        print(f"{'—'*55}")
        for i, issue in enumerate(warning, 1):
            print(f"  {i}. {issue}")
    
    if check:
        print(f"\n⚪ 需人工确认:")
        print(f"{'—'*55}")
        for i, issue in enumerate(check, 1):
            print(f"  {i}. {issue}")
    
    # 格式合规率
    format_total = ref_count if ref_count > 0 else 1
    format_errors = sum(1 for i in all_issues['WARNING'] if i.startswith('格式:'))
    format_compliance = max(0, (format_total - format_errors) / format_total * 100)
    
    print(f"\n📊 格式合规率: {format_compliance:.0f}%")
    
    print(f"\n{'='*65}")
    if severe:
        print("❌ 存在严重引用问题，须修正后重检。")
    elif warning:
        print("⚠️  存在格式问题，建议修正后提交。")
    else:
        print("✅ 参考文献检查通过。")
    print()
    
    return len(severe) == 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='参考文献格式自动检查')
    parser.add_argument('filepath', help='文档文件路径')
    parser.add_argument('--type', choices=['SCI','CN','PAT','BK','RPT','STD-CN','STD-INT','WX','PPT'],
                       default='CN', help='文档类型(默认CN)')
    args = parser.parse_args()
    
    passed = run_checks(args.filepath, args.type)
    sys.exit(0 if passed else 1)
