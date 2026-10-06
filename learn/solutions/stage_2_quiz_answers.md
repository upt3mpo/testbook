# Stage 2 Quiz Answers

## Integration Tests Quiz Answers

### 1. What's the main difference between unit tests and integration tests?

**Answer: B) Integration tests test multiple components together**

- Unit tests test individual functions in isolation
- Integration tests test how multiple components work together
- Both can be fast or slow depending on what they test
- Both are important, but they serve different purposes

### 2. What does FastAPI TestClient do?

**Answer: B) Provides a test interface for FastAPI apps**

- TestClient simulates HTTP requests to your FastAPI app
- It allows you to test API endpoints without running a server
- It doesn't run tests faster or create data automatically
- It's specifically designed for testing FastAPI applications

### 3. Why do integration tests need database setup?

**Answer: B) To test real database operations**

- Integration tests verify that components work together correctly
- Database operations are a key part of most applications
- You need real database interactions to test the full workflow
- Mocks wouldn't catch database-related bugs

### 4. What's the purpose of test factories?

**Answer: A) To create test data easily**

- Test factories generate realistic test data
- They reduce code duplication in test setup
- They make tests more maintainable
- They don't run tests in parallel or mock services

### 5. When testing API endpoints, what should you verify?

**Answer: C) Status code, response data, and headers**

- Status code tells you if the request succeeded
- Response data contains the actual result
- Headers can contain important metadata
- You should verify all aspects of the response

### 6. An API returns a validation error as a list of objects, but the frontend assumed a string, and the page went blank. Which test would have caught the mismatch earliest?

**Answer: B) A test that pins the shape of the API's error responses, or a component test fed the real error shape**

- The bug lived in the **gap between two pieces**. Testbook's API returns a plain string for most
  errors and a list of objects for HTTP 422. The frontend only handled the string.
- A test on the **producer** that asserts "`detail` is a string or a list of issues with a `msg` and
  a `loc`" documents both shapes, so the frontend developer learns about the list.
- A test on the **consumer** that renders the component with the real list-shaped error fails the
  moment the component cannot cope. Both are cheap, run in milliseconds, and need no browser.
- A load test (A) and a home-page visual test (D) say nothing about error handling. A manual
  click-through (C) only finds it if someone happens to try an email like `a@b`.
- See [audit finding A11Y-019](../../docs/a11y/AUDIT_LOG.md).

## How Did You Do?

- **6/6:** Excellent! You understand integration testing
- **5/6:** Very good! You're ready for Stage 3
- **4/6:** Good! Review the concepts you missed
- **3/6 or less:** Consider reviewing Stage 2 materials before moving on

## Need More Practice?

- Re-read the [Stage 2 README](../stage_2_integration/README.md)
- Complete the [Stage 2 exercises](../stage_2_integration/exercises/)
- Look at examples in [backend/tests/integration/](../../backend/tests/integration/)
- Practice writing your own integration tests

## Ready for Stage 3?

If you got 4/6 or better, you're ready to move on to [Stage 3: API & E2E Testing](../stage_3_api_e2e/README.md)!

---

_Remember: Integration testing is about testing how components work together. Focus on real interactions, not just individual pieces._
