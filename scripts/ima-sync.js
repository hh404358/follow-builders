import axios from 'axios';

const API_KEY = 'rSAWpVuJjTYWqwZSXrNWoHZSl+pvxL+tfPOAiW0nwVEAIQv9oToEMRAXHk+WDzGuyaSTh8CI4A==';
const CLIENT_ID = '673604a6665155cd973af671ab115321';
const RAW_KB_ID = '2Oor28yUr2eXyEFPBL0bwQU0DsrUEWPW-u9RF9CIUTw=';
const WIKI_KB_ID = 'TcygOiKth0s91W35XJOu4NTAatl-57Bi2g19Wl3jvFw=';

const BASE_URL = 'https://ima.qq.com/openapi';

const HEADERS = {
  'ima-openapi-clientid': CLIENT_ID,
  'ima-openapi-apikey': API_KEY,
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

async function apiRequest(method, endpoint, data = {}) {
  const url = `${BASE_URL}${endpoint}`;
  try {
    const response = await axios({
      method,
      url,
      headers: HEADERS,
      data
    });
    return response.data;
  } catch (error) {
    console.error(`API请求失败 ${endpoint}:`, error.response?.data || error.message);
    throw error;
  }
}

async function getAllKnowledgeList(kbId) {
  const allItems = [];
  let cursor = '';
  let isEnd = false;

  while (!isEnd) {
    const response = await apiRequest('POST', '/wiki/v1/get_knowledge_list', {
      knowledge_base_id: kbId,
      cursor,
      limit: 50
    });

    if (response.data && response.data.list) {
      allItems.push(...response.data.list);
    }

    isEnd = response.data?.is_end === true;
    cursor = response.data?.next_cursor || '';

    console.log(`获取到 ${allItems.length} 条知识，is_end=${isEnd}`);
  }

  return allItems;
}

async function searchNote(title) {
  try {
    const response = await apiRequest('POST', '/note/v1/search_note', {
      search_type: 0,
      query_info: { title },
      start: 0,
      end: 20
    });
    return response.data?.list || [];
  } catch (error) {
    console.error(`搜索笔记失败 ${title}:`, error.message);
    return [];
  }
}

async function createNote(content) {
  const response = await apiRequest('POST', '/note/v1/import_doc', {
    content_format: 1,
    content
  });
  return response.data;
}

async function appendDoc(noteId, content) {
  const response = await apiRequest('POST', '/note/v1/append_doc', {
    note_id: noteId,
    content_format: 1,
    content
  });
  return response.data;
}

async function addWiki(noteId, title) {
  const response = await apiRequest('POST', '/wiki/v1/add_knowledge', {
    media_type: 11,
    note_info: { content_id: noteId },
    title,
    knowledge_base_id: WIKI_KB_ID
  });
  return response.data;
}

async function fetchUrlContent(url) {
  try {
    const response = await axios.get(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      }
    });
    return response.data;
  } catch (error) {
    console.error(`获取URL内容失败 ${url}:`, error.message);
    return null;
  }
}

function classifyTopic(content) {
  const topicKeywords = {
    'Claude Code与Harness Engineering': ['claude', 'harness', 'engineering', 'code', 'trae'],
    'AI Agent架构': ['agent', '架构', 'workflow', 'orchestration', 'workflow'],
    'DeepSeek技术': ['deepseek', 'deep seek'],
    'Prompt Engineering与AI工作流': ['prompt', 'prompting', '工作流', 'prompt engineering'],
    'Embedding模型选型': ['embedding', 'vector', '模型', '选'],
    'AI科研自动化': ['科研', 'research', 'academic', 'paper', 'arxiv'],
    '个人效能与方法论': ['效能', 'productivity', '方法论', '效率', 'time management'],
    '知识库构建': ['knowledge', 'kb', '知识库', 'knowledge base']
  };

  for (const [topic, keywords] of Object.entries(topicKeywords)) {
    if (keywords.some(k => content.toLowerCase().includes(k.toLowerCase()))) {
      return topic;
    }
  }
  return 'AI科研自动化';
}

function analyzeContent(items) {
  const analysis = {
    total: items.length,
    byTopic: {}
  };

  TOPICS.forEach(topic => {
    analysis.byTopic[topic] = [];
  });

  items.forEach(item => {
    const topic = classifyTopic(item.title + ' ' + (item.content || ''));
    if (!analysis.byTopic[topic]) {
      analysis.byTopic[topic] = [];
    }
    analysis.byTopic[topic].push(item);
  });

  return analysis;
}

function compileWikiContent(analysis) {
  const wikiFiles = {};

  for (const [topic, items] of Object.entries(analysis.byTopic)) {
    if (items.length === 0) continue;

    let content = `# ${topic}\n\n`;

    content += `> **摘要**: 本主题包含 ${items.length} 条相关内容，涵盖${items.map(i => i.title).slice(0, 3).join('、')}等核心议题。\n\n`;

    content += `## 内容列表\n\n`;

    items.forEach((item, index) => {
      content += `### ${index + 1}. ${item.title}\n\n`;

      if (item.content) {
        content += `${item.content.substring(0, 300)}...\n\n`;
      }

      if (item.url) {
        content += `**来源**: [${item.url}](${item.url})\n\n`;
      }

      content += `[[${topic}]]\n\n`;
    });

    wikiFiles[topic] = content;
  }

  return wikiFiles;
}

async function main() {
  console.log('=== IMA raw → wiki 增量编译流程 ===\n');

  console.log('步骤1: 获取raw知识库内容...');
  const rawItems = await getAllKnowledgeList(RAW_KB_ID);
  console.log(`步骤1完成: 共获取 ${rawItems.length} 条raw条目\n`);

  console.log('步骤2: 获取微信文章URL内容...');
  for (const item of rawItems) {
    if (item.url && item.url.includes('mp.weixin.qq.com')) {
      console.log(`获取微信文章: ${item.url}`);
      const content = await fetchUrlContent(item.url);
      if (content) {
        item.content = content.substring(0, 2000);
      }
    }
  }
  console.log('步骤2完成\n');

  console.log('步骤3: 内容分析与主题识别...');
  const analysis = analyzeContent(rawItems);
  console.log('步骤3完成\n');

  console.log('步骤4: 编译wiki文件...');
  const wikiFiles = compileWikiContent(analysis);
  console.log(`步骤4完成: 生成 ${Object.keys(wikiFiles).length} 个wiki文件\n`);

  console.log('步骤5: 智能更新策略...');
  const wikiList = await getAllKnowledgeList(WIKI_KB_ID);
  const existingTitles = new Set(wikiList.map(item => item.title));

  let newCount = 0;
  let appendCount = 0;
  const failures = [];
  const results = { new: [], appended: [] };

  for (const [topic, content] of Object.entries(wikiFiles)) {
    try {
      if (existingTitles.has(topic)) {
        console.log(`追加更新: ${topic}`);
        const notes = await searchNote(topic);
        if (notes.length > 0) {
          const noteId = notes[0].note_id || notes[0].id;
          const today = new Date().toISOString().split('T')[0];
          const appendContent = `\n---\n更新于 ${today}\n${content}`;
          await appendDoc(noteId, appendContent);
          appendCount++;
          results.appended.push(topic);
        } else {
          console.log(`未找到同名笔记，创建新笔记: ${topic}`);
          const createResult = await createNote(content);
          const noteId = createResult.note_id || createResult.id;
          await addWiki(noteId, topic);
          newCount++;
          results.new.push(topic);
        }
      } else {
        console.log(`新增: ${topic}`);
        const createResult = await createNote(content);
        const noteId = createResult.note_id || createResult.id;
        await addWiki(noteId, topic);
        newCount++;
        results.new.push(topic);
      }
    } catch (error) {
      console.error(`处理失败 ${topic}:`, error.message);
      failures.push({ topic, error: error.message });
    }
  }

  console.log(`\n步骤5完成: 新增 ${newCount} 个 | 追加更新 ${appendCount} 个\n`);

  console.log('=== 最终报告 ===');
  console.log(`raw条目数: ${rawItems.length}`);
  console.log(`新增: ${newCount} 个 - ${results.new.join(', ') || '无'}`);
  console.log(`已追加更新: ${appendCount} 个 - ${results.appended.join(', ') || '无'}`);
  if (failures.length > 0) {
    console.log('失败详情:');
    failures.forEach(f => console.log(`  - ${f.topic}: ${f.error}`));
  }
  console.log('\n=== 流程结束 ===');

  return {
    rawCount: rawItems.length,
    newCount,
    appendCount,
    results,
    failures
  };
}

main().catch(console.error);