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
 */

import { expect, test } from "@playwright/test";
import {
  loginUser,
  registerUser,
  resetDatabase,
  setupDialogHandler,
  TEST_USERS,
} from "./fixtures/test-helpers.js";

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

      // Arrange - Prepare test user data
      const newUser = {
        email: "testuser@example.com",
        username: "testuser",
        displayName: "Test User",
        password: "TestPassword123!",
      };

      // Act - Register user through UI helper
      await registerUser(page, newUser);

      // Assert - Verify successful registration and auto-login
      await expect(page).toHaveURL("/"); // Redirected to feed
      await expect(page.locator('[data-testid="navbar"]')).toBeVisible(); // Logged in
      await expect(
        page.locator('[data-testid="navbar-username"]')
      ).toContainText(newUser.displayName); // Correct user
    });

    test("should show error for duplicate email", async ({ page }) => {
      await page.goto("/register");

      // Try to register with existing email
      await page.fill(
        '[data-testid="register-email-input"]',
        TEST_USERS.sarah.email
      );
      await page.fill(
        '[data-testid="register-username-input"]',
        "differentuser"
      );
      await page.fill(
        '[data-testid="register-displayname-input"]',
        "Different User"
      );
      await page.fill(
        '[data-testid="register-password-input"]',
        "Password123!"
      );
      await page.click('[data-testid="register-submit-button"]');

      // Should show error
      await expect(page.locator("text=/email.*already/i")).toBeVisible({
        timeout: 5000,
      });
    });

    test("should show error for duplicate username", async ({ page }) => {
      await page.goto("/register");

      // Try to register with existing username
      await page.fill(
        '[data-testid="register-email-input"]',
        "newemail@example.com"
      );
      await page.fill(
        '[data-testid="register-username-input"]',
        TEST_USERS.sarah.username
      );
      await page.fill(
        '[data-testid="register-displayname-input"]',
        "Different User"
      );
      await page.fill(
        '[data-testid="register-password-input"]',
        "Password123!"
      );
      await page.click('[data-testid="register-submit-button"]');

      // Should show error
      await expect(page.locator("text=/username.*already/i")).toBeVisible({
        timeout: 5000,
      });
    });

    test("should validate email format", async ({ page }) => {
      await page.goto("/register");

      await page.fill('[data-testid="register-email-input"]', "notanemail");
      await page.fill('[data-testid="register-username-input"]', "testuser");
      await page.fill(
        '[data-testid="register-displayname-input"]',
        "Test User"
      );
      await page.fill(
        '[data-testid="register-password-input"]',
        "Password123!"
      );

      // Should show HTML5 validation or custom error
      const emailInput = page.locator('[data-testid="register-email-input"]');
      const isInvalid = await emailInput.evaluate((el) => !el.validity.valid);
      expect(isInvalid).toBeTruthy();
    });
  });

  test.describe("Login", () => {
    test("should login with correct credentials", async ({ page }) => {
      await loginUser(page, TEST_USERS.sarah.email, TEST_USERS.sarah.password);

      // Should be on feed page
      await expect(page).toHaveURL("/");
      await expect(page.locator('[data-testid="navbar"]')).toBeVisible();
      await expect(
        page.locator('[data-testid="navbar-username"]')
      ).toContainText(TEST_USERS.sarah.displayName);
    });

    test("should show error for wrong password", async ({ page }) => {
      await page.goto("/");

      await page.fill(
        '[data-testid="login-email-input"]',
        TEST_USERS.sarah.email
      );
      await page.fill(
        '[data-testid="login-password-input"]',
        "WrongPassword123!"
      );
      await page.click('[data-testid="login-submit-button"]');

      // Should show error (backend returns "Incorrect email or password")
      await expect(page.locator('[data-testid="login-error"]')).toBeVisible({
        timeout: 5000,
      });
      await expect(page.locator('[data-testid="login-error"]')).toContainText(
        /incorrect|invalid/i
      );
    });

    test("should show error for non-existent user", async ({ page }) => {
      await page.goto("/");

      await page.fill(
        '[data-testid="login-email-input"]',
        "nonexistent@example.com"
      );
      await page.fill('[data-testid="login-password-input"]', "Password123!");
      await page.click('[data-testid="login-submit-button"]');

      // Should show error (backend returns "Incorrect email or password")
      await expect(page.locator('[data-testid="login-error"]')).toBeVisible({
        timeout: 5000,
      });
      await expect(page.locator('[data-testid="login-error"]')).toContainText(
        /incorrect|invalid/i
      );
    });

    test("should persist login across page refreshes", async ({ page }) => {
      await loginUser(page, TEST_USERS.sarah.email, TEST_USERS.sarah.password);

      // Reload page
      await page.reload();

      // Should still be logged in
      await expect(page.locator('[data-testid="navbar"]')).toBeVisible();
      await expect(
        page.locator('[data-testid="navbar-username"]')
      ).toContainText(TEST_USERS.sarah.displayName);
    });
  });

  test.describe("Logout", () => {
    test("should logout successfully", async ({ page }) => {
      await loginUser(page, TEST_USERS.sarah.email, TEST_USERS.sarah.password);

      // Click logout
      await page.click('[data-testid="navbar-logout-button"]');

      // Should be redirected to login page
      await expect(
        page.locator('[data-testid="login-email-input"]')
      ).toBeVisible();
      await expect(page.locator('[data-testid="navbar"]')).not.toBeVisible();
    });

    test("should not access protected routes after logout", async ({
      page,
      context,
    }) => {
      await loginUser(page, TEST_USERS.sarah.email, TEST_USERS.sarah.password);

      // Logout
      await page.click('[data-testid="navbar-logout-button"]');

      // Try to access protected route
      await page.goto("/settings");

      // Should be redirected to login
      await expect(
        page.locator('[data-testid="login-email-input"]')
      ).toBeVisible();
    });
  });

  test.describe("Protected Routes", () => {
    test("should redirect to login when accessing feed without auth", async ({
      page,
    }) => {
      await page.goto("/");

      // Should show login page
      await expect(
        page.locator('[data-testid="login-email-input"]')
      ).toBeVisible();
    });

    test("should redirect to login when accessing settings without auth", async ({
      page,
    }) => {
      await page.goto("/settings");

      // Should show login page
      await expect(
        page.locator('[data-testid="login-email-input"]')
      ).toBeVisible();
    });

    test("should redirect to login when accessing profile without auth", async ({
      page,
    }) => {
      await page.goto(`/profile/${TEST_USERS.sarah.username}`);

      // Should show login page
      await expect(
        page.locator('[data-testid="login-email-input"]')
      ).toBeVisible();
    });
  });

  test.describe("Auto-login on Registration", () => {
    test("should automatically login after successful registration", async ({
      page,
    }) => {
      const newUser = {
        email: "autouser@example.com",
        username: "autouser",
        displayName: "Auto User",
        password: "AutoPass123!",
      };

      await registerUser(page, newUser);

      // Should be logged in without manual login
      await expect(page.locator('[data-testid="navbar"]')).toBeVisible();

      // Should be able to access protected routes
      await page.click('[data-testid="navbar-settings-link"]');
      await expect(
        page.locator('[data-testid="settings-email"]')
      ).toContainText(newUser.email);
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
