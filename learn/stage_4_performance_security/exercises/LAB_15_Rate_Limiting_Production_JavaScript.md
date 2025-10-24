# 🧪 Lab 15: Rate Limiting Testing (JavaScript)

**Estimated Time:** 60-90 minutes<br>
**Difficulty:** Advanced<br>
**Language:** 🟨 JavaScript<br>
**Prerequisites:** Lab 14 completed

**💡 Need Python instead?** Try [Lab 15: Rate Limiting Testing (Python)](LAB_15_Rate_Limiting_Production_Python.md)!

**What This Adds:** Master rate limiting testing to ensure your application can handle high traffic and prevent abuse. Learn to test and implement rate limiting strategies for production applications.

---

<h2 id="what-youll-learn">🎯 What You'll Learn</h2>

- How security features (like rate limiting) affect your tests
- Why tests pass individually but fail together
- Environment-based configuration for testing
- Advanced Playwright fixture patterns
- Real-world test infrastructure challenges
- How to debug "flaky" tests caused by rate limits

---

<h2 id="background-when-your-code-works-too-well">📚 Background: When Your Code Works TOO Well</h2>

### The Scenario

You implement rate limiting to prevent brute force attacks:

```javascript
// In your API route
app.post(
  "/api/auth/login",
  rateLimit({
    windowMs: 60 * 1000, // 1 minute
    max: 20, // 20 requests per minute
  }),
  (req, res) => {
    // Login logic
  }
);
```

**Great for security!** ✅ Prevents attackers from trying 1000 passwords per second.

**But then your tests start failing...** ❌

---

<h2 id="the-problem">🐛 The Problem</h2>

### Test Results That Don't Make Sense

```bash
# Running one test: ✅ PASSES
$ npx playwright test auth.spec.js --grep "login"
✓ auth.spec.js > Authentication > should login successfully

# Running all tests: ❌ FAILS
$ npx playwright test
✗ auth.spec.js > Authentication > should login successfully
Error: 429 Too Many Requests
```

**What?!** 🤔 The code didn't change, why does it fail?

---

<h2 id="lab-exercise-1-reproduce-the-issue">🔍 Lab Exercise 1: Reproduce the Issue</h2>

### Step 1: Check Current Rate Limits

**Open `backend/routers/auth.py` and look for:**

```python
@limiter.limit("20/minute")
def login(...):
```

This means: **20 login requests per minute, per IP address.**

### Step 2: Count Your Test's Login Calls

**Open `tests/e2e/auth.spec.js` and count how many tests use login.**

**Question:** If you have 25 tests that each need to login, what happens?

<details>
<summary>Click to see answer</summary>

**Answer:** After 20 tests, the 21st test hits the rate limit!

```text
Test 1-20: ✅ Get tokens successfully
Test 21+:  ❌ Get 429 "Rate limit exceeded"
```

</details>

### Step 3: Reproduce the Failure

```bash
cd tests
npm test auth.spec.js
```

**You should see some tests failing with 429 errors.**

✅ **Checkpoint:** You can reproduce the rate limit issue

---

<h2 id="lab-exercise-2-understand-the-problem">🔍 Lab Exercise 2: Understand the Problem</h2>

### Step 1: Check Rate Limit Headers

**Create:** `tests/e2e/test-rate-limits.spec.js`

```javascript
import { test, expect } from "@playwright/test";

test.describe("Rate Limit Testing", () => {
  test("should see rate limit headers", async ({ page }) => {
    // Make a request and check headers
    const response = await page.request.post(
      "http://localhost:8000/api/auth/login",
      {
        data: {
          email: "test@test.com",
          password: "wrongpassword",
        },
      }
    );

    // Check rate limit headers
    const headers = response.headers();
    console.log("Rate limit headers:", {
      "x-ratelimit-limit": headers["x-ratelimit-limit"],
      "x-ratelimit-remaining": headers["x-ratelimit-remaining"],
      "x-ratelimit-reset": headers["x-ratelimit-reset"],
    });

    // Should get 401 for wrong password, not 429
    expect(response.status()).toBe(401);
  });

  test("should hit rate limit after many requests", async ({ page }) => {
    const requests = [];

    // Make 25 requests quickly
    for (let i = 0; i < 25; i++) {
      requests.push(
        page.request.post("http://localhost:8000/api/auth/login", {
          data: {
            email: `test${i}@test.com`,
            password: "wrongpassword",
          },
        })
      );
    }

    // Wait for all requests
    const responses = await Promise.all(requests);

    // Check which ones got rate limited
    const rateLimited = responses.filter((r) => r.status() === 429);
    const notRateLimited = responses.filter((r) => r.status() !== 429);

    console.log(
      `Rate limited: ${rateLimited.length}, Not rate limited: ${notRateLimited.length}`
    );

    // Some should be rate limited
    expect(rateLimited.length).toBeGreaterThan(0);
  });
});
```

**Run it:**

```bash
npx playwright test test-rate-limits.spec.js --headed
```

✅ **Checkpoint:** You understand how rate limits work

---

<h2 id="lab-exercise-3-fix-the-problem">🔍 Lab Exercise 3: Fix the Problem</h2>

### Solution 1: Disable Rate Limiting in Tests

**Create:** `tests/e2e/fixtures/test-config.js`

```javascript
import { test as base } from "@playwright/test";

export const test = base.extend({
  // Override base URL to use test configuration
  baseURL: "http://localhost:8000",

  // Add test-specific configuration
  testConfig: async ({}, use) => {
    // Set environment variable to disable rate limiting
    process.env.DISABLE_RATE_LIMITS = "true";

    await use({
      disableRateLimits: true,
      testMode: true,
    });

    // Cleanup
    delete process.env.DISABLE_RATE_LIMITS;
  },
});

export { expect } from "@playwright/test";
```

### Solution 2: Use Different IP Addresses

**Create:** `tests/e2e/test-rate-limit-solutions.spec.js`

```javascript
import { test, expect } from "./fixtures/test-config.js";

test.describe("Rate Limit Solutions", () => {
  test("should use different IP addresses", async ({ page, context }) => {
    // Create multiple contexts with different IPs
    const contexts = [];

    for (let i = 0; i < 5; i++) {
      const newContext = await context.browser().newContext({
        // Simulate different IP addresses
        extraHTTPHeaders: {
          "X-Forwarded-For": `192.168.1.${100 + i}`,
          "X-Real-IP": `192.168.1.${100 + i}`,
        },
      });
      contexts.push(newContext);
    }

    // Make requests from different contexts
    const requests = contexts.map(async (ctx) => {
      const page = await ctx.newPage();
      const response = await page.request.post(
        "http://localhost:8000/api/auth/login",
        {
          data: {
            email: "test@test.com",
            password: "wrongpassword",
          },
        }
      );
      await ctx.close();
      return response;
    });

    const responses = await Promise.all(requests);

    // All should succeed (different IPs)
    responses.forEach((response) => {
      expect(response.status()).toBe(401); // Wrong password, not rate limited
    });
  });

  test("should wait between requests", async ({ page }) => {
    const responses = [];

    // Make requests with delays
    for (let i = 0; i < 10; i++) {
      const response = await page.request.post(
        "http://localhost:8000/api/auth/login",
        {
          data: {
            email: `test${i}@test.com`,
            password: "wrongpassword",
          },
        }
      );
      responses.push(response);

      // Wait 3 seconds between requests
      await page.waitForTimeout(3000);
    }

    // All should succeed (spread out over time)
    responses.forEach((response) => {
      expect(response.status()).toBe(401); // Wrong password, not rate limited
    });
  });

  test("should use test-specific rate limits", async ({ page }) => {
    // This test assumes the backend has test-specific rate limits
    // that are higher than production limits

    const responses = [];

    // Make many requests quickly
    for (let i = 0; i < 50; i++) {
      const response = await page.request.post(
        "http://localhost:8000/api/auth/login",
        {
          data: {
            email: `test${i}@test.com`,
            password: "wrongpassword",
          },
        }
      );
      responses.push(response);
    }

    // In test mode, should allow more requests
    const rateLimited = responses.filter((r) => r.status() === 429);
    const notRateLimited = responses.filter((r) => r.status() !== 429);

    console.log(
      `Rate limited: ${rateLimited.length}, Not rate limited: ${notRateLimited.length}`
    );

    // Should have fewer rate limited requests in test mode
    expect(rateLimited.length).toBeLessThan(10);
  });
});
```

### Solution 3: Reset Rate Limits Between Tests

**Create:** `tests/e2e/fixtures/rate-limit-reset.js`

```javascript
import { test as base } from "@playwright/test";

export const test = base.extend({
  resetRateLimits: async ({ page }, use) => {
    // Reset rate limits before each test
    await page.request.post("http://localhost:8000/api/test/reset-rate-limits");

    await use();

    // Clean up after test
    await page.request.post("http://localhost:8000/api/test/reset-rate-limits");
  },
});

export { expect } from "@playwright/test";
```

**Use in tests:**

```javascript
import { test, expect } from "./fixtures/rate-limit-reset.js";

test("should reset rate limits between tests", async ({
  page,
  resetRateLimits,
}) => {
  // Rate limits are reset before this test runs

  const response = await page.request.post(
    "http://localhost:8000/api/auth/login",
    {
      data: {
        email: "test@test.com",
        password: "wrongpassword",
      },
    }
  );

  expect(response.status()).toBe(401); // Should not be rate limited
});
```

---

<h2 id="lab-exercise-4-implement-the-best-solution">🔍 Lab Exercise 4: Implement the Best Solution</h2>

### Step 1: Create a Test Configuration

**Create:** `tests/e2e/playwright.config.js`

```javascript
import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests/e2e",
  timeout: 30000,

  use: {
    baseURL: "http://localhost:3000",
    headless: false, // Set to true for CI
  },

  // Global setup
  globalSetup: require.resolve("./global-setup.js"),

  // Global teardown
  globalTeardown: require.resolve("./global-teardown.js"),

  // Test configuration
  testMatch: "**/*.spec.js",

  // Retry failed tests
  retries: 2,

  // Run tests in parallel
  workers: 4,

  // Reporter
  reporter: [["html"], ["json", { outputFile: "test-results/results.json" }]],
});
```

### Step 2: Create Global Setup

**Create:** `tests/e2e/global-setup.js`

```javascript
const { chromium } = require("@playwright/test");

async function globalSetup() {
  console.log("🚀 Starting global setup...");

  // Start Testbook if not already running
  const browser = await chromium.launch();
  const page = await browser.newPage();

  try {
    // Check if Testbook is running
    await page.goto("http://localhost:3000", { timeout: 5000 });
    console.log("✅ Testbook is already running");
  } catch (error) {
    console.log("❌ Testbook is not running, please start it first");
    console.log("Run: cd frontend && npm run dev");
    process.exit(1);
  }

  await browser.close();
  console.log("✅ Global setup complete");
}

module.exports = globalSetup;
```

### Step 3: Create Global Teardown

**Create:** `tests/e2e/global-teardown.js`

```javascript
async function globalTeardown() {
  console.log("🧹 Starting global teardown...");

  // Reset rate limits
  try {
    const response = await fetch(
      "http://localhost:8000/api/test/reset-rate-limits",
      {
        method: "POST",
      }
    );

    if (response.ok) {
      console.log("✅ Rate limits reset");
    } else {
      console.log("⚠️ Could not reset rate limits");
    }
  } catch (error) {
    console.log("⚠️ Could not reset rate limits:", error.message);
  }

  console.log("✅ Global teardown complete");
}

module.exports = globalTeardown;
```

### Step 4: Create Test-Specific Fixtures

**Create:** `tests/e2e/fixtures/auth-fixtures.js`

```javascript
import { test as base } from "@playwright/test";

export const test = base.extend({
  // Login helper that handles rate limits
  login: async ({ page }, use) => {
    const login = async (email, password) => {
      // Try to login with retry logic
      let attempts = 0;
      const maxAttempts = 3;

      while (attempts < maxAttempts) {
        try {
          const response = await page.request.post(
            "http://localhost:8000/api/auth/login",
            {
              data: { email, password },
            }
          );

          if (response.status() === 429) {
            // Rate limited, wait and retry
            console.log(`Rate limited, waiting... (attempt ${attempts + 1})`);
            await page.waitForTimeout(2000);
            attempts++;
            continue;
          }

          if (response.ok) {
            const data = await response.json();
            // Store token for authenticated requests
            await page.context().addCookies([
              {
                name: "token",
                value: data.access_token,
                domain: "localhost",
                path: "/",
              },
            ]);
            return data;
          }

          throw new Error(`Login failed: ${response.status()}`);
        } catch (error) {
          if (attempts === maxAttempts - 1) {
            throw error;
          }
          attempts++;
          await page.waitForTimeout(1000);
        }
      }
    };

    await use(login);
  },

  // Authenticated page helper
  authenticatedPage: async ({ page, login }, use) => {
    await login("sarah.johnson@testbook.com", "Sarah2024!");
    await use(page);
  },
});

export { expect } from "@playwright/test";
```

### Step 5: Use the Fixtures in Tests

**Create:** `tests/e2e/test-auth-with-fixtures.spec.js`

```javascript
import { test, expect } from "./fixtures/auth-fixtures.js";

test.describe("Authentication with Rate Limit Handling", () => {
  test("should login successfully with retry logic", async ({ login }) => {
    const result = await login("sarah.johnson@testbook.com", "Sarah2024!");

    expect(result.access_token).toBeDefined();
    expect(result.token_type).toBe("bearer");
  });

  test("should handle rate limits gracefully", async ({ page, login }) => {
    // Make many login attempts quickly
    const promises = [];
    for (let i = 0; i < 10; i++) {
      promises.push(
        page.request.post("http://localhost:8000/api/auth/login", {
          data: {
            email: `test${i}@test.com`,
            password: "wrongpassword",
          },
        })
      );
    }

    const responses = await Promise.all(promises);

    // Some should be rate limited, some should fail with wrong password
    const rateLimited = responses.filter((r) => r.status() === 429);
    const wrongPassword = responses.filter((r) => r.status() === 401);

    expect(rateLimited.length + wrongPassword.length).toBe(10);
  });

  test("should work with authenticated page", async ({ authenticatedPage }) => {
    // Page is already authenticated
    await authenticatedPage.goto("http://localhost:3000");

    // Should see the feed, not login page
    await expect(
      authenticatedPage.locator('[data-testid="navbar"]')
    ).toBeVisible();
    await expect(
      authenticatedPage.locator('[data-testid="login-email-input"]')
    ).not.toBeVisible();
  });
});
```

---

<h2 id="lab-exercise-5-test-the-solution">🔍 Lab Exercise 5: Test the Solution</h2>

### Step 1: Run the Tests

```bash
cd tests
npx playwright test test-auth-with-fixtures.spec.js --headed
```

### Step 2: Run All Tests

```bash
npx playwright test --headed
```

### Step 3: Check for Rate Limit Issues

```bash
# Run tests multiple times to check for flakiness
for i in {1..5}; do
  echo "Run $i:"
  npx playwright test --headed
done
```

✅ **Checkpoint:** All tests should pass consistently

---

<h2 id="what-you-learned">🎓 What You Learned</h2>

- ✅ How rate limiting affects test execution
- ✅ Why tests pass individually but fail together
- ✅ How to implement retry logic for rate-limited requests
- ✅ How to use different IP addresses to avoid rate limits
- ✅ How to create test-specific configurations
- ✅ How to handle rate limits in CI/CD environments

---

<h2 id="best-practices">💡 Best Practices</h2>

### 1. Use Test-Specific Rate Limits

```javascript
// In your backend configuration
const rateLimitConfig = {
  windowMs: 60 * 1000, // 1 minute
  max: process.env.NODE_ENV === "test" ? 1000 : 20, // Higher limit for tests
};
```

### 2. Implement Retry Logic

```javascript
async function makeRequestWithRetry(requestFn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      const response = await requestFn();
      if (response.status !== 429) {
        return response;
      }
    } catch (error) {
      if (i === maxRetries - 1) throw error;
    }
    await new Promise((resolve) => setTimeout(resolve, 1000 * (i + 1)));
  }
}
```

### 3. Use Test Fixtures

```javascript
// Create reusable fixtures for common test scenarios
export const test = base.extend({
  authenticatedUser: async ({ page }, use) => {
    // Setup authenticated user
    await use(user);
  },
});
```

### 4. Monitor Rate Limit Headers

```javascript
test("should check rate limit headers", async ({ page }) => {
  const response = await page.request.post("/api/auth/login", { data });

  const headers = response.headers();
  console.log("Rate limit info:", {
    limit: headers["x-ratelimit-limit"],
    remaining: headers["x-ratelimit-remaining"],
    reset: headers["x-ratelimit-reset"],
  });
});
```

---

<h2 id="troubleshooting">🐛 Troubleshooting</h2>

### Problem: Tests Still Fail with Rate Limits

**Solution:** Check if rate limiting is properly configured for test environment.

```javascript
// Add to your test setup
process.env.NODE_ENV = "test";
process.env.DISABLE_RATE_LIMITS = "true";
```

### Problem: Tests Are Slow

**Solution:** Use parallel execution and optimize retry logic.

```javascript
// In playwright.config.js
export default defineConfig({
  workers: 4, // Run tests in parallel
  retries: 1, // Reduce retries
});
```

### Problem: CI/CD Tests Fail

**Solution:** Ensure test environment has proper rate limit configuration.

```yaml
# In GitHub Actions
env:
  NODE_ENV: test
  DISABLE_RATE_LIMITS: true
```

---

<h2 id="completion-checklist">✅ Completion Checklist</h2>

- [ ] Reproduced the rate limit issue
- [ ] Understood how rate limits work
- [ ] Implemented retry logic for rate-limited requests
- [ ] Created test-specific configurations
- [ ] Used fixtures to handle authentication
- [ ] All tests pass consistently
- [ ] Understand best practices for handling rate limits

---

<h2 id="key-takeaways">🎯 Key Takeaways</h2>

1. **Rate limiting is a security feature** - Don't disable it in production
2. **Tests need special handling** - Use test-specific configurations
3. **Retry logic is essential** - Handle rate limits gracefully
4. **Fixtures simplify testing** - Create reusable test helpers
5. **Monitor and debug** - Use headers and logs to understand issues

---

**Ready for more?**

- **[Playwright Rate Limiting Guide](https://playwright.dev/docs/network#rate-limiting)** - Official documentation
- **[Rate Limiting Best Practices](https://expressjs.com/en/advanced/best-practice-performance.html#use-rate-limiting)** - Express.js guide
- **[Test Configuration Patterns](https://playwright.dev/docs/test-configuration)** - Playwright config guide

---

**🎉 Congratulations!** You can now handle rate limiting in your tests like a pro!

**Next Lab:** Move to [Stage 5: Capstone](../../stage_5_capstone/README.md) or explore other labs
