/**
 * Helpers shared by every pitfall's tests.
 *
 * A pitfall folder contains `broken/` and `fixed/` pages. The Playwright *project* name
 * (broken or fixed) chooses which one a test opens, so ONE test body is run against both.
 */
import { test } from '@playwright/test';

/** Open this pitfall's page for the current project (broken or fixed). */
export async function openPitfall(page, dir) {
  const edition = test.info().project.name;
  await page.goto(`/${dir}/${edition}/`);
}

/**
 * Mark the current test as "expected to fail on the broken page".
 *
 * This is what makes a pitfall self-checking: if the reference test ever STOPS failing on
 * the broken page, it is no longer catching the bug and Playwright reports it as an
 * unexpected pass. SHOW_RED=1 turns the marker off so you can watch the real failure.
 */
export function expectBugOnBroken(reason) {
  test.fail(test.info().project.name === 'broken' && !process.env.SHOW_RED, reason);
}

/** True if the element, or anything above it, hides it from a sighted user. */
export const isHiddenFromSight = (el) => {
  for (let node = el; node; node = node.parentElement) {
    const s = getComputedStyle(node);
    if (s.display === 'none' || s.visibility === 'hidden' || Number(s.opacity) === 0) return true;
  }
  return false;
};
