# 🧱 Stage 2: Integration Tests

**Testing Components Working Together**

> **💡 Language Selection**: This guide includes both Python and JavaScript examples. Both are expanded by default so you can see all approaches. Click the language tabs to collapse sections you don't need.

## Your Progress

[████████░░░░░░░░░░░░] 40% complete

✅ Stage 1: Unit Tests (completed)<br>
→ **Stage 2: Integration Tests** (you are here)<br>
⬜ Stage 3: E2E Testing<br>
⬜ Stage 4: Performance & Security<br>
⬜ Stage 5: Capstone<br>

**Estimated time remaining:** 5-7 hours (core content) + 3-5 hours (optional exercises)

<h2 id="table-of-contents">📋 Table of Contents</h2>

- [Why Integration Testing Matters: The Glue That Holds Systems Together](#why-integration-testing-matters-the-glue-that-holds-systems-together)
- [Part 1: What Are Integration Tests? 📚](#part-1-what-are-integration-tests)
- [Part 2: HTTP API Testing 🌐](#part-2-http-api-testing)
- [Part 3: Database Integration 🗄️](#part-3-database-integration)
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

## Why Integration Testing Matters: The Glue That Holds Systems Together

### The Real-World Impact

**The Problem Without Integration Tests:**
In 2018, a major e-commerce platform experienced a 2-hour outage during Black Friday, losing $100M in sales. The issue? Their unit tests all passed, but they missed that a database connection pool wasn't being properly initialized when the API server started. The integration between the API and database was broken, but no integration test caught it.

**What Integration Tests Prevent:**

1. **API Contract Violations**: Services that can't communicate properly
2. **Database Inconsistencies**: Data that gets corrupted between systems
3. **Configuration Mismatches**: Settings that work in isolation but fail together
4. **Performance Bottlenecks**: Systems that work alone but slow down together
5. **Security Vulnerabilities**: Authentication that works in tests but fails in production

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
       /  Integration    \  ← API / Component tests ← STAGE 2: CONNECTING COMPONENTS
      /___________________\
     /                     \
    /      Unit Tests       \  ← Vitest (JS) | pytest (Python)
   /_________________________\
```

**Integration Tests (15% of your test suite):**

- Medium speed: Run in seconds to minutes
- More reliable than E2E tests
- Test real interactions between components
- Catch bugs that unit tests miss

**Why 15%?**

- Unit tests catch most bugs (80%)
- Integration tests catch the bugs unit tests miss (15%)
- E2E tests catch the remaining bugs (5%)
- Balance between coverage and speed

### The Business Case

**Real Example:**
A banking application has:

- User service (handles authentication)
- Account service (manages accounts)
- Transaction service (processes payments)

Without integration tests:

- User service works alone ✅
- Account service works alone ✅
- Transaction service works alone ✅
- But when a user tries to transfer money... 💥
- The services can't communicate properly
- Money disappears or gets duplicated
- Customer loses trust, bank loses money

With integration tests:

- Test the complete transfer flow
- Verify all services work together
- Catch integration bugs before production
- Maintain customer trust

### The Developer Experience

**Without Integration Tests:**

- "It works on my machine"
- "The unit tests pass, so it should work"
- "I don't know why it's failing in production"
- "Let me check the logs... there are 10,000 lines"

**With Integration Tests:**

- "I know the components work together"
- "I can see exactly where the integration fails"
- "I can test real scenarios"
- "I have confidence in the system"

### The Quality Mindset

**Integration Testing Teaches You:**

1. **Think About System Boundaries**: How do components interact?
2. **Design for Integration**: Make components easy to integrate
3. **Test Real Scenarios**: Test what users actually do
4. **Handle Failures Gracefully**: What happens when a component fails?
5. **Monitor System Health**: How do you know if integration is working?

### Industry Standards

**Companies That Require Integration Tests:**

- Netflix: Integration tests for all microservices
- Uber: Integration tests for all API endpoints
- Airbnb: Integration tests for all service interactions
- Spotify: Integration tests for all data flows

**Why They Do This:**

- Prevents integration failures
- Enables faster deployment
- Reduces production bugs
- Improves system reliability
- Builds team confidence

### The Integration Testing Mindset

**Key Questions to Ask:**

1. **What can go wrong?** Network failures, timeouts, data corruption
2. **How do components communicate?** APIs, databases, message queues
3. **What are the dependencies?** External services, databases, file systems
4. **How do we handle failures?** Retries, fallbacks, error handling
5. **How do we monitor health?** Logs, metrics, alerts

**Common Integration Patterns:**

- **API Integration**: Test HTTP endpoints with real data
- **Database Integration**: Test database operations with real data
- **Message Queue Integration**: Test async communication
- **File System Integration**: Test file operations
- **External Service Integration**: Test third-party APIs

---

<h2 id="part-1-what-are-integration-tests">Part 1: What Are Integration Tests? 📚</h2>

### The Restaurant Kitchen Analogy

Imagine you're testing a restaurant kitchen. Unit tests would be like testing each chef individually - "Can Chef Sarah chop vegetables?" But integration tests would be like testing the entire kitchen workflow - "Can Chef Sarah chop vegetables AND pass them to Chef Mike who cooks them AND the food gets to the customer hot and on time?"

**Integration tests** verify that multiple parts of your system work correctly together.

### Why Integration Tests Matter

1. **Real interactions**: Tests how components actually work together
2. **Catch integration bugs**: Issues that only appear when parts connect
3. **Verify business workflows**: Complete user journeys, not just individual functions
4. **Test with real data**: Database, APIs, external services

### Unit vs Integration: The Key Difference

<details open>
<summary><strong>🐍 Python</strong></summary>

```python
# Unit Test - Tests ONE function in isolation
def test_validate_password():
    result = validate_password("password123")
    assert result == True

    result = validate_password("weak")
    assert result == False

# Integration Test - Tests MULTIPLE components working together
def test_user_login_workflow():
    # 1. User submits credentials (API call)
    # 2. Password gets validated (validation function)
    # 3. User record is looked up (database query)
    # 4. JWT token is generated (auth service)
    # 5. Token is returned to client (API response)
```

</details>

<details open>
<summary><strong>☕ JavaScript</strong></summary>

```javascript
// Unit Test - Tests ONE function in isolation
test("validate password", () => {
  const result = validatePassword("password123");
  expect(result).toBe(true);

  const weakResult = validatePassword("weak");
  expect(weakResult).toBe(false);
});

// Integration Test - Tests MULTIPLE components working together
test("user login workflow", async () => {
  // 1. User submits credentials (API call)
  // 2. Password gets validated (validation function)
  // 3. User record is looked up (database query)
  // 4. JWT token is generated (auth service)
  // 5. Token is returned to client (API response)
});
```

</details>

### Integration Test Characteristics

**Compared to Unit Tests:**

| Aspect           | Unit Tests              | Integration Tests       |
| ---------------- | ----------------------- | ----------------------- |
| **Speed**        | Milliseconds            | Seconds                 |
| **Scope**        | Single function         | Multiple components     |
| **Dependencies** | Mocked                  | Real (database, APIs)   |
| **Purpose**      | Verify logic            | Verify interactions     |
| **Failures**     | Pinpoint exact function | Show integration issues |

---

<h2 id="part-2-http-api-testing">Part 2: HTTP API Testing 🌐</h2>

### The Restaurant Order Analogy

Think of API testing like testing a restaurant's order system:

**Arrange** = Customer places order (prepare request data)<br>
**Act** = Kitchen processes order (send HTTP request)<br>
**Assert** = Food arrives correctly (verify response)

### HTTP Testing Pattern

<details open>
<summary><strong>🐍 Python</strong></summary>

```python
def test_create_post_api():
    # Arrange - Prepare request data
    payload = {"content": "Hello world!", "user_id": 123}
    headers = {"Authorization": "Bearer token123"}

    # Act - Make HTTP request
    response = client.post("/api/posts", json=payload, headers=headers)

    # Assert - Verify response
    assert response.status_code == 201  # Created
    assert response.json()["content"] == "Hello world!"
    assert "id" in response.json()  # Post was assigned an ID
```

</details>

<details open>
<summary><strong>☕ JavaScript</strong></summary>

```javascript
test("create post API", async () => {
  // Arrange - Prepare request data
  const payload = { content: "Hello world!", user_id: 123 };
  const headers = { Authorization: "Bearer token123" };

  // Act - Make HTTP request
  const response = await fetch("/api/posts", {
    method: "POST",
    headers: { "Content-Type": "application/json", ...headers },
    body: JSON.stringify(payload),
  });

  // Assert - Verify response
  expect(response.status).toBe(201); // Created
  const data = await response.json();
  expect(data.content).toBe("Hello world!");
  expect(data.id).toBeDefined(); // Post was assigned an ID
});
```

</details>

### HTTP Status Codes You Need to Know

- `200 OK` - Success (GET, PATCH)
- `201 Created` - Success (POST)
- `204 No Content` - Success (DELETE)
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Not authenticated
- `403 Forbidden` - Authenticated but not authorized
- `404 Not Found` - Resource doesn't exist
- `500 Internal Server Error` - Server bug

### Testing Different Scenarios

```python
def test_api_endpoint_scenarios():
    # Happy path
    response = client.post("/api/posts", json=valid_data)
    assert response.status_code == 201

    # Missing authentication
    response = client.post("/api/posts", json=valid_data)  # No headers
    assert response.status_code == 401

    # Invalid data
    response = client.post("/api/posts", json={"invalid": "data"})
    assert response.status_code == 400

    # Wrong user tries to delete someone else's post
    response = client.delete("/api/posts/123", headers=wrong_user_headers)
    assert response.status_code == 403
```

---

<h2 id="part-3-database-integration">Part 3: Database Integration 🗄️</h2>

### The Library System Analogy

Think of database integration like testing a library system:

1. **Check out a book** (create record)
2. **Search for books** (query database)
3. **Return a book** (update record)
4. **Remove old books** (delete records)

### Database Testing Pattern

<details open>
<summary><strong>🐍 Python</strong></summary>

```python
def test_database_operations():
    # Arrange - Set up test data
    user = User(username="testuser", email="test@example.com")
    db_session.add(user)
    db_session.commit()

    # Act - Perform database operations
    post = Post(content="Test post", user_id=user.id)
    db_session.add(post)
    db_session.commit()

    # Assert - Verify data was saved
    found_post = db_session.query(Post).filter_by(id=post.id).first()
    assert found_post is not None
    assert found_post.content == "Test post"
    assert found_post.user_id == user.id
```

</details>

<details open>
<summary><strong>☕ JavaScript</strong></summary>

```javascript
test("database operations", async () => {
  // Arrange - Set up test data
  const user = await createTestUser({
    username: "testuser",
    email: "test@example.com",
  });

  // Act - Perform database operations
  const post = await createTestPost({
    content: "Test post",
    userId: user.id,
  });

  // Assert - Verify data was saved
  const foundPost = await Post.findById(post.id);
  expect(foundPost).toBeTruthy();
  expect(foundPost.content).toBe("Test post");
  expect(foundPost.userId).toBe(user.id);
});
```

</details>

### Why Test the Database?

1. **Data persistence**: Verify data actually gets saved
2. **Relationships**: Test foreign keys and associations
3. **Constraints**: Ensure database rules are enforced
4. **Transactions**: Test rollbacks and commits

### Test Data Management

<details open>
<summary><strong>🐍 Python</strong></summary>

```python
# Without factories (repetitive)
def test_user_posts():
    user = User(username="testuser", email="test@example.com")
    db_session.add(user)
    db_session.commit()
    # ... test logic

# With factories (clean)
def test_user_posts(user_factory):
    user = user_factory.create()
    # ... test logic
```

</details>

<details open>
<summary><strong>☕ JavaScript</strong></summary>

```javascript
// Without factories (repetitive)
test("user posts", async () => {
  const user = await User.create({
    username: "testuser",
    email: "test@example.com",
  });
  // ... test logic
});

// With factories (clean)
test("user posts", async () => {
  const user = await createTestUser();
  // ... test logic
});
```

</details>

---

<h2 id="part-4-implementation-guide">Part 4: Implementation Guide 🛠️</h2>

Now let's see these concepts in real code! Choose your track:

<details open>
<summary><strong>🐍 Python Track: Testing API Endpoints</strong></summary>

**Open `backend/tests/integration/test_api_auth.py` and find `test_register_new_user_success`:**

```python
def test_register_new_user_success(self, client):
    """
    Test successful user registration.

    This test verifies the complete user registration workflow:
    1. User submits registration data
    2. System validates the data
    3. Password is hashed and stored securely
    4. User record is created in database
    5. JWT token is generated for auto-login
    6. User data is returned (without sensitive information)

    This is a critical integration test that ensures the entire
    registration flow works end-to-end.
    """
    # Arrange - Prepare new user data
    new_user = {
        "email": "newuser@example.com",
        "username": "newuser",
        "display_name": "New User",
        "password": "SecurePass123!",
        "bio": "This is my bio",
    }

    # Act - Send POST request to registration endpoint
    response = client.post("/api/auth/register", json=new_user)

    # Assert - Verify successful registration and auto-login
    assert response.status_code == 201  # API returns 201 Created
    data = response.json()
    assert "access_token" in data  # Returns token for auto-login
    assert data["token_type"] == "bearer"  # JWT bearer token format
    assert data["email"] == "newuser@example.com"  # Returns user data
    assert data["username"] == "newuser"
    assert data["display_name"] == "New User"
    assert "hashed_password" not in data  # Security: password never exposed
```

**Guided Walkthrough:**

1. **Arrange**: We prepare user registration data
2. **Act**: We send a POST request to the registration endpoint
3. **Assert**: We verify:
   - HTTP status code is 201 (Created)
   - Response contains expected data
   - User was actually saved to the database

**Try This:**

1. **Run the test from command line:**

   ```bash
   # Run specific test
   pytest backend/tests/integration/test_api_auth.py::TestRegisterEndpoint::test_register_new_user_success -v

   # Run all integration tests
   pytest backend/tests/integration/ -v

   # Run with detailed output for debugging
   pytest backend/tests/integration/test_api_auth.py -v -s
   ```

2. **Make it fail intentionally to understand error messages:**

   ```python
   # Temporarily change this line in the test:
   assert response.status_code == 201  # Change to: assert response.status_code == 200
   ```

   Then run the test and see the detailed error message that helps you debug!

3. **Debug integration test failures:**

   ```bash
   # Run with detailed logging
   pytest backend/tests/integration/test_api_auth.py -v -s --log-cli-level=DEBUG

   # Run with database state inspection
   pytest backend/tests/integration/test_api_auth.py -v --capture=no
   ```

4. **Fix it back and run again to see it pass**

**What you'll learn:**

- How to run integration tests from command line
- How to interpret HTTP status code errors
- How to debug API integration issues
- The importance of understanding HTTP response codes

**More Examples:**

- `test_login_success` - See authentication flow
- `test_create_post_unauthorized` - Learn about authorization
- Full file: [test_api_auth.py](../../backend/tests/integration/test_api_auth.py)

</details>

<details open>
<summary><strong>☕ JavaScript Track: Testing API Contracts</strong></summary>

**Open `frontend/src/tests/unit/Register.test.jsx` and find the registration integration test:**

```javascript
it("handles registration API errors gracefully", async () => {
  /**
   * This test demonstrates integration testing by verifying that the Register component
   * properly handles API errors and displays appropriate user feedback.
   *
   * Key Integration Testing Concepts:
   * - Mocking external dependencies (API calls)
   * - Testing component behavior with real error structures
   * - Verifying user experience during error states
   * - Testing async error handling patterns
   */

  // Arrange - Mock register function to return error with proper structure
  // Note: The error structure matches what real APIs return (response.data.detail)
  const mockRegister = vi.fn().mockRejectedValue({
    response: {
      data: {
        detail: "Email already exists", // Specific error message from API
      },
    },
  });

  // Create mock auth context with our failing register function
  const mockAuth = {
    user: null,
    login: vi.fn(),
    logout: vi.fn(),
    register: mockRegister, // This will fail when called
  };

  // Render component with mocked dependencies
  renderRegister(mockAuth);

  // Get all form elements - we need ALL required fields for form submission
  const emailInput = screen.getByTestId("register-email-input");
  const usernameInput = screen.getByTestId("register-username-input");
  const displayNameInput = screen.getByTestId("register-displayname-input");
  const passwordInput = screen.getByTestId("register-password-input");
  const submitButton = screen.getByTestId("register-submit-button");

  // Act - Simulate complete user registration flow that will fail
  // Fill all required form fields (form validation requires all fields)
  fireEvent.change(emailInput, { target: { value: "test@example.com" } });
  fireEvent.change(usernameInput, { target: { value: "testuser" } });
  fireEvent.change(displayNameInput, { target: { value: "Test User" } });
  fireEvent.change(passwordInput, { target: { value: "password123" } });

  // Submit form - this will trigger our mocked API call that fails
  fireEvent.click(submitButton);

  // Assert - Verify error handling works correctly
  // Wait for async error handling to complete
  await waitFor(() => {
    expect(screen.getByTestId("register-error")).toHaveTextContent(
      "Email already exists"
    );
  });

  // Additional assertions we could add:
  // - Verify submit button is re-enabled after error
  // - Verify form fields are still accessible for retry
  // - Verify specific error styling is applied
});
```

**Guided Walkthrough:**

1. **Arrange**:

   - Mock the registration API to return a realistic error structure (`response.data.detail`)
   - Create a mock auth context that uses our failing register function
   - Render the Register component with all necessary providers (BrowserRouter, AuthContext)

2. **Act**:

   - Simulate complete user registration flow by filling ALL required form fields
   - Submit the form, which triggers our mocked API call that will fail
   - This tests the integration between form submission and API error handling

3. **Assert**:
   - Verify the component displays the specific error message from the API
   - Use `waitFor()` to handle the async nature of error handling
   - Test that the user experience remains functional during error states

**Why This Test Matters:**

- **Real-world scenario**: Users will encounter API errors during registration
- **Integration testing**: Tests how the component handles external API failures
- **User experience**: Ensures users get clear feedback when things go wrong
- **Error handling**: Verifies the app doesn't crash on API errors

**Try This:**

1. Run this test: `npm test -- Register.test.jsx`
2. Make it fail by changing the expected error message text
3. Understand the error message
4. Fix it back

**More Examples:**

- `renders registration form` - Basic component rendering
- `calls register API with correct data on form submission` - API integration testing
- `shows loading state during submission` - User experience testing
- `navigates to home page after successful registration` - Navigation flow testing
- Full file: [Register.test.jsx](../../frontend/src/tests/unit/Register.test.jsx)

</details>

<details open>
<summary><strong>🔄 Hybrid Track</strong></summary>

**Test the full stack!** This is what most QA roles require.

1. **Backend APIs (Python)** - How endpoints work
2. **Frontend integration (JavaScript)** - How UI consumes those APIs
3. **Contract tests (JavaScript)** - Verify they agree on structure
4. **See the connection**: Make a breaking change to backend API response and watch frontend contract tests fail!

</details>

---

<h2 id="part-5-hands-on-practice">Part 5: Hands-On Practice 🏃</h2>

### Step 1: Run Integration Tests

**Python Track:**

```bash
cd backend
# Linux/Mac
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\activate

# Run all integration tests
pytest -m integration -v

# Run specific test file
pytest tests/integration/test_api_auth.py -v
```

**JavaScript Track:**

```bash
cd frontend

# Run contract tests
npm test -- tests/integration/contract.test.js

# Run component tests with MSW
npm test -- tests/unit/CreatePost.test.jsx
```

### Step 2: Trace Complete Workflows

**Pick a complete user journey and trace it:**

1. **User Registration Flow:**

   - HTTP POST to `/api/auth/register`
   - Data validation
   - Password hashing
   - Database insertion
   - Response generation

2. **Post Creation Flow:**
   - User authentication
   - POST to `/api/posts`
   - Database insertion
   - Feed update
   - Response to frontend

### Step 3: Experiment with Tests

**Try these experiments:**

1. **Make a test fail intentionally** - Change an assertion and see what happens
2. **Test error scenarios** - Send invalid data and verify proper error responses
3. **Test authorization** - Try to access resources you shouldn't have access to

### Step 4: Write Your First Integration Test

**Python Track - Test a simple API endpoint:**

```python
def test_get_user_profile(client, test_user):
    # Arrange
    user_id = test_user.id

    # Act
    response = client.get(f"/api/users/{user_id}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == test_user.username
    assert data["email"] == test_user.email
```

**JavaScript Track - Test API contract:**

```javascript
test("GET /api/users/:id contract validation", async () => {
  // Arrange
  const userId = 1;

  // Act
  const response = await fetch(`/api/users/${userId}`);

  // Assert
  expect(response.status).toBe(200);
  const data = await response.json();
  expect(data).toHaveProperty("id");
  expect(data).toHaveProperty("username");
  expect(data).toHaveProperty("email");
});
```

---

<h2 id="part-6-additional-patterns">Part 6: Additional Patterns 🚀</h2>

**📝 Note:** The patterns below are **additional enhancements** to your integration testing skills. All the **core concepts** needed to meet the Stage 2 success criteria are covered in Parts 1-5 above.

These patterns enhance your testing capabilities:

### Test Factories

Create realistic test data easily:

<details open>
<summary><strong>🐍 Python</strong></summary>

**Real factories from `backend/tests/factories.py`:**

```python
class UserFactory:
    """
    Factory for creating User instances with sensible defaults.

    This factory follows the Factory Pattern to create test users easily.
    It provides sensible defaults while allowing customization when needed.

    Key Features:
    - Auto-generates unique emails and usernames
    - Handles password hashing automatically
    - Saves to database and returns committed instance
    - Supports batch creation for multiple users
    """

    @classmethod
    def create(cls, db_session, email=None, username=None, **kwargs):
        """
        Create a user with sensible defaults.

        This method creates a User instance with auto-generated values for
        required fields, handles password hashing, and saves to the database.
        Each call generates unique values to avoid conflicts.
        """
        if email is None:
            email = f"user{cls._counter}@test.com"
        if username is None:
            username = f"user{cls._counter}"

        user = User(
            email=email,
            username=username,
            display_name=display_name,
            hashed_password=get_password_hash(password),  # Auto-hash password
            **kwargs,
        )
        db_session.add(user)
        db_session.commit()
        return user

# Usage examples from factories.py:
# Simple user creation
user = UserFactory.create(db_session)

# Custom user with specific data
user = UserFactory.create(
    db_session,
    email="custom@test.com",
    username="customuser",
    display_name="Custom User"
)

# Batch creation for multiple users
users = UserFactory.create_batch(db_session, 10)
```

</details>

<details open>
<summary><strong>☕ JavaScript</strong></summary>

```javascript
// Without factory (repetitive)
test("user posts", async () => {
  const user = await User.create({
    username: "testuser",
    email: "test@example.com",
    display_name: "Test User",
  });
  // ... test logic
});

// With factory (clean)
test("user posts", async () => {
  const user = await createTestUser();
  // ... test logic
});
```

</details>

### MSW (Mock Service Worker) for API Mocking

<details open>
<summary><strong>☕ JavaScript</strong></summary>

**Real MSW handlers from `frontend/src/tests/mocks/handlers.js`:**

```javascript
/**
 * MSW (Mock Service Worker) handlers for component testing
 *
 * These handlers provide realistic API mocking for testing React components
 * without needing a running backend. All responses match the actual FastAPI
 * backend schema, ensuring tests accurately reflect real API behavior.
 *
 * Key Features:
 * - Network-level mocking (intercepts actual fetch/axios calls)
 * - Realistic response data matching backend schema
 * - Support for different HTTP methods and status codes
 * - Easy to override for specific test scenarios
 */

import { http, HttpResponse } from "msw";

const API_BASE = "http://localhost:8000/api";

export const handlers = [
  /**
   * GET /api/feed - Returns user's feed posts
   *
   * This handler mocks the feed endpoint that returns posts from users
   * the current user follows. Used for testing PostList, Feed, and
   * other components that display user feeds.
   */
  http.get(`${API_BASE}/feed`, () => {
    return HttpResponse.json([
      {
        id: 1,
        content: "Mocked post from MSW",
        author: {
          id: 1,
          username: "testuser",
          display_name: "Test User",
        },
        created_at: new Date().toISOString(),
        reaction_counts: { "👍": 5, "❤️": 2 },
        is_own_post: false,
      },
    ]);
  }),

  /**
   * POST /api/posts/ - Create a new post
   *
   * This handler mocks post creation, simulating the backend's response
   * when a user creates a new post. Used for testing CreatePost component
   * and post creation workflows.
   *
   * Request body: { content: string, image_url?: string, video_url?: string }
   * Response: Post object with generated ID and author info
   */
  http.post(`${API_BASE}/posts/`, async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json({
      id: Date.now(), // Simulate auto-generated ID
      content: body.content,
      author: {
        id: 1,
        username: "testuser",
        display_name: "Test User",
      },
      created_at: new Date().toISOString(),
      reaction_counts: {},
      is_own_post: true,
    });
  }),
];
```

**Using MSW in tests:**

```javascript
// From frontend/src/tests/unit/examples/README.md
import { setupServer } from "msw/node";
import { handlers } from "../../../test/mocks/handlers";

const server = setupServer(...handlers);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

test("component fetches data", async () => {
  render(<MyComponent />);

  await waitFor(() => {
    expect(screen.getByText("Mocked post from MSW")).toBeInTheDocument();
  });
});
```

</details>

### API Contract Validation

<details open>
<summary><strong>☕ JavaScript</strong></summary>

```javascript
// Contract validation with OpenAPI schema
import { validateContract } from "../contract-helpers.js";

test("API response matches OpenAPI schema", async () => {
  const response = await fetch("/api/posts");
  const data = await response.json();

  // Validate response structure matches schema
  expect(() => {
    validateContract(data, "/api/posts", "get", 200);
  }).not.toThrow();

  // Verify required fields exist
  expect(data).toHaveProperty("id");
  expect(data).toHaveProperty("content");
  expect(data).toHaveProperty("created_at");
});

// Testing components that fetch data
test("PostList component fetches and displays data", async () => {
  // MSW mocks the API call
  render(<PostList />);

  // Wait for data to load
  await waitFor(() => {
    expect(screen.getByText("Loading...")).toBeInTheDocument();
  });

  await waitFor(() => {
    expect(screen.getByText("Test post")).toBeInTheDocument();
  });
});
```

</details>

### Test Organization

Group related tests together:

<details open>
<summary><strong>🐍 Python</strong></summary>

```python
class TestPostAPI:
    """Tests for post-related API endpoints."""

    def test_create_post_success(self):
        # ... test implementation

    def test_create_post_unauthorized(self):
        # ... test implementation

    def test_create_post_invalid_data(self):
        # ... test implementation
```

</details>

<details open>
<summary><strong>☕ JavaScript</strong></summary>

```javascript
describe("Post API", () => {
  // Tests for post-related API endpoints

  test("create post success", () => {
    // ... test implementation
  });

  test("create post unauthorized", () => {
    // ... test implementation
  });

  test("create post invalid data", () => {
    // ... test implementation
  });
});
```

</details>

### API Contract Testing

**Additional Pattern:** Property-based contract testing with Schemathesis

Instead of writing individual test cases, Schemathesis reads your OpenAPI schema and automatically generates 500+ test cases to validate:

- All endpoints match documentation
- Required fields are enforced
- Data types are correct
- Edge cases are handled
- Security vulnerabilities are found (fuzzing)

**Current Status:** ⚠️ **Skipped** (OpenAPI 3.1.0 compatibility)

FastAPI 0.115+ uses OpenAPI 3.1.0, but Schemathesis only has experimental support. The test is skipped until full support is available.

**Should I learn this?**

- 📚 **Yes!** Read [Contract Testing Guide](../../docs/guides/CONTRACT_TESTING.md) to understand the concept
- 🎯 **For now:** Focus on the 180 integration tests that ARE running
- 🔄 **Alternative:** Frontend contract testing works today! See [Lab 6C](../../learn/stage_3_api_e2e/exercises/LAB_06C_Frontend_Integration_Testing_Python.md)
- 💼 **Career value:** Understanding contract testing is a professional differentiator

---

<h2 id="success-criteria">✅ Success Criteria</h2>

You're ready for Stage 3 when you can:

**Core concepts (all tracks):**

- [ ] Explain the difference between unit and integration tests
- [ ] Test both successful and error responses
- [ ] Verify authorization and authentication
- [ ] Understand HTTP status codes (200, 201, 401, 403, 404)
- [ ] Debug failing integration tests

**Python Track:**

- [ ] Use FastAPI TestClient to make HTTP requests
- [ ] Test API endpoints with database integration
- [ ] Use test factories to create data
- [ ] Write an integration test for an API endpoint

**JavaScript Track:**

- [ ] Use MSW to mock backend APIs
- [ ] Validate API contracts with OpenAPI schema
- [ ] Test components that fetch data
- [ ] Understand the difference between component tests and contract tests

**Hybrid Track:**

- [ ] Can explain how backend API tests and frontend contract tests work together
- [ ] Understand why contract tests prevent integration bugs

---

<h2 id="why-this-matters">🧠 Why This Matters</h2>

### In Real QA Teams

- **Integration tests catch contract bugs** - When APIs change unexpectedly
- **Verify business logic** - Not just individual functions, but complete workflows
- **Test security** - Authorization, authentication, input validation
- **Prevent regressions** - Ensure features keep working after changes

### For Your Career

- **Most common QA task** - Testing APIs is core QA work
- **Cross-functional skill** - Bridge between backend, frontend, QA
- **Interview essential** - You'll be asked to design integration tests
- **Real-world scenarios** - Integration tests mirror actual user actions

---

<h2 id="related-resources">🔗 Related Resources</h2>

### Hands-On Practice

**🐍 Python Track:**

- [Lab 5: API Endpoint Testing (Python)](exercises/LAB_05_API_Endpoint_Testing_Python.md)
- [Lab 6: Advanced API Testing (Python)](exercises/LAB_06_Advanced_API_Testing_Python.md)
- [Lab 7: Test Data Management (Python)](exercises/LAB_07_Test_Data_Management_Python.md)
- [Lab 8: Contract Testing Foundations (Python)](exercises/LAB_08_Contract_Testing_Foundations_Python.md)

**🟨 JavaScript Track:**

- [Lab 5: API Endpoint Testing (JavaScript)](exercises/LAB_05_API_Endpoint_Testing_JavaScript.md)
- [Lab 6: Component Testing (JavaScript)](exercises/LAB_06_Component_Testing_JavaScript.md)
- [Lab 7: Test Data Management (JavaScript)](exercises/LAB_07_Test_Data_Management_JavaScript.md)
- [Lab 8: Contract Testing Foundations (JavaScript)](exercises/LAB_08_Contract_Testing_Foundations_JavaScript.md)

### Documentation

- [API Testing Guide](../../docs/guides/TESTING_GUIDE.md)
- [FastAPI Testing Docs](https://fastapi.tiangolo.com/tutorial/testing/)
- [HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)

### Reference

- [Test Database Setup](../../backend/tests/README.md)
- [Test Factories Documentation](exercises/LAB_07_Test_Data_Management_Python.md)

---

<h2 id="self-check-quiz-optional">🧠 Self-Check Quiz (Optional)</h2>

Before moving to Stage 3, can you answer these questions?

1. **What's the main difference between unit tests and integration tests?**

   - A) Integration tests are slower
   - B) Integration tests test multiple components together
   - C) Unit tests use mocks, integration tests don't
   - D) Integration tests are more important

2. **What does FastAPI TestClient do?**

   - A) Runs tests faster
   - B) Provides a test interface for FastAPI apps
   - C) Creates test data automatically
   - D) Validates API responses

3. **Why do integration tests need database setup?**

   - A) To make tests run faster
   - B) To test real database operations
   - C) To avoid using mocks
   - D) To test multiple functions at once

4. **What's the purpose of test factories?**

   - A) To create test data easily
   - B) To run tests in parallel
   - C) To mock external services
   - D) To generate random test cases

5. **When testing API endpoints, what should you verify?**
   - A) Only the response status code
   - B) Only the response data
   - C) Status code, response data, and headers
   - D) Only that the endpoint doesn't crash

**Answers:** [Check your answers here](../solutions/stage_2_quiz_answers.md)

---

<h2 id="reflection">🤔 Reflection</h2>

Before moving to Stage 3, answer these:

1. **Why do integration tests need a database while unit tests don't?**

2. **Pick one test from `tests/integration/test_api_posts.py`. What would break if you removed authentication?**

3. **How do test factories make integration testing easier?**

4. **What's the difference between a 401 and a 403 status code? Find an example of each in the tests.**

5. **What's one integration test you would add to improve test coverage?**

**Document your answers** in [reflection.md](reflection.md).

---

<h2 id="stage-complete">🎉 Stage Complete</h2>

You now understand how to test multi-component systems!

### 👉 [Continue to Stage 3: API & E2E Testing](../stage_3_api_e2e/README.md)

---

_Pro tip: Integration tests are where most QA engineers spend their time. Master this, and you're job-ready! 💼_
