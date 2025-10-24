# 🧪 Lab 5: API Endpoint Testing (Python)

**Estimated Time:** 60 minutes<br>
**Difficulty:** Intermediate<br>
**Language:** 🐍 Python<br>
**Prerequisites:** Labs 1-4 completed

**💡 Need JavaScript instead?** Try [Lab 5: API Endpoint Testing (JavaScript)](LAB_05_API_Endpoint_Testing_JavaScript.md)!

**What This Adds:** Master API testing with FastAPI TestClient - learn to test real HTTP endpoints, handle authentication, and verify JSON responses. This is essential for testing backend services.

---

<h2 id="what-youll-learn">🎯 What You'll Learn</h2>

- Test real API endpoints
- Use FastAPI TestClient
- Test authentication flow
- Verify JSON responses
- Use pytest fixtures

---

<h2 id="step-by-step-instructions">📋 Step-by-Step Instructions</h2>

### Step 1: Understand the API (10 minutes)

**What is an API endpoint?**

- URL that accepts requests: `/api/auth/login`
- Returns data: `{"access_token": "xxx"}`
- Like a function you call over HTTP

**Testbook's Login Endpoint:**

- **URL:** `POST /api/auth/login`
- **Input:** `{"email": "...", "password": "..."}`
- **Output:** `{"access_token": "...", "token_type": "bearer"}`

### Step 2: Look at Existing API Test (10 minutes)

**Open:** `backend/tests/integration/test_api_auth.py`

**Find this test:**

```python
def test_login_success(self, client, test_user):
    """
    Test successful login with correct credentials.

    This test verifies the complete login flow:
    1. User provides valid email and password
    2. API validates credentials against database
    3. API returns JWT token for authentication
    4. Response includes proper token format
    """
    # Arrange: Use the test_user fixture (already created in database)
    # The test_user has email "testuser@example.com" and password "TestPassword123!"

    # Act: Send POST request to login endpoint with valid credentials
    response = client.post(
        "/api/auth/login",
        json={
            "email": "testuser@example.com",    # Valid email from test_user fixture
            "password": "TestPassword123!",     # Valid password from test_user fixture
        },
    )

    # Assert: Verify the response is successful and contains expected data
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

    # Parse the JSON response
    data = response.json()

    # Verify the response contains an access token
    assert "access_token" in data, "Response should contain access_token"

    # Verify the token type is correct (JWT standard)
    assert data["token_type"] == "bearer", f"Expected 'bearer', got '{data['token_type']}'"
```

**Understand:**

- `client` - TestClient (makes fake API calls)
- `test_user` - Fixture that creates a test user
- `response.status_code` - HTTP status (200 = success)
- `response.json()` - Parse JSON response

✅ **Checkpoint:** You understand the test structure

### Step 3: Run the API Test (5 minutes)

```bash
pytest tests/integration/test_api_auth.py::TestLoginEndpoint::test_login_success -v
```

**Should see:**

```text
tests/test_api_auth.py::TestLoginEndpoint::test_login_success PASSED ✓
```

✅ **Checkpoint:** Test passes!

### Step 4: Write Your Own API Test (20 minutes)

**Challenge:** Test that login fails with wrong password

**Add to `TestLoginEndpoint` class:**

```python
def test_login_with_my_wrong_password(self, client, test_user):
    """Test that login fails with incorrect password."""
    # Arrange - test_user exists from fixture

    # Act - try to login with wrong password
    response = client.post(
        "/api/auth/login",
        json={
            "email": "testuser@example.com",
            "password": "WrongPassword999!",  # Wrong!
        },
    )

    # Assert - should fail
    assert response.status_code == 401  # Unauthorized
    # Should have error message
    assert "detail" in response.json()
```

**Run your test:**

```bash
pytest tests/integration/test_api_auth.py::TestLoginEndpoint::test_login_with_my_wrong_password -v
```

✅ **Checkpoint:** Your test passes!

### Step 5: Test Creating a Post (30 minutes)

**Challenge:** Test the post creation endpoint

**Create this test in `tests/integration/test_api_posts.py`:**

```python
def test_create_my_post(self, client, auth_headers):
    """Test creating a post via API."""
    # Act - create a post
    response = client.post(
        "/api/posts/",
        json={
            "content": "This is my test post!",
            "image_url": None,
            "video_url": None
        },
        headers=auth_headers  # Need auth to create posts
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "This is my test post!"
    assert data["id"] is not None  # Post got an ID
    assert data["author_username"] == "testuser"
```

**Run it:**

```bash
pytest tests/integration/test_api_posts.py::TestCreatePost::test_create_my_post -v
```

✅ **Checkpoint:** Post creation test passes!

---

<h2 id="what-you-learned">🎓 What You Learned</h2>

- ✅ How to test API endpoints with TestClient
- ✅ How to check HTTP status codes
- ✅ How to verify JSON responses
- ✅ How authentication headers work
- ✅ How to test both success and failure cases

---

## 💪 Practice Challenges

### Challenge 1: Test Post Deletion

Write a test that:

1. Creates a post
2. Deletes the post
3. Verifies post is gone (GET returns 404)

**Hint:** Look at `tests/integration/test_api_posts.py::TestDeletePost` for examples

### Challenge 2: Test Comment Creation

Write a test that:

1. Creates a post
2. Adds a comment to the post
3. Verifies comment appears

**Hint:** Endpoint is `POST /api/posts/{post_id}/comments`

### Challenge 3: Test Authorization

Write a test that:

1. User A creates a post
2. User B tries to delete it
3. Verifies it fails with 403 Forbidden

---

<h2 id="common-mistakes">🐛 Common Mistakes</h2>

**Mistake 1:** Forgetting authentication

```python
# ❌ Wrong
response = client.post("/api/posts/", json={...})

# ✅ Correct
response = client.post("/api/posts/", json={...}, headers=auth_headers)
```

**Mistake 2:** Wrong status code

```python
# Check what status code API actually returns
assert response.status_code == 200  # Not always 201!
```

**Mistake 3:** Not checking response structure

```python
# ✅ Always verify response has expected fields
data = response.json()
assert "id" in data
assert "content" in data
```

---

<h2 id="lab-completion-checklist">✅ Lab Completion Checklist</h2>

- [ ] Ran existing API tests
- [ ] Wrote `test_login_with_my_wrong_password` (passes)
- [ ] Wrote `test_create_my_post` (passes)
- [ ] Understand how TestClient works
- [ ] Understand auth headers
- [ ] Completed at least 1 practice challenge

---

<h2 id="quiz">🎯 Quiz</h2>

1. What HTTP status code means "Unauthorized"?
2. What does `client.post()` do?
3. Why do we need `auth_headers` for some endpoints?
4. What does `response.json()` return?
5. How is API testing different from unit testing?

\*_Answers at bottom of page_

---

<h2 id="further-reading">📚 Further Reading</h2>

- [TESTING_GUIDE.md - API Testing Section](../docs/guides/TESTING_GUIDE.md#api-testing)
- [FastAPI Testing Docs](https://fastapi.tiangolo.com/tutorial/testing/)
- Study: `tests/integration/test_api_auth.py` (complete file)

---

**🎉 You're now testing real APIs like a pro!**

**Next Lab:** [Lab 5: Test Data Management (Python)](LAB_05_Test_Data_Management_Python.md)

---

### Quiz Answers

1. 401 (Unauthorized)
2. Makes a POST request to the API
3. Because those endpoints require authentication
4. A Python dictionary/list from JSON
5. API testing tests whole endpoints (multiple functions together), unit testing tests single functions
