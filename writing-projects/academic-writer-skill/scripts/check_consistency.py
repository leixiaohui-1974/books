#!/usr/bin/env python3
"""
跨文档一致性检查脚本
用法: python3 check_consistency.py <文档目录>
按 SKILL.md §6 CONS-01~CONS-10 进行交叉检查

检查逻辑：从已完成文档中提取关键表述，检测不一致。
"""
import re
import sys
import os
import json
from pathlib import Path
from collections import defaultdict

# ============================================================
# CONS规则定义
# ============================================================

CONS_RULES = {
    'CONS-01': {
        'name': 'CHS八原理表述',
        'keywords': ['八原理', 'eight principles', 'CHS原理', 'cybernetics principles'],
        'extract_pattern': r'((?:八|8|eight)\s*(?:原理|principles|大原理).*?(?:\n\n|\Z))',
    },
    'CONS-02': {
        'name': 'WNAL(L0-L5)定义',
        'keywords': ['WNAL', 'L0', 'L1', 'L2', 'L3', 'L4', 'L5', '自主运行等级', 'autonomy level'],
        'extract_pattern': r'((?:WNAL|水网自主运行等级|Water Network Autonomy Level).*?(?:L5|Level\s*5).*?(?:\n\n|\Z))',
    },
    'CONS-03': {
        'name': 'Saint-Venant方程离散化表述',
        'keywords': ['Saint-Venant', 'SV方程', 'shallow water', '浅水方程'],
        'extract_pattern': r'(Saint-Venant.*?(?:\n\n|\Z))',
    },
    'CONS-04': {
        'name': 'MPC控制原理描述',
        'keywords': ['MPC', 'Model Predictive Control', '模型预测控制', 'DMPC'],
        'extract_pattern': r'((?:MPC|模型预测控制|Model Predictive Control|DMPC).*?(?:\n\n|\Z))',
    },
    'CONS-05': {
        'name': 'HydroOS五层架构',
        'keywords': ['HydroOS', '五层', 'five-layer', '水网操作系统'],
        'extract_pattern': r'(HydroOS.*?(?:五层|five.?layer|架构|architecture).*?(?:\n\n|\Z))',
    },
    'CONS-06': {
        'name': '胶东调水工程参数',
        'keywords': ['胶东', 'Jiaodong', '调水'],
        'extract_pattern': r'(胶东.*?(?:km|公里|m³|调水量|流量).*?(?:\n\n|\Z))',
    },
    'CONS-07': {
        'name': '沙坪水电站工程参数',
        'keywords': ['沙坪', 'Shaping', '水电站'],
        'extract_pattern': r'(沙坪.*?(?:MW|装机|水头|流量).*?(?:\n\n|\Z))',
    },
    'CONS-08': {
        'name': '南水北调中线工程参数',
        'keywords': ['南水北调', 'South-to-North', '中线', 'middle route'],
        'extract_pattern': r'(南水北调.*?(?:km|公里|渠池|1432).*?(?:\n\n|\Z))',
    },
    'CONS-09': {
        'name': '安全包络ODD边界条件',
        'keywords': ['ODD', 'Operational Design Domain', '运行设计域', '安全包络', 'Safety Envelope'],
        'extract_pattern': r'((?:ODD|运行设计域|Operational Design Domain|安全包络).*?(?:\n\n|\Z))',
    },
    'CONS-10': {
        'name': '§5.1术语表中英对照',
        'keywords': ['CHS', 'HydroOS', 'WNAL', 'IDZ', 'DMPC', 'MAS'],
        'check_type': 'terminology',  # 特殊处理：检查术语全称是否一致
    },
}

# 术语标准定义（来自SKILL.md §5.1）
STANDARD_TERMS = {
    'CHS': 'Cybernetics of Hydro Systems',
    'HydroOS': 'Hydraulic Network Operating System',
    'WNAL': 'Water Network Autonomy Level',
    'ODD': 'Operational Design Domain',
    'IDZ': 'Integrator Delay Zero',
    'DMPC': 'Distributed Model Predictive Control',
    'MAS': 'Multi-Agent System',
    'MIL': 'Model-in-the-Loop',
    'SIL': 'Software-in-the-Loop',
    'HIL': 'Hardware-in-the-Loop',
    'SE': 'Safety Envelope',
    'CI': 'Cognitive Intelligence',
    'HWLM': 'Hando Water Network Large Model',
}

# ============================================================
# 文件扫描
# ============================================================

def find_documents(base_dir):
    """扫描目录下所有已完成的文档"""
    docs = []
    base = Path(base_dir)
    
    for ext in ['*.md', '*.txt', '*.docx']:
        for f in base.rglob(ext):
            if f.name.startswith('.') or 'node_modules' in str(f):
                continue
            if any(skip in str(f) for skip in ['progress.json', 'review_', 'check_report', 'SKILL.md', 'CLAUDE.md']):
                continue
            docs.append(f)
    
    return docs

def read_document(filepath):
    """读取文档内容"""
    path = Path(filepath)
    if path.suffix == '.md' or path.suffix == '.txt':
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except:
            return ''
    elif path.suffix == '.docx':
        try:
            import docx
            doc = docx.Document(filepath)
            return '\n'.join(p.text for p in doc.paragraphs)
        except:
            return ''
    return ''

# ============================================================
# 一致性检查
# ============================================================

def extract_snippets(content, cons_id):
    """从文档中提取与CONS规则相关的片段"""
    rule = CONS_RULES[cons_id]
    snippets = []
    
    # 检查关键词是否出现
    keywords_found = [kw for kw in rule['keywords'] if kw.lower() in content.lower()]
    if not keywords_found:
        return []
    
    # 提取相关段落
    if 'extract_pattern' in rule:
        matches = re.findall(rule['extract_pattern'], content, re.DOTALL | re.IGNORECASE)
        for m in matches:
            snippet = m.strip()[:500]  # 截取前500字
            if snippet:
                snippets.append(snippet)
    
    return snippets

def check_terminology(content, filepath):
    """检查术语全称一致性(CONS-10)"""
    issues = []
    for abbr, standard_full in STANDARD_TERMS.items():
        # 查找文档中对该缩略语的全称定义
        patterns = [
            rf'{abbr}\s*[\(（]\s*(.+?)\s*[\)）]',       # CHS (Cybernetics of ...)
            rf'(.+?)\s*[\(（]\s*{abbr}\s*[\)）]',       # Cybernetics of ... (CHS)
            rf'{abbr}.*?(?:即|is|refers to)\s*(.+?)[\n。.]',  # CHS即...
        ]
        for pattern in patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                match = match.strip()
                if len(match) > 5 and match != standard_full:
                    # 简单的相似度检查
                    if standard_full.lower() not in match.lower() and match.lower() not in standard_full.lower():
                        issues.append({
                            'abbr': abbr,
                            'found': match,
                            'standard': standard_full,
                            'file': str(filepath),
                        })
    return issues

def extract_numbers(content, keyword):
    """提取关键词附近的数值（用于工程参数一致性检查）"""
    numbers = {}
    # 查找关键词附近的数字+单位组合
    pattern = rf'{keyword}.*?(\d+[\d.,]*)\s*(km|公里|m³/s|m³|MW|万kW|亿|座|米)'
    matches = re.findall(pattern, content, re.IGNORECASE)
    for num, unit in matches:
        key = f"{num}{unit}"
        numbers[key] = True
    return numbers

def compare_snippets(snippets_by_doc, cons_id):
    """比较不同文档中同一CONS的表述差异"""
    issues = []
    docs = list(snippets_by_doc.keys())
    
    if len(docs) < 2:
        return issues  # 不足2个文档，无法比较
    
    # 提取数值参数进行精确比较（工程参数类CONS）
    if cons_id in ('CONS-06', 'CONS-07', 'CONS-08'):
        keyword_map = {
            'CONS-06': '胶东',
            'CONS-07': '沙坪',
            'CONS-08': '南水北调',
        }
        kw = keyword_map[cons_id]
        all_numbers = {}
        for doc, snippets in snippets_by_doc.items():
            combined = ' '.join(snippets)
            nums = extract_numbers(combined, kw)
            all_numbers[doc] = nums
        
        # 交叉比较
        ref_doc = docs[0]
        ref_nums = all_numbers[ref_doc]
        for doc in docs[1:]:
            doc_nums = all_numbers[doc]
            # 如果都提到了数值但不一致
            if ref_nums and doc_nums:
                ref_set = set(ref_nums.keys())
                doc_set = set(doc_nums.keys())
                if ref_set != doc_set and ref_set and doc_set:
                    issues.append({
                        'cons_id': cons_id,
                        'type': '数值参数不一致',
                        'doc1': str(ref_doc),
                        'doc1_values': list(ref_set),
                        'doc2': str(doc),
                        'doc2_values': list(doc_set),
                    })
    
    return issues

# ============================================================
# 主函数
# ============================================================

def run_consistency_check(base_dir):
    """执行完整的跨文档一致性检查"""
    docs = find_documents(base_dir)
    
    if not docs:
        print(f"⚠️  在 {base_dir} 中未找到文档文件")
        return True
    
    print(f"\n{'='*65}")
    print(f" 🔗 跨文档一致性检查报告 (CONS-01 ~ CONS-10)")
    print(f"{'='*65}")
    print(f"\n📂 扫描目录: {base_dir}")
    print(f"📄 发现文档: {len(docs)}个")
    for d in docs[:10]:
        print(f"   - {d.name}")
    if len(docs) > 10:
        print(f"   ... 及其他{len(docs)-10}个文件")
    
    all_issues = []
    cons_coverage = {}
    
    # 逐条CONS规则检查
    for cons_id, rule in CONS_RULES.items():
        snippets_by_doc = {}
        
        for doc_path in docs:
            content = read_document(doc_path)
            if not content:
                continue
            
            if rule.get('check_type') == 'terminology':
                # CONS-10: 术语一致性特殊处理
                term_issues = check_terminology(content, doc_path)
                for ti in term_issues:
                    all_issues.append({
                        'cons_id': cons_id,
                        'level': 'WARNING',
                        'message': f'术语{ti["abbr"]}全称不一致: 发现"{ti["found"]}"，标准为"{ti["standard"]}"',
                        'file': ti['file'],
                    })
            else:
                snippets = extract_snippets(content, cons_id)
                if snippets:
                    snippets_by_doc[doc_path] = snippets
        
        # 记录覆盖情况
        if rule.get('check_type') != 'terminology':
            cons_coverage[cons_id] = len(snippets_by_doc)
            
            # 比较不同文档间的差异
            comparison_issues = compare_snippets(snippets_by_doc, cons_id)
            all_issues.extend(comparison_issues)
    
    # 输出覆盖统计
    print(f"\n📊 CONS规则覆盖统计:")
    for cons_id, rule in CONS_RULES.items():
        name = rule['name']
        count = cons_coverage.get(cons_id, '-')
        status = '✅' if count and count != '-' and count >= 2 else '⚪' if count == '-' or count == 0 else '📄'
        if count == '-':
            print(f"   {cons_id}: {status} {name} (术语检查)")
        else:
            print(f"   {cons_id}: {status} {name} ({count}个文档涉及)")
    
    # 输出问题
    if all_issues:
        print(f"\n⚠️  发现 {len(all_issues)} 个一致性问题:")
        print(f"{'—'*55}")
        for i, issue in enumerate(all_issues, 1):
            cons_id = issue.get('cons_id', '?')
            if 'message' in issue:
                print(f"  {i}. [{cons_id}] {issue['message']}")
                if 'file' in issue:
                    print(f"     文件: {issue['file']}")
            elif 'type' in issue:
                print(f"  {i}. [{cons_id}] {issue['type']}")
                print(f"     文档1: {issue.get('doc1','')} → {issue.get('doc1_values','')}")
                print(f"     文档2: {issue.get('doc2','')} → {issue.get('doc2_values','')}")
    else:
        print(f"\n✅ 未发现一致性问题。")
    
    print(f"\n{'='*65}")
    if all_issues:
        print(f"⚠️  请核实并统一不一致的表述。以先完成的文档为准。")
    else:
        print(f"✅ 跨文档一致性检查通过。")
    print()
    
    return len(all_issues) == 0

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='跨文档一致性检查 (CONS-01~CONS-10)')
    parser.add_argument('dir', help='文档目录路径')
    args = parser.parse_args()
    
    passed = run_consistency_check(args.dir)
    sys.exit(0 if passed else 1)
