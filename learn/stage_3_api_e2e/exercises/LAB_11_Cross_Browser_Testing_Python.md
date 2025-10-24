# 🧪 Lab 11: Cross-Browser Testing (Python)

**Estimated Time:** 90 minutes<br>
**Difficulty:** Advanced<br>
**Language:** 🐍 Python<br>
**Prerequisites:** Lab 10 completed

**💡 Need JavaScript instead?** Try [Lab 11: Cross-Browser Testing (JavaScript)](LAB_11_Cross_Browser_Testing_JavaScript.md)!

**What This Adds:** Master cross-browser testing to ensure your application works consistently across different browsers and devices. This is essential for production applications.

---

## 🎯 What You'll Learn

- **Trace Viewer** - Debug test failures with visual timeline
- **Codegen** - Generate tests by recording user actions
- **Screenshot/Video** - Visual verification and debugging
- **Network HAR files** - Analyze network requests
- **Parallel execution** - Speed up test runs
- **CI/CD integration** - Run tests in GitHub Actions
- **Visual comparisons** - Detect UI changes
- **Mobile viewport testing** - Test responsive design

---

## 📋 Step-by-Step Instructions

### Part 1: Trace Viewer - The Ultimate Debugging Tool (20 minutes)

**Trace Viewer** shows you exactly what happened during a test run, step by step.

#### Step 1: Enable Tracing

**Create:** `playwright.config.py`

```python
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def playwright_config():
    return {
        "use": {
            # Enable tracing for all tests
            "trace": "on-first-retry",
            # Or enable for specific tests
            # "trace": "retain-on-failure",
        },
        # Retry failed tests once to capture trace
        "retries": 1,
        # Run tests in headed mode for better debugging
        # "headless": False,
    }
```

#### Step 2: Run Tests with Tracing

```bash
# Run a specific test with tracing
pytest tests/e2e-python/test_auth.py -v --headed

# Run with trace on failure
pytest tests/e2e-python/ -v --trace on-first-retry
```

#### Step 3: View Trace Files

```bash
# Open trace viewer
playwright show-trace test-results/trace.zip
```

**What you'll see:**

1. **Timeline** - Every action in chronological order
2. **Screenshots** - Visual state at each step
3. **Network requests** - API calls and responses
4. **Console logs** - JavaScript errors and logs
5. **DOM snapshots** - Page structure at each step

#### Step 4: Debug a Failing Test

**Create:** `tests/e2e-python/test_trace_debug.py`

```python
import pytest
from playwright.sync_api import Page, expect

def test_should_demonstrate_trace_debugging(page: Page):
    """This test will fail and we'll debug it with trace."""
    # This test will fail and we'll debug it with trace
    page.goto("http://localhost:3000")

    # Intentionally cause a failure
    page.click('[data-testid="non-existent-button"]')

    # This will fail and generate a trace
    expect(page.locator('[data-testid="success-message"]')).to_be_visible()
```

**Run and debug:**

```bash
pytest tests/e2e-python/test_trace_debug.py -v --trace on-first-retry
playwright show-trace test-results/trace.zip
```

✅ **Checkpoint:** You can use trace viewer to debug test failures

---

### Part 2: Codegen - Generate Tests by Recording (15 minutes)

**Codegen** records your browser actions and generates test code automatically.

#### Step 1: Start Codegen

```bash
# Start codegen for Testbook
playwright codegen http://localhost:3000 --target python
```

**This opens:**

- Browser window with Testbook
- Codegen panel showing generated code
- Record button to start/stop recording

#### Step 2: Record a Test

1. **Click "Record"** in the codegen panel
2. **Navigate to Testbook** and perform actions:
   - Go to login page
   - Fill in email and password
   - Click login
   - Create a post
   - View profile
3. **Click "Stop"** when done

#### Step 3: Use Generated Code

**The generated code looks like:**

```python
from playwright.sync_api import Page, expect

def test_login_and_create_post(page: Page):
    page.goto("http://localhost:3000/")
    page.get_by_role("link", name="Login").click()
    page.get_by_placeholder("Email").fill("test@test.com")
    page.get_by_placeholder("Password").fill("password")
    page.get_by_role("button", name="Login").click()
    page.get_by_placeholder("What's on your mind?").fill("My first post!")
    page.get_by_role("button", name="Post").click()
    page.get_by_role("link", name="Profile").click()
```

#### Step 4: Customize Generated Code

**Improve the generated code:**

```python
import pytest
from playwright.sync_api import Page, expect

def test_should_login_and_create_post(page: Page):
    """Login and create a post using codegen-generated code."""
    # Go to login page
    page.goto("http://localhost:3000/")
    page.get_by_role("link", name="Login").click()

    # Login
    page.get_by_placeholder("Email").fill("sarah.johnson@testbook.com")
    page.get_by_placeholder("Password").fill("Sarah2024!")
    page.get_by_role("button", name="Login").click()

    # Wait for navigation
    page.wait_for_url("http://localhost:3000/")

    # Create post
    page.get_by_placeholder("What's on your mind?").fill("Generated with codegen!")
    page.get_by_role("button", name="Post").click()

    # Verify post was created
    expect(page.get_by_text("Generated with codegen!")).to_be_visible()

    # View profile
    page.get_by_role("link", name="Profile").click()
    expect(page.get_by_text("sarahjohnson")).to_be_visible()
```

✅ **Checkpoint:** You can generate tests using codegen

---

### Part 3: Screenshots and Videos (15 minutes)

**Visual debugging** helps you see exactly what happened during test execution.

#### Step 1: Configure Screenshots

**Update `pytest.ini`:**

```ini
[tool:pytest]
playwright_config = {
    "use": {
        "screenshot": "only-on-failure",
        "video": "retain-on-failure",
    },
    "expect": {
        "to_have_screenshot": {"threshold": 0.2}
    }
}
```

#### Step 2: Test Screenshot Capture

**Create:** `tests/e2e-python/test_screenshots.py`

```python
import pytest
from playwright.sync_api import Page, expect

def test_should_capture_screenshots_on_failure(page: Page):
    """This test will fail and capture a screenshot."""
    page.goto("http://localhost:3000")

    # This will fail and capture a screenshot
    expect(page.locator('[data-testid="non-existent-element"]')).to_be_visible()

def test_should_take_manual_screenshots(page: Page):
    """Take manual screenshots of specific elements."""
    page.goto("http://localhost:3000")

    # Take screenshot of specific element
    page.locator('[data-testid="navbar"]').screenshot(
        path="test-results/navbar.png"
    )

    # Take full page screenshot
    page.screenshot(
        path="test-results/full-page.png",
        full_page=True
    )
```

#### Step 3: Visual Comparisons

**Test UI consistency:**

```python
def test_should_match_visual_baseline(page: Page):
    """Compare page with visual baseline."""
    page.goto("http://localhost:3000")

    # Compare with baseline image
    expect(page).to_have_screenshot("homepage.png")

    # Compare specific element
    expect(page.locator('[data-testid="navbar"]')).to_have_screenshot(
        "navbar.png"
    )
```

**Run tests:**

```bash
pytest tests/e2e-python/test_screenshots.py -v
```

**View results:**

```bash
# Open test results
playwright show-report
```

✅ **Checkpoint:** You can capture and compare screenshots

---

### Part 4: Network Analysis (15 minutes)

**Analyze network requests** to understand API interactions.

#### Step 1: Capture Network Requests

**Create:** `tests/e2e-python/test_network_analysis.py`

```python
import pytest
from playwright.sync_api import Page, expect

def test_should_analyze_network_requests(page: Page):
    """Analyze network requests during test execution."""
    # Start network recording
    def log_request(route):
        print(f"Request: {route.request.method} {route.request.url}")
        route.continue_()

    page.route("**/*", log_request)

    page.goto("http://localhost:3000")

    # Login to trigger API calls
    page.fill('[data-testid="login-email-input"]', "sarah.johnson@testbook.com")
    page.fill('[data-testid="login-password-input"]', "Sarah2024!")
    page.click('[data-testid="login-submit-button"]')

    # Wait for API calls to complete
    page.wait_for_load_state("networkidle")

    # Create a post to see more API calls
    page.fill('[data-testid="create-post-textarea"]', "Network test post")
    page.click('[data-testid="create-post-submit"]')

    page.wait_for_load_state("networkidle")
```

#### Step 2: Save HAR Files

**Update test to save network data:**

```python
def test_should_save_network_har_file(page: Page):
    """Save network requests to HAR file."""
    # Start HAR recording
    page.route_from_har("test-results/network.har")

    page.goto("http://localhost:3000")

    # Perform actions that make API calls
    page.fill('[data-testid="login-email-input"]', "sarah.johnson@testbook.com")
    page.fill('[data-testid="login-password-input"]', "Sarah2024!")
    page.click('[data-testid="login-submit-button"]')

    page.wait_for_load_state("networkidle")

    # Save HAR file
    page.context.close()
```

#### Step 3: Analyze Network Data

**View HAR files:**

```bash
# Open HAR file in browser
playwright show-trace test-results/network.har
```

**What you can analyze:**

- **Request/Response timing** - Which API calls are slow
- **Payload sizes** - Large responses that might cause issues
- **Error responses** - Failed API calls
- **Request dependencies** - Which calls depend on others

✅ **Checkpoint:** You can analyze network requests and responses

---

### Part 5: Parallel Execution & Performance (10 minutes)

**Speed up test runs** with parallel execution and optimization.

#### Step 1: Configure Parallel Execution

**Update `pytest.ini`:**

```ini
[tool:pytest]
addopts = -n auto  # Use pytest-xdist for parallel execution
playwright_config = {
    "workers": 4,
    "fully_parallel": True,
    "retries": 2,
    "timeout": 30000,
    "expect": {"timeout": 5000}
}
```

**Install pytest-xdist for parallel execution:**

```bash
pip install pytest-xdist
```

#### Step 2: Optimize Test Performance

**Create:** `tests/e2e-python/test_performance.py`

```python
import pytest
from playwright.sync_api import Page, expect

def test_should_run_efficiently_in_parallel(page: Page):
    """Optimized test for parallel execution."""
    # Use faster navigation
    page.goto("http://localhost:3000", wait_until="domcontentloaded")

    # Use specific selectors instead of generic ones
    page.locator('[data-testid="login-email-input"]').fill("test@test.com")

    # Wait for specific elements instead of arbitrary timeouts
    page.wait_for_selector('[data-testid="navbar"]', state="visible")

    # Use expect with timeout instead of wait_for
    expect(page.locator('[data-testid="navbar"]')).to_be_visible(timeout=5000)

def test_should_reuse_browser_context(page: Page):
    """Tests in the same file share browser context."""
    # Tests in the same file share browser context
    # This is faster than creating new context for each test
    page.goto("http://localhost:3000")
    expect(page.locator('[data-testid="login-email-input"]')).to_be_visible()
```

#### Step 3: Run Performance Tests

```bash
# Run with parallel execution
pytest tests/e2e-python/test_performance.py -n auto

# Run with performance report
pytest tests/e2e-python/test_performance.py --html=report.html
```

✅ **Checkpoint:** You can run tests in parallel efficiently

---

### Part 6: CI/CD Integration (15 minutes)

**Run Playwright tests in GitHub Actions** for continuous integration.

#### Step 1: Create GitHub Actions Workflow

**Create:** `.github/workflows/playwright-python.yml`

```yaml
name: Playwright Tests (Python)

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    timeout-minutes: 60
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest-xdist

      - name: Install Playwright Browsers
        run: |
          playwright install --with-deps

      - name: Start Testbook
        run: |
          # Start backend
          cd backend
          python -m venv .venv
          # Linux/Mac
          source .venv/bin/activate
          pip install -r requirements.txt
          uvicorn main:app --host 0.0.0.0 --port 8000 &

          # Windows (PowerShell)
          .venv\Scripts\activate
          pip install -r requirements.txt
          Start-Process -NoNewWindow pwsh -ArgumentList "-Command", "uvicorn main:app --host 0.0.0.0 --port 8000"

          # Start frontend
          cd ../frontend
          npm ci
          npm run build
          npm run preview -- --host 0.0.0.0 --port 3000 &

          # Wait for services to be ready
          sleep 10

      - name: Run Playwright tests
        run: |
          pytest tests/e2e-python/ -v --html=report.html

      - name: Upload test results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report-python
          path: report.html
          retention-days: 30
```

#### Step 2: Configure for CI Environment

**Update `pytest.ini` for CI:**

```ini
[tool:pytest]
addopts = -n auto --html=report.html
playwright_config = {
    "use": {
        "base_url": "http://localhost:3000",
        "headless": true,
        "video": "retain-on-failure",
        "trace": "retain-on-failure",
    },
    "timeout": 60000,
    "retries": 2,
    "workers": 4
}
```

#### Step 3: Test CI Integration

```bash
# Test locally with CI settings
CI=true pytest tests/e2e-python/ -v

# Test with Docker (simulates CI environment)
docker run --rm -it -v $(pwd):/workspace -w /workspace mcr.microsoft.com/playwright:v1.40.0-focal bash
```

✅ **Checkpoint:** You can run Playwright tests in CI/CD

---

## 🎓 What You Learned

- ✅ **Trace Viewer** - Debug test failures with visual timeline
- ✅ **Codegen** - Generate tests by recording user actions
- ✅ **Screenshots/Videos** - Visual debugging and verification
- ✅ **Network Analysis** - Understand API interactions
- ✅ **Parallel Execution** - Speed up test runs
- ✅ **CI/CD Integration** - Run tests in GitHub Actions
- ✅ **Performance Optimization** - Make tests run faster

---

## 💪 Practice Challenges

### Challenge 1: Create a Complete Test Suite

Using all the techniques learned:

1. **Generate tests with codegen** for user registration flow
2. **Add trace debugging** for complex interactions
3. **Implement visual comparisons** for key pages
4. **Set up parallel execution** for speed
5. **Configure CI/CD** for automated testing

### Challenge 2: Debug a Complex Test

1. **Create a failing test** with multiple steps
2. **Use trace viewer** to identify the issue
3. **Fix the test** based on trace analysis
4. **Add screenshots** for visual verification

### Challenge 3: Performance Optimization

1. **Measure current test performance**
2. **Implement parallel execution**
3. **Optimize selectors and waits**
4. **Compare before/after performance**

---

## 🎯 Pro Tips

### Tip 1: Use Trace Viewer for Complex Debugging

```bash
# Always run with trace when debugging
pytest tests/e2e-python/ -v --trace on-first-retry --headed

# View trace files
playwright show-trace test-results/trace.zip
```

### Tip 2: Generate Tests for New Features

```bash
# Start codegen for new feature
playwright codegen http://localhost:3000/new-feature --target python

# Record the complete user flow
# Copy generated code to test file
# Customize and improve the generated code
```

### Tip 3: Optimize for CI/CD

```python
# Use environment variables for CI
import os

is_ci = os.getenv("CI") == "true"

playwright_config = {
    "use": {
        "headless": is_ci,
        "video": "retain-on-failure" if is_ci else "off",
        "trace": "retain-on-failure" if is_ci else "off",
    },
    "retries": 2 if is_ci else 0,
}
```

---

## ✅ Completion Checklist

- [ ] Used trace viewer to debug test failures
- [ ] Generated tests using codegen
- [ ] Captured screenshots and videos
- [ ] Analyzed network requests
- [ ] Configured parallel execution
- [ ] Set up CI/CD integration
- [ ] Optimized test performance

---

## 🎯 Key Takeaways

1. **Trace Viewer is your best friend** - Use it for debugging complex failures
2. **Codegen speeds up test creation** - Record first, then customize
3. **Visual debugging is powerful** - Screenshots and videos show what happened
4. **Network analysis reveals issues** - Understand API interactions
5. **Parallel execution saves time** - Run tests faster with multiple workers
6. **CI/CD integration is essential** - Automate testing in your pipeline

---

**Ready for more?**

- **[Playwright Documentation](https://playwright.dev/)** - Official docs
- **[Playwright Best Practices](https://playwright.dev/docs/best-practices)** - Production patterns
- **[GitHub Actions with Playwright](https://playwright.dev/docs/ci)** - CI/CD guide

---

**🎉 Congratulations!** You've mastered Playwright's advanced features and are ready for production E2E testing!

**Next Lab:** [Lab 6: Testing with Rate Limits (Python)](LAB_06_Testing_With_Rate_Limits_Python.md)
