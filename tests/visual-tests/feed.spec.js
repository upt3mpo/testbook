import { test, expect } from "@playwright/test";

import { AuthPage } from "../e2e/pages/AuthPage.js";
import { FeedPage } from "../e2e/pages/FeedPage.js";
import { resetDatabase, TEST_USERS } from "../e2e/fixtures/test-helpers.js";

/**
 * Visual regression baseline for the feed page, logged in.
 *
 * Uses the default seed data (backend/seed.py) rather than creating
 * posts inline, so the baseline reflects real, varied content: posts
 * with and without images, different post lengths, reaction counts.
 * resetDatabase() before the test guarantees that's the exact same
 * seed data every run, not whatever a previous test happened to leave
 * behind.
 */
test.describe("Feed page visual regression", () => {
  test("matches baseline, logged in with seeded posts", async ({ page }) => {
    await resetDatabase(page);

    const auth = new AuthPage(page);
    await auth.gotoLogin();
    await auth.login(TEST_USERS.sarah.email, TEST_USERS.sarah.password);
    await auth.expectLoggedIn(TEST_USERS.sarah.displayName);

    const feed = new FeedPage(page);
    await feed.goto();
    await expect(feed.firstPost()).toBeVisible();
    // Wait for at least the seeded post count so the screenshot isn't
    // taken mid-render with only some posts loaded in.
    await expect
      .poll(() => feed.postCount(), { timeout: 10000 })
      .toBeGreaterThan(0);

    await expect(page).toHaveScreenshot("feed-page.png", {
      fullPage: true,
      // Post.jsx renders each post's timestamp with
      // new Date(post.created_at).toLocaleString() - an absolute
      // date/time string that depends on the browser's locale and
      // timezone (which can legitimately differ between a local
      // machine and the CI runner) and on the actual calendar date the
      // database was seeded, not just a fixed relative offset. Masking
      // it keeps the comparison meaningful for everything that should
      // actually stay pixel-stable (layout, avatars, content, reaction
      // counts) instead of failing on a detail neither environment
      // controls.
      mask: [page.locator('[data-testid$="-time"]')],
    });
  });
});
