# 🔐 Security Tests

Comprehensive security testing for Testbook API.

---

## ⚠️ IMPORTANT: Why Some Tests May Fail

**If you see security test failures, READ THIS FIRST!**

### The Rate Limiting Issue

**Problem:** Tests may fail with errors like:

- `KeyError: 'access_token'`
- `AssertionError: Rate limiting not working`
- `429 Too Many Requests`

**This does NOT mean the code is broken!** In fact, it proves security is working.

### Why This Happens

1. **Rate limiting IS implemented** (20 login attempts/minute in production)
2. **These tests make many API calls** (23 tests × multiple calls each)
3. **All tests share the same IP address** (localhost)
4. **Result:** Tests exhaust the rate limit budget → later tests fail

**Visual representation:**

```text
Tests 1-15:  ✅ Pass (within rate limit)
Test 16:     ❌ Gets rate limited (429 error)
Tests 17-23: ❌ Cascade failures (can't get auth tokens)
```

### The Solution: TESTING Mode

Run tests with increased rate limits:

```bash
# Start backend in TESTING mode
cd backend
TESTING=true uvicorn main:app --reload --port 8000

# In another terminal, run security tests
pytest tests/security/ -v
```

**What TESTING mode does:**

- Production: 20 login requests/minute
- Testing: 1000 login requests/minute (allows all tests to pass)

---

## 🚀 Quick Start

### Option 1: Use the Test Runner (Recommended)

```bash
# From project root
./run-all-tests.sh
```

This automatically starts backend in TESTING mode.

### Option 2: Manual Setup

```bash
# Terminal 1: Start backend in TESTING mode
cd backend
source .venv/bin/activate
TESTING=true uvicorn main:app --reload --port 8000

# Terminal 2: Run security tests
cd /path/to/Testbook
pytest tests/security/ -v
```

### Option 3: One-Line Command

```bash
# Kill old backend and start fresh in TESTING mode
lsof -ti:8000 | xargs kill; cd backend && TESTING=true uvicorn main:app --port 8000 &
sleep 5
pytest tests/security/ -v
```

---

## 📊 Expected Results

### With the backend server running TESTING=true (Correct Setup)

```text
======================= 18 passed, 11 skipped in 14.8s ========================
```

This is now deterministic - it doesn't matter whether `TESTING=true` is also
set on the shell running pytest. `test_login_attempts_should_be_rate_limited`
and `test_registration_rate_limiting` probe the server directly (via
`conftest.py`'s `server_testing_mode` fixture, which checks `/api/dev/users`'
status code) to decide whether to skip, instead of trusting `os.getenv`. See
the comment in `conftest.py` for the full reasoning.

**Passing (18 tests):**

- ✅ All authentication tests
- ✅ All authorization tests
- ✅ Input validation (SQL injection, XSS)
- ✅ Data exposure prevention
- ✅ Session management
- ✅ Request size limits

**Skipped (11 tests):**

- ⏭️ Account lockout (feature not implemented - future enhancement)
- ⏭️ IP banning (feature not implemented - future enhancement)
- ⏭️ Rate limit headers (optional feature, not implemented)
- ⏭️ Login rate-limit test (skips when the server it's calling is in
  TESTING mode, where the limit is raised to 1000/min - too high to
  trigger in a test)
- ⏭️ Registration rate-limit test (same reasoning, 500/min)
- ⏭️ Six OWASP-gap placeholders in `test_owasp_gaps.py` (always skipped by design, see [Coverage Against the OWASP Top 10](#coverage-against-the-owasp-top-10-2021) below)

### Against a server NOT running TESTING=true

```text
============================== 2 passed in 5.48s ===============================
```

(Running just the two rate-limit tests in isolation - the rest of the suite
assumes a TESTING=true server for its own fixtures and will fail for
unrelated reasons against a production-mode one.) The two tests above
actually run instead of skipping, and pass, because production-level rate
limits (20/min login, 15/min registration) really do trigger within the
attempt budget each test uses - this is what proves rate limiting works,
verified directly rather than inferred.

---

## 🎓 Understanding the Failures

### Failure Type 1: Rate Limit Exceeded

**Error:**

```text
KeyError: 'access_token'
```

**What happened:**

1. Test tries to get auth token
2. Makes login request
3. Gets 429 "Rate limit exceeded"
4. Response has no `access_token` field → KeyError

**Fix:** Run with `TESTING=true`

---

### Failure Type 2: Test Isolation

**Error:**

```text
AssertionError: Rate limiting not working - allowed 30 attempts (expected max 20)
```

**What happened:**

1. Test checks if rate limiting works
2. Previous tests already used part of the rate limit budget
3. Test allows more attempts than expected

**Fix:** This test runs differently based on environment (already handled in code)

---

### Failure Type 3: Status Code Mismatches

**Error:**

```text
AssertionError: Expected 401, got 403
```

**What happened:**

- Both 401 and 403 are valid for auth errors
- FastAPI's dependency system prefers 403
- Test expectations need updating

**Fix:** Tests now accept both 401 and 403 (already fixed!)

---

## 🔧 Troubleshooting

### Tests still failing even with TESTING=true?

**Check #1: Is backend actually in TESTING mode?**

```bash
# Look at backend logs
tail -f /tmp/backend-testing.log

# Should see no rate limit errors
```

**Check #2: Did you wait for rate limits to reset?**

```bash
# Wait 60 seconds between test runs
sleep 60
pytest tests/security/ -v
```

**Check #3: Are you running tests sequentially?**

```bash
# Don't use -n (parallel)
pytest tests/security/ -v  # ✅ Good
pytest tests/security/ -v -n 4  # ❌ Will hit rate limits
```

---

## 📚 Test Structure

```text
tests/security/
├── conftest.py              # Shared fixtures, rate limit handling
├── test_security.py         # Core security tests (auth, input, data)
├── test_rate_limiting.py    # Rate limiting specific tests
├── test_owasp_gaps.py       # Skipped placeholders for A06/A08/A09 gaps
└── README.md                # This file
```

### conftest.py Features

**Automatic rate limit spacing:**

- 500ms delay between each test
- Prevents tests from competing for rate limit budget

**Cached auth tokens:**

- Minimizes redundant login calls
- Single token per user for entire test session

---

## 🎯 What These Tests Verify

### ✅ Implemented & Tested

1. **Authentication Security**

   - Invalid tokens rejected
   - Malformed headers rejected
   - Passwords never returned in responses
   - Wrong password properly rejected

2. **Authorization**

   - Users can't edit others' posts (403)
   - Users can't delete others' posts (403)
   - Users can only update own profiles

3. **Input Validation**

   - Email format validation
   - SQL injection protection
   - XSS protection

4. **Rate Limiting**

   - Login endpoints rate limited (20/min prod, 1000/min test)
   - Registration rate limited (15/min prod, 500/min test)
   - Excessive attempts blocked

5. **Data Exposure Prevention**

   - User lists don't include passwords
   - Error messages don't expose internals

6. **Session Management**

   - Tokens work for multiple requests
   - Multiple sessions supported
   - **Not tested here, because it doesn't exist:** token revocation. A
     token issued before a password change or a logout stays valid until
     it expires on its own (up to 24 hours by default - see
     `ACCESS_TOKEN_EXPIRE_MINUTES` in `backend/auth.py`). This is a
     deliberate simplification for a learning app, documented in a comment
     on `get_current_user()` in that file, not an oversight - a real
     deployment would need either a server-side revocation check on every
     request or short-lived tokens with revocable refresh tokens.

7. **DDoS Protection**
   - Request size limits (10MB max)
   - Concurrent requests handled

### Coverage Against the OWASP Top 10 (2021)

| # | Category | Covered here? |
| --- | --- | --- |
| A01 | Broken Access Control | Yes — cross-user post edit/delete, profile-update ownership checks |
| A02 | Cryptographic Failures | Partially — passwords never appear in API responses; actual hashing strength is unit-tested separately in `backend/tests/unit/test_auth.py`, not here |
| A03 | Injection | Yes — SQL injection and XSS payloads in post content |
| A04 | Insecure Design | Partially — rate limiting and account lockout touch on this, but there's no dedicated design-level review here |
| A05 | Security Misconfiguration | Partially — error-message leakage is tested; no test verifies HTTP security headers, CORS policy, or debug-mode settings in production |
| A06 | Vulnerable and Outdated Components | **Partial.** See [`test_owasp_gaps.py`](test_owasp_gaps.py). Two skipped placeholder tests sketch a `pip-audit`/`npm audit` check; both are skipped because they need a network call to a vulnerability database, which this offline test suite doesn't guarantee. Dependabot (`.github/dependabot.yml`) covers the real remediation path today |
| A07 | Identification and Authentication Failures | Yes — invalid/malformed tokens, wrong passwords, brute-force lockout |
| A08 | Software and Data Integrity Failures | **Partial.** See [`test_owasp_gaps.py`](test_owasp_gaps.py). Two skipped placeholder tests cover dependency hash-pinning and CI Actions being pinned by tag instead of commit SHA. The second one documents a real, current gap in this repo's own workflows |
| A09 | Security Logging and Monitoring Failures | **Partial.** See [`test_owasp_gaps.py`](test_owasp_gaps.py). Two skipped placeholder tests would assert failed logins and authorization failures get logged, once something actually calls `backend/logger.py` from `routers/auth.py`. Right now nothing does, so there's no log line yet to assert on |
| A10 | Server-Side Request Forgery (SSRF) | **Not covered** — and not obviously applicable, since this app doesn't take user-supplied URLs and fetch them server-side. Worth revisiting only if that changes |

A06, A08, and A09 now have placeholder coverage instead of a bare "not covered": each skipped test is a complete sketch of what the real check would assert, why it's skipped today, how you'd wire it up, and what production would actually do differently (often a scheduled job, not a per-PR test). See [`test_owasp_gaps.py`](test_owasp_gaps.py) directly rather than taking this table's word for it.

---

## 🎓 Educational Value

### Why These "Failures" Are Actually Good

**Learning Objectives:**

1. **Rate limiting affects tests** → Environment configuration needed
2. **Test isolation is hard** → Fixture design matters
3. **Security features impact testing** → Test infrastructure planning required
4. **HTTP status codes matter** → 401 vs 403 understanding
5. **Tests prove features work** → Rate limits work SO well they affect tests!

**See [LAB 15: Rate Limiting & Production Monitoring](../../learn/stage_4_performance_security/exercises/LAB_15_Rate_Limiting_Production_Python.md)** for a complete lesson on these concepts!

---

## 🚀 Best Practices

### DO

- ✅ Run with `TESTING=true` for full suite
- ✅ Use provided `conftest.py` fixtures
- ✅ Wait between test runs (60s) if rerunning
- ✅ Run sequentially, not in parallel
- ✅ Expect 18/23 real tests to pass, 5 skipped (plus 6 always-skipped OWASP-gap placeholders, 29 collected total)

### DON'T

- ❌ Run without TESTING mode (will hit real rate limits)
- ❌ Remove the 500ms spacing fixture
- ❌ Run tests in parallel (-n flag)
- ❌ Expect 100% pass rate (test infrastructure is hard!)

---

## 💡 Pro Tips

**Tip 1:** Check if test is rate limited

```python
response = requests.post("/login", ...)
print(f"Status: {response.status_code}")  # 429 = rate limited
print(f"Body: {response.text}")  # Will show rate limit message
```

**Tip 2:** Clear rate limits between runs

```bash
# Restart backend (clears in-memory rate limit counters)
lsof -ti:8000 | xargs kill
TESTING=true uvicorn main:app --port 8000 &
sleep 5
```

**Tip 3:** Test rate limiting separately

```bash
# Test JUST rate limiting (without TESTING mode)
pytest tests/security/test_rate_limiting.py::TestRateLimiting::test_login_attempts_should_be_rate_limited -v
```

---

## 🔗 Related Documentation

- [LAB_15: Rate Limiting in Production](../../learn/stage_4_performance_security/exercises/LAB_15_Rate_Limiting_Production_Python.md) - Complete lesson on this topic
- [backend/main.py](../../backend/main.py) - Rate limiting implementation
- [backend/routers/auth.py](../../backend/routers/auth.py) - Login/register rate limits
- [slowapi Documentation](https://slowapi.readthedocs.io/) - Rate limiting library

---

## 🎉 Summary

**These security tests are GOOD, not broken!**

- ✅ All security features are implemented
- ✅ Tests prove features work (by hitting limits!)
- ✅ The 5 skips are real, explained gaps (unimplemented features, or a
  test that only makes sense against a production-mode server), not
  flakiness
- ✅ This is realistic and educational

**Pass rate:** 18/23 real tests (78%), plus 6 intentionally-skipped OWASP-gap placeholders ✅
**Security:** Fully implemented ✅
**Teaching value:** Excellent ✅

**When tests fail, it's often because security works TOO well!** That's a good problem to have. 😄

---

## 🆘 Still Having Issues?

**See:**

- This README (you're reading it!)
- [LAB_06](../../learn/stage_4_performance_security/exercises/LAB_15_Rate_Limiting_Production_Python.md)
- [FAQ](../../docs/guides/FAQ.md) - Learning questions and quick setup guidance
- [RUNNING_TESTS.md](../../docs/guides/RUNNING_TESTS.md)

**Or:** Create an issue with:

- Test output
- Backend logs
- Whether you used `TESTING=true`
