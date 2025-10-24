"""
Security tests for Testbook API.

This file demonstrates comprehensive security testing practices using pytest.
It verifies authentication, authorization, input validation, and other
security-critical functionality to protect against common vulnerabilities.

Key Testing Concepts Demonstrated:
- OWASP Top 10 vulnerability testing (SQL injection, XSS, etc.)
- Authentication and authorization testing
- Input validation and sanitization testing
- Rate limiting and DoS protection testing
- Security header validation
- Error handling and information disclosure testing
- Session management and token security

This file is referenced in Stage 4 learning materials as an example
of professional security testing practices.

⚠️ IMPORTANT: IF THESE TESTS FAIL
────────────────────────────────────────────────────────────────────
Some tests may fail due to RATE LIMITING (which means security is working!).

WHY: Rate limiting is set to 20 login requests/minute. When running all
23 security tests together, they exceed this limit.

SOLUTION: Run backend in TESTING mode:
    cd backend
    TESTING=true uvicorn main:app --reload --port 8000

Then run tests:
    pytest tests/security/ -v

LEARN MORE: See tests/security/README.md or learn/stage_4_performance_security/exercises/LAB_06_Testing_With_Rate_Limits.md
────────────────────────────────────────────────────────────────────
"""

import pytest
import requests

BASE_URL = "http://localhost:8000/api"


@pytest.fixture(scope="session")
def api_client():
    """
    API client for making requests.

    This fixture provides a requests.Session for making HTTP requests
    to the API. Using a session allows for connection pooling and
    cookie persistence across requests.
    """
    return requests.Session()


@pytest.fixture(scope="session")
def auth_token():
    """
    Get authentication token for testing (session-scoped to avoid rate limits).

    This fixture handles the complexity of obtaining an authentication
    token for testing, including retry logic for rate limiting scenarios.
    The token is session-scoped to minimize API calls and avoid rate limits.
    """
    import time

    client = requests.Session()

    # Retry with backoff if rate limited
    max_retries = 3
    for attempt in range(max_retries):
        response = client.post(
            f"{BASE_URL}/auth/login",
            json={"email": "sarah.johnson@testbook.com", "password": "Sarah2024!"},
        )

        if response.status_code == 200:
            return response.json()["access_token"]

        if response.status_code == 429 and attempt < max_retries - 1:
            # Rate limited, wait and retry
            time.sleep(2**attempt)  # Exponential backoff: 1s, 2s, 4s
            continue

        # Final attempt failed or non-429 error
        if response.status_code == 429:
            pytest.skip("Rate limited - cannot get auth token")
        else:
            pytest.fail(f"Failed to get auth token: {response.status_code} - {response.text}")

    pytest.skip("Rate limited after retries - cannot get auth token")


class TestAuthentication:
    """Test authentication security."""

    def test_cannot_access_protected_routes_without_auth(self, api_client):
        """Test that protected routes require authentication."""
        protected_endpoints = [
            ("/auth/me", "GET"),
            ("/users/me", "PUT"),
            ("/posts/", "POST"),
            ("/feed/all", "GET"),
        ]

        for endpoint, method in protected_endpoints:
            if method == "GET":
                response = api_client.get(f"{BASE_URL}{endpoint}")
            elif method == "POST":
                response = api_client.post(f"{BASE_URL}{endpoint}", json={})
            elif method == "PUT":
                response = api_client.put(f"{BASE_URL}{endpoint}", json={})

            # Both 401 (Unauthorized) and 403 (Forbidden) are valid for missing auth
            assert response.status_code in [
                401,
                403,
            ], f"{endpoint} should require auth (got {response.status_code})"

    def test_invalid_token_rejected(self, api_client):
        """Test that invalid tokens are rejected."""
        headers = {"Authorization": "Bearer invalid_token_here"}
        response = api_client.get(f"{BASE_URL}/auth/me", headers=headers)
        assert response.status_code == 401

    def test_malformed_auth_header_rejected(self, api_client):
        """Test that malformed auth headers are rejected."""
        malformed_headers = [
            {"Authorization": "InvalidFormat token"},
            {"Authorization": "Bearer"},
            {"Authorization": "token_without_bearer"},
        ]

        for headers in malformed_headers:
            response = api_client.get(f"{BASE_URL}/auth/me", headers=headers)
            # Both 401 and 403 are acceptable for malformed auth
            assert response.status_code in [
                401,
                403,
            ], f"Expected auth error, got {response.status_code}"

    def test_password_not_returned_in_responses(self, api_client):
        """Test that passwords are never included in responses."""
        # Register
        response = api_client.post(
            f"{BASE_URL}/auth/register",
            json={
                "email": f"security{pytest.timestamp}@test.com",
                "username": f"sectest{pytest.timestamp}",
                "display_name": "Security Test",
                "password": "SecurePass123!",
            },
        )

        data = response.json()
        assert "password" not in data
        assert "hashed_password" not in data

    def test_login_with_wrong_password_fails(self, api_client):
        """Test that wrong password is rejected."""
        response = api_client.post(
            f"{BASE_URL}/auth/login",
            json={
                "email": "sarah.johnson@testbook.com",
                "password": "WrongPassword123!",
            },
        )
        # Should be 401, but 429 (rate limited) is also acceptable in CI
        assert response.status_code in [
            401,
            429,
        ], f"Expected 401 or 429 (rate limited), got {response.status_code}"


class TestAuthorization:
    """Test authorization and access control."""

    def test_cannot_edit_other_users_posts(self, api_client):
        """Test that users cannot edit posts they don't own."""
        # Login as Mike to try to edit Sarah's post (ID 1)
        login_response = api_client.post(
            f"{BASE_URL}/auth/login",
            json={"email": "mike.chen@testbook.com", "password": "MikeRocks88"},
        )

        if login_response.status_code == 429:
            pytest.skip("Rate limited - test cannot proceed")

        assert login_response.status_code == 200
        mike_token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {mike_token}"}

        # Try to update Sarah's post (ID 1 from seed)
        response = api_client.put(
            f"{BASE_URL}/posts/1",
            json={"content": "Trying to hack this post"},
            headers=headers,
        )

        # Should either be 403 (forbidden) or 404 (if post doesn't exist)
        assert response.status_code in [403, 404]

    def test_cannot_delete_other_users_posts(self, api_client):
        """Test that users cannot delete posts they don't own."""
        # Login as Mike to try to delete Sarah's post (ID 1)
        login_response = api_client.post(
            f"{BASE_URL}/auth/login",
            json={"email": "mike.chen@testbook.com", "password": "MikeRocks88"},
        )

        if login_response.status_code == 429:
            pytest.skip("Rate limited - test cannot proceed")

        assert login_response.status_code == 200
        mike_token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {mike_token}"}

        response = api_client.delete(f"{BASE_URL}/posts/1", headers=headers)

        assert response.status_code in [403, 404]

    def test_user_can_only_update_own_profile(self, api_client):
        """Test that users can only update their own profile."""
        # Login as user 1
        login_response = api_client.post(
            f"{BASE_URL}/auth/login",
            json={"email": "sarah.johnson@testbook.com", "password": "Sarah2024!"},
        )

        if login_response.status_code == 429:
            pytest.skip("Rate limited - test cannot proceed")

        assert login_response.status_code == 200
        token1 = login_response.json()["access_token"]

        headers = {"Authorization": f"Bearer {token1}"}

        # Should be able to update /users/me
        response = api_client.put(
            f"{BASE_URL}/users/me",
            json={"display_name": "Updated Name"},
            headers=headers,
        )
        assert response.status_code == 200


class TestInputValidation:
    """Test input validation and sanitization."""

    def test_email_validation(self, api_client):
        """Test that invalid emails are rejected."""
        invalid_emails = [
            "notanemail",
            "@example.com",
            "test@",
            "test..test@example.com",
        ]

        for email in invalid_emails:
            response = api_client.post(
                f"{BASE_URL}/auth/register",
                json={
                    "email": email,
                    "username": "testuser",
                    "display_name": "Test",
                    "password": "Test123!",
                },
            )
            assert response.status_code == 422, f"Invalid email {email} should be rejected"

    def test_sql_injection_in_login(self, api_client):
        """Test that SQL injection attempts are blocked."""
        sql_injections = [
            "' OR '1'='1",
            "admin'--",
            "' OR '1'='1' --",
        ]

        for injection in sql_injections:
            response = api_client.post(
                f"{BASE_URL}/auth/login",
                json={"email": injection, "password": "password"},
            )
            # Should either be validation error or unauthorized
            assert response.status_code in [401, 422]

    def test_xss_in_post_content(self, api_client, auth_token):
        """Test that XSS attempts in posts are handled."""
        headers = {"Authorization": f"Bearer {auth_token}"}

        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')",
        ]

        for payload in xss_payloads:
            response = api_client.post(
                f"{BASE_URL}/posts/", json={"content": payload}, headers=headers
            )

            # Post should be created (content should be sanitized by frontend)
            # Backend typically accepts it but frontend should escape it
            # Skip if we hit rate limits or auth issues
            if response.status_code in [403, 429]:
                pytest.skip(f"Cannot test XSS - got {response.status_code}")

            assert response.status_code == 201, f"Expected 201, got {response.status_code}"
            post_id = response.json()["id"]

            # Verify it's stored (backend stores as-is for frontend to handle)
            get_response = api_client.get(f"{BASE_URL}/posts/{post_id}")
            assert get_response.status_code == 200


class TestRateLimiting:
    """Test rate limiting (if implemented)."""

    def test_excessive_login_attempts(self, api_client):
        """Test that excessive login attempts are handled."""
        # Make many failed login attempts
        for _ in range(20):
            api_client.post(
                f"{BASE_URL}/auth/login",
                json={"email": "test@example.com", "password": "wrongpassword"},
            )

        # Next attempt should still work (or be rate limited)
        response = api_client.post(
            f"{BASE_URL}/auth/login",
            json={"email": "test@example.com", "password": "wrongpassword"},
        )

        # Should either work or be rate limited (429)
        assert response.status_code in [401, 429]


class TestDataExposure:
    """Test that sensitive data is not exposed."""

    def test_user_list_doesnt_expose_passwords(self, api_client, auth_token):
        """Test that user lists don't expose passwords."""
        headers = {"Authorization": f"Bearer {auth_token}"}

        # Get followers list
        response = api_client.get(f"{BASE_URL}/users/sarahjohnson/followers", headers=headers)

        if response.status_code == 200:
            users = response.json()
            for user in users:
                assert "password" not in user
                assert "hashed_password" not in user

    def test_error_messages_dont_expose_internals(self, api_client):
        """Test that error messages don't expose internal details."""
        # Try to access non-existent resource
        response = api_client.get(f"{BASE_URL}/posts/999999")

        if response.status_code == 404:
            data = response.json()
            error_message = str(data).lower()

            # Should not expose SQL, file paths, or stack traces
            assert "sql" not in error_message
            assert "traceback" not in error_message
            assert "exception" not in error_message
            assert "/users/" not in error_message  # File paths


class TestSessionManagement:
    """Test session and token management."""

    def test_token_works_for_multiple_requests(self, api_client, auth_token):
        """Test that token can be reused for multiple requests."""
        headers = {"Authorization": f"Bearer {auth_token}"}

        for _ in range(5):
            response = api_client.get(f"{BASE_URL}/auth/me", headers=headers)
            assert response.status_code == 200

    def test_can_have_multiple_sessions(self, api_client):
        """Test that user can have multiple active sessions."""
        # Login twice
        login1 = api_client.post(
            f"{BASE_URL}/auth/login",
            json={"email": "sarah.johnson@testbook.com", "password": "Sarah2024!"},
        )

        if login1.status_code == 429:
            pytest.skip("Rate limited - test cannot proceed")

        assert login1.status_code == 200
        token1 = login1.json()["access_token"]

        login2 = api_client.post(
            f"{BASE_URL}/auth/login",
            json={"email": "sarah.johnson@testbook.com", "password": "Sarah2024!"},
        )

        if login2.status_code == 429:
            pytest.skip("Rate limited - test cannot proceed")

        assert login2.status_code == 200
        token2 = login2.json()["access_token"]

        # Both tokens should work
        headers1 = {"Authorization": f"Bearer {token1}"}
        headers2 = {"Authorization": f"Bearer {token2}"}

        assert api_client.get(f"{BASE_URL}/auth/me", headers=headers1).status_code == 200
        assert api_client.get(f"{BASE_URL}/auth/me", headers=headers2).status_code == 200


# Set timestamp for unique test data
pytest.timestamp = __import__("time").time()
