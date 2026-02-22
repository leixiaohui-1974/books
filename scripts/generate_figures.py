#!/usr/bin/env python3
"""
T1-CN《水系统控制论》书稿插图批量生成脚本
使用 DALL-E 3 API 生成全书 30+ 张插图

使用方法:
1. 设置 API Key: export OPENAI_API_KEY="sk-..."
2. 运行脚本：python3 generate_figures.py
3. 查看输出：figures/ 目录

依赖:
pip install openai requests Pillow
"""

from openai import OpenAI
import json
import os
import requests
from PIL import Image
from io import BytesIO
from pathlib import Path
from datetime import datetime

# 初始化客户端
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 输出目录
output_dir = Path("figures")
output_dir.mkdir(exist_ok=True)

# T1-CN 全书插图清单（30+ 张）
FIGURES = [
    # ========== 第一章 ==========
    {
        "id": "fig01-01",
        "chapter": 1,
        "section": "§1.2",
        "caption": "图 1-1: 水利工程运行管理系统五代演进",
        "prompt": """A horizontal timeline diagram showing five generations of water system 
        operation management evolution from 1950s to 2020s. 
        Gen1 (1950s): Manual operation with icon of person with clipboard. 
        Gen2 (1980s): SCADA automation with computer screen icon. 
        Gen3 (2000s): Networked control with network icon. 
        Gen4 (2010s): Digital twin with 3D model icon. 
        Gen5 (2020s): Autonomous operation with AI brain icon. 
        Clean infographic style, progress arrow from left to right, 
        blue gradient colors, each generation in a box with year and label, 
        professional textbook illustration, white background, vector quality --ar 16:9""",
    },
    {
        "id": "fig01-02",
        "chapter": 1,
        "section": "§1.3",
        "caption": "图 1-2: 传统人工调度与自主运行对比",
        "prompt": """A split comparison illustration. Left side labeled 'Traditional': 
        busy control room with multiple operators, many monitor screens, 
        manual valve wheels, chaotic atmosphere. Right side labeled 'Autonomous': 
        clean modern control room, minimal human supervision, AI system interface, 
        automated controls, calm atmosphere. Professional technical illustration, 
        blue and orange contrast colors, vector style, textbook quality --ar 16:9""",
    },
    {
        "id": "fig01-03",
        "chapter": 1,
        "section": "§1.4",
        "caption": "图 1-3: 水利系统与自动驾驶系统类比",
        "prompt": """A comparison diagram showing analogy between water system and 
        autonomous vehicle. Top: Autonomous car with sensors (LiDAR, camera, radar), 
        decision-making system, actuators (steering, brake, throttle). 
        Bottom: Water system with sensors (water level, flow, pressure), 
        control system (MPC, AI), actuators (gates, pumps, valves). 
        Arrows showing correspondence between components. Clean technical 
        diagram, blue color scheme, academic illustration style --ar 16:9""",
    },
    {
        "id": "fig01-04",
        "chapter": 1,
        "section": "§1.5",
        "caption": "图 1-4: CHS 八原理层次关系图",
        "prompt": """A hierarchical diagram showing eight principles of Cybernetics of 
        Hydro Systems (CHS) organized in five horizontal layers from bottom to top. 
        Layer 1 (bottom, foundation): P1 Transfer Function, P2 Controllability. 
        Layer 2 (architecture): P3 Hierarchical Control, P4 Safety Envelope. 
        Layer 3 (verification): P5 In-loop Verification. 
        Layer 4 (intelligence): P6 Cognitive Enhancement, P7 Human-Machine Fusion. 
        Layer 5 (top, evolution): P8 Autonomous Evolution. 
        Forward arrows between layers showing dependency. One red feedback arrow 
        from P4 to P8 showing safety constraint. Clean academic diagram, 
        blue color scheme with red highlight, vector quality --ar 16:9""",
    },
    {
        "id": "fig01-05",
        "chapter": 1,
        "section": "§1.5",
        "caption": "图 1-5: 本书结构导读图",
        "prompt": """A flowchart showing book structure with nine chapters organized 
        in four parts. Part 1 (Foundation): Ch1 Introduction, Ch2 CPS Framework, 
        Ch3 Eight Principles, Ch4 WNAL/ODD, Ch5 HydroOS. Part 2 (Case Studies): 
        Ch6 Single Station, Ch7 Cascade, Ch8 Network. Part 3 (Future): 
        Ch9 Outlook. Arrows showing logical flow from foundation to practice 
        to future. Professional book structure diagram, blue gradient colors, 
        clean layout, academic quality --ar 9:16""",
    },
    
    # ========== 第二章 ==========
    {
        "id": "fig02-01",
        "chapter": 2,
        "section": "§2.2",
        "caption": "图 2-1: 水系统 CPS 三维分析框架",
        "prompt": """A three-dimensional coordinate system showing CPS framework 
        for water systems. X-axis labeled 'Physical (P)' with icons of dams, 
        pumps, pipes, channels. Y-axis labeled 'Cyber (C)' with icons of 
        sensors, networks, computers, algorithms. Z-axis labeled 'Social (S)' 
        with icons of operators, managers, policies, regulations. Three axes 
        intersecting at origin, clean 3D diagram, professional academic 
        illustration, blue-green-orange for three axes, white background --ar 4:3""",
    },
    {
        "id": "fig02-02",
        "chapter": 2,
        "section": "§2.4",
        "caption": "图 2-2: 可控模型族层次结构",
        "prompt": """A pyramid diagram showing hierarchical model family for water 
        system control. Top (high fidelity): PDE models, 3D simulation, 
        offline use. Middle (reduced order): Transfer functions, 
        linearized models, online control. Bottom (data-driven): 
        Machine learning, neural networks, parameter calibration. 
        Arrows showing derivation from high to low fidelity. 
        Professional technical diagram, blue gradient, vector style --ar 4:3""",
    },
    {
        "id": "fig02-03",
        "chapter": 2,
        "section": "§2.6",
        "caption": "图 2-3: 三类约束同步处理框架",
        "prompt": """A Venn diagram showing three types of constraints for water 
        system operation. Circle 1 (blue): Physical Constraints (water level, 
        flow, pressure limits). Circle 2 (green): Operational Constraints 
        (power demand, water supply, ecological flow). Circle 3 (orange): 
        Governance Constraints (policies, regulations, safety standards). 
        Intersection in center labeled 'Feasible Operating Region'. 
        Clean diagram, professional academic style --ar 4:3""",
    },
    {
        "id": "fig02-04",
        "chapter": 2,
        "section": "§2.7",
        "caption": "图 2-4: 四态机状态迁移图",
        "prompt": """A four-state machine state transition diagram for water system 
        operation. Four states in circular layout: Normal (green, center), 
        Warning (yellow, top), Restricted (orange, right), Emergency (red, bottom). 
        Transition arrows between states with condition labels like 
        'constraint violation', 'recovery', 'MRC triggered'. 
        Decision points shown as diamonds. Professional control system 
        diagram, state machine visualization, color-coded states --ar 1:1""",
    },
    
    # ========== 第三章 ==========
    {
        "id": "fig03-01",
        "chapter": 3,
        "section": "§3.1",
        "caption": "图 3-1: CHS 八原理依赖导图",
        "prompt": """A dependency graph showing eight principles of CHS with 
        directional relationships. P1 and P2 at bottom as foundation. 
        P3 and P4 in middle as architecture. P5 in center as verification. 
        P6 and P7 upper middle as intelligence. P8 at top as evolution. 
        Directed arrows showing dependencies. One special red arrow from 
        P4 to P8 showing safety constraint on evolution. Clean hierarchical 
        diagram, professional academic style, blue with red highlight --ar 16:9""",
    },
    
    # ========== 第四章 ==========
    {
        "id": "fig04-01",
        "chapter": 4,
        "section": "§4.3",
        "caption": "图 4-1: 水网自主等级 WNAL 六级分类",
        "prompt": """A horizontal ladder or staircase diagram showing six levels 
        of Water Network Autonomy from L0 to L5. L0 (bottom): Manual 
        (person icon). L1: Rule-based (gear icon). L2: Conditional 
        Autonomy (robot assistant icon). L3: High Autonomy (advanced 
        robot icon). L4: Full Autonomy (AI brain icon). L5 (top): 
        Unconditional Autonomy (super AI icon). Each level with brief 
        description box. Progress arrow upward. Professional infographic, 
        blue to purple gradient, modern design --ar 9:16""",
    },
    {
        "id": "fig04-02",
        "chapter": 4,
        "section": "§4.4",
        "caption": "图 4-2: 运行设计域 ODD 边界定义",
        "prompt": """A multi-dimensional boundary diagram showing ODD definition 
        for water system. Axes: Water Level (m), Flow Rate (m³/s), 
        Power Output (MW). A 3D envelope showing feasible operating 
        region with green (normal), yellow (caution), red (forbidden) 
        zones. Clear boundary surfaces labeled. Professional 3D plot, 
        scientific visualization, blue-green-red colors --ar 4:3""",
    },
    {
        "id": "fig04-03",
        "chapter": 4,
        "section": "§4.4",
        "caption": "图 4-3: 嵌套式安全包络三区设计",
        "prompt": """A target-style diagram with three concentric zones. 
        Inner circle (green): Normal Operation Zone, autonomous control 
        enabled. Middle ring (yellow): Caution Zone, degraded control, 
        increased monitoring. Outer ring (red): Danger Zone, manual 
        takeover required. Clear zone labels and boundary values. 
        Professional safety diagram, traffic light colors, vector quality --ar 1:1""",
    },
    {
        "id": "fig04-04",
        "chapter": 4,
        "section": "§4.5",
        "caption": "图 4-4: 在环验证三级体系",
        "prompt": """A three-stage verification pipeline diagram. Stage 1 (left): 
        MIL - Model-in-the-Loop with computer icon, simulation software, 
        120 test scenarios. Stage 2 (middle): SIL - Software-in-the-Loop 
        with code generation icon, PLC icon, 150 scenarios. Stage 3 (right): 
        HIL - Hardware-in-the-Loop with real hardware icon, real-time 
        simulator, 50 scenarios. Arrows showing progression. Professional 
        verification flowchart, blue color scheme --ar 16:9""",
    },
    
    # ========== 第五章 ==========
    {
        "id": "fig05-01",
        "chapter": 5,
        "section": "§5.2",
        "caption": "图 5-1: HydroOS 三层架构",
        "prompt": """A three-layer architecture diagram of HydroOS water network 
        operating system. Top layer (blue): Cognitive AI Engine with 
        LLM, Knowledge Graph, Multi-Agent icons. Middle layer (green): 
        Physical AI Engine with Hydrodynamic Models, MPC, Safety Envelope 
        icons. Bottom layer (gray): Device Abstraction Layer with 
        Device Drivers, Protocol Adapters, SCADA Integration icons. 
        Clear layer separation, bidirectional data flow arrows between 
        layers. Professional technical architecture diagram, vector style --ar 3:2""",
    },
    {
        "id": "fig05-02",
        "chapter": 5,
        "section": "§5.3",
        "caption": "图 5-2: 策略门禁四重检查机制",
        "prompt": """A flowchart showing four-gate strategy validation mechanism. 
        Gate 1: ODD Compliance Check. Gate 2: Safety Envelope Check. 
        Gate 3: Constraint Satisfaction Check. Gate 4: Governance Rule Check. 
        Strategy passes through all gates to be executed. Any gate failure 
        triggers rejection or degradation. Clear pass/fail paths. Professional 
        process flowchart, blue color scheme --ar 16:9""",
    },
    {
        "id": "fig05-03",
        "chapter": 5,
        "section": "§5.4",
        "caption": "图 5-3: 四状态运行模式管理",
        "prompt": """A state machine diagram showing four operational modes. 
        Normal Mode (green): Full autonomy, optimization enabled. 
        Degraded Mode (yellow): Conservative control, enhanced monitoring. 
        Restricted Mode (orange): Limited autonomy, human confirmation. 
        Emergency Mode (red): MRC activated, manual takeover. State 
        transitions with triggers labeled. Professional state diagram --ar 4:3""",
    },
    {
        "id": "fig05-04",
        "chapter": 5,
        "section": "§5.5",
        "caption": "图 5-4: HydroOS 与 SCADA 集成架构",
        "prompt": """An integration diagram showing HydroOS on top of existing 
        SCADA system. Bottom: SCADA (PLCs, RTUs, Sensors, Actuators). 
        Top: HydroOS (PAI, CAI, DAL). Integration layer shows protocol 
        adapters (Modbus, OPC UA). Arrows showing data flow from SCADA 
        to HydroOS and control commands back. Professional integration 
        architecture, blue and gray colors --ar 16:9""",
    },
    {
        "id": "fig05-05",
        "chapter": 5,
        "section": "§5.6",
        "caption": "图 5-5: HydroOS 部署路径与 WNAL 等级对齐",
        "prompt": """A roadmap diagram showing HydroOS deployment aligned with 
        WNAL levels. Phase 1 (L1): Basic Automation, 6-12 months. 
        Phase 2 (L2): Conditional Autonomy, 12-18 months. Phase 3 (L3): 
        High Autonomy, 18-24 months. Each phase with key milestones 
        and deliverables. Timeline arrow. Professional roadmap infographic, 
        blue gradient colors --ar 16:9""",
    },
    
    # ========== 第六章 ==========
    {
        "id": "fig06-01",
        "chapter": 6,
        "section": "§6.1",
        "caption": "图 6-1: 沙坪水电站地理位置与工程布局",
        "prompt": """A map-style diagram showing Shaping Hydropower Station 
        location and layout. Main elements: reservoir, dam, powerhouse, 
        spillway, intake, tailrace. Clear labels for each component. 
        Top-down view, technical drawing style, blue and gray colors, 
        professional engineering diagram --ar 4:3""",
    },
    {
        "id": "fig06-02",
        "chapter": 6,
        "section": "§6.2",
        "caption": "图 6-2: 沙坪水电站安全包络三区划分",
        "prompt": """A vertical cross-section diagram showing safety envelope 
        zones for Shaping reservoir. Green zone: 365-372m (normal). 
        Yellow zone: 363-365m and 372-375m (caution). Red zone: 
        <363m and >375m (danger). Clear water level markings, 
        zone labels with control strategies. Professional safety 
        diagram, traffic light colors --ar 4:3""",
    },
    {
        "id": "fig06-03",
        "chapter": 6,
        "section": "§6.2",
        "caption": "图 6-3: 沙坪水电站 HydroOS 架构映射",
        "prompt": """A three-layer diagram showing HydroOS architecture mapped 
        to Shaping station. Top: CAI (LLM for decision support). 
        Middle: PAI (MPC controller, safety envelope). Bottom: 
        DAL (gate drivers, sensor interfaces). Station-specific 
        labels and parameters. Professional technical diagram --ar 3:2""",
    },
    {
        "id": "fig06-04",
        "chapter": 6,
        "section": "§6.2",
        "caption": "图 6-4: 沙坪水电站分层优化控制策略",
        "prompt": """A hierarchical control strategy diagram. Top layer: 
        Day-ahead optimization (24h horizon). Middle layer: 
        Real-time rolling optimization (1h horizon). Bottom layer: 
        Second-level execution (1s cycle). Arrows showing information 
        flow between layers. Professional control architecture diagram --ar 4:3""",
    },
    
    # ========== 第七章 ==========
    {
        "id": "fig07-01",
        "chapter": 7,
        "section": "§7.1",
        "caption": "图 7-1: 瀑深枕梯级 EDC 三层控制架构",
        "prompt": """A three-tier control architecture for Pubugou-Shenxigou-Zhentou 
        cascade EDC. Top: Grid Dispatch Center (sends total load command). 
        Middle: Basin Control Center (EDC, allocates to stations). 
        Bottom: Three station AGC systems (Pubugou, Shenxigou, Zhentou). 
        Water flow arrows downward, information flow arrows bidirectional. 
        Professional cascade control diagram, blue color scheme --ar 3:2""",
    },
    {
        "id": "fig07-02",
        "chapter": 7,
        "section": "§7.1",
        "caption": "图 7-2: 瀑深枕梯级水力耦合传播示意",
        "prompt": """A cascade diagram showing hydraulic coupling propagation. 
        Top: Pubugou reservoir (large) with outflow Q_p. Arrow labeled 
        '90 min delay' to middle: Shenxigou reservoir (small) with 
        outflow Q_s. Arrow labeled '40 min delay' to bottom: 
        Zhentou reservoir (very small). Flow hydrographs on right 
        showing delayed response. Professional hydraulic diagram --ar 9:16""",
    },
    {
        "id": "fig07-03",
        "chapter": 7,
        "section": "§7.2",
        "caption": "图 7-3: 瀑深枕梯级 ODD 定义与水位域划分",
        "prompt": """Three parallel water level diagrams for three stations. 
        Each showing green (operable zone), yellow (high/dead zone), 
        red (violation zone). Shenxigou and Zhentou have narrower 
        operable zones than Pubugou. Arrows showing upstream constraint 
        propagation to downstream. Professional ODD diagram --ar 16:9""",
    },
    {
        "id": "fig07-04",
        "chapter": 7,
        "section": "§7.5",
        "caption": "图 7-4: 瀑深枕梯级多策略分级控制体系",
        "prompt": """A pyramid diagram showing three-level strategy hierarchy. 
        Top (green): Normal Strategy (economic priority). Middle (yellow): 
        Conservative Strategy (safety priority). Bottom (red): 
        Emergency Strategy (MRC + manual takeover). Trigger conditions 
        on right side. Hysteresis loop on left to prevent frequent 
        switching. Professional control strategy diagram --ar 4:3""",
    },
    
    # ========== 第八章 ==========
    {
        "id": "fig08-01",
        "chapter": 8,
        "section": "§8.2",
        "caption": "图 8-1: 胶东调水数字孪生"1+5"架构",
        "prompt": """A central hub with five surrounding modules diagram. 
        Center: Digital Twin Platform (Data Center, Model Platform, 
        Knowledge Platform, Warning Platform). Surrounding five 
        applications: Water Allocation, Channel Control, Pump Station 
        Management, Emergency Control, Reservoir Management. 
        Arrows showing data flow. Professional architecture diagram, 
        blue color scheme --ar 16:9""",
    },
    {
        "id": "fig08-02",
        "chapter": 8,
        "section": "§8.2",
        "caption": "图 8-2: 胶东调水 ODD 动态扩展与水位域演进",
        "prompt": """Three nested envelopes showing ODD evolution. 
        Inner (2023, 60% coverage): Initial ODD. Middle (2024, 85%): 
        Extended ODD. Outer (2025, 95%): Target ODD. Timeline on 
        right. Each zone with typical scenario examples. Professional 
        evolution diagram, blue gradient --ar 16:9""",
    },
    {
        "id": "fig08-03",
        "chapter": 8,
        "section": "§8.3",
        "caption": "图 8-3: 云边协同三态工作模式状态迁移",
        "prompt": """A triangular state diagram showing three cloud-edge 
        collaboration modes. Top (green): Cloud-Dominant Mode 
        (communication >80%). Right (yellow): Cloud-Edge Coordination 
        (50-80%). Left (red): Edge Autonomy (<50% or interrupted). 
        Transition conditions labeled on arrows. Professional 
        state machine diagram --ar 4:3""",
    },
    {
        "id": "fig08-04",
        "chapter": 8,
        "section": "§8.3",
        "caption": "图 8-4: 胶东调水物理 AI 引擎算法架构",
        "prompt": """A three-layer algorithm architecture diagram. 
        Bottom: Data Preprocessing (missing value filling, outlier 
        detection, normalization). Middle: Core Algorithms 
        (1D/2D hydrodynamic model, MPC, DE, POA). Top: Output 
        Applications (water level prediction, flow optimization, 
        gate scheduling). Performance specs on right. Professional 
        algorithm architecture --ar 3:2""",
    },
    {
        "id": "fig08-05",
        "chapter": 8,
        "section": "§8.4",
        "caption": "图 8-5: 胶东调水认知 AI 引擎与大模型应用",
        "prompt": """A central AI brain (DeepSeek 7B) with four surrounding 
        application modules: Natural Language QA, Plan Recommendation, 
        Decision Explanation, Report Generation. Bottom: Knowledge 
        Base (50000+ documents, 5000+ entities, 30-year history). 
        Top: Performance metrics (92% accuracy, <3s response). 
        Professional AI architecture diagram, purple color scheme --ar 16:9""",
    },
    {
        "id": "fig08-06",
        "chapter": 8,
        "section": "§8.5",
        "caption": "图 8-6: 胶东调水 WNAL 等级演进路线图 (2023-2030)",
        "prompt": """A horizontal timeline from 2023 to 2030 showing 
        WNAL evolution path. 2023 (L2), 2024 (L2+), 2025 (L3 pilot), 
        2026 (L3), 2028 (L3+), 2030 (L4 exploration). Each milestone 
        with key tasks and investment. Gradient color from light 
        blue to dark blue. Professional roadmap infographic --ar 16:9""",
    },
    
    # ========== 第九章 ==========
    {
        "id": "fig09-01",
        "chapter": 9,
        "section": "§9.2",
        "caption": "图 9-1: CHS 人才四类复合能力模型",
        "prompt": """A four-quadrant competency model diagram. 
        Quadrant 1: Hydraulic Mechanisms (water system physics). 
        Quadrant 2: Control & Optimization (MPC, algorithms). 
        Quadrant 3: Intelligent Software (AI, ML, coding). 
        Quadrant 4: Governance & Safety (policies, regulations). 
        Center intersection: CHS Professional. Professional 
        competency model diagram, four colors --ar 1:1""",
    },
    {
        "id": "fig09-02",
        "chapter": 9,
        "section": "§9.3",
        "caption": "图 9-2: 四支柱课程体系架构",
        "prompt": """Four pillar diagram supporting CHS education. 
        Pillar A: Modeling & Control (hydrodynamics, control theory). 
        Pillar B: AI & Data Science (ML, deep learning, statistics). 
        Pillar C: Systems Engineering (platform, deployment, operations). 
        Pillar D: Governance & Safety (policies, management, ethics). 
        Top beam: Integration & Practice. Professional education 
        framework diagram --ar 16:9""",
    },
    {
        "id": "fig09-03",
        "chapter": 9,
        "section": "§9.5",
        "caption": "图 9-3: CHS 学科建设十年路线图 (2026-2035)",
        "prompt": """A horizontal roadmap from 2026 to 2035 showing 
        CHS discipline development. Phase 1 (2026-2028): Foundation 
        (curriculum, platforms). Phase 2 (2029-2031): Expansion 
        (programs, partnerships). Phase 3 (2032-2035): Maturity 
        (degrees, international recognition). Each phase with 
        milestones. Professional strategic roadmap --ar 16:9""",
    },
]

def generate_figure(fig_data):
    """生成单张插图"""
    print(f"📝 生成 {fig_data['id']}: {fig_data['caption']}")
    
    try:
        # 调用 DALL-E 3 API
        response = client.images.generate(
            model="dall-e-3",
            prompt=fig_data['prompt'],
            size="1024x1024",
            quality="hd",
            n=1,
        )
        
        image_url = response.data[0].url
        
        # 下载图片
        image = Image.open(requests.get(image_url).stream)
        
        # 保存
        output_path = output_dir / f"{fig_data['id']}.png"
        image.save(output_path, "PNG", dpi=(300, 300))
        
        # 保存元数据
        metadata = {
            "id": fig_data['id'],
            "chapter": fig_data['chapter'],
            "section": fig_data['section'],
            "caption": fig_data['caption'],
            "prompt": fig_data['prompt'],
            "url": image_url,
            "generated_at": datetime.now().isoformat(),
            "file": str(output_path),
        }
        
        with open(output_dir / f"{fig_data['id']}.json", 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 完成：{output_path}")
        return True
        
    except Exception as e:
        print(f"❌ 失败：{e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("T1-CN《水系统控制论》书稿插图批量生成")
    print("=" * 60)
    print(f"📊 总计 {len(FIGURES)} 张插图")
    print(f"📁 输出目录：{output_dir.absolute()}")
    print("=" * 60)
    
    # 检查 API Key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ 错误：未设置 OPENAI_API_KEY 环境变量")
        print("请运行：export OPENAI_API_KEY='sk-...'")
        return
    
    # 批量生成
    success_count = 0
    for fig in FIGURES:
        if generate_figure(fig):
            success_count += 1
    
    # 统计
    print("\n" + "=" * 60)
    print(f"✅ 完成：{success_count}/{len(FIGURES)} 张")
    print(f"📊 成功率：{success_count/len(FIGURES)*100:.1f}%")
    print("=" * 60)
    
    # 生成索引文件
    index = {
        "total": len(FIGURES),
        "generated": success_count,
        "figures": [
            {
                "id": fig['id'],
                "chapter": fig['chapter'],
                "caption": fig['caption'],
                "file": f"{fig['id']}.png"
            }
            for fig in FIGURES
        ],
        "generated_at": datetime.now().isoformat(),
    }
    
    with open(output_dir / "index.json", 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    
    print(f"📄 索引文件：{output_dir / 'index.json'}")

if __name__ == "__main__":
    main()
