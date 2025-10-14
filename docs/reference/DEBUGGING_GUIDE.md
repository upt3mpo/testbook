# 🐛 Debugging Guide

**How to debug failing tests like a professional**

---

## 🎯 Quick Navigation

1. [Reading Error Messages](#reading-error-messages)
2. [Debugging Pytest Tests](#debugging-pytest-tests)
3. [Debugging Playwright Tests](#debugging-playwright-tests)
4. [Common Error Patterns](#common-error-patterns)
5. [Advanced Debugging Techniques](#advanced-debugging-techniques)

---

## 📖 Reading Error Messages

### Anatomy of a Pytest Error

```python
================================ FAILURES =================================
_______________ TestLogin::test_login_wrong_password ______________

client = <fastapi.testclient.TestClient object at 0x7f8b9c>

    def test_login_wrong_password(client):
        """Test login with wrong password fails."""
        response = client.post(
            "/api/auth/login",
            json={"email": "test@test.com", "password": "wrong"}
        )
>       assert response.status_code == 401
E       AssertionError: assert 500 == 401
E        +  where 500 = <Response [500]>.status_code

tests/integration/test_api_auth.py:45: AssertionError
```

**How to Read This:**

1. **Test Name**: `TestLogin::test_login_wrong_password` - Which test failed
2. **Location**: `tests/integration/test_api_auth.py:45` - Exact line that failed
3. **Expected**: `401` - What you expected
4. **Actual**: `500` - What you got
5. **Context**: Shows the code that failed with `>` marker

**What to Do:**

- 500 error means server error, not 401 (unauthorized)
- Check backend logs for the actual error
- Server might be crashing on wrong password

---

### Anatomy of a Playwright Error

```javascript
Error: Timeout 30000ms exceeded.
Call log:
  - waiting for selector "[data-testid="login-button"]"

    at tests/e2e/auth.spec.js:15:3
```

**How to Read This:**

1. **Error Type**: Timeout - Element never appeared
2. **Selector**: `[data-testid="login-button"]` - What it couldn't find
3. **Location**: `auth.spec.js:15` - Where the test is
4. **Timeout**: 30000ms - How long it waited

**What to Do:**

- Element might not exist (typo in data-testid?)
- Element might be created but hidden
- Page might not have loaded
- Check the screenshot (if enabled)

---

## 🐍 Debugging Pytest Tests

### Method 1: Print Statements

**Simple but effective:**

```python
def test_something(client):
    response = client.post("/api/auth/login", json={...})

    # Print to see what you got
    print(f"Status: {response.status_code}")
    print(f"Body: {response.json()}")
    print(f"Headers: {response.headers}")

    assert response.status_code == 200
```

**Run with `-s` to see prints:**

```bash
pytest tests/integration/test_api_auth.py::test_something -v -s
```

---

### Method 2: Using `--pdb` (Debugger)

**Drop into interactive debugger when test fails:**

```bash
pytest tests/integration/test_api_auth.py::test_something --pdb
```

**When test fails, you get:**

```python
> /path/to/test_api_auth.py(45)test_something()
-> assert response.status_code == 200
(Pdb)
```

**Commands in debugger:**

```python
(Pdb) print(response.status_code)  # See variable value
500

(Pdb) print(response.json())  # See response body
{'detail': 'Internal Server Error'}

(Pdb) p response.headers  # 'p' is shorthand for print
Headers({...})

(Pdb) list  # Show code around current line
 40    def test_something(client):
 41        response = client.post(...)
 42  ->    assert response.status_code == 200
 43
 44    def test_other():

(Pdb) up  # Go up one stack frame
(Pdb) down  # Go down one stack frame

(Pdb) continue  # Continue to next failure (or end)
(Pdb) quit  # Exit debugger
```

---

### Method 3: Using `breakpoint()`

**Add debugger anywhere in your test:**

```python
def test_something(client):
    response = client.post("/api/auth/login", json={...})

    # Pause here
    breakpoint()

    # Now you can inspect everything:
    # - Type: response.status_code
    # - Type: response.json()
    # - Type: continue (to keep going)

    assert response.status_code == 200
```

**Run normally:**

```bash
pytest tests/integration/test_api_auth.py::test_something -v
```

---

### Method 4: Show Local Variables

**See all variables when test fails:**

```bash
pytest tests/integration/test_api_auth.py::test_something -v -l
```

**Output shows:**

```python
    def test_something(client):
>       assert response.status_code == 200
E       AssertionError: assert 500 == 200

response   = <Response [500]>
client     = <TestClient object at 0x...>
```

---

### Method 5: Stop on First Failure

**Don't run all tests if one fails:**

```bash
pytest -x  # Stop on first failure
pytest -v -x --pdb  # Stop and debug first failure
```

---

### Method 6: Run Specific Test

**Focus on one failing test:**

```bash
# Run just one test
pytest tests/integration/test_api_auth.py::TestLogin::test_login_wrong_password -v

# Even more specific with -k
pytest -k "login and wrong" -v
```

---

## 🎭 Debugging Playwright Tests

### Method 1: Headed Mode

**See the browser:**

```bash
npx playwright test --headed
```

**What you'll see:**

- Browser opens and you watch test run
- Can see what's happening visually
- Helps identify timing issues

---

### Method 2: Debug Mode

**Step through test line by line:**

```bash
npx playwright test auth.spec.js --debug
```

**What happens:**

- Playwright Inspector opens
- Browser opens
- Test pauses at start
- Use buttons to step through:
  - ▶️ Resume
  - ⏭️ Step over
  - ⏯️ Pause
  - ⏹️ Stop

**In the inspector:**

- See current line highlighted
- See DOM on right side
- Can click elements to inspect
- Can type selectors to test them

---

### Method 3: Using `page.pause()`

**Add breakpoint in test:**

```javascript
test('debug login', async ({ page }) => {
  await page.goto('http://localhost:3000');

  await page.fill('[data-testid="login-email-input"]', 'test@test.com');

  // Pause here - inspector opens
  await page.pause();

  await page.fill('[data-testid="login-password-input"]', 'password');
  await page.click('[data-testid="login-submit-button"]');
});
```

---

### Method 4: Screenshots

**Take screenshot at specific point:**

```javascript
test('debug login', async ({ page }) => {
  await page.goto('http://localhost:3000');

  // Screenshot before
  await page.screenshot({ path: 'before-login.png' });

  await page.fill('[data-testid="login-email-input"]', 'test@test.com');
  await page.fill('[data-testid="login-password-input"]', 'password');

  // Screenshot after
  await page.screenshot({ path: 'after-fill.png' });

  await page.click('[data-testid="login-submit-button"]');

  // Screenshot result
  await page.screenshot({ path: 'after-click.png' });
});
```

**View screenshots:**

```bash
ls *.png
open before-login.png  # macOS
start before-login.png  # Windows
```

---

### Method 5: Console Logs

**See what's happening:**

```javascript
test('debug login', async ({ page }) => {
  // Log page URL
  console.log('Current URL:', page.url());

  // Log element text
  const text = await page.locator('h1').textContent();
  console.log('Page title:', text);

  // Log element count
  const count = await page.locator('button').count();
  console.log('Number of buttons:', count);

  // Log if element exists
  const exists = await page.locator('[data-testid="navbar"]').count() > 0;
  console.log('Navbar exists:', exists);
});
```

---

### Method 6: Trace Viewer

**Record full test execution:**

```javascript
// In playwright.config.js
use: {
  trace: 'on',  // or 'retain-on-failure'
}
```

**View trace:**

```bash
npx playwright show-trace trace.zip
```

**Shows:**

- Every action
- Screenshots at each step
- Network requests
- Console logs
- Timing information

---

## 🔍 Common Error Patterns

### Error Pattern 1: Element Not Found

**Error:**

```
Error: Timeout waiting for selector "[data-testid="button"]"
```

**Debugging Steps:**

1. **Check if selector is correct:**

```javascript
// Print all data-testid attributes
await page.evaluate(() => {
  const elements = document.querySelectorAll('[data-testid]');
  elements.forEach(el => console.log(el.getAttribute('data-testid')));
});
```

2. **Check if element exists at all:**

```javascript
const count = await page.locator('[data-testid="button"]').count();
console.log('Found elements:', count);
```

3. **Check page HTML:**

```javascript
const html = await page.content();
console.log(html);  // See all HTML
```

4. **Take screenshot:**

```javascript
await page.screenshot({ path: 'debug.png', fullPage: true });
```

---

### Error Pattern 2: Test Works Alone, Fails Together

**Error:**
Tests pass individually but fail when run together.

**Debugging Steps:**

1. **Check for test data pollution:**

```python
# Add to conftest.py or beforeEach
def test_something(db_session):
    # Verify database is clean
    user_count = db_session.query(User).count()
    print(f"Users at start: {user_count}")

    # Your test
    ...
```

2. **Run tests in isolation:**

```bash
# Run just one
pytest tests/integration/test_api_auth.py::test_login -v

# Run in order
pytest tests/integration/test_api_auth.py -v
```

3. **Check for shared state:**

- Global variables
- Database not reset
- Files not cleaned up

**Fix:**

```python
@pytest.fixture(autouse=True)
def reset_state(db_session):
    """Reset state before each test."""
    # Clean up database
    db_session.query(User).delete()
    db_session.query(Post).delete()
    db_session.commit()
    yield
    # Clean up after
```

---

### Error Pattern 3: Import Errors

**Error:**

```
ModuleNotFoundError: No module named 'pytest'
```

**Debugging Steps:**

1. **Check if in venv:**

```bash
which python  # Should show path with venv
echo $VIRTUAL_ENV  # Should show venv path
```

2. **Activate venv:**

```bash
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate  # Windows
```

3. **Reinstall dependencies:**

```bash
pip install -r requirements.txt
```

4. **Check Python path:**

```python
import sys
print(sys.path)  # Should include venv
```

---

### Error Pattern 4: Async/Await Issues (Playwright)

**Error:**

```
TypeError: Cannot read property 'click' of undefined
```

**Usually caused by missing `await`:**

```javascript
// ❌ BAD - Missing await
test('bug', async ({ page }) => {
  page.goto('http://localhost:3000');  // Missing await!
  await page.click('button');  // Clicks before page loads
});

// ✅ GOOD - All awaits present
test('fixed', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await page.click('button');
});
```

**Debugging:**

- Check every page. method has `await`
- Use TypeScript to catch missing awaits

---

## 🔬 Advanced Debugging Techniques

### Technique 1: Binary Search

**When many tests fail:**

1. Comment out half the tests
2. Run remaining half
3. If they pass, problem is in commented half
4. Repeat until you find the problematic test

```python
# def test_1(): pass
# def test_2(): pass
def test_3(): pass  # Uncomment these
def test_4(): pass  # Uncomment these
# def test_5(): pass
# def test_6(): pass
```

---

### Technique 2: Logging

**Add detailed logging:**

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_something(client):
    logger.debug("Starting test")
    response = client.post(...)
    logger.debug(f"Got response: {response.status_code}")
    logger.debug(f"Response body: {response.json()}")
    assert response.status_code == 200
```

---

### Technique 3: Minimal Reproduction

**Create minimal test that shows the problem:**

```python
def test_minimal_repro(client):
    """Minimal test showing the bug."""
    # Simplest possible test that fails
    response = client.get("/api/health")
    print(response.json())
    assert response.status_code == 200
```

---

### Technique 4: Compare Working vs Broken

**Find what changed:**

```bash
# Run working test
pytest tests/test_working.py -v

# Run broken test
pytest tests/test_broken.py -v

# Compare what's different:
# - Different fixtures?
# - Different setup?
# - Different data?
```

---

## 📝 Debugging Checklist

When a test fails, check:

- [ ] Read the error message carefully
- [ ] Note which line failed
- [ ] Check what was expected vs actual
- [ ] Run test in isolation
- [ ] Add print statements
- [ ] Run with debugger (`--pdb` or `--debug`)
- [ ] Take screenshots (Playwright)
- [ ] Check backend logs (for E2E tests)
- [ ] Verify test data setup
- [ ] Check if app is running (E2E tests)
- [ ] Check if database is clean
- [ ] Try running in headed mode (Playwright)
- [ ] Verify selector is correct (Playwright)

---

## 💡 Pro Tips

1. **Start simple** - Add prints before using debugger
2. **Run one test** - Focus on the failing test
3. **Read carefully** - Error messages usually tell you exactly what's wrong
4. **Check the obvious** - Is app running? Is venv activated?
5. **Binary search** - When many tests fail, find the first failure
6. **Take breaks** - Fresh eyes see problems faster
7. **Ask for help** - After you've tried debugging yourself

---

## 📚 Related Resources

- [COMMON_MISTAKES.md](../course/COMMON_MISTAKES.md) - Common errors and fixes
- [QUICK_REFERENCE_PYTEST.md](QUICK_REFERENCE_PYTEST.md) - Pytest commands
- [QUICK_REFERENCE_PLAYWRIGHT.md](QUICK_REFERENCE_PLAYWRIGHT.md) - Playwright commands
- [Python Debugger (pdb) Docs](https://docs.python.org/3/library/pdb.html)
- [Playwright Debugging Guide](https://playwright.dev/docs/debug)

---

**🎯 Remember:** Every bug you fix makes you a better tester!
