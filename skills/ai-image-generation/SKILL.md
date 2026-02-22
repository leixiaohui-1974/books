# AI 图像生成技能指南

> 创建时间：2026-02-22  
> 适用范围：书稿插图/论文配图/技术图表/PPT 素材  
> 目标：掌握 AI 驱动的科研图像生成技能

---

## 一、AI 图像生成工具对比

### 1.1 主流工具总览

| 工具 | 类型 | 价格 | 特点 | 适用场景 |
|------|------|------|------|---------|
| **DALL-E 3** | 文生图 | $20/月 | 理解能力强，适合复杂场景 | 概念图/示意图 |
| **Midjourney** | 文生图 | $10-60/月 | 艺术效果好，细节丰富 | 封面/插图 |
| **Stable Diffusion** | 文生图 | 免费 | 开源，可本地部署 | 批量生成 |
| **Leonardo.ai** | 文生图 | 免费+$10/月 | 科学插图优化 | 技术图表 |
| **BioRender** | 模板库 | 免费+$30/月 | 生物医学专用 | 生物/医学图 |
| **Mind the Graph** | 模板库 | $10-25/月 | 科研 infographic | 科普图/摘要图 |
| **Draw.io** | 手绘 | 免费 | 流程图/架构图 | 技术框图 |
| **Mermaid** | 代码绘图 | 免费 | 文本描述生成 | 流程图/时序图 |

### 1.2 Nano Banana 类似工具

**Nano Banana 特点**：
- 文本描述生成图片
- 支持技术图表
- 风格简洁专业
- 适合书稿插图

**替代方案**：

#### 方案 1: DALL-E 3 (推荐)

```
优势:
- 理解复杂提示词
- 生成质量稳定
- 支持文字渲染
- API 可集成

访问:
- https://chat.openai.com (ChatGPT Plus)
- https://labs.openai.com (DALL-E Labs)
- API: api.openai.com

价格:
- ChatGPT Plus: $20/月
- API: $0.04/张 (1024x1024)
```

#### 方案 2: Leonardo.ai

```
优势:
- 科学插图优化
- 每日免费 150 积分
- 支持 ControlNet
- 可训练自定义模型

访问:
- https://leonardo.ai

价格:
- 免费：150 积分/天
- 付费：$10-48/月
```

#### 方案 3: Stable Diffusion + ControlNet

```
优势:
- 完全免费
- 本地部署
- 精确控制构图
- 可批量生成

部署:
- WebUI: https://github.com/AUTOMATIC1111/stable-diffusion-webui
- ComfyUI: https://github.com/comfyanonymous/ComfyUI

硬件要求:
- GPU: NVIDIA 8GB+ 显存
- 内存：16GB+
- 硬盘：50GB+
```

---

## 二、文生图提示词工程

### 2.1 基本结构

```
Prompt 公式:

[主体描述] + [细节特征] + [风格定位] + [技术参数] + [负面提示]

示例:
"A professional technical diagram of water distribution network 
control system, three-layer architecture with DAL/PAI/CAI, 
clean vector style, blue color scheme, high contrast, 
minimalist design, suitable for academic paper --ar 16:9 --v 5"

分解:
- 主体：water distribution network control system
- 细节：three-layer architecture with DAL/PAI/CAI
- 风格：clean vector style, blue color scheme
- 技术：high contrast, minimalist design
- 用途：suitable for academic paper
- 参数：--ar 16:9 (宽高比) --v 5 (版本)
```

### 2.2 科研插图提示词模板

#### 系统架构图

```
Prompt:
"A clean technical architecture diagram showing [系统名称] 
with [N] layers, layered structure, top layer shows [上层功能], 
middle layer shows [中层功能], bottom layer shows [下层功能], 
arrows indicate data flow, professional vector illustration, 
blue and white color scheme, minimalist style, 
suitable for academic publication, high resolution --ar 3:2 --q 2"

中文翻译:
"一张清晰的技术架构图，展示 [系统名称]，包含 [N] 层结构，
顶层显示 [上层功能]，中层显示 [中层功能]，底层显示 [下层功能]，
箭头表示数据流，专业矢量插图，蓝白配色，极简风格，
适合学术出版，高分辨率"
```

#### 流程图

```
Prompt:
"A professional flowchart diagram illustrating [流程名称] process, 
starting from [起点], going through [步骤 1], [步骤 2], [步骤 3], 
ending at [终点], decision diamonds for branching, 
clean lines and boxes, technical drawing style, 
blue color scheme, white background, academic quality --ar 4:3"
```

#### 数据可视化

```
Prompt:
"A scientific data visualization chart showing [数据类型], 
[折线图/柱状图/散点图/热力图], clear axis labels, 
professional color palette (viridis/plasma), 
grid lines, legend, suitable for Nature/Science publication, 
high contrast, vector style --ar 16:9"
```

#### 概念示意图

```
Prompt:
"A conceptual illustration of [概念名称], 
showing [核心思想], metaphor of [比喻对象], 
abstract but clear, modern scientific illustration style, 
gradient colors, clean composition, 
suitable for textbook cover or chapter opening, 
professional quality --ar 3:4 --q 2"
```

### 2.3 负面提示词 (Negative Prompt)

```
通用负面提示:
"blurry, low quality, distorted, ugly, deformed, 
noisy, cluttered, messy, unprofessional, 
cartoon, anime, photorealistic, 3d render, 
text watermark, signature, frame, border"

科研插图特别负面提示:
"no photorealistic elements, no artistic filters, 
no decorative elements, no people, no faces, 
no brand logos, no copyright text"
```

---

## 三、DALL-E 3 实战

### 3.1 访问方式

#### ChatGPT Plus (推荐)

```
步骤:
1. 访问 https://chat.openai.com
2. 订阅 ChatGPT Plus ($20/月)
3. 对话中直接要求生成图片
4. 可多次修改直到满意

示例对话:
User: "帮我生成一张水系统控制论的理论框架图"
Assistant: [生成图片]
User: "把颜色改成蓝色系，增加箭头表示关系"
Assistant: [重新生成]
```

#### API 调用

```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

response = client.images.generate(
    model="dall-e-3",
    prompt="A professional technical diagram of water distribution network control system...",
    size="1024x1024",
    quality="hd",
    n=1,
)

image_url = response.data[0].url
print(f"图片 URL: {image_url}")
```

### 3.2 高质量提示词示例

#### 示例 1: CHS 理论框架图

```
Prompt:
"A comprehensive theoretical framework diagram for Cybernetics of 
Hydro Systems (CHS), showing eight principles organized in five 
layers: modeling foundation layer (P1-P2), architecture layer 
(P3-P4), verification layer (P5), intelligence layer (P6-P7), 
and evolution layer (P8). Clean hierarchical structure with 
connecting arrows, professional academic illustration style, 
blue and gray color scheme, vector graphics quality, suitable 
for textbook publication, white background, high resolution --ar 16:9 --q 2"

预期效果:
- 五层水平排列
- 每层包含 1-2 个原理
- 箭头表示依赖关系
- 蓝灰色系专业风格
```

#### 示例 2: HydroOS 三层架构图

```
Prompt:
"A three-layer architecture diagram of HydroOS water network 
operating system. Top layer: Cognitive AI Engine (CAI) with 
LLM, knowledge graph, multi-agent coordination. Middle layer: 
Physical AI Engine (PAI) with hydrodynamic models, MPC controller, 
safety envelope. Bottom layer: Device Abstraction Layer (DAL) 
with device drivers, protocol adapters, SCADA integration. 
Clear layer separation, data flow arrows between layers, 
professional technical illustration, blue gradient colors, 
vector style, suitable for academic paper, white background --ar 3:2 --q 2"

预期效果:
- 三层垂直堆叠
- 每层标注核心组件
- 箭头表示数据流向
- 蓝色渐变专业配色
```

#### 示例 3: WNAL 等级演进图

```
Prompt:
"A horizontal timeline diagram showing Water Network Autonomy 
Level (WNAL) evolution from L0 to L5. L0: manual operation 
(icon: person), L1: rule-based automation (icon: gear), 
L2: conditional autonomy (icon: robot assistant), 
L3: high autonomy (icon: advanced robot), 
L4: full autonomy (icon: AI brain), 
L5: unconditional autonomy (icon: super AI). 
Each level with brief description box, progress arrow, 
professional infographic style, blue to purple gradient, 
clean modern design, suitable for textbook, white background --ar 16:9 --q 2"

预期效果:
- 水平时间轴
- 每级配图标和说明
- 蓝到紫渐变色
- 现代信息图风格
```

#### 示例 4: 安全包络三区图

```
Prompt:
"A safety envelope diagram showing three-zone protection for 
water system operation. Inner green zone (normal operation, 
autonomous control), middle yellow zone (caution, degraded 
control), outer red zone (danger, manual takeover). 
Concentric circles or nested boundaries, clear zone labels, 
warning icons for red zone, check marks for green zone, 
professional safety diagram style, traffic light colors 
(green/yellow/red), vector quality, white background --ar 4:3 --q 2"

预期效果:
- 嵌套三区 (绿/黄/红)
- 清晰标注
- 交通灯配色
- 专业安全图风格
```

#### 示例 5: 四态机状态迁移图

```
Prompt:
"A four-state machine state transition diagram for water system 
operation management. Four states: Normal (green), Warning 
(yellow), Restricted (orange), Emergency (red). States arranged 
in circular or diamond layout, transition arrows with condition 
labels, decision points shown as diamonds, professional control 
system diagram, state machine visualization, clear typography, 
color-coded states, vector style, academic quality --ar 1:1 --q 2"

预期效果:
- 四状态圆形/菱形布局
- 迁移箭头带条件标注
- 状态颜色编码
- 专业控制系统图
```

---

## 四、Stable Diffusion 本地部署

### 4.1 WebUI 安装

```bash
# 1. 克隆仓库
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git
cd stable-diffusion-webui

# 2. 下载模型
# 访问 https://civitai.com 下载检查点文件
# 推荐模型:
# - SDXL Base 1.0 (高质量)
# - Realistic Vision (写实风格)
# - Deliberate (通用)

# 放置模型到:
models/Stable-diffusion/

# 3. 启动
./webui.sh  # Linux/Mac
webui.bat  # Windows

# 4. 访问
# http://localhost:7860
```

### 4.2 ControlNet 精确控制

```
ControlNet 功能:
- Canny: 边缘检测控制
- Depth: 深度图控制
- Pose: 姿态控制
- Scribble: 草图控制
- Inpaint: 局部重绘

使用流程:
1. 上传参考图 (草图/边缘图/深度图)
2. 选择 ControlNet 模型
3. 输入提示词
4. 生成 (保持构图)

示例:
- 上传手绘草图 → ControlNet Scribble
- 上传架构图线稿 → ControlNet Canny
- 上传 3D 模型深度 → ControlNet Depth
```

### 4.3 批量生成脚本

```python
from PIL import Image
import requests
from io import BytesIO
import os

# 提示词列表
prompts = [
    "A technical diagram of water system control architecture...",
    "A flowchart showing MPC control process...",
    "A conceptual illustration of ODD definition...",
    # ... 更多提示词
]

# 批量生成
for i, prompt in enumerate(prompts):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="hd",
        n=1,
    )
    
    image_url = response.data[0].url
    image = Image.open(requests.get(image_url).stream)
    image.save(f"figure_{i+1:02d}.png")
    print(f"✅ Saved: figure_{i+1:02d}.png")
```

---

## 五、论文配图工作流

### 5.1 完整流程

```
Step 1: 需求分析 (30 分钟)
├── 确定图的类型 (架构图/流程图/数据图/概念图)
├── 确定尺寸比例 (16:9/4:3/1:1)
├── 确定配色方案 (蓝/绿/红/渐变)
└── 确定风格 (矢量/写实/扁平)

Step 2: 草图设计 (1 小时)
├── 手绘或使用 Draw.io 画草图
├── 标注关键元素
├── 确定布局结构
└── 保存为参考图

Step 3: AI 生成 (2-4 小时)
├── 编写详细提示词
├── 使用 DALL-E 3 生成初稿
├── 迭代优化 (3-5 轮)
├── 使用 ControlNet 精确控制 (可选)
└── 选择最佳版本

Step 4: 后期处理 (1-2 小时)
├── 使用 Illustrator/GIMP 调整
├── 添加文字标注
├── 调整颜色对比度
├── 导出多种格式 (PNG/SVG/PDF)
└── 分辨率检查 (≥300 DPI)

Step 5: 质量检查 (30 分钟)
├── 清晰度检查
├── 颜色一致性
├── 文字可读性
├── 与正文引用一致
└── 符合期刊要求
```

### 5.2 期刊要求对照

| 期刊 | 分辨率 | 格式 | 色彩模式 | 最大宽度 |
|------|--------|------|---------|---------|
| Nature | 300 DPI | TIFF/EPS | RGB/CMYK | 单栏 89mm/双栏 183mm |
| Science | 300 DPI | EPS/PDF | RGB | 单栏 90mm/全宽 190mm |
| WRR | 300 DPI | TIFF/EPS | RGB | 170mm |
| EMS | 300 DPI | PNG/TIFF | RGB | 180mm |
| 水利学报 | 300 DPI | JPG/PNG | RGB | 165mm |

### 5.3 导出设置

```
# GIMP 导出设置

File → Export As → figure.png

设置:
- Quality: 100%
- Resolution: 300 DPI
- Color Space: sRGB
- Compression: None (TIFF)

# Illustrator 导出设置

File → Export → Export As

设置:
- Format: PDF/EPS/SVG
- Resolution: 300 PPI
- Color Mode: RGB
- Embed Fonts: Yes
```

---

## 六、实战案例：T1-CN 书插图生成

### 6.1 第一章插图

#### 图 1-1: 五代演进图

```
Prompt:
"A horizontal timeline showing five generations of water system 
operation management evolution. Gen1: Manual operation (1950s, 
icon: person with clipboard), Gen2: SCADA automation (1980s, 
icon: computer screen), Gen3: Networked control (2000s, 
icon: network), Gen4: Digital twin (2010s, icon: 3D model), 
Gen5: Autonomous operation (2020s, icon: AI brain). 
Clean infographic style, progress arrow from left to right, 
blue gradient colors, each generation in a box with year 
and description, professional textbook illustration, 
white background --ar 16:9 --q 2"

文件命名：fig01-01_evolution.png
尺寸：1024x576 (16:9)
用途：第一章§1.2 五代演进
```

#### 图 1-2: 自主运行概念图

```
Prompt:
"A conceptual illustration comparing traditional manual operation 
vs autonomous operation of water systems. Left side: multiple 
operators in control room, many screens, manual valves 
(labeled 'Traditional'). Right side: sleek AI system, 
automated controls, minimal human supervision (labeled 
'Autonomous'). Split composition with dividing line, 
professional technical illustration, blue and orange 
contrast colors, vector style, textbook quality --ar 16:9 --q 2"

文件命名：fig01-02_autonomous_concept.png
尺寸：1024x576 (16:9)
用途：第一章§1.3 自主运行概念
```

### 6.2 第二章插图

#### 图 2-1: CPS 三维框架图

```
Prompt:
"A three-dimensional coordinate system showing CPS framework 
for water systems. X-axis: Physical (P) with icons of 
dams, pumps, pipes. Y-axis: Cyber (C) with icons of 
sensors, networks, computers. Z-axis: Social (S) with 
icons of operators, managers, policies. Three axes 
intersecting at origin, clean 3D diagram, professional 
academic illustration, blue green orange for three axes, 
white background, vector quality --ar 4:3 --q 2"

文件命名：fig02-01_cps_framework.png
尺寸：768x1024 (4:3)
用途：第二章§2.2 CPS 框架
```

### 6.3 第三章插图

#### 图 3-1: 八原理依赖导图

```
Prompt:
"A dependency diagram showing eight principles of CHS organized 
in five horizontal layers. Layer 1 (bottom): P1 Transfer 
Function, P2 Controllability. Layer 2: P3 Hierarchical Control, 
P4 Safety Envelope. Layer 3: P5 In-loop Verification. Layer 4: 
P6 Cognitive Enhancement, P7 Human-Machine Fusion. Layer 5 (top): 
P8 Autonomous Evolution. Forward arrows between layers, 
feedback arrow from P4 to P8 (red color). Clean hierarchical 
diagram, professional academic style, blue color scheme with 
red highlight for constraint arrow, vector graphics --ar 16:9 --q 2"

文件命名：fig03-01_eight_principles.png
尺寸：1024x576 (16:9)
用途：第三章§3.1 八原理框架
```

### 6.4 批量生成脚本

```python
#!/usr/bin/env python3
"""
T1-CN 书稿插图批量生成脚本
使用 DALL-E 3 API 生成全书 30+ 张插图
"""

from openai import OpenAI
import json
import os
from pathlib import Path

# 初始化客户端
client = OpenAI(api_key="your-api-key")

# 插图清单
figures = [
    {
        "id": "fig01-01",
        "chapter": 1,
        "prompt": "A horizontal timeline showing five generations...",
        "section": "§1.2",
        "caption": "图 1-1: 水利工程运行管理系统五代演进",
        "aspect_ratio": "16:9"
    },
    {
        "id": "fig01-02",
        "chapter": 1,
        "prompt": "A conceptual illustration comparing traditional...",
        "section": "§1.3",
        "caption": "图 1-2: 传统人工调度与自主运行对比",
        "aspect_ratio": "16:9"
    },
    # ... 更多插图
]

# 输出目录
output_dir = Path("figures")
output_dir.mkdir(exist_ok=True)

# 批量生成
for fig in figures:
    print(f"📝 生成 {fig['id']}: {fig['caption']}")
    
    response = client.images.generate(
        model="dall-e-3",
        prompt=fig['prompt'],
        size="1024x1024",
        quality="hd",
        n=1,
    )
    
    image_url = response.data[0].url
    
    # 下载并保存
    import requests
    from PIL import Image
    from io import BytesIO
    
    image = Image.open(requests.get(image_url).stream)
    image.save(output_dir / f"{fig['id']}.png")
    
    # 保存元数据
    metadata = {
        "id": fig['id'],
        "caption": fig['caption'],
        "section": fig['section'],
        "prompt": fig['prompt'],
        "url": image_url
    }
    
    with open(output_dir / f"{fig['id']}.json", 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 完成：{fig['id']}.png")

print("\n🎉 全部完成!")
```

---

## 七、技能检查清单

### 工具使用
- [ ] 注册并会使用 DALL-E 3
- [ ] 了解 Midjourney 基本用法
- [ ] 会部署 Stable Diffusion WebUI
- [ ] 掌握 ControlNet 精确控制
- [ ] 会使用 Leonardo.ai

### 提示词工程
- [ ] 掌握基本 Prompt 结构
- [ ] 会写系统架构图提示词
- [ ] 会写流程图提示词
- [ ] 会写数据可视化提示词
- [ ] 会写负面提示词

### 后期处理
- [ ] 会用 GIMP/Photoshop 调整
- [ ] 会用 Illustrator 添加文字
- [ ] 会导出符合期刊要求的格式
- [ ] 会检查分辨率 (≥300 DPI)

### 实战能力
- [ ] 能独立生成书稿插图
- [ ] 能生成论文配图
- [ ] 能制作 PPT 素材
- [ ] 能批量生成系列图

---

## 八、学习资源

### 在线教程

- [DALL-E 3 官方文档](https://platform.openai.com/docs/guides/images)
- [Midjourney 文档](https://docs.midjourney.com/)
- [Stable Diffusion WebUI 教程](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki)
- [ControlNet 使用指南](https://github.com/lllyasviel/ControlNet)

### 提示词库

- [Prompt Engineering Guide](https://github.com/dair-ai/Prompt-Engineering-Guide)
- [Midjourney Prompt Book](https://midjourney.gitbook.io/docs/)
- [Scientific Illustration Prompts](https://www.lexica.art/)

### 社区

- [Reddit r/StableDiffusion](https://reddit.com/r/StableDiffusion)
- [Discord Midjourney](https://discord.gg/midjourney)
- [CivitAI 模型社区](https://civitai.com/)

---

**最后更新**: 2026-02-22  
**维护者**: AI Assistant  
**适用仓库**: books / WriterLLM  
**工具推荐**: DALL-E 3 (首选) / Leonardo.ai (免费) / Stable Diffusion (本地)
