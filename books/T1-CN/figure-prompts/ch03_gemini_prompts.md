# 第三章 Gemini 图片生成提示词

## 图3-1: CHS 八原理依赖导图（五层结构）

**English Prompt for Gemini:**

```
Create a professional academic diagram showing the five-layer dependency structure of the CHS (Cybernetics of Hydro Systems) Eight Principles.

LAYOUT: Vertical pyramid structure, 2400×1800 px, clean engineering illustration style

FIVE LAYERS (bottom to top):

LAYER 1 - Foundation (底层：基础层, deep blue #1565C0):
- P1: Transfer Function (传递函数化)
  Icon: mathematical function symbol f(x)
- P2: Controllability & Observability (可控可观性)
  Icon: eye + hand symbol

LAYER 2 - Architecture (第二层：架构层, light blue #42A5F5):
- P3: Hierarchical & Distributed Control (分层分布式)
  Icon: multi-layer network structure

LAYER 3 - Operation (第三层：运行层, green #4CAF50):
- P4: Safety Envelope (安全包络)
  Icon: shield with safety boundary
- P7: Human-Machine Collaboration (人机共融)
  Icon: human + robot handshake

LAYER 4 - Assurance (第四层：保障层, orange #FF9800):
- P5: xIL Verification (在环验证)
  Icon: test loop symbol MIL→SIL→HIL
- P6: Cognitive Augmentation (认知增强)
  Icon: brain + AI symbol

LAYER 5 - Evolution (顶层：演进层, purple #7B1FA2):
- P8: Lifelong Autonomous Evolution (全生命周期自主演进)
  Icon: circular arrow with growth symbol

DEPENDENCY ARROWS:
- Upward solid arrows showing dependencies (gray #666):
  - P1, P2 → P3
  - P3 → P4, P7
  - P1, P2 → P5
  - P4 → P5
  - P3, P4 → P6
  - P5, P6, P7 → P8

- ONE red dashed constraint loop:
  - P4 → P8 with label "安全约束贯穿演进 Safety Constraint Throughout Evolution"
  - This is a constraint feedback, not a dependency

ANNOTATIONS:
- Each principle shows both Chinese and English names
- Layer labels on the left side
- Modern, professional textbook style
- Use icons/symbols to make each principle visually distinct
- Color gradient: darker at bottom (foundation) to lighter/colorful at top (evolution)
- White background, clear visual hierarchy

STYLE: Academic illustration, not cartoon. Think of engineering textbook diagrams. Clean lines, modern sans-serif font, professional color scheme.

Minimum 2400×1800 px, 300 DPI.
```

---

## 图3-2: MBD 四层一闭环架构

**English Prompt for Gemini:**

```
Create a professional diagram showing the MBD (Model-Based Design) Four-Layer One-Loop Framework for water systems.

LAYOUT: Vertical flow diagram with four layers + feedback loop, 2400×1600 px, clean engineering style

FOUR LAYERS (top to bottom):

LAYER 1 - ODD Definition (顶层：ODD定义层, light blue #E3F2FD with blue border #1565C0):
- Title: "ODD Definition Layer | 运行设计域定义层"
- Content box showing:
  - Six ODD parameters: 水文/设备/通信/环境/负载/时间
    (Hydrology / Equipment / Communication / Environment / Load / Time)
  - Icon: boundary/envelope symbol
  - Link annotation: "↔ P4 Safety Envelope"

LAYER 2 - Model & Decision (第二层：模型决策层, solid blue #1565C0, white text):
- Title: "Model & Decision Layer | 模型决策层"
- Content box showing:
  - Four model types: PBM | SM | OSEM | Data-driven
    (Physics-Based Model | Simplified Model | Online State Estimation | Data Model)
  - MPC decision engine
  - Link annotation: "↔ P1 Transfer Function"

LAYER 3 - xIL Verification (第三层：在环验证层, green #4CAF50, white text):
- Title: "xIL Verification Layer | 在环验证层"
- Content box showing:
  - Verification progression: MIL → SIL → HIL
  - Five-element evidence chain
  - Link annotation: "↔ P5 xIL Verification"

LAYER 4 - Field Execution (底层：现场执行层, gray #757575, white text):
- Title: "Field Execution Layer | 现场执行层"
- Content box showing:
  - SCADA + PLC + Actuators
  - Icon: industrial control equipment
  - Link annotation: "↔ P2 Controllability & Observability"

FLOW ARROWS:
- Downward solid arrows (blue/green):
  - Layer 1 → Layer 2: "Target & Constraints | 目标与约束 ↓"
  - Layer 2 → Layer 3: "Model & Strategy | 模型与策略 ↓"
  - Layer 3 → Layer 4: "Verified Pass | 验证通过 ↓"

- Upward dashed arrows (gray):
  - Layer 2 → Layer 1: "State Feedback | 状态反馈 ↑"
  - Layer 3 → Layer 2: "Verification Report | 验证报告 ↑"

- RED dashed feedback loop (emphasized):
  - Layer 4 → Layer 1: "Data Feedback Loop | 数据回馈↑ 持续进化闭环"
  - This is the "One Loop" in "Four-Layer One-Loop"
  - Curved arrow on the side, bold red color #D32F2F

ANNOTATIONS:
- Chinese + English bilingual labels
- Show which CHS principle (P1-P8) corresponds to each layer
- Clean modern diagram style
- White background
- Clear visual hierarchy with color coding

STYLE: Engineering system architecture diagram. Professional, not decorative. Think of diagrams in IEEE/ACM papers or technical textbooks.

Minimum 2400×1600 px, 300 DPI.
```

---

## 使用说明

将以上提示词分别输入 Gemini (Imagen 3) 进行图片生成。生成后：
1. 保存为 `fig_03_01_principles_dag_gemini.png` 和 `fig_03_02_mbd_framework_gemini.png`
2. 上传到 GitHub
3. 更新 ch03_final.md 中的图片链接

**文件创建时间**: 2026-02-25 06:48
