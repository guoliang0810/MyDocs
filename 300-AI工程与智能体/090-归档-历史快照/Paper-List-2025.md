> [!WARNING] 历史快照 — 已核查出事实错误，勿直接引用
> **核查日期**：2026-10-26
> **主要问题**：全文 **0 个 arXiv 编号、0 位作者、0 条链接**；其中 "OpenAI Swarm" 被包装成带正式标题的论文，
> 实为 GitHub 仓库 `openai/swarm`（2024-10 发布，2025-03 已被 OpenAI Agents SDK 取代）；
> "GAIA 15%" 的数据实为论文原文（2023-11）的 GPT-4+plugins 分数，被错挂到"2024年"；
> Magentic-One 角色数不全（漏 ComputerTerminal）。
> **可信的 6 篇论文编号见** → [[100-物理AI产品与领域/020-领域知识/领域知识索引]]
> **原则**：引用任何编号前，必须打开 abs 页核对标题与作者。

# 2025 AI Agent 必读论文列表

## Benchmark & Evaluation
- **GAIA: A Benchmark for General AI Assistants**
    - *核心贡献*: 提出了一个真正具有挑战性的通用助手基准测试，涵盖了推理、工具使用和多模态能力。2024年 GPT-4 仅得分 15% 左右，2025年 SOTA 模型已突破 60%。
- **AgentBench: Evaluating LLMs as Agents**
    - *核心贡献*: 全面评估 LLM 在 8 个不同环境下的 Agent 能力。

## Multi-Agent Systems
- **Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks** (Microsoft)
    - *核心贡献*: 提出了一个通用的多智能体编排框架，包含 Orchestrator, WebSurfer, FileSurfer, Coder 等角色。
- **OpenAI Swarm: Educational Framework for Lightweight Multi-Agent Orchestration**
    - *核心贡献*: 强调了 "Handoff" (交接) 机制在多智能体协作中的重要性，轻量级、无状态的设计理念。

## Reasoning & Planning
- **Self-Refine: Iterative Refinement with Self-Feedback**
    - *核心贡献*: 让 Agent 自我检查输出并进行修正，显著提升代码生成和数学推理能力。
- **Tree of Thoughts (ToT)**
    - *核心贡献*: 将思维链 (CoT) 扩展为树状搜索，允许 Agent 进行回溯和探索不同的推理路径。

## Large Action Models (LAM)
- **Octopus v2: On-device Language Model for Super Agent**
    - *核心贡献*: 针对端侧设备优化的超快 Function Calling 模型，延迟极低，适合手机端 Agent。
