# 🚨 Common Mistakes & Solutions

**A catalog of frequent student errors and how to fix them**

---

## 🎯 Table of Contents

1. [Environment Setup Mistakes](#environment-setup-mistakes)
2. [Testing Command Mistakes](#testing-command-mistakes)
3. [Python/Pytest Mistakes](#pythonpytest-mistakes)
4. [Playwright/E2E Mistakes](#playwrighte2e-mistakes)
5. [Test Writing Mistakes](#test-writing-mistakes)
6. [Git & Version Control Mistakes](#git--version-control-mistakes)
7. [Conceptual Mistakes](#conceptual-mistakes)

---

## 🔧 Environment Setup Mistakes

### Mistake 1: Not Activating Virtual Environment

**Symptom:**

```bash
$ pytest
-bash: pytest: command not found
```

or

```bash
ModuleNotFoundError: No module named 'pytest'
```

**Why This Happens:**
Python packages are installed in the virtual environment, but you're using the system Python.

**Fix:**

```bash
# macOS/Linux
cd backend
source .venv/bin/activate

# Windows
cd backend
.venv\Scripts\activate

# Verify it worked - should show (venv) in prompt
(venv) $
```

**Prevention:**
Always activate venv before running tests. Add this to your workflow checklist.

---

### Mistake 2: Wrong Directory

**Symptom:**

```bash
$ pytest
ERROR: file or directory not found: tests
```

**Why This Happens:**
You're not in the `backend/` directory where the tests are located.

**Fix:**

```bash
# Check where you are
pwd

# Should be in: /path/to/Testbook/backend
cd backend

# Verify tests directory exists
ls tests/
```

**Prevention:**
Always run `cd backend` before running pytest commands.

---

### Mistake 3: Using Wrong Start Script

**Symptom:**

- Tests fail with connection errors
- App doesn't open correctly
- Port conflicts

**Why This Happens:**
Using `start.sh` (production) instead of `start-dev.sh` (development).

**Fix:**

```bash
# Stop current processes
# Press Ctrl+C in both terminals

# Use development mode
./start-dev.sh  # macOS/Linux
start-dev.bat   # Windows

# Open correct URL
http://localhost:3000  # Not 8000!
```

**Prevention:**
Read [WHICH_START_SCRIPT.md](../../WHICH_START_SCRIPT.md) and always use dev mode for learning.

---

### Mistake 4: Opening Wrong Port

**Symptom:**
"I started the app but only see JSON"

**Why This Happens:**
Opening `http://localhost:8000` which is the API, not the frontend.

**Fix:**

```bash
# Frontend is on port 3000 in dev mode
http://localhost:3000  ✅

# Port 8000 is the API
http://localhost:8000/docs  ✅ (API documentation)
http://localhost:8000  ❌ (Not the app)
```

**Prevention:**
Bookmark `http://localhost:3000` for development.

---

## 🧪 Testing Command Mistakes

### Mistake 5: Missing `-v` Flag

**Symptom:**

```bash
$ pytest
.....F..
```

"Which test failed? I can't tell!"

**Why This Happens:**
Without `-v` (verbose), pytest shows minimal output.

**Fix:**

```bash
# Always use verbose mode
pytest -v

# Shows:
tests/test_auth.py::test_login PASSED ✓
tests/test_auth.py::test_bad_password FAILED ✗
```

**Prevention:**
Make `pytest -v` your default command.

---

### Mistake 6: Running Tests Without Backend Running (E2E)

**Symptom:**

```bash
Error: connect ECONNREFUSED 127.0.0.1:8000
```

**Why This Happens:**
E2E tests need the app running, but it's not started.

**Fix:**

```bash
# Terminal 1: Start app
./start-dev.sh  # macOS/Linux or start-dev.bat (Windows)

# Terminal 2: Run E2E tests
cd tests
npx playwright test
```

**Prevention:**
Always start app before E2E tests. Backend tests don't need this (they use TestClient).

---

### Mistake 7: Forgetting to Reset Database

**Symptom:**

- Tests fail with "User already exists"
- Tests pass when run alone, fail when run together
- Inconsistent test results

**Why This Happens:**
Previous test data affects current tests.

**Fix:**

```bash
# Before running E2E tests
./reset-database.sh

# Or in test code
test.beforeEach(async ({ page }) => {
  await resetDatabase(page);
});
```

**Prevention:**
Reset database before each test suite or in beforeEach hooks.

---

## 🐍 Python/Pytest Mistakes

### Mistake 8: Test Name Doesn't Start with `test_`

**Symptom:**

```bash
$ pytest -v
collected 0 items
```

"Why aren't my tests running?"

**Why This Happens:**
Pytest only discovers functions starting with `test_`.

**Fix:**

```python
# ❌ BAD
def check_login():
    assert user.is_logged_in

# ✅ GOOD
def test_login():
    assert user.is_logged_in
```

**Prevention:**
Always start test functions with `test_`.

---

### Mistake 9: Using `==` Instead of `assert`

**Symptom:**

```python
def test_something():
    result == 5  # Test always passes!
```

**Why This Happens:**
`==` is a comparison that returns True/False but doesn't fail the test.

**Fix:**

```python
# ❌ BAD
def test_something():
    result == 5  # Just compares, doesn't assert

# ✅ GOOD
def test_something():
    assert result == 5  # Actually fails test if false
```

**Prevention:**
Always use `assert` keyword in tests.

---

### Mistake 10: Not Using Fixtures Properly

**Symptom:**

```python
def test_user():
    # Creating user manually every time
    user = User(email="test@test.com")
    db.add(user)
    db.commit()
```

**Why This Happens:**
Not understanding how fixtures provide reusable test data.

**Fix:**

```python
# ❌ BAD - Manual setup
def test_user_email():
    user = User(email="test@test.com")
    db.add(user)
    db.commit()
    assert user.email == "test@test.com"

# ✅ GOOD - Using fixture
def test_user_email(test_user):
    assert test_user.email == "testuser@example.com"
```

**Prevention:**
Check `conftest.py` for available fixtures before creating test data manually.

---

### Mistake 11: Forgetting to Import

**Symptom:**

```python
NameError: name 'pytest' is not defined
```

**Why This Happens:**
Missing import statements.

**Fix:**

```python
# Add at top of test file
import pytest
from models import User, Post
from auth import get_password_hash
```

**Prevention:**
Start every test file with necessary imports.

---

## 🎭 Playwright/E2E Mistakes

### Mistake 12: Using `waitForTimeout()` Everywhere

**Symptom:**

```javascript
await page.waitForTimeout(2000);  // Flaky tests!
await page.click('button');
```

**Why This Happens:**
Thinking you need to manually wait for things.

**Fix:**

```javascript
// ❌ BAD - Arbitrary timeout
await page.waitForTimeout(2000);
await page.click('button');

// ✅ GOOD - Wait for specific element
await page.waitForSelector('button', { state: 'visible' });
await page.click('button');

// ✅ EVEN BETTER - Playwright auto-waits
await page.click('button');  // Already waits!
```

**Prevention:**
Trust Playwright's auto-waiting. Only use `waitForTimeout` as last resort.

---

### Mistake 13: Wrong Selector

**Symptom:**

```javascript
Error: Timeout waiting for selector "button#login"
```

**Why This Happens:**
Using wrong selector or element doesn't exist.

**Fix:**

```javascript
// ❌ BAD - Fragile CSS selector
await page.click('.btn-primary.submit-btn')

// ✅ GOOD - Use data-testid
await page.click('[data-testid="login-submit-button"]')

// Check what exists
console.log(await page.content());  // See all HTML
```

**Prevention:**
Always use `data-testid` attributes. Check the frontend code to find the exact name.

---

### Mistake 14: Not Waiting for Navigation

**Symptom:**
Test runs too fast and misses navigation.

**Why This Happens:**
Click triggers navigation but test continues immediately.

**Fix:**

```javascript
// ❌ BAD - Might check before navigation completes
await page.click('a[href="/profile"]');
await expect(page).toHaveURL('/profile');  // Might fail

// ✅ GOOD - Wait for navigation
await Promise.all([
  page.waitForNavigation(),
  page.click('a[href="/profile"]')
]);

// ✅ EVEN BETTER - Wait for URL
await page.click('a[href="/profile"]');
await page.waitForURL('/profile');
```

**Prevention:**
Use `waitForURL()` or `waitForNavigation()` when clicking links.

---

### Mistake 15: Testing Implementation Instead of Behavior

**Symptom:**

```javascript
// Test breaks when CSS class names change
await expect(page.locator('.user-avatar-img')).toBeVisible();
```

**Why This Happens:**
Testing internal details (class names) instead of user-visible behavior.

**Fix:**

```javascript
// ❌ BAD - Testing implementation
await expect(page.locator('.user-avatar-img')).toBeVisible();

// ✅ GOOD - Testing behavior with data-testid
await expect(page.locator('[data-testid="user-avatar"]')).toBeVisible();

// ✅ EVEN BETTER - Testing user-visible text
await expect(page.getByAltText('User avatar')).toBeVisible();
```

**Prevention:**
Test what users see and do, not internal implementation details.

---

## ✍️ Test Writing Mistakes

### Mistake 16: Testing Multiple Things in One Test

**Symptom:**

```python
def test_user_functionality(test_user):
    # Creating post
    assert post.author_id == test_user.id
    # Following user
    assert user2 in test_user.following
    # Updating profile
    assert test_user.bio == "Updated"
    # Deleting post
    assert deleted_post is None
```

**Why This Happens:**
Trying to test too much at once.

**Fix:**

```python
# ❌ BAD - One giant test
def test_everything(test_user):
    # 50 lines of testing different things
    ...

# ✅ GOOD - Separate tests
def test_user_can_create_post(test_user):
    post = create_post(test_user)
    assert post.author_id == test_user.id

def test_user_can_follow_another_user(test_user, test_user_2):
    test_user.following.append(test_user_2)
    assert test_user_2 in test_user.following

def test_user_can_update_profile(test_user):
    test_user.bio = "Updated"
    assert test_user.bio == "Updated"
```

**Prevention:**
One test should test one thing. Name describes what it tests.

---

### Mistake 17: No Docstrings

**Symptom:**

```python
def test_user(test_user):
    assert test_user.email == "testuser@example.com"
```

"What does this test verify?"

**Why This Happens:**
Forgetting to document what the test does.

**Fix:**

```python
# ❌ BAD - No explanation
def test_user(test_user):
    assert test_user.email == "testuser@example.com"

# ✅ GOOD - Clear docstring
def test_user_has_valid_email(test_user):
    """Test that test user fixture creates user with correct email."""
    assert test_user.email == "testuser@example.com"
```

**Prevention:**
Always add docstring explaining what test verifies.

---

### Mistake 18: Not Testing Error Cases

**Symptom:**
Only testing the "happy path" where everything works.

**Why This Happens:**
Focusing on success cases, forgetting failures.

**Fix:**

```python
# ❌ INCOMPLETE - Only tests success
def test_login_success(client):
    response = client.post("/api/auth/login", json={...})
    assert response.status_code == 200

# ✅ COMPLETE - Tests both success and failure
def test_login_success(client):
    """Test login with correct credentials."""
    response = client.post("/api/auth/login", json={...})
    assert response.status_code == 200

def test_login_wrong_password(client):
    """Test login with incorrect password fails."""
    response = client.post("/api/auth/login", json={...})
    assert response.status_code == 401

def test_login_nonexistent_user(client):
    """Test login with non-existent user fails."""
    response = client.post("/api/auth/login", json={...})
    assert response.status_code == 401
```

**Prevention:**
For every happy path test, write at least 2 error case tests.

---

### Mistake 19: Hardcoding Test Data

**Symptom:**

```python
def test_get_post(client):
    response = client.get("/api/posts/1")  # Post ID 1 might not exist!
```

**Why This Happens:**
Assuming specific IDs or data will exist.

**Fix:**

```python
# ❌ BAD - Hardcoded ID
def test_get_post(client):
    response = client.get("/api/posts/1")  # Brittle!

# ✅ GOOD - Create test data
def test_get_post(client, test_post):
    """Test retrieving a post by ID."""
    response = client.get(f"/api/posts/{test_post.id}")
    assert response.status_code == 200
    assert response.json()["id"] == test_post.id
```

**Prevention:**
Always create or use fixture data. Never assume IDs.

---

## 🔀 Git & Version Control Mistakes

### Mistake 20: Committing Test Database

**Symptom:**
Git shows `test_testbook.db` as modified every test run.

**Why This Happens:**
Test database file not in `.gitignore`.

**Fix:**

```bash
# Check .gitignore includes
*.db
test_*.db
**/*.db

# Remove from git if already tracked
git rm --cached backend/test_testbook.db
```

**Prevention:**
Never commit database files. They're generated by tests.

---

### Mistake 21: Committing Virtual Environment

**Symptom:**
Thousands of files in `venv/` folder show up in git.

**Why This Happens:**
Virtual environment not in `.gitignore`.

**Fix:**

```bash
# Check .gitignore includes
venv/
env/
.venv/

# Remove if already tracked
git rm -r --cached backend/venv/
```

**Prevention:**
Never commit `venv/`. Only commit `requirements.txt`.

---

## 💭 Conceptual Mistakes

### Mistake 22: Thinking Unit Tests Need Database

**Symptom:**

```python
def test_password_hash():
    db = SessionLocal()  # Don't need database!
    hashed = get_password_hash("password")
    assert hashed != "password"
```

**Why This Happens:**
Not understanding what "unit" means.

**Fix:**

```python
# ❌ BAD - Unit test using database
def test_password_hash(db_session):
    hashed = get_password_hash("password")
    # Don't need database for this!

# ✅ GOOD - Pure unit test
def test_password_hash():
    """Test password hashing function in isolation."""
    hashed = get_password_hash("password")
    assert hashed != "password"
    assert hashed.startswith("$2b$")
```

**Prevention:**
Unit tests test one function in isolation. No database, no API, no network.

---

### Mistake 23: Not Understanding Test Pyramid

**Symptom:**
Writing 100 E2E tests, 5 unit tests.

**Why This Happens:**
Not understanding testing strategy.

**Fix:**

```text
         E2E Tests (Few)
      /               \
   Integration Tests (Some)
  /                         \
Unit Tests (Many - Fast, Focused)
```

**Right Balance:**

- 70% Unit tests (fast, test functions)
- 20% Integration tests (test APIs)
- 10% E2E tests (test user flows)

**Prevention:**
Start with unit tests, add integration tests, finish with E2E tests.

---

### Mistake 24: Testing the Framework

**Symptom:**

```python
def test_fastapi_returns_json(client):
    response = client.get("/api/health")
    assert response.headers["content-type"] == "application/json"
```

**Why This Happens:**
Testing that FastAPI works instead of testing your code.

**Fix:**

```python
# ❌ BAD - Testing FastAPI framework
def test_fastapi_returns_json(client):
    assert response.headers["content-type"] == "application/json"

# ✅ GOOD - Testing your logic
def test_health_check_returns_healthy_status(client):
    """Test health endpoint returns correct status."""
    response = client.get("/api/health")
    assert response.json()["status"] == "healthy"
```

**Prevention:**
Don't test the framework. Trust it works. Test YOUR code.

---

## 📚 Quick Troubleshooting Checklist

When tests fail, check:

- [ ] Are you in the correct directory? (`backend/` for pytest, `tests/` for playwright)
- [ ] Is virtual environment activated? (Should see `(venv)` in prompt)
- [ ] Is the app running? (E2E tests need this, backend tests don't)
- [ ] Did you run `./start-dev.sh`? (Not `start.sh`)
- [ ] Are you on the right port? (3000 for frontend, 8000 for API)
- [ ] Did you reset the database? (`./reset-database.sh`)
- [ ] Are all dependencies installed? (`pip install -r requirements.txt`)
- [ ] Did you read the error message carefully?

---

## 💡 Learning from Mistakes

**Remember:** Everyone makes these mistakes! The key is:

1. **Read error messages carefully** - They usually tell you exactly what's wrong
2. **Check this guide** - Your error is probably here
3. **Ask for help** - After trying to fix it yourself
4. **Document your solution** - Help others avoid the same mistake

---

## 📖 Related Resources

- [DEBUGGING_GUIDE.md](../reference/DEBUGGING_GUIDE.md) - How to debug failing tests
- [QUICK_REFERENCE_PYTEST.md](../reference/QUICK_REFERENCE_PYTEST.md) - Pytest commands
- [QUICK_REFERENCE_PLAYWRIGHT.md](../reference/QUICK_REFERENCE_PLAYWRIGHT.md) - Playwright commands
- [docs/guides/RUNNING_TESTS.md](../guides/RUNNING_TESTS.md) - Comprehensive testing guide

---

**🎓 Pro Tip:** Keep this guide open while you work. It'll save you hours of debugging!
