import re

from playwright.sync_api import Page, expect

PITFALL = "catch-it/generic-title"


def test_each_page_has_its_own_title(page: Page, open_pitfall, expect_bug_on_broken):
    expect_bug_on_broken("the title never changes as you move between pages")
    open_pitfall(PITFALL)

    page.get_by_role("link", name="Settings").click()
    expect(page).to_have_title(re.compile("Settings"))

    page.get_by_role("link", name="Profile").click()
    expect(page).to_have_title(re.compile("Profile"))


def test_moving_to_a_new_page_is_announced(page: Page, open_pitfall, expect_bug_on_broken):
    expect_bug_on_broken('a single-page app gives no "new page" cue, and nothing announces it')
    open_pitfall(PITFALL)

    page.get_by_role("link", name="Settings").click()

    # A polite status region that a screen reader reads out after each navigation.
    expect(page.get_by_role("status")).to_contain_text("Settings")


def test_a_default_axe_scan_does_not_see_the_problem_that_is_the_lesson(page: Page, open_pitfall, axe_source):
    # axe checks that a <title> EXISTS (rule document-title). It does not know the page is a
    # single-page app, or that the title should change as the content does.
    open_pitfall(PITFALL)
    page.evaluate(axe_source)
    assert page.evaluate("axe.run()")["violations"] == []

    page.get_by_role("link", name="Settings").click()
    assert page.evaluate("axe.run()")["violations"] == []
