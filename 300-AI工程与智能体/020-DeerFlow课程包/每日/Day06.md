# Day06（4×45min）：Middleware 链（横切关注点的工程化实现）

## 今日目标
- 在 Lead Agent 的运行时引入 middleware 链：前置/后置处理
- 把“日志、trace、错误治理、上下文注入”从业务节点里剥离
- 形成可插拔的 middleware 接口（后面 Day07–Day09 全靠它）

---

## 第1节（45min）：为什么需要 Middleware
### 课件
1. Agent 项目里最难的是“横切关注点”：目录、上传、记忆、安全、限流
2. 如果都塞到节点里：节点会变成巨石（不可测试、不可维护）
3. middleware = 可组合的小模块，严格顺序执行

### 当堂练习
- 写下 3 个你认为应该做成 middleware 的功能（例：trace_id 注入）

---

## 第2节（45min）：定义 Middleware 协议（最小可用）
### 课件
1. 两个钩子就能起飞：`before(state)` 与 `after(state, result)`
2. middleware 顺序是“架构决策”：早做的影响后做的

### 课堂跟做
定义 middleware 接口（你可以用抽象类/协议/约定函数）：
- `before(state) -> state`
- `after(state) -> state`

并实现一个运行器：
- 输入：middlewares 列表 + graph invoke
- 行为：按顺序 before → 执行 graph → 逆序 after

---

## 第3节（45min）：实现 2 个通用 middleware
### 课件
1. TraceMiddleware：给每次请求生成/透传 trace_id
2. LoggingMiddleware：统一日志（节点名/工具名/耗时）

### 课堂跟做
实现：
- `TraceMiddleware`：若请求 header 有 trace id 则使用，否则生成
- `LoggingMiddleware`：记录一次 run 的开始/结束/耗时/错误类型

当堂练习：
- 故意制造一次工具参数错误，观察日志是否可读

---

## 第4节（45min）：把 middleware 接入你的 Lead Agent
### 课件
1. 接入点：在 graph invoke 前后挂钩
2. 不要耦合：middleware 不应依赖具体 node 实现细节

### 课堂跟做
把 middleware 链接入：
- `POST /threads/{thread_id}/messages`
- 确保每次调用都有 trace_id（返回给客户端也可以）

---

## 当天作业
### 必做
- middleware 链可工作（至少 2 个 middleware）
- middleware 的顺序可配置（列表顺序即执行顺序）
- 发生错误时：middleware 能看到并记录错误类型

### 选做
- 增加 `TimingMiddleware`：为每个 node/tool 记录耗时（先粗粒度也行）
- 增加 `RedactionMiddleware`：日志里敏感字段脱敏（key/token）

### 提交物
- `artifacts/day06_middleware_order.md`：写出你当前 middleware 顺序与理由
- `scripts/smoke.md`：演示一次成功 + 一次失败（看日志）

### 自测
- 你能解释：为什么 middleware 的顺序是“架构决策”吗？

---

## 老师教案
- 今天是“架构味道”的起点：强调“抽象边界”比框架 API 更重要

