# Day01（4×45min）：工程化入门 + 最小 API + 课程仓库建立

## 今日目标
- 建好课程项目仓库 `mini-deerflow`（能运行、能提交）
- 跑通最小 FastAPI：`/health`、`/threads`（假数据即可）
- 统一“线程/产物/上传”目录约定（先建空目录，后续逐步接入）

## 课前准备（老师/学生）
- 已完成：`附录/00-环境搭建与自检.md`
- 创建一个空目录作为课程代码：`mini-deerflow/`

---

## 第1节（45min）：课程地图与工程化最小闭环
### 课件（可直接投屏）
1. 为什么要做“工程化 Agent”：可控、可扩、可调试、可交付
2. 本课程最终产物 Mini-DeerFlow 的模块图（先有边界感）
3. 每天的固定交付：能跑 + 能演示 + 有作业提交物
4. 线程隔离三目录：workspace / uploads / artifacts（先约定，后实现）

### 当堂练习
- 写下你理解的 3 个名词：Thread、Tool、Sandbox（一句话解释）

### 学生材料（带走）
- 今日术语卡片：Thread = 一次对话的隔离单元；Artifacts = 产物；Uploads = 用户输入文件

---

## 第2节（45min）：初始化项目（pyproject + 目录结构）
### 课件
1. 为什么用 `src/`：避免导入混乱
2. 为什么要有 `config/`：把“可变的”抽出来
3. 为什么要有 `scripts/`：一键自检与演示

### 课堂跟做（老师领跑，学生跟打）
在 `mini-deerflow/` 创建目录（允许用你熟悉的方式创建）：
```text
mini-deerflow/
  src/
    gateway/
    config/
  workspace/
  uploads/
  artifacts/
  scripts/
  README.md
```

在 `README.md` 写 5 行：
- 项目名
- 如何启动
- 如何验证 `/health`
- 今日完成点
- 明日计划

### 当堂练习
- 提交一次 Git commit（信息示例：`day01 init skeleton`）

---

## 第3节（45min）：最小 FastAPI 服务（health + threads）
### 课件
1. API 网关的职责：对外、稳定、可测试
2. “统一响应格式”的必要性：前端/调用方更省心

### 课堂跟做（伪代码级别要求，能跑为准）
实现三个端点（可按你习惯组织文件）：
- `GET /health` → `{"ok": true}`
- `GET /threads` → 返回线程列表（先用内存假数据）
- `POST /threads` → 创建线程（返回 `thread_id`）

建议返回结构（统一 shape）：
```json
{ "data": "...", "error": null }
```

### 当堂练习
- 用浏览器或 curl 访问 `/health`，截图或复制响应保存到作业目录

---

## 第4节（45min）：工程约定（目录、命名、日志）
### 课件
1. 目录约定：workspace/uploads/artifacts 对应每个 thread 的隔离子目录
2. 日志三要素：timestamp、level、trace_id（先预留字段）
3. 错误处理：不要让异常直接 500 返回大段堆栈给用户

### 当堂练习
- 给 `/threads` 接口加最小日志：请求开始 + 返回数量

---

## 当天作业
### 必做
- 交付一个可运行的 FastAPI 项目，含：
  - `/health`、`/threads`（GET/POST）
  - `workspace/ uploads/ artifacts/ scripts/` 目录存在
  - `README.md` 有启动与验证说明

### 选做
- 增加 `GET /threads/{thread_id}`（查单个线程）
- 统一错误响应（例如 400/404 时 `{"data": null, "error": {...}}`）

### 提交物
- 代码仓库
- `scripts/smoke.md`：列出你如何验证（复制你实际执行的命令/操作）

### 自测（你会就算过）
- 你能解释：为什么 threads 要有独立目录吗？
- 你能解释：为什么统一响应格式能降低后续成本吗？

---

## 老师教案（授课提示）
- 节奏控制：今天只追求“能跑”，不要纠结最佳实践
- 常见卡点：学生环境问题多，留出 10 分钟机动时间
- 板书建议：画出 3 个目录与 thread_id 的映射关系

