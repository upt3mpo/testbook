#!/usr/bin/env node
// Accessibility lint for markdown docs.
// Rules: no emoji outside code, no ASCII progress bars, no vague link text.
// Exempt: U+2713 and U+2717 (check/cross marks used with a text label).
import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';

const files = execFileSync('git', ['ls-files', '*.md'], { encoding: 'utf8' })
  .split('\n')
  .filter(Boolean);

const emoji = /[\p{Extended_Pictographic}\u{FE0F}\u{200D}]/u;
const exempt = /[✓✗]/gu;
const bar = /[█░▓▒]{3,}/u;
const vague = /\[(here|click here|link|this|read more|more)\]\(/i;

let problems = 0;
for (const file of files) {
  let fenced = false;
  readFileSync(file, 'utf8').split('\n').forEach((line, i) => {
    if (line.trimStart().startsWith('```')) { fenced = !fenced; return; }
    if (fenced) return;
    const text = line.replace(/`[^`]*`/g, '').replace(exempt, '');
    const report = (msg) => { problems++; console.log(`${file}:${i + 1}: ${msg}`); };
    if (emoji.test(text)) report('emoji outside code (use words)');
    if (bar.test(text)) report('ASCII progress bar (use text)');
    if (vague.test(text)) report('vague link text (describe the destination)');
  });
}
console.log(problems ? `${problems} problem(s)` : 'docs a11y lint: clean');
process.exit(problems ? 1 : 0);
