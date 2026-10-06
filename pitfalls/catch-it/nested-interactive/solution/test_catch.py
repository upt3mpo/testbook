from playwright.sync_api import Page

PITFALL = "catch-it/nested-interactive"


def test_one_control_is_one_tab_stop(page: Page, open_pitfall, expect_bug_on_broken):
    expect_bug_on_broken("the View button sits inside the View link, so Tab stops twice")
    open_pitfall(PITFALL)

    # Tab once through the page (Comment, then View) and record what each stop is. Three presses
    # is enough to see every stop without wrapping round to the start again.
    stops = []
    for _ in range(3):
        page.keyboard.press("Tab")
        stops.append(page.evaluate("document.activeElement.textContent.trim()"))

    assert stops.count("View") == 1


def test_activating_the_control_once_opens_it_once(page: Page, open_pitfall, expect_bug_on_broken):
    expect_bug_on_broken("a link and a button are both focusable, so there are two things to activate")
    open_pitfall(PITFALL)

    # Exactly one thing named "View" can be activated, and it is the link.
    assert page.get_by_role("link", name="View").count() == 1
    assert page.get_by_role("button", name="View").count() == 0


def test_a_default_axe_scan_does_not_see_the_problem_that_is_the_lesson(page: Page, open_pitfall, axe_source):
    # A button inside a link is invalid HTML, but axe has no rule that flags this particular
    # nesting. Every control has a name and a role, so every snapshot check passes.
    open_pitfall(PITFALL)
    page.evaluate(axe_source)
    assert page.evaluate("axe.run()")["violations"] == []
