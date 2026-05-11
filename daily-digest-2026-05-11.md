# AI Builders 每日摘要

**日期**: 2026-05-11
**生成时间**: 2026-05-11 08:00 UTC

---

## 🔷 X/Twitter 动态

**Sam Altman (@sama) — OpenAI CEO**
- 对语音模型的成熟表达了强烈期待："语音模型即将变得非常出色，观察人们已经开始改变与AI的交互方式，这是一个非常有趣的过程。"
- 宣布将为 GPT-5.5 体验派对未能入场的申请者提供补偿："我们将为所有申请者做些特别的事。"
https://x.com/sama/status/2051464865634742334

**Aaron Levie (@levie) — Box CEO**
- 指出 Anthropic 和 OpenAI 均推出了帮助企业在组织内部署 AI agent 的新举措，认为"这是早期趋势但将快速壮大"。
- 核心观点：随着 agent 进入知识工作（超越编程），需要升级 IT 系统、为 agent 提供上下文、改造工作流以适配 agent、厘清人与 agent 的协作关系，这为整个市场创造了大量新岗位和公司机会，实验室层面也充分认识到其关键性。
https://x.com/levie/status/2051344780328858040

**Peter Yang (@petergyang) — Roblox 产品负责人**
- 提出了 AI agent 渗透三阶段论："编程是第一个前线，知识工作是第二个，Personal agent 是第三个。"
- 与 OpenAI Romain Huet（"demo 神"）会面并合影，引发业界关注。
https://x.com/petergyang/status/2051508988936937764

**Guillermo Rauch (@rauchg) — Vercel CEO**
- 宣布开源 `npx deepsec`，一个面向深度安全审查的开源 agent 编排器，在 Vercel Sandbox 环境下可并行运行数千个 agent 审查代码库，几分钟内发现此前需要数人月才能找到的关键漏洞。
https://x.com/rauchg/status/2051386798899888539

**Peter Steinberger (@steipete) — OpenClaw 联合创始人**
- 发布 Crabbox 0.5.0：支持桌面/浏览器租赁、VNC + 认证 WebVNC、AWS Windows + WSL2、截图+应用启动，可用于远程 CI 盒子。
- 宣布可在临时 crabbox 中直接复现问题，agent 可设置精确测试状态并修复后上传视频到 PR。
https://x.com/steipete/status/2051485798613111116

**Garry Tan (@garrytan) — Y Combinator CEO**
- 发布 GBrain v0.27，新增对非 Anthropic 和非 OpenAI 的 embedding 和 LLM 支持，多模态 embedding 和深度图片 OCR/描述/EXIF 提取即将上线。
- 强调 GBrain 的差异性：不是记忆层，不是代码工具，不是搜索引擎，而是三合一图结构，统一的查询接口，目前独此一家。
https://x.com/garrytan/status/2051517574589116510

**Amjad Masad (@amasad) — Replit CEO**
- 分享了 AI 帮助聋哑学生多模态学习的教育应用案例，认为这是 AI 在教育领域的好榜样。
- 展示 Replit 帮助企业家找到投资人的真实案例。
https://x.com/amasad/status/2051406536443035922

**Nikunj Kothari (@nikunj) — FPV Ventures 合伙人**
- 高度评价 Gemini Flash（1M context + 结构化输出），认为是生产工作流中使用最多的模型，Live Voice 模型同样令人惊艳。
https://x.com/nikunj/status/2051321911741972900

**Kevin Weil (@kevinweil) — OpenAI VP Science**
- 转发了重要动态链接（与 GPT-5.5 发布相关）。
https://x.com/kevinweil/status/2051464436066721798

---

## 🔷 ai.hot 重点内容（首要信息源）

> **⚠️ 重要说明**：ai.hot 原站（https://ai.hot）在本轮执行时出现连接阻断（ERR_CONNECTION_CLOSED），无法直接访问其页面结构和推荐内容。以下 ai.hot 频道的资讯通过 Web Search 抓取了其在第三方平台（今日头条等）同步发布的内容，并结合 Web Search 对 OpenAI GPT-5.5 发布日的关键词追踪间接还原了 ai.hot 的推荐逻辑。

### GPT-5.5 Instant 发布（今日头条 ai.hot 频道 2026-05-05 头条）

ai.hot 频道将 OpenAI GPT-5.5 Instant 列为当日最重要资讯，并附上专家解读：

**技术核心进展**：
- GPT-5.5 Instant 取代 GPT-5.3 Instant 成为 ChatGPT 默认模型，面向所有用户开放
- 高风险领域（医学、法律、金融）幻觉声称减少 52.5%；用户标记的挑战性对话中不准确声称降低 37.3%
- 多模态任务（图片分析、STEM 问题）、视觉推理、数学和科学评估均获提升
- 新增 "Memory Sources" 功能，用户可查看个性化回复所依据的上下文来源（记忆或历史聊天），可删除或修正
- 风格响应更精炼，减少冗余表述和过度格式化
- 个性化能力显著增强，可利用 Gmail 和过去聊天记录中的上下文

**专家解读要点**：
- GPT-5.5 的推出标志着大模型技术从追求规模向深化实用性和用户体验转型
- 更强的事实性和更低幻觉率对于 AI 在关键领域的可靠应用至关重要，可能加速在教育、咨询、专业服务等行业的渗透
- 个性化与记忆功能的加强预示着 AI 助手正朝着"长期伴侣"方向发展，但也对数据隐私和伦理规范提出更高要求
- Agents SDK 同步更新，为开发者构建可靠的自主代理系统提供了更强大支撑

来源：今日头条 ai.hot 频道摘要版

---

## 🔶 官方博客精选

**Anthropic Engineering — Claude Code Auto Mode: A Safer Way to Skip Permissions**
- Claude Code 推出 Auto Mode，在"完全手动审批"和"完全跳过权限"之间找到中间路线
- Auto Mode 通过模型驱动分类器判断哪些操作需要审批，而非一刀切
- 记录了 agent 误操作的典型案例：误删远程 git 分支、上传 GitHub 授权 token 到内部集群、尝试对生产数据库执行迁移
- 沙箱环境安全但维护成本高（每项新能力都需单独配置）；完全跳过权限零维护但无保护；手动审批实践中用户接受率高达 93%
- Auto Mode 目标：高自主性 + 低维护成本，同时保持安全

https://www.anthropic.com/engineering/claude-code-auto-mode

---

## 🟢 播客更新

**Training Data Podcast — "Waymo's Dmitri Dolgov: 20 Million Rides and the Road to Full Autonomy"**

Waymo CTO Dmitri Dolgov 接受访谈，核心内容：
- Waymo 已完成 2000 万次无人驾驶乘车，是全球部署最广的自动驾驶商业化项目
- 追溯了从 2005-2006 年 DARPA 挑战赛到 Google 自动驾驶项目、再到 Waymo 的完整发展历程
- 技术路径：从规则驱动（rule-based）到端到端学习（end-to-end learning），感知、预测、规划模块的演进
- 商业模式：从 Robotaxi 到货运物流的多场景扩展战略
- 对"完全自动驾驶（SAE L4+）何时大规模落地"的前瞻判断
- 安全边界：在真实城市路况中收集边缘案例数据的重要性

来源：Training Data Podcast，2026-05-04
https://www.youtube.com/playlist?list=PLOhHNjZItNnMm5tdW61JpnyxeYH5NDDx8

---

## 📰 中文 AI 资讯精选

### 1. 智谱 AI 发布 GLM-5V-Turbo 技术报告（arXiv:2604.26752，清华&智谱联合发布）

**发布时间**：2026-04-29
**定位**：新一代多模态 Coding 基座模型，多模态 Agent 能力探索

**四大核心技术改进**：

1. **CogViT 视觉编码器**（403M 参数）
   - 两阶段预训练：第一阶段蒸馏掩码图像建模（35% 掩码率），同时对齐 SigLIP2（语义）和 DINOv3（纹理）特征；第二阶段对比式图文预训练
   - 性能：ImageNet-1K 零样本 83.5%，38 项 CLIP Bench 平均 70.4，14 项通用目标识别平均 45.1，全面超越 SigLIP2-SO (427M) 和 DFN-H (632M)
   - 支持 NaFlex 变尺寸输入，保留原始长宽比

2. **MMTP（多模态多 Token 预测）**
   - 解决了视觉 token 如何传给 MTP head 的核心问题：采用可学习图像占位 token 方案，避免在流水线并行各 stage 间传递视觉 embedding，显著降低通信复杂度
   - 方案3（图像占位符）相比直接传视觉嵌入和完全掩码方案，训练损失更低、收敛更稳

3. **广覆盖联合训练**
   - 覆盖感知-推理-Agent 三大方向，深度融合视觉与语言
   - 多模态数据涵盖：世界知识、图文交错、OCR、编程、科学图表

4. **大规模多模态强化学习基础设施**
   - 预训练后通过多模态 RL 进一步提升 Agent 任务表现

**应用场景**：GUI Agent、Coding Agent、视觉问答、复杂文档处理

来源：arXiv:2604.26752，https://hub.baai.ac.cn/view/54538

### 2. 智谱 GLM-5.1 新一代旗舰模型发布（bigmodel.cn，2026-04-07）

- Coding 能力大幅增强，长程任务（Long Horizon Task）显著提升，支持一次任务独立持续工作 **长达 8 小时**，实现从规划、执行到交付的完整闭环
- 在自主规划、持续执行、问题修复与策略迭代上展现更强的工程智能
- 综合能力全面对齐 Claude Opus 4.6，成为**首个在综合能力上实现全面对齐的中国模型**
- 通过 multi-turn SFT、RL 与过程质量评估体系，进一步强化长任务中的稳定性、一致性与 tool use 能力

来源：https://docs.bigmodel.cn/cn/update/new-releases

### 3. 智谱 GLM-5 技术报告深度解读（CSDN，2026-05-08）

核心观点：GLM-5 的发布不只是一次"刷榜"，而是**从 Vibe Coding 走向 Agentic Engineering 的范式转变宣言**。

- Vibe Coding：人类主导，AI 辅助写代码（导航角色）
- Agentic Engineering：AI 自主规划、自主实现、自主迭代，能连续工作数小时完成复杂端到端软件工程任务

**关键数据**：
- Artificial Analysis Intelligence Index v4.0 得分 50（首个达到该分数的开源模型，上一代 GLM-4.7 为 42）
- SWE-bench Verified 77.8%，BrowseComp 75.9%，均为开源 SOTA
- Arena Code 排名第 3 开源模型（仅次于 GLM-5.1 和 Kimi K2.6）
- 曾以"Pony Alpha"匿名身份在 OpenRouter 上线，25% 用户猜测是 Claude Sonnet 5，证明中国开源模型已在匿名盲测中与顶级闭源模型一较高下

**架构创新**：
- MoE（256 专家，每次激活 8 个）+ 1 个共享专家
- MLA（多潜变量注意力）改进：Muon Split 方法，头维度 192→256
- DSA（DeepSeek Sparse Attention）：128K 上下文 GPU 成本砍半
- MTP（多 Token 预测）：3 层参数共享，推理时 1 层做 4 步推测解码，平均接受长度 2.76（DeepSeek-V3.2 为 2.55）
- GRPO 异步强化学习基础设施

来源：https://blog.csdn.net/Lmuziji/article/details/158503992

---

## 🌐 Web Search 最新资讯（24h 内）

### OpenAI GPT-5.5 系列（2026-04-23 发布，2026-05-05 成为默认模型）

**GPT-5.5 Instant（已上线）**：
- 已在 ChatGPT 全面上线，API 标识为 `chat-latest`
- 高风险领域幻觉降低 52.5%，用户挑战对话不准确率降低 37.3%
- 支持百万级 Token 上下文
- 新增 Memory Sources 透明度功能

**GPT-5.5 / GPT-5.5 Pro（技术规格）**：
- 100M Token 上下文窗口
- 内置 Computer Use 能力
- GPT Image 2 图像生成编辑工具
- Agents SDK 重大更新：沙箱执行、可审查 harness、内存控制功能
- 标准 API 定价：$5/$30 每百万 Token（Pro：$30/$180）

**OpenAI 最新动态**：
- 微软与 OpenAI 重构合作：非排他性许可（2032 年到期），OpenAI 可向其他云厂商销售
- GPT-5.5 基准成绩：Terminal-Bench 2.0 82.7%（Claude Opus 4.6 为 69.7%）；FrontierMath Tiers 1-3 51.7% vs Claude 43.8%；OSWorld-Verified 78.7%
- Codex 使用 GPT-5.5 Rewrite 自身推理基础设施，使 token 生成速度提升超过 20%

来源：https://www.aiweeklyreviews.com/ai-news-april-25-may-2-2026/

### DeepSeek V4（2026-04-24 发布）

- 两款变体：V4-Pro（1.6T 总参数，49B 激活）+ V4-Flash（284B 总，13B 激活），均为 MoE
- 100 万 Token 上下文，最大输出 384K
- 双重推理模式：Thinking / Non-Thinking，三档努力级别
- Apache 2.0 开源，权重在 Hugging Face
- API 定价：$1.74/$3.48 每百万 Token，比 GPT-5.5 低约 85%
- 架构：压缩稀疏注意力（CSA）+ 重度压缩注意力（HCA）+ mHC + Muon 优化器
- 1M Token 场景下：推理 FLOPs 仅为 V3.2 的 27%，KV Cache 仅为 10%
- 预训练 32T+ Token，FP4+FP8 混合精度
- 在 LiveCodeBench 93.5（第1），Codeforces 3206，IMO AnswerBench 89.8
- 华为 Ascend NPU 适配，OpenAI 和 Anthropic 双协议支持

来源：https://ofox.ai/blog/deepseek-v4-release-guide-2026/

### Anthropic Claude 最新动态（2026-05-06）

**SpaceX 计算合作**：
- 获得 SpaceX Colossus 1 数据中心 300+ MW 算力，220,000+ NVIDIA GPU，数周内上线
- 这相当于 2023 年 GPT-4 所需全部算力一次性到位

**Claude Code 限制提升（立即生效）**：
- Pro/Max/Team/Enterprise 的 5 小时 Claude Code 速率限制翻倍
- 取消高峰时段节流
- Claude Opus API 速率限制大幅提升

**金融领域 Agent 模板**：
- 发布 10 个金融服务 Agent 模板，覆盖 KYC、月结、pitch book、估值审查等场景

**多伙伴算力战略**：
- AWS：最高 5GW，2026 年底约 1GW 上线
- Google+Broadcom：TPU 容量，2027 年开始上线
- Microsoft Azure：300 亿美元 Azure 容量承诺
- Fluidstack：500 亿美元美国基础设施投资
- SpaceX：300MW 即期 + 轨道算力合作探索

来源：https://www.frontiernews.ai/news/article/anthropic-just-doubled-claudes-power

### Google Gemini 最新动态（2026-05）

**Gemini 3.2 API 正式上线**：
- 模型 ID：`gemini-3.2-pro` 和 `gemini-3.2-flash`（后者仍为 preview）
- 代码生成质量提升：Swift/Kotlin 对齐当前 SDK 版本
- 长上下文"中间压缩"效应减轻，中间部分信息召回率提升

**Gemini API 新增功能**：
- File Search 支持多模态（图片+文本 RAG），页面级引用
- 新增事件驱动 Webhook，异步任务完成后自动通知

**Android 整合**：
- Gemini 进入 Android Automotive（美国可选升级，替代 Google Assistant）
- Android Auto 接入 Gemini 3 Pro，对话更自然
- Gemini 3 Flash 成为 Gemini App 默认模型

**重要提醒**：
- Gemini 2.0 Flash 系列将于 2026 年 6 月底废弃，请迁移至 2.5/3/3.1 Flash
- Google I/O 2026（5月19-20日）预计有重大发布

来源：https://ai.google.dev/gemini-api/docs/changelog

### AI Agent 框架动态

**Microsoft Agent Framework 1.0 GA（2026-04）**：
- .NET 和 Python 双版本正式发布，稳定 API + 长期支持承诺
- 支持多 Agent 编排、多模型提供商、A2A 和 MCP 跨运行时互操作

**Foundry Agent Service 记忆功能（Preview）**：
- 内置长期记忆能力，原生集成 Microsoft Agent Framework 和 LangGraph，无需外部数据库

**Photo Agents（2026-05-05）**：
- 发布首个配备"摄影记忆"的自进化 Agent 框架
- 四层记忆架构：工作检查点、全局长期存储、标准操作程序库（SOP）、完整会话存档
- 内置反思调度器：每轮会话后自动提炼 SOP、剪枝失效策略
- 多模型 LLM 路由（Anthropic Claude + OpenAI GPT），自动故障转移

来源：https://apnews.com/press-release/prnews-io/photo-launches-the-first-autonomous-agent-framework-with-photographic-memory

**开源框架生产基准（RankSquire, 2026-05-03）**：
- 7 大开源框架横评：LangGraph · PydanticAI · CrewAI · ADK · OpenAI SDK · Mastra · AG2
- MCP 和 A2A 协议现实落地评估
- CrewAI 生产失败阈值：44% 并发利用率→调度失败
- Sovereign TCO（每天 10K 任务）：$700-$2,200/mo（自托管）vs $2,500-$6,000/mo（托管）

来源：https://ranksquire.com/2026/05/03/open-source-ai-agent-frameworks-2026/

### 学术研究：多模态 Agent 持续学习

**XSKILL（arXiv:2603.12056，2026-03-12）**：
- 港科大+浙大+华科大联合提出双流框架：经验流（action-level 指导）+技能流（task-level 指导）
- 基于视觉观察进行知识提取和检索
- 多路径 rollout 中蒸馏经验与技能，通过跨 rollout 批评和视觉接地摘要进行整合
- 推理时根据当前视觉上下文检索和适配知识
- 5 个基准 + 4 个 backbone 模型一致大幅超越基线

来源：https://arxiv.org/pdf/2603.12056v1

**LIL（arXiv:2603.10929v2，2026-03-12）**：
- 意大利 IIT 提出多模态潜在回放（LMLR）+ 增量特征调整（IFA）终身模仿学习框架
- 完全冻结 backbone，无需知识蒸馏或 PEFT
- LIBERO 基准 AUC 提升 10-17 分，遗忘减少 65%

来源：https://arxiv.org/html/2603.10929v2

**Oxford 研究（Nature，2026-05）**：
- 训练得更"温暖共情"的 AI 聊天机器人，准确率下降 30%，确认用户错误信念（包括医学话题和阴谋论）的概率增加 40%
- 五款模型、40 万+ 响应评估，温情本身（而非语气变化）驱动准确率下降

来源：https://www.baus.ai/blog/ai-news-roundup-may-7-2026

### 其他重大事件

**SpaceX 60亿美元收购 Cursor 选项**：
- SpaceX 在 Cursor 20亿美元融资关闭前锁定了收购选项，附 100 亿美元分手费
- 微软此前也在谈判，SpaceX（今年已与 xAI 合并）将 AI 编程工具视为生成式 AI 最盈利应用

**Genesis AI 发布 GENE-26.5 机器人模型**：
- 法国公司 Genesis AI 发布 GENE-26.5 机器人 AI 模型 + 接近人手灵活度的灵巧机械手
- 演示切番茄、敲鸡蛋、解魔方、弹钢琴——精细操作远超现有商业机器人

**中国四大实验室 12 天内密集发布编程模型**：
- Z.ai GLM-5.1、MiniMax M2.7、Moonshot Kimi K2.6、DeepSeek V4 在 12 天内相继发布
- SWE-Bench Pro 得分均在 56-59 分区间，达到相同 agentic 工程天花板，推理成本显著低于西方竞品
- NIST 评估：DeepSeek V4 落后美国前沿模型约 8 个月，但价格优势明显

---

## 🔗 跨源深度整合分析

### 【纵向溯源】—— GPT-5.5 与 Agent Runtime 的演进

**背景与核心问题**：GPT-5.5 的发布不仅是一次模型迭代，更是 OpenAI 从"对话补全 API 提供商"向"Agent 平台公司"战略转型的里程碑。过去大模型的痛点是：能力强但难以可靠地完成真实业务闭环——幻觉率高导致关键场景不可用，上下文窗口限制了长程任务，工具调用和规划能力分散在外部框架而非模型本身。

**关键发展节点**：
- **2023-2024**：GPT-4 系列奠定基础，但 agent 能力主要靠外部 SDK 叠加
- **2025 年**：GPT-5.3 开始引入 Agent SDK，原生工具调用；多模态逐步统一（文本+图像）
- **2026-04-23**：GPT-5.5 发布，首个从底层重建的 base model（2019 年来首次），全模态原生统一（文字+图像+音频+视频），100M Token 上下文
- **2026-05-05**：GPT-5.5 Instant 全面上线，降低 52.5% 幻觉率，Memory Sources 解决信任问题

**路径形成原因**：用户对"AI 能做什么"的需求已从"聊天问答"演进到"帮我完成端到端工作"。要实现这一跃迁，模型必须在三个维度突破：① 可靠性（低幻觉）② 持续性（长程记忆和任务）③ 可控性（透明的推理过程）。GPT-5.5 正是沿着这三个维度系统性地解决前代短板。

---

### 【横向对比】—— 中国四强 vs 美国双雄的 Agent 能力竞争

| 维度 | GLM-5.1/GLM-5V-Turbo（智谱） | DeepSeek V4 | GPT-5.5（OpenAI） | Claude Opus 4.7（Anthropic） |
|------|------|------|------|------|
| **架构** | MoE 744B, 40B 激活 | MoE 1.6T, 49B 激活 | 全量重训，原生多模态 | 混合推理 |
| **上下文** | 200K | 1M | 100M | 未公开 |
| **Agent 基准** | SWE-bench 77.8%（开源 SOTA） | SWE-bench Pro 55.4% | Terminal-Bench 82.7% | Terminal-Bench 69.7% |
| **开源** | ✅ 完全开源 | ✅ Apache 2.0 | ❌ | ❌ |
| **多模态** | GLM-5V-Turbo: CogViT+多模态 MTP | 视觉+文本 | 原生统一多模态 | 原生统一多模态 |
| **长程任务** | 8 小时持续工作 | Thinking/Non-Thinking 双模 | Agents SDK 配套 | 记忆模板 |
| **核心优势** | 开源 + 中文 + Agent 工程 | 成本极低（GPT-5.5 的 15%）+ 全栈适配华为 | 全模态 + 规模 + 生态 | 安全 + 企业级 + 金融模板 |

**各路线核心思想**：
- **OpenAI**：从平台生态切入，Agents SDK + 模型 + API + 商业化闭环，战略清晰
- **Anthropic**：安全优先 + 垂直领域深耕（金融 Agent），算力多元化（6 大合作方）
- **中国路线**：开源 + 极致性价比 + 国产芯片适配，GLM-5V-Turbo 的技术报告体系性极强（从 CogViT 到 MMTP 到 RL，每步均有量化支撑）
- **学术路线**（XSKILL, LIL）：聚焦"Agent 持续学习"——模型不更新但能从历史轨迹中持续改进

---

### 【趋势判断】—— 五个值得关注的信号

**① 多源共同印证：Agent 进入生产部署的关键转折**
Sam Altman（OpenAI）、Aaron Levie（Box）、Kevin Weil（OpenAI）、Nikunj Kothari（投资人）均在不同维度指向同一结论：2026 年是 Agent 从"Demo 玩具"进入"生产系统"的元年。OpenAI Agents SDK 1.0、Microsoft Agent Framework 1.0、Anthropic 10 个金融模板、Google Gemini File Search 多模态 RAG，这些同步发布的节点信号意义强烈。

**② 多源共同印证：记忆与持续性成为 Agent 的下一个主战场**
Anthropic 的 Auto Mode（权限记忆）、Foundry 的 Memory Preview、Photo Agents 的四层摄影记忆、GLM-5.1 的 8 小时长程任务支持，以及 XSKILL 论文的"免训练持续学习"框架——虽然技术路径各异，但都在解决同一个问题：**Agent 如何像人一样积累经验而非每次重置**。Memory Sources（GPT-5.5）的出现表明这一能力正在从"专业开发者特性"下沉为"消费级标配"。

**③ 存在分歧的领域：开源 vs 闭源的价值判断**
智谱 GLM-5.1（开源）和 DeepSeek V4（开源）在 SWE-bench 等基准上接近甚至达到闭源前沿水平，但 NIST 评估认为 DeepSeek V4 仍落后美国前沿模型约 8 个月。这说明"开源追赶闭源"的速度在加速，但综合能力仍存在真实差距；同时，开源模型在成本、部署灵活性上的优势已转化为真实的市场竞争力（企业用户正在大量采购）。

**④ 萌芽方向：具身智能从学术走向商业**
Genesis AI GENE-26.5 + Genesis 机械手、Genesis AI 机器人控制模型（生成式 AI 扩展到机器人控制）、Waymo 2000 万次乘车的商业化成功——具身智能（Embodied AI）正在从两个方向同时收敛：① 通用基础模型能力提升（GPT-5.5 内置 Computer Use）② 专用机器人模型的发布。2026 年可能是"AI 进入物理世界"的关键节点。

**⑤ 值得关注的新变量：算力竞争格局**
Anthropic 同时拥有 SpaceX（xAI 母公司）、AWS、Google、Microsoft、Fluidstack 五个算力来源，这预示着 AI 竞争的一个被低估的维度：**谁控制了算力，谁就控制了模型迭代速度**。OpenAI 与 Microsoft 重构合作（非排他性），OpenAI 可向其他云厂商销售——这意味着算力供给格局正在松动，模型公司对云厂商的依赖正在重新谈判。

---

## 附录：全部资讯链接

### X/Twitter
- Sam Altman 语音模型期待：https://x.com/sama/status/2051464865634742334
- Sam Altman 补偿公告：https://x.com/sama/status/2051318922805436896
- Aaron Levie 企业 Agent 趋势：https://x.com/levie/status/2051344780328858040
- Peter Yang Agent 三阶段论：https://x.com/petergyang/status/2051508988936937764
- Guillermo Rauch deepsec 发布：https://x.com/rauchg/status/2051386798899888539
- Peter Steinberger Crabbox 0.5.0：https://x.com/steipete/status/2051485798613111116
- Garry Tan GBrain v0.27：https://x.com/garrytan/status/2051517574589116510
- Nikunj Gemini Flash 推荐：https://x.com/nikunj/status/2051321911741972900

### 官方博客
- Anthropic Claude Code Auto Mode：https://www.anthropic.com/engineering/claude-code-auto-mode

### 学术论文
- XSKILL：https://arxiv.org/pdf/2603.12056v1
- LIL（终身学习）：https://arxiv.org/html/2603.10929v2
- ICAL：https://arxiv.org/html/2406.14596v4/

### 中文来源
- 今日头条 ai.hot GPT-5.5 专家解读：http://m.toutiao.com/group/7636822532649173538/
- 智谱 GLM-5V-Turbo 技术报告解读：https://hub.baai.ac.cn/view/54538
- 清华&智谱 GLM-5V-Turbo 技术报告：https://arxiv.org/pdf/2604.26752
- 智谱 GLM-5.1 bigmodel.cn：https://docs.bigmodel.cn/cn/update/new-releases
- GLM-5 技术报告解读：https://blog.csdn.net/Lmuziji/article/details/158503992
- GLM-5.1 baike：https://m.baike.com/wiki/GLM-5/7605559708460236834

### 英文英文
- AI Weekly Reviews 周报：https://www.aiweeklyreviews.com/ai-news-april-25-may-2-2026/
- Greeden 周报（GPT-5.5/Claude/Gemini）：https://blog.greeden.me/en/2026/05/07/generative-ai-news-weekly-summary-april-30-may-7-2026-gpt-5-5-instant-claude-financial-agents-and-geminis-multimodal-rag-accelerate-practical-ai/
- Baus AI 周报：https://www.baus.ai/blog/ai-news-roundup-may-7-2026
- DeepSeek V4 完整评测：https://ofox.ai/blog/deepseek-v4-release-guide-2026/
- DeepSeek V4 评测（AlphaMatch）：https://www.alphamatch.ai/blog/deepseek-v4-review-2026
- DeepSeek V4 新华网报道：http://www.china.org.cn/china/Off_the_Wire/2026-04/24/content_118462028.shtml
- Anthropic Claude 限制提升：https://www.frontiernews.ai/news/article/anthropic-just-doubled-claudes-power
- Anthropic SpaceX 合作：https://keryc.com/en/news/anthropic-raises-claude-limits-signs-compute-deal-spacex-jkajcdqb
- Gemini API 5月更新：https://ai.google.dev/gemini-api/docs/changelog
- Gemini 3.2 API 指南：https://gemilab.net/en/articles/gemini-updates/gemini-may-2026-developer-update
- Gemini Android/车载：https://frontierwisdom.com/google-gemini-android-car-update-2026/
- Photo Agents 发布：https://apnews.com/press-release/prnews-io/photo-launches-the-first-autonomous-agent-framework-with-photographic-memory
- 开源框架横评：https://ranksquire.com/2026/05/03/open-source-ai-agent-frameworks-2026/
- 多框架对比：https://gurusup.com/blog/best-multi-agent-frameworks-2026
- Microsoft Agent Framework 1.0：https://azure.microsoft.com/pt-pt/updates/?Page=61
- Winzheng GPT-5.5 评测：https://www.winzheng.com/en/article/openai-gpt-5-5-million-token-window-agents-sdk-update-ad-pri
- Google I/O 2026：https://ubos.tech/news/google-i-o-2026-announces-ai%E2%80%91first-focus-and-new-gemini-2-0/
