from playwright.sync_api import Page, expect

PITFALL = "trust-it/test-id-hides-bug"


def test_the_post_menu_opens_found_the_way_a_user_finds_it(page: Page, open_pitfall, expect_bug_on_broken):
    expect_bug_on_broken("the only name is a symbol, so a query by the real name finds nothing")
    open_pitfall(PITFALL)

    # Find controls by role and name, as a screen reader user (and Playwright's own guidance)
    # would. A test id is invisible to users, so it can never notice a missing name.
    menu_button = page.get_by_role("button", name="Post options")
    # Assert it exists first: click() would otherwise wait out the whole timeout.
    expect(menu_button).to_be_visible()
    menu_button.click()

    expect(page.locator("#menu")).to_be_visible()


def test_a_default_axe_scan_does_not_see_the_problem_either_that_is_the_lesson(page: Page, open_pitfall, axe_source):
    # The ellipsis glyph counts as text, so axe's button-name rule is satisfied: the button
    # "has a name". It is just a useless one. Whether a name is MEANINGFUL is a human call,
    # and a test id (which users never see) cannot make that call either.
    open_pitfall(PITFALL)
    page.evaluate(axe_source)
    assert page.evaluate("axe.run()")["violations"] == []
