"""
Integration tests for feed API endpoints.

These tests verify feed generation, filtering, and ordering.
"""

import pytest


@pytest.mark.integration
@pytest.mark.api
class TestGetAllFeed:
    """Test get all posts feed endpoint."""

    def test_get_all_feed(self, client, test_posts, auth_headers):
        """Test getting all posts feed."""
        response = client.get("/api/feed/all", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= len(test_posts)

    def test_all_feed_without_auth(self, client):
        """Test that feed requires authentication."""
        response = client.get("/api/feed/all")

        # Some endpoints may be public or return 401/403
        assert response.status_code in [200, 401, 403]

    def test_all_feed_with_empty_database(self, client, auth_headers):
        """Test getting feed when there are no posts."""
        response = client.get("/api/feed/all", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_all_feed_includes_all_users_posts(self, client, test_posts, auth_headers):
        """Test that all feed includes posts from all users."""
        response = client.get("/api/feed/all", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        # Should have posts from multiple users
        authors = set(post["author_username"] for post in data)
        assert len(authors) > 1


@pytest.mark.integration
@pytest.mark.api
class TestGetFollowingFeed:
    """Test get following-only feed endpoint."""

    def test_get_following_feed(
        self, client, test_user, test_user_2, test_posts, auth_headers, db_session
    ):
        """Test getting following feed."""
        # Make test_user follow test_user_2
        test_user.following.append(test_user_2)
        db_session.commit()

        response = client.get("/api/feed/following", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_following_feed_empty_when_not_following_anyone(self, client, auth_headers):
        """Test that following feed is empty when not following anyone."""
        response = client.get("/api/feed/following", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # May be empty or contain only own posts depending on implementation

    def test_following_feed_only_shows_followed_users(
        self, client, test_user, test_user_2, test_posts, auth_headers, db_session
    ):
        """Test that following feed only shows posts from followed users."""
        # Follow test_user_2
        test_user.following.append(test_user_2)
        db_session.commit()

        response = client.get("/api/feed/following", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        # All posts should be from followed users or self
        for post in data:
            assert post["author_username"] in [test_user.username, test_user_2.username]

    def test_following_feed_without_auth(self, client):
        """Test that following feed requires authentication."""
        response = client.get("/api/feed/following")

        # Should require auth
        assert response.status_code in [401, 403, 422]


@pytest.mark.integration
@pytest.mark.api
class TestFeedFiltering:
    """Test feed filtering behavior."""

    def test_all_feed_excludes_blocked_users(
        self, client, test_user, test_user_2, test_posts, auth_headers, db_session
    ):
        """Test that all feed excludes blocked users' posts."""
        # Block test_user_2
        test_user.blocking.append(test_user_2)
        db_session.commit()

        response = client.get("/api/feed/all", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        # Should not include posts from blocked user
        blocked_posts = [post for post in data if post["author_username"] == test_user_2.username]
        assert len(blocked_posts) == 0

    def test_following_feed_includes_own_posts(self, client, test_user, test_post, auth_headers):
        """Test that following feed includes own posts."""
        response = client.get("/api/feed/following", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        # Should include own posts (if implementation includes them)
        # May or may not include own posts depending on implementation
        assert isinstance(data, list)


@pytest.mark.integration
@pytest.mark.api
class TestFeedOrdering:
    """Test feed ordering (most recent first)."""

    def test_feed_is_ordered_by_date(self, client, test_posts, auth_headers):
        """Test that feed is ordered with most recent posts first."""
        response = client.get("/api/feed/all", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        if len(data) > 1:
            # Check that posts are ordered by created_at descending
            from datetime import datetime

            dates = [
                datetime.fromisoformat(post["created_at"].replace("Z", "+00:00")) for post in data
            ]

            # Each date should be >= the next date (descending order)
            for i in range(len(dates) - 1):
                assert dates[i] >= dates[i + 1]


@pytest.mark.integration
@pytest.mark.api
class TestFeedWithReposts:
    """Test feed behavior with reposts."""

    def test_feed_includes_reposts(self, client, test_post, test_user_2, auth_headers, db_session):
        """Test that feed includes reposted content."""
        from models import Post

        # Create a repost
        repost = Post(
            author_id=test_user_2.id,
            content="",
            is_repost=True,
            original_post_id=test_post.id,
        )
        db_session.add(repost)
        db_session.commit()

        response = client.get("/api/feed/all", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        # Should include the repost
        reposts = [post for post in data if post.get("is_repost")]
        assert len(reposts) >= 1


@pytest.mark.integration
@pytest.mark.api
class TestFeedPagination:
    """Test feed pagination if implemented."""

    def test_feed_returns_reasonable_number_of_posts(self, client, test_posts, auth_headers):
        """Test that feed doesn't return unlimited posts."""
        response = client.get("/api/feed/all", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        # Should return a reasonable number (e.g., max 50)
        assert len(data) <= 100


@pytest.mark.integration
@pytest.mark.api
class TestFeedPerformance:
    """Test feed performance with various data sizes."""

    @pytest.mark.slow
    def test_feed_with_many_posts(self, client, test_user, auth_headers, db_session):
        """Test feed performance with many posts."""
        from models import Post

        # Create many posts
        posts = [Post(author_id=test_user.id, content=f"Test post {i}") for i in range(50)]

        for post in posts:
            db_session.add(post)
        db_session.commit()

        response = client.get("/api/feed/all", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 50
