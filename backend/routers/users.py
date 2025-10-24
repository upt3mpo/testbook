import uuid
from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

import models
import schemas
from auth import get_current_user
from database import get_db

router = APIRouter()

# Directory for uploaded profile pictures
UPLOAD_DIR = Path(__file__).parent.parent / "static" / "uploads" / "avatars"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.get("/{username}/followers", response_model=List[schemas.UserListItem])
def get_followers(
    username: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Get list of users who follow this user"""
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    followers = []
    for follower in user.followers:
        followers.append(
            schemas.UserListItem(
                id=follower.id,
                username=follower.username,
                display_name=follower.display_name,
                bio=follower.bio,
                profile_picture=follower.profile_picture,
                is_following=follower in current_user.following,
                is_blocked=follower in current_user.blocking
                or current_user in follower.blocking,
            )
        )

    return followers


@router.get("/{username}/following", response_model=List[schemas.UserListItem])
def get_following(
    username: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Get list of users this user is following"""
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    following = []
    for followed_user in user.following:
        following.append(
            schemas.UserListItem(
                id=followed_user.id,
                username=followed_user.username,
                display_name=followed_user.display_name,
                bio=followed_user.bio,
                profile_picture=followed_user.profile_picture,
                is_following=followed_user in current_user.following,
                is_blocked=followed_user in current_user.blocking
                or current_user in followed_user.blocking,
            )
        )

    return following


@router.get("/{username}", response_model=schemas.UserProfileResponse)
def get_user_profile(
    username: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Get user profile by username"""
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if blocked
    is_blocked = user in current_user.blocking or current_user in user.blocking

    followers_count = len(user.followers)
    following_count = len(user.following)
    posts_count = db.query(models.Post).filter(models.Post.author_id == user.id).count()
    is_following = user in current_user.following

    return schemas.UserProfileResponse(
        id=user.id,
        username=user.username,
        display_name=user.display_name,
        bio=user.bio,
        profile_picture=user.profile_picture,
        created_at=user.created_at,
        followers_count=followers_count,
        following_count=following_count,
        posts_count=posts_count,
        is_following=is_following,
        is_blocked=is_blocked,
    )


@router.post("/me/upload-avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Upload a profile picture"""
    # Validate file type
    allowed_extensions = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
    file_ext = Path(file.filename).suffix.lower()

    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}",
        )

    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = UPLOAD_DIR / unique_filename

    # Save file
    try:
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")

    # Update user's profile picture
    old_picture = current_user.profile_picture
    current_user.profile_picture = f"/static/uploads/avatars/{unique_filename}"
    db.commit()

    # Delete old uploaded avatar if it exists (but not default avatars)
    if old_picture and old_picture.startswith("/static/uploads/avatars/"):
        old_path = (
            Path(__file__).parent.parent
            / "static"
            / "uploads"
            / "avatars"
            / Path(old_picture).name
        )
        if old_path.exists():
            old_path.unlink()

    return {"url": current_user.profile_picture, "filename": file.filename}


@router.put("/me", response_model=schemas.UserResponse)
def update_current_user(
    user_update: schemas.UserUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update current user's profile"""
    if user_update.display_name is not None:
        current_user.display_name = user_update.display_name
    if user_update.bio is not None:
        current_user.bio = user_update.bio
    if user_update.profile_picture is not None:
        # If clearing profile picture, set to default
        if user_update.profile_picture == "":
            current_user.profile_picture = "/static/images/default-avatar.jpg"
        else:
            current_user.profile_picture = user_update.profile_picture
    if user_update.theme is not None:
        current_user.theme = user_update.theme
    if user_update.text_density is not None:
        current_user.text_density = user_update.text_density

    db.commit()
    db.refresh(current_user)

    return schemas.UserResponse(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        display_name=current_user.display_name,
        bio=current_user.bio,
        profile_picture=current_user.profile_picture,
        theme=current_user.theme,
        text_density=current_user.text_density,
        created_at=current_user.created_at,
        followers_count=len(current_user.followers),
        following_count=len(current_user.following),
        is_following=False,
        is_blocked=False,
    )


@router.delete("/me")
def delete_current_user(
    current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Delete current user's account"""
    db.delete(current_user)
    db.commit()
    return {"message": "Account deleted successfully"}


@router.post("/{username}/follow")
def follow_user(
    username: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Follow a user"""
    user_to_follow = (
        db.query(models.User).filter(models.User.username == username).first()
    )
    if not user_to_follow:
        raise HTTPException(status_code=404, detail="User not found")

    if user_to_follow.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")

    if user_to_follow in current_user.following:
        raise HTTPException(status_code=400, detail="Already following this user")

    current_user.following.append(user_to_follow)
    db.commit()

    return {"message": f"Now following {username}"}


@router.delete("/{username}/follow")
def unfollow_user(
    username: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Unfollow a user"""
    user_to_unfollow = (
        db.query(models.User).filter(models.User.username == username).first()
    )
    if not user_to_unfollow:
        raise HTTPException(status_code=404, detail="User not found")

    if user_to_unfollow not in current_user.following:
        raise HTTPException(status_code=400, detail="Not following this user")

    current_user.following.remove(user_to_unfollow)
    db.commit()

    return {"message": f"Unfollowed {username}"}


@router.post("/{username}/block")
def block_user(
    username: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Block a user"""
    user_to_block = (
        db.query(models.User).filter(models.User.username == username).first()
    )
    if not user_to_block:
        raise HTTPException(status_code=404, detail="User not found")

    if user_to_block.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot block yourself")

    if user_to_block in current_user.blocking:
        raise HTTPException(status_code=400, detail="Already blocking this user")

    # Unfollow if following
    if user_to_block in current_user.following:
        current_user.following.remove(user_to_block)
    if current_user in user_to_block.following:
        user_to_block.following.remove(current_user)

    current_user.blocking.append(user_to_block)
    db.commit()

    return {"message": f"Blocked {username}"}


@router.delete("/{username}/block")
def unblock_user(
    username: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Unblock a user"""
    user_to_unblock = (
        db.query(models.User).filter(models.User.username == username).first()
    )
    if not user_to_unblock:
        raise HTTPException(status_code=404, detail="User not found")

    if user_to_unblock not in current_user.blocking:
        raise HTTPException(status_code=400, detail="Not blocking this user")

    current_user.blocking.remove(user_to_unblock)
    db.commit()

    return {"message": f"Unblocked {username}"}


@router.get("/{username}/posts", response_model=List[schemas.PostResponse])
def get_user_posts(
    username: str,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Get posts by a specific user"""
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if blocked
    if user in current_user.blocking or current_user in user.blocking:
        return []

    posts = (
        db.query(models.Post)
        .filter(models.Post.author_id == user.id)
        .order_by(models.Post.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    result = []
    for post in posts:
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
            original_post = schemas.PostResponse(
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
