# Embedding 模型选型

> **摘要**：2026 年 Embedding 模型选型实测，覆盖 Gemini、Jina、Qwen、BGE、OpenAI 等十大模型。本主题整合选型框架和关键结论。

## 背景：Embedding 为什么重要

Embedding 是 [[AI Agent 架构]] 中检索增强生成（RAG）和知识图谱的基础。选错 Embedding 模型，下游所有检索和推理质量都会受损。

## 2026 年十大 Embedding 模型实测

| 模型 | 维度 | 最大长度 | 中文能力 | 英文能力 | 多语言 | 价格 |
|------|------|---------|---------|---------|--------|------|
| Gemini Embedding | 768 | 8K | ★★★★ | ★★★★★ | ★★★★★ | 低 |
| Jina Embedding v3 | 1024 | 8K | ★★★ | ★★★★ | ★★★★ | 中 |
| Qwen Embedding | 1536 | 8K | ★★★★★ | ★★★★ | ★★★★ | 低 |
| BGE-M3 | 1024 | 8K | ★★★★★ | ★★★★ | ★★★★ | 开源免费 |
| OpenAI text-embedding-3-large | 3072 | 8K | ★★★ | ★★★★★ | ★★★★ | 高 |
| Cohere Embed v3 | 1024 | 512 | ★★ | ★★★★ | ★★★★ | 中 |

## 选型建议

1. **中文为主场景**：Qwen Embedding 或 BGE-M3
2. **英文为主场景**：Gemini Embedding 或 OpenAI
3. **多语言混合**：Gemini Embedding（性价比最优）
4. **成本敏感**：BGE-M3（开源免费，可本地部署）
5. **长文档检索**：Jina Embedding v3（8K 上下文）

## 与其他主题的关联

- → [[AI Agent 架构]]：GBrain 使用多模态 Embedding 构建知识图谱
- → [[知识库构建]]：Embedding 是知识库检索的核心

## 原始材料索引

1. 2026 年，Embedding 要怎么选？（实测 Gemini、jina、Qwen、BGE、OpenAI 十大模型）
