"""
Authentication E2E Tests - Python/Playwright
Tests user registration, login, and logout flows
"""

import re
import time

from playwright.sync_api import Page, expect


class TestAuthentication:
    """Test suite for authentication flows"""

    # Registration Tests
    def test_register_new_user_successfully(
        self, page: Page, base_url: str, test_users: dict, fresh_database
    ):
        """Test new user registration"""
        # Arrange - Navigate to registration page and prepare unique user data
        page.goto(f"{base_url}/register")

        timestamp = int(time.time())
        new_user = {
            "email": f"testuser{timestamp}@testbook.com",
            "username": f"testuser{timestamp}",
            "displayName": "Test User",
            "password": "TestPass123!",
        }

        # Act - Fill registration form and submit
        page.fill('[data-testid="register-email-input"]', new_user["email"])
        page.fill('[data-testid="register-username-input"]', new_user["username"])
        page.fill('[data-testid="register-displayname-input"]', new_user["displayName"])
        page.fill('[data-testid="register-password-input"]', new_user["password"])
        page.click('[data-testid="register-submit-button"]')

        # Assert - Verify auto-login and redirect to feed
        page.wait_for_url(f"{base_url}/", timeout=10000)  # Redirected to feed
        expect(page.locator('[data-testid="navbar"]')).to_be_visible(
            timeout=10000
        )  # Logged in
        expect(page.locator('[data-testid="navbar-username"]')).to_contain_text(
            new_user["displayName"]  # Correct user displayed
        )

    def test_register_duplicate_email_error(
        self, page: Page, base_url: str, test_users: dict, fresh_database
    ):
        """Test registration fails with duplicate email"""
        page.goto(f"{base_url}/register")

        # Try to register with existing email
        page.fill('[data-testid="register-email-input"]', test_users["sarah"]["email"])
        page.fill('[data-testid="register-username-input"]', "differentuser")
        page.fill('[data-testid="register-displayname-input"]', "Different User")
        page.fill('[data-testid="register-password-input"]', "Password123!")
        page.click('[data-testid="register-submit-button"]')

        # Should show error
        expect(page.locator("text=/email.*already/i")).to_be_visible(timeout=5000)

    def test_register_duplicate_username_error(
        self, page: Page, base_url: str, test_users: dict, fresh_database
    ):
        """Test registration fails with duplicate username"""
        page.goto(f"{base_url}/register")

        # Try to register with existing username
        page.fill('[data-testid="register-email-input"]', "newemail@example.com")
        page.fill(
            '[data-testid="register-username-input"]', test_users["sarah"]["username"]
        )
        page.fill('[data-testid="register-displayname-input"]', "Different User")
        page.fill('[data-testid="register-password-input"]', "Password123!")
        page.click('[data-testid="register-submit-button"]')

        # Should show error
        expect(page.locator("text=/username.*already/i")).to_be_visible(timeout=5000)

    def test_register_validate_email_format(self, page: Page, base_url: str):
        """Test registration validates email format"""
        page.goto(f"{base_url}/register")

        page.fill('[data-testid="register-email-input"]', "notanemail")
        page.fill('[data-testid="register-username-input"]', "testuser")
        page.fill('[data-testid="register-displayname-input"]', "Test User")
        page.fill('[data-testid="register-password-input"]', "Password123!")

        # Should show HTML5 validation or custom error
        email_input = page.locator('[data-testid="register-email-input"]')
        is_invalid = email_input.evaluate("el => !el.validity.valid")
        assert is_invalid

    # Login Tests
    def test_login_success(
        self, page: Page, base_url: str, test_users: dict, fresh_database
    ):
        """Test successful login with valid credentials"""
        page.goto(base_url)

        # Fill login form
        user = test_users["sarah"]
        page.fill('[data-testid="login-email-input"]', user["email"])
        page.fill('[data-testid="login-password-input"]', user["password"])

        # Submit
        page.click('[data-testid="login-submit-button"]')

        # Should be on feed page
        page.wait_for_url(f"{base_url}/", timeout=10000)
        expect(page.locator('[data-testid="navbar"]')).to_be_visible(timeout=10000)
        expect(page.locator('[data-testid="navbar-username"]')).to_contain_text(
            user["name"]
        )

    def test_login_wrong_password_error(
        self, page: Page, base_url: str, test_users: dict, fresh_database
    ):
        """Test login shows error for wrong password"""
        page.goto(base_url)

        page.fill('[data-testid="login-email-input"]', test_users["sarah"]["email"])
        page.fill('[data-testid="login-password-input"]', "WrongPassword123!")
        page.click('[data-testid="login-submit-button"]')

        # Should show error
        expect(page.locator('[data-testid="login-error"]')).to_be_visible(timeout=5000)
        expect(page.locator('[data-testid="login-error"]')).to_contain_text(
            re.compile("incorrect|invalid", re.IGNORECASE)
        )

    def test_login_nonexistent_user_error(
        self, page: Page, base_url: str, fresh_database
    ):
        """Test login shows error for non-existent user"""
        page.goto(base_url)

        page.fill('[data-testid="login-email-input"]', "nonexistent@example.com")
        page.fill('[data-testid="login-password-input"]', "Password123!")
        page.click('[data-testid="login-submit-button"]')

        # Should show error
        expect(page.locator('[data-testid="login-error"]')).to_be_visible(timeout=5000)
        expect(page.locator('[data-testid="login-error"]')).to_contain_text(
            re.compile("incorrect|invalid", re.IGNORECASE)
        )

    def test_login_persist_across_refresh(
        self, page: Page, base_url: str, test_users: dict, fresh_database
    ):
        """Test login persists across page refreshes"""
        page.goto(base_url)

        user = test_users["sarah"]
        page.fill('[data-testid="login-email-input"]', user["email"])
        page.fill('[data-testid="login-password-input"]', user["password"])
        page.click('[data-testid="login-submit-button"]')

        page.wait_for_url(f"{base_url}/", timeout=10000)

        # Reload page
        page.reload()

        # Should still be logged in
        expect(page.locator('[data-testid="navbar"]')).to_be_visible(timeout=10000)
        expect(page.locator('[data-testid="navbar-username"]')).to_contain_text(
            user["name"]
        )

    # Logout Tests
    def test_logout_success(self, page: Page, base_url: str, login_as):
        """Test user logout"""
        # Login first
        login_as("sarah")

        # Click logout
        page.click('[data-testid="navbar-logout-button"]')

        # Should be redirected to login page
        expect(page.locator('[data-testid="login-email-input"]')).to_be_visible(
            timeout=5000
        )
        expect(page.locator('[data-testid="navbar"]')).not_to_be_visible()

    def test_logout_cannot_access_protected_routes(
        self, page: Page, base_url: str, login_as
    ):
        """Test cannot access protected routes after logout"""
        # Login first
        login_as("sarah")

        # Logout
        page.click('[data-testid="navbar-logout-button"]')

        # Try to access protected route
        page.goto(f"{base_url}/settings")

        # Should be redirected to login
        expect(page.locator('[data-testid="login-email-input"]')).to_be_visible(
            timeout=5000
        )

    # Protected Routes Tests
    def test_protected_route_feed_redirects(self, page: Page, base_url: str):
        """Test feed redirects to login when not authenticated"""
        page.goto(base_url)

        # Should show login page
        expect(page.locator('[data-testid="login-email-input"]')).to_be_visible()

    def test_protected_route_settings_redirects(self, page: Page, base_url: str):
        """Test settings redirects to login when not authenticated"""
        page.goto(f"{base_url}/settings")

        # Should show login page
        expect(page.locator('[data-testid="login-email-input"]')).to_be_visible()

    def test_protected_route_profile_redirects(
        self, page: Page, base_url: str, test_users: dict
    ):
        """Test profile redirects to login when not authenticated"""
        page.goto(f"{base_url}/profile/{test_users['sarah']['username']}")

        # Should show login page
        expect(page.locator('[data-testid="login-email-input"]')).to_be_visible()

    # Auto-login after Registration
    def test_auto_login_after_registration(
        self, page: Page, base_url: str, fresh_database
    ):
        """Test automatically login after successful registration"""
        page.goto(f"{base_url}/register")

        timestamp = int(time.time())
        new_user = {
            "email": f"autouser{timestamp}@testbook.com",
            "username": f"autouser{timestamp}",
            "displayName": "Auto User",
            "password": "AutoPass123!",
        }

        page.fill('[data-testid="register-email-input"]', new_user["email"])
        page.fill('[data-testid="register-username-input"]', new_user["username"])
        page.fill('[data-testid="register-displayname-input"]', new_user["displayName"])
        page.fill('[data-testid="register-password-input"]', new_user["password"])
        page.click('[data-testid="register-submit-button"]')

        # Should be logged in without manual login
        page.wait_for_url(f"{base_url}/", timeout=10000)
        expect(page.locator('[data-testid="navbar"]')).to_be_visible(timeout=10000)

        # Should be able to access protected routes
        page.click('[data-testid="navbar-settings-link"]')
        expect(page.locator('[data-testid="settings-email"]')).to_contain_text(
            new_user["email"], timeout=10000
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
