# AI Agent 架构

> **摘要**：2026 年 AI Agent 框架进入"架构选型"阶段，OpenClaw、Hermes、Claude Code、DeerFlow、nanobot 各有侧重。本主题从源码级深度对比五大框架的核心架构决策，并分析 GBrain 作为"Agent 大脑"的差异化定位。

## 背景：Agent 架构为什么重要

Agent 不是"LLM + 工具调用"的简单组合。架构决策决定了：
- **可靠性**：单 Agent vs 多 Agent，集中式 vs 分布式
- **可观测性**：执行链路追踪、状态回滚
- **可扩展性**：工具注册、技能组合、上下文管理
- **安全性**：权限边界、操作审批、沙箱隔离

## 五大框架源码级对比

| 维度 | OpenClaw | Hermes | Claude Code | DeerFlow | nanobot |
|------|----------|--------|-------------|----------|---------|
| **核心思想** | 技能即分类，一切皆 Skill | 轻量级 Agent 编排 | 完整 Harness 工程 | 流式 Agent 工作流 | 极简 Agent 内核 |
| **架构模式** | 插件式技能注册 | ReAct 循环 | 主-子 Agent 层级 | DAG 工作流 | 单 Agent + 工具 |
| **上下文管理** | 全局技能图谱 | 对话历史窗口 | 分层上下文压缩 | 流式上下文传递 | 最小上下文 |
| **工具集成** | MCP 协议 | 函数调用 | 内置工具集 + MCP | 插件系统 | HTTP 工具调用 |
| **安全机制** | 沙箱隔离 | 人工审批 | 模型分类器 + 确认暂停 | 无内置 | 无内置 |
| **适用场景** | 通用 AI 助手 | 编程辅助 | 全栈 AI 编程 | 复杂工作流 | 轻量自动化 |
| **开源状态** | 开源 | 开源 | 闭源（源码已泄漏） | 开源 | 开源 |

## 核心架构决策分析

### 1. 单 Agent vs 多 Agent

- **单 Agent**（Hermes, nanobot）：简单可靠，但长任务容易"迷路"
- **主-子 Agent**（Claude Code）：主 Agent 规划，子 Agent 执行，可靠性高但复杂度高
- **DAG 工作流**（DeerFlow）：任务分解为有向无环图，并行执行，适合确定性流程

→ 关键洞察：**Agent 数量不是越多越好，而是与任务复杂度匹配**。简单任务用单 Agent，复杂任务用主-子模式，确定性流程用 DAG。

### 2. 上下文管理策略

- **窗口截断**（Hermes）：简单但丢失早期信息
- **分层压缩**（Claude Code）：auto-compact 自动压缩旧上下文，保留关键信息
- **图谱检索**（OpenClaw/GBrain）：将信息存入知识图谱，按需检索

→ 关键洞察：**上下文管理是 Agent 可靠性的基石**。→ 详见 [[Claude Code 与 Harness Engineering]]

### 3. 工具集成范式

- **MCP 协议**（OpenClaw, Claude Code）：标准化工具注册和调用，生态最广
- **函数调用**（Hermes）：轻量但缺乏标准化
- **内置工具集**（Claude Code）：开箱即用但扩展性受限

## GBrain：Agent 的"大脑"

YC 总裁 Garry Tan 开源的 GBrain v0.27 定位为 Agent 的记忆和检索层：
- 不是记忆层、代码工具或搜索引擎中的任何一个，而是三者统一
- 底层是知识图谱 + 统一查询接口
- 支持多模态嵌入、深度照片 OCR、EXIF 提取
- Tan 本人使用 10 万 Markdown 文件 + OpenClaw + Hermes Agent 全天候运行

## 趋势判断

**多源共同印证**：
1. MCP 协议正在成为工具集成的行业标准
2. 上下文管理从"窗口截断"向"智能压缩+图谱检索"演进
3. Agent 安全从"人工审批"向"模型分类器"过渡

**存在分歧**：
1. 多 Agent 是否必要——Claude Code 坚持主-子模式，Hermes 认为单 Agent + 好工具足够
2. Agent 是否需要持久记忆——GBrain 认为必须，nanobot 认为无状态更可靠

**萌芽方向**：
1. Agent 间协作协议（A2A）可能成为下一个标准化方向
2. 世界模型作为 Agent 的"模拟器"进行前瞻决策

## 原始材料索引

1. AI Agent 架构怎么选？OpenClaw / hermes-agent / Claude Code / DeerFlow / nanobot 源码级深度对比
2. YC 总裁开源了自己亲手写的 AI Agent 大脑，1 周就 1 万点赞
3. 装了最近爆火的 Hermes，和 OpenClaw 的对比来了
4. Kimi K2.6 + Hermes 实测！Karpathy 同款保姆级教程来了
