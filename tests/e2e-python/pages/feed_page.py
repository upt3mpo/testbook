"""Page object for the Feed page"""

from playwright.sync_api import Locator, Page, expect

from .base_page import BasePage


class FeedPage(BasePage):
    """Reusable helpers for interacting with the feed."""

    def __init__(self, page: Page):
        super().__init__(page)

        # Selectors
        self.navbar = '[data-testid="navbar"]'
        self.create_post_textarea = '[data-testid="create-post-textarea"]'
        self.create_post_submit = '[data-testid="create-post-submit-button"]'
        self.post_items = '[data-testid-generic="post-item"]'
        self.post_delete_button = '[data-testid$="-delete-button"]'
        self.post_react_button = '[data-testid$="-react-button"]'

    def goto(self, wait_for_posts: bool = True) -> None:
        """Navigate to feed page.

        Args:
            wait_for_posts: If True, wait for posts to load from API (default: True)
        """
        super().goto("/")
        expect(self.page.locator(self.navbar)).to_be_visible(timeout=10000)

        if wait_for_posts:
            # Wait for feed to finish loading posts from API
            # This is important in CI where API calls may be slower
            try:
                self.page.wait_for_load_state("networkidle", timeout=5000)
            except:
                # If networkidle times out, wait a bit more for API calls
                self.page.wait_for_timeout(2000)

    def create_post(self, content: str) -> None:
        """Create a new post."""
        self.page.fill(self.create_post_textarea, content)
        self.page.click(self.create_post_submit)
        self.page.wait_for_timeout(500)

        # Verify post appeared
        expect(self.first_post()).to_contain_text(content)

    def first_post(self) -> Locator:
        """Get the first (most recent) post."""
        return self.page.locator(self.post_items).first

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
        """Find a specific post by its content."""
        return self.page.locator(self.post_items, has_text=content)

    def delete_post(self, post: Locator) -> None:
        """Delete a specific post."""
        post.locator(self.post_delete_button).click()
        self.page.wait_for_timeout(500)

    def react_to_post(self, post: Locator, reaction: str = "like") -> None:
        """Add a reaction to a post."""
        post.locator(self.post_react_button).hover()
        self.page.wait_for_timeout(200)
        post.locator(f'[data-testid$="-reaction-{reaction}"]').click()
        self.page.wait_for_timeout(300)
