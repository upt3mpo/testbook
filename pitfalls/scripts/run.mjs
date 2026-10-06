/**
 * Convenience wrapper so the same commands work on macOS, Linux and Windows
 * (setting environment variables inline differs between shells).
 *
 *   npm run red -- catch-it/invisible-tab-stops       watch the reference test FAIL on the broken page
 *   npm run exercise -- catch-it/invisible-tab-stops  run YOUR test (exercise/) against both pages
 *   npm run test:py                                    run the Python reference solutions
 */
import { spawnSync } from 'node:child_process';

const [mode, target = ''] = process.argv.slice(2);
const env = { ...process.env };
let cmd;
let args;

if (mode === 'red') {
  env.SHOW_RED = '1';
  [cmd, args] = ['npx', ['playwright', 'test', '--project=broken', target]];
} else if (mode === 'exercise') {
  env.EXERCISES = '1';
  env.SHOW_RED = '1';
  [cmd, args] = ['npx', ['playwright', 'test', '--project=broken', '--project=fixed', target]];
} else if (mode === 'py') {
  [cmd, args] = ['python3', ['-m', 'pytest', target || '.']];
} else {
  console.error('Usage: node scripts/run.mjs <red|exercise|py> [path]');
  process.exit(2);
}
process.exit(spawnSync(cmd, args, { stdio: 'inherit', env, shell: process.platform === 'win32' }).status ?? 1);
