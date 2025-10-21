# Stage 1 Quiz Answers

## Unit Tests Quiz Answers

### 1. What is the difference between unit tests and integration tests?

**Answer: B) Unit tests test individual functions in isolation**

- Unit tests test one function or method in isolation
- Integration tests test how multiple components work together
- While unit tests are often faster, that's not the defining characteristic
- Both are important, but they serve different purposes

### 2. What does AAA stand for in test structure?

**Answer: B) Arrange, Act, Assert**

- **Arrange:** Set up test data and conditions
- **Act:** Execute the function being tested
- **Assert:** Verify the expected outcome
- This pattern makes tests clear and maintainable

### 3. When would you use a pytest fixture?

**Answer: B) When you need to share setup code between tests**

- Fixtures are for sharing setup/teardown code
- They help avoid code duplication
- They can be used across multiple test functions
- They're not just for testing multiple functions

### 4. What makes a good test name?

**Answer: B) Describes what the test does**

- Good test names explain what's being tested
- They should be descriptive and clear
- Examples: `test_user_login_with_valid_credentials`, `test_password_hashing_works`
- Avoid generic names like `test_1` or `test_function`

### 5. Why do we test edge cases?

**Answer: B) They catch bugs that happy path tests miss**

- Edge cases often reveal bugs in boundary conditions
- They test the limits of your code
- Examples: empty strings, null values, maximum values
- They're not necessarily easier or more fun, but they're important

## How Did You Do?

- **5/5:** Excellent! You understand unit testing fundamentals
- **4/5:** Very good! You're ready for Stage 2
- **3/5:** Good! Review the concepts you missed
- **2/5 or less:** Consider reviewing Stage 1 materials before moving on

## Need More Practice?

- Re-read the [Stage 1 README](../stage_1_unit/README.md)
- Complete the [Stage 1 exercises](../stage_1_unit/exercises/)
- Look at examples in [backend/tests/unit/](../../backend/tests/unit/)
- Practice writing your own unit tests

## Ready for Stage 2?

If you got 3/5 or better, you're ready to move on to [Stage 2: Integration Tests](../stage_2_integration/README.md)!

---

_Remember: The goal isn't to memorize answers, but to understand the concepts. If you're unsure about any answer, review the relevant materials._
