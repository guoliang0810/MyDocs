> [!WARNING] 历史快照 — 含虚构 API 版本，风险最高
> **核查日期**：2026-10-26
> **主要问题**：
> - "**Assistants API v3 (2026)**" — 🔴 **该版本不存在**。Assistants API 仅有 v1/v2，
>   且已于 2025-08-26 宣布弃用、**2026-08-26 正式关停**（按今天算已下线）。
> - "Operator (电脑操作员) 代号" — 🔴 Operator 是正式产品名，不是代号；
>   且 2025-01 版本只操作自己的浏览器，不接管用户本地电脑。
> - "Swarm 核心：Routines 和 Handoffs" — ⚠️ 正式两个原语是 Agents + Handoffs；
>   Routines 是 README 中列举的 client-side pattern 之一，非并列原语。
> - 分支对话、File Search 混合检索、Code Interpreter 联网 — 能力真实，但**归属对象错误**
>   （属于 Responses API，非 Assistants API）。
> - 关键缺失：Operator 已于 2025-07-17 全面并入 ChatGPT 成为 "ChatGPT agent"，独立站已 sunset。
> **原则**：产品生命周期信息必须查官方 release notes，不能靠记忆。

# OpenAI "Operator" 与 Assistants API 演进

## OpenAI Operator (电脑操作员)
> 2025年发布的里程碑式产品（代号），能够直接接管用户电脑完成复杂任务。

- **核心能力**:
    - **Computer Use**: 能够看懂屏幕，控制鼠标键盘。
    - **跨应用工作流**: 比如 "帮我查一下去巴黎的机票，对比三家网站，把结果做成 Excel 发给我"。
    - **浏览器沙箱**: 在安全的环境中执行网页操作。

## Assistants API v3 (2026)
- **状态管理**: 更加成熟的 Thread 管理，支持分支对话。
- **File Search (RAG)**: 性能大幅提升，支持混合检索 (Hybrid Search)。
- **Code Interpreter**: 支持更多 Python 库，甚至支持部分网络访问（受控白名单）。

## Swarm Framework
- 虽然 OpenAI 官方称其为 "实验性/教育性" 框架，但在 2025 年被广泛模仿。
- 核心思想：**Routines** (程序) 和 **Handoffs** (交接)。
- 这种模式非常适合客服场景：前台 Agent 分类意图 -> 转接给 售后 Agent / 销售 Agent。
