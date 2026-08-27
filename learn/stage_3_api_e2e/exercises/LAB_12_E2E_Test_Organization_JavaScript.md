# 🧪 Lab 12: E2E Test Organization

**Estimated Time:** 90 minutes<br>
**Difficulty:** Intermediate<br>
**Language:** 🟨 JavaScript<br>
**Prerequisites:** Lab 11 completed

**💡 Need Python instead?** Try [Lab 12: E2E Test Organization (Python)](LAB_12_E2E_Test_Organization_Python.md)!

**What This Adds:** Organize E2E tests for maintainability, CI/CD integration, and team collaboration.

---

## 🎯 What You'll Learn

- **Test organization** - Structure tests for maintainability
- **CI/CD integration** - Run E2E tests in pipelines
- **Test data management** - Handle test data in E2E tests
- **Parallel execution** - Run tests efficiently
- **Reporting** - Generate test reports and screenshots
- **Environment management** - Test across different environments

---

## 📋 Why Test Organization Matters

**The Problem:**

- 100+ E2E tests scattered across files
- Tests fail randomly due to flaky setup
- No clear way to run specific test suites
- Hard to debug when tests fail in CI
- Tests take hours to run

**The Solution:**
Organize tests with clear structure, proper data management, and CI/CD integration.

---

## 📋 Step-by-Step Instructions

### Part 1: Test Structure Organization (30 minutes)

**Note:** `tests/e2e/` already has real files from Labs 9-11 (`playwright.config.js`,
`auth.spec.js`, `posts.spec.js`, `users.spec.js`, `fixtures/test-helpers.js`, etc.).
The structure below is a larger, "how would this scale to 100+ tests" reorganization
- it reuses the same filename (`playwright.config.js`) with different contents and
nests specs one level deeper (`tests/e2e/tests/smoke/...`). Don't paste these over
your working Lab 9-11 config and specs; either build this in a separate scratch
directory to see the pattern, or read through it comparing to what's already there
rather than overwriting it.

#### Step 1: Create Test Directory Structure

Create the following directory structure:

```text
tests/e2e/
├── playwright.config.js        # Playwright configuration
├── package.json                # E2E test dependencies
├── pages/                      # Page Object Model classes
│   ├── BasePage.js
│   ├── LoginPage.js
│   ├── RegisterPage.js
│   └── FeedPage.js         # Testbook has no "/dashboard" route - posts live on the feed ("/")
├── tests/                      # Test files
│   ├── smoke/                  # Critical path tests
│   │   └── critical-flows.spec.js
│   ├── regression/             # Full feature tests
│   │   ├── user-management.spec.js
│   │   ├── post-management.spec.js
│   │   └── authentication.spec.js
│   └── integration/            # Cross-feature tests
│       └── user-post-workflow.spec.js
├── data/                       # Test data
│   ├── users.json
│   ├── posts.json
│   └── test-config.json
├── utils/                      # Helper utilities
│   ├── database-helpers.js
│   ├── api-helpers.js
│   └── screenshot-helpers.js
└── reports/                    # Test reports and artifacts
    ├── html/
    ├── screenshots/
    └── videos/
```

#### Step 2: Create Playwright Configuration

Create `tests/e2e/playwright.config.js`:

```javascript
// Note: tests/package.json declares "type": "module", so this project uses
// ESM `import`/`export` syntax throughout - not CommonJS `require()`.
import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./tests",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ["html", { outputFolder: "reports/html" }],
    ["json", { outputFile: "reports/results.json" }],
    ["junit", { outputFile: "reports/results.xml" }],
  ],
  use: {
    baseURL: process.env.E2E_BASE_URL || "http://localhost:3000",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
    video: "retain-on-failure",
    actionTimeout: 30000,
    navigationTimeout: 30000,
  },
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
    {
      name: "firefox",
      use: { ...devices["Desktop Firefox"] },
    },
    {
      name: "webkit",
      use: { ...devices["Desktop Safari"] },
    },
    {
      name: "mobile-chrome",
      use: { ...devices["Pixel 5"] },
    },
    {
      name: "mobile-safari",
      use: { ...devices["iPhone 12"] },
    },
  ],
  webServer: [
    {
      command:
        "cd ../../backend && TESTING=true python -m uvicorn main:app --host 0.0.0.0 --port 8000",
      port: 8000,
      reuseExistingServer: !process.env.CI,
    },
    {
      // frontend/package.json has no "start" script - "dev" runs the Vite dev server
      command: "cd ../../frontend && npm run dev",
      port: 3000,
      reuseExistingServer: !process.env.CI,
    },
  ],
});
```

**⚠️ Important:** This is a separate, self-contained config for this
exercise - it is not the real `tests/playwright.config.js` Testbook ships
with. The real config only enables the `chromium` project by default
(firefox/webkit/mobile projects are present but commented out); running
`--project=firefox` or `--project=webkit` against the real Testbook suite
will fail with "Project(s) 'firefox' not found" until you uncomment the
corresponding block in `tests/playwright.config.js`. The config above
enables all five projects explicitly, so cross-browser commands only "just
work" here because this file defines them - they won't work against
Testbook's real config as-is.

#### Step 3: Create Base Page Object

Create `tests/e2e/pages/BasePage.js`:

```javascript
class BasePage {
  constructor(page) {
    this.page = page;
    this.baseUrl = process.env.E2E_BASE_URL || "http://localhost:3000";
  }

  async goto(path = "") {
    const url = `${this.baseUrl}${path}`;
    await this.page.goto(url);
    await this.page.waitForLoadState("networkidle");
  }

  async waitForElement(selector, timeout = 30000) {
    return await this.page.waitForSelector(selector, { timeout });
  }

  async clickElement(selector) {
    const element = await this.waitForElement(selector);
    await element.click();
  }

  async fillInput(selector, value) {
    const element = await this.waitForElement(selector);
    await element.fill(value);
  }

  async getText(selector) {
    const element = await this.waitForElement(selector);
    return await element.textContent();
  }

  async isVisible(selector) {
    try {
      const element = await this.page.waitForSelector(selector, {
        timeout: 5000,
      });
      return await element.isVisible();
    } catch {
      return false;
    }
  }

  async takeScreenshot(name) {
    await this.page.screenshot({
      path: `tests/e2e/reports/screenshots/${name}.png`,
      fullPage: true,
    });
  }

  async waitForUrl(urlPattern, timeout = 30000) {
    await this.page.waitForURL(urlPattern, { timeout });
  }

  async waitForResponse(urlPattern) {
    return await this.page.waitForResponse((response) =>
      response.url().includes(urlPattern)
    );
  }
}

export default BasePage;
```

Create `tests/e2e/pages/LoginPage.js`:

```javascript
import BasePage from "./BasePage.js";

class LoginPage extends BasePage {
  constructor(page) {
    super(page);
    this.emailInput = "input[data-testid='login-email-input']";
    this.passwordInput = "input[data-testid='login-password-input']";
    this.loginButton = "button[data-testid='login-submit-button']";
    // Testbook's real testid is "login-error" (not "login-error-message"),
    // and there is no dedicated success-message element - a successful
    // login just redirects to "/" and shows the navbar.
    this.errorMessage = "[data-testid='login-error']";
  }

  async login(email, password) {
    await this.fillInput(this.emailInput, email);
    await this.fillInput(this.passwordInput, password);
    await this.clickElement(this.loginButton);
  }

  async isLoginSuccessful() {
    return await this.isVisible("[data-testid='navbar']");
  }

  async getErrorMessage() {
    if (await this.isVisible(this.errorMessage)) {
      return await this.getText(this.errorMessage);
    }
    return "";
  }

  async waitForLoginSuccess() {
    // Testbook has no /dashboard route - a successful login redirects to "/"
    await this.waitForUrl("http://localhost:3000/");
  }
}

export default LoginPage;
```

---

### Part 2: Test Data Management (20 minutes)

#### Step 1: Create Test Data Files

Create `tests/e2e/data/users.json`:

```json
{
  "validUsers": [
    {
      "email": "test@example.com",
      "username": "testuser",
      "displayName": "Test User",
      "password": "password123",
      "bio": "Test user bio"
    },
    {
      "email": "admin@example.com",
      "username": "admin",
      "displayName": "Admin User",
      "password": "admin123",
      "bio": "Admin user bio"
    }
  ],
  "invalidUsers": [
    {
      "email": "invalid-email",
      "username": "ab",
      "displayName": "",
      "password": "123",
      "expectedErrors": [
        "Invalid email format",
        "Username too short",
        "Password too short"
      ]
    }
  ]
}
```

Create `tests/e2e/data/posts.json`:

**Note:** Testbook's actual `Post` model only has a `content` field (plus
optional `image_url`/`video_url`) - see `backend/schemas.py`'s
`PostCreate`. There's no `title` or `tags` field on real posts. The
`title`/`tags` fields below are kept as a generic example of structuring
test data with more fields than the app under test currently has; drop
them if you adapt this file to drive real Testbook E2E tests.

```json
{
  "validPosts": [
    {
      "title": "Test Post 1",
      "content": "This is a test post for E2E testing.",
      "tags": ["test", "e2e"]
    },
    {
      "title": "Test Post 2",
      "content": "Another test post with different content.",
      "tags": ["test", "automation"]
    }
  ],
  "invalidPosts": [
    {
      "title": "",
      "content": "Post without title",
      "expectedErrors": ["Title is required"]
    },
    {
      "title": "Valid Title",
      "content": "",
      "expectedErrors": ["Content is required"]
    }
  ]
}
```

#### Step 2: Create Data Helper Functions

Create `tests/e2e/utils/data-helpers.js`:

```javascript
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

// __dirname isn't available in ESM - derive it from import.meta.url instead
const __dirname = path.dirname(fileURLToPath(import.meta.url));

class DataHelper {
  constructor() {
    this.dataDir = path.join(__dirname, "..", "data");
  }

  loadJson(filename) {
    const filepath = path.join(this.dataDir, filename);
    const data = fs.readFileSync(filepath, "utf8");
    return JSON.parse(data);
  }

  getValidUsers() {
    return this.loadJson("users.json").validUsers;
  }

  getInvalidUsers() {
    return this.loadJson("users.json").invalidUsers;
  }

  getValidPosts() {
    return this.loadJson("posts.json").validPosts;
  }

  getInvalidPosts() {
    return this.loadJson("posts.json").invalidPosts;
  }

  getUserByEmail(email) {
    const users = this.getValidUsers();
    const user = users.find((u) => u.email === email);
    if (!user) {
      throw new Error(`User with email ${email} not found`);
    }
    return user;
  }

  getRandomUser() {
    const users = this.getValidUsers();
    return users[Math.floor(Math.random() * users.length)];
  }

  generateRandomUser(overrides = {}) {
    const randomId = Math.floor(Math.random() * 10000);
    const user = {
      email: `test${randomId}@example.com`,
      username: `user${randomId}`,
      displayName: `Test User ${randomId}`,
      password: "password123",
      bio: `Bio for user ${randomId}`,
    };
    return { ...user, ...overrides };
  }

  generateRandomPost(overrides = {}) {
    const randomId = Math.floor(Math.random() * 10000);
    const post = {
      title: `Test Post ${randomId}`,
      content: `This is test content ${randomId}`,
      tags: ["test", "automation", "e2e", "playwright"]
        .sort(() => 0.5 - Math.random())
        .slice(0, 2),
    };
    return { ...post, ...overrides };
  }
}

export default DataHelper;
```

---

### Part 3: Test Organization by Category (20 minutes)

#### Step 1: Create Smoke Tests

Create `tests/e2e/tests/smoke/critical-flows.spec.js`:

```javascript
import { test, expect } from "@playwright/test";
import LoginPage from "../../pages/LoginPage.js";
import FeedPage from "../../pages/FeedPage.js";
import DataHelper from "../../utils/data-helpers.js";

// Note: Testbook has no "/dashboard" route or welcome-message banner -
// after login, users land on the feed ("/"). These tests use a FeedPage
// object (data-testid="feed-page") rather than a fictional DashboardPage,
// and verify the logged-in user via navbar-username (which shows the
// user's display name), matching how tests/e2e/auth.spec.js does it.
test.describe("Critical Flows", () => {
  let dataHelper;

  test.beforeEach(async () => {
    dataHelper = new DataHelper();
  });

  test("user can login and view feed", async ({ page }) => {
    // Arrange
    const loginPage = new LoginPage(page);
    const feedPage = new FeedPage(page);
    const user = dataHelper.getUserByEmail("test@example.com");

    // Act
    await loginPage.goto("/login");
    await loginPage.login(user.email, user.password);

    // Assert
    expect(await loginPage.isLoginSuccessful()).toBeTruthy();
    expect(await feedPage.isVisible("[data-testid='feed-page']")).toBeTruthy();
    expect(await loginPage.getText("[data-testid='navbar-username']")).toBe(
      user.displayName
    );
  });

  test("user can create post", async ({ page }) => {
    // Arrange
    const loginPage = new LoginPage(page);
    const feedPage = new FeedPage(page);
    const user = dataHelper.getUserByEmail("test@example.com");
    // Testbook posts only have a `content` field (no title/tags) - see
    // backend/schemas.py PostCreate - so we use the post content directly.
    const post = dataHelper.getValidPosts()[0];

    // Act
    await loginPage.goto("/login");
    await loginPage.login(user.email, user.password);
    await feedPage.createPost(post.content);

    // Assert
    expect(await feedPage.isPostVisible(post.content)).toBeTruthy();
  });

  test("user can logout", async ({ page }) => {
    // Arrange
    const loginPage = new LoginPage(page);
    const feedPage = new FeedPage(page);
    const user = dataHelper.getUserByEmail("test@example.com");

    // Act
    await loginPage.goto("/login");
    await loginPage.login(user.email, user.password);
    await feedPage.logout();

    // Assert
    expect(
      await loginPage.isVisible("input[data-testid='login-email-input']")
    ).toBeTruthy();
    expect(page.url()).toContain("/login");
  });
});
```

#### Step 2: Create Regression Tests

Create `tests/e2e/tests/regression/user-management.spec.js`:

```javascript
import { test, expect } from "@playwright/test";
import LoginPage from "../../pages/LoginPage.js";
import RegisterPage from "../../pages/RegisterPage.js";
import DataHelper from "../../utils/data-helpers.js";

test.describe("User Management", () => {
  let dataHelper;

  test.beforeEach(async () => {
    dataHelper = new DataHelper();
  });

  test("user registration with valid data", async ({ page }) => {
    // Arrange
    const registerPage = new RegisterPage(page);
    const user = dataHelper.generateRandomUser();

    // Act
    await registerPage.goto("/register");
    await registerPage.register(
      user.email,
      user.username,
      user.displayName,
      user.password
    );

    // Assert
    // Note: Testbook shows no "Registration successful!" banner - a
    // successful registration auto-logs the user in and redirects to "/",
    // so a passing registration is verified by the navbar appearing.
    expect(await registerPage.isRegistrationSuccessful()).toBeTruthy();
    expect(
      await registerPage.isVisible("[data-testid='navbar']")
    ).toBeTruthy();
  });

  test("user registration with invalid data", async ({ page }) => {
    // Arrange
    const registerPage = new RegisterPage(page);
    const invalidUser = dataHelper.getInvalidUsers()[0];

    // Act
    await registerPage.goto("/register");
    await registerPage.register(
      invalidUser.email,
      invalidUser.username,
      invalidUser.displayName,
      invalidUser.password
    );

    // Assert
    // Real error testid is "register-error" (not "register-error-message")
    expect(await registerPage.isRegistrationSuccessful()).toBeFalsy();
    expect(await registerPage.getErrorMessage()).not.toBe("");
  });

  test("user can update profile", async ({ page }) => {
    // Arrange
    const loginPage = new LoginPage(page);
    const user = dataHelper.getUserByEmail("test@example.com");

    // Act
    await loginPage.goto("/login");
    await loginPage.login(user.email, user.password);

    // Note: Testbook has no bare "/profile" route or inline edit form on the
    // profile page - editing display name/bio happens on "/settings" (the
    // Profile page's "Edit Profile" button just navigates there).
    await page.goto("http://localhost:3000/settings");
    await page.fill(
      '[data-testid="settings-display-name-input"]',
      "Updated Name"
    );
    await page.fill('[data-testid="settings-bio-input"]', "Updated bio");
    await page.click('[data-testid="settings-save-button"]');

    // Assert
    await expect(page.locator('[data-testid="settings-success"]')).toBeVisible();
  });
});
```

---

### Part 4: CI/CD Integration (20 minutes)

#### Step 1: Create GitHub Actions Workflow

Create `.github/workflows/e2e-tests.yml`:

```yaml
name: E2E Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  e2e-tests:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        browser: [chromium, firefox, webkit]

    steps:
      - uses: actions/checkout@v3

      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          # Testbook targets Node 24 (see other workflows in .github/workflows/)
          node-version: "24"
          cache: "npm"

      - name: Install dependencies
        run: |
          cd frontend
          npm ci
          cd ../tests/e2e
          npm ci

      - name: Install Playwright browsers
        run: |
          cd tests/e2e
          npx playwright install ${{ matrix.browser }}
          npx playwright install-deps

      - name: Start backend server
        env:
          # TESTING=true enables the /api/dev/reset endpoint and relaxed
          # rate limits the E2E suite depends on - without it, tests that
          # reset the database will fail.
          TESTING: true
        run: |
          cd backend
          pip install -r requirements.txt
          python -m uvicorn main:app --host 0.0.0.0 --port 8000 &
          sleep 10

      - name: Start frontend server
        run: |
          cd frontend
          npm run build
          # frontend/package.json has no "start" script - use "preview"
          # (Vite's static server) to serve the production build instead.
          npm run preview -- --host 0.0.0.0 --port 3000 &
          sleep 10

      - name: Run E2E tests
        run: |
          cd tests/e2e
          npx playwright test --project=${{ matrix.browser }} --reporter=html

      - name: Upload test results
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: e2e-test-results-${{ matrix.browser }}
          path: |
            tests/e2e/reports/
            tests/e2e/test-results/
```

#### Step 2: Create Test Scripts

Create `tests/e2e/package.json`:

```json
{
  "name": "testbook-e2e-tests",
  "version": "1.0.0",
  "description": "E2E tests for Testbook application",
  "type": "module",
  "scripts": {
    "test": "playwright test",
    "test:smoke": "playwright test tests/smoke/",
    "test:regression": "playwright test tests/regression/",
    "test:integration": "playwright test tests/integration/",
    "test:chromium": "playwright test --project=chromium",
    "test:firefox": "playwright test --project=firefox",
    "test:webkit": "playwright test --project=webkit",
    "test:mobile": "playwright test --project=mobile-chrome --project=mobile-safari",
    "test:headed": "playwright test --headed",
    "test:debug": "playwright test --debug",
    "test:ui": "playwright test --ui",
    "report": "playwright show-report",
    "install": "playwright install"
  },
  "devDependencies": {
    "@playwright/test": "^1.56.1"
  }
}
```

**⚠️ Important:** Node resolves ESM vs. CommonJS using the *nearest*
`package.json` in the directory tree. The real `tests/package.json` already
sets `"type": "module"` for everything under `tests/`, which is why
`tests/e2e/auth.spec.js`, `posts.spec.js`, etc. can use `import`. If you
create a second `package.json` inside `tests/e2e/` without `"type": "module"`,
Node would treat that subtree as CommonJS instead and break the real ESM spec
files sitting right next to it - so this field is required, not optional,
in this exercise.

---

## 💪 Challenge Exercises

### Challenge 1: Create Test Suite Runner

```javascript
// Create tests/e2e/run-tests.js
import { execSync } from "child_process";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

class TestRunner {
  constructor() {
    this.projectRoot = path.join(__dirname, "..", "..");
  }

  async runTestSuite(suite, browser = "chromium", parallel = false) {
    const cmd = [
      "npx playwright test",
      `tests/e2e/tests/${suite}/`,
      `--project=${browser}`,
      "--reporter=html",
    ];

    if (parallel) {
      cmd.push("--workers=auto");
    }

    try {
      console.log(`Running ${suite} tests with ${browser}...`);
      execSync(cmd.join(" "), {
        stdio: "inherit",
        cwd: this.projectRoot,
      });
      console.log(`✅ ${suite} tests passed!`);
      return true;
    } catch (error) {
      console.error(`❌ ${suite} tests failed!`);
      return false;
    }
  }

  async runAllSuites() {
    const suites = ["smoke", "regression", "integration"];
    const browsers = ["chromium", "firefox", "webkit"];

    for (const suite of suites) {
      for (const browser of browsers) {
        const success = await this.runTestSuite(suite, browser);
        if (!success) {
          process.exit(1);
        }
      }
    }
  }
}

// CLI usage
// ESM equivalent of CommonJS's `require.main === module` check
const isMainModule =
  process.argv[1] && import.meta.url === `file://${process.argv[1]}`;

if (isMainModule) {
  const args = process.argv.slice(2);
  const suite = args[0];
  const browser = args[1] || "chromium";
  const parallel = args.includes("--parallel");

  const runner = new TestRunner();

  if (suite === "all") {
    runner.runAllSuites();
  } else {
    runner.runTestSuite(suite, browser, parallel);
  }
}

export default TestRunner;
```

### Challenge 2: Create Test Data Factory

```javascript
// Create tests/e2e/utils/test-data-factory.js
class TestDataFactory {
  static generateUser(overrides = {}) {
    const randomId = Math.floor(Math.random() * 10000);
    const user = {
      email: `test${randomId}@example.com`,
      username: `user${randomId}`,
      displayName: `Test User ${randomId}`,
      password: "password123",
      bio: `Bio for user ${randomId}`,
    };
    return { ...user, ...overrides };
  }

  static generatePost(overrides = {}) {
    const randomId = Math.floor(Math.random() * 10000);
    const post = {
      title: `Test Post ${randomId}`,
      content: `This is test content ${randomId}`,
      tags: ["test", "automation", "e2e", "playwright"]
        .sort(() => 0.5 - Math.random())
        .slice(0, 2),
    };
    return { ...post, ...overrides };
  }

  static generateMultipleUsers(count) {
    return Array.from({ length: count }, () => this.generateUser());
  }

  static generateMultiplePosts(count) {
    return Array.from({ length: count }, () => this.generatePost());
  }
}

export default TestDataFactory;
```

---

## ✅ Completion Checklist

- [ ] Can organize E2E tests in a maintainable structure
- [ ] Can use Page Object Model for test organization
- [ ] Can manage test data effectively
- [ ] Can run tests in CI/CD pipelines
- [ ] Can generate test reports and screenshots
- [ ] Can run tests in parallel for efficiency
- [ ] Completed all challenge exercises
- [ ] Understand how to scale E2E testing for teams

---

## 💡 Pro Tips

1. **Start with smoke tests** - Get critical paths working first
2. **Use Page Object Model** - Keep tests maintainable and readable
3. **Organize by feature** - Group related tests together
4. **Use test data factories** - Generate data dynamically
5. **Run in parallel** - Speed up test execution

---

## 📚 Next Steps

**Continue building your skills:**

- **[Lab 13: Load Testing with k6 (JavaScript)](../../stage_4_performance_security/exercises/LAB_13_Load_Testing_k6.md)** - Performance testing
- **[Lab 14: Security Testing & OWASP (JavaScript)](../../stage_4_performance_security/exercises/LAB_14_Security_Testing_OWASP_JavaScript.md)** - Security testing
- **[Lab 15: Rate Limiting & Production Monitoring (JavaScript)](../../stage_4_performance_security/exercises/LAB_15_Rate_Limiting_Production_JavaScript.md)** - Production readiness

---

**🎉 Congratulations!** You now understand how to organize E2E tests for maintainability and team collaboration!

**Next Lab:** [Lab 13: Load Testing with k6 (JavaScript)](../../stage_4_performance_security/exercises/LAB_13_Load_Testing_k6.md)
