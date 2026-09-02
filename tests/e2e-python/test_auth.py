"""
Authentication E2E Tests - Python/Playwright

This file demonstrates comprehensive end-to-end testing of user authentication
flows using Playwright for Python. These tests simulate real user interactions
with the browser to verify complete user journeys.

Key Testing Concepts Demonstrated:
- End-to-end user workflow testing (registration, login, logout)
- Browser automation with Playwright
- Page Object Model: interactions go through pages.auth_page.AuthPage
  rather than raw selectors, so a UI change only needs updating in one place
- Cross-page testing (registration -> login -> feed)
- Error handling and edge case testing
- Async operation handling (waiting for elements, navigation)

This file is referenced in Stage 3 learning materials as an example
of professional E2E testing practices.
"""

import re
import time

from playwright.sync_api import Page, expect

from pages.auth_page import AuthPage


class TestAuthentication:
    """
    Test suite for authentication flows.

    This class demonstrates E2E testing of complete user authentication
    workflows. Unlike unit or integration tests, these tests verify the
    entire user experience from browser interaction to database persistence.

    Key Learning Points:
    - Testing complete user journeys (not just individual functions)
    - Simulating real user behavior in a real browser
    - Handling async operations and timing issues
    - Verifying both positive and negative user flows
    - Cross-page navigation and state management
    """

    # Registration Tests
    def test_register_new_user_successfully(
        self, page: Page, base_url: str, test_users: dict, fresh_database
    ):
        """
        Test new user registration with complete user workflow.

        This test verifies the entire user registration journey:
        1. User navigates to registration page
        2. User fills out registration form
        3. User submits form
        4. System processes registration
        5. User is automatically logged in
        6. User is redirected to feed page
        7. User sees their profile in navigation

        This is a critical E2E test that ensures the complete
        registration flow works from the user's perspective.
        """
        auth = AuthPage(page)
        auth.goto_register()

        # Generate unique user data to avoid conflicts
        timestamp = int(time.time())
        display_name = "Test User"
        auth.register(
            email=f"testuser{timestamp}@testbook.com",
            username=f"testuser{timestamp}",
            display_name=display_name,
            password="TestPass123!",
        )

        auth.expect_logged_in(display_name=display_name)

    def test_register_duplicate_email_error(
        self, page: Page, base_url: str, test_users: dict, fresh_database
    ):
        """Test registration fails with duplicate email"""
        auth = AuthPage(page)
        auth.goto_register()

        # Try to register with existing email
        auth.register(
            email=test_users["sarah"]["email"],
            username="differentuser",
            display_name="Different User",
            password="Password123!",
        )

        auth.expect_register_error(re.compile("email.*already", re.IGNORECASE))

    def test_register_duplicate_username_error(
        self, page: Page, base_url: str, test_users: dict, fresh_database
    ):
        """Test registration fails with duplicate username"""
        auth = AuthPage(page)
        auth.goto_register()

        # Try to register with existing username
        auth.register(
            email="newemail@example.com",
            username=test_users["sarah"]["username"],
            display_name="Different User",
            password="Password123!",
        )

        auth.expect_register_error(re.compile("username.*already", re.IGNORECASE))

    def test_register_validate_email_format(self, page: Page, base_url: str):
        """Test registration validates email format"""
        auth = AuthPage(page)
        auth.goto_register()

        auth.register(
            email="notanemail",
            username="testuser",
            display_name="Test User",
            password="Password123!",
        )

        # Should show HTML5 validation, not a server round-trip
        assert auth.is_register_email_invalid()

    # Login Tests
    def test_login_success(
        self, page: Page, base_url: str, test_users: dict, fresh_database
    ):
        """Test successful login with valid credentials"""
        auth = AuthPage(page)
        auth.goto_login()

        user = test_users["sarah"]
        auth.login(user["email"], user["password"])

        auth.expect_logged_in(display_name=user["name"])

    def test_login_wrong_password_error(
        self, page: Page, base_url: str, test_users: dict, fresh_database
    ):
        """Test login shows error for wrong password"""
        auth = AuthPage(page)
        auth.goto_login()

        auth.login(test_users["sarah"]["email"], "WrongPassword123!")

        auth.expect_login_error(re.compile("incorrect|invalid", re.IGNORECASE))

    def test_login_nonexistent_user_error(
        self, page: Page, base_url: str, fresh_database
    ):
        """Test login shows error for non-existent user"""
        auth = AuthPage(page)
        auth.goto_login()

        auth.login("nonexistent@example.com", "Password123!")

        auth.expect_login_error(re.compile("incorrect|invalid", re.IGNORECASE))

    def test_login_persist_across_refresh(
        self, page: Page, base_url: str, test_users: dict, fresh_database
    ):
        """Test login persists across page refreshes"""
        auth = AuthPage(page)
        auth.goto_login()

        user = test_users["sarah"]
        auth.login(user["email"], user["password"])
        auth.expect_logged_in()

        page.reload()

        # Should still be logged in
        auth.expect_logged_in(display_name=user["name"])

    # Logout Tests
    def test_logout_success(self, page: Page, base_url: str, login_as):
        """Test user logout"""
        login_as("sarah")

        auth = AuthPage(page)
        auth.logout()

        auth.expect_logged_out()

    def test_logout_cannot_access_protected_routes(
        self, page: Page, base_url: str, login_as
    ):
        """Test cannot access protected routes after logout"""
        login_as("sarah")

        auth = AuthPage(page)
        auth.logout()

        # Try to access protected route
        page.goto(f"{base_url}/settings")

        auth.expect_on_login_page()

    # Protected Routes Tests
    def test_protected_route_feed_redirects(self, page: Page, base_url: str):
        """Test feed redirects to login when not authenticated"""
        page.goto(base_url)
        AuthPage(page).expect_on_login_page()

    def test_protected_route_settings_redirects(self, page: Page, base_url: str):
        """Test settings redirects to login when not authenticated"""
        page.goto(f"{base_url}/settings")
        AuthPage(page).expect_on_login_page()

    def test_protected_route_profile_redirects(
        self, page: Page, base_url: str, test_users: dict
    ):
        """Test profile redirects to login when not authenticated"""
        page.goto(f"{base_url}/profile/{test_users['sarah']['username']}")
        AuthPage(page).expect_on_login_page()

    # Auto-login after Registration
    def test_auto_login_after_registration(
        self, page: Page, base_url: str, fresh_database
    ):
        """Test automatically login after successful registration"""
        auth = AuthPage(page)
        auth.goto_register()

        timestamp = int(time.time())
        email = f"autouser{timestamp}@testbook.com"
        auth.register(
            email=email,
            username=f"autouser{timestamp}",
            display_name="Auto User",
            password="AutoPass123!",
        )

        # Should be logged in without manual login
        auth.expect_logged_in()

        # Should be able to access protected routes
        auth.navbar_settings_link.click()
        expect(page.get_by_test_id("settings-email")).to_contain_text(
            email, timeout=10000
        )


# 🧠 Why These Tests Matter:
#
# Python E2E tests with Playwright are POWERFUL because:
#
# 1. **Same Language for Full Stack** - Python for backend API AND frontend UI testing
# 2. **Real Browser Validation** - Tests actual user experience in Chrome/Firefox
# 3. **Integration Verification** - Ensures React frontend and FastAPI backend communicate correctly
# 4. **Visual Regression Detection** - Catches UI breaks that API tests miss
#
# Python's Unique Advantage for E2E:
# - Use requests library to SEED data via API (fast setup)
# - Then use Playwright to VERIFY data in UI (realistic validation)
# - Example: Create 100 posts via API in 2 seconds, verify UI displays them correctly
# - 10-100x faster than clicking through UI for test setup!
#
# What These Tests Catch:
# - ✅ Frontend-backend contract mismatches (API returns snake_case, UI expects camelCase)
# - ✅ UI routing issues (wrong redirects, broken links)
# - ✅ Visual bugs (elements not visible, incorrect text)
# - ✅ Timing issues (race conditions, async operations)
# - ✅ Authentication state bugs (session not persisted, logout doesn't clear state)
#
# In Real QA Teams:
# - E2E tests are the final gate before production deployment
# - They run in CI/CD on every main branch commit
# - Failed E2E tests block releases (most critical test tier)
# - They serve as acceptance tests (proves feature works end-to-end)
#
# For Your Career:
# - Python E2E testing is a RARE and valuable skill
# - Combines backend knowledge with frontend testing
# - Shows you can use Python for complete application testing
# - Interview question: "How would you test a full user workflow?" - Demo this test running!
# - Demonstrates Page Object Model, fixtures, and professional E2E patterns
