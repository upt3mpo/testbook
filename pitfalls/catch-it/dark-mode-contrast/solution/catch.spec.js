import AxeBuilder from '@axe-core/playwright';
import { expect, test } from '@playwright/test';
import { expectBugOnBroken, openPitfall } from '../../../fixtures.js';

const PITFALL = 'catch-it/dark-mode-contrast';

const contrastViolations = (page) =>
  new AxeBuilder({ page })
    .withRules(['color-contrast'])
    .analyze()
    .then((r) => r.violations);

test('the default (light) theme passes - which is why the suite looked green', async ({ page }) => {
  // Same result on BOTH pages: the bug only exists in a state nobody scanned.
  await openPitfall(page, PITFALL);
  expect(await contrastViolations(page)).toEqual([]);
});

test('the dark theme passes too', async ({ page }) => {
  expectBugOnBroken('white text on the dark accent colour is 3.45:1; 4.5:1 is required');
  await openPitfall(page, PITFALL);

  // Reach the state first, THEN scan it. Every theme, mode or preference a user can switch
  // is another state to test.
  await page.getByRole('button', { name: 'Dark theme' }).click();
  await expect(page.locator('html')).toHaveAttribute('data-theme', 'dark');

  expect(await contrastViolations(page)).toEqual([]);
});
