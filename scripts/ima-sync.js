#!/usr/bin/env node

import { writeFile } from "fs/promises";
import { join } from "path";

const API_KEY = "rSAWpVuJjTYWqwZSXrNWoHZSl+pvxL+tfPOAiW0nwVEAIQv9oToEMRAXHk+WDzGuyaSTh8CI4A==";
const CLIENT_ID = "673604a6665155cd973af671ab115321";
const RAW_KB_ID = "2Oor28yUr2eXyEFPBL0bwQU0DsrUEWPW-u9RF9CIUTw=";
const WIKI_KB_ID = "TcygOiKth0s91W35XJOu4NTAatl-57Bi2g19Wl3jvFw=";

const HEADERS = {
  "Content-Type": "application/json",
  "ima-openapi-clientid": CLIENT_ID,
  "ima-openapi-apikey": API_KEY,
};

let requestCount = 0;
const MAX_REQUESTS_PER_MINUTE = 30;

async function rateLimit() {
  requestCount++;
  if (requestCount % MAX_REQUESTS_PER_MINUTE === 0) {
    console.error(`  Rate limit: waiting 60 seconds...`);
    await new Promise(r => setTimeout(r, 60000));
  } else {
    await new Promise(r => setTimeout(r, 200));
  }
}

async function apiPost(url, body) {
  await rateLimit();
  const res = await fetch(url, {
    method: "POST",
    headers: HEADERS,
    body: JSON.stringify(body),
  });
  const data = await res.json();
  if (data.code !== 0) {
    if (data.code === 200001) {
      console.error(`  API Error ${data.code}: ${data.msg} - waiting 60 seconds...`);
      await new Promise(r => setTimeout(r, 60000));
      return apiPost(url, body);
    }
    throw new Error(`API Error ${data.code}: ${data.msg || JSON.stringify(data)}`);
  }
  return data.data;
}

async function getKnowledgeList(kbId, folderId = "001a718e4e00167e") {
  const allItems = [];
  let cursor = "";
  let isEnd = false;

  while (!isEnd) {
    const params = {
      knowledge_base_id: kbId,
      cursor,
      limit: 50,
    };
    if (folderId) {
      params.folder_id = folderId;
    }
    const data = await apiPost("https://ima.qq.com/openapi/wiki/v1/get_knowledge_list", params);
    
    const list = data.knowledge_list || [];
    if (Array.isArray(list)) {
      allItems.push(...list);
      console.error(`  Fetched ${list.length} items (folder: ${folderId || "root"})`);
    }
    
    cursor = data.next_cursor || "";
    isEnd = data.is_end || !cursor || list.length === 0;
    
    for (const item of list) {
      if (item.media_type === 99 && item.media_id) {
        console.error(`  Recursively fetching folder: ${item.title} (${item.media_id})`);
        const subItems = await getKnowledgeList(kbId, item.media_id);
        allItems.push(...subItems);
      }
    }
  }
  return allItems;
}

async function getNoteContent(noteId) {
  try {
    const data = await apiPost("https://ima.qq.com/openapi/note/v1/get_note", {
      note_id: noteId,
    });
    return data.content || "";
  } catch (err) {
    console.error(`  Get note content failed for "${noteId}": ${err.message}`);
    return "";
  }
}

async function searchNote(title) {
  try {
    const data = await apiPost("https://ima.qq.com/openapi/note/v1/search_note", {
      search_type: 0,
      query_info: { title },
      start: 0,
      end: 20,
    });
    return data.list || [];
  } catch (err) {
    console.error(`  Search note failed for "${title}": ${err.message}`);
    return [];
  }
}

async function createNote(content) {
  const data = await apiPost("https://ima.qq.com/openapi/note/v1/import_doc", {
    content_format: 1,
    content,
  });
  return data.note_id;
}

async function appendDoc(noteId, content) {
  await apiPost("https://ima.qq.com/openapi/note/v1/append_doc", {
    note_id: noteId,
    content_format: 1,
    content,
  });
}

async function addWiki(noteId, title) {
  await apiPost("https://ima.qq.com/openapi/wiki/v1/add_knowledge", {
    media_type: 11,
    note_info: { content_id: noteId },
    title,
    knowledge_base_id: WIKI_KB_ID,
  });
}

async function fetchUrlContent(url) {
  try {
    const res = await fetch(url, {
      headers: {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml",
      },
      signal: AbortSignal.timeout(30000),
    });
    if (!res.ok) {
      throw new Error(`HTTP ${res.status}`);
    }
    return await res.text();
  } catch (err) {
    console.error(`  Failed to fetch URL: ${url} - ${err.message}`);
    return null;
  }
}

function cleanContent(content) {
  if (!content) return "";
  return content
    .replace(/<script[\s\S]*?<\/script>/gi, "")
    .replace(/<style[\s\S]*?<\/style>/gi, "")
    .replace(/<[^>]+>/g, " ")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&nbsp;/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function extractSummary(content) {
  if (!content) return "";
  const lines = content.split(/[\n\r]+/).filter(line => line.trim());
  if (lines.length === 0) return "";
  return lines[0].slice(0, 300).trim() + (lines[0].length > 300 ? "..." : "");
}

const THEME_KEYWORDS = {
  "Claude Code与Harness Engineering": ["claude", "harness", "anthropic", "code", "engineering", "tool use", "agentic"],
  "AI Agent架构": ["agent", "architecture", "framework", "llm", "multi-agent", "orchestration", "workflow"],
  "DeepSeek技术": ["deepseek", "model", "llm", "training", "inference", "open source"],
  "Prompt Engineering与AI工作流": ["prompt", "engineering", "workflow", "chain", "rag", "fine-tuning", "instruction"],
  "Embedding模型选型": ["embedding", "vector", "model", "similarity", "search", "database"],
  "AI科研自动化": ["research", "automation", "paper", "arxiv", "scientific", "analysis"],
  "个人效能与方法论": ["productivity", "efficiency", "methodology", "workflow", "system", "note-taking"],
  "知识库构建": ["knowledge", "base", "kb", "wiki", "document", "organization", "retrieval"],
};

function classifyTheme(title, content) {
  const text = (title + " " + content).toLowerCase();
  let bestTheme = "其他";
  let bestScore = 0;

  for (const [theme, keywords] of Object.entries(THEME_KEYWORDS)) {
    let score = 0;
    for (const keyword of keywords) {
      if (text.includes(keyword)) score++;
    }
    if (score > bestScore) {
      bestScore = score;
      bestTheme = theme;
    }
  }

  if (bestScore === 0) {
    const fallback = Object.keys(THEME_KEYWORDS)[0];
    return fallback;
  }
  return bestTheme;
}

function generateMarkdown(title, content, theme) {
  const summary = extractSummary(content);
  const links = Object.keys(THEME_KEYWORDS)
    .filter(t => t !== theme)
    .map(t => `[[${t}]]`)
    .join(" ");

  return `# ${title}\n\n> ${summary}\n\n## 来源\n\n${content.slice(0, 2000)}\n\n## 关联主题\n\n${links}\n`;
}

async function main() {
  console.error("=== Step 1: 获取raw知识库内容 ===");
  const rawItems = await getKnowledgeList(RAW_KB_ID);
  console.error(`  Raw知识库条目数: ${rawItems.length}`);

  const rawContent = [];
  for (const item of rawItems) {
    if (item.media_type === 99) continue;
    
    console.error(`  Processing: ${item.title} (type: ${item.media_type})`);
    
    let content = item.content || "";
    
    if (item.content_id) {
      console.error(`    Fetching note content: ${item.content_id}`);
      const noteContent = await getNoteContent(item.content_id);
      if (noteContent) {
        content += "\n\n" + noteContent;
      }
    }
    
    if (item.url) {
      console.error(`    Fetching URL: ${item.url}`);
      const urlContent = await fetchUrlContent(item.url);
      if (urlContent) {
        content += "\n\n" + cleanContent(urlContent);
      }
    }
    
    rawContent.push({
      title: item.title,
      content: content,
      url: item.url,
      media_id: item.media_id,
      content_id: item.content_id,
    });
  }

  console.error("\n=== Step 2-3: 分析与主题识别 ===");
  const themeGroups = {};
  for (const item of rawContent) {
    const theme = classifyTheme(item.title, item.content);
    if (!themeGroups[theme]) themeGroups[theme] = [];
    themeGroups[theme].push(item);
    console.error(`  "${item.title}" -> ${theme}`);
  }

  console.error("\n=== Step 4: 编译wiki文件 ===");
  const wikiFiles = [];
  for (const [theme, items] of Object.entries(themeGroups)) {
    console.error(`  Compiling: ${theme} (${items.length} items)`);
    let markdown = `# ${theme}\n\n`;
    
    for (const item of items) {
      markdown += `## ${item.title}\n\n> ${extractSummary(item.content)}\n\n${item.content.slice(0, 500)}...\n\n`;
      if (item.url) {
        markdown += `**来源**: [${item.url}](${item.url})\n\n`;
      }
    }
    
    wikiFiles.push({
      title: theme,
      content: markdown,
      itemCount: items.length,
    });
  }

  console.error("\n=== Step 5: 智能更新策略 ===");
  console.error("  A. 获取wiki当前列表");
  const wikiItems = await getKnowledgeList(WIKI_KB_ID, "");
  const existingTitles = new Map();
  for (const item of wikiItems) {
    if (item.media_type !== 99) {
      existingTitles.set(item.title, item);
    }
  }
  console.error(`  Wiki现有条目: ${existingTitles.size}`);

  const results = {
    new: [],
    appended: [],
    failed: [],
  };

  const today = new Date().toISOString().split("T")[0];

  for (const wikiFile of wikiFiles) {
    console.error(`  B. Processing: ${wikiFile.title}`);
    
    if (existingTitles.has(wikiFile.title)) {
      console.error(`    Wiki中已存在同名笔记，尝试追加更新`);
      const existing = existingTitles.get(wikiFile.title);
      try {
        let noteId = existing.content_id || existing.media_id;
        if (!noteId) {
          const searchResults = await searchNote(wikiFile.title);
          if (searchResults.length > 0) {
            noteId = searchResults[0].note_id;
          }
        }
        if (!noteId) {
          throw new Error("无法获取note_id");
        }
        console.error(`    使用note_id: ${noteId}`);
        const appendContent = `\n---\n更新于 ${today}\n\n${wikiFile.content}`;
        await appendDoc(noteId, appendContent);
        results.appended.push(wikiFile.title);
        console.error(`    ✓ 已追加更新`);
      } catch (err) {
        if (err.message.includes("not author")) {
          console.error(`    ⚠ 跳过：权限不足，无法追加更新非本人创建的笔记`);
          results.appended.push(wikiFile.title + " (权限跳过)");
        } else {
          console.error(`    ✗ 追加更新失败: ${err.message}`);
          results.failed.push({ title: wikiFile.title, error: err.message });
        }
      }
    } else {
      console.error(`    Wiki中不存在同名笔记，创建新笔记`);
      try {
        const noteId = await createNote(wikiFile.content);
        console.error(`    Created note: ${noteId}`);
        await addWiki(noteId, wikiFile.title);
        results.new.push(wikiFile.title);
        console.error(`    ✓ 新增成功`);
      } catch (err) {
        console.error(`    ✗ 新增失败: ${err.message}`);
        results.failed.push({ title: wikiFile.title, error: err.message });
      }
    }
  }

  console.error("\n=== Step 6: 报告 ===");
  const report = `
## IMA Raw → Wiki 增量编译报告

**日期**: ${today}

### 统计数据
- **Raw知识库条目数**: ${rawContent.length}
- **主题数量**: ${Object.keys(themeGroups).length}
- **新增**: ${results.new.length} 个
- **追加更新**: ${results.appended.length} 个
- **失败**: ${results.failed.length} 个

### 新增主题
${results.new.length > 0 ? results.new.map(t => `- ${t}`).join("\n") : "无"}

### 追加更新主题
${results.appended.length > 0 ? results.appended.map(t => `- ${t}`).join("\n") : "无"}

### 失败详情
${results.failed.length > 0 ? results.failed.map(f => `- ${f.title}: ${f.error}`).join("\n") : "无"}

### 主题分布
${Object.entries(themeGroups).map(([theme, items]) => `- ${theme}: ${items.length} 条`).join("\n")}
  `;

  console.error(report);

  const reportPath = join(new URL(".", import.meta.url).pathname, "..", "sync-report.md");
  await writeFile(reportPath, report);
  console.error(`\n报告已保存到: ${reportPath}`);
}

main().catch(err => {
  console.error("IMA Sync failed:", err.message);
  console.error(err.stack);
  process.exit(1);
});