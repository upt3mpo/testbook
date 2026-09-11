"""Page object for the Settings page."""

import re

from playwright.sync_api import Page, expect

from .base_page import BasePage


class SettingsPage(BasePage):
    """Reusable helpers for the account settings page (profile fields,
    theme/density preferences, avatar, and account deletion).
    """

    def __init__(self, page: Page):
        super().__init__(page)

        # Selectors
        self.email_display = '[data-testid="settings-email"]'
        self.error_message = '[data-testid="settings-error"]'
        self.success_message = '[data-testid="settings-success"]'
        self.avatar_preview = '[data-testid="settings-avatar-preview"]'
        self.avatar_input = '[data-testid="settings-avatar-input"]'
        self.clear_avatar_button = '[data-testid="settings-clear-avatar-button"]'
        self.display_name_input = '[data-testid="settings-display-name-input"]'
        self.bio_input = '[data-testid="settings-bio-input"]'
        self.theme_select = '[data-testid="settings-theme-select"]'
        self.text_density_select = '[data-testid="settings-text-density-select"]'
        self.save_button = '[data-testid="settings-save-button"]'
        self.delete_account_button = '[data-testid="settings-delete-account-button"]'

    def goto(self) -> None:
        """Navigate to the settings page."""
        super().goto("/settings")

    def save(self) -> None:
        """Click the save button."""
        self.page.locator(self.save_button).click()

    def update_display_name(self, display_name: str) -> None:
        """Fill in a new display name and save."""
        self.page.locator(self.display_name_input).fill(display_name)
        self.save()

    def update_bio(self, bio: str) -> None:
        """Fill in a new bio and save."""
        self.page.locator(self.bio_input).fill(bio)
        self.save()

    def change_theme(self, theme: str) -> None:
        """Select a theme ("light" or "dark") and save."""
        self.page.locator(self.theme_select).select_option(theme)
        self.save()

    def change_text_density(self, density: str) -> None:
        """Select a text density ("normal" or "compact") and save."""
        self.page.locator(self.text_density_select).select_option(density)
        self.save()

    def clear_avatar(self) -> None:
        """Click the clear-avatar button."""
        self.page.locator(self.clear_avatar_button).click()

    def delete_account(self) -> None:
        """Click the delete-account button. The confirm() dialogs this
        triggers are auto-accepted by the page fixture's dialog handler.
        """
        self.page.locator(self.delete_account_button).click()

    def expect_save_succeeded(self) -> None:
        """Assert the "Settings updated successfully!" message appeared."""
        expect(self.page.locator(self.success_message)).to_be_visible(timeout=5000)

    def expect_theme_applied(self, theme: str) -> None:
        """Assert the given theme is actually applied to the page (the
        <html> element's data-theme attribute), not just selected in the
        dropdown.
        """
        expect(self.page.locator("html")).to_have_attribute("data-theme", theme)

    def expect_avatar_is_default(self) -> None:
        """Assert the avatar preview reverted to the default image."""
        expect(self.page.locator(self.avatar_preview)).to_have_attribute(
            "src", re.compile("default-avatar")
        )
