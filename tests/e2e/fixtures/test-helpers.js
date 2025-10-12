/**
 * Test helper functions for Testbook E2E tests.
 *
 * These utilities help with common operations like logging in,
 * creating posts, and resetting test data.
 */

const { expect } = require('@playwright/test');

// Get backend URL from environment or use default
const BACKEND_URL = process.env.BACKEND_URL || process.env.API_URL || 'http://localhost:8000';

/**
 * Reset the database to a clean state using the dev API.
 * @param {import('@playwright/test').Page} page
 */
async function resetDatabase(page) {
  const response = await page.request.post(`${BACKEND_URL}/api/dev/reset`);
  expect(response.ok()).toBeTruthy();
}

/**
 * Seed database with specific test data scenario.
 * @param {import('@playwright/test').Page} page
 * @param {string} scenario - Type of data to seed
 *
 * Available scenarios:
 * - 'default': Standard seed data (default)
 * - 'empty': Clean database with no users
 * - 'high_traffic': Many posts and interactions
 * - 'minimal': Only basic users, no posts
 */
async function seedDatabase(page, scenario = 'default') {
  // First reset to clean state
  await resetDatabase(page);

  if (scenario === 'empty') {
    // Database is already reset, no additional seeding
    return;
  }

  if (scenario === 'minimal') {
    // Default reset includes users, so this is the same as default
    // Could extend to reset + create only 1-2 users if needed
    return;
  }

  if (scenario === 'high_traffic') {
    // Create additional posts using dev API
    const testPosts = [
      { user_id: 1, content: 'Just had an amazing coffee! ☕' },
      { user_id: 1, content: 'Working on a new project today!' },
      { user_id: 2, content: 'Beautiful sunset tonight 🌅' },
      { user_id: 2, content: 'Anyone want to grab lunch?' },
      { user_id: 3, content: 'New photos uploaded! Check them out!' },
      { user_id: 3, content: 'Feeling grateful today 💚' },
    ];

    for (const postData of testPosts) {
      try {
        await page.request.post(`${BACKEND_URL}/api/dev/create-post`, {
          params: postData
        });
      } catch (error) {
        console.warn(`Failed to create test post: ${error.message}`);
      }
    }
  }

  // Default scenario uses the standard seeded data
}

/**
 * Login a user with email and password.
 * @param {import('@playwright/test').Page} page
 * @param {string} email
 * @param {string} password
 */
async function loginUser(page, email, password) {
  await page.goto('/');

  // Fill login form
  await page.fill('[data-testid="login-email-input"]', email);
  await page.fill('[data-testid="login-password-input"]', password);
  await page.click('[data-testid="login-submit-button"]');

  // Wait for navigation to complete (with timeout)
  await page.waitForURL('/', { timeout: 10000 });

  // Verify logged in (navbar should be visible)
  await expect(page.locator('[data-testid="navbar"]')).toBeVisible({ timeout: 10000 });

  // Wait for any pending API calls to complete
  await page.waitForLoadState('networkidle', { timeout: 5000 }).catch(() => {});
}

/**
 * Register a new user.
 * @param {import('@playwright/test').Page} page
 * @param {Object} userData
 * @param {string} userData.email
 * @param {string} userData.username
 * @param {string} userData.displayName
 * @param {string} userData.password
 */
async function registerUser(page, userData) {
  await page.goto('/register');

  await page.fill('[data-testid="register-email-input"]', userData.email);
  await page.fill('[data-testid="register-username-input"]', userData.username);
  await page.fill('[data-testid="register-displayname-input"]', userData.displayName);
  await page.fill('[data-testid="register-password-input"]', userData.password);
  await page.click('[data-testid="register-submit-button"]');

  // Should auto-login and redirect to feed (with generous timeout for API call)
  await page.waitForURL('/', { timeout: 10000 });
  await expect(page.locator('[data-testid="navbar"]')).toBeVisible({ timeout: 10000 });

  // Wait for page to fully load
  await page.waitForLoadState('networkidle', { timeout: 5000 }).catch(() => {});
}

/**
 * Create a post.
 * @param {import('@playwright/test').Page} page
 * @param {string} content
 */
async function createPost(page, content) {
  await page.fill('[data-testid="create-post-textarea"]', content);
  await page.click('[data-testid="create-post-submit-button"]');

  // Wait for post to appear in feed (wait for first post with this content)
  await expect(page.locator(`text="${content}"`).first()).toBeVisible({ timeout: 10000 });

  // Wait for form to clear and API to complete
  await page.waitForLoadState('networkidle', { timeout: 5000 }).catch(() => {});
}

/**
 * Get the first (most recent) post on the feed.
 * @param {import('@playwright/test').Page} page
 * @returns {Promise<import('@playwright/test').Locator>}
 */
function getFirstPost(page) {
  return page.locator('[data-testid-generic="post-item"]').first();
}

/**
 * Get all posts by a specific author.
 * @param {import('@playwright/test').Page} page
 * @param {string} username
 * @returns {Promise<import('@playwright/test').Locator>}
 */
function getPostsByAuthor(page, username) {
  return page.locator(`[data-testid-generic="post-item"][data-post-author="${username}"]`);
}

/**
 * Get the first post owned by the current user.
 * @param {import('@playwright/test').Page} page
 * @returns {Promise<import('@playwright/test').Locator>}
 */
function getFirstOwnPost(page) {
  return page.locator('[data-is-own-post="true"]').first();
}

/**
 * Add a reaction to a post.
 * @param {import('@playwright/test').Locator} post
 * @param {string} reactionType - 'like', 'love', 'haha', 'wow', 'sad', 'angry'
 */
async function addReaction(post, reactionType) {
  const reactButton = post.locator('[data-testid$="-react-button"]');

  // Ensure button is visible
  await expect(reactButton).toBeVisible({ timeout: 5000 });

  // Click the react button to open the dropdown (force click to avoid pointer intercept)
  await reactButton.click({ force: true });
  await post.page().waitForTimeout(500);

  // Click the specific reaction
  const reactionBtn = post.locator(`[data-testid$="-reaction-${reactionType}"]`);
  await expect(reactionBtn).toBeVisible({ timeout: 3000 });
  await reactionBtn.click({ force: true });

  // Wait for the API response
  await post.page().waitForTimeout(1000);
}

/**
 * Add a comment to a post.
 * @param {import('@playwright/test').Locator} post
 * @param {string} commentText
 */
async function addComment(post, commentText) {
  await post.locator('[data-testid$="-comment-button"]').click();
  await post.locator('[data-testid$="-comment-input"]').fill(commentText);
  await post.locator('[data-testid$="-comment-submit"]').click();
}

/**
 * Test user credentials.
 */
const TEST_USERS = {
  sarah: {
    email: 'sarah.johnson@testbook.com',
    password: 'Sarah2024!',
    username: 'sarahjohnson',
    displayName: 'Sarah Johnson'
  },
  mike: {
    email: 'mike.chen@testbook.com',
    password: 'MikeRocks88',
    username: 'mikechen',
    displayName: 'Mike Chen'
  },
  emma: {
    email: 'emma.davis@testbook.com',
    password: 'EmmaLovesPhotos',
    username: 'emmadavis',
    displayName: 'Emma Davis'
  },
  newuser: {
    email: 'newuser@testbook.com',
    password: 'NewUser123!',
    username: 'newuser',
    displayName: 'New User'
  }
};

/**
 * Setup page to auto-accept all browser dialogs (alert, confirm, prompt).
 * This is essential for tests that trigger window.confirm() or window.alert().
 *
 * @param {import('@playwright/test').Page} page
 *
 * @example
 * test.beforeEach(async ({ page }) => {
 *   setupDialogHandler(page);
 *   // ... rest of setup
 * });
 */
function setupDialogHandler(page) {
  page.on('dialog', async dialog => {
    console.log(`Auto-accepting ${dialog.type()}: ${dialog.message()}`);
    await dialog.accept();
  });
}

module.exports = {
  resetDatabase,
  seedDatabase,
  loginUser,
  registerUser,
  createPost,
  getFirstPost,
  getPostsByAuthor,
  getFirstOwnPost,
  addReaction,
  addComment,
  setupDialogHandler,
  TEST_USERS,
  BACKEND_URL
};

