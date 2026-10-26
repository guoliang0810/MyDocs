# Prompt Engineering 高级技巧

## 1. CoT (Chain of Thought)
让模型“一步步思考”。
> Prompt: "Let's think step by step."
> 进阶: "Please break down the problem into sub-tasks, solve each one, and then combine the results."

## 2. ReAct (Reason + Act)
Agent 的核心循环。
- **Thought**: 我需要做什么？（比如：查天气）
- **Action**: 调用天气 API。
- **Observation**: API 返回“北京，晴，25度”。
- **Thought**: 我现在知道了天气，可以回答用户了。
- **Action**: 回答“北京今天天气不错...”

## 3. Few-Shot Prompting (少样本提示)
不要只给指令，给几个示例 (Examples)。
- 示例是告诉 LLM “输出格式”和“推理风格”的最有效方式。

## 4. DSPy (Declarative Self-improving Language Programs)
- ⚠️ **归因修正（2026-10-26 核查）**：DSPy 论文发布于 **2023-10**（arXiv:2310.03714），
  **不是** 2025 年的产物。把它当作"2025 年趋势"是时间错挂。
- 核心思想：不手动微调 Prompt 里的词语，而是定义 **Metrics（评估标准）** 和 **Dataset**，
  让 DSPy 自动优化 Prompt。
- *观点*: "Prompt Engineering is dead. Long live DSPy."

### ⭐ 对 FDE 的真价值
把客户 PoC 的**验收指标直接写成 metric**，用 DSPy 自动优化 prompt，
而不是靠"我觉得这个 prompt 更好"来调。示例：

```python
# 伪代码：把验收判据变成可优化目标
metric = lambda out, ref: abs(out["target_value"] - ref["target_value"]) / ref["target_value"] < 0.05
dspy.Configure(lm=lm, optimizer=BootstrapFewShot(metric=metric))
```

> 与 [[100-物理AI产品与领域/020-领域知识/LLM在物理仿真中的角色边界]] 的关系：
> metric 可以是"数值是否由求解器算出"这类**结构性判据**，而非只看文本相似度。
