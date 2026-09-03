from datetime import UTC, datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

# Association tables for many-to-many relationships
followers = Table(
    "followers",
    Base.metadata,
    Column("follower_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("followed_id", Integer, ForeignKey("users.id"), primary_key=True),
)

blocks = Table(
    "blocks",
    Base.metadata,
    Column("blocker_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("blocked_id", Integer, ForeignKey("users.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=False
    )
    display_name: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    # bio/profile_picture/theme/text_density/created_at are nullable=False
    # (tightened from the original schema's implicit nullable=True) because
    # every insert path in this app goes through these Python-side
    # defaults and none ever sets them to None - see the type-hints pass
    # that added this (Item 8 of the follow-up audit) for the grep that
    # confirmed it. That keeps their type honest as non-Optional, matching
    # what schemas.UserResponse already expected.
    bio: Mapped[str] = mapped_column(Text, nullable=False, default="")
    profile_picture: Mapped[str] = mapped_column(
        String, nullable=False, default="/static/images/default-avatar.jpg"
    )
    theme: Mapped[str] = mapped_column(String, nullable=False, default="light")
    text_density: Mapped[str] = mapped_column(String, nullable=False, default="normal")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(UTC)
    )

    # Relationships
    posts: Mapped[list["Post"]] = relationship(
        "Post", back_populates="author", cascade="all, delete-orphan"
    )
    comments: Mapped[list["Comment"]] = relationship(
        "Comment", back_populates="author", cascade="all, delete-orphan"
    )
    reactions: Mapped[list["Reaction"]] = relationship(
        "Reaction", back_populates="user", cascade="all, delete-orphan"
    )

    # Following relationships. back_populates (rather than backref) on
    # both sides so the reverse attributes (followers/blocked_by) are
    # visible to mypy instead of only existing at runtime.
    following: Mapped[list["User"]] = relationship(
        "User",
        secondary=followers,
        primaryjoin=id == followers.c.follower_id,
        secondaryjoin=id == followers.c.followed_id,
        back_populates="followers",
    )
    followers: Mapped[list["User"]] = relationship(
        "User",
        secondary=followers,
        primaryjoin=id == followers.c.followed_id,
        secondaryjoin=id == followers.c.follower_id,
        back_populates="following",
    )

    # Blocking relationships
    blocking: Mapped[list["User"]] = relationship(
        "User",
        secondary=blocks,
        primaryjoin=id == blocks.c.blocker_id,
        secondaryjoin=id == blocks.c.blocked_id,
        back_populates="blocked_by",
    )
    blocked_by: Mapped[list["User"]] = relationship(
        "User",
        secondary=blocks,
        primaryjoin=id == blocks.c.blocked_id,
        secondaryjoin=id == blocks.c.blocker_id,
        back_populates="blocking",
    )


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    author_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    image_url: Mapped[str | None] = mapped_column(String, nullable=True)
    video_url: Mapped[str | None] = mapped_column(String, nullable=True)
    # is_repost is nullable=False (tightened, see the User fields above for
    # why) - every post goes through this default, repost or not.
    is_repost: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    original_post_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("posts.id"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(UTC)
    )

    # Relationships
    author: Mapped["User"] = relationship("User", back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship(
        "Comment", back_populates="post", cascade="all, delete-orphan"
    )
    reactions: Mapped[list["Reaction"]] = relationship(
        "Reaction", back_populates="post", cascade="all, delete-orphan"
    )
    original_post: Mapped[Optional["Post"]] = relationship(
        "Post", remote_side=[id], backref="reposts"
    )


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    post_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("posts.id"), nullable=False
    )
    author_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(UTC)
    )

    # Relationships
    post: Mapped["Post"] = relationship("Post", back_populates="comments")
    author: Mapped["User"] = relationship("User", back_populates="comments")


class Reaction(Base):
    __tablename__ = "reactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    post_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("posts.id"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    reaction_type: Mapped[str] = mapped_column(
        String, nullable=False
    )  # like, love, haha, wow, sad, angry
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(UTC)
    )

    # Relationships
    post: Mapped["Post"] = relationship("Post", back_populates="reactions")
    user: Mapped["User"] = relationship("User", back_populates="reactions")
