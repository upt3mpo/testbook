# JavaScript Playwright E2E Tests

End-to-end tests for Testbook using JavaScript and Playwright Test.

---

<h2 id="quick-start">🚀 Quick Start</h2>

### 1. Install Dependencies

```bash
cd tests
npm install
npx playwright install chromium
```

**💡 Learning-Focused Configuration:** We configure Playwright to run only Chrome by default for faster execution. This reduces test time from ~5 minutes to ~1 minute, making the learning experience smoother. You can still run other browsers if needed for cross-browser testing.

### 2. Start Testbook

```bash
# From project root
./start-dev.sh
```

### 3. Run Tests

```bash
# Run all tests (Chrome only by default)
npm test

# Run all browsers (slower)
npm run test:all-browsers

# Run specific test file
npx playwright test auth.spec.js

# Run with visible browser (headed mode)
npm run test:headed

# Run in debug mode (step through tests)
npm run test:debug
```

---

<h2 id="configuration">⚙️ Configuration</h2>

### Environment Variables

Tests can be configured via environment variables. Configuration is managed through:

1. **Default values** in `playwright.config.js`
2. **Environment variables** (highest priority)
3. **`.env` file** in `tests/` directory

**Create `.env` file:**

```bash
cp env.example .env
# Then edit .env with your settings
```

### Available Configuration

| Variable      | Default                 | Description                 |
| ------------- | ----------------------- | --------------------------- |
| `BASE_URL`    | `http://localhost:3000` | Frontend URL                |
| `BACKEND_URL` | `http://localhost:8000` | Backend API URL             |
| `HEADLESS`    | `true`                  | Run in headless mode        |
| `CI`          | `false`                 | Enable CI-specific behavior |

**Override at runtime:**

```bash
BASE_URL=http://localhost:3000 npx playwright test
```

---

<h2 id="test-helpers">🧪 Test Helpers</h2>

All test helpers are in `fixtures/test-helpers.js`:

### Database Management

**`resetDatabase(page)`** - Reset database to clean state

```javascript
const { resetDatabase } = require("./fixtures/test-helpers");

test("my test", async ({ page }) => {
  await resetDatabase(page);
  // Database is now clean
});
```

**`seedDatabase(page, scenario)`** - Seed specific test data

```javascript
await seedDatabase(page, "users_with_posts");
```

### User Authentication

**`loginUser(page, email, password)`** - Login a user

```javascript
const { loginUser, TEST_USERS } = require("./fixtures/test-helpers");

test("my test", async ({ page }) => {
  await loginUser(page, TEST_USERS.sarah.email, TEST_USERS.sarah.password);
  // Now logged in
});
```

**`registerUser(page, userData)`** - Register new user

```javascript
await registerUser(page, {
  email: "newuser@example.com",
  username: "newuser",
  displayName: "New User",
  password: "Password123!",
});
```

### Post Management

**`createPost(page, content)`** - Create a post

```javascript
const { createPost } = require("./fixtures/test-helpers");

await createPost(page, "This is my test post!");
```

**`getFirstPost(page)`** - Get first post locator

```javascript
const post = getFirstPost(page);
await expect(post).toContainText("my post");
```

**`getPostsByAuthor(page, username)`** - Get posts by specific author

```javascript
const posts = getPostsByAuthor(page, "sarahjohnson");
```

### Interactions

**`addReaction(post, reactionType)`** - Add reaction to post

```javascript
const post = getFirstPost(page);
await addReaction(post, "like");
```

**`addComment(post, commentText)`** - Add comment to post

```javascript
const post = getFirstPost(page);
await addComment(post, "Great post!");
```

### Test Users

Pre-configured test users available in `TEST_USERS`:

```javascript
const { TEST_USERS } = require("./fixtures/test-helpers");

TEST_USERS.sarah; // Sarah Johnson
TEST_USERS.mike; // Mike Chen
TEST_USERS.emma; // Emma Davis
TEST_USERS.newuser; // For registration tests
```

---

## 📁 Test Structure

```text
tests/e2e/
├── fixtures/
│   └── test-helpers.js      # Reusable helper functions
├── auth.spec.js             # Authentication tests
├── posts.spec.js            # Post creation/interaction tests
├── users.spec.js            # User profile tests
└── README.md                # This file
```

---

<h2 id="writing-tests">🎯 Writing Tests</h2>

### Basic Test Example

```javascript
const { test, expect } = require("@playwright/test");
const { loginUser, TEST_USERS } = require("./fixtures/test-helpers");

test("user can create post", async ({ page }) => {
  // Login
  await loginUser(page, TEST_USERS.sarah.email, TEST_USERS.sarah.password);

  // Create post
  await page.fill('[data-testid="create-post-textarea"]', "Test post!");
  await page.click('[data-testid="create-post-submit-button"]');

  // Verify
  await expect(page.locator('text="Test post!"')).toBeVisible();
});
```

### Using Test Helpers

```javascript
const { test, expect } = require("@playwright/test");
const {
  resetDatabase,
  loginUser,
  createPost,
  getFirstPost,
  TEST_USERS,
} = require("./fixtures/test-helpers");

test("complete post flow", async ({ page }) => {
  // Reset database first
  await resetDatabase(page);

  // Login
  await loginUser(page, TEST_USERS.sarah.email, TEST_USERS.sarah.password);

  // Create post
  await createPost(page, "My test post");

  // Verify post appears
  const post = getFirstPost(page);
  await expect(post).toContainText("My test post");
});
```

### Test Hooks

```javascript
test.describe("Post Tests", () => {
  test.beforeEach(async ({ page }) => {
    // Reset database before each test
    await resetDatabase(page);

    // Login
    await loginUser(page, TEST_USERS.sarah.email, TEST_USERS.sarah.password);
  });

  test("create post", async ({ page }) => {
    // Test already logged in due to beforeEach
    await createPost(page, "Test");
  });
});
```

---

<h2 id="debugging-tests">🐛 Debugging Tests</h2>

### Run with Visible Browser

```bash
# See the browser
npx playwright test --headed

# Slow motion (helps see what's happening)
npx playwright test --headed --slow-mo=1000
```

### Debug Mode

```bash
# Opens Playwright Inspector
npx playwright test --debug

# Debug specific test
npx playwright test auth.spec.js --debug
```

### Using Pause

```javascript
test("my test", async ({ page }) => {
  await page.goto("/");

  await page.pause(); // Test pauses here - you can inspect

  // Continue test...
});
```

### Screenshots & Videos

Screenshots are automatically taken on failure.

Videos are recorded only on failure (if configured).

**Manual screenshot:**

```javascript
await page.screenshot({ path: "screenshot.png" });
```

---

<h2 id="running-specific-tests">🏃 Running Specific Tests</h2>

### By File

```bash
npx playwright test auth.spec.js
```

### By Pattern

```bash
npx playwright test login
```

### Specific Test

```bash
npx playwright test auth.spec.js:10  # Line number
```

### By Browser

```bash
# Test only in Chromium
npx playwright test --project=chromium

# Test only in Firefox
npx playwright test --project=firefox
```

---

<h2 id="test-reports">📊 Test Reports</h2>

### HTML Report

```bash
# Run tests
npx playwright test

# View report manually (configured to NOT auto-open)
npx playwright show-report

# Or directly open the file
open playwright-report/index.html  # macOS
```

**Note:** The HTML report is configured with `open: 'never'` to prevent auto-opening after tests complete. This allows tests to finish cleanly in CI/CD and automation scenarios.

### Trace Viewer (for failures)

```bash
# Run with trace
npx playwright test --trace on

# View trace
npx playwright show-trace trace.zip
```

---

<h2 id="troubleshooting">🔧 Troubleshooting</h2>

### "net::ERR_CONNECTION_REFUSED"

**Problem:** Cannot connect to app

**Solutions:**

1. Start the app: `./start-dev.sh`
2. Verify frontend runs: open `http://localhost:3000`
3. Check `BASE_URL` in config

### "Timeout 30000ms exceeded"

**Problem:** Element not found or action timed out

**Solutions:**

1. Run in headed mode: `npx playwright test --headed`
2. Check `data-testid` attribute is correct
3. Ensure element is visible and enabled
4. Add explicit wait: `await page.waitForSelector('[data-testid="..."]')`

### "Database reset failed"

**Problem:** Cannot reset database

**Solutions:**

1. Check backend is running: `curl http://localhost:8000/docs`
2. Verify `/api/dev/reset` endpoint exists
3. Update `BACKEND_URL` if needed

### Tests Pass Individually but Fail Together

**Problem:** Test isolation issues

**Solutions:**

1. Use `resetDatabase()` in `beforeEach` hooks
2. Don't share state between tests
3. Run tests serially: `npx playwright test --workers=1`

---

<h2 id="best-practices">📚 Best Practices</h2>

### ✅ Do

- Use `data-testid` attributes for selectors
- Use `expect()` with auto-retry
- Reset database for isolated tests
- Use test helpers for common operations
- Write independent tests

### ❌ Don't

- Use `page.waitForTimeout()` - use explicit waits
- Hardcode URLs - use `page.goto('/')` with baseURL
- Chain too many actions without assertions
- Share state between tests
- Use fragile CSS selectors

---

## 🎯 Example Patterns

### Complete User Flow

```javascript
test("complete user journey", async ({ page }) => {
  const {
    loginUser,
    createPost,
    getFirstPost,
    addReaction,
    TEST_USERS,
  } = require("./fixtures/test-helpers");

  // Login
  await loginUser(page, TEST_USERS.sarah.email, TEST_USERS.sarah.password);

  // Create post
  await createPost(page, "Hello Testbook!");

  // React to post
  const post = getFirstPost(page);
  await addReaction(post, "like");

  // Verify
  await expect(post).toContainText("Hello Testbook!");
});
```

### API Setup + UI Verification

```javascript
test("verify post created via API", async ({ page, request }) => {
  // Setup via API (faster)
  const response = await request.post("http://localhost:8000/api/posts", {
    headers: { Authorization: `Bearer ${token}` },
    data: { content: "Test post" },
  });

  // Verify via UI
  await loginUser(page, TEST_USERS.sarah.email, TEST_USERS.sarah.password);
  await expect(page.locator('text="Test post"')).toBeVisible();
});
```

---

## 🔗 Related Documentation

- [Playwright Test Docs](https://playwright.dev/docs/intro)
- [Main Testing Guide](../../docs/guides/RUNNING_TESTS.md)
- [Lab 4: E2E Testing (JavaScript)](../../learn/stage_3_api_e2e/exercises/LAB_04_E2E_Testing_JavaScript.md)
- [Python E2E Tests](../e2e-python/README.md) (alternative approach)
- [Test Alignment Guide](./E2E_TEST_ALIGNMENT.md) (JS vs Python differences)

---

## 🎯 JavaScript-Specific Tests

### Accessibility Tests (`accessibility-axe.spec.js`)

**Why JavaScript-only?**

- `axe-core` is the industry-standard accessibility testing library (by Deque)
- `@axe-core/playwright` integration is mature and well-maintained
- WCAG 2.1 compliance testing is more commonly done in JavaScript environments
- Python accessibility tools (axe-playwright-python) are less mature

**What it tests:**

- ✅ WCAG 2.1 Level A and AA compliance
- ✅ Color contrast ratios
- ✅ ARIA attributes and semantic HTML
- ✅ Keyboard navigation accessibility
- ✅ Screen reader compatibility

**Career Value:**

- Accessibility testing is a specialized, high-demand skill
- Shows awareness of inclusive design and legal compliance (ADA)
- Many companies require WCAG compliance for their products

**Interview Talking Points:**

> "For Testbook, I implemented automated accessibility testing using axe-core and Playwright to ensure WCAG 2.1 AA compliance across all pages. This catches ~40% of accessibility issues automatically, which I then complement with manual keyboard navigation and screen reader testing."

---

## 💡 Tips

- **Use --headed for development:** See what's happening
- **Use --debug for failures:** Step through problematic tests
- **Use test helpers:** Don't repeat login/setup code
- **Reset database liberally:** Isolation prevents flaky tests
- **Check the HTML report:** Great for understanding failures

---

**Happy Testing!** 🚀
