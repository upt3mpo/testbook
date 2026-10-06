// Pitfalls have their own runner, separate from Testbook's suite (tests/). Each pitfall's
// reference solution runs twice: against its `broken` page and its `fixed` page.
//
//   broken project: the reference test is EXPECTED to fail (test.fail), and that expected
//                   failure is what proves the pitfall is real. Set SHOW_RED=1 to see the
//                   actual red failure instead.
//   fixed project:  the same test must pass.
import { defineConfig } from '@playwright/test';

const PORT = Number(process.env.PITFALLS_PORT || 4100);
// Learner skeletons are ignored unless asked for (npm run exercise -- <path>). This has to
// be repeated per project: a project-level testIgnore replaces the top-level one.
const ignoreExercises = process.env.EXERCISES ? [] : ['**/exercise/**'];

export default defineConfig({
  testDir: '.',
  testMatch: ['**/solution/*.spec.js', '**/suspect/*.spec.js', '**/exercise/*.spec.js', 'catalog.spec.js'],
  timeout: 20_000,
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: 0,
  reporter: [['list'], ['html', { outputFolder: 'playwright-report', open: 'never' }]],
  use: { baseURL: `http://localhost:${PORT}` },
  projects: [
    { name: 'broken', testIgnore: ['catalog.spec.js', ...ignoreExercises] },
    { name: 'fixed', testIgnore: ['catalog.spec.js', ...ignoreExercises] },
    { name: 'catalog', testMatch: ['catalog.spec.js'] },
  ],
  webServer: {
    command: 'node serve.mjs',
    url: `http://localhost:${PORT}`,
    reuseExistingServer: true,
    env: { PITFALLS_PORT: String(PORT) },
  },
});
