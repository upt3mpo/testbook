/**
 * Keeps the collection honest. Every pitfall must have the same shape, be linked from the
 * landing page, and have reference solutions in BOTH language tracks. Add a pitfall and
 * forget one of these, and this fails.
 */
import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { expect, test } from '@playwright/test';

const ROOT = new URL('.', import.meta.url).pathname;
const SHELVES = { 'catch-it': 'solution', 'trust-it': 'solution' };
const index = readFileSync(join(ROOT, 'index.html'), 'utf-8');

const pitfalls = Object.keys(SHELVES).flatMap((shelf) =>
  readdirSync(join(ROOT, shelf), { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => ({ shelf, slug: entry.name, dir: join(ROOT, shelf, entry.name) }))
);

test('there are pitfalls on both shelves', () => {
  expect(pitfalls.filter((p) => p.shelf === 'catch-it').length).toBeGreaterThan(0);
  expect(pitfalls.filter((p) => p.shelf === 'trust-it').length).toBeGreaterThan(0);
});

for (const { shelf, slug, dir } of pitfalls) {
  test(`${shelf}/${slug} is complete`, () => {
    const required = ['README.md', 'exercise.md', 'broken/index.html', 'fixed/index.html'];
    if (shelf === 'trust-it') required.push('suspect');
    for (const file of required) expect(existsSync(join(dir, file)), `${file} is missing`).toBe(true);

    // Both language tracks, for the reference solution and the learner exercise.
    for (const sub of ['solution', 'exercise']) {
      const files = readdirSync(join(dir, sub));
      expect(
        files.some((f) => f.endsWith('.spec.js')),
        `${sub}/ needs a JavaScript file`
      ).toBe(true);
      expect(
        files.some((f) => f.startsWith('test_') && f.endsWith('.py')),
        `${sub}/ needs a Python file`
      ).toBe(true);
    }
    if (shelf === 'trust-it') {
      const files = readdirSync(join(dir, 'suspect'));
      expect(
        files.some((f) => f.endsWith('.spec.js')),
        'suspect/ needs a JavaScript file'
      ).toBe(true);
      expect(
        files.some((f) => f.endsWith('.py')),
        'suspect/ needs a Python file'
      ).toBe(true);
    }
  });

  test(`${shelf}/${slug} is linked from the landing page`, () => {
    expect(index).toContain(`${shelf}/${slug}/broken/`);
    expect(index).toContain(`${shelf}/${slug}/fixed/`);
  });

  test(`${shelf}/${slug} pages are accessible documents themselves`, () => {
    // The broken page is broken in exactly ONE way. Everything else about it must still be a
    // proper page, or the lesson is muddied: a language, a title, a main landmark, one h1.
    for (const edition of ['broken', 'fixed']) {
      const html = readFileSync(join(dir, edition, 'index.html'), 'utf-8');
      expect(html, `${edition}: <html lang>`).toMatch(/<html lang="en">/);
      expect(html, `${edition}: <title>`).toMatch(/<title>[^<]+<\/title>/);
      expect(html, `${edition}: <main>`).toContain('<main>');
      expect((html.match(/<h1[ >]/g) || []).length, `${edition}: exactly one h1`).toBe(1);
    }
  });
}
