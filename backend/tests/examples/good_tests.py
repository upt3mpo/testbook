"""
Examples of GOOD tests - Best practices to follow.

Use these patterns in your actual tests.
"""

import time
from datetime import datetime, timedelta

import pytest


# ✅ GOOD PATTERN 1: Use fixtures, no hardcoded IDs
def test_get_user_good(client, test_user):
    """GOOD: Uses fixture to create test data."""
    response = client.get(f"/api/users/{test_user.id}")
    assert response.status_code == 200
    assert response.json()["id"] == test_user.id


# ✅ GOOD PATTERN 2: Wait for condition, not arbitrary time
def test_async_good():
    """GOOD: Wait for actual condition with timeout."""
    trigger_task()

    # Wait for condition
    max_wait = 10
    start = time.time()
    result = None

    while time.time() - start < max_wait:
        result = get_result()
        if result == "done":
            break
        time.sleep(0.1)  # Small polling interval

    assert result == "done"


# ✅ GOOD PATTERN 3: Independent tests
def test_step1_good(db_session):
    """GOOD: Each test creates its own data."""
    user = User(email="user1@test.com")
    db_session.add(user)
    db_session.commit()
    assert user.id is not None


def test_step2_good(db_session):
    """GOOD: Independent - creates its own user."""
    user = User(email="user2@test.com")
    db_session.add(user)
    db_session.commit()
    assert user.id is not None


# ✅ GOOD PATTERN 4: Clear assertions
def test_with_assertions_good():
    """GOOD: Has specific assertions."""
    user = create_user()

    assert user is not None
    assert user.id is not None
    assert user.email == "testuser@example.com"


# ✅ GOOD PATTERN 5: One test, one concept
def test_user_creation_good():
    """GOOD: Tests only user creation."""
    user = create_user()
    assert user.id is not None
    assert user.email is not None


def test_post_creation_good():
    """GOOD: Separate test for post creation."""
    user = create_user()
    post = create_post(user)
    assert post.id is not None
    assert post.author_id == user.id


def test_comment_creation_good():
    """GOOD: Separate test for comment creation."""
    user = create_user()
    post = create_post(user)
    comment = create_comment(post)
    assert comment.id is not None
    assert comment.post_id == post.id


# ✅ GOOD PATTERN 6: Descriptive test name
def test_user_has_id_after_creation_good():
    """GOOD: Clear what's being tested from the name."""
    user = create_user()
    assert user.id is not None


# ✅ GOOD PATTERN 7: Test behavior, not implementation
def test_password_hashing_behavior_good():
    """GOOD: Tests behavior - password is secure."""
    password = "test123"
    hashed = get_password_hash(password)

    # Test behavior: password is hashed (not plaintext)
    assert hashed != password

    # Test behavior: can verify correct password
    assert verify_password(password, hashed) is True

    # Test behavior: wrong password fails
    assert verify_password("wrong", hashed) is False


# ✅ GOOD PATTERN 8: Use fixtures for cleanup
@pytest.fixture
def user_fixture(db_session):
    """GOOD: Fixture handles cleanup automatically."""
    user = User(email="test@test.com")
    db_session.add(user)
    db_session.commit()
    yield user
    # Cleanup happens automatically


def test_with_cleanup_good(user_fixture):
    """GOOD: Uses fixture - automatic cleanup."""
    assert user_fixture.id is not None
    # user_fixture will be cleaned up automatically


# ✅ GOOD PATTERN 9: Stable E2E selectors (JavaScript example in comments)
"""
// ✅ GOOD - JavaScript example
test('good selector', async ({ page }) => {
  // Use data-testid - stable and semantic
  await page.click('[data-testid="submit-button"]');
  await page.click('[data-testid="cancel-button"]');

  // Or use role-based selectors
  await page.getByRole('button', { name: 'Submit' }).click();
});
"""


# ✅ GOOD PATTERN 10: Relative time checking
def test_timestamp_good():
    """GOOD: Checks timestamp is recent, not exact value."""
    before = datetime.utcnow()
    user = create_user()
    after = datetime.utcnow()

    # Check timestamp is within our time window
    assert before <= user.created_at <= after

    # Or check it's recent (within last minute)
    time_diff = datetime.utcnow() - user.created_at
    assert time_diff < timedelta(minutes=1)


# ✅ GOOD PATTERN 11: Comprehensive API testing
def test_api_complete_good(client, test_user):
    """GOOD: Tests status code AND response data."""
    response = client.get(f"/api/users/{test_user.id}")

    # Check status code
    assert response.status_code == 200

    # Check response structure
    data = response.json()
    assert "id" in data
    assert "email" in data

    # Check response data
    assert data["id"] == test_user.id
    assert data["email"] == test_user.email


# ✅ GOOD PATTERN 12: Test error cases
def test_error_handling_good(client):
    """GOOD: Tests error scenarios."""
    # Test 404 - not found
    response = client.get("/api/users/99999")
    assert response.status_code == 404

    # Test 401 - unauthorized
    response = client.get("/api/auth/me")  # No auth header
    assert response.status_code == 401

    # Test 400 - bad request
    response = client.post("/api/auth/register", json={})
    assert response.status_code in [400, 422]


# ✅ GOOD PATTERN 13: Use builders for complex data
class UserBuilder:
    """GOOD: Builder pattern for test data."""

    def __init__(self):
        self.email = "test@test.com"
        self.username = "testuser"

    def with_email(self, email):
        self.email = email
        return self

    def build(self, db_session):
        user = User(email=self.email, username=self.username)
        db_session.add(user)
        db_session.commit()
        return user


def test_with_builder_good(db_session):
    """GOOD: Uses builder for flexible test data."""
    user = UserBuilder().with_email("custom@test.com").build(db_session)

    assert user.email == "custom@test.com"


# Compare these patterns to bad_tests.py to see the difference!
