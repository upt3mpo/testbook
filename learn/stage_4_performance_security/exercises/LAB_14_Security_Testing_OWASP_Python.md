# 🧪 Lab 14: Security Testing & OWASP

**Estimated Time:** 120 minutes<br>
**Difficulty:** Advanced<br>
**Language:** 🐍 Python<br>
**Prerequisites:** Lab 13 completed

**💡 Need JavaScript instead?** Try [Lab 14: Security Testing & OWASP (JavaScript)](LAB_14_Security_Testing_OWASP_JavaScript.md)!

**What This Adds:** Master security testing with pytest to identify vulnerabilities and ensure your application is protected against common attacks like SQL injection, XSS, and CSRF. This is essential for production applications.

---

## 🎯 What You'll Learn

- **OWASP Top 10** - Understand common web application vulnerabilities
- **Security testing techniques** - Test for SQL injection, XSS, CSRF, and more
- **Authentication security** - Test password policies, session management
- **API security** - Test for authorization bypasses and data exposure
- **Security scanning** - Use automated tools to find vulnerabilities
- **Security best practices** - Implement secure coding patterns

---

## 📋 Why Security Testing Matters

**The Problem:**

- Applications vulnerable to common attacks
- Sensitive data exposed through APIs
- Authentication bypasses allow unauthorized access
- No systematic way to test security

**The Solution:**
Security testing systematically identifies vulnerabilities and ensures proper security controls are in place.

---

## 📋 Step-by-Step Instructions

> **Before you start:** These exercises hit a running Testbook backend, so start it in test mode first: `TESTING=true uvicorn main:app --reload --port 8000` (see `../../../docs/guides/PLAYWRIGHT_QUICKSTART.md` for why — it unlocks the `/api/dev/reset` endpoint and relaxes rate limits to 1000/min so your new tests aren't cut off by the real 20/min production login limit). Testbook already ships a working security suite you can run as-is at `tests/security/test_security.py` and `tests/security/test_rate_limiting.py` (fixtures in `tests/security/conftest.py`) — it's plain `pytest` + the `requests` library hitting `http://localhost:8000/api` over HTTP, **not** `fastapi.testclient.TestClient` with a `db_session` fixture as shown below. The code in this lab uses the in-process `TestClient`/`db_session` pattern as an alternative teaching style (it assumes fixtures — `client`, `db_session`, `test_user` — that aren't defined here or anywhere in this repo; treat it as illustrative pseudocode to adapt, not copy-paste-ready code). If you want tests that actually run against Testbook as it exists today, mirror `tests/security/conftest.py` instead: a `requests.Session()` against the live server.

### Part 1: OWASP Top 10 Testing (40 minutes)

#### Step 1: Install Security Testing Tools

```bash
cd backend
pip install bandit safety semgrep
```

#### Step 2: Test for SQL Injection (A01:2021 - Broken Access Control)

Create `tests/security/test_sql_injection.py`:

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from models import User, Post
from auth import get_password_hash

class TestSQLInjection:
    """Test for SQL injection vulnerabilities."""

    def test_login_sql_injection(self, client: TestClient, db_session: Session):
        """Test login endpoint for SQL injection."""
        # Create a test user
        user = User(
            email="test@example.com",
            username="testuser",
            display_name="Test User",
            hashed_password=get_password_hash("password123")
        )
        db_session.add(user)
        db_session.commit()

        # Test SQL injection in email field
        sql_injection_payloads = [
            "test@example.com' OR '1'='1",
            "test@example.com'; DROP TABLE users; --",
            "test@example.com' UNION SELECT * FROM users --",
            "test@example.com' OR 1=1 --",
        ]

        for payload in sql_injection_payloads:
            response = client.post("/api/auth/login", json={
                "email": payload,
                "password": "password123"
            })

            # NOTE: Testbook's login schema types `email` as pydantic `EmailStr`
            # (see backend/schemas.py), so a malformed string like the payloads
            # above usually fails format validation before it ever reaches a
            # query — that's a 422, not a 401. Neither is a 500, which is the
            # actual thing we're testing for. Real tests/security/test_security.py
            # asserts `status_code in [401, 422]` for exactly this reason.
            assert response.status_code in [401, 422], f"SQL injection payload '{payload}' should return 401 or 422, got {response.status_code}"

            # Should not expose database errors. NOTE: on a 422, `detail` is a
            # list of validation-error objects, not a string — normalize first.
            response_data = response.json()
            detail = response_data.get("detail", "")
            detail_text = str(detail).lower()
            assert "sql" not in detail_text
            assert "database" not in detail_text

    def test_user_search_sql_injection(self, client: TestClient, db_session: Session):
        """Test user search endpoint for SQL injection.

        NOTE: Testbook doesn't currently expose a `/api/users/search` endpoint
        (see `backend/routers/users.py` — it has `/{username}`, `/{username}/followers`,
        `/{username}/following`, but no query-based search). Adapt this pattern to
        whatever endpoint accepts free-text/user-controlled input in your app.
        """
        # Create test users
        users = [
            User(email="user1@example.com", username="user1", display_name="User 1", hashed_password=get_password_hash("password")),
            User(email="user2@example.com", username="user2", display_name="User 2", hashed_password=get_password_hash("password")),
        ]
        for user in users:
            db_session.add(user)
        db_session.commit()

        # Test SQL injection in search parameter
        sql_injection_payloads = [
            "user' OR '1'='1",
            "user'; DROP TABLE users; --",
            "user' UNION SELECT * FROM users --",
        ]

        for payload in sql_injection_payloads:
            response = client.get(f"/api/users/search?q={payload}")

            # Should return 400 (bad request) or empty results, not 500
            assert response.status_code in [200, 400], f"SQL injection payload '{payload}' should return 200 or 400, got {response.status_code}"

            if response.status_code == 200:
                # Should not return all users (which would indicate successful injection)
                data = response.json()
                assert len(data.get("users", [])) == 0, f"SQL injection payload '{payload}' should return empty results"

    def test_post_content_sql_injection(self, client: TestClient, db_session: Session, test_user):
        """Test post creation for SQL injection in content.

        NOTE: Testbook's `PostCreate` schema (backend/schemas.py) only has
        `content`, `image_url`, `video_url` — no `title`. Pydantic silently
        drops unknown fields by default, so passing `"title"` below won't error,
        it's just dead weight; feel free to drop it. Same applies to every
        other `/api/posts` call in this lab that includes a `title`.
        """
        # Login first
        login_response = client.post("/api/auth/login", json={
            "email": test_user.email,
            "password": "password123"
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Test SQL injection in post content
        sql_injection_payloads = [
            "Normal post'; DROP TABLE posts; --",
            "Post' OR '1'='1",
            "Post'; INSERT INTO posts (content) VALUES ('Hacked'); --",
        ]

        for payload in sql_injection_payloads:
            response = client.post("/api/posts", json={
                "title": "Test Post",
                "content": payload
            }, headers=headers)

            # Should return 201 (created) or 400 (bad request), not 500
            assert response.status_code in [201, 400], f"SQL injection payload '{payload}' should return 201 or 400, got {response.status_code}"

            # Verify the malicious SQL was not executed
            if response.status_code == 201:
                # Check that no extra posts were created
                posts_count = db_session.query(Post).count()
                assert posts_count == 1, "SQL injection should not create extra posts"
```

#### Step 3: Test for Cross-Site Scripting (XSS) (A03:2021 - Injection)

Create `tests/security/test_xss.py`:

```python
import pytest
from fastapi.testclient import TestClient
from html import escape

class TestXSS:
    """Test for Cross-Site Scripting (XSS) vulnerabilities."""

    def test_post_content_xss(self, client: TestClient, test_user):
        """Test post content for XSS vulnerabilities.

        NOTE: Testbook's backend intentionally does NOT sanitize or
        HTML-escape post content — it stores whatever you send as-is, on the
        premise that escaping-on-render is the frontend's job (see
        tests/security/test_security.py::TestInputValidation::test_xss_in_post_content,
        which asserts a 201 and that the raw payload round-trips unchanged).
        Asserting the payload is stripped/escaped at the API layer, as this
        test originally did, would fail against the real app. What actually
        matters for XSS defense here is that the *React frontend* escapes on
        render (JSX does this by default) rather than using
        `dangerouslySetInnerHTML` on untrusted content.
        """
        # Login first
        login_response = client.post("/api/auth/login", json={
            "email": test_user.email,
            "password": "password123"
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Test XSS payloads
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')",
            "<svg onload=alert('XSS')>",
            "';alert('XSS');//",
        ]

        for payload in xss_payloads:
            response = client.post("/api/posts", json={
                "title": "XSS Test Post",
                "content": payload
            }, headers=headers)

            # Should return 201 (created)
            assert response.status_code == 201, f"XSS payload '{payload}' should return 201, got {response.status_code}"

            # Get the created post
            post_id = response.json()["id"]
            get_response = client.get(f"/api/posts/{post_id}", headers=headers)

            # Backend stores content as-is (no server-side sanitization) — the
            # raw payload round-trips unchanged. That's expected here, not a bug.
            content = get_response.json()["content"]
            assert content == payload, f"Backend should store '{payload}' as-is for the frontend to escape on render"

    def test_user_profile_xss(self, client: TestClient, test_user):
        """Test user profile fields for XSS vulnerabilities."""
        # Login first
        login_response = client.post("/api/auth/login", json={
            "email": test_user.email,
            "password": "password123"
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Test XSS in display name
        xss_payload = "<script>alert('XSS')</script>"

        response = client.put("/api/users/me", json={
            "display_name": xss_payload,
            "bio": "Test bio"
        }, headers=headers)

        # Should return 200 (updated)
        assert response.status_code == 200, f"XSS payload in display_name should return 200, got {response.status_code}"

        # NOTE: the "get my profile" route is GET /api/auth/me (see
        # backend/routers/auth.py) — there's no GET /api/users/me in this app
        # (only PUT and DELETE live under /api/users/me).
        # Get updated profile
        profile_response = client.get("/api/auth/me", headers=headers)
        display_name = profile_response.json()["display_name"]

        # Same as post content: Testbook doesn't sanitize server-side, so the
        # raw payload round-trips unchanged (frontend's job to escape on render).
        assert display_name == xss_payload, "Backend should store display_name as-is for the frontend to escape on render"

    def test_search_xss(self, client: TestClient):
        """Test search functionality for XSS vulnerabilities.

        NOTE: same caveat as `test_user_search_sql_injection` above — there's no
        real `/api/users/search` endpoint in Testbook today.
        """
        # Test XSS in search parameter
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')",
        ]

        for payload in xss_payloads:
            response = client.get(f"/api/users/search?q={payload}")

            # Should return 200 (ok) or 400 (bad request)
            assert response.status_code in [200, 400], f"XSS payload '{payload}' should return 200 or 400, got {response.status_code}"

            if response.status_code == 200:
                # Response should not contain unescaped XSS payload
                response_text = response.text
                assert "<script>" not in response_text, f"XSS payload '{payload}' should be escaped in response"
                assert "javascript:" not in response_text, f"XSS payload '{payload}' should be escaped in response"
```

#### Step 4: Test for Cross-Site Request Forgery (CSRF) (A01:2021 - Broken Access Control)

> **Reality check:** Testbook's API is a stateless, bearer-token JSON API — there's no cookie-based session and no `/api/csrf-token` endpoint, so classic CSRF (where a browser auto-attaches a session cookie to a forged cross-site request) doesn't really apply here the way it would to a cookie-session app. `tests/security/test_security.py` does not contain a CSRF test class. The code below is a hypothetical example of how you'd test CSRF token validation *if* the app used cookie sessions — it will 404 against the real Testbook API. Treat it as a conceptual exercise, not a runnable test.

Create `tests/security/test_csrf.py`:

```python
import pytest
from fastapi.testclient import TestClient

class TestCSRF:
    """Test for Cross-Site Request Forgery (CSRF) vulnerabilities."""

    def test_csrf_protection_on_state_changing_operations(self, client: TestClient, test_user):
        """Test that state-changing operations require CSRF protection."""
        # Login first
        login_response = client.post("/api/auth/login", json={
            "email": test_user.email,
            "password": "password123"
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Test operations that should be protected against CSRF
        state_changing_operations = [
            ("POST", "/api/posts", {"title": "Test Post", "content": "Test content"}),
            ("PUT", "/api/users/me", {"display_name": "New Name"}),
            ("DELETE", "/api/posts/1", {}),
        ]

        for method, endpoint, data in state_changing_operations:
            # Test without CSRF token (should fail)
            response = client.request(method, endpoint, json=data, headers=headers)

            # Should return 403 (forbidden) or 400 (bad request) for CSRF protection
            assert response.status_code in [403, 400], f"{method} {endpoint} should require CSRF protection, got {response.status_code}"

    def test_csrf_token_validation(self, client: TestClient, test_user):
        """Test CSRF token validation."""
        # Login first
        login_response = client.post("/api/auth/login", json={
            "email": test_user.email,
            "password": "password123"
        })
        token = login_response.json()["access_token"]

        # Get CSRF token
        csrf_response = client.get("/api/csrf-token", headers={"Authorization": f"Bearer {token}"})
        assert csrf_response.status_code == 200
        csrf_token = csrf_response.json()["csrf_token"]

        headers = {
            "Authorization": f"Bearer {token}",
            "X-CSRF-Token": csrf_token
        }

        # Test with valid CSRF token (should succeed)
        response = client.post("/api/posts", json={
            "title": "Test Post",
            "content": "Test content"
        }, headers=headers)

        assert response.status_code == 201, f"POST with valid CSRF token should succeed, got {response.status_code}"

        # Test with invalid CSRF token (should fail)
        invalid_headers = {
            "Authorization": f"Bearer {token}",
            "X-CSRF-Token": "invalid_token"
        }

        response = client.post("/api/posts", json={
            "title": "Test Post 2",
            "content": "Test content 2"
        }, headers=invalid_headers)

        assert response.status_code == 403, f"POST with invalid CSRF token should fail, got {response.status_code}"
```

---

### Part 2: Authentication and Authorization Security (30 minutes)

#### Step 1: Test Password Security

Create `tests/security/test_password_security.py`:

```python
import pytest
from fastapi.testclient import TestClient
import re

class TestPasswordSecurity:
    """Test password security policies.

    NOTE: Testbook's real `/api/auth/register` (backend/routers/auth.py) does
    not enforce password strength today — any non-empty string is accepted, so
    it would return 201, not 400, for every password below. This class is a
    spec for a policy you could add and test-drive, not a description of the
    app's current behavior.
    """

    def test_weak_password_rejection(self, client: TestClient):
        """Test that weak passwords are rejected."""
        weak_passwords = [
            "123456",
            "password",
            "12345678",
            "qwerty",
            "abc123",
            "password123",
            "admin",
            "letmein",
            "welcome",
            "monkey",
        ]

        for password in weak_passwords:
            response = client.post("/api/auth/register", json={
                "email": f"test{password}@example.com",
                "username": f"user{password}",
                "display_name": "Test User",
                "password": password
            })

            # Should return 400 (bad request) for weak passwords
            assert response.status_code == 400, f"Weak password '{password}' should be rejected, got {response.status_code}"

            response_data = response.json()
            assert "password" in response_data.get("detail", "").lower()

    def test_password_complexity_requirements(self, client: TestClient):
        """Test password complexity requirements."""
        # Test passwords missing required complexity
        invalid_passwords = [
            "short",  # Too short
            "nouppercase123!",  # No uppercase
            "NOLOWERCASE123!",  # No lowercase
            "NoNumbers!",  # No numbers
            "NoSpecialChars123",  # No special characters
        ]

        for password in invalid_passwords:
            response = client.post("/api/auth/register", json={
                "email": f"test{password}@example.com",
                "username": f"user{password}",
                "display_name": "Test User",
                "password": password
            })

            # Should return 400 (bad request)
            assert response.status_code == 400, f"Invalid password '{password}' should be rejected, got {response.status_code}"

        # Test valid password
        valid_password = "ValidPassword123!"
        response = client.post("/api/auth/register", json={
            "email": "test@example.com",
            "username": "testuser",
            "display_name": "Test User",
            "password": valid_password
        })

        # Should return 201 (created)
        assert response.status_code == 201, f"Valid password should be accepted, got {response.status_code}"

    def test_password_brute_force_protection(self, client: TestClient, db_session):
        """Test protection against password brute force attacks."""
        from models import User
        from auth import get_password_hash

        # Create a test user
        user = User(
            email="bruteforce@example.com",
            username="bruteforce",
            display_name="Brute Force Test",
            hashed_password=get_password_hash("CorrectPassword123!")
        )
        db_session.add(user)
        db_session.commit()

        # NOTE: Testbook's real login limit is 20/min in production (see
        # backend/routers/auth.py) — 10 attempts below won't trip it. Increase
        # the range past 20 if you want to actually observe a 429 in production
        # mode; account lockout itself isn't implemented (see
        # tests/security/test_rate_limiting.py::TestBruteForceProtection, which
        # documents this with skipped stub tests).
        # Attempt multiple failed logins
        for i in range(10):
            response = client.post("/api/auth/login", json={
                "email": "bruteforce@example.com",
                "password": "WrongPassword"
            })

            assert response.status_code in [401, 429], f"Failed login attempt {i+1} got unexpected {response.status_code}"

    def test_session_security(self, client: TestClient, test_user):
        """Test session security."""
        # Login
        login_response = client.post("/api/auth/login", json={
            "email": test_user.email,
            "password": "password123"
        })

        assert login_response.status_code == 200
        token = login_response.json()["access_token"]

        # NOTE: the current-user route is GET /api/auth/me, not /api/users/me
        # (see backend/routers/auth.py).
        # Test that token is required for protected endpoints
        response = client.get("/api/auth/me")
        assert response.status_code == 401, "Protected endpoint should require authentication"

        # Test with valid token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/auth/me", headers=headers)
        assert response.status_code == 200, "Valid token should allow access"

        # Test with invalid token
        invalid_headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/api/auth/me", headers=invalid_headers)
        assert response.status_code == 401, "Invalid token should be rejected"

        # Test with expired token (if implemented)
        # This would require mocking time or using a very short token expiry
```

#### Step 2: Test Authorization Bypass

Create `tests/security/test_authorization.py`:

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from models import User, Post
from auth import get_password_hash

class TestAuthorization:
    """Test for authorization bypass vulnerabilities."""

    def test_unauthorized_access_to_other_users_data(self, client: TestClient, db_session: Session):
        """Test that users cannot access other users' data."""
        # Create two users
        user1 = User(
            email="user1@example.com",
            username="user1",
            display_name="User 1",
            hashed_password=get_password_hash("password123")
        )
        user2 = User(
            email="user2@example.com",
            username="user2",
            display_name="User 2",
            hashed_password=get_password_hash("password123")
        )
        db_session.add_all([user1, user2])
        db_session.commit()

        # Login as user1
        login_response = client.post("/api/auth/login", json={
            "email": "user1@example.com",
            "password": "password123"
        })
        token1 = login_response.json()["access_token"]
        headers1 = {"Authorization": f"Bearer {token1}"}

        # Try to access user2's profile
        # NOTE: Testbook's real profile route is GET /api/users/{username} (a
        # public profile lookup by username, not numeric ID — see
        # backend/routers/users.py), so it returns 200 for any existing user
        # rather than 403/404. Public profiles being viewable isn't a bug; use
        # this pattern against a route that's actually meant to be private.
        response = client.get(f"/api/users/{user2.username}", headers=headers1)

        # Should return 403 (forbidden) or 404 (not found)
        assert response.status_code in [403, 404], "User should not access other user's profile"

    def test_unauthorized_post_modification(self, client: TestClient, db_session: Session):
        """Test that users cannot modify other users' posts."""
        # Create two users
        user1 = User(
            email="user1@example.com",
            username="user1",
            display_name="User 1",
            hashed_password=get_password_hash("password123")
        )
        user2 = User(
            email="user2@example.com",
            username="user2",
            display_name="User 2",
            hashed_password=get_password_hash("password123")
        )
        db_session.add_all([user1, user2])
        db_session.commit()

        # Create a post as user2
        post = Post(
            author_id=user2.id,
            title="User2's Post",
            content="This is user2's post"
        )
        db_session.add(post)
        db_session.commit()

        # Login as user1
        login_response = client.post("/api/auth/login", json={
            "email": "user1@example.com",
            "password": "password123"
        })
        token1 = login_response.json()["access_token"]
        headers1 = {"Authorization": f"Bearer {token1}"}

        # Try to modify user2's post
        response = client.put(f"/api/posts/{post.id}", json={
            "title": "Hacked Post",
            "content": "This post was hacked by user1"
        }, headers=headers1)

        # Should return 403 (forbidden) or 404 (not found)
        assert response.status_code in [403, 404], "User should not modify other user's post"

    def test_privilege_escalation(self, client: TestClient, db_session: Session):
        """Test for privilege escalation vulnerabilities.

        NOTE: Testbook has no `is_admin` field and no `/api/admin/*` routes today
        (checked `backend/models.py` and `backend/routers/`) — there's no admin
        role to escalate to. This is a template for a *future* admin feature, not
        a test you can run against the app as it exists now.
        """
        # Create a regular user
        user = User(
            email="user@example.com",
            username="user",
            display_name="Regular User",
            hashed_password=get_password_hash("password123"),
            is_admin=False
        )
        db_session.add(user)
        db_session.commit()

        # Login as regular user
        login_response = client.post("/api/auth/login", json={
            "email": "user@example.com",
            "password": "password123"
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Try to access admin endpoints
        admin_endpoints = [
            ("GET", "/api/admin/users"),
            ("GET", "/api/admin/stats"),
            ("POST", "/api/admin/ban-user"),
        ]

        for method, endpoint in admin_endpoints:
            response = client.request(method, endpoint, headers=headers)

            # Should return 403 (forbidden)
            assert response.status_code == 403, f"Regular user should not access admin endpoint {method} {endpoint}"

    def test_idor_vulnerability(self, client: TestClient, db_session: Session):
        """Test for Insecure Direct Object Reference (IDOR) vulnerabilities."""
        # Create two users
        user1 = User(
            email="user1@example.com",
            username="user1",
            display_name="User 1",
            hashed_password=get_password_hash("password123")
        )
        user2 = User(
            email="user2@example.com",
            username="user2",
            display_name="User 2",
            hashed_password=get_password_hash("password123")
        )
        db_session.add_all([user1, user2])
        db_session.commit()

        # Create posts for both users
        post1 = Post(author_id=user1.id, title="User1 Post", content="User1 content")
        post2 = Post(author_id=user2.id, title="User2 Post", content="User2 content")
        db_session.add_all([post1, post2])
        db_session.commit()

        # Login as user1
        login_response = client.post("/api/auth/login", json={
            "email": "user1@example.com",
            "password": "password123"
        })
        token1 = login_response.json()["access_token"]
        headers1 = {"Authorization": f"Bearer {token1}"}

        # Try to access user2's post by ID
        response = client.get(f"/api/posts/{post2.id}", headers=headers1)

        # Should return 403 (forbidden) or 404 (not found)
        assert response.status_code in [403, 404], "User should not access other user's post via IDOR"
```

---

### Part 3: API Security Testing (30 minutes)

#### Step 1: Test for Information Disclosure

Create `tests/security/test_information_disclosure.py`:

```python
import pytest
from fastapi.testclient import TestClient

class TestInformationDisclosure:
    """Test for information disclosure vulnerabilities."""

    def test_error_message_information_disclosure(self, client: TestClient):
        """Test that error messages don't disclose sensitive information."""
        # Test with invalid endpoint
        response = client.get("/api/invalid-endpoint")

        # Should return 404, not 500 with stack trace
        assert response.status_code == 404, "Invalid endpoint should return 404"

        # Error message should not contain sensitive information
        response_data = response.json()
        error_detail = response_data.get("detail", "")

        # Should not contain stack traces, file paths, or internal details
        assert "traceback" not in error_detail.lower()
        assert "file" not in error_detail.lower()
        assert "line" not in error_detail.lower()
        assert "exception" not in error_detail.lower()

    def test_database_error_disclosure(self, client: TestClient):
        """Test that database errors don't disclose sensitive information.

        NOTE: `/api/posts/` (see backend/routers/posts.py) requires
        authentication via `Depends(get_current_user)` — with no
        `Authorization` header, an unauthenticated request there returns 401
        (or 403), not 400/422. The two cases below need different expected
        codes; they aren't interchangeable.
        """
        # Test with malformed data that might cause database errors
        response = client.post("/api/auth/register", json={"email": "invalid", "password": "test"})
        assert response.status_code == 422, f"Malformed register payload should return 422, got {response.status_code}"

        response = client.post("/api/posts/", json={"content": "Test"})
        assert response.status_code in [401, 403], f"Unauthenticated post creation should return 401/403, got {response.status_code}"

        # Error message should not contain database details. NOTE: on a 422 the
        # FastAPI `detail` is a list of validation-error dicts, not a string —
        # normalize before checking substrings.
        response_data = response.json()
        error_detail = str(response_data.get("detail", "")).lower()

        # Should not contain database-specific information
        assert "sql" not in error_detail
        assert "database" not in error_detail
            assert "table" not in error_detail.lower()
            assert "column" not in error_detail.lower()

    def test_sensitive_data_exposure(self, client: TestClient, test_user):
        """Test that sensitive data is not exposed in API responses."""
        # Login
        login_response = client.post("/api/auth/login", json={
            "email": test_user.email,
            "password": "password123"
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Get user profile (GET /api/auth/me, not /api/users/me)
        response = client.get("/api/auth/me", headers=headers)
        assert response.status_code == 200

        user_data = response.json()

        # Should not contain sensitive fields
        sensitive_fields = ["hashed_password", "password", "secret", "private_key"]
        for field in sensitive_fields:
            assert field not in user_data, f"Sensitive field '{field}' should not be exposed in user profile"

    def test_http_method_disclosure(self, client: TestClient):
        """Test that HTTP methods are properly handled."""
        # Test unsupported methods on various endpoints
        endpoints = ["/api/health", "/api/users", "/api/posts"]
        unsupported_methods = ["PATCH", "HEAD", "OPTIONS"]

        for endpoint in endpoints:
            for method in unsupported_methods:
                response = client.request(method, endpoint)

                # Should return 405 (method not allowed) or 404 (not found)
                assert response.status_code in [405, 404], f"{method} {endpoint} should return 405/404, got {response.status_code}"

    def test_cors_configuration(self, client: TestClient):
        """Test CORS configuration for security."""
        # Test preflight request
        response = client.options("/api/health", headers={
            "Origin": "https://malicious-site.com",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type"
        })

        # Should return 200 with proper CORS headers
        assert response.status_code == 200

        # Check CORS headers
        cors_headers = {
            "Access-Control-Allow-Origin",
            "Access-Control-Allow-Methods",
            "Access-Control-Allow-Headers"
        }

        for header in cors_headers:
            assert header in response.headers, f"CORS header '{header}' should be present"
```

#### Step 2: Test for Rate Limiting

> **Filename note:** don't call this file `tests/security/test_rate_limiting.py` — Testbook already has a real one at that path (with different fixtures/content), and creating a new file there would overwrite it. Use a distinct name, e.g. `tests/security/test_rate_limiting_extra.py`.

Create `tests/security/test_rate_limiting_extra.py`:

```python
import pytest
from fastapi.testclient import TestClient
import time

class TestRateLimiting:
    """Test rate limiting functionality.

    NOTE: Testbook's real login limit is 20/min in production (1000/min when
    TESTING=true) and register is 15/min prod (500/min TESTING) — see
    `backend/routers/auth.py`. The small counts below (5, 10) are just
    illustrative of the *pattern*; against the real app you'd need roughly
    20+ requests within a minute (in production mode) before you'd actually
    see a 429.
    """

    def test_login_rate_limiting(self, client: TestClient, db_session):
        """Test rate limiting on login endpoint."""
        from models import User
        from auth import get_password_hash

        # Create a test user
        user = User(
            email="ratelimit@example.com",
            username="ratelimit",
            display_name="Rate Limit Test",
            hashed_password=get_password_hash("password123")
        )
        db_session.add(user)
        db_session.commit()

        # Make multiple login attempts
        for i in range(25):
            response = client.post("/api/auth/login", json={
                "email": "ratelimit@example.com",
                "password": "wrongpassword"
            })

            if i < 20:
                # First 20 attempts should return 401 (production limit is 20/min)
                assert response.status_code == 401, f"Login attempt {i+1} should return 401"
            else:
                # After 20 attempts, should be rate limited
                assert response.status_code == 429, f"Login attempt {i+1} should be rate limited"

    def test_api_endpoint_rate_limiting(self, client: TestClient, test_user):
        """Test rate limiting on API endpoints."""
        # Login first
        login_response = client.post("/api/auth/login", json={
            "email": test_user.email,
            "password": "password123"
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # NOTE: /api/feed/all has no route-specific limit in Testbook, so it
        # falls under the global default in backend/main.py — 100/min in
        # production, 1000/min when TESTING=true. 20 requests won't trip
        # either; this loop illustrates the pattern, not a limit you'll
        # actually observe at this request count.
        # Make multiple requests to a rate-limited endpoint
        for i in range(20):
            response = client.get("/api/feed/all", headers=headers)
            assert response.status_code in [200, 429], f"Request {i+1} got unexpected {response.status_code}"

    def test_rate_limit_headers(self, client: TestClient, test_user):
        """Test that rate limit headers are present."""
        # Login first
        login_response = client.post("/api/auth/login", json={
            "email": test_user.email,
            "password": "password123"
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Make a request
        response = client.get("/api/feed/all", headers=headers)

        # Should include rate limit headers
        rate_limit_headers = [
            "X-RateLimit-Limit",
            "X-RateLimit-Remaining",
            "X-RateLimit-Reset"
        ]

        for header in rate_limit_headers:
            assert header in response.headers, f"Rate limit header '{header}' should be present"

    def test_rate_limit_reset(self, client: TestClient, test_user):
        """Test that rate limits reset after the time window."""
        # Login first
        login_response = client.post("/api/auth/login", json={
            "email": test_user.email,
            "password": "password123"
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # NOTE: as above, /api/feed/all uses the 100/min (prod) or 1000/min
        # (TESTING) global default — 15 requests won't exhaust it. Bump this
        # well past whichever limit is active if you want to actually see a 429.
        # Exhaust rate limit
        for i in range(15):
            response = client.get("/api/feed/all", headers=headers)
            if response.status_code == 429:
                break

        # Wait for rate limit to reset (this would need to be implemented)
        # For now, just test that rate limiting is working
        assert response.status_code in [200, 429], "Unexpected status while probing rate limit"
```

---

### Part 4: Automated Security Scanning (20 minutes)

#### Step 1: Create Security Scan Script

Create `tests/security/security_scan.py`:

```python
#!/usr/bin/env python3
"""
Automated security scanning script for Testbook application.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_bandit_scan():
    """Run Bandit security scan on Python code."""
    print("🔍 Running Bandit security scan...")

    try:
        result = subprocess.run([
            'bandit', '-r', 'backend/', '-f', 'json', '-o', 'security-report-bandit.json'
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print("⚠️  Bandit found security issues:")
            print(result.stdout)
            return False
        else:
            print("✅ Bandit scan passed - no security issues found")
            return True
    except FileNotFoundError:
        print("❌ Bandit not found. Install with: pip install bandit")
        return False

def run_safety_scan():
    """Run Safety scan for vulnerable dependencies."""
    print("🔍 Running Safety dependency scan...")

    try:
        result = subprocess.run([
            'safety', 'check', '--json', '--output', 'security-report-safety.json'
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print("⚠️  Safety found vulnerable dependencies:")
            print(result.stdout)
            return False
        else:
            print("✅ Safety scan passed - no vulnerable dependencies found")
            return True
    except FileNotFoundError:
        print("❌ Safety not found. Install with: pip install safety")
        return False

def run_semgrep_scan():
    """Run Semgrep security scan."""
    print("🔍 Running Semgrep security scan...")

    try:
        result = subprocess.run([
            'semgrep', '--config=auto', 'backend/', '--json', '--output=security-report-semgrep.json'
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print("⚠️  Semgrep found security issues:")
            print(result.stdout)
            return False
        else:
            print("✅ Semgrep scan passed - no security issues found")
            return True
    except FileNotFoundError:
        print("❌ Semgrep not found. Install with: pip install semgrep")
        return False

def run_security_tests():
    """Run security test suite."""
    print("🔍 Running security test suite...")

    try:
        result = subprocess.run([
            'pytest', 'tests/security/', '-v', '--tb=short'
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print("⚠️  Security tests failed:")
            print(result.stdout)
            return False
        else:
            print("✅ Security tests passed")
            return True
    except FileNotFoundError:
        print("❌ Pytest not found")
        return False

def generate_security_report():
    """Generate comprehensive security report."""
    print("📊 Generating security report...")

    report = {
        "timestamp": "2024-01-01T00:00:00Z",
        "scans": {
            "bandit": "security-report-bandit.json",
            "safety": "security-report-safety.json",
            "semgrep": "security-report-semgrep.json"
        },
        "tests": "Security test suite results"
    }

    # This would generate a comprehensive HTML report
    print("✅ Security report generated")

def main():
    """Main security scanning function."""
    print("🛡️  Starting security scan...")

    # Change to project root
    project_root = Path(__file__).parent.parent.parent
    os.chdir(project_root)

    results = []

    # Run all security scans
    results.append(("Bandit", run_bandit_scan()))
    results.append(("Safety", run_safety_scan()))
    results.append(("Semgrep", run_semgrep_scan()))
    results.append(("Security Tests", run_security_tests()))

    # Generate report
    generate_security_report()

    # Print summary
    print("\n📋 Security Scan Summary:")
    print("=" * 50)

    all_passed = True
    for scan_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{scan_name:20} {status}")
        if not passed:
            all_passed = False

    print("=" * 50)

    if all_passed:
        print("🎉 All security scans passed!")
        sys.exit(0)
    else:
        print("⚠️  Some security scans failed. Please review the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

#### Step 2: Create Security Test Configuration

Create `tests/security/security_config.py`:

```python
"""
Security test configuration and utilities.
"""

import os
from typing import Dict, List

# OWASP Top 10 2021
OWASP_TOP_10 = {
    "A01": "Broken Access Control",
    "A02": "Cryptographic Failures",
    "A03": "Injection",
    "A04": "Insecure Design",
    "A05": "Security Misconfiguration",
    "A06": "Vulnerable and Outdated Components",
    "A07": "Identification and Authentication Failures",
    "A08": "Software and Data Integrity Failures",
    "A09": "Security Logging and Monitoring Failures",
    "A10": "Server-Side Request Forgery (SSRF)"
}

# Security test payloads
SECURITY_PAYLOADS = {
    "sql_injection": [
        "'; DROP TABLE users; --",
        "' OR '1'='1",
        "' UNION SELECT * FROM users --",
        "'; INSERT INTO users VALUES ('hacker', 'hacker@evil.com'); --",
    ],
    "xss": [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "javascript:alert('XSS')",
        "<svg onload=alert('XSS')>",
    ],
    "command_injection": [
        "; ls -la",
        "| cat /etc/passwd",
        "&& whoami",
        "`id`",
    ],
    "path_traversal": [
        "../../../etc/passwd",
        "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
        "....//....//....//etc/passwd",
    ],
    "xxe": [
        "<?xml version='1.0'?><!DOCTYPE foo [<!ENTITY xxe SYSTEM 'file:///etc/passwd'>]><foo>&xxe;</foo>",
    ],
}

# Security headers that should be present
REQUIRED_SECURITY_HEADERS = [
    "X-Content-Type-Options",
    "X-Frame-Options",
    "X-XSS-Protection",
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "Referrer-Policy",
]

# Rate limiting configuration
# NOTE: these are generic placeholder values for the exercise, not Testbook's
# actual limits. Testbook's real login limit is 20/min in production (1000/min
# when TESTING=true) and register is 15/min prod (500/min TESTING) — see
# backend/routers/auth.py. There's no password-reset flow in this app.
RATE_LIMITS = {
    "login_attempts_per_minute": 20,
    "register_attempts_per_minute": 15,
    "api_requests_per_minute_default": 100,
}

# Password complexity requirements
# NOTE: Testbook's /api/auth/register does NOT currently enforce any of this —
# it accepts any non-empty password string (see backend/schemas.py / auth.py).
# This table is a template for a policy you could add, not a description of
# existing behavior.
PASSWORD_REQUIREMENTS = {
    "min_length": 8,
    "require_uppercase": True,
    "require_lowercase": True,
    "require_numbers": True,
    "require_special_chars": True,
    "max_length": 128,
}

def get_security_headers() -> Dict[str, str]:
    """Get recommended security headers."""
    return {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "Content-Security-Policy": "default-src 'self'",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    }

def get_test_endpoints() -> List[str]:
    """Get list of endpoints to test for security vulnerabilities.

    NOTE: adjusted to match Testbook's actual routes (see backend/main.py /
    backend/routers/) — there is no /api/auth/logout (JWTs are stateless;
    "logout" just means the client discards the token) and no
    /api/users/search.
    """
    return [
        "/api/auth/login",
        "/api/auth/register",
        "/api/users/me",
        "/api/users/{username}/followers",
        "/api/posts/",
        "/api/feed/all",
        "/api/health",
    ]

def get_sensitive_data_fields() -> List[str]:
    """Get list of fields that should not be exposed in API responses."""
    return [
        "password",
        "hashed_password",
        "secret",
        "private_key",
        "api_key",
        "token",
        "ssn",
        "credit_card",
        "bank_account",
    ]
```

---

## 💪 Challenge Exercises

### Challenge 1: Create Custom Security Test Suite

```python
# Create tests/security/test_custom_security.py
import pytest
from fastapi.testclient import TestClient

class TestCustomSecurity:
    """Custom security tests for specific vulnerabilities."""

    def test_custom_vulnerability(self, client: TestClient):
        """Test for a custom security vulnerability."""
        # TODO: Implement custom security test
        # 1. Identify a specific vulnerability in your application
        # 2. Create a test that exploits it
        # 3. Verify that the vulnerability is properly handled
        pass

    def test_business_logic_security(self, client: TestClient):
        """Test for business logic security issues."""
        # TODO: Test business logic for security issues
        # 1. Test that business rules are properly enforced
        # 2. Test for race conditions
        # 3. Test for privilege escalation through business logic
        pass
```

### Challenge 2: Create Security Monitoring Dashboard

```python
# Create tests/security/security_monitoring.py
class SecurityMonitoring:
    """Security monitoring and alerting system."""

    def __init__(self):
        self.alerts = []
        self.metrics = {}

    def log_security_event(self, event_type: str, details: dict):
        """Log a security event."""
        # TODO: Implement security event logging
        pass

    def check_security_metrics(self):
        """Check security metrics and generate alerts."""
        # TODO: Implement security metrics checking
        pass

    def generate_security_report(self):
        """Generate security monitoring report."""
        # TODO: Implement security report generation
        pass
```

---

## ✅ Completion Checklist

- [ ] Can test for OWASP Top 10 vulnerabilities
- [ ] Can test authentication and authorization security
- [ ] Can test API security and information disclosure
- [ ] Can use automated security scanning tools
- [ ] Can create custom security tests
- [ ] Completed all challenge exercises
- [ ] Understand security testing best practices

---

## 💡 Pro Tips

1. **Start with OWASP Top 10** - Focus on the most common vulnerabilities
2. **Use automated tools** - Combine manual testing with automated scanning
3. **Test edge cases** - Look for vulnerabilities in unexpected places
4. **Monitor continuously** - Security testing should be ongoing
5. **Stay updated** - Keep up with new security threats and testing techniques

---

## 📚 Next Steps

**Continue building your skills:**

- **[Lab 15: Rate Limiting & Production Monitoring (Python)](LAB_15_Rate_Limiting_Production_Python.md)** - Production readiness
- **[Lab 16: Complete Test Suite Design (Python)](LAB_15_Rate_Limiting_Production_Python.md)** - Test strategy
- **[Lab 17: Portfolio Project & Presentation (Python)](../../stage_5_capstone/README.md)** - Final project

---

**🎉 Congratulations!** You now understand security testing and can identify and prevent common web application vulnerabilities!

**Next Lab:** [Lab 15: Rate Limiting & Production Monitoring (Python)](LAB_15_Rate_Limiting_Production_Python.md)
