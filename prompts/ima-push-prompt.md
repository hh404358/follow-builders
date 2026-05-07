## IMA 推送提示词模板

当你需要将内容保存到 IMA 知识库时，直接使用以下命令格式：

### 推送到个人笔记

```bash
node /workspace/scripts/push-to-ima.js "标题" /path/to/content.md
```

### 推送到 wiki 知识库

```bash
node /workspace/scripts/push-to-ima.js "标题" /path/to/content.md wiki
```

### Python 版本（可选）

如果 Node.js 不可用，使用 Python：

```python
import requests
import json
import os

CONFIG_DIR = os.path.expanduser('~/.config/ima')
WIKI_KB_ID = 'TcygOiKth0s91W35XJOu4NTAatl-57Bi2g19Wl3jvFw='

def push_to_ima(title: str, content: str, kb_type: str = 'note') -> dict:
    """
    推送内容到 IMA
    
    Args:
        title: 笔记标题
        content: Markdown 内容
        kb_type: 'note' (个人笔记) 或 'wiki' (wiki 知识库)
    
    Returns:
        {'note_id': str, 'wiki_added': bool}
    """
    client_id = open(f'{CONFIG_DIR}/client_id').read().strip()
    api_key = open(f'{CONFIG_DIR}/api_key').read().strip()
    
    headers = {
        'ima-openapi-clientid': client_id,
        'ima-openapi-apikey': api_key,
        'Content-Type': 'application/json',
    }
    
    # 1. 创建笔记
    resp = requests.post(
        'https://ima.qq.com/openapi/note/v1/import_doc',
        headers=headers,
        json={'content_format': 1, 'content': content}
    )
    data = resp.json()
    
    if data['code'] != 0:
        raise Exception(f"IMA Error: {data['msg']}")
    
    note_id = data['data']['note_id']
    
    # 2. 如果是 wiki，添加到 wiki 知识库
    wiki_added = False
    if kb_type == 'wiki':
        wiki_resp = requests.post(
            'https://ima.qq.com/openapi/wiki/v1/add_knowledge',
            headers=headers,
            json={
                'media_type': 11,
                'note_info': {'content_id': note_id},
                'title': title,
                'knowledge_base_id': WIKI_KB_ID
            }
        )
        wiki_data = wiki_resp.json()
        if wiki_data['code'] == 0:
            wiki_added = True
    
    return {'note_id': note_id, 'wiki_added': wiki_added}


# 使用示例
result = push_to_ima("测试笔记", "# 测试\\n\\n这是测试内容", "wiki")
print(f"笔记ID: {result['note_id']}, 已添加wiki: {result['wiki_added']}")
```

### 快速调用命令

```bash
# 推送到个人笔记
node /workspace/scripts/push-to-ima.js "AI Builders 每日摘要" /workspace/daily-digest-2026-05-06.md

# 推送到 wiki 知识库
node /workspace/scripts/push-to-ima.js "Claude Code 架构分析" /workspace/wiki/Claude-Code-与-Harness-Engineering.md wiki
```
