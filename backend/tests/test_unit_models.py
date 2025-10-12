"""
Unit tests for database models.

These tests verify that database models work correctly,
including relationships, cascades, and constraints.
"""

from datetime import datetime

import pytest
from auth import get_password_hash
from models import Comment, Post, Reaction, User
from sqlalchemy.exc import IntegrityError


@pytest.mark.unit
@pytest.mark.database
class TestUserModel:
    """Test User model functionality."""

    def test_create_user(self, db_session):
        """Test creating a user with all required fields."""
        user = User(
            email="newuser@example.com",
            username="newuser",
            display_name="New User",
            hashed_password=get_password_hash("password123"),
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        assert user.id is not None
        assert user.email == "newuser@example.com"
        assert user.username == "newuser"
        assert user.display_name == "New User"
        assert user.created_at is not None
        assert user.theme == "light"  # Default value
        assert user.text_density == "normal"  # Default value

    def test_user_email_must_be_unique(self, db_session):
        """Test that duplicate email raises error."""
        user1 = User(
            email="duplicate@example.com",
            username="user1",
            display_name="User 1",
            hashed_password=get_password_hash("password123"),
        )
        db_session.add(user1)
        db_session.commit()

        user2 = User(
            email="duplicate@example.com",  # Duplicate email
            username="user2",
            display_name="User 2",
            hashed_password=get_password_hash("password123"),
        )
        db_session.add(user2)

        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_user_username_must_be_unique(self, db_session):
        """Test that duplicate username raises error."""
        user1 = User(
            email="user1@example.com",
            username="duplicateuser",
            display_name="User 1",
            hashed_password=get_password_hash("password123"),
        )
        db_session.add(user1)
        db_session.commit()

        user2 = User(
            email="user2@example.com",
            username="duplicateuser",  # Duplicate username
            display_name="User 2",
            hashed_password=get_password_hash("password123"),
        )
        db_session.add(user2)

        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_user_has_default_profile_picture(self, db_session):
        """Test that user gets default profile picture."""
        user = User(
            email="test@example.com",
            username="testuser",
            display_name="Test User",
            hashed_password=get_password_hash("password123"),
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        assert user.profile_picture == "/static/images/default-avatar.jpg"

    def test_user_created_at_is_set(self, db_session):
        """Test that created_at timestamp is automatically set."""
        user = User(
            email="test@example.com",
            username="testuser",
            display_name="Test User",
            hashed_password=get_password_hash("password123"),
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        # Just verify created_at is set and is a datetime
        assert user.created_at is not None
        assert isinstance(user.created_at, datetime)


@pytest.mark.unit
@pytest.mark.database
class TestPostModel:
    """Test Post model functionality."""

    def test_create_post(self, db_session, test_user):
        """Test creating a post."""
        post = Post(
            author_id=test_user.id,
            content="This is a test post",
        )
        db_session.add(post)
        db_session.commit()
        db_session.refresh(post)

        assert post.id is not None
        assert post.author_id == test_user.id
        assert post.content == "This is a test post"
        assert post.is_repost is False
        assert post.created_at is not None

    def test_post_author_relationship(self, db_session, test_user):
        """Test that post.author relationship works."""
        post = Post(
            author_id=test_user.id,
            content="Test post",
        )
        db_session.add(post)
        db_session.commit()
        db_session.refresh(post)

        assert post.author.id == test_user.id
        assert post.author.username == test_user.username

    def test_user_posts_relationship(self, db_session, test_user):
        """Test that user.posts relationship works."""
        post1 = Post(author_id=test_user.id, content="Post 1")
        post2 = Post(author_id=test_user.id, content="Post 2")

        db_session.add_all([post1, post2])
        db_session.commit()
        db_session.refresh(test_user)

        assert len(test_user.posts) == 2
        assert post1 in test_user.posts
        assert post2 in test_user.posts

    def test_post_with_image_url(self, db_session, test_user):
        """Test creating a post with an image."""
        post = Post(
            author_id=test_user.id,
            content="Post with image",
            image_url="/static/images/test.jpg",
        )
        db_session.add(post)
        db_session.commit()
        db_session.refresh(post)

        assert post.image_url == "/static/images/test.jpg"
        assert post.video_url is None

    def test_post_with_video_url(self, db_session, test_user):
        """Test creating a post with a video."""
        post = Post(
            author_id=test_user.id,
            content="Post with video",
            video_url="/static/videos/test.mp4",
        )
        db_session.add(post)
        db_session.commit()
        db_session.refresh(post)

        assert post.video_url == "/static/videos/test.mp4"
        assert post.image_url is None

    def test_repost_creation(self, db_session, test_user, test_user_2):
        """Test creating a repost."""
        original_post = Post(
            author_id=test_user.id,
            content="Original post",
        )
        db_session.add(original_post)
        db_session.commit()
        db_session.refresh(original_post)

        repost = Post(
            author_id=test_user_2.id,
            content="",
            is_repost=True,
            original_post_id=original_post.id,
        )
        db_session.add(repost)
        db_session.commit()
        db_session.refresh(repost)

        assert repost.is_repost is True
        assert repost.original_post_id == original_post.id
        assert repost.original_post.content == "Original post"


@pytest.mark.unit
@pytest.mark.database
class TestCommentModel:
    """Test Comment model functionality."""

    def test_create_comment(self, db_session, test_post, test_user_2):
        """Test creating a comment."""
        comment = Comment(
            post_id=test_post.id,
            author_id=test_user_2.id,
            content="Great post!",
        )
        db_session.add(comment)
        db_session.commit()
        db_session.refresh(comment)

        assert comment.id is not None
        assert comment.post_id == test_post.id
        assert comment.author_id == test_user_2.id
        assert comment.content == "Great post!"
        assert comment.created_at is not None

    def test_comment_post_relationship(self, db_session, test_post, test_user_2):
        """Test that comment.post relationship works."""
        comment = Comment(
            post_id=test_post.id,
            author_id=test_user_2.id,
            content="Test comment",
        )
        db_session.add(comment)
        db_session.commit()
        db_session.refresh(comment)

        assert comment.post.id == test_post.id
        assert comment.post.content == test_post.content

    def test_comment_author_relationship(self, db_session, test_post, test_user_2):
        """Test that comment.author relationship works."""
        comment = Comment(
            post_id=test_post.id,
            author_id=test_user_2.id,
            content="Test comment",
        )
        db_session.add(comment)
        db_session.commit()
        db_session.refresh(comment)

        assert comment.author.id == test_user_2.id
        assert comment.author.username == test_user_2.username

    def test_post_comments_relationship(
        self, db_session, test_post, test_user_2, test_user_3
    ):
        """Test that post.comments relationship works."""
        comment1 = Comment(
            post_id=test_post.id,
            author_id=test_user_2.id,
            content="First comment",
        )
        comment2 = Comment(
            post_id=test_post.id,
            author_id=test_user_3.id,
            content="Second comment",
        )

        db_session.add_all([comment1, comment2])
        db_session.commit()
        db_session.refresh(test_post)

        assert len(test_post.comments) == 2


@pytest.mark.unit
@pytest.mark.database
class TestReactionModel:
    """Test Reaction model functionality."""

    @pytest.mark.parametrize(
        "reaction_type", ["like", "love", "haha", "wow", "sad", "angry"]
    )
    def test_create_reaction(self, db_session, test_post, test_user_2, reaction_type):
        """Test creating different types of reactions."""
        reaction = Reaction(
            post_id=test_post.id,
            user_id=test_user_2.id,
            reaction_type=reaction_type,
        )
        db_session.add(reaction)
        db_session.commit()
        db_session.refresh(reaction)

        assert reaction.id is not None
        assert reaction.reaction_type == reaction_type

    def test_reaction_post_relationship(self, db_session, test_post, test_user_2):
        """Test that reaction.post relationship works."""
        reaction = Reaction(
            post_id=test_post.id,
            user_id=test_user_2.id,
            reaction_type="like",
        )
        db_session.add(reaction)
        db_session.commit()
        db_session.refresh(reaction)

        assert reaction.post.id == test_post.id

    def test_reaction_user_relationship(self, db_session, test_post, test_user_2):
        """Test that reaction.user relationship works."""
        reaction = Reaction(
            post_id=test_post.id,
            user_id=test_user_2.id,
            reaction_type="love",
        )
        db_session.add(reaction)
        db_session.commit()
        db_session.refresh(reaction)

        assert reaction.user.id == test_user_2.id

    def test_post_reactions_relationship(
        self, db_session, test_post, test_user_2, test_user_3
    ):
        """Test that post.reactions relationship works."""
        reaction1 = Reaction(
            post_id=test_post.id,
            user_id=test_user_2.id,
            reaction_type="like",
        )
        reaction2 = Reaction(
            post_id=test_post.id,
            user_id=test_user_3.id,
            reaction_type="love",
        )

        db_session.add_all([reaction1, reaction2])
        db_session.commit()
        db_session.refresh(test_post)

        assert len(test_post.reactions) == 2


@pytest.mark.unit
@pytest.mark.database
class TestRelationships:
    """Test user relationship functionality (follow/block)."""

    def test_user_follow_relationship(self, db_session, test_user, test_user_2):
        """Test following another user."""
        test_user.following.append(test_user_2)
        db_session.commit()
        db_session.refresh(test_user)
        db_session.refresh(test_user_2)

        assert test_user_2 in test_user.following
        assert test_user in test_user_2.followers

    def test_user_block_relationship(self, db_session, test_user, test_user_2):
        """Test blocking another user."""
        test_user.blocking.append(test_user_2)
        db_session.commit()
        db_session.refresh(test_user)
        db_session.refresh(test_user_2)

        assert test_user_2 in test_user.blocking
        assert test_user in test_user_2.blocked_by

    def test_multiple_followers(self, db_session, test_user, test_user_2, test_user_3):
        """Test user with multiple followers."""
        test_user_2.following.append(test_user)
        test_user_3.following.append(test_user)
        db_session.commit()
        db_session.refresh(test_user)

        assert len(test_user.followers) == 2
        assert test_user_2 in test_user.followers
        assert test_user_3 in test_user.followers


@pytest.mark.unit
@pytest.mark.database
class TestCascadeDeletes:
    """Test cascade delete behavior."""

    def test_delete_user_deletes_posts(self, db_session, test_user):
        """Test that deleting a user deletes their posts."""
        post = Post(author_id=test_user.id, content="Test post")
        db_session.add(post)
        db_session.commit()
        post_id = post.id

        db_session.delete(test_user)
        db_session.commit()

        assert db_session.query(Post).filter(Post.id == post_id).first() is None

    def test_delete_post_deletes_comments(self, db_session, test_post, test_user_2):
        """Test that deleting a post deletes its comments."""
        comment = Comment(
            post_id=test_post.id,
            author_id=test_user_2.id,
            content="Test comment",
        )
        db_session.add(comment)
        db_session.commit()
        comment_id = comment.id

        db_session.delete(test_post)
        db_session.commit()

        assert (
            db_session.query(Comment).filter(Comment.id == comment_id).first() is None
        )

    def test_delete_post_deletes_reactions(self, db_session, test_post, test_user_2):
        """Test that deleting a post deletes its reactions."""
        reaction = Reaction(
            post_id=test_post.id,
            user_id=test_user_2.id,
            reaction_type="like",
        )
        db_session.add(reaction)
        db_session.commit()
        reaction_id = reaction.id

        db_session.delete(test_post)
        db_session.commit()

        assert (
            db_session.query(Reaction).filter(Reaction.id == reaction_id).first()
            is None
        )
