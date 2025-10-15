# 🌐 Stage 3: API & E2E Testing

**Testing Complete User Journeys**

End-to-end (E2E) tests simulate real users interacting with your application in a browser. API tests verify contracts and external integrations. Together, they ensure your entire system works as users expect.

---

## 🎯 Learning Goals

By the end of this stage, you will:

- ✅ Understand E2E testing and when to use it
- ✅ Write browser automation tests with Playwright
- ✅ Use Page Object Model for maintainable tests
- ✅ Test complete user workflows (login → action → verify)
- ✅ Validate API contracts with OpenAPI/Postman
- ✅ Handle async operations and network requests
- ✅ Capture screenshots and videos for debugging

**Duration:** 4-5 hours

---

## 📂 Where to Look

### E2E Tests (Playwright)

Choose your language preference:

#### 🐍 Python E2E Tests

1. **[`tests/e2e-python/test_auth.py`](../../tests/e2e-python/test_auth.py)**
   - Login and registration flows
   - Session management

2. **[`tests/e2e-python/test_posts.py`](../../tests/e2e-python/test_posts.py)**
   - Creating and interacting with posts
   - Comments and reactions

3. **[`tests/e2e-python/test_users.py`](../../tests/e2e-python/test_users.py)**
   - User profiles and interactions
   - Follow/unfollow workflows

4. **[`tests/e2e-python/pages/`](../../tests/e2e-python/pages/)**
   - Page Object Model implementation
   - Reusable page classes

#### ☕ JavaScript E2E Tests

1. **[`tests/e2e/auth.spec.js`](../../tests/e2e/auth.spec.js)**
   - Authentication flows
   - Login/logout

2. **[`tests/e2e/posts.spec.js`](../../tests/e2e/posts.spec.js)**
   - Post creation and management
   - User interactions

3. **[`tests/e2e/users.spec.js`](../../tests/e2e/users.spec.js)**
   - Profile viewing
   - Social features

### API/Contract Tests

1. **[`tests/api/README.md`](../../tests/api/README.md)**
   - API testing overview
   - Newman/Postman collection usage

2. **[`tests/api/Testbook.postman_collection.json`](../../tests/api/Testbook.postman_collection.json)**
   - Complete API contract tests
   - Request/response examples

3. **[`backend/tests/integration/test_api_contract.py`](../../backend/tests/integration/test_api_contract.py)**
   - Property-based contract testing with Schemathesis
   - ⚠️ Currently skipped (OpenAPI 3.1.0 compatibility)
   - See [Contract Testing Guide](../../docs/guides/CONTRACT_TESTING.md) for full explanation

**💡 Advanced API Testing (Optional):**

Contract testing automatically generates hundreds of test cases from your API schema. While the backend Schemathesis test is currently skipped, you can:

- Learn the concept: [Contract Testing Guide](../../docs/guides/CONTRACT_TESTING.md)
- Try frontend contracts: [Lab 6C](../../labs/LAB_06C_Frontend_Integration_Testing.md) (works today!)
- Use Postman collections above for manual contract validation

---

## 🔍 What to Look For

### 1. E2E Test Structure

```python
async def test_user_can_create_post(page, login):
    # Arrange - User is logged in (via login fixture)
    await page.goto("http://localhost:3000/feed")

    # Act - Complete user workflow
    await page.fill("#post-input", "Hello World!")
    await page.click("#submit-post")

    # Assert - Verify UI updated
    await expect(page.locator(".post-content").first).to_have_text("Hello World!")
```

**Key observations:**

- Tests real browser interactions
- Uses actual URLs and selectors
- Verifies visual/UI elements
- Async/await for browser operations

### 2. Page Object Model (POM)

```python
class FeedPage:
    def __init__(self, page):
        self.page = page
        self.post_input = page.locator("#post-input")
        self.submit_button = page.locator("#submit-post")

    async def create_post(self, content):
        await self.post_input.fill(content)
        await self.submit_button.click()
```

**Benefits:**

- Reusable page interactions
- Centralized selectors
- Easier maintenance
- More readable tests

### 3. Waiting and Timing

```python
# Wait for element to appear
await page.wait_for_selector(".post-content")

# Wait for navigation
await page.wait_for_url("**/feed")

# Wait for API response
async with page.expect_response("**/api/posts") as response:
    await page.click("#submit-post")
```

**E2E tests must handle:**

- Network delays
- Animations
- Async operations
- Load times

### 4. Contract Testing

```python
def test_api_response_matches_schema(client):
    response = client.get("/posts")
    data = response.json()

    # Validate structure
    assert "posts" in data
    assert isinstance(data["posts"], list)

    # Validate schema
    for post in data["posts"]:
        assert "id" in post
        assert "title" in post
        assert "created_at" in post
```

**Contract tests ensure:**

- API structure doesn't break
- Required fields are present
- Data types are correct
- Backwards compatibility

### 5. Visual Testing

```python
# Take screenshot
await page.screenshot(path="test-result.png")

# Full page screenshot
await page.screenshot(path="full-page.png", full_page=True)

# Video recording (configured in playwright.config)
```

**Visual artifacts help:**

- Debug failures
- Document bugs
- Communicate with team
- Create demos

---

## 🏃 How to Practice

### Step 1: Run E2E Tests

#### Python E2E

```bash
cd tests/e2e-python
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pytest -v
```

#### JavaScript E2E

```bash
cd tests
npx playwright test
```

**Watch the browser!** E2E tests are visual - see what happens.

### Step 2: Run in Headed Mode

See the browser while tests run:

```bash
# Python
HEADLESS=false pytest -v

# JavaScript
npx playwright test --headed
```

**This is amazing for learning!** Watch each step.

### Step 3: Explore Page Objects

Open `tests/e2e-python/pages/feed_page.py`:

**Questions:**

1. What interactions are abstracted?
2. How do page objects reduce duplication?
3. What happens if a selector changes?

### Step 4: Test a Complete Flow

Trace a full user journey:

1. Find `test_user_can_login_and_create_post`
2. List every step the test performs
3. Run it in headed mode
4. Identify what could fail at each step

### Step 5: Run Contract Tests

```bash
cd tests/api

# Using Newman (if installed)
newman run Testbook.postman_collection.json

# Or using Python
cd ../../backend
pytest tests/integration/test_api_contract.py -v
```

**Check:** Do all endpoints return expected schemas?

### Step 6: Write an E2E Test

Add a test for viewing a user profile:

```python
@pytest.mark.e2e
async def test_view_user_profile(page, login, test_user):
    """User can view another user's profile."""
    # Navigate to user profile
    await page.goto(f"http://localhost:3000/profile/{test_user.username}")

    # Verify profile loaded
    await expect(page.locator(".profile-username")).to_have_text(test_user.username)

    # Verify posts are visible
    await expect(page.locator(".user-posts")).to_be_visible()
```

---

## ✅ Success Criteria

You're ready for Stage 4 when you can:

- [ ] Explain when to use E2E vs integration tests
- [ ] Write a basic Playwright test
- [ ] Use Page Object Model effectively
- [ ] Handle waits and async operations
- [ ] Debug E2E test failures using screenshots
- [ ] Understand API contract testing
- [ ] Test complete multi-step user workflows
- [ ] Choose appropriate test granularity (unit vs integration vs E2E)

---

## 🧠 Why This Matters

### In Real QA Teams

- **E2E tests catch UI bugs** - Issues integration tests miss
- **Contract tests prevent breaking changes** - Frontend/backend stay in sync
- **User perspective** - Tests verify actual user experience
- **Cross-browser testing** - Works on Chrome, Firefox, Safari
- **Visual regression** - Screenshots show unexpected changes

### For Your Career

- **High-value skill** - E2E testing is in huge demand
- **Tool expertise** - Playwright is industry-leading
- **Full-stack knowledge** - Understand frontend + backend + UI
- **Debugging ability** - E2E tests teach systematic troubleshooting
- **Portfolio demos** - Videos/screenshots showcase your work

---

## 💡 Key Concepts

### Testing Pyramid Extended

```text
       /\      ← Manual exploratory testing
      /  \     ← Few E2E tests (slowest, most expensive)
     /____\
    /      \   ← Some API/contract tests
   /________\
  /          \ ← More integration tests
 /____________\
/              \ ← Many unit tests (fastest, cheapest)
```

**E2E tests are at the top:**

- Most realistic
- Catch the most critical bugs
- But slowest and most fragile
- Use sparingly for key workflows

### When to Use Each Test Type

| Test Type | When to Use | Example |
|-----------|-------------|---------|
| **Unit** | Test business logic | Password hashing function |
| **Integration** | Test API endpoints | POST /posts returns 201 |
| **E2E** | Test user workflows | User logs in and creates post |
| **Contract** | Verify API schemas | /posts returns correct structure |

### E2E Best Practices

✅ **DO:**

- Test critical user paths
- Use Page Object Model
- Run in CI/CD pipeline
- Capture screenshots on failure
- Keep tests independent

❌ **DON'T:**

- Test every edge case with E2E
- Hard-code waits (use smart waits)
- Test API logic in E2E
- Make tests depend on each other
- Ignore flaky tests

---

## 🔗 Related Resources

### Hands-On Practice

- [Lab 4: E2E Testing (Python)](../../labs/LAB_04_E2E_Testing_Python.md)
- [Lab 4: E2E Testing (JavaScript)](../../labs/LAB_04_E2E_Testing_JavaScript.md)
- [Lab 4B: Advanced E2E (Python)](../../labs/LAB_04B_Advanced_E2E_Python.md)
- [Lab 6B: Component Testing (JavaScript)](../../labs/LAB_06B_Advanced_Component_Testing.md)
- [Lab 6C: Contract Testing (JavaScript)](../../labs/LAB_06C_Frontend_Integration_Testing.md)

### Documentation

- [Playwright Documentation](https://playwright.dev/)
- [E2E Testing Guide](../../tests/e2e-python/README.md)
- [API Testing with Newman](../../tests/api/NEWMAN_GUIDE.md)

### Advanced Topics

- [Section 8: Advanced E2E Patterns](../../docs/course/SECTION_08_ADVANCED_E2E_PATTERNS.md)
- [Flaky Tests Guide](../../docs/guides/FLAKY_TESTS_GUIDE.md)

---

## 🤔 Reflection

Before moving to Stage 4, answer these:

1. **Why are E2E tests slower than integration tests? Is it worth the trade-off?**

2. **How does the Page Object Model make tests more maintainable?**

3. **Pick one E2E test. List 3 things that could cause it to fail (even if the app works fine).**

4. **What's the difference between testing an API with integration tests vs contract tests?**

5. **Imagine you're testing a shopping cart. What would you test with E2E vs integration tests?**

**Document your answers** in [reflection.md](reflection.md).

---

## 🎉 Stage Complete

You now understand full-stack testing from browser to database!

### 👉 [Continue to Stage 4: Performance & Security](../stage_4_performance_security/README.md)

---

*Pro tip: E2E testing is where QA engineers become invaluable. Master this, and you're a full-stack QA engineer! 🚀*
