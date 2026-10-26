---
title: Sim2Real 与物理 AI 落地
tags: [Sim2Real, 现实差距, 试验闭环]
status: active
updated: 2026-10-26
---

# Sim2Real 与物理 AI 落地

> 仿真能不能预测真实结果？这个问题在工业界长期只有一个模糊答案。
> **解法不是更准的模型，是更严格的对照设计。**

---

## 一、核心概念：SRCC（Sim-to-Real Correlation Coefficient）

目前唯一把"仿真能否预测真实结果"**形式化**的指标，由
**`2510.20808`**（*The Reality Gap in Robotics: Challenges, Solutions, and Best Practices*）提出。
作者团队含 Dieter Fox、Scaramuzza 等，已被 **Annual Review of Control, Robotics, and Autonomous Systems 2026** 接收。

### 该综述揭示的行业结构性事实

> "Most published robotics work reports success rates **within simulation alone or within real environments alone,
> not in paired comparisons** that would let you calculate the SRCC."

> ⭐ **翻译成大白话：绝大多数工作根本没做过配对对照，
> 所以"仿真能不能预测实物"这个问题，历史上基本没人能回答。**

---

## 二、⭐ 因此，专家一定会做的额外工作

### ① 建立"配对对照"数据采集规范

仿真与实物**必须跑同一组工况编号**，才能算相关系数。

> **这直接决定"仿真能不能预测实物"这个问题是否有答案。**
> 这是一条**流程要求**，不是一次研究——意味着交付流程必须从一开始就按工况编号组织。

### ② 把"现实差距"写进产品文档的置信度章节

不藏在附录里。客户有权在签署前知道差距有多大。

### ③ 标准化误差归因

区分开：

| 归因类别 | 典型表现 |
|---|---|
| 接触 / 摩擦 | 摩擦系数假设与实际不符 |
| 执行器延迟 | 时序误差 |
| 传感器噪声 | 幅值/频谱特征偏差 |
| 机械间隙与柔性 | 刚度模型简化过度 |
| 控制回路时序抖动 | 时序问题 |

### ④ 域随机化是工程手段，不是万能药

奠基工作：Tobin et al. 2017 IROS；
OpenAI 的 ADR（Automatic Domain Randomization, 2019）用于自动扩展随机化区间。
⚠️ 具体 arXiv 编号本次未逐一核实。

---

## 三、⭐ 工程仿真领域的等价物：试验闭环，而非域随机化

这是本节最关键的一条，也是清航飞迈三个标杆场景的共同方法论。

### C919 复材机翼

走的是 **"材料、设计、分析、工艺、装配、试验"全流程** 路径，
采用 **面向制造装配的设计（DFMA）理念**，
并通过**典型盒段和全尺寸盒段试验件**制造、装配进行验证；
试验采用 **T800 级复合材料高层级积木式试验**。

> ⭐ **这就是 Sim2Real 在工程仿真领域的等价物——用试验闭环替代域随机化。**
> 机器人领域靠域随机化补足现实差距；航空领域靠**实物试验**补足。
> 后者更贵，但结论的可信度等级完全不同。

### 骨科植入物

对应 **ASME V&V 40-2018** 风险框架。
**VVUQ 40.1-2026**（胫骨托组件疲劳试验最坏情况尺寸识别）提供了一个几乎可直接套用的范式。

### 医疗线的特殊要求

模拟器必须通过 **ASME V&V 40** 风险框架——
可信度应"commensurate with the degree to which the computational model is relied on as evidence of device performance,
functional characteristic, and/or safety to support a decision,
**and the consequences of that decision being incorrect**"。

---

## 四、⭐ 对标最强证据：Airbus 的盲预测

VVUQ 90 分委会成员 Javad Fatemi（Airbus Defence and Space，复材结构专家）在 NAFEMS 2026 UK 会议主旨演讲说明：

其案例研究是"**ESA 技术项目中的复材运载器发动机框架**，
用 VVUQ 框架成功对全尺寸发动机框架试验结果做了**盲预测**（blind prediction）"。

> ⭐ **盲预测是仿真可信度的最高形态**：
> 在拿到试验结果之前就用模型预测，然后检验误差。
> 这与"用试验数据校准后再预测"是完全不同的证据等级。
>
> **C919 场景应该追求的，正是这个等级的可核验证据。**

---

## 五、落地检查清单

- [ ] 仿真与实物/试验使用**同一套工况编号体系**
- [ ] 交付文档有独立的**置信度与现实差距**章节
- [ ] 误差归因表：接触、执行器、传感器、间隙柔性、时序，逐项说明
- [ ] 域随机化范围（如采用）与未覆盖区间的明确声明
- [ ] 已有试验数据时，评估是否能做**盲预测**并记录偏差
- [ ] 医疗线项目已对照 **ASME V&V 40** 的风险分级要求自检

---

## 🔗 相关

- [[代理模型与神经算子工程化]]
- [[仿真可信度V-V与标准体系]]
- [[FDE角色与工作标准]]
