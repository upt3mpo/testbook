"""Page object for registration, login, and logout."""

from playwright.sync_api import Page, expect

from .base_page import BasePage


class AuthPage(BasePage):
    """Reusable helpers for the register, login, and logout flows.

    Registration and login are two different pages in the app, but they
    share the same shape of interaction (fill a form, submit, check the
    result), so one page object covers both rather than splitting into
    two classes that would mostly duplicate each other.
    """

    def __init__(self, page: Page):
        super().__init__(page)

        # Registration form
        self.register_email_input = page.get_by_test_id("register-email-input")
        self.register_username_input = page.get_by_test_id("register-username-input")
        self.register_displayname_input = page.get_by_test_id(
            "register-displayname-input"
        )
        self.register_password_input = page.get_by_test_id("register-password-input")
        self.register_submit_button = page.get_by_test_id("register-submit-button")
        self.register_error = page.get_by_test_id("register-error")

        # Login form
        self.login_email_input = page.get_by_test_id("login-email-input")
        self.login_password_input = page.get_by_test_id("login-password-input")
        self.login_submit_button = page.get_by_test_id("login-submit-button")
        self.login_error = page.get_by_test_id("login-error")

        # Navbar (present once logged in)
        self.navbar = page.get_by_test_id("navbar")
        self.navbar_username = page.get_by_test_id("navbar-username")
        self.navbar_logout_button = page.get_by_test_id("navbar-logout-button")
        self.navbar_settings_link = page.get_by_test_id("navbar-settings-link")

    def goto_register(self) -> None:
        """Navigate to the registration page."""
        self.goto("/register")

    def goto_login(self) -> None:
        """Navigate to the login page (the app's root when logged out)."""
        self.goto("/")

    def register(
        self, email: str, username: str, display_name: str, password: str
    ) -> None:
        """Fill out and submit the registration form. Does not wait for
        the result - use expect_logged_in() or expect_register_error()
        after calling this, since a test may want to check either a
        success or a failure path.
        """
        self.register_email_input.fill(email)
        self.register_username_input.fill(username)
        self.register_displayname_input.fill(display_name)
        self.register_password_input.fill(password)
        self.register_submit_button.click()

    def is_register_email_invalid(self) -> bool:
        """Check whether the browser's native HTML5 validation currently
        considers the email field invalid (e.g. after entering
        "notanemail"). Reads the input's own validity state rather than
        submitting the form, since this is checking client-side
        validation, not a server response.
        """
        return self.register_email_input.evaluate("el => !el.validity.valid")

    def login(self, email: str, password: str) -> None:
        """Fill out and submit the login form. Does not wait for the
        result - use expect_logged_in() or expect_login_error() after
        calling this.
        """
        self.login_email_input.fill(email)
        self.login_password_input.fill(password)
        self.login_submit_button.click()

    def logout(self) -> None:
        """Click the navbar logout button."""
        self.navbar_logout_button.click()

    def expect_logged_in(self, display_name: str | None = None) -> None:
        """Assert the navbar is visible (i.e. the user is authenticated),
        and optionally that it shows a specific display name.
        """
        expect(self.page).to_have_url(f"{self.base_url}/", timeout=10000)
        expect(self.navbar).to_be_visible(timeout=10000)
        if display_name is not None:
            expect(self.navbar_username).to_contain_text(display_name)

    def expect_logged_out(self) -> None:
        """Assert the navbar is gone and the login form is showing."""
        expect(self.navbar).not_to_be_visible()
        expect(self.login_email_input).to_be_visible(timeout=5000)

    def expect_on_login_page(self) -> None:
        """Assert the login form is showing (used for protected-route
        redirect checks, where no login has happened yet).
        """
        expect(self.login_email_input).to_be_visible(timeout=5000)

    def expect_login_error(self, pattern) -> None:
        """Assert the login error message is visible and matches pattern."""
        expect(self.login_error).to_be_visible(timeout=5000)
        expect(self.login_error).to_contain_text(pattern)

    def expect_register_error(self, pattern) -> None:
        """Assert the registration error message is visible and matches
        pattern. Uses the register-error testid rather than a raw
        text-content locator, so it doesn't depend on the exact wording
        of the error message staying the same.
        """
        expect(self.register_error).to_be_visible(timeout=5000)
        expect(self.register_error).to_contain_text(pattern)
