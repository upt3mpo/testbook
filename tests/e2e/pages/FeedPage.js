import { expect } from "@playwright/test";

import { BasePage } from "./BasePage.js";

/**
 * Page object for the Feed page.
 *
 * Mirrors tests/e2e-python/pages/feed_page.py.
 */
class FeedPage extends BasePage {
  constructor(page) {
    super(page);

    // Centralized selectors - change here if UI changes
    this.navbar = '[data-testid="navbar"]';
    this.createPostTextarea = '[data-testid="create-post-textarea"]';
    this.createPostSubmit = '[data-testid="create-post-submit-button"]';
    this.postItems = '[data-testid-generic="post-item"]';
    this.postDeleteButton = '[data-testid$="-delete-button"]';
    this.postReactButton = '[data-testid$="-react-button"]';
    this.postMenuButton = '[data-testid$="-menu-button"]';
    this.postEditButton = '[data-testid$="-edit-button"]';
    this.postEditTextarea = '[data-testid$="-edit-textarea"]';
    this.postSaveButton = '[data-testid$="-save-button"]';
    this.postCancelButton = '[data-testid$="-cancel-button"]';
    this.postCommentButton = '[data-testid$="-comment-button"]';
    this.postCommentForm = '[data-testid$="-comment-form"]';
    this.postRepostButton = '[data-testid$="-repost-button"]';
    this.feedTabAll = page.getByTestId("feed-tab-all");
    this.feedTabFollowing = page.getByTestId("feed-tab-following");
  }

  /**
   * Navigate to the feed and wait for it to be ready.
   * @param {boolean} waitForPosts - wait for the feed's API calls to settle (default true)
   */
  async goto(waitForPosts = true) {
    await super.goto("/");
    await expect(this.page.locator(this.navbar)).toBeVisible({ timeout: 10000 });

    if (waitForPosts) {
      // Best-effort wait for the feed's API calls to settle. If this
      // itself times out (a genuinely slow load), callers that need to
      // see posts already use their own retrying assertion (firstPost(),
      // postCount({ waitForLoad: true }), etc.), so nothing here needs a
      // fallback fixed-time wait.
      await this.page
        .waitForLoadState("networkidle", { timeout: 5000 })
        .catch(() => {});
    }
  }

  /**
   * Create a new post and verify it appears.
   * @param {string} content
   */
  async createPost(content) {
    await this.page.locator(this.createPostTextarea).fill(content);
    await this.page.locator(this.createPostSubmit).click();

    // toContainText() retries, which already covers the time it takes
    // the API call and re-render to finish - no separate wait is needed
    // before it.
    await expect(this.firstPost()).toContainText(content);
  }

  /** Get the first (most recent) post. */
  firstPost() {
    return this.page.locator(this.postItems).first();
  }

  /** Get the first post owned by the current user. */
  firstOwnPost() {
    return this.page.locator('[data-is-own-post="true"]').first();
  }

  /** Get all posts. */
  allPosts() {
    return this.page.locator(this.postItems);
  }

  /**
   * Count visible posts.
   * @param {{ waitForLoad?: boolean, timeout?: number }} [options]
   */
  async postCount({ waitForLoad = false, timeout = 5000 } = {}) {
    if (waitForLoad) {
      // No posts found within timeout - fall through and return 0.
      await expect(this.allPosts().first()).toBeVisible({ timeout }).catch(() => {});
    }

    return this.allPosts().count();
  }

  /**
   * Find a specific post by its content.
   *
   * Prefer this over firstPost()/firstOwnPost() whenever a test just
   * created the post it's about to interact with: the feed sorts by
   * created_at, and one seeded demo post is deliberately timestamped at
   * "now" (days_ago: 0 in backend/seed.py) - close enough to a
   * freshly-created post's timestamp that which one sorts first is a
   * genuine race, not a fixed order. Filtering by content sidesteps
   * that race. Only use firstPost()/firstOwnPost() when a test is
   * specifically verifying feed ordering itself.
   */
  findPostByContent(content) {
    return this.page.locator(this.postItems).filter({ hasText: content });
  }

  /** Open a post's "..." dropdown menu (edit/delete). */
  async openPostMenu(post) {
    const menuButton = post.locator(this.postMenuButton);
    await expect(menuButton).toBeVisible({ timeout: 5000 });
    await menuButton.click({ force: true });
  }

  /**
   * Open a post's menu, edit its content, and save.
   *
   * The confirm() dialog this triggers is auto-accepted by
   * setupDialogHandler() as part of resolving the save click, so the
   * caller can check the result (e.g. the edit form disappearing) right
   * after calling this without an extra wait.
   */
  async editPost(post, newContent) {
    await this.openPostMenu(post);

    const editButton = post.locator(this.postEditButton);
    await expect(editButton).toBeVisible({ timeout: 5000 });
    await editButton.click({ force: true });

    const editTextarea = post.locator(this.postEditTextarea);
    await expect(editTextarea).toBeVisible({ timeout: 5000 });
    await editTextarea.fill(newContent);

    const saveButton = post.locator(this.postSaveButton);
    await expect(saveButton).toBeVisible({ timeout: 5000 });
    await saveButton.click();
  }

  /**
   * Open a post's menu and click Edit, returning the edit textarea. Use
   * this (instead of editPost()) when a test needs to cancel rather
   * than save.
   */
  async startEditingPost(post) {
    await this.openPostMenu(post);

    const editButton = post.locator(this.postEditButton);
    await expect(editButton).toBeVisible({ timeout: 5000 });
    await editButton.click({ force: true });

    const editTextarea = post.locator(this.postEditTextarea);
    await expect(editTextarea).toBeVisible({ timeout: 5000 });
    return editTextarea;
  }

  /** Click Cancel on a post that's currently being edited. */
  async cancelEditingPost(post) {
    const cancelButton = post.locator(this.postCancelButton);
    await expect(cancelButton).toBeVisible({ timeout: 5000 });
    await cancelButton.click();
  }

  /**
   * Open a post's menu and delete it.
   *
   * The confirm() dialog this triggers is auto-accepted by
   * setupDialogHandler() as part of resolving the delete click.
   */
  async deletePost(post) {
    await this.openPostMenu(post);

    const deleteButton = post.locator(this.postDeleteButton);
    await expect(deleteButton).toBeVisible({ timeout: 5000 });
    await deleteButton.click({ force: true });
  }

  /**
   * Open a post's reaction dropdown and pick a reaction. Works for
   * applying a new reaction, changing an existing one, or removing one
   * (clicking the currently-active reaction again removes it) - all
   * three go through this same interaction.
   */
  async reactToPost(post, reaction = "like") {
    const reactButton = post.locator(this.postReactButton);
    await expect(reactButton).toBeVisible({ timeout: 5000 });
    await reactButton.click({ force: true });

    // expect() below already retries until the dropdown has rendered,
    // so no separate wait is needed for the open animation.
    const reactionButton = post.locator(`[data-testid$="-reaction-${reaction}"]`);
    await expect(reactionButton).toBeVisible({ timeout: 5000 });
    await reactionButton.click({ force: true });
  }

  /** Click a post's Comment button to reveal its inline comment form. */
  async openCommentForm(post) {
    await post.locator(this.postCommentButton).click();
  }

  /**
   * Click a post's Repost button. Toggles: reposts it if not already
   * reposted, un-reposts it if already reposted.
   */
  async toggleRepost(post) {
    await post.locator(this.postRepostButton).click();
  }

  /** Switch the feed to the "All" tab. */
  async goToAllTab() {
    await this.feedTabAll.click();
  }

  /** Switch the feed to the "Following" tab. */
  async goToFollowingTab() {
    await this.feedTabFollowing.click();
  }
}

export { FeedPage };
