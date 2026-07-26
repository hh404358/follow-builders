import json
import os
from datetime import datetime

RAW_KB_ID = "2Oor28yUr2eXyEFPBL0bwQU0DsrUEWPW-u9RF9CIUTw="
WIKI_KB_ID = "TcygOiKth0s91W35XJOu4NTAatl-57Bi2g19Wl3jvFw="

EXISTING_TOPICS = [
    "Claude Code与Harness Engineering",
    "AI Agent架构",
    "DeepSeek技术",
    "Prompt Engineering与AI工作流",
    "Embedding模型选型",
    "AI科研自动化",
    "个人效能与方法论",
    "知识库构建"
]

def load_feed_data():
    data = []
    
    with open('/workspace/feed-blogs.json', 'r') as f:
        blogs = json.load(f)
        for blog in blogs['blogs']:
            data.append({
                'type': 'blog',
                'title': blog['title'],
                'source': blog['name'],
                'content': blog['content'],
                'url': blog['url'],
                'published_at': blog.get('publishedAt')
            })
    
    with open('/workspace/feed-x.json', 'r') as f:
        x_data = json.load(f)
        for user in x_data['x']:
            for tweet in user['tweets']:
                data.append({
                    'type': 'tweet',
                    'title': tweet['text'][:80],
                    'source': user['name'],
                    'content': tweet['text'],
                    'url': tweet['url'],
                    'published_at': tweet['createdAt']
                })
    
    with open('/workspace/feed-podcasts.json', 'r') as f:
        podcasts = json.load(f)
        for podcast in podcasts['podcasts']:
            data.append({
                'type': 'podcast',
                'title': podcast['title'],
                'source': podcast['name'],
                'content': podcast['transcript'],
                'url': podcast['url'],
                'published_at': podcast.get('publishedAt')
            })
    
    return data

def analyze_content(raw_data):
    analysis = {
        'total_items': len(raw_data),
        'by_type': {},
        'topics': {},
        'trends': [],
        'cross_references': []
    }
    
    for item in raw_data:
        item_type = item['type']
        if item_type not in analysis['by_type']:
            analysis['by_type'][item_type] = 0
        analysis['by_type'][item_type] += 1
    
    topic_keywords = {
        'Claude Code与Harness Engineering': ['claude', 'code', 'auto mode', 'harness', 'engineering', 'permission', 'classifier', 'agentic'],
        'AI Agent架构': ['agent', 'agents', 'multi-agent', 'orchestrator', 'framework', 'architecture', 'tool use', 'tool selection'],
        'DeepSeek技术': ['deepseek'],
        'Prompt Engineering与AI工作流': ['prompt', 'prompt injection', 'workflow', 'evaluation', 'classifier', 'safety'],
        'Embedding模型选型': ['embedding', 'embeddings', 'vector', 'model selection', 'multi-modal'],
        'AI科研自动化': ['research', 'automation', 'eval', 'evaluation', 'testing', 'QA'],
        '个人效能与方法论': ['productivity', 'efficiency', 'methodology', 'system', 'workflow', 'devops', 'deepsec'],
        '知识库构建': ['knowledge', 'knowledge base', 'memory', 'retrieval', 'vector db', 'graph']
    }
    
    for item in raw_data:
        content = item['content'].lower() + ' ' + item['title'].lower()
        matched_topics = []
        
        for topic, keywords in topic_keywords.items():
            if any(keyword.lower() in content for keyword in keywords):
                matched_topics.append(topic)
                if topic not in analysis['topics']:
                    analysis['topics'][topic] = []
                analysis['topics'][topic].append(item)
        
        if matched_topics:
            for i, t1 in enumerate(matched_topics):
                for t2 in matched_topics[i+1:]:
                    ref = (t1, t2) if t1 < t2 else (t2, t1)
                    if ref not in analysis['cross_references']:
                        analysis['cross_references'].append(ref)
    
    trend_patterns = [
        ('agent adoption', ['agent', 'agents', 'multi-agent', 'orchestrator']),
        ('auto mode safety', ['auto mode', 'classifier', 'safety', 'permission']),
        ('embedding diversity', ['embedding', 'multi-modal', 'vector']),
        ('AI in education', ['education', 'student', 'class', 'teacher']),
        ('open source AI', ['open source', 'oss', 'github'])
    ]
    
    for trend_name, keywords in trend_patterns:
        count = sum(1 for item in raw_data if any(k.lower() in (item['content'] + item['title']).lower() for k in keywords))
        if count > 0:
            analysis['trends'].append({'name': trend_name, 'count': count})
    
    return analysis

def compile_wiki_files(analysis):
    wiki_dir = '/workspace/wiki'
    os.makedirs(wiki_dir, exist_ok=True)
    
    wiki_files = {}
    
    for topic, items in analysis['topics'].items():
        filename = f"{topic.replace('/', '_').replace(' ', '_')}.md"
        filepath = os.path.join(wiki_dir, filename)
        
        content = f"# {topic}\n\n"
        content += f"> 本主题共收录 {len(items)} 条内容\n\n"
        
        for item in items:
            content += f"## {item['title']}\n\n"
            content += f"> **来源**: {item['source']} | **类型**: {item['type']}\n"
            if item.get('url'):
                content += f"> **链接**: [{item['url']}]({item['url']})\n"
            if item.get('published_at'):
                content += f"> **发布时间**: {item['published_at']}\n"
            content += "\n"
            
            if item['type'] == 'tweet':
                content += item['content'] + "\n\n"
            else:
                content += item['content'][:500] + "..." if len(item['content']) > 500 else item['content']
                content += "\n\n"
        
        for other_topic in analysis['topics']:
            if other_topic != topic:
                pair = (topic, other_topic) if topic < other_topic else (other_topic, topic)
                if pair in analysis['cross_references']:
                    content += f"[[{other_topic}]]\n"
        
        wiki_files[topic] = {'filename': filename, 'filepath': filepath, 'content': content}
    
    for topic, info in wiki_files.items():
        with open(info['filepath'], 'w', encoding='utf-8') as f:
            f.write(info['content'])
    
    return wiki_files

def simulate_wiki_update(wiki_files):
    existing_notes = {
        'Claude Code与Harness Engineering': {'note_id': 'note_1', 'exists': True},
        'AI Agent架构': {'note_id': 'note_2', 'exists': True},
        '个人效能与方法论': {'note_id': 'note_3', 'exists': True}
    }
    
    results = {
        'new': [],
        'updated': [],
        'failed': []
    }
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    for topic, info in wiki_files.items():
        if topic in existing_notes:
            append_content = f"\n---\n更新于 {today}\n{info['content'][:200]}..."
            results['updated'].append({
                'topic': topic,
                'note_id': existing_notes[topic]['note_id'],
                'action': 'append_doc',
                'content': append_content
            })
        else:
            results['new'].append({
                'topic': topic,
                'action': 'create_and_add',
                'content': info['content']
            })
    
    return results

def generate_report(raw_data, analysis, update_results):
    report = f"""
# IMA Raw → Wiki 增量编译报告

## 执行时间
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 一、Raw知识库概览

- **总条目数**: {analysis['total_items']}
- **条目类型分布**:
{chr(10).join([f"  - {k}: {v}条" for k, v in analysis['by_type'].items()])}

## 二、内容分析

### 2.1 纵向溯源

本批次内容涵盖多个AI领域的最新动态，包括：
- Claude Code的auto mode安全机制
- AI Agent的工具使用和架构设计
- 自动驾驶领域的技术演进（Waymo）

### 2.2 横向对比

不同来源对相同主题的观点对比：
- **AI Agent安全性**: Anthropic强调分类器和权限控制，Vercel推出deepsec进行深度安全审查
- **AI商业化**: Swyx对比OAI和Anthropic估值，Aaron Levie讨论企业AI部署趋势

### 2.3 趋势判断

{chr(10).join([f"- **{t['name']}**: {t['count']}条相关内容" for t in analysis['trends']])}

## 三、主题识别

共识别出 {len(analysis['topics'])} 个主题：

{chr(10).join([f"- **{topic}**: {len(items)}条内容" for topic, items in analysis['topics'].items()])}

## 四、Wiki更新结果

### 4.1 新增笔记
- 数量: {len(update_results['new'])}
{chr(10).join([f"  - {item['topic']}" for item in update_results['new']])}

### 4.2 追加更新
- 数量: {len(update_results['updated'])}
{chr(10).join([f"  - {item['topic']}" for item in update_results['updated']])}

### 4.3 失败记录
- 数量: {len(update_results['failed'])}

## 五、跨主题关联

{chr(10).join([f"- [[{t1}]] ↔ [[{t2}]]" for t1, t2 in analysis['cross_references']])}

## 六、备注

⚠️ **注意**: IMA API认证失败（错误码200002），本次编译基于本地feed数据模拟执行。
请检查API Key是否过期或格式是否正确，并重试完整流程。
"""
    return report

def main():
    print("步骤1: 加载raw知识库内容...")
    raw_data = load_feed_data()
    print(f"  已加载 {len(raw_data)} 条内容")
    
    print("\n步骤2: 分析内容...")
    analysis = analyze_content(raw_data)
    print(f"  识别出 {len(analysis['topics'])} 个主题")
    print(f"  发现 {len(analysis['trends'])} 个趋势")
    print(f"  发现 {len(analysis['cross_references'])} 个跨主题关联")
    
    print("\n步骤3: 编译wiki文件...")
    wiki_files = compile_wiki_files(analysis)
    print(f"  已生成 {len(wiki_files)} 个wiki文件")
    
    print("\n步骤4: 模拟Wiki更新...")
    update_results = simulate_wiki_update(wiki_files)
    print(f"  新增: {len(update_results['new'])}")
    print(f"  追加更新: {len(update_results['updated'])}")
    
    print("\n步骤5: 生成报告...")
    report = generate_report(raw_data, analysis, update_results)
    report_path = '/workspace/report.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"  报告已保存到 {report_path}")
    
    print("\n" + "="*60)
    print(report)

if __name__ == '__main__':
    main()