import AxeBuilder from '@axe-core/playwright';
import { expect, test } from '@playwright/test';
import { expectBugOnBroken, openPitfall } from '../../../fixtures.js';

const PITFALL = 'catch-it/silent-error';

async function submitEmptyForm(page) {
  await openPitfall(page, PITFALL);
  await page.getByRole('button', { name: 'Log in' }).click();
}

test('the error is exposed as an alert so it is announced', async ({ page }) => {
  expectBugOnBroken('the error is a plain <div>: a screen reader user hears nothing');
  await submitEmptyForm(page);

  const alert = page.getByRole('alert');
  await expect(alert).toBeVisible();
  await expect(alert).toHaveText('Incorrect email or password');
});

test('focus is not dropped on <body> after the failed submit', async ({ page }) => {
  expectBugOnBroken('the submit button is disabled mid-request, so focus falls back to <body>');
  await submitEmptyForm(page);
  await page.getByText('Incorrect email or password').waitFor();

  const tag = await page.evaluate(() => document.activeElement.tagName);
  expect(tag).not.toBe('BODY');
});

test('a default axe scan does not see the problem - that is the lesson', async ({ page }) => {
  // The message has good colour contrast and the page is structurally fine. Whether a
  // message is ANNOUNCED depends on how it was inserted, not on how it looks.
  await submitEmptyForm(page);
  await page.getByText('Incorrect email or password').waitFor();
  expect((await new AxeBuilder({ page }).analyze()).violations).toEqual([]);
});
