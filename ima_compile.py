#!/usr/bin/env python3
"""
IMA raw → wiki 增量编译流程
"""

import json
import requests
import time
from datetime import datetime
from typing import Dict, List, Set, Tuple

# API配置
API_KEY = "rSAWpVuJjTYWqwZSXrNWoHZSl+pvxL+tfPOAiW0nwVEAIQv9oToEMRAXHk+WDzGuyaSTh8CI4A=="
CLIENT_ID = "673604a6665155cd973af671ab115321"
RAW_KB_ID = "2Oor28yUr2eXyEFPBL0bwQU0DsrUEWPW-u9RF9CIUTw="
WIKI_KB_ID = "TcygOiKth0s91W35XJOu4NTAatl-57Bi2g19Wl3jvFw="

HEADERS = {
    "ima-openapi-clientid": CLIENT_ID,
    "ima-openapi-apikey": API_KEY,
    "Content-Type": "application/json"
}

BASE_URL = "https://ima.qq.com/openapi"

def api_call(endpoint: str, body: Dict) -> Dict:
    """调用IMA API"""
    url = f"{BASE_URL}/{endpoint}"
    response = requests.post(url, headers=HEADERS, json=body)
    return response.json()

def get_knowledge_list(kb_id: str, folder_id: str = "", cursor: str = "") -> Tuple[List[Dict], bool, str]:
    """获取知识库列表"""
    body = {
        "knowledge_base_id": kb_id,
        "cursor": cursor,
        "limit": 50
    }
    if folder_id:
        body["folder_id"] = folder_id
    
    result = api_call("wiki/v1/get_knowledge_list", body)
    if result.get("code") == 0:
        data = result["data"]
        return data["knowledge_list"], data["is_end"], data["next_cursor"]
    return [], True, ""

def get_all_knowledge(kb_id: str, folder_id: str = "") -> List[Dict]:
    """递归获取所有知识条目"""
    all_items = []
    cursor = ""
    
    while True:
        items, is_end, next_cursor = get_knowledge_list(kb_id, folder_id, cursor)
        all_items.extend(items)
        
        # 递归获取子文件夹
        for item in items:
            if item["media_type"] == 99:  # folder
                sub_items = get_all_knowledge(kb_id, item["media_id"])
                all_items.extend(sub_items)
        
        if is_end:
            break
        cursor = next_cursor
    
    return all_items

def search_note(title: str) -> Dict:
    """搜索笔记"""
    body = {
        "search_type": 0,
        "query_info": {"title": title},
        "start": 0,
        "end": 20
    }
    return api_call("note/v1/search_note", body)

def create_note(content: str) -> str:
    """创建笔记"""
    body = {
        "content_format": 1,
        "content": content
    }
    result = api_call("note/v1/import_doc", body)
    if result.get("code") == 0:
        return result["data"]["note_id"]
    return ""

def append_note(note_id: str, content: str) -> bool:
    """追加笔记内容"""
    body = {
        "note_id": note_id,
        "content_format": 1,
        "content": content
    }
    result = api_call("note/v1/append_doc", body)
    return result.get("code") == 0

def add_to_wiki(note_id: str, title: str) -> bool:
    """添加笔记到wiki知识库"""
    body = {
        "media_type": 11,
        "note_info": {"content_id": note_id},
        "title": title,
        "knowledge_base_id": WIKI_KB_ID
    }
    result = api_call("wiki/v1/add_knowledge", body)
    return result.get("code") == 0

def main():
    print("=" * 60)
    print("IMA raw → wiki 增量编译流程")
    print("=" * 60)
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 步骤1: 获取raw知识库所有内容
    print("步骤1: 获取raw知识库所有内容...")
    raw_items = get_all_knowledge(RAW_KB_ID)
    
    # 过滤掉文件夹，只保留实际内容
    content_items = [item for item in raw_items if item["media_type"] != 99]
    
    print(f"  - 总条目数: {len(raw_items)}")
    print(f"  - 内容条目数: {len(content_items)}")
    print(f"  - 文件夹数: {len(raw_items) - len(content_items)}")
    print()
    
    # 步骤2: 获取wiki当前列表
    print("步骤2: 获取wiki知识库当前列表...")
    wiki_items = get_all_knowledge(WIKI_KB_ID)
    wiki_titles = {item["title"] for item in wiki_items}
    
    print(f"  - wiki现有条目数: {len(wiki_items)}")
    print(f"  - 已存在主题数: {len(wiki_titles)}")
    print()
    
    # 步骤3: 分析内容并识别主题
    print("步骤3: 分析内容并识别主题...")
    
    # 定义主题分类规则
    themes = {
        "Claude Code与Harness Engineering": {
            "keywords": ["Claude Code", "Harness", "Karpathy", "源码", "逆向工程", "Mythos", "Auto Mode"],
            "items": []
        },
        "AI Agent架构": {
            "keywords": ["Agent", "OpenClaw", "Hermes", "DeerFlow", "nanobot", "GBrain", "Multi-Agent"],
            "items": []
        },
        "DeepSeek技术": {
            "keywords": ["DeepSeek", "LCA", "长文本", "KV Cache", "多模态", "V4"],
            "items": []
        },
        "Prompt Engineering与AI工作流": {
            "keywords": ["Prompt", "提示词", "Token", "Vibe", "Skill", "工作流", "优化"],
            "items": []
        },
        "Embedding模型选型": {
            "keywords": ["Embedding", "Gemini", "jina", "Qwen", "BGE", "OpenAI"],
            "items": []
        },
        "AI科研自动化": {
            "keywords": ["科研", "DeepScientist", "论文", "绘图", "自动化", "北大开源"],
            "items": []
        },
        "个人效能与方法论": {
            "keywords": ["效能", "七习惯", "金字塔", "学会提问", "空腹力", "学习方法"],
            "items": []
        },
        "知识库构建": {
            "keywords": ["知识库", "IMA", "第二大脑", "分类学"],
            "items": []
        }
    }
    
    # 分类条目
    for item in content_items:
        title = item["title"]
        matched = False
        
        for theme_name, theme_data in themes.items():
            for keyword in theme_data["keywords"]:
                if keyword.lower() in title.lower():
                    theme_data["items"].append(item)
                    matched = True
                    break
        
        if not matched:
            # 未匹配的条目归入"其他"
            if "其他" not in themes:
                themes["其他"] = {"keywords": [], "items": []}
            themes["其他"]["items"].append(item)
    
    # 显示分类结果
    print("  主题分类统计:")
    for theme_name, theme_data in themes.items():
        count = len(theme_data["items"])
        if count > 0:
            print(f"    - {theme_name}: {count}条")
    print()
    
    # 步骤4: 编译wiki文件并执行智能更新
    print("步骤4: 编译wiki文件并执行智能更新...")
    
    new_count = 0
    update_count = 0
    failed_count = 0
    failed_details = []
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    for theme_name, theme_data in themes.items():
        if len(theme_data["items"]) == 0:
            continue
        
        print(f"\n  处理主题: {theme_name}")
        
        # 编译wiki内容
        content = f"# {theme_name}\n\n"
        content += f"> 摘要：本主题整合 {len(theme_data['items'])} 条原始材料，涵盖{theme_name}的核心进展。\n\n"
        content += f"更新于 {today}\n\n"
        content += "## 来源条目\n\n"
        
        for item in theme_data["items"]:
            title = item["title"]
            media_type = item["media_type"]
            content += f"- [[{title}]] (来源类型: media_type={media_type})\n"
        
        content += "\n## 核心要点\n\n"
        content += "（基于原始材料的深度分析）\n\n"
        
        # 检查wiki中是否已存在
        existing_title = None
        existing_note_id = None
        
        # 使用更宽松的匹配：搜索包含主题关键词的笔记
        search_result = search_note(theme_name)
        if search_result.get("code") == 0:
            # 搜索API返回的是 search_note_infos，不是 note_list
            note_infos = search_result.get("data", {}).get("search_note_infos", [])
            if not note_infos:
                note_infos = search_result.get("data", {}).get("note_list", [])
            
            for note_info in note_infos:
                # 兼容两种数据结构
                note_book_info = note_info.get("note_book_info", note_info)
                note_title = note_book_info.get("title", "")
                note_id = note_book_info.get("note_id", "")
                
                # 检查标题是否包含主题名称或主题名称包含标题
                # 使用更宽松的匹配：只要标题包含主题的核心关键词即可
                theme_keywords = theme_name.replace("与", " ").replace("和", " ").split()
                match_count = 0
                for keyword in theme_keywords:
                    if len(keyword) >= 3 and keyword in note_title:  # 只匹配长度>=3的关键词
                        match_count += 1
                
                # 至少匹配一个关键词
                if match_count >= 1:
                    existing_title = note_title
                    existing_note_id = note_id
                    break
        
        if existing_note_id:
            # 追加更新
            print(f"    - 状态: 已存在，追加更新")
            print(f"    - 匹配标题: {existing_title}")
            
            append_content = f"\n---\n更新于 {today}\n新增条目: {len(theme_data['items'])}条\n"
            
            if append_note(existing_note_id, append_content):
                update_count += 1
                print(f"    - 结果: 追加成功")
            else:
                failed_count += 1
                failed_details.append(f"{theme_name}: 追加失败")
                print(f"    - 结果: 追加失败")
        else:
            # 创建新笔记
            print(f"    - 状态: 不存在，创建新笔记")
            
            note_id = create_note(content)
            if note_id:
                if add_to_wiki(note_id, theme_name):
                    new_count += 1
                    print(f"    - 结果: 创建成功并添加到wiki")
                else:
                    failed_count += 1
                    failed_details.append(f"{theme_name}: 添加到wiki失败")
                    print(f"    - 结果: 添加到wiki失败")
            else:
                failed_count += 1
                failed_details.append(f"{theme_name}: 创建笔记失败")
                print(f"    - 结果: 创建笔记失败")
    
    print()
    
    # 步骤5: 生成报告
    print("=" * 60)
    print("编译完成报告")
    print("=" * 60)
    print(f"raw条目总数: {len(content_items)}")
    print(f"新增主题: {new_count}个")
    print(f"追加更新: {update_count}个")
    print(f"失败详情: {failed_count}个")
    
    if failed_details:
        print("\n失败详情:")
        for detail in failed_details:
            print(f"  - {detail}")
    
    print()
    print("=" * 60)

if __name__ == "__main__":
    main()