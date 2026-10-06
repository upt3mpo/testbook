/**
 * Shared accessibility test helpers.
 *
 * One place owns the axe tag list and the "scan + attach the report" logic, so
 * individual tests stay one line long and nobody narrows the tags by accident.
 */

import AxeBuilder from '@axe-core/playwright';
import { expect } from '@playwright/test';

/**
 * Target standard: WCAG 2.2 Level AA, plus axe's best-practice rules.
 *
 * Do NOT drop 'best-practice'. landmark-one-main, region, page-has-heading-one,
 * heading-order and several others carry no WCAG tag, so a WCAG-only list
 * passes while real structural bugs ship. Do not drop 'wcag22aa' either: it is
 * where target-size (2.5.8) lives.
 */
export const AXE_TAGS = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa', 'best-practice'];

/**
 * Scan the current page state with axe and fail on any violation.
 *
 * On failure the full axe result is attached to the Playwright report as JSON,
 * and the assertion message lists each rule, impact, and first offending node,
 * so the failure is actionable without opening the report.
 *
 * @param {import('@playwright/test').Page} page
 * @param {import('@playwright/test').TestInfo} testInfo
 * @param {{ name?: string, include?: string, exclude?: string[] }} [options]
 */
export async function expectNoA11yViolations(page, testInfo, options = {}) {
  const { name = 'axe', include, exclude = [] } = options;

  let builder = new AxeBuilder({ page }).withTags(AXE_TAGS);
  if (include) builder = builder.include(include);
  for (const selector of exclude) builder = builder.exclude(selector);

  const results = await builder.analyze();

  if (results.violations.length > 0) {
    await testInfo.attach(`${name}-violations.json`, {
      body: JSON.stringify(results.violations, null, 2),
      contentType: 'application/json',
    });
  }

  const summary = results.violations.map(
    (v) => `${v.id} [${v.impact}] x${v.nodes.length} - ${v.help}\n    ${v.nodes[0].target.join(' ')}`
  );
  expect(results.violations, `${name}:\n  ${summary.join('\n  ')}`).toEqual([]);
}

/**
 * Press the key that moves keyboard focus to the next control, in whichever engine is running.
 *
 * Browsers disagree about what Tab does. Chromium and Firefox move focus through every
 * interactive element. Safari (WebKit) by default only tabs through form fields, and needs Option
 * (Alt) held to include links and buttons, unless the user has turned on "Press Tab to highlight
 * each item on a webpage". A test that hard-codes "Tab" therefore fails on WebKit even though the
 * app is fine. Use this helper in any test that tabs through links and buttons.
 *
 * @param {import('@playwright/test').Page} page
 */
export async function pressTab(page) {
  const engine = page.context().browser()?.browserType().name();
  await page.keyboard.press(engine === 'webkit' ? 'Alt+Tab' : 'Tab');
}
