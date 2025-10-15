import os

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
from database import engine, get_db
from seed import seed_database

router = APIRouter()


def require_test_mode():
    """Dependency to require test mode for dangerous operations"""
    # Check TESTING environment variable dynamically to support runtime changes
    testing = os.getenv("TESTING", "false").lower() == "true"
    if not testing:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Dev endpoints are only available in test mode. Set TESTING=true in environment.",
        )
    return True


@router.post("/reset")
def reset_database(db: Session = Depends(get_db), _: bool = Depends(require_test_mode)):
    """Reset database to initial state (drop all tables and recreate)

    ⚠️ REQUIRES TEST MODE: Set TESTING=true in environment to use this endpoint.
    This prevents accidental database deletion in non-test environments.
    """
    # Close all sessions
    db.close()

    # Drop all tables
    models.Base.metadata.drop_all(bind=engine)

    # Recreate all tables
    models.Base.metadata.create_all(bind=engine)

    # Reseed database
    seed_database()

    return {"message": "Database reset successfully"}


@router.post("/seed")
def reseed_database(_: bool = Depends(require_test_mode)):
    """Reseed database with fresh data (keeps existing data)

    ⚠️ REQUIRES TEST MODE: Set TESTING=true in environment to use this endpoint.
    """
    seed_database()
    return {"message": "Database seeded successfully"}


@router.get("/users")
def get_all_users_with_passwords(
    db: Session = Depends(get_db), _: bool = Depends(require_test_mode)
):
    """Get all users with their plain text passwords (for testing only)

    ⚠️ REQUIRES TEST MODE: Set TESTING=true in environment to use this endpoint.
    ⚠️ SECURITY WARNING: This endpoint exposes plaintext passwords and should ONLY
    be used in test environments for test data verification.
    """
    users = db.query(models.User).all()

    # Hardcoded passwords for seed users
    user_passwords = {
        "sarah.johnson@testbook.com": "Sarah2024!",
        "mike.chen@testbook.com": "MikeRocks88",
        "emma.davis@testbook.com": "EmmaLovesPhotos",
        "alex.rodriguez@testbook.com": "Alex1234",
        "lisa.williams@testbook.com": "LisaFitness2024",
        "james.taylor@testbook.com": "JamesT@ylor99",
        "olivia.brown@testbook.com": "OliviaBrown!23",
        "daniel.kim@testbook.com": "DannyK1m2024",
        "newuser@testbook.com": "NewUser123!",
    }

    result = []
    for user in users:
        password = user_passwords.get(user.email, "password123")
        result.append(
            {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "display_name": user.display_name,
                "password": password,
                "bio": user.bio,
                "profile_picture": user.profile_picture,
            }
        )

    return result


@router.post("/create-post")
def create_test_post(
    user_id: int,
    content: str,
    image_url: str = None,
    video_url: str = None,
    db: Session = Depends(get_db),
    _: bool = Depends(require_test_mode),
):
    """Quickly create a post for a specific user (for testing)

    ⚠️ REQUIRES TEST MODE: Set TESTING=true in environment to use this endpoint.
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return {"error": "User not found"}

    new_post = models.Post(
        author_id=user_id,
        content=content,
        image_url=image_url,
        video_url=video_url,
        is_repost=False,
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {
        "message": "Post created successfully",
        "post_id": new_post.id,
        "author": user.display_name,
    }
