# T1-CN Mermaid 代码生成插图

> 使用方法：
> 1. 复制对应代码块到 mermaid.live 或 VS Code Mermaid 插件
> 2. 导出为 PNG（背景白色，宽度≥1800px）
> 3. 也可用 `mmdc` CLI 工具批量渲染：
>    `npx -p @mermaid-js/mermaid-cli mmdc -i input.mmd -o output.png -w 2400 -b white`

---

## 图 1-6: 章节依赖关系（DAG）

```mermaid
graph TD
    subgraph "第一部分：导论"
        ch01["第一章<br/>绪论"]
    end
    
    subgraph "第二部分：理论基础"
        ch02["第二章<br/>控制论视角"]
        ch03["第三章<br/>八原理概览"]
        ch04["第四章<br/>形式化描述"]
        ch05["第五章<br/>可控可观性"]
    end
    
    subgraph "第三部分：八原理与验证"
        ch06["第六章<br/>八原理详述"]
        ch07["第七章<br/>WNAL分级"]
        ch08["第八章<br/>安全与验证"]
    end
    
    subgraph "第四部分：系统架构"
        ch09["第九章<br/>MBD方法论"]
        ch10["第十章<br/>HydroOS"]
        ch11["第十一章<br/>物理AI与认知AI"]
    end
    
    subgraph "第五部分：工程实践"
        ch12["第十二章<br/>沙坪·点"]
        ch13["第十三章<br/>梯级·链"]
        ch14["第十四章<br/>胶东·网"]
    end
    
    ch01 --> ch02
    ch01 --> ch03
    ch03 --> ch04
    ch04 --> ch05
    ch03 --> ch06
    ch06 --> ch07
    ch06 --> ch08
    ch06 --> ch09
    ch09 --> ch10
    ch10 --> ch11
    ch11 -.-> ch12
    ch12 --> ch13
    ch13 --> ch14

    style ch01 fill:#1565C0,color:#fff,stroke:#0D47A1,stroke-width:3px
    style ch03 fill:#1565C0,color:#fff
    style ch06 fill:#1565C0,color:#fff
    style ch10 fill:#1565C0,color:#fff
```

---

## 图 2-1: 水系统状态—输入—输出—扰动框图

```mermaid
graph LR
    subgraph " "
        direction LR
        U["u_k<br/>闸门/泵站控制<br/>Control Input"] -->|"输入"| SYS["水利系统<br/>f(·)<br/>Hydro System"]
        D["d_k<br/>降雨/取水扰动<br/>Disturbance"] -->|"扰动"| SYS
        THETA["θ_k<br/>慢变参数<br/>Parameters"] -.->|"参数"| SYS
        SYS -->|"输出"| Y["y_k<br/>水位/流量<br/>Observation"]
        Y --> NOISE(("+ v_k<br/>噪声"))
        NOISE --> OBS["观测值"]
        OBS -->|"状态反馈"| CTRL["控制器<br/>Controller"]
        CTRL -->|"控制量"| U
    end

    style SYS fill:#1565C0,color:#fff,stroke:#0D47A1,stroke-width:2px
    style CTRL fill:#4CAF50,color:#fff
    style D fill:#FF7043,color:#fff
    style THETA fill:#E0E0E0,color:#212121
```

---

## 图 2-4: 异常工况四态机状态迁移图

```mermaid
stateDiagram-v2
    [*] --> Normal
    
    Normal: 正常态 Normal<br/>策略：性能优化<br/>人机：自动运行
    Restricted: 受限态 Restricted<br/>策略：保守策略<br/>人机：加强监督
    Degraded: 降级态 Degraded<br/>策略：固定流量带<br/>人机：请求接管
    Takeover: 接管态 Takeover<br/>策略：人工控制<br/>人机：人工主导
    
    Normal --> Restricted: 预测可信度下降<br/>通信质量变差
    Restricted --> Degraded: 关键状态逼近黄区<br/>多传感器离线
    Degraded --> Takeover: 红区触及<br/>执行器故障<br/>人工主动接管
    
    Takeover --> Degraded: 故障排除<br/>人工确认
    Degraded --> Restricted: 状态回归绿区
    Restricted --> Normal: 可信度恢复<br/>通信恢复
```

---

## 图 3-2: MBD 四层一闭环架构

```mermaid
graph TB
    subgraph "ODD定义层 ODD Definition"
        ODD["运行设计域六维参数<br/>水文/设备/通信/环境/负载/时间<br/>↔ P4安全包络"]
    end
    
    subgraph "模型决策层 Model & Decision"
        MOD["四类模型协同<br/>PBM | SM | OSEM | 数据模型<br/>+ MPC决策引擎<br/>↔ P1传递函数化"]
    end
    
    subgraph "在环验证层 xIL Verification"
        VER["MIL → SIL → HIL<br/>五元组证据链<br/>↔ P5在环验证"]
    end
    
    subgraph "现场执行层 Field Execution"
        EXE["SCADA + PLC + 执行器<br/>↔ P2可控可观性"]
    end
    
    ODD -->|"目标与约束 ↓"| MOD
    MOD -->|"模型与策略 ↓"| VER
    VER -->|"验证通过 ↓"| EXE
    EXE -.->|"数据回馈 ↑<br/>持续进化闭环"| ODD
    
    MOD -->|"状态反馈 ↑"| ODD
    VER -->|"验证报告 ↑"| MOD

    style ODD fill:#E3F2FD,stroke:#1565C0,stroke-width:2px
    style MOD fill:#1565C0,color:#fff
    style VER fill:#4CAF50,color:#fff
    style EXE fill:#757575,color:#fff
```

---

## 图 7-2: WNAL 等级跃迁四重门槛

```mermaid
graph LR
    START["L_k<br/>当前等级"] --> GATE{"四重门槛<br/>全部通过?"}
    
    GATE -->|"✓全部通过"| END["L_k+1<br/>升级等级"]
    GATE -->|"✗任一未通过"| FAIL["不得升级<br/>补强短板"]
    
    subgraph "门槛一：技术门槛 Technical"
        T1["模型精度<15%误差<br/>传感器覆盖≥90%<br/>算法性能达标<br/>计算平台实时"]
    end
    
    subgraph "门槛二：验证门槛 Verification"
        T2["MIL/SIL/HIL通过<br/>场景覆盖率达标<br/>极端场景专项测试"]
    end
    
    subgraph "门槛三：治理门槛 Governance"
        T3["SOP完备<br/>责任矩阵明确<br/>应急预案演练<br/>监管审批"]
    end
    
    subgraph "门槛四：运行门槛 Operational"
        T4["试运行时间达标<br/>KPI持续达标<br/>零安全事件记录"]
    end
    
    T1 --> GATE
    T2 --> GATE
    T3 --> GATE
    T4 --> GATE

    style START fill:#42A5F5,color:#fff
    style END fill:#1565C0,color:#fff
    style FAIL fill:#E53935,color:#fff
    style GATE fill:#FFB300,color:#212121
    style T1 fill:#E3F2FD,stroke:#1565C0
    style T2 fill:#E8F5E9,stroke:#4CAF50
    style T3 fill:#FFF3E0,stroke:#FF7043
    style T4 fill:#F3E5F5,stroke:#7B1FA2
```

---

## 图 9-2: MBD "四层一闭环"总体框架（详细版）

```mermaid
graph TB
    subgraph "ODD定义层"
        ODD_H["水文维<br/>Hydrology"]
        ODD_E["设备维<br/>Equipment"]
        ODD_C["通信维<br/>Comm."]
        ODD_V["环境维<br/>Environ."]
        ODD_L["负载维<br/>Load"]
        ODD_T["时间维<br/>Time"]
        ZONE["三区阈值<br/>红/黄/绿"]
    end
    
    subgraph "模型决策层"
        PBM["PBM<br/>物理模型"]
        SM["SM<br/>简化模型"]
        OSEM["OSEM<br/>观测模型"]
        DATA["数据<br/>增强模型"]
        MPC["MPC决策引擎"]
        PBM --> MPC
        SM --> MPC
        OSEM --> MPC
        DATA --> MPC
    end
    
    subgraph "在环验证层"
        MIL["MIL<br/>模型在环"]
        SIL["SIL<br/>软件在环"]
        HIL["HIL<br/>硬件在环"]
        EVID["五元组证据链"]
        MIL --> SIL --> HIL
        HIL --> EVID
    end
    
    subgraph "现场执行层"
        SCADA["SCADA<br/>数据采集"]
        PLC["PLC<br/>控制执行"]
        ACT["执行器<br/>闸门/泵站"]
        SCADA --> PLC --> ACT
    end
    
    ZONE --> MPC
    MPC --> MIL
    EVID -->|"验证通过"| PLC
    ACT -.->|"数据回馈<br/>持续进化闭环"| ODD_H

    style MPC fill:#1565C0,color:#fff
    style ZONE fill:#E53935,color:#fff
    style EVID fill:#4CAF50,color:#fff
```

---

## 图 10-2: 策略门禁四项检查流程

```mermaid
graph LR
    IN["PAI/CAI<br/>候选策略"] --> C1{"检查一<br/>安全包络<br/>合规性"}
    
    C1 -->|"通过"| C2{"检查二<br/>操作约束<br/>合规性"}
    C1 -->|"不通过"| R1["拒绝<br/>附原因"]
    
    C2 -->|"通过"| C3{"检查三<br/>权限<br/>合规性"}
    C2 -->|"不通过"| R2["拒绝"]
    
    C3 -->|"通过"| C4{"检查四<br/>一致性<br/>检查"}
    C3 -->|"不通过"| R3["拒绝"]
    
    C4 -->|"通过"| OUT["策略放行<br/>→DAL执行"]
    C4 -->|"冲突"| COORD["协调<br/>解冲突"]
    COORD --> C4

    style IN fill:#42A5F5,color:#fff
    style C1 fill:#E53935,color:#fff
    style C2 fill:#FF7043,color:#fff
    style C3 fill:#FFC107,color:#212121
    style C4 fill:#4CAF50,color:#fff
    style OUT fill:#1565C0,color:#fff
    style R1 fill:#FFCDD2
    style R2 fill:#FFCDD2
    style R3 fill:#FFCDD2
```

---

## 图 10-3: HydroOS 四态机状态转换图

```mermaid
stateDiagram-v2
    [*] --> Normal
    
    Normal: 正常态<br/>PAI全功能运行<br/>自主控制模式
    Degraded: 降级态<br/>PAI降级运行，CAI离线<br/>保守控制模式
    Emergency: 应急态<br/>仅DAL基础保护<br/>最小风险模式
    Maintenance: 检修态<br/>人工完全接管<br/>维护模式
    
    Normal --> Degraded: 传感器部分离线<br/>模型预测偏差增大
    Degraded --> Emergency: 关键设备故障<br/>安全包络红区触发
    Emergency --> Maintenance: 系统稳定后转入维护
    Maintenance --> Normal: 维护完成+系统自检通过
    Degraded --> Normal: 故障恢复+状态验证通过
    Normal --> Maintenance: 计划维护窗口
```

---

## 图 12-3: 沙坪 MPC 滚动优化控制流程

```mermaid
graph TD
    A["数据采集<br/>SCADA采集水位/流量/出力<br/>（5分钟周期）"] --> B["状态估计<br/>OSEM更新库容/入库流量/机组特性"]
    B --> C["来流预测<br/>基于枕头坝出库+时延模型<br/>预测未来80分钟入库序列"]
    C --> D{"ODD检查<br/>六维参数<br/>在ODD内？"}
    
    D -->|"是"| E["MPC优化<br/>80分钟滚动窗口<br/>16步控制序列<br/>目标：水位稳定+最小闸门动作"]
    D -->|"否"| F["切换保守模式<br/>或请求接管"]
    
    E --> G{"安全包络检查<br/>预测轨迹<br/>在绿/黄区内？"}
    G -->|"是"| H["执行<br/>下发首步控制指令<br/>闸门/机组调整"]
    G -->|"否"| I["修正约束<br/>切换保守策略"]
    I --> E
    
    H -->|"等待5分钟<br/>滚动重复"| A

    style A fill:#757575,color:#fff
    style B fill:#90CAF9,color:#212121
    style C fill:#42A5F5,color:#fff
    style E fill:#1565C0,color:#fff
    style H fill:#4CAF50,color:#fff
    style D fill:#FFC107,color:#212121
    style G fill:#E53935,color:#fff
    style F fill:#FF7043,color:#fff
```

---

## 图 13-2: 梯级 EDC 两级架构

```mermaid
graph TB
    subgraph "电网 Power Grid"
        GRID["四川500kV电网<br/>AGC总出力指令 P_cmd"]
    end
    
    subgraph "集控层 Centralized Control"
        AGC_IF["AGC接口<br/>接收电网指令"]
        OPT["站间负荷分配优化<br/>BDPSA算法（<1秒）"]
        MODE["策略模式选择器"]
        M1["水位平稳"]
        M2["最大蓄能"]
        M3["少调负荷"]
        M4["深枕平衡"]
        M5["枕站平衡"]
        AGC_IF --> OPT
        OPT --> MODE
        MODE --- M1
        MODE --- M2
        MODE --- M3
        MODE --- M4
        MODE --- M5
    end
    
    subgraph "厂控层 Plant Control"
        PU["瀑布沟厂控<br/>3600MW<br/>机组负荷优化"]
        SH["深溪沟厂控<br/>660MW<br/>水位优先控制"]
        ZH["枕头坝厂控<br/>760MW<br/>与沙坪预调通讯"]
    end
    
    GRID -->|"AGC指令"| AGC_IF
    MODE -->|"P_瀑"| PU
    MODE -->|"P_深"| SH
    MODE -->|"P_枕"| ZH
    PU -.->|"实发出力+水位反馈"| OPT
    SH -.->|"实发出力+水位反馈"| OPT
    ZH -.->|"实发出力+水位反馈"| OPT

    style GRID fill:#E53935,color:#fff
    style OPT fill:#1565C0,color:#fff
    style MODE fill:#FFB300,color:#212121
    style PU fill:#42A5F5,color:#fff
    style SH fill:#42A5F5,color:#fff
    style ZH fill:#42A5F5,color:#fff
```
