"""Page object for the Profile page"""

from playwright.sync_api import Page, expect

from .base_page import BasePage


class ProfilePage(BasePage):
    """Reusable helpers for interacting with user profiles."""

    def __init__(self, page: Page):
        super().__init__(page)

        # Selectors
        self.profile_username = '[data-testid="profile-username"]'
        self.follow_unfollow_button = '[data-testid="profile-follow-button"]'
        self.followers_count = '[data-testid="profile-followers-link"]'
        self.following_count = '[data-testid="profile-following-link"]'

    def goto(self, username: str, wait_for_load: bool = True) -> None:
        """Navigate to a user's profile.

        Args:
            username: The username of the profile to visit
            wait_for_load: If True, wait for profile data to load from API (default: True)
        """
        super().goto(f"/profile/{username}")
        expect(self.page.locator(self.profile_username)).to_be_visible()

        if wait_for_load:
            # Wait for profile to finish loading from API
            # This is important in CI where API calls may be slower
            try:
                self.page.wait_for_load_state("networkidle", timeout=5000)
            except:
                # If networkidle times out, wait a bit more for API calls
                self.page.wait_for_timeout(2000)

    def follow_user(self) -> None:
        """Ensure the user is followed (clicking Follow button if not already following)."""
        button = self.page.locator(self.follow_unfollow_button)
        expect(button).to_be_visible(timeout=5000)

        # Check current state
        current_text = button.inner_text()

        if "Follow" in current_text:
            # Not following yet, click to follow
            button.click()
            self.page.wait_for_timeout(500)
        # If already following ("Unfollow"), do nothing

    def unfollow_user(self) -> None:
        """Click the follow/unfollow button to unfollow the user."""
        button = self.page.locator(self.follow_unfollow_button)
        expect(button).to_be_visible(timeout=5000)

        # Check current state and only unfollow if currently following
        current_text = button.inner_text()

        if "Unfollow" in current_text:
            button.click()
            self.page.wait_for_timeout(500)

    def is_following(self, wait_timeout: int = 5000) -> bool:
        """Check if currently following this user.

        Args:
            wait_timeout: Maximum time to wait for button to appear (milliseconds)

        Returns:
            True if following (button says "Unfollow"), False if not (button says "Follow")
        """
        button = self.page.locator(self.follow_unfollow_button)
        try:
            expect(button).to_be_visible(timeout=wait_timeout)
            button_text = button.inner_text()
            return "Unfollow" in button_text
        except:
            return False

    def get_follower_count(self, wait_timeout: int = 5000) -> int:
        """Get the number of followers.

        Args:
            wait_timeout: Maximum time to wait for count to appear (milliseconds)
        """
        locator = self.page.locator(self.followers_count)
        expect(locator).to_be_visible(timeout=wait_timeout)
        text = locator.inner_text()
        # Extract number from text like "5 followers"
        import re

        match = re.search(r"(\d+)", text)
        return int(match.group(1)) if match else 0

    def get_following_count(self, wait_timeout: int = 5000) -> int:
        """Get the number of following.

        Args:
            wait_timeout: Maximum time to wait for count to appear (milliseconds)
        """
        locator = self.page.locator(self.following_count)
        expect(locator).to_be_visible(timeout=wait_timeout)
        text = locator.inner_text()
        # Extract number from text like "10 following"
        import re

        match = re.search(r"(\d+)", text)
        return int(match.group(1)) if match else 0

    def get_post_count(self) -> int:
        """Get the number of posts on profile."""
        return self.page.locator('[data-testid-generic="post-item"]').count()
