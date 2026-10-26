# Day20（4×45min）：对照阅读 DeerFlow 源码并复刻“骨架”

## 今日目标
- 用对照索引把 DeerFlow 的关键模块跑一遍“架构阅读”
- 复刻 DeerFlow 的 4 个关键骨架点：
  - lead agent 组装（model/tools/middlewares）
  - middleware 链顺序与职责
  - sandbox 抽象与 provider
  - skills/工具发现与注入
- 输出一份“对照笔记”：你项目的模块 ↔ DeerFlow 模块

---

## 第1节（45min）：入口阅读（Lead Agent 如何被组装）
### 课件
1. 入口文件看什么：
   - 组装顺序（model/tools/middleware/prompt）
   - 配置如何影响运行时（plan mode、subagent）
2. 读源码方法：
   - 先找“工厂函数/组装函数”
   - 再找“抽象接口”
   - 最后看“细节实现”

### 课堂跟读（老师带读）
对照阅读（参考 `附录/02-DeerFlow对照阅读索引.md`）：
- lead agent 入口与 middlewares 构建

当堂练习：
- 写下 DeerFlow middleware 的顺序，并用一句话解释每个 middleware

---

## 第2节（45min）：中间件链的“架构味道”
### 课件
1. 为什么 ThreadDataMiddleware 要在最前
2. 为什么 ClarificationMiddleware 必须最后（拦截澄清请求）
3. 为什么 MemoryMiddleware 在 Title 后面（先有标题再入记忆）

### 课堂跟做
把你自己的 middleware 链顺序写成 artifacts，并对齐 DeerFlow：
- `artifacts/day20_middleware_alignment.md`

---

## 第3节（45min）：Sandbox/Skills/Subagents 三件套对照
### 课件
1. sandbox：抽象接口 + provider 实现 + 工具封装
2. skills：扫描发现 + 解析 + 注入 prompt
3. subagents：执行器 + 限流 + 超时 + 聚合

### 课堂跟做
产出对照表 artifacts：
- `artifacts/day20_module_mapping.md`：你的模块名 ↔ DeerFlow 模块名 ↔ 职责

---

## 第4节（45min）：复刻骨架（只复刻“形”，不追细节）
### 课件
1. 架构师训练：先复刻骨架，再逐步填肉
2. 骨架验收：能把调用链路走通即可

### 课堂跟做
完成 3 个“骨架型改造”（任选你最缺的）：
- 把 lead agent 组装统一到一个工厂函数
- 把 tools 分组（例如 filesystem/tooling/network）
- 把 skills 注入统一到一个 prompt apply 函数

---

## 当天作业
### 必做
- 产出 2 份对照 artifacts：
  - middleware 对齐说明
  - 模块映射表
- 至少完成 1 个骨架改造，并保持测试/自检通过

### 选做
- 选 1 个 DeerFlow 的 middleware/模块，做一次“功能对齐”实现

### 提交物
- `artifacts/day20_middleware_alignment.md`
- `artifacts/day20_module_mapping.md`
- 代码变更（通过 smoke/test）

### 自测
- 你能解释：为什么“顺序”是中间件链的核心吗？

---

## 老师教案
- 今天不要陷入细节，目标是“读懂骨架”，并把骨架映射到自己的项目

