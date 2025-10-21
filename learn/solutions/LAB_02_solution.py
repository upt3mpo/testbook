"""
Lab 2 Solution: Testing Real Functions

Complete solutions for password hashing and JWT token testing.
"""

from datetime import datetime, timedelta

import pytest
from auth import (
    create_access_token,
    decode_token,
    get_password_hash,
    verify_password,
)


@pytest.mark.unit
class TestPasswordHashing:
    """Test password hashing functions."""

    def test_password_is_hashed(self):
        """Test that password hashing produces a different string."""
        password = "TestPassword123!"
        hashed = get_password_hash(password)

        # Password should be transformed
        assert hashed != password
        assert len(hashed) > len(password)

        # Bcrypt format check
        assert hashed.startswith("$2b$")

    def test_password_hash_is_consistent_length(self):
        """Test that bcrypt hashes are always 60 characters."""
        password1 = "short"
        password2 = "this is a very long password with lots of characters"

        hash1 = get_password_hash(password1)
        hash2 = get_password_hash(password2)

        # Bcrypt always produces 60-character hashes
        assert len(hash1) == 60
        assert len(hash2) == 60

    def test_same_password_produces_different_hashes(self):
        """Test that hashing same password twice produces different hashes (salt)."""
        password = "TestPassword123!"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)

        # Should be different (bcrypt uses random salt)
        assert hash1 != hash2

        # But both should verify
        assert verify_password(password, hash1)
        assert verify_password(password, hash2)

    def test_verify_correct_password(self):
        """Test that correct password verification succeeds."""
        password = "TestPassword123!"
        hashed = get_password_hash(password)

        assert verify_password(password, hashed) is True

    def test_verify_wrong_password(self):
        """Test that wrong password verification fails."""
        password = "TestPassword123!"
        wrong_password = "WrongPassword456!"
        hashed = get_password_hash(password)

        assert verify_password(wrong_password, hashed) is False

    def test_empty_password(self):
        """Test handling of empty password."""
        # bcrypt can handle empty strings
        hashed = get_password_hash("")
        assert hashed.startswith("$2b$")
        assert verify_password("", hashed) is True

    def test_special_characters_in_password(self):
        """Test password with special characters."""
        password = "P@ssw0rd!#$%^&*()"
        hashed = get_password_hash(password)

        assert verify_password(password, hashed) is True
        assert verify_password("P@ssw0rd", hashed) is False

    def test_unicode_password(self):
        """Test password with unicode characters."""
        password = "Пароль123!🔒"
        hashed = get_password_hash(password)

        assert verify_password(password, hashed) is True

    def test_very_long_password(self):
        """Test with very long password."""
        password = "a" * 100  # 100 characters
        hashed = get_password_hash(password)

        assert verify_password(password, hashed) is True
        assert len(hashed) == 60  # Still 60 chars


@pytest.mark.unit
class TestJWTTokens:
    """Test JWT token creation and validation."""

    def test_create_access_token(self):
        """Test creating access token."""
        data = {"sub": "test@example.com"}
        token = create_access_token(data=data)

        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

        # JWT has 3 parts separated by dots
        assert token.count(".") == 2

    def test_token_contains_subject(self):
        """Test that token contains the subject."""
        email = "test@example.com"
        data = {"sub": email}
        token = create_access_token(data=data)

        # Decode token to verify contents
        # (In production, would use proper validation)
        payload = decode_token(token)
        assert payload["sub"] == email

    def test_token_has_expiration(self):
        """Test that token has expiration time."""
        data = {"sub": "test@example.com"}
        token = create_access_token(data=data)

        payload = decode_token(token)
        assert "exp" in payload

        # Expiration should be in the future
        exp_timestamp = payload["exp"]
        now_timestamp = datetime.utcnow().timestamp()
        assert exp_timestamp > now_timestamp

    def test_token_expires_in_30_minutes(self):
        """Test that token expires in 30 minutes (default)."""
        data = {"sub": "test@example.com"}
        token = create_access_token(data=data)

        payload = decode_token(token)
        exp_time = datetime.fromtimestamp(payload["exp"])
        now = datetime.utcnow()

        # Should expire in about 30 minutes
        diff = exp_time - now
        assert 29 < diff.total_seconds() / 60 < 31

    def test_create_token_with_custom_expiration(self):
        """Test creating token with custom expiration."""
        data = {"sub": "test@example.com"}
        # Create token that expires in 60 minutes
        token = create_access_token(data=data, expires_delta=timedelta(minutes=60))

        payload = decode_token(token)
        exp_time = datetime.fromtimestamp(payload["exp"])
        now = datetime.utcnow()

        # Should expire in about 60 minutes
        diff = exp_time - now
        assert 59 < diff.total_seconds() / 60 < 61

    def test_token_with_additional_claims(self):
        """Test creating token with additional claims."""
        data = {
            "sub": "test@example.com",
            "role": "admin",
            "permissions": ["read", "write"],
        }
        token = create_access_token(data=data)

        payload = decode_token(token)
        assert payload["sub"] == "test@example.com"
        assert payload["role"] == "admin"
        assert payload["permissions"] == ["read", "write"]


# Additional edge cases and challenge solutions


@pytest.mark.unit
class TestPasswordEdgeCases:
    """Test edge cases for password handling."""

    def test_null_password_handling(self):
        """Test that None password is handled."""
        # This tests error handling - should it allow None?
        # Actual behavior depends on implementation
        try:
            hashed = get_password_hash(None)
            # If it doesn't raise, verify it created something
            assert hashed is not None
        except (TypeError, AttributeError):
            # If it raises, that's also valid behavior
            pass

    def test_whitespace_password(self):
        """Test password that's only whitespace."""
        password = "   "
        hashed = get_password_hash(password)

        assert verify_password("   ", hashed) is True
        assert verify_password("  ", hashed) is False  # Different spaces

    def test_case_sensitive_verification(self):
        """Test that password verification is case-sensitive."""
        password = "Password123!"
        hashed = get_password_hash(password)

        assert verify_password("Password123!", hashed) is True
        assert verify_password("password123!", hashed) is False
        assert verify_password("PASSWORD123!", hashed) is False


# Grading Notes for Instructors:
#
# EXCELLENT (95-100%):
# - All required tests present and passing
# - Tests additional edge cases
# - Well-documented with clear docstrings
# - Demonstrates deep understanding
# - Covers None/empty/special character cases
#
# GOOD (85-94%):
# - All required tests present and passing
# - Some edge cases tested
# - Good documentation
# - Shows solid understanding
#
# ACCEPTABLE (75-84%):
# - Most required tests present
# - Basic test coverage
# - Minimal documentation
# - Demonstrates basic understanding
#
# NEEDS IMPROVEMENT (<75%):
# - Missing tests
# - Tests don't pass
# - Poor documentation
# - Doesn't show understanding
#
# Common issues to watch for:
# 1. Not testing edge cases (empty, None, special chars)
# 2. Only testing happy path
# 3. Not understanding what each function does
# 4. Hardcoded values instead of using variables
# 5. Missing docstrings
