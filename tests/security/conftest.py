"""
Shared fixtures for security tests.

This file handles rate limiting and test isolation issues.

WHY THIS EXISTS:
────────────────────────────────────────────────────────────────────
When we implemented rate limiting (good for security!), tests started
failing because they compete for the same rate limit budget.

SOLUTION: This conftest provides:
1. Automatic spacing between tests (500ms delay)
2. Cached auth tokens (minimize login calls)
3. Session-level fixtures (reduce API calls)

These fixtures run AUTOMATICALLY - you don't need to import them!

LEARN MORE: See README.md in this directory
────────────────────────────────────────────────────────────────────
"""

import time

import pytest
import requests

BASE_URL = "http://localhost:8000/api"


@pytest.fixture(scope="session", autouse=True)
def wait_for_rate_limit_reset():
    """
    Wait a bit at the start of test session to ensure rate limits are reset.
    """
    time.sleep(1)
    yield


@pytest.fixture(autouse=True)
def rate_limit_spacing():
    """
    Add delay between tests to avoid hitting rate limits.

    Even with TESTING mode (100 requests/minute), running 23 tests
    that each make multiple API calls can exceed limits.

    This fixture runs automatically before each test.
    """
    yield
    # Delay AFTER each test completes
    time.sleep(0.5)  # 500ms between tests - enough to stay under limits


# Cached token to minimize login calls
_test_token_cache = {}


@pytest.fixture(scope="session")
def get_auth_token():
    """
    Factory fixture that returns a function to get auth tokens.

    Uses caching to minimize API calls and avoid rate limits.
    """

    def _get_token(email="sarah.johnson@testbook.com", password="Sarah2024!"):
        cache_key = f"{email}:{password}"

        if cache_key not in _test_token_cache:
            response = requests.post(
                f"{BASE_URL}/auth/login",
                json={"email": email, "password": password},
                timeout=5,
            )
            if response.status_code == 200:
                _test_token_cache[cache_key] = response.json()["access_token"]
            else:
                pytest.fail(
                    f"Failed to get token: {response.status_code} - {response.text}"
                )

        return _test_token_cache[cache_key]

    return _get_token
