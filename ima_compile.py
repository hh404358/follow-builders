import requests
import json
import re
from datetime import datetime, timezone
from urllib.parse import urlparse

API_KEY = "rSAWpVuJjTYWqwZSXrNWoHZSl+pvxL+tfPOAiW0nwVEAIQv9oToEMRAXHk+WDzGuyaSTh8CI4A=="
CLIENT_ID = "673604a6665155cd973af671ab115321"
RAW_KB_ID = "2Oor28yUr2eXyEFPBL0bwQU0DsrUEWPW-u9RF9CIUTw="
WIKI_KB_ID = "TcygOiKth0s91W35XJOu4NTAatl-57Bi2g19Wl3jvFw="

BASE_URL = "https://ima.qq.com/openapi"

headers = {
    "ima-openapi-clientid": CLIENT_ID.strip(),
    "ima-openapi-apikey": API_KEY.strip(),
    "Content-Type": "application/json"
}

EXISTING_TOPICS = [
    "Claude Code与Harness Engineering",
    "AI Agent架构",
    "DeepSeek技术",
    "Prompt Engineering与AI工作流",
    "Embedding模型选型",
    "AI科研自动化",
    "个人效能与方法论",
    "知识库构建"
]

topic_keywords = {
    "Claude Code与Harness Engineering": ["claude", "code", "harness", "engineering", "developer", "dev"],
    "AI Agent架构": ["agent", "architecture", "agentic", "multi-agent", "workflow"],
    "DeepSeek技术": ["deepseek", "model", "llm", "inference"],
    "Prompt Engineering与AI工作流": ["prompt", "engineering", "prompting", "workflow", "prompting"],
    "Embedding模型选型": ["embedding", "vector", "retrieval", "rag"],
    "AI科研自动化": ["research", "science", "automation", "paper", "arxiv"],
    "个人效能与方法论": ["productivity", "efficiency", "methodology", "workflow", "todo"],
    "知识库构建": ["knowledge", "kb", "database", "information", "retrieval"]
}

def api_request(method, endpoint, data=None):
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method == "GET":
            response = requests.get(url, headers=headers, params=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"API请求失败 {endpoint}: {e}")
        return None

def get_knowledge_list(kb_id, cursor=""):
    results = []
    while True:
        data = {"knowledge_base_id": kb_id, "cursor": cursor, "limit": 50}
        response = api_request("POST", "/wiki/v1/get_knowledge_list", data)
        if not response or "data" not in response:
            break
        items = response.get("data", {}).get("items", [])
        results.extend(items)
        is_end = response.get("data", {}).get("is_end", True)
        cursor = response.get("data", {}).get("cursor", "")
        if is_end or not cursor:
            break
    return results

def search_note(title):
    data = {
        "search_type": 0,
        "query_info": {"title": title},
        "start": 0,
        "end": 20
    }
    response = api_request("POST", "/note/v1/search_note", data)
    if response and "data" in response:
        return response["data"].get("items", [])
    return []

def create_note(content):
    data = {"content_format": 1, "content": content}
    response = api_request("POST", "/note/v1/import_doc", data)
    if response and "data" in response:
        return response["data"].get("note_id")
    return None

def append_doc(note_id, content):
    data = {"note_id": note_id, "content_format": 1, "content": content}
    response = api_request("POST", "/note/v1/append_doc", data)
    return response is not None and response.get("code") == 0

def add_wiki_knowledge(note_id, title, kb_id):
    data = {
        "media_type": 11,
        "note_info": {"content_id": note_id},
        "title": title,
        "knowledge_base_id": kb_id
    }
    response = api_request("POST", "/wiki/v1/add_knowledge", data)
    return response is not None and response.get("code") == 0

def webfetch(url):
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"WebFetch失败 {url}: {e}")
        return None

def extract_text_from_html(html):
    text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def classify_topic(title, content):
    text = (title + " " + content).lower()
    for topic, keywords in topic_keywords.items():
        for keyword in keywords:
            if keyword.lower() in text:
                return topic
    return "AI科研自动化"

def analyze_content(content):
    lines = content.split('\n')
    summary_lines = []
    key_points = []
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('>'):
            summary_lines.append(stripped)
        elif len(stripped) > 20 and not stripped.startswith('#'):
            key_points.append(stripped[:100])
    
    return {
        "summary": "\n".join(summary_lines),
        "key_points": key_points[:5]
    }

def build_markdown(topic, items):
    md = f"# {topic}\n\n"
    md += f"> 主题概述：{topic} 相关的最新研究和实践\n\n"
    
    for item in items:
        title = item.get("title", "未命名")
        content = item.get("content", "")
        url = item.get("url", "")
        
        md += f"## {title}\n\n"
        
        if url:
            md += f"来源：{url}\n\n"
        
        analysis = analyze_content(content)
        if analysis["summary"]:
            md += analysis["summary"] + "\n\n"
        
        if analysis["key_points"]:
            md += "### 核心要点\n\n"
            for point in analysis["key_points"]:
                md += f"- {point}\n"
            md += "\n"
        
        related_topics = []
        for t in EXISTING_TOPICS:
            if t != topic and any(kw.lower() in (title + content).lower() for kw in topic_keywords[t]):
                related_topics.append(t)
        
        if related_topics:
            md += "### 相关主题\n\n"
            for rt in related_topics:
                md += f"[[{rt}]]\n"
            md += "\n"
        
        md += "---\n\n"
    
    return md

def main():
    print("=" * 60)
    print("IMA Raw → Wiki 增量编译流程")
    print("=" * 60)
    
    print("\n步骤1: 获取raw知识库内容...")
    raw_items = get_knowledge_list(RAW_KB_ID)
    print(f"Raw知识库条目数: {len(raw_items)}")
    
    enriched_items = []
    for item in raw_items:
        title = item.get("title", "未命名")
        content = item.get("content", "")
        url = item.get("url", "")
        
        if url and ("mp.weixin.qq.com" in url or "weixin" in url.lower()):
            print(f"获取微信文章: {url}")
            html_content = webfetch(url)
            if html_content:
                content = extract_text_from_html(html_content)
        
        enriched_items.append({
            "title": title,
            "content": content,
            "url": url
        })
    
    print("\n步骤2: 分析内容...")
    print("\n步骤3: 识别主题...")
    
    topic_items = {}
    for item in enriched_items:
        topic = classify_topic(item["title"], item["content"])
        if topic not in topic_items:
            topic_items[topic] = []
        topic_items[topic].append(item)
    
    print(f"识别到的主题: {list(topic_items.keys())}")
    
    print("\n步骤4: 编译wiki文件...")
    topic_contents = {}
    for topic, items in topic_items.items():
        md = build_markdown(topic, items)
        topic_contents[topic] = md
        print(f"  - {topic}: {len(items)} 个条目")
    
    print("\n步骤5: 智能更新策略...")
    print("  A. 获取wiki当前列表...")
    wiki_items = get_knowledge_list(WIKI_KB_ID)
    existing_titles = {item.get("title", "") for item in wiki_items}
    print(f"  Wiki现有条目数: {len(existing_titles)}")
    
    new_count = 0
    append_count = 0
    failed_items = []
    
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    for topic, content in topic_contents.items():
        print(f"\n  处理主题: {topic}")
        
        if topic in existing_titles:
            print(f"    - 已存在，尝试追加更新...")
            search_results = search_note(topic)
            if search_results:
                note_id = search_results[0].get("note_id")
                if note_id:
                    append_content = f"\n---\n更新于 {today}\n{content}"
                    success = append_doc(note_id, append_content)
                    if success:
                        append_count += 1
                        print(f"    ✓ 追加更新成功")
                    else:
                        failed_items.append(f"{topic}: 追加更新失败")
                        print(f"    ✗ 追加更新失败")
                else:
                    failed_items.append(f"{topic}: 未找到note_id")
                    print(f"    ✗ 未找到note_id")
            else:
                failed_items.append(f"{topic}: 搜索笔记失败")
                print(f"    ✗ 搜索笔记失败")
        else:
            print(f"    - 不存在，创建新笔记...")
            note_id = create_note(content)
            if note_id:
                success = add_wiki_knowledge(note_id, topic, WIKI_KB_ID)
                if success:
                    new_count += 1
                    print(f"    ✓ 新增成功")
                else:
                    failed_items.append(f"{topic}: 添加到wiki失败")
                    print(f"    ✗ 添加到wiki失败")
            else:
                failed_items.append(f"{topic}: 创建笔记失败")
                print(f"    ✗ 创建笔记失败")
    
    print("\n" + "=" * 60)
    print("步骤6: 报告")
    print("=" * 60)
    print(f"\nRaw条目数: {len(raw_items)}")
    print(f"新增: {new_count} 个")
    print(f"追加更新: {append_count} 个")
    
    if new_count > 0:
        print(f"\n新增主题:")
        for topic in topic_contents.keys():
            if topic not in existing_titles:
                print(f"  - {topic}")
    
    if append_count > 0:
        print(f"\n追加更新主题:")
        for topic in topic_contents.keys():
            if topic in existing_titles:
                print(f"  - {topic}")
    
    if failed_items:
        print(f"\n失败详情:")
        for item in failed_items:
            print(f"  - {item}")
    
    print(f"\n编译完成于 {today}")

if __name__ == "__main__":
    main()