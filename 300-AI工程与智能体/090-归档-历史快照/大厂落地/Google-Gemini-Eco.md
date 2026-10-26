> [!WARNING] 历史快照 — 含虚构产品名，勿直接引用
> **核查日期**：2026-10-26
> **主要问题**：
> - "**Google Workspace Agents**" — 🔴 **无此产品名**。实为 **Google Workspace Studio**
>   （2025-12-03 GA，前身 Workspace Flows）。
> - "开发 **Android Intent 扩展**" — 🔴 名称虚构。Google 的产品是 **Android App Extensions**。
> - "Vertex AI Agent Builder" — ⚠️ 2026-04-22 Cloud Next 上 Vertex AI 品牌已退役，
>   重组为 **Gemini Enterprise Agent Platform**。
> - "Gemini 2.0 / **3.0**" — ⚠️ 正式名是 "Gemini 3"，无 "3.0"；当前应为 Gemini 3.1 Pro / 3.8 Flash。
> - "Gemini Nano 内置于 Pixel 和三星旗舰机" — ⚠️ 部分不实：AICore 首发为 Pixel 8 Pro/9 系列，
>   三星旗舰走自有端侧模型。
> - 真实存在且未记错：Project Astra、Search Grounding、Vertex AI Agent Builder（已更名）。

# Google Gemini Agent 生态 (2026 现状)

## 核心技术栈
- **Gemini 2.0 / 3.0 Models**: 原生多模态 (Native Multimodal)，具备超长上下文 (1M+ tokens)，能够理解长视频和复杂代码库。
- **Project Astra**: Google 的通用 AI 助手愿景，强调实时视频理解和记忆能力。

## 落地场景
1.  **Android 系统级整合**:
    *   Gemini Nano 内置于 Pixel 和三星旗舰机。
    *   可以跨应用读取屏幕内容（如在地图和日历之间自动操作）。
2.  **Google Workspace Agents**:
    *   在 Docs, Gmail, Drive 中自动流转工作。
    *   例如：从 Gmail 提取发票 -> 写入 Sheets -> 发送 Slack 通知。
3.  **Vertex AI Agent Builder**:
    *   企业级开发平台，支持无代码/低代码构建 RAG Agent。
    *   深度集成 Google Search Grounding，减少幻觉。

## 开发者机会
- 利用 **Gemini API** 的 Function Calling 构建垂直领域 Agent。
- 开发 **Android Intent** 扩展，让 Gemini 能控制你的 App。
