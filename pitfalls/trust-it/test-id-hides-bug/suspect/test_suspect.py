# THE TEST UNDER SUSPICION. Green on BOTH pages, including the one where the menu button's only
# name is a symbol. Should you trust it? (Run it, then read ../README.md.)
from playwright.sync_api import Page, expect


def test_the_post_menu_opens(page: Page, open_pitfall):
    open_pitfall("trust-it/test-id-hides-bug")

    page.get_by_test_id("post-menu").click()

    expect(page.locator("#menu")).to_be_visible()
