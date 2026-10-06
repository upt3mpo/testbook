import AxeBuilder from '@axe-core/playwright';
import { expect, test } from '@playwright/test';
import { expectBugOnBroken, openPitfall } from '../../../fixtures.js';

const PITFALL = 'catch-it/generic-title';

test('each page has its own title', async ({ page }) => {
  expectBugOnBroken('the title never changes as you move between pages');
  await openPitfall(page, PITFALL);

  await page.getByRole('link', { name: 'Settings' }).click();
  await expect(page).toHaveTitle(/Settings/);

  await page.getByRole('link', { name: 'Profile' }).click();
  await expect(page).toHaveTitle(/Profile/);
});

test('moving to a new page is announced', async ({ page }) => {
  expectBugOnBroken('a single-page app gives no "new page" cue, and nothing announces it');
  await openPitfall(page, PITFALL);

  await page.getByRole('link', { name: 'Settings' }).click();

  // A polite status region that a screen reader reads out after each navigation.
  await expect(page.getByRole('status')).toContainText('Settings');
});

test('a default axe scan does not see the problem - that is the lesson', async ({ page }) => {
  // axe checks that a <title> EXISTS (rule document-title). It does not know the page is a
  // single-page app, or that the title should change as the content does.
  await openPitfall(page, PITFALL);
  expect((await new AxeBuilder({ page }).analyze()).violations).toEqual([]);

  await page.getByRole('link', { name: 'Settings' }).click();
  expect((await new AxeBuilder({ page }).analyze()).violations).toEqual([]);
});
