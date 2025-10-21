# 🧪 Running Tests - Complete Guide

Comprehensive cross-platform guide for running all Testbook tests.

**✅ 166 Backend Tests | 60+ E2E Tests | All Verified Working**

---

## 🖥️ Platform-Specific Quick Start

### macOS / Linux

```bash
cd backend && source .venv/bin/activate && pytest -v
```

### Windows

```bat
cd backend
.venv\Scripts\activate
pytest -v
```

**Expected:** 166 tests pass in ~51 seconds ✅

---

## 📚 Test Categories

### Backend Tests (Python/pytest)

- **166 tests** (unit, integration, database)
- **84% coverage**
- **Platform:** All (Python is cross-platform)
- **Language:** Python

### E2E Tests (Playwright)

- **60+ tests** (browser automation)
- **Cross-browser** (Chrome, Firefox, Safari)
- **Platform:** All
- **Language:** JavaScript or Python (your choice!)

> **Before you run E2E tests:** start the development servers with `./start-dev.sh` (macOS/Linux) or `start-dev.bat` (Windows). The UI will be available at `http://localhost:3000` and the API at `http://localhost:8000`.

### API Tests

- **Tools:** Postman/Newman (all platforms) or Python requests
- **Language:** Agnostic (HTTP calls)

### Performance Tests (K6)

- **3 scripts** (smoke, load, stress)
- **Platform:** All (K6 is cross-platform)

### Security Tests

- **23 tests**
- **Platform:** All
- **Language:** Python

---

## 📚 Table of Contents

1. [Backend Tests (Python/pytest)](#backend-tests)
2. [E2E Tests (Playwright)](#e2e-tests)
3. [API Tests (Postman/Newman)](#api-tests)
4. [Performance Tests (K6)](#performance-tests)
5. [Security Tests](#security-tests)
6. [CI/CD](#cicd-integration)
7. [Coverage Reports](#test-coverage)

---

## Backend Tests

### Setup

```bash
cd backend

# Activate virtual environment
# See [Quick Commands](docs/reference/QUICK_COMMANDS.md#virtual-environment) for all platforms

# Install dependencies (if not already installed)
pip install -r requirements.txt
```

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v
# See [Quick Commands](docs/reference/QUICK_COMMANDS.md) for all pytest options

# Run specific test directory
pytest tests/unit/
pytest tests/integration/

# Run specific test file
pytest tests/unit/test_auth.py

# Run specific test
pytest tests/unit/test_auth.py::TestPasswordHashing::test_password_is_hashed

# Run by marker
pytest -m unit              # Only unit tests
pytest -m integration       # Only integration tests
pytest -m api               # Only API tests
pytest -m database          # Only database tests

# Run excluding slow tests
pytest -m "not slow"

# Run in parallel (faster)
pytest -n auto
```

### With Coverage

```bash
# Run with coverage report
pytest --cov

# Generate HTML coverage report
pytest --cov --cov-report=html
# See [Quick Commands](docs/reference/QUICK_COMMANDS.md) for all coverage options

# View HTML report
open htmlcov/index.html  # macOS
start htmlcov/index.html # Windows
```

### Test Organization

- `tests/unit/` - Unit tests (fast, isolated)
  - `test_auth.py` - Password hashing, JWT tokens
  - `test_models.py` - Database models, relationships
- `tests/integration/` - Integration tests (API endpoints and database)
  - `test_api_auth.py` - Authentication endpoints
  - `test_api_posts.py` - Posts endpoints
  - `test_api_users.py` - Users endpoints
  - `test_api_feed.py` - Feed endpoints
  - `test_api_contract.py` - API contract validation
  - `test_database.py` - Database constraints
- `tests/conftest.py` - Shared fixtures
- `tests/factories.py` - Test data factories

**Documentation:** [backend/tests/README.md](../../backend/tests/README.md)

---

## E2E Tests

### Setup

```bash
cd tests

# Install dependencies
npm install

# Install browsers (first time only)
npx playwright install chromium  # Chrome only for faster setup
```

### Running Tests

```bash
# Run all E2E tests
npm test

# Run in headed mode (see browser)
npm run test:headed

# Run in UI mode (interactive)
npm run test:ui

# Run in debug mode
npm run test:debug

# Run specific browser
npm run test:chromium
npm run test:firefox
npm run test:webkit

# Run mobile tests
npm run test:mobile

# Run specific test file
npx playwright test auth.spec.js

# Run tests matching pattern
npx playwright test --grep "login"
```

### Viewing Results

```bash
# Open HTML report
npm run report

# Reports include:
# - Screenshots (on failure)
# - Videos (on failure)
# - Traces (on retry)
```

### Test Files

- `e2e/auth.spec.js` - Authentication flows
- `e2e/posts.spec.js` - Post operations
- `e2e/users.spec.js` - User profiles and interactions

**Documentation:** [tests/README.md](../../tests/README.md)

---

## API Tests

### Postman/Newman

#### Setup

```bash
# Install Newman (CLI)
npm install -g newman newman-reporter-htmlextra

# Or use Postman GUI
# Download from https://www.postman.com/downloads/
```

#### Running Tests

```bash
# Run with Newman (CLI)
newman run tests/api/Testbook.postman_collection.json

# Run with HTML report
newman run tests/api/Testbook.postman_collection.json \
  --reporters cli,htmlextra \
  --reporter-htmlextra-export newman-report.html

# Run specific folder
newman run tests/api/Testbook.postman_collection.json \
  --folder "Authentication"
```

#### Using Postman GUI

1. Open Postman
2. Click "Import"
3. Select `tests/api/Testbook.postman_collection.json`
4. Run collection with "Runner"

### Python API Examples

```bash
# Install dependencies
pip install requests

# Run all examples
python tests/api/python_api_examples.py

# Use as library
python
>>> from tests.api.python_api_examples import TestbookAPI
>>> api = TestbookAPI()
>>> api.login("sarah.johnson@testbook.com", "Sarah2024!")
>>> posts = api.get_all_feed()
```

**Documentation:** [tests/api/README.md](../../tests/api/README.md)

---

## Performance Tests

### Setup

```bash
# Install K6

# macOS
brew install k6

# Ubuntu/Debian
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 \
  --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
echo "deb https://dl.k6.io/deb stable main" | \
  sudo tee /etc/apt/sources.list.d/k6.list
sudo apt-get update
sudo apt-get install k6

# Windows
choco install k6
```

### Running Tests

```bash
# Smoke test (minimal load)
k6 run tests/performance/smoke-test.js

# Load test (sustained load)
k6 run tests/performance/load-test.js

# Stress test (breaking point)
k6 run tests/performance/stress-test.js

# Custom configuration
k6 run --vus 50 --duration 10m tests/performance/load-test.js

# Save results
k6 run --out json=results.json tests/performance/load-test.js
```

### Understanding Results

```text
✓ health check returns 200
✓ login successful
✓ feed loads successfully

http_req_duration.........: avg=245ms  p(95)=456ms  p(99)=678ms
http_req_failed...........: 0.23%
```

- `p(95)` = 95% of requests faster than this
- `p(99)` = 99% of requests faster than this
- Low error rate = good performance

**Documentation:** [tests/performance/README.md](../../tests/performance/README.md)

---

## Security Tests

### ⚠️ IMPORTANT: Security Tests & Rate Limiting

**These tests may fail if run without TESTING mode!**

Why? Rate limiting is implemented (good for security!) but tests compete for the rate limit budget.

**Solution:** Run backend in TESTING mode (relaxed rate limits for testing):

```bash
# Start backend in TESTING mode
cd backend
TESTING=true uvicorn main:app --reload --port 8000

# In another terminal, run security tests
pytest tests/security/ -v

# Or use the test runner (handles this automatically)
cd ..
./run-all-tests.sh
```

### Running Tests

```bash
# Recommended: Start backend in TESTING mode first
cd backend
TESTING=true uvicorn main:app --reload

# Then run security tests
cd ..
pytest tests/security/ -v

# Run specific test class
pytest tests/security/test_security.py::TestAuthentication -v

# Run just rate limiting tests
pytest tests/security/test_rate_limiting.py -v
```

### Understanding Test Results

**Expected:** 17-19/23 tests passing (74-83%) ✅

**If you see failures:**

1. Check if backend is in TESTING mode
2. See `tests/security/README.md` for troubleshooting
3. Read `learn/stage_4_performance_security/exercises/LAB_06_Testing_With_Rate_Limits.md` for complete explanation

**The "failures" often prove security is working!**

### What's Tested

- ✅ Authentication enforcement
- ✅ Authorization checks
- ✅ Input validation
- ✅ SQL injection protection
- ✅ XSS handling
- ✅ Data exposure prevention
- ✅ Session management

**Documentation:** [tests/security/README.md](../../tests/security/README.md)

---

## CI/CD Integration

All tests run automatically in GitHub Actions:

### Workflows

1. **Backend Tests** - `.github/workflows/backend-tests.yml`

   - Unit, integration, and database tests
   - Coverage reporting
   - Multiple Python versions

2. **E2E Tests** - `.github/workflows/e2e-tests.yml`

   - Playwright tests
   - Multiple browsers
   - Mobile testing

3. **API Tests** - `.github/workflows/api-tests.yml`

   - Newman/Postman tests
   - Python API examples

4. **Performance Tests** - `.github/workflows/performance-tests.yml`
   - K6 load tests
   - Weekly schedule

### Viewing Results

- Go to GitHub repository
- Click "Actions" tab
- Select workflow run
- Download artifacts (coverage reports, test results)

---

## Test Coverage

### Backend Coverage

```bash
cd backend

# Generate coverage report
pytest --cov --cov-report=html --cov-report=term

# View HTML report
open htmlcov/index.html  # macOS
start htmlcov/index.html # Windows

# Check coverage threshold
pytest --cov --cov-fail-under=70
```

### Coverage Goals

- **Unit Tests**: 80%+ coverage
- **Integration Tests**: All endpoints covered
- **Overall**: 70%+ coverage

### Coverage Reports in CI

Coverage reports automatically uploaded to:

- GitHub Actions artifacts
- Codecov (if configured)

---

## Test Data Management

### Resetting Database

**Easy Way (Scripts):**

```bash
# macOS/Linux
./reset-database.sh

# Windows
reset-database.bat
```

**Via API:**

```bash
curl -X POST http://localhost:8000/api/dev/reset
```

**In Tests:**

```python
# Python
import requests
requests.post('http://localhost:8000/api/dev/reset')
```

```javascript
// JavaScript/Playwright
await page.request.post("http://localhost:8000/api/dev/reset");
```

### Test Accounts

All tests use these pre-seeded accounts:

| Email                        | Password        | Use Case            |
| ---------------------------- | --------------- | ------------------- |
| <sarah.johnson@testbook.com> | Sarah2024!      | Primary test user   |
| <mike.chen@testbook.com>     | MikeRocks88     | Secondary test user |
| <emma.davis@testbook.com>    | EmmaLovesPhotos | Photographer user   |
| <newuser@testbook.com>       | NewUser123!     | Clean account       |

---

## Troubleshooting

### Backend Tests Failing

```bash
# Check if backend dependencies are installed
cd backend
pip list

# Reinstall dependencies
pip install -r requirements.txt

# Delete test database
rm test_testbook.db

# Run single test to debug
pytest tests/unit/test_auth.py::test_password_is_hashed -v
```

### E2E Tests Failing

```bash
# Check if backend is running
curl http://localhost:8000/api/health

# Reinstall Playwright browsers
cd tests
npx playwright install chromium --with-deps  # Chrome only for faster setup

# Run in headed mode to see what's happening
npm run test:headed

# Run single test
npx playwright test auth.spec.js --headed --debug
```

### API Tests Failing

```bash
# Check backend is running
curl http://localhost:8000/api/health

# Reset database
curl -X POST http://localhost:8000/api/dev/reset

# Run Newman in verbose mode
newman run tests/api/Testbook.postman_collection.json --verbose
```

### Performance Tests Failing

```bash
# Check K6 is installed
k6 version

# Check backend is running and responsive
curl http://localhost:8000/api/health

# Start with smoke test first
k6 run tests/performance/smoke-test.js

# Check backend logs for errors
cd backend
uvicorn main:app --reload --log-level debug
```

---

## Best Practices

### Before Running Tests

1. ✅ Make sure backend is running
2. ✅ Reset database to clean state
3. ✅ Check all dependencies installed
4. ✅ Check no port conflicts

### During Development

1. ✅ Run relevant tests frequently
2. ✅ Use `--verbose` to see detailed output
3. ✅ Fix failing tests immediately
4. ✅ Add tests for new features

### Before Committing

1. ✅ Run all test suites
2. ✅ Check test coverage
3. ✅ Verify CI/CD will pass
4. ✅ Update tests if needed

---

## Running All Tests (Full Suite)

```bash
# Terminal 1: Start backend
cd backend
source .venv/bin/activate
python seed.py
uvicorn main:app --reload

# Terminal 2: Backend tests
cd backend
pytest -v --cov

# Terminal 3: E2E tests
cd tests
npm test

# Terminal 4: API tests
newman run tests/api/Testbook.postman_collection.json

# Terminal 5: Performance tests
k6 run tests/performance/smoke-test.js

# Terminal 6: Security tests
pytest tests/security/ -v
```

**Estimated time:** 10-15 minutes for complete test suite

---

## Learning Resources

### Testing Guides

- [Backend Testing Guide](TESTING_GUIDE.md#backend-testing)
- [API Testing Guide](../../tests/api/README.md)
- [E2E Testing Guide](../../tests/README.md)
- [Performance Testing Guide](../../tests/performance/README.md)
- [Security Testing Guide](../../tests/security/README.md)

### Quick References

- [Testing Cheat Sheet](../reference/TESTING_CHEATSHEET.md)
- [Testing Patterns](../reference/TESTING_PATTERNS.md)
- [Testing Features](../reference/TESTING_FEATURES.md)

### External Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Playwright Documentation](https://playwright.dev/)
- [K6 Documentation](https://k6.io/docs/)
- [Postman Learning](https://learning.postman.com/)

---

## Getting Help

1. Check this guide first
2. Review relevant README in test directory
3. Check existing test examples
4. Review test output and error messages
5. Check GitHub Issues

---

**Happy Testing! 🚀**
