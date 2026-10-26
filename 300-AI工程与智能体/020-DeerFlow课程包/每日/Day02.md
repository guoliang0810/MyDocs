# Day02（4×45min）：LLM 调用封装 + Prompt 结构 + 配置管理

## 今日目标
- 抽象出 `LLMClient`（或等价）统一调用接口
- 形成可复用的 Prompt 模板：system / user / tool messages
- 完成基础配置加载：环境变量 → 配置对象（最小可用）

---

## 第1节（45min）：LLM 调用在工程里应该长什么样
### 课件
1. “直接在业务代码里调用 LLM”会发生什么：难测、难换模型、难控成本
2. 抽象的最小集合：`chat(messages) -> response`
3. 结构化日志：记录 model、tokens（先预留）、耗时、trace_id

### 当堂练习
- 写出你希望 LLMClient 暴露的 3 个方法名（例如 `chat`, `stream_chat`, `count_tokens`）

---

## 第2节（45min）：实现最小 LLMClient（先不追求完美）
### 课件
1. 配置从哪里来：`.env` / 环境变量 / config 文件
2. 不要把 API Key 打到日志里

### 课堂跟做（可按你已有依赖选择实现）
实现一个最小 `LLMClient`：
- 输入：`messages: list[dict]`（role/content）
- 输出：`text: str`（先只取文本）
- 错误：捕获异常，转换为可读错误（不要直接抛到 HTTP 层）

建议最小配置字段：
- `MODEL_NAME`
- `API_BASE`（可选）
- `API_KEY`
- `TIMEOUT_SECONDS`

---

## 第3节（45min）：Prompt 模板（系统提示词与工程约束）
### 课件
1. System Prompt 放什么：角色、边界、工具说明、输出格式
2. User Prompt 放什么：任务目标、输入数据、约束
3. 工程化输出：强制 JSON / markdown 结构（后续做 artifacts）

### 课堂跟做
写一个 `build_system_prompt()`（或等价）包含：
- 你的 agent 角色（研究助手/工程助手）
- 工具使用规则（先写“只能用已注册工具”）
- 输出格式要求：默认用 markdown，产物用标题分段

当堂练习：
- 用同一个 system prompt，给 2 个不同 user 请求，比较输出差异

---

## 第4节（45min）：把 LLM 接到网关里（先做一个 /chat）
### 课件
1. 为什么要做一个“最小 chat endpoint”：尽早形成端到端闭环
2. 线程：先不做记忆，只做“对话输入 → LLM → 输出”

### 课堂跟做
新增 API：
- `POST /chat`：body 里传 `message`，返回 LLM 回复文本
- 记录日志：请求开始/结束、耗时、返回长度

---

## 当天作业
### 必做
- 有 `LLMClient` 抽象（或等价），网关通过它调用模型
- `POST /chat` 可用（简单对话即可）
- system prompt 以函数/模板形式存在（不是散落字符串）

### 选做
- 支持 streaming（SSE 或 chunked），先留接口也可以
- 增加请求级 trace_id（header 或生成）

### 提交物
- `artifacts/day02_prompt.md`：你最终 system prompt 的版本
- `scripts/smoke.md`：如何验证 `/chat`

### 自测
- 你能解释：为什么要把 LLM 调用封装成 client 吗？
- 你能解释：system prompt 和 user prompt 各自的职责吗？

---

## 老师教案（授课提示）
- 不要在 Day02 引入太多框架争论，目标是“跑通 + 可替换”
- 强调密钥安全：不进日志、不进仓库

