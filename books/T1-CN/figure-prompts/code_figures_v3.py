#!/usr/bin/env python3
"""
T1-CN v3 matplotlib 图 — 全部加大字号
印刷基准：170mm宽@300dpi=2008px，最小标注5mm≈24px
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np, os

plt.rcParams.update({
    'font.sans-serif': ['Noto Sans CJK SC', 'WenQuanYi Micro Hei', 'SimHei'],
    'axes.unicode_minus': False,
    'figure.dpi': 300, 'savefig.dpi': 300,
    'savefig.bbox': 'tight', 'savefig.pad_inches': 0.3,
    'font.size': 14,          # 全局基准
    'axes.titlesize': 18,
    'axes.labelsize': 16,
    'xtick.labelsize': 14,
    'ytick.labelsize': 14,
    'legend.fontsize': 13,
})

C_BLUE='#1565C0'; C_LBLUE='#42A5F5'; C_XLBLUE='#90CAF9'
C_GREEN='#4CAF50'; C_PURPLE='#7B1FA2'; C_ORANGE='#FF7043'
C_RED='#E53935'; C_YELLOW='#FFC107'; C_GOLD='#FFB300'
C_TEXT='#212121'; C_GRAY='#757575'; C_LGRAY='#E0E0E0'

OUT = '/home/claude/figure_output/v3'
os.makedirs(OUT, exist_ok=True)

def save(fig, name):
    p = os.path.join(OUT, name)
    fig.savefig(p, facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"✅ {name}")

# ==== 图 6-3 安全包络 ====
def fig_06_03():
    fig, ax = plt.subplots(figsize=(12, 7))
    t = np.linspace(0, 24, 500)
    wl = 52.0 + 0.8*np.sin(t/4) + 0.3*np.sin(t/1.5)
    wl[160:250] += 0.8*np.exp(-((t[160:250]-10)/1.5)**2)
    np.random.seed(42)
    wl += 0.05*np.random.randn(len(t))

    ax.axhspan(53.8, 54.5, color=C_RED, alpha=0.15, label='红区 — 确定性保护')
    ax.axhspan(53.2, 53.8, color=C_YELLOW, alpha=0.2, label='黄区 — 保守策略')
    ax.axhspan(51.0, 53.2, color=C_GREEN, alpha=0.08, label='绿区 — 性能优先')
    ax.axhspan(50.5, 51.0, color=C_YELLOW, alpha=0.2)
    ax.axhspan(50.0, 50.5, color=C_RED, alpha=0.15)

    for y in [53.8, 53.2, 51.0, 50.5]:
        ax.axhline(y, color=C_GRAY, linestyle=':', linewidth=0.8, alpha=0.5)

    ax.plot(t, wl, color=C_BLUE, linewidth=2, label='实际水位')

    ax.annotate('进入黄区 → 自动切换保守模式', xy=(9.5, 52.85), xytext=(14, 53.5),
                fontsize=13, color=C_ORANGE, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=C_ORANGE, lw=2))
    ax.annotate('恢复绿区', xy=(13, 52.3), xytext=(16, 51.3),
                fontsize=13, color=C_GREEN, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=C_GREEN, lw=2))

    ax.text(23.8, 54.0, '红区', fontsize=15, color=C_RED, ha='right', fontweight='bold')
    ax.text(23.8, 53.5, '黄区', fontsize=15, color='#F57F17', ha='right', fontweight='bold')
    ax.text(23.8, 52.0, '绿区', fontsize=15, color=C_GREEN, ha='right', fontweight='bold')

    ax.set_ylabel('水位 (m)', fontsize=16, fontweight='bold')
    ax.set_xlabel('时间 (h)', fontsize=16, fontweight='bold')
    ax.set_ylim(50.0, 54.5)
    ax.legend(loc='upper left', fontsize=13, framealpha=0.9)
    ax.grid(True, alpha=0.3)

    ax.set_title('图 6-3　安全包络红黄绿三区示意图\nFig. 6-3 Safety Envelope: Three-Zone Diagram',
                fontsize=18, fontweight='bold', color=C_TEXT, pad=15)
    save(fig, 'fig_06_03_safety_envelope.png')

# ==== 图 7-3 八原理×WNAL映射 ====
def fig_07_03():
    fig, ax = plt.subplots(figsize=(11, 8))
    # 8行×6列, 2=必须, 1=部分, 0=不需要
    data = np.array([
        [0, 1, 2, 2, 2, 2],  # P1
        [0, 0, 1, 2, 2, 2],  # P2
        [0, 0, 0, 2, 2, 2],  # P3
        [0, 0, 1, 2, 2, 2],  # P4
        [0, 0, 1, 2, 2, 2],  # P5
        [0, 0, 0, 1, 2, 2],  # P6
        [0, 1, 1, 2, 2, 2],  # P7
        [0, 0, 0, 0, 1, 2],  # P8
    ])
    rows = ['P1 传递函数化', 'P2 可控可观性', 'P3 分层分布式',
            'P4 安全包络', 'P5 在环验证', 'P6 认知增强',
            'P7 人机共融', 'P8 自主演进']
    cols = ['L0', 'L1', 'L2', 'L3', 'L4', 'L5']
    row_colors = [C_BLUE, C_BLUE, C_BLUE, C_RED, C_GREEN, C_PURPLE, C_PURPLE, C_GOLD]
    cmap = {0: 'white', 1: C_XLBLUE, 2: C_BLUE}
    sym = {0: '', 1: '◐', 2: '●'}

    cw, ch = 1.0, 1.0
    for i in range(8):
        for j in range(6):
            rect = plt.Rectangle((j*cw, (7-i)*ch), cw, ch, facecolor=cmap[data[i,j]],
                                 edgecolor=C_LGRAY, linewidth=1)
            ax.add_patch(rect)
            tc = 'white' if data[i,j]==2 else (C_BLUE if data[i,j]==1 else C_LGRAY)
            ax.text(j*cw+cw/2, (7-i)*ch+ch/2, sym[data[i,j]],
                    ha='center', va='center', fontsize=20, color=tc)

    for i, (label, color) in enumerate(zip(rows, row_colors)):
        ax.text(-0.15, (7-i)*ch+ch/2, label, ha='right', va='center',
                fontsize=15, color=color, fontweight='bold')

    for j, label in enumerate(cols):
        ax.text(j*cw+cw/2, 8.3, label, ha='center', va='bottom',
                fontsize=18, fontweight='bold', color=C_TEXT)

    ax.axvline(x=3*cw, color=C_RED, linewidth=3, linestyle='--')
    ax.text(3*cw, -0.6, '最小完备集分界', ha='center', fontsize=14, color=C_RED, fontweight='bold')

    legend_items = [
        mpatches.Patch(facecolor=C_BLUE, label='● 必须完整实现'),
        mpatches.Patch(facecolor=C_XLBLUE, label='◐ 部分/基本形式'),
        mpatches.Patch(facecolor='white', edgecolor=C_LGRAY, label='○ 不要求'),
    ]
    ax.legend(handles=legend_items, loc='lower left', fontsize=13, framealpha=0.9)

    ax.set_xlim(-0.2, 6.5)
    ax.set_ylim(-1.0, 8.8)
    ax.axis('off')
    ax.set_title('图 7-3　CHS八原理与WNAL等级映射\nFig. 7-3 Mapping of Eight Principles to WNAL',
                fontsize=18, fontweight='bold', color=C_TEXT, pad=15)
    save(fig, 'fig_07_03_mapping.png')

# ==== 图 12-2 ODD雷达+三区 ====
def fig_12_02():
    fig = plt.figure(figsize=(14, 6))
    # 左：雷达
    ax_r = fig.add_subplot(121, projection='polar')
    cats = ['水文维', '设备维', '通信维', '环境维', '负载维', '时间维']
    N = len(cats)
    angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    angles += angles[:1]
    normal = [0.7, 0.8, 0.9, 0.8, 0.7, 0.75]; normal += normal[:1]
    ext = [0.9, 0.6, 0.7, 0.6, 0.9, 0.5]; ext += ext[:1]

    ax_r.plot(angles, normal, 'o-', color=C_BLUE, linewidth=2.5, markersize=8, label='正常ODD')
    ax_r.fill(angles, normal, alpha=0.15, color=C_BLUE)
    ax_r.plot(angles, ext, 's--', color=C_ORANGE, linewidth=2, markersize=7, label='扩展ODD')
    ax_r.fill(angles, ext, alpha=0.1, color=C_ORANGE)
    ax_r.set_xticks(angles[:-1])
    ax_r.set_xticklabels(cats, fontsize=15, fontweight='bold')
    ax_r.set_ylim(0, 1)
    ax_r.set_yticks([0.25, 0.5, 0.75])
    ax_r.set_yticklabels(['0.25', '0.5', '0.75'], fontsize=11)
    ax_r.legend(loc='lower right', fontsize=13, bbox_to_anchor=(1.2, -0.08))
    ax_r.set_title('ODD六维参数', fontsize=17, fontweight='bold', pad=20)

    # 右：三区
    ax2 = fig.add_subplot(122)
    zones = [
        (554.0, 0.5, C_RED,    '红区 确定性保护'),
        (553.5, 0.5, C_YELLOW, '黄区 保守策略'),
        (552.0, 1.5, C_GREEN,  '绿区 性能优先'),
        (551.5, 0.5, C_YELLOW, '黄区 保守策略'),
        (551.0, 0.5, C_RED,    '红区 确定性保护'),
    ]
    for y, h, c, label in zones:
        ax2.barh(y+h/2, 1, height=h, color=c, alpha=0.25, edgecolor=c, linewidth=1.5)
        ax2.text(0.5, y+h/2, label, ha='center', va='center', fontsize=14, fontweight='bold', color=C_TEXT)

    ax2.set_ylim(550.5, 554.5)
    ax2.set_xlim(0, 1); ax2.set_xticks([])
    ax2.set_ylabel('水位 (m)', fontsize=16, fontweight='bold')
    ax2.yaxis.set_major_locator(plt.MultipleLocator(0.5))
    ax2.tick_params(axis='y', labelsize=13)
    ax2.grid(axis='y', alpha=0.3)
    ax2.set_title('沙坪三区运行规则', fontsize=17, fontweight='bold')

    fig.suptitle('图 12-2　沙坪ODD六维参数与三区运行规则\nFig. 12-2 Shaping ODD Parameters & Three-Zone Rules',
                fontsize=18, fontweight='bold', color=C_TEXT, y=1.02)
    fig.tight_layout()
    save(fig, 'fig_12_02_odd_radar.png')

if __name__ == '__main__':
    print("="*50)
    print("T1-CN v3 matplotlib (大字号)")
    print("="*50)
    fig_06_03()
    fig_07_03()
    fig_12_02()
    print("Done!")
