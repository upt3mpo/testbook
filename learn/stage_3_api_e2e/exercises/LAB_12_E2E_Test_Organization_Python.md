# 🧪 Lab 12: E2E Test Organization

**Estimated Time:** 90 minutes<br>
**Difficulty:** Intermediate<br>
**Language:** 🐍 Python<br>
**Prerequisites:** Lab 11 completed

**💡 Need JavaScript instead?** Try [Lab 12: E2E Test Organization (JavaScript)](LAB_12_E2E_Test_Organization_JavaScript.md)!

**What This Adds:** Organize E2E tests for maintainability, CI/CD integration, and team collaboration.

---

## 🎯 What You'll Learn

- **Test organization** - Structure tests for maintainability
- **CI/CD integration** - Run E2E tests in pipelines
- **Test data management** - Handle test data in E2E tests
- **Parallel execution** - Run tests efficiently
- **Reporting** - Generate test reports and screenshots
- **Environment management** - Test across different environments

---

## 📋 Why Test Organization Matters

**The Problem:**

- 100+ E2E tests scattered across files
- Tests fail randomly due to flaky setup
- No clear way to run specific test suites
- Hard to debug when tests fail in CI
- Tests take hours to run

**The Solution:**
Organize tests with clear structure, proper data management, and CI/CD integration.

---

## 📋 Step-by-Step Instructions

### Part 1: Test Structure Organization (30 minutes)

#### Step 1: Create Test Directory Structure

Create the following directory structure:

```
tests/e2e/
├── conftest.py                 # Shared fixtures and configuration
├── pytest.ini                 # E2E-specific pytest configuration
├── requirements.txt            # E2E test dependencies
├── pages/                      # Page Object Model classes
│   ├── __init__.py
│   ├── base_page.py
│   ├── login_page.py
│   ├── dashboard_page.py
│   └── post_page.py
├── tests/                      # Test files
│   ├── __init__.py
│   ├── smoke/                  # Critical path tests
│   │   ├── __init__.py
│   │   └── test_critical_flows.py
│   ├── regression/             # Full feature tests
│   │   ├── __init__.py
│   │   ├── test_user_management.py
│   │   ├── test_post_management.py
│   │   └── test_authentication.py
│   └── integration/            # Cross-feature tests
│       ├── __init__.py
│       └── test_user_post_workflow.py
├── data/                       # Test data
│   ├── __init__.py
│   ├── users.json
│   ├── posts.json
│   └── test_config.json
├── utils/                      # Helper utilities
│   ├── __init__.py
│   ├── database_helpers.py
│   ├── api_helpers.py
│   └── screenshot_helpers.py
└── reports/                    # Test reports and artifacts
    ├── html/
    ├── screenshots/
    └── videos/
```

#### Step 2: Create Base Configuration

Create `tests/e2e/conftest.py`:

```python
import pytest
import os
from playwright.sync_api import sync_playwright
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Post
from auth import get_password_hash

# Test configuration
TEST_CONFIG = {
    "base_url": os.getenv("E2E_BASE_URL", "http://localhost:3000"),
    "api_url": os.getenv("E2E_API_URL", "http://localhost:8000"),
    "database_url": os.getenv("E2E_DATABASE_URL", "sqlite:///test_e2e.db"),
    "browser": os.getenv("E2E_BROWSER", "chromium"),
    "headless": os.getenv("E2E_HEADLESS", "true").lower() == "true",
    "slow_mo": int(os.getenv("E2E_SLOW_MO", "0")),
    "timeout": int(os.getenv("E2E_TIMEOUT", "30000"))
}

@pytest.fixture(scope="session")
def browser_context_args():
    """Configure browser context for all tests."""
    return {
        "viewport": {"width": 1280, "height": 720},
        "ignore_https_errors": True,
        "record_video_dir": "tests/e2e/reports/videos/",
        "record_video_size": {"width": 1280, "height": 720}
    }

@pytest.fixture(scope="session")
def playwright_context():
    """Create Playwright context for the test session."""
    with sync_playwright() as p:
        browser = getattr(p, TEST_CONFIG["browser"]).launch(
            headless=TEST_CONFIG["headless"],
            slow_mo=TEST_CONFIG["slow_mo"]
        )
        yield browser
        browser.close()

@pytest.fixture
def browser_page(playwright_context, browser_context_args):
    """Create a new browser page for each test."""
    context = playwright_context.new_context(**browser_context_args)
    page = context.new_page()
    page.set_default_timeout(TEST_CONFIG["timeout"])
    yield page
    context.close()

@pytest.fixture(scope="session")
def test_database():
    """Create test database for E2E tests."""
    engine = create_engine(TEST_CONFIG["database_url"])
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)

    yield SessionLocal

    # Cleanup
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(test_database):
    """Create database session for each test."""
    session = test_database()
    yield session
    session.close()

@pytest.fixture
def test_user(db_session):
    """Create a test user for E2E tests."""
    user = User(
        email="e2e@test.com",
        username="e2euser",
        display_name="E2E Test User",
        hashed_password=get_password_hash("password123"),
        bio="E2E test user"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def test_posts(db_session, test_user):
    """Create test posts for E2E tests."""
    posts = []
    for i in range(3):
        post = Post(
            author_id=test_user.id,
            content=f"E2E test post {i+1}",
            title=f"Test Post {i+1}"
        )
        posts.append(post)
        db_session.add(post)

    db_session.commit()
    for post in posts:
        db_session.refresh(post)

    return posts

@pytest.fixture(autouse=True)
def setup_test_environment(browser_page, test_user, test_posts):
    """Setup test environment before each test."""
    # Navigate to base URL
    browser_page.goto(TEST_CONFIG["base_url"])

    # Wait for page to load
    browser_page.wait_for_load_state("networkidle")

    yield

    # Cleanup after each test
    # Clear any test data that might have been created
    pass
```

#### Step 3: Create Page Object Model

Create `tests/e2e/pages/base_page.py`:

```python
from playwright.sync_api import Page, Locator
from typing import Optional

class BasePage:
    """Base page class with common functionality."""

    def __init__(self, page: Page):
        self.page = page
        self.base_url = "http://localhost:3000"

    def goto(self, path: str = "") -> None:
        """Navigate to a page."""
        url = f"{self.base_url}{path}"
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")

    def wait_for_element(self, selector: str, timeout: int = 30000) -> Locator:
        """Wait for an element to be visible."""
        return self.page.wait_for_selector(selector, timeout=timeout)

    def click_element(self, selector: str) -> None:
        """Click an element."""
        element = self.wait_for_element(selector)
        element.click()

    def fill_input(self, selector: str, value: str) -> None:
        """Fill an input field."""
        element = self.wait_for_element(selector)
        element.fill(value)

    def get_text(self, selector: str) -> str:
        """Get text content of an element."""
        element = self.wait_for_element(selector)
        return element.text_content()

    def is_visible(self, selector: str) -> bool:
        """Check if an element is visible."""
        try:
            element = self.page.wait_for_selector(selector, timeout=5000)
            return element.is_visible()
        except:
            return False

    def take_screenshot(self, name: str) -> None:
        """Take a screenshot."""
        self.page.screenshot(path=f"tests/e2e/reports/screenshots/{name}.png")

    def wait_for_url(self, url_pattern: str, timeout: int = 30000) -> None:
        """Wait for URL to match pattern."""
        self.page.wait_for_url(url_pattern, timeout=timeout)
```

Create `tests/e2e/pages/login_page.py`:

```python
from .base_page import BasePage
from playwright.sync_api import Page

class LoginPage(BasePage):
    """Login page object model."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.email_input = "input[data-testid='login-email-input']"
        self.password_input = "input[data-testid='login-password-input']"
        self.login_button = "button[data-testid='login-submit-button']"
        self.error_message = "[data-testid='login-error-message']"
        self.success_message = "[data-testid='login-success-message']"

    def login(self, email: str, password: str) -> None:
        """Perform login action."""
        self.fill_input(self.email_input, email)
        self.fill_input(self.password_input, password)
        self.click_element(self.login_button)

    def is_login_successful(self) -> bool:
        """Check if login was successful."""
        return self.is_visible(self.success_message)

    def get_error_message(self) -> str:
        """Get login error message."""
        if self.is_visible(self.error_message):
            return self.get_text(self.error_message)
        return ""

    def wait_for_login_success(self) -> None:
        """Wait for login success."""
        self.wait_for_url("**/dashboard")
```

---

### Part 2: Test Data Management (20 minutes)

#### Step 1: Create Test Data Files

Create `tests/e2e/data/users.json`:

```json
{
  "valid_users": [
    {
      "email": "test@example.com",
      "username": "testuser",
      "display_name": "Test User",
      "password": "password123",
      "bio": "Test user bio"
    },
    {
      "email": "admin@example.com",
      "username": "admin",
      "display_name": "Admin User",
      "password": "admin123",
      "bio": "Admin user bio"
    }
  ],
  "invalid_users": [
    {
      "email": "invalid-email",
      "username": "ab",
      "display_name": "",
      "password": "123",
      "expected_errors": [
        "Invalid email format",
        "Username too short",
        "Password too short"
      ]
    }
  ]
}
```

Create `tests/e2e/data/posts.json`:

```json
{
  "valid_posts": [
    {
      "title": "Test Post 1",
      "content": "This is a test post for E2E testing.",
      "tags": ["test", "e2e"]
    },
    {
      "title": "Test Post 2",
      "content": "Another test post with different content.",
      "tags": ["test", "automation"]
    }
  ],
  "invalid_posts": [
    {
      "title": "",
      "content": "Post without title",
      "expected_errors": ["Title is required"]
    },
    {
      "title": "Valid Title",
      "content": "",
      "expected_errors": ["Content is required"]
    }
  ]
}
```

#### Step 2: Create Data Helper Functions

Create `tests/e2e/utils/data_helpers.py`:

```python
import json
import os
from typing import Dict, List, Any

class DataHelper:
    """Helper class for managing test data."""

    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), "..", "data")

    def load_json(self, filename: str) -> Dict[str, Any]:
        """Load JSON data from file."""
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'r') as f:
            return json.load(f)

    def get_valid_users(self) -> List[Dict[str, str]]:
        """Get list of valid test users."""
        return self.load_json("users.json")["valid_users"]

    def get_invalid_users(self) -> List[Dict[str, str]]:
        """Get list of invalid test users."""
        return self.load_json("users.json")["invalid_users"]

    def get_valid_posts(self) -> List[Dict[str, str]]:
        """Get list of valid test posts."""
        return self.load_json("posts.json")["valid_posts"]

    def get_invalid_posts(self) -> List[Dict[str, str]]:
        """Get list of invalid test posts."""
        return self.load_json("posts.json")["invalid_posts"]

    def get_user_by_email(self, email: str) -> Dict[str, str]:
        """Get user data by email."""
        users = self.get_valid_users()
        for user in users:
            if user["email"] == email:
                return user
        raise ValueError(f"User with email {email} not found")

    def get_random_user(self) -> Dict[str, str]:
        """Get a random valid user."""
        import random
        users = self.get_valid_users()
        return random.choice(users)
```

---

### Part 3: Test Organization by Category (20 minutes)

#### Step 1: Create Smoke Tests

Create `tests/e2e/tests/smoke/test_critical_flows.py`:

```python
import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utils.data_helpers import DataHelper

class TestCriticalFlows:
    """Critical path tests that must pass for basic functionality."""

    def test_user_can_login_and_view_dashboard(self, browser_page, test_user):
        """Test that user can login and access dashboard."""
        # Arrange
        login_page = LoginPage(browser_page)
        dashboard_page = DashboardPage(browser_page)

        # Act
        login_page.goto("/login")
        login_page.login(test_user.email, "password123")

        # Assert
        assert login_page.is_login_successful()
        assert dashboard_page.is_dashboard_visible()
        assert dashboard_page.get_welcome_message() == f"Welcome, {test_user.display_name}!"

    def test_user_can_create_post(self, browser_page, test_user):
        """Test that user can create a new post."""
        # Arrange
        login_page = LoginPage(browser_page)
        dashboard_page = DashboardPage(browser_page)
        post_page = PostPage(browser_page)

        # Act
        login_page.goto("/login")
        login_page.login(test_user.email, "password123")
        dashboard_page.click_create_post()
        post_page.create_post("Test Post", "This is a test post content")

        # Assert
        assert post_page.is_post_created()
        assert post_page.get_post_title() == "Test Post"

    def test_user_can_logout(self, browser_page, test_user):
        """Test that user can logout successfully."""
        # Arrange
        login_page = LoginPage(browser_page)
        dashboard_page = DashboardPage(browser_page)

        # Act
        login_page.goto("/login")
        login_page.login(test_user.email, "password123")
        dashboard_page.logout()

        # Assert
        assert login_page.is_visible("input[data-testid='login-email-input']")
        assert browser_page.url.endswith("/login")
```

#### Step 2: Create Regression Tests

Create `tests/e2e/tests/regression/test_user_management.py`:

```python
import pytest
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.dashboard_page import DashboardPage
from utils.data_helpers import DataHelper

class TestUserManagement:
    """Regression tests for user management functionality."""

    def test_user_registration_with_valid_data(self, browser_page):
        """Test user registration with valid data."""
        # Arrange
        register_page = RegisterPage(browser_page)
        data_helper = DataHelper()
        user_data = data_helper.get_random_user()

        # Act
        register_page.goto("/register")
        register_page.register(
            user_data["email"],
            user_data["username"],
            user_data["display_name"],
            user_data["password"]
        )

        # Assert
        assert register_page.is_registration_successful()
        assert register_page.get_success_message() == "Registration successful!"

    def test_user_registration_with_invalid_data(self, browser_page):
        """Test user registration with invalid data."""
        # Arrange
        register_page = RegisterPage(browser_page)
        data_helper = DataHelper()
        invalid_user = data_helper.get_invalid_users()[0]

        # Act
        register_page.goto("/register")
        register_page.register(
            invalid_user["email"],
            invalid_user["username"],
            invalid_user["display_name"],
            invalid_user["password"]
        )

        # Assert
        assert not register_page.is_registration_successful()
        assert register_page.get_error_message() != ""

    def test_user_profile_update(self, browser_page, test_user):
        """Test user can update their profile."""
        # Arrange
        login_page = LoginPage(browser_page)
        profile_page = ProfilePage(browser_page)

        # Act
        login_page.goto("/login")
        login_page.login(test_user.email, "password123")
        profile_page.goto("/profile")
        profile_page.update_profile(
            display_name="Updated Name",
            bio="Updated bio"
        )

        # Assert
        assert profile_page.is_profile_updated()
        assert profile_page.get_display_name() == "Updated Name"
        assert profile_page.get_bio() == "Updated bio"
```

---

### Part 4: CI/CD Integration (20 minutes)

#### Step 1: Create GitHub Actions Workflow

Create `.github/workflows/e2e-tests.yml`:

```yaml
name: E2E Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  e2e-tests:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        browser: [chromium, firefox, webkit]

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install -r tests/e2e/requirements.txt

      - name: Install Playwright browsers
        run: |
          playwright install ${{ matrix.browser }}
          playwright install-deps

      - name: Start backend server
        run: |
          cd backend
          python -m uvicorn main:app --host 0.0.0.0 --port 8000 &
          sleep 10

      - name: Start frontend server
        run: |
          cd frontend
          npm install
          npm run build
          npm start &
          sleep 10

      - name: Run E2E tests
        run: |
          cd backend
          pytest tests/e2e/ -v --browser=${{ matrix.browser }} --html=reports/e2e-report-${{ matrix.browser }}.html

      - name: Upload test results
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: e2e-test-results-${{ matrix.browser }}
          path: |
            backend/tests/e2e/reports/
            backend/reports/
```

#### Step 2: Create Pytest Configuration

Create `tests/e2e/pytest.ini`:

```ini
[tool:pytest]
testpaths = tests/e2e/tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    --strict-markers
    --strict-config
    --html=reports/e2e-report.html
    --self-contained-html
    --screenshot=on
    --video=on
    --video-encoding=vp8
    --video-size=1280x720
    --video-mode=retain-on-failure
    --screenshot-mode=retain-on-failure
    --browser=chromium
    --headed
    --slow-mo=1000
    --timeout=30000
    --maxfail=5
    --tb=short
    --durations=10
markers =
    smoke: Critical path tests
    regression: Full feature tests
    integration: Cross-feature tests
    slow: Tests that take longer to run
    flaky: Tests that are known to be flaky
    skip_ci: Tests to skip in CI environment
```

---

## 💪 Challenge Exercises

### Challenge 1: Create Test Suite Runner

```python
# Create tests/e2e/run_tests.py
import subprocess
import sys
import argparse

def run_test_suite(suite: str, browser: str = "chromium", parallel: bool = False):
    """Run specific test suite."""
    cmd = [
        "pytest",
        f"tests/e2e/tests/{suite}/",
        f"--browser={browser}",
        "--html=reports/e2e-report.html",
        "--self-contained-html"
    ]

    if parallel:
        cmd.extend(["-n", "auto"])

    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)

    return result.returncode == 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run E2E test suites")
    parser.add_argument("--suite", choices=["smoke", "regression", "integration"], required=True)
    parser.add_argument("--browser", default="chromium", choices=["chromium", "firefox", "webkit"])
    parser.add_argument("--parallel", action="store_true", help="Run tests in parallel")

    args = parser.parse_args()

    success = run_test_suite(args.suite, args.browser, args.parallel)
    sys.exit(0 if success else 1)
```

### Challenge 2: Create Test Data Factory

```python
# Create tests/e2e/utils/test_data_factory.py
import random
import string
from typing import Dict, List

class TestDataFactory:
    """Factory for generating test data."""

    @staticmethod
    def generate_user(overrides: Dict = None) -> Dict[str, str]:
        """Generate a random user."""
        user = {
            "email": f"test{random.randint(1000, 9999)}@example.com",
            "username": f"user{random.randint(1000, 9999)}",
            "display_name": f"Test User {random.randint(1000, 9999)}",
            "password": "password123",
            "bio": f"Bio for user {random.randint(1000, 9999)}"
        }

        if overrides:
            user.update(overrides)

        return user

    @staticmethod
    def generate_post(overrides: Dict = None) -> Dict[str, str]:
        """Generate a random post."""
        post = {
            "title": f"Test Post {random.randint(1000, 9999)}",
            "content": f"This is test content {random.randint(1000, 9999)}",
            "tags": random.sample(["test", "automation", "e2e", "playwright"], 2)
        }

        if overrides:
            post.update(overrides)

        return post

    @staticmethod
    def generate_multiple_users(count: int) -> List[Dict[str, str]]:
        """Generate multiple users."""
        return [TestDataFactory.generate_user() for _ in range(count)]
```

---

## ✅ Completion Checklist

- [ ] Can organize E2E tests in a maintainable structure
- [ ] Can use Page Object Model for test organization
- [ ] Can manage test data effectively
- [ ] Can run tests in CI/CD pipelines
- [ ] Can generate test reports and screenshots
- [ ] Can run tests in parallel for efficiency
- [ ] Completed all challenge exercises
- [ ] Understand how to scale E2E testing for teams

---

## 💡 Pro Tips

1. **Start with smoke tests** - Get critical paths working first
2. **Use Page Object Model** - Keep tests maintainable and readable
3. **Organize by feature** - Group related tests together
4. **Use test data factories** - Generate data dynamically
5. **Run in parallel** - Speed up test execution

---

## 📚 Next Steps

**Continue building your skills:**

- **[Lab 13: Load Testing with k6 (JavaScript)](LAB_13_Load_Testing_k6.md)** - Performance testing
- **[Lab 14: Security Testing & OWASP (Python)](LAB_14_Security_Testing_OWASP_Python.md)** - Security testing
- **[Lab 15: Rate Limiting & Production Monitoring (Python)](LAB_15_Rate_Limiting_Production_Python.md)** - Production readiness

---

**🎉 Congratulations!** You now understand how to organize E2E tests for maintainability and team collaboration!

**Next Lab:** [Lab 13: Load Testing with k6 (JavaScript)](LAB_13_Load_Testing_k6.md)
