"""
T2b 第六章 — Nano Banana Pro + PIL 混合生成
策略：AI生成精美图形布局（英文标签），PIL覆盖精确中文文字
"""
import os, sys, time
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont

load_dotenv("D:/cowork/教材/github_books/books/T1-CN/.env")

from google import genai
from google.genai import types

API_KEY = os.getenv("NB_API_KEY")
client = genai.Client(api_key=API_KEY)

OUT = Path("D:/cowork/教材/github_books/books/T_Revision_Working/T2b/figures/ch06")
OUT.mkdir(parents=True, exist_ok=True)

# 字体（Windows 中文字体）
def get_font(size, bold=False):
    font_paths = [
        "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/simsun.ttc",
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except:
                continue
    return ImageFont.load_default()

STYLE = "Professional flat vector diagram for an academic textbook. Clean modern design, blue color scheme (#1565C0 primary, #4CAF50 green, #7B1FA2 purple, #FF7043 orange), white background, no text labels needed - just shapes, arrows, and color blocks. Minimal, elegant, high-quality infographic style. 300dpi."


def gen_and_save(prompt, filename, use_imagen=False):
    """Generate image using AI model"""
    print(f"  调用API生成中...")
    try:
        response = client.models.generate_content(
            model='gemini-3-pro-image-preview',
            contents=[prompt],
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE', 'TEXT'],
            ),
        )
        if response.candidates and response.candidates[0].content:
            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    img = part.as_image()
                    img.save(str(OUT / filename))
                    print(f"  AI图形已保存")
                    return True
            # 没有图片，检查原因
            print(f"  finish_reason: {response.candidates[0].finish_reason}")
        elif response.candidates:
            print(f"  无内容, finish_reason: {response.candidates[0].finish_reason}")
        else:
            print(f"  无candidates")
    except Exception as e:
        print(f"  API错误: {e}")
    return False


# ============================================================
# 图6-1: HydroClaw 五层架构原理图
# ============================================================
def fig6_1():
    print("\n[1/7] 图6-1: HydroClaw 五层架构原理图")
    prompt = f"""Create a professional 5-layer pyramid architecture diagram.
The pyramid has 5 horizontal layers stacked vertically, bottom is widest, top is narrowest.
Layer colors from bottom to top: blue-grey, light blue, medium blue, deep blue, dark navy blue.
Each layer is a rounded rectangle getting narrower toward the top.
Left side: a green upward arrow and a red downward arrow.
Right side: an orange vertical arrow.
NO TEXT LABELS - just the clean colored shapes and arrows on white background.
{STYLE}
Aspect ratio: 16:10 landscape, high resolution."""

    fn = "fig6-1_five_layer_arch.png"
    if not gen_and_save(prompt, fn):
        print("  ✗ AI生成失败，跳过")
        return

    # PIL叠加中文
    img = Image.open(OUT / fn)
    w, h = img.size
    draw = ImageDraw.Draw(img)

    font_title = get_font(int(h*0.035), bold=True)
    font_layer = get_font(int(h*0.028), bold=True)
    font_sub = get_font(int(h*0.02))
    font_side = get_font(int(h*0.022), bold=True)

    # 标题
    draw.text((w//2, int(h*0.03)), "图6-1  HydroClaw 五层架构原理图",
              fill="#212121", font=font_title, anchor="mt")

    # 五层标注（大致位置按比例）
    layers = [
        (0.82, "L0 Core — 领域算法层", "仿真/控制/预测/辨识等14个领域模块"),
        (0.66, "L1 Tool — 工具层", "MCP协议封装的可调用工具"),
        (0.50, "L2 Skill — 工作流层", "固定工作流（快思考）"),
        (0.35, "L3 Agent — 智能体层", "自主推理（慢思考）"),
        (0.20, "L4 Orchestrator — 编排层", "任务分发·路由·安全审核"),
    ]
    for y_ratio, name, desc in layers:
        cy = int(h * y_ratio)
        draw.text((w//2, cy - int(h*0.015)), name, fill="white", font=font_layer, anchor="mm")
        draw.text((w//2, cy + int(h*0.015)), desc, fill="#E3F2FD", font=font_sub, anchor="mm")

    # 左侧
    draw.text((int(w*0.04), int(h*0.45)), "数据流↑", fill="#4CAF50", font=font_side, anchor="mm")
    draw.text((int(w*0.09), int(h*0.55)), "控制流↓", fill="#D32F2F", font=font_side, anchor="mm")
    # 右侧
    draw.text((int(w*0.93), int(h*0.50)), "Tool→Skill→Agent\n三级抽象",
              fill="#FF7043", font=font_sub, anchor="mm")

    img.save(OUT / fn)
    print(f"  ✓ 中文标注完成: {fn}")


# ============================================================
# 图6-2: MCP 工具协议三要素
# ============================================================
def fig6_2():
    print("\n[2/7] 图6-2: MCP 工具协议三要素")
    prompt = f"""Create a professional 3-column infographic layout.
Three equal cards side by side with rounded borders on white background.
LEFT card: light blue background, shows a code/JSON card shape inside
CENTER card: light blue background, shows 3 small server boxes connected by dashed lines to a green box at bottom
RIGHT card: light blue background, shows 4 boxes stacked vertically with arrows between them (blue, blue, green, orange colors)
Bottom: two small horizontal arrows pointing right
NO TEXT - just clean shapes and layout.
{STYLE}
Aspect ratio: 16:9 landscape."""

    fn = "fig6-2_mcp_three_elements.png"
    if not gen_and_save(prompt, fn):
        print("  ✗ 跳过")
        return

    img = Image.open(OUT / fn)
    w, h = img.size
    draw = ImageDraw.Draw(img)
    font_t = get_font(int(h*0.04), bold=True)
    font_h = get_font(int(h*0.035), bold=True)
    font_s = get_font(int(h*0.025))

    draw.text((w//2, int(h*0.04)), "图6-2  MCP 工具协议三要素", fill="#212121", font=font_t, anchor="mt")

    # 三列标题
    cols = [(w*0.18, "工具描述", "Tool Description"),
            (w*0.50, "工具发现", "Tool Discovery"),
            (w*0.82, "工具调用", "Tool Invocation")]
    for cx, zh, en in cols:
        draw.text((int(cx), int(h*0.12)), zh, fill="#1565C0", font=font_h, anchor="mt")
        draw.text((int(cx), int(h*0.17)), en, fill="#9E9E9E", font=font_s, anchor="mt")

    # 底部说明
    draw.text((w*0.30, h*0.92), "描述使发现成为可能", fill="#616161", font=font_s, anchor="mm")
    draw.text((w*0.70, h*0.92), "发现使调用有据可依", fill="#616161", font=font_s, anchor="mm")

    img.save(OUT / fn)
    print(f"  ✓ {fn}")


# ============================================================
# 图6-3: 四预闭环条件链路图
# ============================================================
def fig6_3():
    print("\n[3/7] 图6-3: 四预闭环条件链路图")
    prompt = f"""Create a professional left-to-right flowchart.
4 blue rounded rectangle steps connected by arrows going left to right.
After the 2nd step, there is an orange diamond decision shape.
From the diamond, one path goes DOWN to a green rounded rectangle (terminal).
The other path continues RIGHT to steps 3 and 4.
Clean layout, no text needed, just the shapes and arrows on white background.
Blue boxes (#1565C0), orange diamond (#FF7043), green terminal (#4CAF50).
{STYLE}
Aspect ratio: 2:1 wide landscape."""

    fn = "fig6-3_four_forecast_loop.png"
    if not gen_and_save(prompt, fn):
        print("  ✗ 跳过")
        return

    img = Image.open(OUT / fn)
    w, h = img.size
    draw = ImageDraw.Draw(img)
    font_t = get_font(int(h*0.05), bold=True)
    font_b = get_font(int(h*0.055), bold=True)
    font_s = get_font(int(h*0.035))
    font_sm = get_font(int(h*0.028))

    draw.text((w//2, int(h*0.04)), "图6-3  四预闭环条件链路图", fill="#212121", font=font_t, anchor="mt")
    draw.text((w//2, int(h*0.11)), "条件链接：逐级触发，按需执行", fill="#FF7043", font=font_s, anchor="mt")

    # 步骤标注（位置需要根据AI生成的图调整）
    steps = [
        (0.12, 0.45, "预报", "run_forecast()"),
        (0.30, 0.45, "预警", "check_alert()"),
        (0.65, 0.45, "预演", "run_simulation()"),
        (0.85, 0.45, "预案", "generate_plan()"),
    ]
    for xr, yr, name, tool in steps:
        draw.text((int(w*xr), int(h*yr)), name, fill="white", font=font_b, anchor="mm")
        draw.text((int(w*xr), int(h*(yr+0.08))), tool, fill="#BBDEFB", font=font_sm, anchor="mm")

    # 菱形标注
    draw.text((int(w*0.47), int(h*0.45)), "预警等级\n≥黄色?", fill="white", font=font_sm, anchor="mm")
    draw.text((int(w*0.55), int(h*0.38)), "是", fill="#D32F2F", font=font_s, anchor="mm")
    draw.text((int(w*0.49), int(h*0.62)), "否", fill="#4CAF50", font=font_s, anchor="mm")
    draw.text((int(w*0.47), int(h*0.78)), "正常运行", fill="white", font=font_b, anchor="mm")

    img.save(OUT / fn)
    print(f"  ✓ {fn}")


# ============================================================
# 图6-4: Orchestrator 四级路由原理
# ============================================================
def fig6_4():
    print("\n[4/7] 图6-4: Orchestrator 四级路由原理")
    prompt = f"""Create a professional funnel/inverted-pyramid diagram.
4 horizontal bars stacked vertically, getting narrower from top to bottom.
Colors from top to bottom: light blue, medium blue, bright blue, dark navy.
Each bar is a rounded rectangle.
An arrow enters from the top and exits from the bottom.
Left side: a vertical orange double-arrow.
Right side: 4 small labels area.
NO TEXT, just the clean funnel shape with gradient blues.
{STYLE}
Aspect ratio: 3:4 portrait."""

    fn = "fig6-4_orchestrator_routing.png"
    if not gen_and_save(prompt, fn):
        print("  ✗ 跳过")
        return

    img = Image.open(OUT / fn)
    w, h = img.size
    draw = ImageDraw.Draw(img)
    font_t = get_font(int(h*0.028), bold=True)
    font_l = get_font(int(h*0.022), bold=True)
    font_s = get_font(int(h*0.018))

    draw.text((w//2, int(h*0.02)), "图6-4  Orchestrator 四级路由原理",
              fill="#212121", font=font_t, anchor="mt")
    draw.text((w//2, int(h*0.06)), "▼ 用户请求", fill="#424242", font=font_l, anchor="mt")

    funnel = [
        (0.22, "第一级：Skill 短语匹配", "覆盖80%日常请求", "~毫秒"),
        (0.38, "第二级：工具关键词匹配", "单工具直接调用", "~秒"),
        (0.54, "第三级：能力路由", "按Agent能力矩阵分发", "~秒"),
        (0.70, "第四级：Planning 分解", "仅用于复杂多步任务", "~分钟"),
    ]
    for yr, name, desc, speed in funnel:
        draw.text((w//2, int(h*yr)), name, fill="white", font=font_l, anchor="mm")
        draw.text((w//2, int(h*(yr+0.04))), desc, fill="#E3F2FD", font=font_s, anchor="mm")
        draw.text((int(w*0.92), int(h*yr)), speed, fill="#1565C0", font=font_s, anchor="mm")

    # 左侧标注
    draw.text((int(w*0.05), int(h*0.25)), "快速确定", fill="#4CAF50", font=font_s, anchor="mm")
    draw.text((int(w*0.05), int(h*0.68)), "慢速灵活", fill="#7B1FA2", font=font_s, anchor="mm")

    draw.text((w//2, int(h*0.85)), "▼ 执行结果", fill="#424242", font=font_l, anchor="mm")

    img.save(OUT / fn)
    print(f"  ✓ {fn}")


# ============================================================
# 图6-5: SafetyAgent ODD 三区间否决流程
# ============================================================
def fig6_5():
    print("\n[5/7] 图6-5: SafetyAgent ODD 三区间否决流程")
    prompt = f"""Create a professional horizontal flowchart.
LEFT: a purple rounded rectangle.
CENTER: a larger red-bordered rectangle.
RIGHT: three rounded rectangles stacked vertically - green (top), yellow (middle), red (bottom).
Arrows from center to each of the three right boxes. The bottom red arrow is thicker.
Arrow from left to center.
Bottom: a red highlighted text banner.
NO TEXT, just clean shapes and arrows. Traffic light colors (green, yellow, red) for the three outputs.
{STYLE}
Aspect ratio: 16:9 landscape."""

    fn = "fig6-5_safety_odd_veto.png"
    if not gen_and_save(prompt, fn):
        print("  ✗ 跳过")
        return

    img = Image.open(OUT / fn)
    w, h = img.size
    draw = ImageDraw.Draw(img)
    font_t = get_font(int(h*0.04), bold=True)
    font_b = get_font(int(h*0.035), bold=True)
    font_s = get_font(int(h*0.028))
    font_warn = get_font(int(h*0.03), bold=True)

    draw.text((w//2, int(h*0.03)), "图6-5  SafetyAgent ODD 三区间否决流程",
              fill="#212121", font=font_t, anchor="mt")

    # 左侧
    draw.text((int(w*0.12), int(h*0.42)), "任意 Agent", fill="#7B1FA2", font=font_b, anchor="mm")
    draw.text((int(w*0.12), int(h*0.50)), "提出操作建议", fill="#9C27B0", font=font_s, anchor="mm")
    # 中间
    draw.text((int(w*0.40), int(h*0.38)), "SafetyAgent", fill="#D32F2F", font=font_b, anchor="mm")
    draw.text((int(w*0.40), int(h*0.48)), "check_odd()", fill="#B71C1C", font=font_s, anchor="mm")
    draw.text((int(w*0.40), int(h*0.55)), "检查当前状态区间", fill="#C62828", font=font_s, anchor="mm")
    # 右侧三条
    draw.text((int(w*0.78), int(h*0.23)), "Normal >> 放行，执行操作", fill="white", font=font_b, anchor="mm")
    draw.text((int(w*0.78), int(h*0.48)), "Extended >> 人工确认", fill="#5D4037", font=font_b, anchor="mm")
    draw.text((int(w*0.78), int(h*0.73)), "MRC >> 否决+最小风险方案", fill="white", font=font_b, anchor="mm")

    # 底部
    draw.text((w//2, int(h*0.92)), "SafetyAgent 拥有绝对否决权，优先级高于所有其他 Agent",
              fill="#D32F2F", font=font_warn, anchor="mm")

    img.save(OUT / fn)
    print(f"  ✓ {fn}")


# ============================================================
# 图6-6: 认知API四维框架与角色映射
# ============================================================
def fig6_6():
    print("\n[6/7] 图6-6: 认知API四维框架与角色映射")
    prompt = f"""Create a professional 5x4 grid/matrix table.
5 rows and 4 columns. Some cells are filled with blue (#1565C0), others with light grey (#E0E0E0).
Pattern:
Row 1: blue, grey, grey, blue
Row 2: blue, blue, blue, grey
Row 3: blue, blue, grey, grey
Row 4: blue, blue, blue, blue (all blue)
Row 5: blue, blue, grey, grey
Clean table with clear cell borders on white background.
A horizontal blue arrow above the columns, a vertical purple arrow on the right side.
NO TEXT, just the colored grid.
{STYLE}
Aspect ratio: 4:3."""

    fn = "fig6-6_cognitive_api_matrix.png"
    if not gen_and_save(prompt, fn):
        print("  ✗ 跳过")
        return

    img = Image.open(OUT / fn)
    w, h = img.size
    draw = ImageDraw.Draw(img)
    font_t = get_font(int(h*0.032), bold=True)
    font_h = get_font(int(h*0.028), bold=True)
    font_s = get_font(int(h*0.022))
    font_sub = get_font(int(h*0.024))

    draw.text((w//2, int(h*0.02)), "图6-6  认知API四维框架与角色映射",
              fill="#212121", font=font_t, anchor="mt")
    draw.text((w//2, int(h*0.065)), "感知 → 认知 → 决策 → 控制（信息流方向）",
              fill="#1565C0", font=font_s, anchor="mt")

    # 列标题
    cols = ["感知\nPerception", "认知\nCognition", "决策\nDecision", "控制\nControl"]
    for j, c in enumerate(cols):
        draw.text((int(w*(0.28+j*0.16)), int(h*0.13)), c, fill="#1565C0", font=font_s, anchor="mt")

    # 行标题
    rows = ["operator\n(运维人员)", "designer\n(设计师)", "researcher\n(研究员)",
            "admin\n(管理员)", "teacher\n(教学)"]
    for i, r in enumerate(rows):
        draw.text((int(w*0.12), int(h*(0.28+i*0.13))), r, fill="#424242", font=font_s, anchor="mm")

    # 右侧
    draw.text((int(w*0.95), int(h*0.50)), "CHS\n四维\n认知\n链路", fill="#7B1FA2", font=font_sub, anchor="mm")

    img.save(OUT / fn)
    print(f"  ✓ {fn}")


# ============================================================
# 图6-7: 双引擎闭环原理（简洁版）
# ============================================================
def fig6_7():
    print("\n[7/7] 图6-7: 双引擎闭环原理（简洁版）")
    prompt = f"""Create a professional circular closed-loop diagram.
A large circle divided into top half (purple tinted #7B1FA2 with opacity) and bottom half (blue tinted #1565C0 with opacity).
Top half contains 3 small rounded boxes in a row, connected by arrows.
Bottom half contains 3 small rounded boxes in a row, connected by arrows.
Left side: a downward arrow from top to bottom half.
Right side: a diamond shape, with a green arrow going to a green box labeled 'GO', and a red dashed arrow going back up.
Clean and elegant. NO TEXT.
{STYLE}
Aspect ratio: 1:1 square."""

    fn = "fig6-7_dual_engine_loop.png"
    if not gen_and_save(prompt, fn):
        print("  ✗ 跳过")
        return

    img = Image.open(OUT / fn)
    w, h = img.size
    draw = ImageDraw.Draw(img)
    font_t = get_font(int(h*0.03), bold=True)
    font_b = get_font(int(h*0.028), bold=True)
    font_s = get_font(int(h*0.022))
    font_warn = get_font(int(h*0.025), bold=True)

    draw.text((w//2, int(h*0.02)), "图6-7  双引擎闭环原理（简洁版）",
              fill="#212121", font=font_t, anchor="mt")

    # 上半：认知AI
    draw.text((w//2, int(h*0.20)), "认知AI引擎", fill="#7B1FA2", font=font_b, anchor="mm")
    cog = [("理解", 0.28, 0.32), ("推理", 0.45, 0.32), ("提议方案", 0.62, 0.32)]
    for label, xr, yr in cog:
        draw.text((int(w*xr), int(h*yr)), label, fill="#4A148C", font=font_s, anchor="mm")

    # 下半：物理AI
    draw.text((w//2, int(h*0.72)), "物理AI引擎", fill="#1565C0", font=font_b, anchor="mm")
    phy = [("约束检查", 0.28, 0.62), ("水力仿真", 0.45, 0.62), ("校验结果", 0.62, 0.62)]
    for label, xr, yr in phy:
        draw.text((int(w*xr), int(h*yr)), label, fill="#0D47A1", font=font_s, anchor="mm")

    # 左侧
    draw.text((int(w*0.10), int(h*0.47)), "提议方案↓", fill="#7B1FA2", font=font_s, anchor="mm")
    # 右侧决策
    draw.text((int(w*0.82), int(h*0.47)), "校验通过?", fill="#E65100", font=font_s, anchor="mm")
    draw.text((int(w*0.90), int(h*0.30)), "执行", fill="#4CAF50", font=font_b, anchor="mm")
    draw.text((int(w*0.90), int(h*0.37)), "通过", fill="#4CAF50", font=font_s, anchor="mm")
    draw.text((int(w*0.78), int(h*0.27)), "否决\n修改方案", fill="#D32F2F", font=font_s, anchor="mm")

    # 底部
    draw.text((w//2, int(h*0.90)), "物理AI引擎拥有绝对否决权",
              fill="#1565C0", font=font_warn, anchor="mm")

    img.save(OUT / fn)
    print(f"  ✓ {fn}")


# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("  Nano Banana Pro + PIL — T2b 第六章插图生成")
    print("=" * 60)

    figs = [fig6_1, fig6_2, fig6_3, fig6_4, fig6_5, fig6_6, fig6_7]
    for i, func in enumerate(figs):
        func()
        if i < len(figs) - 1:
            time.sleep(4)  # Rate limit

    print(f"\n{'='*60}")
    print(f"  全部完成！输出: {OUT}")
    print(f"{'='*60}")
