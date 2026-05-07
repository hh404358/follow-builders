#!/usr/bin/env node
/**
 * push-to-ima.js - 推送内容到 IMA 知识库
 * 用法: node push-to-ima.js <title> <content_file> [kb_type]
 * 
 * kb_type: 'note' (默认) | 'wiki'
 * 
 * 示例:
 *   node push-to-ima.js "我的笔记" /workspace/notes/test.md
 *   node push-to-ima.js "维基文章" /workspace/wiki/article.md wiki
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

const SCRIPT_DIR = path.join(os.homedir(), '.openclaw/workspace/skills/ima-skills');
const CONFIG_DIR = path.join(os.homedir(), '.config/ima');

const WIKI_KB_ID = 'TcygOiKth0s91W35XJOu4NTAatl-57Bi2g19Wl3jvFw=';

function loadCredentials() {
  const clientId = fs.readFileSync(path.join(CONFIG_DIR, 'client_id'), 'utf8').trim();
  const apiKey = fs.readFileSync(path.join(CONFIG_DIR, 'api_key'), 'utf8').trim();
  return { clientId, apiKey };
}

async function pushToIMA(title, content, kbType = 'note') {
  const { clientId, apiKey } = loadCredentials();
  
  const body = {
    content_format: 1,
    content: content
  };
  
  const res = await fetch('https://ima.qq.com/openapi/note/v1/import_doc', {
    method: 'POST',
    headers: {
      'ima-openapi-clientid': clientId,
      'ima-openapi-apikey': apiKey,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });
  
  const text = await res.text();
  const data = JSON.parse(text);
  
  if (data.code !== 0) {
    throw new Error(`IMA API Error: ${data.msg}`);
  }
  
  const noteId = data.data.note_id;
  
  if (kbType === 'wiki') {
    const addRes = await fetch('https://ima.qq.com/openapi/wiki/v1/add_knowledge', {
      method: 'POST',
      headers: {
        'ima-openapi-clientid': clientId,
        'ima-openapi-apikey': apiKey,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        media_type: 11,
        note_info: { content_id: noteId },
        title: title,
        knowledge_base_id: WIKI_KB_ID
      }),
    });
    
    const addText = await addRes.text();
    const addData = JSON.parse(addText);
    
    if (addData.code !== 0) {
      throw new Error(`Add to wiki failed: ${addData.msg}`);
    }
    
    return { noteId, wikiAdded: true };
  }
  
  return { noteId, wikiAdded: false };
}

async function main() {
  const args = process.argv.slice(2);
  
  if (args.length < 2) {
    console.log('用法: node push-to-ima.js <title> <content_file> [kb_type]');
    console.log('  kb_type: note (默认) | wiki');
    console.log('');
    console.log('示例:');
    console.log('  node push-to-ima.js "我的笔记" /workspace/notes/test.md');
    console.log('  node push-to-ima.js "维基文章" /workspace/wiki/article.md wiki');
    process.exit(1);
  }
  
  const title = args[0];
  const contentFile = args[1];
  const kbType = args[2] || 'note';
  
  if (!fs.existsSync(contentFile)) {
    console.error(`错误: 文件不存在 - ${contentFile}`);
    process.exit(1);
  }
  
  const content = fs.readFileSync(contentFile, 'utf8');
  
  try {
    console.log(`正在推送 "${title}" 到 IMA...`);
    const result = await pushToIMA(title, content, kbType);
    console.log(`✓ 成功!`);
    console.log(`  笔记 ID: ${result.noteId}`);
    if (result.wikiAdded) {
      console.log(`  已添加到 wiki 知识库`);
    }
  } catch (err) {
    console.error(`✗ 失败: ${err.message}`);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { pushToIMA };
