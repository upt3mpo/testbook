from playwright.sync_api import Page, expect


def test_escape_closes_a_menu_that_is_open_and_the_test_proves_it_was_open_first(
    page: Page, open_pitfall, expect_bug_on_broken
):
    expect_bug_on_broken("Escape does nothing on this page; a trustworthy test must notice")
    open_pitfall("trust-it/vacuous-escape-test")

    # Open the menu by KEYBOARD. A mouse click hovers first, and on this page hover and click
    # both write the same state, so click() opens-then-closes the menu and the old test never
    # gave Escape anything to close.
    page.get_by_role("button", name="Menu").focus()
    page.keyboard.press("Enter")

    # Precondition: assert the menu is really open BEFORE pressing Escape. Without this line
    # the test can pass without ever exercising the feature.
    expect(page.locator("#menu")).to_be_visible()

    page.keyboard.press("Escape")
    expect(page.locator("#menu")).to_be_hidden()
