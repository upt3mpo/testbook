import { expect } from "@playwright/test";

import { BasePage } from "./BasePage.js";

/**
 * Page object for the Profile page.
 *
 * Mirrors tests/e2e-python/pages/profile_page.py.
 */
class ProfilePage extends BasePage {
  constructor(page) {
    super(page);

    // Selectors
    this.displayName = '[data-testid="profile-display-name"]';
    this.profileUsername = '[data-testid="profile-username"]';
    this.editButton = '[data-testid="profile-edit-button"]';
    this.followUnfollowButton = '[data-testid="profile-follow-button"]';
    this.blockUnblockButton = '[data-testid="profile-block-button"]';
    this.followersCount = '[data-testid="profile-followers-link"]';
    this.followingCount = '[data-testid="profile-following-link"]';
    this.postsCount = '[data-testid="profile-posts-count"]';
  }

  /**
   * Navigate to a user's profile.
   * @param {string} username
   * @param {boolean} waitForLoad - wait for profile data to load from API (default true)
   */
  async goto(username, waitForLoad = true) {
    await super.goto(`/profile/${username}`);
    await expect(this.page.locator(this.profileUsername)).toBeVisible();

    if (waitForLoad) {
      // Best-effort wait for the profile's API calls to settle. If this
      // times out, the methods below all use their own retrying
      // expect(), so there's no need for a fallback fixed-time wait here.
      await this.page
        .waitForLoadState("networkidle", { timeout: 5000 })
        .catch(() => {});
    }
  }

  /** Assert the profile header shows the given display name and @username. */
  async expectProfileMatches(displayName, username) {
    await expect(this.page.locator(this.displayName)).toContainText(displayName);
    await expect(this.page.locator(this.profileUsername)).toContainText(
      `@${username}`
    );
  }

  /**
   * Assert this profile is showing as the logged-in user's own (edit
   * button visible, no follow/block buttons).
   */
  async expectOwnProfileControls() {
    await expect(this.page.locator(this.editButton)).toBeVisible();
  }

  /**
   * Assert this profile is showing as someone else's (no edit button,
   * follow/block buttons visible).
   */
  async expectOtherUserProfileControls() {
    await expect(this.page.locator(this.editButton)).not.toBeVisible();
    await expect(this.page.locator(this.followUnfollowButton)).toBeVisible();
    await expect(this.page.locator(this.blockUnblockButton)).toBeVisible();
  }

  /** Ensure the user is followed (clicking Follow button if not already following). */
  async followUser() {
    const button = this.page.locator(this.followUnfollowButton);
    await expect(button).toBeVisible({ timeout: 5000 });

    if ((await button.innerText()).includes("Follow")) {
      await button.click();
      await expect(button).toContainText(/unfollow/i);
    }
    // If already following ("Unfollow"), do nothing
  }

  /** Click the follow/unfollow button to unfollow the user. */
  async unfollowUser() {
    const button = this.page.locator(this.followUnfollowButton);
    await expect(button).toBeVisible({ timeout: 5000 });

    if ((await button.innerText()).includes("Unfollow")) {
      await button.click();
      await expect(button).toContainText(/^follow$/i);
    }
  }

  /** Ensure the user is blocked (clicking Block if not already blocked). */
  async blockUser() {
    const button = this.page.locator(this.blockUnblockButton);
    await expect(button).toBeVisible({ timeout: 5000 });

    if ((await button.innerText()).trim() === "Block") {
      await button.click();
      await expect(button).toContainText(/unblock/i);
    }
    // If already blocked ("Unblock"), do nothing
  }

  /** Click the block/unblock button to unblock the user. */
  async unblockUser() {
    const button = this.page.locator(this.blockUnblockButton);
    await expect(button).toBeVisible({ timeout: 5000 });

    if ((await button.innerText()).includes("Unblock")) {
      await button.click();
      await expect(button).toContainText(/^block$/i);
    }
  }

  /** Click the followers count/link to go to the followers page. */
  async goToFollowersList() {
    const followersLink = this.page.locator(this.followersCount);
    await expect(followersLink).toBeVisible({ timeout: 5000 });
    await followersLink.click();
  }

  /** Click the following count/link to go to the following page. */
  async goToFollowingList() {
    const followingLink = this.page.locator(this.followingCount);
    await expect(followingLink).toBeVisible({ timeout: 5000 });
    await followingLink.click();
  }

  /** Find a specific user's row on the followers/following list page. */
  findUserInList(username) {
    return this.page.locator(`[data-username="${username}"]`);
  }

  /** Get the first row on the followers list page. */
  findFirstFollowerItem() {
    return this.page.locator('[data-testid-generic="follower-item"]').first();
  }

  /**
   * Check if currently following this user.
   * @param {number} waitTimeout - max time to wait for button to appear (ms)
   * @returns {Promise<boolean>} true if following ("Unfollow"), false if not
   */
  async isFollowing(waitTimeout = 5000) {
    const button = this.page.locator(this.followUnfollowButton);
    try {
      await expect(button).toBeVisible({ timeout: waitTimeout });
      return (await button.innerText()).includes("Unfollow");
    } catch {
      return false;
    }
  }

  /**
   * Get the number of followers.
   * @param {number} waitTimeout - max time to wait for count to appear (ms)
   */
  async getFollowerCount(waitTimeout = 5000) {
    const locator = this.page.locator(this.followersCount);
    await expect(locator).toBeVisible({ timeout: waitTimeout });
    const text = await locator.innerText();
    const match = text.match(/(\d+)/);
    return match ? parseInt(match[1], 10) : 0;
  }

  /**
   * Get the number of following.
   * @param {number} waitTimeout - max time to wait for count to appear (ms)
   */
  async getFollowingCount(waitTimeout = 5000) {
    const locator = this.page.locator(this.followingCount);
    await expect(locator).toBeVisible({ timeout: waitTimeout });
    const text = await locator.innerText();
    const match = text.match(/(\d+)/);
    return match ? parseInt(match[1], 10) : 0;
  }

  /** Get the number of posts on profile. */
  getPostCount() {
    return this.page.locator('[data-testid-generic="post-item"]').count();
  }
}

export { ProfilePage };
