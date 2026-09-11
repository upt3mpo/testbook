# 🧪 Lab 6: Advanced API Testing

**Estimated Time:** 120 minutes<br>
**Difficulty:** Advanced<br>
**Language:** 🐍 Python<br>
**Prerequisites:** Lab 5 completed

**💡 Need JavaScript instead?** Try [Lab 6: Component Testing (JavaScript)](LAB_06_Component_Testing_JavaScript.md)!

**What This Adds:** Advanced API testing patterns including database transactions, complex authentication flows, error handling, and performance testing.

**Why this diverges from the JS track here:** this lab previews lightweight response-time assertions early because they're a natural extension of the API tests you're already writing. The JavaScript track's Lab 6 instead covers React component testing, which has no Python equivalent (there's no Python frontend to component-test) — so the two tracks intentionally teach different material at this lab number. Both tracks get full performance testing with k6 in Stage 4, so nothing here is skipped for JS learners, just introduced later.

---

## 🎯 What You'll Learn

- **Database transactions** - Test complex data operations
- **Authentication flows** - Test login, logout, token refresh
- **Error handling** - Test API error responses
- **Performance testing** - Test API response times
- **Data validation** - Test API input/output validation
- **Edge cases** - Test boundary conditions

---

## 📋 Step-by-Step Instructions

### Part 1: Database Transaction Testing (30 minutes)

Test complex operations that involve multiple database changes.

#### Step 1: Create Transaction Test

Create `backend/tests/integration/test_transactions.py`:

```python
"""
Advanced API Testing - Database Transaction Tests

This module demonstrates how to test complex database operations
that involve multiple related records and transaction management.
"""

import pytest
from sqlalchemy.orm import Session
from models import User, Post, Reaction
from auth import get_password_hash

class TestDatabaseTransactions:
    """
    Test complex database operations that require transaction management.

    These tests verify that related database operations work correctly
    together and that transactions can be properly rolled back on errors.
    """

    def test_create_user_with_posts(self, db_session: Session):
        """
        Test creating a user with multiple posts in a single transaction.

        This test verifies that we can create a user and multiple related
        posts atomically - either all succeed or all fail together.
        This is important for data consistency.
        """
        # Arrange: Prepare user data and multiple posts
        user_data = {
            "email": "testuser@example.com",      # Unique email for testing
            "username": "testuser",               # Unique username for testing
            "display_name": "Test User",          # Human-readable display name
            "hashed_password": get_password_hash("password123")  # Securely hashed password
        }

        posts_data = [
            {"content": "First post"},    # User's first post
            {"content": "Second post"},   # User's second post
            {"content": "Third post"}     # User's third post
        ]

        # Act - Create user and posts in a single transaction
        # Create the user first
        user = User(**user_data)
        db_session.add(user)
        db_session.flush()  # Get user ID without committing (allows foreign key references)

        # Create posts that reference the user
        for post_data in posts_data:
            post = Post(author_id=user.id, **post_data)  # Link post to user
            db_session.add(post)

        # Commit the entire transaction (user + all posts)
        db_session.commit()
        db_session.refresh(user)  # Reload user with all relationships

        # Assert: Verify the transaction was successful
        assert user.id is not None, "User should have been assigned an ID"
        assert len(user.posts) == 3, f"Expected 3 posts, got {len(user.posts)}"
        assert all(post.author_id == user.id for post in user.posts), "All posts should belong to the user"

    def test_rollback_on_error(self, db_session: Session):
        """Test that transaction rolls back on error."""
        # Arrange
        user = User(
            email="test@example.com",
            username="test",
            display_name="Test",
            hashed_password=get_password_hash("password")
        )
        db_session.add(user)
        db_session.flush()

        # Act - Try to create post with invalid data
        try:
            post = Post(author_id=user.id, content="")  # Empty content should fail
            db_session.add(post)
            db_session.commit()
        except Exception:
            db_session.rollback()

        # Assert - User should not exist due to rollback
        user_count = db_session.query(User).filter_by(email="test@example.com").count()
        assert user_count == 0
```

#### Step 2: Test Complex Relationships

**Note:** Testbook doesn't have a separate `Like` model - "liking" a post is modeled as a `Reaction` with `reaction_type="like"` (other reaction types are `love`, `haha`, `wow`, `sad`, `angry`). The `User` model exposes these through its `reactions` relationship.

```python
def test_user_likes_posts(self, db_session: Session):
    """Test user reacting to (liking) multiple posts."""
    # Arrange
    user = User(
        email="liker@example.com",
        username="liker",
        display_name="Liker",
        hashed_password=get_password_hash("password")
    )
    db_session.add(user)

    author = User(
        email="author@example.com",
        username="author",
        display_name="Author",
        hashed_password=get_password_hash("password")
    )
    db_session.add(author)
    db_session.flush()

    posts = [
        Post(author_id=author.id, content="Post 1"),
        Post(author_id=author.id, content="Post 2"),
        Post(author_id=author.id, content="Post 3")
    ]
    for post in posts:
        db_session.add(post)
    db_session.flush()

    # Act - User reacts with "like" to all posts
    for post in posts:
        reaction = Reaction(user_id=user.id, post_id=post.id, reaction_type="like")
        db_session.add(reaction)

    db_session.commit()
    db_session.refresh(user)

    # Assert
    assert len(user.reactions) == 3
    assert all(reaction.user_id == user.id for reaction in user.reactions)
```

---

### Part 2: Authentication Flow Testing (30 minutes)

Test complete authentication workflows.

#### Step 1: Test Login Flow

```python
def test_complete_login_flow(self, client, db_session: Session):
    """Test complete user login flow."""
    # Arrange - Create user
    user = User(
        email="test@example.com",
        username="testuser",
        display_name="Test User",
        hashed_password=get_password_hash("password123")
    )
    db_session.add(user)
    db_session.commit()

    # Act - Login
    login_data = {
        "email": "test@example.com",
        "password": "password123"
    }
    response = client.post("/api/auth/login", json=login_data)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Test token is valid
    # Note: the endpoint for "get my own profile" is /api/auth/me, not
    # /api/users/me - GET /api/users/{username} looks up a user by
    # username, and there's no user literally named "me".
    token = data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    profile_response = client.get("/api/auth/me", headers=headers)
    assert profile_response.status_code == 200
    assert profile_response.json()["email"] == "test@example.com"

def test_login_with_wrong_password(self, client, db_session: Session):
    """Test login with incorrect password."""
    # Arrange
    user = User(
        email="test@example.com",
        username="testuser",
        display_name="Test User",
        hashed_password=get_password_hash("correct_password")
    )
    db_session.add(user)
    db_session.commit()

    # Act
    login_data = {
        "email": "test@example.com",
        "password": "wrong_password"
    }
    response = client.post("/api/auth/login", json=login_data)

    # Assert
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]
```

#### Step 2: Test Token Expiration Claim

**Note:** Testbook's API does not implement a refresh-token flow - there's no `POST /api/auth/refresh` endpoint, and the login response only ever contains `access_token` and `token_type` (no `refresh_token`). Instead, let's verify the access token itself carries a valid expiration claim, which is what actually backs session length in this app.

```python
def test_login_token_has_expiration_claim(self, client, db_session: Session):
    """Test that the access token issued at login has a valid expiration claim."""
    from jose import jwt
    from auth import SECRET_KEY, ALGORITHM

    # Arrange - Login first
    user = User(
        email="test@example.com",
        username="testuser",
        display_name="Test User",
        hashed_password=get_password_hash("password123")
    )
    db_session.add(user)
    db_session.commit()

    login_response = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    access_token = login_response.json()["access_token"]

    # Act - Decode the token the same way auth.py does
    payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])

    # Assert
    assert payload["sub"] == "test@example.com"
    assert "exp" in payload  # Token has an expiration claim
```

---

### Part 3: Error Handling Testing (30 minutes)

Test API error responses and edge cases.

#### Step 1: Test Validation Errors

```python
def test_invalid_email_format(self, client):
    """Test API validation for invalid email format."""
    # Act
    response = client.post("/api/auth/register", json={
        "email": "invalid-email",
        "username": "testuser",
        "display_name": "Test User",
        "password": "password123"
    })

    # Assert
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any("email" in str(error) for error in errors)

def test_missing_required_fields(self, client):
    """Test API validation for missing required fields."""
    # Act
    response = client.post("/api/auth/register", json={
        "email": "test@example.com"
        # Missing username, display_name, password
    })

    # Assert
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert len(errors) >= 3  # Should have multiple validation errors

def test_duplicate_email(self, client, db_session: Session):
    """Test API error for duplicate email registration."""
    # Arrange - Create existing user
    user = User(
        email="test@example.com",
        username="existing",
        display_name="Existing User",
        hashed_password=get_password_hash("password")
    )
    db_session.add(user)
    db_session.commit()

    # Act - Try to register with same email
    response = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "username": "newuser",
        "display_name": "New User",
        "password": "password123"
    })

    # Assert
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]
```

#### Step 2: Test Authorization Errors

```python
def test_unauthorized_access(self, client):
    """Test accessing protected endpoint without token."""
    # Act
    response = client.get("/api/auth/me")

    # Assert - FastAPI's HTTPBearer rejects a missing Authorization
    # header with 403 (not 401) before your own code ever runs
    assert response.status_code == 403
    assert "Not authenticated" in response.json()["detail"]

def test_invalid_token(self, client):
    """Test accessing protected endpoint with invalid token."""
    # Act
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/api/auth/me", headers=headers)

    # Assert - get_current_user() raises this exact message for any
    # token that fails to decode/verify
    assert response.status_code == 401
    assert "Could not validate credentials" in response.json()["detail"]

def test_expired_token(self, client, db_session: Session):
    """Test accessing protected endpoint with expired token."""
    # This would require mocking time or using a very short token expiry
    # For now, we'll test the structure
    headers = {"Authorization": "Bearer expired_token"}
    response = client.get("/api/auth/me", headers=headers)

    # Should return 401 for expired token
    assert response.status_code == 401
```

---

### Part 4: Performance Testing (30 minutes)

Test API performance and response times.

#### Step 1: Test Response Times

```python
import time

def test_api_response_time(self, client, db_session: Session):
    """Test that API responds within acceptable time."""
    # Arrange
    user = User(
        email="test@example.com",
        username="testuser",
        display_name="Test User",
        hashed_password=get_password_hash("password123")
    )
    db_session.add(user)
    db_session.commit()

    # Act
    start_time = time.time()
    response = client.get("/api/health")
    end_time = time.time()

    # Assert
    response_time = end_time - start_time
    assert response.status_code == 200
    assert response_time < 1.0  # Should respond within 1 second

def test_bulk_operations_performance(self, client, auth_headers):
    """Test performance of bulk operations."""
    # Arrange - `auth_headers` (from conftest.py) already provides a
    # logged-in user's Authorization header. Creating a post requires
    # authentication, so requests without it would get 403, not 201.

    # Act - Create multiple posts
    start_time = time.time()
    for i in range(10):
        post_data = {"content": f"Test post {i}"}
        response = client.post("/api/posts/", json=post_data, headers=auth_headers)
        assert response.status_code == 201
    end_time = time.time()

    # Assert
    total_time = end_time - start_time
    assert total_time < 5.0  # Should create 10 posts within 5 seconds
    assert total_time / 10 < 0.5  # Average should be under 0.5 seconds per post
```

#### Step 2: Test Database Query Performance

```python
def test_database_query_performance(self, db_session: Session):
    """Test database query performance."""
    # Arrange - Create test data
    users = []
    for i in range(100):
        user = User(
            email=f"user{i}@example.com",
            username=f"user{i}",
            display_name=f"User {i}",
            hashed_password=get_password_hash("password")
        )
        users.append(user)
        db_session.add(user)
    db_session.commit()

    # Act - Test query performance
    start_time = time.time()
    all_users = db_session.query(User).all()
    end_time = time.time()

    # Assert
    query_time = end_time - start_time
    assert len(all_users) == 100
    assert query_time < 0.1  # Should query 100 users in under 0.1 seconds

def test_indexed_query_performance(self, db_session: Session):
    """Test performance of indexed queries."""
    # Arrange - Create user with email
    user = User(
        email="test@example.com",
        username="testuser",
        display_name="Test User",
        hashed_password=get_password_hash("password")
    )
    db_session.add(user)
    db_session.commit()

    # Act - Query by email (should use index)
    start_time = time.time()
    found_user = db_session.query(User).filter_by(email="test@example.com").first()
    end_time = time.time()

    # Assert
    query_time = end_time - start_time
    assert found_user is not None
    assert query_time < 0.01  # Indexed query should be very fast
```

---

## 💪 Challenge Exercises

### Challenge 1: Test Complex Business Logic

```python
def test_user_cannot_like_own_post(self, client, db_session: Session):
    """Test that users cannot like their own posts."""
    # TODO: Implement this test
    # 1. Create a user
    # 2. Create a post by that user
    # 3. Try to like the post
    # 4. Assert that it fails with appropriate error
    pass

def test_post_deletion_cascades_likes(self, client, db_session: Session):
    """Test that deleting a post also deletes all its likes."""
    # TODO: Implement this test
    # 1. Create a user and post
    # 2. Have another user like the post
    # 3. Delete the post
    # 4. Assert that the like is also deleted
    pass
```

### Challenge 2: Test Edge Cases

```python
def test_very_long_content(self, client, db_session: Session):
    """Test handling of very long post content."""
    # TODO: Test with content longer than database limit
    pass

def test_unicode_content(self, client, db_session: Session):
    """Test handling of unicode characters in content."""
    # TODO: Test with emojis, special characters, etc.
    pass
```

---

## 🎓 Advanced Patterns

### Custom Fixtures for Complex Setup

```python
@pytest.fixture
def user_with_posts(db_session: Session):
    """Create a user with multiple posts for testing."""
    user = User(
        email="test@example.com",
        username="testuser",
        display_name="Test User",
        hashed_password=get_password_hash("password123")
    )
    db_session.add(user)
    db_session.flush()

    posts = []
    for i in range(5):
        post = Post(author_id=user.id, content=f"Test post {i}")
        posts.append(post)
        db_session.add(post)

    db_session.commit()
    db_session.refresh(user)
    return user, posts

def test_user_posts_relationship(self, user_with_posts):
    """Test user-posts relationship using custom fixture."""
    user, posts = user_with_posts

    assert len(user.posts) == 5
    assert all(post.author_id == user.id for post in posts)
```

### Testing with Mocks

```python
from unittest.mock import patch, MagicMock

def test_external_api_call(self, client):
    """Test API that calls external service."""
    with patch('requests.get') as mock_get:
        # Mock external API response
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": "test"}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Test your API
        response = client.get("/api/external-data")

        # Assert
        assert response.status_code == 200
        mock_get.assert_called_once()
```

---

## ✅ Completion Checklist

- [ ] Can test complex database transactions
- [ ] Can test complete authentication flows
- [ ] Can test API error handling and validation
- [ ] Can test API performance and response times
- [ ] Can write custom fixtures for complex test data
- [ ] Can test edge cases and boundary conditions
- [ ] Completed all challenge exercises
- [ ] Understand when to use integration vs unit tests

---

## 💡 Pro Tips

1. **Test the happy path first** - Get basic functionality working
2. **Then test edge cases** - Empty data, invalid data, boundary conditions
3. **Test error conditions** - What happens when things go wrong
4. **Use fixtures for complex setup** - Don't repeat setup code
5. **Test performance early** - Catch slow queries before production

---

## 📚 Next Steps

**Continue building your skills:**

- **[Lab 7: Test Data Management (Python)](LAB_07_Test_Data_Management_Python.md)** - Advanced test data patterns
- **[Lab 8: Contract Testing Foundations (Python)](LAB_08_Contract_Testing_Foundations_Python.md)** - API contract testing
- **[Lab 9: Basic E2E Testing (Python)](../../stage_3_api_e2e/exercises/LAB_09_Basic_E2E_Testing_Python.md)** - End-to-end testing

---

**🎉 Congratulations!** You now understand advanced API testing patterns and can test complex backend functionality!

**Next Lab:** [Lab 7: Test Data Management (Python)](LAB_07_Test_Data_Management_Python.md)
