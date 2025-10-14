# 🚀 Stage 4: Performance & Security

**Non-Functional Testing That Matters**

Performance and security testing ensure your application is fast, scalable, and safe. These tests catch issues that functional tests miss: bottlenecks, vulnerabilities, and edge cases under load.

---

## 🎯 Learning Goals

By the end of this stage, you will:

- ✅ Understand performance testing concepts (load, stress, spike)
- ✅ Write load tests with k6
- ✅ Interpret performance metrics (response time, throughput, errors)
- ✅ Test for common security vulnerabilities
- ✅ Verify rate limiting and authentication security
- ✅ Test input validation and SQL injection protection
- ✅ Think like an attacker to find weaknesses

**Duration:** 2-3 hours

---

## 📂 Where to Look

**Note:** Performance and security testing uses tools from both stacks!

---

### 🚀 Performance Tests (JavaScript - k6)

**📁 Folder:** `/tests/performance/`

**All tracks use k6 (JavaScript-based):**

1. **[`smoke-test.js`](../../tests/performance/smoke-test.js)**
   - Basic performance baseline
   - Single user, minimal load

2. **[`load-test.js`](../../tests/performance/load-test.js)**
   - Sustained traffic simulation
   - Multiple concurrent users

3. **[`stress-test.js`](../../tests/performance/stress-test.js)**
   - Breaking point testing
   - Gradually increasing load

4. **[`K6_GUIDE.md`](../../tests/performance/K6_GUIDE.md)**
   - k6 concepts and usage
   - Metrics interpretation

**Tool:** k6 (JavaScript) - tests ANY backend (Python, Node.js, Go, etc.)

---

### 🔒 Security Tests (Python - pytest)

**📁 Folder:** `/tests/security/`

**All tracks use pytest (Python-based):**

1. **[`test_security.py`](../../tests/security/test_security.py)**
   - Input validation
   - SQL injection protection
   - XSS prevention
   - CSRF protection

2. **[`test_rate_limiting.py`](../../tests/security/test_rate_limiting.py)**
   - Rate limit enforcement
   - API abuse prevention
   - DDoS protection

3. **[`README.md`](../../tests/security/README.md)**
   - Security testing overview
   - Best practices

**Tool:** pytest (Python) - tests backend security endpoints

**Why different tools?**
- k6 is industry standard for performance (JavaScript)
- pytest is excellent for security testing (Python)
- Professional QA engineers use both!

---

## 🔍 What to Look For

### 1. Load Test Structure (k6)

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
    stages: [
        { duration: '30s', target: 10 },  // Ramp up
        { duration: '1m', target: 10 },   // Stay at 10 users
        { duration: '30s', target: 0 },   // Ramp down
    ],
};

export default function() {
    // Test scenario
    let response = http.get('http://localhost:8000/posts');

    // Verify performance
    check(response, {
        'status is 200': (r) => r.status === 200,
        'response time < 200ms': (r) => r.timings.duration < 200,
    });

    sleep(1);
}
```

**Key elements:**
- Stages define load pattern
- Checks verify responses
- Virtual users simulate real traffic
- Metrics measured automatically

### 2. Performance Metrics

```
✓ status is 200.........................: 100.00% ✓ 1200 ✗ 0
✓ response time < 200ms.................: 95.00%  ✓ 1140 ✗ 60

http_req_duration......................: avg=158ms min=45ms max=523ms
http_req_failed........................: 0.00%
http_reqs..............................: 1200
```

**What to watch:**
- `http_req_duration` - How fast responses are
- `http_req_failed` - Error rate
- `http_reqs` - Total requests handled
- Check pass rates - Percentage meeting criteria

### 3. Security Test Patterns

```python
@pytest.mark.security
def test_sql_injection_prevention(client):
    """Verify SQL injection attempts are blocked."""
    # Try SQL injection payload
    malicious_input = "'; DROP TABLE users; --"

    response = client.post("/auth/register", json={
        "username": malicious_input,
        "email": "test@test.com",
        "password": "password123"
    })

    # Should be rejected (400) or sanitized (201 but safe)
    assert response.status_code in [400, 422]
```

**Security testing mindset:**
- Think like an attacker
- Test malicious inputs
- Verify proper rejection
- Ensure no data leakage

### 4. Rate Limiting Tests

```python
def test_rate_limit_enforced(client):
    """Verify rate limits prevent API abuse."""
    # Make many requests quickly
    for i in range(150):
        response = client.get("/posts")

        if i < 100:
            assert response.status_code == 200
        else:
            # Should be rate limited after 100 requests
            assert response.status_code == 429  # Too Many Requests
```

**Rate limiting tests:**
- Verify limits are enforced
- Check appropriate status codes
- Ensure legitimate traffic isn't blocked
- Test reset windows

### 5. Input Validation

```python
@pytest.mark.security
def test_xss_prevention(client, auth_headers):
    """Verify XSS payloads are sanitized."""
    xss_payload = "<script>alert('XSS')</script>"

    response = client.post("/posts",
        json={"content": xss_payload},
        headers=auth_headers
    )

    # Should be sanitized or escaped
    post_data = response.json()
    assert "<script>" not in post_data["content"]
```

**Input validation checks:**
- XSS payloads
- HTML injection
- Command injection
- Path traversal

---

## 🏃 How to Practice

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

## ✅ Success Criteria

You're ready for Stage 5 when you can:

- [ ] Explain the difference between load, stress, and spike testing
- [ ] Write a basic k6 load test
- [ ] Interpret performance metrics (p95, throughput, error rate)
- [ ] Identify common security vulnerabilities
- [ ] Test for SQL injection and XSS
- [ ] Verify rate limiting works correctly
- [ ] Think critically about edge cases and attack vectors
- [ ] Prioritize security issues by severity

---

## 🧠 Why This Matters

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

## 💡 Key Concepts

### Performance Testing Types

| Type | Purpose | Example |
|------|---------|---------|
| **Smoke Test** | Verify basic functionality | 1-2 users, happy path |
| **Load Test** | Test expected traffic | 50 concurrent users, 10 minutes |
| **Stress Test** | Find breaking point | Gradually increase to 500 users |
| **Spike Test** | Test sudden traffic | Jump from 10 to 100 users instantly |
| **Soak Test** | Test extended duration | 50 users for 4 hours |

### Key Performance Metrics

- **Response Time (avg, p95, p99)** - How fast requests complete
- **Throughput (req/sec)** - How many requests per second
- **Error Rate (%)** - Percentage of failed requests
- **Concurrent Users** - Simulated users at once
- **Resource Usage** - CPU, memory, network

### OWASP Top 10 (Security)

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

## 🔗 Related Resources

### Hands-On Practice

- [Lab 6: Rate Limiting & Security](../../labs/LAB_06_Testing_With_Rate_Limits.md)

### Documentation

- [k6 Documentation](https://k6.io/docs/)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [Rate Limiting Guide](../../docs/guides/RATE_LIMITING.md)

### Tools

- [k6](https://k6.io/) - Performance testing
- [OWASP ZAP](https://www.zaproxy.org/) - Security scanning
- [Burp Suite](https://portswigger.net/burp) - Security testing

---

## 🤔 Reflection

Before moving to Stage 5, answer these:

1. **Why might an application perform well in development but poorly in production?**

2. **What's more important: average response time or p95 response time? Why?**

3. **Pick one OWASP Top 10 vulnerability. Explain it in simple terms and how you'd test for it.**

4. **If you had to choose between performance testing OR security testing, which would you prioritize? Why?**

5. **What's one security test you think every application should have?**

**Document your answers** in [reflection.md](reflection.md).

---

## 🎉 Stage Complete!

You now understand non-functional testing that protects users and business!

### 👉 [Continue to Stage 5: Job-Ready Capstone](../stage_5_capstone/README.md)

---

*Pro tip: Security vulnerabilities make excellent interview stories. "I found and prevented a SQL injection vulnerability" is resume gold! 🏆*

