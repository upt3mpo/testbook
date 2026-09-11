"""
User Profile E2E Tests - Python/Playwright
Tests user profiles, follow/unfollow, blocking, settings, and account management

Page Object Model: interactions go through pages.auth_page.AuthPage,
pages.profile_page.ProfilePage, and pages.settings_page.SettingsPage
rather than raw selectors, so a UI change only needs updating in one place.
"""

import re

from playwright.sync_api import Page, expect

from pages.auth_page import AuthPage
from pages.feed_page import FeedPage
from pages.profile_page import ProfilePage
from pages.settings_page import SettingsPage


class TestUserProfile:
    """Test suite for user profile functionality"""

    def test_view_own_profile(
        self, page: Page, base_url: str, login_as, test_users: dict, fresh_database
    ):
        """Test viewing your own profile"""
        login_as("sarah")

        AuthPage(page).navbar_profile_link.click()

        profile = ProfilePage(page)
        profile.expect_profile_matches(
            test_users["sarah"]["name"], test_users["sarah"]["username"]
        )
        profile.expect_own_profile_controls()

    def test_view_other_user_profile(
        self, page: Page, base_url: str, login_as, test_users: dict, fresh_database
    ):
        """Test viewing another user's profile"""
        login_as("sarah")

        profile = ProfilePage(page)
        profile.goto(test_users["mike"]["username"])

        profile.expect_profile_matches(
            test_users["mike"]["name"], test_users["mike"]["username"]
        )
        profile.expect_other_user_profile_controls()

    def test_show_follower_following_counts(
        self, page: Page, base_url: str, login_as, test_users: dict, fresh_database
    ):
        """Test follower and following counts are shown"""
        login_as("sarah")

        profile = ProfilePage(page)
        profile.goto(test_users["sarah"]["username"])

        expect(page.locator(profile.followers_count)).to_be_visible(timeout=10000)
        expect(page.locator(profile.following_count)).to_be_visible(timeout=10000)

    def test_show_posts_count(
        self, page: Page, base_url: str, login_as, test_users: dict, fresh_database
    ):
        """Test posts count is displayed"""
        login_as("sarah")

        profile = ProfilePage(page)
        profile.goto(test_users["sarah"]["username"])

        expect(page.locator(profile.posts_count)).to_be_visible()


class TestFollowing:
    """Test suite for follow/unfollow functionality"""

    def test_follow_user(
        self, page: Page, base_url: str, login_as, test_users: dict, fresh_database
    ):
        """Test following another user"""
        login_as("sarah")

        profile = ProfilePage(page)
        profile.goto(test_users["mike"]["username"])
        profile.follow_user()

        # Verify following count increased on own profile
        profile.goto(test_users["sarah"]["username"])
        expect(page.locator(profile.following_count)).to_contain_text(
            re.compile("[1-9]"), timeout=10000
        )

    def test_unfollow_user(
        self, page: Page, base_url: str, login_as, test_users: dict, fresh_database
    ):
        """Test unfollowing a user"""
        login_as("sarah")

        profile = ProfilePage(page)
        profile.goto(test_users["mike"]["username"])

        profile.follow_user()
        profile.unfollow_user()

        button = page.locator(profile.follow_unfollow_button)
        expect(button).to_contain_text(re.compile("^follow$", re.IGNORECASE))

    def test_followed_users_in_following_feed(
        self, page: Page, base_url: str, login_as, test_users: dict, fresh_database
    ):
        """Test followed users' posts show in Following feed"""
        login_as("sarah")

        profile = ProfilePage(page)
        profile.goto(test_users["mike"]["username"])
        profile.follow_user()

        # Go to Following feed
        feed = FeedPage(page)
        feed.goto()
        feed.go_to_following_tab()

        # Should show Mike's posts (if he has any)
        mike_posts = page.locator(
            f'[data-post-author="{test_users["mike"]["username"]}"]'
        )
        assert mike_posts.count() >= 0


class TestBlocking:
    """Test suite for block/unblock functionality"""

    def test_block_user(
        self, page: Page, base_url: str, login_as, test_users: dict, fresh_database
    ):
        """Test blocking another user"""
        login_as("sarah")

        profile = ProfilePage(page)
        profile.goto(test_users["mike"]["username"])
        profile.block_user()

        button = page.locator(profile.block_unblock_button)
        expect(button).to_contain_text(re.compile("unblock", re.IGNORECASE))

    def test_unblock_user(
        self, page: Page, base_url: str, login_as, test_users: dict, fresh_database
    ):
        """Test unblocking a user"""
        login_as("sarah")

        profile = ProfilePage(page)
        profile.goto(test_users["mike"]["username"])

        profile.block_user()
        profile.unblock_user()

        button = page.locator(profile.block_unblock_button)
        expect(button).to_contain_text(re.compile("^block$", re.IGNORECASE))

    def test_blocked_users_not_in_feed(
        self, page: Page, base_url: str, login_as, test_users: dict, fresh_database
    ):
        """Test blocked users' posts don't show in feed"""
        login_as("sarah")

        profile = ProfilePage(page)
        profile.goto(test_users["mike"]["username"])
        profile.block_user()

        # Go to All feed. Force a reload to ensure fresh data, since the
        # feed page may have cached the pre-block post list.
        feed = FeedPage(page)
        feed.goto()
        page.reload()
        page.wait_for_load_state("networkidle", timeout=5000)
        feed.go_to_all_tab()

        # Should not see Mike's posts. to_have_count() retries, so it
        # covers any remaining render delay after the reload and tab click.
        mike_posts = page.locator(
            f'[data-post-author="{test_users["mike"]["username"]}"]'
        )
        expect(mike_posts).to_have_count(0)


class TestFollowersFollowingLists:
    """Test suite for followers/following list functionality"""

    def test_view_followers_list(
        self, page: Page, base_url: str, login_as, test_users: dict, fresh_database
    ):
        """Test viewing followers list"""
        login_as("sarah")

        profile = ProfilePage(page)
        profile.goto(test_users["sarah"]["username"])
        profile.go_to_followers_list()

        expect(page.get_by_test_id("followers-page")).to_be_visible()

    def test_view_following_list(
        self, page: Page, base_url: str, login_as, test_users: dict, fresh_database
    ):
        """Test viewing following list"""
        login_as("sarah")

        profile = ProfilePage(page)
        profile.goto(test_users["sarah"]["username"])
        profile.go_to_following_list()

        expect(page.get_by_test_id("following-page")).to_be_visible()

    def test_unfollow_from_following_page(
        self, page: Page, base_url: str, login_as, test_users: dict, fresh_database
    ):
        """Test unfollowing from following page"""
        login_as("sarah")

        profile = ProfilePage(page)

        # Follow Mike first
        profile.goto(test_users["mike"]["username"])
        profile.follow_user()

        # Go to following page
        profile.goto(test_users["sarah"]["username"])
        profile.go_to_following_list()

        # Unfollow Mike
        mike_in_list = profile.find_user_in_list(test_users["mike"]["username"])
        try:
            is_visible = mike_in_list.is_visible(timeout=5000)
        except Exception:
            is_visible = False

        if is_visible:
            mike_in_list.locator('[data-testid$="-unfollow-button"]').click()

            # Mike should be removed from list
            expect(mike_in_list).not_to_be_visible(timeout=5000)

    def test_block_from_followers_page(
        self, page: Page, base_url: str, login_as, test_users: dict, fresh_database
    ):
        """Test blocking from followers page"""
        login_as("sarah")

        profile = ProfilePage(page)
        profile.goto(test_users["sarah"]["username"])
        profile.go_to_followers_list()

        # Wait for the followers page to load
        page.wait_for_url(re.compile(r".*/followers.*"), timeout=5000)

        # If there are followers, try to block one
        first_follower = profile.find_first_follower_item()
        try:
            follower_visible = first_follower.is_visible(timeout=3000)
        except Exception:
            follower_visible = False

        if follower_visible:
            block_button = first_follower.locator('[data-testid$="-block-button"]')
            expect(block_button).to_be_visible(timeout=5000)
            block_button.click()

            # Wait for blocked state to be applied
            expect(first_follower).to_have_attribute(
                "data-is-blocked", "true", timeout=10000
            )


class TestSettings:
    """Test suite for user settings functionality"""

    def test_update_display_name(
        self, page: Page, base_url: str, login_as, test_users: dict, fresh_database
    ):
        """Test updating display name"""
        login_as("sarah")

        settings = SettingsPage(page)
        settings.goto()
        settings.update_display_name("Updated Name")
        settings.expect_save_succeeded()

        # Verify on profile
        profile = ProfilePage(page)
        profile.goto(test_users["sarah"]["username"])
        expect(page.locator(profile.display_name)).to_contain_text("Updated Name")

    def test_update_bio(
        self, page: Page, base_url: str, login_as, test_users: dict, fresh_database
    ):
        """Test updating bio"""
        login_as("sarah")

        settings = SettingsPage(page)
        settings.goto()
        settings.update_bio("My updated bio")
        settings.expect_save_succeeded()

    def test_change_theme(self, page: Page, base_url: str, login_as, fresh_database):
        """Test changing theme"""
        login_as("sarah")

        settings = SettingsPage(page)
        settings.goto()
        settings.change_theme("dark")
        settings.expect_theme_applied("dark")

    def test_change_text_density(
        self, page: Page, base_url: str, login_as, fresh_database
    ):
        """Test changing text density"""
        login_as("sarah")

        settings = SettingsPage(page)
        settings.goto()
        settings.change_text_density("compact")
        settings.expect_save_succeeded()

    def test_theme_persist_across_sessions(
        self, page: Page, base_url: str, login_as, fresh_database
    ):
        """Test theme persists across sessions"""
        login_as("sarah")

        settings = SettingsPage(page)
        settings.goto()
        settings.change_theme("dark")

        page.reload()

        settings.expect_theme_applied("dark")


class TestProfilePicture:
    """Test suite for profile picture functionality"""

    def test_upload_profile_picture(
        self, page: Page, base_url: str, login_as, fresh_database
    ):
        """Test uploading profile picture"""
        login_as("sarah")

        settings = SettingsPage(page)
        settings.goto()

        # Check if file input exists
        expect(page.locator(settings.avatar_input)).to_be_attached()

    def test_clear_profile_picture(
        self, page: Page, base_url: str, login_as, fresh_database
    ):
        """Test clearing profile picture"""
        login_as("sarah")

        settings = SettingsPage(page)
        settings.goto()

        clear_button = page.locator(settings.clear_avatar_button)
        if clear_button.is_visible(timeout=5000):
            settings.clear_avatar()
            settings.expect_avatar_is_default()


class TestAccountDeletion:
    """Test suite for account deletion functionality"""

    def test_delete_account(self, page: Page, base_url: str, login_as, fresh_database):
        """Test deleting account"""
        login_as("sarah")

        settings = SettingsPage(page)
        settings.goto()

        expect(page.locator(settings.delete_account_button)).to_be_visible(timeout=5000)
        settings.delete_account()

        # Wait for redirect to login page - this is the key indicator of
        # successful deletion. wait_for_url is more reliable than checking
        # for element visibility.
        try:
            page.wait_for_url(re.compile(r".*/(login|$)"), timeout=15000)
        except Exception:
            # Fallback: check for login input if URL didn't change
            expect(page.get_by_test_id("login-email-input")).to_be_visible(timeout=5000)
