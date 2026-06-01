#!/usr/bin/env python3
import requests
import json
import re
import time
from datetime import datetime
from typing import List, Dict, Optional, Tuple


class IMACompiler:
    def __init__(self):
        self.api_key = "rSAWpVuJjTYWqwZSXrNWoHZSl+pvxL+tfPOAiW0nwVEAIQv9oToEMRAXHk+WDzGuyaSTh8CI4A=="
        self.client_id = "673604a6665155cd973af671ab115321"
        self.raw_kb_id = "2Oor28yUr2eXyEFPBL0bwQU0DsrUEWPW-u9RF9CIUTw="
        self.wiki_kb_id = "TcygOiKth0s91W35XJOu4NTAatl-57Bi2g19Wl3jvFw="
        self.base_url = "https://ima.qq.com/openapi"
        self.headers = {
            "ima-openapi-clientid": self.client_id,
            "ima-openapi-apikey": self.api_key,
            "Content-Type": "application/json"
        }
        self.raw_entries = []
        self.wiki_files = {}
        self.report = {
            "raw_entries_count": 0,
            "raw_articles_count": 0,
            "new_topics": [],
            "updated_topics": [],
            "failures": []
        }
        self.existing_wiki_notes = {}
        
        self.topics = [
            "Claude Code与Harness Engineering",
            "AI Agent架构",
            "DeepSeek技术",
            "Prompt Engineering与AI工作流",
            "Embedding模型选型",
            "AI科研自动化",
            "个人效能与方法论",
            "知识库构建"
        ]

        self.topic_keywords = {
            "Claude Code与Harness Engineering": [
                "claude code", "harness", "源码", "anthropic", "claude",
                "mythos", "karpathy", "cli", "mcp"
            ],
            "AI Agent架构": [
                "agent", "openclaw", "hermes", "deerflow", "nanobot",
                "multi-agent", "单agent", "架构选型", "gbrain", "skill",
                "kv cache"
            ],
            "DeepSeek技术": [
                "deepseek", "lca", "kv缓存", "多模态技术报告",
                "极致压缩", "视觉原语", "昇腾"
            ],
            "Prompt Engineering与AI工作流": [
                "prompt", "optimize", "skill", "perplexity",
                "工作流", "优化"
            ],
            "Embedding模型选型": [
                "embedding", "jina", "bge", "qwen", "gemini",
                "向量", "模型选型"
            ],
            "AI科研自动化": [
                "科研", "自进化", "清华", "北大", "论文",
                "huggingface", "自动化", "acl", "cvpr"
            ],
            "个人效能与方法论": [
                "dan koe", "效能", "方法论", "目标", "程序员",
                "鱼皮", "初级", "高级", "appso"
            ],
            "知识库构建": [
                "知识库", "wiki", "digest", "analysis",
                "markdown", "索引"
            ]
        }

    def api_call(self, endpoint: str, data: dict) -> Optional[dict]:
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.post(url, headers=self.headers, json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            if result.get("code") != 0:
                self.report["failures"].append(
                    f"API错误 {endpoint}: code={result.get('code')}, msg={result.get('msg')}"
                )
                return None
            return result.get("data", {})
        except Exception as e:
            self.report["failures"].append(f"API调用失败 {endpoint}: {str(e)}")
            return None

    def get_knowledge_list(self, kb_id: str) -> List[Dict]:
        all_items = []
        cursor = ""
        while True:
            data = {
                "knowledge_base_id": kb_id,
                "cursor": cursor,
                "limit": 50
            }
            result = self.api_call("wiki/v1/get_knowledge_list", data)
            if not result:
                break
            items = result.get("knowledge_list", [])
            all_items.extend(items)
            if result.get("is_end", True):
                break
            cursor = result.get("cursor", "")
            if not cursor:
                break
        return all_items

    def search_note(self, title: str) -> List[Dict]:
        data = {
            "search_type": 0,
            "query_info": {"title": title},
            "start": 0,
            "end": 20
        }
        result = self.api_call("note/v1/search_note", data)
        if not result:
            return []
        return result.get("search_note_infos", [])

    def create_note(self, content: str) -> Optional[str]:
        data = {
            "content_format": 1,
            "content": content
        }
        result = self.api_call("note/v1/import_doc", data)
        if result:
            return result.get("note_id", "")
        return None

    def append_doc(self, note_id: str, content: str) -> bool:
        data = {
            "note_id": note_id,
            "content_format": 1,
            "content": content
        }
        result = self.api_call("note/v1/append_doc", data)
        return result is not None

    def add_to_wiki(self, note_id: str, title: str) -> bool:
        data = {
            "media_type": 11,
            "note_info": {"content_id": note_id},
            "title": title,
            "knowledge_base_id": self.wiki_kb_id
        }
        result = self.api_call("wiki/v1/add_knowledge", data)
        return result is not None

    def fetch_wechat_article_content(self, title: str) -> str:
        try:
            search_url = "https://www.google.com/search?q=" + requests.utils.quote(title + " 微信公众号")
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            r = requests.get(search_url, headers=headers, timeout=10)
            urls = re.findall(r'https?://mp\.weixin\.qq\.com/s[^\s&"<>]+', r.text)
            if urls:
                article_url = urls[0].replace("&amp;", "&")
                ar = requests.get(article_url, headers=headers, timeout=15)
                ar.raise_for_status()
                text = re.sub(r'<[^>]+>', '', ar.text)
                text = re.sub(r'\s+', ' ', text).strip()
                return text[:3000]
        except Exception as e:
            pass
        return ""

    def collect_raw_content(self):
        print("=" * 60)
        print("步骤1: 收集raw知识库内容")
        print("=" * 60)
        all_items = self.get_knowledge_list(self.raw_kb_id)
        
        self.raw_entries = [
            item for item in all_items
            if item.get("media_type") != 99
        ]
        
        self.report["raw_entries_count"] = len(all_items)
        self.report["raw_articles_count"] = len(self.raw_entries)
        
        wechat_count = sum(1 for e in self.raw_entries if e.get("media_type") == 6)
        print(f"  总条目数: {len(all_items)} (含文件夹)")
        print(f"  内容条目数: {len(self.raw_entries)}")
        print(f"  微信文章: {wechat_count}")
        print(f"  其他类型: {len(self.raw_entries) - wechat_count}")
        
        print("\n  正在获取微信文章内容...")
        fetched = 0
        for entry in self.raw_entries:
            if entry.get("media_type") == 6:
                title = entry.get("title", "")
                content = self.fetch_wechat_article_content(title)
                if content:
                    entry["fetched_content"] = content
                    fetched += 1
                    print(f"    ✓ {title[:40]}")
                else:
                    print(f"    ✗ {title[:40]} (跳过)")
                time.sleep(0.5)
        print(f"  成功获取 {fetched}/{wechat_count} 篇微信文章内容")

    def analyze_content(self):
        print("\n" + "=" * 60)
        print("步骤2: 分析内容 (纵向溯源/横向对比/趋势判断)")
        print("=" * 60)
        self.analyzed_content = []
        for entry in self.raw_entries:
            title = entry.get("title", "无标题")
            media_type = entry.get("media_type", 0)
            
            content_parts = []
            content_parts.append(f"标题: {title}")
            
            if entry.get("fetched_content"):
                content_parts.append(entry["fetched_content"][:2000])
            
            content = "\n".join(content_parts)
            
            self.analyzed_content.append({
                "title": title,
                "content": content,
                "media_type": media_type,
                "media_id": entry.get("media_id", ""),
                "raw_entry": entry
            })
        
        print(f"  分析完成: {len(self.analyzed_content)} 条内容")

    def identify_topics(self):
        print("\n" + "=" * 60)
        print("步骤3: 识别主题")
        print("=" * 60)
        self.topic_content = {topic: [] for topic in self.topics}
        
        for item in self.analyzed_content:
            title_lower = item["title"].lower()
            content_lower = item["content"].lower()
            combined = title_lower + " " + content_lower
            
            best_topic = None
            best_score = 0
            
            for topic, keywords in self.topic_keywords.items():
                score = sum(1 for kw in keywords if kw in combined)
                if score > best_score:
                    best_score = score
                    best_topic = topic
            
            if best_score == 0:
                best_topic = "知识库构建"
            
            self.topic_content[best_topic].append(item)
        
        for topic, items in self.topic_content.items():
            if items:
                print(f"  {topic}: {len(items)} 条")
                for item in items:
                    print(f"    - {item['title'][:50]}")

    def compile_wiki_files(self):
        print("\n" + "=" * 60)
        print("步骤4: 编译wiki文件")
        print("=" * 60)
        today = datetime.now().strftime("%Y-%m-%d")
        
        for topic, items in self.topic_content.items():
            if not items:
                continue
            
            content = f"# {topic}\n\n"
            content += f"> 增量编译于 {today} | 来源条目: {len(items)}\n\n"
            
            for item in items:
                title = item["title"]
                item_content = item["content"]
                
                content += f"## {title}\n\n"
                
                if item.get("fetched_content"):
                    summary = item["fetched_content"][:800]
                    content += f"{summary}\n\n"
                else:
                    content += f"来源类型: media_type={item['media_type']}\n\n"
                
                related_topics = [
                    t for t in self.topics 
                    if t != topic and any(
                        kw in title.lower() 
                        for kw in self.topic_keywords.get(t, [])
                    )
                ]
                if related_topics:
                    content += "关联主题: " + " ".join(f"[[{rt}]]" for rt in related_topics) + "\n\n"
                
                content += f"[[{title}]]\n\n"
            
            self.wiki_files[topic] = content
            print(f"  ✓ {topic} ({len(items)} 条目)")

    def get_existing_wiki_notes(self):
        print("\n  获取wiki现有笔记...")
        wiki_items = self.get_knowledge_list(self.wiki_kb_id)
        
        for item in wiki_items:
            title = item.get("title", "")
            media_id = item.get("media_id", "")
            if item.get("media_type") == 11 and title:
                self.existing_wiki_notes[title] = media_id
        
        print(f"  现有wiki笔记: {len(self.existing_wiki_notes)} 个")

    def find_wiki_note_id(self, topic: str) -> Optional[str]:
        notes = self.search_note(topic)
        for note_info in notes:
            note_book = note_info.get("note_book_info", {})
            note_title = note_book.get("title", "")
            note_id = note_book.get("note_id", "")
            if topic in note_title or note_title in topic:
                return note_id
        return None

    def smart_update(self):
        print("\n" + "=" * 60)
        print("步骤5: 智能更新策略")
        print("=" * 60)
        self.get_existing_wiki_notes()
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        for topic, content in self.wiki_files.items():
            existing_note_id = None
            existing_title = None
            
            for wiki_title, wiki_media_id in self.existing_wiki_notes.items():
                if topic in wiki_title or wiki_title in topic:
                    existing_title = wiki_title
                    break
            
            if existing_title:
                note_id = self.find_wiki_note_id(topic)
                if note_id:
                    append_content = (
                        f"\n---\n"
                        f"更新于 {today}\n\n"
                        f"{content}"
                    )
                    if self.append_doc(note_id, append_content):
                        self.report["updated_topics"].append(topic)
                        print(f"  📝 已追加更新: {topic} (note_id={note_id})")
                    else:
                        self.report["failures"].append(f"追加更新失败: {topic}")
                else:
                    self.report["failures"].append(f"找到wiki笔记但无法获取note_id: {topic}")
            else:
                note_id = self.create_note(content)
                if note_id:
                    if self.add_to_wiki(note_id, topic):
                        self.report["new_topics"].append(topic)
                        print(f"  ✨ 新增: {topic} (note_id={note_id})")
                    else:
                        self.report["failures"].append(f"添加到wiki失败: {topic}")
                else:
                    self.report["failures"].append(f"创建笔记失败: {topic}")

    def generate_report(self):
        print("\n" + "=" * 60)
        print("步骤6: 编译报告")
        print("=" * 60)
        print(f"  Raw总条目数: {self.report['raw_entries_count']}")
        print(f"  Raw内容条目数: {self.report['raw_articles_count']}")
        print(f"  新增: {len(self.report['new_topics'])} 个")
        for t in self.report["new_topics"]:
            print(f"    ✨ {t}")
        print(f"  追加更新: {len(self.report['updated_topics'])} 个")
        for t in self.report["updated_topics"]:
            print(f"    📝 {t}")
        if self.report["failures"]:
            print(f"  失败详情: {len(self.report['failures'])} 个")
            for f in self.report["failures"]:
                print(f"    ✗ {f}")
        else:
            print("  失败详情: 无")
        print("=" * 60)

    def run(self):
        print("🚀 开始执行 IMA raw → wiki 增量编译流程")
        print(f"   时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.collect_raw_content()
        self.analyze_content()
        self.identify_topics()
        self.compile_wiki_files()
        self.smart_update()
        self.generate_report()
        
        print("\n✅ 流程完成！")


if __name__ == "__main__":
    compiler = IMACompiler()
    compiler.run()
