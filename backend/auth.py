import os
from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

import models
from database import get_db

# Security Configuration
# Load from environment with secure defaults
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    # This fallback exists so the app runs out of the box for local
    # dev/testing without an .env file. It is not a real secret - it's
    # committed in this repo, so anyone who has ever cloned it can forge a
    # valid token for any user against a deployment that still uses this
    # default. Any real deployment must set SECRET_KEY to a random value
    # (e.g. `openssl rand -hex 32`) that is never committed.
    import sys

    SECRET_KEY = "testbook-secret-key-for-testing-only-do-not-use-in-production"  # pragma: allowlist secret
    if "pytest" not in sys.modules:  # Don't warn during tests
        print(
            "WARNING: Using default SECRET_KEY. Set SECRET_KEY environment variable in production!"
        )

# HS256 (symmetric) is fine here because this app both signs and verifies
# its own tokens with the same process/key - there's no third party that
# needs to verify a token without being able to also forge one. RS256
# (asymmetric) is the better choice once a separate service needs to verify
# tokens without holding the signing key itself (e.g. a gateway or another
# microservice that only checks tokens, never issues them) - that's the
# real reason RS256 shows up in production auth systems, not because HS256
# is inherently weaker for a single-service setup like this one.
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# 24 hours (1440 minutes) by default. That's long for a real production
# system - a stolen token stays valid for a full day with nothing else to
# stop it - but it's a reasonable default for a learning app where the
# alternative (a short-lived access token plus a refresh-token flow) would
# add real complexity to every lab in this curriculum without teaching a
# testing concept. A production deployment would use a much shorter access
# token (minutes, not hours) paired with a refresh token that can actually
# be revoked - see the revocation note on get_current_user below.
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", str(60 * 24))
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()
optional_security = HTTPBearer(auto_error=False)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bool(pwd_context.verify(plain_password, hashed_password))


def get_password_hash(password: str) -> str:
    return str(pwd_context.hash(password))


def create_access_token(
    data: dict[str, Any], expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return str(jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM))


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> models.User:
    """Resolve the current user from a bearer token.

    There is no revocation here, deliberately: a JWT that decodes and
    hasn't expired is accepted, full stop. There is no server-side check
    against a blacklist or a "logged out" flag, so a token issued before a
    password change or an intentional logout stays valid until it expires
    on its own (up to ACCESS_TOKEN_EXPIRE_MINUTES later). A production
    system needs one of: a token blacklist/allowlist checked on every
    request (adds a database or cache lookup to every authenticated call,
    trading away the whole point of a stateless JWT), or short-lived access
    tokens paired with revocable refresh tokens (the more common real-world
    answer, and the reason ACCESS_TOKEN_EXPIRE_MINUTES above is worth
    revisiting before shipping this pattern anywhere real).
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception from e

    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception

    return user


def get_optional_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(optional_security),
    db: Session = Depends(get_db),
) -> models.User | None:
    """Get current user if authenticated, otherwise return None"""
    if not credentials:
        return None

    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None

        return db.query(models.User).filter(models.User.email == email).first()
    except JWTError:
        return None
