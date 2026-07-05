import axios from 'axios';
import * as fs from 'fs';
import * as path from 'path';

const IMA_API_KEY = 'rSAWpVuJjTYWqwZSXrNWoHZSl+pvxL+tfPOAiW0nwVEAIQv9oToEMRAXHk+WDzGuyaSTh8CI4A==';
const IMA_CLIENT_ID = '673604a6665155cd973af671ab115321';
const RAW_KB_ID = '2Oor28yUr2eXyEFPBL0bwQU0DsrUEWPW-u9RF9CIUTw=';
const WIKI_KB_ID = 'TcygOiKth0s91W35XJOu4NTAatl-57Bi2g19Wl3jvFw=';

const BASE_URL = 'https://ima.qq.com/openapi';
const HEADERS = {
  'ima-openapi-clientid': IMA_CLIENT_ID,
  'ima-openapi-apikey': IMA_API_KEY,
  'Content-Type': 'application/json'
};

const TOPICS = [
  'Claude Code与Harness Engineering',
  'AI Agent架构',
  'DeepSeek技术',
  'Prompt Engineering与AI工作流',
  'Embedding模型选型',
  'AI科研自动化',
  '个人效能与方法论',
  '知识库构建'
];

const TOPIC_KEYWORDS = {
  'Claude Code与Harness Engineering': ['claude', 'code', 'harness', 'engineering', 'ide', 'trae', 'cursor'],
  'AI Agent架构': ['agent', 'agentic', 'architecture', 'workflow', 'autonomous', 'multi-agent'],
  'DeepSeek技术': ['deepseek', 'moonshot', 'model', 'llm', 'inference'],
  'Prompt Engineering与AI工作流': ['prompt', 'engineering', 'workflow', 'chain', 'rag', 'fine-tune'],
  'Embedding模型选型': ['embedding', 'vector', 'model', 'similarity', 'retrieval'],
  'AI科研自动化': ['research', 'paper', 'arxiv', 'scientific', 'automation'],
  '个人效能与方法论': ['productivity', 'efficiency', 'methodology', 'workflow', 'system'],
  '知识库构建': ['knowledge', 'base', 'kb', 'wiki', 'notes', 'organize']
};

async function request(method, url, data = {}) {
  try {
    const response = await axios({
      method,
      url: `${BASE_URL}${url}`,
      headers: HEADERS,
      data: JSON.stringify(data),
      proxy: false
    });
    return response.data;
  } catch (error) {
    console.error(`API请求失败 ${url}:`, error.response?.data || error.message);
    throw error;
  }
}

async function getWikiKnowledgeList(kbId) {
  const allItems = [];
  let cursor = '';
  let isEnd = false;

  while (!isEnd) {
    const result = await request('POST', '/wiki/v1/get_knowledge_list', {
      knowledge_base_id: kbId,
      cursor,
      limit: 50
    });

    if (result.data?.knowledge_list) {
      allItems.push(...result.data.knowledge_list);
    }
    isEnd = result.data?.is_end || false;
    cursor = result.data?.cursor || '';
  }

  return allItems;
}

async function getNoteContent(noteId) {
  const result = await request('POST', '/note/v1/search_note', {
    search_type: 0,
    query_info: { title: '' },
    start: 0,
    end: 1
  });
  return null;
}

async function fetchUrlContent(url) {
  try {
    const response = await axios.get(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
      }
    });
    return response.data;
  } catch (error) {
    console.error(`URL抓取失败 ${url}:`, error.message);
    return null;
  }
}

function classifyTopic(title, content) {
  const text = `${title} ${content || ''}`.toLowerCase();
  for (const [topic, keywords] of Object.entries(TOPIC_KEYWORDS)) {
    if (keywords.some(kw => text.includes(kw.toLowerCase()))) {
      return topic;
    }
  }
  return '其他';
}

function generateSummary(content) {
  if (!content || content.length < 50) return '';
  const sentences = content.replace(/[\r\n]+/g, ' ').split(/[。！？.!?]/);
  const summary = sentences.slice(0, 3).filter(s => s.trim().length > 10).join('。') + '。';
  return summary.length > 200 ? summary.substring(0, 200) + '...' : summary;
}

function buildDoubleLinks(topics) {
  return topics.map(t => `[[${t}]]`).join(' ');
}

async function main() {
  console.log('=== IMA Raw → Wiki 增量编译流程 ===');
  console.log('日期:', new Date().toISOString().split('T')[0]);
  console.log('');

  console.log('步骤1: 获取raw知识库内容...');
  const rawItems = await getWikiKnowledgeList(RAW_KB_ID);
  console.log(`Raw条目总数: ${rawItems.length}`);

  const processedItems = [];
  for (const item of rawItems) {
    const title = item.title || '无标题';
    let content = item.content || '';

    if (item.url && (item.url.includes('mp.weixin.qq.com') || item.url.includes('weixin'))) {
      console.log(`  抓取微信文章: ${title}`);
      const fetched = await fetchUrlContent(item.url);
      if (fetched) {
        content = fetched.substring(0, 5000);
      }
    }

    processedItems.push({ title, content, url: item.url });
  }

  console.log(`\n步骤2-4: 分析内容、识别主题、编译wiki文件...`);
  
  const topicContents = {};
  TOPICS.forEach(t => topicContents[t] = []);
  topicContents['其他'] = [];

  for (const item of processedItems) {
    const topic = classifyTopic(item.title, item.content);
    topicContents[topic].push(item);
  }

  const wikiFiles = [];
  for (const [topic, items] of Object.entries(topicContents)) {
    if (items.length === 0) continue;
    
    let mdContent = `# ${topic}\n\n`;
    
    for (const item of items) {
      const summary = generateSummary(item.content);
      mdContent += `## ${item.title}\n\n`;
      if (summary) {
        mdContent += `> ${summary}\n\n`;
      }
      if (item.url) {
        mdContent += `[原文链接](${item.url})\n\n`;
      }
    }

    const relatedTopics = TOPICS.filter(t => t !== topic && t !== '其他');
    if (relatedTopics.length > 0) {
      mdContent += `\n---\n\n## 相关主题\n\n${buildDoubleLinks(relatedTopics)}`;
    }

    wikiFiles.push({ title: topic, content: mdContent });
    console.log(`  生成主题: ${topic} (${items.length}条)`);
  }

  console.log(`\n步骤5: 智能更新策略...`);
  
  console.log('  获取wiki当前列表...');
  const wikiList = await getWikiKnowledgeList(WIKI_KB_ID);
  const existingTitles = new Set(wikiList.map(item => item.title));
  console.log(`  Wiki当前条目数: ${existingTitles.size}`);

  let addedCount = 0;
  let updatedCount = 0;
  const failedItems = [];

  for (const file of wikiFiles) {
    try {
      if (existingTitles.has(file.title)) {
        console.log(`  已存在: ${file.title} → 追加更新`);
        
        const searchResult = await request('POST', '/note/v1/search_note', {
          search_type: 0,
          query_info: { title: file.title },
          start: 0,
          end: 1
        });

        const noteId = searchResult.data?.note_list?.[0]?.note_id;
        if (noteId) {
          const today = new Date().toISOString().split('T')[0];
          const appendContent = `\n---\n更新于 ${today}\n\n${file.content}`;
          
          await request('POST', '/note/v1/append_doc', {
            note_id: noteId,
            content_format: 1,
            content: appendContent
          });
          updatedCount++;
        } else {
          throw new Error('未找到对应笔记ID');
        }
      } else {
        console.log(`  不存在: ${file.title} → 新增`);
        
        const createResult = await request('POST', '/note/v1/import_doc', {
          content_format: 1,
          content: file.content
        });

        const noteId = createResult.data?.note_id;
        if (noteId) {
          await request('POST', '/wiki/v1/add_knowledge', {
            media_type: 11,
            note_info: { content_id: noteId },
            title: file.title,
            knowledge_base_id: WIKI_KB_ID
          });
          addedCount++;
        } else {
          throw new Error('创建笔记失败');
        }
      }
    } catch (error) {
      console.error(`  失败: ${file.title} - ${error.message}`);
      failedItems.push({ title: file.title, error: error.message });
    }
  }

  console.log(`\n步骤6: 生成报告...`);
  console.log('====================================');
  console.log('         编译报告');
  console.log('====================================');
  console.log(`Raw条目数: ${rawItems.length}`);
  console.log(`新增: ${addedCount}个`);
  console.log(`追加更新: ${updatedCount}个`);
  
  if (failedItems.length > 0) {
    console.log(`\n失败详情:`);
    failedItems.forEach(item => {
      console.log(`  - ${item.title}: ${item.error}`);
    });
  }
  
  console.log('====================================');
}

main().catch(console.error);
