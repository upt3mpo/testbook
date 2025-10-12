/**
 * E2E tests for authentication flows.
 *
 * Tests registration, login, logout, and authentication state.
 */

const { test, expect } = require('@playwright/test');
const { resetDatabase, loginUser, registerUser, setupDialogHandler, TEST_USERS } = require('./fixtures/test-helpers');

test.describe('Authentication', () => {
  test.beforeEach(async ({ page }) => {
    // Auto-accept all browser dialogs (confirm/alert)
    setupDialogHandler(page);

    await resetDatabase(page);
  });

  test.describe('Registration', () => {
    test('should register new user successfully', async ({ page }) => {
      const newUser = {
        email: 'testuser@example.com',
        username: 'testuser',
        displayName: 'Test User',
        password: 'TestPassword123!'
      };

      await registerUser(page, newUser);

      // Should be logged in and redirected to feed
      await expect(page).toHaveURL('/');
      await expect(page.locator('[data-testid="navbar"]')).toBeVisible();
      await expect(page.locator('[data-testid="navbar-username"]')).toContainText(newUser.displayName);
    });

    test('should show error for duplicate email', async ({ page }) => {
      await page.goto('/register');

      // Try to register with existing email
      await page.fill('[data-testid="register-email-input"]', TEST_USERS.sarah.email);
      await page.fill('[data-testid="register-username-input"]', 'differentuser');
      await page.fill('[data-testid="register-displayname-input"]', 'Different User');
      await page.fill('[data-testid="register-password-input"]', 'Password123!');
      await page.click('[data-testid="register-submit-button"]');

      // Should show error
      await expect(page.locator('text=/email.*already/i')).toBeVisible({ timeout: 5000 });
    });

    test('should show error for duplicate username', async ({ page }) => {
      await page.goto('/register');

      // Try to register with existing username
      await page.fill('[data-testid="register-email-input"]', 'newemail@example.com');
      await page.fill('[data-testid="register-username-input"]', TEST_USERS.sarah.username);
      await page.fill('[data-testid="register-displayname-input"]', 'Different User');
      await page.fill('[data-testid="register-password-input"]', 'Password123!');
      await page.click('[data-testid="register-submit-button"]');

      // Should show error
      await expect(page.locator('text=/username.*already/i')).toBeVisible({ timeout: 5000 });
    });

    test('should validate email format', async ({ page }) => {
      await page.goto('/register');

      await page.fill('[data-testid="register-email-input"]', 'notanemail');
      await page.fill('[data-testid="register-username-input"]', 'testuser');
      await page.fill('[data-testid="register-displayname-input"]', 'Test User');
      await page.fill('[data-testid="register-password-input"]', 'Password123!');

      // Should show HTML5 validation or custom error
      const emailInput = page.locator('[data-testid="register-email-input"]');
      const isInvalid = await emailInput.evaluate((el) => !el.validity.valid);
      expect(isInvalid).toBeTruthy();
    });
  });

  test.describe('Login', () => {
    test('should login with correct credentials', async ({ page }) => {
      await loginUser(page, TEST_USERS.sarah.email, TEST_USERS.sarah.password);

      // Should be on feed page
      await expect(page).toHaveURL('/');
      await expect(page.locator('[data-testid="navbar"]')).toBeVisible();
      await expect(page.locator('[data-testid="navbar-username"]')).toContainText(TEST_USERS.sarah.displayName);
    });

    test('should show error for wrong password', async ({ page }) => {
      await page.goto('/');

      await page.fill('[data-testid="login-email-input"]', TEST_USERS.sarah.email);
      await page.fill('[data-testid="login-password-input"]', 'WrongPassword123!');
      await page.click('[data-testid="login-submit-button"]');

      // Should show error (backend returns "Incorrect email or password")
      await expect(page.locator('[data-testid="login-error"]')).toBeVisible({ timeout: 5000 });
      await expect(page.locator('[data-testid="login-error"]')).toContainText(/incorrect|invalid/i);
    });

    test('should show error for non-existent user', async ({ page }) => {
      await page.goto('/');

      await page.fill('[data-testid="login-email-input"]', 'nonexistent@example.com');
      await page.fill('[data-testid="login-password-input"]', 'Password123!');
      await page.click('[data-testid="login-submit-button"]');

      // Should show error (backend returns "Incorrect email or password")
      await expect(page.locator('[data-testid="login-error"]')).toBeVisible({ timeout: 5000 });
      await expect(page.locator('[data-testid="login-error"]')).toContainText(/incorrect|invalid/i);
    });

    test('should persist login across page refreshes', async ({ page }) => {
      await loginUser(page, TEST_USERS.sarah.email, TEST_USERS.sarah.password);

      // Reload page
      await page.reload();

      // Should still be logged in
      await expect(page.locator('[data-testid="navbar"]')).toBeVisible();
      await expect(page.locator('[data-testid="navbar-username"]')).toContainText(TEST_USERS.sarah.displayName);
    });
  });

  test.describe('Logout', () => {
    test('should logout successfully', async ({ page }) => {
      await loginUser(page, TEST_USERS.sarah.email, TEST_USERS.sarah.password);

      // Click logout
      await page.click('[data-testid="navbar-logout-button"]');

      // Should be redirected to login page
      await expect(page.locator('[data-testid="login-email-input"]')).toBeVisible();
      await expect(page.locator('[data-testid="navbar"]')).not.toBeVisible();
    });

    test('should not access protected routes after logout', async ({ page, context }) => {
      await loginUser(page, TEST_USERS.sarah.email, TEST_USERS.sarah.password);

      // Logout
      await page.click('[data-testid="navbar-logout-button"]');

      // Try to access protected route
      await page.goto('/settings');

      // Should be redirected to login
      await expect(page.locator('[data-testid="login-email-input"]')).toBeVisible();
    });
  });

  test.describe('Protected Routes', () => {
    test('should redirect to login when accessing feed without auth', async ({ page }) => {
      await page.goto('/');

      // Should show login page
      await expect(page.locator('[data-testid="login-email-input"]')).toBeVisible();
    });

    test('should redirect to login when accessing settings without auth', async ({ page }) => {
      await page.goto('/settings');

      // Should show login page
      await expect(page.locator('[data-testid="login-email-input"]')).toBeVisible();
    });

    test('should redirect to login when accessing profile without auth', async ({ page }) => {
      await page.goto(`/profile/${TEST_USERS.sarah.username}`);

      // Should show login page
      await expect(page.locator('[data-testid="login-email-input"]')).toBeVisible();
    });
  });

  test.describe('Auto-login on Registration', () => {
    test('should automatically login after successful registration', async ({ page }) => {
      const newUser = {
        email: 'autouser@example.com',
        username: 'autouser',
        displayName: 'Auto User',
        password: 'AutoPass123!'
      };

      await registerUser(page, newUser);

      // Should be logged in without manual login
      await expect(page.locator('[data-testid="navbar"]')).toBeVisible();

      // Should be able to access protected routes
      await page.click('[data-testid="navbar-settings-link"]');
      await expect(page.locator('[data-testid="settings-email"]')).toContainText(newUser.email);
    });
  });
});

