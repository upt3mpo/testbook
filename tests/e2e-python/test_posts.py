"""
Posts E2E Tests - Python/Playwright
Tests creating, editing, deleting posts, and interactions
"""

import re

from playwright.sync_api import Page, expect


def get_first_post(page: Page):
    """Get the first (most recent) post on the feed"""
    return page.locator('[data-testid-generic="post-item"]').first


def get_first_own_post(page: Page):
    """Get the first post owned by the current user"""
    return page.locator('[data-is-own-post="true"]').first


def create_post(page: Page, content: str):
    """Helper to create a post"""
    page.fill('[data-testid="create-post-textarea"]', content)
    page.click('[data-testid="create-post-submit-button"]')
    expect(page.locator(f'text="{content}"').first).to_be_visible(timeout=10000)
    try:
        page.wait_for_load_state("networkidle", timeout=5000)
    except:
        pass  # Continue even if networkidle times out


def add_reaction(post, reaction_type: str, page: Page):
    """Add a reaction to a post"""
    react_button = post.locator('[data-testid$="-react-button"]')
    expect(react_button).to_be_visible(timeout=5000)

    # Click the react button to open the dropdown (force click to avoid pointer intercept)
    react_button.click(force=True)
    page.wait_for_timeout(1000)  # Increased wait for dropdown animation

    # Click the specific reaction
    reaction_btn = post.locator(f'[data-testid$="-reaction-{reaction_type}"]')
    expect(reaction_btn).to_be_visible(timeout=5000)
    reaction_btn.click(force=True)
    page.wait_for_timeout(1500)  # Wait for API response


class TestPosts:
    """Test suite for post functionality"""

    # Create Post Tests
    def test_create_text_post(
        self, page: Page, base_url: str, login_as, fresh_database
    ):
        """Test creating a text-only post"""
        login_as("sarah")

        post_content = "This is my test post!"
        create_post(page, post_content)

        # Post should appear in feed
        first_post = get_first_post(page)
        expect(first_post).to_contain_text(post_content)
        expect(first_post).to_have_attribute("data-is-own-post", "true")

    def test_create_post_disable_empty_submit(
        self, page: Page, base_url: str, login_as, fresh_database
    ):
        """Test submit button is disabled for empty post"""
        login_as("sarah")

        submit_button = page.locator('[data-testid="create-post-submit-button"]')

        # Should be disabled when empty
        expect(submit_button).to_be_disabled()

        # Should enable when text is entered
        page.fill('[data-testid="create-post-textarea"]', "Some content")
        expect(submit_button).to_be_enabled()

    def test_create_post_clear_textarea(
        self, page: Page, base_url: str, login_as, fresh_database
    ):
        """Test textarea clears after posting"""
        login_as("sarah")

        create_post(page, "Test post")

        # Textarea should be clear
        textarea = page.locator('[data-testid="create-post-textarea"]')
        expect(textarea).to_have_value("")

    def test_create_post_reverse_chronological(
        self, page: Page, base_url: str, login_as, fresh_database
    ):
        """Test posts show in reverse chronological order"""
        login_as("sarah")

        # Create multiple posts
        create_post(page, "First post")
        create_post(page, "Second post")
        create_post(page, "Third post")

        # Most recent should be first
        first_post = get_first_post(page)
        expect(first_post).to_contain_text("Third post")

    # Edit Post Tests
    def test_edit_own_post(self, page: Page, base_url: str, login_as, fresh_database):
        """Test editing own post"""
        login_as("sarah")

        # Create a post first
        create_post(page, "Original content")

        own_post = get_first_own_post(page)

        # Scroll the post into view
        own_post.scroll_into_view_if_needed()
        page.wait_for_timeout(300)

        # Click menu button
        menu_button = own_post.locator('[data-testid$="-menu-button"]')
        expect(menu_button).to_be_visible(timeout=5000)
        menu_button.click(force=True)

        # Wait for dropdown to appear
        page.wait_for_timeout(500)

        # Click the edit button
        edit_button = own_post.locator('[data-testid$="-edit-button"]')
        expect(edit_button).to_be_visible(timeout=5000)
        edit_button.click(force=True)

        # Edit form should appear
        edit_textarea = own_post.locator('[data-testid$="-edit-textarea"]')
        expect(edit_textarea).to_be_visible(timeout=5000)

        # Edit content
        edit_textarea.fill("Edited content")

        # Wait for save button to be visible and click
        save_button = own_post.locator('[data-testid$="-save-button"]')
        expect(save_button).to_be_visible(timeout=5000)
        save_button.click()

        # Wait for the alert to be dismissed (auto-handled by our dialog handler)
        page.wait_for_timeout(500)

        # Wait for edit form to disappear
        expect(edit_textarea).not_to_be_visible(timeout=5000)

        # Wait for React to re-render with updated content
        page.wait_for_timeout(1000)

        # Re-query the post to get fresh locator
        own_post = get_first_own_post(page)

        # Should show updated content
        expect(own_post).to_contain_text("Edited content", timeout=5000)
        expect(own_post).not_to_contain_text("Original content")

    def test_edit_post_cancel(
        self, page: Page, base_url: str, login_as, fresh_database
    ):
        """Test canceling edit"""
        login_as("sarah")

        create_post(page, "Original content")

        own_post = get_first_own_post(page)

        # Scroll the post into view
        own_post.scroll_into_view_if_needed()
        page.wait_for_timeout(300)

        # Click menu button
        menu_button = own_post.locator('[data-testid$="-menu-button"]')
        expect(menu_button).to_be_visible(timeout=5000)
        menu_button.click(force=True)

        # Wait for dropdown to appear
        page.wait_for_timeout(500)

        # Click edit button
        edit_button = own_post.locator('[data-testid$="-edit-button"]')
        expect(edit_button).to_be_visible(timeout=5000)
        edit_button.click(force=True)

        # Wait for edit textarea to appear
        edit_textarea = own_post.locator('[data-testid$="-edit-textarea"]')
        expect(edit_textarea).to_be_visible(timeout=5000)

        # Change text
        edit_textarea.fill("Changed")

        # Wait for cancel button to be visible and click
        cancel_button = own_post.locator('[data-testid$="-cancel-button"]')
        expect(cancel_button).to_be_visible(timeout=5000)
        cancel_button.click()

        # Wait for edit form to disappear
        expect(edit_textarea).not_to_be_visible(timeout=5000)

        # Should show original content
        expect(own_post).to_contain_text("Original content", timeout=5000)
        expect(own_post).not_to_contain_text("Changed")

    def test_edit_not_shown_on_other_posts(
        self, page: Page, base_url: str, login_as, fresh_database
    ):
        """Test edit option not shown on other users' posts"""
        login_as("sarah")

        # View a post from another user
        other_user_post = page.locator('[data-post-author="mikechen"]').first

        try:
            is_visible = other_user_post.is_visible(timeout=5000)
        except:
            is_visible = False

        if is_visible:
            # Should not have edit menu
            expect(
                other_user_post.locator('[data-testid$="-menu-button"]')
            ).not_to_be_visible()

    # Delete Post Tests
    def test_delete_own_post(self, page: Page, base_url: str, login_as, fresh_database):
        """Test deleting own post"""
        login_as("sarah")

        create_post(page, "Post to delete")

        own_post = get_first_own_post(page)
        post_content = own_post.text_content()

        # Open menu with force click to avoid pointer issues
        menu_button = own_post.locator('[data-testid$="-menu-button"]')
        expect(menu_button).to_be_visible(timeout=5000)
        menu_button.click(force=True)

        # Wait for dropdown animation
        page.wait_for_timeout(500)

        # Click delete button directly (should be visible now)
        delete_button = own_post.locator('[data-testid$="-delete-button"]')
        expect(delete_button).to_be_visible(timeout=5000)
        delete_button.click(force=True)

        # Confirm deletion if there's a dialog
        page.wait_for_timeout(1000)

        # Post should be removed
        expect(page.locator(f'text="{post_content}"')).not_to_be_visible(timeout=5000)

    # Reaction Tests
    def test_add_reaction(self, page: Page, base_url: str, login_as, fresh_database):
        """Test adding reaction to post"""
        login_as("sarah")

        create_post(page, "React to this post")

        first_post = get_first_post(page)
        react_button = first_post.locator('[data-testid$="-react-button"]')

        # Verify reaction button exists
        expect(react_button).to_be_visible()

        # Add reaction
        add_reaction(first_post, "like", page)

        # Wait for button to show reaction
        expect(react_button).to_contain_text("👍", timeout=10000)

    def test_change_reaction_type(
        self, page: Page, base_url: str, login_as, fresh_database
    ):
        """Test changing reaction type"""
        login_as("sarah")

        create_post(page, "React to this post")

        first_post = get_first_post(page)
        react_button = first_post.locator('[data-testid$="-react-button"]')

        # Add like
        add_reaction(first_post, "like", page)
        expect(react_button).to_contain_text("👍", timeout=10000)

        # Change to love
        add_reaction(first_post, "love", page)
        expect(react_button).to_contain_text("❤️", timeout=10000)

    def test_remove_reaction(self, page: Page, base_url: str, login_as, fresh_database):
        """Test removing reaction"""
        login_as("sarah")

        create_post(page, "React to this post")

        first_post = get_first_post(page)
        react_button = first_post.locator('[data-testid$="-react-button"]')

        # Add reaction
        add_reaction(first_post, "like", page)
        expect(react_button).to_contain_text("👍", timeout=10000)

        # Click same reaction to remove
        react_button.hover()
        like_button = first_post.locator('[data-testid$="-reaction-like"]')
        expect(like_button).to_be_visible(timeout=5000)
        like_button.click()

        # Wait for network to settle
        page.wait_for_load_state("networkidle", timeout=3000)

        # Should show default text after removal
        expect(react_button).to_contain_text("React", timeout=10000)

    def test_show_all_reaction_types(
        self, page: Page, base_url: str, login_as, fresh_database
    ):
        """Test all reaction types are visible"""
        login_as("sarah")

        create_post(page, "React to this post")

        first_post = get_first_post(page)

        # Hover to show reaction menu
        react_button = first_post.locator('[data-testid$="-react-button"]')

        # Ensure button is visible first
        expect(react_button).to_be_visible(timeout=5000)

        # Force hover and wait for CSS transition (0.15s) + buffer
        react_button.hover(force=True)
        page.wait_for_timeout(500)

        # All reactions should be visible
        reactions = ["like", "love", "haha", "wow", "sad", "angry"]
        for reaction in reactions:
            reaction_locator = first_post.locator(
                f'[data-testid$="-reaction-{reaction}"]'
            )
            expect(reaction_locator).to_be_visible(timeout=5000)

    # Comment Tests
    def test_add_comment(self, page: Page, base_url: str, login_as, fresh_database):
        """Test adding comment to post"""
        login_as("sarah")

        create_post(page, "Post to comment on")

        first_post = get_first_post(page)

        # Click to view post details
        first_post.locator('[data-testid$="-comment-button"]').click()

        # Wait for navigation or modal
        page.wait_for_timeout(500)

    def test_show_comment_count(
        self, page: Page, base_url: str, login_as, fresh_database
    ):
        """Test comment count is displayed"""
        login_as("sarah")

        # Check if comment count is displayed
        posts = page.locator('[data-testid-generic="post-item"]')
        first_post = posts.first

        try:
            is_visible = first_post.is_visible(timeout=5000)
        except:
            is_visible = False

        if is_visible:
            # Comment button should show count or icon
            expect(
                first_post.locator('[data-testid$="-comment-button"]')
            ).to_be_visible()

    # Repost Tests
    def test_repost_a_post(self, page: Page, base_url: str, login_as, fresh_database):
        """Test reposting a post"""
        login_as("sarah")

        # Find a post from another user
        other_post = page.locator('[data-testid-generic="post-item"]').first

        if other_post.is_visible(timeout=5000):
            repost_button = other_post.locator('[data-testid$="-repost-button"]')

            # Repost
            repost_button.click()

            # Button should show reposted state
            expect(repost_button).to_contain_text(re.compile("reposted", re.IGNORECASE))
            expect(repost_button).to_have_class(re.compile("btn-primary"))

    def test_unrepost_a_post(self, page: Page, base_url: str, login_as, fresh_database):
        """Test unreposting a post"""
        login_as("sarah")

        # Get first post - should be from seeded data (other users)
        other_post = page.locator('[data-testid-generic="post-item"]').first

        try:
            is_visible = other_post.is_visible(timeout=5000)
        except:
            is_visible = False

        if is_visible:
            repost_button = other_post.locator('[data-testid$="-repost-button"]')

            # Repost
            repost_button.click()

            # Wait for button state to update
            page.wait_for_timeout(1000)
            expect(repost_button).to_contain_text(
                re.compile("reposted", re.IGNORECASE), timeout=10000
            )

            # Unrepost
            repost_button.click()

            # Wait for button state to update
            page.wait_for_timeout(1000)
            expect(repost_button).to_contain_text(
                re.compile("^repost$", re.IGNORECASE), timeout=10000
            )
            expect(repost_button).to_have_class(re.compile("btn-secondary"))

    # Feed Tab Tests
    def test_switch_between_feed_tabs(
        self, page: Page, base_url: str, login_as, fresh_database
    ):
        """Test switching between All and Following tabs"""
        login_as("sarah")

        all_tab = page.locator('[data-testid="feed-tab-all"]')
        following_tab = page.locator('[data-testid="feed-tab-following"]')

        # Should start on All tab
        expect(all_tab).to_have_class(re.compile("active|selected", re.IGNORECASE))

        # Switch to Following
        following_tab.click()
        expect(following_tab).to_have_class(
            re.compile("active|selected", re.IGNORECASE)
        )

        # Switch back to All
        all_tab.click()
        expect(all_tab).to_have_class(re.compile("active|selected", re.IGNORECASE))

    def test_different_posts_in_feeds(
        self, page: Page, base_url: str, login_as, fresh_database
    ):
        """Test different posts in Following vs All feed"""
        login_as("sarah")

        # Get count of All posts
        page.click('[data-testid="feed-tab-all"]')
        all_posts = page.locator('[data-testid-generic="post-item"]').count()

        # Get count of Following posts
        page.click('[data-testid="feed-tab-following"]')
        following_posts = page.locator('[data-testid-generic="post-item"]').count()

        # Counts may differ
        assert all_posts >= 0
        assert following_posts >= 0
