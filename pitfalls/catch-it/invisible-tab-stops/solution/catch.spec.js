import AxeBuilder from '@axe-core/playwright';
import { expect, test } from '@playwright/test';
import { expectBugOnBroken, isHiddenFromSight, openPitfall } from '../../../fixtures.js';

const PITFALL = 'catch-it/invisible-tab-stops';

test('no Tab stop lands on a control the user cannot see', async ({ page }) => {
  expectBugOnBroken('the closed picker leaves 3 invisible controls in the Tab order');
  await openPitfall(page, PITFALL);

  // Press Tab through the whole page, noting every stop that a sighted user could not see.
  const invisibleStops = [];
  for (let i = 0; i < 8; i++) {
    await page.keyboard.press('Tab');
    const stop = await page.evaluate((fn) => {
      const el = document.activeElement;
      return {
        label: el.getAttribute('aria-label') || el.textContent.trim(),
        hidden: new Function(`return (${fn})`)()(el),
      };
    }, isHiddenFromSight.toString());
    if (stop.hidden) invisibleStops.push(stop.label);
  }

  expect(invisibleStops).toEqual([]);
});

test('a default axe scan does not see the problem - that is the lesson', async ({ page }) => {
  // Same result on BOTH pages: axe inspects one snapshot of the DOM, and a transparent
  // control is not a rule violation. Only pressing Tab and watching focus reveals this bug.
  await openPitfall(page, PITFALL);
  const results = await new AxeBuilder({ page }).analyze();
  expect(results.violations).toEqual([]);
});
