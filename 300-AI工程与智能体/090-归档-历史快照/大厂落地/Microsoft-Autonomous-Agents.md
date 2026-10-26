> [!WARNING] 历史快照 — 内容方向正确但关键生态变更全缺
> **核查日期**：2026-10-26
> **主要问题**：
> - 全文**未提** AutoGen 自 2025-10 进入**维护模式**、Semantic Kernel 同步停更、
>   **2026-04-02 Microsoft Agent Framework 1.0 GA** 才是官方继任者 ——
>   一篇讲"2026 生态"的笔记漏掉了当年最重要的生态变更。
> - Magentic-One 角色数不全（漏 **ComputerTerminal**）。
> - 旧索引中 `Microsoft Copilot Stack` 为空链，且与实际文件名不对应。
> **准确且可保留的部分**：Copilot Studio 源自 Power Virtual Agents（2023-11 品牌停用）、
>   Autonomous Agents 方向、Dynamics 365 整合、M365 Copilot 中调用 Copilot Agents。

# Microsoft Copilot 自主 Agent 生态

## Copilot Studio
- **定位**: 企业级 Agent 构建平台（原 Power Virtual Agents 的进化）。
- **特性**:
    - **Autonomous Agents**: 不仅仅是聊天机器人，而是能自主触发流程的后台服务。
    - **Dynamics 365 整合**: 在销售、客服、供应链管理中深度嵌入。
    - **Copilot Agents**: 可以在 Microsoft 365 Copilot (Teams, Word) 中被调用的技能插件。

## Magentic-One 框架
- 微软研究院推出的多智能体系统。
- **设计哲学**: 既然一个通用模型很难完美解决所有问题，不如用一堆专才模型。
- **角色**:
    - `Orchestrator`: 负责拆解任务，指挥别人。
    - `WebSurfer`: 负责上网查资料。
    - `FileSurfer`: 负责读写文件。
    - `Coder`: 负责写代码。
- **启示**: 对于复杂任务（如竞品分析、代码重构），多智能体协作是必经之路。
