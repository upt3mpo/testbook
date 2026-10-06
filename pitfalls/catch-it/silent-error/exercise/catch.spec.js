// YOUR TURN. Write a test that FAILS on the broken page and PASSES on the fixed page.
//
// Run it:   npm run exercise -- catch-it/silent-error
// Hints are in ../exercise.md - try without them first.
import { expect, test } from '@playwright/test';
import { openPitfall } from '../../../fixtures.js';

test.fixme('catches the silent error', async ({ page }) => {
  await openPitfall(page, 'catch-it/silent-error');
  await page.getByRole('button', { name: 'Log in' }).click();

  // TODO: a sighted user sees the message appear. What would a screen reader user get,
  // and where is keyboard focus afterwards?

  expect(true).toBe(false); // replace with a real assertion, then remove test.fixme above
});
