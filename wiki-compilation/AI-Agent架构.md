# AI Agent架构

## 摘要

> 2026年是AI Agent爆发年。本周多篇深度文章对 OpenClaw、hermes-agent、Claude Code、DeerFlow、nanobot 等主流 Agent 架构进行源码级对比，揭示不同架构的设计哲学与适用场景。

## 背景

AI Agent 从单 Agent 向多 Agent 协作演进，架构选择成为核心竞争力。不同框架在任务分解、工具调用、记忆管理等方面各有特色。

## 发展节点

- **2024-2025**: 单 Agent 时代，ReAct、Plan-then-Execute 模式流行
- **2026年初**: 多 Agent 框架涌现，Harness Engineering 理念兴起
- **2026-04**: Hermes 发布，YC 总裁开源 AI Agent 大脑
- **2026-05**: Agent 评测基准发布，南大团队揭示模型真实能力

## 核心分析

### 主流架构对比

| 框架 | 设计理念 | 核心特点 | 适用场景 |
|------|---------|---------|---------|
| Claude Code | Harness Engineering | 精细化任务控制 | 代码开发 |
| Hermes | 简洁高效 | 轻量级实现 | 快速原型 |
| OpenClaw | 模块化 | 高度可扩展 | 企业应用 |
| DeerFlow | 研究导向 | 多跳推理 | 深度研究 |
| nanobot | 微服务 | 松耦合 | 复杂系统 |

### 架构演进趋势

1. **从规划到执行**: 减少 Plan 依赖，强调实时响应
2. **多 Agent 协作**: 主 Agent + 专家 Agent 分层
3. **工具生态**: MCP 协议统一工具接口
4. **记忆管理**: 向量数据库 + RAG 成为标配

### Karpathy 的观点

> "不喜欢 Plan 模式！人类必须负责 Plan！别去追 LLM 的逃逸速度，构建自己的 RL 环境！"

## 跨主题关联

- [[Claude Code与Harness Engineering]]：Claude Code 是 Agent 架构的典型代表
- [[DeepSeek技术]]：DeepSeek 在 Agent 推理优化上的探索
- [[Prompt Engineering与AI工作流]]：Agent 任务分解与 Prompt 设计

## 原始材料索引

### 架构对比
- [AI Agent 架构怎么选？OpenClaw / hermes-agent / Claude Code / DeerFlow / nanobot 源码级深度对比](https://mp.weixin.qq.com/s/qdnbKai0YHERpAnpg84Oeg)
- [YC 总裁开源了自己亲手写的 AI Agent 大脑，1 周就 1 万点赞](https://mp.weixin.qq.com/s/XZHiLs2wNJDGZPP-W2ESPg)

### Hermes 相关
- [一文带你看懂Harness Engineering是个啥](https://mp.weixin.qq.com/s/yI1rQHVwJqszdpadzAe_4A)
- [最新！万字综述Harness革命](https://mp.weixin.qq.com/s/0CTwb4aEr5mWwsdRdwzwkw)
- [装了最近爆火的 Hermes，和OpenClaw的对比来了](https://mp.weixin.qq.com/s/2YsgaHJmOsAuq8tDFlEOvg)

### Agent 评测
- [南大团队直击大模型高分神话：人类90分，最强模型仅49分](https://mp.weixin.qq.com/s/HRehP9A9AFs8quxcc2WVhQ)

### Agent 使用技巧
- [用好Agent最重要的技巧不是Skills，是这四个字](https://mp.weixin.qq.com/s/F7w9IWGSrCn2FbIgXoyvnA)

## 标签

#AIAgent #Agent架构 #多Agent #Harness
