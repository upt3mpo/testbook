from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr


# Auth schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class RegisterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    access_token: str
    token_type: str
    email: EmailStr
    username: str
    display_name: str


class TokenData(BaseModel):
    email: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    display_name: str
    bio: Optional[str] = ""


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    display_name: Optional[str] = None
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    theme: Optional[str] = None
    text_density: Optional[str] = None


class UserListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    display_name: str
    bio: str
    profile_picture: str
    is_following: bool = False
    is_blocked: bool = False


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    username: str
    display_name: str
    bio: str
    profile_picture: str
    theme: str
    text_density: str
    created_at: datetime
    followers_count: int = 0
    following_count: int = 0
    is_following: bool = False
    is_blocked: bool = False


class UserProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    display_name: str
    bio: str
    profile_picture: str
    created_at: datetime
    followers_count: int = 0
    following_count: int = 0
    posts_count: int = 0
    is_following: bool = False
    is_blocked: bool = False


# Post schemas
class PostCreate(BaseModel):
    content: str
    image_url: Optional[str] = None
    video_url: Optional[str] = None


class RepostCreate(BaseModel):
    original_post_id: int
    content: Optional[str] = ""


class CommentCreate(BaseModel):
    content: str


class ReactionCreate(BaseModel):
    reaction_type: str  # like, love, haha, wow, sad, angry


class ReactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    reaction_type: str
    user_id: int
    username: str
    display_name: str
    created_at: datetime


class CommentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    content: str
    author_id: int
    author_username: str
    author_display_name: str
    author_profile_picture: str
    created_at: datetime


class PostResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    content: str
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    is_repost: bool = False
    original_post_id: Optional[int] = None
    original_post: Optional["PostResponse"] = None
    author_id: int
    author_username: str
    author_display_name: str
    author_profile_picture: str
    created_at: datetime
    comments_count: int = 0
    reactions_count: int = 0
    reposts_count: int = 0
    user_reaction: Optional[str] = None
    has_reposted: bool = False


class PostDetailResponse(PostResponse):
    model_config = ConfigDict(from_attributes=True)

    comments: List[CommentResponse] = []
    reactions: List[ReactionResponse] = []


# Feed schemas
class FeedResponse(BaseModel):
    posts: List[PostResponse]
    total: int


# Dev schemas
class DevUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    username: str
    display_name: str
    password: str  # Plain text for testing purposes only
