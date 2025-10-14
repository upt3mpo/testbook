import uuid
from pathlib import Path

import models
import schemas
from auth import get_current_user
from database import get_db
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

router = APIRouter()

# Directory for uploaded files
UPLOAD_DIR = Path(__file__).parent.parent / "static" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_media(
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user),
):
    """Upload an image or video file"""
    # Validate file type
    allowed_extensions = {
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".webp",
        ".mp4",
        ".mov",
        ".avi",
    }
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

    # Return the URL
    file_url = f"/static/uploads/{unique_filename}"
    return {"url": file_url, "filename": file.filename}


@router.post("/", response_model=schemas.PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(
    post_data: schemas.PostCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new post"""
    new_post = models.Post(
        author_id=current_user.id,
        content=post_data.content,
        image_url=post_data.image_url,
        video_url=post_data.video_url,
        is_repost=False,
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return schemas.PostResponse(
        id=new_post.id,
        content=new_post.content,
        image_url=new_post.image_url,
        video_url=new_post.video_url,
        is_repost=False,
        original_post_id=None,
        original_post=None,
        author_id=current_user.id,
        author_username=current_user.username,
        author_display_name=current_user.display_name,
        author_profile_picture=current_user.profile_picture,
        created_at=new_post.created_at,
        comments_count=0,
        reactions_count=0,
        reposts_count=0,
        user_reaction=None,
        has_reposted=False,
    )


@router.put("/{post_id}", response_model=schemas.PostResponse)
def update_post(
    post_id: int,
    post_data: schemas.PostCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a post"""
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")

    # Update post content
    post.content = post_data.content
    if post_data.image_url is not None:
        post.image_url = post_data.image_url
    if post_data.video_url is not None:
        post.video_url = post_data.video_url

    db.commit()
    db.refresh(post)

    return _format_single_post(post, current_user, db)


@router.delete("/repost/{post_id}")
def delete_repost(
    post_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Remove a repost of a post"""
    # Find the user's repost of this post
    repost = (
        db.query(models.Post)
        .filter(
            models.Post.author_id == current_user.id,
            models.Post.original_post_id == post_id,
            models.Post.is_repost.is_(True),
        )
        .first()
    )

    if not repost:
        raise HTTPException(status_code=404, detail="Repost not found")

    db.delete(repost)
    db.commit()

    return {"message": "Repost removed successfully"}


@router.post("/repost", response_model=schemas.PostResponse)
def create_repost(
    repost_data: schemas.RepostCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a repost of an existing post"""
    original_post = (
        db.query(models.Post).filter(models.Post.id == repost_data.original_post_id).first()
    )
    if not original_post:
        raise HTTPException(status_code=404, detail="Original post not found")

    # Check if already reposted
    existing_repost = (
        db.query(models.Post)
        .filter(
            models.Post.author_id == current_user.id,
            models.Post.original_post_id == repost_data.original_post_id,
        )
        .first()
    )

    if existing_repost:
        raise HTTPException(status_code=400, detail="Already reposted this post")

    new_repost = models.Post(
        author_id=current_user.id,
        content=repost_data.content or "",
        is_repost=True,
        original_post_id=repost_data.original_post_id,
    )

    db.add(new_repost)
    db.commit()
    db.refresh(new_repost)

    # Prepare original post response
    original_post_response = schemas.PostResponse(
        id=original_post.id,
        content=original_post.content,
        image_url=original_post.image_url,
        video_url=original_post.video_url,
        is_repost=False,
        original_post_id=None,
        original_post=None,
        author_id=original_post.author_id,
        author_username=original_post.author.username,
        author_display_name=original_post.author.display_name,
        author_profile_picture=original_post.author.profile_picture,
        created_at=original_post.created_at,
        comments_count=len(original_post.comments),
        reactions_count=len(original_post.reactions),
        reposts_count=db.query(models.Post)
        .filter(models.Post.original_post_id == original_post.id)
        .count(),
        user_reaction=None,
        has_reposted=False,
    )

    return schemas.PostResponse(
        id=new_repost.id,
        content=new_repost.content,
        image_url=None,
        video_url=None,
        is_repost=True,
        original_post_id=repost_data.original_post_id,
        original_post=original_post_response,
        author_id=current_user.id,
        author_username=current_user.username,
        author_display_name=current_user.display_name,
        author_profile_picture=current_user.profile_picture,
        created_at=new_repost.created_at,
        comments_count=0,
        reactions_count=0,
        reposts_count=0,
        user_reaction=None,
        has_reposted=True,
    )


@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a post"""
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")

    db.delete(post)
    db.commit()

    return {"message": "Post deleted successfully"}


@router.get("/{post_id}", response_model=schemas.PostDetailResponse)
def get_post(
    post_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a single post with all details"""
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Check if blocked
    if post.author in current_user.blocking or current_user in post.author.blocking:
        raise HTTPException(status_code=403, detail="Cannot view this post")

    # Get user reaction
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

    # Prepare comments
    comments = []
    for comment in post.comments:
        comments.append(
            schemas.CommentResponse(
                id=comment.id,
                content=comment.content,
                author_id=comment.author_id,
                author_username=comment.author.username,
                author_display_name=comment.author.display_name,
                author_profile_picture=comment.author.profile_picture,
                created_at=comment.created_at,
            )
        )

    # Prepare reactions
    reactions = []
    for reaction in post.reactions:
        reactions.append(
            schemas.ReactionResponse(
                id=reaction.id,
                reaction_type=reaction.reaction_type,
                user_id=reaction.user_id,
                username=reaction.user.username,
                display_name=reaction.user.display_name,
                created_at=reaction.created_at,
            )
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

    return schemas.PostDetailResponse(
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
        comments_count=len(post.comments),
        reactions_count=len(post.reactions),
        reposts_count=db.query(models.Post).filter(models.Post.original_post_id == post.id).count(),
        user_reaction=user_reaction,
        has_reposted=has_reposted,
        comments=comments,
        reactions=reactions,
    )


@router.post(
    "/{post_id}/comments",
    response_model=schemas.CommentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_comment(
    post_id: int,
    comment_data: schemas.CommentCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Add a comment to a post"""
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    new_comment = models.Comment(
        post_id=post_id, author_id=current_user.id, content=comment_data.content
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return schemas.CommentResponse(
        id=new_comment.id,
        content=new_comment.content,
        author_id=current_user.id,
        author_username=current_user.username,
        author_display_name=current_user.display_name,
        author_profile_picture=current_user.profile_picture,
        created_at=new_comment.created_at,
    )


@router.post(
    "/{post_id}/reactions", response_model=schemas.PostResponse, status_code=status.HTTP_201_CREATED
)
def add_reaction(
    post_id: int,
    reaction_data: schemas.ReactionCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Add or update reaction to a post"""
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Check if user already reacted
    existing_reaction = (
        db.query(models.Reaction)
        .filter(
            models.Reaction.post_id == post_id,
            models.Reaction.user_id == current_user.id,
        )
        .first()
    )

    if existing_reaction:
        # Update existing reaction
        existing_reaction.reaction_type = reaction_data.reaction_type
        db.commit()
        db.refresh(existing_reaction)
    else:
        # Create new reaction
        new_reaction = models.Reaction(
            post_id=post_id,
            user_id=current_user.id,
            reaction_type=reaction_data.reaction_type,
        )
        db.add(new_reaction)
        db.commit()
        db.refresh(new_reaction)

    # Return full post with updated reaction state
    db.refresh(post)
    return _format_single_post(post, current_user, db)


@router.delete("/{post_id}/reactions", response_model=schemas.PostResponse)
def remove_reaction(
    post_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Remove reaction from a post"""
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    reaction = (
        db.query(models.Reaction)
        .filter(
            models.Reaction.post_id == post_id,
            models.Reaction.user_id == current_user.id,
        )
        .first()
    )

    if not reaction:
        raise HTTPException(status_code=404, detail="Reaction not found")

    db.delete(reaction)
    db.commit()

    # Return full post with updated reaction state
    db.refresh(post)
    return _format_single_post(post, current_user, db)


def _format_single_post(
    post: models.Post, current_user: models.User, db: Session
) -> schemas.PostResponse:
    """Helper function to format a single post for response"""
    # Get counts
    comments_count = len(post.comments)
    reactions_count = len(post.reactions)
    reposts_count = db.query(models.Post).filter(models.Post.original_post_id == post.id).count()

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

    return schemas.PostResponse(
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
