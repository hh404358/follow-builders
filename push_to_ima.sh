#!/bin/bash

# 读取 Markdown 内容
MARKDOWN_CONTENT=$(cat daily-digest-2026-05-15.md)

# 第一步：导入文档到 IMA 笔记
echo "正在导入文档到 IMA 笔记..."
IMPORT_RESPONSE=$(curl -s -X POST "https://ima.qq.com/openapi/note/v1/import_doc" \
  -H "ima-openapi-clientid: 673604a6665155cd973af671ab115321" \
  -H "ima-openapi-apikey: Y869muklEIrSezgzOdqLXdPZ/lOdmqDB3BY/s9DSIfu3+MmsALESlZe5ls2xLXRqfBFzw1OTqw==" \
  -H "Content-Type: application/json" \
  -d "{\"content_format\": 1, \"content\": $(printf '%s' "$MARKDOWN_CONTENT" | jq -R -s '.')}")

echo "导入响应: $IMPORT_RESPONSE"

# 尝试提取 content_id
NOTE_ID=$(echo "$IMPORT_RESPONSE" | jq -r '.data.content_id // empty')

if [ -n "$NOTE_ID" ]; then
  echo "文档导入成功！content_id: $NOTE_ID"
  
  # 第二步：添加到知识库
  echo "正在添加到知识库..."
  WIKI_RESPONSE=$(curl -s -X POST "https://ima.qq.com/openapi/wiki/v1/add_knowledge" \
    -H "ima-openapi-clientid: 673604a6665155cd973af671ab115321" \
    -H "ima-openapi-apikey: Y869muklEIrSezgzOdqLXdPZ/lOdmqDB3BY/s9DSIfu3+MmsALESlZe5ls2xLXRqfBFzw1OTqw==" \
    -H "Content-Type: application/json" \
    -d "{\"media_type\": 11, \"note_info\": {\"content_id\": \"$NOTE_ID\"}, \"title\": \"AI Builders 每日摘要 - 2026年5月15日\", \"knowledge_base_id\": \"TcygOiKth0s91W35XJOu4NTAatl-57Bi2g19Wl3jvFw==\"}")
  
  echo "知识库添加响应: $WIKI_RESPONSE"
else
  echo "文档导入失败或未返回 content_id"
fi
