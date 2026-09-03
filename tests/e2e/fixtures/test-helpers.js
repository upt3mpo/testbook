/**
 * Test helper functions for Testbook E2E tests.
 *
 * Login, registration, and post/reaction interactions go through the
 * page objects in pages/ instead. What's left here is database setup
 * (resetDatabase, seedDatabase), dialog handling, and shared test data
 * (TEST_USERS) - things that aren't tied to a specific page.
 */

import { expect } from "@playwright/test";

// Get backend URL from environment or use default
const BACKEND_URL =
  process.env.BACKEND_URL || process.env.API_URL || "http://localhost:8000";

/**
 * Reset the database to a clean state using the dev API.
 * @param {import('@playwright/test').Page} page
 */
async function resetDatabase(page) {
  try {
    const response = await page.request.post(`${BACKEND_URL}/api/dev/reset`);
    if (!response.ok()) {
      console.warn("Dev reset endpoint not available, skipping database reset");
      return;
    }
  } catch (error) {
    console.warn(
      "Dev reset endpoint not available, skipping database reset:",
      error.message
    );
    return;
  }
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
async function seedDatabase(page, scenario = "default") {
  // First reset to clean state
  await resetDatabase(page);

  if (scenario === "empty") {
    // Database is already reset, no additional seeding
    return;
  }

  if (scenario === "minimal") {
    // Default reset includes users, so this is the same as default
    // Could extend to reset + create only 1-2 users if needed
    return;
  }

  if (scenario === "high_traffic") {
    // Create additional posts using dev API
    const testPosts = [
      { user_id: 1, content: "Just had an amazing coffee! ☕" },
      { user_id: 1, content: "Working on a new project today!" },
      { user_id: 2, content: "Beautiful sunset tonight 🌅" },
      { user_id: 2, content: "Anyone want to grab lunch?" },
      { user_id: 3, content: "New photos uploaded! Check them out!" },
      { user_id: 3, content: "Feeling grateful today 💚" },
    ];

    for (const postData of testPosts) {
      try {
        await page.request.post(`${BACKEND_URL}/api/dev/create-post`, {
          params: postData,
        });
      } catch (error) {
        console.warn(`Failed to create test post: ${error.message}`);
      }
    }
  }

  // Default scenario uses the standard seeded data
}

/**
 * Get all posts by a specific author.
 * @param {import('@playwright/test').Page} page
 * @param {string} username
 * @returns {Promise<import('@playwright/test').Locator>}
 */
function getPostsByAuthor(page, username) {
  return page.locator(
    `[data-testid-generic="post-item"][data-post-author="${username}"]`
  );
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
    email: "sarah.johnson@testbook.com",
    password: "Sarah2024!",
    username: "sarahjohnson",
    displayName: "Sarah Johnson",
  },
  mike: {
    email: "mike.chen@testbook.com",
    password: "MikeRocks88",
    username: "mikechen",
    displayName: "Mike Chen",
  },
  emma: {
    email: "emma.davis@testbook.com",
    password: "EmmaLovesPhotos",
    username: "emmadavis",
    displayName: "Emma Davis",
  },
  newuser: {
    email: "newuser@testbook.com",
    password: "NewUser123!",
    username: "newuser",
    displayName: "New User",
  },
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
  page.on("dialog", async (dialog) => {
    console.log(`Auto-accepting ${dialog.type()}: ${dialog.message()}`);
    await dialog.accept();
  });
}

export {
  addComment,
  BACKEND_URL,
  getPostsByAuthor,
  resetDatabase,
  seedDatabase,
  setupDialogHandler,
  TEST_USERS,
};
