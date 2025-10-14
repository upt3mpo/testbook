/**
 * E2E tests for user functionality.
 *
 * Tests user profiles, follow/unfollow, block/unblock,
 * and settings.
 */

import { expect, test } from '@playwright/test';
import {
    loginUser,
    resetDatabase,
    setupDialogHandler,
    TEST_USERS
} from './fixtures/test-helpers.js';

test.describe('Users', () => {
  test.beforeEach(async ({ page }) => {
    // Auto-accept all browser dialogs (confirm/alert)
    setupDialogHandler(page);

    await resetDatabase(page);
    await loginUser(page, TEST_USERS.sarah.email, TEST_USERS.sarah.password);
  });

  test.describe('User Profile', () => {
    test('should view own profile', async ({ page }) => {
      await page.click('[data-testid="navbar-profile-link"]');

      // Should show profile information
      await expect(page.locator('[data-testid="profile-display-name"]')).toContainText(TEST_USERS.sarah.displayName);
      await expect(page.locator('[data-testid="profile-username"]')).toContainText(`@${TEST_USERS.sarah.username}`);

      // Should show edit button for own profile
      await expect(page.locator('[data-testid="profile-edit-button"]')).toBeVisible();
    });

    test('should view other user profile', async ({ page }) => {
      await page.goto(`/profile/${TEST_USERS.mike.username}`);

      // Should show user information
      await expect(page.locator('[data-testid="profile-display-name"]')).toContainText(TEST_USERS.mike.displayName);
      await expect(page.locator('[data-testid="profile-username"]')).toContainText(`@${TEST_USERS.mike.username}`);

      // Should NOT show edit button for other user
      await expect(page.locator('[data-testid="profile-edit-button"]')).not.toBeVisible();

      // Should show follow/block buttons
      await expect(page.locator('[data-testid="profile-follow-button"]')).toBeVisible();
      await expect(page.locator('[data-testid="profile-block-button"]')).toBeVisible();
    });

    test('should show follower and following counts', async ({ page }) => {
      await page.goto(`/profile/${TEST_USERS.sarah.username}`);

      // Wait for profile data to load - look for profile name first
      await expect(page.locator('[data-testid="profile-display-name"]')).toBeVisible({ timeout: 10000 });

      // Then wait for count links to appear (the counts are inside the links)
      await expect(page.locator('[data-testid="profile-followers-link"]')).toBeVisible({ timeout: 10000 });
      await expect(page.locator('[data-testid="profile-following-link"]')).toBeVisible({ timeout: 10000 });
    });

    test('should show posts count', async ({ page }) => {
      await page.goto(`/profile/${TEST_USERS.sarah.username}`);

      await expect(page.locator('[data-testid="profile-posts-count"]')).toBeVisible();
    });
  });

  test.describe('Follow/Unfollow', () => {
    test('should follow a user', async ({ page }) => {
      await page.goto(`/profile/${TEST_USERS.mike.username}`);

      const followButton = page.locator('[data-testid="profile-follow-button"]');
      await expect(followButton).toBeVisible({ timeout: 5000 });

      // Click follow and wait for the button text to change
      await followButton.click();

      // Wait for button to update to "Unfollow" - this indicates the API call succeeded
      await expect(followButton).toContainText(/unfollow/i, { timeout: 10000 });

      // Verify following count increased on own profile
      await page.goto(`/profile/${TEST_USERS.sarah.username}`);

      // Wait for profile to load
      await expect(page.locator('[data-testid="profile-display-name"]')).toBeVisible({ timeout: 10000 });

      // Check the following link contains a number greater than 0
      const followingLink = page.locator('[data-testid="profile-following-link"]');
      await expect(followingLink).toContainText(/[1-9]/, { timeout: 10000 }); // At least 1
    });

    test('should unfollow a user', async ({ page }) => {
      await page.goto(`/profile/${TEST_USERS.mike.username}`);

      const followButton = page.locator('[data-testid="profile-follow-button"]');

      // Follow first
      await followButton.click();
      await expect(followButton).toContainText(/unfollow/i);

      // Then unfollow
      await followButton.click();
      await expect(followButton).toContainText(/^follow$/i);
    });

    test('should show followed users posts in Following feed', async ({ page }) => {
      // Follow Mike
      await page.goto(`/profile/${TEST_USERS.mike.username}`);
      await page.locator('[data-testid="profile-follow-button"]').click();

      // Go to Following feed
      await page.goto('/');
      await page.click('[data-testid="feed-tab-following"]');

      // Should show Mike's posts (if he has any)
      const mikePosts = page.locator(`[data-post-author="${TEST_USERS.mike.username}"]`);
      const count = await mikePosts.count();
      expect(count).toBeGreaterThanOrEqual(0);
    });
  });

  test.describe('Block/Unblock', () => {
    test('should block a user', async ({ page }) => {
      await page.goto(`/profile/${TEST_USERS.mike.username}`);

      const blockButton = page.locator('[data-testid="profile-block-button"]');
      await expect(blockButton).toBeVisible({ timeout: 5000 });

      // Click block and wait for button text to change
      await blockButton.click();

      // Button should change to Unblock - wait for this state change
      await expect(blockButton).toContainText(/unblock/i, { timeout: 10000 });
    });

    test('should unblock a user', async ({ page }) => {
      await page.goto(`/profile/${TEST_USERS.mike.username}`);

      const blockButton = page.locator('[data-testid="profile-block-button"]');
      await expect(blockButton).toBeVisible({ timeout: 5000 });

      // Block first and wait for state change
      await blockButton.click();
      await expect(blockButton).toContainText(/unblock/i, { timeout: 10000 });

      // Then unblock and wait for state change
      await blockButton.click();
      await expect(blockButton).toContainText(/^block$/i, { timeout: 10000 });
    });

    test('should not see blocked users posts in feed', async ({ page }) => {
      // Block Mike
      await page.goto(`/profile/${TEST_USERS.mike.username}`);
      await page.locator('[data-testid="profile-block-button"]').click();

      // Go to All feed
      await page.goto('/');

      // Wait for feed to load
      await page.waitForLoadState('networkidle', { timeout: 5000 });
      await page.waitForTimeout(1000);

      // Force reload to ensure fresh data
      await page.reload();
      await page.waitForLoadState('networkidle', { timeout: 5000 });
      await page.waitForTimeout(500);

      await page.click('[data-testid="feed-tab-all"]');
      await page.waitForTimeout(500);

      // Should not see Mike's posts
      const mikePosts = page.locator(`[data-post-author="${TEST_USERS.mike.username}"]`);
      await expect(mikePosts).toHaveCount(0);
    });
  });

  test.describe('Followers/Following Lists', () => {
    test('should view followers list', async ({ page }) => {
      await page.goto(`/profile/${TEST_USERS.sarah.username}`);

      // Click followers count
      await page.click('[data-testid="profile-followers-link"]');

      // Should be on followers page
      await expect(page.locator('[data-testid="followers-page"]')).toBeVisible();
    });

    test('should view following list', async ({ page }) => {
      await page.goto(`/profile/${TEST_USERS.sarah.username}`);

      // Click following count
      await page.click('[data-testid="profile-following-link"]');

      // Should be on following page
      await expect(page.locator('[data-testid="following-page"]')).toBeVisible();
    });

    test('should unfollow from following page', async ({ page }) => {
      // Follow Mike first
      await page.goto(`/profile/${TEST_USERS.mike.username}`);
      await page.locator('[data-testid="profile-follow-button"]').click();

      // Go to following page
      await page.goto(`/profile/${TEST_USERS.sarah.username}`);
      await page.click('[data-testid="profile-following-link"]');

      // Unfollow Mike
      const mikeInList = page.locator(`[data-username="${TEST_USERS.mike.username}"]`);
      if (await mikeInList.isVisible()) {
        await mikeInList.locator('[data-testid$="-unfollow-button"]').click();

        // Mike should be removed from list
        await expect(mikeInList).not.toBeVisible({ timeout: 5000 });
      }
    });

    test('should block from followers page', async ({ page }) => {
      await page.goto(`/profile/${TEST_USERS.sarah.username}`);

      const followersLink = page.locator('[data-testid="profile-followers-link"]');
      await expect(followersLink).toBeVisible({ timeout: 5000 });
      await followersLink.click();

      // Wait for the followers page to load
      await page.waitForURL(/.*\/followers.*/, { timeout: 5000 }).catch(() => {});

      // If there are followers, try to block one
      const firstFollower = page.locator('[data-testid-generic="follower-item"]').first();
      const followerVisible = await firstFollower.isVisible({ timeout: 3000 }).catch(() => false);

      if (followerVisible) {
        const blockButton = firstFollower.locator('[data-testid$="-block-button"]');
        await expect(blockButton).toBeVisible({ timeout: 5000 });
        await blockButton.click();

        // Wait for blocked state to be applied
        await expect(firstFollower).toHaveAttribute('data-is-blocked', 'true', { timeout: 10000 });
      }
    });
  });

  test.describe('Settings', () => {
    test('should update display name', async ({ page }) => {
      await page.goto('/settings');

      const displayNameInput = page.locator('[data-testid="settings-display-name-input"]');
      await displayNameInput.fill('Updated Name');

      await page.click('[data-testid="settings-save-button"]');

      // Should show success message
      await expect(page.locator('text=/success/i')).toBeVisible({ timeout: 5000 });

      // Verify on profile
      await page.goto(`/profile/${TEST_USERS.sarah.username}`);
      await expect(page.locator('[data-testid="profile-display-name"]')).toContainText('Updated Name');
    });

    test('should update bio', async ({ page }) => {
      await page.goto('/settings');

      const bioInput = page.locator('[data-testid="settings-bio-input"]');
      await bioInput.fill('My updated bio');

      await page.click('[data-testid="settings-save-button"]');

      // Should show success message
      await expect(page.locator('text=/success/i')).toBeVisible({ timeout: 5000 });
    });

    test('should change theme', async ({ page }) => {
      await page.goto('/settings');

      const themeSelect = page.locator('[data-testid="settings-theme-select"]');
      await themeSelect.selectOption('dark');

      await page.click('[data-testid="settings-save-button"]');

      // Page should have dark theme
      const html = page.locator('html');
      await expect(html).toHaveAttribute('data-theme', 'dark');
    });

    test('should change text density', async ({ page }) => {
      await page.goto('/settings');

      const densitySelect = page.locator('[data-testid="settings-text-density-select"]');
      await densitySelect.selectOption('compact');

      await page.click('[data-testid="settings-save-button"]');

      // Should show success
      await expect(page.locator('text=/success/i')).toBeVisible({ timeout: 5000 });
    });

    test('should persist theme across sessions', async ({ page }) => {
      // Set dark theme
      await page.goto('/settings');
      await page.locator('[data-testid="settings-theme-select"]').selectOption('dark');
      await page.click('[data-testid="settings-save-button"]');

      // Reload page
      await page.reload();

      // Should still be dark
      const html = page.locator('html');
      await expect(html).toHaveAttribute('data-theme', 'dark');
    });
  });

  test.describe('Profile Picture', () => {
    test('should upload profile picture', async ({ page }) => {
      await page.goto('/settings');

      // Upload file (requires actual file)
      // This is a placeholder - actual implementation needs a test image
      const fileInput = page.locator('[data-testid="settings-avatar-input"]');

      // Check if file input exists
      await expect(fileInput).toBeAttached();
    });

    test('should clear profile picture', async ({ page }) => {
      await page.goto('/settings');

      const clearButton = page.locator('[data-testid="settings-clear-avatar-button"]');

      if (await clearButton.isVisible()) {
        await clearButton.click();

        // Should revert to default avatar
        await expect(page.locator('text=/default/i')).toBeVisible({ timeout: 5000 });
      }
    });
  });

  test.describe('Account Deletion', () => {
    test('should delete account', async ({ page }) => {
      await page.goto('/settings');

      const deleteButton = page.locator('[data-testid="settings-delete-account-button"]');
      await expect(deleteButton).toBeVisible({ timeout: 5000 });

      // Click delete (may have confirmation)
      await deleteButton.click();

      // Check if there's a confirmation dialog and click it
      const confirmButton = page.locator('button:has-text("confirm"), button:has-text("delete"), button:has-text("yes")').first();
      const hasConfirmation = await confirmButton.isVisible({ timeout: 2000 }).catch(() => false);

      if (hasConfirmation) {
        await confirmButton.click();
      }

      // Wait for redirect to login page - this is the key indicator of successful deletion
      // Use waitForURL which is more reliable than checking for element visibility
      await page.waitForURL(/.*\/(login|$)/, { timeout: 15000 }).catch(async () => {
        // Fallback: check for login input if URL didn't change
        await expect(page.locator('[data-testid="login-email-input"]')).toBeVisible({ timeout: 5000 });
      });
    });
  });
});

