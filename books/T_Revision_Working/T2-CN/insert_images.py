#!/usr/bin/env python3
"""Insert image references into T2-CN markdown files"""
import os
import re
from datetime import datetime

log_file = "/tmp/t2cn_images.log"

def log_msg(msg):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] {msg}\n")
    print(msg)

log_msg("开始插入图片引用...")

# Image insertion map
image_map = {
    "ch00_引子.md": ["ch00_1", "ch00_2", "ch00_3"],
    "ch01_五代人生.md": ["ch01_1", "ch01_2", "ch01_3", "ch01_4"],
    "ch02_为什么难管.md": ["ch02_1", "ch02_2", "ch02_3"],
    "ch03_给水网做体检.md": ["ch03_1", "ch03_2", "ch03_3", "ch03_4"],
    "ch04_八原理.md": ["ch04_1", "ch04_2", "ch04_3", "ch04_4", "ch04_5"],
    "ch05_水网学开车.md": ["ch05_1", "ch05_2", "ch05_3", "ch05_4"],
    "ch06_安全第一.md": ["ch06_1", "ch06_2", "ch06_3", "ch06_4"],
    "ch07_先在电脑里试驾.md": ["ch07_1", "ch07_2", "ch07_3", "ch07_4"],
    "ch08_水网操作系统.md": ["ch08_1", "ch08_2", "ch08_3", "ch08_4"],
    "ch09_沙坪故事.md": ["ch09_1", "ch09_2", "ch09_3", "ch09_4", "ch09_5"],
    "ch10_大渡河接力赛.md": ["ch10_1", "ch10_2", "ch10_3", "ch10_4", "ch10_5"],
    "ch11_千里送水.md": ["ch11_1", "ch11_2", "ch11_3", "ch11_4", "ch11_5"],
    "ch12_从今天开始觉醒.md": ["ch12_1", "ch12_2", "ch12_3", "ch12_4"],
}

success = 0
failed = 0

for filename, images in image_map.items():
    filepath = filename
    if not os.path.exists(filepath):
        log_msg(f"✗ {filename} 不存在")
        failed += 1
        continue
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find insertion point (end of file or before references section)
        if "## 参考文献" in content:
            insert_pos = content.find("## 参考文献")
        else:
            insert_pos = len(content)
        
        # Build image markdown
        image_markdown = "\n\n---\n\n## 配图\n\n"
        for i, img_key in enumerate(images, 1):
            img_url = f"https://raw.githubusercontent.com/leixiaohui-1974/books/main/books/T2-CN/H/fig_{img_key}.png"
            image_markdown += f"\n![图{i}]({img_url})\n"
        
        # Insert images
        new_content = content[:insert_pos] + image_markdown + "\n" + content[insert_pos:]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        log_msg(f"✓ {filename} ({len(images)} 张图片)")
        success += 1
    except Exception as e:
        log_msg(f"✗ {filename}: {str(e)}")
        failed += 1

log_msg(f"插入完成: {success}/{len(image_map)} 成功，{failed} 失败")
