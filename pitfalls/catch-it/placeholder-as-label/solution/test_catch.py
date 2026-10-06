from playwright.sync_api import Page, expect

PITFALL = "catch-it/placeholder-as-label"


def test_each_field_can_be_found_by_its_label(page: Page, open_pitfall, expect_bug_on_broken):
    expect_bug_on_broken("the fields have a placeholder but no label, so get_by_label finds nothing")
    open_pitfall(PITFALL)

    # get_by_label only works when a real <label> (or aria-label) names the field. A test that
    # finds the field by placeholder or test id would keep passing on the broken page.
    expect(page.get_by_label("Email")).to_be_visible()
    expect(page.get_by_label("Password")).to_be_visible()


def test_the_label_is_still_visible_after_the_user_has_typed(page: Page, open_pitfall, expect_bug_on_broken):
    expect_bug_on_broken("the only cue is the placeholder, which vanishes as soon as you type")
    open_pitfall(PITFALL)

    page.locator("input[type=email]").fill("sarah@example.com")
    expect(page.get_by_text("Email", exact=True)).to_be_visible()


def test_a_default_axe_scan_does_not_see_the_problem_that_is_the_lesson(page: Page, open_pitfall, axe_source):
    # axe accepts a non-empty placeholder as an accessible name, so its `label` rule is
    # satisfied. The expectation of a persistent label (WCAG 3.3.2, and good practice) is
    # stronger than what a tool can check.
    open_pitfall(PITFALL)
    page.evaluate(axe_source)
    assert page.evaluate("axe.run()")["violations"] == []
