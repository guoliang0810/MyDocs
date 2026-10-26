# Day17（4×45min）：可观测性与事件流（trace + task 事件 + SSE 选做）

## 今日目标
- 让系统可观测：trace_id 贯穿 gateway/runtime/tools/subagents
- 为 task/subagent 增加事件：started/progress/done/error
- 实现事件拉取接口（必做：轮询），选做：SSE

---

## 第1节（45min）：没有可观测就没有工程化 Agent
### 课件
1. Agent 的 bug 常见在哪里：工具调用错、上下文错、边界错、超时
2. 你需要看见什么：
   - 一次请求的全链路 trace
   - 每个节点/工具的耗时与结果摘要
   - 子任务的状态变化

### 当堂练习
- 写出一次 messages 请求，你希望日志里至少出现的 6 个字段

---

## 第2节（45min）：Trace 贯穿（统一上下文字段）
### 课件
1. trace_id 从哪来：header/生成
2. span 的概念：一次 run 里多个节点/工具/子任务
3. 初学者实现：先把 trace_id 透传到所有日志

### 课堂跟做
完善 middleware：
- before：保证 state/context 有 trace_id
- tools/subagents 调用时：把 trace_id 作为参数透传（或从上下文读）

---

## 第3节（45min）：事件模型（Event Bus / Event Store）
### 课件
1. 事件 vs 日志：事件给 UI/调用方用，日志给开发者用
2. 事件结构建议：
```json
{ "type":"task.progress", "task_id":"...", "ts":"...", "data":{...} }
```

### 课堂跟做
实现最小 EventStore（内存版）：
- `append(event)`
- `list(since_ts|cursor)`

把 subagent executor 的状态变化写事件：
- started/progress/done/error

---

## 第4节（45min）：对外事件接口（必做轮询，选做 SSE）
### 课件
1. 轮询：简单可靠
2. SSE：体验更好（但更复杂）

### 课堂跟做
必做 API：
- `GET /threads/{thread_id}/events?cursor=...`

选做 API：
- `GET /threads/{thread_id}/events/stream`（SSE）

---

## 当天作业
### 必做
- trace_id 出现在所有关键日志（gateway/runtime/tools/subagents）
- subagent/task 的状态变化会产生事件
- events API 可按 cursor 拉取增量

### 选做
- SSE 流式事件
- 把关键事件写入 artifacts（便于复盘）

### 提交物
- `artifacts/day17_event_examples.json`：示例事件序列
- 一次完整任务的 trace 演示（贴日志关键行）

### 自测
- 你能解释：为什么事件要给 UI 用，而日志给开发者用吗？

---

## 老师教案
- 今天强调“可观测不是锦上添花”，是后续所有复杂功能的地基

