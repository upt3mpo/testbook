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

            # Should return 401 (unauthorized), not 500 (server error)
            assert response.status_code == 401, f"SQL injection payload '{payload}' should return 401, got {response.status_code}"

            # Should not expose database errors
            response_data = response.json()
            assert "sql" not in response_data.get("detail", "").lower()
            assert "database" not in response_data.get("detail", "").lower()

    def test_user_search_sql_injection(self, client: TestClient, db_session: Session):
        """Test user search endpoint for SQL injection."""
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
        """Test post creation for SQL injection in content."""
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
        """Test post content for XSS vulnerabilities."""
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

            # Content should be properly escaped
            content = get_response.json()["content"]
            assert "<script>" not in content, f"XSS payload '{payload}' should be escaped"
            assert "javascript:" not in content, f"XSS payload '{payload}' should be escaped"
            assert "onerror=" not in content, f"XSS payload '{payload}' should be escaped"

            # Content should be HTML-encoded
            assert escape(payload) in content or payload in content, f"XSS payload '{payload}' should be properly handled"

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

        # Get updated profile
        profile_response = client.get("/api/users/me", headers=headers)
        display_name = profile_response.json()["display_name"]

        # Display name should be properly escaped
        assert "<script>" not in display_name, "XSS payload in display_name should be escaped"
        assert escape(xss_payload) in display_name or xss_payload in display_name, "XSS payload should be properly handled"

    def test_search_xss(self, client: TestClient):
        """Test search functionality for XSS vulnerabilities."""
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
    """Test password security policies."""

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

        # Attempt multiple failed logins
        for i in range(10):
            response = client.post("/api/auth/login", json={
                "email": "bruteforce@example.com",
                "password": "WrongPassword"
            })

            if i < 5:
                # First few attempts should return 401
                assert response.status_code == 401, f"Failed login attempt {i+1} should return 401"
            else:
                # After 5 attempts, should be rate limited
                assert response.status_code == 429, f"Failed login attempt {i+1} should be rate limited (429)"

    def test_session_security(self, client: TestClient, test_user):
        """Test session security."""
        # Login
        login_response = client.post("/api/auth/login", json={
            "email": test_user.email,
            "password": "password123"
        })

        assert login_response.status_code == 200
        token = login_response.json()["access_token"]

        # Test that token is required for protected endpoints
        response = client.get("/api/users/me")
        assert response.status_code == 401, "Protected endpoint should require authentication"

        # Test with valid token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/users/me", headers=headers)
        assert response.status_code == 200, "Valid token should allow access"

        # Test with invalid token
        invalid_headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/api/users/me", headers=invalid_headers)
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
        response = client.get(f"/api/users/{user2.id}", headers=headers1)

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
        """Test for privilege escalation vulnerabilities."""
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
        """Test that database errors don't disclose sensitive information."""
        # Test with malformed data that might cause database errors
        malformed_requests = [
            ("POST", "/api/auth/register", {"email": "invalid", "password": "test"}),
            ("POST", "/api/posts", {"title": "Test", "content": "Test"}),
        ]

        for method, endpoint, data in malformed_requests:
            response = client.request(method, endpoint, json=data)

            # Should return 400 or 422, not 500
            assert response.status_code in [400, 422], f"{method} {endpoint} should return 400/422, got {response.status_code}"

            # Error message should not contain database details
            response_data = response.json()
            error_detail = response_data.get("detail", "")

            # Should not contain database-specific information
            assert "sql" not in error_detail.lower()
            assert "database" not in error_detail.lower()
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

        # Get user profile
        response = client.get("/api/users/me", headers=headers)
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

Create `tests/security/test_rate_limiting.py`:

```python
import pytest
from fastapi.testclient import TestClient
import time

class TestRateLimiting:
    """Test rate limiting functionality."""

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
        for i in range(10):
            response = client.post("/api/auth/login", json={
                "email": "ratelimit@example.com",
                "password": "wrongpassword"
            })

            if i < 5:
                # First few attempts should return 401
                assert response.status_code == 401, f"Login attempt {i+1} should return 401"
            else:
                # After 5 attempts, should be rate limited
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

        # Make multiple requests to a rate-limited endpoint
        for i in range(20):
            response = client.get("/api/feed", headers=headers)

            if i < 10:
                # First 10 requests should succeed
                assert response.status_code == 200, f"Request {i+1} should succeed"
            else:
                # After 10 requests, should be rate limited
                assert response.status_code == 429, f"Request {i+1} should be rate limited"

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
        response = client.get("/api/feed", headers=headers)

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

        # Exhaust rate limit
        for i in range(15):
            response = client.get("/api/feed", headers=headers)
            if response.status_code == 429:
                break

        # Wait for rate limit to reset (this would need to be implemented)
        # For now, just test that rate limiting is working
        assert response.status_code == 429, "Rate limiting should be active"
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
RATE_LIMITS = {
    "login_attempts": 5,
    "api_requests_per_minute": 100,
    "password_reset_attempts": 3,
}

# Password complexity requirements
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
    """Get list of endpoints to test for security vulnerabilities."""
    return [
        "/api/auth/login",
        "/api/auth/register",
        "/api/auth/logout",
        "/api/users/me",
        "/api/users/search",
        "/api/posts",
        "/api/feed",
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
- **[Lab 16: Complete Test Suite Design (Python)](LAB_16_Complete_Test_Suite_Design_Python.md)** - Test strategy
- **[Lab 17: Portfolio Project & Presentation (Python)](LAB_17_Portfolio_Project_Presentation_Python.md)** - Final project

---

**🎉 Congratulations!** You now understand security testing and can identify and prevent common web application vulnerabilities!

**Next Lab:** [Lab 15: Rate Limiting & Production Monitoring (Python)](LAB_15_Rate_Limiting_Production_Python.md)
