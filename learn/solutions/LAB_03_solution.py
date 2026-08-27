"""
Lab 3 Solution: Testing API Endpoints

Complete solutions for API endpoint testing with FastAPI TestClient.
"""

import pytest


@pytest.mark.integration
@pytest.mark.api
class TestLoginEndpoint:
    """Test login endpoint solutions."""

    def test_login_with_wrong_password(self, client, test_user):
        """Test that login fails with incorrect password."""
        response = client.post(
            "/api/auth/login",
            json={
                "email": "testuser@example.com",
                "password": "WrongPassword999!",
            },
        )

        assert response.status_code == 401
        assert "detail" in response.json()
        detail = response.json()["detail"].lower()
        assert "invalid" in detail or "incorrect" in detail


@pytest.mark.integration
@pytest.mark.api
class TestRegistrationEndpoint:
    """Test registration endpoint solutions."""

    def test_register_new_user(self, client):
        """Test successful user registration."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "newuser@example.com",
                "username": "newuser",
                "display_name": "New User",
                "password": "SecurePass123!",
                "bio": "This is my bio",
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        # Password should NOT be in response
        assert "password" not in data
        assert "hashed_password" not in data

    def test_register_duplicate_email(self, client, test_user):
        """Test registration with duplicate email fails."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": test_user.email,  # Duplicate!
                "username": "differentuser",
                "display_name": "Different User",
                "password": "SecurePass123!",
            },
        )

        assert response.status_code == 400
        assert "email" in response.json()["detail"].lower()

    def test_register_invalid_email(self, client):
        """Test registration with invalid email format."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "notanemail",  # Invalid format
                "username": "testuser",
                "display_name": "Test User",
                "password": "SecurePass123!",
            },
        )

        assert response.status_code == 422  # Validation error


@pytest.mark.integration
@pytest.mark.api
class TestProtectedEndpoints:
    """Test endpoints that require authentication."""

    def test_get_current_user_with_auth(self, client, test_user, auth_headers):
        """Test getting current user with valid token."""
        response = client.get("/api/auth/me", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user.email
        assert data["username"] == test_user.username

    def test_get_current_user_without_auth(self, client):
        """Test that /api/auth/me requires authentication."""
        response = client.get("/api/auth/me")

        # FastAPI's HTTPBearer rejects a missing Authorization header with
        # 403 (not 401) before our own code ever runs
        assert response.status_code == 403

    def test_create_post_without_auth(self, client):
        """Test that creating post requires authentication."""
        response = client.post(
            "/api/posts/",
            json={"content": "Test post"},
        )

        assert response.status_code == 403


@pytest.mark.integration
@pytest.mark.api
class TestPostsAPI:
    """Test posts API endpoints."""

    def test_create_post(self, client, auth_headers):
        """Test creating a new post."""
        response = client.post(
            "/api/posts/",
            json={
                "content": "This is my test post!",
                "image_url": None,
                "video_url": None,
            },
            headers=auth_headers,
        )

        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["content"] == "This is my test post!"
        assert "created_at" in data

    def test_get_post_by_id(self, client, test_post, auth_headers):
        """Test retrieving a specific post."""
        response = client.get(
            f"/api/posts/{test_post.id}",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_post.id
        assert data["content"] == test_post.content

    def test_update_own_post(self, client, test_post, auth_headers):
        """Test updating your own post."""
        response = client.put(
            f"/api/posts/{test_post.id}",
            json={"content": "Updated content!"},
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["content"] == "Updated content!"

    def test_delete_own_post(self, client, test_post, auth_headers):
        """Test deleting your own post."""
        response = client.delete(
            f"/api/posts/{test_post.id}",
            headers=auth_headers,
        )

        assert response.status_code == 200

        # Verify it's gone
        get_response = client.get(
            f"/api/posts/{test_post.id}",
            headers=auth_headers,
        )
        assert get_response.status_code == 404

    def test_cannot_update_others_post(self, client, test_post, test_user_2):
        """Test that users cannot update posts they don't own."""
        from auth import create_access_token

        # Create token for different user
        token2 = create_access_token(data={"sub": test_user_2.email})
        headers2 = {"Authorization": f"Bearer {token2}"}

        # Try to update test_post (owned by test_user)
        response = client.put(
            f"/api/posts/{test_post.id}",
            json={"content": "Trying to hack!"},
            headers=headers2,
        )

        assert response.status_code == 403


@pytest.mark.integration
@pytest.mark.api
class TestCommentsAPI:
    """Test comments API endpoints."""

    def test_add_comment_to_post(self, client, test_post, auth_headers):
        """Test adding a comment to a post."""
        response = client.post(
            f"/api/posts/{test_post.id}/comments",
            json={"content": "Great post!"},
            headers=auth_headers,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["content"] == "Great post!"
        assert data["post_id"] == test_post.id

    # Note: there is no comment-deletion endpoint in the current API
    # (only POST /{post_id}/comments to create one) - a
    # `test_delete_own_comment` test doesn't correspond to any real
    # route, so it's intentionally omitted here.


@pytest.mark.integration
@pytest.mark.api
class TestReactionsAPI:
    """Test reactions API endpoints."""

    def test_add_reaction_to_post(self, client, test_post, auth_headers):
        """Test adding a reaction to a post."""
        response = client.post(
            f"/api/posts/{test_post.id}/reactions",
            json={"reaction_type": "like"},
            headers=auth_headers,
        )

        # This endpoint returns the full post (schemas.PostResponse), not a
        # standalone reaction object - there's no "reaction_type" key at
        # the top level. The caller's own reaction shows up as
        # `user_reaction` on the post.
        assert response.status_code == 201
        data = response.json()
        assert data["id"] == test_post.id
        assert data["user_reaction"] == "like"
        assert data["reactions_count"] == 1

    def test_remove_reaction(self, client, test_post, auth_headers):
        """Test removing a reaction from a post."""
        # First add reaction
        client.post(
            f"/api/posts/{test_post.id}/reactions",
            json={"reaction_type": "like"},
            headers=auth_headers,
        )

        # Then remove it
        response = client.delete(
            f"/api/posts/{test_post.id}/reactions",
            headers=auth_headers,
        )

        assert response.status_code == 200

    def test_reacting_twice_with_same_type_is_idempotent(self, client, test_post, auth_headers):
        """Test that reacting twice with the same type doesn't create a duplicate.

        Note: POST /{post_id}/reactions is not a toggle - sending the same
        reaction_type again just updates the existing reaction in place
        (still 201, still one reaction). To remove a reaction you call
        DELETE /{post_id}/reactions instead (see test_remove_reaction).
        """
        response1 = client.post(
            f"/api/posts/{test_post.id}/reactions",
            json={"reaction_type": "like"},
            headers=auth_headers,
        )
        assert response1.status_code == 201
        assert response1.json()["reactions_count"] == 1

        # Reacting again with the same type does not remove or duplicate it
        response2 = client.post(
            f"/api/posts/{test_post.id}/reactions",
            json={"reaction_type": "like"},
            headers=auth_headers,
        )
        assert response2.status_code == 201
        assert response2.json()["reactions_count"] == 1
        assert response2.json()["user_reaction"] == "like"


# Challenge Solutions


@pytest.mark.integration
@pytest.mark.api
class TestCompleteUserJourney:
    """Test complete user journey from registration to posting."""

    def test_full_user_flow(self, client):
        """Test: Register → Login → Create Post → Comment → React."""
        # Step 1: Register
        register_response = client.post(
            "/api/auth/register",
            json={
                "email": "journey@test.com",
                "username": "journeyuser",
                "display_name": "Journey User",
                "password": "Test123!",
            },
        )
        assert register_response.status_code == 201
        register_data = register_response.json()
        token = register_data["access_token"]
        # Verify user data is returned immediately
        assert register_data["username"] == "journeyuser"
        headers = {"Authorization": f"Bearer {token}"}

        # Step 2: Verify auto-login (get current user)
        me_response = client.get("/api/auth/me", headers=headers)
        assert me_response.status_code == 200
        assert me_response.json()["username"] == "journeyuser"

        # Step 3: Create post
        post_response = client.post(
            "/api/posts/",
            json={"content": "My first post!"},
            headers=headers,
        )
        assert post_response.status_code == 201
        post_id = post_response.json()["id"]

        # Step 4: Get the post
        get_response = client.get(f"/api/posts/{post_id}", headers=headers)
        assert get_response.status_code == 200
        assert get_response.json()["content"] == "My first post!"

        # Step 5: Add comment
        comment_response = client.post(
            f"/api/posts/{post_id}/comments",
            json={"content": "Commenting on my own post!"},
            headers=headers,
        )
        assert comment_response.status_code == 201

        # Step 6: Add reaction
        reaction_response = client.post(
            f"/api/posts/{post_id}/reactions",
            json={"reaction_type": "love"},
            headers=headers,
        )
        assert reaction_response.status_code == 201


# Grading Notes for Instructors:
#
# EXCELLENT (95-100%):
# - All required endpoint tests present
# - Tests both success and error cases
# - Tests authentication properly
# - Comprehensive assertions (status code + response data)
# - Well-documented
# - Bonus: Complete user journey test
#
# GOOD (85-94%):
# - Most endpoint tests present
# - Tests main scenarios
# - Good use of fixtures
# - Checks status codes and basic response data
#
# ACCEPTABLE (75-84%):
# - Basic endpoint tests present
# - Some use of auth headers
# - Basic assertions
# - May be missing error cases
#
# NEEDS IMPROVEMENT (<75%):
# - Missing endpoint tests
# - Not testing authentication
# - Only checking status codes
# - Not using fixtures properly
#
# Common deductions:
# - Not testing error cases: -15 points
# - Using `data=` instead of `json=`: -10 points
# - Not checking response content: -10 points
# - Hardcoded URLs/IDs: -10 points
# - Missing auth headers on protected endpoints: -15 points
