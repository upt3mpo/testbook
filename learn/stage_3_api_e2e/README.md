# 🌐 Stage 3: API & E2E Testing

**Testing Complete User Journeys**

End-to-end (E2E) tests simulate real users interacting with your application in a browser. API tests verify contracts and external integrations. Together, they ensure your entire system works as users expect.

## Your Progress

[████████████████████] 60% complete
✅ Stage 1: Unit Tests (completed)
✅ Stage 2: Integration Tests (completed)
→ **Stage 3: API & E2E Testing** (you are here)
⬜ Stage 4: Performance & Security
⬜ Stage 5: Capstone

**Estimated time remaining:** 6-9 hours

---

## 🎯 Learning Goals

By the end of this stage, you will:

- ✅ Understand E2E testing and when to use it
- ✅ Write browser automation tests with Playwright
- ✅ Use Page Object Model for maintainable tests
- ✅ Test complete user workflows (login → action → verify)
- ✅ Validate API contracts with OpenAPI/Postman
- ✅ Handle async operations and network requests
- ✅ Capture screenshots and videos for debugging

**Duration:** 4-5 hours

---

## 📂 Where to Look

### E2E Tests (Playwright)

Choose your language preference:

#### 🐍 Python E2E Tests

1. **[`tests/e2e-python/test_auth.py`](../../tests/e2e-python/test_auth.py)**

   - Login and registration flows
   - Session management

2. **[`tests/e2e-python/test_posts.py`](../../tests/e2e-python/test_posts.py)**

   - Creating and interacting with posts
   - Comments and reactions

3. **[`tests/e2e-python/test_users.py`](../../tests/e2e-python/test_users.py)**

   - User profiles and interactions
   - Follow/unfollow workflows

4. **[`tests/e2e-python/pages/`](../../tests/e2e-python/pages/)**
   - Page Object Model implementation
   - Reusable page classes

#### ☕ JavaScript E2E Tests

1. **[`tests/e2e/auth.spec.js`](../../tests/e2e/auth.spec.js)**

   - Authentication flows
   - Login/logout

2. **[`tests/e2e/posts.spec.js`](../../tests/e2e/posts.spec.js)**

   - Post creation and management
   - User interactions

3. **[`tests/e2e/users.spec.js`](../../tests/e2e/users.spec.js)**
   - Profile viewing
   - Social features

### API/Contract Tests

1. **[`tests/api/README.md`](../../tests/api/README.md)**

   - API testing overview
   - Newman/Postman collection usage

2. **[`tests/api/Testbook.postman_collection.json`](../../tests/api/Testbook.postman_collection.json)**

   - Complete API contract tests
   - Request/response examples

3. **[`backend/tests/integration/test_api_contract.py`](../../backend/tests/integration/test_api_contract.py)**
   - Property-based contract testing with Schemathesis
   - ⚠️ Currently skipped (OpenAPI 3.1.0 compatibility)
   - See [Contract Testing Guide](../../docs/guides/CONTRACT_TESTING.md) for full explanation

**💡 Advanced API Testing (Optional):**

Contract testing automatically generates hundreds of test cases from your API schema. While the backend Schemathesis test is currently skipped, you can:

- Learn the concept: [Contract Testing Guide](../../docs/guides/CONTRACT_TESTING.md)
- Try frontend contracts: [Lab 6C](exercises/LAB_06C_Frontend_Integration_Testing.md) (works today!)
- Use Postman collections above for manual contract validation

---

## 🔍 What to Look For

### 1. E2E Test Structure

```python
async def test_user_can_create_post(page, login):
    # Arrange - User is logged in (via login fixture)
    await page.goto("http://localhost:3000/feed")

    # Act - Complete user workflow
    await page.fill("#post-input", "Hello World!")
    await page.click("#submit-post")

    # Assert - Verify UI updated
    await expect(page.locator(".post-content").first).to_have_text("Hello World!")
```

**Key observations:**

- Tests real browser interactions
- Uses actual URLs and selectors
- Verifies visual/UI elements
- Async/await for browser operations

### 2. Page Object Model (POM)

```python
class FeedPage:
    def __init__(self, page):
        self.page = page
        self.post_input = page.locator("#post-input")
        self.submit_button = page.locator("#submit-post")

    async def create_post(self, content):
        await self.post_input.fill(content)
        await self.submit_button.click()
```

**Benefits:**

- Reusable page interactions
- Centralized selectors
- Easier maintenance
- More readable tests

### 3. Waiting and Timing

```python
# Wait for element to appear
await page.wait_for_selector(".post-content")

# Wait for navigation
await page.wait_for_url("**/feed")

# Wait for API response
async with page.expect_response("**/api/posts") as response:
    await page.click("#submit-post")
```

**E2E tests must handle:**

- Network delays
- Animations
- Async operations
- Load times

### 4. Contract Testing

```python
def test_api_response_matches_schema(client):
    response = client.get("/posts")
    data = response.json()

    # Validate structure
    assert "posts" in data
    assert isinstance(data["posts"], list)

    # Validate schema
    for post in data["posts"]:
        assert "id" in post
        assert "title" in post
        assert "created_at" in post
```

**Contract tests ensure:**

- API structure doesn't break
- Required fields are present
- Data types are correct
- Backwards compatibility

### 5. Visual Testing

```python
# Take screenshot
await page.screenshot(path="test-result.png")

# Full page screenshot
await page.screenshot(path="full-page.png", full_page=True)

# Video recording (configured in playwright.config)
```

**Visual artifacts help:**

- Debug failures
- Document bugs
- Communicate with team
- Create demos

---

## 🏃 How to Practice

### Step 1: Run E2E Tests

#### Python E2E

```bash
cd tests/e2e-python
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pytest -v
```

#### JavaScript E2E

```bash
cd tests
npx playwright test
```

**Watch the browser!** E2E tests are visual - see what happens.

### Step 2: Run in Headed Mode

See the browser while tests run:

```bash
# Python
HEADLESS=false pytest -v

# JavaScript
npx playwright test --headed
```

**This is amazing for learning!** Watch each step.

### Step 3: Explore Page Objects

Open `tests/e2e-python/pages/feed_page.py`:

**Questions:**

1. What interactions are abstracted?
2. How do page objects reduce duplication?
3. What happens if a selector changes?

### Step 4: Test a Complete Flow

Trace a full user journey:

1. Find `test_user_can_login_and_create_post`
2. List every step the test performs
3. Run it in headed mode
4. Identify what could fail at each step

### Step 5: Run Contract Tests

```bash
cd tests/api

# Using Newman (if installed)
newman run Testbook.postman_collection.json

# Or using Python
cd ../../backend
pytest tests/integration/test_api_contract.py -v
```

**Check:** Do all endpoints return expected schemas?

### Step 6: Write an E2E Test

Add a test for viewing a user profile:

```python
@pytest.mark.e2e
async def test_view_user_profile(page, login, test_user):
    """User can view another user's profile."""
    # Navigate to user profile
    await page.goto(f"http://localhost:3000/profile/{test_user.username}")

    # Verify profile loaded
    await expect(page.locator(".profile-username")).to_have_text(test_user.username)

    # Verify posts are visible
    await expect(page.locator(".user-posts")).to_be_visible()
```

---

## ✅ Success Criteria

You're ready for Stage 4 when you can:

- [ ] Explain when to use E2E vs integration tests
- [ ] Write a basic Playwright test
- [ ] Use Page Object Model effectively
- [ ] Handle waits and async operations
- [ ] Debug E2E test failures using screenshots
- [ ] Understand API contract testing
- [ ] Test complete multi-step user workflows
- [ ] Choose appropriate test granularity (unit vs integration vs E2E)

---

## 🧠 Why This Matters

### In Real QA Teams

- **E2E tests catch UI bugs** - Issues integration tests miss
- **Contract tests prevent breaking changes** - Frontend/backend stay in sync
- **User perspective** - Tests verify actual user experience
- **Cross-browser testing** - Works on Chrome, Firefox, Safari
- **Visual regression** - Screenshots show unexpected changes

### For Your Career

- **High-value skill** - E2E testing is in huge demand
- **Tool expertise** - Playwright is industry-leading
- **Full-stack knowledge** - Understand frontend + backend + UI
- **Debugging ability** - E2E tests teach systematic troubleshooting
- **Portfolio demos** - Videos/screenshots showcase your work

---

## 💡 Key Concepts

### Testing Pyramid Extended

```text
       /\      ← Manual exploratory testing
      /  \     ← Few E2E tests (slowest, most expensive)
     /____\
    /      \   ← Some API/contract tests
   /________\
  /          \ ← More integration tests
 /____________\
/              \ ← Many unit tests (fastest, cheapest)
```

**E2E tests are at the top:**

- Most realistic
- Catch the most critical bugs
- But slowest and most fragile
- Use sparingly for key workflows

### When to Use Each Test Type

| Test Type       | When to Use         | Example                          |
| --------------- | ------------------- | -------------------------------- |
| **Unit**        | Test business logic | Password hashing function        |
| **Integration** | Test API endpoints  | POST /posts returns 201          |
| **E2E**         | Test user workflows | User logs in and creates post    |
| **Contract**    | Verify API schemas  | /posts returns correct structure |

### E2E Best Practices

✅ **DO:**

- Test critical user paths
- Use Page Object Model
- Run in CI/CD pipeline
- Capture screenshots on failure
- Keep tests independent

❌ **DON'T:**

- Test every edge case with E2E
- Hard-code waits (use smart waits)
- Test API logic in E2E
- Make tests depend on each other
- Ignore flaky tests

---

## 🚀 Advanced E2E Patterns (Dual-Path Content)

This section provides advanced E2E testing patterns for both Playwright Python and Playwright JavaScript, enabling learners to master professional E2E testing regardless of their stack preference.

### 🎯 Learning Objectives

By the end of this section, you will be able to:

- ✅ Implement Page Object Model in both Python and JavaScript
- ✅ Create advanced fixtures for complex test scenarios
- ✅ Handle dynamic content and async operations
- ✅ Intercept and mock network requests
- ✅ Run tests across multiple browsers
- ✅ Implement retry strategies and error handling
- ✅ Capture screenshots and videos for debugging
- ✅ Set up E2E tests in CI/CD pipelines

### 🗺️ Choose Your Path

This section provides parallel content for both stacks. You can:

1. **Follow your primary stack** (Python OR JavaScript)
2. **Learn both** to understand full-stack E2E testing
3. **Compare approaches** using the [Testing Comparison Guide](../../docs/guides/TESTING_COMPARISON_PYTHON_JS.md)

---

## Part 1: Page Object Model (Both Stacks)

The Page Object Model (POM) is a design pattern that creates an object repository for web elements, making tests more maintainable and reusable.

### Why Use Page Object Model?

**Without POM (❌ Brittle):**

```python
# Every test duplicates selectors
def test_login():
    page.fill('[data-testid="email"]', 'user@test.com')
    page.fill('[data-testid="password"]', 'pass')
    page.click('[data-testid="submit"]')

def test_register():
    page.fill('[data-testid="email"]', 'new@test.com')
    # If selector changes, must update ALL tests!
```

**With POM (✅ Maintainable):**

```python
# Update selector in ONE place
class LoginPage:
    def login(self, email, password):
        self.page.fill(self.email_input, email)
        self.page.fill(self.password_input, password)
        self.page.click(self.submit_button)
```

### 🐍 Python Implementation

**Step 1: Create Base Page Class**

```python
# tests/e2e-python/pages/base_page.py
from playwright.sync_api import Page, expect

class BasePage:
    """Base class for all page objects."""

    def __init__(self, page: Page, base_url: str = "http://localhost:3000"):
        self.page = page
        self.base_url = base_url

    def goto(self, path: str = "") -> None:
        """Navigate to a specific path."""
        url = f"{self.base_url}{path}"
        self.page.goto(url)

    def wait_for_load(self) -> None:
        """Wait for page to fully load."""
        self.page.wait_for_load_state("networkidle", timeout=10000)

    def screenshot(self, name: str) -> None:
        """Take a screenshot."""
        self.page.screenshot(path=f"screenshots/{name}.png")
```

**Step 2: Create Specific Page Objects**

```python
# tests/e2e-python/pages/feed_page.py
from playwright.sync_api import Page, expect, Locator
from .base_page import BasePage

class FeedPage(BasePage):
    """Page object for the Feed page."""

    def __init__(self, page: Page):
        super().__init__(page)

        # Selectors
        self.navbar = '[data-testid="navbar"]'
        self.create_post_textarea = '[data-testid="create-post-textarea"]'
        self.create_post_submit = '[data-testid="create-post-submit"]'
        self.post_items = '[data-testid-generic="post-item"]'
        self.post_delete_button = '[data-testid$="-delete-button"]'
        self.post_react_button = '[data-testid$="-react-button"]'

    def goto(self) -> None:
        """Navigate to feed page."""
        super().goto("/")
        expect(self.page.locator(self.navbar)).to_be_visible(timeout=10000)

    def create_post(self, content: str) -> None:
        """Create a new post."""
        self.page.fill(self.create_post_textarea, content)
        self.page.click(self.create_post_submit)
        self.page.wait_for_timeout(500)

        # Verify post appeared
        expect(self.first_post()).to_contain_text(content)

    def first_post(self) -> Locator:
        """Get the first (most recent) post."""
        return self.page.locator(self.post_items).first

    def all_posts(self) -> Locator:
        """Get all posts."""
        return self.page.locator(self.post_items)

    def post_count(self) -> int:
        """Count visible posts."""
        return self.all_posts().count()

    def find_post_by_content(self, content: str) -> Locator:
        """Find a specific post by its content."""
        return self.page.locator(self.post_items, has_text=content)

    def delete_post(self, post: Locator) -> None:
        """Delete a specific post."""
        post.locator(self.post_delete_button).click()
        self.page.wait_for_timeout(500)

    def react_to_post(self, post: Locator, reaction: str = "like") -> None:
        """Add a reaction to a post."""
        post.locator(self.post_react_button).hover()
        self.page.wait_for_timeout(200)
        post.locator(f'[data-testid$="-reaction-{reaction}"]').click()
        self.page.wait_for_timeout(300)
```

**Step 3: Use in Tests**

```python
# tests/e2e-python/test_with_pom.py
import pytest
from playwright.sync_api import Page
from pages.feed_page import FeedPage

@pytest.mark.pom
class TestFeedWithPOM:
    """Tests using Page Object Model."""

    def test_create_post(self, page: Page, login_as, fresh_database):
        """Test creating a post using POM."""
        login_as("sarah")

        feed = FeedPage(page)
        feed.goto()

        # Clean, readable test code
        feed.create_post("Testing with Page Objects!")

        assert feed.post_count() >= 1
        assert "Testing with Page Objects!" in feed.first_post().inner_text()

    def test_delete_post(self, page: Page, login_as, fresh_database):
        """Test deleting a post using POM."""
        login_as("sarah")

        feed = FeedPage(page)
        feed.goto()

        # Create and delete a post
        feed.create_post("Post to delete")
        initial_count = feed.post_count()

        feed.delete_post(feed.first_post())

        assert feed.post_count() == initial_count - 1
```

### 🟨 JavaScript Implementation

**Step 1: Create Base Page Class**

```javascript
// tests/e2e/pages/BasePage.js
const { expect } = require("@playwright/test");

class BasePage {
  constructor(page, baseURL = "http://localhost:3000") {
    this.page = page;
    this.baseURL = baseURL;
  }

  async goto(path = "") {
    const url = `${this.baseURL}${path}`;
    await this.page.goto(url);
  }

  async waitForLoad() {
    await this.page.waitForLoadState("networkidle", { timeout: 10000 });
  }

  async screenshot(name) {
    await this.page.screenshot({ path: `screenshots/${name}.png` });
  }
}

module.exports = { BasePage };
```

**Step 2: Create Specific Page Objects**

```javascript
// tests/e2e/pages/FeedPage.js
const { expect } = require("@playwright/test");
const { BasePage } = require("./BasePage");

class FeedPage extends BasePage {
  constructor(page) {
    super(page);

    // Selectors
    this.navbar = '[data-testid="navbar"]';
    this.createPostTextarea = '[data-testid="create-post-textarea"]';
    this.createPostSubmit = '[data-testid="create-post-submit"]';
    this.postItems = '[data-testid-generic="post-item"]';
    this.postDeleteButton = '[data-testid$="-delete-button"]';
    this.postReactButton = '[data-testid$="-react-button"]';
  }

  async goto() {
    await super.goto("/");
    await expect(this.page.locator(this.navbar)).toBeVisible({
      timeout: 10000,
    });
  }

  async createPost(content) {
    await this.page.fill(this.createPostTextarea, content);
    await this.page.click(this.createPostSubmit);
    await this.page.waitForTimeout(500);

    // Verify post appeared
    await expect(this.firstPost()).toContainText(content);
  }

  firstPost() {
    return this.page.locator(this.postItems).first();
  }

  allPosts() {
    return this.page.locator(this.postItems);
  }

  async postCount() {
    return await this.allPosts().count();
  }

  findPostByContent(content) {
    return this.page.locator(this.postItems, { hasText: content });
  }

  async deletePost(post) {
    await post.locator(this.postDeleteButton).click();
    await this.page.waitForTimeout(500);
  }

  async reactToPost(post, reaction = "like") {
    await post.locator(this.postReactButton).hover();
    await this.page.waitForTimeout(200);
    await post.locator(`[data-testid$="-reaction-${reaction}"]`).click();
    await this.page.waitForTimeout(300);
  }
}

module.exports = { FeedPage };
```

**Step 3: Use in Tests**

```javascript
// tests/e2e/with-pom.spec.js
const { test, expect } = require("@playwright/test");
const { FeedPage } = require("./pages/FeedPage");
const { loginUser } = require("./fixtures/test-helpers");

test.describe("Feed with Page Object Model", () => {
  test("create post", async ({ page }) => {
    await loginUser(page, "sarah.johnson@testbook.com", "Sarah2024!");

    const feed = new FeedPage(page);
    await feed.goto();

    // Clean, readable test code
    await feed.createPost("Testing with Page Objects!");

    const count = await feed.postCount();
    expect(count).toBeGreaterThanOrEqual(1);
  });

  test("delete post", async ({ page }) => {
    await loginUser(page, "sarah.johnson@testbook.com", "Sarah2024!");

    const feed = new FeedPage(page);
    await feed.goto();

    // Create and delete a post
    await feed.createPost("Post to delete");
    const initialCount = await feed.postCount();

    await feed.deletePost(feed.firstPost());

    const finalCount = await feed.postCount();
    expect(finalCount).toBe(initialCount - 1);
  });
});
```

---

## Part 2: Advanced Fixtures

### 🐍 Python Advanced Fixtures

**Parametrized Fixtures**

```python
# tests/e2e-python/conftest.py

@pytest.fixture(params=["sarah", "mike", "emma"])
def any_user(request, login_as):
    """Parametrized fixture - test runs 3 times with different users."""
    user_key = request.param
    login_as(user_key)
    return user_key

@pytest.fixture
def authenticated_feed(page: Page, login_as) -> 'FeedPage':
    """Fixture that provides an authenticated feed page."""
    from pages.feed_page import FeedPage

    login_as("sarah")
    feed = FeedPage(page)
    feed.goto()
    return feed

@pytest.fixture
def create_test_posts(authenticated_feed):
    """Fixture factory for creating multiple posts."""
    def _create_posts(count: int = 3, prefix: str = "Test post"):
        posts = []
        for i in range(count):
            content = f"{prefix} {i+1}"
            authenticated_feed.create_post(content)
            posts.append(content)
        return posts

    return _create_posts
```

**Usage:**

```python
def test_with_any_user(any_user, feed_page, fresh_database):
    """This test runs 3 times - once per user!"""
    feed_page.goto()
    feed_page.create_post(f"Posted by {any_user}")
    assert feed_page.post_count() >= 1

def test_with_multiple_posts(authenticated_feed, create_test_posts):
    """Test with pre-created posts."""
    posts = create_test_posts(count=5)

    assert authenticated_feed.post_count() >= 5

    for content in posts:
        assert authenticated_feed.find_post_by_content(content).is_visible()
```

### 🟨 JavaScript Advanced Fixtures

**Custom Fixtures**

```javascript
// tests/e2e/fixtures/custom-fixtures.js
const { test as base } = require('@playwright/test');
const { FeedPage } = require('../pages/FeedPage');
const { loginUser } = require('./test-helpers');

const test = base.extend({
  // Authenticated page fixture
  authenticatedPage: async ({ page }, use) => {
    await loginUser(page, 'sarah.johnson@testbook.com', 'Sarah2024!');
    await use(page);
  },

  // Feed page fixture
  feedPage: async ({ page }, use) => {
    const feed = new FeedPage(page);
    await use(feed);
  },

  // Authenticated feed fixture
  authenticatedFeed: async ({ page }, use) => {
    await loginUser(page, 'sarah.johnson@testbook.com', 'Sarah2024!');
    const feed = new FeedPage(page);
    await feed.goto();
    await use(feed);
  },

  // Network mock fixture
  mockEmptyFeed: async ({ page }, use) => {
    await page.route('**/api/feed**', route => {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([]),
      });
    });
    await use(page);
  },
});

module.exports = { test };
```

**Usage:**

```javascript
const { test, expect } = require("./fixtures/custom-fixtures");

test("with authenticated feed fixture", async ({ authenticatedFeed }) => {
  // Already logged in and on feed page!
  await authenticatedFeed.createPost("Using fixture!");
  const count = await authenticatedFeed.postCount();
  expect(count).toBeGreaterThanOrEqual(1);
});

test("with mocked empty feed", async ({ mockEmptyFeed, feedPage }) => {
  await feedPage.goto();
  // Feed will be empty due to mock
  await expect(mockEmptyFeed.locator("text=/no posts/i")).toBeVisible();
});
```

---

## Part 3: Network Interception & Mocking

### 🐍 Python Network Interception

```python
import json
from playwright.sync_api import Page, Route

def test_mock_api_error(page: Page, login_as, fresh_database):
    """Test handling of API errors with network mocking."""
    login_as("sarah")

    # Mock the feed API to return error
    def handle_route(route: Route):
        route.fulfill(
            status=500,
            content_type="application/json",
            body=json.dumps({"detail": "Server error"})
        )

    page.route("**/api/feed**", handle_route)

    page.goto("http://localhost:3000")

    # Should show error message
    from playwright.sync_api import expect
    expect(page.locator("text=/error.*loading/i")).to_be_visible(timeout=5000)

def test_mock_slow_network(page: Page, login_as):
    """Simulate slow network to test loading states."""
    login_as("sarah")

    def handle_route(route: Route):
        import time
        time.sleep(2)  # 2 second delay
        route.continue_()

    page.route("**/api/feed**", handle_route)

    page.goto("http://localhost:3000")

    # Should show loading indicator
    from playwright.sync_api import expect
    expect(page.locator('[role="status"]')).to_be_visible(timeout=1000)
```

### 🟨 JavaScript Network Interception

```javascript
const { test, expect } = require("@playwright/test");

test("mock API error", async ({ page }) => {
  await loginUser(page, "sarah.johnson@testbook.com", "Sarah2024!");

  // Mock the feed API to return error
  await page.route("**/api/feed**", (route) => {
    route.fulfill({
      status: 500,
      contentType: "application/json",
      body: JSON.stringify({ detail: "Server error" }),
    });
  });

  await page.goto("http://localhost:3000");

  // Should show error message
  await expect(page.locator("text=/error.*loading/i")).toBeVisible({
    timeout: 5000,
  });
});

test("mock slow network", async ({ page }) => {
  await loginUser(page, "sarah.johnson@testbook.com", "Sarah2024!");

  // Add delay to API responses
  await page.route("**/api/feed**", async (route) => {
    await new Promise((resolve) => setTimeout(resolve, 2000)); // 2 second delay
    await route.continue();
  });

  await page.goto("http://localhost:3000");

  // Should show loading indicator
  await expect(page.locator('[role="status"]')).toBeVisible({ timeout: 1000 });
});
```

---

## Part 4: Multi-Browser Testing

### Configuration

**Python: pytest.ini**

```ini
[pytest]
markers =
    chromium: Run in Chromium
    firefox: Run in Firefox
    webkit: Run in Safari/WebKit
```

**JavaScript: playwright.config.js**

```javascript
module.exports = {
  projects: [
    {
      name: "chromium",
      use: { browserName: "chromium" },
    },
    {
      name: "firefox",
      use: { browserName: "firefox" },
    },
    {
      name: "webkit",
      use: { browserName: "webkit" },
    },
  ],
};
```

### Running Multi-Browser Tests

**Python:**

```bash
# Install browsers
playwright install chromium  # Chrome only for faster setup
playwright install firefox webkit  # Additional browsers if needed

# Run parametrized across browsers
pytest --browser chromium
pytest --browser firefox
pytest --browser webkit
```

**JavaScript:**

```bash
# Install browsers
npx playwright install chromium  # Chrome only for faster setup
npx playwright install firefox webkit  # Additional browsers if needed

# Run all projects
npx playwright test

# Run specific browser
npx playwright test --project=firefox
```

---

## Part 5: CI/CD Integration

See the [CI/CD section in Stage 5](../stage_5_capstone/README.md#cicd-automation) for detailed CI setup for both Python and JavaScript E2E tests.

**Quick GitHub Actions Example:**

```yaml
name: E2E Tests
on: [push]
jobs:
  e2e-python:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
      - run: pip install -r tests/e2e-python/requirements.txt
      - run: playwright install chromium --with-deps # Chrome only for faster CI
      - run: HEADLESS=true pytest tests/e2e-python/

  e2e-javascript:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npx playwright install chromium --with-deps # Chrome only for faster CI
      - run: npx playwright test
```

---

## 🎓 Section Summary

You've learned advanced E2E patterns in both Python and JavaScript:

- ✅ **Page Object Model** - Maintainable, reusable test code
- ✅ **Advanced fixtures** - Powerful test setup and teardown
- ✅ **Network interception** - Test edge cases and errors
- ✅ **Multi-browser testing** - Ensure cross-browser compatibility
- ✅ **CI/CD integration** - Automated testing in pipelines

---

## 📚 Next Steps

1. **Complete [Lab 4B (Python)](exercises/LAB_04B_Advanced_E2E_Python.md)** - Advanced Python patterns
2. **Review [Testing Comparison Guide](../../docs/guides/TESTING_COMPARISON_PYTHON_JS.md)** - Compare Python vs JavaScript
3. **Practice Project:** Implement POM for entire test suite
4. **Advanced Topic:** Visual regression testing with Playwright

---

## 📖 Additional Resources

- [Playwright Python Documentation](https://playwright.dev/python/)
- [Playwright JavaScript Documentation](https://playwright.dev/)
- [pytest fixtures guide](https://docs.pytest.org/en/stable/fixture.html)
- [Playwright Best Practices](https://playwright.dev/docs/best-practices)

**🎉 You've mastered advanced E2E testing in both stacks! These are production-ready skills!**

---

## 🔗 Related Resources

### Hands-On Practice

- [Lab 4: E2E Testing (Python)](exercises/LAB_04_E2E_Testing_Python.md)
- [Lab 4: E2E Testing (JavaScript)](exercises/LAB_04_E2E_Testing_JavaScript.md)
- [Lab 4B: Advanced E2E (Python)](exercises/LAB_04B_Advanced_E2E_Python.md)
- [Lab 6B: Component Testing (JavaScript)](exercises/LAB_06B_Advanced_Component_Testing.md)
- [Lab 6C: Contract Testing (JavaScript)](exercises/LAB_06C_Frontend_Integration_Testing.md)

### Documentation

- [Playwright Documentation](https://playwright.dev/)
- [E2E Testing Guide](../../tests/e2e-python/README.md)
- [API Testing with Newman](../../tests/api/NEWMAN_GUIDE.md)

### Advanced Topics

- [Section 8: Advanced E2E Patterns](../../docs/course/SECTION_08_ADVANCED_E2E_PATTERNS.md)
- [Flaky Tests Guide](../../docs/guides/FLAKY_TESTS_GUIDE.md)

---

## 🧠 Self-Check Quiz (Optional)

Before moving to Stage 4, can you answer these questions?

1. **What's the main purpose of E2E testing?**

   - A) To test individual functions
   - B) To test complete user workflows
   - C) To test API endpoints
   - D) To test database operations

2. **What is the Page Object Model?**

   - A) A way to organize test files
   - B) A pattern for organizing page interactions
   - C) A method for running tests faster
   - D) A way to mock external services

3. **Why are E2E tests slower than unit tests?**

   - A) They test more code
   - B) They use real browsers and network requests
   - C) They're written in JavaScript
   - D) They test multiple functions

4. **What should you do when an E2E test fails?**

   - A) Always fix the test
   - B) Always fix the application
   - C) Investigate to determine if it's a test or app issue
   - D) Skip the test

5. **What's the difference between E2E and integration tests?**
   - A) E2E tests use browsers, integration tests don't
   - B) Integration tests are faster
   - C) E2E tests test the full stack
   - D) All of the above

**Answers:** [Check your answers here](solutions/stage_3_quiz_answers.md)

---

## 🤔 Reflection

Before moving to Stage 4, answer these:

1. **Why are E2E tests slower than integration tests? Is it worth the trade-off?**

2. **How does the Page Object Model make tests more maintainable?**

3. **Pick one E2E test. List 3 things that could cause it to fail (even if the app works fine).**

4. **What's the difference between testing an API with integration tests vs contract tests?**

5. **Imagine you're testing a shopping cart. What would you test with E2E vs integration tests?**

**Document your answers** in [reflection.md](reflection.md).

---

## 🎉 Stage Complete

You now understand full-stack testing from browser to database!

### 👉 [Continue to Stage 4: Performance & Security](../stage_4_performance_security/README.md)

---

_Pro tip: E2E testing is where QA engineers become invaluable. Master this, and you're a full-stack QA engineer! 🚀_
