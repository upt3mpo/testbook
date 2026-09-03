# 🧪 Lab 9: Basic E2E Testing (JavaScript)

**Estimated Time:** 90 minutes<br>
**Difficulty:** Intermediate<br>
**Language:** 🟨 JavaScript<br>
**Prerequisites:** Lab 8 completed

**💡 Need Python instead?** Try [Lab 9: Basic E2E Testing (Python)](LAB_09_Basic_E2E_Testing_Python.md)!

**What This Adds:** Master end-to-end testing with Playwright - learn to test complete user workflows in real browsers, ensuring your application works as users expect it to.

---

<h2 id="what-youll-learn">🎯 What You'll Learn</h2>

- Write E2E tests with Playwright (JavaScript)
- Test in a real browser
- Select elements with data-testid
- Test complete user flows
- See tests run visually!

---

<h2 id="step-by-step-instructions">📋 Step-by-Step Instructions</h2>

### Step 1: Setup Playwright (10 minutes)

```bash
cd tests
npm install
npx playwright install chromium
```

**Wait for installation...**

✅ **Checkpoint:** Run `npx playwright --version` and see version number

### Step 2: Make Sure Testbook is Running (5 minutes)

**In a separate terminal, start the development servers:**

```bash
# macOS / Linux
TESTING=true ./start-dev.sh

# Windows
set TESTING=true && start-dev.bat
```

This launches the backend on `http://localhost:8000` and the frontend UI on `http://localhost:3000`. `TESTING=true` enables the dev-only `/api/dev/reset` endpoint and higher rate limits that E2E tests rely on — see [`../../../docs/guides/PLAYWRIGHT_QUICKSTART.md`](../../../docs/guides/PLAYWRIGHT_QUICKSTART.md) for details.

**Verify:** Open <http://localhost:3000> in your browser – you should see Testbook!

✅ **Checkpoint:** Testbook loads in your browser

### Step 3: Watch a Test Run! (10 minutes)

**Run an existing test in HEADED mode (you'll see the browser!):**

```bash
cd tests
npx playwright test auth.spec.js --headed
```

**🎬 What you'll see:**

- Browser window opens automatically
- Form fields fill themselves
- Buttons click themselves
- Test passes or fails

**This is E2E testing magic!** ✨

✅ **Checkpoint:** You watched a test run in the browser

### Step 4: Run in DEBUG Mode (15 minutes)

**This is even cooler - you can control the test!**

```bash
npx playwright test auth.spec.js --debug
```

**What happens:**

- Test pauses at each step
- You can see what's selected
- You can step through line-by-line
- Inspector shows you everything

**Try it:**

- Click "Step over" button to run each line
- Hover over elements to see them highlight
- See exactly what the test does

**Bonus: Slow Motion Mode**

```bash
npx playwright test auth.spec.js --headed --slow-mo=1000
```

(Slows down each action by 1 second - great for demos!)

✅ **Checkpoint:** You used Playwright Inspector

### Step 5: Understand Selectors (15 minutes)

**Open:** `tests/e2e/auth.spec.js`

**Find:**

```javascript
await page.fill('[data-testid="login-email-input"]', email);
```

**This means:**

- `page.fill()` - Type into an input field
- `[data-testid="login-email-input"]` - Find element by its test ID
- `email` - The value to type

**Why `data-testid`?**

- Specifically for testing
- Won't change if CSS changes
- Clear and reliable

**Other selectors you'll use:**

```javascript
await page.click('[data-testid="login-submit-button"]');
await page.locator('[data-testid="navbar"]').toBeVisible();
await page.fill('[data-testid="create-post-textarea"]', "My post");
```

✅ **Checkpoint:** You understand how to find elements

### Step 6: Write Your First E2E Test! (35 minutes)

**Create:** `tests/e2e/my_first_e2e.spec.js`

```javascript
import { test, expect } from "@playwright/test";

test("My first E2E test - Login and create post", async ({ page }) => {
  // Step 1: Go to Testbook
  await page.goto("http://localhost:3000");

  // Step 2: Login
  await page.fill(
    '[data-testid="login-email-input"]',
    "sarah.johnson@testbook.com"
  );
  await page.fill('[data-testid="login-password-input"]', "Sarah2024!");
  await page.click('[data-testid="login-submit-button"]');

  // Step 3: Wait for page to load
  await expect(page.locator('[data-testid="navbar"]')).toBeVisible();

  // Step 4: Create a post
  await page.fill(
    '[data-testid="create-post-textarea"]',
    "My first E2E test post!"
  );
  await page.click('[data-testid="create-post-submit-button"]');

  // Step 5: Verify post appears. toContainText() retries on its own until
  // the post shows up (or the timeout is hit), so there's no need for a
  // separate wait before it.
  const firstPost = page.locator('[data-testid-generic="post-item"]').first();
  await expect(firstPost).toContainText("My first E2E test post!");

  console.log("✅ Test passed! Post created successfully!");
});
```

**Run your test in headed mode (watch it work!):**

```bash
npx playwright test my_first_e2e.spec.js --headed
```

**🎬 Watch the magic:**

- Browser opens
- Form fills automatically
- Login happens
- Post is created
- Test verifies result

✅ **Checkpoint:** YOUR first E2E test runs and passes!

---

<h2 id="what-you-learned">🎓 What You Learned</h2>

- ✅ How to write E2E tests with Playwright
- ✅ How to select elements with data-testid
- ✅ How to interact with the UI (fill, click)
- ✅ How to verify results (expect, toBeVisible, toContainText)
- ✅ How powerful automated testing is!

---

## 💪 Practice Challenges

### Challenge 1: Test Logout

Write a test that:

1. Logs in
2. Clicks logout button
3. Verifies user is logged out (login form visible)

**Hint:** Logout button test-id is `navbar-logout-button`

### Challenge 2: Test Registration

Write a test that:

1. Goes to registration page
2. Fills all fields (use unique email!)
3. Submits
4. Verifies auto-login (navbar appears)

**Hint:** Use `/register` route

### Challenge 3: Test Reaction

Write a test that:

1. Logs in
2. Hovers over react button on first post
3. Clicks like emoji
4. Verifies emoji appears in button

**Hint:** Use `.hover()` method

---

<h2 id="troubleshooting">🐛 Troubleshooting</h2>

**Problem:** `page.goto: net::ERR_CONNECTION_REFUSED`
**Solution:** Make sure the dev servers are running (`./start-dev.sh`) so the frontend is available on <http://localhost:3000> and the API on <http://localhost:8000>

**Problem:** `Timeout waiting for element`
**Solution:** Check the data-testid is correct, or add longer timeout

**Problem:** `Test fails randomly`
**Solution:** Resist the urge to add `await page.waitForTimeout()` - a
fixed wait either isn't long enough (still flaky) or wastes time on every
run (and still isn't guaranteed long enough). Use `expect(...).toBeVisible()`
or `.toContainText()` instead: they retry until the condition is true or a
timeout is hit, so they wait exactly as long as needed. If a test is flaky
even with retrying assertions, that's usually a real race condition worth
tracking down - see [`TESTING_ANTIPATTERNS.md`](../../../docs/concepts/TESTING_ANTIPATTERNS.md#2-time-and-sleep-anti-patterns)
for a real example found and fixed in Testbook's own test suite.

---

<h2 id="lab-completion-checklist">✅ Lab Completion Checklist</h2>

- [ ] Playwright installed successfully
- [ ] Watched test run in headed mode
- [ ] Used Playwright Inspector (debug mode)
- [ ] Wrote `my_first_e2e.spec.js` and it passes
- [ ] Understand selectors and interactions
- [ ] Completed at least 1 practice challenge

---

<h2 id="pro-tips">🎯 Pro Tips</h2>

**Tip 1:** Always run in headed mode while developing

```bash
npx playwright test mytest.spec.js --headed
```

**Tip 2:** Use debug mode when test fails

```bash
npx playwright test mytest.spec.js --debug
```

**Tip 3:** Generate selectors automatically

```bash
npx playwright codegen http://localhost:3000
```

(This opens recorder - click around and it writes test code!)

---

## 🆚 JavaScript vs Python?

**Both versions of this lab teach the same concepts!**

| Aspect       | JavaScript (this lab)         | Python                           |
| ------------ | ----------------------------- | -------------------------------- |
| **Syntax**   | Async/await                   | Synchronous, clean               |
| **Best For** | JS developers, frontend teams | Python developers, backend teams |
| **Features** | Identical                     | Identical                        |
| **Speed**    | Same                          | Same                             |

**Choose based on your comfort level!** Both are excellent.

---

**🎉 You're now writing E2E tests! This is professional-level testing!**

**Next Lab:** [Lab 10: Advanced E2E Patterns (JavaScript)](LAB_10_Advanced_E2E_Patterns_JavaScript.md)
