/**
 * Base class for all page objects.
 *
 * Mirrors tests/e2e-python/pages/base_page.py. The JS suite has
 * `baseURL` configured in playwright.config.js, so unlike the Python
 * side (which has no such config and builds full URLs itself), goto()
 * here can just hand the relative path straight to page.goto().
 */
class BasePage {
  constructor(page) {
    this.page = page;
  }

  async goto(path = "") {
    await this.page.goto(path);
  }

  async waitForLoad() {
    await this.page.waitForLoadState("networkidle", { timeout: 10000 });
  }

  async screenshot(name) {
    await this.page.screenshot({ path: `test-results/screenshots/${name}.png` });
  }
}

export { BasePage };
