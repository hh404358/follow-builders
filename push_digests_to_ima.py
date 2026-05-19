import requests
import json
from datetime import datetime

# IMA API配置
CLIENT_ID = "673604a6665155cd973af671ab115321"
API_KEY = "Y869muklEIrSezgzOdqLXdPZ/lOdmqDB3BY/s9DSIfu3+MmsALESLZe5ls2xLXRqfBFzw1OTqw=="
KNOWLEDGE_BASE_ID = "TcygOiKth0s91W35XJOu4NTAatl-57Bi2g19Wl3jvFw="

# API端点
IMPORT_DOC_URL = "https://ima.qq.com/openapi/note/v1/import_doc"
ADD_KNOWLEDGE_URL = "https://ima.qq.com/openapi/wiki/v1/add_knowledge"

# 请求头
headers = {
    "ima-openapi-clientid": CLIENT_ID,
    "ima-openapi-apikey": API_KEY,
    "Content-Type": "application/json"
}

def push_digest_to_ima(file_path, title):
    """推送单个摘要到IMA知识库"""
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"正在推送: {title}")
        
        # 第一步：导入文档
        import_payload = {
            "content_format": 1,
            "content": content
        }
        
        response = requests.post(IMPORT_DOC_URL, headers=headers, json=import_payload, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        if result.get('code') != 0:
            print(f"导入文档失败: {result.get('msg')}")
            return False
        
        note_id = result.get('data', {}).get('note_id')
        if not note_id:
            print("未能获取note_id")
            return False
        
        print(f"文档导入成功，note_id: {note_id}")
        
        # 第二步：添加到知识库
        add_payload = {
            "media_type": 11,
            "note_info": {"content_id": note_id},
            "title": title,
            "knowledge_base_id": KNOWLEDGE_BASE_ID
        }
        
        add_response = requests.post(ADD_KNOWLEDGE_URL, headers=headers, json=add_payload, timeout=60)
        add_response.raise_for_status()
        
        add_result = add_response.json()
        if add_result.get('code') != 0:
            print(f"添加到知识库失败: {add_result.get('msg')}")
            return False
        
        print(f"✓ {title} 成功推送到知识库！")
        return True
        
    except Exception as e:
        print(f"推送失败: {str(e)}")
        return False

def main():
    # 要推送的文件列表
    digests = [
        {
            "file_path": "/workspace/daily-digest-2026-05-15.md",
            "title": "AI Builders 每日摘要 - 2026年5月15日"
        },
        {
            "file_path": "/workspace/daily-digest-2026-05-16.md",
            "title": "AI Builders 每日摘要 - 2026年5月16日"
        },
        {
            "file_path": "/workspace/daily-digest-2026-05-17.md",
            "title": "AI Builders 每日摘要 - 2026年5月17日"
        },
        {
            "file_path": "/workspace/daily-digest-2026-05-18.md",
            "title": "AI Builders 每日摘要 - 2026年5月18日"
        },
        {
            "file_path": "/workspace/daily-digest-2026-05-19.md",
            "title": "AI Builders 每日摘要 - 2026年5月19日"
        }
    ]
    
    print("=" * 60)
    print("开始批量推送摘要到IMA知识库")
    print("=" * 60)
    
    success_count = 0
    for digest in digests:
        if push_digest_to_ima(digest["file_path"], digest["title"]):
            success_count += 1
        print("-" * 60)
    
    print(f"\n推送完成！成功: {success_count}/{len(digests)}")

if __name__ == "__main__":
    main()
