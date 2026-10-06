// YOUR TURN. The suspect test is green on a page where Escape does nothing.
// 1. Prove it: which line of the page can you delete and the test still passes?
// 2. Write a version that you CAN trust: it must fail on the broken page and pass on the
//    fixed page.
//
// Run it:   npm run exercise -- trust-it/vacuous-escape-test
// Hints are in ../exercise.md - try without them first.
import { expect, test } from '@playwright/test';
import { openPitfall } from '../../../fixtures.js';

test.fixme('a trustworthy Escape test', async ({ page }) => {
  await openPitfall(page, 'trust-it/vacuous-escape-test');

  // TODO: make sure the menu is really open before you press Escape.

  expect(true).toBe(false); // replace with a real assertion, then remove test.fixme above
});
