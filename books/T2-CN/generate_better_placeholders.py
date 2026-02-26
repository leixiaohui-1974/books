#!/usr/bin/env python3
"""
生成高质量占位图 - T2-CN《水网觉醒》
每张图显示：章节编号、图片编号、完整提示词
方便作者直接拷贝提示词到 Nano Banana 等 AI 绘图工具

使用方法：
    python3 generate_better_placeholders.py

输出：H/ 目录下的 PNG 文件（覆盖原有占位图）
"""
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

# ─── 字体路径 ───────────────────────────────────────────────────────────
FONT_EN = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONT_EN_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FONT_ZH = '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf'

# ─── 图片尺寸 ────────────────────────────────────────────────────────────
W, H_IMG = 1200, 900

# ─── 配色方案 ────────────────────────────────────────────────────────────
BG_COLOR       = (15, 32, 60)       # 深蓝背景（科技感）
HEADER_COLOR   = (0, 120, 200)      # 蓝色标题栏
BADGE_COLOR    = (0, 80, 160)       # 徽章底色
PROMPT_BG      = (20, 45, 85)       # 提示词区域背景
TEXT_WHITE     = (255, 255, 255)    # 白色文字
TEXT_CYAN      = (100, 220, 255)    # 青色（提示词标签）
TEXT_YELLOW    = (255, 210, 0)      # 黄色（图片ID）
TEXT_GRAY      = (180, 200, 220)    # 灰色（副文字）
WATERMARK_CLR  = (40, 60, 100)      # 水印色
BORDER_COLOR   = (0, 150, 230)      # 边框色


# ─── 提示词数据 ───────────────────────────────────────────────────────────
# 来源：chapter_image_prompts.md 的完整提示词
# key格式 -> (章节名称, 完整提示词)

PROMPTS = {
    # 封面
    "cover": (
        "封面",
        "A futuristic Chinese water network awakening scene. A vast landscape with rivers, reservoirs, canals, "
        "and pumping stations interconnected by glowing blue digital lines forming a neural network pattern. "
        "The water infrastructure gradually transitions from traditional gray concrete on the left to luminous "
        "digital-blue smart infrastructure on the right, symbolizing the transformation from manual operation "
        "to autonomous control. Dawn light breaks through clouds over mountains in the background. Chinese water "
        "engineering style (dams, sluice gates, aqueducts). Color palette: deep navy blue, cyan, white highlights, "
        "warm amber sunrise. Style: cinematic digital illustration, slightly futuristic, clean and professional. "
        "No text. 16:9 aspect ratio."
    ),
    # 引子
    "prologue": (
        "引子·暴雨夜的调度室",
        "Interior of a Chinese water dispatch control room at night during a rainstorm. A lone operator sits "
        "before multiple glowing blue monitoring screens showing water level curves, dam cross-sections, and "
        "alarm indicators. Rain streaks across a large window behind him. The screens cast a blue glow on his "
        "worried face. On the desk: a landline phone, a walkie-talkie, a paper logbook. The atmosphere is tense "
        "— red warning lights flash on some screens. Outside the window, lightning illuminates a reservoir dam. "
        "Style: cinematic illustration, moody lighting, tech-blue and warm amber tones. No text. 16:9."
    ),
    # Ch01
    "ch01": (
        "第一章·五代人生",
        "A horizontal timeline illustration showing five generations of water engineering evolution, from left "
        "to right: (1) An ancient Chinese water gauge stone pillar by a river, a worker reading water marks; "
        "(2) A 1950s mechanical chart recorder with paper roll; (3) A 1990s SCADA control room with CRT monitors; "
        "(4) A 2010s digital dashboard with flat screens and touchscreens; (5) A futuristic holographic water "
        "network display with AI indicators glowing blue. Each era is connected by a flowing river that transforms "
        "from muddy brown to crystal blue to digital cyan. Style: clean infographic illustration, side-scrolling "
        "panorama, color evolves from sepia to modern blue. No text. 16:9."
    ),
    # Ch02
    "ch02": (
        "第二章·为什么水网这么难管",
        "A conceptual illustration of five challenges in water system control, arranged as five intertwined "
        "obstacles around a central water network. (1) A clock with slow-moving hands representing 'time delay'; "
        "(2) Tangled blue ropes representing 'strong coupling'; (3) A curved non-linear graph representing "
        "'nonlinearity'; (4) Multiple constraint barriers like walls representing 'multi-constraints'; (5) "
        "Fog/clouds representing 'uncertainty'. In the center, a simplified water network (reservoirs, canals, "
        "pumping stations) struggles within these five forces. Color palette: various shades of blue with red "
        "accent for difficulty. Style: abstract conceptual diagram, clean geometric shapes, slightly isometric. "
        "No text. 4:3."
    ),
    # Ch03
    "ch03": (
        "第三章·给水网做体检",
        "A medical checkup metaphor for water infrastructure. A large dam/reservoir is positioned like a patient "
        "on an examination table. A doctor figure (wearing engineer's hard hat instead of medical cap) holds a "
        "stethoscope connected to sensors on the dam. An X-ray display beside them shows the internal structure "
        "of the water system — pipes, channels, valves — with some areas highlighted in green (healthy/observable) "
        "and some in red crosshatch (blind spots/unobservable). Diagnostic charts float around showing "
        "controllability and observability matrices. Style: clean medical-tech illustration, light blue and white, "
        "friendly professional tone. No text. 4:3."
    ),
    # Ch04
    "ch04": (
        "第四章·八大原理",
        "Eight glowing principle icons arranged in a circular mandala pattern around a central water network "
        "symbol. Each icon represents one CHS principle: (1) Shield for safety boundary; (2) Layered pyramid "
        "for hierarchical control; (3) Eye for observability; (4) Joystick for controllability; (5) Loop arrows "
        "for feedback; (6) Brain for cognitive augmentation; (7) Puzzle pieces for modularity; (8) Lock for "
        "security. All icons connected by flowing water lines forming an octagonal web. The central symbol is a "
        "stylized water droplet with circuit board patterns inside. Color palette: deep blue background, cyan "
        "and gold glowing icons. Style: elegant tech-spiritual mandala, flat design with subtle glow effects. "
        "No text. 1:1."
    ),
    # Ch05
    "ch05": (
        "第五章·水网学开车——WNAL自主等级",
        "A vertical ladder or staircase illustration showing six levels (L0 to L5) of water network autonomy, "
        "ascending from bottom to top. At each level, a small scene shows the relationship between human operator "
        "and system: L0 — operator manually turns valve wheels; L1 — operator watches a simple gauge; L2 — "
        "operator monitors a screen with some automation; L3 — operator supervises while system operates (hands "
        "off wheel); L4 — operator reads a book while system runs autonomously; L5 — empty control room, system "
        "fully autonomous. A self-driving car is subtly shown beside the ladder for analogy. Gradient from warm "
        "brown (bottom/manual) to cool blue (top/autonomous). Style: clean step diagram, friendly illustration "
        "style. No text. 9:16 or 4:3."
    ),
    # Ch06
    "ch06": (
        "第六章·安全第一——三色安全包络",
        "A dramatic three-zone safety envelope visualization centered on a reservoir cross-section. The water "
        "level zones are clearly color-coded: bottom GREEN zone (normal operation, calm water, efficient turbines "
        "spinning), middle YELLOW zone (cautious operation, slightly choppy water, amber warning lights), top "
        "RED zone (emergency, turbulent water, red alarm, emergency gates activating). The boundaries between "
        "zones glow with transition indicators. On the right side, a traffic light metaphor reinforces the three "
        "colors. The overall composition suggests protection and order within potential chaos. Style: dramatic "
        "yet clean technical illustration, vivid green-yellow-red on dark blue background. No text. 16:9."
    ),
    # Ch07
    "ch07": (
        "第七章·先在电脑里试驾——在环验证",
        "A three-stage verification pipeline shown as three connected testing chambers, progressing from virtual "
        "to real. Left chamber 'MIL': a computer screen showing mathematical equations and simulation curves, "
        "purely digital environment. Middle chamber 'SIL': a server rack running embedded code, with digital "
        "displays showing real-time data. Right chamber 'HIL': a physical control panel connected to a miniature "
        "water system model with real pumps, valves, and water flowing. An arrow flows left to right labeled "
        "with increasing realism. A few bug/defect icons are caught at each stage like a filter. Background: "
        "laboratory/testing facility aesthetic. Style: clean technical cutaway illustration, blue-gray tones. "
        "No text. 16:9."
    ),
    # Ch08
    "ch08": (
        "第八章·水网操作系统——HydroOS",
        "An operating system architecture visualization for water networks, inspired by smartphone OS layer "
        "diagrams. Three horizontal layers stacked: Bottom layer 'DAL' (Device Abstraction) shows simplified "
        "icons of pumps, gates, sensors, and valves in various brands — all connected through a universal "
        "adapter. Middle layer 'Control' shows control algorithms, strategy modules, and a security gate/"
        "checkpoint. Top layer 'Governance' shows audit logs, permission settings, and version control. "
        "On the right side, a four-state machine diagram (startup → running → degraded → shutdown) with "
        "circular arrows. The whole structure sits atop a stylized circuit board with water channel patterns. "
        "Style: clean OS architecture diagram, Material Design aesthetic, blue and teal palette. No text. 4:3."
    ),
    # Ch09
    "ch09": (
        "第九章·沙坪的故事",
        "A bird's-eye view illustration of Shaping hydropower station nestled in a narrow river gorge. The "
        "small reservoir (cup-sized compared to the gorge) is at the center, with four turbine units visible "
        "through a cutaway of the powerhouse. Digital overlay shows: MPC prediction curves floating above the "
        "water surface, a safety envelope boundary glowing around the reservoir water level, and sensor data "
        "streams flowing from instruments to a small control room. Upstream, water rushes in from a larger dam "
        "(Zhentouba). The scene contrasts the tiny physical scale of the station with the sophisticated digital "
        "control overlay. Mountain scenery, Sichuan landscape. Style: technical aerial illustration with digital "
        "augmented reality overlay, blue-green natural tones with cyan digital elements. No text. 16:9."
    ),
    # Ch10
    "ch10": (
        "第十章·大渡河的接力赛",
        "A dramatic illustration of cascade hydropower stations along the Dadu River, shown as a relay race. "
        "Three large dams (Pubugou, Shenxigou, Zhentoba) are arranged from top-left to bottom-right along a "
        "winding river valley, connected by blue water flow arrows with timing labels. Each dam has a small "
        "'runner' figure passing a baton to the next, symbolizing coordinated handoff. Green communication "
        "lines arc between the stations showing EDC coordination signals. At the top, a central 'coordinator "
        "tower' oversees all three stations. The river flows powerfully between steep mountain gorges. "
        "Style: epic landscape illustration with relay race metaphor, dramatic lighting, blue-green river "
        "against dark mountain silhouettes. No text. 16:9."
    ),
    # Ch11
    "ch11": (
        "第十一章·千里送水——胶东调水",
        "A panoramic map-style illustration of the Jiaodong water transfer project stretching 571km across "
        "Shandong peninsula. The route shows the full pipeline from the Yellow River (left) through open "
        "canals, pumping stations (13 icons), sluice gates, and reservoirs, reaching cities (Qingdao, Yantai, "
        "Weihai) on the right coast. A digital twin overlay shows the same network in glowing blue holographic "
        "lines above the physical infrastructure. Three AI icons float at key points: a stethoscope (equipment "
        "health), a drone (visual inspection), and a chat bubble (cognitive AI). Three time-scale layers are "
        "subtly visible: yearly plan at top, daily schedule in middle, real-time control at bottom. "
        "Style: illustrated map with digital overlay, cartographic aesthetic meets tech visualization, warm "
        "earth tones for land with blue digital elements. No text. 16:9."
    ),
    # Ch12
    "ch12": (
        "第十二章·从今天开始觉醒",
        "A hopeful sunrise scene over a modern Chinese water dispatch control room. Through the large panoramic "
        "window, a river valley with dams and canals stretches into the distance under golden dawn light. "
        "Inside, a confident young engineer sits relaxed, supervising a calm green-status dashboard. A cup of "
        "tea steams on the desk. The screens show all-green system status with a subtle AI assistant interface "
        "on one screen. The atmosphere is peaceful, competent, and forward-looking — a contrast to the tense "
        "nighttime scene of the prologue. On the desk, two books are visible (symbolizing T1 and T2). "
        "Style: warm hopeful illustration, golden morning light, clean modern interior, optimistic tone. "
        "No text. 16:9."
    ),
}


def make_placeholder(key, chapter_name, prompt_text, output_path):
    """生成高质量占位图，包含完整提示词"""
    img = Image.new('RGB', (W, H_IMG), color=BG_COLOR)
    draw = ImageDraw.Draw(img)

    try:
        font_bold_large = ImageFont.truetype(FONT_EN_BOLD, 28)
        font_bold_med   = ImageFont.truetype(FONT_EN_BOLD, 20)
        font_regular    = ImageFont.truetype(FONT_EN, 16)
        font_small      = ImageFont.truetype(FONT_EN, 13)
        font_zh         = ImageFont.truetype(FONT_ZH, 22)
        font_zh_small   = ImageFont.truetype(FONT_ZH, 16)
    except:
        font_bold_large = font_bold_med = font_regular = font_small = font_zh = font_zh_small = None

    # ── 顶部标题栏 ──────────────────────────────────────────────
    draw.rectangle([(0, 0), (W, 70)], fill=HEADER_COLOR)
    title_main = "《水网觉醒》 T2-CN  ·  待生成插图占位图"
    draw.text((20, 10), title_main, font=font_zh, fill=TEXT_WHITE)
    draw.text((20, 40), "Placeholder — Replace with AI-generated image from Nano Banana",
              font=font_small, fill=TEXT_GRAY)

    # ── 图片ID徽章 ─────────────────────────────────────────────
    badge_text = key.upper()
    draw.rectangle([(W-160, 10), (W-10, 60)], fill=BADGE_COLOR, outline=BORDER_COLOR, width=1)
    draw.text((W-85, 35), badge_text, font=font_bold_large, fill=TEXT_YELLOW, anchor="mm")

    # ── 章节名称 ────────────────────────────────────────────────
    draw.rectangle([(0, 70), (W, 120)], fill=(10, 25, 50))
    draw.text((20, 95), chapter_name, font=font_zh, fill=TEXT_CYAN, anchor="lm")

    # ── 中央"图片待生成"视觉占位 ────────────────────────────────
    # 画一个带虚线框的矩形，表示图片区域
    box_x1, box_y1, box_x2, box_y2 = 20, 130, W//2 - 20, 560
    draw.rectangle([(box_x1, box_y1), (box_x2, box_y2)],
                   fill=(8, 20, 45), outline=BORDER_COLOR, width=2)

    # 对角线（表示"空图"）
    draw.line([(box_x1, box_y1), (box_x2, box_y2)], fill=(30, 60, 100), width=1)
    draw.line([(box_x1, box_y2), (box_x2, box_y1)], fill=(30, 60, 100), width=1)

    # 中心图标文字
    cx = (box_x1 + box_x2) // 2
    cy = (box_y1 + box_y2) // 2
    draw.text((cx, cy - 30), "AI IMAGE", font=font_bold_large, fill=(50, 100, 180), anchor="mm")
    draw.text((cx, cy + 10), "PENDING GENERATION", font=font_bold_med, fill=(50, 100, 180), anchor="mm")
    draw.text((cx, cy + 40), "Use prompt below with Nano Banana", font=font_small, fill=(70, 120, 180), anchor="mm")

    # ── 提示词区域（右侧）─────────────────────────────────────
    px1, py1, px2, py2 = W//2 + 10, 130, W - 20, 560
    draw.rectangle([(px1, py1), (px2, py2)], fill=PROMPT_BG, outline=BORDER_COLOR, width=1)

    # 提示词标签
    draw.rectangle([(px1, py1), (px2, py1+30)], fill=BADGE_COLOR)
    draw.text((px1 + 10, py1 + 15), "🎨  Nano Banana Prompt  (copy & paste)",
              font=font_small, fill=TEXT_CYAN, anchor="lm")

    # 提示词正文（自动换行）
    prompt_area_w = px2 - px1 - 20  # pixels
    # 估算每行字符数（DejaVu约8px/char at size 13）
    chars_per_line = prompt_area_w // 8
    wrapped = textwrap.fill(prompt_text, width=chars_per_line)
    lines = wrapped.split('\n')

    y_text = py1 + 40
    for line in lines:
        if y_text > py2 - 20:
            break
        draw.text((px1 + 10, y_text), line, font=font_small, fill=TEXT_WHITE)
        y_text += 17

    # ── 底部信息栏 ────────────────────────────────────────────
    draw.rectangle([(0, 560), (W, H_IMG)], fill=(8, 20, 45))

    # 使用说明
    instructions = [
        "📋  使用说明：",
        "1. 复制上方英文提示词",
        "2. 打开 Nano Banana（或 Midjourney / DALL-E / Stable Diffusion）",
        "3. 粘贴提示词并生成图片",
        "4. 下载生成图，重命名为此文件名并替换",
        f"5. 目标文件名: {os.path.basename(output_path)}",
    ]
    y_inst = 575
    for i, line in enumerate(instructions):
        color = TEXT_CYAN if i == 0 else TEXT_GRAY
        draw.text((20, y_inst), line, font=font_zh_small if i == 0 else font_small, fill=color)
        y_inst += 22

    # 推荐尺寸
    ratio_hint = "推荐比例: 16:9 (1920×1080) 或 4:3 (1600×1200)"
    draw.text((W - 20, 575), ratio_hint, font=font_small, fill=TEXT_GRAY, anchor="ra")

    # 时间戳水印
    ts = datetime.now().strftime('%Y-%m-%d')
    draw.text((W - 20, H_IMG - 20), f"Generated: {ts}  |  T2-CN Placeholder v2",
              font=font_small, fill=WATERMARK_CLR, anchor="ra")

    img.save(output_path, quality=95)


def main():
    os.makedirs("H", exist_ok=True)
    print("生成高质量占位图（带提示词）...")
    print("=" * 60)

    count = 0
    for key, (chapter_name, prompt) in PROMPTS.items():
        filename = f"H/fig_{key}_placeholder.png"
        make_placeholder(key, chapter_name, prompt, filename)
        print(f"  ✓  {filename}  [{chapter_name}]")
        count += 1

    print("=" * 60)
    print(f"完成！共生成 {count} 张占位图")
    print("\n下一步：")
    print("  将 H/ 目录中的占位图发给设计师，或自行将提示词粘贴到 Nano Banana 生成真实图片")
    print("  生成后将真实图片覆盖对应占位图即可")
    print()
    print("提示词汇总文件已存在：")
    print("  chapter_image_prompts.md  （原始提示词，每章一张主图）")


if __name__ == "__main__":
    main()
