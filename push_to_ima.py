import requests
import json
from datetime import datetime

# 读取Markdown文件
with open('daily-digest-2026-05-20.md', 'r', encoding='utf-8') as f:
    content = f.read()

# IMA API配置
client_id = "673604a6665155cd973af671ab115321"
api_key = "Y869muklEIrSezgzOdqLXdPZ/lOdmqDB3BY/s9DSIfu+MmsALESlZe5ls2xLXRqfBFzw1OTqw=="
knowledge_base_id = "TcygOiKth0s91W35XJOu4NTAatl-57Bi2g19Wl3jvFw=="

headers = {
    "ima-openapi-clientid": client_id,
    "ima-openapi-apikey": api_key,
    "Content-Type": "application/json"
}

# 第一步：导入文档
import_url = "https://ima.qq.com/openapi/note/v1/import_doc"
import_payload = {
    "content_format": 1,
    "content": content
}

print("正在推送文档至IMA...")
import_response = requests.post(import_url, headers=headers, json=import_payload, timeout=60)
print(f"导入响应状态码: {import_response.status_code}")

if import_response.status_code == 200:
    import_result = import_response.json()
    print(f"导入响应: {json.dumps(import_result, ensure_ascii=False, indent=2)}")
    
    # 获取note_id
    note_id = import_result.get("data", {}).get("note_id") or import_result.get("note_id")
    
    if note_id:
        print(f"获得note_id: {note_id}")
        
        # 第二步：添加到知识库
        add_knowledge_url = "https://ima.qq.com/openapi/wiki/v1/add_knowledge"
        add_payload = {
            "media_type": 11,
            "note_info": {
                "content_id": note_id
            },
            "title": "AI Builders 每日摘要 - 2026年5月20日",
            "knowledge_base_id": knowledge_base_id
        }
        
        print("\n正在添加到知识库...")
        add_response = requests.post(add_knowledge_url, headers=headers, json=add_payload, timeout=60)
        print(f"添加知识库响应状态码: {add_response.status_code}")
        print(f"添加知识库响应: {json.dumps(add_response.json(), ensure_ascii=False, indent=2)}")
    else:
        print("未获取到note_id，无法添加到知识库")
else:
    print(f"导入失败，响应内容: {import_response.text}")
