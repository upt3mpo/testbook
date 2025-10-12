"""Base page class for all page objects"""

from playwright.sync_api import Page


class BasePage:
    """Base class for all page objects."""

    def __init__(self, page: Page, base_url: str = "http://localhost:3000"):
        self.page = page
        self.base_url = base_url

    def goto(self, path: str = "") -> None:
        """Navigate to a specific path."""
        url = f"{self.base_url}{path}"
        self.page.goto(url)

    def wait_for_load(self) -> None:
        """Wait for page to fully load."""
        self.page.wait_for_load_state("networkidle", timeout=10000)

    def screenshot(self, name: str) -> None:
        """Take a screenshot."""
        self.page.screenshot(path=f"test-results/screenshots/{name}.png")
