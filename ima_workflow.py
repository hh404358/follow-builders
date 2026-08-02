#!/usr/bin/env python3
"""IMA raw → wiki 增量编译流程脚本"""
import json
import time
import subprocess
import sys
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from urllib.error import URLError, HTTPError

# ========== 配置 ==========
API_KEY = "rSAWpVuJjTYWqwZSXrNWoHZSl+pvxL+tfPOAiW0nwVEAIQv9oToEMRAXHk+WDzGuyaSTh8CI4A=="
CLIENT_ID = "673604a6665155cd973af671ab115321"
RAW_KB_ID = "2Oor28yUr2eXyEFPBL0bwQU0DsrUEWPW-u9RF9CIUTw="
WIKI_KB_ID = "TcygOiKth0s91W35XJOu4NTAatl-57Bi2g19Wl3jvFw="

BASE_URL = "https://ima.qq.com/openapi"
HEADERS = {
    "Content-Type": "application/json",
    "ima-openapi-clientid": CLIENT_ID,
    "ima-openapi-apikey": API_KEY,
}

def ima_api(path, body, retries=3):
    """调用IMA API"""
    url = BASE_URL + path
    data = json.dumps(body).encode("utf-8")
    for attempt in range(retries):
        try:
            req = Request(url, data=data, headers=HEADERS, method="POST")
            with urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                return result
        except (URLError, HTTPError) as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            print(f"API Error {path}: {e}", file=sys.stderr)
            raise

def web_fetch(url):
    """使用WebFetch获取网页内容（通过命令行curl模拟，失败则返回空）"""
    try:
        # 直接调用系统curl获取
        cmd = ["curl", "-sL", "--max-time", "30", "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36", url]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=35)
        if result.returncode == 0 and len(result.stdout) > 100:
            # 提取纯文本（简单HTML转文本）
            import re
            html = result.stdout
            # 移除script/style
            html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL|re.I)
            html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL|re.I)
            # 移除标签
            text = re.sub(r'<[^>]+>', ' ', html)
            # 清理空白
            text = re.sub(r'\s+', ' ', text).strip()
            return text[:10000]  # 限制长度
    except Exception as e:
        print(f"WebFetch error for {url}: {e}", file=sys.stderr)
    return ""

# ========== 步骤1: 获取raw知识库内容 ==========
def get_knowledge_list(kb_id):
    """获取知识库所有条目，自动翻页"""
    all_items = []
    cursor = ""
    page = 0
    while True:
        page += 1
        body = {
            "knowledge_base_id": kb_id,
            "cursor": cursor,
            "limit": 50,
        }
        resp = ima_api("/wiki/v1/get_knowledge_list", body)
        print(f"  Page {page}: status={resp.get('status')}, code={resp.get('code')}")
        data = resp.get("data", {}) or {}
        items = data.get("list", []) or []
        all_items.extend(items)
        print(f"    Got {len(items)} items, total so far: {len(all_items)}")
        # 检查is_end
        is_end = data.get("is_end", True)
        cursor = data.get("next_cursor", data.get("cursor", "")) or ""
        if is_end or not cursor or len(items) == 0:
            break
        time.sleep(0.3)
    return all_items

def is_wechat_article(item):
    """判断是否为微信文章"""
    title = (item.get("title") or "").lower()
    url = (item.get("url") or item.get("source_url") or "").lower()
    item_type = str(item.get("media_type") or item.get("type") or "")
    return "mp.weixin" in url or "微信" in title or "wechat" in title or item_type in ["3", "11"]

def extract_url(item):
    """从条目中提取URL"""
    return item.get("url") or item.get("source_url") or item.get("link") or ""

def extract_title(item):
    """从条目中提取标题"""
    return item.get("title") or item.get("name") or "未命名条目"

def extract_note_id(item):
    """提取note_id / content_id"""
    note_info = item.get("note_info") or {}
    return note_info.get("content_id") or note_info.get("note_id") or item.get("note_id") or item.get("content_id") or item.get("id") or ""

def load_raw_items():
    """加载并保存raw条目"""
    print("=" * 60)
    print("步骤1: 获取raw知识库内容")
    print("=" * 60)
    items = get_knowledge_list(RAW_KB_ID)
    print(f"\n共获取raw知识库条目: {len(items)} 个")
    
    # 保存原始列表
    with open("/workspace/raw_items.json", "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    
    # 分类
    with_url = [i for i in items if extract_url(i)]
    with_note = [i for i in items if extract_note_id(i)]
    print(f"  - 含URL条目: {len(with_url)}")
    print(f"  - 含note_id条目: {len(with_note)}")
    print(f"  - 微信文章类: {len([i for i in items if is_wechat_article(i)])}")
    
    # 打印前5条预览
    for i, item in enumerate(items[:5]):
        title = extract_title(item)
        url = extract_url(item)
        nid = extract_note_id(item)
        print(f"  [{i+1}] {title[:60]}")
        if url: print(f"       URL: {url[:100]}")
        if nid: print(f"       note_id: {nid}")
    
    return items

if __name__ == "__main__":
    load_raw_items()
