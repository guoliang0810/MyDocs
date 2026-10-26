# Day15（4×45min）：测试与回归（关键路径覆盖 + 契约测试）

## 今日目标
- 为关键路径补齐可回归测试：threads/messages/tools/artifacts
- 引入契约测试思维：API 响应结构稳定
- 建立最小 CI 思维：一条命令跑完自检

---

## 第1节（45min）：为什么 Agent 项目更需要测试
### 课件
1. LLM 不稳定：你要测试的是“系统边界与流程”，不是“文案”
2. 可测试点：
   - API 结构与错误码
   - 工具参数校验与边界
   - sandbox 路径限制
   - memory 存取与注入逻辑

### 当堂练习
- 写下 5 个“必须可回归”的行为（例如：路径穿越必须被拒绝）

---

## 第2节（45min）：搭建测试骨架（pytest 或等价）
### 课件
1. 单测 vs 集成：单测测纯函数，集成测接口链路
2. 测试数据隔离：每次测试用临时目录

### 课堂跟做
实现最小测试集（示例）：
- `test_health_ok`
- `test_create_thread`
- `test_send_message_returns_assistant`
- `test_artifact_write_and_list`

当堂练习：
- 故意改坏一个响应结构，观察测试是否能抓到

---

## 第3节（45min）：契约测试（data/error 结构永不变）
### 课件
1. 契约是什么：调用方依赖你的响应 shape
2. 契约测试关注：
   - 字段存在性
   - 类型
   - 错误结构

### 课堂跟做
为每个 endpoint 写一个“shape 断言”：
- `data` 与 `error` 字段必须存在
- 错误时 `data=null`
- 成功时 `error=null`

---

## 第4节（45min）：最小回归脚本（不依赖测试框架也能跑）
### 课件
1. 为什么要有 smoke 脚本：快速排查部署环境问题
2. 一键脚本包含：
   - 启动服务（或假设已启动）
   - 调用关键接口
   - 输出结果与 exit code

### 课堂跟做
写 `scripts/smoke.py`（或等价）：
- health → create thread → send message → list artifacts/tools
- 任一步失败则返回非 0

---

## 当天作业
### 必做
- 至少 6 个测试覆盖关键路径（含 1 个失败 case）
- smoke 脚本存在且能跑通
- 新增功能必须先写测试再实现（从今天开始执行）

### 选做
- 为 sandbox 路径穿越加专门测试
- 为 memory 注入写测试（注入内容包含已知偏好）

### 提交物
- `tests/` 或等价目录
- `scripts/smoke.py` 输出示例（贴到 artifacts/day15_smoke_output.md）

### 自测
- 你能解释：为什么不测试 LLM 文案本身，而测试流程与边界吗？

---

## 老师教案
- 今天要给学生建立习惯：每次改动先想“怎么回归验证”

