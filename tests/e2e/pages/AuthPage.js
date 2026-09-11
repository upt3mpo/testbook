import { expect } from "@playwright/test";

import { BasePage } from "./BasePage.js";

/**
 * Page object for registration, login, and logout.
 *
 * Mirrors tests/e2e-python/pages/auth_page.py. Registration and login
 * are two different pages in the app, but they share the same shape of
 * interaction (fill a form, submit, check the result), so one page
 * object covers both rather than splitting into two classes that would
 * mostly duplicate each other.
 *
 * The form inputs and buttons have no <label>, aria-label, or ARIA role
 * of their own in the markup, so getByTestId is the honest choice here
 * (not a raw CSS locator, just the semantic API's testid method) rather
 * than forcing getByRole/getByLabel where the app doesn't support them.
 */
class AuthPage extends BasePage {
  constructor(page) {
    super(page);

    // Registration form
    this.registerEmailInput = page.getByTestId("register-email-input");
    this.registerUsernameInput = page.getByTestId("register-username-input");
    this.registerDisplayNameInput = page.getByTestId("register-displayname-input");
    this.registerPasswordInput = page.getByTestId("register-password-input");
    this.registerSubmitButton = page.getByTestId("register-submit-button");
    this.registerError = page.getByTestId("register-error");

    // Login form
    this.loginEmailInput = page.getByTestId("login-email-input");
    this.loginPasswordInput = page.getByTestId("login-password-input");
    this.loginSubmitButton = page.getByTestId("login-submit-button");
    this.loginError = page.getByTestId("login-error");

    // Navbar (present once logged in)
    this.navbar = page.getByTestId("navbar");
    this.navbarUsername = page.getByTestId("navbar-username");
    this.navbarLogoutButton = page.getByTestId("navbar-logout-button");
    this.navbarSettingsLink = page.getByTestId("navbar-settings-link");
    this.navbarProfileLink = page.getByTestId("navbar-profile-link");
  }

  async gotoRegister() {
    await this.goto("/register");
  }

  async gotoLogin() {
    await this.goto("/");
  }

  /**
   * Fill out and submit the registration form. Does not wait for the
   * result - call expectLoggedIn() or expectRegisterError() after this,
   * since a test may want to check either a success or a failure path.
   */
  async register({ email, username, displayName, password }) {
    await this.registerEmailInput.fill(email);
    await this.registerUsernameInput.fill(username);
    await this.registerDisplayNameInput.fill(displayName);
    await this.registerPasswordInput.fill(password);
    await this.registerSubmitButton.click();
  }

  /**
   * Check whether the browser's native HTML5 validation currently
   * considers the email field invalid (e.g. after entering
   * "notanemail"). Reads the input's own validity state rather than
   * submitting the form, since this is checking client-side validation,
   * not a server response.
   */
  async isRegisterEmailInvalid() {
    return this.registerEmailInput.evaluate((el) => !el.validity.valid);
  }

  /**
   * Fill out and submit the login form. Does not wait for the result -
   * call expectLoggedIn() or expectLoginError() after this.
   */
  async login(email, password) {
    await this.loginEmailInput.fill(email);
    await this.loginPasswordInput.fill(password);
    await this.loginSubmitButton.click();
  }

  async logout() {
    await this.navbarLogoutButton.click();
  }

  /**
   * Assert the navbar is visible (i.e. the user is authenticated), and
   * optionally that it shows a specific display name.
   */
  async expectLoggedIn(displayName) {
    await expect(this.page).toHaveURL("/", { timeout: 10000 });
    await expect(this.navbar).toBeVisible({ timeout: 10000 });
    if (displayName !== undefined) {
      await expect(this.navbarUsername).toContainText(displayName);
    }
  }

  /** Assert the navbar is gone and the login form is showing. */
  async expectLoggedOut() {
    await expect(this.navbar).not.toBeVisible();
    await expect(this.loginEmailInput).toBeVisible({ timeout: 5000 });
  }

  /**
   * Assert the login form is showing (used for protected-route redirect
   * checks, where no login has happened yet).
   */
  async expectOnLoginPage() {
    await expect(this.loginEmailInput).toBeVisible({ timeout: 5000 });
  }

  async expectLoginError(pattern) {
    await expect(this.loginError).toBeVisible({ timeout: 5000 });
    await expect(this.loginError).toContainText(pattern);
  }

  /**
   * Assert the registration error message is visible and matches
   * pattern. Uses the register-error testid rather than a raw
   * text-content locator, so it doesn't depend on the exact wording of
   * the error message staying the same.
   */
  async expectRegisterError(pattern) {
    await expect(this.registerError).toBeVisible({ timeout: 5000 });
    await expect(this.registerError).toContainText(pattern);
  }
}

export { AuthPage };
