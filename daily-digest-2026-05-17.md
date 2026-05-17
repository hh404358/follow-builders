
# AI Builders 每日摘要

**日期**: 2026年5月17日

---

## 🔷 X/Twitter 动态

### OpenAI 相关
- Sam Altman 表示对语音模型的发展感到兴奋，观察到人们开始改变与 AI 交互的方式
- OpenAI 正在大规模重组，Greg Brockman 全面接管产品战略，将 ChatGPT、Codex 和 API 合并为统一组织
- OpenAI 与马耳他合作，向所有公民免费提供 ChatGPT Plus

### 模型与 AI 技术
- Swyx 比较了 OpenAI 与 Ant 的估值和 ARR
- Nikunj 指出创业公司若只关注炫酷发布和分发而忽视留存，将很快面临问题，同时赞赏 Gemini Flash 的性价比
- Peter Yang 提出了一个有趣的观点：“编码是第一个前沿，知识工作是第二个，个人代理是第三个”

### 智能体与工具
- Guillermo Rauch (Vercel CEO) 宣布推出 `deepsec` - 一个开源的智能体编排器，用于深度安全审查
- Aaron Levie (Box CEO) 认为 Anthropic 和 OpenAI 都在帮助企业在组织内部署 AI 智能体，这是一个早期但将迅速壮大的趋势
- Garry Tan 发布了 GBrain v0.27，支持更多非 Anthropic/OpenAI 嵌入和 LLM，并预告即将推出多模态嵌入和深度照片 OCR
- Peter Steinberger 宣布 Crabbox 0.5.0 上线，支持桌面/浏览器租用、VNC + 认证 WebVNC、AWS Windows + WSL2、截图 + 应用启动

---

## 🔷 ai.hot 重点内容（首要信息源）

### 具身智能
- **Figure 人形机器人**：连续自主运行 4 天，在真实仓库环境中不间断工作，标志着从单次演示到持续运行的关键一步

### 开发工具与智能体
- **MagicPath 与 Codex 深度整合**：用户可将 MagicPath 作为原生画布直接在 Codex 中运行，实现设计开发一体化
- **Codex 自定义快捷键**：支持根据实际工作方式配置，提升使用体验

### 开源模型与研究
- **蚂蚁百灵 Ring-2.6-1T**：万亿参数推理模型开源，主打智能体执行能力，使用 Async RL 和 IcePop 训练方法，vLLM 首日即支持
- **NVIDIA SANA-WM**：26 亿参数开源世界模型，可生成长达 1 分钟、720p 分辨率的视频
- **Δ-Mem**：专为大型语言模型设计的高效在线内存系统，通过仅存储和更新模型激活的增量变化，减少内存占用高达 70%
- **XSKILL**：多模态智能体的双通道持续学习框架，无需参数更新即可从经验和技能中持续改进

### 行业动态
- **AI 带来的岗位流失**：美国开始出现人工智能相关岗位的大规模裁员
- **Anthropic Founder's Playbook**：警告 AI 可能提高创业失败率，指出 Claude Code 等工具使快速生成原型变得容易，但容易混淆“能运行”与“有市场需求”

### 安全与突破
- **利用 Anthropic Mythos 构建 macOS 内核漏洞**：研究人员成功绕过苹果 M5 芯片内存完整性执行安全系统

---

## 🔶 官方博客精选

### Anthropic Engineering Blog
- **Claude Code 自动模式**：一种更安全的跳过权限方式，在手动审查和无防护措施之间找到了平衡，使用基于模型的分类器来委托审批

---

## 🟢 播客更新

### Training Data Podcast
- **Waymo 的 Dmitri Dolgov 谈 2000 万次乘车和完全自动驾驶之路**：讨论了自动驾驶技术的发展历程、持续改进以及大规模部署的挑战

---

## 📰 中文 AI 资讯精选

### 智谱 AI GLM-5.1
- 新一代旗舰模型上线，Coding 能力大幅增强
- 支持长程任务，可在单次任务中独立、持续工作长达 8 小时
- 实现从规划、执行到交付的完整闭环
- 在自主规划、持续执行、问题修复与策略迭代上展现更强的工程智能
- 综合能力全面对齐 Claude Opus 4.6

### 具身智能国家基地
- 国家人工智能应用中试基地（具身智能）在杭州挂牌启用
- 为机器人提供国家级职业技能训练场
- 杭州市于 5 月 1 日施行首部具身智能机器人地方性法规
- 目前杭州已集聚机器人产业相关企业 700 余家，2025 年产值达 1068 亿元

---

## 🌐 Web Search 最新资讯（24h 内）

### OpenAI 最新动态
- **GPT-5.5 发布**：拥有 100 万 token 上下文窗口，Agents SDK 重大更新
- **GPT-Realtime-2**：全球首个具备 GPT-5 级别推理能力的音频模型
- **Workspace Agents**：替代传统 GPTs，实现自主工作流执行，采用信用计费模式
- **GPT-5 前景**：深度多模态、长期记忆与状态追踪、System-2 思维，AGI 临近

### DeepSeek V4
- **正式发布**：包含 V4-Pro（1.6T 总参，49B 激活）和 V4-Flash（284B 总参，13B 激活）
- **1M 上下文窗口**：成为标配，创新的混合注意力架构实现高效处理
- **双模式支持**：Thinking / Non-Thinking 模式
- **价格优势**：V4-Pro 仅为 Claude Opus 4.7 的 1/7，GPT-5.5 的 1/6
- **开源权重**：MIT 许可证，可自托管和微调

### 智谱 GLM-5.1 深度信息
- **744B MoE 架构**：40-44B 激活参数，256 专家，8 个激活/令牌
- **200K 上下文窗口**，131K 最大输出
- **纯华为硬件训练**：使用 100,000 个华为 Ascend 910B 芯片，无 Nvidia GPU
- **MIT 许可证**：可在 Hugging Face 获取
- **SWE-bench 成绩 77.8%**，接近 Claude Opus 4.6 的 80.8%
- **向量数据库优化**：600+ 迭代后吞吐量提升 6.9 倍
- **完整 Linux 桌面构建**：8 小时内完成，655 次迭代

### 多模态持续学习研究
- **XSKILL**：双通道框架，从经验和技能中持续学习，无需参数更新
- **ICAL（In-Context Abstraction Learning）**：使用检索增强生成改进策略
- **Lifelong Imitation Learning**：多模态潜在回放和增量调整，LIBERO 基准上 SOTA

---

## 🔗 跨源深度整合分析

### 纵向溯源

#### 智能体技术发展历程
智能体概念从早期的工具调用发展到如今的自主工作流，经历了关键节点：
1. **单一工具调用阶段**：模型仅能执行简单的预定义工具调用
2. **多工具编排阶段**：能够组合多个工具完成复杂任务
3. **自主规划阶段**：模型可以自主规划任务路径（如 OpenAI Workspace Agents）
4. **持续学习阶段**：无需参数更新即可从经验中改进（XSKILL）
5. **长程任务阶段**：支持 8 小时以上的连续自主工作（GLM-5.1）

这种发展路径是由**应用需求驱动**的：从简单的问答到复杂的知识工作自动化，再到工程级任务执行。企业对效率提升的渴望是主要推动力。

#### 开源模型演进
开源模型经历了从"追赶"到"并跑"再到部分"领跑"的过程：
- **参数量增长**：从数十亿到数千亿（DeepSeek V4-Pro 1.6T，GLM-5.1 744B）
- **架构创新**：MoE 成为主流，混合注意力机制实现高效长上下文
- **性能突破**：在特定领域（如编码）接近甚至超越闭源模型
- **生态成熟**：vLLM 等工具首日支持新模型，形成完整开发链路

### 横向对比

#### 主要模型对比

| 特性 | GPT-5.5 | Claude Opus 4.6/4.7 | DeepSeek V4-Pro | GLM-5.1 |
|------|---------|-------------------|-----------------|---------|
| 上下文 | 1M tokens | 200K+ | 1M tokens | 200K |
| 编码性能 | 高 | 领先 (80.8% SWE-bench) | 接近 (SWE-bench Verified 80.6%) | 77.8% SWE-bench |
| 长程任务 | 支持 | 支持 | 支持 | 8 小时自主工作 |
| 价格 | 高 | 很高 | 低 (1/7-1/6) | 中 (1/15 Claude) |
| 开源 | 否 | 否 | 是 (MIT) | 是 (MIT) |
| 硬件依赖 | Nvidia | Nvidia | 兼容 | 纯华为训练 |

#### 智能体框架对比
- **OpenAI Workspace Agents**：目标是企业工作流自动化，信用计费，与现有生态深度整合
- **Vercel deepsec**：专注安全审查领域，与 Vercel Sandbox 优化集成
- **XSKILL**：研究导向，强调持续学习和视觉锚定，无需参数更新
- **Claude Code Auto Mode**：平衡安全和效率，使用模型分类器进行权限判断

### 趋势判断

#### 共识趋势
1. **长上下文窗口成为标配**：1M 不再是卖点而是基线
2. **智能体从演示走向实用**：Figure 机器人连续运行 4 天、GLM-5.1 8 小时自主工作标志着实用化拐点
3. **开源模型持续挤压闭源利润空间**：DeepSeek、GLM 等在保持 90%+ 性能的同时价格仅为 1/5-1/15
4. **多模态深度融合**：不再是文本+视觉拼接，而是从底层统一建模
5. **持续学习受到重视**：XSKILL 等方法解决了"每次都从零开始"的问题

#### 分歧领域
- **AGI 路径**：OpenAI 认为 GPT-5 可能跨越 60% AGI 定义，而其他公司更强调特定领域深耕
- **商业模式**：OpenAI 推动广告平台和信用计费，Anthropic 警告创业失败率可能提高
- **安全与开放的平衡**：Mythos 能构建 macOS 内核漏洞，既展示能力也引发担忧

#### 萌芽方向
1. **无需参数更新的持续学习**：XSKILL 代表的 RAG 式进化路径
2. **高效内存系统**：Δ-Mem 节省 70% 内存，使超大模型更实用
3. **世界模型用于视频生成**：NVIDIA SANA-WM 生成长达 1 分钟 720p 视频
4. **具身智能国家基础设施**：杭州的国家级训练基地可能成为行业标准

---

## 附录：全部资讯链接

### 关键文章
- [OpenAI GPT-5.5 发布](https://www.winzheng.com/en/article/openai-gpt-5-5-million-token-window-agents-sdk-update-ad-pri)
- [DeepSeek V4 官方文档](https://api-docs.deepseek.com/news/news260424)
- [GLM-5.1 官方公告](https://docs.bigmodel.cn/cn/update/new-releases)
- [XSKILL arXiv 论文](https://arxiv.org/pdf/2603.12056)
- [Anthropic Founder's Playbook](https://x.com/berryxia/status/2055635826462130227)

### 播客与视频
- [Waymo 的 Dmitri Dolgov 访谈](https://www.youtube.com/playlist?list=PLOhHNjZItNnMm5tdW61JpnyxeYH5NDDx8)

### 开源项目
- [XSKILL GitHub](https://github.com/XSkill-Agent/XSkill)
- [DeepSeek V4](https://huggingface.co/collections/deepseek-ai/deepseek-v4)

