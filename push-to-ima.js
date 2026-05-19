
const fs = require('fs');
const https = require('https');

// 配置
const CLIENT_ID = '673604a6665155cd973af671ab115321';
const API_KEY = 'Y869muklEIrSezgzOdqLXdPZ/lOdmqDB3BY/s9DSIfu3+MmsALESLZe5ls2xLXRqfBFzw1OTqw==';
const KB_ID = 'TcygOiKth0s91W35XJOu4NTAatl-57Bi2g19Wl3jvFw==';
const FILE_PATH = '/workspace/daily-digest-2026-05-19.md';

// 读取文件内容
const content = fs.readFileSync(FILE_PATH, 'utf8');

// 步骤1: 导入文档
function importDocument() {
    return new Promise((resolve, reject) => {
        const postData = JSON.stringify({
            content_format: 1,
            content: content
        });

        const options = {
            hostname: 'ima.qq.com',
            port: 443,
            path: '/openapi/note/v1/import_doc',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'ima-openapi-clientid': CLIENT_ID,
                'ima-openapi-apikey': API_KEY,
                'Content-Length': Buffer.byteLength(postData)
            }
        };

        console.log('正在推送文档到 IMA...');

        const req = https.request(options, (res) => {
            let data = '';
            res.on('data', (chunk) => { data += chunk; });
            res.on('end', () => {
                try {
                    const result = JSON.parse(data);
                    console.log('文档导入成功:', result);
                    resolve(result);
                } catch (e) {
                    console.error('解析响应失败:', data);
                    reject(e);
                }
            });
        });

        req.on('error', (e) => {
            console.error('请求失败:', e);
            reject(e);
        });

        req.write(postData);
        req.end();
    });
}

// 步骤2: 添加到知识库
function addToKnowledgeBase(noteId) {
    return new Promise((resolve, reject) => {
        const postData = JSON.stringify({
            media_type: 11,
            note_info: {
                content_id: noteId
            },
            title: 'AI Builders 每日摘要 - 2026年5月19日',
            knowledge_base_id: KB_ID
        });

        const options = {
            hostname: 'ima.qq.com',
            port: 443,
            path: '/openapi/wiki/v1/add_knowledge',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'ima-openapi-clientid': CLIENT_ID,
                'ima-openapi-apikey': API_KEY,
                'Content-Length': Buffer.byteLength(postData)
            }
        };

        console.log('正在添加到知识库...');

        const req = https.request(options, (res) => {
            let data = '';
            res.on('data', (chunk) => { data += chunk; });
            res.on('end', () => {
                try {
                    const result = JSON.parse(data);
                    console.log('知识库添加成功:', result);
                    resolve(result);
                } catch (e) {
                    console.error('解析响应失败:', data);
                    reject(e);
                }
            });
        });

        req.on('error', (e) => {
            console.error('请求失败:', e);
            reject(e);
        });

        req.write(postData);
        req.end();
    });
}

// 执行完整流程
async function main() {
    try {
        console.log('开始执行 AI Builders 每日摘要推送流程...');
        
        // 导入文档
        const importResult = await importDocument();
        
        // 假设返回的结构中有 note_id/content_id
        const noteId = importResult.data?.content_id || importResult.data?.note_id || importResult.content_id;
        
        if (noteId) {
            // 添加到知识库
            await addToKnowledgeBase(noteId);
            console.log('\n✅ 完整流程执行成功!');
        } else {
            console.log('\n⚠️  文档导入成功，但无法找到 content_id 来添加到知识库');
            console.log('导入结果:', importResult);
        }
        
    } catch (error) {
        console.error('\n❌ 执行失败:', error);
    }
}

main();

