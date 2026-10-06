// YOUR TURN. The suspect test is green on a page where the menu button's only name is a symbol.
// 1. Prove it: what could you remove from the page and the test would still pass?
// 2. Write a version you CAN trust: it must fail on the broken page and pass on the fixed one.
//
// Run it:   npm run exercise -- trust-it/test-id-hides-bug
// Hints are in ../exercise.md - try without them first.
import { expect, test } from '@playwright/test';
import { openPitfall } from '../../../fixtures.js';

test.fixme('a trustworthy post-menu test', async ({ page }) => {
  await openPitfall(page, 'trust-it/test-id-hides-bug');

  // TODO: find the button the way a user would, not the way a developer labelled it.

  expect(true).toBe(false); // replace with a real assertion, then remove test.fixme above
});
