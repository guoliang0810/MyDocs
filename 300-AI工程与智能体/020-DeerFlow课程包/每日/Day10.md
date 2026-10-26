# Day10（4×45min）：网关 API 完整化（threads/history/artifacts/tools）

## 今日目标
- 把你的系统对外 API 整理成“像产品一样可用”
- 增加 history、artifacts、tools/skills 列表接口
- 统一请求/响应模型（字段命名、错误码、分页/限制）

---

## 第1节（45min）：API 作为“契约”
### 课件
1. 为什么要有清晰 API：前端、自动化测试、外部集成
2. 契约要素：输入 schema、输出 schema、错误码、示例

### 当堂练习
- 列出你当前已有的 endpoint，并标注“稳定/不稳定”

---

## 第2节（45min）：threads 与 history
### 课件
1. thread 生命周期：create → send message → list history → close（可选）
2. history 返回什么：messages（role/content/ts）、tool calls、artifacts 指针

### 课堂跟做
补齐接口（命名可调整，但要一致）：
- `GET /threads`（分页或 limit）
- `POST /threads`
- `GET /threads/{thread_id}`
- `GET /threads/{thread_id}/history`
- `POST /threads/{thread_id}/messages`

---

## 第3节（45min）：artifacts 与 uploads 接口整理
### 课件
1. 资源式 API：list/get/download
2. 不要把二进制直接塞 JSON：用下载接口

### 课堂跟做
补齐或规范：
- `GET /threads/{thread_id}/artifacts`
- `GET /threads/{thread_id}/artifacts/{artifact_id}`
- `POST /threads/{thread_id}/uploads`
- `GET /threads/{thread_id}/uploads`

---

## 第4节（45min）：tools/skills 列表与运行时信息
### 课件
1. 为什么要暴露可用工具：UI 选择、调试、权限管理
2. “技能”可以先当成“工具包”视角（Day14 再真正做 Skills 系统）

### 课堂跟做
新增：
- `GET /tools`：返回工具元数据（name/description/args_schema/permission）
- `GET /runtime`：返回版本、配置摘要（不含密钥）

---

## 当天作业
### 必做
- 给每个 endpoint 写 1 个示例请求与响应（写在 artifacts/day10_api_examples.md）
- 接口返回结构统一（data/error）
- history/artifacts/tools 至少各有一个可用接口

### 选做
- 增加 OpenAPI 文档的可读描述（summary/response model）
- 增加简单鉴权（例如 API key header，占位即可）

### 提交物
- `artifacts/day10_api_examples.md`
- `scripts/smoke.md`：按顺序走一遍“创建 thread → 发消息 → 产物 → history”

### 自测
- 你能解释：为什么 API 是“契约”吗？

---

## 老师教案
- 今天的重点是“一致性”，不要追求接口多，追求能被别人用

