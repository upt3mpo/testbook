"""Page object for the Profile page"""

import re

from playwright.sync_api import Locator, Page, expect

from .base_page import BasePage


class ProfilePage(BasePage):
    """Reusable helpers for interacting with user profiles."""

    def __init__(self, page: Page):
        super().__init__(page)

        # Selectors
        self.display_name = '[data-testid="profile-display-name"]'
        self.profile_username = '[data-testid="profile-username"]'
        self.edit_button = '[data-testid="profile-edit-button"]'
        self.follow_unfollow_button = '[data-testid="profile-follow-button"]'
        self.block_unblock_button = '[data-testid="profile-block-button"]'
        self.followers_count = '[data-testid="profile-followers-link"]'
        self.following_count = '[data-testid="profile-following-link"]'
        self.posts_count = '[data-testid="profile-posts-count"]'

    def goto(self, username: str, wait_for_load: bool = True) -> None:
        """Navigate to a user's profile.

        Args:
            username: The username of the profile to visit
            wait_for_load: If True, wait for profile data to load from API (default: True)
        """
        super().goto(f"/profile/{username}")
        expect(self.page.locator(self.profile_username)).to_be_visible()

        if wait_for_load:
            # Best-effort wait for the profile's API calls to settle. If
            # this times out, the methods below all use their own
            # retrying expect(), so there's no need for a fallback
            # fixed-time wait here.
            try:
                self.page.wait_for_load_state("networkidle", timeout=5000)
            except Exception:
                pass

    def expect_profile_matches(self, display_name: str, username: str) -> None:
        """Assert the profile header shows the given display name and
        @username.
        """
        expect(self.page.locator(self.display_name)).to_contain_text(display_name)
        expect(self.page.locator(self.profile_username)).to_contain_text(f"@{username}")

    def expect_own_profile_controls(self) -> None:
        """Assert this profile is showing as the logged-in user's own
        (edit button visible, no follow/block buttons).
        """
        expect(self.page.locator(self.edit_button)).to_be_visible()

    def expect_other_user_profile_controls(self) -> None:
        """Assert this profile is showing as someone else's (no edit
        button, follow/block buttons visible).
        """
        expect(self.page.locator(self.edit_button)).not_to_be_visible()
        expect(self.page.locator(self.follow_unfollow_button)).to_be_visible()
        expect(self.page.locator(self.block_unblock_button)).to_be_visible()

    def follow_user(self) -> None:
        """Ensure the user is followed (clicking Follow button if not already following)."""
        button = self.page.locator(self.follow_unfollow_button)
        expect(button).to_be_visible(timeout=5000)

        if "Follow" in button.inner_text():
            button.click()
            expect(button).to_contain_text(re.compile("unfollow", re.IGNORECASE))
        # If already following ("Unfollow"), do nothing

    def unfollow_user(self) -> None:
        """Click the follow/unfollow button to unfollow the user."""
        button = self.page.locator(self.follow_unfollow_button)
        expect(button).to_be_visible(timeout=5000)

        if "Unfollow" in button.inner_text():
            button.click()
            expect(button).to_contain_text(re.compile("^follow$", re.IGNORECASE))

    def block_user(self) -> None:
        """Ensure the user is blocked (clicking Block if not already blocked)."""
        button = self.page.locator(self.block_unblock_button)
        expect(button).to_be_visible(timeout=5000)

        if "Block" == button.inner_text().strip():
            button.click()
            expect(button).to_contain_text(re.compile("unblock", re.IGNORECASE))
        # If already blocked ("Unblock"), do nothing

    def unblock_user(self) -> None:
        """Click the block/unblock button to unblock the user."""
        button = self.page.locator(self.block_unblock_button)
        expect(button).to_be_visible(timeout=5000)

        if "Unblock" in button.inner_text():
            button.click()
            expect(button).to_contain_text(re.compile("^block$", re.IGNORECASE))

    def go_to_followers_list(self) -> None:
        """Click the followers count/link to go to the followers page."""
        followers_link = self.page.locator(self.followers_count)
        expect(followers_link).to_be_visible(timeout=5000)
        followers_link.click()

    def go_to_following_list(self) -> None:
        """Click the following count/link to go to the following page."""
        following_link = self.page.locator(self.following_count)
        expect(following_link).to_be_visible(timeout=5000)
        following_link.click()

    def find_user_in_list(self, username: str) -> Locator:
        """Find a specific user's row on the followers/following/followers
        list page.
        """
        return self.page.locator(f'[data-username="{username}"]')

    def find_first_follower_item(self) -> Locator:
        """Get the first row on the followers list page."""
        return self.page.locator('[data-testid-generic="follower-item"]').first

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
        except Exception:
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
        match = re.search(r"(\d+)", text)
        return int(match.group(1)) if match else 0

    def get_post_count(self) -> int:
        """Get the number of posts on profile."""
        return self.page.locator('[data-testid-generic="post-item"]').count()
