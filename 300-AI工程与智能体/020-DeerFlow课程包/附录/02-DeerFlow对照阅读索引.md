# DeerFlow 对照阅读索引（建议 Day20 使用）

本索引用来把你在课程里实现的“Mini-DeerFlow”与 DeerFlow 2.0 的真实工程做对照，帮助你形成“架构师视角”：模块边界、横切关注点、运行时治理与扩展点。

## 建议阅读顺序（从入口到系统）
### 1) Lead Agent 入口与组装
- 入口：`backend/src/agents/lead_agent/agent.py`
  - 看 `make_lead_agent`：模型/工具/middleware 如何拼装
  - 看 `_build_middlewares`：中间件链顺序为何如此（线程目录、上传、沙箱、补消息、摘要、todo、标题、记忆、图像、澄清）

### 2) Middlewares（横切关注点）
- 目录：`backend/src/agents/middlewares/`
  - 先读：`thread_data_middleware.py`、`uploads_middleware.py`
  - 再读：`memory_middleware.py`、`title_middleware.py`
  - 进阶：`clarification_middleware.py`（为什么必须最后）

### 3) Sandbox（执行隔离）
- 抽象与工具：`backend/src/sandbox/`
- Local provider：`backend/src/sandbox/local/`
- 关注点：路径虚拟化、线程隔离目录映射、允许的操作集

### 4) Tools / Skills（能力系统）
- Tools：`backend/src/tools/`
- Skills：`backend/src/skills/`
- 关注点：发现与加载、类型定义、能力注入到 prompt、与 MCP 的关系

### 5) Subagents（任务委派）
- 目录：`backend/src/subagents/`
- 关注点：并发限制、超时、后台执行、结果回传（事件/轮询）

### 6) Gateway（对外 API）
- 目录：`backend/src/gateway/`
- 路由：`backend/src/gateway/routers/`
  - skills、models、memory、uploads、artifacts

---

## 对照表：你课程里要做的 vs DeerFlow 怎么做
### 线程隔离目录
- 你：`ThreadDataMiddleware`（你实现的版本）
- DeerFlow：ThreadDataMiddleware + sandbox 路径映射

### 工具调用与安全
- 你：工具参数校验 + allowlist + 错误码
- DeerFlow：工具分组、沙箱工具集、视图工具、澄清中间件

### 记忆
- 你：JSON 存储 + 注入 prompt
- DeerFlow：异步队列、去抖、结构化抽取、缓存失效

### 子代理
- 你：Executor + 线程池/async 并发 + 超时
- DeerFlow：内置 subagents + 最大并发限制 middleware

