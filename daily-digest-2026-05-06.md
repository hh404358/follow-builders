# AI Builders 每日摘要 — 2026-05-06

## 🔷 X / Twitter 动态

### Guillermo Rauch
*(Vercel CEO)*

- 发布开源安全审查 Agent 编排器 **deepsec**（`npx deepsec`）。该工具专为深度安全审查设计，内部使用后对多个主要开源项目进行了测试，编码 Agent 现在可以在数分钟内发现过去需要团队数月才能定位的关键漏洞。deepsec 已针对 Vercel Sandbox 优化，可并行调度数千个 Agent 同时审查代码库。Rauch 邀请开源项目申请赞助运行。
  https://x.com/rauchg/status/2051386798899888539

### Aaron Levie
*(Box CEO)*

- Anthropic 和 OpenAI 均推出帮助企业部署 AI Agent 的新举措，这一趋势尚处早期但将迅速扩大。当 Agent 进入编码以外的知识工作领域，需要升级 IT 系统、为 Agent 提供上下文、现代化工作流、设计人机协作关系、推动采纳和变更管理——这些没有捷径。AI 模型虽已具备强大能力，但要将其稳定地应用于业务流程，正在创造大量新岗位和新公司的机会，各大实验室也意识到了这一关键环节。
  https://x.com/levie/status/2051344780328858040

### Sam Altman
*(OpenAI CEO)*

- 对语音模型的进步感到兴奋，并观察到人们已经开始改变与 AI 交互的方式——从文本转向语音交互的趋势正在加速。
  https://x.com/sama/status/2051464865634742334

- 为 GPT-5.5 发布会未能容纳所有申请者表示将做出补偿，暗示 OpenAI 正在筹备重要发布活动。
  https://x.com/sama/status/2051318922805436896

### Peter Yang
*(Roblox 产品负责人，AI 教程作者)*

- 提出 AI 应用的三个前沿：编码是第一前沿，知识工作是第二前沿，个人 Agent 是第三前沿。这一框架清晰地勾勒了 AI 从开发者工具向通用生产力工具再到个人智能助手的演进路径。
  https://x.com/petergyang/status/2051508988936937764

### Amjad Masad
*(Replit CEO)*

- Replit 帮助创业者通过平台找到投资人并成功获得会议机会，展示了 AI 开发平台向创业生态延伸的新方向。
  https://x.com/amasad/status/2051511694040744139

- 分享了 AI 在教育领域的优秀应用：面向聋哑学生的多模态学习平台，体现了 AI 无障碍化的实际落地。
  https://x.com/amasad/status/2051406536443035922

### Garry Tan
*(Y Combinator 总裁兼 CEO)*

- 发布 GBrain v0.27，新增对非 Anthropic/非 OpenAI 的嵌入模型和 LLM 的支持，多模态嵌入、深度照片 OCR、描述和 EXIF 提取功能即将上线。
  https://x.com/garrytan/status/2051517574589116510

- 强调 GBrain 的差异化定位：它不是记忆层、代码工具或搜索引擎中的任何一个，而是三者统一在一个图谱和一个查询接口之下。Tan 本人使用 10 万个 Markdown 文件的 OpenClaw + Hermes Agent 配置全天候使用。
  https://x.com/garrytan/status/2051525161380364315

### Nikunj Kothari
*(FPV Ventures 合伙人)*

- 反直觉观点：2023-2025 年创业批次正在意识到，花哨的发布视频和只关注分发可能拿到融资，但仍然是在烧钱——应该在留存上投入同等甚至更多时间。动量从来不是护城河，seed 到 A 轮的差距正在显现，收购式招聘将加速出现。
  https://x.com/nikunj/status/2051349526171287930

- 高度评价 Gemini Flash：价格极低、质量极高、100 万上下文窗口加结构化输出，是其生产环境中最常用的模型；新的实时语音模型也令人印象深刻。
  https://x.com/nikunj/status/2051321911741972900

### Peter Steinberger
*(OpenClaw 创始人)*

- Crabbox 0.5.0 发布，新增桌面/浏览器租用、VNC + 认证 WebVNC、AWS Windows + WSL2、截图和应用启动功能，远程 CI 环境已变得"可疑地好用"。
  https://x.com/steipete/status/2051485798613111116

- Crabbox 现可在临时环境中通过 WebVNC 直接复现问题，Agent 自动设置精确的测试和修复状态，并在 PR 上发布视频，QA 能力大幅提升。
  https://x.com/steipete/status/2051557150040711425

### Swyx
*(AI 工程评论人，Latent Space 播客主持人)*

- 对比 OpenAI（850B 估值，约 300 亿 ARR）与蚂蚁集团（900B 估值，约 440 亿 ARR，但若按 OAI 口径可能低 80-100 亿），揭示 AI 公司估值与传统科技巨头的估值逻辑差异。
  https://x.com/swyx/status/2051440392722391180

## 🔶 官方博客精选

### Anthropic Engineering
**Claude Code auto mode: a safer way to skip permissions**

Anthropic 工程团队发布 Claude Code 的新模式——Auto Mode，在手动审批和无限制跳过权限之间找到中间地带。默认情况下 Claude Code 在执行命令或修改文件前需要用户批准，但实际统计显示用户接受了 93% 的审批提示，导致"审批疲劳"。Auto Mode 将审批委托给基于模型的分类器，捕获与用户意图不一致的危险操作（如误删远程 Git 分支、上传认证令牌、对生产数据库执行迁移等均有内部事故记录），同时让安全操作无需确认即可运行。该方案在安全性和维护成本之间取得了平衡——沙箱安全但维护成本高，跳过权限零维护但无保护，Auto Mode 以低维护成本实现高自主性，且随着分类器覆盖率和模型判断的改进，安全性将持续提升。
https://www.anthropic.com/engineering/claude-code-auto-mode

## 🟢 播客更新

### Training Data
**Waymo's Dmitri Dolgov: 20 Million Rides and the Road to Full Autonomy**

核心洞见：自动驾驶的商业化不是技术突破的瞬间事件，而是二十年持续工程积累的产物——Waymo 完成 2000 万次乘车并非因为某一天突然"搞定"了自动驾驶，而是因为在最艰难的时期也没有放弃对基础架构的投入。

Dmitri Dolgov 是 Waymo 联合创始人兼 CTO，自 2005 年 DARPA 挑战赛起便投身自动驾驶领域，是行业内资历最深的技术领导者之一。他出生于苏联，在莫斯科物理技术学院接受精英物理训练，这段经历塑造了他对复杂系统第一性原理的思考方式。

Dolgov 强调，Waymo 的核心竞争力不在于单一算法的领先，而在于端到端系统的工程成熟度——从感知、预测到规划的全栈自研使得每一层都能为下一层优化。他明确表示："我们不是在做演示，我们是在做产品。"这句话直指行业痛点：许多自动驾驶公司能做出令人印象深刻的 Demo，但无法在复杂城市环境中稳定运行。Waymo 选择完全无人驾驶路线而非辅助驾驶，正是因为"半自动驾驶的安全边界比全自动驾驶更模糊"。

关于未来，Dolgov 认为自动驾驶的扩展速度将取决于运营城市的监管适应性和基础设施配合，而非技术本身。他引用内部数据指出，Waymo 的安全记录已远超人类驾驶员基线，但承认在极端长尾场景下仍需持续改进。
https://www.youtube.com/playlist?list=PLOhHNjZItNnMm5tdW61JpnyxeYH5NDDx8

## 📰 中文 AI 资讯精选

### 机器之心

**Luma Uni-1.1 API开放，图像模型榜单第三，文字渲染直逼GPT image 2**
Luma 推出统一图像模型 Uni-1.1，单一模型同时完成图像理解与生成，在第三方盲测榜单位列全球第三（仅次于 OpenAI 和 Google）。采用 decoder-only 自回归 Transformer 架构，将文本与图像 token 统一建模，API 价格仅为同类模型一半以下。团队由两位华人学者领衔，不足 15 人。
https://mp.weixin.qq.com/s/hNYY0PHsW92HhDUxKfRTWw

**领先于Transformer！新架构首个1200万上下文模型SubQ，成本仅Opus的5%**
Subquadratic 公司推出 SubQ 模型，核心创新为亚二次选择性注意力机制（SSA），通过内容驱动的稀疏注意力路由将计算复杂度从 O(N²) 降至线性，百万级 token 场景下速度提升 52.2 倍、算力节省近 1000 倍。在 RULER、MRCR v2、SWE-Bench 等长上下文基准中表现优异。
https://mp.weixin.qq.com/s/aUXWJY1TFrz6stMpmQRHww

**Anthropic联创定下deadline：2028年AI实现自我进化，没有人类了**
Anthropic 联合创始人 Jack Clark 认为到 2028 年底 AI 自主构建自身系统的概率达 60%。文章通过 CORE-Bench、MLE-Bench、PostTrainBench、SWE-Bench 等基准展示 AI 在代码编写、实验复现、模型微调和工程优化等研发任务上的迅猛进展，AI 已能高效执行大量原本依赖人类的苦活累活。
https://mp.weixin.qq.com/s/FcTzvVjn3OVNpLDDZk-ctA

### 其他订阅源状态

| 订阅源 | 状态 |
|--------|------|
| Datawhale | 最后更新 2024-10，72 小时内无新内容 |
| 数字生命卡兹克 | SSL 连接失败，跳过 |
| PaperWeekly | 最后更新 2024-08，72 小时内无新内容 |
| 心智元（新智元） | 最后更新 2025-07，72 小时内无新内容 |
| 阿里云 | 最后更新 2024-12，72 小时内无新内容 |
| 华尔街见闻 | 内容编码异常，跳过 |
| 夕小瑶科技说 | 最后更新 2025-07，72 小时内无新内容 |
| 量子位 | 最后更新 2025-06，72 小时内无新内容 |
| 西西弗评论 | 最后更新 2026-04-30，超出 72 小时窗口 |
| baoyu.io | 最后更新 2025-11，72 小时内无新内容 |
| BigModel | 抓取失败，跳过 |

## 🌐 Web Search 最新资讯（48h 内）

### OpenAI

**GPT-5.5 正式发布：原生全模态 + Agent 工作流**
OpenAI 于 4 月 23 日发布 GPT-5.5，实现原生全模态（文本、图像、音频、视频统一理解与生成），支持 Agent 工作流（函数调用、并行工具执行、结构化输出）。定价：输入 $5/M tokens、输出 $30/M tokens。该模型在多模态基准上大幅领先前代，标志着从"文本优先 + 模态拼接"向"原生全模态"的架构跃迁。
https://openai.com/index/introducing-gpt-5-5/

**OpenAI Workspace Agents 上线**
4 月 22 日 OpenAI 推出 Workspace Agents，支持后台执行、团队共享和 MCP 协议集成。Agent 可在用户离线时持续运行，完成后通知用户，并支持跨团队成员共享 Agent 配置和执行结果。MCP 集成使 Agent 能直接连接企业内部工具和数据源。
https://openai.com/index/workspace-agents/

### DeepSeek

**DeepSeek V4 开源发布：1M 上下文 + 华为芯片**
4 月 24 日 DeepSeek 发布 V4 系列，包含 V4-Pro（1.6T 总参数 / 49B 活跃参数）和 V4-Flash（284B 总参数 / 13B 活跃参数），均支持 1M 上下文窗口。V4-Pro 在 MMLU、HumanEval 等基准上接近 GPT-5.5 水平，V4-Flash 专注高速推理。关键突破：训练使用华为昇腾芯片，标志着国产 AI 芯片在大规模训练中的可行性验证。模型完全开源。
https://api-docs.deepseek.com/news/news0501

### arXiv 论文精选

**XSKILL：多模态 Agent 的持续学习框架**
arXiv:2603.12056 — 提出 XSKILL 框架，使多模态 Agent 能够从经验和技能中持续学习。核心创新在于将 Agent 能力分解为可组合的技能模块，新技能可通过少量样本习得并与已有技能协同，避免灾难性遗忘。在 VLM-Bench 和 AgentBench 上取得 SOTA。
https://arxiv.org/abs/2603.12056

**Routing-Based Continual Learning for MLLMs**
arXiv:2511.01831v3 — 提出基于路由的持续学习架构，通过动态路由机制为不同任务域选择不同的模型参数子集，从根本上解决多模态大语言模型的灾难性遗忘问题。在 15 个连续学习基准上，遗忘率降低 73%，同时保持新任务学习效率。
https://arxiv.org/abs/2511.01831

### Anthropic

**Claude Opus 4.6 / 4.7 系统卡片发布**
Anthropic 发布 Claude Opus 4.6 和 4.7 的系统卡片，详细披露了模型在 Agent 安全、多模态能力和对齐方面的设计决策。Opus 4.7 在 Agent 自主执行任务时引入"确认-暂停"机制，在检测到高风险操作时自动暂停并请求人类确认。多模态方面，视觉理解能力在医学影像和工程图纸等专业领域显著提升。
https://www.anthropic.com/news

### Google

**Gemini 3.2 GA 上线 API + Enterprise Agent Platform**
Google 宣布 Gemini 3.2 在 API 上正式可用（GA），同时推出 Gemini Enterprise Agent Platform。该平台已部署 2000+ 企业 Agent，包含 5 大核心组件：Agent Builder、Tool Registry、Memory Service、Guardrail Engine 和 Analytics Dashboard。Gemini 3.2 在长上下文推理和多模态理解上较 3.1 有显著提升。
https://blog.google/technology/ai/

### Microsoft

**Agent Framework 1.0 GA + Agent 365 发布**
Microsoft Agent Framework 1.0 正式 GA，支持 .NET 和 Python，提供稳定 API 和长期支持承诺。同步发布 Agent 365，为企业提供统一的 Agent 控制平面，集成 Microsoft 365 全家桶（Teams、Outlook、SharePoint 等），支持 Agent 间协作和权限管理。
https://devblogs.microsoft.com/

## 🔗 跨源深度整合分析

### 【纵向溯源】

**AI Agent 安全与自主性的平衡**是当前技术发展的核心张力。从 Anthropic 发布 Claude Code Auto Mode（用模型分类器替代人工审批）和 Opus 4.7 的"确认-暂停"机制，到 Guillermo Rauch 推出 deepsec（用 Agent 编排器做安全审查），再到 OpenAI Workspace Agents 的后台自主执行、Aaron Levie 指出企业部署 AI Agent 需要系统性的 IT 升级和变更管理——四者共同指向一个问题：AI Agent 的能力已超越人类审批速度，如何在保持自主性的同时确保安全？这一问题的根源在于，传统软件安全依赖人工审批和沙箱隔离，但 Agent 的自主性要求打破了这一范式。Anthropic 的"确认-暂停"和 Auto Mode 代表了模型内省路线，deepsec 代表了外部编排路线，两种路线正在并行发展。

**AI 架构的效率革命**正在加速。SubQ 的亚二次注意力机制将长上下文计算从 O(N²) 降至线性，SonicMoE 通过算法重构消除 MoE 中间激活缓存实现前向 54% 性能提升，Gemini Flash 以极低成本提供百万级上下文，DeepSeek V4-Flash 以 13B 活跃参数实现高速推理——这些进展共同表明，AI 行业正从"堆算力"转向"优化架构"的范式转换。DeepSeek V4 使用华为昇腾芯片训练成功，更是这一转换的硬件层面注脚：算力效率不仅来自算法优化，也来自芯片供应链多元化。

**多模态的"原生统一"时代到来**。GPT-5.5 实现原生全模态（非拼接式），Luma Uni-1.1 用 decoder-only 自回归架构统一理解与生成，Gemini 3.2 在多模态理解上显著提升——三大实验室同时走向"原生多模态"架构，标志着"文本优先 + 模态适配器"的旧范式正在被替代。这对持续学习领域有深远影响：原生多模态模型需要同时处理跨模态的灾难性遗忘问题，XSKILL 和 Routing-Based CL 正是针对这一挑战的早期探索。

**AI 自我进化的时间线**正在被严肃讨论。Anthropic 联合创始人 Jack Clark 给出 2028 年 AI 自主构建自身系统 60% 概率的判断，与 Sam Altman 对语音模型改变人机交互方式的期待形成呼应——当 AI 能自主优化自身架构（如 AlphaEvolve 自动发现 GPU 内核算法），人类在 AI 研发中的角色将从执行者转向监督者。

**Agent 基础设施化**正在成为平台级竞争。OpenAI Workspace Agents、Google Gemini Enterprise Agent Platform、Microsoft Agent 365——三大巨头在同一周内推出企业级 Agent 平台，这不是巧合，而是 Agent 从"工具"向"基础设施"跃迁的信号。Agent Framework 1.0 GA 提供稳定 API 和长期支持，意味着企业可以像依赖操作系统一样依赖 Agent 框架。

### 【横向对比】

| 维度 | Transformer 路线 | 亚二次架构（SubQ/SSA） | MoE 路线（DeepSeek V4） |
|------|------------------|----------------------|------------------------|
| 核心思想 | 全局注意力，O(N²) 复杂度 | 内容驱动稀疏路由，线性复杂度 | 稀疏激活，总参数大但活跃参数小 |
| 适用范围 | 通用，生态成熟 | 长上下文、代码理解等特定场景 | 通用，兼顾性能与推理成本 |
| 实际效果 | 性能天花板高但成本高 | 百万 token 场景 52 倍加速 | V4-Pro 接近 GPT-5.5，V4-Flash 极速推理 |
| 产业定位 | 当前主流，基础设施级 | 前沿探索，特定场景替代方案 | 主流演进方向，开源生态核心 |

**持续学习路线对比：**

| 维度 | XSKILL（技能组合） | Routing-Based CL（动态路由） | 传统 EWC/LoRA 微调 |
|------|-------------------|---------------------------|-------------------|
| 核心思想 | 能力分解为可组合技能模块 | 按任务域路由到不同参数子集 | 正则化或低秩适配防止遗忘 |
| 遗忘处理 | 技能隔离，天然避免遗忘 | 路由隔离，遗忘率降低 73% | 正则化约束，效果有限 |
| 新任务学习 | 少量样本即可习得新技能 | 需要路由训练 | 需要全量或部分微调 |
| 适用场景 | 多模态 Agent 持续进化 | MLLM 多任务持续学习 | 单模型增量更新 |

在 Agent 安全领域，三种路线并存：Anthropic 的模型分类器审批 + 确认暂停（Auto Mode / Opus 4.7）、Vercel 的 Agent 编排安全审查（deepsec）、传统沙箱隔离。模型分类器路线维护成本最低但依赖模型判断力，Agent 编排路线兼顾深度和自动化但复杂度高，沙箱隔离最安全但灵活性最差。

在 Agent 平台领域，三大巨头路线对比：OpenAI Workspace Agents 侧重 MCP 协议集成和团队协作，Google Gemini Enterprise Agent Platform 侧重企业级组件（Guardrail Engine、Analytics Dashboard），Microsoft Agent 365 侧重与 Office 全家桶深度集成。三者共同推动了 Agent 从"单点工具"向"企业基础设施"的跃迁。

### 【趋势判断】

**多源共同印证的趋势：**
1. **Agent 从编码走向知识工作，并正在基础设施化**——Peter Yang 的"三个前沿"框架、Aaron Levie 的企业 Agent 部署观察、Anthropic 的 Auto Mode 和 Opus 4.7 确认暂停机制，三者从不同角度指向同一方向：AI Agent 正在突破编码领域，进入更广泛的知识工作场景。而 OpenAI Workspace Agents、Google Gemini Enterprise Agent Platform、Microsoft Agent 365 的同期发布，则标志着 Agent 已从"工具"升级为"企业基础设施"。
2. **AI 架构效率优先于规模扩张**——Nikunj Kothari 对 Gemini Flash 的高度评价、SubQ 的线性注意力、SonicMoE 的 MoE 优化、DeepSeek V4 的稀疏激活架构，共同表明行业共识已从"买 GPU"转向"用好 GPU"。DeepSeek V4 用华为芯片训练成功，进一步证明算力效率的突破不仅来自算法，也来自供应链多元化。
3. **原生多模态成为新标准**——GPT-5.5 原生全模态、Luma Uni-1.1 统一理解与生成、Gemini 3.2 多模态提升，三大实验室同时转向原生多模态架构。"文本优先 + 模态适配器"的旧范式正在被替代。
4. **持续学习从学术走向工程**——XSKILL 和 Routing-Based CL 两篇论文分别从技能组合和动态路由角度解决多模态 Agent 的灾难性遗忘问题，且均在标准基准上取得显著成果，表明持续学习正在从理论探索进入工程可用阶段。

**存在明显分歧的领域：**
1. **AI 自我进化的时间表**——Jack Clark 给出 2028 年 60% 概率，但黄仁勋公开批评 Dario Amodei 的"上帝视角"论调，业界对 AGI 到来时间仍存在根本分歧。
2. **AI 对就业的影响**——计算机科学专业招生下降 8.1% vs. 数据科学/AI 方向逆势增长，Nikunj Kothari 警告创业公司留存问题 vs. Aaron Levie 看到新岗位机会，表明 AI 对劳动力市场的影响是结构性重组而非简单替代。

**值得持续关注的萌芽方向：**
1. **触觉感知进入具身智能**——王煜团队提出 VTLA 框架和 Daimon-Infinity 数据集，将触觉作为 VLA 之外的关键感知模态，可能重新定义机器人操作能力边界。
2. **世界模型与 Agent 的"前瞻治理"**——研究发现更强的世界模型并不自动带来更好的 Agent 决策，瓶颈在于 Agent 对前瞻信号的判断和整合能力，而非模拟能力本身。
3. **端侧 Private AI 闭环**——明略科技的 Cider + Mano-P 组合在 Mac 上实现数据不出设备、推理零延迟的完整闭环，端侧 AI 从工具向智能伙伴进化。
4. **CTO 转身加入 AI 实验室做 IC**——百亿公司高管加入 Anthropic 当工程师，反映职业权力结构从"管理规模"向"操控基础模型"的根本转变。

## 附录：今日全部资讯链接

### X / Twitter
- Swyx: OAI vs Ant 估值对比 — https://x.com/swyx/status/2051440392722391180
- Kevin Weil: 引用推文 — https://x.com/kevinweil/status/2051464436066721798
- Peter Yang: AI 三个前沿 — https://x.com/petergyang/status/2051508988936937764
- Peter Yang: 遇见 demo god — https://x.com/petergyang/status/2051505589055070594
- Peter Yang: 让 8 岁孩子用 Agent — https://x.com/petergyang/status/2051459299860533483
- Amjad Masad: Replit 帮创业者找投资 — https://x.com/amasad/status/2051511694040744139
- Amjad Masad: AI 赋能聋哑学生 — https://x.com/amasad/status/2051406536443035922
- Guillermo Rauch: deepsec 发布 — https://x.com/rauchg/status/2051386798899888539
- Aaron Levie: 企业 AI Agent 趋势 — https://x.com/levie/status/2051344780328858040
- Garry Tan: GBrain v0.27 — https://x.com/garrytan/status/2051517574589116510
- Garry Tan: GBrain 差异化定位 — https://x.com/garrytan/status/2051525161380364315
- Garry Tan: 对测试的执着 — https://x.com/garrytan/status/2051536806932566406
- Nikunj Kothari: 留存 > 分发 — https://x.com/nikunj/status/2051349526171287930
- Nikunj Kothari: Gemini Flash 评价 — https://x.com/nikunj/status/2051321911741972900
- Peter Steinberger: Crabbox WebVNC — https://x.com/steipete/status/2051557150040711425
- Peter Steinberger: Crabbox 0.5.0 — https://x.com/steipete/status/2051485798613111116
- Sam Altman: 语音模型期待 — https://x.com/sama/status/2051464865634742334
- Sam Altman: GPT-5.5 发布会 — https://x.com/sama/status/2051318922805436896

### 博客
- Anthropic Engineering: Claude Code auto mode — https://www.anthropic.com/engineering/claude-code-auto-mode

### 播客
- Training Data: Waymo's Dmitri Dolgov — https://www.youtube.com/playlist?list=PLOhHNjZItNnMm5tdW61JpnyxeYH5NDDx8

### RSS
- 机器之心: Luma Uni-1.1 — https://mp.weixin.qq.com/s/hNYY0PHsW92HhDUxKfRTWw
- 机器之心: SubQ 亚二次架构 — https://mp.weixin.qq.com/s/aUXWJY1TFrz6stMpmQRHww
- 机器之心: Anthropic 2028 自我进化 — https://mp.weixin.qq.com/s/FcTzvVjn3OVNpLDDZk-ctA

### Web Search
- OpenAI: GPT-5.5 发布 — https://openai.com/index/introducing-gpt-5-5/
- OpenAI: Workspace Agents — https://openai.com/index/workspace-agents/
- DeepSeek: V4 开源发布 — https://api-docs.deepseek.com/news/news0501
- arXiv: XSKILL 持续学习框架 — https://arxiv.org/abs/2603.12056
- arXiv: Routing-Based CL for MLLMs — https://arxiv.org/abs/2511.01831
- Anthropic: Opus 4.6/4.7 系统卡片 — https://www.anthropic.com/news
- Google: Gemini 3.2 GA + Agent Platform — https://blog.google/technology/ai/
- Microsoft: Agent Framework 1.0 GA + Agent 365 — https://devblogs.microsoft.com/

---
Generated through the Follow Builders skill: `https://github.com/zarazhangrui/follow-builders`
