# 🚀 Stage 4: Performance & Security

**Non-Functional Testing That Matters**

> **💡 Language Selection**: This guide includes both Python and JavaScript examples. Both are expanded by default so you can see all approaches. Click the language tabs to collapse sections you don't need.

## Your Progress

[████████████████████░░░░] 80% complete

✅ Stage 1: Unit Tests (completed)<br>
✅ Stage 2: Integration Tests (completed)<br>
✅ Stage 3: API & E2E Testing (completed)<br>
→ **Stage 4: Performance & Security** (you are here)<br>
⬜ Stage 5: Capstone

**Estimated time remaining:** 6-8 hours (core content) + 4-6 hours (optional exercises)

## Lab Structure

**Lab 13: Load Testing with k6** - Performance testing fundamentals with k6
**Lab 14: Security Testing with OWASP** - Security testing with OWASP guidelines
**Lab 15: Rate Limiting Testing** - Advanced rate limiting and security patterns

### Lab Progression

1. **Lab 13** - Start with performance testing basics using k6
2. **Lab 14** - Learn security testing with OWASP Top 10
3. **Lab 15** - Master rate limiting and advanced security patterns

### Language Tracks

- **Python Track**: Focus on pytest-based security testing
- **JavaScript Track**: Focus on Playwright and k6 integration
- **Hybrid Track**: Combine both approaches for comprehensive testing

### Prerequisites

- Completed Stage 3: API & E2E Testing
- Understanding of load testing concepts
- Basic knowledge of security testing principles

### Learning Outcomes

By the end of Stage 4, you will:

- Understand performance testing fundamentals and metrics
- Implement load testing with k6
- Test for OWASP Top 10 security vulnerabilities
- Master rate limiting and security patterns
- Be ready for production-level testing challenges

### Quick Start

1. **Choose your track**: Python, JavaScript, or Hybrid
2. **Start with Lab 13**: Load Testing with k6
3. **Progress through labs**: Follow the sequential structure
4. **Complete all exercises**: Ensure comprehensive understanding
5. **Move to Stage 5**: Capstone project

### Lab Details

- **Lab 13**: Load Testing with k6 - Performance testing fundamentals
- **Lab 14**: Security Testing with OWASP - Security testing with OWASP guidelines
- **Lab 15**: Rate Limiting Testing - Advanced rate limiting and security patterns

<h2 id="table-of-contents">📋 Table of Contents</h2>

- [Why Performance & Security Testing Matters: The Foundation of Production Readiness](#why-performance--security-testing-matters-the-foundation-of-production-readiness)
- [Lab Structure](#lab-structure)
- [Part 1: What Are Performance Tests? 📚](#part-1-what-are-performance-tests)
- [Part 2: Load Testing with k6 🚀](#part-2-load-testing-with-k6)
- [Part 3: Security Testing 🔒](#part-3-security-testing)
- [Part 4: Implementation Guide 🛠️](#part-4-implementation-guide)
- [Part 5: Hands-On Practice 🏃](#part-5-hands-on-practice)
- [Part 6: Additional Patterns 🚀](#part-6-additional-patterns)
- [✅ Success Criteria](#success-criteria)
- [🧠 Why This Matters](#why-this-matters)
- [🔗 Related Resources](#related-resources)
- [🧠 Self-Check Quiz (Optional)](#self-check-quiz-optional)
- [🤔 Reflection](#reflection)
- [🎉 Stage Complete](#stage-complete)

---

## Why Performance & Security Testing Matters: The Foundation of Production Readiness

### The Real-World Impact

**The Problem Without Performance Testing:**
In 2020, a major video conferencing platform experienced a 3-hour outage during peak usage. The platform was designed to handle 10 million concurrent users, but when usage spiked to 15 million due to a global event, the system couldn't handle the load. The outage cost the company $50M in lost revenue and damaged their reputation.

**The Problem Without Security Testing:**
In 2017, Equifax experienced a massive data breach that exposed 147 million people's personal information. The breach was caused by a vulnerability in a web application that could have been prevented with proper security testing. The company paid $700M in settlements and lost significant customer trust.

**What Performance & Security Tests Prevent:**

1. **System Failures**: Applications that crash under load
2. **Data Breaches**: Security vulnerabilities that expose user data
3. **Performance Degradation**: Slow response times that frustrate users
4. **Compliance Violations**: Security issues that violate regulations
5. **Business Losses**: Downtime and breaches that cost money and reputation

### The Testing Pyramid Applied

```text
                ▲
               /_\  ← Manual / Exploratory Testing
              /   \
             / E2E \  ← Playwright (JS / Python)
            /_______\
           /         \
          / Component \  ← Vitest + RTL (JS only)
         /_____________\
        /               \
       /  Integration    \  ← API / Component tests
      /___________________\
     /                     \
    /      Unit Tests       \  ← Vitest (JS) | pytest (Python)
   /_________________________\
```

**Performance & Security Tests (Critical for Production):**

- Performance tests: Run in minutes to hours
- Security tests: Run in minutes to hours
- Test non-functional requirements
- Ensure production readiness

**Why These Tests Are Critical:**

- Functional tests ensure features work
- Performance tests ensure features work under load
- Security tests ensure features work safely
- All three are needed for production readiness

### The Business Case

**Real Example - Performance:**
An e-commerce application processes:

- 1,000 orders per minute during normal hours
- 10,000 orders per minute during peak hours
- 100,000 orders per minute during Black Friday

Without performance testing:

- System works with 1,000 orders ✅
- System crashes with 10,000 orders 💥
- Black Friday is a disaster
- Customers can't complete purchases
- Revenue is lost

With performance testing:

- Test system under expected load
- Identify bottlenecks before production
- Scale infrastructure appropriately
- Maintain customer satisfaction

**Real Example - Security:**
A banking application handles:

- User authentication
- Financial transactions
- Personal data storage
- Regulatory compliance

Without security testing:

- Application works functionally ✅
- But has SQL injection vulnerabilities 💥
- Hackers steal customer data
- Regulatory fines are imposed
- Customer trust is lost

With security testing:

- Test for common vulnerabilities
- Ensure data protection
- Maintain regulatory compliance
- Protect customer trust

### The Developer Experience

**Without Performance & Security Testing:**

- "It works on my machine"
- "I don't know why it's slow in production"
- "I don't know why it's not secure"
- "Let me check the logs... there are performance issues"

**With Performance & Security Testing:**

- "I know the system can handle the load"
- "I know the system is secure"
- "I can identify bottlenecks and vulnerabilities"
- "I have confidence in production readiness"

### The Quality Mindset

**Performance & Security Testing Teaches You:**

1. **Think About Scale**: How does the system behave under load?
2. **Think About Security**: What are the attack vectors?
3. **Design for Performance**: Make the system fast and efficient
4. **Design for Security**: Make the system secure by design
5. **Monitor Production**: How do you know if the system is healthy?

### Industry Standards

**Companies That Require Performance & Security Testing:**

- Google: Performance testing for all services
- Microsoft: Security testing for all applications
- Amazon: Performance and security testing for all systems
- Netflix: Performance and security testing for all platforms

**Why They Do This:**

- Prevents system failures
- Protects user data
- Maintains regulatory compliance
- Ensures customer satisfaction
- Builds team confidence

### The Performance & Security Testing Mindset

**Key Questions to Ask:**

1. **What is the expected load?** Normal, peak, and extreme usage
2. **What are the performance requirements?** Response time, throughput, availability
3. **What are the security threats?** OWASP Top 10, industry-specific risks
4. **How do we handle failures?** Graceful degradation, error handling
5. **How do we monitor health?** Performance metrics, security alerts

**Common Performance & Security Patterns:**

- **Load Testing**: Test under expected load
- **Stress Testing**: Test beyond normal capacity
- **Security Scanning**: Test for vulnerabilities
- **Penetration Testing**: Test for attack vectors
- **Compliance Testing**: Test for regulatory requirements

---

<h2 id="part-1-what-are-performance-tests">Part 1: What Are Performance Tests? 📚</h2>

### The Traffic Jam Analogy

Imagine you're testing a highway. Functional tests would be like checking that cars can drive from point A to point B. But performance tests would be like testing what happens when there's a traffic jam - can the highway handle 1000 cars at once? What happens when everyone tries to exit at the same time?

**Performance tests** verify that your application can handle real-world load and stress.

### Why Performance Tests Matter

1. **Real-world conditions**: Test under actual user load
2. **Find bottlenecks**: Identify what breaks under pressure
3. **Plan capacity**: Know how many users you can support
4. **Prevent crashes**: Catch issues before users do
5. **Optimize resources**: Find where to improve performance

### Types of Performance Tests

**1. Smoke Tests** - "Is it working at all?"

- Single user, minimal load
- Basic functionality check
- Quick health check

**2. Load Tests** - "Can it handle normal traffic?"

- Realistic user load
- Sustained traffic simulation
- Normal operating conditions

**3. Stress Tests** - "What's the breaking point?"

- Gradually increasing load
- Find system limits
- Test failure recovery

**4. Spike Tests** - "What happens during traffic spikes?"

- Sudden load increases
- Black Friday scenarios
- Viral content moments

### Performance Metrics You Need to Know

**Response Time:**

- **Average**: Typical response time
- **P95**: 95% of requests faster than this
- **P99**: 99% of requests faster than this

**Throughput:**

- **Requests per second (RPS)**: How many requests handled
- **Transactions per second (TPS)**: Business operations completed

**Error Rate:**

- **Success rate**: Percentage of successful requests
- **Error rate**: Percentage of failed requests

---

<h2 id="part-2-load-testing-with-k6">Part 2: Load Testing with k6 🚀</h2>

### The k6 Tool Explained

k6 is like having a thousand virtual users that can all use your app at the same time. It's written in JavaScript but can test any backend (Python, Node.js, Go, etc.).

### Basic k6 Test Structure

```javascript
import http from "k6/http";
import { check, sleep } from "k6";

// Define load pattern
export let options = {
  stages: [
    { duration: "30s", target: 10 }, // Ramp up to 10 users
    { duration: "1m", target: 10 }, // Stay at 10 users
    { duration: "30s", target: 0 }, // Ramp down to 0 users
  ],
};

// This function runs for each virtual user
export default function () {
  // Make a request
  let response = http.get("http://localhost:8000/posts");

  // Verify the response
  check(response, {
    "status is 200": (r) => r.status === 200,
    "response time < 200ms": (r) => r.timings.duration < 200,
  });

  // Wait 1 second before next request
  sleep(1);
}
```

### Understanding k6 Options

**Stages define load pattern:**

- `duration`: How long this stage lasts
- `target`: How many virtual users during this stage

**Common patterns:**

```javascript
// Gradual ramp-up
stages: [
  { duration: "2m", target: 10 }, // Ramp up to 10 users over 2 minutes
  { duration: "5m", target: 10 }, // Stay at 10 users for 5 minutes
  { duration: "2m", target: 20 }, // Ramp up to 20 users over 2 minutes
  { duration: "5m", target: 20 }, // Stay at 20 users for 5 minutes
  { duration: "2m", target: 0 }, // Ramp down to 0 users over 2 minutes
];

// Spike test
stages: [
  { duration: "1m", target: 10 }, // Normal load
  { duration: "30s", target: 100 }, // Sudden spike
  { duration: "1m", target: 10 }, // Back to normal
  { duration: "30s", target: 0 }, // Ramp down
];
```

### Performance Metrics Interpretation

**k6 output example:**

```text
✓ status is 200.........................: 100.00% ✓ 1200 ✗ 0
✓ response time < 200ms.................: 95.00%  ✓ 1140 ✗ 60

http_req_duration......................: avg=158ms min=45ms max=523ms
http_req_failed........................: 0.00%
http_reqs..............................: 1200
```

**What this means:**

- **100% status 200**: All requests succeeded
- **95% response time < 200ms**: 95% of requests were fast enough
- **avg=158ms**: Average response time was 158 milliseconds
- **0.00% failed**: No requests failed
- **1200 requests**: Total requests made

### Good vs Bad Performance

**Good Performance:**

- Response time < 200ms average
- P95 < 500ms
- Error rate < 1%
- Consistent performance under load

**Bad Performance:**

- Response time > 1000ms average
- P95 > 2000ms
- Error rate > 5%
- Performance degrades under load

---

<h2 id="part-3-security-testing">Part 3: Security Testing 🔒</h2>

### The Security Guard Analogy

Think of security testing like being a security guard at a building. You need to check:

- Can unauthorized people get in?
- Are the locks working properly?
- What happens if someone tries to break in?
- Are there any hidden entrances?

**Security tests** verify that your application is safe from attacks and vulnerabilities.

### Common Security Vulnerabilities

**1. SQL Injection**

- Attackers inject malicious SQL code
- Can steal or delete data
- Test with malicious input

**2. Cross-Site Scripting (XSS)**

- Attackers inject malicious JavaScript
- Can steal user data or hijack sessions
- Test with script tags

**3. Cross-Site Request Forgery (CSRF)**

- Attackers trick users into unwanted actions
- Can perform actions without user consent
- Test with forged requests

**4. Rate Limiting Bypass**

- Attackers overwhelm the system
- Can cause denial of service
- Test with rapid requests

### Security Testing Mindset

**Think like an attacker:**

- What would a hacker try?
- How can I break this system?
- What data can I steal?
- How can I cause damage?

**Test malicious inputs:**

- SQL injection payloads
- XSS scripts
- Command injection
- Path traversal attacks

---

<h2 id="part-4-implementation-guide">Part 4: Implementation Guide 🛠️</h2>

Now let's see these concepts in real code! Choose your track:

### 🚀 Performance Testing with k6

**Open `tests/performance/load-test.js` and find the main test:**

```javascript
/**
 * K6 Load Test for Testbook API
 *
 * This file demonstrates comprehensive performance testing using k6.
 * It tests the system under sustained load to identify performance
 * characteristics, bottlenecks, and system limits.
 *
 * Key Testing Concepts Demonstrated:
 * - Load testing with realistic user scenarios
 * - Performance metrics collection and analysis
 * - Threshold-based pass/fail criteria
 * - Custom metrics for specific operations
 * - CI vs local testing configurations
 * - Error rate monitoring and analysis
 */

import { check, group, sleep } from "k6";
import http from "k6/http";
import { Rate, Trend } from "k6/metrics";

// Custom metrics for detailed performance analysis
// These help us track specific aspects of our application's performance
const errorRate = new Rate("errors"); // Track overall error rate
const loginDuration = new Trend("login_duration"); // Track login performance
const feedDuration = new Trend("feed_duration"); // Track feed loading performance
const postCreationDuration = new Trend("post_creation_duration"); // Track post creation performance

// Test configuration - defines how the load test will run
export const options = {
  stages: [
    // Gradual ramp-up to avoid overwhelming the system
    { duration: "30s", target: 10 }, // Ramp up to 10 users over 30 seconds
    { duration: "1m", target: 10 }, // Stay at 10 users for 1 minute (baseline)
    { duration: "30s", target: 15 }, // Ramp up to 15 users over 30 seconds
    { duration: "2m", target: 15 }, // Stay at 15 users for 2 minutes (stress test)
    { duration: "30s", target: 0 }, // Ramp down to 0 users over 30 seconds
  ],
  thresholds: {
    // Performance thresholds - these define what "good performance" means
    // If any threshold is exceeded, the test will fail
    http_req_duration: ["p(95)<1000", "p(99)<2000"], // 95% of requests < 1s, 99% < 2s
    http_req_failed: ["rate<0.05"], // Error rate must be < 5%
    errors: ["rate<0.05"], // Custom error rate < 5%
    login_duration: ["p(95)<500"], // Login should be fast (95% < 500ms)
    feed_duration: ["p(95)<1000"], // Feed loading performance (95% < 1s)
    post_creation_duration: ["p(95)<600"], // Post creation performance (95% < 600ms)
  },
};
```

**Guided Walkthrough:**

1. **Stages**: We ramp up to 10 users, stay there for 1 minute, then ramp down
2. **Request**: We make a GET request to the posts endpoint
3. **Checks**: We verify the response is successful and fast
4. **Sleep**: We wait 1 second before the next request

**Try This:**

1. **Run the performance test from command line:**

   ```bash
   # Run basic load test
   k6 run tests/performance/load-test.js

   # Run with custom user count
   k6 run tests/performance/load-test.js --vus=20 --duration=2m

   # Run with detailed output
   k6 run tests/performance/load-test.js --verbose
   ```

2. **Interpret performance metrics:**

   ```bash
   # Run and save results to file
   k6 run tests/performance/load-test.js --out=json=results.json

   # Generate HTML report
   k6 run tests/performance/load-test.js --out=json=results.json
   k6 run tests/performance/load-test.js --out=json=results.json --summary-export=summary.json
   ```

3. **Make it fail intentionally to see performance limits:**

   ```javascript
   // Temporarily change this line in the test:
   { duration: "30s", target: 10 }  // Change to: { duration: "30s", target: 100 }
   ```

   Then run the test and see how the system handles high load!

4. **Fix it back and run again to see it pass**

**What you'll learn:**

- How to run performance tests from command line
- How to interpret performance metrics and identify bottlenecks
- How to test system limits and failure points
- The importance of performance monitoring

**More Examples:**

- `smoke-test.js` - Basic health check
- `stress-test.js` - Find breaking point
- Full file: [load-test.js](../../tests/performance/load-test.js)

### 🔒 Security Testing with pytest

**Open `tests/security/test_security.py` and find `test_sql_injection_prevention`:**

<details open>
<summary><strong>🐍 Python</strong></summary>

```python
@pytest.mark.security
def test_sql_injection_prevention(api_client):
    """
    Verify SQL injection attempts are blocked.

    This test demonstrates OWASP Top 10 #1 vulnerability testing.
    SQL injection occurs when malicious SQL code is inserted into
    application inputs, potentially allowing attackers to:
    - Access unauthorized data
    - Modify or delete data
    - Execute administrative operations

    This test verifies that the application properly validates
    and sanitizes user inputs to prevent SQL injection attacks.
    """
    # Arrange: Prepare malicious SQL injection payload
    # This payload would delete the users table if the application is vulnerable
    malicious_input = "'; DROP TABLE users; --"

    # Act: Send registration request with malicious input
    response = api_client.post(f"{BASE_URL}/auth/register", json={
        "username": malicious_input,  # Malicious SQL injection attempt
        "email": "test@test.com",     # Valid email
        "password": "password123"     # Valid password
    })

    # Assert: Verify the application properly handles the malicious input
    # Should be rejected (400) or sanitized (201 but safe)
    # If this returns 200/201, the application is vulnerable to SQL injection
    assert response.status_code in [400, 422], f"Expected rejection, got {response.status_code}"

    # Additional verification: ensure the users table still exists
    # (This would be caught by other tests, but shows the severity)
    # In a real test suite, we might verify the database state here
```

</details>

<details open>
<summary><strong>☕ JavaScript</strong></summary>

```javascript
test("SQL injection prevention", async () => {
  /**
   * Test that the application prevents SQL injection attacks.
   *
   * This test attempts to inject malicious SQL code into the username field
   * during user registration. A secure application should either:
   * 1. Reject the request with a 400/422 error (input validation)
   * 2. Sanitize the input and create the user safely (input sanitization)
   */

  // Arrange: Prepare malicious SQL injection payload
  // This payload would delete the users table if the application is vulnerable
  const maliciousInput = "'; DROP TABLE users; --";

  // Act: Send registration request with malicious input
  const response = await fetch("/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      username: maliciousInput, // Malicious SQL injection attempt
      email: "test@test.com", // Valid email
      password: "password123", // Valid password
    }),
  });

  // Assert: Verify the application properly handles the malicious input
  // Should be rejected (400) or sanitized (201 but safe)
  // If this returns 200/201, the application is vulnerable to SQL injection
  expect([400, 422]).toContain(response.status);
});
```

</details>

**Guided Walkthrough:**

1. **Malicious Input**: We try to inject SQL code that would delete the users table
2. **Request**: We send this malicious input to the registration endpoint
3. **Assertion**: We verify the system rejects or sanitizes the input

**Try This:**

1. **Run the security test from command line:**

   ```bash
   # Run specific security test
   pytest tests/security/test_security.py::test_sql_injection_prevention -v

   # Run all security tests
   pytest tests/security/ -v

   # Run with detailed output
   pytest tests/security/test_security.py -v -s
   ```

2. **Test security vulnerabilities:**

   ```bash
   # Run with rate limiting disabled (TESTING mode)
   cd backend
   # Linux/Mac
   TESTING=true uvicorn main:app --reload --port 8000

   # Windows (PowerShell)
   $env:TESTING='true'; uvicorn main:app --reload --port 8000

   # Then run security tests
   cd ../tests/security
   pytest test_security.py -v
   ```

3. **Make it fail intentionally to see security testing in action:**

   ```python
   # Temporarily comment out input validation in backend/auth.py
   # Then run the test and see it catch the vulnerability!
   ```

   This shows how security tests protect against real vulnerabilities!

4. **Fix it back and run again to see it pass**

**What you'll learn:**

- How to run security tests from command line
- How to test for real security vulnerabilities
- How to interpret security test results
- The importance of security testing in production

**More Examples:**

- `test_xss_prevention` - Test for XSS attacks
- `test_rate_limiting` - Test rate limit enforcement
- Full file: [test_security.py](../../tests/security/test_security.py)

### 🔄 Hybrid Track

**Test both performance and security!** This is what senior QA engineers do.

1. **Performance (k6)** - Test how fast and scalable the system is
2. **Security (pytest)** - Test how safe the system is
3. **Combined** - Test performance under security constraints
4. **See the connection**: High load can expose security vulnerabilities

---

<h2 id="part-5-hands-on-practice">Part 5: Hands-On Practice 🏃</h2>

### Step 1: Run Performance Tests

```bash
# Install k6
# macOS: brew install k6
# Linux: See https://k6.io/docs/getting-started/installation/
# Windows: choco install k6

# Run smoke test (baseline)
cd tests/performance
k6 run smoke-test.js

# Run load test (realistic traffic)
k6 run load-test.js

# Run stress test (find limits)
k6 run stress-test.js
```

**Observe:** Metrics, graphs, and failure points.

### Step 2: Interpret Results

Look at your load test results:

**Questions:**

1. What's the average response time?
2. What's the 95th percentile (p95)?
3. Are any requests failing?
4. Could the system handle more load?

### Step 3: Run Security Tests

```bash
cd tests/security
pytest -v

# Run specific test
pytest test_security.py::test_sql_injection_prevention -v
```

**Try making a test fail:**

- Comment out input validation
- Disable rate limiting
- See how tests catch vulnerabilities

### Step 4: Test Rate Limiting

```python
def test_rate_limiting_behavior(client):
    """Understand rate limiting in action."""
    responses = []

    # Make 150 requests
    for i in range(150):
        r = client.get("/posts")
        responses.append(r.status_code)

    # Analyze results
    success_count = responses.count(200)
    limited_count = responses.count(429)

    print(f"Success: {success_count}, Rate limited: {limited_count}")
```

**Run it and observe** when rate limiting kicks in.

### Step 5: Think Like an Attacker

Try to break the application:

**Common attacks to test:**

1. SQL injection: `' OR '1'='1`
2. XSS: `<script>alert(1)</script>`
3. Path traversal: `../../etc/passwd`
4. Oversized inputs: 10MB text string
5. Special characters: `\x00\x00\x00`

**Write tests for each!**

---

<h2 id="part-6-additional-patterns">Part 6: Additional Patterns 🚀</h2>

**📝 Note:** The patterns below are **additional enhancements** to your performance and security testing skills. All the **core concepts** needed to meet the Stage 4 success criteria are covered in Parts 1-5 above.

These patterns enhance your security testing capabilities:

### OWASP Top 10 Security Risks

The most critical web application security risks:

1. **Broken Access Control** - Improper authorization
2. **Cryptographic Failures** - Weak encryption, exposed data
3. **Injection** - SQL, command, XSS
4. **Insecure Design** - Missing security controls
5. **Security Misconfiguration** - Default configs, verbose errors
6. **Vulnerable Components** - Outdated libraries
7. **Authentication Failures** - Weak passwords, session issues
8. **Data Integrity Failures** - Unsigned/unverified data
9. **Logging Failures** - Insufficient monitoring
10. **Server-Side Request Forgery (SSRF)** - Unvalidated URLs

### Performance Testing Types

| Type            | Purpose                    | Example                             |
| --------------- | -------------------------- | ----------------------------------- |
| **Smoke Test**  | Verify basic functionality | 1-2 users, happy path               |
| **Load Test**   | Test expected traffic      | 50 concurrent users, 10 minutes     |
| **Stress Test** | Find breaking point        | Gradually increase to 500 users     |
| **Spike Test**  | Test sudden traffic        | Jump from 10 to 100 users instantly |
| **Soak Test**   | Test extended duration     | 50 users for 4 hours                |

### Security Testing Mindset

✅ **Think like an attacker:**

- What's the worst input I can send?
- Can I access others' data?
- Can I bypass authentication?
- Can I cause a crash or DOS?

✅ **Test assumptions:**

- "Users will only send valid data" ❌
- "Nobody will try that" ❌
- "The frontend validates it" ❌

---

<h2 id="success-criteria">✅ Success Criteria</h2>

You're ready for Stage 5 when you can:

**Core concepts (all tracks):**

- [ ] Explain the difference between load, stress, and spike testing
- [ ] Write a basic k6 load test
- [ ] Interpret performance metrics (p95, throughput, error rate)
- [ ] Identify common security vulnerabilities
- [ ] Test for SQL injection and XSS
- [ ] Verify rate limiting works correctly
- [ ] Think critically about edge cases and attack vectors
- [ ] Prioritize security issues by severity

**Performance Track:**

- [ ] Use k6 to create load tests
- [ ] Interpret performance metrics and graphs
- [ ] Identify performance bottlenecks
- [ ] Test different load patterns (ramp-up, spike, soak)

**Security Track:**

- [ ] Use pytest to create security tests
- [ ] Test for OWASP Top 10 vulnerabilities
- [ ] Understand security testing mindset
- [ ] Write tests for input validation and rate limiting

**Hybrid Track:**

- [ ] Can explain how performance and security testing complement each other
- [ ] Understand when to use each testing approach
- [ ] Can write both performance and security tests

---

<h2 id="why-this-matters">🧠 Why This Matters</h2>

### In Real QA Teams

- **Performance issues cost money** - Slow apps lose users and revenue
- **Security bugs are critical** - One breach can destroy a company
- **Proactive testing** - Find issues before attackers do
- **Capacity planning** - Know your system's limits
- **SLA compliance** - Meet response time guarantees

### For Your Career

- **High-value niche** - Performance and security testers are rare
- **Cross-functional skill** - Work with DevOps, security, and engineering
- **Business impact** - Directly affect user experience and safety
- **Incident prevention** - Stop production fires before they start
- **Specialized knowledge** - Commands higher salaries

---

<h2 id="related-resources">🔗 Related Resources</h2>

### Hands-On Practice

**🐍 Python Track:**

- [Lab 13: Load Testing with k6 (Python)](exercises/LAB_13_Load_Testing_k6.md)
- [Lab 14: Security Testing with OWASP (Python)](exercises/LAB_14_Security_Testing_OWASP_Python.md)
- [Lab 15: Rate Limiting Testing (Python)](exercises/LAB_15_Rate_Limiting_Testing_Python.md)

**🟨 JavaScript Track:**

- [Lab 13: Load Testing with k6 (JavaScript)](exercises/LAB_13_Load_Testing_k6.md)
- [Lab 14: Security Testing with OWASP (JavaScript)](exercises/LAB_14_Security_Testing_OWASP_JavaScript.md)
- [Lab 15: Rate Limiting Testing (JavaScript)](exercises/LAB_15_Rate_Limiting_Testing_JavaScript.md)

### Documentation

- [k6 Documentation](https://k6.io/docs/)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [Rate Limiting Guide](../../docs/guides/RATE_LIMITING.md)

### Tools

- [k6](https://k6.io/) - Performance testing
- [OWASP ZAP](https://www.zaproxy.org/) - Security scanning
- [Burp Suite](https://portswigger.net/burp) - Security testing

---

<h2 id="self-check-quiz-optional">🧠 Self-Check Quiz (Optional)</h2>

Before moving to Stage 5, can you answer these questions?

1. **What's the main purpose of performance testing?**

   - A) To find bugs in the code
   - B) To ensure the app works under load
   - C) To test individual functions
   - D) To verify API endpoints

2. **What does p95 response time mean?**

   - A) The average response time
   - B) 95% of requests are faster than this time
   - C) The slowest response time
   - D) The response time for 95% of users

3. **What is the OWASP Top 10?**

   - A) The 10 most common web vulnerabilities
   - B) The 10 best testing tools
   - C) The 10 most important test cases
   - D) The 10 fastest testing frameworks

4. **Why is security testing important?**

   - A) It makes apps run faster
   - B) It protects against attacks and data breaches
   - C) It improves user experience
   - D) It reduces development time

5. **What's the difference between load testing and stress testing?**
   - A) Load testing uses more users
   - B) Load testing checks normal load, stress testing checks breaking point
   - C) Stress testing is faster
   - D) There's no difference

**Answers:** [Check your answers here](../solutions/stage_4_quiz_answers.md)

---

<h2 id="reflection">🤔 Reflection</h2>

Before moving to Stage 5, answer these:

1. **Why might an application perform well in development but poorly in production?**

2. **What's more important: average response time or p95 response time? Why?**

3. **Pick one OWASP Top 10 vulnerability. Explain it in simple terms and how you'd test for it.**

4. **If you had to choose between performance testing OR security testing, which would you prioritize? Why?**

5. **What's one security test you think every application should have?**

**Document your answers** in [reflection.md](reflection.md).

---

<h2 id="stage-complete">🎉 Stage Complete</h2>

You now understand non-functional testing that protects users and business!

### 👉 [Continue to Stage 5: Job-Ready Capstone](../stage_5_capstone/README.md)

---

_Pro tip: Performance and security testing are where QA engineers become invaluable. Master these, and you're ready for senior roles! 🚀_
