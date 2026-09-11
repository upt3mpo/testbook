"""
Page object for the Feed page.

This file demonstrates the Page Object Model (POM) pattern for E2E testing.
The Page Object Model encapsulates page-specific logic and selectors,
making tests more maintainable and readable.

Key Testing Concepts Demonstrated:
- Page Object Model pattern for maintainable E2E tests
- Centralized selector management
- Reusable page interaction methods
- Async operation handling (waiting for API calls)
- Error handling and fallback strategies
- Test data verification and assertions

This file is referenced in Stage 3 learning materials as an example
of professional Page Object Model implementation.
"""

from playwright.sync_api import Locator, Page, expect

from .base_page import BasePage


class FeedPage(BasePage):
    """
    Reusable helpers for interacting with the feed page.

    This class encapsulates all interactions with the feed page,
    including post creation, viewing, and management. It follows
    the Page Object Model pattern to provide a clean interface
    for tests while hiding the complexity of selectors and timing.

    Key Learning Points:
    - Centralized selector management (change selectors in one place)
    - Reusable methods for common actions (create_post, get_posts)
    - Proper async handling (waiting for API calls, network idle)
    - Error handling and fallback strategies
    - Clear method names that describe user actions
    """

    def __init__(self, page: Page):
        super().__init__(page)

        # Centralized selectors - change here if UI changes
        self.navbar = '[data-testid="navbar"]'
        self.create_post_textarea = '[data-testid="create-post-textarea"]'
        self.create_post_submit = '[data-testid="create-post-submit-button"]'
        self.post_items = '[data-testid-generic="post-item"]'
        self.post_delete_button = '[data-testid$="-delete-button"]'
        self.post_react_button = '[data-testid$="-react-button"]'
        self.post_menu_button = '[data-testid$="-menu-button"]'
        self.post_edit_button = '[data-testid$="-edit-button"]'
        self.post_edit_textarea = '[data-testid$="-edit-textarea"]'
        self.post_save_button = '[data-testid$="-save-button"]'
        self.post_cancel_button = '[data-testid$="-cancel-button"]'
        self.post_comment_button = '[data-testid$="-comment-button"]'
        self.post_comment_form = '[data-testid$="-comment-form"]'
        self.post_repost_button = '[data-testid$="-repost-button"]'
        self.feed_tab_all = page.get_by_test_id("feed-tab-all")
        self.feed_tab_following = page.get_by_test_id("feed-tab-following")

    def goto(self, wait_for_posts: bool = True) -> None:
        """
        Navigate to feed page and wait for it to be ready.

        This method handles the complexity of navigating to the feed
        and ensuring all content is loaded before tests interact with it.

        Args:
            wait_for_posts: If True, wait for posts to load from API (default: True)
        """
        super().goto("/")
        expect(self.page.locator(self.navbar)).to_be_visible(timeout=10000)

        if wait_for_posts:
            # Best-effort wait for the feed's API calls to settle. If this
            # itself times out (a genuinely slow load), callers that need
            # to see posts already use their own retrying assertion
            # (first_post(), post_count(wait_for_load=True), etc.), so
            # nothing here needs a fallback fixed-time wait.
            try:
                self.page.wait_for_load_state("networkidle", timeout=5000)
            except Exception:
                pass

    def create_post(self, content: str) -> None:
        """
        Create a new post and verify it appears.

        This method encapsulates the complete post creation workflow:
        1. Fill in the post content
        2. Submit the post
        3. Wait for the post to appear
        4. Verify the content is correct

        Args:
            content: The text content for the new post
        """
        self.page.fill(self.create_post_textarea, content)
        self.page.click(self.create_post_submit)

        # Verify post appeared. to_contain_text() retries, which already
        # covers the time it takes the API call and re-render to finish -
        # no separate wait is needed before it.
        expect(self.first_post()).to_contain_text(content)

    def first_post(self) -> Locator:
        """Get the first (most recent) post."""
        return self.page.locator(self.post_items).first

    def first_own_post(self) -> Locator:
        """Get the first post owned by the current user."""
        return self.page.locator('[data-is-own-post="true"]').first

    def all_posts(self) -> Locator:
        """Get all posts."""
        return self.page.locator(self.post_items)

    def post_count(self, wait_for_load: bool = False, timeout: int = 5000) -> int:
        """Count visible posts.

        Args:
            wait_for_load: If True, wait for at least one post to appear before counting
            timeout: Maximum time to wait for posts (milliseconds)

        Returns:
            Number of visible posts
        """
        if wait_for_load:
            try:
                # Wait for at least one post to appear
                expect(self.all_posts().first).to_be_visible(timeout=timeout)
            except:
                # No posts found within timeout, return 0
                pass

        return self.all_posts().count()

    def find_post_by_content(self, content: str) -> Locator:
        """Find a specific post by its content.

        Prefer this over first_post()/first_own_post() whenever a test just
        created the post it's about to interact with: the feed sorts by
        created_at, and one seeded demo post is deliberately timestamped at
        "now" (days_ago: 0 in backend/seed.py) - close enough to a
        freshly-created post's timestamp that which one sorts first is a
        genuine race, not a fixed order. Filtering by content sidesteps
        that race. Only use first_post()/first_own_post() when a test is
        specifically verifying feed ordering itself.
        """
        return self.page.locator(self.post_items).filter(has_text=content)

    def open_post_menu(self, post: Locator) -> None:
        """Open a post's "..." dropdown menu (edit/delete)."""
        menu_button = post.locator(self.post_menu_button)
        expect(menu_button).to_be_visible(timeout=5000)
        menu_button.click(force=True)

    def edit_post(self, post: Locator, new_content: str) -> None:
        """Open a post's menu, edit its content, and save.

        The confirm() dialog this triggers is auto-accepted by the page
        fixture's dialog handler as part of resolving the save click, so
        the caller can check the result (e.g. the edit form disappearing)
        right after calling this without an extra wait.
        """
        self.open_post_menu(post)

        edit_button = post.locator(self.post_edit_button)
        expect(edit_button).to_be_visible(timeout=5000)
        edit_button.click(force=True)

        edit_textarea = post.locator(self.post_edit_textarea)
        expect(edit_textarea).to_be_visible(timeout=5000)
        edit_textarea.fill(new_content)

        save_button = post.locator(self.post_save_button)
        expect(save_button).to_be_visible(timeout=5000)
        save_button.click()

    def start_editing_post(self, post: Locator) -> Locator:
        """Open a post's menu and click Edit, returning the edit textarea.
        Use this (instead of edit_post()) when a test needs to cancel
        rather than save.
        """
        self.open_post_menu(post)

        edit_button = post.locator(self.post_edit_button)
        expect(edit_button).to_be_visible(timeout=5000)
        edit_button.click(force=True)

        edit_textarea = post.locator(self.post_edit_textarea)
        expect(edit_textarea).to_be_visible(timeout=5000)
        return edit_textarea

    def cancel_editing_post(self, post: Locator) -> None:
        """Click Cancel on a post that's currently being edited."""
        cancel_button = post.locator(self.post_cancel_button)
        expect(cancel_button).to_be_visible(timeout=5000)
        cancel_button.click()

    def delete_post(self, post: Locator) -> None:
        """Open a post's menu and delete it.

        The confirm() dialog this triggers is auto-accepted by the page
        fixture's dialog handler as part of resolving the delete click.
        """
        self.open_post_menu(post)

        delete_button = post.locator(self.post_delete_button)
        expect(delete_button).to_be_visible(timeout=5000)
        delete_button.click(force=True)

    def react_to_post(self, post: Locator, reaction: str = "like") -> None:
        """Open a post's reaction dropdown and pick a reaction. Works for
        applying a new reaction, changing an existing one, or removing one
        (clicking the currently-active reaction again removes it) - all
        three go through this same interaction.
        """
        react_button = post.locator(self.post_react_button)
        expect(react_button).to_be_visible(timeout=5000)
        react_button.click(force=True)

        # expect() below already retries until the dropdown has rendered,
        # so no separate wait is needed for the open animation.
        reaction_button = post.locator(f'[data-testid$="-reaction-{reaction}"]')
        expect(reaction_button).to_be_visible(timeout=5000)
        reaction_button.click(force=True)

    def open_comment_form(self, post: Locator) -> None:
        """Click a post's Comment button to reveal its inline comment form."""
        post.locator(self.post_comment_button).click()

    def toggle_repost(self, post: Locator) -> None:
        """Click a post's Repost button. Toggles: reposts it if not
        already reposted, un-reposts it if already reposted.
        """
        post.locator(self.post_repost_button).click()

    def go_to_all_tab(self) -> None:
        """Switch the feed to the "All" tab."""
        self.feed_tab_all.click()

    def go_to_following_tab(self) -> None:
        """Switch the feed to the "Following" tab."""
        self.feed_tab_following.click()
