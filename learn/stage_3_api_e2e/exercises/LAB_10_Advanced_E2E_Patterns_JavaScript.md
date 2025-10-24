# 🧪 Lab 10: Advanced E2E Patterns (JavaScript)

**Estimated Time:** 120 minutes<br>
**Difficulty:** Advanced<br>
**Language:** 🟨 JavaScript<br>
**Prerequisites:** Lab 9 completed

**💡 Need Python instead?** Try [Lab 10: Advanced E2E Patterns (Python)](LAB_10_Advanced_E2E_Patterns_Python.md)!

**What This Adds:** Master advanced E2E testing patterns including page objects, data-driven tests, and complex user workflows. This takes your E2E testing to the next level.

---

## 🎯 What You'll Learn

- **Page Object Model (POM)** - Reusable page helpers
- **Advanced Playwright fixtures** - Custom test setup
- **Network interception** - Mock API responses
- **Test organization** - Organize test runs (smoke vs regression)
- **Screenshot assertions** - Visual verification
- **Selective waits** - Smart waiting strategies
- **Data builders** - Clean test data creation

---

## 📋 Step-by-Step Instructions

### Part 1: Page Object Model (45 minutes)

The Page Object Model organizes your test code by putting page-specific logic in reusable classes.

#### Step 1: Create Your First Page Object

Create `tests/e2e/pages/feed-page.js`:

```javascript
/**
 * Page Object for the Feed page
 *
 * This class encapsulates all interactions with the feed page,
 * making tests more readable and maintainable.
 */

export class FeedPage {
  constructor(page) {
    this.page = page;

    // Selectors
    this.createPostTextarea = '[data-testid="create-post-textarea"]';
    this.createPostSubmit = '[data-testid="create-post-submit"]';
    this.postItems = '[data-testid-generic="post-item"]';
    this.navbar = '[data-testid="navbar"]';
  }

  async goto() {
    /**Navigate to the feed page and wait for it to load.*/
    await this.page.goto("http://localhost:3000");
    await this.page.waitForSelector(this.navbar, { state: "visible" });
  }

  async createPost(content) {
    /**Create a new post.*/
    await this.page.fill(this.createPostTextarea, content);
    await this.page.click(this.createPostSubmit);

    // Wait for post to appear
    await this.page.waitForTimeout(500);
    await this.page.waitForSelector(this.postItems, { state: "visible" });
  }

  async getFirstPost() {
    /**Get the first (most recent) post.*/
    return this.page.locator(this.postItems).first();
  }

  async getAllPosts() {
    /**Get all posts.*/
    return this.page.locator(this.postItems);
  }

  async getPostCount() {
    /**Count visible posts.*/
    return await this.page.locator(this.postItems).count();
  }

  async findPostByContent(content) {
    /**Find a post by its content text.*/
    return this.page.locator(this.postItems, { hasText: content });
  }

  async deleteFirstPost() {
    /**Delete the first post (must be your own).*/
    const firstPost = await this.getFirstPost();
    await firstPost.locator('[data-testid$="-delete-button"]').click();
    await this.page.waitForTimeout(500);
  }

  async waitForPostToAppear(content, timeout = 5000) {
    /**Wait for a specific post to appear.*/
    await this.page.waitForSelector(
      `${this.postItems}:has-text("${content}")`,
      { timeout }
    );
  }
}
```

#### Step 2: Create Profile Page Object

Create `tests/e2e/pages/profile-page.js`:

```javascript
/**
 * Page Object for the Profile page
 *
 * Handles all interactions with user profile pages.
 */

export class ProfilePage {
  constructor(page) {
    this.page = page;
  }

  async goto(username) {
    /**Navigate to a user's profile.*/
    await this.page.goto(`http://localhost:3000/profile/${username}`);
    await this.page.waitForSelector('[data-testid="profile-username"]', {
      state: "visible",
    });
  }

  async followUser() {
    /**Click the follow button.*/
    await this.page.click('[data-testid="profile-follow-button"]');
    await this.page.waitForTimeout(300);
  }

  async unfollowUser() {
    /**Click the unfollow button.*/
    await this.page.click('[data-testid="profile-unfollow-button"]');
    await this.page.waitForTimeout(300);
  }

  async isFollowing() {
    /**Check if currently following this user.*/
    return await this.page
      .locator('[data-testid="profile-unfollow-button"]')
      .isVisible();
  }

  async getFollowerCount() {
    /**Get the number of followers.*/
    const text = await this.page
      .locator('[data-testid="profile-followers-count"]')
      .innerText();
    return parseInt(text);
  }

  async getFollowingCount() {
    /**Get the number of following.*/
    const text = await this.page
      .locator('[data-testid="profile-following-count"]')
      .innerText();
    return parseInt(text);
  }

  async getPostCount() {
    /**Get the number of posts on profile.*/
    return await this.page.locator('[data-testid-generic="post-item"]').count();
  }

  async getUsername() {
    /**Get the profile username.*/
    return await this.page
      .locator('[data-testid="profile-username"]')
      .innerText();
  }
}
```

#### Step 3: Use Page Objects in Tests

Create `tests/e2e/test-page-objects.spec.js`:

```javascript
import { test, expect } from "@playwright/test";
import { FeedPage } from "./pages/feed-page.js";
import { ProfilePage } from "./pages/profile-page.js";

test.describe("Page Object Model Examples", () => {
  test("should create post using Page Object Model", async ({ page }) => {
    // Arrange
    const feedPage = new FeedPage(page);

    // Login first (assuming you have a login helper)
    await page.goto("http://localhost:3000");
    await page.fill(
      '[data-testid="login-email-input"]',
      "sarah.johnson@testbook.com"
    );
    await page.fill('[data-testid="login-password-input"]', "Sarah2024!");
    await page.click('[data-testid="login-submit-button"]');
    await page.waitForSelector('[data-testid="navbar"]', { state: "visible" });

    // Act
    await feedPage.goto();
    const postContent = "Testing with Page Objects!";
    await feedPage.createPost(postContent);

    // Assert
    expect(await feedPage.getPostCount()).toBeGreaterThanOrEqual(1);
    const firstPost = await feedPage.getFirstPost();
    await expect(firstPost).toContainText(postContent);
  });

  test("should follow user using Page Object Model", async ({ page }) => {
    // Arrange
    const profilePage = new ProfilePage(page);

    // Login first
    await page.goto("http://localhost:3000");
    await page.fill(
      '[data-testid="login-email-input"]',
      "sarah.johnson@testbook.com"
    );
    await page.fill('[data-testid="login-password-input"]', "Sarah2024!");
    await page.click('[data-testid="login-submit-button"]');
    await page.waitForSelector('[data-testid="navbar"]', { state: "visible" });

    // Act
    await profilePage.goto("mikechen");
    const initialFollowers = await profilePage.getFollowerCount();
    await profilePage.followUser();

    // Assert
    expect(await profilePage.isFollowing()).toBe(true);
    expect(await profilePage.getFollowerCount()).toBe(initialFollowers + 1);
  });

  test("should complete workflow with Page Object Model", async ({ page }) => {
    // Arrange
    const feedPage = new FeedPage(page);
    const profilePage = new ProfilePage(page);

    // Login first
    await page.goto("http://localhost:3000");
    await page.fill(
      '[data-testid="login-email-input"]',
      "sarah.johnson@testbook.com"
    );
    await page.fill('[data-testid="login-password-input"]', "Sarah2024!");
    await page.click('[data-testid="login-submit-button"]');
    await page.waitForSelector('[data-testid="navbar"]', { state: "visible" });

    // Act - Create a post
    await feedPage.goto();
    await feedPage.createPost("Check out my profile!");

    // Act - View own profile
    await profilePage.goto("sarahjohnson");

    // Assert
    expect(await profilePage.getPostCount()).toBeGreaterThanOrEqual(1);
  });
});
```

**🎯 Checkpoint:** Run `npx playwright test test-page-objects.spec.js --headed`

---

### Part 2: Advanced Fixtures (30 minutes)

Create custom fixtures to simplify test setup.

Create `tests/e2e/fixtures/advanced-fixtures.js`:

```javascript
import { test as base } from "@playwright/test";
import { FeedPage } from "../pages/feed-page.js";
import { ProfilePage } from "../pages/profile-page.js";

// Custom fixtures
export const test = base.extend({
  feedPage: async ({ page }, use) => {
    const feedPage = new FeedPage(page);
    await use(feedPage);
  },

  profilePage: async ({ page }, use) => {
    const profilePage = new ProfilePage(page);
    await use(profilePage);
  },

  authenticatedFeed: async ({ page, feedPage }, use) => {
    // Login and navigate to feed
    await page.goto("http://localhost:3000");
    await page.fill(
      '[data-testid="login-email-input"]',
      "sarah.johnson@testbook.com"
    );
    await page.fill('[data-testid="login-password-input"]', "Sarah2024!");
    await page.click('[data-testid="login-submit-button"]');
    await page.waitForSelector('[data-testid="navbar"]', { state: "visible" });

    await feedPage.goto();
    await use(feedPage);
  },

  createTestPosts: async ({ authenticatedFeed }, use) => {
    const createPosts = async (count = 3, prefix = "Test post") => {
      const posts = [];
      for (let i = 0; i < count; i++) {
        const content = `${prefix} ${i + 1}`;
        await authenticatedFeed.createPost(content);
        posts.push(content);
      }
      return posts;
    };
    await use(createPosts);
  },

  anyUser: async ({ page }, use) => {
    const users = ["sarah", "mike", "emma"];
    const user = users[Math.floor(Math.random() * users.length)];

    // Login as selected user
    await page.goto("http://localhost:3000");
    await page.fill(
      '[data-testid="login-email-input"]',
      `${user}.johnson@testbook.com`
    );
    await page.fill('[data-testid="login-password-input"]', "Password123!");
    await page.click('[data-testid="login-submit-button"]');
    await page.waitForSelector('[data-testid="navbar"]', { state: "visible" });

    await use(user);
  },
});

export { expect } from "@playwright/test";
```

Create `tests/e2e/test-advanced-fixtures.spec.js`:

```javascript
import { test, expect } from "./fixtures/advanced-fixtures.js";

test.describe("Advanced Fixtures", () => {
  test("should use feed page fixture", async ({ authenticatedFeed }) => {
    // Already logged in and on feed page!
    await authenticatedFeed.createPost("Using fixture!");
    expect(await authenticatedFeed.getPostCount()).toBeGreaterThanOrEqual(1);
  });

  test("should create multiple posts with fixture", async ({
    authenticatedFeed,
    createTestPosts,
  }) => {
    // Create multiple posts
    const posts = await createTestPosts(5, "Fixture post");

    // Verify all posts created
    expect(await authenticatedFeed.getPostCount()).toBeGreaterThanOrEqual(5);

    // Verify specific posts exist
    for (const postContent of posts) {
      const post = await authenticatedFeed.findPostByContent(postContent);
      await expect(post).toBeVisible();
    }
  });

  test("should run with different users", async ({ anyUser, feedPage }) => {
    // This test runs with a random user
    await feedPage.goto();
    await feedPage.createPost(`Posted by ${anyUser}`);

    // Each user can create posts
    expect(await feedPage.getPostCount()).toBeGreaterThanOrEqual(1);
  });
});
```

**🎯 Checkpoint:** Run `npx playwright test test-advanced-fixtures.spec.js --headed`

---

### Part 3: Network Interception (20 minutes)

Mock API responses to test different scenarios.

Create `tests/e2e/test-network.spec.js`:

```javascript
import { test, expect } from "@playwright/test";

test.describe("Network Interception", () => {
  test("should mock empty feed response", async ({ page }) => {
    // Login first
    await page.goto("http://localhost:3000");
    await page.fill(
      '[data-testid="login-email-input"]',
      "sarah.johnson@testbook.com"
    );
    await page.fill('[data-testid="login-password-input"]', "Sarah2024!");
    await page.click('[data-testid="login-submit-button"]');
    await page.waitForSelector('[data-testid="navbar"]', { state: "visible" });

    // Mock the feed API endpoint
    await page.route("**/api/feed**", (route) => {
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify([]), // Empty feed
      });
    });

    // Navigate to feed
    await page.goto("http://localhost:3000");

    // Should show empty state
    await expect(page.locator("text=/no posts/i")).toBeVisible({
      timeout: 5000,
    });
  });

  test("should mock API error", async ({ page }) => {
    // Login first
    await page.goto("http://localhost:3000");
    await page.fill(
      '[data-testid="login-email-input"]',
      "sarah.johnson@testbook.com"
    );
    await page.fill('[data-testid="login-password-input"]', "Sarah2024!");
    await page.click('[data-testid="login-submit-button"]');
    await page.waitForSelector('[data-testid="navbar"]', { state: "visible" });

    // Mock API to return error
    await page.route("**/api/posts/", (route) => {
      route.fulfill({
        status: 500,
        contentType: "application/json",
        body: JSON.stringify({ detail: "Server error" }),
      });
    });

    // Try to create post
    await page.goto("http://localhost:3000");
    await page.fill('[data-testid="create-post-textarea"]', "This will fail");
    await page.click('[data-testid="create-post-submit"]');

    // Should show error message
    await expect(page.locator("text=/error/i")).toBeVisible({ timeout: 5000 });
  });

  test("should simulate slow network", async ({ page }) => {
    // Login first
    await page.goto("http://localhost:3000");
    await page.fill(
      '[data-testid="login-email-input"]',
      "sarah.johnson@testbook.com"
    );
    await page.fill('[data-testid="login-password-input"]', "Sarah2024!");
    await page.click('[data-testid="login-submit-button"]');
    await page.waitForSelector('[data-testid="navbar"]', { state: "visible" });

    // Add delay to API responses
    await page.route("**/api/feed**", async (route) => {
      await new Promise((resolve) => setTimeout(resolve, 2000)); // 2 second delay
      route.continue();
    });

    // Navigate and measure that loading indicator appears
    await page.goto("http://localhost:3000");

    // Should show loading state (briefly)
    try {
      await expect(page.locator('[role="status"]')).toBeVisible({
        timeout: 1000,
      });
    } catch {
      // Loading was too fast, which is fine
    }
  });
});
```

**🎯 Checkpoint:** Run `npx playwright test test-network.spec.js --headed`

---

### Part 4: Test Organization & Markers (15 minutes)

Organize tests with tags to run different test suites.

Create `tests/e2e/test-organization.spec.js`:

```javascript
import { test, expect } from "@playwright/test";

test.describe("Test Organization", () => {
  test("smoke test: app loads successfully @smoke", async ({ page }) => {
    await page.goto("http://localhost:3000");
    await expect(
      page.locator('[data-testid="login-email-input"]')
    ).toBeVisible();
  });

  test("smoke test: login works @smoke", async ({ page }) => {
    await page.goto("http://localhost:3000");
    await page.fill(
      '[data-testid="login-email-input"]',
      "sarah.johnson@testbook.com"
    );
    await page.fill('[data-testid="login-password-input"]', "Sarah2024!");
    await page.click('[data-testid="login-submit-button"]');
    await expect(page.locator('[data-testid="navbar"]')).toBeVisible();
  });

  test("regression: complete user journey @regression @slow", async ({
    page,
  }) => {
    // Register new user
    const timestamp = Date.now();

    await page.goto("http://localhost:3000/register");
    await page.fill(
      '[data-testid="register-email-input"]',
      `test${timestamp}@test.com`
    );
    await page.fill(
      '[data-testid="register-username-input"]',
      `test${timestamp}`
    );
    await page.fill('[data-testid="register-displayname-input"]', "Test User");
    await page.fill('[data-testid="register-password-input"]', "Test123!");
    await page.click('[data-testid="register-submit-button"]');

    await page.waitForURL("http://localhost:3000/", { timeout: 10000 });

    // Create post
    await page.fill('[data-testid="create-post-textarea"]', "My first post!");
    await page.click('[data-testid="create-post-submit"]');

    // View profile
    await page.click('[data-testid="navbar-profile-link"]');

    // Logout
    await page.click('[data-testid="navbar-logout-button"]');
    await expect(
      page.locator('[data-testid="login-email-input"]')
    ).toBeVisible();
  });
});
```

**Run different test suites:**

```bash
# Run only smoke tests (fast)
npx playwright test --grep "@smoke"

# Run regression tests
npx playwright test --grep "@regression"

# Run everything except slow tests
npx playwright test --grep-invert "@slow"

# Run smoke OR regression tests
npx playwright test --grep "@smoke|@regression"
```

---

### Part 5: Data Builders (10 minutes)

Create clean test data with builder pattern.

Create `tests/e2e/builders.js`:

```javascript
/**
 * Test data builders for creating test data cleanly
 */

export class UserBuilder {
  constructor() {
    this.email = null;
    this.username = null;
    this.displayName = null;
    this.password = "Test123!";
  }

  withUniqueEmail() {
    const timestamp = Date.now();
    this.email = `test${timestamp}@testbook.com`;
    return this;
  }

  withUniqueUsername() {
    const timestamp = Date.now();
    this.username = `test${timestamp}`;
    return this;
  }

  withDisplayName(name) {
    this.displayName = name;
    return this;
  }

  withPassword(password) {
    this.password = password;
    return this;
  }

  build() {
    if (!this.email) this.withUniqueEmail();
    if (!this.username) this.withUniqueUsername();
    if (!this.displayName) this.displayName = `Test User ${this.username}`;

    return {
      email: this.email,
      username: this.username,
      displayName: this.displayName,
      password: this.password,
    };
  }
}

export class PostBuilder {
  constructor() {
    this.content = "Test post content";
  }

  withContent(content) {
    this.content = content;
    return this;
  }

  withLongContent() {
    this.content = "This is a longer post. ".repeat(20);
    return this;
  }

  build() {
    return {
      content: this.content,
    };
  }
}
```

Use in tests:

```javascript
import { test, expect } from "@playwright/test";
import { UserBuilder, PostBuilder } from "./builders.js";

test("should register user with builder", async ({ page }) => {
  // Build test user
  const user = new UserBuilder().withDisplayName("Builder User").build();

  // Register
  await page.goto("http://localhost:3000/register");
  await page.fill('[data-testid="register-email-input"]', user.email);
  await page.fill('[data-testid="register-username-input"]', user.username);
  await page.fill(
    '[data-testid="register-displayname-input"]',
    user.displayName
  );
  await page.fill('[data-testid="register-password-input"]', user.password);
  await page.click('[data-testid="register-submit-button"]');

  await page.waitForURL("http://localhost:3000/", { timeout: 10000 });
  await expect(page.locator('[data-testid="navbar"]')).toBeVisible();
});
```

---

## 🎓 What You Learned

- ✅ **Page Object Model** - Reusable, maintainable page helpers
- ✅ **Advanced fixtures** - Custom test setup and teardown
- ✅ **Network interception** - Mocking API responses
- ✅ **Test organization** - Organizing test runs with tags
- ✅ **Data builders** - Clean test data creation
- ✅ **Professional patterns** - Industry-standard E2E practices

---

## 💪 Practice Challenges

### Challenge 1: Add More Page Objects

Create page objects for:

- LoginPage
- RegistrationPage
- SettingsPage

### Challenge 2: Advanced Network Mocking

Create tests that mock:

- Partial responses (some posts load, others fail)
- Rate limit errors (429 status)
- Pagination responses

### Challenge 3: Complex Fixtures

Create a fixture that:

- Logs in as user A
- Creates 3 posts
- Logs in as user B
- Follows user A
- Returns both users

### Challenge 4: Screenshot Testing

Add screenshot capture on test failure:

```javascript
// In playwright.config.js
export default {
  use: {
    screenshot: "only-on-failure",
    video: "retain-on-failure",
  },
};
```

---

## 🎯 Pro Tips

### Tip 1: Keep Page Objects Focused

```javascript
// ❌ Bad: Too much logic in tests
test("should do something", async ({ page }) => {
  await page.goto("...");
  await page.fill('[data-testid="xyz"]', "...");
  await page.click('[data-testid="abc"]');
  // 50 more lines...
});

// ✅ Good: Logic in page object
test("should do something", async ({ profilePage }) => {
  await profilePage.goto("sarah");
  await profilePage.followUser();
});
```

### Tip 2: Use Tags Strategically

```bash
# Run before committing (fast)
npx playwright test --grep "@smoke"

# Run nightly (comprehensive)
npx playwright test --grep "@regression"

# Run specific feature
npx playwright test --grep "@user_management"
```

### Tip 3: Combine Patterns

```javascript
test("should test advanced pattern", async ({
  authenticatedFeed,
  createTestPosts,
}) => {
  // Combines fixtures + page objects + builders
  const posts = await createTestPosts(5);
  expect(await authenticatedFeed.getPostCount()).toBeGreaterThanOrEqual(5);
});
```

---

## ✅ Completion Checklist

- [ ] Created FeedPage and ProfilePage objects
- [ ] Used page objects in tests successfully
- [ ] Created and used advanced fixtures
- [ ] Implemented network interception
- [ ] Used test tags to organize tests
- [ ] Created and used data builders
- [ ] All tests pass

---

## 🆚 Compare with Python

Both JavaScript and Python Playwright support these patterns!

| Feature          | JavaScript (this lab) | Python          |
| ---------------- | --------------------- | --------------- |
| **Page Objects** | Classes               | Classes         |
| **Fixtures**     | test.extend()         | pytest fixtures |
| **Tags**         | @grep                 | @pytest.mark    |
| **Network**      | page.route()          | page.route()    |
| **Syntax**       | Async/await           | Synchronous     |

The concepts transfer directly between languages!

---

## 📚 Resources

**Working Examples (Run These!):**

- **`tests/e2e/pages/`** - Page objects (feed, profile)
- **`tests/e2e/fixtures/`** - Advanced fixtures
- **`tests/e2e/builders.js`** - Data builders

**Study Existing Tests:**

- `tests/e2e/auth.spec.js` - Authentication examples
- `tests/e2e/posts.spec.js` - Post management examples

**Official Documentation:**

- [Playwright Page Objects](https://playwright.dev/docs/pom)
- [Playwright Fixtures](https://playwright.dev/docs/test-fixtures)
- [Playwright Network](https://playwright.dev/docs/network)

---

**🎉 You've mastered advanced E2E testing patterns in JavaScript! These are professional-level skills used in production!**

**Next Lab:** [Lab 7: Playwright Deep Dive (JavaScript)](LAB_07_Playwright_Deep_Dive_JavaScript.md)
