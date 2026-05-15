#!/usr/bin/env python3
import requests
import json

# 配置信息
CLIENT_ID = "673604a6665155cd973af671ab115321"
API_KEY = "Y869muklEIrSezgzOdqLXdPZ/lOdmqDB3BY/s9DSIfu3+MmsALESlZe5ls2xLXRqfBFzw1OTqw=="
KB_ID = "TcygOiKth0s91W35XJOu4NTAatl-57Bi2g19Wl3jvFw=="

# 读取 Markdown 内容
with open("/workspace/daily-digest-2026-05-15.md", "r", encoding="utf-8") as f:
    markdown_content = f.read()

# 设置请求头
headers = {
    "ima-openapi-clientid": CLIENT_ID,
    "ima-openapi-apikey": API_KEY,
    "Content-Type": "application/json"
}

print("=" * 60)
print("AI Builders 每日摘要推送脚本")
print("=" * 60)

# 第一步：导入文档
print("\n[1/2] 正在导入文档到 IMA 笔记...")
import_url = "https://ima.qq.com/openapi/note/v1/import_doc"
import_data = {
    "content_format": 1,
    "content": markdown_content
}

try:
    import_response = requests.post(import_url, headers=headers, json=import_data, timeout=30)
    print(f"导入请求状态码: {import_response.status_code}")
    print(f"导入响应: {import_response.text}")
    
    if import_response.status_code == 200:
        result = import_response.json()
        if result.get("code") == 0 and "data" in result:
            note_id = result["data"].get("content_id")
            if note_id:
                print(f"✅ 文档导入成功！content_id: {note_id}")
                
                # 第二步：添加到知识库
                print("\n[2/2] 正在添加到知识库...")
                wiki_url = "https://ima.qq.com/openapi/wiki/v1/add_knowledge"
                wiki_data = {
                    "media_type": 11,
                    "note_info": {"content_id": note_id},
                    "title": "AI Builders 每日摘要 - 2026年5月15日",
                    "knowledge_base_id": KB_ID
                }
                
                wiki_response = requests.post(wiki_url, headers=headers, json=wiki_data, timeout=30)
                print(f"知识库请求状态码: {wiki_response.status_code}")
                print(f"知识库响应: {wiki_response.text}")
                
                if wiki_response.status_code == 200:
                    wiki_result = wiki_response.json()
                    if wiki_result.get("code") == 0:
                        print("✅ 成功添加到知识库！")
                    else:
                        print(f"⚠️ 知识库添加返回非零 code: {wiki_result.get('code')}")
                else:
                    print(f"⚠️ 知识库添加请求失败: {wiki_response.status_code}")
            else:
                print("⚠️ 导入成功但未获取到 content_id")
        else:
            print(f"⚠️ 导入失败: {result.get('message', '未知错误')}")
    else:
        print(f"⚠️ 导入请求失败: {import_response.status_code}")
        
except Exception as e:
    print(f"❌ 推送过程中出错: {str(e)}")

print("\n" + "=" * 60)
print("推送完成！")
print("=" * 60)
print("\n📄 摘要已保存到: /workspace/daily-digest-2026-05-15.md")
