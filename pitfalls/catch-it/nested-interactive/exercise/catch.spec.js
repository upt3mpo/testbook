// YOUR TURN. Write a test that FAILS on the broken page and PASSES on the fixed page.
//
// Run it:   npm run exercise -- catch-it/nested-interactive
// Hints are in ../exercise.md - try without them first.
import { expect, test } from '@playwright/test';
import { openPitfall } from '../../../fixtures.js';

test.fixme('catches the nested interactive control', async ({ page }) => {
  await openPitfall(page, 'catch-it/nested-interactive');

  // TODO: a keyboard user meets this control by pressing Tab. How many times do they have
  // to press it to get past the "View" control?

  expect(true).toBe(false); // replace with a real assertion, then remove test.fixme above
});
