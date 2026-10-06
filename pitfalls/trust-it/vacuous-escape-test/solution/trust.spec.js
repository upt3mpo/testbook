import { expect, test } from '@playwright/test';
import { expectBugOnBroken, openPitfall } from '../../../fixtures.js';

test('Escape closes a menu that is open - and the test proves it was open first', async ({ page }) => {
  expectBugOnBroken('Escape does nothing on this page; a trustworthy test must notice');
  await openPitfall(page, 'trust-it/vacuous-escape-test');

  // Open the menu by KEYBOARD. A mouse click hovers first, and on this page hover and
  // click both write the same state, so click() opens-then-closes the menu and the old
  // test never gave Escape anything to close.
  const menu = page.getByRole('button', { name: 'Menu' });
  await menu.focus();
  await page.keyboard.press('Enter');

  // Precondition: assert the menu is really open BEFORE pressing Escape. Without this line
  // the test can pass without ever exercising the feature.
  await expect(page.locator('#menu')).toBeVisible();

  await page.keyboard.press('Escape');
  await expect(page.locator('#menu')).toBeHidden();
});
