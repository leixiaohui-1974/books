<!-- 变更日志
v1 2026-02-19: 初稿
-->

# 第六章 认知AI引擎设计与实现

---

## 学习目标

完成本章后，读者应能够：

1. 阐述认知AI引擎在CHS框架中的定位与角色，理解其与物理AI引擎的分工与协作关系；
2. 设计认知AI引擎的模块化架构，明确感知层、认知层、决策层和交互层的职责边界与数据流；
3. 定义认知AI引擎的核心API接口，使其能够与HydroOS、SCADA系统和物理AI引擎无缝集成；
4. 设计多轮推理与任务编排机制，使认知AI引擎能够处理复杂的组合式调度决策任务；
5. 建立认知AI引擎的安全治理框架，包括输出审核、权限管理和审计追溯机制。

---

## 认知AI引擎的定位

### 6.1.1 CHS双引擎架构回顾

水系统控制论（CHS）框架将水网智能控制系统划分为两大核心引擎（参见T1-CN第五章、T2b第九章）：

**物理AI引擎（Physical AI Engine）**：负责"算"——基于水力学模型、降阶模型（ROM）和模型预测控制（MPC）进行数值计算和优化求解。它的输入是结构化的状态数据（水位、流量、闸位），输出是数值化的控制指令（闸门开度、泵站功率）。物理AI引擎是水网自主控制的"计算核心"。

**认知AI引擎（Cognitive AI Engine）**：负责"懂"——基于知识图谱、大语言模型和RAG技术处理非结构化信息，进行语义理解、知识推理和自然语言交互。它的输入包括文本查询、规程文档、语音指令和多模态信息，输出包括调度建议、规程解读、风险评估和自然语言解释。认知AI引擎是水网自主控制的"认知核心"。

两者的关系可以用一个类比来说明：物理AI引擎像是一位精通数学的计算工程师，能快速准确地解出最优化问题；认知AI引擎像是一位经验丰富的总工程师，能理解工程背景、阅读规程文件、综合判断各种非量化因素并向调度员解释方案依据。两者缺一不可，协同才能实现完整的自主调度能力。

### 6.1.2 认知AI引擎的四大核心能力

结合前三章的技术组件，认知AI引擎应具备以下四大核心能力：

**能力一：知识管理**（对应第三章）

维护水利领域的结构化知识体系——知识图谱的构建、更新和查询。包括工程拓扑关系、设备参数、规程条款、历史事件等结构化知识的存储与推理。

**能力二：语义理解**（对应第四章）

理解自然语言输入的含义——术语识别、意图判断、上下文理解。这是认知AI引擎与人类用户之间的语义桥梁。

**能力三：知识检索与融合**（对应第五章）

从多源异构知识库中检索相关信息，并将其融合为连贯的决策上下文——RAG的完整流水线。

**能力四：推理与决策辅助**（本章重点）

在前三种能力基础上，进行多步推理、方案生成、风险评估和方案解释。这是认知AI引擎最高层次的能力，也是将"零件"组装为"整机"的关键环节。

### 6.1.3 与HydroOS的集成关系

认知AI引擎是HydroOS（水网操作系统）的核心子系统之一。在HydroOS的三层架构中：

**表6-1 认知AI引擎在HydroOS各层级中的角色**

| HydroOS层级 | 功能 | 认知AI引擎的角色 |
|-------------|------|-----------------|
| 设备抽象层（HAL） | SCADA数据采集与设备控制 | 消费者：接收实时数据 |
| 调度引擎层 | 优化计算与控制决策 | 协作者：与物理AI引擎协同 |
| 应用服务层 | 用户交互与业务应用 | 提供者：提供NL接口和知识服务 |

认知AI引擎通过标准化API与HydroOS的其他组件通信，既不直接操控物理设备（安全隔离），也不替代物理AI引擎的数值计算（能力分工），而是作为"认知中间件"连接人类用户与自动化系统。

---

## 模块化架构设计

认知AI引擎采用四层模块化架构，自底向上为：感知层、认知层、决策层和交互层。

### 6.2.1 架构总览

```
┌─────────────────────────────────────────────────────┐
│                    交互层 (Interaction)               │
│  自然语言对话 │ 语音交互 │ 报告生成 │ 告警解释       │
├─────────────────────────────────────────────────────┤
│                    决策层 (Decision)                  │
│  任务编排 │ 多步推理 │ 方案评估 │ 风险分析 │ 工具调用 │
├─────────────────────────────────────────────────────┤
│                    认知层 (Cognition)                 │

**图6-1 认知AI引擎五层架构**

│  LLM推理 │ RAG检索 │ 知识图谱查询 │ 实体识别 │ 意图分类│
├─────────────────────────────────────────────────────┤
│                    感知层 (Perception)                │
│  SCADA数据接入 │ 文档解析 │ 语音识别 │ 图像理解       │
├─────────────────────────────────────────────────────┤
│              外部系统接口 (External Interfaces)       │
│  HydroOS API │ SCADA │ 物理AI引擎 │ 数据库          │
└─────────────────────────────────────────────────────┘
```

### 6.2.2 感知层

感知层负责将外部世界的多源信息转化为认知AI引擎可以处理的统一表示。

**SCADA数据接入模块**

从HydroOS的设备抽象层获取实时运行数据，转化为结构化的状态描述：

```json
{
  "timestamp": "2025-06-15T08:15:00+08:00",
  "source": "SCADA",
  "data": {
    "gate_3": {
      "upstream_level": 42.35,
      "downstream_level": 41.82,
      "opening": 1.2,
      "flow_rate": 28.5,
      "status": "normal"
    },
    "alerts": [
      {"id": "ALT-20250615-001", "type": "level_warning", "device": "WL-003", "value": 42.85, "threshold": 42.50}
    ]
  }
}
```

**文档解析模块**

对新入库的文档进行解析和预处理，输出标准化文本并触发索引更新（参见第五章分块策略）。支持的格式包括PDF、Word、HTML和扫描图片（OCR）。

**语音识别模块**

将调度员的语音指令转化为文本。在调度中心的嘈杂环境中，推荐使用Whisper或FunASR等开源语音识别模型，并针对水利术语进行热词优化。

**图像理解模块**（前瞻性设计）

识别SCADA界面截图、工程照片和监控画面中的信息。当前主要依赖视觉语言模型（VLM）的能力，成熟度有限，建议作为可选模块。

### 6.2.3 认知层

认知层是引擎的核心计算层，集成了前三章的所有技术组件。

**LLM推理模块**

封装第四章训练的领域大语言模型，提供统一的文本生成接口：

```python
class LLMModule:
    def generate(self, prompt: str, max_tokens: int = 2048, 
                 temperature: float = 0.1) -> str:
        """基础文本生成"""
        
    def chat(self, messages: List[Message], 
             system_prompt: str = None) -> str:
        """多轮对话生成"""
        
    def structured_output(self, prompt: str, 
                          schema: dict) -> dict:
        """结构化输出（JSON格式约束）"""
```

温度参数的选择对输出质量有重要影响：

| 任务类型 | 推荐温度 | 理由 |
|---------|---------|------|
| 事实查询 | 0.0-0.1 | 需要确定性、一致性的回答 |
| 方案建议 | 0.3-0.5 | 需要一定创造性但不能偏离事实 |
| 报告生成 | 0.3-0.7 | 语言多样性较重要 |
| 风险分析 | 0.1-0.2 | 需要严谨、保守的分析 |

**RAG检索模块**

封装第五章的完整检索流水线，提供统一检索接口：

```python
class RAGModule:
    def retrieve(self, query: str, top_k: int = 5,
                 filters: dict = None) -> List[Document]:
        """混合检索（语义+BM25+知识图谱）"""
        
    def retrieve_and_generate(self, query: str, 
                               system_prompt: str = None) -> RAGResponse:
        """端到端RAG：检索+生成+引用"""
```

**知识图谱模块**

封装第三章的知识图谱，提供结构化查询接口：

```python
class KGModule:
    def query(self, cypher: str) -> List[dict]:
        """执行Cypher查询"""
    
    def entity_lookup(self, entity_name: str) -> EntityInfo:
        """实体属性查询"""
    
    def path_query(self, start: str, end: str, 
                   max_hops: int = 3) -> List[Path]:
        """关系链查询"""
    
    def impact_analysis(self, entity: str, 
                        event_type: str) -> ImpactReport:
        """影响范围分析"""
```

**实体识别与意图分类模块**

对用户输入进行浅层语义分析：

```python
class NLUModule:
    def classify_intent(self, text: str) -> Intent:
        """意图分类：regulation_query/equipment_status/
           situation_analysis/case_search/knowledge_qa/
           computation_request/report_generation"""
    
    def extract_entities(self, text: str) -> List[Entity]:
        """实体提取：设备名称/地点/工况类型/时间/数值"""
    
    def resolve_coreference(self, text: str, 
                             context: List[str]) -> str:
        """指代消解：基于对话历史解析代词指代"""
```

### 6.2.4 决策层

决策层在认知层之上，负责复杂任务的编排、多步推理和方案评估。这是认知AI引擎区别于简单问答系统的核心层。

**任务编排引擎（Task Orchestrator）**

对于复杂查询，任务编排引擎将其分解为多个子任务，协调各认知模块按正确顺序执行。编排逻辑采用有向无环图（DAG）表示：

```
用户查询："3号闸门水位异常，分析原因并给出处置方案"

任务分解DAG：
T1: 实体识别("3号闸门") → 设备ID
T2: SCADA查询(设备ID) → 当前状态数据  [依赖T1]
T3: 知识图谱查询(设备ID, "上下游关系") → 关联设备  [依赖T1]
T4: RAG检索("水位异常原因诊断") → 诊断知识  [并行]
T5: RAG检索("3号闸门历史故障") → 历史案例  [并行]
T6: LLM推理(T2+T3+T4+T5) → 原因分析  [依赖T2-T5]
T7: RAG检索("水位异常处置规程") → 处置规程  [并行]
T8: LLM推理(T6+T7) → 处置方案  [依赖T6+T7]
T9: 安全检查(T8) → 合规确认  [依赖T8]
T10: 回答组装(T6+T8+T9) → 最终回答  [依赖T6+T8+T9]
```

任务编排引擎的设计要点：

1. **并行执行**：无依赖关系的子任务并行执行，减少总延迟
2. **失败处理**：某个子任务失败时，提供降级方案（如知识图谱不可用时，退化为纯RAG）
3. **超时控制**：每个子任务设置超时上限，防止单个模块阻塞整个流水线
4. **中间结果缓存**：相同的子任务结果可以在会话内缓存复用

**多步推理引擎（Multi-Step Reasoning）**

对于需要链式推理的问题，采用ReAct（Reasoning + Acting）范式：

```
思考(Thought): 用户问3号闸门水位异常的原因。我需要先了解当前的水位数据和正常范围。
行动(Action): 调用SCADA查询3号闸门当前水位 → 42.85m
观察(Observation): 当前水位42.85m，超过警戒值42.50m达0.35m。

思考: 水位超高可能的原因包括上游来水增加、下游阻塞、闸门故障等。
      我需要检查上游来水数据和闸门状态。
行动: 调用SCADA查询上游来水流量 → 35.2 m³/s（设计流量30 m³/s的117%）
行动: 调用知识图谱查询下游设备状态 → 4号闸门正在检修(全关)
观察: 上游来水超过设计值17%，同时下游4号闸门检修关闭。

思考: 两个因素叠加——上游来水偏大且下游通道受限，这是水位异常的主因。
      需要检索处置方案。
行动: 调用RAG检索"上游来水偏大+下游闸门检修 处置方案"
观察: 规程第5.3.2条规定此类工况应启动旁路退水...

最终回答: 3号闸门水位异常（42.85m，超警戒0.35m）的原因分析如下...
```

ReAct范式的关键优势在于推理过程的**可解释性**——每一步的思考和行动都被记录，调度员可以审查推理链的每个环节，判断结论是否可靠。

**方案评估模块**

当认知AI引擎生成调度建议时，需要对方案进行多维评估：

| 评估维度 | 评估方法 | 信息来源 |
|---------|---------|---------|
| 安全合规性 | 规则检查+规程比对 | 知识图谱+RAG |
| 物理可行性 | 调用物理AI引擎验证 | MPC/ROM仿真 |
| 历史可参考性 | 历史案例相似度匹配 | RAG检索 |
| 操作复杂度 | 步骤数和协调需求评估 | LLM评估 |
| 风险等级 | 基于ODD和Safety Envelope判断 | 知识图谱规则 |

**工具调用框架（Tool Calling）**

认知AI引擎通过工具调用框架与外部系统交互。采用类似OpenAI Function Calling的机制，LLM在需要外部信息或执行操作时，生成结构化的工具调用请求：

```json
{
  "tool": "scada_query",
  "parameters": {
    "device_id": "gate_3",
    "metrics": ["upstream_level", "downstream_level", "opening"],
    "time_range": "current"
  }
}
```

引擎的工具注册表：

| 工具名称 | 功能 | 权限等级 |
|---------|------|---------|
| scada_query | 查询SCADA实时/历史数据 | 只读 |
| kg_query | 查询知识图谱 | 只读 |
| rag_search | RAG检索 | 只读 |
| physical_ai_simulate | 调用物理AI引擎进行仿真 | 只读 |
| alert_send | 发送告警通知 | 需审批 |
| report_generate | 生成调度报告 | 只读 |
| schedule_suggest | 提交调度建议（需人工确认） | 需审批 |

[安全原则] 认知AI引擎**永远不直接执行控制操作**（如改变闸门开度）。所有控制类操作必须通过物理AI引擎，并经人工确认后才能执行。认知AI引擎的权限严格限制为"只读+建议"，这是安全治理的底线。

### 6.2.5 交互层

交互层负责与最终用户的界面交互。

**自然语言对话接口**

支持文本和语音两种输入模式的多轮对话。对话管理需要维护以下状态：

```python
class ConversationState:
    session_id: str
    user_id: str
    user_role: str          # dispatcher/engineer/manager
    history: List[Message]  # 对话历史
    context: dict           # 当前工况上下文
    active_task: Task       # 当前正在处理的任务
    permissions: Set[str]   # 用户权限集
```

**报告生成接口**

根据运行数据和分析结果，自动生成结构化的调度报告。报告模板包括：日报、周报、月度调度总结、应急事件报告等。

**告警解释接口**

当SCADA系统发出告警时，认知AI引擎自动生成告警的上下文解释：

```
[原始告警] ALT-20250615-001: WL-003水位42.85m超过警戒值42.50m

[认知AI引擎增强解释]
■ 告警设备：3号节制闸上游水位计WL-003
■ 当前值：42.85m（超警戒0.35m，超警戒率7.8%）
■ 变化趋势：过去1小时水位上升0.42m，上升速率偏快
■ 可能原因：上游来水流量35.2m³/s（设计流量117%），
            下游4号闸门检修关闭导致过流能力受限
■ 建议操作：开启退水闸-3至0.5m泄水（规程第5.3.2条）
■ 紧急程度：橙色（需在30分钟内处置）
```

这种告警增强是认知AI引擎最直接的价值体现之一——将一条简短的数值告警转化为调度员可以立即理解和行动的完整决策支持信息。

---

## 核心API设计

认知AI引擎通过RESTful API和WebSocket两种方式对外提供服务。

### 6.3.1 RESTful API

**对话接口**

```
POST /api/v1/chat
Request:
{
  "session_id": "sess_20250615_001",
  "message": "3号闸门水位异常，帮我分析原因",
  "context": {
    "current_condition": "normal_operation",
    "season": "summer"
  }
}

Response:
{
  "session_id": "sess_20250615_001",
  "reply": "3号节制闸水位异常（42.85m，超警戒0.35m）的原因分析如下...",
  "sources": [
    {"type": "scada", "device": "WL-003", "timestamp": "2025-06-15T08:15:00"},
    {"type": "regulation", "clause": "5.3.2", "document": "调度规程v2025"},
    {"type": "knowledge_graph", "entity": "gate_3", "relation": "downstream_of"}
  ],
  "confidence": 0.87,
  "safety_check": "passed",
  "reasoning_trace": ["思考步骤1...", "思考步骤2...", "..."]
}
```

**知识查询接口**

```
POST /api/v1/knowledge/query
Request:
{
  "query": "冰期调度的特殊要求有哪些？",
  "search_mode": "hybrid",
  "top_k": 5
}
```

**告警增强接口**

```
POST /api/v1/alert/enhance
Request:
{
  "alert_id": "ALT-20250615-001",
  "alert_type": "level_warning",
  "device_id": "WL-003",
  "value": 42.85,
  "threshold": 42.50
}
```

**调度建议接口**

```
POST /api/v1/schedule/suggest
Request:
{
  "scenario": "上游来水增加30%，当前冰期，4号闸门检修",
  "constraints": ["safety_envelope", "ice_period_rules"],
  "objective": "维持输水安全的前提下最大化输水量"
}

Response:
{
  "suggestions": [
    {
      "priority": 1,
      "action": "开启退水闸-3至0.5m",
      "rationale": "根据规程第5.3.2条，下游通道受限时应启动旁路退水",
      "risk_level": "low",
      "requires_confirmation": true
    },
    {
      "priority": 2,
      "action": "降低上游引水闸开度至0.8m",
      "rationale": "控制入流量，配合退水闸降低干渠水位",
      "risk_level": "medium",
      "requires_confirmation": true
    }
  ],
  "simulation_result": {
    "predicted_level_after_1h": 42.15,
    "below_warning": true,
    "source": "physical_ai_engine_simulation"
  }
}
```

### 6.3.2 WebSocket接口（实时流式）

对于需要流式输出的场景（如长回答的逐步生成、实时推理过程展示），使用WebSocket：

```
ws://engine:8080/ws/chat

Client → Server: {"type": "message", "text": "分析当前工况并给出建议"}
Server → Client: {"type": "thinking", "text": "正在查询SCADA数据..."}
Server → Client: {"type": "thinking", "text": "正在检索相关规程..."}
Server → Client: {"type": "stream", "text": "根据当前工况分析，"}
Server → Client: {"type": "stream", "text": "3号闸门水位偏高的原因..."}
Server → Client: {"type": "sources", "data": [...]}
Server → Client: {"type": "done"}
```

流式输出对用户体验至关重要——调度员可以在回答生成过程中就开始阅读，而不需要等待全部生成完毕。同时，"正在查询SCADA数据""正在检索规程"等中间状态的展示增强了用户对系统的信任感。

### 6.3.3 与物理AI引擎的接口

认知AI引擎与物理AI引擎之间的通信接口：

**请求仿真**

```
POST /api/v1/physical_ai/simulate
Request:
{
  "scenario": {
    "gate_3_opening": 1.2,
    "gate_4_opening": 0.0,  // 检修关闭
    "inlet_flow": 35.2,
    "spillway_3_opening": 0.5  // 建议操作
  },
  "predict_horizon": 3600,  // 预测1小时
  "metrics": ["level_at_gate_3", "level_at_gate_4", "total_flow"]
}

Response:
{
  "predictions": {
    "level_at_gate_3": {"t_0": 42.85, "t_3600": 42.15, "trend": "decreasing"},
    "level_at_gate_4": {"t_0": 41.20, "t_3600": 41.35, "trend": "stable"},
    "total_flow": {"t_0": 28.5, "t_3600": 26.8}
  },
  "safety_check": {
    "within_envelope": true,
    "closest_boundary": "gate_3_max_level: 43.00m (margin: 0.85m)"
  }
}
```

这个接口实现了认知AI引擎与物理AI引擎的关键协作：认知AI引擎根据规程和推理生成调度方案→调用物理AI引擎进行仿真验证→将验证结果反馈给调度员。

---

## 任务编排与工作流

### 6.4.1 预定义工作流

对于高频的标准化任务，预定义工作流可以保证处理的一致性和可靠性：

**工作流一：告警响应**

```yaml
workflow: alert_response
trigger: new_alert
steps:
  - name: contextualize
    module: scada_query
    action: 获取告警设备的当前状态和近期趋势
    
  - name: diagnose
    module: kg_query + rag_search
    action: 查询设备关联关系 + 检索故障诊断知识
    
  - name: assess_impact
    module: kg_query
    action: 分析告警可能影响的上下游设施范围
    
  - name: retrieve_protocol
    module: rag_search
    action: 检索适用的处置规程条款
    
  - name: generate_response
    module: llm
    action: 综合以上信息生成告警增强报告
    
  - name: safety_check
    module: safety_validator
    action: 检查建议操作是否符合安全约束
    
  - name: output
    action: 输出增强告警信息到调度员界面
```

**工作流二：调度日报生成**

```yaml
workflow: daily_report
trigger: scheduled(time="08:00")
steps:
  - name: collect_data
    module: scada_query
    action: 获取过去24小时的运行数据摘要
    
  - name: identify_events
    module: llm
    action: 从运行数据中识别关键事件
    
  - name: retrieve_context
    module: rag_search
    action: 为每个关键事件检索相关背景信息
    
  - name: analyze_performance
    module: llm
    action: 分析各项运行指标的达标情况
    
  - name: generate_report
    module: llm
    action: 生成日报初稿（含数据表格、事件摘要、建议）
    
  - name: format_output
    action: 格式化为标准日报模板并存档
```

**工作流三：工况变化评估**

```yaml
workflow: condition_change_assessment
trigger: manual_or_auto("工况参数发生显著变化")
steps:
  - name: detect_change
    module: scada_query
    action: 确认工况变化的具体参数和幅度
    
  - name: check_odd
    module: kg_query
    action: 判断变化后的工况是否仍在运行设计域(ODD)内
    
  - name: simulate_impact
    module: physical_ai
    action: 仿真预测工况变化对系统的影响
    
  - name: retrieve_guidance
    module: rag_search
    action: 检索相关工况的调度策略指导
    
  - name: generate_assessment
    module: llm
    action: 生成工况评估报告和调度建议
    
  - name: escalate_if_needed
    condition: "out_of_ODD == true"
    action: 触发告警并建议启动应急预案
```

### 6.4.2 动态任务编排

预定义工作流无法覆盖所有情况。对于非标准化的复杂查询，采用LLM驱动的动态任务编排——让LLM自主决定调用哪些工具、以什么顺序执行。

这需要在LLM的系统提示中描述可用工具及其功能：

```
你是水利工程认知AI引擎的决策模块。你可以使用以下工具：

1. scada_query(device_id, metrics, time_range): 查询SCADA实时或历史数据
2. kg_query(cypher): 执行知识图谱Cypher查询
3. rag_search(query, filters): 从知识库中检索相关文档
4. physical_ai_simulate(scenario, horizon): 调用物理AI引擎进行仿真
5. calculator(expression): 执行数值计算

当需要使用工具时，输出以下格式：
<tool_call>{"tool": "工具名", "parameters": {...}}</tool_call>

使用工具前先思考为什么需要调用它，使用后根据结果决定下一步行动。
```

动态编排的优势在于灵活性——它可以处理预定义工作流未覆盖的新型查询。但灵活性也带来了风险：LLM可能生成无效的工具调用、陷入无限循环、或遗漏关键步骤。因此需要以下安全护栏：

- **最大工具调用次数限制**：单次查询不超过10次工具调用
- **超时限制**：单次查询总处理时间不超过60秒
- **工具调用审计**：记录每次工具调用的输入、输出和耗时
- **回退机制**：动态编排失败时，退化为预定义工作流或直接RAG

### 6.4.3 Agent框架选型

实现任务编排的技术框架选型：

| 框架 | 特点 | 适用场景 | 推荐度 |
|------|------|---------|--------|
| LangChain | 生态最丰富、组件最全 | 快速原型开发 | ★★★★☆ |
| LlamaIndex | RAG能力最强 | RAG为核心的系统 | ★★★★☆ |
| AutoGen | 多Agent协作 | 复杂多步推理 | ★★★☆☆ |
| 自研框架 | 完全可控、轻量 | 生产环境 | ★★★★★ |

[工程建议] 对于生产级的认知AI引擎，**推荐在原型阶段使用LangChain/LlamaIndex快速验证，然后在生产阶段迁移到自研轻量框架**。自研框架的优势在于：（1）去除不需要的抽象层，降低延迟；（2）完全掌控工具调用的安全策略；（3）便于与HydroOS的其他组件深度集成。

自研框架的核心组件仅需约2000-3000行Python代码：

```
cognitive_engine/
├── core/
│   ├── orchestrator.py      # 任务编排器
│   ├── tool_registry.py     # 工具注册表
│   ├── safety_guard.py      # 安全护栏
│   └── session_manager.py   # 会话管理
├── modules/
│   ├── llm_module.py        # LLM封装
│   ├── rag_module.py        # RAG封装
│   ├── kg_module.py         # 知识图谱封装
│   └── nlu_module.py        # NLU模块
├── tools/
│   ├── scada_tool.py        # SCADA数据查询
│   ├── physical_ai_tool.py  # 物理AI引擎接口
│   └── calculator_tool.py   # 数值计算
├── workflows/
│   ├── alert_response.yaml  # 告警响应工作流
│   ├── daily_report.yaml    # 日报生成工作流
│   └── condition_assess.yaml
└── api/
    ├── rest_api.py          # RESTful API
    └── ws_api.py            # WebSocket API
```

---

## 安全治理框架

认知AI引擎涉及水利基础设施的运行决策，安全治理是系统设计的重中之重。

### 6.5.1 安全设计原则

**原则一：只读+建议（Read-Only + Advisory）**

认知AI引擎对物理系统没有直接控制权。它可以读取SCADA数据、查询知识库、生成调度建议，但任何控制操作（如改变闸门开度）必须经过人工确认后由物理AI引擎执行。

**原则二：透明可审计（Transparent & Auditable）**

引擎的每一次推理过程、每一次工具调用、每一个输出都被完整记录，支持事后审计和问责追溯。

**原则三：分级授权（Role-Based Access Control）**

不同角色的用户具有不同的访问权限：

| 角色 | 可用功能 | 限制 |
|------|---------|------|
| 调度员 | 查询、分析、建议、报告 | 不可修改知识库 |
| 高级调度员 | 全部+确认调度建议执行 | 安全相关需二人确认 |
| 系统管理员 | 全部+知识库管理+模型更新 | 需登录审计 |
| 审计员 | 只读查看所有操作日志 | 不可执行任何操作 |

**原则四：失败安全（Fail-Safe）**

当认知AI引擎出现故障（LLM服务中断、知识库不可用等）时，系统自动降级到安全模式：

- LLM不可用 → 退化为规则匹配+关键词检索
- 知识图谱不可用 → 退化为纯RAG
- 全部AI组件不可用 → 仅提供SCADA数据展示，所有决策转为人工

### 6.5.2 输出安全审核

认知AI引擎的每个输出在发送给用户前，都经过多层安全审核：

**第一层：规则检查**

硬编码的安全规则，不可绕过：

```python
SAFETY_RULES = [
    # 不允许建议超出设备物理极限的操作
    Rule("gate_opening <= gate_max_opening"),
    # 冰期流速限制
    Rule("if ice_period: flow_velocity <= 0.8"),
    # 不允许建议同时关闭所有退水闸
    Rule("not all(spillway.closed for spillway in spillways)"),
    # 建议操作必须在ODD范围内
    Rule("suggested_state in ODD"),
]
```

**第二层：LLM自检**

让LLM对自己的输出进行安全自检：

```
请检查以下调度建议是否存在安全隐患：
建议内容：[待检查的建议]
安全检查清单：
1. 是否可能导致水位超过安全上限？
2. 是否可能导致设备超负荷运行？
3. 是否违反当前工况下的调度规程？
4. 操作是否可逆？不可逆操作是否标注了风险？
```

**第三层：数值范围校验**

对输出中涉及的数值进行范围校验：

| 参数类型 | 合理范围 | 超范围处理 |
|---------|---------|-----------|
| 闸门开度 | 0 - 设备最大开度 | 告警+截断 |
| 流量 | 0 - 设计流量×150% | 告警 |
| 水位 | 渠底高程 - 渠顶高程 | 告警+截断 |
| 调节速率 | 0 - 规程允许最大速率 | 告警 |

### 6.5.3 审计日志

所有交互记录以结构化格式存入审计数据库：

```json
{
  "log_id": "LOG-20250615-08:16:32-001",
  "timestamp": "2025-06-15T08:16:32+08:00",
  "session_id": "sess_20250615_001",
  "user_id": "dispatcher_zhang",
  "user_role": "senior_dispatcher",
  "input": {
    "type": "text",
    "content": "3号闸门水位异常，帮我分析原因"
  },
  "processing": {
    "intent": "situation_analysis",
    "entities": ["gate_3", "level_anomaly"],
    "tool_calls": [
      {"tool": "scada_query", "params": {...}, "result_size": 256, "latency_ms": 45},
      {"tool": "kg_query", "params": {...}, "result_size": 128, "latency_ms": 23},
      {"tool": "rag_search", "params": {...}, "result_size": 1024, "latency_ms": 312}
    ],
    "reasoning_steps": 5,
    "total_latency_ms": 2840
  },
  "output": {
    "type": "analysis_with_suggestion",
    "content_hash": "sha256:a1b2c3d4...",
    "safety_check": "passed",
    "confidence": 0.87,
    "sources_count": 3
  }
}
```

审计日志支持以下分析场景：

- **事后追溯**：某次调度决策出现问题时，追溯AI引擎给出的建议和推理过程
- **质量统计**：统计一段时间内的回答准确率、用户满意度趋势
- **性能监控**：分析各模块的延迟分布，发现性能瓶颈
- **安全审计**：检查是否有异常的查询模式或未授权的访问尝试

---

## 可靠性与性能设计

### 6.6.1 高可用架构

调度系统需要7×24小时运行，认知AI引擎的可用性要求为99.9%（年停机时间<8.76小时）。

**双活部署**：部署两套完整的引擎实例，通过负载均衡器分配请求。当一套实例故障时，另一套自动承接全部流量。

**模块级容错**：各模块独立运行，单个模块故障不影响整体服务。例如知识图谱服务宕机时，引擎自动跳过知识图谱检索环节，仅使用RAG和LLM提供降级服务。

**数据库主从复制**：向量数据库和知识图谱数据库采用主从复制架构，主库故障时自动切换到从库。

### 6.6.2 性能优化

**目标延迟**：端到端响应时间P95 < 5秒。

优化措施：

| 环节 | 典型延迟 | 优化方法 | 优化后延迟 |
|------|---------|---------|-----------|
| 意图分类+实体识别 | 200ms | 轻量级分类器（非LLM） | 50ms |
| 向量检索 | 100ms | HNSW索引+缓存 | 30ms |
| BM25检索 | 50ms | Elasticsearch优化 | 20ms |
| 知识图谱查询 | 150ms | 查询缓存+索引优化 | 50ms |
| Cross-Encoder重排 | 500ms | 批处理+GPU加速 | 200ms |
| LLM生成（500tokens） | 3000ms | vLLM+KV-Cache | 2000ms |
| **总计** | **~4000ms** | | **~2350ms** |

**缓存策略**：

- **查询级缓存**：对完全相同的查询缓存回答，TTL=5分钟
- **检索级缓存**：对相似查询（嵌入向量余弦相似度>0.95）复用检索结果，TTL=10分钟
- **SCADA数据缓存**：实时数据缓存30秒，历史数据缓存1小时

### 6.6.3 可观测性

建立完善的监控体系：

**黄金指标**：
- **延迟**：P50/P95/P99响应时间
- **流量**：QPS（每秒查询数）
- **错误率**：5xx错误比例
- **饱和度**：GPU利用率、显存占用、队列深度

**业务指标**：
- 每日活跃用户数
- 平均对话轮数
- 用户反馈正面率
- 安全审核拦截率

**告警阈值**：

| 指标 | 黄色告警 | 红色告警 |
|------|---------|---------|
| P95延迟 | >5秒 | >10秒 |
| 错误率 | >1% | >5% |
| GPU利用率 | >85% | >95% |
| 安全审核拦截率 | >10% | >20% |

---

## 工程实施路线

### 6.7.1 分阶段实施计划

认知AI引擎的建设不是一蹴而就的工程，推荐分三个阶段递进实施：

**阶段一：知识问答系统（3-4个月）**

目标：实现基于RAG的智能问答能力。

交付物：
- 调度规程知识库（分块+索引）
- 基础RAG检索+LLM问答
- 文本对话界面
- 基础安全审核

WNAL等级对应：L1-L2辅助

**阶段二：智能分析助手（4-6个月）**

目标：在阶段一基础上增加SCADA数据集成和多步推理能力。

新增交付物：
- SCADA实时数据接入
- 知识图谱集成
- 告警增强功能
- 多步推理（ReAct）
- 工况分析和调度建议
- 与物理AI引擎的仿真验证接口

WNAL等级对应：L2-L3辅助决策

**阶段三：认知AI引擎完整版（6-8个月）**

目标：实现完整的四层架构，具备自主运行辅助能力。

新增交付物：
- 完整的工作流引擎
- 报告自动生成
- 语音交互
- 高可用双活部署
- 完整的安全治理和审计体系

WNAL等级对应：L3自主（有监督）

### 6.7.2 技术栈推荐

| 组件 | 推荐技术 | 备选 |
|------|---------|------|
| LLM推理 | vLLM | TGI, Ollama |
| 向量数据库 | Qdrant | Milvus, ChromaDB |
| 知识图谱 | Neo4j | NebulaGraph |
| 全文检索 | Elasticsearch | OpenSearch |
| API框架 | FastAPI | Flask |
| 消息队列 | Redis Streams | RabbitMQ |
| 监控 | Prometheus + Grafana | Datadog |
| 日志 | ELK Stack | Loki |
| 容器化 | Docker + K8s | Docker Compose |

### 6.7.3 硬件配置建议

**最小配置**（满足阶段一需求）：

| 组件 | 硬件 | 数量 |
|------|------|------|
| LLM推理服务器 | 1×A100-80GB 或 2×A800-80GB | 1台 |
| 数据库服务器 | 64GB RAM, 1TB SSD | 1台 |
| 应用服务器 | 32GB RAM, 16核CPU | 1台 |

**推荐配置**（满足阶段二-三需求）：

| 组件 | 硬件 | 数量 |
|------|------|------|
| LLM推理服务器 | 2×A100-80GB | 2台（双活） |
| 数据库服务器 | 128GB RAM, 2TB NVMe | 2台（主从） |
| 应用服务器 | 64GB RAM, 32核CPU | 2台（负载均衡） |
| 存储 | NAS或对象存储 | 10TB |

---

## 本章小结

本章系统设计了认知AI引擎的完整架构，主要内容包括：

1. **定位与角色**：明确了认知AI引擎在CHS双引擎架构中的定位——"懂"的能力（与物理AI引擎的"算"的能力互补），以及其四大核心能力（知识管理、语义理解、知识检索与融合、推理与决策辅助）和在HydroOS中的集成角色。

2. **四层模块化架构**：设计了感知层→认知层→决策层→交互层的分层架构，每一层的核心模块、接口定义和数据流关系清晰明确。决策层的任务编排引擎和多步推理引擎是区别于简单问答系统的关键组件。

3. **核心API设计**：定义了对话、知识查询、告警增强和调度建议四类RESTful API，以及流式输出的WebSocket接口，并给出了与物理AI引擎的仿真验证接口设计。

4. **任务编排与工作流**：设计了三个预定义工作流（告警响应、日报生成、工况评估）和基于LLM的动态任务编排机制，讨论了Agent框架选型策略。

5. **安全治理框架**：建立了"只读+建议""透明可审计""分级授权""失败安全"四大安全原则，设计了三层输出安全审核机制（规则检查→LLM自检→数值校验）和完整的审计日志方案。

6. **可靠性与性能**：给出了高可用双活部署方案、性能优化措施（端到端P95<5秒）和完善的可观测性监控体系。

7. **工程实施路线**：提出了三阶段递进实施计划（知识问答→智能分析→完整引擎），给出了技术栈推荐和硬件配置建议。

---

## 习题

### 基础题

**6-1.** 比较物理AI引擎和认知AI引擎的输入、输出和核心能力，解释为什么CHS框架需要"双引擎"而非单一引擎。

**6-2.** 解释认知AI引擎的"只读+建议"安全原则。为什么认知AI引擎不应该具有直接控制物理设备的权限？如果未来技术成熟度提高，这个原则是否可以放松？

**6-3.** 描述ReAct（Reasoning + Acting）推理范式的基本流程。用一个水利领域的例子说明"思考—行动—观察"循环如何工作。

### 应用题

**6-4.** 为以下场景设计完整的任务编排DAG（包括子任务列表、依赖关系和所用模块）：

> 调度员问："明天有暴雨预警，而且5号泵站计划检修，能否推迟检修？如果不能推迟，暴雨期间应采取什么补偿措施？"

**6-5.** 设计认知AI引擎的降级策略表——当以下组件分别不可用时，系统如何降级运行：（a）LLM推理服务；（b）向量数据库；（c）知识图谱；（d）SCADA数据接口。

### 思考题

**6-6.** 认知AI引擎的一个核心挑战是"信任校准"——调度员对AI建议的信任程度应该恰到好处：过低则系统形同虚设，过高则可能导致自动化偏信（Automation Complacency）。你如何设计引擎的交互方式，使调度员建立恰当的信任水平？考虑置信度展示、推理过程透明度和偏差案例教育等维度。

---

## 拓展阅读

1. **Yao, S. et al. (2023).** "ReAct: Synergizing Reasoning and Acting in Language Models." *ICLR 2023*. — ReAct范式的原始论文，将推理与工具调用统一到LLM的生成过程中。

2. **Schick, T. et al. (2023).** "Toolformer: Language Models Can Teach Themselves to Use Tools." *NeurIPS 2023*. — LLM自主学习使用外部工具的方法，对认知AI引擎的动态工具调用有重要启示。

3. **Wu, Q. et al. (2023).** "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation." *arXiv:2308.08155*. — 多Agent对话框架，适用于复杂多步推理任务的编排。

4. **Lei, X. et al. (2025b).** "Architecture of Autonomous Intelligent Water Networks." *南水北调与水利科技*, DOI: 10.13476/j.cnki.nsbdqk.2025.0079. — 描述了CHS框架中物理AI引擎与认知AI引擎的双引擎架构设计。

5. **Lei, X. et al. (2025a).** "Theoretical Background and Research Paradigm of Cybernetics of Hydro Systems." *南水北调与水利科技*, DOI: 10.13476/j.cnki.nsbdqk.2025.0077. — CHS理论框架，包含"认知增强"原理的正式定义。

---

> **下一章预告**：第七章将讨论人机协同决策与对话调度——如何设计认知AI引擎与调度员之间的交互模式，使得AI辅助真正提升而非干扰调度决策的质量。我们将讨论人机信任模型、对话策略设计、决策权限分配以及调度员培训方案。
