// THE TEST UNDER SUSPICION. It is green on BOTH pages, including the one where Escape does
// not work at all. Should you trust it? (Run it, then read ../README.md.)
import { expect, test } from '@playwright/test';
import { openPitfall } from '../../../fixtures.js';

test('Escape closes the menu', async ({ page }) => {
  await openPitfall(page, 'trust-it/vacuous-escape-test');

  await page.getByRole('button', { name: 'Menu' }).click();
  await page.keyboard.press('Escape');

  await expect(page.locator('#menu')).toBeHidden();
});
