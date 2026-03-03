"""
T2b 第六章 全部7张插图生成脚本
使用 matplotlib 绘制，中文标注，统一配色
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

# ========== 统一配色 ==========
C_PRIMARY   = '#1565C0'  # 深蓝
C_GREEN     = '#4CAF50'  # 绿/安全
C_PURPLE    = '#7B1FA2'  # 紫/认知
C_ORANGE    = '#FF7043'  # 橙红/警告
C_BG        = '#FFFFFF'
C_GRID      = '#E0E0E0'
C_YELLOW    = '#FFC107'
C_RED       = '#D32F2F'
C_LIGHT_BLUE = '#BBDEFB'
C_MID_BLUE   = '#64B5F6'
C_DARK_BLUE  = '#0D47A1'
C_BLUE_GREY  = '#78909C'
C_LIGHT_GREY = '#F5F5F5'
C_GREY       = '#9E9E9E'

OUT = os.path.dirname(os.path.abspath(__file__))

# 中文字体设置
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 11


# =====================================================
# 图6-1: HydroClaw 五层架构原理图
# =====================================================
def fig6_1():
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    fig.patch.set_facecolor(C_BG)

    # 五层金字塔（从底到顶）
    layers = [
        {'name': 'L0 Core — 领域算法层', 'desc': '仿真 / 控制 / 预测 / 辨识等14个领域模块',
         'color': C_BLUE_GREY, 'y': 0.8, 'w': 12, 'comp': 'Saint-Venant · MPC · Kalman'},
        {'name': 'L1 Tool — 工具层', 'desc': 'MCP协议封装的可调用工具',
         'color': C_LIGHT_BLUE, 'y': 2.6, 'w': 10, 'comp': 'run_simulation · get_forecast · check_odd'},
        {'name': 'L2 Skill — 工作流层', 'desc': '固定工作流（"快思考"）',
         'color': C_MID_BLUE, 'y': 4.4, 'w': 8, 'comp': '四预闭环 · 日常巡检 · 应急处置'},
        {'name': 'L3 Agent — 智能体层', 'desc': '自主推理（"慢思考"）',
         'color': C_PRIMARY, 'y': 6.2, 'w': 6, 'comp': 'ForecastAgent · ScheduleAgent · SafetyAgent'},
        {'name': 'L4 Orchestrator — 编排层', 'desc': '任务分发 · 路由 · 安全审核',
         'color': C_DARK_BLUE, 'y': 8.0, 'w': 4, 'comp': '四级路由 · Planning · 人类审批'},
    ]

    for i, layer in enumerate(layers):
        x = (14 - layer['w']) / 2
        rect = FancyBboxPatch((x, layer['y']), layer['w'], 1.5,
                              boxstyle="round,pad=0.15", linewidth=1.5,
                              edgecolor='white', facecolor=layer['color'], alpha=0.9)
        ax.add_patch(rect)
        # 层名（白色粗体）
        ax.text(7, layer['y'] + 0.95, layer['name'],
                ha='center', va='center', fontsize=13, fontweight='bold', color='white')
        # 描述（白色小字）
        ax.text(7, layer['y'] + 0.4, layer['desc'],
                ha='center', va='center', fontsize=9.5, color='#E3F2FD')

    # 右侧标注：三级抽象
    ax.annotate('', xy=(13.2, 7.0), xytext=(13.2, 2.6),
                arrowprops=dict(arrowstyle='->', color=C_ORANGE, lw=2))
    ax.text(13.4, 4.8, 'Tool → Skill → Agent\n三级抽象', fontsize=9,
            color=C_ORANGE, va='center', ha='left', fontstyle='italic')

    # 左侧标注：数据流↑ 控制流↓
    ax.annotate('', xy=(0.6, 8.5), xytext=(0.6, 1.5),
                arrowprops=dict(arrowstyle='->', color=C_GREEN, lw=2))
    ax.text(0.3, 5.0, '数\n据\n流\n↑', fontsize=10, color=C_GREEN,
            va='center', ha='center', fontweight='bold')

    ax.annotate('', xy=(1.2, 1.5), xytext=(1.2, 8.5),
                arrowprops=dict(arrowstyle='->', color=C_RED, lw=2))
    ax.text(1.5, 5.0, '控\n制\n流\n↓', fontsize=10, color=C_RED,
            va='center', ha='center', fontweight='bold')

    # 标题
    ax.text(7, 9.7, '图6-1  HydroClaw 五层架构原理图', ha='center', va='center',
            fontsize=15, fontweight='bold', color='#212121')

    fig.tight_layout()
    fig.savefig(os.path.join(OUT, 'fig6-1_five_layer_arch.png'), dpi=200, bbox_inches='tight',
                facecolor=C_BG, edgecolor='none')
    plt.close(fig)
    print('  ✓ 图6-1 完成')


# =====================================================
# 图6-2: MCP 工具协议三要素
# =====================================================
def fig6_2():
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 7)
    ax.axis('off')
    fig.patch.set_facecolor(C_BG)

    col_x = [1.5, 5.5, 9.5]
    col_titles = ['工具描述', '工具发现', '工具调用']
    col_subtitles = ['Tool Description', 'Tool Discovery', 'Tool Invocation']
    col_icons = ['{ }', '🔍', '▶']

    for i, (x, title, sub) in enumerate(zip(col_x, col_titles, col_subtitles)):
        # 卡片背景
        rect = FancyBboxPatch((x - 1.3, 1.2), 3.2, 4.5,
                              boxstyle="round,pad=0.2", linewidth=2,
                              edgecolor=C_PRIMARY, facecolor='#E3F2FD', alpha=0.3)
        ax.add_patch(rect)

        # 标题
        ax.text(x + 0.3, 5.2, title, ha='center', va='center',
                fontsize=14, fontweight='bold', color=C_PRIMARY)
        ax.text(x + 0.3, 4.7, sub, ha='center', va='center',
                fontsize=9, color=C_GREY, fontstyle='italic')

    # 左列内容：JSON Schema 卡片
    schema_lines = [
        'name: "forecast_tool"',
        'params: {',
        '  station_id: string',
        '  horizon: int',
        '}',
        'returns: object',
    ]
    for j, line in enumerate(schema_lines):
        ax.text(1.8, 3.9 - j * 0.35, line, fontsize=8.5,
                color='#37474F', va='center')

    # 中列内容：注册中心
    # 服务器图标
    for j, (yy, label) in enumerate([(3.8, 'MCP 服务器 A'), (3.0, 'MCP 服务器 B'), (2.2, 'MCP 服务器 C')]):
        rect2 = FancyBboxPatch((4.6, yy - 0.2), 2.5, 0.5,
                               boxstyle="round,pad=0.08", linewidth=1,
                               edgecolor=C_PRIMARY, facecolor=C_LIGHT_BLUE, alpha=0.6)
        ax.add_patch(rect2)
        ax.text(5.85, yy + 0.05, label, ha='center', va='center', fontsize=9, color=C_DARK_BLUE)

    # 注册中心
    reg = FancyBboxPatch((5.0, 1.3), 1.7, 0.5,
                         boxstyle="round,pad=0.08", linewidth=2,
                         edgecolor=C_GREEN, facecolor='#E8F5E9')
    ax.add_patch(reg)
    ax.text(5.85, 1.55, '注册中心', ha='center', va='center', fontsize=10, fontweight='bold', color=C_GREEN)
    for yy in [3.6, 2.8, 2.0]:
        ax.annotate('', xy=(5.85, 1.8), xytext=(5.85, yy),
                    arrowprops=dict(arrowstyle='->', color=C_GREEN, lw=1.2, ls='--'))

    # 右列内容：请求→处理→响应→日志
    steps = ['请求 (Request)', '处理 (Execute)', '响应 (Response)', '日志 (Audit)']
    step_colors = [C_PRIMARY, C_PRIMARY, C_GREEN, C_ORANGE]
    for j, (step, sc) in enumerate(zip(steps, step_colors)):
        yy = 4.0 - j * 0.8
        rect3 = FancyBboxPatch((8.6, yy - 0.2), 2.5, 0.5,
                               boxstyle="round,pad=0.08", linewidth=1.5,
                               edgecolor=sc, facecolor='white')
        ax.add_patch(rect3)
        ax.text(9.85, yy + 0.05, step, ha='center', va='center', fontsize=9.5, color=sc, fontweight='bold')
        if j < 3:
            ax.annotate('', xy=(9.85, yy - 0.25), xytext=(9.85, yy - 0.5),
                        arrowprops=dict(arrowstyle='->', color='#616161', lw=1.5))

    # 底部标注
    ax.annotate('', xy=(5.0, 0.6), xytext=(2.0, 0.6),
                arrowprops=dict(arrowstyle='->', color=C_GREY, lw=1.5))
    ax.text(3.5, 0.35, '描述使发现成为可能', fontsize=9, ha='center', color='#616161')
    ax.annotate('', xy=(9.5, 0.6), xytext=(6.5, 0.6),
                arrowprops=dict(arrowstyle='->', color=C_GREY, lw=1.5))
    ax.text(8.0, 0.35, '发现使调用有据可依', fontsize=9, ha='center', color='#616161')

    # 标题
    ax.text(7, 6.6, '图6-2  MCP 工具协议三要素', ha='center', va='center',
            fontsize=15, fontweight='bold', color='#212121')

    fig.tight_layout()
    fig.savefig(os.path.join(OUT, 'fig6-2_mcp_three_elements.png'), dpi=200, bbox_inches='tight',
                facecolor=C_BG, edgecolor='none')
    plt.close(fig)
    print('  ✓ 图6-2 完成')


# =====================================================
# 图6-3: 四预闭环条件链路图
# =====================================================
def fig6_3():
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 6)
    ax.axis('off')
    fig.patch.set_facecolor(C_BG)

    # 标题
    ax.text(7, 5.6, '图6-3  四预闭环条件链路图', ha='center', va='center',
            fontsize=15, fontweight='bold', color='#212121')
    ax.text(7, 5.1, '条件链接：逐级触发，按需执行', ha='center', va='center',
            fontsize=11, color=C_ORANGE, fontstyle='italic')

    # 四个步骤
    steps = [
        {'name': '预  报', 'tool': 'run_forecast()', 'x': 1.5},
        {'name': '预  警', 'tool': 'check_alert()', 'x': 4.5},
        {'name': '预  演', 'tool': 'run_simulation()', 'x': 9.0},
        {'name': '预  案', 'tool': 'generate_plan()', 'x': 12.0},
    ]

    for i, step in enumerate(steps):
        rect = FancyBboxPatch((step['x'] - 0.9, 2.8), 1.8, 1.2,
                              boxstyle="round,pad=0.15", linewidth=2,
                              edgecolor=C_PRIMARY, facecolor=C_PRIMARY, alpha=0.9)
        ax.add_patch(rect)
        ax.text(step['x'], 3.55, step['name'], ha='center', va='center',
                fontsize=14, fontweight='bold', color='white')
        ax.text(step['x'], 3.1, step['tool'], ha='center', va='center',
                fontsize=8, color='#BBDEFB')

    # 箭头：预报→预警
    ax.annotate('', xy=(3.5, 3.4), xytext=(2.5, 3.4),
                arrowprops=dict(arrowstyle='->', color='#424242', lw=2))

    # 菱形判断节点
    diamond_x, diamond_y = 6.7, 3.4
    diamond = plt.Polygon([(diamond_x, diamond_y + 0.7),
                           (diamond_x + 0.9, diamond_y),
                           (diamond_x, diamond_y - 0.7),
                           (diamond_x - 0.9, diamond_y)],
                          closed=True, facecolor=C_ORANGE, edgecolor='#E64A19', linewidth=2)
    ax.add_patch(diamond)
    ax.text(diamond_x, diamond_y + 0.05, '预警等级\n≥黄色?', ha='center', va='center',
            fontsize=8.5, fontweight='bold', color='white')

    # 预警→菱形
    ax.annotate('', xy=(diamond_x - 0.95, diamond_y), xytext=(5.4, diamond_y),
                arrowprops=dict(arrowstyle='->', color='#424242', lw=2))

    # 菱形→"否"→绿色终止
    ax.annotate('', xy=(diamond_x, 1.5), xytext=(diamond_x, diamond_y - 0.75),
                arrowprops=dict(arrowstyle='->', color=C_GREEN, lw=2))
    ax.text(diamond_x + 0.3, 2.2, '否', fontsize=11, color=C_GREEN, fontweight='bold')

    # 绿色终止符
    term = FancyBboxPatch((diamond_x - 0.7, 0.8), 1.4, 0.6,
                          boxstyle="round,pad=0.15", linewidth=2,
                          edgecolor=C_GREEN, facecolor=C_GREEN, alpha=0.8)
    ax.add_patch(term)
    ax.text(diamond_x, 1.1, '正常运行', ha='center', va='center',
            fontsize=11, fontweight='bold', color='white')

    # 菱形→"是"→预演
    ax.annotate('', xy=(8.1, diamond_y), xytext=(diamond_x + 0.95, diamond_y),
                arrowprops=dict(arrowstyle='->', color=C_RED, lw=2.5))
    ax.text(7.5, diamond_y + 0.35, '是', fontsize=11, color=C_RED, fontweight='bold')

    # 预演→预案
    ax.annotate('', xy=(11.1, 3.4), xytext=(9.9, 3.4),
                arrowprops=dict(arrowstyle='->', color='#424242', lw=2))

    fig.tight_layout()
    fig.savefig(os.path.join(OUT, 'fig6-3_four_forecast_loop.png'), dpi=200, bbox_inches='tight',
                facecolor=C_BG, edgecolor='none')
    plt.close(fig)
    print('  ✓ 图6-3 完成')


# =====================================================
# 图6-4: Orchestrator 四级路由原理
# =====================================================
def fig6_4():
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    fig.patch.set_facecolor(C_BG)

    # 标题
    ax.text(5, 9.6, '图6-4  Orchestrator 四级路由原理', ha='center', va='center',
            fontsize=14, fontweight='bold', color='#212121')

    # 用户请求入口
    ax.text(5, 9.0, '▼ 用户请求', ha='center', va='center',
            fontsize=12, fontweight='bold', color='#424242')
    ax.annotate('', xy=(5, 8.5), xytext=(5, 8.8),
                arrowprops=dict(arrowstyle='->', color='#424242', lw=2))

    # 漏斗四层
    funnel = [
        {'name': '第一级：Skill 短语匹配', 'color': '#BBDEFB', 'y': 7.5, 'w': 8.0,
         'speed': '~毫秒', 'desc': '覆盖80%日常请求'},
        {'name': '第二级：工具关键词匹配', 'color': '#90CAF9', 'y': 5.8, 'w': 6.0,
         'speed': '~秒', 'desc': '单工具直接调用'},
        {'name': '第三级：能力路由', 'color': '#42A5F5', 'y': 4.1, 'w': 4.5,
         'speed': '~秒', 'desc': '按Agent能力矩阵分发'},
        {'name': '第四级：Planning 分解', 'color': C_DARK_BLUE, 'y': 2.4, 'w': 3.0,
         'speed': '~分钟', 'desc': '仅用于复杂多步任务'},
    ]

    for i, f in enumerate(funnel):
        x = (10 - f['w']) / 2
        text_color = 'white' if i >= 2 else '#0D47A1'
        rect = FancyBboxPatch((x, f['y']), f['w'], 1.1,
                              boxstyle="round,pad=0.12", linewidth=2,
                              edgecolor='white', facecolor=f['color'], alpha=0.95)
        ax.add_patch(rect)
        ax.text(5, f['y'] + 0.7, f['name'], ha='center', va='center',
                fontsize=12, fontweight='bold', color=text_color)
        ax.text(5, f['y'] + 0.25, f['desc'], ha='center', va='center',
                fontsize=9, color=text_color, alpha=0.8)

        # 右侧响应速度
        ax.text(9.5, f['y'] + 0.55, f['speed'], ha='center', va='center',
                fontsize=10, fontweight='bold', color=f['color'] if i < 2 else 'white',
                bbox=dict(boxstyle='round,pad=0.3', facecolor=f['color'], edgecolor='none', alpha=0.3))

        # 层间箭头
        if i < 3:
            ax.annotate('', xy=(5, funnel[i+1]['y'] + 1.1), xytext=(5, f['y']),
                        arrowprops=dict(arrowstyle='->', color='#9E9E9E', lw=1.5, ls='--'))

    # 左侧标注
    ax.annotate('', xy=(0.5, 8.0), xytext=(0.5, 3.0),
                arrowprops=dict(arrowstyle='<->', color=C_ORANGE, lw=1.5))
    ax.text(0.15, 7.3, '快\n速\n确\n定', fontsize=9, color=C_GREEN, ha='center', fontweight='bold')
    ax.text(0.15, 3.8, '慢\n速\n灵\n活', fontsize=9, color=C_PURPLE, ha='center', fontweight='bold')

    # 右侧标注
    ax.text(9.5, 8.3, '响应速度', ha='center', va='center',
            fontsize=10, fontweight='bold', color='#616161')

    # 底部输出
    ax.annotate('', xy=(5, 1.5), xytext=(5, 2.4),
                arrowprops=dict(arrowstyle='->', color='#424242', lw=2))
    ax.text(5, 1.2, '▼ 执行结果', ha='center', va='center',
            fontsize=12, fontweight='bold', color='#424242')

    fig.tight_layout()
    fig.savefig(os.path.join(OUT, 'fig6-4_orchestrator_routing.png'), dpi=200, bbox_inches='tight',
                facecolor=C_BG, edgecolor='none')
    plt.close(fig)
    print('  ✓ 图6-4 完成')


# =====================================================
# 图6-5: SafetyAgent ODD 三区间否决流程
# =====================================================
def fig6_5():
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 7)
    ax.axis('off')
    fig.patch.set_facecolor(C_BG)

    # 标题
    ax.text(7, 6.6, '图6-5  SafetyAgent ODD 三区间否决流程', ha='center', va='center',
            fontsize=15, fontweight='bold', color='#212121')

    # 左侧：Agent 提出建议
    rect1 = FancyBboxPatch((0.5, 2.8), 2.4, 1.4,
                           boxstyle="round,pad=0.15", linewidth=2,
                           edgecolor=C_PURPLE, facecolor='#F3E5F5')
    ax.add_patch(rect1)
    ax.text(1.7, 3.7, '任意 Agent', ha='center', va='center',
            fontsize=11, fontweight='bold', color=C_PURPLE)
    ax.text(1.7, 3.25, '提出操作建议', ha='center', va='center',
            fontsize=9, color='#6A1B9A')

    # 箭头→SafetyAgent
    ax.annotate('', xy=(3.8, 3.5), xytext=(2.9, 3.5),
                arrowprops=dict(arrowstyle='->', color='#424242', lw=2))

    # 中间：SafetyAgent
    rect2 = FancyBboxPatch((3.8, 2.5), 3.0, 2.0,
                           boxstyle="round,pad=0.15", linewidth=2.5,
                           edgecolor=C_RED, facecolor='#FFEBEE')
    ax.add_patch(rect2)
    ax.text(5.3, 4.0, 'SafetyAgent', ha='center', va='center',
            fontsize=13, fontweight='bold', color=C_RED)
    ax.text(5.3, 3.45, 'check_odd()', ha='center', va='center',
            fontsize=9, color='#B71C1C')
    ax.text(5.3, 3.0, '检查当前状态区间', ha='center', va='center',
            fontsize=9, color='#C62828')

    # 三条分支
    # 上方绿色：normal → 放行
    ax.annotate('', xy=(9.0, 5.2), xytext=(6.8, 4.2),
                arrowprops=dict(arrowstyle='->', color=C_GREEN, lw=2.5))
    rect_g = FancyBboxPatch((9.0, 4.8), 3.5, 0.9,
                            boxstyle="round,pad=0.12", linewidth=2,
                            edgecolor=C_GREEN, facecolor=C_GREEN, alpha=0.9)
    ax.add_patch(rect_g)
    ax.text(10.75, 5.25, 'Normal  >>  放行，执行操作', ha='center', va='center',
            fontsize=11, fontweight='bold', color='white')

    # 中间黄色：extended → 人工确认
    ax.annotate('', xy=(9.0, 3.5), xytext=(6.8, 3.5),
                arrowprops=dict(arrowstyle='->', color=C_YELLOW, lw=2.5))
    rect_y = FancyBboxPatch((9.0, 3.0), 3.5, 0.9,
                            boxstyle="round,pad=0.12", linewidth=2,
                            edgecolor=C_YELLOW, facecolor=C_YELLOW, alpha=0.85)
    ax.add_patch(rect_y)
    ax.text(10.75, 3.45, 'Extended  >>  人工确认对话框', ha='center', va='center',
            fontsize=11, fontweight='bold', color='#5D4037')

    # 下方红色：mrc → 否决
    ax.annotate('', xy=(9.0, 1.8), xytext=(6.8, 2.8),
                arrowprops=dict(arrowstyle='->', color=C_RED, lw=3.5))
    rect_r = FancyBboxPatch((9.0, 1.3), 3.5, 0.9,
                            boxstyle="round,pad=0.12", linewidth=3,
                            edgecolor=C_RED, facecolor=C_RED, alpha=0.95)
    ax.add_patch(rect_r)
    ax.text(10.75, 1.75, 'MRC  >>  否决 + 最小风险方案', ha='center', va='center',
            fontsize=11, fontweight='bold', color='white')

    # 底部注释
    ax.text(7, 0.5, 'SafetyAgent 拥有绝对否决权，优先级高于所有其他 Agent',
            ha='center', va='center', fontsize=11, fontweight='bold', color=C_RED,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFCDD2', edgecolor=C_RED, alpha=0.6))

    fig.tight_layout()
    fig.savefig(os.path.join(OUT, 'fig6-5_safety_odd_veto.png'), dpi=200, bbox_inches='tight',
                facecolor=C_BG, edgecolor='none')
    plt.close(fig)
    print('  ✓ 图6-5 完成')


# =====================================================
# 图6-6: 认知API四维框架与角色映射
# =====================================================
def fig6_6():
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    fig.patch.set_facecolor(C_BG)

    # 标题
    ax.text(5, 7.6, '图6-6  认知API四维框架与角色映射', ha='center', va='center',
            fontsize=14, fontweight='bold', color='#212121')

    dims = ['感知\nPerception', '认知\nCognition', '决策\nDecision', '控制\nControl']
    roles = ['operator\n(运维人员)', 'designer\n(设计师)', 'researcher\n(研究员)',
             'admin\n(管理员)', 'teacher\n(教学)']

    # 权限矩阵 (1=可访问蓝, 0=不可访问灰)
    matrix = [
        [1, 0, 0, 1],  # operator: 感知+控制
        [1, 1, 1, 0],  # designer: 感知+认知+决策
        [1, 1, 0, 0],  # researcher: 感知+认知
        [1, 1, 1, 1],  # admin: 全部
        [1, 1, 0, 0],  # teacher: 感知+认知
    ]

    cell_w, cell_h = 1.5, 0.9
    start_x, start_y = 2.5, 1.5

    # 绘制列标题
    for j, dim in enumerate(dims):
        ax.text(start_x + j * cell_w + cell_w / 2, start_y + len(roles) * cell_h + 0.5,
                dim, ha='center', va='center', fontsize=10, fontweight='bold', color=C_PRIMARY)

    # 绘制行标题和单元格
    for i, role in enumerate(roles):
        yi = start_y + (len(roles) - 1 - i) * cell_h
        ax.text(start_x - 0.3, yi + cell_h / 2, role, ha='right', va='center',
                fontsize=9.5, fontweight='bold', color='#424242')
        for j in range(4):
            xj = start_x + j * cell_w
            color = C_PRIMARY if matrix[i][j] else '#E0E0E0'
            alpha = 0.85 if matrix[i][j] else 0.4
            label = '可访问' if matrix[i][j] else '—'
            label_color = 'white' if matrix[i][j] else '#9E9E9E'

            rect = FancyBboxPatch((xj + 0.05, yi + 0.05), cell_w - 0.1, cell_h - 0.1,
                                  boxstyle="round,pad=0.05", linewidth=1,
                                  edgecolor='white', facecolor=color, alpha=alpha)
            ax.add_patch(rect)
            ax.text(xj + cell_w / 2, yi + cell_h / 2, label,
                    ha='center', va='center', fontsize=8.5, color=label_color, fontweight='bold')

    # 右侧标注
    ax.annotate('', xy=(9.2, start_y + len(roles) * cell_h + 0.2),
                xytext=(9.2, start_y),
                arrowprops=dict(arrowstyle='->', color=C_PURPLE, lw=2))
    ax.text(9.5, start_y + len(roles) * cell_h / 2, 'CHS\n四维\n认知\n链路', ha='center', va='center',
            fontsize=10, fontweight='bold', color=C_PURPLE)

    # 顶部维度方向箭头
    ax.annotate('', xy=(start_x + 4 * cell_w, start_y + len(roles) * cell_h + 1.1),
                xytext=(start_x, start_y + len(roles) * cell_h + 1.1),
                arrowprops=dict(arrowstyle='->', color=C_PRIMARY, lw=2))
    ax.text(start_x + 2 * cell_w, start_y + len(roles) * cell_h + 1.35,
            '感知 → 认知 → 决策 → 控制（信息流方向）',
            ha='center', va='center', fontsize=10, color=C_PRIMARY, fontstyle='italic')

    # 图例
    for lx, lc, ll in [(1.0, C_PRIMARY, '可访问'), (2.8, '#E0E0E0', '不可访问')]:
        rect_l = FancyBboxPatch((lx, 0.3), 0.4, 0.3,
                                boxstyle="round,pad=0.03", linewidth=1,
                                edgecolor='white', facecolor=lc, alpha=0.8)
        ax.add_patch(rect_l)
        ax.text(lx + 0.6, 0.45, ll, va='center', fontsize=9, color='#424242')

    fig.tight_layout()
    fig.savefig(os.path.join(OUT, 'fig6-6_cognitive_api_matrix.png'), dpi=200, bbox_inches='tight',
                facecolor=C_BG, edgecolor='none')
    plt.close(fig)
    print('  ✓ 图6-6 完成')


# =====================================================
# 图6-7: 双引擎闭环原理（简洁版）
# =====================================================
def fig6_7():
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    fig.patch.set_facecolor(C_BG)

    # 标题
    ax.text(5, 9.6, '图6-7  双引擎闭环原理（简洁版）', ha='center', va='center',
            fontsize=14, fontweight='bold', color='#212121')

    # 上半圆：认知AI引擎（紫色区域）
    theta_top = np.linspace(0, np.pi, 100)
    r = 3.0
    cx, cy = 5, 5
    x_top = cx + r * np.cos(theta_top)
    y_top = cy + r * np.sin(theta_top)
    ax.fill_between(x_top, cy, y_top, color=C_PURPLE, alpha=0.12)
    ax.plot(x_top, y_top, color=C_PURPLE, lw=2.5)

    ax.text(5, 7.2, '认知AI引擎', ha='center', va='center',
            fontsize=14, fontweight='bold', color=C_PURPLE)

    # 认知三步
    cog_steps = [('理解', 3.2, 6.3), ('推理', 5.0, 6.3), ('提议方案', 6.8, 6.3)]
    for label, sx, sy in cog_steps:
        rect = FancyBboxPatch((sx - 0.65, sy - 0.3), 1.3, 0.6,
                              boxstyle="round,pad=0.08", linewidth=1.5,
                              edgecolor=C_PURPLE, facecolor='#E1BEE7', alpha=0.8)
        ax.add_patch(rect)
        ax.text(sx, sy, label, ha='center', va='center', fontsize=10, fontweight='bold', color='#4A148C')

    ax.annotate('', xy=(4.2, 6.3), xytext=(3.9, 6.3),
                arrowprops=dict(arrowstyle='->', color=C_PURPLE, lw=1.5))
    ax.annotate('', xy=(6.1, 6.3), xytext=(5.7, 6.3),
                arrowprops=dict(arrowstyle='->', color=C_PURPLE, lw=1.5))

    # 下半圆：物理AI引擎（蓝色区域）
    theta_bot = np.linspace(np.pi, 2 * np.pi, 100)
    x_bot = cx + r * np.cos(theta_bot)
    y_bot = cy + r * np.sin(theta_bot)
    ax.fill_between(x_bot, cy, y_bot, color=C_PRIMARY, alpha=0.12)
    ax.plot(x_bot, y_bot, color=C_PRIMARY, lw=2.5)

    ax.text(5, 2.8, '物理AI引擎', ha='center', va='center',
            fontsize=14, fontweight='bold', color=C_PRIMARY)

    # 物理三步
    phy_steps = [('约束检查', 3.2, 3.7), ('水力仿真', 5.0, 3.7), ('校验结果', 6.8, 3.7)]
    for label, sx, sy in phy_steps:
        rect = FancyBboxPatch((sx - 0.65, sy - 0.3), 1.3, 0.6,
                              boxstyle="round,pad=0.08", linewidth=1.5,
                              edgecolor=C_PRIMARY, facecolor='#BBDEFB', alpha=0.8)
        ax.add_patch(rect)
        ax.text(sx, sy, label, ha='center', va='center', fontsize=10, fontweight='bold', color='#0D47A1')

    ax.annotate('', xy=(4.2, 3.7), xytext=(3.9, 3.7),
                arrowprops=dict(arrowstyle='->', color=C_PRIMARY, lw=1.5))
    ax.annotate('', xy=(6.1, 3.7), xytext=(5.7, 3.7),
                arrowprops=dict(arrowstyle='->', color=C_PRIMARY, lw=1.5))

    # 左侧：认知→物理（提议方案下传）
    ax.annotate('', xy=(2.2, 4.0), xytext=(2.2, 6.0),
                arrowprops=dict(arrowstyle='->', color=C_PURPLE, lw=2.5,
                                connectionstyle='arc3,rad=0.3'))
    ax.text(1.2, 5.0, '提议\n方案↓', ha='center', va='center',
            fontsize=10, fontweight='bold', color=C_PURPLE)

    # 中间菱形决策节点
    diamond_x, diamond_y = 8.5, 5.0
    diamond = plt.Polygon([(diamond_x, diamond_y + 0.6),
                           (diamond_x + 0.7, diamond_y),
                           (diamond_x, diamond_y - 0.6),
                           (diamond_x - 0.7, diamond_y)],
                          closed=True, facecolor='#FFF9C4', edgecolor='#F57F17', linewidth=2)
    ax.add_patch(diamond)
    ax.text(diamond_x, diamond_y, '校验\n通过?', ha='center', va='center',
            fontsize=8, fontweight='bold', color='#E65100')

    # 物理→菱形
    ax.annotate('', xy=(diamond_x - 0.75, diamond_y - 0.3), xytext=(7.5, 3.7),
                arrowprops=dict(arrowstyle='->', color=C_PRIMARY, lw=2))

    # 通过→执行（绿色）
    ax.annotate('', xy=(9.5, 6.5), xytext=(diamond_x + 0.3, diamond_y + 0.6),
                arrowprops=dict(arrowstyle='->', color=C_GREEN, lw=2.5))
    rect_exec = FancyBboxPatch((8.8, 6.5), 1.5, 0.7,
                               boxstyle="round,pad=0.1", linewidth=2,
                               edgecolor=C_GREEN, facecolor=C_GREEN, alpha=0.85)
    ax.add_patch(rect_exec)
    ax.text(9.55, 6.85, '执行 >>', ha='center', va='center',
            fontsize=11, fontweight='bold', color='white')
    ax.text(diamond_x + 0.7, 6.0, '通过', fontsize=9, color=C_GREEN, fontweight='bold')

    # 否决→修改方案（红色，返回认知）
    ax.annotate('', xy=(7.8, 6.0), xytext=(diamond_x - 0.3, diamond_y + 0.6),
                arrowprops=dict(arrowstyle='->', color=C_RED, lw=2.5, ls='--'))
    ax.text(diamond_x - 1.2, 6.0, '否决\n修改方案', fontsize=9, color=C_RED, fontweight='bold', ha='center')

    # 分隔线
    ax.plot([2, 8], [5, 5], color='#BDBDBD', lw=1, ls=':')

    # 底部注释
    ax.text(5, 1.3, '物理AI引擎拥有绝对否决权',
            ha='center', va='center', fontsize=12, fontweight='bold', color=C_PRIMARY,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#E3F2FD', edgecolor=C_PRIMARY, alpha=0.6))

    fig.tight_layout()
    fig.savefig(os.path.join(OUT, 'fig6-7_dual_engine_loop.png'), dpi=200, bbox_inches='tight',
                facecolor=C_BG, edgecolor='none')
    plt.close(fig)
    print('  ✓ 图6-7 完成')


# =====================================================
# 主函数
# =====================================================
if __name__ == '__main__':
    print('开始生成 T2b 第六章全部插图...\n')
    fig6_1()
    fig6_2()
    fig6_3()
    fig6_4()
    fig6_5()
    fig6_6()
    fig6_7()
    print(f'\n全部完成! 图片保存在: {OUT}')
