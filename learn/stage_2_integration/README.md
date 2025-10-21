# 🧱 Stage 2: Integration Tests

**Testing Components Working Together**

Integration tests verify that multiple parts of your system work correctly together. Unlike unit tests that isolate functions, integration tests check real API endpoints, database operations, and multi-component workflows.

## Your Progress

[████████████████░░░░] 40% complete
✅ Stage 1: Unit Tests (completed)
→ **Stage 2: Integration Tests** (you are here)
⬜ Stage 3: API & E2E Testing
⬜ Stage 4: Performance & Security
⬜ Stage 5: Capstone

**Estimated time remaining:** 9-12 hours

---

## 🎯 Learning Goals

By the end of this stage, you will:

- ✅ Understand integration vs unit testing
- ✅ Test HTTP API endpoints with FastAPI TestClient
- ✅ Verify database operations and transactions
- ✅ Test authentication and authorization flows
- ✅ Organize larger, more complex test suites
- ✅ Use test factories for realistic data

**Duration:** 3-4 hours

---

## 📂 Where to Look

**Choose your track:** Integration testing looks different for backend APIs vs frontend components!

---

### 🐍 Python Track (Backend API Integration)

**📁 Folder:** `/backend/tests/integration/`

1. **[`test_api_auth.py`](../../backend/tests/integration/test_api_auth.py)**

   - User registration and login endpoints
   - JWT token authentication
   - Authorization checks

2. **[`test_api_posts.py`](../../backend/tests/integration/test_api_posts.py)**

   - Creating, reading, updating, deleting posts
   - Comments and reactions
   - Reposts and interactions

3. **[`test_api_users.py`](../../backend/tests/integration/test_api_users.py)**

   - User profiles
   - Follow/unfollow functionality
   - Block/unblock operations

4. **[`test_api_feed.py`](../../backend/tests/integration/test_api_feed.py)**

   - Feed generation
   - Filtering and ordering
   - Complex queries

5. **[`test_database.py`](../../backend/tests/integration/test_database.py)**
   - Database constraints
   - Transactions and rollbacks
   - Cascade deletes

**Supporting Files:**

- [`backend/tests/conftest.py`](../../backend/tests/conftest.py) - pytest fixtures
- [`backend/tests/factories.py`](../../backend/tests/factories.py) - Test data factories

**Tools:** pytest, FastAPI TestClient, SQLAlchemy

---

### ☕ JavaScript Track (Frontend Integration)

**📁 Folders:** `/frontend/src/tests/integration/`

1. **[`contract.test.js`](../../frontend/src/tests/integration/contract.test.js)**

   - API contract validation (OpenAPI schema)
   - Ensures frontend/backend agreement
   - Request/response structure verification

2. **Frontend component tests with MSW:**

   - [`CreatePost.test.jsx`](../../frontend/src/tests/unit/CreatePost.test.jsx) - API mocking
   - [`Navbar.test.jsx`](../../frontend/src/tests/unit/Navbar.test.jsx) - Context integration
   - See [Lab 6B](../../learn/stage_4_performance_security/exercises/LAB_06B_Advanced_Component_Testing.md) for MSW patterns

3. **[`tests/mocks/handlers.js`](../../frontend/src/tests/mocks/handlers.js)**
   - Mock Service Worker API handlers
   - Realistic network mocking
   - Schema-compliant responses

**Supporting Files:**

- [`frontend/src/tests/setup.js`](../../frontend/src/tests/setup.js) - MSW server setup
- [`frontend/src/tests/contract-helpers.js`](../../frontend/src/tests/contract-helpers.js) - Contract validation utilities

**Tools:** Vitest, MSW (Mock Service Worker), axios, OpenAPI validation

---

### 🔄 Hybrid Track

**Test the full stack!** This is what most QA roles require.

1. Backend APIs (Python) - How endpoints work
2. Frontend integration (JavaScript) - How UI consumes those APIs
3. Contract tests (JavaScript) - Verify they agree on structure
4. See how changes in backend schema break frontend tests!

**Time:** 4-5 hours (both tracks)

---

## 🔍 What to Look For

### 1. HTTP Testing Pattern

```python
def test_api_endpoint(client, auth_headers):
    # Arrange - Prepare request data
    payload = {"title": "Test Post"}

    # Act - Make HTTP request
    response = client.post("/posts", json=payload, headers=auth_headers)

    # Assert - Verify response
    assert response.status_code == 201
    assert response.json()["title"] == "Test Post"
```

**Key observations:**

- `client` fixture provides FastAPI TestClient
- `auth_headers` handles authentication
- We test the full HTTP request/response cycle

### 2. Database Integration

```python
def test_database_operation(db_session, test_user):
    # Create via API or directly in DB
    post = Post(title="Test", user_id=test_user.id)
    db_session.add(post)
    db_session.commit()

    # Query and verify
    found = db_session.query(Post).filter_by(id=post.id).first()
    assert found is not None
    assert found.title == "Test"
```

**Notice:**

- Tests interact with real database
- Fixtures handle cleanup between tests
- We verify data persistence

### 3. Test Organization

Look at how tests are grouped:

```python
class TestPostCreation:
    """Tests for creating posts."""

    def test_create_post_success(self):
        pass

    def test_create_post_unauthorized(self):
        pass

    def test_create_post_invalid_data(self):
        pass
```

**Benefits:**

- Related tests grouped together
- Shared setup via class fixtures
- Clear test categories

### 4. Authorization Testing

```python
def test_delete_other_users_post(client, test_user, test_user_2):
    # test_user_2 tries to delete test_user's post
    response = client.delete(
        f"/posts/{post_id}",
        headers=auth_headers_user_2
    )
    assert response.status_code == 403  # Forbidden
```

**Security matters!** Tests verify users can't access what they shouldn't.

### 5. Test Factories

```python
from tests.factories import UserFactory, PostFactory

user = UserFactory.create(db_session)
posts = PostFactory.create_batch(db_session, user_id=user.id, count=5)
```

**Factories provide:**

- Realistic test data
- Flexible data generation
- Reduced boilerplate

### 6. 🔍 Advanced Topic: API Contract Testing

**File:** [`backend/tests/integration/test_api_contract.py`](../../backend/tests/integration/test_api_contract.py)

This file demonstrates **property-based contract testing** with Schemathesis - an advanced technique that automatically generates hundreds of test cases from your API schema.

**What is it?**
Instead of writing individual test cases, Schemathesis reads your OpenAPI schema and automatically generates 500+ test cases to validate:

- All endpoints match documentation
- Required fields are enforced
- Data types are correct
- Edge cases are handled
- Security vulnerabilities are found (fuzzing)

**Example:** One test for POST /api/posts generates:

- Valid inputs (happy path)
- Missing required fields
- Wrong data types
- Boundary values
- XSS/injection attempts
- 50+ more scenarios you'd never think to test!

**Current Status:** ⚠️ **Skipped** (OpenAPI 3.1.0 compatibility)

FastAPI 0.115+ uses OpenAPI 3.1.0, but Schemathesis only has experimental support. The test is skipped until full support is available.

**Should I learn this?**

- 📚 **Yes!** Read [Contract Testing Guide](../../docs/guides/CONTRACT_TESTING.md) to understand the concept
- 🎯 **For now:** Focus on the 180 integration tests that ARE running
- 🔄 **Alternative:** Frontend contract testing works today! See [Lab 6C](../../learn/stage_4_performance_security/exercises/LAB_06C_Frontend_Integration_Testing.md)
- 💼 **Career value:** Understanding contract testing is a professional differentiator

**Come back to this after completing Stage 3.** The concept is important, but not critical for learning basic integration testing.

---

## 🏃 How to Practice

**Pick your track below:**

---

### 🐍 Python Track Practice

**Step 1: Run Backend Integration Tests**

```bash
cd backend
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Run all integration tests
pytest -m integration -v

# Run specific test file
pytest tests/integration/test_api_auth.py -v
```

**Expected:** All tests pass. Note they take longer than unit tests (database, HTTP).

**Step 2: Trace Complete API Flow**

Pick registration flow in `tests/integration/test_api_auth.py`:

1. Find `test_register_new_user_success`
2. Trace: HTTP POST → Validation → Database → Response
3. Verify by looking at actual endpoint code in `routers/auth.py`

**Step 3: Test Authorization**

Find test verifying authorization (e.g., deleting someone else's post).

**Questions:**

- What HTTP status code means "forbidden"? (403)
- What happens if you remove the auth check?
- How does the test verify security?

---

### ☕ JavaScript Track Practice

**Step 1: Run Frontend Integration Tests**

```bash
cd frontend

# Run contract tests (validate against backend API schema)
npm test -- tests/integration/contract.test.js

# Run component tests with MSW (mocked API)
npm test -- tests/unit/CreatePost.test.jsx
```

**Expected:** Tests pass, MSW intercepts API calls.

**Step 2: Understand Contract Testing**

Open `src/tests/integration/contract.test.js`:

1. Notice OpenAPI schema validation
2. See how frontend validates response structure
3. Understand: If backend changes API, these tests fail!

**Step 3: Explore MSW (Mock Service Worker)**

Open `src/tests/mocks/handlers.js`:

**Questions:**

- How does MSW mock the `/api/posts` endpoint?
- What response structure does it return?
- Why mock instead of calling real API?

**Step 4: Test Component + API Integration**

Look at `tests/unit/CreatePost.test.jsx`:

- Notice: `api.postsAPI.createPost.mockResolvedValueOnce()`
- This tests component behavior when API succeeds/fails
- Integration: Component logic + API calls (without real server)

---

### 🔄 Hybrid Track Practice

**Test both sides of the API contract!**

1. Run backend integration tests (Python)
2. Run frontend contract tests (JavaScript)
3. Make a breaking change to backend API response
4. See which tests fail (contract tests should catch it!)
5. Understand: This is how teams prevent integration bugs

---

## ✅ Success Criteria

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

## 🧠 Why This Matters

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

## 💡 Key Concepts

### Integration Test Characteristics

**Compared to Unit Tests:**

| Aspect           | Unit Tests              | Integration Tests       |
| ---------------- | ----------------------- | ----------------------- |
| **Speed**        | Milliseconds            | Seconds                 |
| **Scope**        | Single function         | Multiple components     |
| **Dependencies** | Mocked                  | Real (database, APIs)   |
| **Purpose**      | Verify logic            | Verify interactions     |
| **Failures**     | Pinpoint exact function | Show integration issues |

### Test Pyramid

```text
         /\
        /  \      ← Few E2E tests (slow, expensive)
       /____\
      /      \    ← More integration tests (moderate speed)
     /________\
    /          \  ← Many unit tests (fast, cheap)
   /____________\
```

**Integration tests** are the middle layer - balanced between speed and realism.

### HTTP Status Codes to Know

- `200 OK` - Success (GET, PATCH)
- `201 Created` - Success (POST)
- `204 No Content` - Success (DELETE)
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Not authenticated
- `403 Forbidden` - Authenticated but not authorized
- `404 Not Found` - Resource doesn't exist
- `500 Internal Server Error` - Server bug

---

## 🔗 Related Resources

### Hands-On Practice

- [Lab 3: Testing API Endpoints](exercises/LAB_03_Testing_API_Endpoints.md)
- [Lab 5: Test Data Management](exercises/LAB_05_Test_Data_Management.md)
- [Lab 6: Testing with Rate Limits](exercises/LAB_06_Testing_With_Rate_Limits.md)

### Documentation

- [API Testing Guide](../../docs/guides/TESTING_GUIDE.md)
- [FastAPI Testing Docs](https://fastapi.tiangolo.com/tutorial/testing/)
- [HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)

### Reference

- [Test Database Setup](../../backend/tests/README.md)
- [Test Factories Documentation](exercises/LAB_05_Test_Data_Management.md)

---

## 🧠 Self-Check Quiz (Optional)

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

**Answers:** [Check your answers here](solutions/stage_2_quiz_answers.md)

---

## 🤔 Reflection

Before moving to Stage 3, answer these:

1. **Why do integration tests need a database while unit tests don't?**

2. **Pick one test from `tests/integration/test_api_posts.py`. What would break if you removed authentication?**

3. **How do test factories make integration testing easier?**

4. **What's the difference between a 401 and a 403 status code? Find an example of each in the tests.**

5. **What's one integration test you would add to improve test coverage?**

**Document your answers** in [reflection.md](reflection.md).

---

## 🎉 Stage Complete

You now understand how to test multi-component systems!

### 👉 [Continue to Stage 3: API & E2E Testing](../stage_3_api_e2e/README.md)

---

_Pro tip: Integration tests are where most QA engineers spend their time. Master this, and you're job-ready! 💼_
