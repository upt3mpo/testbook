// THE TEST UNDER SUSPICION. Green on BOTH pages, including the one where the menu button's only
// name is a symbol. Should you trust it? (Run it, then read ../README.md.)
import { expect, test } from '@playwright/test';
import { openPitfall } from '../../../fixtures.js';

test('the post menu opens', async ({ page }) => {
  await openPitfall(page, 'trust-it/test-id-hides-bug');

  await page.getByTestId('post-menu').click();

  await expect(page.locator('#menu')).toBeVisible();
});
