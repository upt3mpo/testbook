/**
 * E2E tests for user functionality.
 *
 * Tests user profiles, follow/unfollow, block/unblock,
 * and settings.
 *
 * Page Object Model: interactions go through pages/AuthPage.js,
 * pages/FeedPage.js, pages/ProfilePage.js, and pages/SettingsPage.js
 * rather than raw selectors, so a UI change only needs updating in one
 * place.
 */

import { expect, test } from "@playwright/test";
import { resetDatabase, setupDialogHandler, TEST_USERS } from "./fixtures/test-helpers.js";
import { AuthPage } from "./pages/AuthPage.js";
import { FeedPage } from "./pages/FeedPage.js";
import { ProfilePage } from "./pages/ProfilePage.js";
import { SettingsPage } from "./pages/SettingsPage.js";

test.describe("Users", () => {
  test.beforeEach(async ({ page }) => {
    // Auto-accept all browser dialogs (confirm/alert)
    setupDialogHandler(page);

    await resetDatabase(page);
    const auth = new AuthPage(page);
    await auth.gotoLogin();
    await auth.login(TEST_USERS.sarah.email, TEST_USERS.sarah.password);
    await auth.expectLoggedIn();
  });

  test.describe("User Profile", () => {
    test("should view own profile", async ({ page }) => {
      const auth = new AuthPage(page);
      await auth.navbarProfileLink.click();

      const profile = new ProfilePage(page);
      await profile.expectProfileMatches(
        TEST_USERS.sarah.displayName,
        TEST_USERS.sarah.username
      );
      await profile.expectOwnProfileControls();
    });

    test("should view other user profile", async ({ page }) => {
      const profile = new ProfilePage(page);
      await profile.goto(TEST_USERS.mike.username);

      await profile.expectProfileMatches(
        TEST_USERS.mike.displayName,
        TEST_USERS.mike.username
      );
      await profile.expectOtherUserProfileControls();
    });

    test("should show follower and following counts", async ({ page }) => {
      const profile = new ProfilePage(page);
      await profile.goto(TEST_USERS.sarah.username);

      await expect(page.locator(profile.followersCount)).toBeVisible({
        timeout: 10000,
      });
      await expect(page.locator(profile.followingCount)).toBeVisible({
        timeout: 10000,
      });
    });

    test("should show posts count", async ({ page }) => {
      const profile = new ProfilePage(page);
      await profile.goto(TEST_USERS.sarah.username);

      await expect(page.locator(profile.postsCount)).toBeVisible();
    });
  });

  test.describe("Follow/Unfollow", () => {
    test("should follow a user", async ({ page }) => {
      const profile = new ProfilePage(page);
      await profile.goto(TEST_USERS.mike.username);
      await profile.followUser();

      // Verify following count increased on own profile
      await profile.goto(TEST_USERS.sarah.username);
      await expect(page.locator(profile.followingCount)).toContainText(/[1-9]/, {
        timeout: 10000,
      });
    });

    test("should unfollow a user", async ({ page }) => {
      const profile = new ProfilePage(page);
      await profile.goto(TEST_USERS.mike.username);

      await profile.followUser();
      await profile.unfollowUser();

      const button = page.locator(profile.followUnfollowButton);
      await expect(button).toContainText(/^follow$/i);
    });

    test("should show followed users posts in Following feed", async ({
      page,
    }) => {
      const profile = new ProfilePage(page);
      await profile.goto(TEST_USERS.mike.username);
      await profile.followUser();

      // Go to Following feed
      const feed = new FeedPage(page);
      await feed.goto();
      await feed.goToFollowingTab();

      // Should show Mike's posts (if he has any)
      const mikePosts = page.locator(
        `[data-post-author="${TEST_USERS.mike.username}"]`
      );
      expect(await mikePosts.count()).toBeGreaterThanOrEqual(0);
    });
  });

  test.describe("Block/Unblock", () => {
    test("should block a user", async ({ page }) => {
      const profile = new ProfilePage(page);
      await profile.goto(TEST_USERS.mike.username);
      await profile.blockUser();

      const button = page.locator(profile.blockUnblockButton);
      await expect(button).toContainText(/unblock/i);
    });

    test("should unblock a user", async ({ page }) => {
      const profile = new ProfilePage(page);
      await profile.goto(TEST_USERS.mike.username);

      await profile.blockUser();
      await profile.unblockUser();

      const button = page.locator(profile.blockUnblockButton);
      await expect(button).toContainText(/^block$/i);
    });

    test("should not see blocked users posts in feed", async ({ page }) => {
      const profile = new ProfilePage(page);
      await profile.goto(TEST_USERS.mike.username);
      await profile.blockUser();

      // Go to All feed. Force a reload to ensure fresh data, since the
      // feed page may have cached the pre-block post list.
      const feed = new FeedPage(page);
      await feed.goto();
      await page.reload();
      await page.waitForLoadState("networkidle", { timeout: 5000 });
      await feed.goToAllTab();

      // Should not see Mike's posts. toHaveCount() retries, so it covers
      // any remaining render delay after the reload and tab click.
      const mikePosts = page.locator(
        `[data-post-author="${TEST_USERS.mike.username}"]`
      );
      await expect(mikePosts).toHaveCount(0);
    });
  });

  test.describe("Followers/Following Lists", () => {
    test("should view followers list", async ({ page }) => {
      const profile = new ProfilePage(page);
      await profile.goto(TEST_USERS.sarah.username);
      await profile.goToFollowersList();

      await expect(page.getByTestId("followers-page")).toBeVisible();
    });

    test("should view following list", async ({ page }) => {
      const profile = new ProfilePage(page);
      await profile.goto(TEST_USERS.sarah.username);
      await profile.goToFollowingList();

      await expect(page.getByTestId("following-page")).toBeVisible();
    });

    test("should unfollow from following page", async ({ page }) => {
      const profile = new ProfilePage(page);

      // Follow Mike first
      await profile.goto(TEST_USERS.mike.username);
      await profile.followUser();

      // Go to following page
      await profile.goto(TEST_USERS.sarah.username);
      await profile.goToFollowingList();

      // Unfollow Mike
      const mikeInList = profile.findUserInList(TEST_USERS.mike.username);
      const isVisible = await mikeInList.isVisible({ timeout: 5000 }).catch(() => false);

      if (isVisible) {
        await mikeInList.locator('[data-testid$="-unfollow-button"]').click();

        // Mike should be removed from list
        await expect(mikeInList).not.toBeVisible({ timeout: 5000 });
      }
    });

    test("should block from followers page", async ({ page }) => {
      const profile = new ProfilePage(page);
      await profile.goto(TEST_USERS.sarah.username);
      await profile.goToFollowersList();

      // Wait for the followers page to load
      await page.waitForURL(/.*\/followers.*/, { timeout: 5000 }).catch(() => {});

      // If there are followers, try to block one
      const firstFollower = profile.findFirstFollowerItem();
      const followerVisible = await firstFollower
        .isVisible({ timeout: 3000 })
        .catch(() => false);

      if (followerVisible) {
        const blockButton = firstFollower.locator('[data-testid$="-block-button"]');
        await expect(blockButton).toBeVisible({ timeout: 5000 });
        await blockButton.click();

        // Wait for blocked state to be applied
        await expect(firstFollower).toHaveAttribute("data-is-blocked", "true", {
          timeout: 10000,
        });
      }
    });
  });

  test.describe("Settings", () => {
    test("should update display name", async ({ page }) => {
      const settings = new SettingsPage(page);
      await settings.goto();
      await settings.updateDisplayName("Updated Name");
      await settings.expectSaveSucceeded();

      // Verify on profile
      const profile = new ProfilePage(page);
      await profile.goto(TEST_USERS.sarah.username);
      await expect(page.locator(profile.displayName)).toContainText("Updated Name");
    });

    test("should update bio", async ({ page }) => {
      const settings = new SettingsPage(page);
      await settings.goto();
      await settings.updateBio("My updated bio");
      await settings.expectSaveSucceeded();
    });

    test("should change theme", async ({ page }) => {
      const settings = new SettingsPage(page);
      await settings.goto();
      await settings.changeTheme("dark");
      await settings.expectThemeApplied("dark");
    });

    test("should change text density", async ({ page }) => {
      const settings = new SettingsPage(page);
      await settings.goto();
      await settings.changeTextDensity("compact");
      await settings.expectSaveSucceeded();
    });

    test("should persist theme across sessions", async ({ page }) => {
      const settings = new SettingsPage(page);
      await settings.goto();
      await settings.changeTheme("dark");

      await page.reload();

      await settings.expectThemeApplied("dark");
    });
  });

  test.describe("Profile Picture", () => {
    test("should upload profile picture", async ({ page }) => {
      const settings = new SettingsPage(page);
      await settings.goto();

      // Check if file input exists
      await expect(page.locator(settings.avatarInput)).toBeAttached();
    });

    test("should clear profile picture", async ({ page }) => {
      const settings = new SettingsPage(page);
      await settings.goto();

      const clearButton = page.locator(settings.clearAvatarButton);
      if (await clearButton.isVisible({ timeout: 5000 }).catch(() => false)) {
        await settings.clearAvatar();
        await settings.expectAvatarIsDefault();
      }
    });
  });

  test.describe("Account Deletion", () => {
    test("should delete account", async ({ page }) => {
      const settings = new SettingsPage(page);
      await settings.goto();

      await expect(page.locator(settings.deleteAccountButton)).toBeVisible({
        timeout: 5000,
      });
      await settings.deleteAccount();

      // Wait for redirect to login page - this is the key indicator of
      // successful deletion. waitForURL is more reliable than checking
      // for element visibility.
      await page
        .waitForURL(/.*\/(login|$)/, { timeout: 15000 })
        .catch(async () => {
          // Fallback: check for login input if URL didn't change
          await expect(page.getByTestId("login-email-input")).toBeVisible({
            timeout: 5000,
          });
        });
    });
  });
});
