import AxeBuilder from '@axe-core/playwright';
import { expect, test } from '@playwright/test';
import { expectBugOnBroken, openPitfall } from '../../../fixtures.js';

const PITFALL = 'catch-it/nested-interactive';

test('one control is one Tab stop', async ({ page }) => {
  expectBugOnBroken('the View button sits inside the View link, so Tab stops twice');
  await openPitfall(page, PITFALL);

  // Tab once through the page (Comment, then View) and record what each stop is. Three presses
  // is enough to see every stop without wrapping round to the start again.
  const stops = [];
  for (let i = 0; i < 3; i++) {
    await page.keyboard.press('Tab');
    stops.push(await page.evaluate(() => document.activeElement.textContent.trim()));
  }

  expect(stops.filter((name) => name === 'View')).toHaveLength(1);
});

test('activating the control once opens it once', async ({ page }) => {
  expectBugOnBroken('a link and a button are both focusable, so there are two things to activate');
  await openPitfall(page, PITFALL);

  const views = page.getByRole('link', { name: 'View' });
  const buttons = page.getByRole('button', { name: 'View' });
  // Exactly one thing named "View" can be activated, and it is the link.
  expect(await views.count()).toBe(1);
  expect(await buttons.count()).toBe(0);
});

test('a default axe scan does not see the problem - that is the lesson', async ({ page }) => {
  // A button inside a link is invalid HTML, but axe has no rule that flags this particular
  // nesting. Every control has a name and a role, so every snapshot check passes.
  await openPitfall(page, PITFALL);
  expect((await new AxeBuilder({ page }).analyze()).violations).toEqual([]);
});
