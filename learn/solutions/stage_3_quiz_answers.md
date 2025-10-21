# Stage 3 Quiz Answers

## API & E2E Testing Quiz Answers

### 1. What's the main purpose of E2E testing?

**Answer: B) To test complete user workflows**

- E2E tests simulate real user interactions
- They test the entire application from frontend to backend
- They verify that user workflows work end-to-end
- They catch integration issues that other tests miss

### 2. What is the Page Object Model?

**Answer: B) A pattern for organizing page interactions**

- Page Object Model encapsulates page elements and actions
- It makes tests more maintainable and readable
- It separates test logic from page structure
- It's not about organizing files or running tests faster

### 3. Why are E2E tests slower than unit tests?

**Answer: B) They use real browsers and network requests**

- E2E tests launch real browsers (Chrome, Firefox, etc.)
- They make actual HTTP requests
- They interact with the full application stack
- This makes them slower but more realistic

### 4. What should you do when an E2E test fails?

**Answer: C) Investigate to determine if it's a test or app issue**

- E2E tests can fail for many reasons
- The failure might be in the test, the app, or the environment
- Always investigate before making changes
- Don't automatically assume it's the test or the app

### 5. What's the difference between E2E and integration tests?

**Answer: D) All of the above**

- E2E tests use browsers, integration tests typically don't
- Integration tests are generally faster
- E2E tests test the full stack (frontend + backend + database)
- Both are important but serve different purposes

## How Did You Do?

- **5/5:** Excellent! You understand E2E testing
- **4/5:** Very good! You're ready for Stage 4
- **3/5:** Good! Review the concepts you missed
- **2/5 or less:** Consider reviewing Stage 3 materials before moving on

## Need More Practice?

- Re-read the [Stage 3 README](../stage_3_api_e2e/README.md)
- Complete the [Stage 3 exercises](../stage_3_api_e2e/exercises/)
- Look at examples in [tests/e2e/](../../tests/e2e/)
- Practice writing your own E2E tests

## Ready for Stage 4?

If you got 3/5 or better, you're ready to move on to [Stage 4: Performance & Security](../stage_4_performance_security/README.md)!

---

_Remember: E2E testing is about testing real user workflows. Focus on what users actually do, not just technical details._
