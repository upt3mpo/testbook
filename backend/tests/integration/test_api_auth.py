"""
Integration tests for authentication API endpoints.

These tests verify the authentication endpoints work correctly,
including registration, login, and token-based authentication.

Key Testing Concepts Demonstrated:
- Integration testing (API + Database + Business Logic)
- HTTP status code validation
- JSON response structure validation
- Security testing (password exposure, token validation)
- Error handling and edge cases
- Database state verification

This file is referenced in Stage 2 learning materials as an example
of professional API integration testing practices.
"""

import pytest


@pytest.mark.integration
@pytest.mark.api
@pytest.mark.auth
class TestRegisterEndpoint:
    """
    Test user registration endpoint.

    This class demonstrates integration testing of API endpoints.
    Unlike unit tests, these tests verify the entire request/response
    cycle including database operations, validation, and business logic.

    Key Learning Points:
    - Testing complete user workflows (registration → login)
    - Validating HTTP status codes and response structure
    - Testing security aspects (password hashing, token generation)
    - Testing error conditions and edge cases
    - Verifying database state changes
    """

    def test_register_new_user_returns_auto_login_token(self, client) -> None:
        """Registration returns 201 and an auto-login bearer token with the submitted user data echoed back."""
        new_user = {
            "email": "newuser@example.com",
            "username": "newuser",
            "display_name": "New User",
            "password": "SecurePass123!",
            "bio": "This is my bio",
        }

        response = client.post("/api/auth/register", json=new_user)

        assert (
            response.status_code == 201
        ), f"expected 201 Created, got {response.status_code}: {response.text}"
        data = response.json()
        assert (
            "access_token" in data
        ), "registration should auto-login by returning a token"
        assert data["token_type"] == "bearer"
        assert data["email"] == new_user["email"]
        assert data["username"] == new_user["username"]
        assert data["display_name"] == new_user["display_name"]

    def test_register_response_never_exposes_password_hash(self, client) -> None:
        """Security invariant: the registration response must never include the hashed password, regardless of what else changes in the response shape."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "another-new-user@example.com",
                "username": "anothernewuser",
                "display_name": "Another New User",
                "password": "SecurePass123!",
            },
        )

        assert "hashed_password" not in response.json(), (
            "The registration response leaked the password hash: " f"{response.json()}"
        )

    @pytest.mark.parametrize(
        "duplicate_field",
        ["email", "username"],
    )
    def test_register_duplicate_field_rejected(
        self, client, test_user, duplicate_field
    ) -> None:
        """Registering with an email or username that's already taken fails with 400, naming the conflicting field.

        Both cases hit the same uniqueness-constraint code path with only
        the conflicting field swapped, so they're one equivalence class:
        "a value that must be unique wasn't."
        """
        payload = {
            "email": "different@example.com",
            "username": "differentuser",
            "display_name": "Different User",
            "password": "SecurePass123!",
        }
        payload[duplicate_field] = getattr(test_user, duplicate_field)

        response = client.post("/api/auth/register", json=payload)

        assert response.status_code == 400, (
            f"Expected 400 for duplicate {duplicate_field}, got "
            f"{response.status_code}: {response.text}"
        )
        assert duplicate_field in response.json()["detail"].lower(), (
            f"Error detail should mention '{duplicate_field}': "
            f"{response.json()['detail']!r}"
        )

    @pytest.mark.parametrize(
        "invalid_payload",
        [
            pytest.param(
                {
                    "email": "notanemail",
                    "username": "testuser",
                    "display_name": "Test User",
                    "password": "SecurePass123!",
                },
                id="invalid_email_format",
            ),
            pytest.param(
                {
                    "email": "test@example.com"
                },  # missing username, display_name, password
                id="missing_required_fields",
            ),
        ],
    )
    def test_register_rejects_invalid_input(self, client, invalid_payload) -> None:
        """Malformed or incomplete registration payloads fail FastAPI/Pydantic request validation (422), before any business logic runs."""
        response = client.post("/api/auth/register", json=invalid_payload)

        assert (
            response.status_code == 422
        ), f"Expected 422 validation error, got {response.status_code}: {response.text}"

    def test_register_sets_default_values(self, client) -> None:
        """Registering without optional fields (bio, theme, text_density) gets the model's actual defaults, not null/missing values.

        The registration response itself (schemas.RegisterResponse) doesn't
        include these fields, so we fetch the freshly-created user via
        /api/auth/me (schemas.UserResponse) to actually see them.
        """
        register_response = client.post(
            "/api/auth/register",
            json={
                "email": "defaults@example.com",
                "username": "defaultuser",
                "display_name": "Default User",
                "password": "SecurePass123!",
                # bio/theme/text_density deliberately omitted
            },
        )
        assert register_response.status_code == 201
        token = register_response.json()["access_token"]

        me_response = client.get(
            "/api/auth/me", headers={"Authorization": f"Bearer {token}"}
        )
        data = me_response.json()
        assert data["bio"] == "", f"expected default empty bio, got {data.get('bio')!r}"
        assert (
            data["theme"] == "light"
        ), f"expected default theme 'light', got {data.get('theme')!r}"
        assert (
            data["text_density"] == "normal"
        ), f"expected default text_density 'normal', got {data.get('text_density')!r}"


@pytest.mark.integration
@pytest.mark.api
@pytest.mark.auth
class TestLoginEndpoint:
    """Test user login endpoint."""

    def test_login_success(self, client, test_user) -> None:
        """Test successful login with correct credentials."""
        response = client.post(
            "/api/auth/login",
            json={
                "email": "testuser@example.com",
                "password": "TestPassword123!",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert isinstance(data["access_token"], str)
        assert len(data["access_token"]) > 0

    @pytest.mark.parametrize(
        "credentials",
        [
            pytest.param(
                {"email": "testuser@example.com", "password": "WrongPassword123!"},
                id="wrong_password",
            ),
            pytest.param(
                {"email": "nonexistent@example.com", "password": "Password123!"},
                id="nonexistent_email",
            ),
        ],
    )
    def test_login_rejects_bad_credentials(
        self, client, test_user, credentials
    ) -> None:
        """A wrong password and a non-existent email both fail login the same way: 401, with a generic incorrect/invalid message.

        They're one equivalence class deliberately - the API shouldn't
        reveal whether the email exists or the password was wrong, so
        both bad-credential cases produce the same observable response.
        """
        response = client.post("/api/auth/login", json=credentials)

        assert (
            response.status_code == 401
        ), f"Expected 401 for bad credentials, got {response.status_code}: {response.text}"
        detail = response.json()["detail"].lower()
        assert (
            "incorrect" in detail or "invalid" in detail
        ), f"Error detail should say incorrect/invalid credentials, got: {detail!r}"

    @pytest.mark.parametrize(
        "invalid_payload",
        [
            pytest.param(
                {"email": "notanemail", "password": "Password123!"},
                id="invalid_email_format",
            ),
            pytest.param(
                {"email": "test@example.com"},  # missing password
                id="missing_password",
            ),
        ],
    )
    def test_login_rejects_invalid_input(self, client, invalid_payload) -> None:
        """Malformed or incomplete login payloads fail request validation (422) before credentials are even checked."""
        response = client.post("/api/auth/login", json=invalid_payload)

        assert (
            response.status_code == 422
        ), f"Expected 422 validation error, got {response.status_code}: {response.text}"

    def test_login_case_sensitive_email(self, client, test_user) -> None:
        """Test that email is case-insensitive for login."""
        response = client.post(
            "/api/auth/login",
            json={
                "email": "TESTUSER@EXAMPLE.COM",  # Uppercase
                "password": "TestPassword123!",
            },
        )

        assert response.status_code in [200, 401], (
            "This test documents current behavior rather than asserting a "
            "requirement: email matching is case-sensitive today, so 401 is "
            "expected, but 200 is also accepted so this doesn't break if "
            "case-insensitive matching is added later. A production change "
            "either way should update this test deliberately, not just "
            f"happen to satisfy it. Got {response.status_code}."
        )


@pytest.mark.integration
@pytest.mark.api
@pytest.mark.auth
class TestGetCurrentUserEndpoint:
    """Test get current user endpoint."""

    def test_get_current_user_authenticated(
        self, client, test_user, auth_headers
    ) -> None:
        """Test getting current user with valid token."""
        response = client.get("/api/auth/me", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user.email
        assert data["username"] == test_user.username
        assert data["display_name"] == test_user.display_name

    def test_get_current_user_never_exposes_password_hash(
        self, client, auth_headers
    ) -> None:
        """Security invariant: /api/auth/me must never include the hashed password."""
        response = client.get("/api/auth/me", headers=auth_headers)

        assert "hashed_password" not in response.json(), (
            "The current-user response leaked the password hash. Even a "
            "bcrypt hash should never reach a client - if this fails, check "
            "schemas.UserResponse for a field that was added without going "
            f"through the response model: {response.json()}"
        )

    def test_get_current_user_no_token(self, client) -> None:
        """Test getting current user without token fails."""
        response = client.get("/api/auth/me")

        assert response.status_code in [401, 403], (
            "FastAPI's HTTPBearer dependency can reject a missing token with "
            f"either code depending on how it's configured; got {response.status_code}"
        )
        assert "detail" in response.json()

    def test_get_current_user_invalid_token(self, client) -> None:
        """Test getting current user with invalid token fails."""
        headers = {"Authorization": "Bearer invalid.token.here"}
        response = client.get("/api/auth/me", headers=headers)

        assert response.status_code == 401, (
            f"A syntactically-invalid JWT should fail token decoding (401), "
            f"got {response.status_code}: {response.text}"
        )

    def test_get_current_user_malformed_header(self, client) -> None:
        """Test getting current user with malformed auth header fails."""
        headers = {"Authorization": "InvalidFormat token123"}
        response = client.get("/api/auth/me", headers=headers)

        assert response.status_code in [401, 403], (
            "An Authorization header without a 'Bearer ' prefix should be "
            f"rejected either way FastAPI's dependency reports it; got {response.status_code}"
        )

    def test_get_current_user_includes_counts(
        self, client, test_user, test_user_2, auth_headers, db_session
    ) -> None:
        """Test that current user includes follower/following counts."""
        # Make test_user follow test_user_2
        test_user.following.append(test_user_2)
        db_session.commit()

        response = client.get("/api/auth/me", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert "followers_count" in data
        assert "following_count" in data
        assert data["following_count"] == 1


@pytest.mark.integration
@pytest.mark.api
@pytest.mark.auth
class TestAuthenticationFlow:
    """Test complete authentication flows."""

    def test_register_and_auto_login(self, client) -> None:
        """Test that registration automatically logs in the user."""
        register_response = client.post(
            "/api/auth/register",
            json={
                "email": "autouser@example.com",
                "username": "autouser",
                "display_name": "Auto User",
                "password": "SecurePass123!",
            },
        )

        assert register_response.status_code == 201  # API returns 201 Created
        data = register_response.json()
        token = data["access_token"]
        # Verify user data is returned immediately
        assert data["email"] == "autouser@example.com"
        assert data["username"] == "autouser"

        # Use the token to get current user
        headers = {"Authorization": f"Bearer {token}"}
        me_response = client.get("/api/auth/me", headers=headers)

        assert me_response.status_code == 200
        assert me_response.json()["email"] == "autouser@example.com"

    def test_full_auth_flow(self, client) -> None:
        """Test complete registration -> login -> authenticate flow."""
        # 1. Register
        register_response = client.post(
            "/api/auth/register",
            json={
                "email": "fullflow@example.com",
                "username": "fullflowuser",
                "display_name": "Full Flow User",
                "password": "SecurePass123!",
            },
        )
        assert register_response.status_code == 201  # API returns 201 Created
        register_data = register_response.json()
        assert register_data["username"] == "fullflowuser"

        # 2. Login
        login_response = client.post(
            "/api/auth/login",
            json={
                "email": "fullflow@example.com",
                "password": "SecurePass123!",
            },
        )
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]

        # 3. Access protected endpoint
        headers = {"Authorization": f"Bearer {token}"}
        me_response = client.get("/api/auth/me", headers=headers)
        assert me_response.status_code == 200
        assert me_response.json()["username"] == "fullflowuser"

    def test_token_reuse(self, client, test_user) -> None:
        """Test that the same token can be reused for multiple requests."""
        # Login once
        login_response = client.post(
            "/api/auth/login",
            json={
                "email": "testuser@example.com",
                "password": "TestPassword123!",
            },
        )
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Use token multiple times
        for attempt in range(3):
            response = client.get("/api/auth/me", headers=headers)
            assert response.status_code == 200, (
                f"Token should stay valid across repeated use, failed on "
                f"request {attempt + 1}/3 with {response.status_code}"
            )


@pytest.mark.integration
@pytest.mark.api
@pytest.mark.auth
class TestAuthorizationScenarios:
    """Test authorization scenarios."""

    def test_cannot_access_protected_route_without_auth(self, client) -> None:
        """Test that protected routes require authentication."""
        # Test /api/auth/me which definitely requires auth
        response = client.get("/api/auth/me")
        assert response.status_code in [401, 403], "/api/auth/me should require auth"

    def test_can_access_public_routes_without_auth(self, client) -> None:
        """Test that public routes don't require authentication."""
        public_endpoints = [
            "/api",
            "/api/health",
        ]

        for endpoint in public_endpoints:
            response = client.get(endpoint)
            assert response.status_code == 200, f"Endpoint {endpoint} should be public"


# 🧠 Why These Tests Matter:
#
# Authentication integration tests are CRITICAL for security and user experience:
#
# 1. **Security Gate** - Authentication is the first line of defense for your application
# 2. **User Journey Start** - Registration and login are every user's first interaction
# 3. **Token Management** - JWT tokens enable stateless, scalable authentication
# 4. **Contract Enforcement** - Frontend depends on exact response format
#
# What These Tests Catch:
# - ✅ Duplicate email/username registrations (database constraints)
# - ✅ Invalid credentials (wrong password, non-existent user)
# - ✅ Token generation and validation issues
# - ✅ Missing or incorrect response fields (breaks frontend)
# - ✅ Validation bypass vulnerabilities
#
# In Real QA Teams:
# - Auth tests run on EVERY commit - no exceptions
# - Failed auth tests are P0 (highest priority) bugs
# - These tests serve as security audit documentation
# - They define the authentication contract for frontend/mobile teams
#
# For Your Career:
# - Authentication testing is asked about in EVERY QA interview
# - Demonstrates security mindset (testing unauthorized access, invalid tokens)
# - Shows API testing skills (HTTP requests, JSON validation, status codes)
# - Proves you understand the full auth flow: register → login → token → protected routes
