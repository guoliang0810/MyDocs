# Day16（4×45min）：模块边界与分层（Gateway vs Runtime vs Providers）

## 今日目标
- 把项目按职责分层，减少“互相引用一团糟”
- 明确三层边界：
  - Gateway（HTTP/鉴权/响应）
  - Runtime（编排/状态/中间件）
  - Providers（sandbox/memory/skills 的具体实现）
- 形成一张“架构图 + 依赖方向”作为团队协作依据

---

## 第1节（45min）：为什么架构师天天讲“边界”
### 课件
1. 无边界：改一处，处处裂
2. 有边界：可替换、可测试、可演进
3. 依赖方向：上层依赖抽象，下层提供实现

### 当堂练习
- 把你当前项目文件按三层分一分，写出每层的职责一句话

---

## 第2节（45min）：定义抽象接口（让实现可替换）
### 课件
1. 抽象不是为了优雅，是为了隔离变化
2. 典型抽象：
   - `Sandbox` 接口
   - `MemoryStore` 接口
   - `SkillLoader` 接口

### 课堂跟做
做一次小重构（不追求全做完，先把骨架立住）：
- runtime 只依赖接口，不直接 import 本地实现
- gateway 通过依赖注入/工厂函数拿到 runtime 实例

当堂练习：
- 用“假实现”替换 memory store（例如内存版）跑通测试

---

## 第3节（45min）：配置的分层覆盖（默认→环境→请求）
### 课件
1. 为什么配置会失控：硬编码、散落、覆盖逻辑混乱
2. 分层覆盖示例：
   - default：仓库默认
   - env：部署环境
   - request：单次请求 override（例如 model_name）

### 课堂跟做
实现配置加载顺序（最简）：
- `load_default()`
- `apply_env_override()`
- `apply_request_override()`

---

## 第4节（45min）：输出“架构图”与“依赖规则”
### 课件
1. 架构图不是画给别人看的，是用来指导重构与协作
2. 依赖规则示例：
   - gateway 不可 import provider 的私有模块
   - provider 不可 import gateway

### 课堂跟做
产出 2 份 artifacts：
- `architecture.md`：三层职责 + 模块列表
- `dependency_rules.md`：依赖方向规则与例子

---

## 当天作业
### 必做
- 项目分层清晰（至少主模块按三层组织）
- runtime 依赖抽象接口（至少对 sandbox/memory 之一）
- 产出架构图与依赖规则 artifacts

### 选做
- 用静态检查（简单脚本）扫描禁止依赖（例如 grep import 规则）

### 提交物
- `artifacts/day16_architecture.md`
- `artifacts/day16_dependency_rules.md`

### 自测
- 你能解释：为什么“上层依赖抽象”会让项目更可维护吗？

---

## 老师教案
- 今天是“从能跑到能维护”的转折点，不要怕重构，但要小步验证

