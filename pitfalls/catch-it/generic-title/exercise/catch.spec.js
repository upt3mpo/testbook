// YOUR TURN. Write a test that FAILS on the broken page and PASSES on the fixed page.
//
// Run it:   npm run exercise -- catch-it/generic-title
// Hints are in ../exercise.md - try without them first.
import { expect, test } from '@playwright/test';
import { openPitfall } from '../../../fixtures.js';

test.fixme('catches the generic title', async ({ page }) => {
  await openPitfall(page, 'catch-it/generic-title');
  await page.getByRole('link', { name: 'Settings' }).click();

  // TODO: the content changed. What else should have changed with it?

  expect(true).toBe(false); // replace with a real assertion, then remove test.fixme above
});
