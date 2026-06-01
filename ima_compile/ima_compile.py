#!/usr/bin/env python3
import requests
import json
import os
from datetime import datetime
from typing import List, Dict, Any


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
            "new_topics": [],
            "updated_topics": [],
            "failures": []
        }
        self.existing_wiki_titles = set()
        
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

    def get_knowledge_list(self, kb_id: str) -> List[Dict]:
        """获取知识库列表，支持分页"""
        all_items = []
        cursor = ""
        while True:
            url = f"{self.base_url}/wiki/v1/get_knowledge_list"
            data = {
                "knowledge_base_id": kb_id,
                "cursor": cursor,
                "limit": 50
            }
            try:
                response = requests.post(url, headers=self.headers, json=data)
                response.raise_for_status()
                result = response.json()
                items = result.get("data", {}).get("list", [])
                all_items.extend(items)
                if result.get("data", {}).get("is_end", True):
                    break
                cursor = result.get("data", {}).get("cursor", "")
            except Exception as e:
                self.report["failures"].append(f"获取知识库列表失败: {str(e)}")
                break
        return all_items

    def fetch_wechat_article(self, url: str) -> str:
        """使用WebFetch获取微信文章内容"""
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except Exception as e:
            self.report["failures"].append(f"获取微信文章失败 {url}: {str(e)}")
            return ""

    def collect_raw_content(self):
        """步骤1: 获取raw知识库内容"""
        print("步骤1: 收集raw知识库内容...")
        self.raw_entries = self.get_knowledge_list(self.raw_kb_id)
        self.report["raw_entries_count"] = len(self.raw_entries)
        
        for entry in self.raw_entries:
            if entry.get("media_type") == 1:  # 假设1是链接类型
                url = entry.get("url", "")
                if url and ("weixin" in url or "mp.weixin" in url):
                    content = self.fetch_wechat_article(url)
                    entry["content"] = content
        
        print(f"  收集到 {len(self.raw_entries)} 条raw条目")

    def analyze_content(self):
        """步骤2: 按CLAUDE.md分析内容（纵向溯源/横向对比/趋势判断）"""
        print("步骤2: 分析内容...")
        analyzed_content = []
        for entry in self.raw_entries:
            title = entry.get("title", "无标题")
            content = entry.get("content", "") or entry.get("summary", "") or f"标题: {title}"
            analyzed_content.append({
                "title": title,
                "content": content,
                "raw_entry": entry
            })
        self.analyzed_content = analyzed_content

    def identify_topics(self):
        """步骤3: 识别主题"""
        print("步骤3: 识别主题...")
        self.topic_content = {topic: [] for topic in self.topics}
        
        for item in self.analyzed_content:
            title = item["title"].lower()
            content = item["content"].lower()
            assigned = False
            
            for topic in self.topics:
                topic_lower = topic.lower()
                keywords = topic_lower.split()
                if any(kw in title or kw in content for kw in keywords):
                    self.topic_content[topic].append(item)
                    assigned = True
                    break
            
            if not assigned:
                self.topic_content["知识库构建"].append(item)

    def compile_wiki_files(self):
        """步骤4: 编译wiki文件"""
        print("步骤4: 编译wiki文件...")
        for topic, items in self.topic_content.items():
            if not items:
                continue
                
            content = f"# {topic}\n\n"
            content += "> 汇总时间: " + datetime.now().strftime("%Y-%m-%d") + "\n\n"
            
            for item in items:
                title = item["title"]
                item_content = item["content"]
                content += f"## {title}\n\n"
                content += f"{item_content}\n\n"
                content += f"[[{title}]]\n\n"
            
            self.wiki_files[topic] = content

    def get_existing_wiki_notes(self):
        """获取wiki中已存在的笔记"""
        print("获取wiki现有笔记...")
        wiki_items = self.get_knowledge_list(self.wiki_kb_id)
        self.existing_wiki_titles = {item.get("title", "") for item in wiki_items}

    def search_note(self, title: str) -> str:
        """搜索笔记ID"""
        url = f"{self.base_url}/note/v1/search_note"
        data = {
            "search_type": 0,
            "query_info": {"title": title},
            "start": 0,
            "end": 20
        }
        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            result = response.json()
            notes = result.get("data", {}).get("notes", [])
            for note in notes:
                if note.get("title") == title:
                    return note.get("note_id")
        except Exception as e:
            self.report["failures"].append(f"搜索笔记失败 {title}: {str(e)}")
        return ""

    def create_note(self, title: str, content: str) -> str:
        """创建笔记"""
        url = f"{self.base_url}/note/v1/import_doc"
        data = {
            "content_format": 1,
            "content": content
        }
        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            result = response.json()
            return result.get("data", {}).get("note_id", "")
        except Exception as e:
            self.report["failures"].append(f"创建笔记失败 {title}: {str(e)}")
            return ""

    def append_doc(self, note_id: str, content: str):
        """追加内容到笔记"""
        url = f"{self.base_url}/note/v1/append_doc"
        data = {
            "note_id": note_id,
            "content_format": 1,
            "content": content
        }
        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            return True
        except Exception as e:
            self.report["failures"].append(f"追加内容失败 {note_id}: {str(e)}")
            return False

    def add_to_wiki(self, note_id: str, title: str):
        """添加笔记到wiki"""
        url = f"{self.base_url}/wiki/v1/add_knowledge"
        data = {
            "media_type": 11,
            "note_info": {"content_id": note_id},
            "title": title,
            "knowledge_base_id": self.wiki_kb_id
        }
        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            return True
        except Exception as e:
            self.report["failures"].append(f"添加到wiki失败 {title}: {str(e)}")
            return False

    def smart_update(self):
        """步骤5: 智能更新策略"""
        print("步骤5: 执行智能更新...")
        self.get_existing_wiki_notes()
        
        for topic, content in self.wiki_files.items():
            if topic in self.existing_wiki_titles:
                note_id = self.search_note(topic)
                if note_id:
                    append_content = f"\n---\n更新于 {datetime.now().strftime('%Y-%m-%d')}\n{content}"
                    if self.append_doc(note_id, append_content):
                        self.report["updated_topics"].append(topic)
                        print(f"  已追加更新: {topic}")
            else:
                note_id = self.create_note(topic, content)
                if note_id:
                    if self.add_to_wiki(note_id, topic):
                        self.report["new_topics"].append(topic)
                        print(f"  新增: {topic}")

    def generate_report(self):
        """步骤6: 生成报告"""
        print("\n" + "="*50)
        print("IMA raw → wiki 增量编译报告")
        print("="*50)
        print(f"Raw条目数: {self.report['raw_entries_count']}")
        print(f"新增: {len(self.report['new_topics'])}个")
        for topic in self.report["new_topics"]:
            print(f"  - {topic}")
        print(f"追加更新: {len(self.report['updated_topics'])}个")
        for topic in self.report["updated_topics"]:
            print(f"  - {topic}")
        if self.report["failures"]:
            print(f"失败详情:")
            for failure in self.report["failures"]:
                print(f"  - {failure}")
        print("="*50)

    def run(self):
        """执行完整流程"""
        print("开始执行 IMA raw → wiki 增量编译流程...")
        self.collect_raw_content()
        self.analyze_content()
        self.identify_topics()
        self.compile_wiki_files()
        self.smart_update()
        self.generate_report()
        print("流程完成！")


if __name__ == "__main__":
    compiler = IMACompiler()
    compiler.run()
