#!/usr/bin/env python3
"""
技术标准文档质量自动检查脚本
用法: python3 check_standard.py <文件路径> [--type cn|int]
配合 writing-projects/academic-writer-skill/SKILL.md §7.6 使用
"""
import re
import sys
import argparse

def load_document(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

# ============================================================
# 通用检查（国内/国际共用）
# ============================================================

def check_structure_cn(content):
    """检查国内标准结构完整性 (GB/T 1.1-2020)"""
    issues = []
    required = [
        ('前言', r'前\s*言'),
        ('范围', r'^1\s+范围|^1\s+Scope'),
        ('规范性引用文件', r'^2\s+规范性引用文件'),
        ('术语和定义', r'^3\s+术语和定义|^3\s+术语'),
    ]
    for name, pattern in required:
        if not re.search(pattern, content, re.MULTILINE):
            issues.append({
                'level': 'SEVERE', 'category': '结构合规',
                'message': f'缺少必要章节：{name}',
                'suggestion': f'按GB/T 1.1-2020要求补充"{name}"章节'
            })
    
    # 检查前言要素
    foreword_match = re.search(r'前\s*言(.*?)(?=^1\s|\Z)', content, re.DOTALL | re.MULTILINE)
    if foreword_match:
        fw = foreword_match.group(1)
        for element in ['归口', '起草单位', '起草人']:
            if element not in fw:
                issues.append({
                    'level': 'WARNING', 'category': '前言要素',
                    'message': f'前言中未找到"{element}"信息',
                    'suggestion': f'前言须包含归口单位、起草单位、主要起草人'
                })
    return issues

def check_structure_int(content):
    """检查国际标准结构完整性 (ISO/IEC Directives Part 2)"""
    issues = []
    required = [
        ('Foreword', r'Foreword'),
        ('Scope', r'^1\s+Scope'),
        ('Normative references', r'^2\s+Normative references'),
        ('Terms and definitions', r'^3\s+Terms and definitions'),
    ]
    for name, pattern in required:
        if not re.search(pattern, content, re.MULTILINE):
            issues.append({
                'level': 'SEVERE', 'category': 'Structure',
                'message': f'Missing required clause: {name}',
                'suggestion': f'Add "{name}" per ISO/IEC Directives Part 2'
            })
    
    # 检查法文标题
    if not re.search(r'[À-ÿ]', content):
        issues.append({
            'level': 'WARNING', 'category': 'Bilingual title',
            'message': '未检测到法文字符——ISO标准须提供英法双语标题',
            'suggestion': '在封面/标题页添加法文标题'
        })
    
    # 检查阶段标识
    stages = ['WD', 'CD', 'DIS', 'FDIS', 'IS']
    found_stage = any(re.search(rf'\b{s}\b', content[:500]) for s in stages)
    if not found_stage:
        issues.append({
            'level': 'CHECK', 'category': 'Stage',
            'message': '未在文档开头检测到阶段标识(WD/CD/DIS/FDIS/IS)',
            'suggestion': '确认文件阶段并在封面标注'
        })
    return issues

def check_normative_wording_cn(content):
    """检查国内标准条文用语一致性"""
    issues = []
    # 正确用语: 应/宜/可/不应/不宜
    # 错误用语: 必须/建议/希望/最好/尽量
    
    wrong_words = {
        '必须': '标准条文中应使用「应」而非「必须」',
        '建议': '标准条文中应使用「宜」而非「建议」',
        '希望': '标准条文不宜使用「希望」',
        '最好': '标准条文应使用「宜」而非「最好」',
        '尽量': '标准条文应使用「宜」而非「尽量」',
        '需要': '条文中考虑使用「应」(强制)或「宜」(推荐)替代「需要」',
        '要求': '条文正文中「要求」可能应改为「应」',
    }
    
    # 跳过前言和引言，只检查正文条文
    body_match = re.search(r'^1\s+范围', content, re.MULTILINE)
    if body_match:
        body = content[body_match.start():]
    else:
        body = content
    
    for word, suggestion in wrong_words.items():
        occurrences = [(m.start(), m.group()) for m in re.finditer(word, body)]
        if occurrences:
            # 过滤掉引用/脚注/术语定义中的使用
            real_count = len(occurrences)
            if real_count > 0:
                issues.append({
                    'level': 'WARNING', 'category': '条文用语',
                    'message': f'条文正文中出现「{word}」({real_count}处)',
                    'suggestion': suggestion
                })
    
    # 统计正确用语分布
    correct_counts = {}
    for w in ['应', '宜', '可', '不应', '不宜']:
        # 需要精准匹配，避免"应用""应该"等误匹配
        if w in ['应', '宜', '可']:
            # 前后不能接中文字
            pattern = rf'(?<![不\u4e00-\u9fff]){w}(?![用该当为以行])'
            if w == '可':
                pattern = rf'(?<!不)可(?![以能行是用])'
        else:
            pattern = re.escape(w)
        count = len(re.findall(pattern, body))
        correct_counts[w] = count
    
    total_normative = sum(correct_counts.values())
    if total_normative == 0:
        issues.append({
            'level': 'SEVERE', 'category': '条文用语',
            'message': '未检测到规范性用语（应/宜/可/不应/不宜）',
            'suggestion': '条文正文必须使用GB/T 1.1-2020规定的规范用语'
        })
    
    return issues, correct_counts

def check_normative_wording_int(content):
    """检查国际标准条文用语一致性"""
    issues = []
    
    wrong_words = {
        'must': '条文中应使用 "shall" 而非 "must"',
        'need to': '条文中应使用 "shall" 或 "should" 而非 "need to"',
        'has to': '条文中应使用 "shall" 而非 "has to"',
        'is required': '条文中应使用 "shall" 而非 "is required"',
        'it is recommended': '条文中应使用 "should" 而非 "it is recommended"',
    }
    
    body_match = re.search(r'^1\s+Scope', content, re.MULTILINE)
    body = content[body_match.start():] if body_match else content
    
    for word, suggestion in wrong_words.items():
        count = len(re.findall(rf'\b{word}\b', body, re.IGNORECASE))
        if count > 0:
            issues.append({
                'level': 'WARNING', 'category': 'Normative wording',
                'message': f'Found "{word}" in normative text ({count} times)',
                'suggestion': suggestion
            })
    
    correct_counts = {}
    for w in ['shall', 'should', 'may', 'shall not', 'should not']:
        count = len(re.findall(rf'\b{w}\b', body))
        correct_counts[w] = count
    
    total = sum(correct_counts.values())
    if total == 0:
        issues.append({
            'level': 'SEVERE', 'category': 'Normative wording',
            'message': 'No normative keywords (shall/should/may) detected',
            'suggestion': 'Normative text must use ISO/IEC Directives Part 2 wording'
        })
    
    return issues, correct_counts

def check_clause_numbering(content):
    """检查条文编号连续性"""
    issues = []
    clause_nums = re.findall(r'^(\d+(?:\.\d+)*)\s', content, re.MULTILINE)
    
    if not clause_nums:
        return issues
    
    # 检查一级条目连续性
    top_level = sorted(set(int(n.split('.')[0]) for n in clause_nums if '.' not in n or n.count('.') == 0))
    
    for i in range(len(top_level) - 1):
        if top_level[i+1] - top_level[i] > 1:
            issues.append({
                'level': 'WARNING', 'category': '条文编号',
                'message': f'一级条文编号不连续：{top_level[i]}后跳至{top_level[i+1]}',
                'suggestion': '检查是否遗漏章节'
            })
    return issues

def check_cross_references(content):
    """检查交叉引用有效性"""
    issues = []
    # 查找交叉引用
    refs = re.findall(r'见?\s*(\d+\.\d+(?:\.\d+)?)', content)
    # 查找已定义的条目
    defined = set(re.findall(r'^(\d+(?:\.\d+)*)\s', content, re.MULTILINE))
    
    for ref in refs:
        if ref not in defined:
            issues.append({
                'level': 'CHECK', 'category': '交叉引用',
                'message': f'引用了条文 {ref}，但未找到对应章节',
                'suggestion': f'确认 {ref} 是否存在，或调整引用'
            })
    return issues

def check_annex_labels(content):
    """检查附录标注"""
    issues = []
    annexes = re.findall(r'附录\s*([A-Z])\s*(.*)', content)
    for letter, rest in annexes:
        if '规范性' not in rest and '资料性' not in rest and 'normative' not in rest.lower() and 'informative' not in rest.lower():
            issues.append({
                'level': 'WARNING', 'category': '附录标注',
                'message': f'附录{letter}未标注类型',
                'suggestion': f'须标注"(规范性)"或"(资料性)"'
            })
    return issues

def check_units(content, is_international=False):
    """检查量和单位"""
    issues = []
    # 常见非SI单位
    non_si = {
        r'\bpsi\b': 'Pa (帕斯卡)',
        r'\bft\b': 'm (米)',
        r'\bgal\b': 'L (升)',
        r'\binch\b': 'mm (毫米)',
    }
    for pattern, replacement in non_si.items():
        if re.search(pattern, content, re.IGNORECASE):
            issues.append({
                'level': 'CHECK', 'category': '量和单位',
                'message': f'检测到可能的非SI单位匹配',
                'suggestion': f'请确认是否应使用SI单位 {replacement}'
            })
    return issues

def check_terminology_definitions(content):
    """检查术语定义格式"""
    issues = []
    # 检查术语章节
    term_section = re.search(r'(术语和定义|Terms and definitions)(.*?)(?=^\d+\s+(?!术语)|\Z)', 
                             content, re.DOTALL | re.MULTILINE)
    if term_section:
        terms_text = term_section.group(2)
        term_entries = re.findall(r'^3\.\d+\s*\n?(.*?)(?=^3\.\d+|\Z)', terms_text, re.DOTALL | re.MULTILINE)
        if len(term_entries) == 0:
            issues.append({
                'level': 'WARNING', 'category': '术语定义',
                'message': '术语章节为空或格式不规范',
                'suggestion': '每个术语使用"属概念+种差"定义法'
            })
    return issues

def generate_stats(content, std_type):
    """生成文档统计"""
    char_count = len(content)
    lines = content.split('\n')
    clause_count = len(re.findall(r'^\d+(?:\.\d+)*\s', content, re.MULTILINE))
    annex_count = len(re.findall(r'附录\s*[A-Z]|Annex\s+[A-Z]', content))
    
    return {
        '标准类型': '国内标准' if std_type == 'cn' else '国际标准',
        '总字符数': char_count,
        '总行数': len(lines),
        '条文数': clause_count,
        '附录数': annex_count,
    }

def run_checks(filepath, std_type='cn'):
    """执行全部检查"""
    content = load_document(filepath)
    all_issues = []
    
    # 结构检查
    if std_type == 'cn':
        all_issues.extend(check_structure_cn(content))
    else:
        all_issues.extend(check_structure_int(content))
    
    # 条文用语检查
    if std_type == 'cn':
        wording_issues, wording_stats = check_normative_wording_cn(content)
    else:
        wording_issues, wording_stats = check_normative_wording_int(content)
    all_issues.extend(wording_issues)
    
    # 通用检查
    all_issues.extend(check_clause_numbering(content))
    all_issues.extend(check_cross_references(content))
    all_issues.extend(check_annex_labels(content))
    all_issues.extend(check_units(content, std_type == 'int'))
    all_issues.extend(check_terminology_definitions(content))
    
    stats = generate_stats(content, std_type)
    
    # 输出报告
    print(f"\n{'='*65}")
    if std_type == 'cn':
        print(f" 📋 国内技术标准质量检查报告 (GB/T 1.1-2020)")
    else:
        print(f" 📋 International Standard Quality Check (ISO/IEC Directives Part 2)")
    print(f"{'='*65}")
    
    print(f"\n📊 基本统计:")
    for k, v in stats.items():
        print(f"   {k}: {v}")
    
    print(f"\n📊 规范用语分布:")
    for w, c in wording_stats.items():
        bar = '█' * min(c, 40)
        print(f"   「{w}」: {c}次 {bar}")
    
    # 计算合规率
    severe = [i for i in all_issues if i['level'] == 'SEVERE']
    warning = [i for i in all_issues if i['level'] == 'WARNING']
    check = [i for i in all_issues if i['level'] == 'CHECK']
    
    total_checks = 10  # 基准检查项数
    compliance_rate = max(0, (total_checks - len(severe)) / total_checks * 100)
    
    print(f"\n📊 条文合规率: {compliance_rate:.0f}%")
    print(f"   共发现 {len(all_issues)} 个问题 "
          f"(🔴严重:{len(severe)} 🟡警告:{len(warning)} ⚪待确认:{len(check)})")
    
    if severe:
        print(f"\n🔴 严重问题（必须修正）:")
        print(f"{'—'*55}")
        for i, item in enumerate(severe, 1):
            print(f"  {i}. [{item['category']}] {item['message']}")
            print(f"     → {item['suggestion']}")
    
    if warning:
        print(f"\n🟡 警告（建议修正）:")
        print(f"{'—'*55}")
        for i, item in enumerate(warning, 1):
            print(f"  {i}. [{item['category']}] {item['message']}")
            print(f"     → {item['suggestion']}")
    
    if check:
        print(f"\n⚪ 需人工确认:")
        print(f"{'—'*55}")
        for i, item in enumerate(check, 1):
            print(f"  {i}. [{item['category']}] {item['message']}")
            print(f"     → {item['suggestion']}")
    
    print(f"\n{'='*65}")
    if severe:
        print("❌ 条文合规率未达100%，须修正后重检。")
    elif warning:
        print("⚠️  建议修正警告项后提交审查。")
    else:
        print("✅ 标准文档检查通过，可提交审查。")
    print()
    
    return len(severe) == 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='技术标准文档质量检查')
    parser.add_argument('filepath', help='标准文档文件路径')
    parser.add_argument('--type', choices=['cn', 'int'], default='cn',
                       help='标准类型: cn=国内(GB/T 1.1), int=国际(ISO/IEC)')
    args = parser.parse_args()
    
    passed = run_checks(args.filepath, args.type)
    sys.exit(0 if passed else 1)
