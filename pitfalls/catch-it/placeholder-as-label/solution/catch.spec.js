import AxeBuilder from '@axe-core/playwright';
import { expect, test } from '@playwright/test';
import { expectBugOnBroken, openPitfall } from '../../../fixtures.js';

const PITFALL = 'catch-it/placeholder-as-label';

test('each field can be found by its label', async ({ page }) => {
  expectBugOnBroken('the fields have a placeholder but no label, so getByLabel finds nothing');
  await openPitfall(page, PITFALL);

  // getByLabel only works when a real <label> (or aria-label) names the field. A test that
  // finds the field by placeholder or test id would keep passing on the broken page.
  await expect(page.getByLabel('Email')).toBeVisible();
  await expect(page.getByLabel('Password')).toBeVisible();
});

test('the label is still visible after the user has typed', async ({ page }) => {
  expectBugOnBroken('the only cue is the placeholder, which vanishes as soon as you type');
  await openPitfall(page, PITFALL);

  await page.locator('input[type=email]').fill('sarah@example.com');
  await expect(page.getByText('Email', { exact: true })).toBeVisible();
});

test('a default axe scan does not see the problem - that is the lesson', async ({ page }) => {
  // axe accepts a non-empty placeholder as an accessible name, so its `label` rule is
  // satisfied. The expectation of a persistent label (WCAG 3.3.2, and good practice) is
  // stronger than what a tool can check.
  await openPitfall(page, PITFALL);
  expect((await new AxeBuilder({ page }).analyze()).violations).toEqual([]);
});
