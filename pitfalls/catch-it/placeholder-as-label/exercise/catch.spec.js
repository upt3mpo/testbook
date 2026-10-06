// YOUR TURN. Write a test that FAILS on the broken page and PASSES on the fixed page.
//
// Run it:   npm run exercise -- catch-it/placeholder-as-label
// Hints are in ../exercise.md - try without them first.
import { expect, test } from '@playwright/test';
import { openPitfall } from '../../../fixtures.js';

test.fixme('catches the placeholder-only fields', async ({ page }) => {
  await openPitfall(page, 'catch-it/placeholder-as-label');

  // TODO: find each field the way a screen reader user would meet it.

  expect(true).toBe(false); // replace with a real assertion, then remove test.fixme above
});
