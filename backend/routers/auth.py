import os

from fastapi import APIRouter, Depends, HTTPException, Request, status
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session

import models
import schemas
from auth import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)
from database import get_db

router = APIRouter()

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Adjust rate limits based on environment
# Testing mode: Very permissive for load tests and CI
# Production: Conservative for security
TESTING_MODE = os.getenv("TESTING", "false").lower() == "true"
LOGIN_RATE = "1000/minute" if TESTING_MODE else "20/minute"
REGISTER_RATE = "500/minute" if TESTING_MODE else "15/minute"


@router.post(
    "/register",
    response_model=schemas.RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit(REGISTER_RATE)
def register(
    request: Request, user_data: schemas.UserCreate, db: Session = Depends(get_db)
):
    """Register a new user and return access token (rate limited: 15/min prod, 500/min test)"""
    # Check if email already exists
    if db.query(models.User).filter(models.User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # Check if username already exists
    if db.query(models.User).filter(models.User.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken"
        )

    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = models.User(
        email=user_data.email,
        username=user_data.username,
        display_name=user_data.display_name,
        hashed_password=hashed_password,
        bio=user_data.bio or "",
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create access token for immediate login
    access_token = create_access_token(data={"sub": new_user.email})
    return schemas.RegisterResponse(
        access_token=access_token,
        token_type="bearer",
        email=new_user.email,
        username=new_user.username,
        display_name=new_user.display_name,
    )


@router.post("/login", response_model=schemas.Token)
@limiter.limit(LOGIN_RATE)
def login(
    request: Request, login_data: schemas.LoginRequest, db: Session = Depends(get_db)
):
    """Login with email and password (rate limited: 20/min prod, 1000/min test)"""
    user = db.query(models.User).filter(models.User.email == login_data.email).first()

    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})
    return schemas.Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=schemas.UserResponse)
def get_current_user_info(
    current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Get current authenticated user info"""
    followers_count = len(current_user.followers)
    following_count = len(current_user.following)

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
        followers_count=followers_count,
        following_count=following_count,
        is_following=False,
        is_blocked=False,
    )
