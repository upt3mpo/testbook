/**
 * E2E tests for authentication flows.
 *
 * This file demonstrates comprehensive end-to-end testing of user authentication
 * flows using Playwright for JavaScript. These tests simulate real user interactions
 * with the browser to verify complete user journeys.
 *
 * Key Testing Concepts Demonstrated:
 * - End-to-end user workflow testing (registration, login, logout)
 * - Browser automation with Playwright
 * - Real user interaction simulation (clicking, typing, navigation)
 * - Cross-page testing (registration → login → feed)
 * - Error handling and edge case testing
 * - Visual verification of UI elements
 * - Async operation handling (waiting for elements, navigation)
 * - Test organization with describe blocks and helper functions
 *
 * This file is referenced in Stage 3 learning materials as an example
 * of professional E2E testing practices.
 *
 * Page Object Model: interactions go through pages/AuthPage.js rather
 * than raw selectors, so a UI change only needs updating in one place.
 */

import { expect, test } from "@playwright/test";
import { resetDatabase, setupDialogHandler, TEST_USERS } from "./fixtures/test-helpers.js";
import { AuthPage } from "./pages/AuthPage.js";

test.describe("Authentication", () => {
  /**
   * Setup for each test to ensure clean state.
   *
   * This beforeEach hook runs before each test to:
   * 1. Handle browser dialogs (alerts, confirms)
   * 2. Reset the database to a clean state
   *
   * This ensures each test starts with a known, clean state
   * and doesn't interfere with other tests.
   */
  test.beforeEach(async ({ page }) => {
    // Auto-accept all browser dialogs (confirm/alert)
    setupDialogHandler(page);

    await resetDatabase(page);
  });

  test.describe("Registration", () => {
    test("should register new user successfully", async ({ page }) => {
      /**
       * Test complete user registration workflow.
       *
       * This test verifies the entire user registration journey:
       * 1. User navigates to registration page
       * 2. User fills out registration form
       * 3. User submits form
       * 4. System processes registration
       * 5. User is automatically logged in
       * 6. User is redirected to feed page
       * 7. User sees their profile in navigation
       *
       * This is a critical E2E test that ensures the complete
       * registration flow works from the user's perspective.
       */

      const auth = new AuthPage(page);
      await auth.gotoRegister();

      const newUser = {
        email: "testuser@example.com",
        username: "testuser",
        displayName: "Test User",
        password: "TestPassword123!",
      };

      await auth.register(newUser);
      await auth.expectLoggedIn(newUser.displayName);
    });

    test("should show error for duplicate email", async ({ page }) => {
      const auth = new AuthPage(page);
      await auth.gotoRegister();

      // Try to register with existing email
      await auth.register({
        email: TEST_USERS.sarah.email,
        username: "differentuser",
        displayName: "Different User",
        password: "Password123!",
      });

      await expect(page.locator("text=/email.*already/i")).toBeVisible({
        timeout: 5000,
      });
    });

    test("should show error for duplicate username", async ({ page }) => {
      const auth = new AuthPage(page);
      await auth.gotoRegister();

      // Try to register with existing username
      await auth.register({
        email: "newemail@example.com",
        username: TEST_USERS.sarah.username,
        displayName: "Different User",
        password: "Password123!",
      });

      await expect(page.locator("text=/username.*already/i")).toBeVisible({
        timeout: 5000,
      });
    });

    test("should validate email format", async ({ page }) => {
      const auth = new AuthPage(page);
      await auth.gotoRegister();

      await auth.registerEmailInput.fill("notanemail");
      await auth.registerUsernameInput.fill("testuser");
      await auth.registerDisplayNameInput.fill("Test User");
      await auth.registerPasswordInput.fill("Password123!");

      // Should show HTML5 validation or custom error
      expect(await auth.isRegisterEmailInvalid()).toBeTruthy();
    });
  });

  test.describe("Login", () => {
    test("should login with correct credentials", async ({ page }) => {
      const auth = new AuthPage(page);
      await auth.gotoLogin();
      await auth.login(TEST_USERS.sarah.email, TEST_USERS.sarah.password);

      await auth.expectLoggedIn(TEST_USERS.sarah.displayName);
    });

    test("should show error for wrong password", async ({ page }) => {
      const auth = new AuthPage(page);
      await auth.gotoLogin();
      await auth.login(TEST_USERS.sarah.email, "WrongPassword123!");

      // Backend returns "Incorrect email or password"
      await auth.expectLoginError(/incorrect|invalid/i);
    });

    test("should show error for non-existent user", async ({ page }) => {
      const auth = new AuthPage(page);
      await auth.gotoLogin();
      await auth.login("nonexistent@example.com", "Password123!");

      // Backend returns "Incorrect email or password"
      await auth.expectLoginError(/incorrect|invalid/i);
    });

    test("should persist login across page refreshes", async ({ page }) => {
      const auth = new AuthPage(page);
      await auth.gotoLogin();
      await auth.login(TEST_USERS.sarah.email, TEST_USERS.sarah.password);
      await auth.expectLoggedIn(TEST_USERS.sarah.displayName);

      await page.reload();

      // Should still be logged in
      await auth.expectLoggedIn(TEST_USERS.sarah.displayName);
    });
  });

  test.describe("Logout", () => {
    test("should logout successfully", async ({ page }) => {
      const auth = new AuthPage(page);
      await auth.gotoLogin();
      await auth.login(TEST_USERS.sarah.email, TEST_USERS.sarah.password);

      await auth.logout();

      await auth.expectLoggedOut();
    });

    test("should not access protected routes after logout", async ({
      page,
      context,
    }) => {
      const auth = new AuthPage(page);
      await auth.gotoLogin();
      await auth.login(TEST_USERS.sarah.email, TEST_USERS.sarah.password);

      await auth.logout();

      // Try to access protected route
      await auth.goto("/settings");

      await auth.expectOnLoginPage();
    });
  });

  test.describe("Protected Routes", () => {
    test("should redirect to login when accessing feed without auth", async ({
      page,
    }) => {
      const auth = new AuthPage(page);
      await auth.goto("/");

      await auth.expectOnLoginPage();
    });

    test("should redirect to login when accessing settings without auth", async ({
      page,
    }) => {
      const auth = new AuthPage(page);
      await auth.goto("/settings");

      await auth.expectOnLoginPage();
    });

    test("should redirect to login when accessing profile without auth", async ({
      page,
    }) => {
      const auth = new AuthPage(page);
      await auth.goto(`/profile/${TEST_USERS.sarah.username}`);

      await auth.expectOnLoginPage();
    });
  });

  test.describe("Auto-login on Registration", () => {
    test("should automatically login after successful registration", async ({
      page,
    }) => {
      const auth = new AuthPage(page);
      await auth.gotoRegister();

      const newUser = {
        email: "autouser@example.com",
        username: "autouser",
        displayName: "Auto User",
        password: "AutoPass123!",
      };

      await auth.register(newUser);

      // Should be logged in without manual login
      await expect(auth.navbar).toBeVisible();

      // Should be able to access protected routes
      await auth.navbarSettingsLink.click();
      await expect(page.getByTestId("settings-email")).toContainText(newUser.email);
    });
  });
});

// 🧠 Why These Tests Matter:
//
// E2E tests for authentication are CRITICAL because they test the REAL user experience:
//
// 1. **Complete User Journey** - Tests full registration/login flow in actual browser
// 2. **Frontend + Backend Integration** - Verifies React UI and FastAPI backend work together
// 3. **Visual Validation** - Tests what users actually see (error messages, redirects, UI state)
// 4. **Cross-Browser Compatibility** - Playwright tests work on Chrome, Firefox, Safari
//
// What These Tests Catch:
// - ✅ Broken registration form (fields don't submit)
// - ✅ Login redirects to wrong page
// - ✅ Error messages don't appear in UI
// - ✅ Session state issues (user appears logged out after login)
// - ✅ Navigation bugs (protected routes accessible without auth)
//
// In Real QA Teams:
// - E2E tests are the "smoke tests" run before every release
// - They catch integration bugs that unit/component tests miss
// - Failed E2E auth tests are deployment blockers
// - They verify the most critical user path (can't use app if can't log in!)
//
// For Your Career:
// - E2E testing is THE most in-demand QA skill
// - Playwright is industry-leading tool (used by Microsoft, Google, etc.)
// - Shows you can test complete workflows, not just individual pieces
// - Interview question: "How would you test user registration?" - Show this test running!
// - Demonstrates understanding of async operations, waits, and selectors
