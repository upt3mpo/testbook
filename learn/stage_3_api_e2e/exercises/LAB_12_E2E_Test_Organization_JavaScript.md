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

#### Step 1: Create Test Directory Structure

Create the following directory structure:

```
tests/e2e/
├── playwright.config.js        # Playwright configuration
├── package.json                # E2E test dependencies
├── pages/                      # Page Object Model classes
│   ├── BasePage.js
│   ├── LoginPage.js
│   ├── DashboardPage.js
│   └── PostPage.js
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
const { defineConfig, devices } = require("@playwright/test");

module.exports = defineConfig({
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
        "cd ../../backend && python -m uvicorn main:app --host 0.0.0.0 --port 8000",
      port: 8000,
      reuseExistingServer: !process.env.CI,
    },
    {
      command: "cd ../../frontend && npm start",
      port: 3000,
      reuseExistingServer: !process.env.CI,
    },
  ],
});
```

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

module.exports = BasePage;
```

Create `tests/e2e/pages/LoginPage.js`:

```javascript
const BasePage = require("./BasePage");

class LoginPage extends BasePage {
  constructor(page) {
    super(page);
    this.emailInput = "input[data-testid='login-email-input']";
    this.passwordInput = "input[data-testid='login-password-input']";
    this.loginButton = "button[data-testid='login-submit-button']";
    this.errorMessage = "[data-testid='login-error-message']";
    this.successMessage = "[data-testid='login-success-message']";
  }

  async login(email, password) {
    await this.fillInput(this.emailInput, email);
    await this.fillInput(this.passwordInput, password);
    await this.clickElement(this.loginButton);
  }

  async isLoginSuccessful() {
    return await this.isVisible(this.successMessage);
  }

  async getErrorMessage() {
    if (await this.isVisible(this.errorMessage)) {
      return await this.getText(this.errorMessage);
    }
    return "";
  }

  async waitForLoginSuccess() {
    await this.waitForUrl("**/dashboard");
  }
}

module.exports = LoginPage;
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
const fs = require("fs");
const path = require("path");

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

module.exports = DataHelper;
```

---

### Part 3: Test Organization by Category (20 minutes)

#### Step 1: Create Smoke Tests

Create `tests/e2e/tests/smoke/critical-flows.spec.js`:

```javascript
const { test, expect } = require("@playwright/test");
const LoginPage = require("../../pages/LoginPage");
const DashboardPage = require("../../pages/DashboardPage");
const DataHelper = require("../../utils/data-helpers");

test.describe("Critical Flows", () => {
  let dataHelper;

  test.beforeEach(async () => {
    dataHelper = new DataHelper();
  });

  test("user can login and view dashboard", async ({ page }) => {
    // Arrange
    const loginPage = new LoginPage(page);
    const dashboardPage = new DashboardPage(page);
    const user = dataHelper.getUserByEmail("test@example.com");

    // Act
    await loginPage.goto("/login");
    await loginPage.login(user.email, user.password);

    // Assert
    expect(await loginPage.isLoginSuccessful()).toBeTruthy();
    expect(await dashboardPage.isDashboardVisible()).toBeTruthy();
    expect(await dashboardPage.getWelcomeMessage()).toBe(
      `Welcome, ${user.displayName}!`
    );
  });

  test("user can create post", async ({ page }) => {
    // Arrange
    const loginPage = new LoginPage(page);
    const dashboardPage = new DashboardPage(page);
    const postPage = new PostPage(page);
    const user = dataHelper.getUserByEmail("test@example.com");
    const post = dataHelper.getValidPosts()[0];

    // Act
    await loginPage.goto("/login");
    await loginPage.login(user.email, user.password);
    await dashboardPage.clickCreatePost();
    await postPage.createPost(post.title, post.content);

    // Assert
    expect(await postPage.isPostCreated()).toBeTruthy();
    expect(await postPage.getPostTitle()).toBe(post.title);
  });

  test("user can logout", async ({ page }) => {
    // Arrange
    const loginPage = new LoginPage(page);
    const dashboardPage = new DashboardPage(page);
    const user = dataHelper.getUserByEmail("test@example.com");

    // Act
    await loginPage.goto("/login");
    await loginPage.login(user.email, user.password);
    await dashboardPage.logout();

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
const { test, expect } = require("@playwright/test");
const LoginPage = require("../../pages/LoginPage");
const RegisterPage = require("../../pages/RegisterPage");
const ProfilePage = require("../../pages/ProfilePage");
const DataHelper = require("../../utils/data-helpers");

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
    expect(await registerPage.isRegistrationSuccessful()).toBeTruthy();
    expect(await registerPage.getSuccessMessage()).toBe(
      "Registration successful!"
    );
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
    expect(await registerPage.isRegistrationSuccessful()).toBeFalsy();
    expect(await registerPage.getErrorMessage()).not.toBe("");
  });

  test("user profile update", async ({ page }) => {
    // Arrange
    const loginPage = new LoginPage(page);
    const profilePage = new ProfilePage(page);
    const user = dataHelper.getUserByEmail("test@example.com");

    // Act
    await loginPage.goto("/login");
    await loginPage.login(user.email, user.password);
    await profilePage.goto("/profile");
    await profilePage.updateProfile("Updated Name", "Updated bio");

    // Assert
    expect(await profilePage.isProfileUpdated()).toBeTruthy();
    expect(await profilePage.getDisplayName()).toBe("Updated Name");
    expect(await profilePage.getBio()).toBe("Updated bio");
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
          node-version: "18"
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
        run: |
          cd backend
          pip install -r requirements.txt
          python -m uvicorn main:app --host 0.0.0.0 --port 8000 &
          sleep 10

      - name: Start frontend server
        run: |
          cd frontend
          npm run build
          npm start &
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
    "@playwright/test": "^1.40.0"
  }
}
```

---

## 💪 Challenge Exercises

### Challenge 1: Create Test Suite Runner

```javascript
// Create tests/e2e/run-tests.js
const { execSync } = require("child_process");
const path = require("path");

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
if (require.main === module) {
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

module.exports = TestRunner;
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

module.exports = TestDataFactory;
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

- **[Lab 13: Load Testing with k6 (JavaScript)](LAB_13_Load_Testing_k6.md)** - Performance testing
- **[Lab 14: Security Testing & OWASP (JavaScript)](LAB_14_Security_Testing_OWASP_JavaScript.md)** - Security testing
- **[Lab 15: Rate Limiting & Production Monitoring (JavaScript)](LAB_15_Rate_Limiting_Production_JavaScript.md)** - Production readiness

---

**🎉 Congratulations!** You now understand how to organize E2E tests for maintainability and team collaboration!

**Next Lab:** [Lab 13: Load Testing with k6 (JavaScript)](LAB_13_Load_Testing_k6.md)
