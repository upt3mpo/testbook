"""
Integration tests for users API endpoints.

These tests verify user profile management, follow/unfollow,
block/unblock, and user relationships.
"""

import pytest


@pytest.mark.integration
@pytest.mark.api
class TestGetUserProfile:
    """Test get user profile endpoint."""

    def test_get_user_by_username(self, client, test_user, auth_headers) -> None:
        """Test getting user profile by username."""
        response = client.get(f"/api/users/{test_user.username}", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["username"] == test_user.username
        assert data["display_name"] == test_user.display_name

    def test_get_user_profile_never_exposes_password_hash(
        self, client, test_user, auth_headers
    ) -> None:
        """Security invariant: a user profile response must never include the hashed password."""
        response = client.get(f"/api/users/{test_user.username}", headers=auth_headers)

        assert (
            "hashed_password" not in response.json()
        ), f"User profile response leaked the password hash: {response.json()}"

    def test_get_nonexistent_user(self, client, auth_headers) -> None:
        """Test getting non-existent user."""
        response = client.get("/api/users/nonexistentuser", headers=auth_headers)

        assert response.status_code == 404

    def test_get_user_includes_counts(self, client, test_user, auth_headers) -> None:
        """Test that user profile includes follower/following/posts counts."""
        response = client.get(f"/api/users/{test_user.username}", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert "followers_count" in data
        assert "following_count" in data
        assert "posts_count" in data


@pytest.mark.integration
@pytest.mark.api
class TestUpdateUserProfile:
    """Test update user profile endpoint."""

    def test_update_own_profile(self, client, auth_headers) -> None:
        """Test updating own profile."""
        response = client.put(
            "/api/users/me",
            json={"display_name": "Updated Name", "bio": "Updated bio"},
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["display_name"] == "Updated Name"
        assert data["bio"] == "Updated bio"

    def test_update_profile_without_auth(self, client) -> None:
        """Test that updating profile requires authentication."""
        response = client.put("/api/users/me", json={"display_name": "New Name"})

        assert response.status_code in [401, 403, 422]

    @pytest.mark.parametrize(
        ("field", "value"),
        [
            pytest.param("theme", "dark", id="theme"),
            pytest.param("text_density", "compact", id="text_density"),
        ],
    )
    def test_update_display_preference(
        self, client, auth_headers, field, value
    ) -> None:
        """PUT /api/users/me updates a single display preference field and echoes the new value back.

        theme and text_density are both simple, independent preference
        fields updated through the same endpoint the same way - there's
        no interaction between them worth a separate test each.
        """
        response = client.put(
            "/api/users/me", json={field: value}, headers=auth_headers
        )

        assert (
            response.status_code == 200
        ), f"Expected 200 updating {field}, got {response.status_code}: {response.text}"
        data = response.json()
        assert (
            data[field] == value
        ), f"Expected {field}={value!r}, got {data.get(field)!r}"


@pytest.mark.integration
@pytest.mark.api
class TestFollowUnfollow:
    """Test follow/unfollow functionality."""

    def test_follow_user(self, client, test_user_2, auth_headers) -> None:
        """Test following another user."""
        response = client.post(
            f"/api/users/{test_user_2.username}/follow", headers=auth_headers
        )

        assert response.status_code == 200
        assert "following" in response.json()["message"].lower()

    def test_unfollow_user(
        self, client, test_user_2, auth_headers, db_session, test_user
    ) -> None:
        """Test unfollowing a user."""
        # Follow first
        test_user.following.append(test_user_2)
        db_session.commit()

        # Then unfollow
        response = client.delete(
            f"/api/users/{test_user_2.username}/follow", headers=auth_headers
        )

        assert response.status_code == 200
        assert "unfollowed" in response.json()["message"].lower()

    def test_follow_nonexistent_user(self, client, auth_headers) -> None:
        """Test following non-existent user."""
        response = client.post(
            "/api/users/nonexistentuser/follow", headers=auth_headers
        )

        assert response.status_code == 404

    def test_follow_yourself(self, client, auth_headers, test_user) -> None:
        """Test that you cannot follow yourself."""
        response = client.post(
            f"/api/users/{test_user.username}/follow", headers=auth_headers
        )

        # Should either fail or be ignored
        assert response.status_code in [200, 400]

    def test_follow_without_auth(self, client, test_user_2) -> None:
        """Test that following requires authentication."""
        response = client.post(f"/api/users/{test_user_2.username}/follow")

        assert response.status_code in [401, 403, 422]

    def test_double_follow(
        self, client, test_user_2, auth_headers, db_session, test_user
    ) -> None:
        """Test following the same user twice."""
        # Follow once
        test_user.following.append(test_user_2)
        db_session.commit()

        # Try to follow again
        response = client.post(
            f"/api/users/{test_user_2.username}/follow", headers=auth_headers
        )

        # Should handle gracefully
        assert response.status_code in [200, 400]


@pytest.mark.integration
@pytest.mark.api
class TestBlockUnblock:
    """Test block/unblock functionality."""

    def test_block_user(self, client, test_user_2, auth_headers) -> None:
        """Test blocking another user."""
        response = client.post(
            f"/api/users/{test_user_2.username}/block", headers=auth_headers
        )

        assert response.status_code == 200
        assert "blocked" in response.json()["message"].lower()

    def test_unblock_user(
        self, client, test_user_2, auth_headers, db_session, test_user
    ) -> None:
        """Test unblocking a user."""
        # Block first
        test_user.blocking.append(test_user_2)
        db_session.commit()

        # Then unblock
        response = client.delete(
            f"/api/users/{test_user_2.username}/block", headers=auth_headers
        )

        assert response.status_code == 200
        assert "unblocked" in response.json()["message"].lower()

    def test_block_yourself(self, client, auth_headers, test_user) -> None:
        """Test that you cannot block yourself."""
        response = client.post(
            f"/api/users/{test_user.username}/block", headers=auth_headers
        )

        # Should either fail or be ignored
        assert response.status_code in [200, 400]

    def test_block_without_auth(self, client, test_user_2) -> None:
        """Test that blocking requires authentication."""
        response = client.post(f"/api/users/{test_user_2.username}/block")

        assert response.status_code in [401, 403, 422]


@pytest.mark.integration
@pytest.mark.api
class TestGetFollowersFollowing:
    """Test get followers/following list endpoints."""

    def test_get_followers_list(
        self, client, test_user, test_user_2, db_session, auth_headers
    ) -> None:
        """Test getting user's followers list."""
        # Make test_user_2 follow test_user
        test_user_2.following.append(test_user)
        db_session.commit()

        response = client.get(
            f"/api/users/{test_user.username}/followers", headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_get_following_list(
        self, client, test_user, test_user_2, db_session, auth_headers
    ) -> None:
        """Test getting user's following list."""
        # Make test_user follow test_user_2
        test_user.following.append(test_user_2)
        db_session.commit()

        response = client.get(
            f"/api/users/{test_user.username}/following", headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_get_followers_empty_list(self, client, test_user, auth_headers) -> None:
        """Test getting followers list when user has no followers."""
        response = client.get(
            f"/api/users/{test_user.username}/followers", headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_followers_requires_auth(self, client, test_user) -> None:
        """Test that getting followers requires authentication."""
        response = client.get(f"/api/users/{test_user.username}/followers")

        # Should require auth
        assert response.status_code in [401, 403, 422]


@pytest.mark.integration
@pytest.mark.api
class TestGetUserPosts:
    """Test get user's posts endpoint."""

    def test_get_user_posts(self, client, test_user, test_post, auth_headers) -> None:
        """Test getting a user's posts."""
        response = client.get(
            f"/api/users/{test_user.username}/posts", headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["author_username"] == test_user.username

    def test_get_posts_for_user_with_no_posts(
        self, client, test_user_2, auth_headers
    ) -> None:
        """Test getting posts for user with no posts."""
        response = client.get(
            f"/api/users/{test_user_2.username}/posts", headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


@pytest.mark.integration
@pytest.mark.api
class TestDeleteAccount:
    """Test delete account functionality."""

    def test_delete_own_account(self, client, auth_headers, test_user) -> None:
        """Test deleting own account."""
        response = client.delete("/api/users/me", headers=auth_headers)

        assert response.status_code == 200

        # Verify the user is actually gone, not just that the delete call
        # returned 200. A bare TestClient.get() doesn't raise on HTTP
        # errors, so there's no exception here to catch - the earlier
        # try/except around this assert was silently swallowing real
        # assertion failures (AssertionError is an Exception too).
        get_response = client.get(
            f"/api/users/{test_user.username}", headers=auth_headers
        )
        assert get_response.status_code in [401, 404], (
            "Deleted user's profile should be gone (404) or the token should "
            f"be invalidated (401), got {get_response.status_code}"
        )

    def test_delete_account_without_auth(self, client) -> None:
        """Test that deleting account requires authentication."""
        response = client.delete("/api/users/me")

        assert response.status_code in [
            401,
            403,
        ], f"Deleting an account with no auth header should be rejected, got {response.status_code}"


@pytest.mark.integration
@pytest.mark.api
class TestUserRelationships:
    """Test complex user relationship scenarios."""

    def test_follow_then_block(
        self, client, test_user, test_user_2, auth_headers, db_session
    ) -> None:
        """Test following then blocking a user."""
        # Follow
        test_user.following.append(test_user_2)
        db_session.commit()

        # Block
        response = client.post(
            f"/api/users/{test_user_2.username}/block", headers=auth_headers
        )

        assert response.status_code == 200

        # Verify still blocked even if followed
        db_session.refresh(test_user)
        assert test_user_2 in test_user.blocking

    def test_mutual_follow(
        self, client, test_user, test_user_2, auth_headers, db_session
    ) -> None:
        """Test mutual following between two users."""
        from auth import create_access_token

        # User 1 follows User 2
        test_user.following.append(test_user_2)
        db_session.commit()

        # User 2 follows User 1
        token2 = create_access_token(data={"sub": test_user_2.email})
        headers2 = {"Authorization": f"Bearer {token2}"}

        response = client.post(
            f"/api/users/{test_user.username}/follow", headers=headers2
        )

        assert response.status_code == 200

        # Verify mutual following
        db_session.refresh(test_user)
        db_session.refresh(test_user_2)
        assert test_user_2 in test_user.following
        assert test_user in test_user_2.following
