# Day14（4×45min）：Skills 系统（发现/加载/命名冲突/能力注入）

## 今日目标
- 设计 Skills 的最小规范：metadata + prompt + tools 绑定（可简化）
- 实现 skills 发现与加载：从目录扫描并生成“可用技能列表”
- 处理命名冲突：同名技能怎么选、怎么提示

---

## 第1节（45min）：Tool vs Skill（为什么要再抽一层）
### 课件
1. Tool：一个动作（函数/接口）
2. Skill：一组能力的“打包”：描述、约束、示例、可用工具
3. Skill 解决的问题：
   - 给模型更稳定的能力提示
   - 给 UI 更清晰的能力入口
   - 给团队协作更明确的扩展点

### 当堂练习
- 设计一个技能：`research_report`，写出它包含的 3 个工具与输出模板

---

## 第2节（45min）：定义 Skill 规范（最简版本）
### 课件
1. 初学者建议用文件约定：
   - `skills/<skill_name>/SKILL.md`
   - （可选）`skills/<skill_name>/manifest.json`
2. 最小字段：
   - name、display_name、description、example、prompt_snippet

### 课堂跟做
实现一个 SkillParser：
- 输入：SKILL.md 文本
- 输出：Skill 对象（name/description/prompt_snippet）

当堂练习：
- 写 1 个 SKILL.md（手写即可），能被 parser 解析出 name

---

## 第3节（45min）：SkillsLoader（扫描与加载）
### 课件
1. loader 负责：扫描目录、解析文件、构建索引
2. 冲突治理：
   - 同名技能：按优先级目录（custom > public）覆盖
   - 或：保留两个版本并提示用户选择

### 课堂跟做
实现：
- `discover_skills(root_dir) -> list[skill_path]`
- `load_skills(root_dir) -> dict[name, skill]`

并新增 API：
- `GET /skills`：返回技能列表

---

## 第4节（45min）：能力注入（把 skill 变成 prompt 的一部分）
### 课件
1. 注入位置：system prompt 的“能力区”
2. 注入内容：技能摘要 + 使用规则 + 示例（不要太长）
3. 注入策略：只注入“启用的 skills”，避免提示词膨胀

### 课堂跟做
实现：
- `apply_skills_to_system_prompt(system_prompt, enabled_skills) -> new_prompt`

当堂练习：
- 启用 `research_report` 技能后，让 agent 输出更结构化的报告

---

## 当天作业
### 必做
- skills 目录可扫描，至少 2 个技能可被列出
- 命名冲突有明确策略（覆盖或并存）
- skills 可注入 system prompt（可开关）

### 选做
- 给 skill 加版本号/作者字段
- 让 skill 绑定工具权限（启用 skill 自动启用对应工具组）

### 提交物
- `skills/` 下至少 2 个 SKILL.md
- `artifacts/day14_skills_list.json`：API 返回样例

### 自测
- 你能解释：为什么 skills 注入要可开关吗？

---

## 老师教案
- 今天强调“规范先行”：先约定文件结构与字段，再谈复杂功能

