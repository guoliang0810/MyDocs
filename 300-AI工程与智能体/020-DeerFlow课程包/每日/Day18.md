# Day18（4×45min）：安全工程（输入校验/最小权限/密钥管理/红线清单）

## 今日目标
- 把安全变成“工程机制”：输入校验、权限模型、密钥不落盘
- 建立工具权限（permission scope）并在 gateway/runtime enforce
- 形成红线清单：哪些能力默认禁止、哪些必须二次确认

---

## 第1节（45min）：Agent 项目常见安全事故清单
### 课件
1. 路径穿越：读到不该读的文件
2. 命令注入：执行危险命令
3. 数据泄漏：密钥进入日志/产物
4. 过度权限：一个工具拿到全系统权限

### 当堂练习
- 写出你项目里“最危险的 2 个接口/工具”，并写出防护手段

---

## 第2节（45min）：输入校验（HTTP 层 + 工具层双保险）
### 课件
1. HTTP 层校验：schema、大小限制、mime 白名单
2. 工具层校验：参数类型、范围、枚举、必填项
3. 错误返回：统一结构 + 不泄漏内部细节

### 课堂跟做
补齐至少 3 个输入校验点：
- uploads：文件大小上限、扩展名/mime
- write_artifact：扩展名白名单、content 长度限制
- execute_command：allowed list + args 校验

---

## 第3节（45min）：最小权限（Permission Scopes）
### 课件
1. 权限模型示例：
   - `filesystem:read`
   - `filesystem:write`
   - `sandbox:exec`
   - `network:fetch`
2. 默认最小权限：不开 exec、不开 network
3. 权限的归属：
   - tool 定义需要什么权限
   - 请求/线程/用户决定是否授予

### 课堂跟做
实现权限检查：
- ToolRegistry 里为每个 tool 标注 `required_permissions`
- runtime 执行 tool 前检查 `granted_permissions`
- 不满足则返回“权限不足”错误结构

---

## 第4节（45min）：密钥管理与红线清单
### 课件
1. 密钥只来自环境变量/安全存储，不进入 config 文件
2. 日志脱敏：遇到 token/key 直接打码
3. 红线清单（默认禁止）：
   - 扫描内网/端口
   - 删除/覆盖系统文件
   - 输出用户隐私/密钥

### 课堂跟做
产出 artifacts：
- `security_redlines.md`：红线清单
- `permissions_matrix.md`：工具-权限矩阵

---

## 当天作业
### 必做
- 至少 5 个输入校验（HTTP+Tool 合计）
- 工具权限模型可用：无权限时被拒绝且错误可读
- 红线清单与权限矩阵 artifacts 完成

### 选做
- 增加“二次确认”机制：高危工具需显式确认字段
- 增加日志脱敏 middleware（简单正则即可）

### 提交物
- `artifacts/day18_security_redlines.md`
- `artifacts/day18_permissions_matrix.md`
- `scripts/smoke.md`：演示一次“无权限被拒绝”

### 自测
- 你能解释：为什么要“HTTP 层 + 工具层”双保险吗？

---

## 老师教案
- 今天不要怕讲“保守”，安全是后续能上线的前提

