# Day07（4×45min）：线程目录隔离 + 上传注入（Uploads Middleware）

## 今日目标
- 为每个 thread 创建隔离目录：`workspace/{thread_id}`、`uploads/{thread_id}`、`artifacts/{thread_id}`
- 实现 UploadsMiddleware：让“上传文件列表”进入 agent 上下文
- 提供上传 API：`POST /threads/{thread_id}/uploads`（最小可用）

---

## 第1节（45min）：为什么每个 thread 都要隔离目录
### 课件
1. 隔离解决：并发冲突、权限边界、清理与回收
2. 路径虚拟化概念：对模型统一成 `/mnt/user-data/...`（先概念，后实现）

### 当堂练习
- 写出 3 个目录的职责差异：workspace vs uploads vs artifacts

---

## 第2节（45min）：ThreadDataMiddleware（目录准备）
### 课件
1. middleware 的职责：为后续 sandbox/tools 提供“已准备好的上下文”
2. 目录创建必须幂等：重复请求不报错

### 课堂跟做
实现 `ThreadDataMiddleware`：
- 输入：state（含 thread_id）
- 动作：确保 3 个目录存在；把物理路径写入 state（或 context）
- 输出：更新后的 state

当堂练习：
- 连续调用两次同一 thread，目录不应重复报错

---

## 第3节（45min）：实现上传 API（先落盘即可）
### 课件
1. 上传要落在哪：`uploads/{thread_id}/`
2. 元数据要记什么：文件名、大小、mime、保存路径、上传时间

### 课堂跟做
实现：
- `POST /threads/{thread_id}/uploads`：multipart 上传
- `GET /threads/{thread_id}/uploads`：列出文件

当堂练习：
- 上传一个 `.txt`，列出后确认可读

---

## 第4节（45min）：UploadsMiddleware（把上传“注入上下文”）
### 课件
1. 注入什么：文件清单 + 每个文件的可用访问方式
2. 注入多少：不要把大文件全文塞进 messages
3. 注入位置：system prompt 或一个专门的 context message

### 课堂跟做
实现 UploadsMiddleware：
- 读取 thread uploads 列表
- 在 state.messages 前面插入一个“上下文消息”，内容示例：
  - 已上传文件：a.txt（路径：...，大小：...）
  - 读取方式：用工具 `read_file` 读取（后续会加权限）

---

## 当天作业
### 必做
- thread 隔离目录自动创建并写入 state/context
- 上传 API 可用：上传 + 列表
- UploadsMiddleware 能把“文件清单”注入到 agent 上下文

### 选做
- 上传时生成 `file_id`（uuid），避免同名覆盖
- 增加 `GET /threads/{thread_id}/uploads/{file_id}` 下载

### 提交物
- 上传一个示例文件，并让 agent 在回复里引用“已上传文件名”
- `scripts/smoke.md`：上传→调用 messages→看到注入效果

### 自测
- 你能解释：为什么不把大文件全文直接塞进 messages 吗？

---

## 老师教案
- 今天要反复强调“注入的是索引，不是内容”，避免学生把 token 用爆

