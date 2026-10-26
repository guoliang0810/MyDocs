# Day03（4×45min）：LangGraph/状态机思维 + 最小 Lead Agent 跑通

## 今日目标
- 把“对话”从一个 endpoint 升级为“可编排流程”
- 实现最小 Lead Agent：输入 →（可选计划）→ 回答
- 引入 `ThreadState`（或等价）作为状态载体

---

## 第1节（45min）：从 while True 到“可控流程图”
### 课件
1. 传统对话：单次调用 = 黑盒
2. Agent 工程：多步骤 = 白盒可观测
3. 状态机三要素：状态（State）、节点（Node）、转移（Edge）

### 当堂练习
- 把“写研究报告”拆成 4 步，并写出每步输入/输出一句话

---

## 第2节（45min）：定义 ThreadState（你的运行时“内存”）
### 课件
1. State 放什么：messages、thread_id、workspace 路径、artifacts 列表
2. State 不放什么：超大文件内容、敏感信息

### 课堂跟做
定义一个最小 state（示例字段）：
- `thread_id: str`
- `messages: list[message]`
- `latest_user_message: str | None`
- `artifacts: list[artifact_meta]`

当堂练习：
- 写一个函数：`append_user_message(state, text) -> state`

---

## 第3节（45min）：搭建最小 Graph（1~2 个节点即可）
### 课件
1. Node：纯函数/可测试
2. Edge：条件转移（先用固定转移）
3. 终止：什么时候结束（明确停止条件）

### 课堂跟做（目标：跑通一次 graph invoke）
实现两个节点：
- `prepare_node`：把 user 输入写入 state
- `llm_node`：用 `LLMClient` 基于 state.messages 生成回复，并 append 到 messages

当堂练习：
- 打印/记录每个节点的输入输出摘要（不要打印密钥）

---

## 第4节（45min）：把 Graph 接到 API：/threads/{id}/messages
### 课件
1. gateway 和 runtime 的分工：gateway 负责 HTTP，runtime 负责编排
2. 为什么要保存 thread：为后续 uploads/memory/sandbox 做准备

### 课堂跟做
新增 API：
- `POST /threads/{thread_id}/messages`：把 message 交给 Lead Agent graph，返回 assistant 回复
- 暂时用内存 dict 保存 thread state（Day09 再接长期记忆/存储）

---

## 当天作业
### 必做
- 你的项目里出现“可编排的 runtime”（LangGraph 或你自写状态机）
- `POST /threads/{thread_id}/messages` 能跑通多轮对话
- 每个节点都有最小日志（节点名 + 输入长度 + 输出长度）

### 选做
- 增加一个 `should_end` 条件：比如用户输入 `exit` 时结束
- 把 state 持久化到 JSON（先简单存到 `workspace/`）

### 提交物
- `artifacts/day03_graph.png`（可选：手画拍照也行）：你的 graph 结构图
- `scripts/smoke.md`：两轮对话验证步骤

### 自测
- 你能解释：为什么引入 state 会让系统更可控吗？
- 你能解释：Node 应该尽量“纯”是什么意思吗？

---

## 老师教案
- 今天的关键不是“LangGraph API 细节”，而是“把流程变成白盒”
- 如果学生卡在依赖安装：允许先用自写状态机替代，保留接口不变

