"""
Test data factories using the Factory pattern.

These factories make it easy to create test data with sensible defaults
while allowing customization when needed.
"""

from typing import Optional

from auth import get_password_hash
from models import Comment, Post, Reaction, User


class UserFactory:
    """
    Factory for creating User instances with sensible defaults.

    This factory follows the Factory Pattern to create test users easily.
    It provides sensible defaults while allowing customization when needed.

    Key Features:
    - Auto-generates unique emails and usernames
    - Handles password hashing automatically
    - Saves to database and returns committed instance
    - Supports batch creation for multiple users

    Usage Examples:
        # Simple user creation
        user = UserFactory.create(db_session)

        # Custom user with specific data
        user = UserFactory.create(
            db_session,
            email="custom@test.com",
            username="customuser",
            display_name="Custom User"
        )

        # Batch creation for multiple users
        users = UserFactory.create_batch(db_session, 5)
    """

    _counter = 0

    @classmethod
    def create(
        cls,
        db_session,
        email: Optional[str] = None,
        username: Optional[str] = None,
        display_name: Optional[str] = None,
        password: str = "TestPassword123!",
        bio: Optional[str] = None,
        **kwargs,
    ) -> User:
        """
        Create a user with sensible defaults.

        This method creates a User instance with auto-generated values for
        required fields, handles password hashing, and saves to the database.
        Each call generates unique values to avoid conflicts.

        Args:
            db_session: Database session for saving the user
            email: User email (auto-generated as "user{N}@test.com" if not provided)
            username: Username (auto-generated as "user{N}" if not provided)
            display_name: Display name (auto-generated as "Test User {N}" if not provided)
            password: Plain password (will be hashed using bcrypt)
            bio: User bio (auto-generated if not provided)
            **kwargs: Additional User model fields

        Returns:
            User: Created and committed user instance ready for testing
        """
        cls._counter += 1

        if email is None:
            email = f"user{cls._counter}@test.com"

        if username is None:
            username = f"user{cls._counter}"

        if display_name is None:
            display_name = f"Test User {cls._counter}"

        user = User(
            email=email,
            username=username,
            display_name=display_name,
            hashed_password=get_password_hash(password),
            bio=bio or f"Bio for {username}",
            **kwargs,
        )

        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        return user

    @classmethod
    def create_batch(cls, db_session, count: int, **kwargs) -> list[User]:
        """Create multiple users at once.

        Args:
            db_session: Database session
            count: Number of users to create
            **kwargs: Common attributes for all users

        Returns:
            list[User]: List of created users
        """
        return [cls.create(db_session, **kwargs) for _ in range(count)]


class PostFactory:
    """Factory for creating Post instances."""

    @classmethod
    def create(
        cls,
        db_session,
        author: User,
        content: Optional[str] = None,
        image_url: Optional[str] = None,
        video_url: Optional[str] = None,
        **kwargs,
    ) -> Post:
        """Create a post with defaults.

        Args:
            db_session: Database session
            author: User who creates the post
            content: Post content (auto-generated if not provided)
            image_url: Optional image URL
            video_url: Optional video URL
            **kwargs: Additional Post model fields

        Returns:
            Post: Created and committed post instance
        """
        if content is None:
            content = f"Test post from {author.username}"

        post = Post(
            author_id=author.id,
            content=content,
            image_url=image_url,
            video_url=video_url,
            **kwargs,
        )

        db_session.add(post)
        db_session.commit()
        db_session.refresh(post)

        return post

    @classmethod
    def create_batch(cls, db_session, author: User, count: int, **kwargs) -> list[Post]:
        """Create multiple posts for an author.

        Args:
            db_session: Database session
            author: User who creates posts
            count: Number of posts to create
            **kwargs: Common attributes for all posts

        Returns:
            list[Post]: List of created posts
        """
        return [cls.create(db_session, author, **kwargs) for _ in range(count)]


class CommentFactory:
    """Factory for creating Comment instances."""

    @classmethod
    def create(
        cls,
        db_session,
        post: Post,
        author: User,
        content: Optional[str] = None,
        **kwargs,
    ) -> Comment:
        """Create a comment with defaults.

        Args:
            db_session: Database session
            post: Post to comment on
            author: User who creates comment
            content: Comment content (auto-generated if not provided)
            **kwargs: Additional Comment model fields

        Returns:
            Comment: Created and committed comment instance
        """
        if content is None:
            content = f"Comment from {author.username}"

        comment = Comment(post_id=post.id, author_id=author.id, content=content, **kwargs)

        db_session.add(comment)
        db_session.commit()
        db_session.refresh(comment)

        return comment

    @classmethod
    def create_batch(
        cls, db_session, post: Post, author: User, count: int, **kwargs
    ) -> list[Comment]:
        """Create multiple comments on a post.

        Args:
            db_session: Database session
            post: Post to comment on
            author: User who creates comments
            count: Number of comments to create
            **kwargs: Common attributes for all comments

        Returns:
            list[Comment]: List of created comments
        """
        return [cls.create(db_session, post, author, **kwargs) for _ in range(count)]


class ReactionFactory:
    """Factory for creating Reaction instances."""

    @classmethod
    def create(
        cls, db_session, post: Post, user: User, reaction_type: str = "like", **kwargs
    ) -> Reaction:
        """Create a reaction with defaults.

        Args:
            db_session: Database session
            post: Post to react to
            user: User who creates reaction
            reaction_type: Type of reaction (like, love, haha, wow, sad, angry)
            **kwargs: Additional Reaction model fields

        Returns:
            Reaction: Created and committed reaction instance
        """
        reaction = Reaction(post_id=post.id, user_id=user.id, reaction_type=reaction_type, **kwargs)

        db_session.add(reaction)
        db_session.commit()
        db_session.refresh(reaction)

        return reaction


# Convenience functions for common scenarios


def create_user_with_posts(
    db_session, num_posts: int = 3, username: Optional[str] = None, **user_kwargs
) -> tuple[User, list[Post]]:
    """Create a user with multiple posts.

    Args:
        db_session: Database session
        num_posts: Number of posts to create
        username: Optional username
        **user_kwargs: Additional user attributes

    Returns:
        tuple: (user, list of posts)
    """
    user = UserFactory.create(db_session, username=username, **user_kwargs)
    posts = PostFactory.create_batch(db_session, user, num_posts)
    return user, posts


def create_post_with_comments(
    db_session, author: Optional[User] = None, num_comments: int = 3, **post_kwargs
) -> tuple[Post, list[Comment]]:
    """Create a post with multiple comments.

    Args:
        db_session: Database session
        author: Post author (created if not provided)
        num_comments: Number of comments to create
        **post_kwargs: Additional post attributes

    Returns:
        tuple: (post, list of comments)
    """
    if author is None:
        author = UserFactory.create(db_session)

    post = PostFactory.create(db_session, author, **post_kwargs)

    # Create comments from different users
    commenters = UserFactory.create_batch(db_session, num_comments)
    comments = [CommentFactory.create(db_session, post, commenter) for commenter in commenters]

    return post, comments


def create_social_network(db_session, num_users: int = 5, posts_per_user: int = 2) -> dict:
    """Create a small social network for testing.

    Args:
        db_session: Database session
        num_users: Number of users to create
        posts_per_user: Number of posts each user creates

    Returns:
        dict: {
            'users': list of users,
            'posts': list of all posts,
            'relationships': dict of user relationships
        }
    """
    # Create users
    users = UserFactory.create_batch(db_session, num_users)

    # Create posts for each user
    all_posts = []
    for user in users:
        posts = PostFactory.create_batch(db_session, user, posts_per_user)
        all_posts.extend(posts)

    # Create some follow relationships
    # User 0 follows everyone
    for user in users[1:]:
        users[0].following.append(user)

    # Users follow each other in pairs
    for i in range(1, len(users), 2):
        if i + 1 < len(users):
            users[i].following.append(users[i + 1])
            users[i + 1].following.append(users[i])

    db_session.commit()

    return {
        "users": users,
        "posts": all_posts,
        "relationships": {
            "following": {user.username: [u.username for u in user.following] for user in users}
        },
    }


# Usage examples:
"""
# Simple user creation
user = UserFactory.create(db_session)

# Custom user
user = UserFactory.create(
    db_session,
    email="custom@test.com",
    username="customuser",
    display_name="Custom User"
)

# Batch creation
users = UserFactory.create_batch(db_session, 10)

# User with posts
user, posts = create_user_with_posts(db_session, num_posts=5)

# Post with comments
post, comments = create_post_with_comments(db_session, num_comments=10)

# Complete social network
network = create_social_network(db_session, num_users=10, posts_per_user=3)
"""
