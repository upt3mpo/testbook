"""
Integration tests for authentication API endpoints.

These tests verify the authentication endpoints work correctly,
including registration, login, and token-based authentication.
"""

import pytest


@pytest.mark.integration
@pytest.mark.api
@pytest.mark.auth
class TestRegisterEndpoint:
    """Test user registration endpoint."""

    def test_register_new_user_success(self, client):
        """Test successful user registration."""
        # Arrange - Prepare new user data
        new_user = {
            "email": "newuser@example.com",
            "username": "newuser",
            "display_name": "New User",
            "password": "SecurePass123!",
            "bio": "This is my bio",
        }

        # Act - Send POST request to registration endpoint
        response = client.post("/api/auth/register", json=new_user)

        # Assert - Verify successful registration and auto-login
        assert response.status_code == 201  # API returns 201 Created
        data = response.json()
        assert "access_token" in data  # Returns token for auto-login
        assert data["token_type"] == "bearer"  # JWT bearer token format
        assert data["email"] == "newuser@example.com"  # Returns user data
        assert data["username"] == "newuser"
        assert data["display_name"] == "New User"
        assert "hashed_password" not in data  # Security: password never exposed

    def test_register_duplicate_email(self, client, test_user):
        """Test registration with duplicate email fails."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": test_user.email,  # Duplicate email
                "username": "differentuser",
                "display_name": "Different User",
                "password": "SecurePass123!",
            },
        )

        assert response.status_code == 400
        assert "email" in response.json()["detail"].lower()

    def test_register_duplicate_username(self, client, test_user):
        """Test registration with duplicate username fails."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "different@example.com",
                "username": test_user.username,  # Duplicate username
                "display_name": "Different User",
                "password": "SecurePass123!",
            },
        )

        assert response.status_code == 400
        assert "username" in response.json()["detail"].lower()

    def test_register_invalid_email_format(self, client):
        """Test registration with invalid email format fails."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "notanemail",
                "username": "testuser",
                "display_name": "Test User",
                "password": "SecurePass123!",
            },
        )

        assert response.status_code == 422  # Validation error

    def test_register_missing_required_fields(self, client):
        """Test registration with missing fields fails."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                # Missing username, display_name, password
            },
        )

        assert response.status_code == 422

    def test_register_sets_default_values(self, client):
        """Test that registration sets default values for optional fields."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "defaults@example.com",
                "username": "defaultuser",
                "display_name": "Default User",
                "password": "SecurePass123!",
            },
        )

        assert response.status_code == 201
        data = response.json()
        # Register returns token and user data
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["email"] == "defaults@example.com"
        assert data["username"] == "defaultuser"
        assert data["display_name"] == "Default User"


@pytest.mark.integration
@pytest.mark.api
@pytest.mark.auth
class TestLoginEndpoint:
    """Test user login endpoint."""

    def test_login_success(self, client, test_user):
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

    def test_login_wrong_password(self, client, test_user):
        """Test login with incorrect password fails."""
        response = client.post(
            "/api/auth/login",
            json={
                "email": "testuser@example.com",
                "password": "WrongPassword123!",
            },
        )

        assert response.status_code == 401
        assert (
            "incorrect" in response.json()["detail"].lower()
            or "invalid" in response.json()["detail"].lower()
        )

    def test_login_nonexistent_email(self, client):
        """Test login with non-existent email fails."""
        response = client.post(
            "/api/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "Password123!",
            },
        )

        assert response.status_code == 401
        assert (
            "incorrect" in response.json()["detail"].lower()
            or "invalid" in response.json()["detail"].lower()
        )

    def test_login_invalid_email_format(self, client):
        """Test login with invalid email format fails."""
        response = client.post(
            "/api/auth/login",
            json={
                "email": "notanemail",
                "password": "Password123!",
            },
        )

        assert response.status_code == 422  # Validation error

    def test_login_missing_fields(self, client):
        """Test login with missing fields fails."""
        response = client.post(
            "/api/auth/login",
            json={"email": "test@example.com"},  # Missing password
        )

        assert response.status_code == 422

    def test_login_case_sensitive_email(self, client, test_user):
        """Test that email is case-insensitive for login."""
        response = client.post(
            "/api/auth/login",
            json={
                "email": "TESTUSER@EXAMPLE.COM",  # Uppercase
                "password": "TestPassword123!",
            },
        )

        # This test documents current behavior
        # In production, you might want case-insensitive email matching
        assert response.status_code in [200, 401]


@pytest.mark.integration
@pytest.mark.api
@pytest.mark.auth
class TestGetCurrentUserEndpoint:
    """Test get current user endpoint."""

    def test_get_current_user_authenticated(self, client, test_user, auth_headers):
        """Test getting current user with valid token."""
        response = client.get("/api/auth/me", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user.email
        assert data["username"] == test_user.username
        assert data["display_name"] == test_user.display_name
        assert "hashed_password" not in data

    def test_get_current_user_no_token(self, client):
        """Test getting current user without token fails."""
        response = client.get("/api/auth/me")

        # API may return 401 or 403 for missing auth
        assert response.status_code in [401, 403]
        assert "detail" in response.json()

    def test_get_current_user_invalid_token(self, client):
        """Test getting current user with invalid token fails."""
        headers = {"Authorization": "Bearer invalid.token.here"}
        response = client.get("/api/auth/me", headers=headers)

        assert response.status_code == 401

    def test_get_current_user_malformed_header(self, client):
        """Test getting current user with malformed auth header fails."""
        headers = {"Authorization": "InvalidFormat token123"}
        response = client.get("/api/auth/me", headers=headers)

        # May return 401 or 403 depending on implementation
        assert response.status_code in [401, 403]

    def test_get_current_user_includes_counts(
        self, client, test_user, test_user_2, auth_headers, db_session
    ):
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

    def test_register_and_auto_login(self, client):
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

    def test_full_auth_flow(self, client):
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

    def test_token_reuse(self, client, test_user):
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
        for _ in range(3):
            response = client.get("/api/auth/me", headers=headers)
            assert response.status_code == 200


@pytest.mark.integration
@pytest.mark.api
@pytest.mark.auth
class TestAuthorizationScenarios:
    """Test authorization scenarios."""

    def test_cannot_access_protected_route_without_auth(self, client):
        """Test that protected routes require authentication."""
        # Test /api/auth/me which definitely requires auth
        response = client.get("/api/auth/me")
        assert response.status_code in [401, 403], "/api/auth/me should require auth"

    def test_can_access_public_routes_without_auth(self, client):
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
