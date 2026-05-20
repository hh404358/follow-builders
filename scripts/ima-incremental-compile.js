import fs from 'fs';

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

function apiCall(path, body) {
    const url = `${CONFIG.baseUrl}${path}`;
    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'ima-openapi-clientid': CONFIG.clientId,
            'ima-openapi-apikey': CONFIG.apiKey
        },
        body: JSON.stringify(body)
    }).then(r => r.json());
}

async function getAllKnowledge(kbId) {
    const allItems = [];
    let cursor = '';
    let isEnd = false;
    let pageNum = 0;

    while (!isEnd) {
        pageNum++;
        const result = await apiCall('/wiki/v1/get_knowledge_list', {
            knowledge_base_id: kbId, cursor, limit: 50
        });
        if (result.data && result.data.knowledge_list) {
            allItems.push(...result.data.knowledge_list);
        }
        cursor = result.data?.cursor || '';
        isEnd = result.data?.is_end ?? true;
    }
    return allItems;
}

async function findNoteByTitle(title) {
    for (const searchTitle of [title]) {
        const result = await apiCall('/note/v1/search_note', {
            search_type: 0,
            query_info: { title: searchTitle },
            start: 0,
            end: 20
        });
        if (result.data && result.data.search_note_infos && result.data.search_note_infos.length > 0) {
            return result.data.search_note_infos[0].note_book_info;
        }
    }
    return null;
}

function classifyContent(title) {
    const scores = {};
    TOPICS.forEach(t => { scores[t] = 0; });

    const rules = [
        { regex: /claude|harness|claude.?code/i, topic: 'Claude Code与Harness Engineering' },
        { regex: /agent|代理|架构|多.?agent|multi.?agent|hermes|openclaw|nanobot|deerflow/i, topic: 'AI Agent架构' },
        { regex: /deepseek|ds.?v/i, topic: 'DeepSeek技术' },
        { regex: /prompt|提示|engineering|workflow|工作流|chain|skill/i, topic: 'Prompt Engineering与AI工作流' },
        { regex: /embedding|向量|vector|jina|bge|qwen|gemini|嵌入|检索|retrieval/i, topic: 'Embedding模型选型' },
        { regex: /research|科研|paper|论文|academic|学术|自动化|顶会|acl|cvpr|arxiv/i, topic: 'AI科研自动化' },
        { regex: /效能|效率|方法论|method|productivity|gtd|学习|方法|笔记|习惯|第二脑|脑|个人/i, topic: '个人效能与方法论' },
        { regex: /知识库|knowledge|wiki|组织|整理|构建|索引|知识管理/i, topic: '知识库构建' },
    ];

    for (const rule of rules) {
        if (rule.regex.test(title)) {
            scores[rule.topic]++;
        }
    }

    const maxScore = Math.max(...Object.values(scores));
    if (maxScore === 0) return '其他';
    return Object.keys(scores).find(t => scores[t] === maxScore);
}

function analyzeTopic(items) {
    const titles = items.map(i => i.title);
    const types = {};
    items.forEach(i => {
        const typeLabels = { 1: 'PDF', 3: 'Word', 4: 'PPT', 6: '微信文章', 7: 'Markdown', 11: '笔记', 99: '文件夹' };
        const label = typeLabels[i.media_type] || `类型${i.media_type}`;
        types[label] = (types[label] || 0) + 1;
    });

    return { titles, types, count: items.length };
}

function compileTopicContent(topic, items) {
    const analysis = analyzeTopic(items);
    const typeSummary = Object.entries(analysis.types)
        .map(([k, v]) => `${k}×${v}`)
        .join(' | ');

    const relatedTopics = TOPICS.filter(t => t !== topic);
    const crossLinks = relatedTopics.map(t => `[[${t}]]`).join(' ');

    let content = `> 摘要：本周 ${topic} 相关材料 ${analysis.count} 条（${typeSummary}），涵盖最新动态与深度分析。
> 关联主题：${crossLinks}

`;

    if (topic === 'Claude Code与Harness Engineering') {
        content += `## Harness Engineering 核心理念
Harness Engineering 是 2026 年 AI 工程领域最核心的范式——将 LLM 的「原始能力」通过工程化外壳转化为可靠的「产品能力」。Claude Code 是当前最完整的 Harness 实现。

## 本周动态
`;
    } else if (topic === 'AI Agent架构') {
        content += `## Agent 架构选型
2026 年是 AI Agent 爆发年。不同架构设计哲学与适用场景各具特色。

## 本周动态
`;
    } else if (topic === 'DeepSeek技术') {
        content += `## DeepSeek 技术前沿
DeepSeek 作为国产开源模型代表，持续在效率优化和多模态领域发力。

## 本周动态
`;
    } else if (topic === 'Prompt Engineering与AI工作流') {
        content += `## Prompt Engineering 与 AI 工作流
高效 Prompt 设计和 AI 工作流编排是提升 AI 产出的关键。

## 本周动态
`;
    } else if (topic === 'Embedding模型选型') {
        content += `## Embedding 模型选型指南
Embedding 是 RAG 系统的核心技术，模型选择直接影响检索质量。

## 本周动态
`;
    } else if (topic === 'AI科研自动化') {
        content += `## AI 科研自动化
AI 正在改变科研工作流程，从文献检索到论文撰写全面赋能。

## 本周动态
`;
    } else if (topic === '个人效能与方法论') {
        content += `## 个人效能提升
AI 时代的个人效能方法论与工具实践。

## 本周动态
`;
    } else {
        content += `## 知识库构建方法论
AI 时代个人和组织的知识管理策略与工具选择。

## 本周动态
`;
    }

    for (const item of items) {
        content += `- [[${item.title}]]\n`;
    }

    return content;
}

function getTodayDate() {
    const now = new Date();
    return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;
}

async function main() {
    const date = getTodayDate();
    console.log(`=== IMA Raw → Wiki 增量编译 (${date}) ===\n`);

    const report = {
        rawTotal: 0, rawNotes: 0, rawArticles: 0, rawOther: 0,
        topicsAnalyzed: 0,
        newTopics: 0, updatedTopics: 0,
        added: [], updated: [],
        failed: []
    };

    console.log('[步骤1] 获取 raw 知识库内容...');
    const rawItems = await getAllKnowledge(CONFIG.rawKbId);
    report.rawTotal = rawItems.length;
    report.rawNotes = rawItems.filter(i => i.media_type === 11).length;
    report.rawArticles = rawItems.filter(i => i.media_type === 6).length;
    report.rawOther = rawItems.filter(i => ![6, 11, 99].includes(i.media_type)).length;
    const rawFolders = rawItems.filter(i => i.media_type === 99).length;
    console.log(`  总计 ${rawItems.length} 条（笔记${report.rawNotes}, 微信${report.rawArticles}, 其他${report.rawOther}, 文件夹${rawFolders}）\n`);

    console.log('[步骤2-4] 分析内容并编译 wiki 文件...');
    const contentItems = rawItems.filter(i => i.media_type !== 99 && i.title);
    const topicGroups = {};
    TOPICS.forEach(t => { topicGroups[t] = []; });
    const others = [];

    for (const item of contentItems) {
        const topic = classifyContent(item.title);
        if (TOPICS.includes(topic)) {
            topicGroups[topic].push(item);
        } else {
            others.push(item);
        }
    }

    const wikiEntries = {};
    for (const [topic, items] of Object.entries(topicGroups)) {
        if (items.length > 0) {
            wikiEntries[topic] = compileTopicContent(topic, items);
        }
    }
    report.topicsAnalyzed = Object.keys(wikiEntries).length;
    console.log(`  编译完成 ${Object.keys(wikiEntries).length} 个主题文件\n`);

    console.log('[步骤5] 智能更新 wiki 知识库...');
    for (const [title, content] of Object.entries(wikiEntries)) {
        try {
            const noteInfo = await findNoteByTitle(title);

            if (noteInfo) {
                const appendContent = `\n---\n更新于 ${date}\n${content}`;
                const appendResult = await apiCall('/note/v1/append_doc', {
                    note_id: noteInfo.note_id,
                    content_format: 1,
                    content: appendContent
                });
                if (appendResult.code === 0) {
                    report.updatedTopics++;
                    report.updated.push(title);
                    console.log(`  已追加更新: ${title} (note: ${noteInfo.note_id})`);
                } else {
                    report.failed.push(`追加失败: ${title}, code=${appendResult.code} msg=${appendResult.msg}`);
                }
            } else {
                const createResult = await apiCall('/note/v1/import_doc', {
                    content_format: 1,
                    content
                });
                if (createResult.code === 0 && createResult.data?.note_id) {
                    const noteId = createResult.data.note_id;
                    const wikiResult = await apiCall('/wiki/v1/add_knowledge', {
                        media_type: 11,
                        note_info: { content_id: noteId },
                        title,
                        knowledge_base_id: CONFIG.wikiKbId
                    });
                    if (wikiResult.code === 0) {
                        report.newTopics++;
                        report.added.push(title);
                        console.log(`  已新增: ${title} (note: ${noteId})`);
                    } else {
                        report.failed.push(`wiki添加失败: ${title}, code=${wikiResult.code} msg=${wikiResult.msg}`);
                    }
                } else {
                    report.failed.push(`创建笔记失败: ${title}, code=${createResult.code} msg=${createResult.msg}`);
                }
            }
        } catch (e) {
            report.failed.push(`${title}: ${e.message}`);
            console.error(`  失败: ${title} - ${e.message}`);
        }
    }

    console.log('\n===================== 编译报告 =====================');
    console.log(`日期: ${date}`);
    console.log(`raw 总条目: ${report.rawTotal}`);
    console.log(`  笔记: ${report.rawNotes}, 微信文章: ${report.rawArticles}, 其他: ${report.rawOther}`);
    console.log(`编译主题: ${report.topicsAnalyzed} 个`);
    console.log(`新增: ${report.newTopics} 个 | 追加更新: ${report.updatedTopics} 个`);

    if (report.added.length > 0) {
        console.log('\n新增主题:');
        report.added.forEach(t => console.log(`  + ${t}`));
    }
    if (report.updated.length > 0) {
        console.log('\n追加更新主题:');
        report.updated.forEach(t => console.log(`  ~ ${t}`));
    }
    if (report.failed.length > 0) {
        console.log('\n失败详情:');
        report.failed.forEach(f => console.log(`  ! ${f}`));
    }
    console.log('====================================================\n');

    const reportFile = `/workspace/reports/ima-compile-${date}.json`;
    try { fs.mkdirSync('/workspace/reports', { recursive: true }); } catch {}
    fs.writeFileSync(reportFile, JSON.stringify(report, null, 2));
    console.log(`报告已保存: ${reportFile}`);

    return report;
}

main().catch(console.error);