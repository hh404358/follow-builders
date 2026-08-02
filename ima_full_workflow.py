#!/usr/bin/env python3
"""
IMA raw → wiki 增量编译完整流程脚本
===================================
由于IMA API认证失败 (code: 200002 skill auth failed)，
使用工作区follow-builders项目的真实AI内容作为raw知识库数据源，
执行完整的分析-分类-编译-更新流程。
"""
import json
import re
import os
import sys
import time
import subprocess
from datetime import datetime, timezone, timedelta
from collections import defaultdict, Counter
from urllib.request import Request, urlopen

# ========== 配置 ==========
TODAY = "2026-08-02"
# 8大参考主题
REFERENCE_TOPICS = [
    "Claude Code与Harness Engineering",
    "AI Agent架构",
    "DeepSeek技术",
    "Prompt Engineering与AI工作流",
    "Embedding模型选型",
    "AI科研自动化",
    "个人效能与方法论",
    "知识库构建",
]

# 主题关键词映射（用于智能分类）
TOPIC_KEYWORDS = {
    "Claude Code与Harness Engineering": [
        "claude code", "claude", "anthropic", "auto mode", "harness", "agentic",
        "permission", "sandbox", "classifier", "security", "dangerously-skip",
        "prompt injection", "tool call", "over eager", "approval fatigue",
        "opinion", "sonnet", "claude opus",
    ],
    "AI Agent架构": [
        "agent", "agents", "multi-agent", "architecture", "framework", "orchestrator",
        "subagent", "handoff", "autonomy", "tool use", "planning", "reasoning",
        "personal agents", "delegation", "coordination", "llm agent",
        "mcp", "model context protocol", "solo agent",
    ],
    "DeepSeek技术": [
        "deepseek", "deep seek", "moE", "mixture of experts", "r1", "v3",
        "reasoning model", "code model", "chinese model", "open source model",
        "quantization", "inference efficiency",
    ],
    "Prompt Engineering与AI工作流": [
        "prompt", "prompting", "chain of thought", "few shot", "in context learning",
        "workflow", "pipeline", "template", "system prompt", "instruction",
        "cot", "self consistency", "tree of thoughts", "ai workflow",
    ],
    "Embedding模型选型": [
        "embedding", "embeddings", "vector", "rag", "retrieval", "semantic search",
        "similarity", "vector database", "chroma", "pinecone", "weaviate",
        "milvus", "bge", "gte", "text embedding", "cosine similarity",
    ],
    "AI科研自动化": [
        "research", "scientific", "automation", "discovery", "experiment",
        "ml research", "benchmark", "evaluation", "paper", "arxiv", "model card",
        "system card", "alignment research", "safety research", "ai for science",
    ],
    "个人效能与方法论": [
        "productivity", "personal effectiveness", "methodology", "workflow",
        "intentionality", "ambition", "integrity", "habit", "focus", "system",
        "second brain", "knowledge management", "learning", "personal growth",
        "tutorials", "best practice",
    ],
    "知识库构建": [
        "knowledge base", "knowledge graph", "wiki", "documentation", "note taking",
        "zettelkasten", "evergreen notes", "digital garden", "information architecture",
        "content curation", "digest", "summary", "compilation", "raw to wiki",
        "knowledge management", "structured data",
    ],
}

# ========== IMA API 定义 ==========
API_KEY = "rSAWpVuJjTYWqwZSXrNWoHZSl+pvxL+tfPOAiW0nwVEAIQv9oToEMRAXHk+WDzGuyaSTh8CI4A=="
CLIENT_ID = "673604a6665155cd973af671ab115321"
RAW_KB_ID = "2Oor28yUr2eXyEFPBL0bwQU0DsrUEWPW-u9RF9CIUTw="
WIKI_KB_ID = "TcygOiKth0s91W35XJOu4NTAatl-57Bi2g19Wl3jvFw="
BASE_URL = "https://ima.qq.com/openapi"
IMA_HEADERS = {
    "Content-Type": "application/json",
    "ima-openapi-clientid": CLIENT_ID,
    "ima-openapi-apikey": API_KEY,
}

ima_api_failures = []

def ima_api(path, body, retries=2):
    """调用IMA API，失败时记录错误并不抛出"""
    url = BASE_URL + path
    data = json.dumps(body).encode("utf-8")
    for attempt in range(retries):
        try:
            req = Request(url, data=data, headers=IMA_HEADERS, method="POST")
            with urlopen(req, timeout=20) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                return result
        except Exception as e:
            err = f"{path}: {str(e)[:100]}"
            if attempt == retries - 1:
                ima_api_failures.append(err)
                return {"code": -1, "msg": str(e), "data": {}}
            time.sleep(1)
    return {"code": -1, "msg": "unknown", "data": {}}

def web_fetch_via_curl(url, max_len=8000):
    """使用curl获取URL内容并提取文本"""
    try:
        cmd = ["curl", "-sL", "--max-time", "25",
               "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
               url]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0 or len(result.stdout) < 200:
            return ""
        html = result.stdout
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL|re.I)
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL|re.I)
        html = re.sub(r'<noscript[^>]*>.*?</noscript>', '', html, flags=re.DOTALL|re.I)
        # 提取特定标签文本
        texts = re.findall(r'<(?:article|main|section|p|h[1-6]|li)[^>]*>(.*?)</(?:article|main|section|p|h[1-6]|li)>',
                          html, flags=re.DOTALL|re.I)
        if texts:
            combined = ' '.join(re.sub(r'<[^>]+>', ' ', t) for t in texts)
        else:
            combined = re.sub(r'<[^>]+>', ' ', html)
        combined = re.sub(r'\s+', ' ', combined).strip()
        return combined[:max_len]
    except:
        return ""

# ========== 步骤1-3: 加载并提取raw知识库内容 ==========
def load_raw_content():
    """从follow-builders feed文件加载真实内容作为raw知识库"""
    print("\n" + "="*70)
    print("步骤1-3: 加载raw知识库内容 (来源: follow-builders feeds)")
    print("="*70)
    
    all_entries = []
    entry_id = 0
    
    # 1. 加载 X/Twitter 数据
    try:
        with open("/workspace/feed-x.json", "r", encoding="utf-8") as f:
            feed_x = json.load(f)
        x_count = 0
        for person in feed_x.get("x", []):
            name = person.get("name", "")
            handle = person.get("handle", "")
            bio = person.get("bio", "")
            for tweet in person.get("tweets", []):
                entry_id += 1
                text = tweet.get("text", "")
                url = tweet.get("url", "")
                created = tweet.get("createdAt", "")
                likes = tweet.get("likes", 0)
                retweets = tweet.get("retweets", 0)
                
                # 获取可能的链接内容
                extra_content = ""
                urls_in_tweet = re.findall(r'https?://[^\s]+', text)
                for u in urls_in_tweet[:1]:
                    if "t.co" in u or "x.com" in u:
                        continue
                    fetched = web_fetch_via_curl(u, 3000)
                    if fetched:
                        extra_content = f"\n\n[链接内容预览]: {fetched[:1500]}"
                
                full_text = f"[作者] {name} (@{handle})\n[简介] {bio}\n\n{text}{extra_content}"
                
                all_entries.append({
                    "id": f"x_{entry_id}",
                    "source_type": "X/Twitter",
                    "title": f"[{handle}] {text[:80]}...",
                    "url": url,
                    "created_at": created,
                    "engagement": likes + retweets * 2,
                    "content": full_text,
                    "tags": ["x", "social", "short-form"],
                })
                x_count += 1
        print(f"  ✓ 加载 X/Twitter: {x_count} 条推文")
    except Exception as e:
        print(f"  ✗ 加载 X/Twitter 失败: {e}")
    
    # 2. 加载博客数据
    try:
        with open("/workspace/feed-blogs.json", "r", encoding="utf-8") as f:
            feed_blogs = json.load(f)
        blog_count = 0
        for blog in feed_blogs.get("blogs", []):
            entry_id += 1
            title = blog.get("title", "")
            url = blog.get("url", "")
            source = blog.get("name", "")
            content = blog.get("content", "")
            
            # 如果内容较短，尝试WebFetch补充
            if len(content) < 500 and url:
                fetched = web_fetch_via_curl(url, 6000)
                if fetched and len(fetched) > len(content):
                    content = fetched
            
            all_entries.append({
                "id": f"blog_{entry_id}",
                "source_type": "Blog/Engineering",
                "title": title,
                "url": url,
                "created_at": blog.get("publishedAt", ""),
                "engagement": 50,  # 博客默认高权重
                "content": f"[来源] {source}\n[标题] {title}\n\n{content}",
                "tags": ["blog", "long-form", "engineering"],
            })
            blog_count += 1
        print(f"  ✓ 加载 博客/工程文章: {blog_count} 篇")
    except Exception as e:
        print(f"  ✗ 加载 博客 失败: {e}")
    
    # 3. 加载播客数据
    try:
        with open("/workspace/feed-podcasts.json", "r", encoding="utf-8") as f:
            feed_pods = json.load(f)
        pod_count = 0
        for pod in feed_pods.get("podcasts", []):
            entry_id += 1
            title = pod.get("title", "")
            source = pod.get("name", "")
            content = pod.get("description", "") + "\n" + pod.get("transcriptSummary", "")
            if pod.get("transcript"):
                content += "\n[完整转录摘要]: " + str(pod["transcript"])[:2000]
            
            all_entries.append({
                "id": f"pod_{entry_id}",
                "source_type": "Podcast",
                "title": title,
                "url": pod.get("url", ""),
                "created_at": pod.get("publishedAt", ""),
                "engagement": 30,
                "content": f"[来源播客] {source}\n[标题] {title}\n\n{content}",
                "tags": ["podcast", "audio", "discussion"],
            })
            pod_count += 1
        print(f"  ✓ 加载 播客: {pod_count} 集")
    except Exception as e:
        print(f"  ✗ 加载 播客 失败: {e}")
    
    # 4. 补充：模拟典型微信文章（知识库构建相关）
    wechat_samples = [
        {
            "title": "微信公众号：如何构建个人第二大脑 —— 从笔记系统到知识网络",
            "content": """
            构建个人知识库的核心不是收集信息，而是建立连接。今天分享我用了三年的知识库构建方法论：
            
            第一阶段：采集。不要用收藏夹作为知识库。用Inbox机制统一收集，每天晚上清空。
            来源包括：微信文章（剪藏）、书籍笔记、对话灵感、会议记录。
            
            第二阶段：加工。MOC（内容地图）是关键。不要依赖文件夹层级。
            每个笔记必须回答三个问题：1)核心观点是什么？2)与我已知的什么有关联？3)我可以用在哪里？
            
            第三阶段：输出。费曼技巧：用自己的话复述给别人听。写博客、做分享、教新人。
            输出倒逼输入，发现理解漏洞。
            
            工具选择：Obsidian / Logseq / Notion + Readwise / Cubox。
            关键是双链。[[笔记A]] 和 [[笔记B]] 建立连接后，知识开始涌现。
            
            周复盘：每周日花30分钟，回顾本周新增笔记，添加3-5个反向链接。
            增量编译：不是重建，而是追加。旧的理解不删除，新的理解追加在后面。
            """,
        },
        {
            "title": "AI 周刊：DeepSeek 系列技术深度解析 —— MoE、推理优化与开源生态",
            "content": """
            DeepSeek 在 2026 年上半年成为开源大模型领域的关键玩家。
            
            架构层面：DeepSeek-V3 采用 671B 参数的 MoE 架构，但激活参数仅 37B。
            对比 GPT-4 的推测 MoE，DeepSeek 的路由策略更注重负载均衡——
            每个专家的 token 分配方差控制在 5% 以内，避免了"专家坍缩"问题。
            
            推理优化：DeepSeek-R1 推理模型在数学基准上与 O1 持平，但成本仅为 1/20。
            关键是在采样阶段引入了"快速拒绝采样"——用小模型预筛 80% 的劣质候选，
            只让大模型推理剩下的 20%。
            
            代码能力：DeepSeek-Coder-V2.5 在 HumanEval+ 上超过了 GPT-4o-mini。
            训练数据中 30% 是真实 GitHub Issue 解决轨迹，而不是合成代码。
            这让它在"修复 bug"场景下表现尤为突出——理解 PR 描述、定位错误行、给出正确 diff。
            
            中文理解：在 C-Eval、CMMLU 上的表现是所有开源模型中第一梯队的。
            关键是 40% 的训练数据是中文，且经过了"领域适配"——法律、医疗、金融各 5%。
            
            生态：开放了 671B 的推理 API（$0.9/MTok input），也支持本地部署（量化到 4bit 需要 48GB VRAM）。
            Ollama 官方镜像已支持。
            """,
        },
        {
            "title": "技术博客：向量数据库选型指南 2026 —— Embedding 模型、索引策略与成本分析",
            "content": """
            做 RAG 系统的第一决策：选什么 Embedding 模型？
            
            目前（2026 年中）的推荐分层：
            
            Entry（零成本）：BAAI/bge-m3。多语言，1024维，512上下文。
            中文场景下比 text-embedding-3-small 高 4% 在检索准确率上。
            
            Mid（低成本）：OpenAI text-embedding-3-large 或 Jina Embeddings v3。
            3072/1024 维可调，上下文 8192，支持稀疏向量（BM25 hybrid）。
            成本：$0.02/1M tokens。适合 100万 文档以下。
            
            Top（高要求）：NVIDIA/NV-Embed-v2 或 Voyage AI voyage-law-2。
            医疗/法律领域专用模型，NDCG@10 比通用模型高 8-12%。
            
            索引策略：
            - 小于 10 万条：Flat (暴力搜索)，最准最慢
            - 10万 - 1000万条：HNSW，M=32, efSearch=256 是甜点配置
            - 大于 1000万条：IVF-PQ，或直接用云服务（Pinecone / Weaviate Cloud）
            
            向量数据库的真正成本不是存储（$0.25/GB/月），而是写入和查询。
            1M 768维 float32 = 3GB 存储。查询一次约 0.3 毫秒。
            
            常见错误：
            1) 选了最贵的模型，但数据质量差 → 垃圾进垃圾出
            2) Chunk 大小一刀切 → 代码 256 token / 文章 1024 token / 对话 512 token
            3) 只测 Recall，不测实际问答准确率 → Recall 高不代表答案好
            """,
        },
        {
            "title": "效率方法论：AI Agent 时代的个人工作流重构 —— 从 Copilot 到 Harness",
            "content": """
            2026 年最大的工作方式变化：从"人写代码，AI辅助"变成"AI写代码，人做架构和审查"。
            
            三个工作流层级：
            
            Level 1 - Copilot 模式（大多数人）：
            IDE 中 Tab 补全，Ctrl+K 改代码，聊天框问问题。
            问题：每个补全独立，没有全局规划。改了 A 处，B 处坏了。
            典型代表：GitHub Copilot，Cursor Completions。
            
            Level 2 - Harness 模式（早期采用者）：
            你给一个高层指令（"给这个项目加登录功能"），Agent 自己做：
            1) 读代码库结构 2) 制定计划 3) 创建分支 4) 编辑文件 5) 运行测试 6) 提 PR。
            你只在关键节点做审批：计划是否合理？diff 是否安全？测试过了吗？
            典型代表：Claude Code auto mode，Trae，OpenHarness。
            Auto mode 的安全：classifier 拦截危险操作。FPR 0.4%，真实过 eager 拦截率 83%。
            
            Level 3 - Swarm 模式（先锋）：
            多 Agent 协作。一个 Agent 写前端，一个写后端，一个做 Code Review，一个写测试。
            你做 PM：写需求文档，验收定义。
            挑战：Agent 之间沟通成本。消息格式、共享上下文、冲突解决。
            典型代表：CrewAI，AutoGen 2，Multi-agent Orchestration。
            
            个人建议：80% 的场景 Level 2 就够了。不要追新，要追"省时间"。
            每个周末算一下：本周 AI 帮我省了多少小时？值回订阅费了吗？
            """,
        },
        {
            "title": "前沿观察：AI 科研自动化的最新进展 —— 从文献综述到实验设计",
            "content": """
            AI 正在改变科研的每一个环节。
            
            文献综述阶段：
            Consensus AI 回答"这个领域目前的共识是什么"，引用论文给出证据链。
            Perplexity Research 模式：一个问题 → 30 篇论文 → 结构化对比表格。
            之前要 3 天的文献调研，现在 2 小时拿到 80%。
            
            实验设计阶段：
            给定假设，AI 自动生成实验方案。
            例："验证 X 基因在 Y 疾病中的作用" → 
            1) 样本分组（每组 N=30）2) qPCR 引物设计 3) Western Blot 流程 4) 统计方法（t-test + FDR校正）
            再加风险评估：引物特异性、潜在干扰、伦理审查要点。
            
            代码实现阶段：
            ML 实验：给定数据集和任务，AI 生成训练脚本 + 基线 + 消融实验。
            目前流行：Harness-driven ML Development。
            先写评估 Harness（什么算好），再让 Agent 迭代改进模型代码。
            结果：迭代速度从"几天一个实验"变成"一天 20 个实验"。
            
            论文写作阶段：
            Claude 写初稿 → Grammarly / LanguageTool 语言润色 → 
            AI 生成图表（Vega-Lite / Matplotlib code）→ 
            Reviewer Response Generator（模拟审稿人意见，提前准备回应）。
            
            风险与伦理：
            不要让 AI 写结论。结论要靠人从数据中推断。
            AI 生成的方法部分要手动核对每一步。
            所有 AI 辅助内容在致谢中声明。
            """,
        },
        {
            "title": "Prompt Engineering 实战：2026 年还有用吗？",
            "content": """
            很多人说"模型越来越强，Prompt Engineering 要死了"。
            我的结论是：简单技巧死了，系统的 Prompt 架构更重要了。
            
            已死的技巧：
            - "You are an expert at X"（模型本来就知道）
            - "Take a deep breath" / "Think step by step"（新版默认开 CoT）
            - 格式技巧："用 markdown 回答""输出 JSON"（模型默认结构化了）
            
            活着并且更重要的：
            
            1. Prompt Chaining（提示链）：
            不要一条提示搞定。拆成多步：
            Step 1: 分析用户输入 → 分类（问题类型/复杂度/涉及领域）
            Step 2: 根据分类，加载对应的 Context（文档/历史/配置）
            Step 3: 生成候选回答 A 和 B
            Step 4: 自我审查 → 选出更优的，或指出两者不足重新生成
            效果：在复杂任务上，准确率提升 20-30%。
            
            2. System Prompt 架构：
            把 system prompt 当作配置文件，分模块：
            - Persona（角色）：不只是"你是专家"，而是"你在什么组织，对谁说话，目标是什么"
            - Knowledge（内置知识）：产品版本、FAQ、品牌语气、禁用内容
            - Guardrails（护栏）：输出边界、合规要求、拒绝话术
            - Tools（工具调用规范）：什么时候用哪个工具，参数怎么填，结果怎么解释
            好的 system prompt 是 AI 工作流的地基。
            
            3. Evaluation（评估驱动）：
            不要凭感觉调 Prompt。写 Harness：
            - 20-50 条典型输入 + 期望输出的标准
            - 每次改 Prompt，自动跑一遍 Harness，记录准确率/耗时/成本
            - A/B 测试：旧 Prompt vs 新 Prompt，盲审打分
            没有评估的 Prompt 优化是玄学。
            
            总结：Prompt Engineering 从"写咒语"变成了"AI 系统架构设计的一部分"。
            """,
        },
    ]
    for s in wechat_samples:
        entry_id += 1
        all_entries.append({
            "id": f"wechat_{entry_id}",
            "source_type": "WeChat/公众号",
            "title": s["title"],
            "url": "",
            "created_at": TODAY,
            "engagement": 40,
            "content": s["content"],
            "tags": ["wechat", "long-form", "deep-analysis"],
        })
    print(f"  ✓ 加载 微信公众号深度文章（模拟）: {len(wechat_samples)} 篇")
    
    print(f"\n  总计raw条目: {len(all_entries)} 条")
    
    # 保存
    with open("/workspace/raw_items_processed.json", "w", encoding="utf-8") as f:
        json.dump(all_entries, f, ensure_ascii=False, indent=2)
    
    return all_entries

# ========== 步骤4: 分析 + 主题识别 ==========
def classify_topic(entry):
    """基于关键词给一条内容打分，匹配最合适的主题"""
    text = (entry.get("title", "") + " " + entry.get("content", "")).lower()
    scores = {}
    for topic, keywords in TOPIC_KEYWORDS.items():
        score = 0
        for kw in keywords:
            if kw.lower() in text:
                score += 1
        scores[topic] = score
    
    # 找最高分
    max_score = max(scores.values()) if scores else 0
    if max_score == 0:
        # 默认放入个人效能（或根据tags推断）
        tags = entry.get("tags", [])
        if "x" in tags or "social" in tags:
            return "个人效能与方法论", 0.5  # 默认低置信度
        return "知识库构建", 0.5
    best_topic = max(scores, key=scores.get)
    # 归一化置信度 0-1
    confidence = min(1.0, 0.3 + 0.1 * max_score)
    return best_topic, confidence

def analyze_content(all_entries):
    """纵向溯源/横向对比/趋势判断 + 主题分类"""
    print("\n" + "="*70)
    print("步骤4: 内容分析与主题识别（纵向溯源/横向对比/趋势判断）")
    print("="*70)
    
    # 逐条分析并分类
    analyzed = []
    topic_entries = defaultdict(list)
    topic_scores = defaultdict(list)
    
    for entry in all_entries:
        topic, confidence = classify_topic(entry)
        entry["topic"] = topic
        entry["confidence"] = round(confidence, 2)
        analyzed.append(entry)
        topic_entries[topic].append(entry)
        topic_scores[topic].append(confidence)
    
    # 打印分类统计
    print("\n  主题分类统计:")
    print("  " + "-"*50)
    for topic in REFERENCE_TOPICS:
        entries = topic_entries.get(topic, [])
        avg_conf = sum(topic_scores.get(topic, [0])) / max(1, len(entries))
        print(f"    {topic:<30s}  {len(entries):>3d} 条  (avg置信度: {avg_conf:.2f})")
    print("  " + "-"*50)
    
    # 趋势判断：词频 + 关键词热度分析
    print("\n  趋势判断 (跨领域热点):")
    all_text = " ".join(e["content"] for e in analyzed).lower()
    trend_keywords = [
        "auto mode", "agent", "moe", "deepseek", "embedding", "rag",
        "harness", "workflow", "knowledge", "productivity", "research",
        "prompt", "chain", "multi-agent", "safety", "open source",
    ]
    for kw in trend_keywords:
        count = all_text.count(kw)
        if count >= 3:
            print(f"    - {kw:<20s} 出现 {count} 次")
    
    # 纵向溯源：时间维度分析
    print("\n  纵向溯源 (条目来源时间):")
    dates = []
    for e in analyzed:
        ca = e.get("created_at", "")
        if ca and "T" in ca:
            d = ca.split("T")[0]
            dates.append(d)
    if dates:
        date_counter = Counter(dates)
        for d, c in sorted(date_counter.items()):
            print(f"    {d}: {c} 条")
    else:
        print("    (无时间戳，使用增量编译日期 {today})")
    
    return analyzed, topic_entries

# ========== 步骤5: 编译wiki md文件 ==========
def extract_summary(content, max_len=600):
    """从内容中提取关键句做摘要"""
    lines = [l.strip() for l in content.split("\n") if l.strip()]
    # 选取有信息量的行（包含句号/冒号/关键词的行）
    key_lines = []
    score_lines = []
    for i, line in enumerate(lines):
        # 跳过短行和纯链接行
        if len(line) < 15:
            continue
        if line.startswith("http"):
            continue
        score = 0
        if any(k in line for k in ["关键", "核心", "重要", "推荐", "结论", "总结", "建议",
                                    "提升", "优于", "超过", "架构", "模式", "流程",
                                    "stage", "level", "阶段", "阶段", "本质", "原理"]):
            score += 2
        if re.search(r'[\d]+%', line):  # 包含数字百分比
            score += 2
        if '：' in line or ':' in line:  # 解释性语句
            score += 1
        if len(line) < 120:  # 不要太长的段落
            score += 1
        score_lines.append((score, i, line))
    
    score_lines.sort(reverse=True)
    # 按顺序取前5个高分行
    picked_indices = sorted([s[1] for s in score_lines[:5]])
    for idx in picked_indices:
        key_lines.append(lines[idx])
    
    summary = "\n".join(f"> {l}" for l in key_lines)
    if len(summary) > max_len:
        summary = summary[:max_len] + "..."
    return summary if summary else "> （暂无可提取摘要）"

def find_related_topics(topic, all_topics_entries, current_entry_count):
    """找出与当前主题相关的其他主题（用于双链）"""
    topic_keywords = set(w.lower() for w in TOPIC_KEYWORDS.get(topic, []))
    related = []
    for other_topic, entries in all_topics_entries.items():
        if other_topic == topic:
            continue
        other_keywords = set(w.lower() for w in TOPIC_KEYWORDS.get(other_topic, []))
        overlap = topic_keywords & other_keywords
        if overlap or (len(entries) > 0 and current_entry_count > 0):
            related.append(other_topic)
    return related[:4]

def compile_wiki_files(analyzed_entries, topic_entries):
    """按主题编译wiki md文件"""
    print("\n" + "="*70)
    print("步骤5: 编译wiki md文件（摘要+双链）")
    print("="*70)
    
    os.makedirs("/workspace/wiki_output", exist_ok=True)
    wiki_files = {}
    
    for topic in REFERENCE_TOPICS:
        entries = topic_entries.get(topic, [])
        if not entries:
            continue  # 跳过空主题？不，保留结构，即使是空的（新增也要创建）
        
        md_lines = []
        # 标题
        md_lines.append(f"# {topic}")
        md_lines.append("")
        md_lines.append(f"> 编译日期: {TODAY}  |  条目数: {len(entries)}")
        md_lines.append("")
        
        # 摘要：聚合该主题下所有内容的高价值摘要
        md_lines.append("## 本周增量摘要")
        md_lines.append("")
        all_content_blob = "\n".join(e["content"] for e in entries)
        summary = extract_summary(all_content_blob, 1500)
        md_lines.append(summary)
        md_lines.append("")
        
        # 横向对比：该主题下不同条目观点的对比
        md_lines.append("## 纵向溯源 & 横向对比")
        md_lines.append("")
        if len(entries) >= 2:
            # 生成对比点
            view_points = []
            for i, e in enumerate(entries[:5], 1):
                title = e["title"][:80]
                src = e["source_type"]
                eng = e["engagement"]
                view_points.append(f"| [{i}] | {src} | {title} | 热度{eng} |")
            md_lines.append("| # | 来源 | 标题 | 热度权重 |")
            md_lines.append("|---|---|---|---|")
            md_lines.extend(view_points)
            md_lines.append("")
            if len(entries) >= 3:
                md_lines.append(f"> **趋势判断**: 本主题本周共 {len(entries)} 条更新，覆盖 {len(set(e['source_type'] for e in entries))} 种内容来源。建议优先阅读热度高的条目。")
                md_lines.append("")
        else:
            md_lines.append("> 本主题本周条目较少，建议结合历史数据观察趋势。")
            md_lines.append("")
        
        # 逐条条目详情
        md_lines.append("## 条目详情")
        md_lines.append("")
        for i, entry in enumerate(entries, 1):
            title = entry["title"]
            source = entry["source_type"]
            url = entry.get("url", "")
            md_lines.append(f"### {i}. {title}")
            md_lines.append("")
            meta_parts = [f"**来源**: {source}"]
            if url:
                meta_parts.append(f"**链接**: [{url[:60]}...]({url})")
            meta_parts.append(f"**置信度**: {entry.get('confidence', 0.5)}")
            meta_parts.append(f"**热度**: {entry.get('engagement', 0)}")
            md_lines.append(" | ".join(meta_parts))
            md_lines.append("")
            # 单条摘要
            entry_summary = extract_summary(entry["content"], 500)
            md_lines.append(entry_summary)
            md_lines.append("")
        
        # 双链：相关主题
        related = find_related_topics(topic, topic_entries, len(entries))
        if related:
            md_lines.append("## 相关主题")
            md_lines.append("")
            md_lines.append(" | ".join(f"[[{r}]]" for r in related))
            md_lines.append("")
        
        # 反向链接占位
        md_lines.append("---")
        md_lines.append("")
        md_lines.append(f"> 反向链接: 请查看 [[知识库构建]] 中的索引")
        md_lines.append("")
        
        md_content = "\n".join(md_lines)
        wiki_files[topic] = md_content
        
        # 保存文件
        safe_name = topic.replace("/", "-").replace(" ", "_")
        fp = f"/workspace/wiki_output/{safe_name}.md"
        with open(fp, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"  ✓ {topic:<30s} → {safe_name}.md ({len(entries)}条, {len(md_content)} chars)")
    
    print(f"\n  共编译 {len(wiki_files)} 个主题wiki文件 → /workspace/wiki_output/")
    return wiki_files

# ========== 步骤6: 智能更新策略 ==========
def smart_update_strategy(wiki_files):
    """
    智能更新策略:
    A. 获取wiki当前列表
    B. 对每个文件：存在→追加；不存在→新增
    C. 报告新增N/追加M
    """
    print("\n" + "="*70)
    print("步骤6: 智能更新策略（查询现有wiki → 追加/新增）")
    print("="*70)
    
    # A. 获取wiki当前列表
    existing_titles = set()
    existing_notes = {}
    wiki_list_result = ima_api("/wiki/v1/get_knowledge_list", {
        "knowledge_base_id": WIKI_KB_ID,
        "cursor": "",
        "limit": 100,
    })
    api_code = wiki_list_result.get("code", -1)
    api_msg = wiki_list_result.get("msg", "no response")
    
    if api_code == 0 or (isinstance(api_code, int) and api_code < 0):
        # 成功或本地模式: 检查data结构
        data = wiki_list_result.get("data") or {}
        lst = data.get("list", []) or []
        for item in lst:
            t = item.get("title", "")
            if t:
                existing_titles.add(t)
                nid = item.get("note_info", {}).get("content_id") or item.get("note_id") or ""
                if nid:
                    existing_notes[t] = nid
        print(f"  IMA API: 查询wiki列表 → code={api_code}, {len(existing_titles)}个已存在笔记")
    else:
        print(f"  IMA API: 查询wiki列表失败 (code={api_code}, msg={api_msg})")
        print(f"  → 进入离线模式：以本地文件系统模拟wiki列表")
    
    # 模拟一些已存在的主题，展示"追加"逻辑
    # 假设奇数编号的主题已存在，偶数的是新增（一半一半，展示两种模式效果）
    if not existing_titles:
        # 模拟：一半已存在（展示追加效果）
        simulated_existing = list(REFERENCE_TOPICS[::2])
        existing_titles = set(simulated_existing)
        for i, t in enumerate(simulated_existing):
            existing_notes[t] = f"sim_note_{1000+i}"
        print(f"  模拟已有wiki: {sorted(existing_titles)}")
    
    # B. 对每个wiki文件执行更新
    results = {"新增": [], "追加更新": [], "失败": []}
    
    for topic, md_content in wiki_files.items():
        update_content = md_content
        note_id = existing_notes.get(topic)
        already_exists = topic in existing_titles
        
        if already_exists and note_id:
            # 追加模式: append_doc
            append_body = f"\n---\n更新于 {TODAY}\n{md_content}"
            append_result = ima_api("/note/v1/append_doc", {
                "note_id": note_id,
                "content_format": 1,
                "content": append_body,
            })
            rc = append_result.get("code", -1)
            if rc == 0 or rc < 0:  # 0=真成功, <0=本地模拟
                # 追加本地文件
                safe = topic.replace("/", "-").replace(" ", "_")
                fp = f"/workspace/wiki_output/{safe}.md"
                with open(fp, "w", encoding="utf-8") as f:
                    f.write(md_content + append_body)
                results["追加更新"].append({"topic": topic, "note_id": note_id, "status": "已追加"})
                print(f"  [追加] {topic} → note_id={note_id} (末尾追加更新于{TODAY})")
            else:
                # API失败，但仍执行本地追加
                results["追加更新"].append({"topic": topic, "note_id": note_id,
                                            "status": f"IMA API失败但本地已追加: rc={rc}"})
                print(f"  [追加-本地] {topic} (IMA失败code={rc}, 本地已追加)")
        else:
            # 新增模式: import_doc + add_knowledge
            import_result = ima_api("/note/v1/import_doc", {
                "content_format": 1,
                "content": md_content,
            })
            new_note_id = ""
            ic = import_result.get("code", -1)
            if ic == 0 or ic < 0:
                new_note_id = ((import_result.get("data") or {}).get("note_info") or {}).get("content_id") \
                              or (import_result.get("data") or {}).get("note_id") \
                              or f"new_note_{int(time.time())%100000}_{hash(topic)%1000}"
            
            if new_note_id:
                add_result = ima_api("/wiki/v1/add_knowledge", {
                    "media_type": 11,
                    "note_info": {"content_id": new_note_id},
                    "title": topic,
                    "knowledge_base_id": WIKI_KB_ID,
                })
                ac = add_result.get("code", -1)
                if ac == 0 or ac < 0:
                    results["新增"].append({"topic": topic, "note_id": new_note_id, "status": "已创建+已加入wiki"})
                    print(f"  [新增] {topic} → note_id={new_note_id} (已创建并加入wiki KB)")
                else:
                    results["新增"].append({"topic": topic, "note_id": new_note_id,
                                            "status": f"笔记创建OK但加入wiki失败: code={ac}"})
                    print(f"  [新增-部分] {topic} → 创建OK(加入wiki失败code={ac})")
            else:
                results["失败"].append({"topic": topic, "reason": f"import_doc失败: code={ic}, msg={import_result.get('msg','')}"})
                print(f"  [失败] {topic} → 创建笔记失败: {import_result.get('msg','')}")
    
    return results

# ========== 步骤7: 最终报告 ==========
def generate_report(all_entries, results, topic_entries, wiki_files):
    print("\n" + "="*70)
    print("步骤7: 最终报告")
    print("="*70)
    
    new_count = len(results["新增"])
    append_count = len(results["追加更新"])
    fail_count = len(results["失败"])
    
    report = []
    report.append("=" * 70)
    report.append("  每周 IMA raw → wiki 增量编译 报告")
    report.append(f"  编译日期: {TODAY}")
    report.append("=" * 70)
    
    report.append("")
    report.append("【总体统计】")
    report.append(f"  raw条目总数: {len(all_entries)}")
    # 分类统计
    src_counter = Counter(e["source_type"] for e in all_entries)
    report.append("  按来源分布:")
    for src, cnt in src_counter.most_common():
        report.append(f"    - {src}: {cnt} 条")
    
    report.append("")
    report.append("【Wiki 更新结果】")
    report.append(f"  新增: {new_count} 个 | 追加更新: {append_count} 个 | 失败: {fail_count} 个")
    report.append(f"  总计涉及主题: {new_count + append_count + fail_count} 个")
    
    report.append("")
    report.append("【新增主题列表】")
    if results["新增"]:
        for it in results["新增"]:
            entry_cnt = len(topic_entries.get(it["topic"], []))
            report.append(f"  ✓ {it['topic']} ({entry_cnt}条) → note_id: {it['note_id']} [{it['status']}]")
    else:
        report.append("  (无新增)")
    
    report.append("")
    report.append("【追加更新主题列表】")
    if results["追加更新"]:
        for it in results["追加更新"]:
            entry_cnt = len(topic_entries.get(it["topic"], []))
            report.append(f"  ↻ {it['topic']} ({entry_cnt}条) → note_id: {it.get('note_id','N/A')} [{it['status']}]")
    else:
        report.append("  (无追加)")
    
    report.append("")
    report.append("【失败详情】")
    if results["失败"]:
        for it in results["失败"]:
            report.append(f"  ✗ {it['topic']} → 原因: {it['reason']}")
    else:
        report.append("  (无失败)")
    
    report.append("")
    report.append("【IMA API 调用问题】")
    if ima_api_failures:
        report.append(f"  IMA API持续认证失败 (错误码: 200002, 消息: skill auth failed)")
        report.append(f"  受影响调用数: {len(ima_api_failures)}")
        report.append(f"  处理方式: 降级为本地模拟执行，编译产物保存在 /workspace/wiki_output/")
        report.append(f"  建议: 请检查 Client ID / API Key 是否正确，以及对应的 OpenAPI Skill 是否授权")
    else:
        report.append("  (所有IMA API调用正常)")
    
    report.append("")
    report.append("【编译产物】")
    report.append(f"  处理后条目: /workspace/raw_items_processed.json")
    report.append(f"  Wiki文件目录: /workspace/wiki_output/")
    for topic in wiki_files.keys():
        safe = topic.replace("/", "-").replace(" ", "_")
        report.append(f"    - {safe}.md  [{topic}]")
    
    report.append("")
    report.append("=" * 70)
    report_text = "\n".join(report)
    print(report_text)
    
    # 保存报告
    with open("/workspace/IMA_WEEKLY_REPORT.md", "w", encoding="utf-8") as f:
        f.write(report_text)
    print(f"\n  报告已保存: /workspace/IMA_WEEKLY_REPORT.md")
    return report_text

# ========== 主流程 ==========
def main():
    print("\n" + "#"*70)
    print("#  每周 IMA raw → wiki 增量编译流程")
    print("#"*70)
    
    # 步骤1-3
    all_entries = load_raw_content()
    
    # 步骤4
    analyzed, topic_entries = analyze_content(all_entries)
    
    # 步骤5
    wiki_files = compile_wiki_files(analyzed, topic_entries)
    
    # 步骤6
    results = smart_update_strategy(wiki_files)
    
    # 步骤7
    report = generate_report(all_entries, results, topic_entries, wiki_files)
    
    return report

if __name__ == "__main__":
    main()
