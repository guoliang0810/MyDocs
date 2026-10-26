# Day21（4×45min）：毕业项目整合 + 答辩脚本 + 故障演练

## 今日目标
- 把 Mini-DeerFlow 整体串起来：线程→消息→工具→产物→记忆→子任务→事件
- 准备一份“可复现演示脚本”（一键 smoke + 演示数据）
- 做 3 个故障演练：超时、权限不足、摘要失败降级

---

## 第1节（45min）：毕业验收清单（今天只做“收口”）
### 课件
1. 毕业验收必须满足：
   - 多步研究任务产出 report.md
   - 子任务并行并聚合
   - 长期记忆生效
   - sandbox 边界有效
2. 一个工程能否交付，取决于：能否稳定复现

### 当堂练习
- 选一个你最担心的验收点，写出“如何证明它 OK”的演示步骤

---

## 第2节（45min）：一键演示脚本（从 0 到产物）
### 课件
1. 演示脚本内容：
   - 启动服务
   - 创建 thread
   - 上传文件（可选）
   - 发起研究任务（planner/executor/checker）
   - 下载 artifacts（report、summary）

### 课堂跟做
实现 `scripts/demo.py`（或等价），支持：
- `--base-url`
- `--thread-id`（可选）
- 输出最终报告的下载链接/路径

当堂练习：
- 让脚本最后打印“验收结果清单”（每项 PASS/FAIL）

---

## 第3节（45min）：故障演练（让系统“优雅失败”）
### 课件
1. 工程能力来自失败处理，而不是成功路径
2. 三个必演练故障：
   - 工具超时（例如 exec/tool timeout）
   - 权限不足（高危工具被拒绝）
   - 摘要失败（降级裁剪仍可继续）

### 课堂跟做
给每个故障增加“可观测输出”：
- 日志有 trace_id + error_type
- events 里有 error 事件
- artifacts 里有 gap/summary（可选）

---

## 第4节（45min）：答辩脚本（像架构师一样讲清楚取舍）
### 课件
1. 5 分钟讲解结构：
   - 目标与边界
   - 架构图（3 层）
   - 核心链路（一次消息从进到出）
   - 安全策略（sandbox/permissions）
   - 可观测与回归（events/tests/smoke）
2. 架构师常问 3 问：
   - 你为什么这么拆？
   - 你的边界在哪里？
   - 你的降级策略是什么？

### 课堂跟做
产出 3 个最终 artifacts：
- `final_architecture.md`
- `final_demo_script.md`
- `final_failure_drills.md`

---

## 当天作业（毕业提交）
### 必做
- demo 脚本可一键跑通（至少在你机器上）
- 3 个故障演练能复现，并输出可观测证据
- 最终 3 份答辩 artifacts 完成

### 选做
- 打包成 Docker compose（老师机器一键跑）
- 增加简单前端页面（列 threads、history、artifacts、events）

### 提交物
- 代码仓库
- `scripts/demo.py`
- `artifacts/final_*` 三份文档

### 自测
- 你能在 5 分钟内讲清楚：middleware、sandbox、skills、memory、subagents 各自解决什么问题吗？

---

## 老师教案
- 今天不要再加新功能，只做“稳定 + 可复现 + 可讲清楚”

