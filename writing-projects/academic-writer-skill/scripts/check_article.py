#!/usr/bin/env python3
"""
公众号文章质量自动检查脚本
用法: python3 check_article.py <文件路径>
配合 writing-projects/SKILL.md 使用
"""
import re
import sys
import json
from collections import Counter

def load_article(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def strip_markdown(text):
    """去除Markdown标记，保留纯文字"""
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'\[([^\]]+)\]\(.*?\)', r'\1', text)
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'^>\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'^---\s*$', '', text, flags=re.MULTILINE)
    return text

def check_paragraph_length(content):
    """检查段落长度"""
    issues = []
    lines = content.split('\n')
    para = ''
    para_start = 0
    para_line = 0
    
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped == '' or stripped.startswith('#') or stripped == '---':
            if para.strip():
                pure = strip_markdown(para).strip()
                char_count = len(pure)
                if char_count > 200:
                    preview = pure[:40] + '...'
                    issues.append({
                        'level': 'SEVERE',
                        'category': '段落长度',
                        'line': para_line,
                        'message': f'段落过长({char_count}字)，手机上形成文字墙',
                        'preview': preview,
                        'suggestion': '拆分为2-3段，每段不超过150字'
                    })
                elif char_count > 150:
                    preview = pure[:40] + '...'
                    issues.append({
                        'level': 'WARNING',
                        'category': '段落长度',
                        'line': para_line,
                        'message': f'段落偏长({char_count}字)',
                        'preview': preview,
                        'suggestion': '建议拆分'
                    })
            para = ''
            para_start = i + 1
        else:
            if not para:
                para_line = i
            para += stripped
    
    # 处理最后一段
    if para.strip():
        pure = strip_markdown(para).strip()
        char_count = len(pure)
        if char_count > 200:
            issues.append({
                'level': 'SEVERE', 'category': '段落长度', 'line': para_line,
                'message': f'最后段落过长({char_count}字)', 'suggestion': '拆分'
            })
    
    return issues

def check_sentence_length(content):
    """检查句子长度"""
    issues = []
    pure = strip_markdown(content)
    # 按中文句末标点切分
    sentences = re.split(r'[。！？\n]', pure)
    for s in sentences:
        s = s.strip()
        if len(s) > 70:
            preview = s[:35] + '...'
            issues.append({
                'level': 'WARNING',
                'category': '句子长度',
                'message': f'长句({len(s)}字): {preview}',
                'suggestion': '拆分为两个短句'
            })
    return issues

def check_heading_levels(content):
    """检查标题层级"""
    issues = []
    lines = content.split('\n')
    h1_count = 0
    for i, line in enumerate(lines, 1):
        if line.startswith('# ') and not line.startswith('## '):
            h1_count += 1
            if h1_count > 1:
                issues.append({
                    'level': 'WARNING', 'category': '标题层级', 'line': i,
                    'message': f'出现第{h1_count}个一级标题，全文应仅有一个',
                    'suggestion': '降级为二级标题(##)'
                })
        if line.startswith('### '):
            issues.append({
                'level': 'SEVERE', 'category': '标题层级', 'line': i,
                'message': '出现三级标题，公众号文章禁止使用三级及以下标题',
                'suggestion': '改为加粗文字或并入上级标题'
            })
        if line.startswith('#### '):
            issues.append({
                'level': 'SEVERE', 'category': '标题层级', 'line': i,
                'message': '出现四级标题，严重违规',
                'suggestion': '删除或改为加粗文字'
            })
    return issues

def check_typos(content):
    """检查常见错别字和易混词"""
    issues = []
    typo_map = {
        '帐号': '账号', '帐户': '账户', '帐目': '账目',
        '好象': '好像', '象是': '像是',
        '在也': '再也', '在次': '再次', '在三': '再三',
        '以经': '已经', '以后': '注意区分"以后"(将来)和"已后"',
        '增加水平': '提高水平', '增加能力': '提升能力',
        '发挥效益': '注意搭配：发挥作用/产生效益',
    }
    for wrong, correct in typo_map.items():
        if wrong in content:
            issues.append({
                'level': 'CHECK', 'category': '错别字',
                'message': f"发现'{wrong}'",
                'suggestion': f"请确认是否应为'{correct}'"
            })
    
    # 检查"的地得"
    # 简单规则：动词+的+动词 → 可能应为"地"
    de_patterns = re.findall(r'[\u4e00-\u9fff]{1,4}的[\u4e00-\u9fff]{2,4}着', content)
    if de_patterns:
        issues.append({
            'level': 'CHECK', 'category': '的地得',
            'message': f'可能存在"的/地"混用: {de_patterns[:3]}',
            'suggestion': '修饰动词用"地"，修饰名词用"的"'
        })
    
    return issues

def check_punctuation(content):
    """检查标点符号"""
    issues = []
    
    # 中文语境中使用英文标点
    mixed = re.findall(r'[\u4e00-\u9fff][,;:!?][\u4e00-\u9fff]', content)
    if mixed:
        issues.append({
            'level': 'WARNING', 'category': '标点符号',
            'message': f'中文间使用英文标点({len(mixed)}处): {mixed[:5]}',
            'suggestion': '替换为对应的中文标点'
        })
    
    # 检查破折号
    if '--' in content and '——' not in content.replace('---', ''):
        issues.append({
            'level': 'WARNING', 'category': '标点符号',
            'message': "使用了'--'而非中文破折号'——'",
            'suggestion': "替换为'——'（两个em dash）"
        })
    
    # 检查省略号
    if '...' in content and '……' not in content:
        issues.append({
            'level': 'CHECK', 'category': '标点符号',
            'message': "使用了英文省略号'...'",
            'suggestion': "中文语境建议使用'……'"
        })
    
    return issues

def check_spacing(content):
    """检查中英文间距"""
    issues = []
    # 中文紧跟英文字母（无空格）
    no_space_patterns = re.findall(
        r'([\u4e00-\u9fff][A-Za-z]|[A-Za-z][\u4e00-\u9fff])', content
    )
    # 过滤掉Markdown标记内的
    real_issues = []
    for p in no_space_patterns:
        # 排除标题标记等
        if p not in ['#', '**', '##']:
            real_issues.append(p)
    
    if len(real_issues) > 0:
        issues.append({
            'level': 'WARNING', 'category': '中英间距',
            'message': f'发现{len(real_issues)}处中英文间缺少空格',
            'preview': str(real_issues[:8]),
            'suggestion': '中文与英文/数字之间加一个半角空格'
        })
    
    return issues

def check_bold_density(content):
    """检查加粗密度"""
    issues = []
    sections = re.split(r'^## ', content, flags=re.MULTILINE)
    for idx, sec in enumerate(sections[1:], 1):
        # 提取节标题
        title_match = re.match(r'(.+?)[\n]', sec)
        title = title_match.group(1).strip() if title_match else f'第{idx}节'
        
        bolds = re.findall(r'\*\*[^*]+\*\*', sec)
        if len(bolds) > 5:
            issues.append({
                'level': 'WARNING', 'category': '加粗密度',
                'message': f'"{title}"中加粗{len(bolds)}处(建议≤3)',
                'suggestion': '减少加粗，只保留最关键的点睛句和数据'
            })
        
        # 检查连续加粗段
        lines_in_sec = sec.split('\n')
        consecutive_bold = 0
        for line in lines_in_sec:
            if line.strip().startswith('**') and line.strip().endswith('**'):
                consecutive_bold += 1
                if consecutive_bold >= 2:
                    issues.append({
                        'level': 'WARNING', 'category': '加粗密度',
                        'message': f'"{title}"中出现连续加粗段落',
                        'suggestion': '连续加粗段落造成视觉疲劳，间隔使用'
                    })
                    break
            else:
                consecutive_bold = 0
    
    return issues

def check_banned_words(content):
    """检查禁用词"""
    issues = []
    banned = {
        '赋能': '换用"支撑""助力""推动"等',
        '抓手': '换用"切入点""着力点""关键环节"等',
        '颗粒度': '换用"精细程度""细致程度"等',
        '对齐': '换用"统一""协调""一致"等（技术术语除外）',
        '打法': '换用"策略""方法""路径"等',
        '笔者认为': '直接陈述观点即可',
        '本文将': '直接开始写即可',
        '综上所述': '换用更有力的结束方式',
        '总而言之': '换用更有力的结束方式',
        '众所周知': '删除，直接陈述事实',
        '不言而喻': '删除，用事实说话',
    }
    for word, suggestion in banned.items():
        count = content.count(word)
        if count > 0:
            issues.append({
                'level': 'WARNING', 'category': '禁用词',
                'message': f"发现'{word}'({count}次)",
                'suggestion': suggestion
            })
    return issues

def check_opening(content):
    """检查开头质量"""
    issues = []
    lines = content.split('\n')
    first_para = ''
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith('#') and stripped != '---':
            first_para = stripped
            break
    
    if first_para:
        bad_starts = {
            '随着': '空泛开头，缺乏吸引力',
            '近年来': '空泛开头，建议用数据/问题/判断开篇',
            '当前': '空泛开头',
            '在新时代': '口号式开头',
            '为了': '文件式开头',
        }
        for prefix, reason in bad_starts.items():
            if first_para.startswith(prefix):
                issues.append({
                    'level': 'WARNING', 'category': '开头质量',
                    'message': f"文章以'{prefix}'开头——{reason}",
                    'suggestion': '建议用一个数字、反常识判断、问题或画面开篇'
                })
    return issues

def check_ending(content):
    """检查结尾"""
    issues = []
    lines = [l.strip() for l in content.split('\n') if l.strip()]
    
    # 检查署名行
    for line in lines[-5:]:
        if re.match(r'^(作者|撰文|文/|——.+$)', line):
            issues.append({
                'level': 'SEVERE', 'category': '结尾格式',
                'message': '文末包含作者署名行',
                'suggestion': '删除（用户要求文末不写署名）'
            })
    
    # 检查空泛结尾
    for line in lines[-3:]:
        if line.startswith('综上所述') or line.startswith('总而言之') or line.startswith('总之'):
            issues.append({
                'level': 'WARNING', 'category': '结尾质量',
                'message': f'结尾使用"{line[:6]}..."——缺乏回味感',
                'suggestion': '用提出新问题、回扣开头、有力判断等方式结束'
            })
    
    return issues

def check_bullet_lists(content):
    """检查正文中的bullet列表"""
    issues = []
    lines = content.split('\n')
    bullet_count = 0
    first_bullet_line = 0
    in_code_block = False
    
    for i, line in enumerate(lines, 1):
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        if re.match(r'^\s*[-*]\s+\S', line) and not line.startswith('#'):
            bullet_count += 1
            if first_bullet_line == 0:
                first_bullet_line = i
    
    if bullet_count > 0:
        issues.append({
            'level': 'WARNING', 'category': 'Bullet列表',
            'line': first_bullet_line,
            'message': f'正文中使用了{bullet_count}个bullet列表项',
            'suggestion': '公众号排版易错位，改用自然语言列举（如"包括三方面：第一...第二...第三..."）'
        })
    
    return issues

def check_word_frequency(content):
    """检查高频重复词"""
    issues = []
    pure = strip_markdown(content)
    # 提取2-4字词组的简单方法
    words = re.findall(r'[\u4e00-\u9fff]{2,4}', pure)
    freq = Counter(words)
    
    # 排除常见虚词
    common = {'这个', '那个', '一个', '可以', '不是', '就是', '但是', '而且', 
              '因为', '所以', '如果', '已经', '的是', '也是', '还是', '不能',
              '能够', '什么', '他们', '我们', '需要', '进行', '通过', '实现',
              '系统', '工程', '水利', '控制', '水网', '技术', '管理', '运行'}
    
    for word, count in freq.most_common(30):
        if word not in common and count >= 8:
            issues.append({
                'level': 'CHECK', 'category': '用词重复',
                'message': f"'{word}'出现{count}次",
                'suggestion': '考虑使用同义词替换部分出现'
            })
    
    return issues

def generate_stats(content):
    """生成文章基本统计"""
    pure = strip_markdown(content)
    char_count = len(re.sub(r'\s', '', pure))
    
    lines = content.split('\n')
    h2_count = sum(1 for l in lines if l.startswith('## '))
    
    # 段落数
    paras = [p for p in re.split(r'\n\s*\n', content) 
             if p.strip() and not p.strip().startswith('#') and p.strip() != '---']
    
    # 预计阅读时间（中文约400字/分钟）
    read_time = round(char_count / 400, 1)
    
    return {
        '总字数': char_count,
        '节数': h2_count,
        '段落数': len(paras),
        '预计阅读时间': f'{read_time}分钟',
    }

def run_all_checks(filepath):
    """执行全部检查"""
    content = load_article(filepath)
    
    all_issues = []
    all_issues.extend(check_paragraph_length(content))
    all_issues.extend(check_sentence_length(content))
    all_issues.extend(check_heading_levels(content))
    all_issues.extend(check_typos(content))
    all_issues.extend(check_punctuation(content))
    all_issues.extend(check_spacing(content))
    all_issues.extend(check_bold_density(content))
    all_issues.extend(check_banned_words(content))
    all_issues.extend(check_bullet_lists(content))
    all_issues.extend(check_opening(content))
    all_issues.extend(check_ending(content))
    all_issues.extend(check_word_frequency(content))
    
    stats = generate_stats(content)
    
    # 输出报告
    print(f"\n{'='*65}")
    print(f" 📝 公众号文章质量检查报告")
    print(f"{'='*65}")
    print(f"\n📊 基本统计:")
    for k, v in stats.items():
        print(f"   {k}: {v}")
    
    if not all_issues:
        print(f"\n✅ 所有{11}项检查全部通过！文章可以发布。\n")
        return True
    
    # 按级别分组
    severe = [i for i in all_issues if i['level'] == 'SEVERE']
    warning = [i for i in all_issues if i['level'] == 'WARNING']
    check = [i for i in all_issues if i['level'] == 'CHECK']
    
    print(f"\n共发现 {len(all_issues)} 个问题 "
          f"(🔴严重:{len(severe)} 🟡警告:{len(warning)} ⚪待确认:{len(check)})")
    
    if severe:
        print(f"\n🔴 严重问题（必须修正才能发布）:")
        print(f"{'—'*55}")
        for i, item in enumerate(severe, 1):
            line_info = f"[第{item['line']}行]" if 'line' in item else ''
            print(f"  {i}. {line_info} {item['message']}")
            print(f"     → {item['suggestion']}")
    
    if warning:
        print(f"\n🟡 警告（强烈建议修正）:")
        print(f"{'—'*55}")
        for i, item in enumerate(warning, 1):
            line_info = f"[第{item.get('line', '?')}行]" if 'line' in item else ''
            print(f"  {i}. [{item['category']}] {line_info} {item['message']}")
            print(f"     → {item['suggestion']}")
    
    if check:
        print(f"\n⚪ 需人工确认:")
        print(f"{'—'*55}")
        for i, item in enumerate(check, 1):
            print(f"  {i}. [{item['category']}] {item['message']}")
            print(f"     → {item['suggestion']}")
    
    print(f"\n{'='*65}")
    
    if severe:
        print("❌ 存在严重问题，文章尚不能发布。请修正后重新检查。")
    elif warning:
        print("⚠️  存在警告项，建议修正后发布。")
    else:
        print("✅ 仅有待确认项，人工确认后即可发布。")
    
    print()
    return len(severe) == 0

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python3 check_article.py <文章文件路径>")
        print("示例: python3 check_article.py article.md")
        sys.exit(1)
    
    filepath = sys.argv[1]
    passed = run_all_checks(filepath)
    sys.exit(0 if passed else 1)
