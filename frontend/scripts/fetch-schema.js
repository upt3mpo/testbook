#!/usr/bin/env node
/**
 * Fetch OpenAPI schema from FastAPI backend
 *
 * This script fetches the OpenAPI schema from the running backend
 * and saves it for use in contract testing (Lab 6C).
 *
 * Usage:
 *   node scripts/fetch-schema.js
 *   API_URL=http://localhost:8000 node scripts/fetch-schema.js
 */

import fs from 'fs';
import http from 'http';
import https from 'https';
import path from 'path';
import { fileURLToPath } from 'url';

// ESM equivalents for __dirname
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const API_URL = process.env.API_URL || 'http://localhost:8000';
const OUTPUT_FILE = path.join(__dirname, '../src/tests/openapi-schema.json');

console.log(`📥 Fetching OpenAPI schema from ${API_URL}/openapi.json...`);

const client = API_URL.startsWith('https') ? https : http;

client.get(`${API_URL}/openapi.json`, (res) => {
  let data = '';

  res.on('data', (chunk) => {
    data += chunk;
  });

  res.on('end', () => {
    try {
      const schema = JSON.parse(data);

      // Ensure output directory exists
      const dir = path.dirname(OUTPUT_FILE);
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }

      fs.writeFileSync(OUTPUT_FILE, JSON.stringify(schema, null, 2));
      console.log(`✅ Schema saved to ${OUTPUT_FILE}`);
      console.log(`📊 Found ${Object.keys(schema.paths || {}).length} API endpoints`);
      console.log(`📋 FastAPI version: ${schema.info?.version || 'unknown'}`);

      // Show some stats
      const paths = Object.keys(schema.paths || {});
      const methods = paths.flatMap(p => Object.keys(schema.paths[p]));
      console.log(`📈 Total operations: ${methods.length}`);

    } catch (error) {
      console.error('❌ Failed to parse schema:', error.message);
      process.exit(1);
    }
  });
}).on('error', (error) => {
  console.error('❌ Failed to fetch schema:', error.message);
  console.error('💡 Make sure backend is running on', API_URL);
  console.error('   Run: ./start-dev.sh');
  process.exit(1);
});
