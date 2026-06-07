#!/usr/bin/env node
import dotenv from 'dotenv';
import https from 'https';
import fs from 'fs';
import path from 'path';

// Load environment variables
dotenv.config();

// IMA Configuration from user input
const IMA_API_KEY = 'rSAWpVuJjTYWqwZSXrNWoHZSl+pvxL+tfPOAiW0nwVEAIQv9oToEMRAXHk+WDzGuyaSTh8CI4A==';
const IMA_CLIENT_ID = '673604a6665155cd973af671ab115321';
const RAW_KB_ID = '2Oor28yUr2eXyEFPBL0bwQU0DsrUEWPW-u9RF9CIUTw=';
const WIKI_KB_ID = 'TcygOiKth0s91W35XJOu4NTAatl-57Bi2g19Wl3jvFw=';

// Helper function to make HTTPS requests
function makeRequest(url, options, data = null) {
  return new Promise((resolve, reject) => {
    const req = https.request(url, options, (res) => {
      let body = '';
      res.on('data', (chunk) => body += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(body);
          resolve(result);
        } catch (err) {
          reject(err);
        }
      });
    });
    req.on('error', reject);
    if (data) {
      req.write(JSON.stringify(data));
    }
    req.end();
  });
}

// Step 1: Fetch raw KB content
async function fetchRawKB() {
  console.log('Fetching raw KB content...');
  const allItems = [];
  let cursor = '';
  let isEnd = false;

  while (!isEnd) {
    const response = await makeRequest(
      'https://ima.qq.com/openapi/wiki/v1/get_knowledge_list',
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'ima-openapi-clientid': IMA_CLIENT_ID,
          'ima-openapi-apikey': IMA_API_KEY
        }
      },
      {
        knowledge_base_id: RAW_KB_ID,
        cursor: cursor,
        limit: 50
      }
    );

    if (response.list) {
      allItems.push(...response.list);
    }
    cursor = response.cursor || '';
    isEnd = response.is_end;
  }

  console.log(`Fetched ${allItems.length} items from raw KB`);
  return allItems;
}

// Main function
async function main() {
  try {
    const rawItems = await fetchRawKB();
    console.log('Raw items:', rawItems);
  } catch (error) {
    console.error('Error:', error);
    process.exit(1);
  }
}

main();
