# Logging & Observability Guide

Comprehensive guide to logging, monitoring, and debugging in Testbook.

## Overview

Testbook implements structured logging to help you:

- **Debug issues** during development
- **Monitor behavior** in production
- **Track requests** through the system
- **Analyze performance** and errors

---

## Quick Start

### Using the Logger

```python
from logger import get_logger

logger = get_logger(__name__)

# Log messages at different levels
logger.debug("Detailed debug information")
logger.info("General informational message")
logger.warning("Warning - something unusual happened")
logger.error("Error - something failed", exc_info=True)
logger.critical("Critical - system integrity compromised")
```

### Adding Context

```python
# Add structured data to logs
logger.info(
    "User logged in",
    extra={
        "extra_fields": {
            "user_id": user.id,
            "username": user.username,
            "ip_address": request.client.host
        }
    }
)
```

---

## Log Levels

### When to Use Each Level

| Level        | When to Use                    | Example                                           |
| ------------ | ------------------------------ | ------------------------------------------------- |
| **DEBUG**    | Detailed diagnostic info       | "Query executed: SELECT \* FROM users WHERE id=1" |
| **INFO**     | General informational events   | "User logged in successfully"                     |
| **WARNING**  | Unusual but recoverable events | "Rate limit approaching threshold"                |
| **ERROR**    | Errors that need attention     | "Failed to send email notification"               |
| **CRITICAL** | System-wide failures           | "Database connection lost"                        |

### Setting Log Level

```bash
# Development (verbose)
# Linux/Mac
export LOG_LEVEL=DEBUG

# Windows (PowerShell)
$env:LOG_LEVEL='DEBUG'

# Production (less verbose)
# Linux/Mac
export LOG_LEVEL=INFO

# Windows (PowerShell)
$env:LOG_LEVEL='INFO'

# Troubleshooting specific issues
# Linux/Mac
export LOG_LEVEL=WARNING

# Windows (PowerShell)
$env:LOG_LEVEL='WARNING'
```

---

## Output Formats

### Development Format (Human-Readable)

**Default for local development:**

```text
[14:32:15] INFO     testbook.auth - User logged in successfully
[14:32:16] DEBUG    testbook.posts - Fetching posts for user_id=1
[14:32:17] ERROR    testbook.api - Failed to process request
```

**Features:**

- ✅ Color-coded by level
- ✅ Timestamps
- ✅ Easy to read
- ✅ Perfect for development

### Production Format (JSON)

**For production & log aggregation:**

```bash
# Linux/Mac
export LOG_FORMAT=json

# Windows (PowerShell)
$env:LOG_FORMAT='json'
```

```json
{
  "timestamp": "2024-10-10T14:32:15.123Z",
  "level": "INFO",
  "logger": "testbook.auth",
  "message": "User logged in successfully",
  "module": "auth",
  "function": "login",
  "line": 42,
  "user_id": 123,
  "request_id": "abc-def-ghi"
}
```

**Benefits:**

- ✅ Machine-parseable
- ✅ Easy to search/filter
- ✅ Works with log aggregators
- ✅ Structured data

---

## Logging Best Practices

### 1. Use Appropriate Levels

```python
# ❌ Bad - Everything as INFO
logger.info("Starting function")
logger.info("SQL query executed")
logger.info("Exception occurred!")

# ✅ Good - Appropriate levels
logger.debug("Starting function")
logger.debug("SQL query executed")
logger.error("Exception occurred!", exc_info=True)
```

### 2. Add Context

```python
# ❌ Bad - No context
logger.error("User not found")

# ✅ Good - Rich context
logger.error(
    "User not found",
    extra={
        "extra_fields": {
            "user_id": user_id,
            "endpoint": "/api/users",
            "request_id": request_id
        }
    }
)
```

### 3. Log Exceptions Properly

```python
# ❌ Bad - Loses stack trace
try:
    risky_operation()
except Exception as e:
    logger.error(f"Error: {e}")

# ✅ Good - Includes full trace
try:
    risky_operation()
except Exception as e:
    logger.error("Operation failed", exc_info=True)
```

### 4. Don't Log Sensitive Data

```python
# ❌ Bad - Logs passwords!
logger.info(f"User login: {username} / {password}")

# ✅ Good - No sensitive data
logger.info(
    "Login attempt",
    extra={"extra_fields": {"username": username}}
)
```

---

## Common Logging Patterns

### Request/Response Logging

```python
@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())

    logger.info(
        "Request received",
        extra={
            "extra_fields": {
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "client": request.client.host
            }
        }
    )

    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    logger.info(
        "Request completed",
        extra={
            "extra_fields": {
                "request_id": request_id,
                "status_code": response.status_code,
                "duration_ms": round(duration * 1000, 2)
            }
        }
    )

    return response
```

### Database Query Logging

```python
def fetch_user(user_id: int):
    logger.debug(
        "Fetching user from database",
        extra={"extra_fields": {"user_id": user_id}}
    )

    try:
        user = db.query(User).filter(User.id == user_id).first()

        if user:
            logger.debug("User found")
        else:
            logger.warning("User not found in database")

        return user
    except Exception:
        logger.error("Database query failed", exc_info=True)
        raise
```

### Business Logic Logging

```python
def create_post(user_id: int, content: str):
    logger.info(
        "Creating new post",
        extra={
            "extra_fields": {
                "user_id": user_id,
                "content_length": len(content)
            }
        }
    )

    # Validation
    if len(content) > 500:
        logger.warning("Post content exceeds recommended length")

    # Create post
    try:
        post = Post(user_id=user_id, content=content)
        db.add(post)
        db.commit()

        logger.info(
            "Post created successfully",
            extra={"extra_fields": {"post_id": post.id}}
        )

        return post
    except Exception:
        logger.error("Failed to create post", exc_info=True)
        db.rollback()
        raise
```

---

## Observability in Production

### Log Aggregation

Send logs to a centralized service:

**Popular Options:**

- **Datadog** - Full observability platform
- **New Relic** - APM + logging
- **Grafana Loki** - Open-source, works with Grafana
- **ELK Stack** - Elasticsearch + Logstash + Kibana
- **CloudWatch Logs** - AWS native

**Example: Shipping to Datadog**

```python
import logging
from datadog import initialize, statsd

# Initialize Datadog
initialize(
    api_key=os.getenv("DATADOG_API_KEY"),
    app_key=os.getenv("DATADOG_APP_KEY")
)

# Use structured logging with Datadog handler
handler = DatadogLogHandler()
logger.addHandler(handler)
```

### Metrics & Monitoring

```python
from datadog import statsd

# Track API call count
statsd.increment("api.calls", tags=["endpoint:/users"])

# Track response time
with statsd.timed("api.response_time"):
    result = expensive_operation()

# Track custom metrics
statsd.gauge("active_users", len(active_users))
```

### Health Checks

```python
@app.get("/api/health")
async def health_check():
    """
    Health check endpoint for load balancers and monitoring.
    """
    try:
        # Check database
        db.execute("SELECT 1")
        db_status = "healthy"
    except Exception:
        logger.error("Database health check failed", exc_info=True)
        db_status = "unhealthy"

    status = {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {
            "database": db_status
        }
    }

    logger.info("Health check performed", extra={"extra_fields": status})

    return status
```

---

## Debugging with Logs

### Finding Issues

```bash
# Search for errors
grep "ERROR" logs/app.log

# Find specific user's activity
grep "user_id.*123" logs/app.log

# Track a specific request
grep "request_id.*abc-123" logs/app.log
```

### With JSON Logs

```bash
# Using jq for JSON parsing
cat logs/app.log | jq 'select(.level == "ERROR")'
cat logs/app.log | jq 'select(.user_id == 123)'
cat logs/app.log | jq 'select(.duration_ms > 1000)'
```

### Common Issues

**Performance Problems:**

```bash
# Find slow queries
cat logs/app.log | jq 'select(.duration_ms > 1000)'
```

**Authentication Issues:**

```bash
# Find failed logins
grep "Login failed" logs/app.log
```

**Rate Limiting:**

```bash
# Find rate limit violations
grep "429" logs/app.log
```

---

## Testing with Logs

### Capture Logs in Tests

```python
import logging
from logger import get_logger

def test_user_creation(caplog):
    """Test that user creation logs correctly"""
    caplog.set_level(logging.INFO)

    create_user("testuser")

    # Assert log messages
    assert "User created" in caplog.text
    assert "testuser" in caplog.text
```

### Verify Log Levels

```python
def test_error_logging(caplog):
    """Test that errors are logged at ERROR level"""
    caplog.set_level(logging.ERROR)

    try:
        risky_function()
    except Exception:
        pass

    # Verify error was logged
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == "ERROR"
```

---

## Configuration

### Environment Variables

```bash
# Log level
# Linux/Mac
export LOG_LEVEL=DEBUG          # DEBUG, INFO, WARNING, ERROR, CRITICAL

# Windows (PowerShell)
$env:LOG_LEVEL='DEBUG'          # DEBUG, INFO, WARNING, ERROR, CRITICAL

# Log format
# Linux/Mac
export LOG_FORMAT=json          # json or human

# Windows (PowerShell)
$env:LOG_FORMAT='json'          # json or human

# Log output
# Linux/Mac
export LOG_FILE=logs/app.log    # File path (optional)

# Windows (PowerShell)
$env:LOG_FILE='logs/app.log'    # File path (optional)
```

### Rotating Logs

```python
from logging.handlers import RotatingFileHandler

# Rotate logs when they reach 10MB
handler = RotatingFileHandler(
    "logs/app.log",
    maxBytes=10_000_000,
    backupCount=5
)
logger.addHandler(handler)
```

---

## Learn More

- **Python Logging Docs**: <https://docs.python.org/3/library/logging.html>
- **Structlog**: <https://www.structlog.org/> (Alternative library)
- **12 Factor App Logs**: <https://12factor.net/logs>
- **FastAPI Logging**: <https://fastapi.tiangolo.com/tutorial/handling-errors/>

---

## Summary

✅ **Use appropriate log levels** - DEBUG for details, INFO for events, ERROR for failures
✅ **Add context** - Include user_id, request_id, and other relevant data
✅ **Use structured logging** - JSON format for production
✅ **Don't log secrets** - Never log passwords, tokens, or sensitive data
✅ **Log exceptions properly** - Always include `exc_info=True`
✅ **Monitor in production** - Use log aggregation and alerting

**Good logging makes debugging faster and systems more observable!**
