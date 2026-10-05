/**
 * Lighthouse CI puppeteer script: sign in before each audited URL.
 *
 * Lighthouse starts every run with a fresh, logged-out browser, and Testbook
 * redirects a logged-out visit to "/" straight to "/login". Without this script
 * the Feed, Profile, Post detail and Settings pages would all be audited as the
 * login page. Lighthouse CI runs this script before each URL; the session it
 * creates is kept because lighthouserc.js sets `disableStorageReset`.
 *
 * Uses the seeded test account. Run against a seeded database
 * (`curl -X POST http://localhost:8000/api/dev/reset`).
 */

const BASE_URL = process.env.BASE_URL || 'http://localhost:3000';
const EMAIL = process.env.LH_EMAIL || 'sarah.johnson@testbook.com';
const PASSWORD = process.env.LH_PASSWORD || 'Sarah2024!'; // pragma: allowlist secret

module.exports = async (browser, context) => {
  // Public pages need no session.
  if (!context.url.startsWith(BASE_URL) || /\/(login|register)$/.test(context.url)) {
    return;
  }

  const page = await browser.newPage();
  await page.goto(`${BASE_URL}/login`, { waitUntil: 'networkidle0' });
  await page.type('#login-email', EMAIL);
  await page.type('#login-password', PASSWORD);
  await Promise.all([page.waitForSelector('[data-testid="navbar"]'), page.click('button[type="submit"]')]);
  await page.close();
};
