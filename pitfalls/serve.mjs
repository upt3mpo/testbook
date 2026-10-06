/**
 * A tiny static file server for the pitfalls: no dependencies, no build step.
 * Serves this folder on http://localhost:4100 (override with PITFALLS_PORT).
 * Directory URLs serve their index.html, so /catch-it/placeholder-as-label/broken/
 * just works.
 */
import { createReadStream, existsSync, statSync } from 'node:fs';
import { createServer } from 'node:http';
import { extname, join, normalize, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(fileURLToPath(new URL('.', import.meta.url)));
const PORT = Number(process.env.PITFALLS_PORT || 4100);
const TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json',
  '.md': 'text/plain; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
};

createServer((req, res) => {
  const pathname = decodeURIComponent(new URL(req.url, 'http://x').pathname);
  let file = resolve(join(ROOT, normalize(pathname)));
  // Never serve anything outside this folder, and never serve installed packages.
  if (!file.startsWith(ROOT) || file.includes('node_modules')) {
    res.writeHead(403).end('Forbidden');
    return;
  }
  if (existsSync(file) && statSync(file).isDirectory()) file = join(file, 'index.html');
  if (!existsSync(file)) {
    res.writeHead(404).end('Not found');
    return;
  }
  res.writeHead(200, { 'Content-Type': TYPES[extname(file)] || 'application/octet-stream' });
  createReadStream(file).pipe(res);
}).listen(PORT, () => console.log(`Pitfalls on http://localhost:${PORT}`));
