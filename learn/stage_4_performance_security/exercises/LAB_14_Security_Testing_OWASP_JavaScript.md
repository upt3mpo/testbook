# 🧪 Lab 14: Security Testing & OWASP (JavaScript)

**Estimated Time:** 120 minutes<br>
**Difficulty:** Advanced<br>
**Language:** 🟨 JavaScript<br>
**Prerequisites:** Lab 13 completed

**💡 Need Python instead?** Try [Lab 14: Security Testing & OWASP (Python)](LAB_14_Security_Testing_OWASP_Python.md)!

**What This Adds:** Master security testing with Playwright to identify vulnerabilities and ensure your application is protected against common attacks like SQL injection, XSS, and CSRF. This is essential for production applications.

---

## 🎯 What You'll Learn

- **OWASP Top 10** - Understand common web application vulnerabilities
- **Security testing techniques** - Test for SQL injection, XSS, CSRF, and more
- **Authentication security** - Test password policies, session management
- **API security** - Test for authorization bypasses and data exposure
- **Security scanning** - Use automated tools to find vulnerabilities
- **Security best practices** - Implement secure coding patterns

---

## 📋 Why Security Testing Matters

**The Problem:**

- Applications vulnerable to common attacks
- Sensitive data exposed through APIs
- Authentication bypasses allow unauthorized access
- No systematic way to test security

**The Solution:**
Security testing systematically identifies vulnerabilities and ensures proper security controls are in place.

---

## 📋 Step-by-Step Instructions

> **Before you start:** Testbook's actual security test suite (`tests/security/test_security.py`, `tests/security/test_rate_limiting.py`) is Python/pytest-only, hitting the API directly with the `requests` library — there is no equivalent JS file anywhere in `tests/security/`. This lab translates the same OWASP ideas into Playwright so you can practice them from the JS side; treat the code below as a teaching device to adapt, not as code that already exists in this repo. Two things to know before you adapt it: (1) the real frontend identifies elements with `data-testid` attributes, not plain CSS `#id` selectors — e.g. the login form is `[data-testid="login-email-input"]`, `[data-testid="login-password-input"]`, `[data-testid="login-submit-button"]`, and errors render into `[data-testid="login-error"]` (see `frontend/src/pages/Login.jsx` and the real specs in `tests/e2e/auth.spec.js`, which use exactly this pattern) — every `#email`/`#login-button`/`.error-message`-style selector below needs updating to match. (2) Several routes referenced below (`/create-post`, `/posts`, `/users/2`, `/posts/2/edit`, `/search`) don't exist in `frontend/src/App.jsx`'s router — the real routes are `/`, `/login`, `/register`, `/post/:postId`, `/profile/:username`, `/profile/:username/followers`, `/profile/:username/following`, `/settings`. You'll also need the backend running with `TESTING=true` (`cd backend && TESTING=true uvicorn main:app --reload --port 8000`; see `../../../docs/guides/PLAYWRIGHT_QUICKSTART.md`) so rate limits don't get in the way and `/api/dev/reset` is available between runs.

### Part 1: OWASP Top 10 Testing (40 minutes)

#### Step 1: Install Security Testing Tools

```bash
npm install --save-dev @playwright/test
```

(`helmet` and `express-rate-limit` are Express.js server middleware — Testbook's backend is FastAPI, so those don't apply here; rate limiting is already implemented with `slowapi`, see `backend/main.py` / `backend/routers/auth.py`. Likewise skip `jest`/`supertest` — the tests below use Playwright's own `test`/`expect`, not Jest.)

#### Step 2: Create Security Test Configuration

```javascript
// tests/security/security.config.js
module.exports = {
  testDir: "./tests/security",
  timeout: 30000,
  retries: 2,
  use: {
    baseURL: "http://localhost:8000",
    trace: "on-first-retry",
  },
  projects: [
    {
      name: "security-tests",
      testMatch: "**/*.security.test.js",
    },
  ],
};
```

#### Step 3: Test for SQL Injection (A03:2021 - Injection)

Create `tests/security/test_sql_injection.js`:

```javascript
const { test, expect } = require("@playwright/test");

test.describe("SQL Injection Tests", () => {
  test("should prevent SQL injection in login", async ({ page }) => {
    await page.goto("/login");

    // Test SQL injection payloads
    const sqlInjectionPayloads = [
      "test@example.com' OR '1'='1",
      "test@example.com'; DROP TABLE users; --",
      "test@example.com' UNION SELECT * FROM users --",
      "test@example.com' OR 1=1 --",
    ];

    for (const payload of sqlInjectionPayloads) {
      await page.fill("#email", payload);
      await page.fill("#password", "password123");
      await page.click("#login-button");

      // Should return 401 (unauthorized), not 500 (server error)
      await expect(page.locator(".error-message")).toBeVisible();

      // Should not expose database errors
      const errorText = await page.locator(".error-message").textContent();
      expect(errorText.toLowerCase()).not.toContain("sql");
      expect(errorText.toLowerCase()).not.toContain("database");
    }
  });

  test("should prevent SQL injection in search", async ({ page }) => {
    // NOTE: Testbook has no /search page or /api/users/search endpoint today
    // (see frontend/src/App.jsx's routes and backend/routers/users.py). Point
    // this at whatever user-input-driven query endpoint your app actually has.
    await page.goto("/search");

    const sqlInjectionPayloads = [
      "user' OR '1'='1",
      "user'; DROP TABLE users; --",
      "user' UNION SELECT * FROM users --",
    ];

    for (const payload of sqlInjectionPayloads) {
      await page.fill("#search-input", payload);
      await page.click("#search-button");

      // Should return 400 (bad request) or empty results, not 500
      const response = await page.waitForResponse((response) =>
        response.url().includes("/api/users/search")
      );

      expect([200, 400]).toContain(response.status());

      if (response.status() === 200) {
        const data = await response.json();
        expect(data.users).toHaveLength(0);
      }
    }
  });
});
```

#### Step 4: Test for Cross-Site Scripting (XSS) (A03:2021 - Injection)

Create `tests/security/test_xss.js`:

```javascript
const { test, expect } = require("@playwright/test");

test.describe("XSS Tests", () => {
  test("should prevent XSS in post content", async ({ page }) => {
    await page.goto("/login");

    // Login first
    await page.fill("#email", "test@example.com");
    await page.fill("#password", "password123");
    await page.click("#login-button");

    await page.goto("/create-post");

    // Test XSS payloads
    const xssPayloads = [
      "<script>alert('XSS')</script>",
      "<img src=x onerror=alert('XSS')>",
      "javascript:alert('XSS')",
      "<svg onload=alert('XSS')>",
      "';alert('XSS');//",
    ];

    for (const payload of xssPayloads) {
      await page.fill("#post-content", payload);
      await page.click("#submit-post");

      // Should return 201 (created)
      await expect(page.locator(".success-message")).toBeVisible();

      // Get the created post
      await page.goto("/posts");
      const postContent = await page
        .locator(".post-content")
        .first()
        .textContent();

      // NOTE: Testbook's backend stores post content as-is, unsanitized (see
      // tests/security/test_security.py::TestInputValidation::test_xss_in_post_content) —
      // and React escapes on render by putting it in a text node rather than
      // interpreting it as markup. That means `.textContent()` here will
      // still literally contain the substring "<script>..." as plain text;
      // that's fine and expected. What actually matters for XSS safety is
      // that it isn't parsed as an HTML element — assert the DOM has no
      // corresponding <script>/<img>/<svg> element, not that the text is
      // stripped:
      const scriptElementCount = await page.locator(".post-content script").count();
      expect(scriptElementCount).toBe(0);
    }
  });
});
```

---

### Part 2: Authentication and Authorization Security (30 minutes)

#### Step 1: Test Password Security

Create `tests/security/test_password_security.js`:

```javascript
const { test, expect } = require("@playwright/test");

test.describe("Password Security Tests", () => {
  test("should reject weak passwords", async ({ page }) => {
    await page.goto("/register");

    const weakPasswords = [
      "123456",
      "password",
      "12345678",
      "qwerty",
      "abc123",
      "password123",
      "admin",
      "letmein",
      "welcome",
      "monkey",
    ];

    for (const password of weakPasswords) {
      await page.fill("#email", `test${password}@example.com`);
      await page.fill("#username", `user${password}`);
      await page.fill("#display-name", "Test User");
      await page.fill("#password", password);
      await page.click("#register-button");

      // Should return 400 (bad request) for weak passwords
      await expect(page.locator(".error-message")).toBeVisible();

      const errorText = await page.locator(".error-message").textContent();
      expect(errorText.toLowerCase()).toContain("password");
    }
  });

  test("should enforce password complexity requirements", async ({ page }) => {
    await page.goto("/register");

    const invalidPasswords = [
      "short", // Too short
      "nouppercase123!", // No uppercase
      "NOLOWERCASE123!", // No lowercase
      "NoNumbers!", // No numbers
      "NoSpecialChars123", // No special characters
    ];

    for (const password of invalidPasswords) {
      await page.fill("#email", `test${password}@example.com`);
      await page.fill("#username", `user${password}`);
      await page.fill("#display-name", "Test User");
      await page.fill("#password", password);
      await page.click("#register-button");

      // Should return 400 (bad request)
      await expect(page.locator(".error-message")).toBeVisible();
    }

    // Test valid password
    await page.fill("#email", "test@example.com");
    await page.fill("#username", "testuser");
    await page.fill("#display-name", "Test User");
    await page.fill("#password", "ValidPassword123!");
    await page.click("#register-button");

    // Should return 201 (created)
    await expect(page.locator(".success-message")).toBeVisible();
  });

  test("should prevent brute force attacks", async ({ page }) => {
    // NOTE: Testbook does not implement account lockout — see
    // tests/security/test_rate_limiting.py::TestBruteForceProtection, where
    // both lockout and IP-ban tests are explicit `pytest.skip(...)` stubs
    // documenting this as not-yet-built. What IS implemented is a 20/min
    // (production) / 1000/min (TESTING=true) rate limit on login, so don't
    // expect a "locked" message — expect the error to eventually reflect a
    // rate limit instead, and only after ~20 attempts in production mode.
    await page.goto("/login");

    // Attempt multiple failed logins
    for (let i = 0; i < 10; i++) {
      await page.fill("#email", "test@example.com");
      await page.fill("#password", "wrongpassword");
      await page.click("#login-button");
      await page.waitForTimeout(1000);

      // Every attempt should show an error — invalid credentials, or (once
      // the real 20/min limit is hit) a rate-limit message.
      await expect(page.locator(".error-message")).toBeVisible();
    }
  });
});
```

#### Step 2: Test Authorization Bypass

Create `tests/security/test_authorization.js`:

```javascript
const { test, expect } = require("@playwright/test");

test.describe("Authorization Tests", () => {
  test("should prevent unauthorized access to other users' data", async ({
    page,
  }) => {
    // Login as user1
    await page.goto("/login");
    await page.fill("#email", "user1@example.com");
    await page.fill("#password", "password123");
    await page.click("#login-button");

    // Try to access user2's profile
    await page.goto("/users/2");

    // Should return 403 (forbidden) or 404 (not found)
    await expect(page.locator(".error-message")).toBeVisible();
  });

  test("should prevent unauthorized post modification", async ({ page }) => {
    // Login as user1
    await page.goto("/login");
    await page.fill("#email", "user1@example.com");
    await page.fill("#password", "password123");
    await page.click("#login-button");

    // Try to modify user2's post
    await page.goto("/posts/2/edit");

    // Should return 403 (forbidden) or 404 (not found)
    await expect(page.locator(".error-message")).toBeVisible();
  });
});
```

---

### Part 3: API Security Testing (30 minutes)

#### Step 1: Test for Information Disclosure

Create `tests/security/test_information_disclosure.js`:

```javascript
const { test, expect } = require("@playwright/test");

test.describe("Information Disclosure Tests", () => {
  test("should not expose sensitive information in error messages", async ({
    page,
  }) => {
    await page.goto("/api/invalid-endpoint");

    // Should return 404, not 500 with stack trace
    const response = await page.waitForResponse((response) =>
      response.url().includes("/api/invalid-endpoint")
    );

    expect(response.status()).toBe(404);

    // Error message should not contain sensitive information
    const errorText = await page.textContent("body");
    expect(errorText.toLowerCase()).not.toContain("traceback");
    expect(errorText.toLowerCase()).not.toContain("file");
    expect(errorText.toLowerCase()).not.toContain("line");
  });

  test("should not expose sensitive data in API responses", async ({
    page,
  }) => {
    await page.goto("/login");
    await page.fill("#email", "test@example.com");
    await page.fill("#password", "password123");
    await page.click("#login-button");

    // Get user profile (real route is GET /api/auth/me, not /api/users/me —
    // see backend/routers/auth.py)
    await page.goto("/api/auth/me");
    const response = await page.waitForResponse((response) =>
      response.url().includes("/api/auth/me")
    );

    const userData = await response.json();

    // Should not contain sensitive fields
    const sensitiveFields = [
      "hashed_password",
      "password",
      "secret",
      "private_key",
    ];
    for (const field of sensitiveFields) {
      expect(userData).not.toHaveProperty(field);
    }
  });
});
```

#### Step 2: Test for Rate Limiting

Create `tests/security/test_rate_limiting.js`:

```javascript
const { test, expect } = require("@playwright/test");

test.describe("Rate Limiting Tests", () => {
  test("should implement rate limiting on login endpoint", async ({ page }) => {
    // NOTE: the real login limit is 20/min in production (1000/min when the
    // backend runs with TESTING=true) — see backend/routers/auth.py. 10
    // attempts illustrates the pattern but won't reliably trip the limit.
    await page.goto("/login");

    // Make multiple login attempts
    for (let i = 0; i < 10; i++) {
      await page.fill("#email", "test@example.com");
      await page.fill("#password", "wrongpassword");
      await page.click("#login-button");
      await page.waitForTimeout(1000);

      // Every attempt should show an error, whether "invalid credentials" or
      // (once the real limit is hit) a rate-limit message.
      await expect(page.locator(".error-message")).toBeVisible();
    }
  });

  test("should include rate limit headers", async ({ page }) => {
    // NOTE: tests/security/test_rate_limiting.py::test_api_requests_have_rate_limit_headers
    // skips rather than fails when these headers are absent — don't assume
    // slowapi is configured to emit them; check first before asserting.
    await page.goto("/login");
    await page.fill("#email", "test@example.com");
    await page.fill("#password", "password123");
    await page.click("#login-button");

    // Make a request to a rate-limited endpoint (real feed route is /api/feed/all)
    await page.goto("/api/feed/all");
    const response = await page.waitForResponse((response) =>
      response.url().includes("/api/feed/all")
    );

    // Should include rate limit headers
    const headers = response.headers();
    expect(headers).toHaveProperty("x-ratelimit-limit");
    expect(headers).toHaveProperty("x-ratelimit-remaining");
    expect(headers).toHaveProperty("x-ratelimit-reset");
  });
});
```

---

### Part 4: Automated Security Scanning (20 minutes)

#### Step 1: Create Security Scan Script

Create `tests/security/security_scan.js`:

```javascript
#!/usr/bin/env node
/**
 * Automated security scanning script for Testbook application.
 */

const { execSync } = require("child_process");
const fs = require("fs");
const path = require("path");

function runSecurityScan() {
  console.log("🛡️  Starting security scan...");

  const results = [];

  // Run security tests
  try {
    console.log("🔍 Running security test suite...");
    execSync("npm run test:security", { stdio: "inherit" });
    results.push({ name: "Security Tests", passed: true });
  } catch (error) {
    console.log("❌ Security tests failed");
    results.push({ name: "Security Tests", passed: false });
  }

  // Run ESLint security rules
  try {
    console.log("🔍 Running ESLint security scan...");
    execSync("npx eslint . --ext .js --config .eslintrc.security.js", {
      stdio: "inherit",
    });
    results.push({ name: "ESLint Security", passed: true });
  } catch (error) {
    console.log("❌ ESLint security scan failed");
    results.push({ name: "ESLint Security", passed: false });
  }

  // Generate report
  generateSecurityReport(results);

  // Print summary
  console.log("\n📋 Security Scan Summary:");
  console.log("=" * 50);

  let allPassed = true;
  results.forEach(({ name, passed }) => {
    const status = passed ? "✅ PASS" : "❌ FAIL";
    console.log(`${name.padEnd(20)} ${status}`);
    if (!passed) allPassed = false;
  });

  console.log("=" * 50);

  if (allPassed) {
    console.log("🎉 All security scans passed!");
    process.exit(0);
  } else {
    console.log(
      "⚠️  Some security scans failed. Please review the issues above."
    );
    process.exit(1);
  }
}

function generateSecurityReport(results) {
  console.log("📊 Generating security report...");

  const report = {
    timestamp: new Date().toISOString(),
    results: results,
    summary: {
      total: results.length,
      passed: results.filter((r) => r.passed).length,
      failed: results.filter((r) => !r.passed).length,
    },
  };

  fs.writeFileSync("security-report.json", JSON.stringify(report, null, 2));
  console.log("✅ Security report generated: security-report.json");
}

if (require.main === module) {
  runSecurityScan();
}

module.exports = { runSecurityScan };
```

---

## 💪 Challenge Exercises

### Challenge 1: Create Custom Security Test Suite

```javascript
// Create tests/security/test_custom_security.js
const { test, expect } = require("@playwright/test");

test.describe("Custom Security Tests", () => {
  test("should test custom vulnerability", async ({ page }) => {
    // TODO: Implement custom security test
    // 1. Identify a specific vulnerability in your application
    // 2. Create a test that exploits it
    // 3. Verify that the vulnerability is properly handled
  });

  test("should test business logic security", async ({ page }) => {
    // TODO: Test business logic for security issues
    // 1. Test that business rules are properly enforced
    // 2. Test for race conditions
    // 3. Test for privilege escalation through business logic
  });
});
```

---

## ✅ Completion Checklist

- [ ] Can test for OWASP Top 10 vulnerabilities
- [ ] Can test authentication and authorization security
- [ ] Can test API security and information disclosure
- [ ] Can use automated security scanning tools
- [ ] Can create custom security tests
- [ ] Completed all challenge exercises
- [ ] Understand security testing best practices

---

## 💡 Pro Tips

1. **Start with OWASP Top 10** - Focus on the most common vulnerabilities
2. **Use automated tools** - Combine manual testing with automated scanning
3. **Test edge cases** - Look for vulnerabilities in unexpected places
4. **Monitor continuously** - Security testing should be ongoing
5. **Stay updated** - Keep up with new security threats and testing techniques

---

## 📚 Next Steps

**Continue building your skills:**

- **[Lab 15: Rate Limiting & Production Monitoring (JavaScript)](LAB_15_Rate_Limiting_Production_JavaScript.md)** - Production readiness
- **[Stage 5: Capstone](../../stage_5_capstone/README.md)** - Portfolio project and presentation

---

**🎉 Congratulations!** You now understand security testing and can identify and prevent common web application vulnerabilities!

**Next Lab:** [Lab 15: Rate Limiting & Production Monitoring (JavaScript)](LAB_15_Rate_Limiting_Production_JavaScript.md)
