## IMA 推送 - 一句话让 AI 推送

在你的 AI 对话中，直接说这句话即可：

```
📤 推送到 IMA wiki
```

AI 会自动执行推送。

---

如果需要更精细控制：

```
📤 推送到 IMA
- 类型: [note / wiki]
- 标题: <标题>
```

---

### AI 需要知道的内部信息（无需告诉 AI，AI 应该自己知道）

```
IMA 凭证路径:
  ~/.config/ima/client_id
  ~/.config/ima/api_key

Wiki 知识库 ID:
  TcygOiKth0s91W35XJOu4NTAatl-57Bi2g19Wl3jvFw=

推送 API:
  POST https://ima.qq.com/openapi/note/v1/import_doc
  Headers: ima-openapi-clientid, ima-openapi-apikey
  Body: { content_format: 1, content: <markdown> }

Wiki 添加 API:
  POST https://ima.qq.com/openapi/wiki/v1/add_knowledge
  Body: { media_type: 11, note_info: { content_id: <note_id> }, title: <title>, knowledge_base_id: <wiki_kb_id> }
```
