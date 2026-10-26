# Day11（4×45min）：Subagent 执行器（并发/超时/聚合）

## 今日目标
- 实现 SubagentExecutor：能并发跑多个子任务并聚合结果
- 加入并发限制与超时（避免资源被打爆）
- 在 API 层提供 task 接口（轮询或简化版事件流）

---

## 第1节（45min）：为什么需要 Subagent
### 课件
1. 单 agent 的瓶颈：串行慢、上下文混
2. 子代理的本质：把任务拆成可并行的小任务
3. 系统关注点：并发上限、超时、取消、结果一致性

### 当堂练习
- 把“写报告”拆 3 个并行子任务：搜集/归纳/结构化

---

## 第2节（45min）：设计 SubagentExecutor 的接口
### 课件
1. 最小接口：
   - `submit(task_spec) -> task_id`
   - `get_status(task_id) -> {running|done|error}`
   - `get_result(task_id) -> result`
2. 任务规范（task_spec）要结构化：name、input、timeout

### 课堂跟做
实现内存级 task store：
- task_id → status/started_at/ended_at/result/error

并实现并发限制：
- 同时最多 N 个 running（建议 N=3）

---

## 第3节（45min）：最小子代理实现（复用你的 Lead Agent 或 LLMClient）
### 课件
1. 初学者版本：subagent 只是“受限能力的 LLM 调用”
2. 进阶版本：subagent 有自己的 tools/沙箱（可选）

### 课堂跟做
实现 `run_subtask(task_spec)`：
- 输入：子任务描述（例如“提取关键点”）
- 输出：结构化结果（json 或 markdown）
- 错误：超时/异常都要返回统一错误结构

当堂练习：
- 并发提交 3 个子任务，最终聚合成一个“总总结”

---

## 第4节（45min）：API 接入（轮询版）
### 课件
1. 轮询模型：简单可靠（先做这个）
2. 事件流模型（SSE）：Day17 再做

### 课堂跟做
新增 API：
- `POST /threads/{thread_id}/tasks`：提交子任务集合（或单个）
- `GET /threads/{thread_id}/tasks/{task_id}`：查状态/结果

---

## 当天作业
### 必做
- SubagentExecutor 可并发跑 3 个子任务，并限制上限
- 超时可配置，超时后状态正确、错误可读
- 有“聚合节点/函数”：把多个子结果合成最终回复或产物

### 选做
- 增加取消任务 `DELETE /tasks/{task_id}`
- 子任务结果写入 artifacts（便于审计）

### 提交物
- `artifacts/day11_parallel_demo.md`：记录 3 个子任务输入输出与最终聚合结果

### 自测
- 你能解释：为什么必须限制并发吗？

---

## 老师教案
- 今天学生最容易卡在并发与共享状态：强调“任务结果存储”要线程安全/原子思维

