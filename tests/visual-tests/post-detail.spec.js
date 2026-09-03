import { test, expect } from "@playwright/test";

import { AuthPage } from "../e2e/pages/AuthPage.js";
import { FeedPage } from "../e2e/pages/FeedPage.js";
import { resetDatabase, TEST_USERS } from "../e2e/fixtures/test-helpers.js";

/**
 * Visual regression baseline for a single post's detail view.
 *
 * Navigates there the way a real user would - log in, land on the
 * feed, click into the first seeded post - rather than hardcoding a
 * post ID. Seeded post IDs are assigned by autoincrement during
 * seed.py's run and aren't guaranteed stable across every database
 * backend/reset cycle; following the same link a user would click
 * avoids depending on that.
 */
test.describe("Post detail page visual regression", () => {
  test("matches baseline: content, reactions, and comment count", async ({
    page,
  }) => {
    await resetDatabase(page);

    const auth = new AuthPage(page);
    await auth.gotoLogin();
    await auth.login(TEST_USERS.sarah.email, TEST_USERS.sarah.password);
    await auth.expectLoggedIn(TEST_USERS.sarah.displayName);

    const feed = new FeedPage(page);
    await feed.goto();
    const post = feed.firstPost();
    await expect(post).toBeVisible();
    await post.locator('[data-testid$="-view-button"]').click();

    await expect(page.getByTestId("post-detail-page")).toBeVisible();
    await expect(page.getByTestId("reactions-section")).toBeVisible();
    await expect(page.getByTestId("comments-section")).toBeVisible();

    await expect(page).toHaveScreenshot("post-detail-page.png", {
      fullPage: true,
      // Same reasoning as feed.spec.js: the post's own timestamp and
      // any comment timestamps are absolute, locale/timezone-dependent
      // strings, not stable pixels.
      mask: [page.locator('[data-testid$="-time"]')],
    });
  });
});
