/**
 * Accessibility Tests with Playwright + axe-core
 *
 * These tests use axe-playwright to perform comprehensive WCAG 2.1 accessibility checks
 * on key pages in the application.
 *
 * Run with: npx playwright test accessibility-axe.spec.js
 */

import AxeBuilder from '@axe-core/playwright';
import { expect, test } from '@playwright/test';

const BASE_URL = process.env.BASE_URL || 'http://localhost:3000';

test.describe('Accessibility (axe-core)', () => {
  test.beforeEach(async ({ page }) => {
    // Ensure app is running
    await page.goto(BASE_URL);
  });

  test('Home page should not have accessibility violations', async ({ page }) => {
    await page.goto(BASE_URL);
    await page.waitForLoadState('networkidle');

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze();

    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test('Register page should not have accessibility violations', async ({ page }) => {
    await page.goto(`${BASE_URL}/register`);
    await page.waitForLoadState('networkidle');

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze();

    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test('Login page should not have accessibility violations', async ({ page }) => {
    await page.goto(`${BASE_URL}/login`);
    await page.waitForLoadState('networkidle');

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze();

    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test('Feed page (authenticated) should not have accessibility violations', async ({
    page,
  }) => {
    // Login first
    await page.goto(`${BASE_URL}/login`);
    await page.fill('input[type="email"]', 'testuser@example.com');
    await page.fill('input[type="password"]', 'TestPassword123!');
    await page.click('button[type="submit"]');
    await page.waitForURL('**/feed');
    await page.waitForLoadState('networkidle');

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze();

    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test('Profile page should not have accessibility violations', async ({ page }) => {
    // Login first
    await page.goto(`${BASE_URL}/login`);
    await page.fill('input[type="email"]', 'testuser@example.com');
    await page.fill('input[type="password"]', 'TestPassword123!');
    await page.click('button[type="submit"]');
    await page.waitForURL('**/feed');

    // Go to profile
    await page.click('a[href*="/profile"]');
    await page.waitForLoadState('networkidle');

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze();

    expect(accessibilityScanResults.violations).toEqual([]);
  });
});

/**
 * Why These Tests Matter
 *
 * **Accessibility is a Legal and Ethical Requirement:**
 * - WCAG 2.1 AA is the standard for ADA compliance
 * - Many countries require accessible web applications by law
 * - 15% of the population has some form of disability
 * - Inaccessible apps exclude users and risk lawsuits
 *
 * **What These Tests Catch:**
 * - Missing alt text on images
 * - Insufficient color contrast
 * - Missing ARIA labels
 * - Keyboard navigation issues
 * - Form labels and error associations
 * - Semantic HTML structure problems
 *
 * **How Real QA Teams Use These:**
 * - Run on every PR to catch accessibility regressions
 * - Include in CI/CD pipeline (prevent deployment of inaccessible code)
 * - Generate reports for compliance documentation
 * - Test with real assistive technologies (screen readers)
 * - Perform manual keyboard-only navigation testing
 *
 * **Career/Interview Value:**
 * - Accessibility testing is a specialized, high-demand skill
 * - Shows awareness of inclusive design
 * - Demonstrates knowledge of WCAG standards
 * - Many companies require accessibility expertise
 * - Can lead to specialized QA roles (Accessibility QA Engineer)
 *
 * **Interview Questions You Can Answer:**
 * Q: "How do you test for accessibility?"
 * A: "I use automated tools like axe-core to catch common WCAG violations,
 *     then perform manual testing with screen readers and keyboard-only
 *     navigation. For Testbook, I wrote Playwright tests with axe-core
 *     integration that check every key page for WCAG 2.1 AA compliance."
 *
 * Q: "What's the difference between automated and manual accessibility testing?"
 * A: "Automated tools like axe-core can catch ~40% of accessibility issues
 *     (missing alt text, color contrast, ARIA). Manual testing catches the
 *     other 60%: keyboard navigation flow, screen reader output, focus management,
 *     and context-dependent issues. Both are necessary."
 */

