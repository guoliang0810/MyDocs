# Day08（4×45min）：上下文治理（摘要/裁剪/保留策略）

## 今日目标
- 为长对话引入“上下文治理”机制，避免 token 超限
- 实现一个 SummarizationMiddleware（最简版）
- 明确 keep 策略：哪些消息永远保留、哪些可摘要

---

## 第1节（45min）：为什么上下文会把 Agent 做崩
### 课件
1. token 成本与上限：长对话=爆炸
2. 盲目裁剪的风险：丢关键信息导致工具乱用/产物错误
3. 工程思路：保留“约束与事实”，压缩“过程噪音”

### 当堂练习
- 选 10 条消息，标记哪些应保留：系统约束/用户偏好/工具结果/闲聊

---

## 第2节（45min）：设计 keep/trim 策略
### 课件
1. keep：system prompt、最近 N 轮、关键工具结果、用户偏好摘要
2. summarize：更早的对话过程
3. trigger：何时触发摘要（按消息数/按估计 token/按字数）

### 课堂跟做
定义配置（最小字段）：
- `summarization_enabled: bool`
- `trigger_message_count: int`
- `keep_last_messages: int`

---

## 第3节（45min）：实现 SummarizationMiddleware（最简）
### 课件
1. 摘要也是 LLM 调用：用更便宜的模型（先只留配置字段）
2. 摘要输出要结构化：事实、待办、未解决问题

### 课堂跟做
实现 SummarizationMiddleware：
- 若 messages 超过 trigger
- 取早期消息 → 生成摘要 → 替换为一条 `summary` 消息（system 或 assistant role 均可）
- 保留最近 keep_last_messages 条原文

当堂练习：
- 构造 30 轮假消息，触发摘要后对话仍能继续

---

## 第4节（45min）：把摘要变成可观测产物
### 课件
1. 为什么要把摘要写成 artifacts：可审计、可回滚、可对比
2. 摘要失败怎么办：降级为裁剪（并记录错误）

### 课堂跟做
当摘要产生时：
- 同步写入 `artifacts/{thread_id}/summary.md`
- 在 API 返回里带上 `summary_artifact_id`（可选）

---

## 当天作业
### 必做
- 有可配置的 summarization 开关与 trigger
- 触发摘要后仍能继续对话（不会崩）
- 摘要产物写入 artifacts

### 选做
- 让摘要只抽取“事实/偏好”，把“细节”丢弃
- 给摘要加版本号（summary_v1、v2…）

### 提交物
- 一次触发摘要的完整演示（日志 + summary.md）

### 自测
- 你能解释：为什么“保留约束与事实”比“保留所有过程”更重要吗？

---

## 老师教案
- 强调：摘要不是魔法，它也会错，所以要可审计（写 artifacts）

