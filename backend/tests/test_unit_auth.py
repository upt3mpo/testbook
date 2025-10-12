"""
Unit tests for authentication utilities.

These tests verify the core authentication functions work correctly,
including password hashing, token creation, and token validation.
"""

from datetime import datetime, timedelta, timezone

import pytest
from auth import (
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
    get_password_hash,
    verify_password,
)
from jose import JWTError, jwt


@pytest.mark.unit
class TestPasswordHashing:
    """Test password hashing and verification functions."""

    def test_password_is_hashed(self):
        """Test that password hashing produces a different string."""
        password = "TestPassword123!"
        hashed = get_password_hash(password)

        assert hashed != password
        assert len(hashed) > len(password)
        assert hashed.startswith("$2b$")  # bcrypt hash format

    def test_verify_correct_password(self):
        """Test that correct password verification succeeds."""
        password = "TestPassword123!"
        hashed = get_password_hash(password)

        assert verify_password(password, hashed) is True

    def test_verify_incorrect_password(self):
        """Test that incorrect password verification fails."""
        password = "TestPassword123!"
        wrong_password = "WrongPassword456!"
        hashed = get_password_hash(password)

        assert verify_password(wrong_password, hashed) is False

    def test_different_hashes_for_same_password(self):
        """Test that same password produces different hashes (salt)."""
        password = "TestPassword123!"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)

        assert hash1 != hash2
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True

    @pytest.mark.parametrize(
        "password",
        [
            "SimplePassword123!",
            "Complex!@#$%^&*()Password456",
            "短密码123",  # Unicode password
            "a" * 100,  # Long password
        ],
    )
    def test_various_password_formats(self, password):
        """Test hashing works with various password formats."""
        hashed = get_password_hash(password)
        assert verify_password(password, hashed) is True


@pytest.mark.unit
class TestJWTTokens:
    """Test JWT token creation and validation."""

    def test_create_token_with_email(self):
        """Test creating a token with email data."""
        email = "test@example.com"
        token = create_access_token(data={"sub": email})

        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_token_contains_correct_data(self):
        """Test that token contains the correct payload data."""
        email = "test@example.com"
        token = create_access_token(data={"sub": email})

        # Decode token without verification for testing
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        assert payload["sub"] == email
        assert "exp" in payload

    def test_token_expiration_is_set(self):
        """Test that token has expiration time."""
        email = "test@example.com"
        expires_delta = timedelta(minutes=30)
        token = create_access_token(data={"sub": email}, expires_delta=expires_delta)

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp_timestamp = payload["exp"]
        exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
        now = datetime.now(timezone.utc)

        # Token should expire approximately 30 minutes from now
        time_diff = exp_datetime - now
        assert 29 <= time_diff.total_seconds() / 60 <= 31

    def test_token_with_custom_expiration(self):
        """Test creating token with custom expiration time."""
        email = "test@example.com"
        custom_expiry = timedelta(hours=2)
        token = create_access_token(data={"sub": email}, expires_delta=custom_expiry)

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp_timestamp = payload["exp"]
        exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
        now = datetime.now(timezone.utc)

        time_diff = exp_datetime - now
        assert 119 <= time_diff.total_seconds() / 60 <= 121

    def test_token_is_verifiable(self):
        """Test that created token can be verified."""
        email = "test@example.com"
        token = create_access_token(data={"sub": email})

        # Should not raise exception
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert payload["sub"] == email

    def test_invalid_token_raises_error(self):
        """Test that invalid token raises JWTError."""
        invalid_token = "invalid.token.here"

        with pytest.raises(JWTError):
            jwt.decode(invalid_token, SECRET_KEY, algorithms=[ALGORITHM])

    def test_token_with_wrong_secret_raises_error(self):
        """Test that token with wrong secret raises error."""
        email = "test@example.com"
        token = create_access_token(data={"sub": email})

        with pytest.raises(JWTError):
            jwt.decode(token, "wrong-secret-key", algorithms=[ALGORITHM])

    def test_expired_token_can_be_detected(self):
        """Test that expired tokens can be detected."""
        email = "test@example.com"
        # Create token that expires immediately
        token = create_access_token(
            data={"sub": email}, expires_delta=timedelta(seconds=-1)
        )

        with pytest.raises(jwt.ExpiredSignatureError):
            jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


@pytest.mark.unit
class TestPasswordComplexity:
    """Test password complexity requirements."""

    @pytest.mark.parametrize(
        "password,should_hash",
        [
            ("Short1!", True),  # Short but valid
            ("a" * 1000, True),  # Very long
            ("", True),  # Empty (should hash but not pass validation elsewhere)
            ("SimplePassword", True),  # No special chars
            ("12345678", True),  # Only numbers
        ],
    )
    def test_password_hashing_accepts_various_inputs(self, password, should_hash):
        """Test that password hashing accepts various inputs."""
        if should_hash:
            hashed = get_password_hash(password)
            assert verify_password(password, hashed) is True


@pytest.mark.unit
class TestTokenDataStructure:
    """Test token data structure and additional claims."""

    def test_token_with_additional_claims(self):
        """Test creating token with additional custom claims."""
        data = {"sub": "test@example.com", "role": "admin", "user_id": 123}
        token = create_access_token(data=data)

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        assert payload["sub"] == "test@example.com"
        assert payload["role"] == "admin"
        assert payload["user_id"] == 123

    def test_token_without_expiration_delta(self):
        """Test creating token with default expiration."""
        email = "test@example.com"
        token = create_access_token(data={"sub": email})

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Should have default expiration
        assert "exp" in payload
        exp_datetime = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        now = datetime.now(timezone.utc)

        # Default is 15 minutes
        time_diff = exp_datetime - now
        assert time_diff.total_seconds() > 0  # Should be in future
