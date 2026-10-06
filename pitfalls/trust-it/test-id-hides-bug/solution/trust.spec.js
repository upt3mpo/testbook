import AxeBuilder from '@axe-core/playwright';
import { expect, test } from '@playwright/test';
import { expectBugOnBroken, openPitfall } from '../../../fixtures.js';

const PITFALL = 'trust-it/test-id-hides-bug';

test('the post menu opens, found the way a user finds it', async ({ page }) => {
  expectBugOnBroken('the only name is a symbol, so a query by the real name finds nothing');
  await openPitfall(page, PITFALL);

  // Find controls by role and name, as a screen reader user (and Playwright's own
  // guidance) would. A test id is invisible to users, so it can never notice a missing name.
  const menuButton = page.getByRole('button', { name: 'Post options' });
  // Assert it exists first: click() would otherwise wait out the whole test timeout.
  await expect(menuButton).toBeVisible();
  await menuButton.click();

  await expect(page.locator('#menu')).toBeVisible();
});

test('a default axe scan does not see the problem either - that is the lesson', async ({ page }) => {
  // The ellipsis glyph counts as text, so axe's button-name rule is satisfied: the button
  // "has a name". It is just a useless one. Whether a name is MEANINGFUL is a human call,
  // and a test id (which users never see) cannot make that call either.
  await openPitfall(page, PITFALL);

  expect((await new AxeBuilder({ page }).analyze()).violations).toEqual([]);
});
