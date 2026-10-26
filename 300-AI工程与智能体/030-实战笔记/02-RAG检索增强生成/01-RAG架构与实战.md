# RAG 检索增强生成 (Retrieval-Augmented Generation)

## 1. 为什么需要 RAG？

大模型 (LLM) 存在两个核心痛点：
1.  **知识截止 (Knowledge Cutoff)**: 模型的知识停留在训练结束的那一天。
2.  **幻觉 (Hallucination)**: 遇到不知道的问题，模型喜欢“一本正经地胡说八道”。
3.  **私有数据不可见**: 模型不知道你公司的内部文档或个人数据。

**RAG 的核心思想**: **考试允许翻书**。在回答问题前，先去知识库里找相关资料，然后把资料和问题一起给模型，让模型基于资料回答。

## 2. RAG 标准架构 (Naive RAG)

### 2.1 流程三步走
1.  **检索 (Retrieval)**: 根据用户问题，从向量数据库中找到最相关的 K 个文档片段。
2.  **增强 (Augmentation)**: 将检索到的片段 (Context) 插入到 Prompt 中。
3.  **生成 (Generation)**: LLM 基于增强后的 Prompt 生成答案。

### 2.2 数据处理流水线 (ETL)
1.  **加载 (Load)**: 读取 PDF, Word, HTML, Markdown 等源文件。
2.  **切分 (Split/Chunking)**: 将长文档切成小的文本块 (Chunk)。
    -   *策略*: 按字符数 (如 500 字符)、按段落、按语义。
    -   *Overlap*: 相邻 Chunk 之间保留重叠 (如 50 字符)，防止语义被切断。
3.  **嵌入 (Embedding)**: 使用 Embedding 模型将文本块转换为向量 (Vector)。
    -   *模型*: OpenAI `text-embedding-3`, BGE (BAAI), M3E。
4.  **存储 (Store)**: 将向量和元数据存入向量数据库 (Vector DB)。

## 3. 核心技术栈

| 组件                  | 推荐技术/工具                                                       |
| :------------------ | :------------------------------------------------------------ |
| **Embedding Model** | BGE-M3 (开源最强多语言), OpenAI Ada-002/Small                        |
| **Vector DB**       | **Milvus** (大规模/生产级), **Chroma** (轻量/本地), **Pinecone** (SaaS) |
| **Orchestration**   | **LangChain**, **LlamaIndex** (RAG 专用)                        |
| **App Platform**    | **FastGPT**, **Dify** (低代码构建 RAG 应用)                          |

## 4. Advanced RAG (进阶 RAG)

Naive RAG 容易遇到“检索不准”或“片段丢失上下文”的问题，进阶策略如下：

### 4.1 混合检索 (Hybrid Search)
同时使用 **关键词检索 (BM25)** 和 **向量检索 (Dense Retrieval)**，然后加权合并结果。
- *解决*: 向量检索对专有名词（如产品型号 "X-2000"）匹配不准的问题。

### 4.2 重排序 (Rerank)
先粗排检索出 Top 50 个文档，再用高精度的 **Rerank 模型** (如 BGE-Reranker) 对这 50 个文档精细打分，取 Top 5 给 LLM。
- *效果*: 大幅提升相关性，是提升 RAG 效果最立竿见影的手段。

### 4.3 查询转换 (Query Transformation)
用户的问题往往是不完整的。
- **Rewrite**: 将用户问题改写为更适合检索的形式。
- **HyDE (Hypothetical Document Embeddings)**: 让 LLM 先生成一个假设性答案，用假设答案去检索相似文档。
- **Multi-Query**: 将一个问题拆解为多个子问题分别检索。

## 5. 实战 Prompt 模板

```markdown
# Role
你是一个智能客服助手。

# Task
请仅根据提供的上下文信息 (Context) 回答用户的问题。
如果上下文中没有相关信息，请直接回答 "我不知道"，不要编造。

# Context
{{context}}

# Question
{{question}}

# Answer
```
