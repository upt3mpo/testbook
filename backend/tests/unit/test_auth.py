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

from datetime import datetime, timedelta, timezone

import pytest
from jose import JWTError, jwt

from auth import ALGORITHM, SECRET_KEY, create_access_token, get_password_hash, verify_password


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

    def test_password_is_hashed(self):
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
        assert hashed != password  # Password is transformed, not stored plainly
        assert len(hashed) > len(password)  # Hash is longer than original
        assert hashed.startswith("$2b$")  # bcrypt hash format (industry standard)

    def test_verify_correct_password(self):
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

    def test_verify_incorrect_password(self):
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

    def test_different_hashes_for_same_password(self):
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
        assert hash1 != hash2  # Each hash is unique due to salt
        assert verify_password(password, hash1) is True  # Both verify correctly
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
        token = create_access_token(data={"sub": email}, expires_delta=timedelta(seconds=-1))

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
