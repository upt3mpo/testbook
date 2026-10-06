# THE TEST UNDER SUSPICION. It is green on BOTH pages, including the one where Escape does
# not work at all. Should you trust it? (Run it, then read ../README.md.)
from playwright.sync_api import Page, expect


def test_escape_closes_the_menu(page: Page, open_pitfall):
    open_pitfall("trust-it/vacuous-escape-test")

    page.get_by_role("button", name="Menu").click()
    page.keyboard.press("Escape")

    expect(page.locator("#menu")).to_be_hidden()
