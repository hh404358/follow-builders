
import fetch from 'node-fetch';

const CONFIG = {
    clientId: '673604a6665155cd973af671ab115321',
    apiKey: 'Y869muklEIrSezgzOdqLXdPZ/lOdmqDB3BY/s9DSIfu3+MmsALESLZe5ls2xLXRqfBFzw1OTqw==',
    rawKbId: '2Oor28yUr2eXyEFPBL0bwQU0DsrUEWPW-u9RF9CIUTw=',
    wikiKbId: 'TcygOiKth0s91W35XJOu4NTAatl-57Bi2g19Wl3jvFw=',
    baseUrl: 'https://ima.qq.com/openapi'
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

const API = {
    async getKnowledgeList(kbId, cursor = '') {
        const url = `${CONFIG.baseUrl}/wiki/v1/get_knowledge_list`;
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'ima-openapi-clientid': CONFIG.clientId,
                'ima-openapi-apikey': CONFIG.apiKey
            },
            body: JSON.stringify({
                knowledge_base_id: kbId,
                cursor,
                limit: 50
            })
        });
        return response.json();
    },

    async createNote(content) {
        const url = `${CONFIG.baseUrl}/note/v1/import_doc`;
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'ima-openapi-clientid': CONFIG.clientId,
                'ima-openapi-apikey': CONFIG.apiKey
            },
            body: JSON.stringify({
                content_format: 1,
                content
            })
        });
        return response.json();
    },

    async searchNote(title) {
        const url = `${CONFIG.baseUrl}/note/v1/search_note`;
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'ima-openapi-clientid': CONFIG.clientId,
                'ima-openapi-apikey': CONFIG.apiKey
            },
            body: JSON.stringify({
                search_type: 0,
                query_info: { title },
                start: 0,
                end: 20
            })
        });
        return response.json();
    },

    async appendDoc(noteId, content) {
        const url = `${CONFIG.baseUrl}/note/v1/append_doc`;
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'ima-openapi-clientid': CONFIG.clientId,
                'ima-openapi-apikey': CONFIG.apiKey
            },
            body: JSON.stringify({
                note_id: noteId,
                content_format: 1,
                content
            })
        });
        return response.json();
    },

    async addToWiki(title, noteId) {
        const url = `${CONFIG.baseUrl}/wiki/v1/add_knowledge`;
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'ima-openapi-clientid': CONFIG.clientId,
                'ima-openapi-apikey': CONFIG.apiKey
            },
            body: JSON.stringify({
                media_type: 11,
                note_info: { content_id: noteId },
                title,
                knowledge_base_id: CONFIG.wikiKbId
            })
        });
        return response.json();
    }
};

async function getAllKnowledge(kbId) {
    const allItems = [];
    let cursor = '';
    let isEnd = false;

    while (!isEnd) {
        const result = await API.getKnowledgeList(kbId, cursor);
        if (result.data &amp;&amp; result.data.list) {
            allItems.push(...result.data.list);
        }
        cursor = result.data?.cursor || '';
        isEnd = result.data?.is_end ?? true;
    }

    return allItems;
}

function classifyContent(content) {
    const topicScores = {};
    TOPICS.forEach(topic =&gt; {
        topicScores[topic] = 0;
    });

    const keywords = {
        'Claude Code与Harness Engineering': ['claude', 'harness', 'code', 'coding', 'engineering'],
        'AI Agent架构': ['agent', '架构', 'framework', 'system', 'design'],
        'DeepSeek技术': ['deepseek', '模型', 'llm', '训练'],
        'Prompt Engineering与AI工作流': ['prompt', 'engineering', 'workflow', 'chain', '流程'],
        'Embedding模型选型': ['embedding', '向量', 'vector', 'retrieval'],
        'AI科研自动化': ['research', '科研', 'automation', '自动化', 'paper'],
        '个人效能与方法论': ['productivity', '效能', '方法论', 'method', 'tool'],
        '知识库构建': ['knowledge', 'wiki', '知识库', '组织', '整理']
    };

    for (const [topic, words] of Object.entries(keywords)) {
        for (const word of words) {
            if (content.toLowerCase().includes(word.toLowerCase())) {
                topicScores[topic]++;
            }
        }
    }

    const maxScore = Math.max(...Object.values(topicScores));
    const selectedTopic = Object.keys(topicScores).find(t =&gt; topicScores[t] === maxScore);
    
    return selectedTopic || '其他';
}

async function fetchWebContent(url) {
    try {
        const response = await fetch(url);
        const html = await response.text();
        const text = html.replace(/&lt;[^&gt;]*&gt;/g, ' ').replace(/\s+/g, ' ').trim();
        return text.substring(0, 5000);
    } catch (e) {
        console.error('WebFetch error:', e);
        return '';
    }
}

function getTodayDate() {
    const now = new Date();
    return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;
}

async function main() {
    console.log('开始执行 IMA raw → wiki 增量编译流程\n');
    
    const report = {
        rawEntries: 0,
        newTopics: 0,
        updatedTopics: 0,
        failed: [],
        details: {
            added: [],
            updated: []
        }
    };

    try {
        // 步骤1: 获取raw知识库内容
        console.log('步骤1: 获取raw知识库内容...');
        const rawItems = await getAllKnowledge(CONFIG.rawKbId);
        report.rawEntries = rawItems.length;
        console.log(`获取到 ${rawItems.length} 条 raw 内容\n`);

        // 步骤2-4: 分析并编译 wiki 文件
        console.log('步骤2-4: 分析内容并编译 wiki 文件...');
        const topicContents = {};
        TOPICS.forEach(topic =&gt; {
            topicContents[topic] = {
                summary: '',
                content: '',
                links: []
            };
        });

        for (const item of rawItems) {
            try {
                let content = item.title || '';
                if (item.url) {
                    const webContent = await fetchWebContent(item.url);
                    content += '\n' + webContent;
                }
                
                const topic = classifyContent(content);
                if (TOPICS.includes(topic)) {
                    topicContents[topic].content += `\n## ${item.title}\n`;
                    if (item.url) {
                        topicContents[topic].content += `来源: ${item.url}\n`;
                    }
                    topicContents[topic].links.push(item.title);
                }
            } catch (e) {
                console.error(`处理条目失败: ${item.title}`, e);
                report.failed.push(`条目: ${item.title}, 错误: ${e.message}`);
            }
        }

        // 生成 wiki 内容
        const wikiFiles = {};
        for (const [topic, data] of Object.entries(topicContents)) {
            if (data.content.trim()) {
                const links = data.links.map(l =&gt; `[[${l}]]`).join(' ');
                wikiFiles[topic] = `&gt; 主题: ${topic}\n&gt; 关联: ${links}\n\n${data.content}`;
            }
        }
        console.log(`编译完成 ${Object.keys(wikiFiles).length} 个主题文件\n`);

        // 步骤5: 智能更新策略
        console.log('步骤5: 智能更新 wiki 知识库...');
        const existingWiki = await getAllKnowledge(CONFIG.wikiKbId);
        const existingTitles = new Set(existingWiki.map(i =&gt; i.title));

        for (const [title, content] of Object.entries(wikiFiles)) {
            try {
                const date = getTodayDate();
                
                if (existingTitles.has(title)) {
                    // 查找现有笔记
                    const searchResult = await API.searchNote(title);
                    if (searchResult.data &amp;&amp; searchResult.data.list &amp;&amp; searchResult.data.list.length &gt; 0) {
                        const noteId = searchResult.data.list[0].note_id;
                        const appendContent = `\n---\n更新于 ${date}\n${content}`;
                        await API.appendDoc(noteId, appendContent);
                        report.updatedTopics++;
                        report.details.updated.push(title);
                        console.log(`已追加更新: ${title}`);
                    }
                } else {
                    // 创建新笔记
                    const createResult = await API.createNote(content);
                    if (createResult.data &amp;&amp; createResult.data.note_id) {
                        const noteId = createResult.data.note_id;
                        await API.addToWiki(title, noteId);
                        report.newTopics++;
                        report.details.added.push(title);
                        console.log(`已新增: ${title}`);
                    }
                }
            } catch (e) {
                console.error(`更新主题失败: ${title}`, e);
                report.failed.push(`主题: ${title}, 错误: ${e.message}`);
            }
        }

        // 步骤6: 报告
        console.log('\n===================== 编译报告 =====================');
        console.log(`raw 条目数: ${report.rawEntries}`);
        console.log(`新增: ${report.newTopics} 个`);
        console.log(`追加更新: ${report.updatedTopics} 个`);
        
        if (report.details.added.length &gt; 0) {
            console.log('\n新增主题:');
            report.details.added.forEach(t =&gt; console.log(`  - ${t}`));
        }
        
        if (report.details.updated.length &gt; 0) {
            console.log('\n追加更新主题:');
            report.details.updated.forEach(t =&gt; console.log(`  - ${t}`));
        }
        
        if (report.failed.length &gt; 0) {
            console.log('\n失败详情:');
            report.failed.forEach(f =&gt; console.log(`  - ${f}`));
        }
        
        console.log('====================================================');

    } catch (e) {
        console.error('执行失败:', e);
        report.failed.push(`全局错误: ${e.message}`);
    }
    
    return report;
}

main().catch(console.error);

