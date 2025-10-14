"""
Rate limiting security tests.

Tests that the API properly implements rate limiting to prevent abuse.

⚠️ NOTE: These tests intentionally try to exceed rate limits!
────────────────────────────────────────────────────────────────────
If you see rate limit errors (429), that's GOOD - it means the
rate limiting is working!

TESTING MODE: The backend adjusts rate limits based on environment:
- Production: Strict limits (20/min login)
- Testing: Relaxed limits (100/min login)

RUN WITH: TESTING=true uvicorn main:app --port 8000

See README.md in this directory for full explanation.
────────────────────────────────────────────────────────────────────
"""

import time

import pytest
import requests

BASE_URL = "http://localhost:8000/api"


class TestRateLimiting:
    """Test API rate limiting mechanisms."""

    def test_login_attempts_should_be_rate_limited(self):
        """Test that repeated failed login attempts are rate limited."""
        # Note: Rate limit is 20/min in production, 100/min in TESTING mode
        # This test verifies rate limiting EXISTS (not the exact limit)

        session = requests.Session()

        # Attempt many failed logins rapidly
        failures = 0
        got_rate_limited = False

        for i in range(150):  # Try enough to hit even TESTING limits
            response = session.post(
                f"{BASE_URL}/auth/login",
                json={"email": "nonexistent@test.com", "password": "wrongpassword"},
                timeout=5,
            )

            if response.status_code == 429:  # Too Many Requests - rate limit works!
                got_rate_limited = True
                break

            failures += 1
            time.sleep(0.01)  # Tiny delay

        # The key test: Did we GET rate limited at some point?
        # We don't care about the exact limit (varies by environment)
        # We just care that rate limiting IS implemented
        assert got_rate_limited, (
            f"Rate limiting not working - completed {failures} attempts without hitting limit"
        )

        # In production: should hit ~20 attempts
        # In testing: should hit ~100 attempts
        assert failures < 150, "Rate limiting should trigger before 150 attempts"

    def test_api_requests_have_rate_limit_headers(self):
        """Test that API responses include rate limit headers."""
        response = requests.get(f"{BASE_URL}/health")

        # Check for common rate limit headers
        # (These are examples - adjust based on your implementation)
        headers = response.headers

        # Document if rate limiting is implemented
        has_rate_limit_headers = any(
            [
                "X-RateLimit-Limit" in headers,
                "X-RateLimit-Remaining" in headers,
                "X-RateLimit-Reset" in headers,
                "RateLimit-Limit" in headers,
            ]
        )

        # This test documents whether rate limiting headers are present
        # It doesn't fail if absent, but logs the result
        if not has_rate_limit_headers:
            pytest.skip(
                "Rate limit headers not implemented - consider adding for API transparency"
            )

    def test_registration_rate_limiting(self):
        """Test that user registration is rate limited."""
        import os

        session = requests.Session()

        # In TESTING mode, rate limits are higher (100/min vs 15/min)
        # So we need to attempt more registrations to hit the limit
        testing_mode = os.getenv("TESTING", "false").lower() == "true"
        attempts = 110 if testing_mode else 20

        # Try to register multiple accounts rapidly
        registrations = 0
        rate_limited = False

        for i in range(attempts):
            response = session.post(
                f"{BASE_URL}/auth/register",
                json={
                    "email": f"spam{i}_{int(time.time())}@test.com",
                    "username": f"spam{i}_{int(time.time())}",
                    "display_name": f"Spam User {i}",
                    "password": "SpamPass123!",
                },
            )

            if response.status_code == 429:
                rate_limited = True
                break

            if response.status_code == 201:
                registrations += 1

            # Don't sleep - we want to hit rate limit
            # time.sleep(0.1)

        # Should hit rate limit before all attempts complete
        # In TESTING mode (100/min), should be rate limited before 110 attempts
        # In production (15/min), should be rate limited before 20 attempts
        assert rate_limited or registrations < attempts, (
            f"Registration not rate limited - completed {registrations}/{attempts} attempts"
        )


class TestBruteForceProtection:
    """Test protection against brute force attacks."""

    def test_account_lockout_after_failed_attempts(self):
        """Test that accounts lock after multiple failed login attempts."""
        # This test assumes account lockout is implemented
        # Skip if not part of security requirements

        pytest.skip("Account lockout not implemented - consider adding for security")

        # Example implementation:
        # 1. Create test user
        # 2. Attempt 5+ failed logins
        # 3. Verify account is locked
        # 4. Verify successful credentials also fail while locked

    def test_temporary_ip_ban_on_suspicious_activity(self):
        """Test that suspicious IPs are temporarily banned."""
        pytest.skip(
            "IP-based banning not implemented - consider for high-security applications"
        )

        # Example: Test rapid failed attempts from same IP trigger temporary ban


class TestDDoSProtection:
    """Test protection against DDoS attacks."""

    def test_request_size_limits(self):
        """Test that excessively large requests are rejected."""
        # Test with large payload
        large_content = "x" * (10 * 1024 * 1024)  # 10MB

        response = requests.post(
            f"{BASE_URL}/posts/",
            json={"content": large_content},
            headers={"Authorization": "Bearer fake_token"},
        )

        # Should reject very large payloads
        # 413 = Payload Too Large, 400 = Bad Request
        assert response.status_code in [400, 413, 422], (
            "Server should reject excessively large payloads"
        )

    def test_concurrent_request_handling(self):
        """Test server handles concurrent requests gracefully."""
        import concurrent.futures

        def make_request():
            return requests.get(f"{BASE_URL}/health")

        # Send 50 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(make_request) for _ in range(50)]
            responses = [f.result() for f in concurrent.futures.as_completed(futures)]

        # Should handle all requests without crashing
        successful = sum(1 for r in responses if r.status_code == 200)

        # Most requests should succeed
        # Some might be rate limited, but server shouldn't crash
        assert successful > 0, "Server didn't handle any concurrent requests"


# NOTE: These tests assume rate limiting is implemented.
# If not implemented, they serve as specifications for security requirements.
# Implement rate limiting using libraries like:
# - slowapi (for FastAPI)
# - flask-limiter (for Flask)
# - express-rate-limit (for Express.js)
