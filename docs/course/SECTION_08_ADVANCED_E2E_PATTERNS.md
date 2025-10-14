# 📘 Section 8: Advanced E2E Testing Patterns

**Dual-Path Content: Python & JavaScript**

This section provides advanced E2E testing patterns for both Playwright Python and Playwright JavaScript, enabling learners to master professional E2E testing regardless of their stack preference.

---

## 🎯 Learning Objectives

By the end of this section, you will be able to:

- ✅ Implement Page Object Model in both Python and JavaScript
- ✅ Create advanced fixtures for complex test scenarios
- ✅ Handle dynamic content and async operations
- ✅ Intercept and mock network requests
- ✅ Run tests across multiple browsers
- ✅ Implement retry strategies and error handling
- ✅ Capture screenshots and videos for debugging
- ✅ Set up E2E tests in CI/CD pipelines

---

## 📚 Prerequisites

- **Required:** Lab 4 (E2E Testing) completed in either Python or JavaScript
- **Recommended:** Understanding of async/await (for JavaScript track)
- **Recommended:** Understanding of pytest fixtures (for Python track)

---

## 🗺️ Choose Your Path

This section provides parallel content for both stacks. You can:

1. **Follow your primary stack** (Python OR JavaScript)
2. **Learn both** to understand full-stack E2E testing
3. **Compare approaches** using the [Testing Comparison Guide](../guides/TESTING_COMPARISON_PYTHON_JS.md)

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

---

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

---

### 🟨 JavaScript Implementation

**Step 1: Create Base Page Class**

```javascript
// tests/e2e/pages/BasePage.js
const { expect } = require('@playwright/test');

class BasePage {
  constructor(page, baseURL = 'http://localhost:3000') {
    this.page = page;
    this.baseURL = baseURL;
  }

  async goto(path = '') {
    const url = `${this.baseURL}${path}`;
    await this.page.goto(url);
  }

  async waitForLoad() {
    await this.page.waitForLoadState('networkidle', { timeout: 10000 });
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
const { expect } = require('@playwright/test');
const { BasePage } = require('./BasePage');

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
    await super.goto('/');
    await expect(this.page.locator(this.navbar)).toBeVisible({ timeout: 10000 });
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

  async reactToPost(post, reaction = 'like') {
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
const { test, expect } = require('@playwright/test');
const { FeedPage } = require('./pages/FeedPage');
const { loginUser } = require('./fixtures/test-helpers');

test.describe('Feed with Page Object Model', () => {
  test('create post', async ({ page }) => {
    await loginUser(page, 'sarah.johnson@testbook.com', 'Sarah2024!');

    const feed = new FeedPage(page);
    await feed.goto();

    // Clean, readable test code
    await feed.createPost('Testing with Page Objects!');

    const count = await feed.postCount();
    expect(count).toBeGreaterThanOrEqual(1);
  });

  test('delete post', async ({ page }) => {
    await loginUser(page, 'sarah.johnson@testbook.com', 'Sarah2024!');

    const feed = new FeedPage(page);
    await feed.goto();

    // Create and delete a post
    await feed.createPost('Post to delete');
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

---

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
const { test, expect } = require('./fixtures/custom-fixtures');

test('with authenticated feed fixture', async ({ authenticatedFeed }) => {
  // Already logged in and on feed page!
  await authenticatedFeed.createPost('Using fixture!');
  const count = await authenticatedFeed.postCount();
  expect(count).toBeGreaterThanOrEqual(1);
});

test('with mocked empty feed', async ({ mockEmptyFeed, feedPage }) => {
  await feedPage.goto();
  // Feed will be empty due to mock
  await expect(mockEmptyFeed.locator('text=/no posts/i')).toBeVisible();
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

---

### 🟨 JavaScript Network Interception

```javascript
const { test, expect } = require('@playwright/test');

test('mock API error', async ({ page }) => {
  await loginUser(page, 'sarah.johnson@testbook.com', 'Sarah2024!');

  // Mock the feed API to return error
  await page.route('**/api/feed**', route => {
    route.fulfill({
      status: 500,
      contentType: 'application/json',
      body: JSON.stringify({ detail: 'Server error' }),
    });
  });

  await page.goto('http://localhost:3000');

  // Should show error message
  await expect(page.locator('text=/error.*loading/i')).toBeVisible({ timeout: 5000 });
});

test('mock slow network', async ({ page }) => {
  await loginUser(page, 'sarah.johnson@testbook.com', 'Sarah2024!');

  // Add delay to API responses
  await page.route('**/api/feed**', async route => {
    await new Promise(resolve => setTimeout(resolve, 2000)); // 2 second delay
    await route.continue();
  });

  await page.goto('http://localhost:3000');

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
      name: 'chromium',
      use: { browserName: 'chromium' },
    },
    {
      name: 'firefox',
      use: { browserName: 'firefox' },
    },
    {
      name: 'webkit',
      use: { browserName: 'webkit' },
    },
  ],
};
```

### Running Multi-Browser Tests

**Python:**

```bash
# Install browsers
playwright install firefox webkit

# Run parametrized across browsers
pytest --browser chromium
pytest --browser firefox
pytest --browser webkit
```

**JavaScript:**

```bash
# Install browsers
npx playwright install firefox webkit

# Run all projects
npx playwright test

# Run specific browser
npx playwright test --project=firefox
```

---

## Part 5: CI/CD Integration

See [CI/CD Documentation](./CI_CD_E2E_TESTING.md) for detailed CI setup for both Python and JavaScript E2E tests.

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
      - run: playwright install --with-deps
      - run: HEADLESS=true pytest tests/e2e-python/

  e2e-javascript:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npx playwright install --with-deps
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

1. **Complete [Lab 4B (Python)](../../labs/LAB_04B_Advanced_E2E_Python.md)** - Advanced Python patterns
2. **Review [Testing Comparison Guide](../guides/TESTING_COMPARISON_PYTHON_JS.md)** - Compare Python vs JavaScript
3. **Practice Project:** Implement POM for entire test suite
4. **Advanced Topic:** Visual regression testing with Playwright

---

## 📖 Additional Resources

- [Playwright Python Documentation](https://playwright.dev/python/)
- [Playwright JavaScript Documentation](https://playwright.dev/)
- [pytest fixtures guide](https://docs.pytest.org/en/stable/fixture.html)
- [Playwright Best Practices](https://playwright.dev/docs/best-practices)

**🎉 You've mastered advanced E2E testing in both stacks! These are production-ready skills!**
