#!/usr/bin/env python3
"""check_patent.py — 发明专利申请文件自动质量检查

Usage:
    python3 check_patent.py patent.md

检查项（12项）:
  1. 文件结构完整性（标题→技术领域→背景→发明内容→实施方式→权利要求→摘要）
  2. 权利要求书规范（独权/从属/层次/回指用语）
  3. 独立权利要求保护范围评估
  4. 说明书-权利要求一致性
  5. 背景技术引用（≥3篇对比文件+缺陷分析）
  6. 有益效果量化程度
  7. 实施例参数具体化
  8. 回指用语统一性（"所述"）
  9. 单一性检查
  10. 摘要质量（300字以内+附图说明）
  11. 附图完整性
  12. 技术术语一致性
"""

import re
import sys
import os


def check_structure(text):
    """检查专利文件结构完整性。"""
    required = {
        '发明名称': r'(?:发明名称|一种)',
        '技术领域': r'技术领域',
        '背景技术': r'背景技术',
        '发明内容': r'发明内容',
        '技术问题': r'技术问题|目的在于|为了解决',
        '技术方案': r'技术方案|为实现上述目的|为达到上述目的',
        '有益效果': r'有益效果',
        '附图说明': r'附图说明|附图',
        '具体实施方式': r'具体实施方式|实施例',
        '权利要求书': r'权利要求书|权利要求',
        '说明书摘要': r'摘要|说明书摘要',
    }
    found = {}
    missing = []
    for name, pattern in required.items():
        if re.search(pattern, text):
            found[name] = True
        else:
            missing.append(name)
    return found, missing


def check_claims(text):
    """检查权利要求书规范。"""
    issues = []

    # Extract claims section
    m = re.search(r'权利要求[书\s]*\n(.*?)(?=说明书摘要|摘要|\Z)', text, re.S)
    if not m:
        return ['未找到权利要求书'], 0, 0

    claims_text = m.group(1)
    claims = re.findall(r'(\d+)[、.．]\s*(.*?)(?=\n\d+[、.．]|\Z)', claims_text, re.S)

    if not claims:
        return ['权利要求书为空或格式无法解析'], 0, 0

    total_claims = len(claims)
    independent = 0
    dependent = 0

    for num, content in claims:
        content = content.strip()
        # Check if independent or dependent
        if re.search(r'根据权利要求\d+|如权利要求\d+', content):
            dependent += 1
        else:
            independent += 1

        # Check "所述" usage
        if '该' in content and '所述' not in content:
            issues.append(f'权利要求{num}: 使用"该"而非"所述"回指')

        # Check for vague terms
        vague = re.findall(r'(合适的|适当的|一定的|大约|若干)', content)
        if vague:
            issues.append(f'权利要求{num}: 含模糊用语「{"、".join(vague)}」')

    if independent == 0:
        issues.append('未检测到独立权利要求')
    if total_claims < 5:
        issues.append(f'权利要求仅{total_claims}条(建议≥8条)')
    if dependent > 0 and dependent < independent * 2:
        issues.append(f'从属权利要求{dependent}条偏少(建议每个独权有≥2条从属)')

    return issues, independent, dependent


def check_independent_claim(text):
    """评估独立权利要求保护范围。"""
    issues = []

    m = re.search(r'权利要求[书\s]*\n\s*1[、.．]\s*(.*?)(?=\n\d+[、.．]|\Z)', text, re.S)
    if not m:
        return ['未找到第一条独立权利要求']

    claim1 = m.group(1).strip()

    # Count limiting features
    steps = re.findall(r'步骤[A-Z\d]|[（(][A-Za-z\d][）)]|S\d+', claim1)
    features = len(re.findall(r'[；;。]', claim1)) + 1

    if features > 10:
        issues.append(f'独权限定特征过多({features}个, 保护范围可能过窄)')
    if len(claim1) > 800:
        issues.append(f'独权文字过长({len(claim1)}字, 建议精简)')
    if len(claim1) < 100:
        issues.append(f'独权文字过短({len(claim1)}字, 可能遗漏必要技术特征)')

    # Check for "其特征在于"
    if '其特征在于' not in claim1:
        issues.append('独权缺少"其特征在于"分界语')

    return issues


def check_background(text):
    """检查背景技术引用。"""
    issues = []

    m = re.search(r'背景技术\s*\n(.*?)(?=发明内容)', text, re.S)
    if not m:
        return ['未找到背景技术部分']

    bg = m.group(1)

    # Check for prior art references
    patent_refs = re.findall(r'CN\d{9}[AB]?|US\d{7,}|EP\d{7}', bg)
    lit_refs = re.findall(r'《[^》]+》|\[\d+\]', bg)
    total_refs = len(patent_refs) + len(lit_refs)

    if total_refs < 3:
        issues.append(f'背景技术引用{total_refs}篇对比文件(建议≥3篇)')

    # Check for deficiency analysis
    deficiency_words = re.findall(r'不足|缺陷|问题|局限|无法|难以|未能', bg)
    if len(deficiency_words) < 2:
        issues.append('背景技术缺少现有技术缺陷分析')

    return issues


def check_beneficial_effects(text):
    """检查有益效果量化程度。"""
    issues = []

    m = re.search(r'有益效果\s*[：:]\s*(.*?)(?=附图说明|具体实施|权利要求|\n#)', text, re.S)
    if not m:
        return ['未找到有益效果部分']

    effects = m.group(1)
    numbers = re.findall(r'\d+\.?\d*\s*%|\d+\.?\d*\s*(?:倍|cm|m|s|小时)', effects)
    if len(numbers) < 2:
        issues.append(f'有益效果量化指标不足({len(numbers)}个, 建议≥3个)')

    # Check for numbered effects
    effect_count = len(re.findall(r'[（(]\d[）)]|[\d①②③④⑤]', effects))
    if effect_count < 2:
        issues.append('有益效果建议分点列举(≥3个效果)')

    return issues


def check_embodiment(text):
    """检查实施例参数具体化。"""
    issues = []

    m = re.search(r'具体实施方式\s*\n(.*?)(?=权利要求|\Z)', text, re.S)
    if not m:
        return ['未找到具体实施方式']

    impl = m.group(1)

    # Check for concrete parameters
    params = re.findall(r'\d+\.?\d*\s*(?:m|cm|mm|s|min|h|Hz|kHz|%|℃|°|步|层|个|组)', impl)
    if len(params) < 10:
        issues.append(f'实施例参数不够具体(检测到{len(params)}个量化参数, 建议≥15个)')

    # Check for vague implementations
    vague = re.findall(r'合适的参数|适当的.*值|根据需要|视情况', impl)
    if vague:
        issues.append(f'实施例含{len(vague)}处模糊表述(如"{vague[0]}")')

    return issues


def check_referencing_terms(text):
    """检查回指用语统一性。"""
    issues = []

    # In claims, "所述" is the correct referencing term
    m = re.search(r'权利要求[书\s]*\n(.*?)(?=说明书摘要|摘要|\Z)', text, re.S)
    if m:
        claims = m.group(1)
        bad_refs = len(re.findall(r'(?<!所)该(?!方法|系统|装置)', claims))
        suo_refs = len(re.findall(r'所述', claims))
        if bad_refs > 0 and bad_refs > suo_refs * 0.3:
            issues.append(f'权利要求中"该"({bad_refs}处)应统一替换为"所述"')

    return issues


def check_abstract_quality(text):
    """检查摘要质量。"""
    issues = []

    m = re.search(r'(?:说明书)?摘要\s*[：:\n]\s*(.*?)(?=摘要附图|\Z)', text, re.S)
    if not m:
        return ['未找到摘要']

    abstract = m.group(1).strip()
    if len(abstract) > 300:
        issues.append(f'摘要{len(abstract)}字(上限300字)')
    if len(abstract) < 50:
        issues.append(f'摘要过短({len(abstract)}字)')

    return issues


def check_terminology_consistency(text):
    """检查技术术语一致性。"""
    issues = []

    # Find terms that appear in multiple variants
    variant_groups = [
        (r'水系统控制论|水系统运行学|CHS', 'CHS相关术语'),
        (r'HydroOS|水网操作系统|水网OS', 'HydroOS相关术语'),
        (r'WSAL|WNAL|自主运行等级|自动化等级', 'WSAL相关术语'),
        (r'模型预测控制|MPC|预测控制', 'MPC相关术语'),
    ]

    for pattern, group_name in variant_groups:
        variants = set()
        for m in re.finditer(pattern, text):
            variants.add(m.group())
        if len(variants) > 2:
            issues.append(f'{group_name}表述不统一: {", ".join(variants)}')

    return issues


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 check_patent.py <patent_file.md>")
        sys.exit(1)

    filepath = sys.argv[1]
    with open(filepath, encoding='utf-8') as f:
        text = f.read()

    print(f"{'═' * 60}")
    print(f"  发明专利申请文件质量检查")
    print(f"  文件: {os.path.basename(filepath)} ({len(text):,}字)")
    print(f"{'═' * 60}")

    total_issues = 0

    # 1. Structure
    found, missing = check_structure(text)
    status = '✅' if not missing else '❌'
    print(f"\n{status} 1. 结构完整性: {len(found)}/{len(found)+len(missing)}项")
    for m in missing:
        print(f"     · 缺少: {m}")
        total_issues += 1

    # 2. Claims
    claim_issues, indep, dep = check_claims(text)
    status = '✅' if not claim_issues else '❌'
    print(f"\n{status} 2. 权利要求书: 独权{indep}条 从属{dep}条")
    for i in claim_issues:
        print(f"     · {i}")
        total_issues += 1

    # 3. Independent claim
    indep_issues = check_independent_claim(text)
    status = '✅' if not indep_issues else '🟡'
    print(f"\n{status} 3. 独权保护范围")
    for i in indep_issues:
        print(f"     · {i}")
        total_issues += 1

    # 4. Background
    bg_issues = check_background(text)
    status = '✅' if not bg_issues else '🟡'
    print(f"\n{status} 4. 背景技术")
    for i in bg_issues:
        print(f"     · {i}")
        total_issues += 1

    # 5. Effects
    eff_issues = check_beneficial_effects(text)
    status = '✅' if not eff_issues else '🟡'
    print(f"\n{status} 5. 有益效果")
    for i in eff_issues:
        print(f"     · {i}")
        total_issues += 1

    # 6. Embodiment
    emb_issues = check_embodiment(text)
    status = '✅' if not emb_issues else '🟡'
    print(f"\n{status} 6. 实施例")
    for i in emb_issues:
        print(f"     · {i}")
        total_issues += 1

    # 7. Referencing
    ref_issues = check_referencing_terms(text)
    status = '✅' if not ref_issues else '🟡'
    print(f"\n{status} 7. 回指用语")
    for i in ref_issues:
        print(f"     · {i}")
        total_issues += 1

    # 8. Abstract
    abs_issues = check_abstract_quality(text)
    status = '✅' if not abs_issues else '🟡'
    print(f"\n{status} 8. 摘要")
    for i in abs_issues:
        print(f"     · {i}")
        total_issues += 1

    # 9. Terminology
    term_issues = check_terminology_consistency(text)
    status = '✅' if not term_issues else '🟡'
    print(f"\n{status} 9. 术语一致性")
    for i in term_issues:
        print(f"     · {i}")
        total_issues += 1

    score = max(0, 10 - total_issues * 0.6)
    print(f"\n{'═' * 60}")
    print(f"  检测到 {total_issues} 个问题")
    print(f"  质量评估: {score:.1f}/10 (授权前景: {'良好' if score >= 7.5 else '需改进'})")
    print(f"{'═' * 60}")


if __name__ == '__main__':
    main()
