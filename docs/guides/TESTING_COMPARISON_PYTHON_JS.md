# 🔄 Testing Comparison: Python vs JavaScript

**A side-by-side guide for test automation across both stacks**

This guide helps you translate testing knowledge between Python and JavaScript, showing equivalent patterns and tools for common testing scenarios.

---

## 📚 Quick Reference Table

| Concept | Python | JavaScript |
|---------|--------|------------|
| **Test Framework** | pytest | Vitest / Jest |
| **E2E Framework** | Playwright (Python) | Playwright (JS) |
| **Assertions** | `assert` | `expect()` |
| **Mocking** | `pytest.mock` / `unittest.mock` | `vi.mock()` |
| **Fixtures** | `@pytest.fixture` | Playwright fixtures |
| **API Testing** | `requests` | `axios` / `fetch` |
| **Component Testing** | N/A | Vitest + Testing Library |
| **Coverage** | `pytest-cov` | `vitest --coverage` |

---

## 🧪 Test Structure Comparison

### Basic Test

**Python (pytest)**
```python
def test_addition():
    """Test that addition works correctly."""
    result = 2 + 2
    assert result == 4
```

**JavaScript (Vitest)**
```javascript
test('addition works correctly', () => {
  const result = 2 + 2;
  expect(result).toBe(4);
});
```

### Test Classes/Groups

**Python (pytest)**
```python
class TestAuthentication:
    """Group of authentication tests"""

    def test_login_success(self):
        assert login("user", "pass") == True

    def test_login_failure(self):
        assert login("user", "wrong") == False
```

**JavaScript (Vitest)**
```javascript
describe('Authentication', () => {
  test('login succeeds with correct credentials', () => {
    expect(login('user', 'pass')).toBe(true);
  });

  test('login fails with wrong credentials', () => {
    expect(login('user', 'wrong')).toBe(false);
  });
});
```

---

## 🔧 Fixtures & Setup

### Basic Fixture

**Python (pytest)**
```python
@pytest.fixture
def database():
    """Provide a clean database for tests."""
    db = create_database()
    yield db
    db.cleanup()

def test_query(database):
    result = database.query("SELECT * FROM users")
    assert len(result) > 0
```

**JavaScript (Playwright)**
```javascript
const test = base.extend({
  database: async ({}, use) => {
    const db = await createDatabase();
    await use(db);
    await db.cleanup();
  },
});

test('query returns users', async ({ database }) => {
  const result = await database.query('SELECT * FROM users');
  expect(result.length).toBeGreaterThan(0);
});
```

### Parametrized Tests

**Python (pytest)**
```python
@pytest.mark.parametrize("username,valid", [
    ("alice", True),
    ("bob123", True),
    ("a", False),  # too short
    ("user@name", False),  # invalid chars
])
def test_username_validation(username, valid):
    assert is_valid_username(username) == valid
```

**JavaScript (Vitest)**
```javascript
test.each([
  ['alice', true],
  ['bob123', true],
  ['a', false],  // too short
  ['user@name', false],  // invalid chars
])('validates username %s as %s', (username, valid) => {
  expect(isValidUsername(username)).toBe(valid);
});
```

---

## 🌐 E2E Testing with Playwright

### Basic E2E Test

**Python**
```python
from playwright.sync_api import Page, expect

def test_login(page: Page):
    """Test login flow."""
    page.goto("http://localhost:3000")
    page.fill('[data-testid="email"]', "user@test.com")
    page.fill('[data-testid="password"]', "password")
    page.click('[data-testid="submit"]')

    expect(page.locator('[data-testid="navbar"]')).to_be_visible()
```

**JavaScript**
```javascript
const { test, expect } = require('@playwright/test');

test('login flow', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await page.fill('[data-testid="email"]', 'user@test.com');
  await page.fill('[data-testid="password"]', 'password');
  await page.click('[data-testid="submit"]');

  await expect(page.locator('[data-testid="navbar"]')).toBeVisible();
});
```

**Key Difference:** Python uses synchronous syntax while JavaScript uses async/await.

### Page Object Model

**Python**
```python
class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.email_input = '[data-testid="email"]'
        self.password_input = '[data-testid="password"]'
        self.submit_button = '[data-testid="submit"]'

    def login(self, email: str, password: str):
        self.page.fill(self.email_input, email)
        self.page.fill(self.password_input, password)
        self.page.click(self.submit_button)

# Usage
def test_login(page: Page):
    login_page = LoginPage(page)
    login_page.login("user@test.com", "password")
```

**JavaScript**
```javascript
class LoginPage {
  constructor(page) {
    this.page = page;
    this.emailInput = '[data-testid="email"]';
    this.passwordInput = '[data-testid="password"]';
    this.submitButton = '[data-testid="submit"]';
  }

  async login(email, password) {
    await this.page.fill(this.emailInput, email);
    await this.page.fill(this.passwordInput, password);
    await this.page.click(this.submitButton);
  }
}

// Usage
test('login flow', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.login('user@test.com', 'password');
});
```

---

## 🎭 Mocking & Stubbing

### Mocking Functions

**Python**
```python
from unittest.mock import Mock, patch

def test_api_call():
    """Test with mocked API."""
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {'user': 'alice'}

        result = fetch_user(1)
        assert result['user'] == 'alice'
        mock_get.assert_called_once_with('/api/users/1')
```

**JavaScript**
```javascript
import { vi } from 'vitest';

test('API call with mock', async () => {
  const mockFetch = vi.fn().mockResolvedValue({
    json: async () => ({ user: 'alice' }),
  });

  global.fetch = mockFetch;

  const result = await fetchUser(1);
  expect(result.user).toBe('alice');
  expect(mockFetch).toHaveBeenCalledWith('/api/users/1');
});
```

### Network Mocking (Playwright)

**Python**
```python
import json
from playwright.sync_api import Route

def test_mocked_api(page: Page):
    """Test with mocked API response."""
    def handle_route(route: Route):
        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({"posts": []})
        )

    page.route("**/api/feed**", handle_route)
    page.goto("http://localhost:3000")

    # Feed will show empty state
    expect(page.locator("text=/no posts/i")).to_be_visible()
```

**JavaScript**
```javascript
test('mocked API response', async ({ page }) => {
  await page.route('**/api/feed**', route => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ posts: [] }),
    });
  });

  await page.goto('http://localhost:3000');

  // Feed will show empty state
  await expect(page.locator('text=/no posts/i')).toBeVisible();
});
```

---

## 📡 API Testing

### Testing REST Endpoints

**Python**
```python
import requests

def test_get_users():
    """Test GET /api/users endpoint."""
    response = requests.get("http://localhost:8000/api/users")

    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "username" in data[0]

def test_create_post():
    """Test POST /api/posts endpoint."""
    response = requests.post(
        "http://localhost:8000/api/posts",
        json={"content": "Test post"},
        headers={"Authorization": "Bearer token123"}
    )

    assert response.status_code == 200
    assert response.json()["content"] == "Test post"
```

**JavaScript**
```javascript
import axios from 'axios';

test('GET /api/users endpoint', async () => {
  const response = await axios.get('http://localhost:8000/api/users');

  expect(response.status).toBe(200);
  expect(response.data.length).toBeGreaterThan(0);
  expect(response.data[0]).toHaveProperty('username');
});

test('POST /api/posts endpoint', async () => {
  const response = await axios.post(
    'http://localhost:8000/api/posts',
    { content: 'Test post' },
    { headers: { Authorization: 'Bearer token123' } }
  );

  expect(response.status).toBe(200);
  expect(response.data.content).toBe('Test post');
});
```

---

## 🏃 Running Tests

### Command Line

| Task | Python | JavaScript |
|------|--------|------------|
| **Run all tests** | `pytest` | `npm test` |
| **Run specific file** | `pytest test_auth.py` | `npm test auth.test.js` |
| **Run with coverage** | `pytest --cov` | `npm test -- --coverage` |
| **Verbose output** | `pytest -v` | `npm test -- --reporter=verbose` |
| **Watch mode** | `pytest-watch` | `npm test -- --watch` |
| **Run specific test** | `pytest -k "test_name"` | `npm test -- -t "test name"` |

### Pytest Markers vs Vitest Filters

**Python**
```python
@pytest.mark.smoke
def test_critical_path():
    pass

@pytest.mark.slow
def test_full_integration():
    pass

# Run: pytest -m smoke
# Run: pytest -m "not slow"
```

**JavaScript**
```javascript
test('critical path', { tag: '@smoke' }, async () => {
  // test code
});

test('full integration', { tag: '@slow' }, async () => {
  // test code
});

// Run: npm test -- --grep @smoke
// Run: npm test -- --grep @slow --invert
```

---

## 🔍 Assertions Comparison

### Common Assertions

| Check | Python | JavaScript |
|-------|--------|------------|
| **Equality** | `assert x == y` | `expect(x).toBe(y)` |
| **Deep equality** | `assert x == y` | `expect(x).toEqual(y)` |
| **Truthy/Falsy** | `assert x` | `expect(x).toBeTruthy()` |
| **Contains** | `assert x in list` | `expect(list).toContain(x)` |
| **Greater than** | `assert x > y` | `expect(x).toBeGreaterThan(y)` |
| **Type check** | `assert isinstance(x, str)` | `expect(typeof x).toBe('string')` |
| **Exception** | `with pytest.raises(Error):` | `expect(() => fn()).toThrow()` |

### Playwright Assertions

| Check | Python | JavaScript |
|-------|--------|------------|
| **Visible** | `expect(el).to_be_visible()` | `await expect(el).toBeVisible()` |
| **Contains text** | `expect(el).to_contain_text("x")` | `await expect(el).toContainText('x')` |
| **Has attribute** | `expect(el).to_have_attribute("x")` | `await expect(el).toHaveAttribute('x')` |
| **Count** | `expect(els).to_have_count(5)` | `await expect(els).toHaveCount(5)` |

---

## 🗂️ Test Organization

### File Structure

**Python Structure**
```
backend/
  tests/
    conftest.py          # Shared fixtures
    unit/                # Unit tests
      test_auth.py
      test_models.py
    integration/         # Integration tests
      test_api_auth.py
      test_api_users.py
      test_api_posts.py
      test_database.py
tests/
  e2e-python/
    conftest.py
    pages/
      __init__.py
      feed_page.py       # Page objects
    test_auth.py         # E2E tests
    test_posts.py
```

**JavaScript Structure**
```
frontend/
  src/
    components/
      __tests__/
        Button.test.jsx  # Component tests
    test/
      setup.js           # Test setup
      mocks/
        handlers.js      # MSW handlers
tests/
  e2e/
    fixtures/
      test-helpers.js    # Shared helpers
    auth.spec.js         # E2E tests
    posts.spec.js
```

---

## ⚙️ Configuration Files

### Pytest Configuration

**pytest.ini**
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    smoke: Quick smoke tests
    slow: Slow-running tests
addopts = -v --tb=short
```

### Vitest Configuration

**vitest.config.js**
```javascript
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.js',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html'],
    },
  },
});
```

### Playwright Configuration

**Python**: `pytest.ini` (shared with pytest)

**JavaScript**: `playwright.config.js`
```javascript
module.exports = {
  testDir: './e2e',
  timeout: 30000,
  use: {
    baseURL: 'http://localhost:3000',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
};
```

---

## 🚀 CI/CD Integration

### GitHub Actions

**Python Tests**
```yaml
name: Python Tests
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest --cov --cov-report=xml
      - uses: codecov/codecov-action@v3
```

**JavaScript Tests**
```yaml
name: JavaScript Tests
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '18'
      - run: npm ci
      - run: npm test -- --coverage
      - uses: codecov/codecov-action@v3
```

---

## 🎯 When to Use Each Stack

### Choose Python When:
- ✅ Backend is Python (FastAPI, Django, Flask)
- ✅ Team has Python expertise
- ✅ Testing APIs and data processing
- ✅ Scientific/data analysis workflows
- ✅ Prefer synchronous syntax

### Choose JavaScript When:
- ✅ Frontend is React/Vue/Angular
- ✅ Team has JavaScript/TypeScript expertise
- ✅ Testing UI components
- ✅ Full-stack JavaScript (Node.js)
- ✅ Prefer async/await patterns

### Use Both When:
- ✅ Full-stack application (Python backend + React frontend)
- ✅ Python for API tests, JavaScript for component tests
- ✅ Playwright E2E in either language (both work!)
- ✅ Maximum coverage across entire stack

---

## 📚 Learning Path Recommendations

### If You Know Python, Learning JavaScript Testing:
1. Start with Vitest (similar to pytest)
2. Learn async/await syntax
3. Understand component testing with Testing Library
4. Playwright syntax is nearly identical!

### If You Know JavaScript, Learning Python Testing:
1. Start with pytest (similar to Vitest)
2. Learn synchronous syntax (simpler!)
3. Understand FastAPI TestClient for API testing
4. Playwright syntax is nearly identical!

---

## 🔗 Useful Resources

### Python Testing
- [pytest documentation](https://docs.pytest.org/)
- [Playwright Python docs](https://playwright.dev/python/)
- [requests documentation](https://requests.readthedocs.io/)
- [LearnPython.org](https://www.learnpython.org/) - Interactive Python basics

### JavaScript Testing
- [Vitest documentation](https://vitest.dev/)
- [Playwright JavaScript docs](https://playwright.dev/)
- [Testing Library docs](https://testing-library.com/)
- [learn-js.org](https://www.learn-js.org/) - Interactive JavaScript basics (async/await, promises, objects)

### Both
- [Testbook repository](../..) - See working examples in both languages!
- [Compare Lab 4 Python vs JavaScript](../../labs/) - See same lab in both stacks

---

## 💡 Pro Tips

1. **Playwright is identical** - Once you learn Playwright in one language, you know it in both! Only syntax differs (async vs sync).

2. **Translate patterns, not code** - Focus on understanding the pattern (fixtures, mocks, page objects) rather than exact syntax.

3. **Use both where appropriate** - Python for backend/API tests, JavaScript for component tests, either for E2E.

4. **Share test data** - Use the same test users, scenarios, and data across both test suites.

5. **Consistent naming** - Use similar test names and organization in both stacks for easier maintenance.

---

**🎓 Key Takeaway:** The concepts are the same across both stacks! If you understand testing in one language, you can quickly learn the other. Focus on patterns, not syntax.

