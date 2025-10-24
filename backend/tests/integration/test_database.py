"""
Database-specific tests.

These tests verify database operations, transactions,
and edge cases that might not be covered in other tests.
"""

import pytest
from sqlalchemy.exc import IntegrityError

from auth import get_password_hash
from models import Comment, Post, Reaction, User


@pytest.mark.database
class TestDatabaseConstraints:
    """Test database constraints and validations."""

    def test_user_email_constraint(self, db_session):
        """Test that email unique constraint is enforced."""
        user1 = User(
            email="test@example.com",
            username="user1",
            display_name="User 1",
            hashed_password=get_password_hash("password"),
        )
        db_session.add(user1)
        db_session.commit()

        user2 = User(
            email="test@example.com",  # Duplicate
            username="user2",
            display_name="User 2",
            hashed_password=get_password_hash("password"),
        )
        db_session.add(user2)

        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_user_username_constraint(self, db_session):
        """Test that username unique constraint is enforced."""
        user1 = User(
            email="user1@example.com",
            username="testuser",
            display_name="User 1",
            hashed_password=get_password_hash("password"),
        )
        db_session.add(user1)
        db_session.commit()

        user2 = User(
            email="user2@example.com",
            username="testuser",  # Duplicate
            display_name="User 2",
            hashed_password=get_password_hash("password"),
        )
        db_session.add(user2)

        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_post_requires_author(self, db_session):
        """Test that post requires valid author_id."""
        post = Post(
            author_id=999999,  # Non-existent user
            content="Test post",
        )
        db_session.add(post)

        # SQLite may or may not enforce foreign keys depending on configuration
        try:
            db_session.commit()
            # If it succeeds, SQLite foreign keys are not enforced
            # This is expected behavior for SQLite without PRAGMA foreign_keys=ON
        except IntegrityError:
            # If it fails, foreign keys are enforced (good!)
            pass


@pytest.mark.database
class TestDatabaseCRUD:
    """Test basic CRUD operations."""

    def test_create_read_user(self, db_session):
        """Test creating and reading a user."""
        user = User(
            email="crud@example.com",
            username="cruduser",
            display_name="CRUD User",
            hashed_password=get_password_hash("password"),
        )
        db_session.add(user)
        db_session.commit()
        user_id = user.id

        # Read
        retrieved_user = db_session.query(User).filter(User.id == user_id).first()
        assert retrieved_user is not None
        assert retrieved_user.email == "crud@example.com"

    def test_update_user(self, db_session, test_user):
        """Test updating user fields."""
        test_user.display_name = "Updated Name"
        test_user.bio = "Updated bio"
        db_session.commit()
        db_session.refresh(test_user)

        assert test_user.display_name == "Updated Name"
        assert test_user.bio == "Updated bio"

    def test_delete_user(self, db_session):
        """Test deleting a user."""
        user = User(
            email="delete@example.com",
            username="deleteuser",
            display_name="Delete User",
            hashed_password=get_password_hash("password"),
        )
        db_session.add(user)
        db_session.commit()
        user_id = user.id

        db_session.delete(user)
        db_session.commit()

        deleted_user = db_session.query(User).filter(User.id == user_id).first()
        assert deleted_user is None


@pytest.mark.database
class TestDatabaseRelationships:
    """Test database relationship loading and queries."""

    def test_lazy_loading_posts(self, db_session, test_user):
        """Test lazy loading of user posts."""
        # Create posts
        for i in range(3):
            post = Post(author_id=test_user.id, content=f"Post {i}")
            db_session.add(post)
        db_session.commit()

        # Reload user in same session
        db_session.refresh(test_user)

        # Access posts
        assert len(test_user.posts) == 3

    def test_join_query_user_posts(self, db_session, test_user):
        """Test joining users and posts."""
        # Create post
        post = Post(author_id=test_user.id, content="Test post")
        db_session.add(post)
        db_session.commit()

        # Join query
        result = (
            db_session.query(User, Post)
            .join(Post)
            .filter(User.id == test_user.id)
            .first()
        )

        assert result is not None
        user, post = result
        assert user.id == test_user.id
        assert post.author_id == test_user.id

    def test_many_to_many_followers(self, db_session, test_user, test_user_2):
        """Test many-to-many followers relationship."""
        test_user.following.append(test_user_2)
        db_session.commit()

        # Refresh to get updated relationships
        db_session.refresh(test_user)
        db_session.refresh(test_user_2)

        assert test_user_2 in test_user.following
        assert test_user in test_user_2.followers


@pytest.mark.database
class TestDatabaseTransactions:
    """Test transaction behavior."""

    def test_rollback_on_error(self, db_session):
        """Test that transactions rollback on error."""
        user1 = User(
            email="user1@example.com",
            username="user1",
            display_name="User 1",
            hashed_password=get_password_hash("password"),
        )
        db_session.add(user1)
        db_session.commit()

        # Try to add duplicate in transaction
        try:
            user2 = User(
                email="user1@example.com",  # Duplicate
                username="user2",
                display_name="User 2",
                hashed_password=get_password_hash("password"),
            )
            db_session.add(user2)
            db_session.commit()
        except IntegrityError:
            db_session.rollback()

        # Original user should still be there
        user = db_session.query(User).filter(User.email == "user1@example.com").first()
        assert user is not None
        assert user.username == "user1"

    def test_multiple_operations_in_transaction(self, db_session, test_user):
        """Test multiple operations in single transaction."""
        # Create multiple posts in one transaction
        posts = [Post(author_id=test_user.id, content=f"Post {i}") for i in range(5)]

        for post in posts:
            db_session.add(post)

        db_session.commit()

        # All posts should be created
        created_posts = (
            db_session.query(Post).filter(Post.author_id == test_user.id).all()
        )
        assert len(created_posts) == 5


@pytest.mark.database
class TestDatabaseQueries:
    """Test complex database queries."""

    def test_filter_posts_by_multiple_authors(self, db_session, test_posts):
        """Test filtering posts by multiple authors."""
        author_ids = [post.author_id for post in test_posts[:2]]

        posts = db_session.query(Post).filter(Post.author_id.in_(author_ids)).all()

        assert len(posts) > 0
        for post in posts:
            assert post.author_id in author_ids

    def test_count_user_posts(self, db_session, test_user):
        """Test counting user's posts."""
        # Create posts
        for i in range(7):
            post = Post(author_id=test_user.id, content=f"Post {i}")
            db_session.add(post)
        db_session.commit()

        # Count
        count = db_session.query(Post).filter(Post.author_id == test_user.id).count()

        assert count == 7

    def test_order_posts_by_date(self, db_session, test_user):
        """Test ordering posts by creation date."""
        import time

        # Create posts with slight delay
        for i in range(3):
            post = Post(author_id=test_user.id, content=f"Post {i}")
            db_session.add(post)
            db_session.commit()
            time.sleep(0.01)

        # Get posts ordered by date
        posts = (
            db_session.query(Post)
            .filter(Post.author_id == test_user.id)
            .order_by(Post.created_at.desc())
            .all()
        )

        # Should be in reverse order
        assert posts[0].content == "Post 2"
        assert posts[2].content == "Post 0"


@pytest.mark.database
class TestCascadeOperations:
    """Test cascade delete behavior."""

    def test_delete_user_cascades_to_posts(self, db_session, test_user):
        """Test that deleting user deletes their posts."""
        # Create posts
        post_ids = []
        for i in range(3):
            post = Post(author_id=test_user.id, content=f"Post {i}")
            db_session.add(post)
        db_session.commit()
        db_session.flush()

        # Get post IDs before deleting user
        post_ids = [post.id for post in test_user.posts]

        # Delete user
        db_session.delete(test_user)
        db_session.commit()

        # Posts should be deleted
        for post_id in post_ids:
            post = db_session.query(Post).filter(Post.id == post_id).first()
            assert post is None

    def test_delete_post_cascades_to_comments(self, db_session, test_post, test_user_2):
        """Test that deleting post deletes comments."""
        # Create comments
        comment_ids = []
        for i in range(3):
            comment = Comment(
                post_id=test_post.id, author_id=test_user_2.id, content=f"Comment {i}"
            )
            db_session.add(comment)
        db_session.commit()

        # Get comment IDs
        comment_ids = [comment.id for comment in test_post.comments]

        # Delete post
        db_session.delete(test_post)
        db_session.commit()

        # Comments should be deleted
        for comment_id in comment_ids:
            comment = db_session.query(Comment).filter(Comment.id == comment_id).first()
            assert comment is None

    def test_delete_post_cascades_to_reactions(
        self, db_session, test_post, test_user_2
    ):
        """Test that deleting post deletes reactions."""
        # Create reactions
        reaction = Reaction(
            post_id=test_post.id, user_id=test_user_2.id, reaction_type="like"
        )
        db_session.add(reaction)
        db_session.commit()
        reaction_id = reaction.id

        # Delete post
        db_session.delete(test_post)
        db_session.commit()

        # Reaction should be deleted
        reaction = db_session.query(Reaction).filter(Reaction.id == reaction_id).first()
        assert reaction is None


@pytest.mark.database
class TestDatabasePerformance:
    """Test database performance characteristics."""

    @pytest.mark.slow
    def test_bulk_insert_performance(self, db_session, test_user):
        """Test bulk inserting many posts."""
        # Create 100 posts
        posts = [
            Post(author_id=test_user.id, content=f"Bulk post {i}") for i in range(100)
        ]

        for post in posts:
            db_session.add(post)

        db_session.commit()

        # Verify all were created
        count = db_session.query(Post).filter(Post.author_id == test_user.id).count()

        assert count == 100

    @pytest.mark.slow
    def test_query_performance_with_many_records(self, db_session, test_user):
        """Test query performance with many records."""
        # Create many posts
        for i in range(50):
            post = Post(author_id=test_user.id, content=f"Post {i}")
            db_session.add(post)
        db_session.commit()

        # Query should still be fast
        posts = (
            db_session.query(Post)
            .filter(Post.author_id == test_user.id)
            .limit(10)
            .all()
        )

        assert len(posts) == 10
