# 🐍 Playwright E2E Tests (Python)

**End-to-end testing with Playwright Python**

This directory contains E2E tests written in Python using Playwright, mirroring the JavaScript E2E tests in `tests/e2e/`.

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd tests/e2e-python
pip install -r requirements.txt
playwright install chromium
```

### 2. Start Application

```bash
# From project root
./start-dev.sh
```

### 3. Run Tests

```bash
# Run all tests
pytest -v

# Run in headed mode (see browser)
pytest -v --headed

# Run in slow motion
pytest -v --headed --slowmo=1000

# Run specific test file
pytest test_auth.py -v

# Run specific test
pytest test_auth.py::TestAuthentication::test_login_success -v
```

---

## 📁 Directory Structure

```
tests/e2e-python/
├── conftest.py              # Pytest fixtures and configuration
├── pytest.ini               # Pytest settings and markers
├── requirements.txt         # Python dependencies
├── test_auth.py            # Authentication tests
├── test_posts.py           # Post creation/management tests
├── test_users.py           # User profile and follow tests
├── pages/                  # 🆕 Page Object Model
│   ├── __init__.py
│   ├── base_page.py        # Base page class
│   ├── feed_page.py        # Feed page object
│   └── profile_page.py     # Profile page object
└── examples/               # 🆕 Example tests from Lab 4B
    ├── test_page_objects_example.py
    ├── test_api_ui_combined_example.py
    └── README.md
```

---

## 🎯 Test Organization

### Pytest Markers

Tests are organized with markers (see `pytest.ini`):

```bash
# Run smoke tests only (fast)
pytest -m smoke -v

# Run regression tests
pytest -m regression -v

# Run Page Object Model examples
pytest -m pom -v

# Run combined API/UI tests
pytest -m combined -v

# Run everything except slow tests
pytest -m "not slow" -v
```

### Test Types

- **test_auth.py** - Registration, login, logout, protected routes
- **test_posts.py** - Creating, viewing, deleting posts
- **test_users.py** - Following, profiles, user interactions
- **examples/** - 🆕 Advanced pattern examples from Lab 4B

---

## 🆕 Advanced Patterns (Lab 4B)

### Page Object Model

```python
from pages.feed_page import FeedPage

def test_with_page_object(page, login_as):
    login_as("sarah")

    feed = FeedPage(page)
    feed.goto()
    feed.create_post("Using page objects!")

    assert feed.post_count() >= 1
```

### Combined API + UI Testing

```python
import requests

def test_api_setup_ui_verify(page, login_as, api_url):
    # Setup via API (FAST!)
    token = get_token(api_url, "sarah")
    for i in range(10):
        create_post_via_api(api_url, token, f"Post {i}")

    # Verify via UI
    login_as("sarah")
    feed = FeedPage(page)
    feed.goto()
    assert feed.post_count() == 10
```

**Learn these patterns:** [Lab 4B: Advanced E2E Python](../../labs/LAB_04B_Advanced_E2E_Python.md)

---

## 🔧 Configuration

### Environment Variables

Set in `.env` file or command line:

```bash
HEADLESS=true          # Run headless (default: true)
SLOW_MO=0             # Slow motion delay in ms (default: 0)
DEFAULT_TIMEOUT=30000 # Default timeout (default: 30000)
VIDEO_ON_FAILURE=false # Record video on failure
FRONTEND_URL=http://localhost:3000
BACKEND_URL=http://localhost:8000
```

### Run Configuration Examples

```bash
# Headed mode with slow motion
HEADLESS=false SLOW_MO=1000 pytest -v

# Custom timeouts
DEFAULT_TIMEOUT=60000 pytest -v

# Record videos on failure
VIDEO_ON_FAILURE=true pytest -v
```

---

## 🐛 Troubleshooting

**Problem:** `Connection refused`
**Solution:** Make sure backend and frontend are running (`./start-dev.sh`)

**Problem:** `Timeout waiting for element`
**Solution:** Increase timeout or add wait: `page.wait_for_timeout(500)`

**Problem:** `Playwright not found`
**Solution:** Run `playwright install chromium`

**Problem:** Tests fail randomly
**Solution:**
- Use `fresh_database` fixture
- Add explicit waits
- Check for race conditions

---

## 🆚 Compare with JavaScript

**See both implementations side-by-side:**

- JavaScript E2E tests: `tests/e2e/`
- [Testing Comparison Guide](../../docs/guides/TESTING_COMPARISON_PYTHON_JS.md)
- [Section 8: Advanced E2E Patterns](../../docs/course/SECTION_08_ADVANCED_E2E_PATTERNS.md)

**Key difference:** Python uses synchronous syntax while JavaScript uses async/await. The Playwright API is otherwise identical!

---

## 📚 Resources

**Getting Started:**
- [Lab 4: E2E Testing Python](../../labs/LAB_04_E2E_Testing_Python.md) - Beginner lab
- [Lab 4B: Advanced E2E Python](../../labs/LAB_04B_Advanced_E2E_Python.md) - Advanced patterns

**Documentation:**
- [Playwright Python Docs](https://playwright.dev/python/)
- [pytest Documentation](https://docs.pytest.org/)

**CI/CD:**
- [CI/CD for E2E Testing](../../docs/course/CI_CD_E2E_TESTING.md) - Automate these tests

---

**🎉 Happy testing with Playwright Python!**
