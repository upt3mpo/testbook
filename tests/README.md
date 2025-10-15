# Testbook E2E Test Suite

End-to-end tests for Testbook using Playwright.

## Setup

### Prerequisites

```bash
# Install Node.js 18+ if not already installed

# Install dependencies
cd tests
npm install

# Install Playwright browsers
npx playwright install
```

## Running Tests

**⚠️ IMPORTANT:** Start Testbook in **development mode** first (port 3000)!

```bash
# In separate terminal - Start the app
./start-dev.sh  # macOS/Linux (NOT start.sh!)
start-dev.bat   # Windows

# Verify: http://localhost:3000 should load
```

### Port Configuration

These tests expect **port 3000** (configured in `playwright.config.js`):

- Frontend: <http://localhost:3000> ✅
- Backend: <http://localhost:8000>

**If using production mode** (`start.sh` - port 8000):

```bash
export BASE_URL=http://localhost:8000  # macOS/Linux
npm test
```

### Basic Commands

```bash
# Run all tests
npm test

# Run tests in headed mode (see browser)
npm run test:headed

# Run tests in UI mode (interactive)
npm run test:ui

# Run tests in debug mode
npm run test:debug

# Run specific browser only
npm run test:chromium
npm run test:firefox
npm run test:webkit

# Run mobile tests
npm run test:mobile
```

### Running Specific Tests

```bash
# Run specific test file
npx playwright test auth.spec.js

# Run tests matching pattern
npx playwright test --grep "login"

# Run tests in specific project
npx playwright test --project=chromium
```

## Test Structure

### Test Files

- `auth.spec.js` - Authentication flows (login, register, logout)
- `posts.spec.js` - Post operations (create, edit, delete, interact)
- `users.spec.js` - User profiles, follow/unfollow, settings

### Helper Functions

Located in `e2e/fixtures/test-helpers.js`:

- `resetDatabase()` - Reset DB to clean state
- `loginUser()` - Login with credentials
- `registerUser()` - Register new user
- `createPost()` - Create a post
- `getFirstPost()` - Get most recent post
- `addReaction()` - Add reaction to post
- `TEST_USERS` - Pre-seeded test user credentials

## Test Patterns

### Basic Test Structure

```javascript
test('should do something', async ({ page }) => {
  // Arrange
  await resetDatabase(page);
  await loginUser(page, TEST_USERS.sarah.email, TEST_USERS.sarah.password);

  // Act
  await page.click('[data-testid="some-button"]');

  // Assert
  await expect(page.locator('[data-testid="result"]')).toBeVisible();
});
```

### Using Test Helpers

```javascript
const { loginUser, createPost, getFirstPost, TEST_USERS } = require('./fixtures/test-helpers');

test('should create and view post', async ({ page }) => {
  await loginUser(page, TEST_USERS.sarah.email, TEST_USERS.sarah.password);
  await createPost(page, 'My test post');

  const firstPost = getFirstPost(page);
  await expect(firstPost).toContainText('My test post');
});
```

### Dynamic Content Selection

```javascript
// Get first post (most recent)
const firstPost = page.locator('[data-testid-generic="post-item"]').first();

// Get posts by specific author
const sarahPosts = page.locator('[data-post-author="sarahjohnson"]');

// Get own posts
const ownPosts = page.locator('[data-is-own-post="true"]');

// Interact with first own post
const ownPost = getFirstOwnPost(page);
await ownPost.locator('[data-testid$="-menu-button"]').click();
```

## Viewing Test Results

### HTML Report

```bash
# Generate and open HTML report
npm run report
```

### Screenshots and Videos

Failed tests automatically capture:

- Screenshots (on failure)
- Videos (on failure)
- Traces (on first retry)

Find them in `test-results/` directory.

## Configuration

Edit `playwright.config.js` to customize:

- Test timeout
- Retry strategy
- Parallel execution
- Browser projects
- Base URL
- Trace/screenshot settings

## Best Practices

1. **Reset database before each test** - Ensures clean state
2. **Use test helpers** - Reduces code duplication
3. **Use data-testid selectors** - More reliable than CSS/text
4. **Test user flows** - Not just individual features
5. **Add wait times carefully** - Use Playwright's auto-waiting when possible
6. **Keep tests independent** - Each test should run alone
7. **Use meaningful test names** - Describe what's being tested

## CI/CD Integration

Tests are automatically run in GitHub Actions. See `.github/workflows/e2e-tests.yml`.

## Debugging

### Debug Mode

```bash
# Run single test in debug mode
npx playwright test auth.spec.js --debug
```

### UI Mode

```bash
# Interactive test runner
npm run test:ui
```

### Trace Viewer

```bash
# View trace for failed test
npx playwright show-trace test-results/path-to-trace.zip
```

## Cross-Browser Testing

Tests run on:

- Chromium
- Firefox
- WebKit (Safari)
- Mobile Chrome
- Mobile Safari

Specify browser with `--project` flag:

```bash
npx playwright test --project=firefox
```

## Troubleshooting

### Backend not starting

Make sure backend is running:

```bash
cd backend
source .venv/bin/activate
uvicorn main:app --reload
```

### Browsers not installed

```bash
npx playwright install
```

### Port conflicts

Change `BASE_URL` in `playwright.config.js` or set environment variable:

```bash
BASE_URL=http://localhost:3000 npm test
```

### Flaky tests

- Use Playwright's auto-waiting (avoid `page.waitForTimeout`)
- Increase timeout for slow operations
- Check for race conditions
- Verify test data cleanup

## Learning Resources

- [Playwright Documentation](https://playwright.dev/)
- [Best Practices](https://playwright.dev/docs/best-practices)
- [Debugging Guide](https://playwright.dev/docs/debug)

## Writing New Tests

1. Create new `.spec.js` file in `e2e/` directory
2. Import test helpers
3. Add `beforeEach` hook to reset database
4. Write tests using arrange-act-assert pattern
5. Use existing helpers when possible
6. Run tests to verify they pass
7. Check cross-browser compatibility

Example:

```javascript
const { test, expect } = require('@playwright/test');
const { resetDatabase, loginUser, TEST_USERS } = require('./fixtures/test-helpers');

test.describe('My Feature', () => {
  test.beforeEach(async ({ page }) => {
    await resetDatabase(page);
    await loginUser(page, TEST_USERS.sarah.email, TEST_USERS.sarah.password);
  });

  test('should test my feature', async ({ page }) => {
    // Your test here
  });
});
```
