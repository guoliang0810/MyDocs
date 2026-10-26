> [!WARNING] 代码 API 已全部废弃 — 保留作为组件分类学参考，勿直接复制运行
> **核查日期**：2026-10-26
>
> 以下 API 在 LangChain 0.3+ 已弃用或迁入 `langchain-classic`：
>
> | 本文件中的写法 | 现状 | 替代 |
> |---|---|---|
> | `initialize_agent` | 🔴 已弃用 | `create_agent`（LangChain 1.0）或改用 **LangGraph** |
> | `AgentType.ZERO_SHOT_REACT_DESCRIPTION` | 🔴 已弃用 | `create_agent(..., tools=...)` |
> | `LLMChain` | 🔴 已弃用 | LCEL 管道 `prompt \| model \| parser` |
> | `SequentialChain` | 🔴 已弃用 | LCEL 管道链 |
> | `RouterChain` | 🔴 已弃用 | LCEL 条件分支（`RunnableBranch`） |
> | `ConversationBufferMemory` | 🔴 已弃用 | `RunnableWithMessageHistory` |
>
> ✅ **仍然有效**：第 2 节的四组件分类学（Model I/O / Retrieval / Chains / Memory）
> 与第 3 节的 **LCEL 管道式编排思维**——这两点是通用的，值得保留。
>
> 💡 **对本库的建议**：物理 AI 场景建议直接用 **LangGraph**（显式状态机，便于做
> 建模→求解→校核的 Checker 环节），而非 LangChain 的高层 Agent 抽象。

# LangChain 开发与 Agent 实战

## 1. 什么是 LangChain?
LangChain 是一个用于构建 LLM 应用的编排框架。它就像胶水，把 LLM、数据源、外部工具连接在一起。

### 核心价值
- **组件化**: 提供标准接口封装各种 LLM、VectorStore、Tool。
- **链式调用**: 将多个操作串联起来 (Chain)。
- **Agent**: 让 LLM 具备决策和行动能力。

## 2. 核心组件 (The Building Blocks)

### 2.1 Model I/O
- **LLMs**: 纯文本模型 (输入文本 -> 输出文本)。
- **ChatModels**: 对话模型 (输入消息列表 -> 输出消息)。
- **Prompts**: `PromptTemplate` 管理和复用提示词。
- **Output Parsers**: 将 LLM 的文本输出解析为结构化数据 (JSON, List, Pydantic)。

### 2.2 Retrieval (RAG 相关)
- **Document Loaders**: 加载 PDF, CSV, Notion 等。
- **Text Splitters**: `RecursiveCharacterTextSplitter`。
- **Vector Stores**: 封装 Chroma, FAISS, Milvus 等接口。
- **Retrievers**: 定义如何查找文档 (如 `SelfQueryRetriever`).

### 2.3 Chains (链)
将组件组装成流水线。
- **LLMChain**: Prompt + LLM。
- **SequentialChain**: 串联多个 Chain (A 的输出是 B 的输入)。
- **RouterChain**: 根据问题类型路由到不同的 Chain (如数学问题 -> MathChain, 历史问题 -> HistoryChain)。

### 2.4 Memory (记忆)
让无状态的 LLM 记住上下文。
- **ConversationBufferMemory**: 记住完整的对话历史。
- **ConversationSummaryMemory**: 自动总结之前的对话，节省 Token。

## 3. LCEL (LangChain Expression Language)

LangChain 从 v0.1 开始推崇的声明式语法，使用 `|` 管道符连接组件，类似 Unix 管道。

```python
# LCEL 示例：构建一个讲笑话的 Chain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

model = ChatOpenAI(model="gpt-4")
prompt = ChatPromptTemplate.from_template("给我讲一个关于 {topic} 的笑话")
output_parser = StrOutputParser()

# 核心链定义
chain = prompt | model | output_parser

# 调用
chain.invoke({"topic": "程序员"})
```

## 4. AI Agent (智能体)

Agent 是 AI 应用的终极形态。**Chain 是执行既定的流程，Agent 是让 LLM 自己决定怎么做。**

### 4.1 核心架构 (ReAct)
**ReAct = Reasoning (推理) + Acting (行动)**
1.  **Thought**: 用户问了这个问题，我该怎么办？(推理)
2.  **Action**: 我需要查一下天气工具。(选择工具)
3.  **Observation**: 工具返回结果 "北京今天晴"。(观察结果)
4.  **Thought**: 我已经知道答案了。(再次推理)
5.  **Final Answer**: 北京今天天气不错。(生成回答)

### 4.2 Tool (工具)
Agent 的手和脚。可以是：
- **Google Search**: 联网搜索。
- **Python REPL**: 执行代码进行计算。
- **Custom Tool**: 自定义 API (如查询公司内部库存)。

### 4.3 实战：构建一个能上网的 Agent

```python
from langchain.agents import load_tools, initialize_agent, AgentType
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(temperature=0)
# 加载工具：谷歌搜索 + 数学计算
tools = load_tools(["serpapi", "llm-math"], llm=llm)

# 初始化 Agent
agent = initialize_agent(
    tools, 
    llm, 
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
    verbose=True
)

# 运行
agent.run("现在的美元汇率是多少？如果我有 100 美元，能换多少人民币？")
```
