# Day04（4×45min）：Tool Calling + 工具注册与错误治理

## 今日目标
- 让 Lead Agent 能调用“你注册的工具”
- 建立工具注册表：名字、schema、权限、实现函数
- 统一工具错误：参数错/执行错/超时 → 可读错误返回给模型与用户

---

## 第1节（45min）：工具 = Agent 的“外设”
### 课件
1. 为什么需要工具：LLM 不擅长访问外部世界、也不安全
2. 工具边界：工具一次只做一件事（可测、可控）
3. 工具协议：输入（JSON）→ 输出（JSON/文本）

### 当堂练习
- 设计 3 个工具名（例如：`search_web`、`read_file`、`write_artifact`），写一句话说明用途

---

## 第2节（45min）：实现工具注册表（Tool Registry）
### 课件
1. 工具元数据：name/description/args_schema/timeout/permission
2. 为什么要 schema：减少幻觉参数、提升稳定性

### 课堂跟做
实现 `ToolRegistry`（或等价）支持：
- `register(tool)`：注册工具
- `get(name)`：取工具
- `list()`：列出可用工具（给前端/调试用）

当堂练习：
- 注册一个纯本地工具：`calculate_length(text) -> int`

---

## 第3节（45min）：让模型能“发起工具调用”
### 课件
1. 两种实现路径：
   - A：LangChain/LangGraph 原生 tool calling
   - B：自己做“函数调用协议”（先解析 JSON 指令）
2. 初学者建议：先用简单协议跑通，再替换为原生 tool calling

### 课堂跟做（最小闭环）
实现一个“工具执行节点”：
- 输入：state（含 messages 与可能的 tool request）
- 动作：解析工具名与参数 → 执行 → 把结果写回 messages
- 输出：更新后的 state

当堂练习：
- 让 agent 在被问“这段文本长度多少？”时调用 `calculate_length`

---

## 第4节（45min）：错误治理与可观测
### 课件
1. 错误分类：参数错误（400）、工具执行失败（500/502）、超时（504）
2. 工具日志：tool_name、args 摘要、耗时、成功/失败
3. 不泄漏：不要把文件全文/密钥写入日志

### 课堂跟做
统一一个工具错误结构（示例）：
```json
{
  "ok": false,
  "error": { "type": "VALIDATION_ERROR", "message": "missing field: url" }
}
```

---

## 当天作业
### 必做
- 至少 2 个工具：一个纯函数工具 + 一个与文件/网络相关的工具（可先 stub）
- 工具注册与列出能力（`GET /tools` 或 `/skills` 先占位也可）
- 工具错误结构统一，且会被写入对话 messages（模型能读到）

### 选做
- 给工具加 timeout（超过即返回超时错误结构）
- 给工具加 permission（例如：`filesystem:read`、`filesystem:write`）

### 提交物
- `artifacts/day04_tools.md`：列出工具名、schema、示例输入输出
- `scripts/smoke.md`：演示一次工具调用成功 + 一次参数错误

### 自测
- 你能解释：为什么工具一次只做一件事吗？
- 你能解释：为什么错误结构要统一吗？

---

## 老师教案
- 今天不要追求“完美的 tool calling 框架”，要先闭环
- 强调：工具输出要短、结构化，避免把大段文本塞回消息

