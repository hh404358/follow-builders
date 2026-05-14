
# AI Builders 每日摘要 - 2026年5月14日

---

## 🔷 X/Twitter 动态

### Swyx (@swyx)
- **分享**：OpenAI 与 Anthropic 的估值与收入对比
  - OpenAI 估值 ~8500亿美元，年营收约300亿美元
  - Anthropic 估值 ~9000亿美元，收入按不同计量方式差异较大（可能在80-100亿美元区间）
  - [推文链接](https://x.com/swyx/status/2051440392722391180)

### Guillermo Rauch (@rauchg)
- **产品更新**：Vercel 发布「deepsec」开源安全审查代理
  - 专门用于深度安全审查的开源工具
  - 支持多智能体协同工作
  - 目前已开源，可直接使用
  - [推文链接](https://x.com/rauchg/status/2051386798899888539)

### Aaron Levie (@levie)
- **观察**：Anthropic 和 OpenAI 均推出面向企业的 AI Agent 部署方案
  - 这是一个早期但增长迅速的趋势
  - 需要升级 IT 系统、让 Agent 获取上下文、现代化工作流程
  - 模型虽有强大能力，但在企业环境中落地需要很多实际工作
  - [推文链接](https://x.com/levie/status/2051344780328858040)

### Garry Tan (@garrytan)
- **产品更新**：GBrain v0.27 发布
  - 新增支持大量非 Anthropic 和非 OpenAI 的嵌入与 LLM
  - 多模态嵌入和深度图片 OCR、描述和 EXIF 提取功能即将推出
  - [推文链接](https://x.com/garrytan/status/2051517574589116510)

### Sam Altman (@sama)
- **评论**：对语音模型未来发展感到兴奋
  - 观察到人们已经在改变与 AI 的交互方式
  - [推文链接](https://x.com/sama/status/2051464865634742334)

### Nikunj Kothari (@nikunj)
- **观点**：Gemini Flash 的性价比非常出色
  - 价格亲民、质量良好、支持 1M 上下文和结构化输出
  - 可能成为生产环境中最常用的模型之一
  - [推文链接](https://x.com/nikunj/status/2051321911741972900)

### Peter Yang (@petergyang)
- **趋势**：编码→知识工作→个人代理，AI 应用路径清晰
  - [推文链接](https://x.com/petergyang/status/2051508988936937764)

### Peter Steinberger (@steipete)
- **产品更新**：Crabbox 0.5.0 发布
  - 支持桌面/浏览器租用、VNC 和认证 WebVNC、AWS Windows + WSL2
  - 截图和应用启动功能
  - [推文链接](https://x.com/steipete/status/2051485798613111116)

---

## 🔷 ai.hot 重点内容（最高优先级）

### ExploitGym: AI智能体能否将安全漏洞转化为真实攻击？
**来源**：Berkeley RDI博客
- **核心内容**：由伯克利 RDI、马普所安全隐私研究所、Anthropic、OpenAI 及谷歌团队合作发布的基准测试
- **关键发现**：前沿 AI 模型已能成功利用相当数量的真实漏洞
- **意义**：安全行业需要认真对待这一现实威胁
- [链接](https://rdi.berkeley.edu/blog/exploitgym)

### 阿里云 Qwen-Character 发布
**来源**：阿里云官方
- **核心功能**：支持记忆、共情和主动交互
- **适用场景**：游戏、虚拟 AI 伴侣、自适应学习
- **效果**：可提升用户参与度 50% 以上
- [链接](https://x.com/alibaba_cloud/status/2054653031472414864)

### Cursor 发布云端智能体开发环境
**来源**：Cursor Blog
- **核心更新**：
  - 多仓库环境支持，让智能体跨代码库协同工作
  - 基于 Dockerfile 的代码化配置，密钥和缓存优化
  - 命中缓存后构建速度提升 70%
  - 增强由智能体主导的环境设置流程
  - 新增环境治理与安全功能
- **意义**：企业落地智能体开发门槛大幅降低
- [链接](https://cursor.com/blog/cloud-agent-development-environments)

### Claude 代码周限额提升 50%
**来源**：ClaudeDevs
- **适用范围**：Pro、Max、Team 及按席位计费的企业用户
- **生效时间**：即日起至 7月13日
- [链接](https://x.com/ClaudeDevs/status/2054639777685934564)

### Claude 电脑与浏览器使用的最佳实践
**来源**：Claude 官方博客
- **核心指导**：针对 Claude 4.6 系列和 Opus 4.7 优化
- **关键建议**：
  - Claude 4.6 API限制：最大长边1568像素、总像素115万
  - Opus 4.7提升：最大长边2576像素、总像素375万
  - 推荐起始分辨率：1280x720
  - Opus 4.7用户优先使用 1080p
- **重要性**：这是能够直接减少 bug 的硬核文档
- [链接](https://claude.com/blog/best-practices-for-computer-and-browser-use-with-claude)

### 解决循环：语言和推理的吸引子模型
**来源**：arXiv 论文
- **核心突破**：解决循环 Transformer 训练不稳定、成本高和深度固定问题
- **架构创新**：
  - 主干模块生成初始输出嵌入
  - 吸引子模块迭代优化固定点
  - 隐式微分计算梯度，训练内存与有效深度无关
  - 迭代次数自适应收敛
- **性能数据**：
  - 语言建模：困惑度降低 46.6%，下游任务准确率提升 19.7%
  - 770M 参数模型性能优于 1.3B Transformer
  - 推理任务：2700 万小模型在数独和迷宫任务上准确率 91.4%/93.1%，超越 Claude 和 GPT o3
- **颠覆性亮点**：训练后模型可内化迭代过程，推理时直接一步到位
- [链接](https://arxiv.org/abs/2605.12466)

### Anthropic 首次在 B2B 采用率上超越 OpenAI
**来源**：The Decoder
- **数据依据**：Ramp AI 指数显示
  - Anthropic 美国企业客户采用率达 34.4%
  - OpenAI 为 32.3%
- **分析**：虽领先，但三个因素可能使其优势迅速减弱
- [链接](https://the-decoder.com/anthropic-overtakes-openai-in-b2b-adoption-for-the-first-time-according-to-ramp-spending-data)

### Meta 在 WhatsApp 推出硬件级端到端加密 AI 对话
**来源**：阿绎 AYi
- **核心创新**：
  - 与仅不保存历史记录的「临时聊天」不同
  - 对话推理完全在手机硬件安全飞地内进行
  - Meta 工程师无法获取明文
  - 不产生任何服务器日志
  - 会话结束后数据永久消失
- **意义**：这是推动 AI 从「玩具」转变为生活基础设施的关键一步
- [链接](https://x.com/AYi_AInotes/status/2054616319127904403)

### Runway 正式发布 Runway Agent
**来源**：Runway 新闻
- **核心功能**：通过单次对话将创意想法转化为完整可发布视频
- **工作流程**：
  - 自然语言描述需求
  - Agent 自主完成概念提案、节奏设计、视觉方向规划
  - 生成包含多场景、旁白、对话和音乐的成片
- **目标用户**：品牌团队、营销人员、创意机构、电影制作人
- **效果**：将数天/数周的制作周期压缩至几分钟
- **状态**：现已上线，新免费计划用户可获得 1500 积分
- [链接](https://runwayml.com/news/introducing-runway-agent)

### Anthropic 推出面向小型企业的 Claude 服务包
**来源**：Anthropic 新闻
- **核心功能**：
  - 连接器生态，集成 QuickBooks、PayPal、HubSpot 等工具
  - 15 个开箱即用的自动化工作流
  - 自动化处理财务、运营、销售等重复任务
- **操作方式**：通过 Claude Cowork 界面操作，用户手动批准关键步骤
- **价值**：AI 第一次真正为「深夜还在忙杂务」的人减负
- [链接](https://www.anthropic.com/news/claude-for-small-business)

---

## 🔶 官方博客精选

### Claude Code auto mode：更安全地跳过权限
**来源**：Anthropic Engineering
- **问题**：默认需要用户批准才能运行命令或修改文件，导致审批疲劳
- **解决方案**：Auto mode 是 Claude Code 的新模式，将审批委托给基于模型的分类器
- **目标**：捕捉不符合用户意图的危险操作，同时让安全的操作无需批准
- **定位**：在手动审查和无防护之间的中间地带
- [链接](https://www.anthropic.com/engineering/claude-code-auto-mode)

---

## 🟢 播客更新

### Waymo 的 Dmitri Dolgov：2000万次骑行与完全自主之路
**来源**：Training Data 播客
- **嘉宾**：Dmitri Dolgov (Waymo 负责人)
- **亮点**：Waymo 已完成 2000万次自动驾驶骑行
- **主题**：从早期 DARPA 挑战赛到今天的规模化部署历程
- [链接](https://www.youtube.com/playlist?list=PLOhHNjZItNnMm5tdW61JpnyxeYH5NDDx8)

---

## 📰 中文 AI 资讯精选

### OpenAI 发布 ChatGPT Agent，整合 Operator 和 DeepResearch
**时间**：2026-05-11
- **核心功能**：
  - 同时调度文本浏览器、图形界面浏览器和代码终端
  - 运行在虚拟机中
  - 执行前征求用户确认，可随时打断
  - 主动提问，数据不全时暂停
- **性能提升**：
  - HLE 测试：41.6 分
  - FrontierMath：27.4% 准确率
  - BrowseComp：比 DeepResearch 高 17.4 个百分点
- **开放范围**：Pro、Plus 和 Team 用户
- **额度**：Pro 用户每月 400 次，Plus/Team 40 次，可购买额外次数
- [链接](https://blog.csdn.net/jike007gt/article/details/1487538459)

### OpenAI 发布 GPT-Realtime-2，推理能力翻倍
- **核心升级**：首个宣称具有「GPT-5级推理」的语音模型
- **性能数据**：
  - Audio MultiChallenge 平均通过率：48.45%，领先 Gemini 3.1 Flash Live 超过 12 个百分点
  - 指令保留率：从 36.7% 跃升至 70.8%
- **上下文**：提升至 128K Tokens
- **定价**：音频输入 32 美元/百万 Token，输出 64 美元/百万 Token
- [链接](http://m.toutiao.com/group/7636936998229944986/)

### DeepSeek V4 预览版发布
**时间**：2026-04-24
- **双模型阵容**：
  - DeepSeek-V4-Pro：1.6T 总参数 / 49B 激活参数
  - DeepSeek-V4-Flash：284B 总参数 / 13B 激活参数
- **亮点**：
  - 1M 上下文窗口成为默认标配
  - Pro 在 Agentic 编码、世界知识、推理方面性能可与顶级闭源模型媲美
  - Flash 推理能力接近 Pro，成本更低、速度更快
- **结构创新**：Token 级压缩 + DSA（DeepSeek 稀疏注意力）
- **定价**：成本仅为 Claude Opus 4.7 的 1/20
- [链接](https://www.knightli.com/en/2026/04/24/deepseek-v4-preview-release/)

### 智谱 GLM-5.1 新一代旗舰模型上线
**时间**：2026-04-07
- **核心提升**：
  - 编码能力大幅增强
  - 长程任务显著提升，支持一次任务独立持续工作 8 小时
  - 实现从规划、执行到交付的完整闭环
- **综合能力**：全面对齐 Claude Opus 4.6
- **能力强化**：多轮 SFT、RL 和过程质量评估体系，强化长任务稳定性和工具调用能力
- [链接](https://docs.bigmodel.cn/cn/update/new-releases)

### Anthropic Claude 限额大调整
**时间**：2026-05-06
- **算力合作**：与 SpaceX 达成独家合作，租用其 Colossus 1 数据中心全部算力
  - 新增超 300 兆瓦容量、22 万张英伟达 GPU
- **额度调整**：
  - Claude Code 5 小时滚动限额翻倍
  - 取消 Pro/Max 高峰时段额度削减
  - Opus 模型 API 速率最高提升 16 倍
- **托管智能体升级**：
  - 多智能体编排
  - 目标结果 (Outcomes) 功能
  - 自主推演 (Dreaming) 能力（研究预览版）
- [链接](https://blog.csdn.net/qq_73472828/article/details/160867575)

### 谷歌发布 Gemini 3 Flash
**时间**：2026-05-12
- **定位**：「前沿智能，为速度而生」
- **性能**：
  - 响应速度比 2.5 Pro 快 3 倍
  - 运行成本仅为 Gemini 3 Pro 的四分之一
  - GPQA Diamond 得分 90.4%
  - Humanity's Last Exam 得分 33.7%
  - MMMU Pro 得分 81.2%（超过 3 Pro）
- **定价**：输入 0.50 美元/百万 Tokens，输出 3.00 美元/百万 Tokens
- [链接](https://blog.csdn.net/guorui_java/article/details/156079428)

### 谷歌 Gemini 2.5 系列正式 GA
**时间**：2026-05-10
- **发布内容**：
  - Gemini 2.5 Pro 正式版（06-05 版）
  - Gemini 2.5 Flash 正式版（05-20 版）
  - 全新 Gemini 2.5 Flash-Lite 预览版
- **定价调整**：
  - Flash 不再区分「推理」和「非推理」模式
  - Flash 价格：输入 0.30 美元/百万 Tokens
  - Flash-Lite：输入 0.10 美元，输出 0.40 美元/百万 Tokens
- **选型建议**：
  - 2.5 Pro：复杂任务、代码生成、智能体、内容创作
  - 2.5 Flash：高并发实时任务、摘要、QA 系统
  - 2.5 Flash-Lite：高频调用场景、成本敏感业务
- [链接](https://blog.csdn.net/weixin_40774379/article/details/148728719)

---

## 🌐 Web Search 最新资讯（24小时内）

### arXiv 多模态持续学习智能体最新论文

#### XSkill: 从经验和技能中持续学习的多模态智能体
**arXiv:2603.12056**
- **核心思路**：识别两种互补的可重用知识形式
  - 经验：提供简洁的动作级指导，用于工具选择和决策
  - 技能：提供结构化的任务级指导，用于规划和工具使用
- **架构**：双流框架，知识提取和检索均基于视觉观察
- **性能**：在 5 个基准测试上显著优于仅工具和基于学习的基线
- **亮点**：两种知识流在影响智能体推理行为上互补，显示出卓越的零样本泛化能力
- [链接](https://arxiv.org/abs/2603.12056)

#### 面向多模态终身理解：数据集和智能体基线
**arXiv:2603.05484**
- **数据集**：MM-Lifelong，包含 181.1 小时视频，跨天、周、月时间尺度
- **关键发现**：
  - 端到端 MLLM 存在工作记忆瓶颈（上下文饱和）
  - 代理基线在稀疏长时时间线上会出现全局定位崩溃
- **解决方案**：Recursive Multimodal Agent (ReMA)，采用动态记忆管理迭代更新递归信念状态
- [链接](https://arxiv.org/pdf/2603.05484v1)

### AI Agent 框架最新动态

#### 微软 AutoGen 0.4 版本发布
- **异步消息传递**：Agent 间通信采用异步机制，无需等待响应即可继续执行
- **模块化和可扩展**：轻松使用自定义 Agent、工具、内存和模型
- **可观测性和调试**：内置指标跟踪、消息追踪和调试工具
- **分布式支持**：设计复杂的分布式 Agent 网络
- **跨语言**：支持不同语言编写的 Agent 互操作
- **UI 更新**：交互式反馈、消息流可视化、可视化拖拽界面
- [链接](https://blog.csdn.net/m0_59614665/article/details/145153945)

#### Microsoft Agent Framework 正式发布
**时间**：2026-04-03
- **核心功能**：
  - 灵活的 Agent 框架：构建、编排和部署 AI Agent 和多智能体系统
  - 多智能体编排：群聊、顺序、并发和交接模式
  - 插件生态：原生函数、OpenAPI、Model Context Protocol (MCP) 等扩展
  - LLM 支持：OpenAI、Foundry、Anthropic 等
  - 运行时支持：进程内和分布式 Agent 执行
  - 多模态：文本、视觉和函数调用
  - 跨平台：.NET 和 Python 实现
- **替代方案**：将取代 Azure ML 和 Foundry 中的 Prompt Flow
- **迁移时间**：Prompt Flow 将于 2027-04-20 完全退役
- [链接](https://azure.microsoft.com/pt-br/updates?id=azure-governance-services-updates)

#### Agent Framework Library 0.8.4.post6 发布
- **定位**：使用 FastAPI 构建和服务对话式 AI Agent 的综合 Python 框架
- **特性**：
  - 快速设置：10-15 分钟创建 Agent
  - 简单 MCP 集成：轻松连接外部工具
  - 技能系统：基于 Markdown
- **发布时间**：2026-05-04
- [链接](https://pypi.org/project/agent-framework-lib/)

---

## 🔗 跨源深度整合分析

### 【纵向溯源】智能体技术发展路径

#### 从工具调用到自主执行的进化
- **2025年前**：AI 主要停留在「回答问题」阶段，工具调用需要显式触发
- **2025年中**：OpenAI Operator、Anthropic Claude Code 等工具开始具备基础环境交互能力
- **2026年初**：多模态理解与工具调用深度融合，视觉反馈环形成
- **2026年5月**：
  - Claude 托管智能体推出自主推演 (Dreaming) 能力
  - Runway Agent 将视频制作流程全链路自动化
  - Cursor 云环境支持智能体跨仓库协同
  - Meta 实现硬件级端到端加密 AI 对话

#### 关键节点形成的技术路径
1. **模型能力提升**：推理能力的突破（DeepSeek V4、GLM-5.1、Gemini 3 系列）
2. **环境交互**：从文本到视觉，再到完整操作系统控制
3. **多智能体协作**：从单一智能体到可编排的智能体团队
4. **安全与隐私**：从权限审批到硬件级隔离
5. **成本优化**：推理模型价格从「昂贵」到「白菜价」（Gemini Flash-Lite $0.1/M输入）

#### 发展路径背后的驱动力
- **需求侧**：开发者和企业需要 AI 做「实际工作」而非仅「提供建议」
- **供给侧**：大模型能力溢出，自然向更复杂的任务场景延伸
- **基础设施**：云环境、容器化、MCP 协议为智能体提供标准化运行时
- **安全实践**：红队测试、漏洞奖励计划、硬件隔离逐步建立信任

### 【横向对比】各技术路线的核心思想

#### 智能体架构路线对比
| 路线 | 代表 | 核心思想 | 基本假设 | 适用场景 |
|------|------|----------|----------|----------|
| **闭源托管** | Claude Managed Agents, ChatGPT Agent | 中心化控制，安全第一 | 用户需要易用性胜过定制化 | 企业标准化工作流 |
| **开源框架** | AutoGen, Microsoft Agent Framework | 可组合、可扩展 | 用户需要深度定制 | 研究、复杂业务场景 |
| **端侧优先** | Meta WhatsApp Incognito Chat | 隐私至上，本地计算 | 数据敏感场景 | 个人助手、健康/财务 |
| **云原生** | Cursor Cloud Agent, Runway Agent | 弹性环境，按需配置 | 需要隔离、可复现的环境 | 开发、内容创作 |

#### 实际应用效果与典型案例

**1. 编码领域**
- **Claude Code**：权限自动模式平衡安全与效率，已获广泛开发者采用
- **GLM-5.1**：开源 SOTA 编码能力，支持 8 小时长程任务
- **Cursor Cloud**：多仓库协同 + 环境即代码，企业落地门槛降低
- **DeepSeek V4**：Agentic 编码基准测试达到开源最高水平

**2. 内容创作**
- **Runway Agent**：从想法到成片自动化，制作周期从数周压缩至分钟级
- **Qwen-Character**：记忆+共情+主动交互，游戏和虚拟伴侣场景提升参与度 50%+
- **Krea 2**：情绪板分享功能优化创意协作流程

**3. 企业应用**
- **Claude for Small Business**：直接对接 QuickBooks、PayPal、HubSpot，自动化处理杂务
- **Anthropic B2B 采用率**：首次超越 OpenAI (34.4% vs 32.3%)
- **多模态 RAG**：Gemini 3.1 Flash-Lite 的成本结构使大规模部署成为可能

#### 在 AI 知识体系中的定位

**当前定位**：智能体是大模型能力的「执行器」
- 解决「模型知道怎么做但没法实际做」的问题
- 连接模型能力与真实世界环境
- 从「建议」到「行动」的关键桥梁

**演进方向**：
1. 从单步工具调用到多步长程任务
2. 从被动执行到主动规划和优化
3. 从单智能体到多智能体协作
4. 从通用智能体到领域专用智能体

### 【趋势判断】共识与分歧

#### 多源共同印证的趋势

1. **智能体将成为标配接口**
   - ai.hot：Runway Agent、Cursor Cloud Agent、Claude Managed Agents 同时发布
   - Web 搜索：所有主要厂商均更新 Agent 框架
   - X 动态：Swyx、Rauchg、Levie 等均讨论 Agent 部署

2. **成本持续下探，能力持续提升**
   - Gemini Flash-Lite：$0.1/M 输入 token，363 tok/s 速度
   - DeepSeek V4：1M 上下文标配，成本仅为竞品几分之一
   - Claude：额度翻倍、速率提升、算力扩容

3. **多模态成为智能体基本能力**
   - Claude 电脑与浏览器最佳实践：专门优化视觉理解
   - GLM-5V-Turbo：多模态编码基座模型
   - Gemini 3 系列：多模态理解与工具调用原生融合

4. **隐私与安全走向硬件级**
   - Meta：硬件安全飞地内进行推理
   - ExploitGym：AI 已能自主利用真实漏洞，安全需严肃对待
   - Claude：从权限请求到 Auto mode 分类器

#### 存在明显分歧的领域

1. **开源 vs 闭源**
   - 支持开源：DeepSeek 完全开放权重，AutoGen 社区驱动
   - 支持闭源：Claude、GPT 托管方案强调安全和易用性
   - 中间路线：GLM 系列部分开源、部分商业授权

2. **推理模式的必要性**
   - Google：Even Flash-Lite 开放全部 4 级 Thinking Levels
   - OpenAI/Anthropic：推理主要留给高端模型
   - 成本敏感场景：推理可关闭以降低延迟和费用

3. **Agent 部署的「最后一公里」**
   - Claude：托管方案 + 预构建连接器
   - Microsoft：Agent Framework 让企业自行构建
   - Cursor：开发环境即 Agent 运行环境

#### 值得关注的萌芽方向

1. **吸引子模型**：解决循环 Transformer 问题，训练后可内化迭代过程
   - 770M 优于 1.3B Transformer，27M 小模型在数独上超越 Claude/GPT o3
   - 可能改写语言模型训练范式

2. **持续学习 Agent**：arXiv 论文探讨从经验中学习，不更新参数也能改进
   - XSkill：经验 + 技能双流框架
   - ReMA：递归信念状态 + 动态记忆管理

3. **硬件级隐私 AI**：Meta 开启的端侧推理 + 安全飞地方向
   - 可能重新定义 AI 产品的信任边界

4. **1M 上下文成为标配**：DeepSeek V4、Gemini 3 系列等均将长上下文作为基础功能

---

## 附录：全部资讯链接

### 🔷 X/Twitter 来源
- [Swyx on OpenAI/Anthropic估值](https://x.com/swyx/status/2051440392722391180)
- [Guillermo Rauch on deepsec](https://x.com/rauchg/status/2051386798899888539)
- [Aaron Levie on enterprise agents](https://x.com/levie/status/2051344780328858040)
- [Garry Tan on GBrain v0.27](https://x.com/garrytan/status/2051517574589116510)
- [Sam Altman on voice AI](https://x.com/sama/status/2051464865634742334)
- [Nikunj on Gemini Flash](https://x.com/nikunj/status/2051321911741972900)
- [Peter Yang on AI path](https://x.com/petergyang/status/2051508988936937764)
- [Peter Steinberger on Crabbox 0.5.0](https://x.com/steipete/status/2051485798613111116)

### 🔷 ai.hot 精选链接
- [ExploitGym](https://rdi.berkeley.edu/blog/exploitgym)
- [Qwen-Character](https://x.com/alibaba_cloud/status/2054653031472414864)
- [Cursor Cloud Agent](https://cursor.com/blog/cloud-agent-development-environments)
- [Claude限额提升](https://x.com/ClaudeDevs/status/2054639777685934564)
- [Claude电脑使用最佳实践](https://claude.com/blog/best-practices-for-computer-and-browser-use-with-claude)
- [吸引子模型论文](https://arxiv.org/abs/2605.12466)
- [Anthropic B2B超越OpenAI](https://the-decoder.com/anthropic-overtakes-openai-in-b2b-adoption-for-the-first-time-according-to-ramp-spending-data)
- [WhatsApp Incognito Chat](https://x.com/AYi_AInotes/status/2054616319127904403)
- [Runway Agent](https://runwayml.com/news/introducing-runway-agent)
- [Claude for Small Business](https://www.anthropic.com/news/claude-for-small-business)

### 🔶 官方博客
- [Claude Code auto mode](https://www.anthropic.com/engineering/claude-code-auto-mode)

### 🟢 播客
- [Waymo的2000万次骑行](https://www.youtube.com/playlist?list=PLOhHNjZItNnMm5tdW61JpnyxeYH5NDDx8)

### 📰 中文资讯
- [ChatGPT Agent](https://blog.csdn.net/jike007gt/article/details/1487538459)
- [GPT-Realtime-2](http://m.toutiao.com/group/7636936998229944986/)
- [DeepSeek V4](https://www.knightli.com/en/2026/04/24/deepseek-v4-preview-release/)
- [GLM-5.1](https://docs.bigmodel.cn/cn/update/new-releases)
- [Claude限额调整](https://blog.csdn.net/qq_73472828/article/details/160867575)
- [Gemini 3 Flash](https://blog.csdn.net/guorui_java/article/details/156079428)
- [Gemini 2.5 GA](https://blog.csdn.net/weixin_40774379/article/details/148728719)

### 🌐 论文与技术文档
- [XSkill arXiv](https://arxiv.org/abs/2603.12056)
- [MM-Lifelong arXiv](https://arxiv.org/pdf/2603.05484v1)
- [AutoGen 0.4](https://blog.csdn.net/m0_59614665/article/details/145153945)
- [Microsoft Agent Framework](https://azure.microsoft.com/pt-br/updates?id=azure-governance-services-updates)
- [Agent Framework Library](https://pypi.org/project/agent-framework-lib/)

---

**摘要生成时间**：2026-05-14  
**数据覆盖窗口**：2026-05-13 至 2026-05-14  
**ai.hot 权重**：最高（核心信息源）

