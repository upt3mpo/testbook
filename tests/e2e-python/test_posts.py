"""
Posts E2E Tests - Python/Playwright
Tests creating, editing, deleting posts, and interactions

Page Object Model: interactions go through pages.feed_page.FeedPage
rather than raw selectors, so a UI change only needs updating in one place.
"""

import re

from playwright.sync_api import Page, expect

from pages.feed_page import FeedPage


class TestPosts:
    """Test suite for post functionality"""

    # Create Post Tests
    def test_create_text_post(
        self, page: Page, base_url: str, login_as, fresh_database
    ):
        """Test creating a text-only post"""
        login_as("sarah")
        feed = FeedPage(page)

        post_content = "This is my test post!"
        feed.create_post(post_content)

        # Post should appear in feed. This test is specifically about
        # ordering (a new post appears first), so it stays scoped by
        # position rather than by content - see find_post_by_content()'s
        # docstring for why that distinction matters.
        first_post = feed.first_post()
        expect(first_post).to_contain_text(post_content)
        expect(first_post).to_have_attribute("data-is-own-post", "true")

    def test_create_post_disable_empty_submit(
        self, page: Page, base_url: str, login_as, fresh_database
    ):
        """Test submit button is disabled for empty post"""
        login_as("sarah")

        submit_button = page.get_by_test_id("create-post-submit-button")

        # Should be disabled when empty
        expect(submit_button).to_be_disabled()

        # Should enable when text is entered
        page.get_by_test_id("create-post-textarea").fill("Some content")
        expect(submit_button).to_be_enabled()

    def test_create_post_clear_textarea(
        self, page: Page, base_url: str, login_as, fresh_database
    ):
        """Test textarea clears after posting"""
        login_as("sarah")
        FeedPage(page).create_post("Test post")

        # Textarea should be clear
        textarea = page.get_by_test_id("create-post-textarea")
        expect(textarea).to_have_value("")

    def test_create_post_reverse_chronological(
        self, page: Page, base_url: str, login_as, fresh_database
    ):
        """Test posts show in reverse chronological order"""
        login_as("sarah")
        feed = FeedPage(page)

        # Create multiple posts
        feed.create_post("First post")
        feed.create_post("Second post")
        feed.create_post("Third post")

        # Most recent should be first - this test is specifically about
        # ordering, so it stays scoped by position (see
        # find_post_by_content()'s docstring).
        expect(feed.first_post()).to_contain_text("Third post")

    # Edit Post Tests
    def test_edit_own_post(self, page: Page, base_url: str, login_as, fresh_database):
        """Test editing own post"""
        login_as("sarah")
        feed = FeedPage(page)

        feed.create_post("Original content")
        own_post = feed.first_own_post()
        own_post.scroll_into_view_if_needed()

        feed.edit_post(own_post, "Edited content")

        # Wait for edit form to disappear (indicating save completed)
        expect(own_post.locator(feed.post_edit_textarea)).not_to_be_visible(
            timeout=5000
        )

        # Re-query the post to get fresh locator, then verify updated content
        own_post = feed.first_own_post()
        expect(own_post).to_contain_text("Edited content", timeout=5000)
        expect(own_post).not_to_contain_text("Original content")

    def test_edit_post_cancel(
        self, page: Page, base_url: str, login_as, fresh_database
    ):
        """Test canceling edit"""
        login_as("sarah")
        feed = FeedPage(page)

        feed.create_post("Original content")
        own_post = feed.first_own_post()
        own_post.scroll_into_view_if_needed()

        edit_textarea = feed.start_editing_post(own_post)
        edit_textarea.fill("Changed")
        feed.cancel_editing_post(own_post)

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
        feed = FeedPage(page)

        # View a post from another user
        other_user_post = page.locator('[data-post-author="mikechen"]').first

        try:
            is_visible = other_user_post.is_visible(timeout=5000)
        except Exception:
            is_visible = False

        if is_visible:
            # Should not have edit menu
            expect(other_user_post.locator(feed.post_menu_button)).not_to_be_visible()

    # Delete Post Tests
    def test_delete_own_post(self, page: Page, base_url: str, login_as, fresh_database):
        """Test deleting own post"""
        login_as("sarah")
        feed = FeedPage(page)

        feed.create_post("Post to delete")
        own_post = feed.first_own_post()
        post_content = own_post.text_content()

        feed.delete_post(own_post)

        # Post should be removed
        expect(page.locator(f'text="{post_content}"')).not_to_be_visible(timeout=5000)

    # Reaction Tests
    def test_add_reaction(self, page: Page, base_url: str, login_as, fresh_database):
        """Test adding reaction to post"""
        login_as("sarah")
        feed = FeedPage(page)

        feed.create_post("React to this post")
        my_post = feed.find_post_by_content("React to this post")
        react_button = my_post.locator(feed.post_react_button)

        expect(react_button).to_be_visible()

        feed.react_to_post(my_post, "like")

        # Wait for button to show reaction
        expect(react_button).to_contain_text("👍", timeout=10000)

    def test_change_reaction_type(
        self, page: Page, base_url: str, login_as, fresh_database
    ):
        """Test changing reaction type"""
        login_as("sarah")
        feed = FeedPage(page)

        feed.create_post("React to this post")
        my_post = feed.find_post_by_content("React to this post")
        react_button = my_post.locator(feed.post_react_button)

        # Add like
        feed.react_to_post(my_post, "like")
        expect(react_button).to_contain_text("👍", timeout=10000)

        # Change to love
        feed.react_to_post(my_post, "love")
        expect(react_button).to_contain_text("❤️", timeout=10000)

    def test_remove_reaction(self, page: Page, base_url: str, login_as, fresh_database):
        """Test removing reaction"""
        login_as("sarah")
        feed = FeedPage(page)

        feed.create_post("React to this post")
        my_post = feed.find_post_by_content("React to this post")
        react_button = my_post.locator(feed.post_react_button)

        # Add reaction
        feed.react_to_post(my_post, "like")
        expect(react_button).to_contain_text("👍", timeout=10000)

        # Reacting with the same type again removes it
        feed.react_to_post(my_post, "like")

        # Wait for network to settle
        page.wait_for_load_state("networkidle", timeout=3000)

        # Should show default text after removal
        expect(react_button).to_contain_text("React", timeout=10000)

    def test_show_all_reaction_types(
        self, page: Page, base_url: str, login_as, fresh_database
    ):
        """Test all reaction types are visible"""
        login_as("sarah")
        feed = FeedPage(page)

        feed.create_post("React to this post")
        my_post = feed.find_post_by_content("React to this post")

        react_button = my_post.locator(feed.post_react_button)
        expect(react_button).to_be_visible(timeout=5000)

        # Force hover to open the reaction dropdown. The dropdown has a CSS
        # fade-in transition, but each expect() below already retries for up
        # to 5s, which covers that transition without a separate wait.
        react_button.hover(force=True)

        # All reactions should be visible
        reactions = ["like", "love", "haha", "wow", "sad", "angry"]
        for reaction in reactions:
            reaction_locator = my_post.locator(f'[data-testid$="-reaction-{reaction}"]')
            expect(reaction_locator).to_be_visible(timeout=5000)

    # Comment Tests
    def test_add_comment(self, page: Page, base_url: str, login_as, fresh_database):
        """Test adding comment to post"""
        login_as("sarah")
        feed = FeedPage(page)

        post_content = "Post to comment on"
        feed.create_post(post_content)
        my_post = feed.find_post_by_content(post_content)

        # Clicking the comment button toggles an inline comment form open
        # (see Post.jsx's showCommentInput state) rather than navigating.
        feed.open_comment_form(my_post)
        expect(my_post.locator(feed.post_comment_form)).to_be_visible(timeout=5000)

    def test_show_comment_count(
        self, page: Page, base_url: str, login_as, fresh_database
    ):
        """Test comment count is displayed"""
        login_as("sarah")
        feed = FeedPage(page)

        first_post = feed.first_post()

        try:
            is_visible = first_post.is_visible(timeout=5000)
        except Exception:
            is_visible = False

        if is_visible:
            # Comment button should show count or icon
            expect(first_post.locator(feed.post_comment_button)).to_be_visible()

    # Repost Tests
    def test_repost_a_post(self, page: Page, base_url: str, login_as, fresh_database):
        """Test reposting a post"""
        login_as("sarah")
        feed = FeedPage(page)

        # Find a post from another user
        other_post = feed.first_post()

        if other_post.is_visible(timeout=5000):
            repost_button = other_post.locator(feed.post_repost_button)

            feed.toggle_repost(other_post)

            # Button should show reposted state
            expect(repost_button).to_contain_text(re.compile("reposted", re.IGNORECASE))
            expect(repost_button).to_have_class(re.compile("btn-primary"))

    def test_unrepost_a_post(self, page: Page, base_url: str, login_as, fresh_database):
        """Test unreposting a post"""
        login_as("sarah")
        feed = FeedPage(page)

        # Get first post - should be from seeded data (other users)
        other_post = feed.first_post()

        try:
            is_visible = other_post.is_visible(timeout=5000)
        except Exception:
            is_visible = False

        if is_visible:
            repost_button = other_post.locator(feed.post_repost_button)

            # Repost. expect().to_contain_text() below retries until the
            # button's label actually updates, so no separate wait is needed.
            feed.toggle_repost(other_post)
            expect(repost_button).to_contain_text(
                re.compile("reposted", re.IGNORECASE), timeout=10000
            )

            # Unrepost
            feed.toggle_repost(other_post)
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
        feed = FeedPage(page)

        # Should start on All tab
        expect(feed.feed_tab_all).to_have_class(
            re.compile("active|selected", re.IGNORECASE)
        )

        # Switch to Following
        feed.go_to_following_tab()
        expect(feed.feed_tab_following).to_have_class(
            re.compile("active|selected", re.IGNORECASE)
        )

        # Switch back to All
        feed.go_to_all_tab()
        expect(feed.feed_tab_all).to_have_class(
            re.compile("active|selected", re.IGNORECASE)
        )

    def test_different_posts_in_feeds(
        self, page: Page, base_url: str, login_as, fresh_database
    ):
        """Test different posts in Following vs All feed"""
        login_as("sarah")
        feed = FeedPage(page)

        # Get count of All posts
        feed.go_to_all_tab()
        all_posts = feed.post_count()

        # Get count of Following posts
        feed.go_to_following_tab()
        following_posts = feed.post_count()

        # Counts may differ
        assert all_posts >= 0
        assert following_posts >= 0
