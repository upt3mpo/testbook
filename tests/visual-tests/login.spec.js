import { test, expect } from "@playwright/test";

import { AuthPage } from "../e2e/pages/AuthPage.js";
import { resetDatabase } from "../e2e/fixtures/test-helpers.js";

/**
 * Visual regression baseline for the login page.
 *
 * The simplest of the three surfaces this pass covers: no user data,
 * no timestamps, no avatars - a static form. That makes it the best
 * one to start with if a baseline update ever needs sanity-checking,
 * since almost nothing here should ever legitimately change.
 */
test.describe("Login page visual regression", () => {
  test("matches baseline", async ({ page }) => {
    const auth = new AuthPage(page);

    // Not logged in, so nothing user-specific to reset, but a clean
    // slate keeps this test independent of whatever ran before it.
    await resetDatabase(page);

    await auth.gotoLogin();
    await expect(auth.loginEmailInput).toBeVisible();
    await expect(auth.loginPasswordInput).toBeVisible();
    await expect(auth.loginSubmitButton).toBeVisible();

    await expect(page).toHaveScreenshot("login-page.png", {
      fullPage: true,
    });
  });
});
