# 大模型基础核心原理 (LLM Foundation)

## 1. AI 发展演进：从 1.0 到 2.0

### 1.1 传统 AI (AI 1.0)
- **特点**: 专用模型 (Specialized Models)，针对特定任务（如人脸识别、推荐系统）训练。
- **局限**: 泛化能力差，一个模型只能干一件事；依赖大量标注数据。
- **代表**: CNN (图像), RNN/LSTM (早期 NLP)。

### 1.2 生成式 AI (AI 2.0 / GenAI)
- **特点**: 通用基础模型 (Foundation Models)，通过海量数据预训练，具备跨任务的泛化能力。
- **能力**: 涌现 (Emergence) 能力，如推理、代码生成、创意写作。
- **代表**: GPT-4, Claude 3, Llama 3, DeepSeek。

## 2. GPT 与 Transformer 架构

### 2.1 Transformer：大模型的基石
> "Attention is All You Need" (2017)
- **核心机制**: 自注意力机制 (Self-Attention)。模型可以同时关注输入序列中的所有位置，捕捉长距离依赖关系。
- **并行计算**: 相比 RNN，Transformer 可以并行训练，极大提升了训练效率和规模。

### 2.2 GPT (Generative Pre-trained Transformer)
- **路线**: Decoder-only 架构（只用 Transformer 的解码器部分）。
- **预训练 (Pre-training)**: 预测下一个 Token (Next Token Prediction)。通过阅读互联网海量文本，学习语言规律和世界知识。
- **Scaling Law**: 模型参数量、数据量、计算量越大，模型效果越好（且呈现幂律关系）。

## 3. 大模型训练三部曲

1.  **预训练 (Pre-training)**
    -   **输入**: 海量无标注文本 (TB 级)。
    -   **产出**: Base Model (基座模型)。
    -   **特点**: 懂语言，有知识，但不懂指令，只会续写。

2.  **有监督微调 (SFT - Supervised Fine-Tuning)**
    -   **输入**: 高质量的指令-回复对 (Instruction-Response Pairs)。
    -   **产出**: Chat Model (对话模型)。
    -   **特点**: 学会听懂指令，按人类意图对话。

3.  **人类反馈强化学习 (RLHF - Reinforcement Learning from Human Feedback)**
    -   **输入**: 人类对模型回答的排序/打分。
    -   **产出**: 对齐人类价值观的模型 (Helpful, Honest, Harmless)。
    -   **特点**: 更符合人类偏好，减少有害输出。

## 4. 常见大模型对比 (2026 视角)

| 模型 | 厂商 | 特点 | 适用场景 |
| :--- | :--- | :--- | :--- |
| **GPT-4o / GPT-5** | OpenAI | 综合能力最强，多模态原生 | 复杂推理，通用任务 |
| **Claude 3.5 Opus** | Anthropic | 长文本能力强，幻觉少，代码强 | 文档分析，编码助手 |
| **Llama 3 (Open)** | Meta | 最强开源模型，生态丰富 | 私有化部署，微调 |
| **DeepSeek-V3** | 深度求索 | 性价比极高，中文能力强，开源 | 国内应用，高频调用 |
| **Qwen 2.5** | 阿里 | 全能型开源，多语言支持好 | 企业级应用 |

## 5. 核心术语表
- **Token**: 大模型处理文本的最小单位（约 0.75 个英文单词，0.5 个汉字）。
- **Context Window (上下文窗口)**: 模型一次能处理的最大 Token 数量（输入+输出）。
- **Temperature**: 控制输出随机性的参数。0 最稳定，1 最有创意。
- **Hallucination (幻觉)**: 模型一本正经地胡说八道。
