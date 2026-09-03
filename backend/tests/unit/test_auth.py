"""
Unit tests for authentication utilities.

These tests verify the core authentication functions work correctly,
including password hashing, token creation, and token validation.

Key Testing Concepts Demonstrated:
- Unit testing isolated functions (no external dependencies)
- AAA Pattern (Arrange-Act-Assert) for clear test structure
- Testing both success and failure scenarios
- Security-focused assertions (password hashing, token validation)
- Edge case testing (empty inputs, invalid tokens)

This file is referenced in Stage 1 learning materials as an example
of professional unit testing practices.
"""

from datetime import UTC, datetime, timedelta

import pytest
from jose import JWTError, jwt

from auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
    get_password_hash,
    verify_password,
)


@pytest.mark.unit
class TestPasswordHashing:
    """
    Test password hashing and verification functions.

    This class demonstrates unit testing of security-critical functions.
    Password hashing is essential for user security - we never store
    plain text passwords, only their bcrypt hashes.

    Key Learning Points:
    - Testing cryptographic functions requires understanding the algorithm
    - We test both positive (correct password) and negative (wrong password) cases
    - We verify the hash format matches bcrypt standards
    - We ensure each hash is unique (salt prevents rainbow table attacks)
    """

    def test_password_is_hashed(self) -> None:
        """
        Test that password hashing produces a different string.

        WHY THIS TEST MATTERS:
        This test verifies the fundamental security principle: passwords
        must be transformed, not stored in plain text. Without this test:
        1. Developers might accidentally store plain text passwords
        2. Security vulnerabilities could go undetected
        3. User data could be compromised in a breach
        4. The application would fail security audits

        REAL-WORLD IMPACT:
        - In 2019, Facebook stored 600M passwords in plain text
        - In 2020, Zoom had a similar issue with 500K accounts
        - These breaches cost millions in fines and lost trust
        - Proper password hashing prevents these disasters

        WHAT WE'RE TESTING:
        1. Hash is different from original password (transformation works)
        2. Hash is longer (bcrypt adds salt and metadata)
        3. Hash follows bcrypt format ($2b$ prefix)

        SECURITY PRINCIPLES:
        - Never store passwords in plain text
        - Use strong hashing algorithms (bcrypt, scrypt, Argon2)
        - Add salt to prevent rainbow table attacks
        - Use appropriate work factors (cost parameter)

        TESTING PATTERN: AAA (Arrange-Act-Assert)
        - Arrange: Set up test data
        - Act: Execute the function being tested
        - Assert: Verify the expected behavior

        This is a critical security test - if this fails, user passwords
        would be stored in plain text, which is a major security vulnerability.
        """
        # Arrange - Set up test data
        password = "TestPassword123!"

        # Act - Execute the function being tested
        hashed = get_password_hash(password)

        # Assert - Verify the results
        assert (
            hashed != password
        ), "Password was stored unhashed - a critical security failure"
        assert len(hashed) > len(
            password
        ), "bcrypt hashes carry salt and metadata, so they're always longer than the input"
        assert hashed.startswith(
            "$2b$"
        ), f"Expected a bcrypt hash (starts with $2b$), got: {hashed[:10]}..."

    def test_verify_correct_password(self) -> None:
        """
        Test that correct password verification succeeds.

        This test verifies the positive case: when a user provides the
        correct password, the verification function should return True.
        This is essential for user login functionality.
        """
        # Arrange - Set up test data
        password = "TestPassword123!"
        hashed = get_password_hash(password)

        # Act - Verify the correct password
        result = verify_password(password, hashed)

        # Assert - Verification should succeed
        assert result is True

    def test_verify_incorrect_password(self) -> None:
        """
        Test that incorrect password verification fails.

        This test verifies the negative case: when a user provides the
        wrong password, verification should fail. This is crucial for
        security - we must reject incorrect passwords.
        """
        # Arrange - Set up test data with wrong password
        password = "TestPassword123!"
        wrong_password = "WrongPassword456!"
        hashed = get_password_hash(password)

        # Act - Verify the incorrect password
        result = verify_password(wrong_password, hashed)

        # Assert - Verification should fail
        assert result is False

    def test_different_hashes_for_same_password(self) -> None:
        """
        Test that same password produces different hashes (salt).

        This test verifies bcrypt's salt functionality. Each password
        should produce a unique hash, even if the password is identical.
        This prevents rainbow table attacks where attackers pre-compute
        hashes for common passwords.
        """
        # Arrange - Set up test password
        password = "TestPassword123!"

        # Act - Hash the same password twice
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)

        # Assert - Different hashes due to random salt (security feature!)
        assert hash1 != hash2, (
            "Hashing the same password twice produced identical hashes - "
            "bcrypt's per-hash salt isn't taking effect, which would make "
            "the app vulnerable to rainbow-table attacks"
        )
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
    def test_various_password_formats(self, password) -> None:
        """Test hashing works with various password formats."""
        hashed = get_password_hash(password)
        assert verify_password(password, hashed) is True


@pytest.mark.unit
class TestJWTTokens:
    """Test JWT token creation and validation."""

    def test_create_token_with_email(self) -> None:
        """Test creating a token with email data."""
        email = "test@example.com"
        token = create_access_token(data={"sub": email})

        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_token_contains_correct_data(self) -> None:
        """Test that token contains the correct payload data."""
        email = "test@example.com"
        token = create_access_token(data={"sub": email})

        # Decode token without verification for testing
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        assert payload["sub"] == email
        assert "exp" in payload

    @pytest.mark.parametrize(
        ("expires_delta", "expected_minutes"),
        [
            pytest.param(timedelta(minutes=30), 30, id="30_minutes"),
            pytest.param(timedelta(hours=2), 120, id="2_hours"),
        ],
    )
    def test_token_expiration_matches_requested_delta(
        self, expires_delta, expected_minutes
    ) -> None:
        """A token's exp claim lands within a minute of now + the requested expires_delta, whether that's a short session or a long one.

        Both cases exercise the same code path (create_access_token's
        expires_delta handling) with only the duration changed, so a
        second, third case beyond "short" and "long" wouldn't add
        coverage a reader can't already infer from these two.
        """
        email = "test@example.com"
        token = create_access_token(data={"sub": email}, expires_delta=expires_delta)

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp_datetime = datetime.fromtimestamp(payload["exp"], tz=UTC)
        now = datetime.now(UTC)

        time_diff_minutes = (exp_datetime - now).total_seconds() / 60
        assert expected_minutes - 1 <= time_diff_minutes <= expected_minutes + 1, (
            f"Expected token to expire in ~{expected_minutes} minutes, "
            f"got {time_diff_minutes:.1f}"
        )

    def test_token_is_verifiable(self) -> None:
        """Test that created token can be verified."""
        email = "test@example.com"
        token = create_access_token(data={"sub": email})

        # Should not raise exception
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert payload["sub"] == email

    def test_invalid_token_raises_error(self) -> None:
        """Test that invalid token raises JWTError."""
        invalid_token = "invalid.token.here"

        with pytest.raises(JWTError):
            jwt.decode(invalid_token, SECRET_KEY, algorithms=[ALGORITHM])

    def test_token_with_wrong_secret_raises_error(self) -> None:
        """Test that token with wrong secret raises error."""
        email = "test@example.com"
        token = create_access_token(data={"sub": email})

        with pytest.raises(JWTError):
            jwt.decode(token, "wrong-secret-key", algorithms=[ALGORITHM])

    def test_expired_token_can_be_detected(self) -> None:
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
        ("password", "should_hash"),
        [
            ("Short1!", True),  # Short but valid
            ("a" * 1000, True),  # Very long
            ("", True),  # Empty (should hash but not pass validation elsewhere)
            ("SimplePassword", True),  # No special chars
            ("12345678", True),  # Only numbers
        ],
    )
    def test_password_hashing_accepts_various_inputs(
        self, password, should_hash
    ) -> None:
        """Test that password hashing accepts various inputs."""
        if should_hash:
            hashed = get_password_hash(password)
            assert verify_password(password, hashed) is True


@pytest.mark.unit
class TestTokenDataStructure:
    """Test token data structure and additional claims."""

    def test_token_with_additional_claims(self) -> None:
        """Test creating token with additional custom claims."""
        data = {"sub": "test@example.com", "role": "admin", "user_id": 123}
        token = create_access_token(data=data)

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        assert payload["sub"] == "test@example.com"
        assert payload["role"] == "admin"
        assert payload["user_id"] == 123

    def test_token_without_expiration_delta(self) -> None:
        """Omitting expires_delta falls back to auth.ACCESS_TOKEN_EXPIRE_MINUTES, not some other default."""
        email = "test@example.com"
        token = create_access_token(data={"sub": email})

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert "exp" in payload

        exp_datetime = datetime.fromtimestamp(payload["exp"], tz=UTC)
        now = datetime.now(UTC)
        time_diff_minutes = (exp_datetime - now).total_seconds() / 60

        assert (
            ACCESS_TOKEN_EXPIRE_MINUTES - 1
            <= time_diff_minutes
            <= ACCESS_TOKEN_EXPIRE_MINUTES + 1
        ), (
            f"Expected the default expiration (~{ACCESS_TOKEN_EXPIRE_MINUTES} "
            f"minutes), got {time_diff_minutes:.1f}"
        )


# 🧠 Why These Tests Matter:
#
# Unit tests for authentication are CRITICAL because:
#
# 1. **Security Foundation** - Password hashing protects user data even if database is breached
# 2. **Fast Feedback** - These tests run in milliseconds, developers run them constantly
# 3. **Edge Cases** - Testing unicode, long passwords, special characters prevents real-world bugs
# 4. **Token Validity** - JWT tests ensure authentication works correctly across the application
#
# In Real QA Teams:
# - These tests run on every commit (CI/CD)
# - They catch security regressions before code review
# - Failed auth tests block deployments
# - They document security requirements (password hashing, token expiration)
#
# For Your Career:
# - Security testing is a high-value skill
# - These demonstrate you understand cryptography basics (hashing, tokens)
# - Interview question: "How would you test authentication?" - You can point to these!
# - Shows you think about edge cases (unicode, empty passwords, timing)
