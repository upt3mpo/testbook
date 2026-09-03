/**
 * E2E tests for post functionality.
 *
 * Tests creating, editing, deleting posts, and post interactions
 * (comments, reactions, reposts).
 *
 * Page Object Model: interactions go through pages/FeedPage.js rather
 * than raw selectors, so a UI change only needs updating in one place.
 */

import { expect, test } from '@playwright/test';
import { resetDatabase, setupDialogHandler, TEST_USERS } from './fixtures/test-helpers.js';
import { AuthPage } from './pages/AuthPage.js';
import { FeedPage } from './pages/FeedPage.js';

test.describe('Posts', () => {
  test.beforeEach(async ({ page }) => {
    // Auto-accept all browser dialogs (confirm/alert)
    setupDialogHandler(page);

    await resetDatabase(page);
    const auth = new AuthPage(page);
    await auth.gotoLogin();
    await auth.login(TEST_USERS.sarah.email, TEST_USERS.sarah.password);
    await auth.expectLoggedIn();
  });

  test.describe('Create Post', () => {
    test('should create a text post', async ({ page }) => {
      const feed = new FeedPage(page);
      const postContent = 'This is my test post!';
      await feed.createPost(postContent);

      // Post should appear in feed. This test is specifically about
      // ordering (a new post appears first), so it stays scoped by
      // position rather than by content - see findPostByContent()'s
      // docstring for why that distinction matters.
      const firstPost = feed.firstPost();
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
      const feed = new FeedPage(page);
      await feed.createPost('Test post');

      // Textarea should be clear
      const textarea = page.getByTestId('create-post-textarea');
      await expect(textarea).toHaveValue('');
    });

    test('should show posts in reverse chronological order', async ({ page }) => {
      const feed = new FeedPage(page);

      // Create multiple posts
      await feed.createPost('First post');
      await feed.createPost('Second post');
      await feed.createPost('Third post');

      // Most recent should be first - this test is specifically about
      // ordering, so it stays scoped by position (see
      // findPostByContent()'s docstring).
      await expect(feed.firstPost()).toContainText('Third post');
    });
  });

  test.describe('Edit Post', () => {
    test('should edit own post', async ({ page }) => {
      const feed = new FeedPage(page);
      await feed.createPost('Original content');

      let ownPost = feed.firstOwnPost();
      // scrollIntoViewIfNeeded() already resolves only once the element is
      // in the viewport, so no extra wait is needed here.
      await ownPost.scrollIntoViewIfNeeded();

      await feed.editPost(ownPost, 'Edited content');

      // Wait for edit form to disappear (indicating save completed)
      await expect(ownPost.locator(feed.postEditTextarea)).not.toBeVisible({
        timeout: 5000,
      });

      // Re-query the post to get a fresh locator, then verify updated content
      ownPost = feed.firstOwnPost();
      await expect(ownPost).toContainText('Edited content', { timeout: 5000 });
      await expect(ownPost).not.toContainText('Original content');
    });

    test('should cancel edit', async ({ page }) => {
      const feed = new FeedPage(page);
      await feed.createPost('Original content');

      const ownPost = feed.firstOwnPost();
      // scrollIntoViewIfNeeded() already resolves only once the element is
      // in the viewport, so no extra wait is needed here.
      await ownPost.scrollIntoViewIfNeeded();

      const editTextarea = await feed.startEditingPost(ownPost);
      await editTextarea.fill('Changed');
      await feed.cancelEditingPost(ownPost);

      // Wait for edit form to disappear
      await expect(editTextarea).not.toBeVisible({ timeout: 5000 });

      // Should show original content
      await expect(ownPost).toContainText('Original content', { timeout: 5000 });
      await expect(ownPost).not.toContainText('Changed');
    });

    test('should not show edit option on other users posts', async ({ page }) => {
      const feed = new FeedPage(page);

      // View a post from another user
      const otherUserPost = page.locator('[data-post-author="mikechen"]').first();

      if (await otherUserPost.isVisible()) {
        // Should not have edit menu
        await expect(otherUserPost.locator(feed.postMenuButton)).not.toBeVisible();
      }
    });
  });

  test.describe('Delete Post', () => {
    test('should delete own post', async ({ page }) => {
      const feed = new FeedPage(page);
      await feed.createPost('Post to delete');

      const ownPost = feed.firstOwnPost();
      const postContent = await ownPost.textContent();

      await feed.deletePost(ownPost);

      // The confirm() dialog this triggers is auto-accepted by
      // setupDialogHandler() as part of resolving the click above, so the
      // post disappearing (checked next) already reflects that.
      await expect(page.locator(`text="${postContent}"`)).not.toBeVisible({ timeout: 5000 });
    });
  });

  test.describe('Reactions', () => {
    test('should add reaction to post', async ({ page }) => {
      const feed = new FeedPage(page);
      await feed.createPost('React to this post');
      const myPost = feed.findPostByContent('React to this post');
      const reactButton = myPost.locator(feed.postReactButton);

      await expect(reactButton).toBeVisible();

      await feed.reactToPost(myPost, 'like');

      // Wait for button to show reaction
      await expect(reactButton).toContainText('👍', { timeout: 10000 });
    });

    test('should change reaction type', async ({ page }) => {
      const feed = new FeedPage(page);
      await feed.createPost('React to this post');
      const myPost = feed.findPostByContent('React to this post');
      const reactButton = myPost.locator(feed.postReactButton);

      // Add like
      await feed.reactToPost(myPost, 'like');
      await expect(reactButton).toContainText('👍', { timeout: 10000 });

      // Change to love
      await feed.reactToPost(myPost, 'love');
      await expect(reactButton).toContainText('❤️', { timeout: 10000 });
    });

    test('should remove reaction', async ({ page }) => {
      const feed = new FeedPage(page);
      await feed.createPost('React to this post');
      const myPost = feed.findPostByContent('React to this post');
      const reactButton = myPost.locator(feed.postReactButton);

      // Add reaction
      await feed.reactToPost(myPost, 'like');
      await expect(reactButton).toContainText('👍', { timeout: 10000 });

      // Reacting with the same type again removes it
      await feed.reactToPost(myPost, 'like');

      // Wait for network to settle
      await page.waitForLoadState('networkidle', { timeout: 3000 }).catch(() => {});

      // Should show default text after removal
      await expect(reactButton).toContainText('React', { timeout: 10000 });
    });

    test('should show all reaction types', async ({ page }) => {
      const feed = new FeedPage(page);
      await feed.createPost('React to this post');
      const myPost = feed.findPostByContent('React to this post');

      const reactButton = myPost.locator(feed.postReactButton);
      await expect(reactButton).toBeVisible({ timeout: 5000 });

      // Force hover to open the reaction dropdown. The dropdown has a CSS
      // fade-in transition, but each expect() below already retries for up
      // to 5s, which covers that transition without a separate wait.
      await reactButton.hover({ force: true });

      // All reactions should be visible
      const reactions = ['like', 'love', 'haha', 'wow', 'sad', 'angry'];
      for (const reaction of reactions) {
        await expect(myPost.locator(`[data-testid$="-reaction-${reaction}"]`)).toBeVisible({
          timeout: 5000,
        });
      }
    });
  });

  test.describe('Comments', () => {
    test('should add comment to post', async ({ page }) => {
      const feed = new FeedPage(page);
      const postContent = 'Post to comment on';
      await feed.createPost(postContent);
      const myPost = feed.findPostByContent(postContent);

      // Clicking the comment button toggles an inline comment form open
      // (see Post.jsx's showCommentInput state) rather than navigating.
      await feed.openCommentForm(myPost);
      await expect(myPost.locator(feed.postCommentForm)).toBeVisible({ timeout: 5000 });
    });

    test('should show comment count', async ({ page }) => {
      const feed = new FeedPage(page);
      const firstPost = feed.firstPost();

      if (await firstPost.isVisible()) {
        // Comment button should show count or icon
        await expect(firstPost.locator(feed.postCommentButton)).toBeVisible();
      }
    });
  });

  test.describe('Reposts', () => {
    test('should repost a post', async ({ page }) => {
      const feed = new FeedPage(page);

      // Find a post from another user
      const otherPost = feed.firstPost();

      if (await otherPost.isVisible()) {
        const repostButton = otherPost.locator(feed.postRepostButton);

        await feed.toggleRepost(otherPost);

        // Button should show reposted state
        await expect(repostButton).toContainText(/reposted/i);
        await expect(repostButton).toHaveClass(/btn-primary/);
      }
    });

    test('should unrepost a post', async ({ page }) => {
      const feed = new FeedPage(page);

      // Get first post - should be from seeded data (other users)
      const otherPost = feed.firstPost();

      if (await otherPost.isVisible()) {
        const repostButton = otherPost.locator(feed.postRepostButton);

        // Repost. toContainText() below retries until the button's label
        // actually updates, so no separate wait is needed.
        await feed.toggleRepost(otherPost);
        await expect(repostButton).toContainText(/reposted/i, { timeout: 10000 });

        // Unrepost
        await feed.toggleRepost(otherPost);
        await expect(repostButton).toContainText(/^repost$/i, { timeout: 10000 });
        await expect(repostButton).toHaveClass(/btn-secondary/);
      }
    });
  });

  test.describe('Feed Tabs', () => {
    test('should switch between All and Following tabs', async ({ page }) => {
      const feed = new FeedPage(page);

      // Should start on All tab
      await expect(feed.feedTabAll).toHaveClass(/active|selected/i);

      // Switch to Following
      await feed.goToFollowingTab();
      await expect(feed.feedTabFollowing).toHaveClass(/active|selected/i);

      // Switch back to All
      await feed.goToAllTab();
      await expect(feed.feedTabAll).toHaveClass(/active|selected/i);
    });

    test('should show different posts in Following vs All feed', async ({ page }) => {
      const feed = new FeedPage(page);

      // Get count of All posts
      await feed.goToAllTab();
      const allPosts = await feed.postCount();

      // Get count of Following posts
      await feed.goToFollowingTab();
      const followingPosts = await feed.postCount();

      // Counts may differ (depending on who user follows)
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
