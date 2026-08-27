# 🧪 Lab 11: Cross-Browser Testing (JavaScript)

**Estimated Time:** 90 minutes<br>
**Difficulty:** Advanced<br>
**Language:** 🟨 JavaScript<br>
**Prerequisites:** Lab 10 completed

**💡 Need Python instead?** Try [Lab 11: Cross Browser Testing (Python)](LAB_11_Cross_Browser_Testing_Python.md)!

**What This Adds:** Master the advanced features of Playwright that make it the go-to E2E testing tool. Learn debugging, code generation, CI/CD integration, and performance optimization techniques used in production.

---

## 🎯 What You'll Learn

- **Trace Viewer** - Debug test failures with visual timeline
- **Codegen** - Generate tests by recording user actions
- **Screenshot/Video** - Visual verification and debugging
- **Network HAR files** - Analyze network requests
- **Cross-browser projects** - Run the same spec against Chromium, Firefox, and WebKit
- **Parallel execution** - Speed up test runs
- **CI/CD integration** - Run tests in GitHub Actions
- **Visual comparisons** - Detect UI changes
- **Mobile viewport testing** - Test responsive design

---

## 📋 Step-by-Step Instructions

### Part 1: Trace Viewer - The Ultimate Debugging Tool (20 minutes)

**Trace Viewer** shows you exactly what happened during a test run, step by step.

#### Step 1: Enable Tracing

**Create:** `playwright.config.js`

```javascript
import { defineConfig } from "@playwright/test";

export default defineConfig({
  use: {
    // Enable tracing for all tests
    trace: "on-first-retry",
    // Or enable for specific tests
    // trace: 'retain-on-failure',
  },

  // Retry failed tests once to capture trace
  retries: 1,

  // Run tests in headed mode for better debugging
  // headless: false,
});
```

#### Step 2: Run Tests with Tracing

```bash
# Run a specific test with tracing
npx playwright test auth.spec.js --headed

# Run with trace on failure
npx playwright test --trace on-first-retry
```

#### Step 3: View Trace Files

```bash
# Open trace viewer
npx playwright show-trace test-results/trace.zip
```

**What you'll see:**

1. **Timeline** - Every action in chronological order
2. **Screenshots** - Visual state at each step
3. **Network requests** - API calls and responses
4. **Console logs** - JavaScript errors and logs
5. **DOM snapshots** - Page structure at each step

#### Step 4: Debug a Failing Test

**Create:** `tests/e2e/test-trace-debug.spec.js`

```javascript
import { test, expect } from "@playwright/test";

test("should demonstrate trace debugging", async ({ page }) => {
  // This test will fail and we'll debug it with trace
  await page.goto("http://localhost:3000");

  // Intentionally cause a failure
  await page.click('[data-testid="non-existent-button"]');

  // This will fail and generate a trace
  await expect(page.locator('[data-testid="success-message"]')).toBeVisible();
});
```

**Run and debug:**

```bash
npx playwright test test-trace-debug.spec.js --trace on-first-retry
npx playwright show-trace test-results/trace.zip
```

✅ **Checkpoint:** You can use trace viewer to debug test failures

---

### Part 2: Codegen - Generate Tests by Recording (15 minutes)

**Codegen** records your browser actions and generates test code automatically.

#### Step 1: Start Codegen

```bash
# Start codegen for Testbook
npx playwright codegen http://localhost:3000
```

**This opens:**

- Browser window with Testbook
- Codegen panel showing generated code
- Record button to start/stop recording

#### Step 2: Record a Test

1. **Click "Record"** in the codegen panel
2. **Navigate to Testbook** and perform actions:
   - Go to login page
   - Fill in email and password
   - Click login
   - Create a post
   - View profile
3. **Click "Stop"** when done

#### Step 3: Use Generated Code

**The generated code looks like:**

```javascript
import { test, expect } from "@playwright/test";

test("test", async ({ page }) => {
  await page.goto("http://localhost:3000/");
  await page.getByRole("link", { name: "Login" }).click();
  await page.getByPlaceholder("Email").fill("test@test.com");
  await page.getByPlaceholder("Password").fill("password");
  await page.getByRole("button", { name: "Log In" }).click();
  await page.getByPlaceholder("What's on your mind?").fill("My first post!");
  await page.getByRole("button", { name: "Post" }).click();
  await page.getByRole("link", { name: "Profile" }).click();
});
```

#### Step 4: Customize Generated Code

**Improve the generated code:**

```javascript
import { test, expect } from "@playwright/test";

test("should login and create post", async ({ page }) => {
  // Go to login page
  await page.goto("http://localhost:3000/");
  await page.getByRole("link", { name: "Login" }).click();

  // Login
  await page.getByPlaceholder("Email").fill("sarah.johnson@testbook.com");
  await page.getByPlaceholder("Password").fill("Sarah2024!");
  await page.getByRole("button", { name: "Log In" }).click();

  // Wait for navigation
  await page.waitForURL("http://localhost:3000/");

  // Create post
  await page
    .getByPlaceholder("What's on your mind?")
    .fill("Generated with codegen!");
  await page.getByRole("button", { name: "Post" }).click();

  // Verify post was created
  await expect(page.getByText("Generated with codegen!")).toBeVisible();

  // View profile
  await page.getByRole("link", { name: "Profile" }).click();
  await expect(page.getByText("sarahjohnson")).toBeVisible();
});
```

✅ **Checkpoint:** You can generate tests using codegen

---

### Part 3: Screenshots and Videos (15 minutes)

**Visual debugging** helps you see exactly what happened during test execution.

#### Step 1: Configure Screenshots

**Update `playwright.config.js`:**

```javascript
export default defineConfig({
  use: {
    // Take screenshot on failure
    screenshot: "only-on-failure",
    // Take video on failure
    video: "retain-on-failure",
  },

  // Global screenshot settings
  expect: {
    // Take screenshot on assertion failure
    toHaveScreenshot: { threshold: 0.2 },
  },
});
```

#### Step 2: Test Screenshot Capture

**Create:** `tests/e2e/test-screenshots.spec.js`

```javascript
import { test, expect } from "@playwright/test";

test("should capture screenshots on failure", async ({ page }) => {
  await page.goto("http://localhost:3000");

  // This will fail and capture a screenshot
  await expect(
    page.locator('[data-testid="non-existent-element"]')
  ).toBeVisible();
});

test("should take manual screenshots", async ({ page }) => {
  await page.goto("http://localhost:3000");

  // Take screenshot of specific element
  await page.locator('[data-testid="navbar"]').screenshot({
    path: "test-results/navbar.png",
  });

  // Take full page screenshot
  await page.screenshot({
    path: "test-results/full-page.png",
    fullPage: true,
  });
});
```

#### Step 3: Visual Comparisons

**Test UI consistency:**

```javascript
test("should match visual baseline", async ({ page }) => {
  await page.goto("http://localhost:3000");

  // Compare with baseline image
  await expect(page).toHaveScreenshot("homepage.png");

  // Compare specific element
  await expect(page.locator('[data-testid="navbar"]')).toHaveScreenshot(
    "navbar.png"
  );
});
```

**Run tests:**

```bash
npx playwright test test-screenshots.spec.js
```

**View results:**

```bash
# Open test results
npx playwright show-report
```

✅ **Checkpoint:** You can capture and compare screenshots

---

### Part 4: Network Analysis (15 minutes)

**Analyze network requests** to understand API interactions.

#### Step 1: Capture Network Requests

**Create:** `tests/e2e/test-network-analysis.spec.js`

```javascript
import { test, expect } from "@playwright/test";

test("should analyze network requests", async ({ page }) => {
  // Start network recording
  await page.route("**/*", (route) => {
    console.log(
      `Request: ${route.request().method()} ${route.request().url()}`
    );
    route.continue();
  });

  await page.goto("http://localhost:3000");

  // Login to trigger API calls
  await page.fill(
    '[data-testid="login-email-input"]',
    "sarah.johnson@testbook.com"
  );
  await page.fill('[data-testid="login-password-input"]', "Sarah2024!");
  await page.click('[data-testid="login-submit-button"]');

  // Wait for API calls to complete
  await page.waitForLoadState("networkidle");

  // Create a post to see more API calls
  await page.fill('[data-testid="create-post-textarea"]', "Network test post");
  await page.click('[data-testid="create-post-submit"]');

  await page.waitForLoadState("networkidle");
});
```

#### Step 2: Save HAR Files

**Update test to save network data:**

```javascript
test("should save network HAR file", async ({ page }) => {
  // Start HAR recording
  await page.routeFromHAR("test-results/network.har");

  await page.goto("http://localhost:3000");

  // Perform actions that make API calls
  await page.fill(
    '[data-testid="login-email-input"]',
    "sarah.johnson@testbook.com"
  );
  await page.fill('[data-testid="login-password-input"]', "Sarah2024!");
  await page.click('[data-testid="login-submit-button"]');

  await page.waitForLoadState("networkidle");

  // Save HAR file
  await page.context().close();
});
```

#### Step 3: Analyze Network Data

**View HAR files:**

```bash
# Open HAR file in browser
npx playwright show-trace test-results/network.har
```

**What you can analyze:**

- **Request/Response timing** - Which API calls are slow
- **Payload sizes** - Large responses that might cause issues
- **Error responses** - Failed API calls
- **Request dependencies** - Which calls depend on others

✅ **Checkpoint:** You can analyze network requests and responses

---

### Part 5: Cross-Browser & Mobile Viewport Testing (15 minutes)

**This is the part that gives the lab its name.** Everything above (trace, codegen, screenshots, network) works the same regardless of browser engine - cross-browser testing is about actually running your suite against more than one engine.

`tests/playwright.config.js` already defines a `projects` array, but only the `chromium` project is active - the `firefox`, `webkit`, and `Mobile Chrome` entries are commented out on purpose (the lab keeps things fast and simple by default):

```javascript
// tests/playwright.config.js (excerpt - already in the repo)
projects: [
  {
    name: "chromium",
    use: { ...devices["Desktop Chrome"] },
  },

  // Additional browsers available but not run by default
  // Uncomment to enable cross-browser testing:
  // {
  //   name: 'firefox',
  //   use: { ...devices['Desktop Firefox'] },
  // },
  // {
  //   name: 'webkit',
  //   use: { ...devices['Desktop Safari'] },
  // },
  // {
  //   name: 'Mobile Chrome',
  //   use: { ...devices['Pixel 5'] },
  // },
],
```

#### Step 1: Run the Same Test Against All Three Engines

Uncomment the `firefox` and `webkit` blocks above, install the extra engines, then target each project from the CLI:

```bash
cd tests
npx playwright install firefox webkit

# Run against a single engine
npx playwright test auth.spec.js --project=firefox
npx playwright test auth.spec.js --project=webkit

# Run against all active projects at once
npx playwright test auth.spec.js --project=chromium --project=firefox --project=webkit
```

Each engine renders and handles events slightly differently - a selector or timing assumption that passes on Chromium can still fail on WebKit, which is exactly what cross-browser testing is meant to catch.

#### Step 2: Mobile Viewport Testing

Uncomment the `Mobile Chrome` project (it uses Playwright's built-in `devices['Pixel 5']` preset, which sets viewport size, user agent, and touch support together) and run against it directly:

```bash
npx playwright test auth.spec.js --project="Mobile Chrome"
```

You can also configure a mobile-sized context by hand in a single test, without touching the shared config:

```javascript
import { test, expect } from "@playwright/test";

test("navbar renders correctly on a mobile viewport", async ({ browser }) => {
  const context = await browser.newContext({
    viewport: { width: 375, height: 812 }, // iPhone-ish size
    isMobile: true,
    hasTouch: true,
  });
  const page = await context.newPage();
  await page.goto("http://localhost:3000");

  await expect(page.locator('[data-testid="navbar"]')).toBeVisible();

  await context.close();
});
```

✅ **Checkpoint:** You can run the same spec against Chromium, Firefox, and WebKit, and against a mobile viewport

---

### Part 6: Parallel Execution & Performance (10 minutes)

**Speed up test runs** with parallel execution and optimization.

**⚠️ Note:** Testbook's own `tests/playwright.config.js` intentionally sets
`workers: 1` and `fullyParallel: false`, because the E2E suite resets the
shared database between tests - running it with `workers: 4` /
`fullyParallel: true` as shown below would make tests interfere with each
other and fail intermittently. The settings below are a general pattern for
suites whose tests are independent, not a change you should make to
Testbook's actual config.

#### Step 1: Configure Parallel Execution

**Update `playwright.config.js`:**

```javascript
export default defineConfig({
  // Run tests in parallel
  workers: 4, // Use 4 parallel workers

  // Or use percentage of CPU cores
  // workers: '50%',

  // Run tests in parallel across files
  fullyParallel: true,

  // Retry failed tests
  retries: 2,

  // Timeout settings
  timeout: 30000,
  expect: {
    timeout: 5000,
  },
});
```

#### Step 2: Optimize Test Performance

**Create:** `tests/e2e/test-performance.spec.js`

```javascript
import { test, expect } from "@playwright/test";

test("should run efficiently in parallel", async ({ page }) => {
  // Use faster navigation
  await page.goto("http://localhost:3000", {
    waitUntil: "domcontentloaded", // Faster than 'load'
  });

  // Use specific selectors instead of generic ones
  await page.locator('[data-testid="login-email-input"]').fill("test@test.com");

  // Wait for specific elements instead of arbitrary timeouts
  await page.waitForSelector('[data-testid="navbar"]', { state: "visible" });

  // Use expect with timeout instead of waitFor
  await expect(page.locator('[data-testid="navbar"]')).toBeVisible({
    timeout: 5000,
  });
});

test("should reuse browser context", async ({ page }) => {
  // Tests in the same file share browser context
  // This is faster than creating new context for each test
  await page.goto("http://localhost:3000");
  await expect(page.locator('[data-testid="login-email-input"]')).toBeVisible();
});
```

#### Step 3: Run Performance Tests

```bash
# Run with parallel execution
npx playwright test --workers=4

# Run with performance report
npx playwright test --reporter=html
```

✅ **Checkpoint:** You can run tests in parallel efficiently

---

### Part 7: CI/CD Integration (15 minutes)

**Run Playwright tests in GitHub Actions** for continuous integration.

#### Step 1: Create GitHub Actions Workflow

**Create:** `.github/workflows/playwright.yml`

```yaml
name: Playwright Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    timeout-minutes: 60
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          # Testbook targets Node 24 (see .nvmrc / other workflows in .github/workflows/)
          node-version: 24

      - name: Install frontend dependencies
        run: |
          cd frontend
          npm ci

      - name: Install E2E test dependencies
        run: |
          # Playwright config and specs live under tests/, not frontend/
          cd tests
          npm ci
          npx playwright install --with-deps

      - name: Start Testbook
        run: |
          # Start backend
          cd backend
          python -m venv .venv
          source .venv/bin/activate
          pip install -r requirements.txt
          # TESTING=true is required: it enables the /api/dev/reset endpoint
          # and the relaxed rate limits that the E2E suite depends on.
          TESTING=true uvicorn main:app --host 0.0.0.0 --port 8000 &

          # Start frontend
          cd ../frontend
          npm run build
          npm run preview -- --host 0.0.0.0 --port 3000 &

          # Wait for services to be ready
          sleep 10

      - name: Run Playwright tests
        run: |
          cd tests
          npx playwright test --project=chromium

      - name: Upload test results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report
          path: tests/playwright-report/
          retention-days: 30
```

#### Step 2: Configure for CI Environment

**Update `playwright.config.js` for CI:**

```javascript
export default defineConfig({
  use: {
    // CI-specific settings
    baseURL: process.env.CI ? "http://localhost:3000" : "http://localhost:3000",

    // Headless mode for CI
    headless: process.env.CI ? true : false,

    // Video and trace for CI debugging
    video: process.env.CI ? "retain-on-failure" : "off",
    trace: process.env.CI ? "retain-on-failure" : "off",
  },

  // CI-specific timeouts
  timeout: process.env.CI ? 60000 : 30000,

  // Retry failed tests in CI
  retries: process.env.CI ? 2 : 0,
});
```

#### Step 3: Test CI Integration

```bash
# Test locally with CI settings
CI=true npx playwright test

# Test with Docker (simulates CI environment)
docker run --rm -it -v $(pwd):/workspace -w /workspace mcr.microsoft.com/playwright:v1.40.0-focal bash
```

✅ **Checkpoint:** You can run Playwright tests in CI/CD

---

## 🎓 What You Learned

- ✅ **Trace Viewer** - Debug test failures with visual timeline
- ✅ **Codegen** - Generate tests by recording user actions
- ✅ **Screenshots/Videos** - Visual debugging and verification
- ✅ **Network Analysis** - Understand API interactions
- ✅ **Cross-Browser & Mobile Testing** - Run the same spec against Chromium, Firefox, WebKit, and a mobile viewport
- ✅ **Parallel Execution** - Speed up test runs
- ✅ **CI/CD Integration** - Run tests in GitHub Actions
- ✅ **Performance Optimization** - Make tests run faster

---

## 💪 Practice Challenges

### Challenge 1: Create a Complete Test Suite

Using all the techniques learned:

1. **Generate tests with codegen** for user registration flow
2. **Add trace debugging** for complex interactions
3. **Implement visual comparisons** for key pages
4. **Set up parallel execution** for speed
5. **Configure CI/CD** for automated testing

### Challenge 2: Debug a Complex Test

1. **Create a failing test** with multiple steps
2. **Use trace viewer** to identify the issue
3. **Fix the test** based on trace analysis
4. **Add screenshots** for visual verification

### Challenge 3: Performance Optimization

1. **Measure current test performance**
2. **Implement parallel execution**
3. **Optimize selectors and waits**
4. **Compare before/after performance**

---

## 🎯 Pro Tips

### Tip 1: Use Trace Viewer for Complex Debugging

```bash
# Always run with trace when debugging
npx playwright test --trace on-first-retry --headed

# View trace files
npx playwright show-trace test-results/trace.zip
```

### Tip 2: Generate Tests for New Features

```bash
# Start codegen for new feature
npx playwright codegen http://localhost:3000/new-feature

# Record the complete user flow
# Copy generated code to test file
# Customize and improve the generated code
```

### Tip 3: Optimize for CI/CD

```javascript
// Use environment variables for CI
const isCI = process.env.CI === "true";

export default defineConfig({
  use: {
    headless: isCI,
    video: isCI ? "retain-on-failure" : "off",
    trace: isCI ? "retain-on-failure" : "off",
  },
  retries: isCI ? 2 : 0,
});
```

---

## ✅ Completion Checklist

- [ ] Used trace viewer to debug test failures
- [ ] Generated tests using codegen
- [ ] Captured screenshots and videos
- [ ] Analyzed network requests
- [ ] Ran the same test against Chromium, Firefox, and WebKit
- [ ] Tested a mobile viewport
- [ ] Configured parallel execution
- [ ] Set up CI/CD integration
- [ ] Optimized test performance

---

## 🎯 Key Takeaways

1. **Trace Viewer is your best friend** - Use it for debugging complex failures
2. **Codegen speeds up test creation** - Record first, then customize
3. **Visual debugging is powerful** - Screenshots and videos show what happened
4. **Network analysis reveals issues** - Understand API interactions
5. **Parallel execution saves time** - Run tests faster with multiple workers
6. **CI/CD integration is essential** - Automate testing in your pipeline

---

**Ready for more?**

- **[Playwright Documentation](https://playwright.dev/)** - Official docs
- **[Playwright Best Practices](https://playwright.dev/docs/best-practices)** - Production patterns
- **[GitHub Actions with Playwright](https://playwright.dev/docs/ci)** - CI/CD guide

---

**🎉 Congratulations!** You've mastered Playwright's advanced features and are ready for production E2E testing!

**Next Lab:** [Lab 12: E2E Test Organization (JavaScript)](LAB_12_E2E_Test_Organization_JavaScript.md)
