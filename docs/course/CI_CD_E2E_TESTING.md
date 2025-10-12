# 🚀 CI/CD for E2E Testing: Python & JavaScript

**Comprehensive guide to automating E2E tests in CI/CD pipelines**

This guide shows how to set up continuous integration for both Playwright Python and Playwright JavaScript tests, along with Vitest component tests and pytest backend tests.

---

## 🎯 What You'll Learn

- ✅ Configure GitHub Actions for both test stacks
- ✅ Set up caching for faster CI runs
- ✅ Capture artifacts (screenshots, videos, reports)
- ✅ Implement retry strategies
- ✅ Run tests in parallel
- ✅ Upload coverage reports
- ✅ Handle test failures gracefully

---

## 📋 Prerequisites

- Tests working locally (Python and/or JavaScript)
- GitHub repository (or GitLab/other CI platform)
- Understanding of YAML configuration

---

## Part 1: GitHub Actions for Python E2E Tests

### Basic Python E2E Workflow

Create `.github/workflows/e2e-python.yml`:

```yaml
name: E2E Tests (Python/Playwright)

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  e2e-python:
    name: Python E2E Tests
    runs-on: ubuntu-latest

    strategy:
      fail-fast: false
      matrix:
        browser: [chromium, firefox]

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install Python dependencies
        run: |
          pip install -r tests/e2e-python/requirements.txt

      - name: Install Playwright browsers
        run: |
          playwright install --with-deps ${{ matrix.browser }}

      - name: Start backend
        run: |
          cd backend
          source venv/bin/activate || python -m venv venv && source venv/bin/activate
          pip install -r requirements.txt
          uvicorn main:app --host 0.0.0.0 --port 8000 &
          sleep 5

      - name: Start frontend
        run: |
          cd frontend
          npm ci
          npm run dev &
          sleep 10
          curl http://localhost:3000 || (echo "Frontend failed to start" && exit 1)

      - name: Run E2E tests
        env:
          BROWSER: ${{ matrix.browser }}
          HEADLESS: true
          BASE_URL: http://localhost:3000
          API_URL: http://localhost:8000
        run: |
          cd tests/e2e-python
          pytest --browser=${{ matrix.browser }} --headed=false -v --tb=short

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: e2e-python-${{ matrix.browser }}-results
          path: |
            tests/e2e-python/test-results/
            tests/e2e-python/screenshots/
          retention-days: 30

      - name: Upload videos on failure
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: e2e-python-${{ matrix.browser }}-videos
          path: tests/e2e-python/test-results/videos/
          retention-days: 30
```

---

## Part 2: GitHub Actions for JavaScript E2E Tests

### Basic JavaScript E2E Workflow

Create `.github/workflows/e2e-javascript.yml`:

```yaml
name: E2E Tests (JavaScript/Playwright)

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  e2e-javascript:
    name: JavaScript E2E Tests
    runs-on: ubuntu-latest

    strategy:
      fail-fast: false
      matrix:
        browser: [chromium, firefox, webkit]
        shard: [1, 2]  # Run in 2 parallel shards

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: |
          cd tests
          npm ci

      - name: Install Playwright browsers
        run: |
          cd tests
          npx playwright install --with-deps ${{ matrix.browser }}

      - name: Start backend
        run: |
          cd backend
          python -m venv venv
          source venv/bin/activate
          pip install -r requirements.txt
          uvicorn main:app --host 0.0.0.0 --port 8000 &
          sleep 5

      - name: Start frontend
        run: |
          cd frontend
          npm ci
          npm run dev &
          sleep 10

      - name: Run E2E tests
        run: |
          cd tests
          npx playwright test --project=${{ matrix.browser }} --shard=${{ matrix.shard }}/${{ strategy.job-total }}

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: e2e-js-${{ matrix.browser }}-shard-${{ matrix.shard }}-results
          path: |
            tests/playwright-report/
            tests/test-results/
          retention-days: 30

      - name: Upload Playwright report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report-${{ matrix.browser }}-${{ matrix.shard }}
          path: tests/playwright-report/
          retention-days: 30
```

---

## Part 3: Component Tests (Vitest)

### Vitest Component Test Workflow

Create `.github/workflows/component-tests.yml`:

```yaml
name: Component Tests (Vitest)

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  component-tests:
    name: React Component Tests
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json

      - name: Install dependencies
        run: |
          cd frontend
          npm ci

      - name: Run component tests
        run: |
          cd frontend
          npm test -- --coverage

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          files: ./frontend/coverage/coverage-final.json
          flags: component-tests
          name: component-coverage

      - name: Upload coverage report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: component-test-coverage
          path: frontend/coverage/
          retention-days: 30
```

---

## Part 4: Backend Tests (pytest)

### Backend Test Workflow

Create `.github/workflows/backend-tests.yml`:

```yaml
name: Backend Tests (pytest)

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  backend-tests:
    name: Backend API Tests
    runs-on: ubuntu-latest

    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: testuser
          POSTGRES_PASSWORD: testpass
          POSTGRES_DB: testdb
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'

      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install pytest-cov

      - name: Run tests with coverage
        env:
          DATABASE_URL: postgresql://testuser:testpass@localhost:5432/testdb
        run: |
          cd backend
          pytest --cov --cov-report=xml --cov-report=html -v

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          files: ./backend/coverage.xml
          flags: backend-tests
          name: backend-coverage-py${{ matrix.python-version }}

      - name: Upload coverage report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: backend-coverage-py${{ matrix.python-version }}
          path: backend/htmlcov/
          retention-days: 30
```

---

## Part 5: Complete Test Suite Workflow

### All-in-One Workflow

Create `.github/workflows/test-suite.yml`:

```yaml
name: Complete Test Suite

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  backend-tests:
    name: Backend Tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          cache: 'pip'
      - run: |
          cd backend
          pip install -r requirements.txt pytest-cov
          pytest --cov --cov-report=xml
      - uses: codecov/codecov-action@v3
        with:
          flags: backend

  component-tests:
    name: Component Tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json
      - run: |
          cd frontend
          npm ci
          npm test -- --coverage
      - uses: codecov/codecov-action@v3
        with:
          flags: component

  e2e-tests:
    name: E2E Tests
    runs-on: ubuntu-latest
    needs: [backend-tests, component-tests]  # Run after unit tests pass

    strategy:
      matrix:
        test-suite: [python, javascript]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'

      - name: Install Playwright
        run: |
          if [ "${{ matrix.test-suite }}" == "python" ]; then
            pip install -r tests/e2e-python/requirements.txt
            playwright install --with-deps chromium
          else
            cd tests && npm ci
            npx playwright install --with-deps chromium
          fi

      - name: Start services
        run: |
          # Start backend
          cd backend
          pip install -r requirements.txt
          uvicorn main:app --port 8000 &

          # Start frontend
          cd ../frontend
          npm ci
          npm run dev &

          # Wait for services
          sleep 15

      - name: Run E2E tests
        run: |
          if [ "${{ matrix.test-suite }}" == "python" ]; then
            cd tests/e2e-python
            pytest -v
          else
            cd tests
            npx playwright test
          fi

      - uses: actions/upload-artifact@v3
        if: always()
        with:
          name: e2e-${{ matrix.test-suite }}-results
          path: tests/**/test-results/

  security-tests:
    name: Security Tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: |
          cd backend
          pip install -r requirements.txt
          uvicorn main:app --port 8000 &
          sleep 5
          cd ../tests/security
          pip install -r requirements.txt
          pytest -v
```

---

## Part 6: Optimization Strategies

### Caching Dependencies

**Python caching:**

```yaml
- uses: actions/setup-python@v4
  with:
    python-version: '3.11'
    cache: 'pip'
    cache-dependency-path: '**/requirements.txt'
```

**Node caching:**

```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '18'
    cache: 'npm'
    cache-dependency-path: '**/package-lock.json'
```

### Caching Playwright Browsers

```yaml
- name: Cache Playwright browsers
  uses: actions/cache@v3
  id: playwright-cache
  with:
    path: ~/.cache/ms-playwright
    key: ${{ runner.os }}-playwright-${{ hashFiles('**/package-lock.json') }}

- name: Install Playwright browsers
  if: steps.playwright-cache.outputs.cache-hit != 'true'
  run: npx playwright install --with-deps
```

### Parallel Test Execution

**Playwright sharding:**

```yaml
strategy:
  matrix:
    shard: [1, 2, 3, 4]

steps:
  - run: npx playwright test --shard=${{ matrix.shard }}/4
```

**pytest-xdist:**

```yaml
- run: pytest -n auto  # Auto-detect CPU count
```

---

## Part 7: Retry Strategies

### Playwright Retry Configuration

**playwright.config.js:**

```javascript
module.exports = {
  retries: process.env.CI ? 2 : 0,  // Retry 2x in CI
  workers: process.env.CI ? 2 : undefined,
};
```

### pytest Retry Configuration

**pytest.ini:**

```ini
[pytest]
addopts = --reruns 2 --reruns-delay 1
```

Install: `pip install pytest-rerun-failures`

---

## Part 8: Handling Test Failures

### Slack Notifications

```yaml
- name: Notify Slack on failure
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    payload: |
      {
        "text": "E2E Tests Failed!",
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "E2E tests failed on ${{ github.ref }}"
            }
          }
        ]
      }
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

### GitHub Pull Request Comments

```yaml
- name: Comment PR with test results
  if: github.event_name == 'pull_request'
  uses: actions/github-script@v6
  with:
    script: |
      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: '✅ All E2E tests passed!'
      })
```

---

## Part 9: Docker-Based CI

### Using Docker Compose in CI

```yaml
jobs:
  e2e-docker:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Start services with Docker Compose
        run: docker-compose up -d

      - name: Wait for services
        run: |
          timeout 60 bash -c 'until curl -f http://localhost:3000; do sleep 2; done'
          timeout 60 bash -c 'until curl -f http://localhost:8000/docs; do sleep 2; done'

      - name: Run E2E tests
        run: |
          docker-compose exec -T backend pytest tests/
          docker-compose exec -T frontend npm test

      - name: Cleanup
        if: always()
        run: docker-compose down -v
```

---

## Part 10: GitLab CI Example

### .gitlab-ci.yml

```yaml
stages:
  - test
  - e2e

backend-tests:
  stage: test
  image: python:3.11
  services:
    - postgres:15
  variables:
    POSTGRES_DB: testdb
    POSTGRES_USER: testuser
    POSTGRES_PASSWORD: testpass
  script:
    - cd backend
    - pip install -r requirements.txt pytest-cov
    - pytest --cov
  coverage: '/TOTAL.*\s+(\d+%)$/'

component-tests:
  stage: test
  image: node:18
  script:
    - cd frontend
    - npm ci
    - npm test -- --coverage
  coverage: '/Lines\s+:\s+(\d+\.\d+)%/'

e2e-python:
  stage: e2e
  image: mcr.microsoft.com/playwright/python:v1.40.0
  script:
    - cd tests/e2e-python
    - pip install -r requirements.txt
    - playwright install
    - pytest -v
  artifacts:
    when: always
    paths:
      - tests/e2e-python/test-results/
    expire_in: 1 week

e2e-javascript:
  stage: e2e
  image: mcr.microsoft.com/playwright:v1.40.0
  script:
    - cd tests
    - npm ci
    - npx playwright test
  artifacts:
    when: always
    paths:
      - tests/playwright-report/
    expire_in: 1 week
```

---

## 🎓 Best Practices Summary

### ✅ Do's

- **Cache dependencies** - Speeds up CI significantly
- **Run unit tests first** - Fail fast strategy
- **Retry flaky tests** - 1-2 retries in CI only
- **Capture artifacts** - Screenshots, videos, reports
- **Upload coverage** - Track coverage trends
- **Use matrix builds** - Test across browsers/versions
- **Parallelize tests** - Reduce CI time
- **Use specific browser versions** - Avoid surprises

### ❌ Don'ts

- **Don't skip tests in CI** - CI should be stricter than local
- **Don't ignore flaky tests** - Fix the root cause
- **Don't run all tests serially** - Use parallel execution
- **Don't use `latest` tags** - Pin versions for consistency
- **Don't store secrets in code** - Use CI secrets
- **Don't run E2E if unit tests fail** - Save CI time

---

## 📊 Monitoring & Metrics

### Key Metrics to Track

1. **Test execution time** - Should stay under 10 minutes
2. **Flake rate** - Should be < 1%
3. **Coverage percentage** - Track trends
4. **Failure rate** - Monitor for patterns
5. **CI queue time** - Optimize if growing

### Tracking with Codecov

```yaml
- uses: codecov/codecov-action@v3
  with:
    files: ./coverage/coverage-final.json
    flags: e2e-tests
    fail_ci_if_error: true
```

---

## 🚀 Next Steps

1. **Implement basic CI** - Start with one workflow
2. **Add caching** - Speed up builds
3. **Add artifacts** - Capture screenshots/videos
4. **Monitor metrics** - Track success rates
5. **Optimize** - Parallel execution, sharding

---

## 📚 Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Playwright CI Guide](https://playwright.dev/docs/ci)
- [pytest CI Integration](https://docs.pytest.org/en/stable/how-to/usage.html#continuous-integration)
- [Codecov Integration](https://docs.codecov.com/docs)

**🎉 Your tests are now running automatically in CI! Professional DevOps achieved!**
