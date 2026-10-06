import AxeBuilder from '@axe-core/playwright';
import { expect, test } from '@playwright/test';
import { expectBugOnBroken, openPitfall } from '../../../fixtures.js';

const PITFALL = 'catch-it/lost-focus';

/** Open the post menu and choose Edit using only the keyboard. */
async function chooseEdit(page) {
  await openPitfall(page, PITFALL);
  await page.getByRole('button', { name: 'Post options' }).focus();
  await page.keyboard.press('Enter');
  await page.getByRole('button', { name: 'Edit', exact: true }).focus();
  await page.keyboard.press('Enter');
}

test('choosing Edit moves focus into the editor', async ({ page }) => {
  expectBugOnBroken('the Edit button vanishes and focus falls back to <body>');
  await chooseEdit(page);

  await expect(page.getByLabel('Edit post')).toBeFocused();
});

test('Cancel returns focus to the control that opened the editor', async ({ page }) => {
  expectBugOnBroken('closing the editor drops focus on <body> again');
  await chooseEdit(page);

  await page.getByRole('button', { name: 'Cancel' }).focus();
  await page.keyboard.press('Enter');

  await expect(page.getByRole('button', { name: 'Post options' })).toBeFocused();
});

test('a default axe scan does not see the problem - that is the lesson', async ({ page }) => {
  // Focus is something that happens over time. A snapshot of the DOM has no "where did
  // focus go after that click?", so no snapshot rule can see this.
  await openPitfall(page, PITFALL);
  expect((await new AxeBuilder({ page }).analyze()).violations).toEqual([]);
});
