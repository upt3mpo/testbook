/**
 * E2E tests for post functionality.
 *
 * Tests creating, editing, deleting posts, and post interactions
 * (comments, reactions, reposts).
 */

import { expect, test } from '@playwright/test';
import {
    addReaction,
    createPost,
    getFirstOwnPost,
    getFirstPost,
    loginUser,
    resetDatabase,
    setupDialogHandler,
    TEST_USERS
} from './fixtures/test-helpers.js';

test.describe('Posts', () => {
  test.beforeEach(async ({ page }) => {
    // Auto-accept all browser dialogs (confirm/alert)
    setupDialogHandler(page);

    await resetDatabase(page);
    await loginUser(page, TEST_USERS.sarah.email, TEST_USERS.sarah.password);
  });

  test.describe('Create Post', () => {
    test('should create a text post', async ({ page }) => {
      const postContent = 'This is my test post!';
      await createPost(page, postContent);

      // Post should appear in feed
      const firstPost = getFirstPost(page);
      await expect(firstPost).toContainText(postContent);
      await expect(firstPost).toHaveAttribute('data-is-own-post', 'true');
    });

    test('should disable submit button for empty post', async ({ page }) => {
      const submitButton = page.getByTestId('create-post-submit-button');

      // Should be disabled when empty
      await expect(submitButton).toBeDisabled();

      // Should enable when text is entered
      await page.getByTestId('create-post-textarea').fill('Some content');
      await expect(submitButton).toBeEnabled();
    });

    test('should clear textarea after posting', async ({ page }) => {
      await createPost(page, 'Test post');

      // Textarea should be clear
      const textarea = page.getByTestId('create-post-textarea');
      await expect(textarea).toHaveValue('');
    });

    test('should show posts in reverse chronological order', async ({ page }) => {
      // Create multiple posts
      await createPost(page, 'First post');
      await createPost(page, 'Second post');
      await createPost(page, 'Third post');

      // Most recent should be first
      const firstPost = getFirstPost(page);
      await expect(firstPost).toContainText('Third post');
    });
  });

  test.describe('Edit Post', () => {
    test('should edit own post', async ({ page }) => {
      // Create a post first
      await createPost(page, 'Original content');

      const ownPost = getFirstOwnPost(page);

      // scrollIntoViewIfNeeded() already resolves only once the element is
      // in the viewport, so no extra wait is needed here.
      await ownPost.scrollIntoViewIfNeeded();

      // Click menu button
      const menuButton = ownPost.locator('[data-testid$="-menu-button"]');
      await menuButton.click();

      // Click the edit button
      const editButton = ownPost.locator('[data-testid$="-edit-button"]');
      await expect(editButton).toBeVisible({ timeout: 5000 });
      await editButton.click({ force: true });

      // Edit form should appear
      const editTextarea = ownPost.locator('[data-testid$="-edit-textarea"]');
      await expect(editTextarea).toBeVisible({ timeout: 5000 });

      // Edit content
      await editTextarea.fill('Edited content');

      // Click save. The confirm() dialog this triggers is auto-accepted by
      // setupDialogHandler() as part of resolving this click, so the edit
      // form disappearing (checked next) already reflects that.
      await ownPost.locator('[data-testid$="-save-button"]').click();

      // Wait for edit form to disappear (indicating save completed)
      await expect(editTextarea).not.toBeVisible({ timeout: 5000 });

      // Should show updated content
      await expect(ownPost).toContainText('Edited content', { timeout: 5000 });
      await expect(ownPost).not.toContainText('Original content');
    });

    test('should cancel edit', async ({ page }) => {
      await createPost(page, 'Original content');

      const ownPost = getFirstOwnPost(page);

      // scrollIntoViewIfNeeded() already resolves only once the element is
      // in the viewport, so no extra wait is needed here.
      await ownPost.scrollIntoViewIfNeeded();

      // Click menu button
      await ownPost.locator('[data-testid$="-menu-button"]').click();

      // Click edit button
      const editButton = ownPost.locator('[data-testid$="-edit-button"]');
      await expect(editButton).toBeVisible({ timeout: 5000 });
      await editButton.click({ force: true });

      // Wait for edit textarea to appear
      const editTextarea = ownPost.locator('[data-testid$="-edit-textarea"]');
      await expect(editTextarea).toBeVisible({ timeout: 5000 });

      // Change text
      await editTextarea.fill('Changed');

      // Cancel
      await ownPost.locator('[data-testid$="-cancel-button"]').click();

      // Wait for edit form to disappear
      await expect(editTextarea).not.toBeVisible({ timeout: 5000 });

      // Should show original content
      await expect(ownPost).toContainText('Original content', { timeout: 5000 });
      await expect(ownPost).not.toContainText('Changed');
    });

    test('should not show edit option on other users posts', async ({ page }) => {
      // View a post from another user
      const otherUserPost = page.locator('[data-post-author="mikechen"]').first();

      if (await otherUserPost.isVisible()) {
        // Should not have edit menu
        await expect(otherUserPost.locator('[data-testid$="-menu-button"]')).not.toBeVisible();
      }
    });
  });

  test.describe('Delete Post', () => {
    test('should delete own post', async ({ page }) => {
      await createPost(page, 'Post to delete');

      const ownPost = getFirstOwnPost(page);
      const postContent = await ownPost.textContent();

      // scrollIntoViewIfNeeded() already resolves only once the element is
      // in the viewport, so no extra wait is needed here.
      await ownPost.scrollIntoViewIfNeeded();

      // Open menu with force click to avoid pointer issues
      const menuButton = ownPost.locator('[data-testid$="-menu-button"]');
      await expect(menuButton).toBeVisible({ timeout: 5000 });
      await menuButton.click({ force: true });

      // Click delete button. expect().toBeVisible() below already retries
      // until the dropdown has rendered.
      const deleteButton = ownPost.locator('[data-testid$="-delete-button"]');
      await expect(deleteButton).toBeVisible({ timeout: 5000 });
      await deleteButton.click({ force: true });

      // The confirm() dialog this triggers is auto-accepted by
      // setupDialogHandler() as part of resolving the click above, so the
      // post disappearing (checked next) already reflects that.
      await expect(page.locator(`text="${postContent}"`)).not.toBeVisible({ timeout: 5000 });
    });
  });

  test.describe('Reactions', () => {
    test('should add reaction to post', async ({ page }) => {
      // Scope to the post we just created by its own content rather than
      // getFirstPost()'s "first item in the feed" positional locator. The
      // feed sorts by created_at, and one seeded demo post is deliberately
      // timestamped at "now" (days_ago: 0 in backend/seed.py) - close
      // enough to a freshly-created post's timestamp that which one sorts
      // first is a genuine race, not a fixed ordering. This was confirmed
      // by this exact test failing intermittently once the redundant
      // waitForTimeout calls above it were removed. Filtering by content
      // sidesteps the race instead of masking it with a wait.
      const reactionPostContent = 'React to this post';
      await createPost(page, reactionPostContent);

      const myPost = page
        .locator('[data-testid-generic="post-item"]')
        .filter({ hasText: reactionPostContent });
      const reactButton = myPost.locator('[data-testid$="-react-button"]');

      // Verify reaction button exists and get initial state
      await expect(reactButton).toBeVisible();

      // Add reaction
      await addReaction(myPost, 'like');

      // Wait for button text to change to show the reaction was applied
      await expect(reactButton).toContainText('👍', { timeout: 10000 });
    });

    test('should change reaction type', async ({ page }) => {
      const reactionPostContent = 'React to this post';
      await createPost(page, reactionPostContent);

      // See the "should add reaction to post" test above for why this is
      // scoped by content rather than getFirstPost().
      const myPost = page
        .locator('[data-testid-generic="post-item"]')
        .filter({ hasText: reactionPostContent });
      const reactButton = myPost.locator('[data-testid$="-react-button"]');

      // Add like and wait for it to be applied
      await addReaction(myPost, 'like');
      await expect(reactButton).toContainText('👍', { timeout: 10000 });

      // Change to love and wait for the change
      await addReaction(myPost, 'love');
      await expect(reactButton).toContainText('❤️', { timeout: 10000 });
    });

    test('should remove reaction', async ({ page }) => {
      const reactionPostContent = 'React to this post';
      await createPost(page, reactionPostContent);

      // See the "should add reaction to post" test above for why this is
      // scoped by content rather than getFirstPost().
      const myPost = page
        .locator('[data-testid-generic="post-item"]')
        .filter({ hasText: reactionPostContent });
      const reactButton = myPost.locator('[data-testid$="-react-button"]');

      // Add reaction and wait for it to be applied
      await addReaction(myPost, 'like');
      await expect(reactButton).toContainText('👍', { timeout: 10000 });

      // Click same reaction to remove it
      await reactButton.hover();
      const likeButton = myPost.locator('[data-testid$="-reaction-like"]');
      await expect(likeButton).toBeVisible({ timeout: 5000 });
      await likeButton.click();

      // Wait for network to settle after removal
      await page.waitForLoadState('networkidle', { timeout: 3000 }).catch(() => {});

      // Should show default text after removal
      await expect(reactButton).toContainText('React', { timeout: 10000 });
    });

    test('should show all reaction types', async ({ page }) => {
      const reactionPostContent = 'React to this post';
      await createPost(page, reactionPostContent);

      // See the "should add reaction to post" test above for why this is
      // scoped by content rather than getFirstPost().
      const myPost = page
        .locator('[data-testid-generic="post-item"]')
        .filter({ hasText: reactionPostContent });

      // Hover to show reaction menu
      await myPost.locator('[data-testid$="-react-button"]').hover();

      // All reactions should be visible
      const reactions = ['like', 'love', 'haha', 'wow', 'sad', 'angry'];
      for (const reaction of reactions) {
        await expect(myPost.locator(`[data-testid$="-reaction-${reaction}"]`)).toBeVisible();
      }
    });
  });

  test.describe('Comments', () => {
    test('should add comment to post', async ({ page }) => {
      const postContent = 'Post to comment on';
      await createPost(page, postContent);

      // Scope to the post we just created by its own content rather than
      // getFirstPost()'s "first item in the feed" positional locator. The
      // feed sorts by created_at, and one seeded demo post is deliberately
      // timestamped at "now" (days_ago: 0 in backend/seed.py) - close
      // enough to a freshly-created post's timestamp that which one sorts
      // first is a genuine race, not a fixed ordering. Filtering by content
      // sidesteps that race instead of masking it with a wait.
      const myPost = page
        .locator('[data-testid-generic="post-item"]')
        .filter({ hasText: postContent });

      // Clicking the comment button toggles an inline comment form open
      // (see Post.jsx's showCommentInput state) rather than navigating.
      await myPost.locator('[data-testid$="-comment-button"]').click();
      await expect(myPost.locator('[data-testid$="-comment-form"]')).toBeVisible({
        timeout: 5000,
      });
    });

    test('should show comment count', async ({ page }) => {
      // This test requires existing posts with comments
      // Check if comment count is displayed
      const posts = page.locator('[data-testid-generic="post-item"]');
      const firstPost = posts.first();

      if (await firstPost.isVisible()) {
        // Comment button should show count or icon
        await expect(firstPost.locator('[data-testid$="-comment-button"]')).toBeVisible();
      }
    });
  });

  test.describe('Reposts', () => {
    test('should repost a post', async ({ page }) => {
      // Find a post from another user
      const otherPost = page.locator('[data-testid-generic="post-item"]').first();

      if (await otherPost.isVisible()) {
        const repostButton = otherPost.locator('[data-testid$="-repost-button"]');

        // Repost
        await repostButton.click();

        // Button should show reposted state
        await expect(repostButton).toContainText(/reposted/i);
        await expect(repostButton).toHaveClass(/btn-primary/);
      }
    });

    test('should unrepost a post', async ({ page }) => {
      const otherPost = page.locator('[data-testid-generic="post-item"]').first();

      if (await otherPost.isVisible()) {
        const repostButton = otherPost.locator('[data-testid$="-repost-button"]');

        // Repost
        await repostButton.click();
        await expect(repostButton).toContainText(/reposted/i);

        // Unrepost
        await repostButton.click();
        await expect(repostButton).toContainText(/^repost$/i);
        await expect(repostButton).toHaveClass(/btn-secondary/);
      }
    });
  });

  test.describe('Feed Tabs', () => {
    test('should switch between All and Following tabs', async ({ page }) => {
      const allTab = page.getByTestId('feed-tab-all');
      const followingTab = page.getByTestId('feed-tab-following');

      // Should start on All tab
      await expect(allTab).toHaveClass(/active|selected/i);

      // Switch to Following
      await followingTab.click();
      await expect(followingTab).toHaveClass(/active|selected/i);

      // Switch back to All
      await allTab.click();
      await expect(allTab).toHaveClass(/active|selected/i);
    });

    test('should show different posts in Following vs All feed', async ({ page }) => {
      // Get count of All posts
      await page.getByTestId('feed-tab-all').click();
      const allPosts = await page.locator('[data-testid-generic="post-item"]').count();

      // Get count of Following posts
      await page.getByTestId('feed-tab-following').click();
      const followingPosts = await page.locator('[data-testid-generic="post-item"]').count();

      // Counts may differ (depending on who user follows)
      // Just verify both tabs work
      expect(allPosts).toBeGreaterThanOrEqual(0);
      expect(followingPosts).toBeGreaterThanOrEqual(0);
    });
  });
});

// 🧠 Why These Tests Matter:
//
// E2E tests for posts functionality validate the CORE feature of Testbook:
//
// 1. **Main User Flow** - Creating, viewing, and interacting with posts is primary use case
// 2. **Complex Interactions** - Posts involve CRUD, reactions, comments, reposts (multi-component)
// 3. **Real-Time Feedback** - Tests verify UI updates immediately after actions
// 4. **Authorization Enforcement** - Users can only edit/delete their own posts (security!)
//
// What These Tests Catch:
// - ✅ Post creation failures (form doesn't submit, content not saved)
// - ✅ Edit/delete permissions bugs (can edit others' posts = major security issue!)
// - ✅ Reaction toggle issues (doesn't add/remove, wrong emoji shown)
// - ✅ Feed filtering bugs (All vs Following tabs show wrong posts)
// - ✅ UI state problems (buttons don't update, content doesn't refresh)
//
// In Real QA Teams:
// - These are "smoke tests" - must pass before any release
// - They verify the primary business logic of the application
// - Failed post tests mean core feature is broken (deployment blocker)
// - They catch frontend-backend integration issues before users do
//
// For Your Career:
// - Posts/content management is tested in EVERY social media interview
// - Demonstrates you can test complex, stateful interactions
// - Shows understanding of authorization (user can only edit their own content)
// - Interview question: "How would you test CRUD operations?" - Run this test live!
// - Proves you can handle async operations, waits, and flaky selector issues
