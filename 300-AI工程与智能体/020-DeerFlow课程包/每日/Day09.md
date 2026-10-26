# Day09（4×45min）：长期记忆（抽取→存储→注入）+ Memory Middleware

## 今日目标
- 做出最小长期记忆：把用户偏好/事实保存到 JSON
- 在对话开始时把记忆注入 system/context
- 引入“异步/去抖”的概念（先做同步版，预留接口）

---

## 第1节（45min）：记忆到底记什么
### 课件
1. 记忆不是“保存所有对话”，而是保存可复用事实
2. 记忆类型：
   - 用户偏好（输出格式、语言风格）
   - 稳定事实（姓名、目标、项目背景）
   - 长期任务（长期目标/里程碑）

### 当堂练习
- 给出 5 条对话，标注哪条应该入记忆，哪条不应该

---

## 第2节（45min）：实现 MemoryStore（JSON 文件版）
### 课件
1. 最简存储：`memory/{user_id}.json` 或 `memory/{thread_id}.json`
2. 读写要有锁/原子性（初学者先用“写临时文件再替换”的思路）

### 课堂跟做
实现：
- `load_memory(scope_id) -> memory_obj`
- `save_memory(scope_id, memory_obj) -> None`

memory_obj 推荐结构：
```json
{
  "facts": [{"key":"name","value":"...","confidence":0.8}],
  "preferences": [{"key":"language","value":"zh"}],
  "updated_at": "..."
}
```

---

## 第3节（45min）：实现 MemoryExtractor（规则优先，LLM 可选）
### 课件
1. 初学者先用规则抽取：比如 “我叫X”、“我喜欢Y”
2. 再引入 LLM 抽取：输出必须结构化 JSON

### 课堂跟做
实现一个最小抽取器：
- 输入：最新一轮 user+assistant
- 输出：要写入的 facts/preferences（可能为空）

当堂练习：
- 让用户说“我叫小明，以后回答用中文、要有小标题”，看是否写入 memory.json

---

## 第4节（45min）：MemoryMiddleware（注入与更新）
### 课件
1. 注入：在 system prompt 前加一段“已知用户偏好/事实”
2. 更新：对话结束后，把抽取结果写入 store
3. 去抖：短时间多轮对话不必每轮都写（先写 TODO，Day17 再做事件/队列）

### 课堂跟做
实现 MemoryMiddleware：
- before：load memory → 注入一条 context message
- after：extract → merge → save

---

## 当天作业
### 必做
- 记忆能跨对话生效：写入后新一轮能被注入并影响回答
- 记忆格式结构化（JSON），可读可调试

### 选做
- 为每条事实加 `confidence` 并实现“低置信不注入”
- 把记忆注入改成“只注入最相关的 3 条”

### 提交物
- `memory/<scope>.json`（示例）
- 一段演示：第一次告诉偏好，第二次自动按偏好输出

### 自测
- 你能解释：为什么记忆要结构化而不是一段自由文本吗？

---

## 老师教案
- 今天强调“先规则、后模型”，让学生建立可控感

