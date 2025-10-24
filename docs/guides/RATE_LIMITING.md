# Rate Limiting Configuration Guide

Comprehensive guide to understanding, configuring, and testing rate limiting in Testbook.

## Overview

Testbook uses **SlowAPI** (built on top of the popular `slowapi` library) to protect against:

- Denial of Service (DoS) attacks
- Brute force authentication attempts
- API abuse and resource exhaustion
- Unintentional DDOS from buggy clients

---

## Current Configuration

### Environment-Based Limits

The app automatically adjusts rate limits based on the `TESTING` environment variable:

```python
# backend/main.py

TESTING_MODE = os.getenv("TESTING", "false").lower() == "true"

if TESTING_MODE:
    # Testing mode: High limits to prevent test failures
    limiter = Limiter(key_func=get_remote_address, default_limits=["1000/minute"])
else:
    # Production mode: Reasonable security limits
    limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])
```

### Default Limits

| Environment     | Default Limit | Use Case                     |
| --------------- | ------------- | ---------------------------- |
| **Development** | 100/minute    | Local testing, normal usage  |
| **Testing**     | 1000/minute   | Automated tests, CI/CD       |
| **Production**  | 100/minute    | Real users, security-focused |

---

## Per-Endpoint Configuration

### Example: Custom Limits for Specific Endpoints

**Note:** Testbook currently uses environment-based default limits (100/minute in production, 1000/minute in testing). The examples below show how you _could_ implement per-endpoint limits if needed.

```python
from slowapi import Limiter
from fastapi import Request

@app.get("/api/health")
@limiter.limit("100/minute")  # Health checks can be frequent
async def health_check(request: Request):
    return {"status": "healthy"}

@app.post("/api/auth/login")
@limiter.limit("20/minute")  # Login attempts should be restricted
async def login(request: Request, credentials: LoginRequest):
    # Authentication logic (Testbook uses environment-based limits)
    pass

@app.post("/api/posts")
@limiter.limit("30/minute")  # Prevent spam posting
async def create_post(request: Request, post_data: PostCreate):
    # Post creation logic (Testbook uses environment-based limits)
    pass
```

**Testbook's Actual Implementation:**

- Default limit: 100 requests/minute (production)
- Testing mode: 1000 requests/minute (when `TESTING=true`)
- Login/Register: Uses environment-based rates (20/min in production, 100/min in testing)
- See `backend/routers/auth.py` for actual implementation

### Recommended Limits by Endpoint Type

| Endpoint Type       | Suggested Limit | Reasoning                        |
| ------------------- | --------------- | -------------------------------- |
| **Authentication**  | 5-10/minute     | Prevent brute force attacks      |
| **Read-only (GET)** | 100-200/minute  | Allow normal browsing            |
| **Create/Update**   | 10-30/minute    | Prevent spam, abuse              |
| **Search/Filter**   | 30-50/minute    | Resource-intensive operations    |
| **Health Checks**   | 100-200/minute  | Monitoring tools need access     |
| **File Uploads**    | 5-10/minute     | Large payloads, storage concerns |

---

## Tuning Rate Limits

### 1. Identify Your Requirements

**Questions to ask:**

- How many requests do legitimate users make per minute?
- What's acceptable during peak traffic?
- What's the cost of false positives (blocking real users)?
- What's the impact of an attack?

### 2. Monitor Current Usage

```python
# Add logging to track request patterns
from logger import get_logger

logger = get_logger(__name__)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)

    # Log rate limit headers
    remaining = response.headers.get("X-RateLimit-Remaining")
    logger.info(
        "Request processed",
        extra={
            "extra_fields": {
                "path": request.url.path,
                "method": request.method,
                "rate_limit_remaining": remaining
            }
        }
    )

    return response
```

### 3. Adjust Limits Gradually

```python
# Start conservative
@router.post("/api/posts")
@limiter.limit("5/minute")  # Very restrictive
async def create_post(request: Request):
    pass

# Monitor for false positives, then increase
@router.post("/api/posts")
@limiter.limit("10/minute")  # Slightly relaxed
async def create_post(request: Request):
    pass

# Find the sweet spot
@router.post("/api/posts")
@limiter.limit("15/minute")  # Balanced
async def create_post(request: Request):
    pass
```

---

## Advanced Configuration

### User-Based Rate Limiting

```python
def get_user_identifier(request: Request) -> str:
    """
    Use user ID for authenticated requests, IP for anonymous.
    Prevents one user on shared IP from affecting others.
    """
    user = getattr(request.state, "user", None)
    if user:
        return f"user:{user.id}"
    return f"ip:{request.client.host}"

# Apply to limiter
limiter = Limiter(key_func=get_user_identifier)
```

### Multiple Rate Limit Windows

```python
@router.post("/api/auth/login")
@limiter.limit("5/minute")   # 5 per minute
@limiter.limit("20/hour")    # 20 per hour
@limiter.limit("50/day")     # 50 per day
async def login(request: Request):
    """
    Multiple limits prevent sustained attacks.
    Attackers can't just wait 60 seconds and retry.
    """
    pass
```

### Dynamic Rate Limiting

```python
def get_dynamic_limit(request: Request) -> str:
    """
    Adjust limits based on user tier, time of day, etc.
    """
    user = getattr(request.state, "user", None)

    if user and user.is_premium:
        return "200/minute"  # Premium users get higher limits
    elif user:
        return "100/minute"  # Regular authenticated users
    else:
        return "50/minute"   # Anonymous users (most restrictive)

@router.get("/api/feed")
@limiter.limit(get_dynamic_limit)
async def get_feed(request: Request):
    pass
```

---

## Testing Rate Limits

### Manual Testing

```bash
# Test rate limit with curl
for i in {1..10}; do
  curl -s -w "Status: %{http_code}\n" http://localhost:8000/api/posts
  sleep 0.5
done
```

### Automated Tests

```python
# tests/test_rate_limiting.py

def test_rate_limit_exceeded(client):
    """Test that rate limits are enforced"""
    endpoint = "/api/posts"

    # Make requests up to the limit
    for i in range(10):
        response = client.get(endpoint)
        assert response.status_code == 200

    # Next request should be rate limited
    response = client.get(endpoint)
    assert response.status_code == 429
    assert "rate limit exceeded" in response.json()["detail"].lower()


def test_rate_limit_headers(client):
    """Test that rate limit headers are present"""
    response = client.get("/api/health")

    assert "X-RateLimit-Limit" in response.headers
    assert "X-RateLimit-Remaining" in response.headers
    assert "X-RateLimit-Reset" in response.headers
```

See `LAB_06_Testing_With_Rate_Limits.md` for comprehensive testing examples.

---

## Monitoring & Alerting

### Track Rate Limit Violations

```python
from logger import get_logger

logger = get_logger(__name__)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """
    Custom handler for rate limit violations.
    Log incidents for security monitoring.
    """
    logger.warning(
        "Rate limit exceeded",
        extra={
            "extra_fields": {
                "ip": request.client.host,
                "path": request.url.path,
                "user_agent": request.headers.get("user-agent")
            }
        }
    )

    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Please try again later."}
    )
```

### Dashboard Metrics

```python
# Track rate limit metrics
rate_limit_violations = Counter(
    "rate_limit_violations_total",
    "Number of rate limit violations",
    ["endpoint", "user_type"]
)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    user_type = "authenticated" if request.state.user else "anonymous"
    rate_limit_violations.labels(
        endpoint=request.url.path,
        user_type=user_type
    ).inc()

    # Return 429 response
    return JSONResponse(...)
```

---

## Common Issues & Solutions

### Issue: Tests Failing Due to Rate Limits

**Solution:** Always set `TESTING=true` when running tests.

```bash
# In test environment
# Linux/Mac
export TESTING=true
pytest -v

# Windows (PowerShell)
$env:TESTING='true'; pytest -v
```

Or in `conftest.py`:

```python
@pytest.fixture(autouse=True)
def set_testing_mode(monkeypatch):
    monkeypatch.setenv("TESTING", "true")
```

### Issue: Legitimate Users Getting Blocked

**Symptoms:**

- 429 errors during normal usage
- Complaints from power users
- High false positive rate

**Solution:** Increase limits gradually

```python
# Before
@limiter.limit("10/minute")

# After
@limiter.limit("30/minute")
```

### Issue: Shared IPs (Corporate Networks)

**Problem:** Multiple users behind same IP share limits

**Solution:** Use user-based rate limiting

```python
limiter = Limiter(key_func=get_user_identifier)  # Not IP-based
```

### Issue: Bot Traffic Overwhelming API

**Solution:** More aggressive limits for unauthenticated users

```python
def get_limit(request: Request) -> str:
    if request.state.user:
        return "100/minute"  # Authenticated
    return "20/minute"      # Anonymous (more restricted)
```

---

## Production Recommendations

### 1. Start Conservative

```python
# Initial production limits (safer)
DEFAULT_LIMIT = "50/minute"
AUTH_LIMIT = "5/minute"
READ_LIMIT = "100/minute"
WRITE_LIMIT = "10/minute"
```

### 2. Monitor & Adjust

- Track 429 responses
- Analyze user patterns
- Collect feedback
- Gradually increase if needed

### 3. Use Multiple Windows

```python
@limiter.limit("10/minute")
@limiter.limit("100/hour")
@limiter.limit("500/day")
```

### 4. Implement User Tiers

```python
if user.is_premium:
    limit = "200/minute"
elif user.is_authenticated:
    limit = "100/minute"
else:
    limit = "50/minute"
```

### 5. Alert on Violations

Set up alerts for:

- Sustained 429 errors from single IP
- Unusual spike in rate limit violations
- Specific endpoints being hammered

---

## Configuration Reference

### Environment Variables

```bash
# Core settings
# Linux/Mac
export TESTING=true              # Enable high limits for tests
export RATE_LIMIT_STORAGE=memory # memory or redis

# Windows (PowerShell)
$env:TESTING='true'              # Enable high limits for tests
$env:RATE_LIMIT_STORAGE='memory' # memory or redis

# Custom limits (if implemented)
export DEFAULT_RATE_LIMIT=100/minute
export AUTH_RATE_LIMIT=5/minute
export API_RATE_LIMIT=50/minute
```

### Storage Backends

**Memory (Default):**

- ✅ Simple, no dependencies
- ❌ Doesn't work with multiple processes
- ✅ Perfect for development

**Redis (Production):**

- ✅ Works with multiple processes
- ✅ Persistent across restarts
- ❌ Requires Redis server

```python
# Using Redis backend
from slowapi.util import get_remote_address
from slowapi import Limiter

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="redis://localhost:6379"
)
```

---

## Learn More

- **SlowAPI Docs**: <https://slowapi.readthedocs.io/>
- **LAB_06**: Testing With Rate Limits (practical exercises)
- **Flask-Limiter**: <https://flask-limiter.readthedocs.io/> (similar concepts)

---

## Summary

✅ **Use environment-based configuration** - Different limits for dev/test/prod
✅ **Start conservative** - Easier to relax than to tighten
✅ **Monitor violations** - Track 429 responses and patterns
✅ **Test thoroughly** - Use LAB_06 exercises
✅ **User-based limits** - Don't penalize whole networks
✅ **Multiple windows** - Prevent sustained attacks

**Rate limiting is a balance between security and user experience!**
