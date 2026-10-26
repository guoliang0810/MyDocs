# LLM 原理与局限性 (Agent 开发视角)

## 1. LLM 是什么？
- 本质是 **Next Token Prediction** (预测下一个词)。
- 它没有真正的“逻辑”或“世界模型”，它只是基于概率统计在模仿人类的文本模式。
- **Context Window (上下文窗口)**: 它是 Agent 的“短期记忆”限制。虽然现在有 1M+ context，但过长会导致 "Lost in the Middle" 现象。

## 2. Agent 开发中常见的 LLM 局限
1.  **幻觉 (Hallucination)**: 一本正经地胡说八道。
    - *对策*: RAG (检索增强), Grounding (接地), 强制引用来源。
2.  **数学与逻辑短板**: 即使是 GPT-4，做复杂算术也可能出错。
    - *对策*: 不要让 LLM 硬算，让它写 Python 代码来算 (Code Interpreter)。
3.  **指令遵循 (Instruction Following) 衰减**: 当 Prompt 太长、规则太多时，LLM 会遗忘后面的指令。
    - *对策*: 拆分 Prompt，使用 Chain of Thought，将复杂任务拆解为多步。

## 3. 为什么需要 Agent？
单纯的 LLM 是被动的（问答式）。
**Agent = LLM + Memory + Planning + Tools**
Agent 赋予了 LLM 主动性 (Agency)，让它能够：
1.  **感知**: 读取外部世界（搜索、API）。
2.  **规划**: 决定第一步做什么，第二步做什么。
3.  **行动**: 执行操作，改变世界。
