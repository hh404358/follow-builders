#!/usr/bin/env python3
import os
import json
import re
import datetime
import requests
from typing import List, Dict, Any, Optional, Set
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class IMAConfig:
    client_id: str
    api_key: str
    raw_kb_id: str
    wiki_kb_id: str


@dataclass
class KnowledgeItem:
    title: str
    content: str
    url: Optional[str] = None
    item_id: Optional[str] = None


class IMAClient:
    def __init__(self, config: IMAConfig):
        self.config = config
        self.base_url = "https://ima.qq.com/openapi"
        self.headers = {
            "ima-openapi-clientid": config.client_id,
            "ima-openapi-apikey": config.api_key,
            "Content-Type": "application/json"
        }

    def get_knowledge_list(self, kb_id: str, cursor: str = "") -> Dict[str, Any]:
        url = f"{self.base_url}/wiki/v1/get_knowledge_list"
        data = {
            "knowledge_base_id": kb_id,
            "cursor": cursor,
            "limit": 50
        }
        print(f"请求 URL: {url}")
        print(f"请求 Headers: {self.headers}")
        print(f"请求数据: {data}")
        response = requests.post(url, headers=self.headers, json=data)
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        response.raise_for_status()
        return response.json()

    def get_all_knowledge_items(self, kb_id: str) -> List[Dict[str, Any]]:
        all_items = []
        cursor = ""
        is_end = False
        
        while not is_end:
            result = self.get_knowledge_list(kb_id, cursor)
            items = result.get("knowledge_list", [])
            all_items.extend(items)
            is_end = result.get("is_end", True)
            cursor = result.get("cursor", "")
        
        return all_items

    def create_note(self, content: str) -> str:
        url = f"{self.base_url}/note/v1/import_doc"
        data = {
            "content_format": 1,
            "content": content
        }
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json().get("note_id")

    def search_note(self, title: str) -> Optional[Dict[str, Any]]:
        url = f"{self.base_url}/note/v1/search_note"
        data = {
            "search_type": 0,
            "query_info": {"title": title},
            "start": 0,
            "end": 20
        }
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        notes = response.json().get("note_list", [])
        return notes[0] if notes else None

    def append_doc(self, note_id: str, content: str):
        url = f"{self.base_url}/note/v1/append_doc"
        data = {
            "note_id": note_id,
            "content_format": 1,
            "content": content
        }
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def add_to_wiki(self, note_id: str, title: str):
        url = f"{self.base_url}/wiki/v1/add_knowledge"
        data = {
            "media_type": 11,
            "note_info": {"content_id": note_id},
            "title": title,
            "knowledge_base_id": self.config.wiki_kb_id
        }
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()


class ContentAnalyzer:
    THEMES = [
        "Claude Code与Harness Engineering",
        "AI Agent架构",
        "DeepSeek技术",
        "Prompt Engineering与AI工作流",
        "Embedding模型选型",
        "AI科研自动化",
        "个人效能与方法论",
        "知识库构建"
    ]

    @staticmethod
    def identify_theme(content: str) -> Optional[str]:
        theme_keywords = {
            "Claude Code与Harness Engineering": ["claude code", "harness", "engineering", "anthropic", "claude"],
            "AI Agent架构": ["agent", "multi-agent", "llm agent", "agent架构"],
            "DeepSeek技术": ["deepseek", "deep seek"],
            "Prompt Engineering与AI工作流": ["prompt", "prompt engineering", "workflow", "工作流"],
            "Embedding模型选型": ["embedding", "向量", "向量数据库", "相似度"],
            "AI科研自动化": ["科研", "research", "自动化", "文献", "paper"],
            "个人效能与方法论": ["个人效能", "productivity", "效率", "方法论", "methodology"],
            "知识库构建": ["知识库", "knowledge base", "wiki", "编译"]
        }
        
        content_lower = content.lower()
        
        for theme, keywords in theme_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                return theme
        
        return None

    @staticmethod
    def analyze_content(raw_items: List[KnowledgeItem]) -> Dict[str, List[KnowledgeItem]]:
        themed_items = defaultdict(list)
        unthemed_items = []
        
        for item in raw_items:
            theme = ContentAnalyzer.identify_theme(item.content + " " + item.title)
            if theme:
                themed_items[theme].append(item)
            else:
                unthemed_items.append(item)
        
        return dict(themed_items)

    @staticmethod
    def generate_summary(items: List[KnowledgeItem]) -> str:
        summary = []
        summary.append("> 摘要\n")
        
        for item in items:
            lines = item.content.split("\n")[:3]
            snippet = "\n".join(lines)
            summary.append(f"- [[{item.title}]]\n  {snippet}\n")
        
        return "\n".join(summary)

    @staticmethod
    def compile_theme_file(theme: str, items: List[KnowledgeItem]) -> str:
        content = []
        content.append(f"# {theme}\n")
        content.append(ContentAnalyzer.generate_summary(items))
        content.append("\n---\n")
        
        for item in items:
            content.append(f"\n## {item.title}\n")
            if item.url:
                content.append(f"- 原始链接: {item.url}\n")
            content.append(f"\n{item.content}\n")
        
        return "\n".join(content)


class WikiCompiler:
    def __init__(self, client: IMAClient, config: IMAConfig):
        self.client = client
        self.config = config
        self.theme_files = {}

    def fetch_raw_knowledge(self) -> List[KnowledgeItem]:
        print("正在获取 raw 知识库内容...")
        items = self.client.get_all_knowledge_items(self.config.raw_kb_id)
        knowledge_items = []
        
        for item in items:
            title = item.get("title", "无标题")
            url = item.get("url")
            content = self._extract_content(item)
            
            if url and "mp.weixin.qq.com" in url:
                try:
                    print(f"正在抓取微信文章: {url}")
                    web_content = self._web_fetch(url)
                    content = web_content if web_content else content
                except Exception as e:
                    print(f"抓取微信文章失败: {e}")
            
            knowledge_items.append(KnowledgeItem(title=title, content=content, url=url))
        
        return knowledge_items

    def _extract_content(self, item: Dict[str, Any]) -> str:
        note_info = item.get("note_info", {})
        return note_info.get("content", "")

    def _web_fetch(self, url: str) -> Optional[str]:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text[:10000]
        except Exception as e:
            print(f"WebFetch 失败: {e}")
            return None

    def compile_themes(self, themed_items: Dict[str, List[KnowledgeItem]]):
        print("正在编译主题文件...")
        for theme, items in themed_items.items():
            self.theme_files[theme] = ContentAnalyzer.compile_theme_file(theme, items)

    def smart_update(self) -> Dict[str, Any]:
        print("正在执行智能更新策略...")
        existing_titles = self._get_existing_wiki_titles()
        results = {"新增": [], "追加更新": [], "失败": []}
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        
        for theme, content in self.theme_files.items():
            try:
                existing_note = self.client.search_note(theme)
                
                if existing_note:
                    note_id = existing_note.get("note_id")
                    append_content = f"\n---\n更新于 {date_str}\n{content}"
                    self.client.append_doc(note_id, append_content)
                    results["追加更新"].append(theme)
                    print(f"已追加更新: {theme}")
                else:
                    note_id = self.client.create_note(content)
                    self.client.add_to_wiki(note_id, theme)
                    results["新增"].append(theme)
                    print(f"已新增: {theme}")
            except Exception as e:
                results["失败"].append({"theme": theme, "error": str(e)})
                print(f"处理失败 {theme}: {e}")
        
        return results

    def _get_existing_wiki_titles(self) -> Set[str]:
        items = self.client.get_all_knowledge_items(self.config.wiki_kb_id)
        return {item.get("title", "") for item in items}

    def generate_report(self, raw_count: int, update_results: Dict[str, Any]):
        print("\n" + "="*50)
        print("IMA 编译报告")
        print("="*50)
        print(f"Raw 条目数: {raw_count}")
        print(f"新增: {len(update_results['新增'])} 个")
        print(f"追加更新: {len(update_results['追加更新'])} 个")
        
        if update_results['新增']:
            print("\n新增主题:")
            for theme in update_results['新增']:
                print(f"  - {theme}")
        
        if update_results['追加更新']:
            print("\n追加更新主题:")
            for theme in update_results['追加更新']:
                print(f"  - {theme}")
        
        if update_results['失败']:
            print("\n失败详情:")
            for fail in update_results['失败']:
                print(f"  - {fail['theme']}: {fail['error']}")


def main():
    config = IMAConfig(
        client_id="673604a6665155cd973af671ab115321",
        api_key="Y869muklEIrSezgzOdqLXdPZ/lOdmqDB3BY/s9DSIfu3+MmsALESLZe5ls2xLXRqfBFzw1OTqw==",
        raw_kb_id="2Oor28yUr2eXyEFPBL0bwQU0DsrUEWPW-u9RF9CIUTw=",
        wiki_kb_id="TcygOiKth0s91W35XJOu4NTAatl-57Bi2g19Wl3jvFw="
    )

    client = IMAClient(config)
    compiler = WikiCompiler(client, config)

    raw_items = compiler.fetch_raw_knowledge()
    themed_items = ContentAnalyzer.analyze_content(raw_items)
    compiler.compile_themes(themed_items)
    update_results = compiler.smart_update()
    compiler.generate_report(len(raw_items), update_results)


if __name__ == "__main__":
    main()
