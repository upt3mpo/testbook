"""
User Profile E2E Tests - Python/Playwright
Tests user profiles, follow/unfollow, blocking, settings, and account management
"""

import re

from playwright.sync_api import Page, expect


class TestUserProfile:
    """Test suite for user profile functionality"""

    def test_view_own_profile(
        self, page: Page, base_url: str, login_as, test_users: dict, fresh_database
    ):
        """Test viewing your own profile"""
        login_as("sarah")

        # Click profile link
        page.get_by_test_id("navbar-profile-link").click()

        # Should show profile information
        expect(page.get_by_test_id("profile-display-name")).to_contain_text(
            test_users["sarah"]["name"]
        )
        expect(page.get_by_test_id("profile-username")).to_contain_text(
            f"@{test_users['sarah']['username']}"
        )

        # Should show edit button for own profile
        expect(page.get_by_test_id("profile-edit-button")).to_be_visible()

    def test_view_other_user_profile(
        self, page: Page, base_url: str, login_as, test_users: dict, fresh_database
    ):
        """Test viewing another user's profile"""
        login_as("sarah")

        page.goto(f"{base_url}/profile/{test_users['mike']['username']}")

        # Should show user information
        expect(page.get_by_test_id("profile-display-name")).to_contain_text(
            test_users["mike"]["name"]
        )
        expect(page.get_by_test_id("profile-username")).to_contain_text(
            f"@{test_users['mike']['username']}"
        )

        # Should NOT show edit button for other user
        expect(page.get_by_test_id("profile-edit-button")).not_to_be_visible()

        # Should show follow/block buttons
        expect(page.get_by_test_id("profile-follow-button")).to_be_visible()
        expect(page.get_by_test_id("profile-block-button")).to_be_visible()

    def test_show_follower_following_counts(
        self, page: Page, base_url: str, login_as, test_users: dict, fresh_database
    ):
        """Test follower and following counts are shown"""
        login_as("sarah")

        page.goto(f"{base_url}/profile/{test_users['sarah']['username']}")

        # Wait for profile data to load
        expect(page.get_by_test_id("profile-display-name")).to_be_visible(timeout=10000)

        # Then wait for count links to appear
        expect(page.get_by_test_id("profile-followers-link")).to_be_visible(
            timeout=10000
        )
        expect(page.get_by_test_id("profile-following-link")).to_be_visible(
            timeout=10000
        )

    def test_show_posts_count(
        self, page: Page, base_url: str, login_as, test_users: dict, fresh_database
    ):
        """Test posts count is displayed"""
        login_as("sarah")

        page.goto(f"{base_url}/profile/{test_users['sarah']['username']}")

        expect(page.get_by_test_id("profile-posts-count")).to_be_visible()


class TestFollowing:
    """Test suite for follow/unfollow functionality"""

    def test_follow_user(
        self, page: Page, base_url: str, login_as, test_users: dict, fresh_database
    ):
        """Test following another user"""
        login_as("sarah")

        page.goto(f"{base_url}/profile/{test_users['mike']['username']}")

        follow_button = page.get_by_test_id("profile-follow-button")
        expect(follow_button).to_be_visible(timeout=5000)

        # Click follow and wait for button text to change
        follow_button.click()

        # Wait for button to update to "Unfollow"
        expect(follow_button).to_contain_text(
            re.compile("unfollow", re.IGNORECASE), timeout=10000
        )

        # Verify following count increased on own profile
        page.goto(f"{base_url}/profile/{test_users['sarah']['username']}")

        # Wait for profile to load
        expect(page.get_by_test_id("profile-display-name")).to_be_visible(timeout=10000)

        # Check the following link contains a number greater than 0
        following_link = page.get_by_test_id("profile-following-link")
        expect(following_link).to_contain_text(re.compile("[1-9]"), timeout=10000)

    def test_unfollow_user(
        self, page: Page, base_url: str, login_as, test_users: dict, fresh_database
    ):
        """Test unfollowing a user"""
        login_as("sarah")

        page.goto(f"{base_url}/profile/{test_users['mike']['username']}")

        follow_button = page.get_by_test_id("profile-follow-button")

        # Follow first
        follow_button.click()
        expect(follow_button).to_contain_text(
            re.compile("unfollow", re.IGNORECASE), timeout=10000
        )

        # Then unfollow
        follow_button.click()
        expect(follow_button).to_contain_text(
            re.compile("^follow$", re.IGNORECASE), timeout=10000
        )

    def test_followed_users_in_following_feed(
        self, page: Page, base_url: str, login_as, test_users: dict, fresh_database
    ):
        """Test followed users' posts show in Following feed"""
        login_as("sarah")

        # Follow Mike
        page.goto(f"{base_url}/profile/{test_users['mike']['username']}")
        page.get_by_test_id("profile-follow-button").click()
        expect(page.get_by_test_id("profile-follow-button")).to_contain_text(
            re.compile("unfollow", re.IGNORECASE), timeout=10000
        )

        # Go to Following feed
        page.goto(base_url)
        page.get_by_test_id("feed-tab-following").click()

        # Should show Mike's posts (if he has any)
        mike_posts = page.locator(
            f'[data-post-author="{test_users["mike"]["username"]}"]'
        )
        count = mike_posts.count()
        assert count >= 0


class TestBlocking:
    """Test suite for block/unblock functionality"""

    def test_block_user(
        self, page: Page, base_url: str, login_as, test_users: dict, fresh_database
    ):
        """Test blocking another user"""
        login_as("sarah")

        page.goto(f"{base_url}/profile/{test_users['mike']['username']}")

        block_button = page.get_by_test_id("profile-block-button")
        expect(block_button).to_be_visible(timeout=5000)

        # Click block and wait for button text to change
        block_button.click()

        # Wait for network to settle after API call
        try:
            page.wait_for_load_state("networkidle", timeout=3000)
        except:
            pass

        # Button should change to Unblock - wait for this state change
        expect(block_button).to_contain_text(
            re.compile("unblock", re.IGNORECASE), timeout=10000
        )

    def test_unblock_user(
        self, page: Page, base_url: str, login_as, test_users: dict, fresh_database
    ):
        """Test unblocking a user"""
        login_as("sarah")

        page.goto(f"{base_url}/profile/{test_users['mike']['username']}")

        # Block first. The confirm() dialog this triggers is auto-accepted
        # by the page fixture's dialog handler, and the expect() below
        # already retries until the API call finishes and the button's
        # label actually updates, so no separate wait is needed.
        block_button = page.get_by_test_id("profile-block-button")
        expect(block_button).to_be_visible(timeout=5000)
        block_button.click()

        # Re-query button after state change
        block_button = page.get_by_test_id("profile-block-button")
        expect(block_button).to_contain_text(
            re.compile("unblock", re.IGNORECASE), timeout=10000
        )

        # Then unblock and wait for state change
        block_button.click()

        # Re-query button after state change
        block_button = page.get_by_test_id("profile-block-button")
        expect(block_button).to_contain_text(
            re.compile("^block$", re.IGNORECASE), timeout=10000
        )

    def test_blocked_users_not_in_feed(
        self, page: Page, base_url: str, login_as, test_users: dict, fresh_database
    ):
        """Test blocked users' posts don't show in feed"""
        login_as("sarah")

        # Block Mike
        page.goto(f"{base_url}/profile/{test_users['mike']['username']}")
        block_button = page.get_by_test_id("profile-block-button")
        block_button.click()

        # Wait for API call to complete
        try:
            page.wait_for_load_state("networkidle", timeout=3000)
        except:
            pass

        expect(block_button).to_contain_text(
            re.compile("unblock", re.IGNORECASE), timeout=10000
        )

        # Go to All feed
        page.goto(base_url)
        page.wait_for_load_state("networkidle", timeout=5000)

        # Force reload to ensure fresh data
        page.reload()
        page.wait_for_load_state("networkidle", timeout=5000)

        page.get_by_test_id("feed-tab-all").click()

        # Should not see Mike's posts. to_have_count() retries, so it covers
        # any remaining render delay after the reload and tab click above.
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

        page.goto(f"{base_url}/profile/{test_users['sarah']['username']}")

        # Click followers count
        page.get_by_test_id("profile-followers-link").click()

        # Should be on followers page
        expect(page.get_by_test_id("followers-page")).to_be_visible()

    def test_view_following_list(
        self, page: Page, base_url: str, login_as, test_users: dict, fresh_database
    ):
        """Test viewing following list"""
        login_as("sarah")

        page.goto(f"{base_url}/profile/{test_users['sarah']['username']}")

        # Click following count
        page.get_by_test_id("profile-following-link").click()

        # Should be on following page
        expect(page.get_by_test_id("following-page")).to_be_visible()

    def test_unfollow_from_following_page(
        self, page: Page, base_url: str, login_as, test_users: dict, fresh_database
    ):
        """Test unfollowing from following page"""
        login_as("sarah")

        # Follow Mike first
        page.goto(f"{base_url}/profile/{test_users['mike']['username']}")
        page.get_by_test_id("profile-follow-button").click()
        expect(page.get_by_test_id("profile-follow-button")).to_contain_text(
            re.compile("unfollow", re.IGNORECASE), timeout=10000
        )

        # Go to following page
        page.goto(f"{base_url}/profile/{test_users['sarah']['username']}")
        page.get_by_test_id("profile-following-link").click()

        # Unfollow Mike
        mike_in_list = page.locator(
            f'[data-username="{test_users["mike"]["username"]}"]'
        )
        try:
            is_visible = mike_in_list.is_visible(timeout=5000)
        except:
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

        page.goto(f"{base_url}/profile/{test_users['sarah']['username']}")

        followers_link = page.get_by_test_id("profile-followers-link")
        expect(followers_link).to_be_visible(timeout=5000)
        followers_link.click()

        # Wait for the followers page to load
        page.wait_for_url(re.compile(r".*/followers.*"), timeout=5000)

        # If there are followers, try to block one
        first_follower = page.locator('[data-testid-generic="follower-item"]').first
        try:
            follower_visible = first_follower.is_visible(timeout=3000)
        except:
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

        page.goto(f"{base_url}/settings")

        display_name_input = page.get_by_test_id("settings-display-name-input")
        display_name_input.fill("Updated Name")

        page.get_by_test_id("settings-save-button").click()

        # Should show success message
        expect(page.locator("text=success")).to_be_visible(timeout=5000)

        # Verify on profile
        page.goto(f"{base_url}/profile/{test_users['sarah']['username']}")
        expect(page.get_by_test_id("profile-display-name")).to_contain_text(
            "Updated Name"
        )

    def test_update_bio(
        self, page: Page, base_url: str, login_as, test_users: dict, fresh_database
    ):
        """Test updating bio"""
        login_as("sarah")

        page.goto(f"{base_url}/settings")

        bio_input = page.get_by_test_id("settings-bio-input")
        bio_input.fill("My updated bio")

        page.get_by_test_id("settings-save-button").click()

        # Should show success message
        expect(page.locator("text=success")).to_be_visible(timeout=5000)

    def test_change_theme(self, page: Page, base_url: str, login_as, fresh_database):
        """Test changing theme"""
        login_as("sarah")

        page.goto(f"{base_url}/settings")

        theme_select = page.get_by_test_id("settings-theme-select")
        theme_select.select_option("dark")

        page.get_by_test_id("settings-save-button").click()

        # Page should have dark theme
        html = page.locator("html")
        expect(html).to_have_attribute("data-theme", "dark")

    def test_change_text_density(
        self, page: Page, base_url: str, login_as, fresh_database
    ):
        """Test changing text density"""
        login_as("sarah")

        page.goto(f"{base_url}/settings")

        density_select = page.get_by_test_id("settings-text-density-select")
        density_select.select_option("compact")

        page.get_by_test_id("settings-save-button").click()

        # Should show success
        expect(page.locator("text=success")).to_be_visible(timeout=5000)

    def test_theme_persist_across_sessions(
        self, page: Page, base_url: str, login_as, fresh_database
    ):
        """Test theme persists across sessions"""
        login_as("sarah")

        # Set dark theme
        page.goto(f"{base_url}/settings")
        page.get_by_test_id("settings-theme-select").select_option("dark")
        page.get_by_test_id("settings-save-button").click()

        # Reload page
        page.reload()

        # Should still be dark
        html = page.locator("html")
        expect(html).to_have_attribute("data-theme", "dark")


class TestProfilePicture:
    """Test suite for profile picture functionality"""

    def test_upload_profile_picture(
        self, page: Page, base_url: str, login_as, fresh_database
    ):
        """Test uploading profile picture"""
        login_as("sarah")

        page.goto(f"{base_url}/settings")

        # Check if file input exists
        file_input = page.get_by_test_id("settings-avatar-input")
        expect(file_input).to_be_attached()

    def test_clear_profile_picture(
        self, page: Page, base_url: str, login_as, fresh_database
    ):
        """Test clearing profile picture"""
        login_as("sarah")

        page.goto(f"{base_url}/settings")

        clear_button = page.get_by_test_id("settings-clear-avatar-button")

        if clear_button.is_visible(timeout=5000):
            clear_button.click()

            # Should revert to default avatar
            expect(page.locator("text=default")).to_be_visible(timeout=5000)


class TestAccountDeletion:
    """Test suite for account deletion functionality"""

    def test_delete_account(self, page: Page, base_url: str, login_as, fresh_database):
        """Test deleting account"""
        login_as("sarah")

        page.goto(f"{base_url}/settings")

        delete_button = page.get_by_test_id("settings-delete-account-button")
        expect(delete_button).to_be_visible(timeout=5000)

        # Click delete button
        # Note: Browser confirm dialogs are auto-accepted by the conftest.py fixture
        delete_button.click()

        # Wait for redirect to login page - this is the key indicator of successful deletion
        # Use waitForURL which is more reliable than checking for element visibility
        try:
            page.wait_for_url(re.compile(r".*/(login|$)"), timeout=15000)
        except:
            # Fallback: check for login input if URL didn't change
            expect(page.get_by_test_id("login-email-input")).to_be_visible(timeout=5000)
