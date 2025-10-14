# 🚀 Newman CLI Guide

**Automate Postman collections from the command line**

Newman is the CLI version of Postman - perfect for CI/CD pipelines and automated testing.

---

## 📦 Installation

```bash
# Install globally
npm install -g newman

# Or use npx (no install needed)
npx newman --version
```

---

## 🎯 Basic Usage

### Run the Testbook Collection

```bash
# From project root
newman run tests/api/Testbook.postman_collection.json

# From tests/api directory
cd tests/api
newman run Testbook.postman_collection.json
```

**Expected Output:**

```text
→ Testbook API Tests
  ✓ Health Check
  ✓ Register User
  ✓ Login User
  ✓ Get Current User
  ...

┌─────────────────────────┬─────────────┬────────────┐
│                         │    executed │     failed │
├─────────────────────────┼─────────────┼────────────┤
│              iterations │           1 │          0 │
├─────────────────────────┼─────────────┼────────────┤
│                requests │          15 │          0 │
├─────────────────────────┼─────────────┼────────────┤
│            test-scripts │          30 │          0 │
├─────────────────────────┼─────────────┼────────────┤
│      assertions         │          45 │          0 │
└─────────────────────────┴─────────────┴────────────┘
```

---

## 🔧 Newman Options

### Reporting

```bash
# HTML report
newman run Testbook.postman_collection.json \
  --reporters html \
  --reporter-html-export report.html

# Open report
open report.html  # macOS
start report.html  # Windows

# JSON report (for CI)
newman run Testbook.postman_collection.json \
  --reporters json \
  --reporter-json-export results.json

# Multiple reporters
newman run Testbook.postman_collection.json \
  --reporters cli,html,json \
  --reporter-html-export report.html \
  --reporter-json-export results.json
```

### Environment Variables

```bash
# With environment file
newman run Testbook.postman_collection.json \
  --environment production.postman_environment.json

# Set variables via CLI
newman run Testbook.postman_collection.json \
  --env-var "baseUrl=http://localhost:8000" \
  --env-var "testUser=sarah.johnson@testbook.com"
```

### Iteration & Delays

```bash
# Run collection multiple times
newman run Testbook.postman_collection.json \
  --iteration-count 5

# Add delay between requests (in ms)
newman run Testbook.postman_collection.json \
  --delay-request 1000

# Timeout per request
newman run Testbook.postman_collection.json \
  --timeout-request 30000
```

### Filtering

```bash
# Run specific folder
newman run Testbook.postman_collection.json \
  --folder "Authentication"

# Run in bail mode (stop on first failure)
newman run Testbook.postman_collection.json \
  --bail

# Disable SSL verification (for local dev)
newman run Testbook.postman_collection.json \
  --insecure
```

---

## 🎯 CI/CD Integration

### GitHub Actions Example

```yaml
# .github/workflows/api-tests.yml
name: API Tests

on: [push, pull_request]

jobs:
  api-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Start Testbook
        run: |
          cd backend
          python -m venv .venv
          source .venv/bin/activate
          pip install -r requirements.txt
          uvicorn main:app &
          sleep 10

      - name: Install Newman
        run: npm install -g newman

      - name: Run API Tests
        run: |
          newman run tests/api/Testbook.postman_collection.json \
            --reporters cli,json \
            --reporter-json-export api-results.json

      - name: Upload Results
        uses: actions/upload-artifact@v3
        with:
          name: api-test-results
          path: api-results.json
```

### GitLab CI Example

```yaml
# .gitlab-ci.yml
api-tests:
  image: postman/newman:alpine
  script:
    - newman run tests/api/Testbook.postman_collection.json
      --reporters cli,json
      --reporter-json-export api-results.json
  artifacts:
    reports:
      junit: api-results.json
    paths:
      - api-results.json
```

### Jenkins Example

```groovy
// Jenkinsfile
stage('API Tests') {
    steps {
        sh 'npm install -g newman'
        sh '''
            newman run tests/api/Testbook.postman_collection.json \
                --reporters cli,junit \
                --reporter-junit-export results.xml
        '''
        junit 'results.xml'
    }
}
```

---

## 📊 Interpreting Results

### Success Indicators

```text
✓ All tests passing
✓ 0 failed assertions
✓ Response times < 500ms
✓ No errors
```

### Failure Indicators

```text
✗ Tests failing
✗ Failed assertions > 0
✗ Response times > 2000ms
✗ Errors present
```

### Example Failure Output

```text
✗ Login User
  AssertionError: expected response status to be 200 but got 401

  at assertion:1 in test-script
  inside "Login User" request
```

**What to check:**

1. Is backend running?
2. Are credentials correct?
3. Check request body format
4. Review response for error message

---

## 🔍 Debugging Newman Tests

### View Request Details

```bash
# Verbose output
newman run Testbook.postman_collection.json --verbose

# Shows:
# - Request URL
# - Request headers
# - Request body
# - Response status
# - Response body
```

### Test Specific Folder

```bash
# Test just authentication endpoints
newman run Testbook.postman_collection.json \
  --folder "Authentication" \
  --verbose
```

### Export and Inspect

```bash
# Generate detailed report
newman run Testbook.postman_collection.json \
  --reporters html \
  --reporter-html-export detailed-report.html

# Open in browser to see:
# - Request/response details
# - Test results
# - Timing information
# - Failure details
```

---

## 💡 Best Practices

### 1. Use Environment Variables

```javascript
// In Postman collection
{
  "request": {
    "url": "{{baseUrl}}/api/auth/login",
    "headers": {
      "Authorization": "Bearer {{authToken}}"
    }
  }
}
```

```bash
# Set via CLI
newman run collection.json \
  --env-var "baseUrl=http://localhost:8000"
```

### 2. Chain Requests with Tests

```javascript
// In Postman test script
pm.test("Save token", function() {
    var data = pm.response.json();
    pm.environment.set("authToken", data.access_token);
});

// Next request uses {{authToken}}
```

### 3. Add Assertions in Postman

```javascript
// Verify status code
pm.test("Status is 200", function() {
    pm.response.to.have.status(200);
});

// Verify response structure
pm.test("Has access token", function() {
    var data = pm.response.json();
    pm.expect(data).to.have.property("access_token");
});

// Verify response time
pm.test("Response time < 500ms", function() {
    pm.expect(pm.response.responseTime).to.be.below(500);
});
```

---

## 🚀 Quick Commands

```bash
# Run tests
newman run tests/api/Testbook.postman_collection.json

# Run with HTML report
newman run tests/api/Testbook.postman_collection.json \
  -r html --reporter-html-export report.html

# Run specific folder
newman run tests/api/Testbook.postman_collection.json \
  --folder "Authentication"

# Run with environment
newman run tests/api/Testbook.postman_collection.json \
  -e environment.json

# Verbose output
newman run tests/api/Testbook.postman_collection.json --verbose

# Bail on first failure
newman run tests/api/Testbook.postman_collection.json --bail
```

---

## 📚 Related Resources

- [Postman Collection](Testbook.postman_collection.json) - The collection file
- [Newman Documentation](https://learning.postman.com/docs/running-collections/using-newman-cli/command-line-integration-with-newman/)
- [Python API Examples](python_api_examples.py) - Alternative approach
- [API Testing Guide](../../docs/guides/TESTING_GUIDE.md) - Comprehensive guide

---

**🎯 Pro Tip:** Use Newman in your CI/CD pipeline for automated API testing on every commit!
