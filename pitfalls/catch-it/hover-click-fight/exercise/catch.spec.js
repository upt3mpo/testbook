// YOUR TURN. Write a test that FAILS on the broken page and PASSES on the fixed page.
//
// Run it:   npm run exercise -- catch-it/hover-click-fight
// Hints are in ../exercise.md - try without them first.
import { expect, test } from '@playwright/test';
import { openPitfall } from '../../../fixtures.js';

test.fixme('catches the hover/click fight', async ({ page }) => {
  await openPitfall(page, 'catch-it/hover-click-fight');

  // TODO: open the picker the way a real mouse user does, then check that what the
  // screen shows and what assistive technology is told (aria-expanded) agree.

  expect(true).toBe(false); // replace with a real assertion, then remove test.fixme above
});
