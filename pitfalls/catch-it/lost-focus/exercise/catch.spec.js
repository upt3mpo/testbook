// YOUR TURN. Write a test that FAILS on the broken page and PASSES on the fixed page.
//
// Run it:   npm run exercise -- catch-it/lost-focus
// Hints are in ../exercise.md - try without them first.
import { expect, test } from '@playwright/test';
import { openPitfall } from '../../../fixtures.js';

test.fixme('catches the lost focus', async ({ page }) => {
  await openPitfall(page, 'catch-it/lost-focus');

  // TODO: open the post menu and choose Edit with the keyboard. Where is focus afterwards?

  expect(true).toBe(false); // replace with a real assertion, then remove test.fixme above
});
