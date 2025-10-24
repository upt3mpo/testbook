from typing import List, Optional, Set

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import models
import schemas
from auth import get_current_user
from database import get_db

router = APIRouter()


@router.get("/all", response_model=List[schemas.PostResponse])
def get_all_feed(
    skip: int = 0,
    limit: int = 50,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all posts from all users (excluding blocked users)"""
    blocked_user_ids = _get_all_blocked_user_ids(current_user)

    # Get all posts excluding blocked users
    query = db.query(models.Post)
    if blocked_user_ids:
        query = query.filter(~models.Post.author_id.in_(blocked_user_ids))

    posts = (
        query.order_by(models.Post.created_at.desc()).offset(skip).limit(limit).all()
    )

    if blocked_user_ids:
        posts = [post for post in posts if post.author_id not in blocked_user_ids]

    return _format_posts(posts, current_user, db, blocked_user_ids)


@router.get("/following", response_model=List[schemas.PostResponse])
def get_following_feed(
    skip: int = 0,
    limit: int = 50,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get posts from users you follow"""
    # Get following user IDs
    following_ids = [user.id for user in current_user.following]
    blocked_user_ids = _get_all_blocked_user_ids(current_user)

    if not following_ids:
        return []

    # Get posts from following
    posts = (
        db.query(models.Post)
        .filter(models.Post.author_id.in_(following_ids))
        .order_by(models.Post.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    if blocked_user_ids:
        posts = [post for post in posts if post.author_id not in blocked_user_ids]

    return _format_posts(posts, current_user, db, blocked_user_ids)


def _format_posts(
    posts: List[models.Post],
    current_user: models.User,
    db: Session,
    blocked_user_ids: Optional[Set[int]] = None,
) -> List[schemas.PostResponse]:
    """Helper function to format posts for response"""
    result = []

    for post in posts:
        if blocked_user_ids and post.author_id in blocked_user_ids:
            continue

        # Get counts
        comments_count = len(post.comments)
        reactions_count = len(post.reactions)
        reposts_count = (
            db.query(models.Post)
            .filter(models.Post.original_post_id == post.id)
            .count()
        )

        # Check user reaction
        user_reaction = None
        for reaction in post.reactions:
            if reaction.user_id == current_user.id:
                user_reaction = reaction.reaction_type
                break

        # Check if user has reposted
        has_reposted = (
            db.query(models.Post)
            .filter(
                models.Post.author_id == current_user.id,
                models.Post.original_post_id == post.id,
            )
            .first()
            is not None
        )

        # Handle original post for reposts
        original_post = None
        if post.is_repost and post.original_post:
            orig = post.original_post
            if blocked_user_ids and orig.author_id in blocked_user_ids:
                orig = None

            original_post = (
                schemas.PostResponse(
                    id=orig.id,
                    content=orig.content,
                    image_url=orig.image_url,
                    video_url=orig.video_url,
                    is_repost=False,
                    original_post_id=None,
                    original_post=None,
                    author_id=orig.author_id,
                    author_username=orig.author.username,
                    author_display_name=orig.author.display_name,
                    author_profile_picture=orig.author.profile_picture,
                    created_at=orig.created_at,
                    comments_count=len(orig.comments),
                    reactions_count=len(orig.reactions),
                    reposts_count=db.query(models.Post)
                    .filter(models.Post.original_post_id == orig.id)
                    .count(),
                    user_reaction=None,
                    has_reposted=False,
                )
                if orig
                else None
            )

        result.append(
            schemas.PostResponse(
                id=post.id,
                content=post.content,
                image_url=post.image_url,
                video_url=post.video_url,
                is_repost=post.is_repost,
                original_post_id=post.original_post_id,
                original_post=original_post,
                author_id=post.author_id,
                author_username=post.author.username,
                author_display_name=post.author.display_name,
                author_profile_picture=post.author.profile_picture,
                created_at=post.created_at,
                comments_count=comments_count,
                reactions_count=reactions_count,
                reposts_count=reposts_count,
                user_reaction=user_reaction,
                has_reposted=has_reposted,
            )
        )

    return result


def _get_all_blocked_user_ids(user: models.User) -> Set[int]:
    blocked_ids = {blocked_user.id for blocked_user in user.blocking}
    blocked_by_ids = {blocking_user.id for blocking_user in user.blocked_by}
    return blocked_ids.union(blocked_by_ids)
