#!/usr/bin/env python3
"""
学术写作质量检查统一调度器
用法: python3 check_quality.py <文件路径> [--type SCI|CN|PAT|BK|RPT|STD-CN|STD-INT|WX|PPT]

自动检测文档类型并分发至对应检查脚本。
- WX: → check_article.py (12项检查)
- STD-CN/STD-INT: → check_standard.py (条文用语+结构合规)
- PPT: → check_ppt.py (配色+字体+Notes+节奏)
- SCI/CN/PAT/BK/RPT: → 通用检查 (引用/公式/术语/一致性)
"""
import sys
import os
import re
import argparse
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent

def detect_type(filepath):
    """根据文件名和内容自动推断文档类型"""
    path = Path(filepath)
    name = path.stem.lower()
    suffix = path.suffix.lower()
    
    # 文件名推断
    if suffix == '.pptx':
        return 'PPT'
    if 'ppt' in name or 'slide' in name or '汇报' in name or '演示' in name:
        return 'PPT'
    if 'wx' in name or '公众号' in name or '推文' in name:
        return 'WX'
    if 'std-cn' in name or 'slt' in name or 'gbt' in name or '行标' in name or '国标' in name:
        return 'STD-CN'
    if 'std-int' in name or 'iso' in name:
        return 'STD-INT'
    if 'sci' in name:
        return 'SCI'
    if 'pat' in name or '专利' in name:
        return 'PAT'
    if 'bk' in name or '书稿' in name or '教材' in name or 'ch0' in name:
        return 'BK'
    if 'rpt' in name or '报告' in name:
        return 'RPT'
    if 'cn-' in name or '中文论文' in name:
        return 'CN'
    
    # 内容推断
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read(3000)  # 只读前3000字符
        
        if 'GB/T' in content or '规范性引用文件' in content or '术语和定义' in content:
            return 'STD-CN'
        if 'Normative references' in content or 'shall' in content.lower()[:2000]:
            return 'STD-INT'
        if '权利要求书' in content or '技术领域' in content[:500]:
            return 'PAT'
        if 'Abstract' in content[:1000] and 'Keywords' in content[:1500]:
            return 'SCI'
        if '摘要' in content[:500] and '关键词' in content[:1000]:
            return 'CN'
        if '执行摘要' in content or 'Executive Summary' in content:
            return 'RPT'
    except:
        pass
    
    return None

def run_wx_check(filepath):
    """调用WX检查脚本"""
    script = SCRIPT_DIR / 'check_article.py'
    result = subprocess.run([sys.executable, str(script), filepath], capture_output=False)
    return result.returncode == 0

def run_std_check(filepath, std_type):
    """调用标准检查脚本"""
    script = SCRIPT_DIR / 'check_standard.py'
    type_arg = 'cn' if std_type == 'STD-CN' else 'int'
    result = subprocess.run([sys.executable, str(script), filepath, '--type', type_arg], capture_output=False)
    return result.returncode == 0

def run_ppt_check(filepath, duration=None):
    """调用PPT检查脚本"""
    script = SCRIPT_DIR / 'check_ppt.py'
    args = [sys.executable, str(script), filepath]
    if duration:
        args.extend(['--duration', str(duration)])
    result = subprocess.run(args, capture_output=False)
    return result.returncode == 0

def run_general_check(filepath, doc_type):
    """通用检查 (SCI/CN/PAT/BK/RPT)"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        print(f"❌ 无法读取文件: {filepath}")
        return False
    
    issues = []
    
    # 1. 公式编号检查
    equations = re.findall(r'\$\$.*?\$\$|\\\[.*?\\\]', content, re.DOTALL)
    numbered_eqs = re.findall(r'\\tag\{|\\label\{|式\s*\(|\(\d+\)', content)
    if equations and not numbered_eqs:
        issues.append(('WARNING', '公式编号', '检测到公式但未发现编号'))
    
    # 2. 图表引用检查
    figures = re.findall(r'[Ff]ig(?:ure|\.)\s*\d+|图\s*\d+', content)
    tables = re.findall(r'[Tt]able\s*\d+|表\s*\d+', content)
    fig_defs = re.findall(r'!\[.*?图.*?\d+|\\begin\{figure\}', content)
    if fig_defs and not figures:
        issues.append(('WARNING', '图表引用', '检测到图片定义但正文中未引用'))
    
    # 3. 参考文献检查 (SCI/CN)
    if doc_type in ('SCI', 'CN'):
        refs = re.findall(r'\[\d+\]|\\\cite\{', content)
        ref_list = re.findall(r'^\[\d+\]|\\bibitem', content, re.MULTILINE)
        if ref_list:
            ref_count = len(ref_list)
            if doc_type == 'SCI' and ref_count < 30:
                issues.append(('WARNING', '参考文献', f'参考文献仅{ref_count}篇(SCI要求≥30篇)'))
    
    # 4. 缩略语检查
    abbrevs = re.findall(r'\b[A-Z]{2,6}\b', content)
    from collections import Counter
    abbrev_freq = Counter(abbrevs)
    for abbr, count in abbrev_freq.most_common(20):
        if count > 3:
            # 检查是否有全称定义
            full_pattern = rf'\({abbr}\)|{abbr}\s*[\(（]|{abbr}.*?全称'
            if not re.search(full_pattern, content[:len(content)//2]):
                issues.append(('CHECK', '缩略语', f'"{abbr}"出现{count}次，未检测到首次全称定义'))
    
    # 5. 数据来源检查
    numbers = re.findall(r'\d+(?:\.\d+)?%|\d{4,}', content)
    source_markers = re.findall(r'来源|数据源|据.*?统计|according to|source', content, re.IGNORECASE)
    if len(numbers) > 10 and len(source_markers) < 2:
        issues.append(('CHECK', '数据来源', f'文中包含{len(numbers)}个数值/百分比，但来源标注偏少'))
    
    # 6. 术语一致性(CHS核心术语)
    chs_terms = {
        'CHS': ['Cybernetics of Hydro Systems', '水系统控制论'],
        'HydroOS': ['Hydraulic Network Operating System', '水网操作系统'],
        'WNAL': ['Water Network Autonomy Level', '水网自主运行等级'],
        'ODD': ['Operational Design Domain', '运行设计域'],
        'IDZ': ['Integrator Delay Zero', '积分延迟零'],
    }
    for abbr, full_names in chs_terms.items():
        if abbr in content:
            has_def = any(fn in content for fn in full_names)
            if not has_def:
                issues.append(('CHECK', '术语定义', f'使用了{abbr}但未检测到全称定义'))
    
    # 7. 专利特有检查
    if doc_type == 'PAT':
        required_sections = ['技术领域', '背景技术', '发明内容', '附图说明', '具体实施方式', '权利要求']
        for sec in required_sections:
            if sec not in content:
                issues.append(('SEVERE', '专利结构', f'缺少"{sec}"部分'))
        
        claims = re.findall(r'权利要求\s*(\d+)', content)
        if claims:
            claim_count = max(int(c) for c in claims)
            if claim_count < 8:
                issues.append(('WARNING', '权利要求', f'仅{claim_count}项权利要求(建议8-15项)'))
    
    # 输出
    print(f"\n{'='*65}")
    print(f" 📝 {doc_type} 文档质量检查报告")
    print(f"{'='*65}")
    
    char_count = len(content)
    print(f"\n📊 基本统计:")
    print(f"   总字符数: {char_count}")
    print(f"   文档类型: {doc_type}")
    
    severe = [i for i in issues if i[0] == 'SEVERE']
    warning = [i for i in issues if i[0] == 'WARNING']
    check = [i for i in issues if i[0] == 'CHECK']
    
    print(f"\n共发现 {len(issues)} 个问题 "
          f"(🔴严重:{len(severe)} 🟡警告:{len(warning)} ⚪待确认:{len(check)})")
    
    for level_name, level_items, emoji in [
        ('严重问题', severe, '🔴'),
        ('警告', warning, '🟡'),
        ('需人工确认', check, '⚪'),
    ]:
        if level_items:
            print(f"\n{emoji} {level_name}:")
            print(f"{'—'*55}")
            for i, (_, cat, msg) in enumerate(level_items, 1):
                print(f"  {i}. [{cat}] {msg}")
    
    print(f"\n{'='*65}")
    if severe:
        print("❌ 存在严重问题，须修正后重检。")
    elif warning:
        print("⚠️  建议修正警告项。")
    else:
        print("✅ 检查通过。")
    print()
    return len(severe) == 0

def main():
    parser = argparse.ArgumentParser(
        description='学术写作质量检查统一调度器',
        epilog='支持文档类型: SCI, CN, PAT, BK, RPT, STD-CN, STD-INT, WX, PPT'
    )
    parser.add_argument('filepath', help='文档文件路径')
    parser.add_argument('--type', choices=['SCI','CN','PAT','BK','RPT','STD-CN','STD-INT','WX','PPT'],
                       help='文档类型(不指定则自动推断)')
    parser.add_argument('--duration', type=int, help='PPT目标汇报时长(分钟)')
    args = parser.parse_args()
    
    if not os.path.exists(args.filepath):
        print(f"❌ 文件不存在: {args.filepath}")
        sys.exit(1)
    
    doc_type = args.type or detect_type(args.filepath)
    if not doc_type:
        print(f"⚠️  无法自动推断文档类型，请使用 --type 参数指定")
        print(f"   可选: SCI, CN, PAT, BK, RPT, STD-CN, STD-INT, WX, PPT")
        sys.exit(1)
    
    print(f"📄 文件: {args.filepath}")
    print(f"📋 文档类型: {doc_type}")
    
    if doc_type == 'WX':
        passed = run_wx_check(args.filepath)
    elif doc_type in ('STD-CN', 'STD-INT'):
        passed = run_std_check(args.filepath, doc_type)
    elif doc_type == 'PPT':
        passed = run_ppt_check(args.filepath, args.duration)
    else:
        passed = run_general_check(args.filepath, doc_type)
    
    sys.exit(0 if passed else 1)

if __name__ == '__main__':
    main()
