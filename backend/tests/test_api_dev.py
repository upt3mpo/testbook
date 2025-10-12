"""
Tests for /api/dev endpoints

These endpoints are protected by test mode and should only be accessible
when TESTING=true is set in the environment.
"""

import os

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestDevEndpointsWithoutTestMode:
    """Test that dev endpoints are properly gated when TESTING is not set"""

    def setup_method(self):
        """Save original TESTING env var"""
        self.original_testing = os.getenv("TESTING")
        # Ensure TESTING is not set
        if "TESTING" in os.environ:
            del os.environ["TESTING"]

    def teardown_method(self):
        """Restore original TESTING env var"""
        if self.original_testing:
            os.environ["TESTING"] = self.original_testing
        elif "TESTING" in os.environ:
            del os.environ["TESTING"]

    def test_reset_endpoint_blocked_without_test_mode(self):
        """POST /api/dev/reset should return 403 without test mode"""
        response = client.post("/api/dev/reset")
        assert response.status_code == 403
        assert "test mode" in response.json()["detail"].lower()

    def test_seed_endpoint_blocked_without_test_mode(self):
        """POST /api/dev/seed should return 403 without test mode"""
        response = client.post("/api/dev/seed")
        assert response.status_code == 403
        assert "test mode" in response.json()["detail"].lower()

    def test_users_endpoint_blocked_without_test_mode(self):
        """GET /api/dev/users should return 403 without test mode"""
        response = client.get("/api/dev/users")
        assert response.status_code == 403
        assert "test mode" in response.json()["detail"].lower()

    def test_create_post_endpoint_blocked_without_test_mode(self):
        """POST /api/dev/create-post should return 403 without test mode"""
        response = client.post(
            "/api/dev/create-post", params={"user_id": 1, "content": "Test post"}
        )
        assert response.status_code == 403
        assert "test mode" in response.json()["detail"].lower()


class TestDevEndpointsWithTestMode:
    """Test that dev endpoints work correctly when TESTING=true"""

    def setup_method(self):
        """Set TESTING=true for these tests"""
        self.original_testing = os.getenv("TESTING")
        os.environ["TESTING"] = "true"

    def teardown_method(self):
        """Restore original TESTING env var"""
        if self.original_testing:
            os.environ["TESTING"] = self.original_testing
        else:
            if "TESTING" in os.environ:
                del os.environ["TESTING"]

    def test_users_endpoint_with_test_mode(self):
        """GET /api/dev/users should return users with passwords in test mode"""
        response = client.get("/api/dev/users")
        assert response.status_code == 200
        users = response.json()
        assert isinstance(users, list)
        if len(users) > 0:
            # Check that password field is present (security warning: only for testing!)
            assert "password" in users[0]
            assert "email" in users[0]
            assert "username" in users[0]

    def test_seed_endpoint_with_test_mode(self):
        """POST /api/dev/seed should work in test mode"""
        response = client.post("/api/dev/seed")
        assert response.status_code == 200
        assert "seeded" in response.json()["message"].lower()

    def test_reset_endpoint_with_test_mode(self):
        """POST /api/dev/reset should work in test mode"""
        response = client.post("/api/dev/reset")
        assert response.status_code == 200
        assert "reset" in response.json()["message"].lower()

    def test_create_post_endpoint_with_test_mode(self):
        """POST /api/dev/create-post should work in test mode"""
        # First, ensure we have a seeded database
        client.post("/api/dev/reset")

        response = client.post(
            "/api/dev/create-post",
            params={"user_id": 1, "content": "Test post from API"},
        )
        assert response.status_code == 200
        assert "created" in response.json()["message"].lower()
        assert response.json()["post_id"] is not None

    def test_create_post_with_invalid_user(self):
        """POST /api/dev/create-post should handle invalid user gracefully"""
        response = client.post(
            "/api/dev/create-post", params={"user_id": 99999, "content": "Test"}
        )
        assert response.status_code == 200
        assert "error" in response.json()


class TestDevEndpointsTestModeCaseInsensitive:
    """Test that TESTING env var accepts various case formats"""

    def teardown_method(self):
        """Clean up TESTING env var"""
        if "TESTING" in os.environ:
            del os.environ["TESTING"]

    def test_testing_true_lowercase(self):
        """TESTING=true (lowercase) should enable test mode"""
        os.environ["TESTING"] = "true"
        response = client.get("/api/dev/users")
        assert response.status_code == 200

    def test_testing_true_uppercase(self):
        """TESTING=TRUE (uppercase) should enable test mode"""
        os.environ["TESTING"] = "TRUE"
        response = client.get("/api/dev/users")
        assert response.status_code == 200

    def test_testing_true_mixed_case(self):
        """TESTING=True (mixed case) should enable test mode"""
        os.environ["TESTING"] = "True"
        response = client.get("/api/dev/users")
        assert response.status_code == 200

    def test_testing_false_blocks_access(self):
        """TESTING=false should block dev endpoints"""
        os.environ["TESTING"] = "false"
        response = client.get("/api/dev/users")
        assert response.status_code == 403

    def test_testing_empty_blocks_access(self):
        """TESTING='' (empty string) should block dev endpoints"""
        os.environ["TESTING"] = ""
        response = client.get("/api/dev/users")
        assert response.status_code == 403
