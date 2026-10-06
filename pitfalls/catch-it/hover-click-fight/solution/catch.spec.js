import AxeBuilder from '@axe-core/playwright';
import { expect, test } from '@playwright/test';
import { expectBugOnBroken, openPitfall } from '../../../fixtures.js';

const PITFALL = 'catch-it/hover-click-fight';

test('a real mouse click opens the picker and aria-expanded agrees', async ({ page }) => {
  expectBugOnBroken('hover opens, the click then closes it: shown on screen but aria-expanded=false');
  await openPitfall(page, PITFALL);

  // Playwright's click() moves the pointer onto the button first (hover), then clicks,
  // exactly like a real mouse.
  const react = page.getByRole('button', { name: 'React' });
  await react.click();

  await expect(react).toHaveAttribute('aria-expanded', 'true');
  await expect(page.getByRole('button', { name: 'Like' })).toBeVisible();
});

test('moving the pointer away does not close a picker opened by keyboard', async ({ page }) => {
  expectBugOnBroken('mouseleave writes the same state, so it closes the keyboard-opened picker');
  await openPitfall(page, PITFALL);

  const react = page.getByRole('button', { name: 'React' });
  await react.focus();
  await page.keyboard.press('Enter');
  await expect(react).toHaveAttribute('aria-expanded', 'true');

  // A pointer wanders over the page and away again.
  await page.mouse.move(0, 0);
  await react.hover();
  await page.mouse.move(0, 0);

  await expect(react).toHaveAttribute('aria-expanded', 'true');
});

test('a default axe scan does not see the problem - that is the lesson', async ({ page }) => {
  // Every static snapshot is internally consistent. The bug only exists in the transition
  // between two inputs, which no single-snapshot scan visits.
  await openPitfall(page, PITFALL);
  expect((await new AxeBuilder({ page }).analyze()).violations).toEqual([]);
});
