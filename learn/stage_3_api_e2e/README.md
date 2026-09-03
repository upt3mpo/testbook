# Stage 3: E2E Testing

**Testing Complete User Journeys**

> **💡 Language Selection**: This guide includes both Python and JavaScript examples. Both are expanded by default so you can see all approaches. Click the language tabs to collapse sections you don't need.

## Your Progress

[████████████░░░░░░░░] 60% complete

✅ Stage 1: Unit Tests (completed)<br>
✅ Stage 2: Integration Tests (completed)<br>
→ **Stage 3: E2E Testing** (you are here)<br>
⬜ Stage 4: Performance & Security<br>
⬜ Stage 5: Capstone

**Estimated time remaining:** 5-7 hours (core content) + 3-5 hours (optional exercises)

<h2 id="table-of-contents">Table of Contents</h2>

- [Why E2E Testing Matters: Testing Like a Real User](#why-e2e-testing-matters-testing-like-a-real-user)
- [Part 1: What Are E2E Tests?](#part-1-what-are-e2e-tests)
- [Part 2: Browser Automation with Playwright](#part-2-browser-automation-with-playwright)
- [Part 3: Page Object Model (POM)](#part-3-page-object-model-pom)
- [Part 4: Implementation Guide](#part-4-implementation-guide)
- [Part 5: API Contract Testing](#part-5-api-contract-testing)
- [Part 6: Hands-On Practice](#part-6-hands-on-practice)
- [Part 7: Additional Patterns](#part-7-additional-patterns)
- [Success Criteria](#success-criteria)
- [Why This Matters](#why-this-matters)
- [Related Resources](#related-resources)
- [Self-Check Quiz (Optional)](#self-check-quiz-optional)
- [Reflection](#reflection)
- [Stage Complete](#stage-complete)

---

## Why E2E Testing Matters: Testing Like a Real User

A backend team can have every unit test and every integration test passing and still ship a broken product: the API returns the right JSON, the database writes correctly, and none of that matters if a JavaScript error on the submit button means a real user can never complete the action. That gap - between "the pieces work" and "the assembled product works for a user clicking through a browser" - is exactly what E2E tests close. They catch cross-browser quirks, frontend/backend contract mismatches, and slow or broken UI flows that no lower-level test is positioned to see, because none of those tests open a real browser.

### The Testing Pyramid Applied

```text
                ▲
               /_\  ← Manual / Exploratory Testing
              /   \
             / E2E \  ← Playwright (JS / Python) ← STAGE 3: COMPLETE USER FLOWS
            /_______\
           /         \
          / Component \  ← Vitest + RTL (JS only)
         /_____________\
        /               \
       /  Integration    \  ← API / Component tests
      /___________________\
     /                     \
    /      Unit Tests       \  ← Vitest (JS) | pytest (Python)
   /_________________________\
```

E2E tests are the smallest slice of the pyramid on purpose: they're slower and more prone to timing-related flakiness than the layers below them, so the pyramid puts most of the coverage burden on unit and integration tests and reserves E2E for the workflows where only a real browser can tell you the truth - a full purchase flow, a login-to-post journey, anything where the frontend and backend have to agree in practice, not just on paper.

Writing E2E tests also changes how you think about the app you're testing: you start asking what a user actually does (not just what a function returns), what happens when the network is slow or a request fails partway through, and whether a flow that's awkward to automate is a sign it's awkward to use. That's the mindset this stage is building, more than any specific tool.

---

<h2 id="part-1-what-are-e2e-tests">Part 1: What Are E2E Tests?</h2>

### The Restaurant Customer Analogy

Imagine you're testing a restaurant. Unit tests would be like testing each chef individually. Integration tests would be like testing the kitchen workflow. But E2E tests would be like being a real customer - walking in the door, looking at the menu, ordering food, eating it, and paying the bill.

**End-to-end (E2E) tests** simulate real users interacting with your application in a browser, just like a real customer would.

### Why E2E Tests Matter

1. **Real user perspective**: Tests what users actually experience
2. **Catch UI bugs**: Issues that integration tests miss
3. **Test complete workflows**: Login → Action → Verify (full user journey)
4. **Cross-browser compatibility**: Works on Chrome, Firefox, Safari
5. **Visual verification**: See what users see

### E2E vs Integration: The Key Difference

<details open>
<summary><strong>🐍 Python</strong></summary>

```python
# Integration Test - Tests API endpoints
def test_create_post_api():
    response = client.post("/api/posts", json={"content": "Hello"})
    assert response.status_code == 201

# E2E Test - Tests complete user workflow
async def test_user_creates_post():
    # 1. User opens browser
    await page.goto("http://localhost:3000")

    # 2. User logs in
    await page.fill("#email", "user@test.com")
    await page.fill("#password", "password123")
    await page.click("#login-button")

    # 3. User creates post
    await page.fill("#post-input", "Hello World!")
    await page.click("#submit-post")

    # 4. User sees their post
    await expect(page.locator(".post-content")).to_have_text("Hello World!")
```

</details>

<details open>
<summary><strong>☕ JavaScript</strong></summary>

```javascript
// Integration Test - Tests API endpoints
test("create post API", async () => {
  const response = await fetch("/api/posts", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ content: "Hello" }),
  });
  expect(response.status).toBe(201);
});

// E2E Test - Tests complete user workflow
test("user creates post", async ({ page }) => {
  // 1. User opens browser
  await page.goto("http://localhost:3000");

  // 2. User logs in
  await page.fill("#email", "user@test.com");
  await page.fill("#password", "password123");
  await page.click("#login-button");

  // 3. User creates post
  await page.fill("#post-input", "Hello World!");
  await page.click("#submit-post");

  // 4. User sees their post
  await expect(page.locator(".post-content")).toHaveText("Hello World!");
});
```

</details>

---

<h2 id="part-2-browser-automation-with-playwright">Part 2: Browser Automation with Playwright</h2>

### The Puppet Master Analogy

Think of Playwright like being a puppet master for a browser. You can:

- Tell the browser to go to a website
- Click buttons and fill forms
- Wait for things to load
- Take screenshots
- Verify what the user sees

### Basic Playwright Test Structure

<details open>
<summary><strong>🐍 Python</strong></summary>

```python
async def test_user_can_create_post(page):
    # Arrange - Navigate to the app
    await page.goto("http://localhost:3000/feed")

    # Act - Simulate user actions
    await page.fill("#post-input", "Hello World!")
    await page.click("#submit-post")

    # Assert - Verify the result
    await expect(page.locator(".post-content").first).to_have_text("Hello World!")
```

</details>

<details open>
<summary><strong>☕ JavaScript</strong></summary>

```javascript
test("user can create post", async ({ page }) => {
  // Arrange - Navigate to the app
  await page.goto("http://localhost:3000/feed");

  // Act - Simulate user actions
  await page.fill("#post-input", "Hello World!");
  await page.click("#submit-post");

  // Assert - Verify the result
  await expect(page.locator(".post-content").first()).toHaveText(
    "Hello World!"
  );
});
```

</details>

### Key Playwright Concepts

**1. Page Object**: The browser tab you're controlling<br>
**2. Locators**: How you find elements on the page<br>
**3. Actions**: What you can do (click, fill, type)<br>
**4. Assertions**: How you verify results

### Common Playwright Actions

<details open>
<summary><strong>🐍 Python</strong></summary>

```python
# Navigation
await page.goto("http://localhost:3000")

# Filling forms
await page.fill("#email", "user@test.com")
await page.fill("#password", "password123")

# Clicking buttons
await page.click("#login-button")

# Waiting for elements
await page.wait_for_selector(".post-content")

# Taking screenshots
await page.screenshot(path="test-result.png")
```

</details>

<details open>
<summary><strong>☕ JavaScript</strong></summary>

```javascript
// Navigation
await page.goto("http://localhost:3000");

// Filling forms
await page.fill("#email", "user@test.com");
await page.fill("#password", "password123");

// Clicking buttons
await page.click("#login-button");

// Waiting for elements
await page.waitForSelector(".post-content");

// Taking screenshots
await page.screenshot({ path: "test-result.png" });
```

</details>

### Handling Async Operations

E2E tests must handle:

- **Network delays**: API calls take time
- **Animations**: UI transitions
- **Load times**: Pages loading
- **User interactions**: Clicking, typing

<details open>
<summary><strong>🐍 Python</strong></summary>

```python
# Wait for element to appear
await page.wait_for_selector(".post-content")

# Wait for navigation
await page.wait_for_url("**/feed")

# Wait for API response
async with page.expect_response("**/api/posts") as response:
    await page.click("#submit-post")
```

</details>

<details open>
<summary><strong>☕ JavaScript</strong></summary>

```javascript
// Wait for element to appear
await page.waitForSelector(".post-content");

// Wait for navigation
await page.waitForURL("**/feed");

// Wait for API response
await page.waitForResponse("**/api/posts", async () => {
  await page.click("#submit-post");
});
```

</details>

---

<h2 id="part-3-page-object-model-pom">Part 3: Page Object Model (POM)</h2>

### The Blueprint Analogy

Think of Page Object Model like having blueprints for each page of your app. Instead of every test knowing where every button is, you have a blueprint that says "this is how you create a post" or "this is how you log in."

### Why Use Page Object Model?

**Without POM (❌ Brittle):**

```python
# Every test duplicates selectors
def test_login():
    page.fill('[data-testid="email"]', 'user@test.com')
    page.fill('[data-testid="password"]', 'pass')
    page.click('[data-testid="submit"]')

def test_register():
    page.fill('[data-testid="email"]', 'new@test.com')
    # If selector changes, must update ALL tests!
```

**With POM (✅ Maintainable):**

```python
# Update selector in ONE place
class LoginPage:
    def login(self, email, password):
        self.page.fill(self.email_input, email)
        self.page.fill(self.password_input, password)
        self.page.click(self.submit_button)
```

### Page Object Structure

Testbook's own page objects use Playwright's **sync** API in Python
(no `async`/`await`), matching how the real test files call them. Here's
a trimmed version of the real `tests/e2e-python/pages/feed_page.py`:

```python
class FeedPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # Centralized selectors
        self.create_post_textarea = '[data-testid="create-post-textarea"]'
        self.create_post_submit = '[data-testid="create-post-submit-button"]'
        self.post_items = '[data-testid-generic="post-item"]'

    def create_post(self, content: str) -> None:
        """Create a new post and verify it appears."""
        self.page.fill(self.create_post_textarea, content)
        self.page.click(self.create_post_submit)
        expect(self.first_post()).to_contain_text(content)

    def first_post(self):
        """Get the first (most recent) post."""
        return self.page.locator(self.post_items).first
```

The JavaScript version (`tests/e2e/pages/FeedPage.js`) is `async`, since
Playwright's JS API is asynchronous throughout - but the shape is the
same: a class wrapping selectors and named methods, extended from a
shared `BasePage`. See both files in full for the rest of the feed
interactions (react, edit, delete, comment, repost).

**Benefits:**

- **Reusable**: One method for creating posts
- **Maintainable**: Change selector in one place
- **Readable**: `feed_page.create_post("Hello")` is clear
- **Testable**: Can test page objects independently

---

<h2 id="part-4-implementation-guide">Part 4: Implementation Guide</h2>

Now let's see these concepts in real code! Choose your track:

> **⚠️ Before you run anything below:** E2E tests need the app running, and the backend specifically needs `TESTING=true` (plain `./start-dev.sh` with no `backend/.env` leaves it unset, which disables the `/api/dev/reset` endpoint and rate-limit allowances these tests depend on). See [Playwright Quick Start](../../docs/guides/PLAYWRIGHT_QUICKSTART.md) for the full setup.

### Python Track: E2E Testing with Playwright

**Open `tests/e2e-python/test_auth.py` and find `test_register_new_user_successfully`:**

```python
def test_register_new_user_successfully(
    self, page: Page, base_url: str, test_users: dict, fresh_database
):
    """
    Test new user registration with complete user workflow.

    This test verifies the entire user registration journey:
    1. User navigates to registration page
    2. User fills out registration form
    3. User submits form
    4. System processes registration
    5. User is automatically logged in
    6. User is redirected to feed page
    7. User sees their profile in navigation

    This is a critical E2E test that ensures the complete
    registration flow works from the user's perspective.
    """
    # Arrange - Navigate to registration page and prepare unique user data
    page.goto(f"{base_url}/register")

    # Generate unique user data to avoid conflicts
    timestamp = int(time.time())
    new_user = {
        "email": f"testuser{timestamp}@testbook.com",
        "username": f"testuser{timestamp}",
        "displayName": "Test User",
        "password": "TestPass123!",
    }

    # Act - Fill registration form and submit
    page.fill('[data-testid="register-email-input"]', new_user["email"])
    page.fill('[data-testid="register-username-input"]', new_user["username"])
    page.fill('[data-testid="register-displayname-input"]', new_user["displayName"])
    page.fill('[data-testid="register-password-input"]', new_user["password"])
    page.click('[data-testid="register-submit-button"]')

    # Assert - Verify auto-login and redirect to feed
    page.wait_for_url(f"{base_url}/", timeout=10000)  # Redirected to feed
    expect(page.locator('[data-testid="navbar"]')).to_be_visible(
        timeout=10000
    )  # Logged in
    expect(page.locator('[data-testid="navbar-username"]')).to_contain_text(
        new_user["displayName"]  # Correct user displayed
    )
```

**Guided Walkthrough:**

1. **Arrange**: We navigate to the login page
2. **Act**: We fill in the email and password, then click login
3. **Assert**: We verify the user was redirected to the feed page

**Try This:**

1. **Run the test from command line:**

   ```bash
   # Run specific test
   pytest tests/e2e-python/test_auth.py::TestAuthentication::test_register_new_user_successfully -v

   # Run in headed mode (see browser)
   HEADLESS=false pytest tests/e2e-python/test_auth.py::TestAuthentication::test_register_new_user_successfully -v

   # Run with screenshots on failure
   pytest tests/e2e-python/test_auth.py::TestAuthentication::test_register_new_user_successfully -v --screenshot=only-on-failure
   ```

2. **Debug E2E test failures:**

   ```bash
   # Run with video recording
   pytest tests/e2e-python/test_auth.py -v --video=retain-on-failure

   # Run with trace for debugging
   pytest tests/e2e-python/test_auth.py -v --tracing=on

   # Run with slow motion to see what's happening
   pytest tests/e2e-python/test_auth.py -v --slowmo=1000
   ```

3. **Make it fail intentionally to see debugging tools:**

   ```python
   # Temporarily change this line in the test:
   await expect(page).to_have_url(f"{base_url}/")  # Change to: await expect(page).to_have_url(f"{base_url}/wrong")
   ```

   Then run with `--screenshot=only-on-failure` to see the screenshot!

4. **Fix it back and run again to see it pass**

**What you'll learn:**

- How to run E2E tests from command line
- How to debug E2E test failures with screenshots and videos
- How to use headed mode for visual debugging
- The importance of proper waits and async handling

**More Examples:**

- `test_login_success` - See authentication flow
- `test_logout_success` - Learn about session management
- Full file: [test_auth.py](../../tests/e2e-python/test_auth.py)

### JavaScript Track: E2E Testing with Playwright

**Open `tests/e2e/auth.spec.js` and find the registration test:**

```javascript
test("should register new user successfully", async ({ page }) => {
  /**
   * Test complete user registration workflow.
   *
   * This test verifies the entire user registration journey:
   * 1. User navigates to registration page
   * 2. User fills out registration form
   * 3. User submits form
   * 4. System processes registration
   * 5. User is automatically logged in
   * 6. User is redirected to feed page
   * 7. User sees their profile in navigation
   *
   * This is a critical E2E test that ensures the complete
   * registration flow works from the user's perspective.
   */

  // Arrange - Prepare test user data
  const newUser = {
    email: "testuser@example.com",
    username: "testuser",
    displayName: "Test User",
    password: "TestPassword123!",
  };

  // Act - Register user through UI helper
  await registerUser(page, newUser);

  // Assert - Verify successful registration and auto-login
  await expect(page).toHaveURL("/"); // Redirected to feed
  await expect(page.locator('[data-testid="navbar"]')).toBeVisible(); // Logged in
  await expect(page.locator('[data-testid="navbar-username"]')).toContainText(
    newUser.displayName
  ); // Correct user
});
```

**Guided Walkthrough:**

1. **Arrange**: We navigate to the login page
2. **Act**: We fill in the email and password, then click login
3. **Assert**: We verify the user was redirected to the feed page

**Try This:**

1. **Run the test from command line (from the `tests/` directory):**

   ```bash
   cd tests

   # Run specific test
   npx playwright test auth.spec.js -g "should register new user successfully"

   # Run in headed mode (see browser)
   npx playwright test auth.spec.js --headed
   ```

   Screenshots and videos aren't CLI flags for this version of Playwright Test - they're
   already configured in `tests/playwright.config.js` (`screenshot: "only-on-failure"`,
   `video: "retain-on-failure"`), so a failing test captures both automatically.

2. **Debug E2E test failures:**

   ```bash
   # Force tracing on for this run
   npx playwright test auth.spec.js --trace=on

   # Then open the trace viewer for a failed test
   npx playwright show-trace test-results/**/trace.zip
   ```

3. **Make it fail intentionally to see debugging tools:**

   ```javascript
   // Temporarily change this line in the test:
   await expect(page).toHaveURL("/"); // Change to: await expect(page).toHaveURL('/wrong')
   ```

   Then check `test-results/` for the automatically captured screenshot and video!

4. **Fix it back and run again to see it pass**

**What you'll learn:**

- How to run E2E tests from command line
- How to debug E2E test failures with screenshots and videos
- How to use headed mode for visual debugging
- The importance of proper waits and async handling

**More Examples:**

- `posts.spec.js` - See post creation workflows
- `users.spec.js` - Learn about user interactions
- Full file: [auth.spec.js](../../tests/e2e/auth.spec.js)

### Hybrid Track

**Test the full stack!** This is what most QA roles require.

1. **Python E2E** - Backend-focused testing with Playwright
2. **JavaScript E2E** - Frontend-focused testing with Playwright
3. **API Contract Tests** - Verify frontend/backend agreement
4. **See the connection**: Make a UI change and watch E2E tests fail!

---

<h2 id="part-5-api-contract-testing">Part 5: API Contract Testing</h2>

### The Contract Analogy

Think of API contracts like a contract between two parties. The frontend says "I expect the API to return data in this format" and the backend says "I promise to return data in that format." Contract tests verify both sides keep their promises.

### What Are API Contracts?

API contracts define:

- **Request format**: What data to send
- **Response format**: What data to expect
- **Status codes**: What each response means
- **Error handling**: What happens when things go wrong

### Contract Testing Pattern

```python
def test_posts_api_contract(client):
    # Act - Make API request
    response = client.get("/api/posts")

    # Assert - Verify response structure
    assert response.status_code == 200
    data = response.json()

    # Check required fields exist
    assert "posts" in data
    assert isinstance(data["posts"], list)

    # Check each post has required fields
    for post in data["posts"]:
        assert "id" in post
        assert "content" in post
        assert "created_at" in post
        assert "user_id" in post
```

### Why Contract Testing Matters

1. **Prevent breaking changes**: Catch when APIs change unexpectedly
2. **Documentation**: Contracts serve as living documentation
3. **Team coordination**: Frontend and backend teams stay in sync
4. **Quality assurance**: Ensure APIs work as expected

### Contract Testing Tools

**Postman Collections:**

```bash
# Run contract tests with Newman
newman run tests/api/Testbook.postman_collection.json
```

**OpenAPI Schema Validation:**

```python
# Validate against OpenAPI schema
def test_api_matches_openapi_schema(client):
    response = client.get("/api/posts")
    # Validate response matches OpenAPI schema
    validate_response(response.json(), openapi_schema)
```

---

<h2 id="part-6-hands-on-practice">Part 6: Hands-On Practice</h2>

### Step 0: Start the App in Testing Mode

E2E tests drive a real browser against a running app, and they need the backend started with `TESTING=true` (this enables the dev-only `/api/dev/reset` endpoint and higher rate limits the suite relies on between tests):

```bash
# Terminal 1: backend, in testing mode
cd backend
source .venv/bin/activate      # Windows: .venv\Scripts\activate
TESTING=true uvicorn main:app --reload --port 8000

# Terminal 2: frontend
cd frontend
npm run dev
```

Leave both running. See [Playwright Quick Start](../../docs/guides/PLAYWRIGHT_QUICKSTART.md) if anything here is unclear.

### Step 1: Run E2E Tests

**Python Track:**

```bash
# Terminal 3
cd tests/e2e-python
pip install -r requirements.txt   # first time only
pytest -v
```

**JavaScript Track:**

```bash
# Terminal 3
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

**Python Track:**
Open `tests/e2e-python/pages/feed_page.py`

**JavaScript Track:**
Open `tests/e2e/pages/FeedPage.js`

Both files cover the same feed interactions (create post, react, edit,
delete, comment) - compare them side by side and see how the same
Page Object Model looks in each language's idioms.

**Questions:**

1. What interactions are abstracted?
2. How do page objects reduce duplication?
3. What happens if a selector changes?

### Step 4: Test a Complete Flow

Trace a full user journey:

1. Find `test_complete_workflow_with_pom` in [`tests/e2e-python/examples/test_page_objects_example.py`](../../tests/e2e-python/examples/test_page_objects_example.py) (login → create post → view profile)
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

### Step 6: Write Your First E2E Test

**Python Track - Test user profile viewing:**

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

**JavaScript Track - Test user profile viewing:**

```javascript
test("user can view profile", async ({ page }) => {
  // Navigate to user profile
  await page.goto("http://localhost:3000/profile/testuser");

  // Verify profile loaded
  await expect(page.locator(".profile-username")).toHaveText("testuser");

  // Verify posts are visible
  await expect(page.locator(".user-posts")).toBeVisible();
});
```

---

<h2 id="part-7-additional-patterns">Part 7: Additional Patterns</h2>

**📝 Note:** The patterns below are **additional enhancements** to your E2E testing skills. All the **core concepts** needed to meet the Stage 3 success criteria are covered in Parts 1-6 above.

These patterns enhance your E2E testing capabilities:

### Visual Testing

Capture screenshots and videos for debugging:

```python
# Take screenshot
await page.screenshot(path="test-result.png")

# Full page screenshot
await page.screenshot(path="full-page.png", full_page=True)

# Video recording (configured in playwright.config)
```

### Cross-Browser Testing

Test on multiple browsers:

```python
# Test on Chrome, Firefox, Safari
@pytest.mark.parametrize("browser", ["chromium", "firefox", "webkit"])
async def test_cross_browser(page, browser):
    # Test runs on each browser
    pass
```

### Network Interception

Mock API responses:

```python
# Intercept API calls
await page.route("**/api/posts", lambda route: route.fulfill(
    status=200,
    content_type="application/json",
    body='{"posts": []}'
))
```

### Retry Strategies

Handle flaky tests:

```python
# Retry failed tests
@pytest.mark.flaky(reruns=3)
async def test_flaky_operation(page):
    # Test that might fail occasionally
    pass
```

---

<h2 id="success-criteria">Success Criteria</h2>

You're ready for Stage 4 when you can:

**Core concepts (all tracks):**

- [] Explain when to use E2E vs integration tests
- [] Write a basic Playwright test
- [] Use Page Object Model effectively
- [] Handle waits and async operations
- [] Debug E2E test failures using screenshots
- [] Understand API contract testing
- [] Test complete multi-step user workflows
- [] Choose appropriate test granularity (unit vs integration vs E2E)

**Python Track:**

- [] Use Playwright Python for browser automation
- [] Create page objects for maintainable tests
- [] Handle async operations with pytest-asyncio
- [] Debug tests with screenshots and videos

**JavaScript Track:**

- [] Use Playwright JavaScript for browser automation
- [] Create test fixtures for reusable setup
- [] Handle async operations with async/await
- [] Debug tests with screenshots and videos

**Hybrid Track:**

- [] Can explain how E2E tests complement integration tests
- [] Understand when to use each testing approach
- [] Can write E2E tests in both Python and JavaScript

---

<h2 id="why-this-matters">Why This Matters</h2>

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

<h2 id="related-resources">Related Resources</h2>

### Hands-On Practice

**🐍 Python Track:**

- [Lab 9: Basic E2E Testing (Python)](exercises/LAB_09_Basic_E2E_Testing_Python.md)
- [Lab 10: Advanced E2E Patterns (Python)](exercises/LAB_10_Advanced_E2E_Patterns_Python.md)
- [Lab 11: Cross-Browser Testing (Python)](exercises/LAB_11_Cross_Browser_Testing_Python.md)
- [Lab 12: E2E Test Organization (Python)](exercises/LAB_12_E2E_Test_Organization_Python.md)

**🟨 JavaScript Track:**

- [Lab 9: Basic E2E Testing (JavaScript)](exercises/LAB_09_Basic_E2E_Testing_JavaScript.md)
- [Lab 10: Advanced E2E Patterns (JavaScript)](exercises/LAB_10_Advanced_E2E_Patterns_JavaScript.md)
- [Lab 11: Cross-Browser Testing (JavaScript)](exercises/LAB_11_Cross_Browser_Testing_JavaScript.md)
- [Lab 12: E2E Test Organization (JavaScript)](exercises/LAB_12_E2E_Test_Organization_JavaScript.md)

### Documentation

- [Playwright Documentation](https://playwright.dev/)
- [E2E Testing Guide](../../docs/guides/TESTING_GUIDE.md)
- [Contract Testing Guide](../../docs/guides/CONTRACT_TESTING.md)

### Reference

- [Playwright Python API](https://playwright.dev/python/)
- [Playwright JavaScript Docs](https://playwright.dev/docs/intro)
- [Postman Collections](../../tests/api/README.md)

---

<h2 id="self-check-quiz-optional">Self-Check Quiz (Optional)</h2>

Before moving to Stage 4, can you answer these questions?

1. **What's the main difference between E2E tests and integration tests?**

   - A) E2E tests are faster
   - B) E2E tests simulate real user interactions
   - C) Integration tests use mocks, E2E tests don't
   - D) E2E tests are more important

2. **What is the Page Object Model?**

   - A) A way to organize test files
   - B) A design pattern for reusable page interactions
   - C) A tool for taking screenshots
   - D) A method for handling async operations

3. **Why do E2E tests need to handle async operations?**

   - A) To make tests run faster
   - B) Because browsers are asynchronous
   - C) To avoid using mocks
   - D) To test multiple functions at once

4. **What's the purpose of API contract testing?**

   - A) To test API performance
   - B) To verify API response structure
   - C) To mock API responses
   - D) To test API security

5. **When should you use E2E tests?**
   - A) For every test case
   - B) For critical user workflows only
   - C) For unit testing
   - D) For API testing only

**Answers:** [Check your answers here](../solutions/stage_3_quiz_answers.md)

---

<h2 id="reflection">Reflection</h2>

Before moving to Stage 4, answer these:

1. **Why are E2E tests slower than integration tests?**

2. **Pick one E2E test from the codebase. What would break if you changed a CSS selector?**

3. **How do page objects make E2E tests more maintainable?**

4. **What's the difference between a 200 and a 201 status code? Find an example of each in the tests.**

5. **What's one E2E test you would add to improve test coverage?**

**Document your answers** in [reflection.md](reflection.md).

---

<h2 id="stage-complete">Stage Complete</h2>

You now understand how to test complete user journeys!

### [Continue to Stage 4: Performance & Security](../stage_4_performance_security/README.md)

---

_Pro tip: E2E testing is where QA engineers really shine. Master this, and you're ready for senior roles! 🚀_
