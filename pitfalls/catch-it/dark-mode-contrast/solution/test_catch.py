from playwright.sync_api import Page, expect

PITFALL = "catch-it/dark-mode-contrast"

CONTRAST_ONLY = "axe.run({ runOnly: ['color-contrast'] })"


def test_the_default_light_theme_passes_which_is_why_the_suite_looked_green(page: Page, open_pitfall, axe_source):
    # Same result on BOTH pages: the bug only exists in a state nobody scanned.
    open_pitfall(PITFALL)
    page.evaluate(axe_source)
    assert page.evaluate(CONTRAST_ONLY)["violations"] == []


def test_the_dark_theme_passes_too(page: Page, open_pitfall, expect_bug_on_broken, axe_source):
    expect_bug_on_broken("white text on the dark accent colour is 3.45:1; 4.5:1 is required")
    open_pitfall(PITFALL)

    # Reach the state first, THEN scan it. Every theme, mode or preference a user can switch is
    # another state to test.
    page.get_by_role("button", name="Dark theme").click()
    expect(page.locator("html")).to_have_attribute("data-theme", "dark")

    page.evaluate(axe_source)
    assert page.evaluate(CONTRAST_ONLY)["violations"] == []
