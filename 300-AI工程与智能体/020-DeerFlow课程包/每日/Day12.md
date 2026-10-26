# Day12（4×45min）：规划-执行-检查（Planner/Executor/Checker）模式

## 今日目标
- 在 runtime 中加入“计划节点”和“检查节点”，提升稳定性
- 把复杂任务拆成：Plan → Execute（工具/子任务）→ Check → Finalize
- 产出一份可复用的“研究任务模板”prompt

---

## 第1节（45min）：为什么要分 Planner/Executor/Checker
### 课件
1. 不分层的后果：模型一口气输出，容易漏步骤/乱调用工具
2. 分层的收益：可控、可观测、可回滚
3. Checker 的价值：把“正确性”从玄学变成流程

### 当堂练习
- 给一个任务：“调研 X 并写报告”，写出你期望的 Plan 结构（3~6 步）

---

## 第2节（45min）：Plan 节点（输出结构化计划）
### 课件
1. 计划输出要结构化：步骤、每步工具、输入输出、停止条件
2. 计划要保守：优先用已有工具，缺工具再提需求

### 课堂跟做
实现 `plan_node`：
- 输入：用户目标 + 可用工具清单
- 输出：JSON 计划（写入 state）

计划 JSON 示例：
```json
{
  "steps": [
    {"id":"s1","tool":"search","input":{"query":"..."},"expect":"sources"},
    {"id":"s2","tool":"write_artifact","input":{"title":"report","content":"..."},"expect":"artifact"}
  ]
}
```

---

## 第3节（45min）：Execute 节点（按计划执行）
### 课件
1. 执行要有“防呆”：未知工具名直接报错
2. 每步结果要落地：写入 state + 可选写 artifacts（便于审计）

### 课堂跟做
实现 `execute_plan_node`：
- 遍历 steps
- 调用 ToolRegistry 或 SubagentExecutor
- 收集结果：`step_results`

当堂练习：
- 让一个计划包含 1 个工具失败步骤，观察 checker 如何处理

---

## 第4节（45min）：Check 节点（自检与修正）
### 课件
1. Checker 做什么：检查是否满足用户目标、是否缺关键引用/证据
2. 失败策略：补做 1~2 步 or 返回“缺口说明”

### 课堂跟做
实现 `check_node`：
- 输入：plan + step_results + 用户目标
- 输出：
  - `ok: true` → 进入 finalize
  - `ok: false` → 追加“补救步骤”并回到 execute（限制最多循环 K 次）

---

## 当天作业
### 必做
- graph 里出现 Planner/Executor/Checker 至少 3 个节点
- 执行能按 plan 调工具，结果可追溯（state 或 artifacts）
- checker 有循环上限（避免死循环）

### 选做
- checker 失败时产出 `gap_report.md`（缺口报告）
- plan 支持并行步骤（对接 Day11 subagent）

### 提交物
- `artifacts/day12_plan.json`：一次真实运行的计划
- `artifacts/day12_report.md`：最终报告产物

### 自测
- 你能解释：为什么 checker 要有循环上限吗？

---

## 老师教案
- 今天强调“结构化输出”，否则后续扩展会非常痛苦

