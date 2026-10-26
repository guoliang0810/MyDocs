# Day13（4×45min）：Sandbox 加固（命令白名单/资源限制/虚拟路径）

## 今日目标
- 扩展 Sandbox：加入“能力开关”与“命令白名单”
- 实现路径虚拟化：对外统一虚拟路径，对内映射物理路径
- 为执行类工具加资源限制策略（先软限制：超时/输出大小）

---

## 第1节（45min）：Sandbox 的三层安全边界
### 课件
1. 第一层：路径边界（只在 thread 目录内）
2. 第二层：能力边界（只允许 read/write/list/exec 的一部分）
3. 第三层：资源边界（时间、输出大小、并发）

### 当堂练习
- 列出 5 个“必须禁止”的命令或操作（例如删除根目录、网络扫描）

---

## 第2节（45min）：虚拟路径设计（对外一致，对内隔离）
### 课件
1. 为什么要虚拟路径：让模型/工具“不知道你的真实机器路径”
2. 典型虚拟路径：
   - `/mnt/user-data/workspace`
   - `/mnt/user-data/uploads`
   - `/mnt/user-data/artifacts`

### 课堂跟做
实现两个函数（或等价）：
- `to_virtual_path(physical_path) -> vpath`
- `to_physical_path(thread_id, vpath) -> physical_path`

硬规则：
- vpath 必须以 `/mnt/user-data/` 开头，否则拒绝
- 映射后必须仍在 thread 的根目录下，否则拒绝

---

## 第3节（45min）：命令执行白名单（最小可用）
### 课件
1. “exec 工具”是最高危工具：先做白名单
2. 白名单策略：
   - 允许命令列表（例如 `python`, `node`, `ls`）
   - 禁止关键字（例如 `rm`, `shutdown`, `format`）
3. 初学者版本：先做“允许列表”，拒绝其他

### 课堂跟做
为 `execute_command` 增加：
- `allowed_commands: list[str]`
- `max_stdout_chars: int`
- `timeout_seconds: int`

当堂练习：
- 执行允许命令成功
- 执行非允许命令被拒绝（返回统一错误结构）

---

## 第4节（45min）：把 Sandbox 规则暴露成配置（可调可测）
### 课件
1. 安全策略必须配置化：不同环境不同策略
2. 配置不要放密钥：只放“策略参数”

### 课堂跟做
在 config 中加入：
- `sandbox.enabled`
- `sandbox.allowed_commands`
- `sandbox.timeout_seconds`
- `sandbox.max_stdout_chars`

---

## 当天作业
### 必做
- 虚拟路径映射完成并有单元自测（至少 3 个 case：正常/越界/非法前缀）
- execute_command 有白名单与超时，拒绝非法命令
- 拒绝时返回统一错误结构，并有日志记录（不泄漏敏感）

### 选做
- 增加输出截断策略（超过 max_stdout_chars 自动截断并标注）
- 为不同 tool 设置不同权限（exec 更严格）

### 提交物
- `artifacts/day13_sandbox_rules.md`：列出你的白名单与边界规则
- `scripts/smoke.md`：演示一次 exec 成功 + 一次被拒绝

### 自测
- 你能解释：为什么“虚拟路径”能提升安全与可移植性吗？

---

## 老师教案
- 今天必须让学生形成直觉：exec 工具默认不该开放

