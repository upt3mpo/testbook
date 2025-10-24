# 🧪 Stage 1: Unit Tests

**Foundation of Test Automation**

> **💡 Language Selection**: This guide includes both Python and JavaScript examples. Both are expanded by default so you can see all approaches. Click the language tabs to collapse sections you don't need.

## Your Progress

[████░░░░░░░░░░░░░░░░] 20% complete

→ **Stage 1: Unit Tests** (you are here)<br>
⬜ Stage 2: Integration Tests<br>
⬜ Stage 3: E2E Testing<br>
⬜ Stage 4: Performance & Security<br>
⬜ Stage 5: Capstone

**Estimated time remaining:** 4-6 hours (core content) + 2-3 hours (optional exercises)

<h2 id="table-of-contents">📋 Table of Contents</h2>

- [Why Unit Testing Matters: The Foundation of Quality](#why-unit-testing-matters-the-foundation-of-quality)
- [Part 1: What Are Unit Tests? 📚](#part-1-what-are-unit-tests)
- [Part 2: The AAA Pattern 🎯](#part-2-the-aaa-pattern)
- [Part 3: Test Fixtures & Setup 🛠️](#part-3-test-fixtures--setup)
- [Part 4: Implementation Guide 🛠️](#part-4-implementation-guide)
- [Part 5: Hands-On Practice 🏃](#part-5-hands-on-practice)
- [Part 6: Additional Patterns 🚀](#part-6-additional-patterns)
- [✅ Success Criteria](#success-criteria)
- [🧠 Why This Matters](#why-this-matters)
- [🔗 Related Resources](#related-resources)
- [🧠 Self-Check Quiz (Optional)](#self-check-quiz-optional)
- [🤔 Reflection](#reflection)
- [🎉 Stage Complete](#stage-complete)

---

## Why Unit Testing Matters: The Foundation of Quality

### The Real-World Impact

**The Problem Without Unit Tests:**
In 2012, Knight Capital Group deployed code without proper unit testing. A single line of code change caused their trading system to lose $440 million in 45 minutes, nearly bankrupting the company. The bug? A function that should have been called once was called multiple times due to a missing unit test that would have caught this logic error.

**What Unit Tests Prevent:**

1. **Logic Errors**: Functions that work for some inputs but fail for others
2. **Regression Bugs**: New changes that break existing functionality
3. **Integration Failures**: Components that work alone but fail together
4. **Performance Issues**: Code that works but is too slow for production
5. **Security Vulnerabilities**: Code that works but has security holes

### The Testing Pyramid Applied

```text
                ▲
               /_\  ← Manual / Exploratory Testing
              /   \
             / E2E \  ← Playwright (JS / Python)
            /_______\
           /         \
          / Component \  ← Vitest + RTL (JS only)
         /_____________\
        /               \
       /  Integration    \  ← API / Component tests
      /___________________\
     /                     \
    /      Unit Tests       \  ← Vitest (JS) | pytest (Python) ← STAGE 1: BUILDING FOUNDATION
   /_________________________\
```

**Unit Tests (80% of your test suite):**

- Fast: Run in milliseconds
- Reliable: Don't depend on external systems
- Precise: Tell you exactly what broke
- Cheap: Easy to write and maintain

**Why 80%?**

- Most bugs are in individual functions
- Unit tests catch bugs early (cheapest to fix)
- They run fast (you'll run them thousands of times per day)
- They give you confidence to refactor and improve code

### The Business Case

**Cost of Bugs by Stage:**

- **Unit Testing**: $1 to fix
- **Integration Testing**: $10 to fix
- **System Testing**: $100 to fix
- **Production**: $1,000+ to fix

**Real Example:**
A banking application processes 1 million transactions per day. A bug in the interest calculation function could affect every transaction. Without unit tests:

- Bug goes to production
- 1 million incorrect calculations
- $50,000 in incorrect interest payments
- Customer trust lost
- Regulatory fines

With unit tests:

- Bug caught in development
- Fixed in 5 minutes
- Cost: $0

### The Developer Experience

**Without Unit Tests:**

- "I'm afraid to change this code"
- "Let me manually test this 20 times"
- "I hope I didn't break anything"
- "Why is this failing? I didn't touch that code!"

**With Unit Tests:**

- "I can refactor confidently"
- "I know exactly what I broke"
- "I can add features without fear"
- "My code documents itself"

### The Quality Mindset

**Unit Testing Teaches You:**

1. **Think About Edge Cases**: What happens with null, empty, or invalid inputs?
2. **Design Better APIs**: If it's hard to test, it's probably hard to use
3. **Write Cleaner Code**: Testable code is usually well-structured code
4. **Document Intent**: Tests show how code should be used
5. **Catch Mistakes Early**: Fix bugs when they're cheap to fix

### Industry Standards

**Companies That Require Unit Tests:**

- Google: 100% unit test coverage for critical systems
- Microsoft: Unit tests required for all production code
- Amazon: "No code without tests" policy
- Netflix: Unit tests run on every commit

**Why They Do This:**

- Prevents production bugs
- Enables faster development
- Reduces maintenance costs
- Improves code quality
- Builds team confidence

---

<h2 id="part-1-what-are-unit-tests">Part 1: What Are Unit Tests? 📚</h2>

### The LEGO Brick Analogy

Imagine building with LEGO bricks. Before building a castle, you'd want to make sure each individual brick isn't cracked or broken, right? Unit tests are like testing each LEGO brick individually.

A **unit test** verifies that a single "unit" of code (usually a function) works correctly in isolation.

### Why Unit Tests Matter

1. **Speed**: Run in milliseconds (you'll run thousands per day)
2. **Pinpoint failures**: Tells you EXACTLY which function broke
3. **Safety net**: Refactor code confidently
4. **Documentation**: Tests show how functions should work

### Your First Unit Test (Concept)

Let's test a simple function that adds two numbers:

<details open>
<summary><strong>🐍 Python</strong></summary>

```python
# The function we want to test
def add(a, b):
    return a + b

# The unit test
def test_add():
    # Arrange: Set up test data
    x = 2
    y = 3

    # Act: Call the function
    result = add(x, y)

    # Assert: Verify the result
    assert result == 5
```

</details>

<details open>
<summary><strong>☕ JavaScript</strong></summary>

```javascript
// The function we want to test
function add(a, b) {
  return a + b;
}

// The unit test
it("add function works correctly", () => {
  // Arrange: Set up test data
  const x = 2;
  const y = 3;

  // Act: Call the function
  const result = add(x, y);

  // Assert: Verify the result
  expect(result).toBe(5);
});
```

</details>

**What just happened?**

1. We isolated ONE function (`add`)
2. We provided known inputs (2 and 3)
3. We verified the output (5)
4. No database, no API, no complexity—just pure logic

### JavaScript Testing Functions: `test()` vs `it()`

**Quick Note:** You'll see both `test()` and `it()` in JavaScript examples. They're **identical** - just different ways to write the same thing:

```javascript
// These are exactly the same:
test("add function works correctly", () => {
  expect(add(2, 3)).toBe(5);
});

it("add function works correctly", () => {
  expect(add(2, 3)).toBe(5);
});
```

**Why the difference?**

- **`test()`** - Direct, clear function name
- **`it()`** - Reads like English: "it should add two numbers correctly"

**Which to use?** Pick one and be consistent! Most teams prefer `it()` because it reads more naturally, but `test()` is perfectly fine too.

> **💡 Quick Reference:** Throughout this course, we'll use `it()` in JavaScript examples because it reads more naturally ("it should do this..."). If you see `test()` in older examples, just mentally replace it with `it()` - they work exactly the same!

### Unit Test Characteristics

**FIRST Principles:**

- **F**ast - Runs in milliseconds
- **I**ndependent - Doesn't depend on other tests
- **R**epeatable - Same result every time
- **S**elf-validating - Pass or fail, no manual checking
- **T**imely - Written alongside or before code

---

<h2 id="part-2-the-aaa-pattern">Part 2: The AAA Pattern 🎯</h2>

Every good unit test follows the **Arrange-Act-Assert** pattern. Think of it like following a recipe:

### The Recipe Analogy

**Arrange** = Gather ingredients (set up test data)<br>
**Act** = Cook the dish (call the function)<br>
**Assert** = Taste and verify (check the result)

### AAA in Action

<details open>
<summary><strong>🐍 Python</strong></summary>

```python
def test_calculate_discount():
    # Arrange - Set up test data
    price = 100.0
    discount_percent = 20

    # Act - Execute the function being tested
    final_price = calculate_discount(price, discount_percent)

    # Assert - Verify the result
    assert final_price == 80.0
```

</details>

<details open>
<summary><strong>☕ JavaScript</strong></summary>

```javascript
it("calculate discount works correctly", () => {
  // Arrange - Set up test data
  const price = 100.0;
  const discountPercent = 20;

  // Act - Execute the function being tested
  const finalPrice = calculateDiscount(price, discountPercent);

  // Assert - Verify the result
  expect(finalPrice).toBe(80.0);
});
```

</details>

### Why AAA Works

1. **Clear structure**: Anyone can read and understand the test
2. **Easy debugging**: When a test fails, you know exactly which phase had the problem
3. **Consistent**: All tests follow the same pattern
4. **Maintainable**: Easy to modify when requirements change

### Common AAA Mistakes

❌ **Mixing phases:**

<details open>
<summary><strong>🐍 Python</strong></summary>

```python
def test_bad_example():
    result = add(2, 3)  # Act
    assert result == 5  # Assert
    # Where's the Arrange? What if we need different inputs?
```

</details>

<details open>
<summary><strong>☕ JavaScript</strong></summary>

```javascript
it("bad example", () => {
  const result = add(2, 3); // Act
  expect(result).toBe(5); // Assert
  // Where's the Arrange? What if we need different inputs?
});
```

</details>

✅ **Clear separation:**

<details open>
<summary><strong>🐍 Python</strong></summary>

```python
def test_good_example():
    # Arrange
    x = 2
    y = 3

    # Act
    result = add(x, y)

    # Assert
    assert result == 5
```

</details>

<details open>
<summary><strong>☕ JavaScript</strong></summary>

```javascript
it("good example", () => {
  // Arrange
  const x = 2;
  const y = 3;

  // Act
  const result = add(x, y);

  // Assert
  expect(result).toBe(5);
});
```

</details>

<h2 id="part-3-test-fixtures--setup">Part 3: Test Fixtures & Setup 🛠️</h2>

### The Kitchen Prep Station Analogy

Imagine you're cooking multiple dishes. Instead of washing the same vegetables for each dish, you'd prep them once and use them throughout your cooking session. Test fixtures work the same way.

A **fixture** is reusable test data or setup that multiple tests can use.

### Simple Fixture Example

<details open>
<summary><strong>🐍 Python</strong></summary>

```python
# Without fixture (repetitive)
def test_user_login():
    user = User(username="testuser", email="test@example.com")
    # ... test login logic

def test_user_profile():
    user = User(username="testuser", email="test@example.com")
    # ... test profile logic

# With fixture (DRY - Don't Repeat Yourself)
@pytest.fixture
def test_user():
    return User(username="testuser", email="test@example.com")

def test_user_login(test_user):
    # ... test login logic

def test_user_profile(test_user):
    # ... test profile logic
```

</details>

<details open>
<summary><strong>☕ JavaScript</strong></summary>

```javascript
// Without fixture (repetitive)
it("user login", () => {
  const user = { username: "testuser", email: "test@example.com" };
  // ... test login logic
});

it("user profile", () => {
  const user = { username: "testuser", email: "test@example.com" };
  // ... test profile logic
});

// With fixture (DRY - Don't Repeat Yourself)
const createTestUser = () => ({
  username: "testuser",
  email: "test@example.com",
});

it("user login", () => {
  const testUser = createTestUser();
  // ... test login logic
});

it("user profile", () => {
  const testUser = createTestUser();
  // ... test profile logic
});
```

</details>

### Why Use Fixtures?

1. **DRY Principle**: Don't Repeat Yourself
2. **Consistency**: Same test data across all tests
3. **Maintainability**: Change data in one place
4. **Cleanup**: Automatic setup and teardown

### Fixture Lifecycle

<details open>
<summary><strong>🐍 Python</strong></summary>

```python
@pytest.fixture
def database_connection():
    # Setup: Run before each test
    conn = create_database_connection()
    yield conn  # Provide to test
    # Teardown: Run after each test
    conn.close()
```

</details>

<details open>
<summary><strong>☕ JavaScript</strong></summary>

```javascript
// Setup and teardown with beforeEach/afterEach
let databaseConnection;

beforeEach(() => {
  // Setup: Run before each test
  databaseConnection = createDatabaseConnection();
});

afterEach(() => {
  // Teardown: Run after each test
  databaseConnection.close();
});

// Or with a custom helper function
const withDatabase = (testFn) => {
  return () => {
    const conn = createDatabaseConnection();
    try {
      testFn(conn);
    } finally {
      conn.close();
    }
  };
};
```

</details>

---

<h2 id="part-4-implementation-guide">Part 4: Implementation Guide 🛠️</h2>

Now let's see these concepts in real code!

<details open>
<summary><strong>🐍 Python: Testing Authentication Functions</strong></summary>

**Open `backend/tests/unit/test_auth.py` and find `test_password_is_hashed`:**

```python
def test_password_is_hashed(self):
    """
    Test that password hashing produces a different string.

    This test verifies the fundamental security principle: passwords
    must be transformed, not stored in plain text. We check:
    1. Hash is different from original password
    2. Hash is longer (bcrypt adds salt and metadata)
    3. Hash follows bcrypt format ($2b$ prefix)

    This is a critical security test - if this fails, user passwords
    would be stored in plain text, which is a major security vulnerability.
    """
    # Arrange - Set up test data
    password = "TestPassword123!"

    # Act - Execute the function being tested
    hashed = get_password_hash(password)

    # Assert - Verify the results
    assert hashed != password  # Password is transformed, not stored plainly
    assert len(hashed) > len(password)  # Hash is longer than original
    assert hashed.startswith("$2b$")  # bcrypt hash format (industry standard)
```

**Guided Walkthrough:**

1. **Arrange**: We create a test password
2. **Act**: We call the `get_password_hash()` function
3. **Assert**: We verify three things:
   - The hash is different from the original password
   - The hash is longer (bcrypt adds salt)
   - The hash starts with "$2b$" (bcrypt format)

**Try This:**

1. **Run the test from command line:**

   ```bash
   # Run specific test
   pytest backend/tests/unit/test_auth.py::TestPasswordHashing::test_password_is_hashed -v

   # Run all tests in file
   pytest backend/tests/unit/test_auth.py -v

   # Run with coverage
   pytest backend/tests/unit/test_auth.py --cov=backend.auth --cov-report=html
   ```

2. **Make it fail intentionally to understand error messages:**

   ```python
   # Temporarily change this line in the test:
   assert hashed != password  # Change to: assert hashed == password
   ```

   Then run the test and see the detailed error message that helps you debug!

3. **Fix it back and run again to see it pass**

**What you'll learn:**

- How to run tests from command line
- How to interpret test failure messages
- How to debug failing tests
- The importance of clear assertion messages

> **💡 Notice: No coverage report!** When running single tests for debugging, we skip coverage to keep output clean and focused. To see coverage, add `--cov=. --cov-report=html` to your pytest command. See [Understanding Pytest Flags](../../docs/guides/RUNNING_TESTS.md#understanding-pytest-flags) for more details.

**More Examples:**

- `test_verify_correct_password` - See AAA pattern in action
- `test_different_hashes_for_same_password` - Learn about salts
- Full file: [test_auth.py](../../backend/tests/unit/test_auth.py)

</details>

<details open>
<summary><strong>☕ JavaScript: Testing Authentication Components</strong></summary>

**Note:** From here on, we'll use `it()` instead of `test()` for better readability. Remember, they're identical!

**Open `frontend/src/tests/unit/Register.test.jsx` and find the form validation test:**

```javascript
it("allows user to type in form fields", () => {
  /**
   * Test user interaction with form inputs.
   *
   * This test verifies that users can interact with form fields,
   * which is fundamental to any form component. We test:
   * 1. Form fields are accessible and interactive
   * 2. User input is captured correctly
   * 3. Form state updates as user types
   *
   * This demonstrates the AAA pattern in React testing:
   * - Arrange: Render component and get form elements
   * - Act: Simulate user typing in form fields
   * - Assert: Verify the form state reflects user input
   */

  // Arrange - Render the component and get form elements
  renderRegister();
  const emailInput = screen.getByTestId("register-email-input");
  const usernameInput = screen.getByTestId("register-username-input");

  // Act - Simulate user typing in the form fields
  fireEvent.change(emailInput, { target: { value: "test@example.com" } });
  fireEvent.change(usernameInput, { target: { value: "testuser" } });

  // Assert - Verify the form state reflects user input
  expect(emailInput.value).toBe("test@example.com");
  expect(usernameInput.value).toBe("testuser");
});
```

**Guided Walkthrough:**

1. **Arrange**: We render the Register component and get references to form fields
2. **Act**: We simulate user typing using `fireEvent.change` (React Testing Library)
3. **Assert**: We verify the input values are updated correctly

**Key Learning Points:**

- Uses `getByTestId()` for form field selection (appropriate for form testing)
- Uses `fireEvent.change()` for form input simulation
- Tests multiple form fields to show state management

**Try This:**

1. **Run the test from command line:**

   ```bash
   # Run specific test
   npm test -- Register.test.jsx -t "allows user to type"

   # Run all tests in file
   npm test -- Register.test.jsx

   # Run with watch mode (re-runs on file changes)
   npm test -- Register.test.jsx --watch

   # Run with coverage
   npm test -- Register.test.jsx --coverage
   ```

2. **Make it fail intentionally to understand error messages:**

   ```javascript
   // Temporarily change this line in the test:
   expect(emailInput.value).toBe("test@example.com"); // Change to: expect(emailInput.value).toBe('wrong@example.com')
   ```

   Then run the test and see the detailed error message that helps you debug!

3. **Fix it back and run again to see it pass**

**What you'll learn:**

- How to run tests from command line
- How to interpret test failure messages
- How to debug failing tests
- The importance of clear assertion messages

**More Examples:**

- `renders registration form` - Basic component rendering
- `shows loading state during submission` - User experience testing
- Full file: [Register.test.jsx](../../frontend/src/tests/unit/Register.test.jsx)

</details>

### 🔄 Hybrid Approach

**Study both!** Understanding both stacks makes you more valuable.

1. **Start with Python backend tests** (understand authentication functions)
2. **Then JavaScript frontend tests** (see how UI handles authentication)
3. **Notice the connections** (backend hashes passwords, frontend collects them)
4. **Compare approaches**: pytest fixtures vs Vitest mocks, function testing vs component testing

---

<h2 id="part-5-hands-on-practice">Part 5: Hands-On Practice 🏃</h2>

### Step 1: Read and Understand

**Python Track:**

```bash
cd backend
# Linux/Mac
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\activate

# Run all unit tests
pytest -m unit -v

# Run specific test file
pytest tests/unit/test_auth.py -v
```

**JavaScript Track:**

```bash
cd frontend
npm test

# Run specific test file
npm test -- CreatePost.test.jsx

# Run in watch mode (reruns on changes)
npm run test:watch
```

### Step 2: Modify Existing Tests

**Try these experiments:**

1. **Make a test fail intentionally** - Change an assertion and see what happens
2. **Add a new assertion** - Test something the current test doesn't verify
3. **Change test data** - Use different inputs and see if tests still pass

### Step 3: Write Your First Test

**Python Track - Test a simple function:**

```python
def test_multiply():
    # Arrange
    x = 4
    y = 5

    # Act
    result = x * y

    # Assert
    assert result == 20
```

**JavaScript Track - Test a simple function:**

```javascript
it("multiply function works correctly", () => {
  // Arrange
  const x = 4;
  const y = 5;

  // Act
  const result = x * y;

  // Assert
  expect(result).toBe(20);
});
```

---

<h2 id="part-6-additional-patterns">Part 6: Additional Patterns 🚀</h2>

**📝 Note:** The patterns below are **additional enhancements** to your unit testing skills. All the **core concepts** needed to meet the Stage 1 success criteria are covered in Parts 1-5 above.

These patterns enhance your unit testing capabilities:

### Parametrized Tests

Test the same function with multiple inputs:

<details open>
<summary><strong>🐍 Python</strong></summary>

```python
@pytest.mark.parametrize("input,expected", [
    (2, 4),
    (3, 9),
    (4, 16),
    (5, 25),
])
def test_square(input, expected):
    assert square(input) == expected
```

</details>

<details open>
<summary><strong>☕ JavaScript</strong></summary>

```javascript
describe.each([
  [2, 4],
  [3, 9],
  [4, 16],
  [5, 25],
])("square function", (input, expected) => {
  it(`should return ${expected} for input ${input}`, () => {
    expect(square(input)).toBe(expected);
  });
});
```

</details>

### Test Organization

<details open>
<summary><strong>🐍 Python</strong></summary>

```python
class TestPasswordHashing:
    """Group related tests together."""

    def test_password_is_hashed(self):
        # ... test implementation

    def test_verify_correct_password(self):
        # ... test implementation
```

</details>

<details open>
<summary><strong>☕ JavaScript</strong></summary>

```javascript
describe("PasswordHashing", () => {
  // Group related tests together

  it("should hash password correctly", () => {
    // ... test implementation
  });

  it("should verify correct password", () => {
    // ... test implementation
  });
});
```

</details>

### Mocking External Dependencies

<details open>
<summary><strong>🐍 Python</strong></summary>

```python
from unittest.mock import patch

def test_send_email(mock_send_email):
    # Mock the email service
    with patch('email_service.send') as mock_send:
        send_welcome_email("user@example.com")
        mock_send.assert_called_once()
```

</details>

<details open>
<summary><strong>☕ JavaScript</strong></summary>

```javascript
import { vi } from "vitest";

it("should send welcome email", () => {
  // Mock the email service
  const mockSend = vi.fn();
  vi.mock("emailService", () => ({
    send: mockSend,
  }));

  sendWelcomeEmail("user@example.com");

  expect(mockSend).toHaveBeenCalledTimes(1);
});
```

</details>

### Pytest Fixtures in Practice

<details open>
<summary><strong>🐍 Python</strong></summary>

**Real fixtures from `backend/tests/conftest.py`:**

```python
@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """
    Create a fresh database session for each test.

    This fixture is the foundation of database testing in Testbook. It provides:
    - A clean database for each test (no data pollution between tests)
    - Automatic table creation and cleanup
    - Transaction isolation (each test gets its own database state)

    Usage in tests:
        def test_user_creation(db_session):
            user = User(email="test@example.com")
            db_session.add(user)
            db_session.commit()
            assert user.id is not None
    """
    # Setup: Create all tables before test runs
    Base.metadata.create_all(bind=test_engine)
    # Create a new database session for this test
    session = TestingSessionLocal()
    try:
        # Provide the session to the test
        yield session
    finally:
        # Cleanup: Close session and drop all tables after test
        session.close()
        Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def test_user(db_session: Session) -> User:
    """
    Create a test user in the database with known credentials.

    This fixture provides a pre-created user for testing authentication,
    authorization, and user-related functionality. The user is automatically
    saved to the test database and available for all tests that need it.

    Usage in tests:
        def test_user_login(client, test_user):
            response = client.post("/api/auth/login", json={
                "email": "testuser@example.com",
                "password": "TestPassword123!"
            })
            assert response.status_code == 200
    """
    # Create a test user with known credentials
    user = User(
        email="testuser@example.com",
        username="testuser",
        display_name="Test User",
        hashed_password=get_password_hash("TestPassword123!"),  # Hash the password
        bio="Test user bio",
    )
    # Save to test database
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)  # Refresh to get the generated ID
    return user
```

**Using the fixtures in tests:**

```python
# From backend/tests/integration/test_api_auth.py
def test_register_new_user_success(self, client):
    # client fixture provides FastAPI TestClient with test database
    # db_session fixture provides database access (automatically injected)
    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 201
```

</details>

<details open>
<summary><strong>☕ JavaScript</strong></summary>

```javascript
// Mock functions with vi.fn()
import { vi } from "vitest";

it("should call API when form is submitted", () => {
  // Create a mock function
  const mockApiCall = vi.fn().mockResolvedValue({ success: true });

  // Use the mock in your test
  const result = await submitForm(mockApiCall);

  // Verify the mock was called
  expect(mockApiCall).toHaveBeenCalledWith({ email: "test@example.com" });
  expect(result.success).toBe(true);
});

// Testing React component state
it("should update state when user types", () => {
  render(<LoginForm />);

  const emailInput = screen.getByTestId("email-input");

  // Act - User types (this updates component state)
  fireEvent.change(emailInput, { target: { value: "test@example.com" } });

  // Assert - State was updated (input value changed)
  expect(emailInput.value).toBe("test@example.com");
});
```

</details>

### Additional React Testing Patterns

<details open>
<summary><strong>☕ JavaScript</strong></summary>

**Testing Custom Hooks:**

```javascript
import { renderHook, act } from "@testing-library/react";
import { useCounter } from "../hooks/useCounter";

describe("useCounter hook", () => {
  it("should increment counter", () => {
    const { result } = renderHook(() => useCounter(0));

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(1);
  });
});
```

**Testing Async Operations:**

```javascript
it("should handle async data loading", async () => {
  const mockFetch = vi.fn().mockResolvedValue({
    json: () => Promise.resolve({ data: "test" }),
  });
  global.fetch = mockFetch;

  render(<DataComponent />);

  await waitFor(() => {
    expect(screen.getByText("test")).toBeInTheDocument();
  });
});
```

</details>

---

<h2 id="success-criteria">✅ Success Criteria</h2>

You're ready for Stage 2 when you can:

**Core concepts (all tracks):**

- [ ] Explain what a unit test is
- [ ] Identify Arrange-Act-Assert in any test
- [ ] Understand what fixtures/mocks do
- [ ] Run unit tests from the command line
- [ ] Read a test and explain what it verifies
- [ ] Make a test fail intentionally and understand the output

**Python Track:**

- [ ] Use pytest fixtures (db_session, test_user)
- [ ] Write a simple pytest unit test from scratch
- [ ] Understand bcrypt password hashing

**JavaScript Track:**

- [ ] Use Vitest and React Testing Library
- [ ] Mock functions with `vi.fn()`
- [ ] Test React component rendering and state
- [ ] Use `it()` for readable test descriptions (we'll use this going forward)

**Hybrid Track:**

- [ ] Can explain how backend unit tests differ from frontend component tests
- [ ] Understand when to use each approach

---

<h2 id="why-this-matters">🧠 Why This Matters</h2>

### In Real QA Teams

- **Unit tests run in seconds** - Developers run them constantly
- **Catch bugs early** - Before code reaches QA or production
- **Document behavior** - Tests show how code should work
- **Enable refactoring** - Change code safely when tests pass

### For Your Career

- **Foundational skill** - All test automation builds on unit testing
- **Interview topic** - You'll be asked to write unit tests
- **Code confidence** - Understanding tests means understanding code
- **Team collaboration** - Speak the same language as developers

---

<h2 id="related-resources">🔗 Related Resources</h2>

### Hands-On Practice

**🐍 Python Track:**

- [Lab 1: Your First Test (Python)](exercises/LAB_01_Your_First_Test_Python.md)
- [Lab 2: Testing Real Functions (Python)](exercises/LAB_02_Testing_Real_Functions_Python.md)
- [Lab 3: Fixtures and Test Data (Python)](exercises/LAB_03_Fixtures_And_Test_Data_Python.md)
- [Lab 4: Debugging and Error Handling (Python)](exercises/LAB_04_Debugging_And_Error_Handling_Python.md)

**🟨 JavaScript Track:**

- [Lab 1: Your First Test (JavaScript)](exercises/LAB_01_Your_First_Test_JavaScript.md)
- [Lab 2: Testing Real Functions (JavaScript)](exercises/LAB_02_Testing_Real_Functions_JavaScript.md)
- [Lab 3: Fixtures and Test Data (JavaScript)](exercises/LAB_03_Fixtures_And_Test_Data_JavaScript.md)
- [Lab 4: Debugging and Error Handling (JavaScript)](exercises/LAB_04_Debugging_And_Error_Handling_JavaScript.md)

### Documentation

- [Pytest Documentation](https://docs.pytest.org/)
- [Testing Best Practices](../../docs/guides/TESTING_GUIDE.md)
- [Quick Reference](../../docs/reference/QUICK_REFERENCE_PYTEST.md)

### Code Examples

- [Good Test Examples](../../backend/tests/examples/good_tests.py)
- [Bad Test Examples](../../backend/tests/examples/bad_tests.py)

---

<h2 id="self-check-quiz-optional">🧠 Self-Check Quiz (Optional)</h2>

Before moving to Stage 2, can you answer these questions?

1. **What is the difference between unit tests and integration tests?**

   - A) Unit tests are faster
   - B) Unit tests test individual functions in isolation
   - C) Integration tests are more important
   - D) There's no difference

2. **What does AAA stand for in test structure?**

   - A) Always Assert Actions
   - B) Arrange, Act, Assert
   - C) All About Assertions
   - D) Arrange, Act, Analyze

3. **When would you use a pytest fixture?**

   - A) When you need to test multiple functions
   - B) When you need to share setup code between tests
   - C) When you want to skip a test
   - D) When you need to test async functions

4. **What makes a good test name?**

   - A) Short and simple
   - B) Describes what the test does
   - C) Uses numbers (test_1, test_2)
   - D) Matches the function name

5. **Why do we test edge cases?**
   - A) They're easier to write
   - B) They catch bugs that happy path tests miss
   - C) They run faster
   - D) They're more fun

**Answers:** [Check your answers here](../solutions/stage_1_quiz_answers.md)

---

<h2 id="reflection">🤔 Reflection</h2>

Before moving to Stage 2, answer these questions:

1. **What surprised you most about unit tests?**

2. **Why do we use fixtures instead of just creating test data in each test?**

3. **Pick one test from `tests/unit/test_auth.py`. What would happen if you removed the assertion?**

4. **How are unit tests different from just manually testing a function in the Python REPL?**

5. **What's one thing you're still confused about?**

**Document your answers** in [reflection.md](reflection.md) or your own notes.

---

<h2 id="stage-complete">🎉 Stage Complete</h2>

Once you've met the success criteria and reflected on the questions:

### 👉 [Continue to Stage 2: Integration Tests](../stage_2_integration/README.md)

---

_Pro tip: Come back to this stage after completing later stages. You'll notice things you missed the first time! 🎯_
