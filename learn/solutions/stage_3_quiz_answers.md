# Stage 3 Quiz Answers

## API & E2E Testing Quiz Answers

### 1. What's the main difference between E2E tests and integration tests?

**Answer: B) E2E tests simulate real user interactions**

- E2E tests drive a real browser the way a user would - clicking, typing, navigating
- Integration tests call APIs or components directly, without a browser in the loop
- E2E tests are slower and more prone to flakiness in exchange for catching real UI/UX bugs
- "Faster" (A) and "more important" (D) are both false - E2E tests are slower and are a smaller slice of the pyramid, not a bigger one

### 2. What is the Page Object Model?

**Answer: B) A design pattern for reusable page interactions**

- POM centralizes a page's selectors and actions into one class (see `tests/e2e-python/pages/feed_page.py` or `tests/e2e/fixtures/test-helpers.js`)
- Tests call methods like `feed.create_post(...)` instead of repeating raw selectors everywhere
- If a selector changes, you update it in one place instead of in every test that uses it
- It's not a file-organization convention (A), a screenshot tool (C), or specifically about async handling (D) - those are separate concerns

### 3. Why do E2E tests need to handle async operations?

**Answer: B) Because browsers are asynchronous**

- Page navigation, network requests, and UI re-renders all happen asynchronously in a real browser
- A test that clicks "submit" and immediately asserts on the result will often run before the response arrives
- That's why Playwright's `expect(...).to_be_visible()` / `toBeVisible()` retry-wait instead of checking once
- This has nothing to do with test speed (A), avoiding mocks (C), or testing multiple functions (D)

### 4. What's the purpose of API contract testing?

**Answer: B) To verify API response structure**

- Contract tests check that responses have the fields and types the frontend expects (see `backend/tests/integration/test_api_contract.py`)
- They catch a backend change that silently breaks the frontend, before it reaches production
- They're not about performance (A), mocking (C), or security (D) - those are separate test categories covered elsewhere in the curriculum

### 5. When should you use E2E tests?

**Answer: B) For critical user workflows only**

- E2E tests are the slowest and most expensive tests to write and maintain, so they're reserved for flows that matter most (login, checkout, posting)
- Using them for every test case (A) would make the suite painfully slow and flaky
- They're not a substitute for unit testing (C) or API testing (D) - each layer of the pyramid covers what the others can't

## How Did You Do?

- **5/5:** Excellent! You understand E2E testing
- **4/5:** Very good! You're ready for Stage 4
- **3/5:** Good! Review the concepts you missed
- **2/5 or less:** Consider reviewing Stage 3 materials before moving on

## Need More Practice?

- Re-read the [Stage 3 README](../stage_3_api_e2e/README.md)
- Complete the [Stage 3 exercises](../stage_3_api_e2e/exercises/)
- Look at examples in [tests/e2e-python/](../../tests/e2e-python/) (Python) or [tests/e2e/](../../tests/e2e/) (JavaScript)
- Practice writing your own E2E tests

## Ready for Stage 4?

If you got 3/5 or better, you're ready to move on to [Stage 4: Performance & Security](../stage_4_performance_security/README.md)!

---

_Remember: E2E testing is about testing real user workflows. Focus on what users actually do, not just technical details._
