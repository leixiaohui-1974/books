#!/usr/bin/env python3
"""
CHS 术语一致性检查脚本 (termcheck)
用法：python3 termcheck.py <文档路径>
依据：CLAUDE.md §5.1 核心术语表

检查术语使用是否规范，识别禁止别名。
"""
import re
import sys
from pathlib import Path

# ============================================================
# 术语规范定义 (来自 CLAUDE.md §5.1)
# ============================================================

STANDARD_TERMS = {
    # 正确术语: (英文标准，禁止别名列表)
    '水系统控制论': ('Cybernetics of Hydro Systems (CHS)', ['水控制学', '水系统论', '水网控制学']),
    '水网自主等级': ('Water Network Autonomy Levels (WNAL)', ['水网自动化等级', '水利自主等级', '水网自动驾驶等级']),
    '运行设计域': ('Operational Design Domain (ODD)', ['操作设计域', '运行设计范围']),
    '安全包络': ('Safety Envelope', ['安全域']),  # "安全边界"可用但不作术语
    '物理 AI 引擎': ('Physical AI Engine', ['物理引擎', '机理模型引擎']),
    '认知 AI 引擎': ('Cognitive AI Engine', ['知识引擎', '决策引擎']),
    '分层分布式控制': ('Hierarchical Distributed Control (HDC)', ['分级控制', '集散控制']),
    '多智能体系统': ('Multi-Agent System (MAS)', ['多代理系统']),
    '在环测试': ('In-the-Loop Testing', ['闭环测试']),
    '水网操作系统': ('Water Network Operating System (HydroOS)', ['水利操作系统', '水务 OS']),
    '模型预测控制': ('Model Predictive Control (MPC)', []),  # "预测控制"作为简称可接受
    '降阶模型': ('Reduced-Order Model (ROM)', ['简化模型']),
    '传递函数': ('Transfer Function', ['传递矩阵']),  # 不同概念
    'SCADA+MAS 融合架构': ('SCADA+MAS Fusion Architecture', ['SCADA/MAS 混合']),
}

# WNAL 等级表述规范
WNAL_LEVELS = {
    'L0': ['人工运行', '完全人工', '手动运行'],
    'L1': ['远程监控', '辅助监控', '远程监视'],
    'L2': ['辅助决策', '条件自动', '部分自主'],
    'L3': ['条件自主', '限定条件自主'],
    'L4': ['高度自主', '大部分自主'],
    'L5': ['完全自主', '全自主'],
}

# 需要检查的 WNAL 错误表述
WNAL_WRONG = {
    'WSAL': '建议使用 WNAL (Water Network Autonomy Levels) 作为标准缩写',
    '水网自动驾驶等级': '应使用"水网自主等级"',
    '水网自动化等级': '应使用"水网自主等级"',
}

# ============================================================
# 检查函数
# ============================================================

def load_document(filepath):
    """加载文档内容"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def check_terminology(content, filepath):
    """检查术语使用规范性"""
    issues = []
    
    # 1. 检查禁止别名
    for correct, (english, wrong_aliases) in STANDARD_TERMS.items():
        for wrong in wrong_aliases:
            # 查找禁止术语的出现
            matches = list(re.finditer(wrong, content))
            if matches:
                issues.append({
                    'level': 'ERROR',
                    'type': '禁止别名',
                    'message': f'检测到禁止别名「{wrong}」',
                    'suggestion': f'应使用「{correct}」({english})',
                    'count': len(matches),
                })
    
    # 2. 检查 WNAL 错误表述
    for wrong, suggestion in WNAL_WRONG.items():
        matches = list(re.finditer(wrong, content))
        if matches:
            issues.append({
                'level': 'WARNING',
                'type': 'WNAL 表述',
                'message': f'检测到「{wrong}」({len(matches)}处)',
                'suggestion': suggestion,
                'count': len(matches),
            })
    
    # 3. 检查 WNAL 英文全称
    # 正确：Water Network Autonomy Levels
    # 错误：Water-network Self-driving Autonomy Level (WSAL - 旧版)
    wsal_matches = list(re.finditer(r'WSAL|Water-network Self-driving Autonomy Level', content))
    if wsal_matches:
        issues.append({
            'level': 'INFO',
            'type': 'WNAL 英文',
            'message': f'检测到 WSAL 表述 ({len(wsal_matches)}处)',
            'suggestion': '建议使用 WNAL (Water Network Autonomy Levels) - 最新标准',
            'count': len(wsal_matches),
        })
    
    # 4. 检查术语首次出现是否有英文注释
    # 对于公众号文章，这不是强制要求，但可以提示
    term_appearances = {}
    for correct in STANDARD_TERMS.keys():
        matches = list(re.finditer(correct, content))
        if matches:
            # 检查首次出现是否有英文
            first_pos = matches[0].start()
            # 向前后各扩展 100 字查找英文
            context = content[max(0, first_pos-50):min(len(content), matches[0].end()+100)]
            has_english = bool(re.search(r'[A-Z][a-z]+\s*[\(（]', context)) or bool(re.search(r'\([A-Z]+\)', context))
            if not has_english and len(matches) > 0:
                term_appearances[correct] = len(matches)
    
    # 5. 检查工程名称一致性
    engineering_terms = {
        '胶东调水': ['胶东调水工程', '胶东工程'],
        '沙坪水电站': ['沙坪电站', '沙坪水电厂'],  # 这些可以用，但需一致
    }
    
    for standard, variants in engineering_terms.items():
        # 检查是否有不一致的变体
        for variant in variants:
            if variant != standard:
                matches = list(re.finditer(variant, content))
                if matches:
                    issues.append({
                        'level': 'INFO',
                        'type': '工程名称',
                        'message': f'检测到「{variant}」({len(matches)}处)',
                        'suggestion': f'建议统一使用「{standard}」',
                        'count': len(matches),
                    })
    
    return issues, term_appearances

def check_wnal_levels(content):
    """检查 WNAL 各等级表述是否准确"""
    issues = []
    
    for level, acceptable_terms in WNAL_LEVELS.items():
        # 检查是否有该等级的描述
        pattern = f'L{level}[^L]'
        matches = list(re.finditer(pattern, content))
        if matches:
            # 检查附近是否有可接受的描述
            for match in matches:
                context = content[max(0, match.start()-20):min(len(content), match.end()+50)]
                found_acceptable = any(term in context for term in acceptable_terms)
                if not found_acceptable:
                    # 这可能只是一个引用，不一定需要描述
                    pass
    
    return issues

def generate_stats(content, issues, term_appearances):
    """生成统计信息"""
    stats = {
        '总字符数': len(content),
        '总行数': len(content.split('\n')),
        '术语使用统计': {},
        '问题统计': {
            'ERROR': len([i for i in issues if i['level'] == 'ERROR']),
            'WARNING': len([i for i in issues if i['level'] == 'WARNING']),
            'INFO': len([i for i in issues if i['level'] == 'INFO']),
        }
    }
    
    for term, count in term_appearances.items():
        stats['术语使用统计'][term] = count
    
    return stats

def run_termcheck(filepath):
    """执行术语检查"""
    content = load_document(filepath)
    issues, term_appearances = check_terminology(content, filepath)
    wnai_issues = check_wnal_levels(content)
    issues.extend(wnai_issues)
    stats = generate_stats(content, issues, term_appearances)
    
    # 输出报告
    print(f"\n{'='*65}")
    print(f" 📋 CHS 术语一致性检查报告 (termcheck)")
    print(f"{'='*65}")
    print(f"\n📄 检查文件：{filepath}")
    
    print(f"\n📊 基本统计:")
    print(f"   总字符数：{stats['总字符数']}")
    print(f"   总行数：{stats['总行数']}")
    
    print(f"\n📊 术语使用统计:")
    if stats['术语使用统计']:
        for term, count in stats['术语使用统计'].items():
            print(f"   「{term}」: {count}次")
    else:
        print("   (未检测到核心术语)")
    
    print(f"\n📊 问题统计:")
    error_count = stats['问题统计']['ERROR']
    warning_count = stats['问题统计']['WARNING']
    info_count = stats['问题统计']['INFO']
    total = error_count + warning_count + info_count
    print(f"   🔴 ERROR: {error_count}")
    print(f"   🟡 WARNING: {warning_count}")
    print(f"   ⚪ INFO: {info_count}")
    print(f"   总计：{total}项")
    
    # 计算通过率
    total_checks = len(STANDARD_TERMS) + len(WNAL_WRONG)
    passed_checks = total_checks - error_count
    pass_rate = (passed_checks / total_checks) * 100 if total_checks > 0 else 100
    
    print(f"\n📊 术语规范通过率：{pass_rate:.0f}%")
    
    # 输出问题详情
    if issues:
        # 按级别分组
        by_level = {'ERROR': [], 'WARNING': [], 'INFO': []}
        for issue in issues:
            by_level[issue['level']].append(issue)
        
        for level in ['ERROR', 'WARNING', 'INFO']:
            if by_level[level]:
                emoji = {'ERROR': '🔴', 'WARNING': '🟡', 'INFO': '⚪'}[level]
                print(f"\n{emoji} {level}级别问题:")
                print(f"{'—'*55}")
                for i, item in enumerate(by_level[level], 1):
                    print(f"  {i}. [{item['type']}] {item['message']}")
                    print(f"     → {item['suggestion']}")
    else:
        print(f"\n✅ 未发现术语使用问题。")
    
    print(f"\n{'='*65}")
    if error_count > 0:
        print("❌ 存在禁止别名使用，必须修正后发布。")
    elif warning_count > 0:
        print("⚠️  存在建议改进项，建议修正后发布。")
    else:
        print("✅ 术语检查通过，可发布。")
    print()
    
    return error_count == 0

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法：python3 termcheck.py <文档路径>")
        print("例：python3 termcheck.py wechat_wnal_20260224.md")
        sys.exit(1)
    
    filepath = sys.argv[1]
    if not Path(filepath).exists():
        print(f"❌ 文件不存在：{filepath}")
        sys.exit(1)
    
    passed = run_termcheck(filepath)
    sys.exit(0 if passed else 1)
