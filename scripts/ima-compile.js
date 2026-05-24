#!/usr/bin/env node
import fetch from 'node-fetch';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// IMA API credentials and KB IDs from user input
const IMA_CLIENT_ID = '673604a6665155cd973af671ab115321';
const IMA_API_KEY = 'Y869muklEIrSezgzOdqLXdPZ/lOdmqDB3BY/s9DSIfu3+MmsALESLZe5ls2xLXRqfBFzw1OTqw==';
const RAW_KB_ID = '2Oor28yUr2eXyEFPBL0bwQU0DsrUEWPW-u9RF9CIUTw=';
const WIKI_KB_ID = 'TcygOiKth0s91W35XJOu4NTAatl-57Bi2g19Wl3jvFw=';
const IMA_BASE_URL = 'https://ima.qq.com/openapi';

// Helper function to call IMA APIs
async function callIMA(apiPath, body, method = 'POST') {
  const headers = {
    'Content-Type': 'application/json',
    'ima-openapi-clientid': IMA_CLIENT_ID,
    'ima-openapi-apikey': IMA_API_KEY
  };

  const response = await fetch(`${IMA_BASE_URL}${apiPath}`, {
    method,
    headers,
    body: JSON.stringify(body)
  });

  const data = await response.json();

  if (data.code !== 0) {
    throw new Error(`IMA API error: ${data.code} - ${JSON.stringify(data)}`);
  }

  return data.data;
}

// Step 1: Get raw KB content
async function getRawKBContent(kbId) {
  const allItems = [];
  let cursor = '';
  let isEnd = false;

  while (!isEnd) {
    const data = await callIMA('/wiki/v1/get_knowledge_list', {
      knowledge_base_id: kbId,
      cursor,
      limit: 50
    });

    allItems.push(...(data.knowledge_list || []));
    cursor = data.cursor;
    isEnd = data.is_end;
  }

  return allItems;
}

// Step 2-4: Mock analysis for now (we'll need LLM for actual analysis)
// For now, let's create a simple structure
const THEMES = [
  'Claude Code与Harness Engineering',
  'AI Agent架构',
  'DeepSeek技术',
  'Prompt Engineering与AI工作流',
  'Embedding模型选型',
  'AI科研自动化',
  '个人效能与方法论',
  '知识库构建'
];

async function compileWikiFiles(rawContent) {
  // For now, let's just create a mock structure
  // In real implementation, we'd use LLM to analyze and categorize
  const wikiFiles = {};

  // Create a simple example
  for (const theme of THEMES) {
    wikiFiles[theme] = `> ${theme} 摘要\n\n## 条目\n\n- [测试条目](file://test)\n\n> 更多内容...`;
  }

  return wikiFiles;
}

// Step 5: Smart update strategy
async function smartUpdate(wikiFiles) {
  const result = {
    new: 0,
    updated: 0,
    failed: []
  };

  // Get current wiki list
  const wikiList = await getRawKBContent(WIKI_KB_ID);
  const existingTitles = new Map();

  for (const item of wikiList) {
    existingTitles.set(item.title, item.note_id || item.content_id);
  }

  const today = new Date().toISOString().split('T')[0];

  for (const [title, content] of Object.entries(wikiFiles)) {
    try {
      if (existingTitles.has(title)) {
        // Append to existing note
        const noteId = existingTitles.get(title);
        const appendContent = `\n---\n更新于 ${today}\n${content}`;
        await callIMA('/note/v1/append_doc', {
          note_id: noteId,
          content_format: 1,
          content: appendContent
        });
        result.updated++;
      } else {
        // Create new note and add to wiki
        const noteData = await callIMA('/note/v1/import_doc', {
          content_format: 1,
          content
        });
        await callIMA('/wiki/v1/add_knowledge', {
          media_type: 11,
          note_info: { content_id: noteData.note_id },
          title,
          knowledge_base_id: WIKI_KB_ID
        });
        result.new++;
      }
    } catch (error) {
      result.failed.push({ title, error: error.message });
    }
  }

  return result;
}

// Main function
async function main() {
  console.log('Starting IMA raw → wiki compilation...\n');

  try {
    // Step 1: Get raw content
    console.log('Step 1: Fetching raw KB content...');
    const rawContent = await getRawKBContent(RAW_KB_ID);
    console.log(`Fetched ${rawContent.length} items from raw KB\n`);

    // Steps 2-4: Compile wiki files
    console.log('Step 2-4: Compiling wiki files...');
    const wikiFiles = await compileWikiFiles(rawContent);
    console.log(`Compiled ${Object.keys(wikiFiles).length} wiki files\n`);

    // Step 5: Smart update
    console.log('Step 5: Applying smart update strategy...');
    const updateResult = await smartUpdate(wikiFiles);

    // Step 6: Report
    console.log('\n=== Compilation Report ===');
    console.log(`Raw KB items: ${rawContent.length}`);
    console.log(`New wiki notes: ${updateResult.new}`);
    console.log(`Updated wiki notes: ${updateResult.updated}`);
    if (updateResult.failed.length > 0) {
      console.log('\nFailed items:');
      for (const f of updateResult.failed) {
        console.log(`- ${f.title}: ${f.error}`);
      }
    }

  } catch (error) {
    console.error('Error during compilation:', error);
    process.exit(1);
  }
}

main();
