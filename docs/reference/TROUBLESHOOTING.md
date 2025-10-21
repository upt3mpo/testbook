# 🔧 Troubleshooting & Common Mistakes Guide

**Complete reference for fixing errors and avoiding common pitfalls**

This comprehensive guide covers both technical troubleshooting (specific error messages and fixes) and common mistakes students make when learning automation testing.

---

## 📑 Quick Index

### Technical Troubleshooting

- [Python Virtual Environment Errors](#-python-virtual-environment-errors)
- [Node.js & npm Errors](#nodejs--npm-errors)
- [Docker & Permissions Errors](#docker--permissions-errors)
- [Database Issues](#database-issues)
- [Port Conflicts](#port-conflicts)
- [Test Execution Errors](#test-execution-errors)
- [Coverage & Reporting Errors](#coverage--reporting-errors)
- [Playwright Issues](#playwright-issues)
- [Platform-Specific Issues](#platform-specific-issues)

### Common Learning Mistakes

- [Environment Setup Mistakes](#environment-setup-mistakes)
- [Testing Command Mistakes](#testing-command-mistakes)
- [Python/Pytest Mistakes](#pythonpytest-mistakes)
- [Playwright/E2E Mistakes](#playwrighte2e-mistakes)
- [Test Writing Mistakes](#test-writing-mistakes)
- [Git & Version Control Mistakes](#git--version-control-mistakes)
- [Conceptual Mistakes](#conceptual-mistakes)

---

## 🐍 Python Virtual Environment Errors

### Error: `command not found: pytest`

**Full Error:**

```bash
$ pytest
-bash: pytest: command not found
```

**Why:** Virtual environment not activated.

**Fix:**

```bash
cd backend
# See [Quick Commands](QUICK_COMMANDS.md#virtual-environment) for all platforms

# Verify - should see (venv) in prompt:
(venv) $
```

### Error: `ModuleNotFoundError: No module named 'pytest'`

**Full Error:**

```bash
ModuleNotFoundError: No module named 'pytest'
```

**Why:** Dependencies not installed in virtual environment.

**Fix:**

```bash
cd backend
# See [Quick Commands](QUICK_COMMANDS.md#virtual-environment) for activation
pip install -r requirements.txt
```

### Error: Virtual environment not found

**Full Error:**

```bash
$ source .venv/bin/activate
-bash: .venv/bin/activate: No such file or directory
```

**Why:** Virtual environment not created.

**Fix:**

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# OR
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

---

## 📦 Node.js & npm Errors

### Error: `npm: command not found`

**Full Error:**

```bash
$ npm install
-bash: npm: command not found
```

**Why:** Node.js not installed.

**Fix:**

```bash
# Install Node.js from https://nodejs.org/
# Then verify:
node --version
npm --version
```

### Error: `npm ERR! peer dep missing`

**Full Error:**

```bash
npm ERR! peer dep missing: react@^18.0.0, required by @testing-library/react@13.4.0
```

**Why:** Peer dependency version mismatch.

**Fix:**

```bash
# Install missing peer dependency
npm install react@^18.0.0

# Or use --legacy-peer-deps (not recommended)
npm install --legacy-peer-deps
```

### Error: `npm ERR! ENOENT: no such file or directory`

**Full Error:**

```bash
npm ERR! ENOENT: no such file or directory, open 'package.json'
```

**Why:** Not in correct directory.

**Fix:**

```bash
# Make sure you're in the right directory
cd frontend  # or tests/
ls package.json  # Should exist
npm install
```

---

## 🐳 Docker & Permissions Errors

### Error: `permission denied while trying to connect`

**Full Error:**

```bash
docker: Got permission denied while trying to connect to the Docker daemon socket
```

**Why:** User not in docker group (Linux) or Docker Desktop not running.

**Fix:**

```bash
# Linux - add user to docker group
sudo usermod -aG docker $USER
# Log out and back in

# macOS/Windows - start Docker Desktop
```

### Error: `docker-compose: command not found`

**Full Error:**

```bash
$ docker-compose up
-bash: docker-compose: command not found
```

**Why:** Docker Compose not installed.

**Fix:**

```bash
# Install Docker Compose
# Or use newer syntax:
docker compose up  # No hyphen
```

---

## 🗄️ Database Issues

### Error: `database is locked`

**Full Error:**

```bash
sqlite3.OperationalError: database is locked
```

**Why:** Another process using the database or file permissions.

**Fix:**

```bash
# Kill any running processes
pkill -f uvicorn
pkill -f python

# Check file permissions
ls -la backend/testbook.db

# Reset database if needed
cd backend
rm testbook.db
python seed.py
```

### Error: `no such table: users`

**Full Error:**

```bash
sqlite3.OperationalError: no such table: users
```

**Why:** Database not initialized or seeded.

**Fix:**

```bash
cd backend
python seed.py  # Creates tables and seed data
```

---

## 🔌 Port Conflicts

### Error: `Address already in use`

**Full Error:**

```bash
OSError: [Errno 48] Address already in use
```

**Why:** Port 8000 or 3000 already occupied.

**Fix:**

```bash
# Find what's using the port
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill the process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows

# Or use different ports
uvicorn main:app --port 8001
```

---

## 🧪 Test Execution Errors

### Error: `pytest: command not found`

**Fix:**

```bash
cd backend
source .venv/bin/activate
pip install pytest
```

### Error: `ImportError: No module named 'backend'`

**Fix:**

```bash
# Run from project root, not backend directory
cd ..  # Go to testbook root
pytest backend/tests/
```

### Error: `Failed: No tests found`

**Fix:**

```bash
# Make sure you're in the right directory
cd backend
pytest tests/  # Not test/
```

---

## 📊 Coverage & Reporting Errors

### Error: `No source for code`

**Full Error:**

```bash
Coverage.py warning: No source for code: '/path/to/file.py'
```

**Why:** Coverage trying to analyze files outside project.

**Fix:**

```bash
# Run from correct directory
cd backend
pytest --cov=. --cov-report=html
```

### Error: `Coverage data not found`

**Fix:**

```bash
# Generate coverage first
pytest --cov=. --cov-report=html

# Then view report
open htmlcov/index.html  # macOS
# Or open the file in browser
```

---

## 🎭 Playwright Issues

### Error: `Browser not found`

**Full Error:**

```bash
Error: Browser not found
```

**Why:** Playwright browsers not installed.

**Fix:**

```bash
# Install browsers
npx playwright install

# Or install specific browser
npx playwright install chromium
```

### Error: `Target page, context or browser has been closed`

**Why:** Browser closed unexpectedly during test.

**Fix:**

```bash
# Check for browser crashes
npx playwright test --headed  # Run with visible browser

# Update Playwright
npm update @playwright/test
npx playwright install
```

### Error: `Timeout waiting for selector`

**Fix:**

```bash
# Increase timeout in test
await page.waitForSelector('selector', { timeout: 10000 })

# Or use proper waits
await page.waitForLoadState('networkidle')
```

---

## 💻 Platform-Specific Issues

### Windows: PowerShell Execution Policy

**Error:**

```bash
cannot be loaded because running scripts is disabled on this system
```

**Fix:**

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Windows: Path Length Limits

**Error:**

```bash
Filename too long
```

**Fix:**

```bash
# Enable long path support
git config core.longpaths true
```

### macOS: Permission Denied

**Error:**

```bash
Permission denied: /usr/local/bin/npm
```

**Fix:**

```bash
# Use nvm instead of system Node.js
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install node
```

---

## 🔧 Environment Setup Mistakes

### Mistake 1: Not Activating Virtual Environment

**Symptom:**

```bash
$ pytest
-bash: pytest: command not found
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
```

### Mistake 2: Installing Packages Globally

**Symptom:**

```bash
# Works on your machine but not others
ModuleNotFoundError: No module named 'pytest'
```

**Why This Happens:**
You installed packages globally instead of in the project's virtual environment.

**Fix:**

```bash
# Always activate virtual environment first
cd backend
source .venv/bin/activate

# Then install packages
pip install -r requirements.txt
```

### Mistake 3: Wrong Directory

**Symptom:**

```bash
# From project root
$ pytest
FAILED - No tests found

# From backend directory
$ pytest
ImportError: No module named 'backend'
```

**Why This Happens:**
Running commands from the wrong directory.

**Fix:**

```bash
# For backend tests
cd backend
source .venv/bin/activate
pytest

# For frontend tests
cd frontend
npm test

# For E2E tests
cd tests
npx playwright test
```

---

## 🧪 Testing Command Mistakes

### Mistake 1: Running All Tests When You Want One

**Symptom:**

```bash
# Takes 5 minutes when you want quick feedback
pytest  # Runs all 180+ tests
```

**Fix:**

```bash
# Run specific test file
pytest tests/unit/test_auth.py

# Run specific test
pytest tests/unit/test_auth.py::test_login_success

# Run tests matching pattern
pytest -k "login"
```

### Mistake 2: Not Using Verbose Output

**Symptom:**

```bash
# Hard to see what's happening
pytest tests/integration/test_posts.py
```

**Fix:**

```bash
# Use verbose output
pytest -v tests/integration/test_posts.py

# Or extra verbose
pytest -vv tests/integration/test_posts.py
```

### Mistake 3: Ignoring Failed Tests

**Symptom:**

```bash
# Tests fail but you keep coding
FAILED tests/unit/test_auth.py::test_password_hash
```

**Fix:**

```bash
# Fix failing tests first
pytest --lf  # Run last failed tests only
```

---

## 🐍 Python/Pytest Mistakes

### Mistake 1: Not Using Fixtures

**Bad:**

```python
def test_create_user():
    # Setup user data every time
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "TestPassword123!"
    }
    # Test code...
```

**Good:**

```python
@pytest.fixture
def user_data():
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "TestPassword123!"
    }

def test_create_user(user_data):
    # Test code...
```

### Mistake 2: Hardcoding Test Data

**Bad:**

```python
def test_user_login():
    response = client.post("/auth/login", json={
        "email": "john@example.com",  # Hardcoded
        "password": "password123"     # Hardcoded
    })
```

**Good:**

```python
def test_user_login(client, test_user):
    response = client.post("/auth/login", json={
        "email": test_user.email,     # Dynamic
        "password": "TestPassword123!" # From fixture
    })
```

### Mistake 3: Not Testing Edge Cases

**Bad:**

```python
def test_create_post():
    # Only tests happy path
    response = client.post("/posts", json={"content": "Hello"})
    assert response.status_code == 201
```

**Good:**

```python
def test_create_post_success(client, auth_headers):
    response = client.post("/posts", json={"content": "Hello"})
    assert response.status_code == 201

def test_create_post_empty_content(client, auth_headers):
    response = client.post("/posts", json={"content": ""})
    assert response.status_code == 422

def test_create_post_too_long(client, auth_headers):
    response = client.post("/posts", json={"content": "x" * 501})
    assert response.status_code == 422
```

---

## 🎭 Playwright/E2E Mistakes

### Mistake 1: Using Hard Waits

**Bad:**

```javascript
await page.waitForTimeout(3000); // Always waits 3 seconds
```

**Good:**

```javascript
await page.waitForSelector('[data-testid="post-content"]'); // Waits until element appears
```

### Mistake 2: Not Using Data Test IDs

**Bad:**

```javascript
await page.click(".btn.btn-primary"); // Fragile CSS selector
```

**Good:**

```javascript
await page.click('[data-testid="submit-button"]'); // Stable test ID
```

### Mistake 3: Not Waiting for Network

**Bad:**

```javascript
await page.click("button");
await expect(page.locator("text=Success")).toBeVisible(); // Might fail
```

**Good:**

```javascript
await page.click("button");
await page.waitForResponse((response) => response.url().includes("/api/posts"));
await expect(page.locator("text=Success")).toBeVisible(); // Reliable
```

---

## ✍️ Test Writing Mistakes

### Mistake 1: Testing Implementation, Not Behavior

**Bad:**

```python
def test_hash_password():
    # Testing implementation details
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw("password", salt)
    assert len(salt) == 29  # Implementation detail
```

**Good:**

```python
def test_hash_password():
    # Testing behavior
    password = "TestPassword123!"
    hashed1 = hash_password(password)
    hashed2 = hash_password(password)

    assert hashed1 != hashed2  # Different salts
    assert verify_password(password, hashed1)  # Can verify
    assert not verify_password("wrong", hashed1)  # Wrong password fails
```

### Mistake 2: One Test, Multiple Assertions

**Bad:**

```python
def test_user_registration():
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201
    assert "token" in response.json()
    assert response.json()["user"]["email"] == user_data["email"]
    assert response.json()["user"]["username"] == user_data["username"]
    # If first assertion fails, you don't know about the others
```

**Good:**

```python
def test_user_registration_success():
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201

def test_user_registration_returns_token():
    response = client.post("/auth/register", json=user_data)
    assert "token" in response.json()

def test_user_registration_returns_user_data():
    response = client.post("/auth/register", json=user_data)
    user_data = response.json()["user"]
    assert user_data["email"] == user_data["email"]
    assert user_data["username"] == user_data["username"]
```

### Mistake 3: Not Cleaning Up Test Data

**Bad:**

```python
def test_create_post():
    # Creates post but doesn't clean up
    response = client.post("/posts", json={"content": "Test"})
    assert response.status_code == 201
    # Post remains in database, affects other tests
```

**Good:**

```python
@pytest.fixture(autouse=True)
def cleanup_posts(db_session):
    yield
    # Clean up after test
    db_session.query(Post).delete()
    db_session.commit()

def test_create_post():
    response = client.post("/posts", json={"content": "Test"})
    assert response.status_code == 201
```

---

## 🔄 Git & Version Control Mistakes

### Mistake 1: Committing Test Failures

**Bad:**

```bash
# Committing when tests are failing
$ pytest
FAILED tests/unit/test_auth.py::test_login
$ git add .
$ git commit -m "Add new feature"
```

**Good:**

```bash
# Fix tests first
$ pytest
FAILED tests/unit/test_auth.py::test_login
# Fix the test
$ pytest
PASSED
$ git add .
$ git commit -m "Add new feature with passing tests"
```

### Mistake 2: Not Using .gitignore

**Bad:**

```bash
# Committing generated files
$ git add backend/htmlcov/
$ git add backend/.pytest_cache/
$ git add frontend/node_modules/
```

**Good:**

```bash
# Add to .gitignore
echo "htmlcov/" >> .gitignore
echo ".pytest_cache/" >> .gitignore
echo "node_modules/" >> .gitignore
```

### Mistake 3: Large Commit Messages

**Bad:**

```bash
git commit -m "fix"
git commit -m "update"
git commit -m "stuff"
```

**Good:**

```bash
git commit -m "Fix flaky E2E test by adding proper wait for API response"
git commit -m "Add unit tests for password validation edge cases"
git commit -m "Update README with new installation instructions"
```

---

## 🧠 Conceptual Mistakes

### Mistake 1: Testing Everything with E2E

**Bad:**

```javascript
// Using E2E for simple unit test
test("should hash password", async ({ page }) => {
  await page.goto("/register");
  await page.fill('[name="password"]', "TestPassword123!");
  // ... complex setup just to test password hashing
});
```

**Good:**

```python
# Unit test for password hashing
def test_hash_password():
    password = "TestPassword123!"
    hashed = hash_password(password)
    assert verify_password(password, hashed)
```

### Mistake 2: Ignoring Test Coverage

**Bad:**

```bash
# Not checking what you're actually testing
pytest  # Runs tests but doesn't show coverage
```

**Good:**

```bash
# Check coverage to see what's missing
pytest --cov=. --cov-report=html
open htmlcov/index.html  # See coverage report
```

### Mistake 3: Writing Tests After Code

**Bad:**

```python
# Write feature first
def create_user(email, password):
    # Implementation
    pass

# Then write tests (if you remember)
def test_create_user():
    # Test
    pass
```

**Good:**

```python
# Write test first (TDD)
def test_create_user():
    user = create_user("test@example.com", "password")
    assert user.email == "test@example.com"

# Then write implementation
def create_user(email, password):
    # Implementation to make test pass
    pass
```

---

## 💡 Quick Tips

### When You're Stuck

1. **Check the error message carefully** - It usually tells you exactly what's wrong
2. **Verify your environment** - Virtual environment activated? Right directory?
3. **Read the documentation** - Most tools have excellent docs
4. **Ask for help** - Post the exact error message and what you tried

### Prevention

1. **Always activate virtual environment** before running Python commands
2. **Run tests frequently** - Don't let failures accumulate
3. **Use descriptive test names** - Makes debugging easier
4. **Keep tests simple** - One concept per test
5. **Clean up after tests** - Use fixtures for setup/teardown

---

## 📚 Related Resources

- [Testing Guide](../guides/TESTING_GUIDE.md) - Comprehensive testing examples
- [Testing Patterns](TESTING_PATTERNS.md) - Advanced testing techniques
- [Debugging Guide](DEBUGGING_GUIDE.md) - Debugging strategies
- [README.md](../../README.md#frequently-asked-questions) - Learning-related questions

---

**Remember:** Every error is a learning opportunity! The key is to understand why it happened and how to prevent it in the future. 🚀
