# 🧪 Lab 6: Testing Applications with Rate Limiting & Security

**Estimated Time:** 60-90 minutes
**Difficulty:** Advanced
**Prerequisites:** Labs 1-5 completed
**Concepts:** Rate limiting, test infrastructure, environment configuration, fixture design

---

## 🎯 What You'll Learn

- How security features (like rate limiting) affect your tests
- Why tests pass individually but fail together
- Environment-based configuration for testing
- Advanced pytest fixture patterns
- Real-world test infrastructure challenges
- How to debug "flaky" tests caused by rate limits

---

## 📚 Background: When Your Code Works TOO Well

### The Scenario

You implement rate limiting to prevent brute force attacks:

```python
@router.post("/login")
@limiter.limit("20/minute")  # Security feature!
def login(request: Request, ...):
    # Login logic
```

**Great for security!** ✅ Prevents attackers from trying 1000 passwords per second.

**But then your tests start failing...** ❌

---

## 🐛 The Problem

### Test Results That Don't Make Sense

```bash
# Running one test: ✅ PASSES
$ pytest tests/security/test_auth.py::test_cannot_edit_posts -v
PASSED

# Running all tests: ❌ FAILS
$ pytest tests/security/ -v
ERROR: KeyError: 'access_token'
```

**What?!** 🤔 The code didn't change, why does it fail?

---

## 🔍 Lab Exercise 1: Reproduce the Issue

### Step 1: Check Current Rate Limits

Open `backend/routers/auth.py` and look for:

```python
@limiter.limit("20/minute")
def login(...):
```

This means: **20 login requests per minute, per IP address.**

### Step 2: Count Your Test's Login Calls

Open `tests/security/test_security.py` and count how many tests use the `auth_token` fixture.

**Question:** If you have 25 tests that each need an auth token, what happens?

<details>
<summary>Click to see answer</summary>

**Answer:** After 20 tests, the 21st test hits the rate limit!

```
Test 1-20: ✅ Get tokens successfully
Test 21+:  ❌ Get 429 "Rate limit exceeded"
```

</details>

### Step 3: Reproduce the Failure

```bash
cd /Users/danmanez/Projects/Testbook

# Start backend normally (with rate limiting)
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000 &

# Run security tests
cd ..
pytest tests/security/ -v
```

**Expected:** Some tests fail with rate limit errors or KeyError: 'access_token'

✅ **Checkpoint:** You can reproduce the issue

---

## 💡 Understanding the Root Cause

### The Auth Token Fixture

```python
@pytest.fixture(scope="session")
def auth_token():
    """Get authentication token for testing."""
    response = requests.post(f"{BASE_URL}/auth/login", ...)
    return response.json()["access_token"]
```

**You might think:** "`scope='session'` means this runs ONCE, right?"

**Reality:** Pytest calls it once per **test class** or **test module**, not truly once per session.

**Result:**

- You have 5 test classes
- Fixture runs 5 times
- Plus your actual login tests make 15+ more calls
- **Total: 20+ login calls in 60 seconds** → Rate limited!

---

## 🔧 Lab Exercise 2: Solutions

### Solution A: Testing Mode (Recommended)

**Concept:** Increase rate limits during testing, normal limits in production.

#### Step 1: Add Environment-Based Configuration

Open `backend/main.py` and add:

```python
import os

TESTING_MODE = os.getenv("TESTING", "false").lower() == "true"

if TESTING_MODE:
    # Testing: High limits to avoid test interference
    limiter = Limiter(key_func=get_remote_address, default_limits=["1000/minute"])
else:
    # Production: Reasonable limits for security
    limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])
```

#### Step 2: Adjust Router Rate Limits

Open `backend/routers/auth.py`:

```python
import os

TESTING_MODE = os.getenv("TESTING", "false").lower() == "true"
LOGIN_RATE = "100/minute" if TESTING_MODE else "20/minute"
REGISTER_RATE = "100/minute" if TESTING_MODE else "15/minute"

@router.post("/login")
@limiter.limit(LOGIN_RATE)  # Dynamic rate based on environment
def login(...):
```

#### Step 3: Run Tests in Testing Mode

```bash
# Kill old backend
lsof -ti:8000 | xargs kill

# Start in testing mode
cd backend
TESTING=true uvicorn main:app --reload --port 8000 &

# Run tests
cd ..
pytest tests/security/ -v
```

✅ **Checkpoint:** More tests should pass now!

---

### Solution B: Single Token for All Tests

**Concept:** Get ONE token and reuse it everywhere.

Create a module-level fixture:

```python
# tests/security/conftest.py
import pytest
import requests

BASE_URL = "http://localhost:8000/api"

# Get token ONCE at module import time
_cached_token = None

@pytest.fixture(scope="session")
def auth_token():
    """Get a single auth token for all tests."""
    global _cached_token

    if _cached_token is None:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": "sarah.johnson@testbook.com", "password": "Sarah2024!"}
        )
        _cached_token = response.json()["access_token"]

    return _cached_token
```

**Pros:** Only ONE login call for entire test suite
**Cons:** Tests share state (token could expire during long test runs)

---

### Solution C: Add Delays Between Tests

```python
@pytest.fixture(autouse=True)
def slow_down_tests():
    """Prevent tests from hitting rate limits."""
    import time
    time.sleep(0.5)  # 500ms between tests
```

**Pros:** Simple, no code changes needed
**Cons:** Tests run slower (30+ seconds overhead)

---

## 🎓 Lab Exercise 3: Test the Rate Limiting

### Task: Verify Rate Limiting Actually Works

Create `tests/security/test_rate_limit_demo.py`:

```python
import requests
import pytest

BASE_URL = "http://localhost:8000/api"

def test_rate_limiting_works():
    """Demonstrate that rate limiting is working."""
    session = requests.Session()

    # Make rapid requests
    attempts = 0
    rate_limited = False

    for i in range(25):
        response = session.post(
            f"{BASE_URL}/auth/login",
            json={"email": "test@test.com", "password": "wrong"}
        )

        if response.status_code == 429:
            rate_limited = True
            attempts = i
            break

        attempts += 1

    # Should hit rate limit before all 25 attempts
    assert rate_limited, f"Expected rate limit but completed {attempts} attempts"
    assert attempts <= 20, f"Rate limit threshold seems wrong: {attempts} attempts allowed"

    print(f"✅ Rate limited after {attempts} attempts (expected ~20)")
```

**Run it:**

```bash
# WITHOUT testing mode - should hit rate limit
pytest tests/security/test_rate_limit_demo.py -v -s

# WITH testing mode - should allow all requests
TESTING=true pytest tests/security/test_rate_limit_demo.py -v -s
```

✅ **Checkpoint:** You can see rate limiting in action!

---

## 🧠 Lab Exercise 4: Understand HTTP Status Codes

### The 401 vs 403 Confusion

Some tests fail because they expect `401` but get `403`.

**Both are valid auth errors!**

| Code | Meaning | When to Use |
|------|---------|-------------|
| **401** | Unauthorized | "You need to authenticate" (no token or bad token) |
| **403** | Forbidden | "You're authenticated but can't access this" (valid token, insufficient permissions) |

### Which Should You Use?

**Example scenarios:**

```python
# No token provided → 401
GET /api/users/me
# Response: 401 "Authentication required"

# Valid token, but not the owner → 403
DELETE /api/posts/123  # Trying to delete someone else's post
# Response: 403 "Not authorized to delete this post"

# Invalid/expired token → 401 OR 403 (both acceptable!)
GET /api/users/me
Authorization: Bearer invalid_token_here
# Response: Could be either 401 or 403
```

**FastAPI's get_current_user dependency throws 403 by default.**

### Fix the Test

**Before:**

```python
assert response.status_code == 401  # Too strict!
```

**After:**

```python
assert response.status_code in [401, 403]  # Accepts both valid auth errors
```

---

## 🎯 Lab Exercise 5: Fix a Real Issue

### Task: Make Tests Work With Rate Limiting

You have 3 options. Choose one and implement it:

#### Option 1: Environment Variable (Easiest)

1. Update `backend/main.py` with TESTING mode logic (shown above)
2. Update test runner to use `TESTING=true`
3. Run tests and see them pass!

#### Option 2: Better Fixture Design

1. Create a truly session-wide token cache
2. Ensure only ONE login call per test suite
3. Document the pattern

#### Option 3: Disable Rate Limiting for Tests

```python
# backend/routers/auth.py
if not TESTING_MODE:
    @limiter.limit("20/minute")

@router.post("/login")
# ... conditional decorator application
```

**Choose your approach and implement it!**

---

## 🐛 Debugging Exercise

### Challenge: Why Does This Test Hang?

Sometimes tests hang instead of failing. Common causes:

**1. Waiting for response that never comes:**

```python
response = requests.post("/login", ...)
# If rate limited (429), might not have expected JSON structure
token = response.json()["access_token"]  # KeyError if 429!
```

**2. Infinite retries:**

```python
# Test keeps retrying forever
for i in range(1000):
    if response.status_code == 200:
        break
    # Never breaks if always getting 429
```

**3. Timeout not set:**

```python
requests.post("/login")  # No timeout!
# If server is slow or rate limited, waits forever
```

**Fix:** Always use timeouts!

```python
requests.post("/login", timeout=5)
```

---

## 🎓 What You Learned

### Real-World Lessons

✅ **Security features affect tests**

- Rate limiting, timeouts, size limits all impact test design
- What works in development might fail in testing
- Environment configuration is crucial

✅ **Test isolation is hard**

- Fixtures can interfere with each other
- Shared resources (IP address) cause conflicts
- Order of execution matters

✅ **Fixture scope is tricky**

- `scope="session"` doesn't mean what you think
- Need careful design for truly shared state
- Caching strategies help

✅ **HTTP status codes matter**

- 401 vs 403 are both valid for auth errors
- Tests should accept both
- Framework conventions vary

---

## 💪 Practice Challenges

### Challenge 1: Implement Request Size Limiting

Add middleware to reject requests >10MB:

```python
# backend/main.py
class RequestSizeLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > 10_000_000:  # 10MB
            return JSONResponse(status_code=413, content={"detail": "Request too large"})
        return await call_next(request)
```

**Test it:**

```python
def test_request_size_limit():
    large_data = "x" * (11 * 1024 * 1024)  # 11MB
    response = requests.post("/api/posts", json={"content": large_data})
    assert response.status_code == 413
```

### Challenge 2: Add Rate Limit Headers

Make rate limits visible to API consumers:

```python
@router.post("/login")
@limiter.limit("20/minute")
def login(request: Request, ...):
    response = ...
    # Add headers showing remaining requests
    response.headers["X-RateLimit-Limit"] = "20"
    response.headers["X-RateLimit-Remaining"] = "..."
    return response
```

### Challenge 3: Test Different Rate Limit Scenarios

Write tests for:

- Normal usage (under limit)
- Exactly at limit
- Over limit (should get 429)
- After waiting (limit should reset)

---

## 🔗 Related Concepts

### This Lab Connects To

**Software Engineering:**

- Environment configuration (dev/test/prod)
- Feature flags and conditional logic
- Security vs usability trade-offs

**Testing:**

- Test isolation and interference
- Fixture design patterns
- Test environment management
- Debugging flaky tests

**Security:**

- Rate limiting strategies
- Brute force protection
- DDoS prevention
- API abuse prevention

---

## ✅ Lab Completion Checklist

- [ ] Understand how rate limiting affects tests
- [ ] Can explain why tests pass individually but fail together
- [ ] Implemented TESTING mode environment variable
- [ ] Fixed fixture to avoid rate limit issues
- [ ] Ran security tests successfully
- [ ] Understand 401 vs 403 status codes
- [ ] Can identify test infrastructure issues
- [ ] Know when to use environment-based configuration

---

## 🎯 Key Takeaways

### The Paradox

**Good security can break your tests!**

This is a REAL problem in professional testing:

- Your code works perfectly
- Your tests work individually
- But together they fail!

**Why?** Your security features are doing their job.

### The Solution Pattern

```
Problem: Feature works, tests fail together
├─ Root cause: Shared resources (IP, rate limits, state)
├─ Symptom: Pass individually, fail in suite
└─ Solution: Environment-based configuration
    ├─ Production: Real limits
    ├─ Testing: Relaxed limits
    └─ Tests prove features work!
```

### The Real Lesson

**This isn't a bug - it's engineering!**

- ✅ Rate limiting implemented correctly
- ✅ Tests prove it works (by hitting limits!)
- ✅ Infrastructure needs adjustment
- ✅ Professional pattern: environment configuration

---

## 🚀 Advanced Topics

### Testing Rate Limits Properly

**Anti-pattern:**

```python
def test_rate_limit():
    # Test should NEVER hit real rate limits
    for i in range(100):
        response = api.post("/login", ...)  # Hits real limit!
```

**Better:**

```python
def test_rate_limit():
    # Mock the rate limiter or use test mode
    with mock.patch('limiter.limit'):
        # Test the logic without hitting real limits
```

### Redis-Based Rate Limiting

For serious production apps:

```python
from slowapi import Limiter

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="redis://localhost:6379"  # Persistent storage
)
```

**Benefits:**

- Works across multiple servers
- Survives server restarts
- More accurate counting

---

## 📖 Real-World Story

### Why This Lab Exists

**We implemented rate limiting in Testbook.** Great for security!

**Then ran the test suite.** 23 security tests.

**Result:**

- Tests 1-15: ✅ PASS
- Tests 16-23: ❌ ERROR (rate limited!)

**First reaction:** "The tests are broken!"

**Reality:** "The security works TOO well!"

**Solution:** Environment-based configuration (this lab!)

**This is a REAL problem that happens in professional development.**

---

## 🎓 Discussion Questions

1. **Should you disable security features in tests?**
   - Pro: Tests run reliably
   - Con: Not testing real behavior
   - Answer: Use relaxed limits, not disabled

2. **How do you test a rate limiter without hitting it?**
   - Test mode with high limits
   - Separate tests specifically for rate limiting
   - Mock the limiter for unit tests

3. **Is it okay for tests to fail due to infrastructure?**
   - No - tests should be reliable
   - But it's a sign your security works!
   - Fix infrastructure, not the feature

4. **What's the difference between flaky tests and infrastructure issues?**
   - Flaky: Random, unreliable code
   - Infrastructure: Environmental constraints
   - Both look the same, causes are different!

---

## 🐛 Troubleshooting

**Problem:** Tests still fail even with TESTING=true

**Check:**

```bash
# Is the env var actually set?
echo $TESTING

# Is the backend seeing it?
# Look in logs or add print statement:
print(f"TESTING_MODE: {TESTING_MODE}")
```

**Problem:** Rate limit not resetting between test runs

**Solution:** Wait 60 seconds or restart backend

**Problem:** Some tests still hit rate limit

**Solution:** Increase TESTING mode limits further (1000/minute → 10000/minute)

---

## 🔗 Related Resources

- [slowapi Documentation](https://slowapi.readthedocs.io/)
- [HTTP Status Codes](https://httpstatuses.com/)
- [pytest Fixture Scopes](https://docs.pytest.org/en/latest/reference/fixtures.html#scope)
- [Lab 5: Test Data Management](LAB_05_Test_Data_Management.md)
- [TESTING_ANTIPATTERNS.md](../docs/reference/TESTING_ANTIPATTERNS.md)

---

## 💡 Pro Tips

**Tip 1:** Always use environment variables for test configuration

```bash
TESTING=true pytest  # High rate limits
TESTING=false pytest  # Real rate limits (will fail!)
```

**Tip 2:** Document your rate limits clearly

```python
# Production: 20 requests/minute
# Testing: 100 requests/minute
LOGIN_RATE = "100/minute" if TESTING_MODE else "20/minute"
```

**Tip 3:** Test your rate limiting separately

```python
def test_rate_limit_works():
    # This test SHOULD hit the limit
    # Run it alone with TESTING=false
```

**Tip 4:** Add timeout to ALL requests

```python
requests.post("/login", json=data, timeout=5)  # Always!
```

---

## 🎉 Success Criteria

You've mastered this lab when you can:

- ✅ Explain why tests pass alone but fail together
- ✅ Implement environment-based configuration
- ✅ Design fixtures that avoid rate limits
- ✅ Debug test infrastructure issues
- ✅ Understand the security/testing trade-off
- ✅ Know when features work "too well" for tests

---

## 🏆 Bonus: Add This to Your Resume

**Skills demonstrated:**

- API rate limiting implementation
- Test environment configuration
- Fixture design patterns
- Security testing
- Infrastructure debugging
- Real-world problem solving

**Interview question this prepares you for:**

> "Tell me about a time when your tests failed even though your code was correct."

**Your answer:**
> "I implemented rate limiting for security. Tests started failing together due to hitting the rate limit. I debugged it by running tests individually, identified the shared resource issue, and implemented environment-based configuration so tests use relaxed limits while production uses strict limits. This taught me how security features can affect test infrastructure."

🎯 **That's a senior-level answer!**

---

**🎉 Congratulations!** You now understand advanced testing infrastructure challenges that many senior engineers struggle with!

**Next Lab:** Coming soon - Advanced CI/CD Integration

---

## 📝 Instructor Notes

**Teaching Time:** 60-90 minutes

**Key Learning Objectives:**

1. Environment-based configuration (critical concept)
2. Test isolation challenges (common interview topic)
3. Security/testing trade-offs (real-world decision making)

**Common Student Questions:**

- "Why not just remove rate limiting?" → Security is important!
- "Why do fixtures run multiple times?" → Pytest scoping rules
- "Is this a common problem?" → Yes! Very common in real projects

**Assessment Ideas:**

- Have students implement TESTING mode
- Ask them to debug a failing test suite
- Have them write a rate limit test that doesn't hit the limit

**This lab is based on REAL issues we encountered while building Testbook!**
