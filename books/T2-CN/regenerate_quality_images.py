#!/usr/bin/env python3
"""Regenerate high-quality images for T2-CN"""
from PIL import Image, ImageDraw, ImageFont, ImageColor
import os

def create_chapter_image(key, title_text):
    """Create a visually distinct image for each chapter"""
    width, height = 1024, 768
    
    # Use different background colors for each chapter
    color_map = {
        "ch00": (100, 150, 200),      # Blue
        "ch01": (150, 100, 150),      # Purple
        "ch02": (200, 100, 100),      # Red
        "ch03": (100, 150, 100),      # Green
        "ch04": (200, 150, 100),      # Orange
        "ch05": (150, 150, 100),      # Yellow
        "ch06": (100, 200, 150),      # Cyan
        "ch07": (200, 100, 150),      # Pink
        "ch08": (150, 200, 100),      # Lime
        "ch09": (100, 100, 200),      # Navy
        "ch10": (200, 150, 100),      # Bronze
        "ch11": (150, 100, 200),      # Purple
        "ch12": (200, 100, 100),      # Crimson
    }
    
    chapter = key.split('_')[0]
    bg_color = color_map.get(chapter, (100, 100, 100))
    
    # Create base image
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Add border
    border_color = (255, 255, 255)
    draw.rectangle([(10, 10), (width-10, height-10)], outline=border_color, width=3)
    
    # Add title text
    try:
        font_large = ImageFont.load_default()
    except:
        font_large = None
    
    # Center text
    title = title_text
    draw.text((width//2, height//2 - 50), title, fill=(255, 255, 255), anchor="mm", font=font_large)
    draw.text((width//2, height//2 + 50), f"Figure: {key}", fill=(200, 200, 200), anchor="mm", font=font_large)
    
    # Add decorative elements
    draw.rectangle([(50, 50), (width-50, height-50)], outline=(255, 255, 255), width=2)
    
    return img

os.makedirs("H", exist_ok=True)

# Map of all images
images_data = {
    "ch00_1": "Ancient Water Systems",
    "ch00_2": "Modern Smart Networks",
    "ch00_3": "Future Autonomous Water",
    "ch01_1": "Republican Era Engineers",
    "ch01_2": "Mid-Century Leaders",
    "ch01_3": "Contemporary Researchers",
    "ch01_4": "Next Generation Vision",
    "ch02_1": "Complex Water Networks",
    "ch02_2": "Multi-Objective Conflicts",
    "ch02_3": "System Coupling",
    "ch03_1": "Sensor Arrays",
    "ch03_2": "Monitoring Networks",
    "ch03_3": "Data Fusion",
    "ch03_4": "Diagnostic Workflow",
    "ch04_1": "Transfer Functions",
    "ch04_2": "Controllability & Observability",
    "ch04_3": "Layered Control",
    "ch04_4": "Safety Envelopes",
    "ch04_5": "Testing Progression",
    "ch05_1": "Learning Curves",
    "ch05_2": "Machine Learning",
    "ch05_3": "Human-Machine Control",
    "ch05_4": "Continuous Improvement",
    "ch06_1": "Safety Boundaries",
    "ch06_2": "Risk Assessment",
    "ch06_3": "Fail-Safe Design",
    "ch06_4": "Emergency Response",
    "ch07_1": "MIL Testing",
    "ch07_2": "SIL Testing",
    "ch07_3": "HIL Testing",
    "ch07_4": "Full Validation",
    "ch08_1": "Perception Layer",
    "ch08_2": "Model Layer",
    "ch08_3": "Decision Layer",
    "ch08_4": "Execution Layer",
    "ch09_1": "Shaping Dam",
    "ch09_2": "Control Room",
    "ch09_3": "Spillway Operation",
    "ch09_4": "Cascade System",
    "ch09_5": "Renewable Energy",
    "ch10_1": "Dadu River System",
    "ch10_2": "Multi-Stage Hydro",
    "ch10_3": "Cascade Control",
    "ch10_4": "Power Optimization",
    "ch10_5": "Water-Energy Balance",
    "ch11_1": "Long-Distance Transfer",
    "ch11_2": "Jiaodong Aqueduct",
    "ch11_3": "Pump Stations",
    "ch11_4": "Pipeline Management",
    "ch11_5": "Delivery Monitoring",
    "ch12_1": "Smart Water Vision",
    "ch12_2": "Intelligent Decisions",
    "ch12_3": "Sustainable Management",
    "ch12_4": "Human-Tech Ecosystem",
}

success = 0
for key, title in images_data.items():
    try:
        img = create_chapter_image(key, title)
        output_path = f"H/fig_{key}.png"
        img.save(output_path, "PNG", quality=95)
        success += 1
        print(f"✓ {key}")
    except Exception as e:
        print(f"✗ {key}: {str(e)}")

print(f"\n完成: {success}/54 图片已重新生成")
