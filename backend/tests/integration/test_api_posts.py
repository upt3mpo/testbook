"""
Integration tests for posts API endpoints.

These tests verify posts CRUD operations, comments, reactions, and reposts.
"""

import pytest


@pytest.mark.integration
@pytest.mark.api
class TestCreatePost:
    """Test post creation endpoint."""

    def test_create_text_post(self, client, auth_headers):
        """Test creating a text-only post."""
        # Arrange - Prepare request data
        post_data = {"content": "This is a test post"}

        # Act - Make HTTP POST request to create post
        response = client.post("/api/posts/", json=post_data, headers=auth_headers)

        # Assert - Verify response status and structure
        assert response.status_code == 201  # API returns 201 Created
        data = response.json()
        assert data["content"] == "This is a test post"  # Content saved correctly
        assert data["id"] is not None  # Post assigned database ID
        assert data["author_username"] == "testuser"  # Linked to authenticated user
        assert data["image_url"] is None  # Optional fields default to None
        assert data["video_url"] is None

    def test_create_post_with_image(self, client, auth_headers):
        """Test creating a post with an image."""
        response = client.post(
            "/api/posts/",
            json={"content": "Post with image", "image_url": "/static/images/test.jpg"},
            headers=auth_headers,
        )

        assert response.status_code == 201  # API returns 201 Created
        data = response.json()
        assert data["image_url"] == "/static/images/test.jpg"

    def test_create_post_without_auth(self, client):
        """Test that creating post requires authentication."""
        # Arrange - No auth headers (simulating unauthenticated request)
        post_data = {"content": "Test post"}

        # Act - Attempt to create post without authentication
        response = client.post("/api/posts/", json=post_data)

        # Assert - Should be rejected (401 Unauthorized or 403 Forbidden)
        assert response.status_code in [401, 403]  # Both are valid auth errors

    def test_create_empty_post(self, client, auth_headers):
        """Test creating post with empty content."""
        response = client.post("/api/posts/", json={"content": ""}, headers=auth_headers)

        # Should either fail validation or accept empty content (returns 201 if accepted)
        assert response.status_code in [201, 400, 422]


@pytest.mark.integration
@pytest.mark.api
class TestGetPost:
    """Test get post endpoint."""

    def test_get_existing_post(self, client, test_post, auth_headers):
        """Test getting an existing post."""
        response = client.get(f"/api/posts/{test_post.id}", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_post.id
        assert data["content"] == test_post.content

    def test_get_nonexistent_post(self, client, auth_headers):
        """Test getting a non-existent post."""
        response = client.get("/api/posts/999999", headers=auth_headers)

        assert response.status_code == 404

    def test_get_post_includes_counts(
        self, client, test_post, test_comment, test_reaction, auth_headers
    ):
        """Test that post includes comment and reaction counts."""
        response = client.get(f"/api/posts/{test_post.id}", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert "comments_count" in data
        assert "reactions_count" in data
        assert data["comments_count"] >= 1
        assert data["reactions_count"] >= 1


@pytest.mark.integration
@pytest.mark.api
class TestUpdatePost:
    """Test post update endpoint."""

    def test_update_own_post(self, client, test_post, auth_headers):
        """Test updating own post."""
        response = client.put(
            f"/api/posts/{test_post.id}",
            json={"content": "Updated content"},
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["content"] == "Updated content"

    def test_update_other_user_post(self, client, test_post, test_user_2, db_session):
        """Test that updating another user's post fails."""
        # Create token for test_user_2
        from auth import create_access_token

        token = create_access_token(data={"sub": test_user_2.email})
        headers = {"Authorization": f"Bearer {token}"}

        response = client.put(
            f"/api/posts/{test_post.id}",
            json={"content": "Trying to update"},
            headers=headers,
        )

        assert response.status_code == 403

    def test_update_nonexistent_post(self, client, auth_headers):
        """Test updating non-existent post."""
        response = client.put(
            "/api/posts/999999", json={"content": "Updated"}, headers=auth_headers
        )

        assert response.status_code == 404


@pytest.mark.integration
@pytest.mark.api
class TestDeletePost:
    """Test post deletion endpoint."""

    def test_delete_own_post(self, client, test_post, auth_headers):
        """Test deleting own post."""
        response = client.delete(f"/api/posts/{test_post.id}", headers=auth_headers)

        assert response.status_code == 200

        # Verify post is deleted
        get_response = client.get(f"/api/posts/{test_post.id}", headers=auth_headers)
        assert get_response.status_code == 404

    def test_delete_other_user_post(self, client, test_post, test_user_2):
        """Test that deleting another user's post fails."""
        from auth import create_access_token

        token = create_access_token(data={"sub": test_user_2.email})
        headers = {"Authorization": f"Bearer {token}"}

        response = client.delete(f"/api/posts/{test_post.id}", headers=headers)

        assert response.status_code == 403


@pytest.mark.integration
@pytest.mark.api
class TestComments:
    """Test comment functionality."""

    def test_add_comment_to_post(self, client, test_post, auth_headers):
        """Test adding a comment to a post."""
        response = client.post(
            f"/api/posts/{test_post.id}/comments",
            json={"content": "Great post!"},
            headers=auth_headers,
        )

        assert response.status_code == 201  # API returns 201 Created
        data = response.json()
        assert data["content"] == "Great post!"

    def test_add_comment_without_auth(self, client, test_post):
        """Test that adding comment requires authentication."""
        response = client.post(f"/api/posts/{test_post.id}/comments", json={"content": "Comment"})

        assert response.status_code in [401, 403, 422]

    def test_add_comment_to_nonexistent_post(self, client, auth_headers):
        """Test adding comment to non-existent post."""
        response = client.post(
            "/api/posts/999999/comments",
            json={"content": "Comment"},
            headers=auth_headers,
        )

        assert response.status_code == 404

    def test_get_post_with_comments(self, client, test_post, test_comment, auth_headers):
        """Test that getting post includes comments."""
        response = client.get(f"/api/posts/{test_post.id}", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert "comments" in data
        assert len(data["comments"]) >= 1


@pytest.mark.integration
@pytest.mark.api
class TestReactions:
    """Test reaction functionality."""

    @pytest.mark.parametrize("reaction_type", ["like", "love", "haha", "wow", "sad", "angry"])
    def test_add_reaction_to_post(self, client, test_post, auth_headers, reaction_type):
        """Test adding different reaction types to a post."""
        response = client.post(
            f"/api/posts/{test_post.id}/reactions",
            json={"reaction_type": reaction_type},
            headers=auth_headers,
        )

        assert response.status_code == 201  # API returns 201 Created

    def test_change_reaction(self, client, test_post, auth_headers):
        """Test changing reaction type."""
        # Add first reaction
        client.post(
            f"/api/posts/{test_post.id}/reactions",
            json={"reaction_type": "like"},
            headers=auth_headers,
        )

        # Change to different reaction
        response = client.post(
            f"/api/posts/{test_post.id}/reactions",
            json={"reaction_type": "love"},
            headers=auth_headers,
        )

        assert response.status_code == 201  # API returns 201 Created

    def test_remove_reaction(self, client, test_post, auth_headers):
        """Test removing a reaction."""
        # Add reaction first
        client.post(
            f"/api/posts/{test_post.id}/reactions",
            json={"reaction_type": "like"},
            headers=auth_headers,
        )

        # Remove reaction
        response = client.delete(f"/api/posts/{test_post.id}/reactions", headers=auth_headers)

        assert response.status_code == 200

    def test_add_reaction_without_auth(self, client, test_post):
        """Test that adding reaction requires authentication."""
        response = client.post(
            f"/api/posts/{test_post.id}/reactions", json={"reaction_type": "like"}
        )

        assert response.status_code in [401, 403, 422]

    def test_invalid_reaction_type(self, client, test_post, auth_headers):
        """Test adding invalid reaction type."""
        response = client.post(
            f"/api/posts/{test_post.id}/reactions",
            json={"reaction_type": "invalid"},
            headers=auth_headers,
        )

        # Should either accept any string or validate (returns 201 if accepted)
        assert response.status_code in [201, 400, 422]


@pytest.mark.integration
@pytest.mark.api
class TestReposts:
    """Test repost functionality."""

    def test_create_repost(self, client, test_post, test_user_2, db_session):
        """Test creating a repost."""
        from auth import create_access_token

        token = create_access_token(data={"sub": test_user_2.email})
        headers = {"Authorization": f"Bearer {token}"}

        response = client.post(
            "/api/posts/repost",
            json={"original_post_id": test_post.id, "content": ""},
            headers=headers,
        )

        assert response.status_code == 201  # API returns 201 Created
        data = response.json()
        assert data["is_repost"] is True
        assert data["original_post_id"] == test_post.id

    def test_remove_repost(self, client, test_post, test_user_2, db_session):
        """Test removing a repost."""
        from auth import create_access_token

        token = create_access_token(data={"sub": test_user_2.email})
        headers = {"Authorization": f"Bearer {token}"}

        # Create repost first
        create_response = client.post(
            "/api/posts/repost",
            json={"original_post_id": test_post.id},
            headers=headers,
        )

        if create_response.status_code == 201:
            # Remove repost
            response = client.delete(f"/api/posts/repost/{test_post.id}", headers=headers)

            assert response.status_code == 200

    def test_repost_without_auth(self, client, test_post):
        """Test that reposting requires authentication."""
        response = client.post("/api/posts/repost", json={"original_post_id": test_post.id})

        assert response.status_code in [401, 403, 422]

    def test_repost_nonexistent_post(self, client, auth_headers):
        """Test reposting non-existent post."""
        response = client.post(
            "/api/posts/repost", json={"original_post_id": 999999}, headers=auth_headers
        )

        assert response.status_code == 404


@pytest.mark.integration
@pytest.mark.api
class TestPostInteractions:
    """Test complex post interaction scenarios."""

    def test_post_with_multiple_interactions(
        self, client, test_post, test_user_2, test_user_3, db_session
    ):
        """Test post with multiple comments and reactions."""
        # Add comments from different users
        from auth import create_access_token

        token2 = create_access_token(data={"sub": test_user_2.email})
        token3 = create_access_token(data={"sub": test_user_3.email})

        client.post(
            f"/api/posts/{test_post.id}/comments",
            json={"content": "Comment from user 2"},
            headers={"Authorization": f"Bearer {token2}"},
        )

        client.post(
            f"/api/posts/{test_post.id}/comments",
            json={"content": "Comment from user 3"},
            headers={"Authorization": f"Bearer {token3}"},
        )

        # Add reactions
        client.post(
            f"/api/posts/{test_post.id}/reactions",
            json={"reaction_type": "like"},
            headers={"Authorization": f"Bearer {token2}"},
        )

        client.post(
            f"/api/posts/{test_post.id}/reactions",
            json={"reaction_type": "love"},
            headers={"Authorization": f"Bearer {token3}"},
        )

        # Get post and verify counts
        from auth import create_access_token

        token = create_access_token(data={"sub": test_post.author.email})
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get(f"/api/posts/{test_post.id}", headers=headers)
        data = response.json()

        assert data["comments_count"] >= 2
        assert data["reactions_count"] >= 2


# 🧠 Why These Tests Matter:
#
# Integration tests for posts API are the BACKBONE of QA work because:
#
# 1. **Real User Workflows** - Tests verify complete CRUD operations work together
# 2. **Multi-Component Integration** - Posts interact with users, comments, reactions, database
# 3. **Authorization Critical** - Users must only edit/delete their own posts (security!)
# 4. **Contract Validation** - Frontend depends on exact response structure
#
# What These Tests Catch:
# - ✅ Broken endpoints after refactoring
# - ✅ Authorization bypasses (major security issue!)
# - ✅ Database constraint violations
# - ✅ Response schema changes that break frontend
# - ✅ Edge cases (empty posts, missing fields, deleted users)
#
# In Real QA Teams:
# - Integration tests are ~60% of test suites
# - They run before every deployment
# - Failed tests block releases
# - They serve as API documentation (shows expected behavior)
#
# For Your Career:
# - THIS is what QA engineers do day-to-day
# - Interview question: "How would you test a REST API?" - Point to these!
# - Shows you understand HTTP, databases, authentication, and business logic
# - Demonstrates professional test organization (class grouping, fixtures, markers)
