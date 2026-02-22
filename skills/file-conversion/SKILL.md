# 文件格式转换完全指南

> 创建时间：2026-02-22  
> 适用范围：books / WriterLLM / patent 三个仓库  
> 目标：掌握所有常用文件格式转换技能

---

## 一、文档格式转换

### 1.1 Markdown ↔ 其他格式

#### Markdown → PDF

**方法 1：WeasyPrint（推荐，支持中文）**
```bash
pip3 install weasyprint

# 转换为 HTML 再转 PDF
markdown input.md -o temp.html
weasyprint temp.html output.pdf

# 或使用 Python 脚本
python3 -c "
from weasyprint import HTML
import markdown

md_text = open('input.md', 'r', encoding='utf-8').read()
html = markdown.markdown(md_text, extensions=['tables', 'fenced_code', 'toc'])
HTML(string=html).write_pdf('output.pdf')
"
```

**方法 2：Pandoc（功能最全）**
```bash
# 安装 pandoc
# Ubuntu/Debian: sudo apt install pandoc
# macOS: brew install pandoc

# 直接转换
pandoc input.md -o output.pdf

# 指定引擎（推荐 xelatex 支持中文）
pandoc input.md --pdf-engine=xelatex -o output.pdf

# 添加元数据
pandoc input.md -o output.pdf \
  -M title="文档标题" \
  -M author="作者名" \
  -M date="2026-02-22"
```

**方法 3：Markdown 命令行工具**
```bash
# 安装
pip3 install markdown

# 转换为 HTML
markdown input.md > output.html

# 或使用 Python
python3 -c "
import markdown
html = markdown.markdown(open('input.md').read(), extensions=['tables', 'fenced_code'])
print(html)
" > output.html
```

#### Markdown → DOCX

```bash
# Pandoc 转换
pandoc input.md -o output.docx

# 保留样式
pandoc input.md --reference-doc=template.docx -o output.docx
```

#### Markdown → EPUB

```bash
# 转换为电子书
pandoc input.md -o output.epub \
  --epub-title="书名" \
  --epub-author="作者"

# 使用 Calibre（更专业）
ebook-convert input.md output.epub
```

#### Markdown → HTML

```bash
# 使用 markdown 命令行
markdown input.md > output.html

# 使用 pandoc
pandoc input.md -o output.html --standalone

# 使用 Python（可定制）
python3 << 'EOF'
import markdown

# 读取 markdown
with open('input.md', 'r', encoding='utf-8') as f:
    md_text = f.read()

# 转换为 HTML（启用扩展）
html = markdown.markdown(md_text, extensions=[
    'tables',      # 表格支持
    'fenced_code', # 代码块
    'toc',         # 目录
    'nl2br',       # 换行转<br>
])

# 添加 HTML 包装
full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>文档标题</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; }}
        th {{ background-color: #f2f2f2; }}
        code {{ background: #f4f4f4; padding: 2px 5px; }}
        pre {{ background: #f4f4f4; padding: 10px; overflow-x: auto; }}
    </style>
</head>
<body>
{html}
</body>
</html>"""

with open('output.html', 'w', encoding='utf-8') as f:
    f.write(full_html)
print("✅ 转换完成")
EOF
```

---

### 1.2 PDF ↔ 其他格式

#### PDF → Word

```bash
# 使用 pandoc（简单 PDF）
pandoc input.pdf -o output.docx

# 使用 pdf2docx（推荐，保持格式）
pip3 install pdf2docx
python3 -c "
from pdf2docx import Converter
cv = Converter('input.pdf')
cv.convert('output.docx')
cv.close()
"
```

#### PDF → Markdown

```bash
# 使用 pdftotext
pdftotext input.pdf output.txt

# 使用 pdfplumber（Python，保持表格）
pip3 install pdfplumber
python3 << 'EOF'
import pdfplumber

with pdfplumber.open('input.pdf') as pdf:
    text = ''
    for page in pdf.pages:
        text += page.extract_text() + '\n\n'
    
    with open('output.md', 'w', encoding='utf-8') as f:
        f.write(text)
print("✅ 转换完成")
EOF
```

#### PDF → 图片

```bash
# 使用 pdf2image
pip3 install pdf2image
python3 << 'EOF'
from pdf2image import convert_from_path

images = convert_from_path('input.pdf', dpi=300)
for i, image in enumerate(images):
    image.save(f'page_{i+1}.png', 'PNG')
print(f"✅ 导出 {len(images)} 页图片")
EOF
```

---

### 1.3 Word ↔ 其他格式

#### Word → Markdown

```bash
# 使用 pandoc
pandoc input.docx -o output.md

# 使用 mammoth（Python，保持结构）
pip3 install mammoth
python3 << 'EOF'
import mammoth

with open("input.docx", "rb") as docx_file:
    result = mammoth.convert_to_html(docx_file)
    html = result.value
    
    # HTML → Markdown（可选）
    import html2text
    h = html2text.HTML2Text()
    md = h.handle(html)
    
    with open('output.md', 'w', encoding='utf-8') as f:
        f.write(md)
print("✅ 转换完成")
EOF
```

#### Word → PDF

```bash
# 使用 LibreOffice（推荐）
libreoffice --headless --convert-to pdf input.docx

# 使用 pandoc
pandoc input.docx -o output.pdf
```

---

## 二、图片格式转换

### 2.1 使用 ImageMagick

```bash
# 安装
# Ubuntu/Debian: sudo apt install imagemagick
# macOS: brew install imagemagick

# 基本转换
convert input.png output.jpg
convert input.jpg output.png

# 批量转换
mogrify -format jpg *.png
mogrify -format png -resize 800x600 *.jpg

# 调整大小
convert input.png -resize 800x600 output.png

# 压缩
convert input.jpg -quality 85 output.jpg

# 合并多页 PDF
convert *.png output.pdf

# PDF 转图片
convert -density 300 input.pdf -quality 100 output.png
```

### 2.2 使用 Python PIL/Pillow

```python
from PIL import Image
import os

# 单张转换
img = Image.open('input.png')
img.save('output.jpg', quality=95)

# 批量转换
for filename in os.listdir('.'):
    if filename.endswith('.png'):
        img = Image.open(filename)
        img.save(filename.replace('.png', '.jpg'), 'JPEG')

# 调整大小
img = Image.open('input.jpg')
img = img.resize((800, 600), Image.Resampling.LANCZOS)
img.save('output.jpg')

# 创建缩略图
img.thumbnail((200, 200))
img.save('thumbnail.jpg')
```

---

## 三、视频/音频格式转换

### 3.1 使用 FFmpeg

```bash
# 安装
# Ubuntu/Debian: sudo apt install ffmpeg
# macOS: brew install ffmpeg

# 视频格式转换
ffmpeg -i input.mp4 -c:v libx264 -c:a aac output.mkv

# 提取音频
ffmpeg -i input.mp4 -q:a 0 -map a output.mp3

# 视频压缩
ffmpeg -i input.mp4 -vcodec libx265 -crf 28 output.mp4

# 调整分辨率
ffmpeg -i input.mp4 -vf scale=1280:720 output_720p.mp4

# 截取片段
ffmpeg -i input.mp4 -ss 00:01:00 -t 00:00:30 -c copy clip.mp4

# 合并视频
ffmpeg -f concat -i file_list.txt -c copy output.mp4

# 添加字幕
ffmpeg -i input.mp4 -subtitles subtitle.srt output.mp4

# 音频格式转换
ffmpeg -i input.wav -b:a 192K output.mp3

# 提取视频 GIF
ffmpeg -i input.mp4 -vf "fps=10,scale=320:-1" output.gif
```

### 3.2 使用 SoX（音频处理）

```bash
# 安装
# Ubuntu/Debian: sudo apt install sox libsox-fmt-all
# macOS: brew install sox

# 音频格式转换
sox input.wav output.mp3
sox input.flac output.wav

# 音频合并
sox input1.wav input2.wav output.wav

# 音频裁剪
sox input.wav output.wav trim 0 30

# 改变语速
sox input.wav output.wav speed 1.2

# 降噪
sox input.wav output.wav noisered profile 0.21
```

---

## 四、电子书格式转换

### 4.1 使用 Calibre

```bash
# 安装
# Ubuntu/Debian: sudo apt install calibre
# macOS: brew install --cask calibre

# EPUB → MOBI
ebook-convert input.epub output.mobi

# MOBI → EPUB
ebook-convert input.mobi output.epub

# PDF → EPUB
ebook-convert input.pdf output.epub

# EPUB → PDF
ebook-convert input.epub output.pdf \
  --paper-size a4 \
  --pdf-page-margin 72

# 批量转换
for f in *.epub; do
    ebook-convert "$f" "${f%.epub}.mobi"
done
```

---

## 五、数据格式转换

### 5.1 JSON ↔ CSV

```python
# JSON → CSV
import json
import csv

with open('input.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('output.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)

# CSV → JSON
import csv
import json

with open('input.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    data = list(reader)

with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

### 5.2 Excel ↔ CSV

```python
import pandas as pd

# Excel → CSV
df = pd.read_excel('input.xlsx')
df.to_csv('output.csv', index=False, encoding='utf-8')

# CSV → Excel
df = pd.read_csv('input.csv')
df.to_excel('output.xlsx', index=False)

# Excel → JSON
df = pd.read_excel('input.xlsx')
df.to_json('output.json', orient='records', force_ascii=False, indent=2)
```

### 5.3 XML ↔ JSON

```python
import xml.etree.ElementTree as ET
import json

# XML → JSON
def xml_to_dict(element):
    result = {}
    for child in element:
        if len(child):
            result[child.tag] = xml_to_dict(child)
        else:
            result[child.tag] = child.text
    return result

tree = ET.parse('input.xml')
root = tree.getroot()
data = xml_to_dict(root)

with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

---

## 六、LaTeX ↔ 其他格式

### 6.1 LaTeX → PDF

```bash
# 使用 pdflatex
pdflatex input.tex
pdflatex input.tex  # 运行两次以解决引用

# 使用 xelatex（支持中文）
xelatex input.tex
xelatex input.tex

# 使用 latexmk（自动处理依赖）
latexmk -pdf input.tex
latexmk -xelatex input.tex  # 中文
```

### 6.2 LaTeX → Markdown

```bash
# 使用 pandoc
pandoc input.tex -o output.md

# 使用 latex2markdown（Python）
pip3 install latex2markdown
latex2markdown input.tex > output.md
```

### 6.3 Markdown → LaTeX

```bash
# 使用 pandoc
pandoc input.md -o output.tex

# 指定文档类
pandoc input.md -o output.tex \
  --template=eisvogel \
  --listings
```

---

## 七、批量转换脚本

### 7.1 批量 Markdown → PDF

```bash
#!/bin/bash
# convert_all_md_to_pdf.sh

for file in *.md; do
    echo "📝 转换：$file"
    pandoc "$file" --pdf-engine=xelatex -o "${file%.md}.pdf" \
      -M title="${file%.md}" \
      -M author="作者" \
      -M date="2026-02-22"
done

echo "✅ 全部转换完成"
```

### 7.2 批量图片压缩

```bash
#!/bin/bash
# compress_images.sh

mkdir -p compressed

for file in *.jpg *.jpeg *.png; do
    if [ -f "$file" ]; then
        echo "🖼️  压缩：$file"
        convert "$file" -quality 85 -resize 1920x1920\> "compressed/$file"
    fi
done

echo "✅ 全部压缩完成"
```

### 7.3 批量视频转 GIF

```bash
#!/bin/bash
# video_to_gif.sh

for file in *.mp4; do
    echo "🎬 转换：$file"
    ffmpeg -i "$file" -vf "fps=10,scale=480:-1" "${file%.mp4}.gif"
done

echo "✅ 全部转换完成"
```

---

## 八、Python 转换工具包

### 8.1 安装依赖

```bash
pip3 install \
  markdown \
  pdfkit \
  weasyprint \
  pdfplumber \
  pdf2docx \
  mammoth \
  html2text \
  pillow \
  pandas \
  openpyxl \
  ebooklib \
  calibre
```

### 8.2 万能转换脚本

```python
#!/usr/bin/env python3
"""
万能文件格式转换脚本
支持：md/html/pdf/docx/epub/jpg/png 等格式互转
"""

import sys
import os
from pathlib import Path

def convert_file(input_path, output_path=None):
    """自动检测格式并转换"""
    input_path = Path(input_path)
    suffix = input_path.suffix.lower()
    
    if output_path is None:
        output_path = input_path.with_suffix('.pdf')
    
    print(f"🔄 转换：{input_path} → {output_path}")
    
    # 根据扩展名选择转换方法
    if suffix == '.md':
        convert_md_to_pdf(input_path, output_path)
    elif suffix == '.docx':
        convert_docx_to_pdf(input_path, output_path)
    # ... 添加更多格式
    
    print(f"✅ 完成：{output_path}")

def convert_md_to_pdf(input_path, output_path):
    """Markdown → PDF"""
    import markdown
    from weasyprint import HTML
    
    with open(input_path, 'r', encoding='utf-8') as f:
        md_text = f.read()
    
    html = markdown.markdown(md_text, extensions=['tables', 'fenced_code', 'toc'])
    HTML(string=html).write_pdf(output_path)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法：python convert.py input_file [output_file]")
        sys.exit(1)
    
    convert_file(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
```

---

## 九、在线转换工具（备用）

| 工具 | 网址 | 支持格式 | 特点 |
|------|------|---------|------|
| CloudConvert | cloudconvert.com | 200+ 格式 | 免费、支持 API |
| Zamzar | zamzar.com | 1200+ 格式 | 老牌、邮件通知 |
| Online-Convert | online-convert.com | 50+ 格式 | 可定制参数 |
| PDF24 | tools.pdf24.org | PDF 相关 | 完全免费 |

---

## 十、最佳实践

### 10.1 文档转换建议

1. **Markdown → PDF**：使用 WeasyPrint 或 Pandoc + xelatex
2. **Word → PDF**：使用 LibreOffice 保持格式最佳
3. **PDF → Word**：使用 pdf2docx 保持排版
4. **批量转换**：先测试单个文件，确认无误后批量

### 10.2 图片转换建议

1. **无损格式**：PNG → PNG（压缩用 pngquant）
2. **有损格式**：JPG 质量 85% 平衡体积和质量
3. **印刷用途**：300 DPI，CMYK 色彩
4. **网络用途**：72-150 DPI，RGB 色彩，WebP 格式

### 10.3 视频转换建议

1. **通用格式**：MP4 (H.264 + AAC)
2. **高质量**：MKV (H.265/HEVC)
3. **网络传播**：MP4，码率 2-5 Mbps
4. **本地播放**：MKV，码率 10-20 Mbps

---

## 十一、故障排查

### 常见问题

**Q1: Pandoc 转换 PDF 失败**
```bash
# 安装 TeX Live
sudo apt install texlive-xetex texlive-lang-chinese

# 或使用简单引擎
pandoc input.md --pdf-engine=wkhtmltopdf -o output.pdf
```

**Q2: 中文显示乱码**
```bash
# 使用 xelatex 引擎
pandoc input.md --pdf-engine=xelatex -o output.pdf

# 或在 CSS 中指定中文字体
body { font-family: "SimSun", "宋体", serif; }
```

**Q3: 表格格式丢失**
```bash
# Pandoc 保留表格
pandoc input.md -o output.docx --reference-doc=template.docx

# 或使用 pandoc-table 扩展
```

**Q4: 图片质量下降**
```bash
# 提高 JPG 质量
convert input.png -quality 95 output.jpg

# 或使用无损格式
convert input.png output.png
```

---

## 十二、技能检查清单

- [ ] Markdown ↔ PDF/HTML/DOCX/EPUB
- [ ] PDF ↔ Word/Markdown/图片
- [ ] Word ↔ Markdown/PDF
- [ ] PNG ↔ JPG ↔ GIF ↔ WebP
- [ ] MP4 ↔ MKV ↔ AVI
- [ ] MP3 ↔ WAV ↔ FLAC
- [ ] JSON ↔ CSV ↔ XML ↔ Excel
- [ ] LaTeX ↔ PDF ↔ Markdown
- [ ] 批量转换脚本编写
- [ ] 故障排查能力

---

**最后更新**: 2026-02-22  
**维护者**: AI Assistant  
**适用仓库**: books / WriterLLM / patent
