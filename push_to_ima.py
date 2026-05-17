
import requests
import json

# IMA API 配置
IMA_CLIENT_ID = "673604a6665155cd973af671ab115321"
IMA_API_KEY = "Y869muklEIrSezgzOdqLXdPZ/lOdmqDB3BY/s9DSIfu3+MmsALESLZe5ls2xLXRqfBFzw1OTqw=="
KB_ID = "TcygOiKth0s91W35XJOu4NTAatl-57Bi2g19Wl3jvFw=="

# 读取摘要文件
with open("/workspace/daily-digest-2026-05-17.md", "r", encoding="utf-8") as f:
    digest_content = f.read()

# 步骤1：导入笔记到 IMA
import_url = "https://ima.qq.com/openapi/note/v1/import_doc"
headers = {
    "ima-openapi-clientid": IMA_CLIENT_ID,
    "ima-openapi-apikey": IMA_API_KEY,
    "Content-Type": "application/json"
}

import_payload = {
    "content_format": 1,
    "content": digest_content
}

print("正在将摘要导入 IMA 笔记...")
response = requests.post(import_url, headers=headers, json=import_payload)

if response.status_code == 200:
    result = response.json()
    note_id = result.get("data", {}).get("note_id")
    print(f"✅ 笔记导入成功！Note ID: {note_id}")
    
    # 步骤2：添加到知识库
    add_kb_url = "https://ima.qq.com/openapi/wiki/v1/add_knowledge"
    add_payload = {
        "media_type": 11,
        "note_info": {
            "content_id": note_id
        },
        "title": "AI Builders 每日摘要 - 2026年5月17日",
        "knowledge_base_id": KB_ID
    }
    
    print("正在添加到知识库...")
    kb_response = requests.post(add_kb_url, headers=headers, json=add_payload)
    
    if kb_response.status_code == 200:
        print("✅ 成功添加到知识库！")
    else:
        print(f"⚠️ 添加到知识库失败: {kb_response.status_code}")
        print(f"响应: {kb_response.text}")
else:
    print(f"❌ 笔记导入失败: {response.status_code}")
    print(f"响应: {response.text}")

print("\n执行完成！")

