// YOUR TURN. Write a test that FAILS on the broken page and PASSES on the fixed page.
//
// Run it:   npm run exercise -- catch-it/dark-mode-contrast
// Hints are in ../exercise.md - try without them first.
import { expect, test } from '@playwright/test';
import { openPitfall } from '../../../fixtures.js';

test.fixme('catches the dark-mode contrast failure', async ({ page }) => {
  await openPitfall(page, 'catch-it/dark-mode-contrast');

  // TODO: a default scan of this page is green. What state have you not looked at yet?

  expect(true).toBe(false); // replace with a real assertion, then remove test.fixme above
});
