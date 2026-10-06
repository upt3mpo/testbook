from playwright.sync_api import Page, expect

PITFALL = "catch-it/lost-focus"


def choose_edit(page: Page, open_pitfall):
    """Open the post menu and choose Edit using only the keyboard."""
    open_pitfall(PITFALL)
    page.get_by_role("button", name="Post options").focus()
    page.keyboard.press("Enter")
    page.get_by_role("button", name="Edit", exact=True).focus()
    page.keyboard.press("Enter")


def test_choosing_edit_moves_focus_into_the_editor(page: Page, open_pitfall, expect_bug_on_broken):
    expect_bug_on_broken("the Edit button vanishes and focus falls back to <body>")
    choose_edit(page, open_pitfall)

    expect(page.get_by_label("Edit post")).to_be_focused()


def test_cancel_returns_focus_to_the_control_that_opened_the_editor(page: Page, open_pitfall, expect_bug_on_broken):
    expect_bug_on_broken("closing the editor drops focus on <body> again")
    choose_edit(page, open_pitfall)

    page.get_by_role("button", name="Cancel").focus()
    page.keyboard.press("Enter")

    expect(page.get_by_role("button", name="Post options")).to_be_focused()


def test_a_default_axe_scan_does_not_see_the_problem_that_is_the_lesson(page: Page, open_pitfall, axe_source):
    # Focus is something that happens over time. A snapshot of the DOM has no "where did focus
    # go after that click?", so no snapshot rule can see this.
    open_pitfall(PITFALL)
    page.evaluate(axe_source)
    assert page.evaluate("axe.run()")["violations"] == []
