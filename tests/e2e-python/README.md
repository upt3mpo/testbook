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

# Run specific test file
pytest test_auth.py -v

# Run specific test
pytest test_auth.py::TestAuthentication::test_login_success -v
```

**Run in headed mode (see browser):**

**macOS/Linux:**

```bash
HEADLESS=false pytest -v
```

**Windows (PowerShell - Recommended):**

```powershell
$env:HEADLESS="false"; pytest -v
```

**Run in slow motion:**

**macOS/Linux:**

```bash
HEADLESS=false SLOW_MO=1000 pytest -v
```

**Windows (PowerShell - Recommended):**

```powershell
$env:HEADLESS="false"; $env:SLOW_MO="1000"; pytest -v
```

---

## 📁 Directory Structure

```text
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

**macOS/Linux:**

```bash
# Headed mode with slow motion
HEADLESS=false SLOW_MO=1000 pytest -v

# Custom timeouts
DEFAULT_TIMEOUT=60000 pytest -v


# Record videos on failure
VIDEO_ON_FAILURE=true pytest -v
```

**Windows (PowerShell - Recommended):**

```powershell
# Headed mode with slow motion
$env:HEADLESS="false"; $env:SLOW_MO="1000"; pytest -v

# Custom timeouts
$env:DEFAULT_TIMEOUT="60000"; pytest -v


# Record videos on failure
$env:VIDEO_ON_FAILURE="true"; pytest -v
```

**Windows (Command Prompt - Alternative):**

```bat
# Headed mode with slow motion (run separately)
set HEADLESS=false
set SLOW_MO=1000
pytest -v
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

## 🐍 Python-Specific Tests

### Example Tests (`examples/` directory)

**Why Python-only?**

- Demonstrates advanced testing patterns for educational purposes (Lab 4B)
- Showcases Python's OOP capabilities (Page Object Model)
- Shows hybrid API + UI testing (Python's strength for full-stack testing)
- Designed for learning, not production coverage

**What's included:**

#### 1. API + UI Combined Testing (`test_api_ui_combined_example.py`)

- **Pattern:** Fast API setup, then UI verification
- **Example:** Create posts via API (fast), verify they appear in UI
- **Why useful:** Faster test execution, demonstrates hybrid approach

#### 2. Page Object Model (`test_page_objects_example.py`)

- **Pattern:** Encapsulate page interactions in reusable classes
- **Example:** `FeedPage`, `ProfilePage` classes with methods like `create_post()`, `follow_user()`
- **Why useful:** Maintainable tests, reduced duplication

**Career Value:**

- Page Object Model is the industry-standard pattern for E2E tests
- Shows understanding of OOP design patterns
- Demonstrates ability to create maintainable test frameworks

**Interview Talking Points:**
> "For Testbook, I created a Page Object Model framework in Python to encapsulate page interactions. This reduced test duplication by 60% and made tests easier to maintain when the UI changed. I also implemented hybrid API+UI testing to speed up test execution by setting up data via API instead of clicking through the UI."

---

**Getting Started:**

- [Lab 4: E2E Testing Python](../../labs/LAB_04_E2E_Testing_Python.md) - Beginner lab
- [Test Alignment Guide](../E2E_TEST_ALIGNMENT.md) - JS vs Python differences

**Documentation:**

- [Playwright Python Docs](https://playwright.dev/python/)

**CI/CD:**

- [CI/CD for E2E Testing](../../docs/course/CI_CD_E2E_TESTING.md) - Automate these tests

---

**🎉 Happy testing with Playwright Python!**
