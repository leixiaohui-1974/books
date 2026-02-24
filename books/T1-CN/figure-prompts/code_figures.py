#!/usr/bin/env python3
"""
T1-CN 全书 matplotlib 代码生成插图
统一配色：#1565C0(深蓝) #4CAF50(绿/安全) #7B1FA2(紫/认知) #FF7043(橙红)
字体：Noto Sans CJK SC
输出：PNG 300dpi，最小 1800×1200px
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Arc
import matplotlib.patheffects as pe
import numpy as np
import os

# ---- 全局配置 ----
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'WenQuanYi Micro Hei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'
plt.rcParams['savefig.pad_inches'] = 0.2

# CHS统一配色
C_BLUE    = '#1565C0'  # 深蓝 - 水力/物理AI
C_LBLUE   = '#42A5F5'  # 蓝 - 控制
C_XLBLUE  = '#90CAF9'  # 浅蓝
C_GREEN   = '#4CAF50'  # 绿 - 安全
C_PURPLE  = '#7B1FA2'  # 紫 - 认知AI
C_ORANGE  = '#FF7043'  # 橙红 - 扰动/警告
C_RED     = '#E53935'  # 红 - 危险
C_YELLOW  = '#FFC107'  # 黄 - 预警
C_GOLD    = '#FFB300'  # 金 - 演进/顶层
C_GRAY    = '#757575'  # 灰
C_LGRAY   = '#E0E0E0'  # 浅灰
C_TEXT    = '#212121'  # 近黑
C_BG_BLUE = '#E3F2FD'
C_BG_GREEN= '#E8F5E9'
C_BG_PURPLE='#F3E5F5'
C_BG_ORANGE='#FFF3E0'

OUT_DIR = '/home/claude/figure_output'
os.makedirs(OUT_DIR, exist_ok=True)

def save_fig(fig, name):
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"✅ {name}")
    return path


# =====================================================
# 图 1-4: CHS八原理层次关系图
# =====================================================
def fig_01_04():
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis('off')
    
    # 五层定义 (y_center, color, bg_color, label, principles)
    layers = [
        (0.7, C_BLUE,   C_BG_BLUE,   '基础层\nFoundation',  ['P1 传递函数化\nTransfer Function', 'P2 可控可观性\nControllability']),
        (2.0, '#0277BD', C_BG_BLUE,   '架构层\nArchitecture', ['P3 分层分布式\nHDC', 'P4 安全包络\nSafety Envelope']),
        (3.3, C_GREEN,  C_BG_GREEN,  '验证层\nVerification', ['P5 在环验证\nxIL Testing']),
        (4.6, C_PURPLE, C_BG_PURPLE, '智能层\nIntelligence', ['P6 认知增强\nCognitive AI', 'P7 人机共融\nHuman-Machine']),
        (5.9, C_GOLD,   C_BG_ORANGE, '演进层\nEvolution',    ['P8 自主演进\nAutonomous Evolution']),
    ]
    
    for y, color, bg, label, principles in layers:
        # 层背景
        rect = FancyBboxPatch((0.3, y-0.45), 9.4, 0.9, boxstyle="round,pad=0.05",
                              facecolor=bg, edgecolor=color, linewidth=1.5)
        ax.add_patch(rect)
        # 层名
        ax.text(1.2, y, label, ha='center', va='center', fontsize=8, color=color, fontweight='bold')
        
        if len(principles) == 2:
            for i, p in enumerate(principles):
                x = 4.5 + i * 2.8
                box = FancyBboxPatch((x-1.2, y-0.35), 2.4, 0.7, boxstyle="round,pad=0.05",
                                     facecolor='white', edgecolor=color, linewidth=1.5)
                ax.add_patch(box)
                ax.text(x, y, p, ha='center', va='center', fontsize=7, color=C_TEXT)
        else:
            x = 5.8
            box = FancyBboxPatch((x-1.2, y-0.35), 2.4, 0.7, boxstyle="round,pad=0.05",
                                 facecolor='white', edgecolor=color, linewidth=1.5)
            ax.add_patch(box)
            ax.text(x, y, principles[0], ha='center', va='center', fontsize=7, color=C_TEXT)
    
    # 层间向上箭头
    for i in range(4):
        y1 = layers[i][0] + 0.5
        y2 = layers[i+1][0] - 0.5
        ax.annotate('', xy=(5.8, y2), xytext=(5.8, y1),
                   arrowprops=dict(arrowstyle='->', color=C_GRAY, lw=1.5))
    
    # P4→P8 红色约束回边
    ax.annotate('', xy=(8.8, 5.9), xytext=(8.8, 2.0),
               arrowprops=dict(arrowstyle='->', color=C_RED, lw=2, linestyle='--',
                              connectionstyle='arc3,rad=-0.3'))
    ax.text(9.5, 4.0, '安全约束\nSafety\nConstraint', ha='center', va='center',
            fontsize=7, color=C_RED, fontweight='bold', fontstyle='italic')
    
    ax.set_title('图 1-4  CHS八原理层次关系图\nFig. 1-4  Hierarchical Structure of CHS Eight Principles',
                fontsize=10, fontweight='bold', color=C_TEXT, pad=15)
    
    return save_fig(fig, 'fig_01_04_eight_principles_hierarchy.png')


# =====================================================
# 图 2-2 / 图 4-1: 可控模型族三层体系
# =====================================================
def fig_02_02():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.5)
    ax.axis('off')
    
    # 三层金字塔 (从底到顶)
    layers_data = [
        (1.0, 8.0, 1.0, C_BLUE,   'PBM：高保真PDE模型\nPhysics-Based Model', '离线仿真/数字孪生\n维度~10³', 1.6),
        (2.5, 6.0, 2.8, C_LBLUE,  'SM：降阶传递函数模型（IDZ等）\nSimplified Model', '在线MPC控制\n维度~10¹', 1.2),
        (4.0, 4.0, 4.5, '#7CB9E8', 'OSEM：数据增强模型\nObservation & State Est.', '参数校正/软测量', 0.8),
    ]
    
    for y, w, x_start, color, label, note, h in layers_data:
        x_center = x_start + w/2
        trap = plt.Polygon([[x_start, y-h/2], [x_start+w, y-h/2], 
                            [x_start+w, y+h/2], [x_start, y+h/2]], 
                           facecolor=color, edgecolor='white', alpha=0.85, linewidth=2)
        ax.add_patch(trap)
        ax.text(x_center, y, label, ha='center', va='center', fontsize=8, color='white', fontweight='bold')
        ax.text(x_start + w + 0.3, y, note, ha='left', va='center', fontsize=7, color=C_GRAY)
    
    # 层间箭头
    ax.annotate('降阶方法\nModel Reduction', xy=(3.5, 2.8), xytext=(2.0, 2.0),
               fontsize=7, color=C_BLUE, ha='center',
               arrowprops=dict(arrowstyle='->', color=C_BLUE, lw=1.5))
    ax.annotate('数据同化\nData Assimilation', xy=(6.5, 3.8), xytext=(7.5, 3.0),
               fontsize=7, color=C_LBLUE, ha='center',
               arrowprops=dict(arrowstyle='->', color=C_LBLUE, lw=1.5, linestyle='--'))
    
    # 左右纵轴标注
    ax.text(0.3, 3.0, '物理保真度 ↓\nFidelity', ha='center', va='center',
            fontsize=7, color=C_BLUE, rotation=90)
    ax.text(9.7, 3.0, '计算效率 ↑\nEfficiency', ha='center', va='center',
            fontsize=7, color=C_GREEN, rotation=90)
    
    ax.set_title('图 2-2  可控模型族的三层体系\nFig. 2-2  Three-Layer Controllable Model Family',
                fontsize=10, fontweight='bold', color=C_TEXT, pad=15)
    
    return save_fig(fig, 'fig_02_02_model_family.png')


# =====================================================
# 图 6-3 / 图 8-1: 安全包络红黄绿三区示意图
# =====================================================
def fig_06_03():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), height_ratios=[3, 1])
    
    # ---- 上半：时序曲线+三色区间 ----
    t = np.linspace(0, 24, 500)
    # 模拟水位曲线
    water_level = 52.0 + 0.8*np.sin(t/4) + 0.3*np.sin(t/1.5) + 0.4*np.random.randn(len(t))*0.1
    # 在t=8-12处制造一个黄区事件
    water_level[160:250] += 0.8 * np.exp(-((t[160:250]-10)/1.5)**2)
    
    # 三区阈值
    red_hi, yellow_hi, green_hi = 53.8, 53.2, 53.2
    green_lo, yellow_lo, red_lo = 51.0, 50.5, 50.0
    
    # 画色带
    ax1.axhspan(red_hi, 54.5, color=C_RED, alpha=0.15, label='红区 Red Zone')
    ax1.axhspan(yellow_hi, red_hi, color=C_YELLOW, alpha=0.2, label='黄区 Yellow Zone')
    ax1.axhspan(green_lo, yellow_hi, color=C_GREEN, alpha=0.1, label='绿区 Green Zone')
    ax1.axhspan(yellow_lo, green_lo, color=C_YELLOW, alpha=0.2)
    ax1.axhspan(50.0, yellow_lo, color=C_RED, alpha=0.15)
    
    # 阈值线
    for y, ls in [(red_hi, '--'), (yellow_hi, ':'), (green_lo, ':'), (yellow_lo, ':'), (50.0, '--')]:
        ax1.axhline(y, color=C_GRAY, linestyle=ls, linewidth=0.8, alpha=0.7)
    
    # 水位曲线
    ax1.plot(t, water_level, color=C_BLUE, linewidth=1.5, label='实际水位 Water Level')
    
    # 标注
    ax1.text(23.5, 54.0, '红区\n确定性保护', fontsize=7, color=C_RED, ha='right', va='center')
    ax1.text(23.5, 53.5, '黄区\n保守策略', fontsize=7, color='#F57F17', ha='right', va='center')
    ax1.text(23.5, 52.0, '绿区\n性能优先', fontsize=7, color=C_GREEN, ha='right', va='center')
    
    # 标注黄区事件
    ax1.annotate('进入黄区\n→自动切换保守模式', xy=(9.5, 52.85), xytext=(14, 53.5),
                fontsize=7, color=C_ORANGE,
                arrowprops=dict(arrowstyle='->', color=C_ORANGE))
    ax1.annotate('恢复绿区', xy=(13, 52.3), xytext=(16, 51.5),
                fontsize=7, color=C_GREEN,
                arrowprops=dict(arrowstyle='->', color=C_GREEN))
    
    ax1.set_ylabel('水位 Water Level (m)', fontsize=9)
    ax1.set_xlabel('时间 Time (h)', fontsize=9)
    ax1.set_ylim(50.0, 54.5)
    ax1.legend(loc='upper left', fontsize=7, framealpha=0.9)
    ax1.grid(True, alpha=0.3)
    
    # ---- 下半：区间切换逻辑 ----
    ax2.axis('off')
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 2)
    
    # 流程框
    boxes = [
        (1.0, 1.0, '状态检测\nState Check', C_LGRAY),
        (3.5, 1.5, '绿区?\nGreen?', C_GREEN),
        (3.5, 0.5, '黄区?\nYellow?', C_YELLOW),
        (6.0, 1.5, '性能优化模式\nOptimization', C_GREEN),
        (6.0, 0.5, '保守+自动恢复\nConservative', '#F57F17'),
        (8.5, 0.5, '确定性保护\n+请求接管\nProtection', C_RED),
    ]
    
    for x, y, txt, color in boxes:
        box = FancyBboxPatch((x-0.7, y-0.3), 1.4, 0.6, boxstyle="round,pad=0.05",
                             facecolor=color, edgecolor='white', alpha=0.3, linewidth=1)
        ax2.add_patch(box)
        ax2.text(x, y, txt, ha='center', va='center', fontsize=6, color=C_TEXT)
    
    # 连线
    for (x1,y1), (x2,y2), label in [
        ((1.7,1.0), (2.8,1.5), ''),
        ((1.7,1.0), (2.8,0.5), ''),
        ((4.2,1.5), (5.3,1.5), '是'),
        ((4.2,0.5), (5.3,0.5), '是'),
        ((4.2,0.5), (7.8,0.5), '否'),
    ]:
        ax2.annotate('', xy=(x2,y2), xytext=(x1,y1),
                    arrowprops=dict(arrowstyle='->', color=C_GRAY, lw=1))
        if label:
            ax2.text((x1+x2)/2, (y1+y2)/2+0.1, label, fontsize=6, ha='center', color=C_TEXT)
    
    fig.suptitle('图 6-3  安全包络红黄绿三区示意图\nFig. 6-3  Safety Envelope: Red-Yellow-Green Three-Zone Diagram',
                fontsize=10, fontweight='bold', color=C_TEXT, y=0.98)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    
    return save_fig(fig, 'fig_06_03_safety_envelope.png')


# =====================================================
# 图 6-4 / 图 8-2: 在环验证×WNAL矩阵
# =====================================================
def fig_06_04():
    fig, ax = plt.subplots(figsize=(8, 4))
    
    # 数据: rows=MIL/SIL/HIL, cols=L0-L5
    # 2=必须, 1=推荐, 0=不需要
    data = np.array([
        [0, 1, 2, 2, 2, 2],  # MIL
        [0, 0, 1, 2, 2, 2],  # SIL
        [0, 0, 0, 1, 2, 2],  # HIL
    ])
    
    colors_map = {0: 'white', 1: C_XLBLUE, 2: C_BLUE}
    
    for i in range(3):
        for j in range(6):
            color = colors_map[data[i, j]]
            rect = plt.Rectangle((j, 2-i), 1, 1, facecolor=color, edgecolor=C_LGRAY, linewidth=1)
            ax.add_patch(rect)
            labels = {0: '', 1: '推荐\nRecom.', 2: '必须\nRequired'}
            txt_color = 'white' if data[i,j]==2 else C_TEXT
            ax.text(j+0.5, 2.5-i, labels[data[i,j]], ha='center', va='center', fontsize=7, color=txt_color)
    
    # 行标签
    for i, label in enumerate(['MIL\n模型在环', 'SIL\n软件在环', 'HIL\n硬件在环']):
        ax.text(-0.1, 2.5-i, label, ha='right', va='center', fontsize=8, color=C_TEXT)
    
    # 列标签
    for j, label in enumerate(['L0', 'L1', 'L2', 'L3', 'L4', 'L5']):
        ax.text(j+0.5, 3.15, label, ha='center', va='bottom', fontsize=9, fontweight='bold', color=C_TEXT)
    
    # L2→L3 红色分界线
    ax.axvline(x=3, color=C_RED, linewidth=2.5, linestyle='--')
    ax.text(3, -0.3, '质变节点\nCritical Threshold', ha='center', va='top', fontsize=7, color=C_RED, fontweight='bold')
    
    # 图例
    legend_items = [
        mpatches.Patch(facecolor=C_BLUE, label='必须 Required'),
        mpatches.Patch(facecolor=C_XLBLUE, label='推荐 Recommended'),
        mpatches.Patch(facecolor='white', edgecolor=C_LGRAY, label='不要求 Not Required'),
    ]
    ax.legend(handles=legend_items, loc='lower right', fontsize=7, framealpha=0.9)
    
    ax.set_xlim(-0.5, 6.5)
    ax.set_ylim(-0.6, 3.5)
    ax.axis('off')
    
    ax.set_title('图 6-4  在环验证深度与WNAL等级对应\nFig. 6-4  xIL Verification Depth vs. WNAL Level',
                fontsize=10, fontweight='bold', color=C_TEXT, pad=15)
    
    return save_fig(fig, 'fig_06_04_xil_wnal_matrix.png')


# =====================================================
# 图 7-1: WNAL L0-L5阶梯图
# =====================================================
def fig_07_01():
    fig, ax = plt.subplots(figsize=(12, 6))
    
    levels = [
        ('L0', '手动运行\nManual', '#BDBDBD', '人工观测+经验决策'),
        ('L1', '规则自动化\nRule-Based', C_XLBLUE, '固定规则自动执行'),
        ('L2', '模型优化控制\nModel-Based', C_LBLUE, '基于模型的MPC优化'),
        ('L3', '条件自主运行\nConditional', C_BLUE, 'ODD内自主决策+安全降级'),
        ('L4', '高度自主运行\nHigh Autonomy', '#0D47A1', '扩展ODD+自诊断自恢复'),
        ('L5', '完全自主运行\nFull Autonomy', C_GOLD, '全工况自主（长期愿景）'),
    ]
    
    bar_width = 0.8
    for i, (lid, name, color, desc) in enumerate(levels):
        # 阶梯效果：高度递增
        h = 0.6 + i * 0.15
        edgecolor = 'white'
        linestyle = '-'
        linewidth = 2
        if lid == 'L5':  # L5虚线边框
            linestyle = '--'
            edgecolor = C_GOLD
            linewidth = 2
        if lid == 'L3':  # L3加粗边框
            edgecolor = C_RED
            linewidth = 3
        
        bar = plt.bar(i, h, bar_width, color=color, edgecolor=edgecolor, 
                     linewidth=linewidth, linestyle=linestyle, alpha=0.85)
        
        # 等级标签
        ax.text(i, h + 0.05, lid, ha='center', va='bottom', fontsize=14, fontweight='bold', 
                color=color if lid != 'L5' else C_GOLD)
        # 名称
        ax.text(i, -0.15, name, ha='center', va='top', fontsize=7, color=C_TEXT)
        # 描述
        ax.text(i, h/2, desc, ha='center', va='center', fontsize=6, color='white' if i > 0 else C_TEXT,
                fontweight='bold' if lid == 'L3' else 'normal')
    
    # L2→L3 红色分界线
    ax.axvline(x=2.5, color=C_RED, linewidth=2.5, linestyle='--', zorder=10)
    ax.text(2.5, 1.6, '质变节点\nCritical\nThreshold', ha='center', va='bottom',
            fontsize=8, color=C_RED, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor=C_RED, alpha=0.9))
    
    # 时间标注
    ax.text(3, -0.55, '近期目标\n3-5年', ha='center', fontsize=7, color=C_BLUE, fontstyle='italic')
    ax.text(4, -0.55, '中期目标\n5-10年', ha='center', fontsize=7, color='#0D47A1', fontstyle='italic')
    ax.text(5, -0.55, '长期愿景', ha='center', fontsize=7, color=C_GOLD, fontstyle='italic')
    
    ax.set_xlim(-0.6, 5.8)
    ax.set_ylim(-0.7, 2.0)
    ax.spines[['top','right','bottom','left']].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    
    # 底部轴标注
    ax.annotate('', xy=(5.5, -0.7), xytext=(-0.4, -0.7),
               arrowprops=dict(arrowstyle='->', color=C_GRAY, lw=1.5))
    ax.text(2.5, -0.8, '自主程度递增  Autonomy Level →', ha='center', fontsize=8, color=C_GRAY)
    
    ax.set_title('图 7-1  WNAL L0-L5 水网自主等级阶梯图\nFig. 7-1  WNAL L0-L5 Water Network Autonomy Level Ladder',
                fontsize=10, fontweight='bold', color=C_TEXT, pad=15)
    
    return save_fig(fig, 'fig_07_01_wnal_ladder.png')


# =====================================================
# 图 7-3: 八原理×WNAL等级映射矩阵
# =====================================================
def fig_07_03():
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 8行(P1-P8)×6列(L0-L5), 2=必须, 1=部分, 0=不需要
    data = np.array([
        [0, 1, 2, 2, 2, 2],  # P1 传递函数化
        [0, 0, 1, 2, 2, 2],  # P2 可控可观性
        [0, 0, 0, 2, 2, 2],  # P3 分层分布式
        [0, 0, 1, 2, 2, 2],  # P4 安全包络
        [0, 0, 1, 2, 2, 2],  # P5 在环验证
        [0, 0, 0, 1, 2, 2],  # P6 认知增强
        [0, 1, 1, 2, 2, 2],  # P7 人机共融
        [0, 0, 0, 0, 1, 2],  # P8 自主演进
    ])
    
    row_labels = ['P1 传递函数化', 'P2 可控可观性', 'P3 分层分布式', 
                  'P4 安全包络', 'P5 在环验证', 'P6 认知增强', 
                  'P7 人机共融', 'P8 自主演进']
    col_labels = ['L0', 'L1', 'L2', 'L3', 'L4', 'L5']
    
    colors_map = {0: 'white', 1: C_XLBLUE, 2: C_BLUE}
    
    for i in range(8):
        for j in range(6):
            color = colors_map[data[i, j]]
            rect = plt.Rectangle((j, 7-i), 1, 1, facecolor=color, edgecolor=C_LGRAY, linewidth=0.8)
            ax.add_patch(rect)
            symbols = {0: '', 1: '◐', 2: '●'}
            txt_color = 'white' if data[i,j]==2 else (C_BLUE if data[i,j]==1 else C_LGRAY)
            ax.text(j+0.5, 7.5-i, symbols[data[i,j]], ha='center', va='center', fontsize=12, color=txt_color)
    
    # 行标签
    for i, label in enumerate(row_labels):
        color = [C_BLUE, C_BLUE, C_BLUE, C_RED, C_GREEN, C_PURPLE, C_PURPLE, C_GOLD][i]
        ax.text(-0.1, 7.5-i, label, ha='right', va='center', fontsize=8, color=color, fontweight='bold')
    
    # 列标签
    for j, label in enumerate(col_labels):
        ax.text(j+0.5, 8.2, label, ha='center', va='bottom', fontsize=10, fontweight='bold', color=C_TEXT)
    
    # L2→L3 红色分界线
    ax.axvline(x=3, color=C_RED, linewidth=2.5, linestyle='--')
    ax.text(3, -0.5, '最小完备集分界\nMinimum Complete Set', ha='center', fontsize=7, color=C_RED, fontweight='bold')
    
    # 右侧标注
    ax.text(6.3, 5.5, 'L3 最小原理集:\nP1-P5 完整\n+ P7 基本形式', 
            fontsize=7, color=C_BLUE, ha='left', va='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=C_BG_BLUE, edgecolor=C_BLUE, alpha=0.8))
    
    # 图例
    legend_items = [
        mpatches.Patch(facecolor=C_BLUE, label='● 必须完整实现'),
        mpatches.Patch(facecolor=C_XLBLUE, label='◐ 部分/基本形式'),
        mpatches.Patch(facecolor='white', edgecolor=C_LGRAY, label='○ 不要求'),
    ]
    ax.legend(handles=legend_items, loc='lower left', fontsize=7, framealpha=0.9)
    
    ax.set_xlim(-0.5, 8)
    ax.set_ylim(-0.8, 8.5)
    ax.axis('off')
    
    ax.set_title('图 7-3  CHS八原理与WNAL等级映射\nFig. 7-3  Mapping of CHS Eight Principles to WNAL Levels',
                fontsize=10, fontweight='bold', color=C_TEXT, pad=10)
    
    return save_fig(fig, 'fig_07_03_principle_wnal_mapping.png')


# =====================================================
# 图 12-2: 沙坪ODD六维雷达图
# =====================================================
def fig_12_02():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), 
                                     subplot_kw={'projection': None},
                                     gridspec_kw={'width_ratios': [1, 1]})
    
    # ---- 左：雷达图 ----
    ax_radar = fig.add_subplot(121, projection='polar')
    categories = ['水文维\nHydrology', '设备维\nEquipment', '通信维\nComm.',
                  '环境维\nEnviron.', '负载维\nLoad', '时间维\nTime']
    N = len(categories)
    angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    angles += angles[:1]
    
    # 正常ODD
    normal = [0.7, 0.8, 0.9, 0.8, 0.7, 0.75]
    normal += normal[:1]
    # 扩展ODD
    extended = [0.9, 0.6, 0.7, 0.6, 0.9, 0.5]
    extended += extended[:1]
    
    ax_radar.plot(angles, normal, 'o-', color=C_BLUE, linewidth=2, label='正常ODD Normal')
    ax_radar.fill(angles, normal, alpha=0.15, color=C_BLUE)
    ax_radar.plot(angles, extended, 's--', color=C_ORANGE, linewidth=1.5, label='扩展ODD Extended')
    ax_radar.fill(angles, extended, alpha=0.1, color=C_ORANGE)
    
    ax_radar.set_xticks(angles[:-1])
    ax_radar.set_xticklabels(categories, fontsize=7)
    ax_radar.set_ylim(0, 1)
    ax_radar.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax_radar.set_yticklabels(['', '', '', ''], fontsize=6)
    ax_radar.legend(loc='lower right', fontsize=7, bbox_to_anchor=(1.3, -0.1))
    ax_radar.set_title('ODD六维参数', fontsize=9, fontweight='bold', pad=15)
    
    ax1.axis('off')  # hide original ax1
    
    # ---- 右：三区水位 ----
    y_labels = ['红区上界\n554.0m', '黄区上界\n553.5m', '', '绿区中值\n552.5m', 
                '', '黄区下界\n551.5m', '红区下界\n551.0m']
    
    ax2.barh(0, 1, height=0.5, color=C_RED, alpha=0.3, left=0)      # 红区上
    ax2.barh(0, 1, height=0.5, color=C_RED, alpha=0.3, left=0)
    
    zones = [
        (554.0, 0.5, C_RED,    '红区 确定性保护\nRed: Protection'),
        (553.5, 0.5, C_YELLOW, '黄区 保守策略\nYellow: Conservative'),
        (552.0, 1.5, C_GREEN,  '绿区 性能优先\nGreen: Optimization'),
        (551.5, 0.5, C_YELLOW, '黄区 保守策略'),
        (551.0, 0.5, C_RED,    '红区 确定性保护'),
    ]
    
    ax2.clear()
    for y_base, height, color, label in zones:
        ax2.barh(y_base, 1, height=height, color=color, alpha=0.25, edgecolor=color, linewidth=1)
        ax2.text(0.5, y_base + height/2, label, ha='center', va='center', fontsize=7, color=C_TEXT)
    
    ax2.set_ylim(550.5, 554.5)
    ax2.set_xlim(0, 1)
    ax2.set_xticks([])
    ax2.set_ylabel('水位 Water Level (m)', fontsize=8)
    ax2.set_title('沙坪三区运行规则', fontsize=9, fontweight='bold')
    ax2.yaxis.set_major_locator(plt.MultipleLocator(0.5))
    ax2.grid(axis='y', alpha=0.3)
    
    fig.suptitle('图 12-2  沙坪ODD六维参数与三区运行规则\nFig. 12-2  Shaping ODD Parameters & Three-Zone Rules',
                fontsize=10, fontweight='bold', color=C_TEXT, y=1.02)
    fig.tight_layout()
    
    return save_fig(fig, 'fig_12_02_shaping_odd_radar.png')


# =====================================================
# 主入口
# =====================================================
if __name__ == '__main__':
    print("=" * 50)
    print("T1-CN matplotlib 代码图生成")
    print("=" * 50)
    
    fig_01_04()
    fig_02_02()
    fig_06_03()
    fig_06_04()
    fig_07_01()
    fig_07_03()
    fig_12_02()
    
    print("\n" + "=" * 50)
    print(f"全部完成！输出目录: {OUT_DIR}")
    print("=" * 50)
