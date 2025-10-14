# ⚡ Playwright Quick Reference

**One-page reference for Playwright E2E testing**

---

## 🚀 Essential Commands

### Running Tests

```bash
# Run all tests
npx playwright test

# Run in headed mode (see browser)
npx playwright test --headed

# Run specific file
npx playwright test auth.spec.js

# Run specific test
npx playwright test auth.spec.js:10  # Line 10

# Run tests matching pattern
npx playwright test -g "login"

# Run in UI mode (interactive)
npx playwright test --ui
```

### Debugging

```bash
# Debug mode (pause on each step)
npx playwright test --debug

# Debug specific test
npx playwright test auth.spec.js --debug

# Show browser
npx playwright test --headed

# Slow down execution
npx playwright test --headed --slow-mo=1000  # 1 second delay
```

### Browsers

```bash
# Run in specific browser
npx playwright test --project=chromium
npx playwright test --project=firefox
npx playwright test --project=webkit

# Run in all browsers
npx playwright test --project=chromium --project=firefox --project=webkit

# Install browsers
npx playwright install
npx playwright install chromium  # Just Chrome
```

### Reports

```bash
# Show HTML report
npx playwright show-report

# Generate report
npx playwright test --reporter=html

# Multiple reporters
npx playwright test --reporter=html,json

# Line reporter (minimal)
npx playwright test --reporter=line
```

---

## 🎯 Test Structure

### Basic Test

```javascript
const { test, expect } = require('@playwright/test');

test('basic test', async ({ page }) => {
  // Navigate
  await page.goto('http://localhost:3000');

  // Interact
  await page.click('button');

  // Assert
  await expect(page.locator('h1')).toHaveText('Welcome');
});
```

### Test Suite

```javascript
test.describe('Feature Name', () => {
  test.beforeEach(async ({ page }) => {
    // Setup before each test
    await page.goto('http://localhost:3000');
  });

  test('first test', async ({ page }) => {
    // Test code
  });

  test('second test', async ({ page }) => {
    // Test code
  });
});
```

### Test Hooks

```javascript
test.describe('Suite', () => {
  test.beforeAll(async ({ browser }) => {
    // Runs once before all tests
  });

  test.beforeEach(async ({ page }) => {
    // Runs before each test
  });

  test.afterEach(async ({ page }) => {
    // Runs after each test
  });

  test.afterAll(async ({ browser }) => {
    // Runs once after all tests
  });
});
```

---

## 🔍 Locators

### Finding Elements

```javascript
// By data-testid (RECOMMENDED)
page.locator('[data-testid="login-button"]')

// By text
page.locator('text=Login')
page.getByText('Login')

// By role
page.getByRole('button', { name: 'Login' })
page.getByRole('textbox', { name: 'Email' })

// By label
page.getByLabel('Email')
page.getByLabel('Password')

// By placeholder
page.getByPlaceholder('Enter email')

// By CSS selector
page.locator('.button')
page.locator('#login-form')
page.locator('button.primary')

// By XPath (avoid if possible)
page.locator('xpath=//button[@type="submit"]')

// Chaining locators
page.locator('[data-testid="post-item"]').locator('button')

// First/Last/Nth
page.locator('[data-testid="post-item"]').first()
page.locator('[data-testid="post-item"]').last()
page.locator('[data-testid="post-item"]').nth(2)
```

### Locator Filters

```javascript
// Has text
page.locator('button').filter({ hasText: 'Submit' })

// Has child
page.locator('div').filter({ has: page.locator('button') })

// Multiple filters
page.locator('article')
  .filter({ hasText: 'John' })
  .filter({ has: page.locator('button') })
```

---

## 🎬 Actions

### Click

```javascript
// Simple click
await page.click('button')
await page.locator('button').click()

// Click with options
await page.click('button', {
  button: 'right',  // right click
  clickCount: 2,    // double click
  delay: 100,       // delay between mousedown and mouseup
})

// Force click (bypass actionability checks)
await page.click('button', { force: true })
```

### Fill

```javascript
// Fill input
await page.fill('input[name="email"]', 'test@example.com')
await page.locator('input[name="email"]').fill('test@example.com')

// Clear then fill
await page.fill('input', '')
await page.fill('input', 'new value')

// Type with delay
await page.type('input', 'slow typing', { delay: 100 })
```

### Other Actions

```javascript
// Check/uncheck
await page.check('input[type="checkbox"]')
await page.uncheck('input[type="checkbox"]')

// Select option
await page.selectOption('select', 'value')
await page.selectOption('select', { label: 'Option Text' })

// Hover
await page.hover('button')

// Focus
await page.focus('input')

// Press key
await page.press('input', 'Enter')
await page.press('input', 'Control+A')

// Upload file
await page.setInputFiles('input[type="file"]', 'path/to/file.jpg')

// Multiple files
await page.setInputFiles('input[type="file"]', [
  'file1.jpg',
  'file2.jpg'
])
```

---

## ✅ Assertions

### Visibility

```javascript
// Element visible
await expect(page.locator('button')).toBeVisible()
await expect(page.locator('button')).not.toBeVisible()

// Element hidden
await expect(page.locator('button')).toBeHidden()

// Element enabled/disabled
await expect(page.locator('button')).toBeEnabled()
await expect(page.locator('button')).toBeDisabled()

// Element editable
await expect(page.locator('input')).toBeEditable()
```

### Content

```javascript
// Text content
await expect(page.locator('h1')).toHaveText('Welcome')
await expect(page.locator('h1')).toContainText('Wel')

// Multiple elements text
await expect(page.locator('li')).toHaveText(['Item 1', 'Item 2'])

// Value
await expect(page.locator('input')).toHaveValue('test@example.com')

// Attribute
await expect(page.locator('button')).toHaveAttribute('type', 'submit')
await expect(page.locator('button')).toHaveAttribute('disabled')

// Class
await expect(page.locator('div')).toHaveClass('active')
await expect(page.locator('div')).toHaveClass(/active/)

// Count
await expect(page.locator('li')).toHaveCount(5)
```

### Page

```javascript
// URL
await expect(page).toHaveURL('http://localhost:3000')
await expect(page).toHaveURL(/login/)

// Title
await expect(page).toHaveTitle('Testbook')
await expect(page).toHaveTitle(/Fake/)

// Screenshot comparison
await expect(page).toHaveScreenshot('screenshot.png')
```

---

## ⏱️ Waiting

### Auto-Waiting

```javascript
// Playwright auto-waits for:
// - Element to be visible
// - Element to be enabled
// - Element to be stable (not animating)

await page.click('button')  // Waits automatically
```

### Manual Waiting

```javascript
// Wait for selector
await page.waitForSelector('button')
await page.waitForSelector('button', { state: 'visible' })
await page.waitForSelector('button', { state: 'hidden' })

// Wait for URL
await page.waitForURL('http://localhost:3000/profile')
await page.waitForURL(/profile/)

// Wait for load state
await page.waitForLoadState('load')  // DOMContentLoaded
await page.waitForLoadState('domcontentloaded')
await page.waitForLoadState('networkidle')

// Wait for timeout
await page.waitForTimeout(1000)  // ⚠️ Avoid - use rarely!

// Wait for function
await page.waitForFunction(() => {
  return document.querySelectorAll('li').length > 5
})
```

---

## 🎯 Navigation

```javascript
// Go to URL
await page.goto('http://localhost:3000')

// Go back/forward
await page.goBack()
await page.goForward()

// Reload
await page.reload()

// Wait for navigation
await Promise.all([
  page.waitForNavigation(),
  page.click('a')
])
```

---

## 📸 Screenshots & Videos

```javascript
// Screenshot element
await page.locator('button').screenshot({ path: 'button.png' })

// Screenshot page
await page.screenshot({ path: 'page.png' })

// Full page screenshot
await page.screenshot({
  path: 'full-page.png',
  fullPage: true
})

// Video recording (in playwright.config.js)
use: {
  video: 'on',  // or 'retain-on-failure'
}
```

---

## 🔧 Common Patterns

### Login Helper

```javascript
async function loginUser(page, email, password) {
  await page.goto('http://localhost:3000');
  await page.fill('[data-testid="login-email-input"]', email);
  await page.fill('[data-testid="login-password-input"]', password);
  await page.click('[data-testid="login-submit-button"]');
  await expect(page.locator('[data-testid="navbar"]')).toBeVisible();
}

// Usage
test('test something', async ({ page }) => {
  await loginUser(page, 'test@test.com', 'password');
  // Continue test...
});
```

### Get First Post

```javascript
async function getFirstPost(page) {
  return page.locator('[data-testid-generic="post-item"]').first();
}

// Usage
const post = await getFirstPost(page);
await post.locator('[data-testid$="-like-button"]').click();
```

### Reset Database

```javascript
async function resetDatabase(page) {
  await page.request.post('http://localhost:8000/api/dev/reset');
}

// Usage in beforeEach
test.beforeEach(async ({ page }) => {
  await resetDatabase(page);
});
```

---

## 🐛 Debugging

### Playwright Inspector

```javascript
// Add breakpoint in test
await page.pause()

// Run with --debug
npx playwright test --debug
```

### Show Browser

```javascript
// Run headed mode
npx playwright test --headed

// Keep browser open on failure
use: {
  headless: false,
  launchOptions: {
    slowMo: 50  // Slow down by 50ms
  }
}
```

### Verbose Logging

```javascript
// Enable debug logs
DEBUG=pw:api npx playwright test

// Log to console
console.log(await page.locator('h1').textContent())
```

---

## 📋 Configuration (playwright.config.js)

```javascript
module.exports = {
  testDir: './tests/e2e',
  timeout: 30000,
  retries: 2,

  use: {
    baseURL: 'http://localhost:3000',
    headless: true,
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    trace: 'on-first-retry',
  },

  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
  ],

  webServer: {
    command: 'npm run dev',
    port: 3000,
    reuseExistingServer: true,
  },
};
```

---

## 🚨 Common Issues

### Element Not Found

```javascript
// Issue: Timeout waiting for element
// Fix: Check selector is correct
await page.locator('[data-testid="exact-name"]').click()

// Fix: Wait for page to load
await page.waitForLoadState('domcontentloaded')

// Fix: Check element is visible
await page.waitForSelector('[data-testid="element"]', { state: 'visible' })
```

### Flaky Tests

```javascript
// Issue: Test sometimes passes, sometimes fails

// Fix 1: Don't use timeouts
// ❌ BAD
await page.waitForTimeout(1000)
await page.click('button')

// ✅ GOOD
await page.waitForSelector('button', { state: 'visible' })
await page.click('button')

// Fix 2: Wait for network to settle
await page.waitForLoadState('networkidle')

// Fix 3: Use proper assertions with retries
await expect(page.locator('h1')).toHaveText('Welcome')
```

### Click Not Working

```javascript
// Issue: Element not clickable

// Fix 1: Wait for element
await page.waitForSelector('button', { state: 'visible' })
await page.click('button')

// Fix 2: Force click (bypass checks)
await page.click('button', { force: true })

// Fix 3: Click by JavaScript
await page.evaluate(() => document.querySelector('button').click())
```

---

## 💡 Best Practices

1. **Use data-testid for selectors** - More stable than CSS classes

   ```javascript
   ✅ page.locator('[data-testid="login-button"]')
   ❌ page.locator('.btn-primary.login')
   ```

2. **Don't use timeouts** - Use proper waits

   ```javascript
   ❌ await page.waitForTimeout(2000)
   ✅ await page.waitForSelector('[data-testid="element"]')
   ```

3. **Use auto-waiting assertions** - Built-in retries

   ```javascript
   ✅ await expect(page.locator('h1')).toHaveText('Welcome')
   ❌ expect(await page.locator('h1').textContent()).toBe('Welcome')
   ```

4. **Reset state between tests** - Use beforeEach

   ```javascript
   test.beforeEach(async ({ page }) => {
     await resetDatabase(page);
   });
   ```

5. **Use helper functions** - DRY principle

   ```javascript
   const { loginUser, createPost } = require('./test-helpers');
   ```

6. **Take screenshots on failure** - Configured in playwright.config.js

   ```javascript
   use: {
     screenshot: 'only-on-failure',
   }
   ```

---

## 📚 Related Resources

- [Playwright Documentation](https://playwright.dev/)
- [tests/README.md](../../tests/README.md) - Testbook E2E tests
- [TESTING_PATTERNS.md](TESTING_PATTERNS.md) - Testing dynamic content

---

**🎯 Most Common Usage:**

```bash
# While developing a test
npx playwright test auth.spec.js --headed --debug

# Before committing
npx playwright test

# Full cross-browser test
npx playwright test --project=chromium --project=firefox --project=webkit
```
