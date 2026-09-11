import { expect } from "@playwright/test";

import { BasePage } from "./BasePage.js";

/**
 * Page object for the Settings page.
 *
 * Mirrors tests/e2e-python/pages/settings_page.py.
 */
class SettingsPage extends BasePage {
  constructor(page) {
    super(page);

    // Selectors
    this.emailDisplay = '[data-testid="settings-email"]';
    this.errorMessage = '[data-testid="settings-error"]';
    this.successMessage = '[data-testid="settings-success"]';
    this.avatarPreview = '[data-testid="settings-avatar-preview"]';
    this.avatarInput = '[data-testid="settings-avatar-input"]';
    this.clearAvatarButton = '[data-testid="settings-clear-avatar-button"]';
    this.displayNameInput = '[data-testid="settings-display-name-input"]';
    this.bioInput = '[data-testid="settings-bio-input"]';
    this.themeSelect = '[data-testid="settings-theme-select"]';
    this.textDensitySelect = '[data-testid="settings-text-density-select"]';
    this.saveButton = '[data-testid="settings-save-button"]';
    this.deleteAccountButton = '[data-testid="settings-delete-account-button"]';
  }

  /** Navigate to the settings page. */
  async goto() {
    await super.goto("/settings");
  }

  /** Click the save button. */
  async save() {
    await this.page.locator(this.saveButton).click();
  }

  /** Fill in a new display name and save. */
  async updateDisplayName(displayName) {
    await this.page.locator(this.displayNameInput).fill(displayName);
    await this.save();
  }

  /** Fill in a new bio and save. */
  async updateBio(bio) {
    await this.page.locator(this.bioInput).fill(bio);
    await this.save();
  }

  /** Select a theme ("light" or "dark") and save. */
  async changeTheme(theme) {
    await this.page.locator(this.themeSelect).selectOption(theme);
    await this.save();
  }

  /** Select a text density ("normal" or "compact") and save. */
  async changeTextDensity(density) {
    await this.page.locator(this.textDensitySelect).selectOption(density);
    await this.save();
  }

  /** Click the clear-avatar button. */
  async clearAvatar() {
    await this.page.locator(this.clearAvatarButton).click();
  }

  /**
   * Click the delete-account button. The confirm() dialogs this
   * triggers are auto-accepted by setupDialogHandler().
   */
  async deleteAccount() {
    await this.page.locator(this.deleteAccountButton).click();
  }

  /** Assert the "Settings updated successfully!" message appeared. */
  async expectSaveSucceeded() {
    await expect(this.page.locator(this.successMessage)).toBeVisible({
      timeout: 5000,
    });
  }

  /**
   * Assert the given theme is actually applied to the page (the <html>
   * element's data-theme attribute), not just selected in the dropdown.
   */
  async expectThemeApplied(theme) {
    await expect(this.page.locator("html")).toHaveAttribute("data-theme", theme);
  }

  /** Assert the avatar preview reverted to the default image. */
  async expectAvatarIsDefault() {
    await expect(this.page.locator(this.avatarPreview)).toHaveAttribute(
      "src",
      /default-avatar/
    );
  }
}

export { SettingsPage };
