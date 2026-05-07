# IMA 推送 - AI 直接调用指南

## 当你说"推送到 IMA"时，AI 应该这样执行：

### 方式 1: 使用封装脚本（推荐）

```bash
# 推送到个人笔记
node /workspace/scripts/push-to-ima.js "<标题>" "<内容文件路径>"

# 推送到 wiki 知识库
node /workspace/scripts/push-to-ima.js "<标题>" "<内容文件路径>" wiki
```

### 方式 2: 直接调用 IMA API

如果脚本不可用，AI 应该使用以下 Node.js 代码：

```javascript
const fetch = require('node:fetch');
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');

const WIKI_KB_ID = 'TcygOiKth0s91W35XJOu4NTAatl-57Bi2g19Wl3jvFw=';

async function pushToIMA(title, content, kbType = 'note') {
  // 加载凭证
  const configDir = path.join(os.homedir(), '.config/ima');
  const clientId = fs.readFileSync(path.join(configDir, 'client_id'), 'utf8').trim();
  const apiKey = fs.readFileSync(path.join(configDir, 'api_key'), 'utf8').trim();
  
  const headers = {
    'ima-openapi-clientid': clientId,
    'ima-openapi-apikey': apiKey,
    'Content-Type': 'application/json',
  };
  
  // 1. 创建笔记
  const resp = await fetch('https://ima.qq.com/openapi/note/v1/import_doc', {
    method: 'POST',
    headers,
    body: JSON.stringify({ content_format: 1, content })
  });
  const data = await resp.json();
  
  if (data.code !== 0) throw new Error(data.msg);
  const noteId = data.data.note_id;
  
  // 2. 如果是 wiki，添加到 wiki 知识库
  if (kbType === 'wiki') {
    await fetch('https://ima.qq.com/openapi/wiki/v1/add_knowledge', {
      method: 'POST',
      headers,
      body: JSON.stringify({
        media_type: 11,
        note_info: { content_id: noteId },
        title,
        knowledge_base_id: WIKI_KB_ID
      })
    });
  }
  
  return { noteId, wikiAdded: kbType === 'wiki' };
}

// AI 调用示例
const result = await pushToIMA(
  '我的笔记标题',
  fs.readFileSync('/path/to/content.md', 'utf8'),
  'wiki'  // 或 'note'
);
console.log('推送成功:', result);
```

## AI 指令模板

当你需要 AI 执行推送时，直接说：

> "把刚才的总结推送到 IMA wiki"

> "将这份报告添加到 IMA 笔记"

> "保存到 IMA wiki 知识库"

AI 收到这类指令后，应该：
1. 获取当前对话中的内容（如摘要、报告等）
2. 确定是推送到 `note` 还是 `wiki`
3. 使用上述代码执行推送
4. 报告推送结果

## 凭证说明

IMA 凭证已配置在：
- `~/.config/ima/client_id`
- `~/.config/ima/api_key`

AI 无需询问，可以直接使用。
