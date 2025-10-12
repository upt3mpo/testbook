"""Page object for the Profile page"""

from playwright.sync_api import Page, expect

from .base_page import BasePage


class ProfilePage(BasePage):
    """Reusable helpers for interacting with user profiles."""

    def __init__(self, page: Page):
        super().__init__(page)

        # Selectors
        self.profile_username = '[data-testid="profile-username"]'
        self.follow_button = '[data-testid="profile-follow-button"]'
        self.unfollow_button = '[data-testid="profile-unfollow-button"]'
        self.followers_count = '[data-testid="profile-followers-count"]'
        self.following_count = '[data-testid="profile-following-count"]'

    def goto(self, username: str) -> None:
        """Navigate to a user's profile."""
        super().goto(f"/profile/{username}")
        expect(self.page.locator(self.profile_username)).to_be_visible()

    def follow_user(self) -> None:
        """Click the follow button."""
        self.page.click(self.follow_button)
        self.page.wait_for_timeout(300)

    def unfollow_user(self) -> None:
        """Click the unfollow button."""
        self.page.click(self.unfollow_button)
        self.page.wait_for_timeout(300)

    def is_following(self) -> bool:
        """Check if currently following this user."""
        return self.page.locator(self.unfollow_button).is_visible()

    def get_follower_count(self) -> int:
        """Get the number of followers."""
        text = self.page.locator(self.followers_count).inner_text()
        return int(text)

    def get_following_count(self) -> int:
        """Get the number of following."""
        text = self.page.locator(self.following_count).inner_text()
        return int(text)

    def get_post_count(self) -> int:
        """Get the number of posts on profile."""
        return self.page.locator('[data-testid-generic="post-item"]').count()
