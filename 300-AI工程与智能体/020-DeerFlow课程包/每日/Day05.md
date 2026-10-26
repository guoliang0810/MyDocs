# Day05（4×45min）：Artifacts 产物系统 + 本地 Sandbox（文件读写边界）

## 今日目标
- 定义“产物（artifact）”的元数据与落盘规则
- 让 Agent 能把结果写入 artifacts 并通过 API 下载/查看
- 实现 LocalSandboxProvider：限制读写在 thread 目录内（防路径穿越）

---

## 第1节（45min）：什么是 Artifacts（为什么 DeerFlow 很强调它）
### 课件
1. 对话只是过程，产物才是交付（markdown、json、图片、代码）
2. 产物需要：可追溯（谁生成）、可复现（输入是什么）、可下载（API）
3. 元数据最小集合：id、thread_id、path、type、created_at

### 当堂练习
- 设计 3 种 artifact type：`report.md`、`data.json`、`plan.md`

---

## 第2节（45min）：实现 artifacts 存储（先简单：文件系统）
### 课件
1. 为什么用每线程目录：隔离、清理、权限边界
2. 为什么要“虚拟路径”：对外统一 `/mnt/user-data/...`（概念先有）

### 课堂跟做
规则建议：
- 每个 thread 有目录：`artifacts/{thread_id}/`
- 文件名：`YYYYMMDD-HHMMSS-title.md`（或 uuid）
- 写入前：校验扩展名/type（白名单）

新增 API（示例）：
- `GET /threads/{thread_id}/artifacts`：列元数据
- `GET /threads/{thread_id}/artifacts/{artifact_id}`：取内容或下载

---

## 第3节（45min）：LocalSandboxProvider（最小安全边界）
### 课件
1. Sandbox 抽象：`read_file/write_file/list_dir/execute_command`
2. 初学者先做 Local 版：核心是路径校验 + 限制能力集
3. 路径穿越攻击：`../../secret` 怎么拦

### 课堂跟做
实现本地沙箱（建议能力）
- `read_file(path)`
- `write_file(path, content)`
- `list_dir(path)`

硬规则：
- 只能访问 thread 的 `workspace/ uploads/ artifacts/` 子目录
- `..`、绝对路径、盘符跳转一律拒绝

当堂练习：
- 试一次写入合法路径成功
- 试一次 `../` 路径失败，并返回统一错误结构

---

## 第4节（45min）：把 artifacts 写入变成一个工具（write_artifact）
### 课件
1. 为什么 artifacts 写入也要走工具：可控、可审计、可复用
2. 让模型产出结构化：标题、摘要、正文、引用（先约束格式）

### 课堂跟做
新增工具：
- `write_artifact(title, content, extension="md") -> artifact_meta`
内部调用 LocalSandboxProvider 写文件，并返回元数据给模型。

---

## 当天作业
### 必做
- artifacts 按 thread 落盘，并能通过 API 列出与读取
- LocalSandboxProvider 完成路径边界防护（至少防 `..`）
- `write_artifact` 工具可用（演示：让 agent 生成一份 `report.md`）

### 选做
- artifacts 元数据写入一个 `index.json`（每 thread 一份）
- 增加 `delete_artifact`（谨慎：需要权限/确认）

### 提交物
- `artifacts/{thread_id}/...` 至少 1 个 markdown 产物
- `scripts/smoke.md`：演示一次“生成产物→API 下载→本地打开”

### 自测
- 你能解释：为什么 sandbox 的第一要务是“边界”吗？
- 你能解释：为什么产物比对话更接近“工程交付”吗？

---

## 老师教案
- 今天一定要现场演示一次“路径穿越被拦截”，让学生建立安全意识
- 产物格式不要追求华丽，先把“可下载可复现”做出来

