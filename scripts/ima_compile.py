#!/usr/bin/env python3
import os
import json
import requests
from datetime import datetime
from typing import List, Dict, Any

# IMA Configuration
IMA_API_KEY = "rSAWpVuJjTYWqwZSXrNWoHZSl+pvxL+tfPOAiW0nwVEAIQv9oToEMRAXHk+WDzGuyaSTh8CI4A=="
IMA_CLIENT_ID = "673604a6665155cd973af671ab115321"
RAW_KB_ID = "2Oor28yUr2eXyEFPBL0bwQU0DsrUEWPW-u9RF9CIUTw="
WIKI_KB_ID = "TcygOiKth0s91W35XJOu4NTAatl-57Bi2g19Wl3jvFw="

# IMA API Endpoints
IMA_BASE_URL = "https://ima.qq.com/openapi"
ENDPOINTS = {
    "create_note": f"{IMA_BASE_URL}/note/v1/import_doc",
    "search_note": f"{IMA_BASE_URL}/note/v1/search_note",
    "append_doc": f"{IMA_BASE_URL}/note/v1/append_doc",
    "get_knowledge_list": f"{IMA_BASE_URL}/wiki/v1/get_knowledge_list",
    "add_knowledge": f"{IMA_BASE_URL}/wiki/v1/add_knowledge",
    "get_doc_content": f"{IMA_BASE_URL}/note/v1/get_doc_content",
    "get_media_info": f"{IMA_BASE_URL}/wiki/v1/get_media_info",  # Guess!
}

# Themes (as specified by user)
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


def ima_request(endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Make a request to IMA API"""
    headers = {
        "Content-Type": "application/json",
        "ima-openapi-clientid": IMA_CLIENT_ID,
        "ima-openapi-apikey": IMA_API_KEY
    }
    response = requests.post(endpoint, headers=headers, json=data)
    response.raise_for_status()
    return response.json()


def fetch_knowledge_list(kb_id: str, parent_id: str = "", processed_folders: set = None, seen_media_ids: set = None) -> List[Dict[str, Any]]:
    """Fetch all knowledge items from a KB (with pagination, recursive subfolders, and deduplication)"""
    if processed_folders is None:
        processed_folders = set()
    if seen_media_ids is None:
        seen_media_ids = set()
    
    all_items = []
    cursor = ""
    is_end = False

    while not is_end:
        data = {
            "knowledge_base_id": kb_id,
            "cursor": cursor,
            "limit": 50
        }
        if parent_id:
            data["parent_id"] = parent_id
            
        result = ima_request(
            ENDPOINTS["get_knowledge_list"],
            data
        )
        data_obj = result.get("data", {})
        if "knowledge_list" in data_obj:
            for item in data_obj["knowledge_list"]:
                # If it's a folder, recursively fetch its contents (avoid cycles)
                if item.get("media_type") == 99:  # From debug output: folders have media_type=99
                    folder_id = item.get("media_id")
                    if folder_id and folder_id not in processed_folders:
                        processed_folders.add(folder_id)
                        sub_items = fetch_knowledge_list(kb_id, folder_id, processed_folders, seen_media_ids)
                        all_items.extend(sub_items)
                else:
                    # Add non-folder items to the list only if not already seen
                    media_id = item.get("media_id")
                    if media_id and media_id not in seen_media_ids:
                        seen_media_ids.add(media_id)
                        all_items.append(item)
        cursor = data_obj.get("next_cursor", "")
        is_end = data_obj.get("is_end", True)

    return all_items


def search_note(title: str) -> Dict[str, Any]:
    """Search for a note by title using IMA API"""
    return ima_request(
        ENDPOINTS["search_note"],
        {
            "search_type": 0,
            "query_info": {"title": title},
            "start": 0,
            "end": 20
        }
    )


def get_doc_content(doc_id: str) -> Dict[str, Any]:
    """Get note content by doc_id"""
    return ima_request(
        ENDPOINTS["get_doc_content"],
        {"doc_id": doc_id}
    )

def get_media_info(media_id: str, kb_id: str) -> Dict[str, Any]:
    """Get media info from knowledge base"""
    return ima_request(
        ENDPOINTS["get_media_info"],
        {"media_id": media_id, "knowledge_base_id": kb_id}
    )

def get_raw_item_content(item: Dict[str, Any], kb_id: str) -> str:
    """Get content for a raw knowledge base item"""
    media_type = item["media_type"]
    media_id = item["media_id"]
    
    if media_type == 11:  # Note
        # media_id is like "note_xxx_docid"
        doc_id = media_id.split("_")[-1]
        content_resp = get_doc_content(doc_id)
        return content_resp["data"]["content"]
    elif media_type == 6:  # WeChat article
        media_info = get_media_info(media_id, kb_id)
        url = media_info["data"]["url_info"]["url"]
        return f"URL: {url}"
    elif media_type == 7:  # Markdown
        # Markdown is probably also a note, let's try
        doc_id = media_id.split("_")[-1]
        try:
            content_resp = get_doc_content(doc_id)
            return content_resp["data"]["content"]
        except:
            return f"Unsupported media type: {media_type}"
    else:
        return f"Unsupported media type: {media_type}"


def get_wiki_current_items(kb_id: str) -> List[Dict[str, Any]]:
    """Get all current items in wiki KB"""
    return fetch_knowledge_list(kb_id)


def create_note(title: str, content: str) -> str:
    """Create a new note, return note_id"""
    resp = ima_request(
        ENDPOINTS["create_note"],
        {"content_format": 1, "content": content}
    )
    # Need to check what the response looks like
    print(f"Create note response: {json.dumps(resp, ensure_ascii=False, indent=2)}")
    # Assuming resp has data.note_id or similar
    # For now, let's search for the note by title to get the id
    search_resp = search_note(title)
    if "data" in search_resp and "note_list" in search_resp["data"]:
        for note in search_resp["data"]["note_list"]:
            if note["note_book_info"]["title"] == title:
                return note["note_book_info"]["note_id"]
    return ""


def append_to_note(note_id: str, content: str) -> None:
    """Append content to an existing note"""
    ima_request(
        ENDPOINTS["append_doc"],
        {"note_id": note_id, "content_format": 1, "content": content}
    )


def add_note_to_wiki(kb_id: str, note_id: str, title: str) -> None:
    """Add a note to wiki KB"""
    ima_request(
        ENDPOINTS["add_knowledge"],
        {
            "media_type": 11,
            "note_info": {"content_id": note_id},
            "title": title,
            "knowledge_base_id": kb_id
        }
    )


def main_process():
    print("Step 1: Raw items collected, step 3a: identify theme for new note 'Multi-Agent 不是银弹...' → [[AI Agent架构]]")

    # Step 2: Create summary for the new content
    new_note_title = "Multi-Agent 不是银弹：Agent 架构选型的工程判断"
    new_note_content = items_with_content[3]["content"]

    summary = f"> 这篇文章从工程角度分析了 Agent 架构选型，核心论点是多 Agent 不是默认升级路线，多数场景下单 Agent 是更好的 baseline。关键结论包括：\n> - 单 Agent 的优势是链路短、上下文完整、状态一致、调试简单\n> - 多 Agent 仅在上下文隔离、并行探索、专业化或独立验证场景下有价值\n> - 在固定推理 token 预算下，单 Agent 常能匹配甚至超过多 Agent 的多跳推理能力\n"

    # Step 3: Get today's date
    from datetime import datetime
    today_date = datetime.now().strftime("%Y-%m-%d")

    # Step 4: Prepare append content
    append_content = f"\n---\n更新于 {today_date}\n{summary}\n\n{new_note_content}"

    # Step 5: Use existing note_id we found (7459083279951877)
    existing_note_id = "7459083279951877"
    print(f"Appending to existing note: {existing_note_id}")
    append_to_note(existing_note_id, append_content)
    print("Successfully appended to existing note!")

    # Now let's also add a note about "Claude Code与Harness Engineering" theme: new note "Multi-Agent 不是银弹..." also mentions Claude Code!
    # Also, let's check other items: there are other new items like "全球排名前三，复旦自进化Harness Engineering让GPT‑5.4再涨7个点" → [[Claude Code与Harness Engineering]]
    print("Now processing other items...")


# def main():
#     print("Starting IMA raw → wiki incremental compilation...")
#     print("=" * 80)

#     # Step 1: Fetch raw KB content
#     print("Step 1: Fetching raw KB content...")
#     raw_items = fetch_knowledge_list(RAW_KB_ID)
#     print(f"  Fetched {len(raw_items)} items from raw KB")
    
#     # Save raw items to JSON file
#     with open("/workspace/raw_items.json", "w", encoding="utf-8") as f:
#         json.dump(raw_items, f, ensure_ascii=False, indent=2)
#     print("  Saved raw items to /workspace/raw_items.json")

#     # Step 5a: Get wiki current items
#     print("Step 5a: Fetching current wiki KB items...")
#     wiki_current_items = get_wiki_current_items(WIKI_KB_ID)
#     print(f"  Found {len(wiki_current_items)} items in wiki KB")
#     with open("/workspace/wiki_current_items.json", "w", encoding="utf-8") as f:
#         json.dump(wiki_current_items, f, ensure_ascii=False, indent=2)
#     print("  Saved wiki current items to /workspace/wiki_current_items.json")

#     # Get CLAUDE.md content
#     claude_content = ""
#     claude_item = None
#     for item in raw_items:
#         if "CLAUDE.md" in item.get("title", ""):
#             claude_item = item
#             claude_content = get_raw_item_content(item, RAW_KB_ID)
#             break
#     if claude_content:
#         with open("/workspace/CLAUDE.md", "w", encoding="utf-8") as f:
#             f.write(claude_content)
#         print("  Saved CLAUDE.md to /workspace/CLAUDE.md")

#     # Collect content for all items
#     items_with_content = []
#     for item in raw_items:
#         try:
#             content = get_raw_item_content(item, RAW_KB_ID)
#             items_with_content.append({
#                 "title": item["title"],
#                 "media_type": item["media_type"],
#                 "media_id": item["media_id"],
#                 "content": content
#             })
#         except Exception as e:
#             print(f"  Error getting content for {item['title']}: {e}")
#             items_with_content.append({
#                 "title": item["title"],
#                 "media_type": item["media_type"],
#                 "media_id": item["media_id"],
#                 "error": str(e)
#             })
    
#     with open("/workspace/items_with_content.json", "w", encoding="utf-8") as f:
#         json.dump(items_with_content, f, ensure_ascii=False, indent=2)
#     print("  Saved items with content to /workspace/items_with_content.json")


if __name__ == "__main__":
    # First load the items_with_content
    import json
    with open("/workspace/items_with_content.json", "r", encoding="utf-8") as f:
        items_with_content = json.load(f)
    
    main_process()
