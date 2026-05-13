import requests
import json

# Read the digest content
with open("daily-digest-2026-05-13.md", "r", encoding="utf-8") as f:
    digest_content = f.read()

# 1. Import the note to IMA
import_url = "https://ima.qq.com/openapi/note/v1/import_doc"
import_headers = {
    "ima-openapi-clientid": "673604a6665155cd973af671ab115321",
    "ima-openapi-apikey": "Y869muklEIrSezgzOdqLXdPZ/lOdmqDB3BY/s9DSIfu3+MmsALESZe5ls2xLXRqfBFzw1OTqw=="
}
import_payload = {
    "content_format": 1,
    "content": digest_content
}

print("Step 1: Importing note to IMA...")
response = requests.post(import_url, headers=import_headers, json=import_payload)
print(f"Import response status: {response.status_code}")
print(f"Import response: {response.text}")

if response.status_code == 200 and response.json().get("code") == 0:
    note_id = response.json().get("data", {}).get("note_id")
    print(f"Successfully imported note, note_id: {note_id}")
    
    # 2. Add the note to the wiki KB
    wiki_url = "https://ima.qq.com/openapi/wiki/v1/add_knowledge"
    wiki_payload = {
        "media_type": 11,
        "note_info": {
            "content_id": note_id
        },
        "title": "AI Builders 每日摘要 - 2026年5月13日",
        "knowledge_base_id": "TcygOiKth0s91W35XJOu4NTAatl-57Bi2g19Wl3jvFw=="
    }
    
    print("\nStep 2: Adding note to wiki KB...")
    wiki_response = requests.post(wiki_url, headers=import_headers, json=wiki_payload)
    print(f"Wiki response status: {wiki_response.status_code}")
    print(f"Wiki response: {wiki_response.text}")
else:
    print("Failed to import note to IMA")
