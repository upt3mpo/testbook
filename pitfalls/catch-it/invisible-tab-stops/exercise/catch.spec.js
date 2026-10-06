// YOUR TURN. Write a test that FAILS on the broken page and PASSES on the fixed page.
//
// Run it:   npm run exercise -- catch-it/invisible-tab-stops
// Hints are in ../exercise.md - try without them first.
import { expect, test } from '@playwright/test';
import { openPitfall } from '../../../fixtures.js';

test.fixme('catches the invisible Tab stops', async ({ page }) => {
  await openPitfall(page, 'catch-it/invisible-tab-stops');

  // TODO: press Tab through the page and decide, at each stop, whether a person
  // looking at the screen could see the control that has focus.

  expect(true).toBe(false); // replace with a real assertion, then remove test.fixme above
});
