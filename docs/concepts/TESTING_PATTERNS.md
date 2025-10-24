# 🎯 Testbook Testing Patterns

> **💡 Language Selection**: This guide includes both Python and JavaScript examples. Both are expanded by default so you can see all approaches. Click the language tabs to collapse sections you don't need.

## Table of Contents

- [Arrange-Act-Assert Pattern](#arrange-act-assert-pattern)
- [Dynamic Content Patterns](#dynamic-content-patterns)
- [Test Structure Best Practices](#test-structure-best-practices)

---

## Arrange-Act-Assert Pattern

The **Arrange-Act-Assert (AAA)** pattern is the fundamental structure for all tests. It provides clarity, consistency, and makes tests easier to understand and maintain.

### What is AAA?

**Arrange** - Set up the test data and conditions
**Act** - Execute the specific behavior being tested
**Assert** - Verify the expected outcome

### Why Use AAA?

- **Clarity**: Each test has a clear structure
- **Consistency**: All tests follow the same pattern
- **Maintainability**: Easy to understand and modify
- **Debugging**: Clear separation makes issues easier to identify

<details open>
<summary><strong>🐍 Python Example (pytest)</strong></summary>

```python
def test_user_login_success():
    # Arrange
    user = create_test_user(email="test@example.com", password="password123")
    login_data = {"email": "test@example.com", "password": "password123"}

    # Act
    response = client.post("/auth/login", json=login_data)

    # Assert
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["user"]["email"] == "test@example.com"
```

</details>

<details open>
<summary><strong>☕ JavaScript Example (Vitest)</strong></summary>

```javascript
test('user login success', () => {
  // Arrange
  const user = createTestUser({ email: 'test@example.com', password: 'password123' });
  const loginData = { email: 'test@example.com', password: 'password123' };

  // Act
  const response = await fetch('/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(loginData)
  });

  // Assert
  expect(response.status).toBe(200);
  const data = await response.json();
  expect(data.access_token).toBeDefined();
  expect(data.user.email).toBe('test@example.com');
});
```

</details>

### React Component Example (Vitest + Testing Library)

```javascript
test("renders login form with submit button", () => {
  // Arrange
  const mockOnSubmit = vi.fn();

  // Act
  render(<LoginForm onSubmit={mockOnSubmit} />);

  // Assert
  expect(screen.getByRole("form")).toBeInTheDocument();
  expect(screen.getByRole("button", { name: /login/i })).toBeInTheDocument();
  expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
  expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
});
```

### Playwright E2E Example

```javascript
test("user can create a new post", async ({ page }) => {
  // Arrange
  await page.goto("/login");
  await page.fill('[data-testid="email-input"]', "test@example.com");
  await page.fill('[data-testid="password-input"]', "password123");
  await page.click('[data-testid="login-button"]');
  await page.waitForURL("/dashboard");

  // Act
  await page.click('[data-testid="new-post-button"]');
  await page.fill('[data-testid="post-content"]', "This is my new post!");
  await page.click('[data-testid="submit-post-button"]');

  // Assert
  await expect(page.locator('[data-testid="post-content"]')).toContainText(
    "This is my new post!"
  );
  await expect(page.locator('[data-testid="success-message"]')).toBeVisible();
});
```

### AAA Best Practices

1. **One concept per test**: Each test should verify one specific behavior
2. **Clear naming**: Test names should describe what is being tested
3. **Minimal setup**: Only arrange what's necessary for the test
4. **Single assertion**: Focus on one outcome per test (when possible)
5. **Descriptive assertions**: Use clear, specific assertion messages

### Common AAA Mistakes

❌ **Mixing concerns in one test**

```python
def test_user_management():
    # This test does too much - user creation AND login
    user = create_user()  # Arrange
    login_response = login(user)  # Act
    assert login_response.status_code == 200  # Assert

    # This should be separate tests
    user_data = get_user_data()  # Arrange
    update_response = update_user(user_data)  # Act
    assert update_response.status_code == 200  # Assert
```

✅ **Separate concerns into focused tests**

```python
def test_user_login_success():
    # Arrange
    user = create_user()
    # Act
    response = login(user)
    # Assert
    assert response.status_code == 200

def test_user_data_update():
    # Arrange
    user_data = get_user_data()
    # Act
    response = update_user(user_data)
    # Assert
    assert response.status_code == 200
```

---

## Dynamic Content Patterns

When testing dynamic content like posts, comments, and user lists, you often don't know the ID in advance:

```javascript
// ❌ Problem: How do you know the new post will be ID 24 or 500?
await page.click('[data-testid="post-24-react-button"]');
```

<h2 id="the-solution">✅ The Solution</h2>

Testbook provides **multiple selection strategies** for dynamic content:

### 1. **Generic Test IDs** (Recommended for Dynamic Content)

Select any item by type, then filter by attributes:

```javascript
// Select ALL posts
const posts = await page.locator('[data-testid-generic="post-item"]');

// Select first post (most recent)
const firstPost = posts.first();

// Select last post
const lastPost = posts.last();

// Select own posts only
const ownPosts = await page.locator(
  '[data-testid-generic="post-item"][data-is-own-post="true"]'
);

// Select posts by specific author
const sarahPosts = await page.locator(
  '[data-testid-generic="post-item"][data-post-author="sarahjohnson"]'
);

// Get count of posts
const postCount = await posts.count();
```

### 2. **Position-Based Selection**

```javascript
// Most recent post
await page.locator('[data-testid-generic="post-item"]').first().click();

// Nth post (0-indexed)
await page.locator('[data-testid-generic="post-item"]').nth(2);

// Last post
await page.locator('[data-testid-generic="post-item"]').last();
```

### 3. **Attribute Filtering**

```javascript
// Filter by multiple attributes
const reposts = await page.locator(
  '[data-testid-generic="post-item"][data-is-repost="true"]'
);

// Chain filters
const ownPosts = await page.locator(
  '[data-testid-generic="post-item"][data-is-own-post="true"]'
);
const firstOwnPost = ownPosts.first();
```

### 4. **After Creating Content, Use API Response**

```javascript
// Create post and get ID from response
const postId = await page.evaluate(async () => {
  const response = await fetch("http://localhost:8000/api/posts/", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ content: "Test post" }),
  });
  const data = await response.json();
  return data.id;
});

// Now you can use the specific ID
await page.click(`[data-testid="post-${postId}-react-button"]`);
```

<h2 id="available-attributes">📋 Available Attributes</h2>

### Posts

```html
<div data-testid="post-{id}" <!-- Unique id if you know it -->
  data-testid-generic="post-item"
  <!-- Generic selector for all posts -->
  data-post-id="{id}"
  <!-- Post ID for filtering -->
  data-post-author="{username}"
  <!-- Author's username -->
  data-is-own-post="true/false"
  <!-- Is current user's post -->
  data-is-repost="true/false"
  <!-- Is this a repost -->
  >
</div>
```

**Usage examples:**

```javascript
// Playwright - Select first post
await page.locator('[data-testid-generic="post-item"]').first();

// Cypress - Select own posts
cy.get('[data-testid-generic="post-item"][data-is-own-post="true"]');

// Selenium - Select posts by author
driver.find_elements(By.CSS_SELECTOR, '[data-post-author="sarahjohnson"]');

// Find and interact with first own post
await page
  .locator('[data-is-own-post="true"]')
  .first()
  .locator('button:has-text("⋯")')
  .click();
```

### Comments

```html
<div data-testid="comment-{id}" <!-- Unique id if you know it -->
  data-testid-generic="comment-item"
  <!-- Generic selector -->
  data-comment-id="{id}"
  <!-- Comment ID -->
  data-author="{username}"
  <!-- Commenter's username -->
  >
</div>
```

**Usage examples:**

```javascript
// Count comments
const commentCount = await page
  .locator('[data-testid-generic="comment-item"]')
  .count();

// Select comments by specific author
await page.locator(
  '[data-testid-generic="comment-item"][data-author="mikechen"]'
);

// Verify your comment appears
await expect(
  page.locator(
    '[data-testid-generic="comment-item"][data-author="sarahjohnson"]'
  )
).toBeVisible();
```

### Followers

```html
<div data-testid="follower-{id}" <!-- Unique id if you know it -->
  data-testid-generic="follower-item"
  <!-- Generic selector -->
  data-user-id="{id}"
  <!-- User ID -->
  data-username="{username}"
  <!-- Username -->
  data-is-blocked="true/false"
  <!-- Block status -->
  >
</div>
```

**Usage examples:**

```javascript
// Count followers
const followerCount = await page
  .locator('[data-testid-generic="follower-item"]')
  .count();

// Find blocked followers
await page.locator(
  '[data-testid-generic="follower-item"][data-is-blocked="true"]'
);

// Find specific follower by username
await page.locator('[data-username="mikechen"]');
```

### Following

```html
<div data-testid="following-{id}" <!-- Unique id if you know it -->
  data-testid-generic="following-item"
  <!-- Generic selector -->
  data-user-id="{id}"
  <!-- User ID -->
  data-username="{username}"
  <!-- Username -->
  data-is-following="true/false"
  <!-- Follow status -->
  >
</div>
```

<h2 id="common-testing-patterns">🎯 Common Testing Patterns</h2>

### Pattern 1: Test Newly Created Content

```javascript
test("create post and verify it appears", async ({ page }) => {
  await loginAs(page, "sarah.johnson@testbook.com", "Sarah2024!");

  // Create post
  await page.fill('[data-testid="create-post-textarea"]', "New test post");
  await page.click('[data-testid="create-post-submit-button"]');

  // Wait for post to appear
  await page.waitForTimeout(500);

  // Verify by selecting first post (most recent)
  const firstPost = page.locator('[data-testid-generic="post-item"]').first();
  await expect(firstPost).toContainText("New test post");

  // Verify it's your own post
  await expect(firstPost).toHaveAttribute("data-is-own-post", "true");
  await expect(firstPost).toHaveAttribute("data-post-author", "sarahjohnson");
});
```

### Pattern 2: Interact with Your Own Posts

```javascript
test("edit your own post", async ({ page }) => {
  await loginAs(page, "sarah.johnson@testbook.com", "Sarah2024!");

  // Find first own post
  const ownPost = page.locator('[data-is-own-post="true"]').first();

  // Click menu button within that post
  await ownPost.locator('[data-testid$="-menu-button"]').click();

  // Click edit
  await ownPost.locator('[data-testid$="-edit-button"]').click();

  // Edit content
  await ownPost
    .locator('[data-testid$="-edit-textarea"]')
    .fill("Edited content");
  await ownPost.locator('[data-testid$="-save-button"]').click();
});
```

### Pattern 3: Count and Iterate

```javascript
test("react to all posts in feed", async ({ page }) => {
  await loginAs(page, "sarah.johnson@testbook.com", "Sarah2024!");

  // Get all posts
  const posts = page.locator('[data-testid-generic="post-item"]');
  const count = await posts.count();

  // React to each post
  for (let i = 0; i < count; i++) {
    const post = posts.nth(i);
    await post.locator('[data-testid$="-react-button"]').hover();
    await post.locator('[data-testid$="-reaction-like"]').click();
  }

  // Verify all have reactions
  for (let i = 0; i < count; i++) {
    await expect(
      posts.nth(i).locator('[data-testid$="-react-button"]')
    ).toContainText("👍");
  }
});
```

### Pattern 4: Find by Content Then Get ID

```javascript
test("find post by content and get its ID", async ({ page }) => {
  await loginAs(page, "sarah.johnson@testbook.com", "Sarah2024!");

  // Find post containing specific text
  const post = page
    .locator('[data-testid-generic="post-item"]')
    .filter({ hasText: "Morning workout" });

  // Get the post ID for later use
  const postId = await post.getAttribute("data-post-id");

  // Now can use specific selectors if needed
  await page.click(`[data-testid="post-${postId}-react-button"]`);
});
```

### Pattern 5: Filter by Multiple Criteria

```javascript
test("find specific user in followers list", async ({ page }) => {
  await loginAs(page, "sarah.johnson@testbook.com", "Sarah2024!");
  await page.goto("/profile/sarahjohnson/followers");

  // Find specific follower by username
  const follower = page.locator(
    '[data-testid-generic="follower-item"][data-username="mikechen"]'
  );

  await expect(follower).toBeVisible();

  // Block them
  await follower.locator('[data-testid$="-block-button"]').click();

  // Verify blocked state changed
  await expect(follower).toHaveAttribute("data-is-blocked", "true");
});
```

<h2 id="python-selenium-examples">🐍 Python/Selenium Examples</h2>

```python
from selenium.webdriver.common.by import By

# Get all posts
posts = driver.find_elements(By.CSS_SELECTOR, '[data-testid-generic="post-item"]')

# Get first (most recent) post
first_post = posts[0]

# Get own posts only
own_posts = driver.find_elements(By.CSS_SELECTOR, '[data-is-own-post="true"]')

# Filter by author
sarah_posts = driver.find_elements(By.CSS_SELECTOR, '[data-post-author="sarahjohnson"]')

# Get post ID for later use
post_id = first_post.get_attribute('data-post-id')

# Use the ID to target specific elements
react_button = driver.find_element(By.CSS_SELECTOR, f'[data-testid="post-{post_id}-react-button"]')
```

<h2 id="cypress-examples">🎭 Cypress Examples</h2>

```javascript
// Select all posts
cy.get('[data-testid-generic="post-item"]');

// Select first post
cy.get('[data-testid-generic="post-item"]').first();

// Filter by own posts
cy.get('[data-is-own-post="true"]');

// Find post by author and get ID
cy.get('[data-post-author="sarahjohnson"]')
  .first()
  .invoke("attr", "data-post-id")
  .then((postId) => {
    // Use the ID
    cy.get(`[data-testid="post-${postId}-react-button"]`).click();
  });

// Count comments
cy.get('[data-testid-generic="comment-item"]').should("have.length", 5);

// Verify comment by specific user exists
cy.get('[data-testid-generic="comment-item"][data-author="mikechen"]').should(
  "exist"
);
```

<h2 id="best-practices">📊 Best Practices</h2>

### ✅ DO: Use Generic Selectors for Dynamic Content

```javascript
// Good - works regardless of ID
await page.locator('[data-testid-generic="post-item"]').first().click();

// Good - filter by attributes
await page.locator('[data-is-own-post="true"]').first();
```

### ❌ DON'T: Hardcode Dynamic IDs

```javascript
// Bad - ID might not exist or be different
await page.click('[data-testid="post-99-react-button"]');

// Bad - position might change
await page.locator(".post").nth(3); // No data-testid!
```

### ✅ DO: Combine API and UI Testing

```python
# Create post via API, get ID
response = requests.post(f"{BASE_URL}/posts/",
    json={"content": "Test post"},
    headers=headers)
post_id = response.json()["id"]

# Now test UI with known ID
driver.get(f"http://localhost:3000/post/{post_id}")
assert driver.find_element(By.CSS_SELECTOR, f'[data-post-id="{post_id}"]')
```

### ✅ DO: Use Wait Strategies

```javascript
// Wait for new content to appear after action
await page.click('[data-testid="create-post-submit-button"]');

// Wait for the new post to appear
await page.waitForSelector('[data-testid-generic="post-item"]');

// Or wait for specific count
const posts = page.locator('[data-testid-generic="post-item"]');
await expect(posts).toHaveCount(22); // Was 21, now 22
```

<h2 id="complete-selector-reference">🔍 Complete Selector Reference</h2>

### Posts

```css
[data-testid-generic="post-item"]           /* All posts */
[data-is-own-post="true"]                   /* Only your posts */
[data-post-author="username"]               /* Posts by specific user */
[data-is-repost="true"]                     /* Only reposts */
```

### Comments

```css
[data-testid-generic="comment-item"]        /* All comments */
[data-author="username"]                    /* Comments by specific user */
```

### Followers

```css
[data-testid-generic="follower-item"]       /* All followers */
[data-username="username"]                  /* Specific follower */
[data-is-blocked="true"]                    /* Blocked followers */
```

### Following

```css
[data-testid-generic="following-item"]      /* All following */
[data-username="username"]                  /* Specific user */
[data-is-following="true"]                  /* Currently following */
```

<h2 id="real-world-test-scenarios">🧪 Real-World Test Scenarios</h2>

### Scenario: User Registration Flow

```javascript
test("new user registration and first post", async ({ page }) => {
  // Register new user
  await page.goto("http://localhost:3000/register");
  await page.fill('[data-testid="register-email-input"]', "newuser@test.com");
  await page.fill('[data-testid="register-username-input"]', "testuser");
  await page.fill('[data-testid="register-displayname-input"]', "Test User");
  await page.fill('[data-testid="register-password-input"]', "Test123!");
  await page.click('[data-testid="register-submit-button"]');

  // Should auto-login and redirect to feed
  await expect(page).toHaveURL("http://localhost:3000/");
  await expect(page.locator('[data-testid="navbar"]')).toBeVisible();

  // Create first post
  await page.fill('[data-testid="create-post-textarea"]', "My first post!");
  await page.click('[data-testid="create-post-submit-button"]');

  // Verify post appears as first item
  const firstPost = page.locator('[data-testid-generic="post-item"]').first();
  await expect(firstPost).toContainText("My first post!");
  await expect(firstPost).toHaveAttribute("data-is-own-post", "true");
  await expect(firstPost).toHaveAttribute("data-post-author", "testuser");
});
```

### Scenario: Complex Interaction Flow

```javascript
test("follow user, view their posts, react and comment", async ({ page }) => {
  await loginAs(page, "sarah.johnson@testbook.com", "Sarah2024!");

  // Go to Mike's profile
  await page.goto("http://localhost:3000/profile/mikechen");

  // Follow Mike
  await page.click('[data-testid="profile-follow-button"]');
  await expect(
    page.locator('[data-testid="profile-follow-button"]')
  ).toContainText("Unfollow");

  // Switch to Following feed
  await page.click('[data-testid="navbar-home-link"]');
  await page.click('[data-testid="feed-tab-following"]');

  // Find Mike's post (should be in following feed now)
  const mikesPost = page
    .locator('[data-testid-generic="post-item"][data-post-author="mikechen"]')
    .first();

  // React to it
  await mikesPost.locator('[data-testid$="-react-button"]').hover();
  await mikesPost.locator('[data-testid$="-reaction-love"]').click();

  // Verify reaction added
  await expect(
    mikesPost.locator('[data-testid$="-react-button"]')
  ).toContainText("❤️");

  // Add comment
  await mikesPost.locator('[data-testid$="-comment-button"]').click();
  await mikesPost
    .locator('[data-testid$="-comment-input"]')
    .fill("Great post!");
  await mikesPost.locator('[data-testid$="-comment-submit"]').click();
});
```

### Scenario: File Upload Test

```javascript
test("upload image and create post", async ({ page }) => {
  await loginAs(page, "sarah.johnson@testbook.com", "Sarah2024!");

  // Fill content
  await page.fill(
    '[data-testid="create-post-textarea"]',
    "Check out this photo!"
  );

  // Upload file
  await page.setInputFiles(
    '[data-testid="create-post-file-input"]',
    "./test-assets/image.jpg"
  );

  // Verify preview
  await expect(
    page.locator('[data-testid="create-post-preview"]')
  ).toBeVisible();

  // Submit
  await page.click('[data-testid="create-post-submit-button"]');

  // Find the new post (first post with your content)
  const newPost = page
    .locator('[data-testid-generic="post-item"]')
    .filter({ hasText: "Check out this photo!" });

  // Verify image is present
  await expect(newPost.locator("img.post-media")).toBeVisible();
});
```

<h2 id="testing-toggle-actions">🔄 Testing Toggle Actions</h2>

### React/Unreact

```javascript
test("toggle reaction on post", async ({ page }) => {
  await loginAs(page, "sarah.johnson@testbook.com", "Sarah2024!");

  const firstPost = page.locator('[data-testid-generic="post-item"]').first();
  const reactButton = firstPost.locator('[data-testid$="-react-button"]');

  // Add reaction
  await reactButton.hover();
  await firstPost.locator('[data-testid$="-reaction-like"]').click();
  await expect(reactButton).toContainText("👍");

  // Remove reaction (click same emoji again)
  await reactButton.hover();
  await firstPost.locator('[data-testid$="-reaction-like"]').click();
  await expect(reactButton).toContainText("React");
});
```

### Repost/Unrepost

```javascript
test("toggle repost", async ({ page }) => {
  await loginAs(page, "sarah.johnson@testbook.com", "Sarah2024!");

  const firstPost = page.locator('[data-testid-generic="post-item"]').first();
  const repostButton = firstPost.locator('[data-testid$="-repost-button"]');

  // Repost
  await repostButton.click();
  await expect(repostButton).toContainText("✓ Reposted");
  await expect(repostButton).toHaveClass(/btn-primary/);

  // Unrepost
  await repostButton.click();
  await expect(repostButton).toContainText("Repost");
  await expect(repostButton).toHaveClass(/btn-secondary/);
});
```

## 🎓 Key Takeaways

1. ✅ **Use `data-testid-generic`** for dynamic lists
2. ✅ **Use `.first()`, `.last()`, `.nth()`** for positional selection
3. ✅ **Use data attributes** for filtering (`data-post-author`, `data-is-own-post`)
4. ✅ **Combine with text filters** when you know the content
5. ✅ **Get IDs from API responses** when creating content via API
6. ✅ **Use proper waits** after creating/updating content
7. ✅ **Both specific and generic IDs** available for flexibility

## 📚 More Resources

- **TESTING_CHEATSHEET.md** - Quick reference
- **TESTING_GUIDE.md** - Detailed examples
- **TESTING_FEATURES.md** - Complete capabilities
- **README.md** - Full feature documentation

---

## 📚 Additional Resources

- **[README.md](../../README.md)** - Main documentation and project overview
- **[TESTING_GUIDE.md](../guides/TESTING_GUIDE.md)** - Complete testing examples
- **[TESTING_FEATURES.md](TESTING_FEATURES.md)** - All testable features
- **[TESTING_CHEATSHEET.md](TESTING_CHEATSHEET.md)** - Quick reference guide
- **[README.md](../../README.md#quick-start-5-minutes)** - Get started quickly

---

## 10. **Handling Browser Dialogs** ⚠️ ESSENTIAL PATTERN

### The Problem

Frontend applications use browser native dialogs:

- `window.confirm()` - Confirmation dialogs
- `window.alert()` - Alert messages
- `window.prompt()` - Input dialogs

**These block JavaScript execution** until dismissed. Tests will hang indefinitely!

### Real Example from Testbook

Our block user feature had this:

```javascript
const handleBlock = async () => {
  if (!window.confirm("Are you sure you want to block this user?")) return;
  await blockUser();
};
```

Tests that clicked the block button would hang, waiting for the dialog to be dismissed. **This broke 5 Testbook tests!**

### ✅ The Solution: Setup Dialog Handler

**Pattern 1: Per-Test Handler**

```javascript
test("should block user", async ({ page }) => {
  // Setup BEFORE the action that triggers dialog
  page.on("dialog", (dialog) => dialog.accept());

  await page.click('[data-testid="block-button"]');
  await expect(page.locator('[data-testid="block-button"]')).toContainText(
    "Unblock"
  );
});
```

**Pattern 2: Global Handler (RECOMMENDED)**

```javascript
// In test-helpers.js
function setupDialogHandler(page) {
  page.on("dialog", async (dialog) => {
    console.log(`Auto-accepting ${dialog.type()}: ${dialog.message()}`);
    await dialog.accept();
  });
}

// In your test files
test.beforeEach(async ({ page }) => {
  setupDialogHandler(page); // Handles ALL dialogs automatically
  await resetDatabase(page);
  await loginUser(page, "user@example.com", "password");
});
```

**Pattern 3: Selective Handling**

```javascript
page.on("dialog", async (dialog) => {
  if (dialog.message().includes("delete")) {
    await dialog.accept(); // Accept deletion
  } else {
    await dialog.dismiss(); // Dismiss others
  }
});
```

### When to Use

✅ **Always use dialog handlers** if your app has:

- Confirmation dialogs (`window.confirm`)
- Success/error alerts (`window.alert`)
- Delete confirmations
- Destructive action warnings

❌ **Don't rely on dialogs for testing logic**

- They're meant for user safety, not test validation
- Test the API response or UI state change instead

### Common Dialog Scenarios

**Scenario 1: Single Confirmation**

```javascript
// Frontend
if (!window.confirm("Delete?")) return;

// Test
page.on("dialog", (dialog) => dialog.accept());
await page.click('[data-testid="delete-button"]');
```

**Scenario 2: Multiple Confirmations**

```javascript
// Frontend has TWO confirms
if (!window.confirm("Sure?")) return;
if (!window.confirm("Really sure?")) return;

// Test - handler accepts all
page.on("dialog", (dialog) => dialog.accept());
await page.click('[data-testid="delete-button"]');
// Both dialogs auto-dismissed!
```

**Scenario 3: Alert After Action**

```javascript
// Frontend
alert("Success!");

// Test
page.on("dialog", (dialog) => dialog.accept());
await page.click('[data-testid="save-button"]');
// Alert auto-dismissed, test continues
```

### Debugging Dialogs

```javascript
// Log all dialogs to see what's happening
page.on("dialog", async (dialog) => {
  console.log("Dialog type:", dialog.type());
  console.log("Dialog message:", dialog.message());
  console.log("Dialog default value:", dialog.defaultValue());
  await dialog.accept();
});
```

---

## 11. **Force Clicks for Timing Issues**

### When to Use `force: true`

Some elements become hidden/unhittable due to:

- CSS transitions
- Dropdown close handlers
- Overlay animations
- Hover state changes

### Real Example from Testbook

Our edit button is in a dropdown with click-outside handler:

```javascript
useEffect(() => {
  const handleClickOutside = (event) => {
    setShowDropdown(false); // Closes dropdown
  };
  document.addEventListener("mousedown", handleClickOutside);
}, [showDropdown]);
```

Tests would open menu, but dropdown closed before clicking edit!

### ✅ The Pattern

```javascript
// Normal click might fail
await page.click('[data-testid="menu-button"]');
await page.click('[data-testid="edit-button"]'); // ❌ Dropdown closed!

// Force click bypasses some checks
await page.click('[data-testid="menu-button"]');
await page.locator('[data-testid="edit-button"]').click({ force: true }); // ✅ Works!
```

### When to Use Force

✅ **Good use cases:**

- Elements with CSS transitions
- Dropdown menus with close handlers
- Elements that become hidden quickly
- Animation conflicts

❌ **Bad use cases:**

- Actually hidden elements (use different selector)
- As first resort (debug the timing first)
- To bypass intentional visibility restrictions

### Alternative: Better Timing

Sometimes you can avoid force clicks with better timing:

```javascript
// Wait for element to be stable
const editButton = page.locator('[data-testid="edit-button"]');
await expect(editButton).toBeVisible({ timeout: 5000 });
await editButton.click();

// Or wait for transitions to complete
await page.waitForTimeout(200); // CSS transition time
await page.click('[data-testid="edit-button"]');
```

**Trade-off:** Force clicks are faster but less realistic. Use when timing isn't the test focus.

---

## 12. **Waiting for State Changes**

### The Pattern: Don't Wait for Time, Wait for State

**❌ BAD - Arbitrary Timeouts:**

```javascript
await page.click('[data-testid="follow-button"]');
await page.waitForTimeout(1000); // Hope it's enough!
await expect(button).toContainText("Unfollow");
```

**✅ GOOD - Wait for Actual Change:**

```javascript
await page.click('[data-testid="follow-button"]');
await expect(button).toContainText("Unfollow", { timeout: 10000 }); // Waits only as long as needed
```

### Real Examples from Testbook Fixes

**Pattern 1: Wait for Button Text Change**

```javascript
// After clicking follow, wait for button to update
await followButton.click();
await expect(followButton).toContainText(/unfollow/i, { timeout: 10000 });
```

**Pattern 2: Wait for Element to Disappear**

```javascript
// After saving edit, wait for edit form to close
await saveButton.click();
await expect(editTextarea).not.toBeVisible({ timeout: 5000 });
```

**Pattern 3: Wait for Network Idle**

```javascript
// After API-heavy operation
await addReaction(post, "like");
await page.waitForLoadState("networkidle", { timeout: 3000 }).catch(() => {});
```

**Pattern 4: Wait for URL Change**

```javascript
// After deletion should redirect
await page.click('[data-testid="delete-account"]');
await page.waitForURL(/.*\/login/, { timeout: 15000 });
```

---

## 📚 More Info

- **[TESTING_GUIDE.md](../guides/TESTING_GUIDE.md)** - Complete testing examples
- **[CONTRACT_TESTING.md](../guides/CONTRACT_TESTING.md)** - Property-based API contract testing
- **[TESTING_FEATURES.md](TESTING_FEATURES.md)** - All testable features
- **[TESTING_CHEATSHEET.md](TESTING_CHEATSHEET.md)** - Quick reference (updated with real fixes!)
- **[TESTING_ANTIPATTERNS.md](TESTING_ANTIPATTERNS.md)** - What NOT to do (includes dialog anti-pattern!)
- **[FLAKY_TESTS_GUIDE.md](../guides/FLAKY_TESTS_GUIDE.md)** ⭐ - Comprehensive guide with real examples

**New:** Patterns 10-12 (dialog handling, force clicks, state waiting) are based on **real fixes** that took Testbook from 87% → 100% test pass rate!

---

**Now you can test dynamic content AND handle all the edge cases!** 🎉

---

## Test Structure Best Practices

### File Organization

```text
tests/
├── unit/           # Fast, isolated tests
│   ├── test_auth.py
│   ├── test_models.py
│   └── test_utils.py
├── integration/    # Component interaction tests
│   ├── test_api_routes.py
│   └── test_database.py
├── e2e/           # End-to-end user workflows
│   ├── test_user_flows.py
│   └── test_admin_flows.py
└── fixtures/      # Shared test data
    ├── users.py
    └── posts.py
```

### Test Naming Conventions

**Python (pytest)**

```python
def test_user_login_success():
def test_user_login_invalid_credentials():
def test_user_login_missing_email():
def test_user_login_empty_password():
```

**JavaScript (Vitest)**

```javascript
test("user login success", () => {});
test("user login invalid credentials", () => {});
test("user login missing email", () => {});
test("user login empty password", () => {});
```

### Test Data Management

**Use factories for consistent test data**

```python
# tests/factories.py
def create_test_user(email="test@example.com", password="password123"):
    return User(email=email, password=hash_password(password))

def create_test_post(content="Test post", author_id=1):
    return Post(content=content, author_id=author_id)
```

**Use fixtures for shared setup**

```python
# conftest.py
@pytest.fixture
def test_client():
    app = create_app()
    with app.test_client() as client:
        yield client

@pytest.fixture
def authenticated_user(test_client):
    user = create_test_user()
    response = test_client.post("/auth/login", json={
        "email": user.email,
        "password": "password123"
    })
    token = response.json()["access_token"]
    return {"user": user, "token": token}
```

### Test Isolation

**Each test should be independent**

```python
def test_user_creation():
    # This test creates its own data
    user_data = {"email": "new@example.com", "password": "password123"}
    response = client.post("/users", json=user_data)
    assert response.status_code == 201

def test_user_login():
    # This test also creates its own data
    user = create_test_user()
    login_data = {"email": user.email, "password": "password123"}
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
```

### Assertion Best Practices

**Use specific assertions**

```python
# ❌ Vague
assert response.status_code == 200

# ✅ Specific
assert response.status_code == 200
assert "access_token" in response.json()
assert response.json()["user"]["email"] == "test@example.com"
```

**Use descriptive assertion messages**

```python
# ❌ Generic
assert len(users) == 1

# ✅ Descriptive
assert len(users) == 1, f"Expected 1 user, got {len(users)}: {[u.email for u in users]}"
```

### Test Documentation

**Write clear test descriptions**

```python
def test_user_can_update_own_profile():
    """
    Test that authenticated users can update their own profile information.

    Given: A logged-in user
    When: They submit a profile update request
    Then: Their profile should be updated with the new information
    """
    # Test implementation...
```

### Performance Considerations

**Use appropriate test types**

- **Unit tests**: Fast (< 1ms), isolated, no I/O
- **Integration tests**: Medium speed (< 100ms), test component interactions
- **E2E tests**: Slower (< 5s), test complete user workflows

**Parallel test execution**

```bash
# Run tests in parallel
pytest -n auto  # Use all CPU cores
pytest -n 4     # Use 4 processes
```

### Maintenance Tips

1. **Keep tests simple**: One concept per test
2. **Use meaningful names**: Test names should describe the behavior
3. **Avoid test interdependencies**: Each test should work in isolation
4. **Clean up after tests**: Use teardown methods when needed
5. **Regular refactoring**: Update tests when code changes
6. **Monitor test performance**: Keep test suite fast and reliable

---

**For more testing patterns and examples, see:**

- [TESTING_CHEATSHEET.md](TESTING_CHEATSHEET.md) - Quick reference
- [TESTING_ANTIPATTERNS.md](TESTING_ANTIPATTERNS.md) - What to avoid
- [FLAKY_TESTS_GUIDE.md](../guides/FLAKY_TESTS_GUIDE.md) - Handling flaky tests
