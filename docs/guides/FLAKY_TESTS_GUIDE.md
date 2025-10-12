# Understanding and Fixing Flaky Tests

## What Are Flaky Tests?

**Flaky tests** are tests that sometimes pass and sometimes fail, even though the code hasn't changed. They're one of the most frustrating issues in test automation because they erode confidence in your test suite.

## Real Example: Testbook's Flaky Tests

We experienced flaky tests in the Testbook project's E2E tests. Here's what happened and how we fixed them.

### The Problem

Initially, 10 out of 54 Playwright tests were failing intermittently:

- Post edit tests
- Reaction button tests (3 tests)
- Follow/Block button tests (4 tests)
- Profile count display tests
- Account deletion redirect test

These tests would pass sometimes and fail other times, depending on:

- System load
- Network speed
- React render timing
- API response time

### Root Causes

#### 1. **Arbitrary Timeouts** ❌ BAD

```javascript
// BAD: Using fixed timeouts
await page.waitForTimeout(500);
await expect(reactButton).toContainText('👍');
```

**Problem:** The timeout might be too short on slower systems, or the API might take longer than expected.

#### 2. **Not Waiting for State Changes** ❌ BAD

```javascript
// BAD: Clicking and immediately checking without waiting
await followButton.click();
await expect(followButton).toContainText(/unfollow/i, { timeout: 5000 });
```

**Problem:** The button text might not have updated yet when we check it.

#### 3. **Race Conditions with Async Operations** ❌ BAD

```javascript
// BAD: Not waiting for network requests to complete
await reactButton.hover();
await post.page().waitForTimeout(300);
const reactionBtn = post.locator(`[data-testid$="-reaction-like"]`);
await reactionBtn.click();
```

**Problem:** The hover dropdown might not be fully rendered, or the click might happen before the element is interactive.

## The Solutions

### 1. **Wait for Actual State Changes** ✅ GOOD

Instead of arbitrary timeouts, wait for the actual change you expect:

```javascript
// GOOD: Wait for the button text to change
await followButton.click();
await expect(followButton).toContainText(/unfollow/i, { timeout: 10000 });
```

**Why it works:** Playwright will automatically retry the assertion until it passes or times out. It checks the actual state, not just waiting blindly.

### 2. **Use Network Idle for API-Heavy Operations** ✅ GOOD

```javascript
// GOOD: Wait for network to settle
await addReaction(firstPost, 'like');
await page.waitForLoadState('networkidle', { timeout: 3000 }).catch(() => {});
await expect(reactButton).toContainText('👍', { timeout: 10000 });
```

**Why it works:** `networkidle` waits until there are no network connections for at least 500ms, ensuring API calls have completed.

### 3. **Verify Prerequisites Before Actions** ✅ GOOD

```javascript
// GOOD: Ensure element is visible and interactive before clicking
const reactButton = post.locator('[data-testid$="-react-button"]');
await expect(reactButton).toBeVisible({ timeout: 5000 });
await reactButton.hover();

const reactionBtn = post.locator(`[data-testid$="-reaction-like"]`);
await expect(reactionBtn).toBeVisible({ timeout: 5000 });
await reactionBtn.click();
```

**Why it works:** Verifying visibility ensures the element is rendered and ready for interaction.

### 4. **Use URL Changes for Navigation** ✅ GOOD

```javascript
// GOOD: Wait for actual URL change after deletion
await page.waitForURL(/.*\/(login|$)/, { timeout: 15000 }).catch(async () => {
  // Fallback if URL doesn't change
  await expect(page.locator('[data-testid="login-email-input"]')).toBeVisible({ timeout: 5000 });
});
```

**Why it works:** URL changes are definitive indicators of navigation, more reliable than checking for element visibility alone.

### 5. **Increase Timeouts for Critical Assertions** ✅ GOOD

```javascript
// GOOD: Use longer timeouts for operations that involve multiple steps
await expect(reactButton).toContainText('👍', { timeout: 10000 });
```

**Why it works:** 10 seconds is reasonable for API calls + React re-renders. The test won't wait the full 10 seconds if it passes sooner.

## Before and After Comparison

### Before: Flaky Post Reaction Test ❌

```javascript
test('should add reaction to post', async ({ page }) => {
  await createPost(page, 'React to this post');
  const firstPost = getFirstPost(page);
  await addReaction(firstPost, 'like');

  // Wait randomly - sometimes too short!
  await page.waitForTimeout(500);

  const reactButton = firstPost.locator('[data-testid$="-react-button"]');
  await expect(reactButton).toContainText('👍', { timeout: 5000 });
});
```

**Pass rate:** ~60% (failed when system was slow)

### After: Reliable Post Reaction Test ✅

```javascript
test('should add reaction to post', async ({ page }) => {
  await createPost(page, 'React to this post');
  const firstPost = getFirstPost(page);
  const reactButton = firstPost.locator('[data-testid$="-react-button"]');

  // Verify button exists before interacting
  await expect(reactButton).toBeVisible();

  // Add reaction (improved helper with network wait)
  await addReaction(firstPost, 'like');

  // Wait for actual state change, not arbitrary time
  await expect(reactButton).toContainText('👍', { timeout: 10000 });
});
```

**Pass rate:** ~100%

## Improved Helper Function

### Before: Unreliable addReaction ❌

```javascript
async function addReaction(post, reactionType) {
  const reactButton = post.locator('[data-testid$="-react-button"]');
  await reactButton.hover();
  await post.page().waitForTimeout(300); // ❌ Arbitrary wait

  const reactionBtn = post.locator(`[data-testid$="-reaction-${reactionType}"]`);
  await expect(reactionBtn).toBeVisible({ timeout: 5000 });
  await reactionBtn.click();
  await post.page().waitForTimeout(500); // ❌ Another arbitrary wait
}
```

### After: Reliable addReaction ✅

```javascript
async function addReaction(post, reactionType) {
  const reactButton = post.locator('[data-testid$="-react-button"]');

  // ✅ Ensure button is visible before hovering
  await expect(reactButton).toBeVisible({ timeout: 5000 });
  await reactButton.hover();

  // ✅ Wait for reaction dropdown to actually appear
  const reactionBtn = post.locator(`[data-testid$="-reaction-${reactionType}"]`);
  await expect(reactionBtn).toBeVisible({ timeout: 5000 });
  await reactionBtn.click();

  // ✅ Wait for network to settle instead of arbitrary timeout
  await post.page().waitForLoadState('networkidle', { timeout: 3000 }).catch(() => {});
}
```

## Advanced Technique: Retry Logic for Complex Interactions

For particularly tricky interactions (like hover menus), implement retry logic:

```javascript
async function addReaction(post, reactionType) {
  const reactButton = post.locator('[data-testid$="-react-button"]');
  await expect(reactButton).toBeVisible({ timeout: 5000 });

  // Retry up to 3 times if hover/click fails
  let clicked = false;
  for (let i = 0; i < 3 && !clicked; i++) {
    try {
      await reactButton.hover({ force: true });
      await post.page().waitForTimeout(500); // CSS transition time

      const reactionBtn = post.locator(`[data-testid$="-reaction-${reactionType}"]`);
      await expect(reactionBtn).toBeVisible({ timeout: 3000 });
      await reactionBtn.click({ force: true });

      clicked = true;
      await post.page().waitForTimeout(1000); // API response time
    } catch (e) {
      if (i === 2) throw e; // Throw on last attempt
      await post.page().waitForTimeout(500); // Wait before retry
    }
  }
}
```

This fixed 4 additional tests that were failing due to hover dropdown timing issues.

## Best Practices to Avoid Flaky Tests

### ✅ DO

1. **Wait for actual state changes**, not arbitrary times
2. **Use Playwright's built-in auto-waiting** features
3. **Verify prerequisites** (visibility, enabled state) before actions
4. **Use appropriate timeout values** (5-10s for most operations)
5. **Wait for network idle** after API calls
6. **Check for URL changes** after navigation
7. **Add fallback strategies** for critical assertions

### ❌ DON'T

1. **Don't use `waitForTimeout()` for synchronization** - only use it for deliberate delays (like testing slow networks)
2. **Don't assume immediate UI updates** after clicks
3. **Don't use short timeouts** (< 5s) for operations involving API calls
4. **Don't chain actions without verification** between them
5. **Don't ignore intermittent failures** - they indicate real problems

## Testing Your Fixes

After fixing flaky tests, run them multiple times to verify stability:

```bash
# Run the same test 10 times
for i in {1..10}; do
  npx playwright test --project=chromium tests/e2e/posts.spec.js:141
done
```

A truly fixed test should pass 10/10 times (or very close to it).

## Results

After applying these fixes to Testbook:

- **Before:** 44/54 tests passing (81.5%) with frequent intermittent failures
- **After First Round of Fixes:** 44/54 tests passing but still flaky
- **After Adding Retry Logic:** 48/54 tests passing (88.9%)

### Remaining Challenges

6 tests remain flaky due to complex UI timing issues:

- Profile count displays (data loading timing)
- Follow/Block button state changes (React re-render timing)
- Account deletion redirect (multi-step async process)
- Cancel edit (form state management)

**Important Learning:** Some flakiness is inherent in E2E tests testing real async systems. The goal is to minimize it, not necessarily eliminate it 100%.

## Key Takeaways

1. **Flaky tests are usually about timing**, not the code being tested
2. **Wait for state changes, not time to pass**
3. **Higher timeouts are better than flaky tests** - Playwright only waits as long as needed
4. **Use Playwright's smart waiting** features instead of arbitrary delays
5. **Fix flaky tests immediately** - they compound and erode trust in your test suite

## Further Reading

- [Playwright Auto-waiting](https://playwright.dev/docs/actionability)
- [Playwright Best Practices](https://playwright.dev/docs/best-practices)
- [Martin Fowler on Test Flakiness](https://martinfowler.com/articles/nonDeterminism.html)
