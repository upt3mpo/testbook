from playwright.sync_api import Page, expect

PITFALL = "catch-it/silent-error"


def submit_empty_form(page: Page, open_pitfall):
    open_pitfall(PITFALL)
    page.get_by_role("button", name="Log in").click()


def test_the_error_is_exposed_as_an_alert_so_it_is_announced(page: Page, open_pitfall, expect_bug_on_broken):
    expect_bug_on_broken("the error is a plain <div>: a screen reader user hears nothing")
    submit_empty_form(page, open_pitfall)

    alert = page.get_by_role("alert")
    expect(alert).to_be_visible()
    expect(alert).to_have_text("Incorrect email or password")


def test_focus_is_not_dropped_on_body_after_the_failed_submit(page: Page, open_pitfall, expect_bug_on_broken):
    expect_bug_on_broken("the submit button is disabled mid-request, so focus falls back to <body>")
    submit_empty_form(page, open_pitfall)
    page.get_by_text("Incorrect email or password").wait_for()

    assert page.evaluate("document.activeElement.tagName") != "BODY"


def test_a_default_axe_scan_does_not_see_the_problem_that_is_the_lesson(page: Page, open_pitfall, axe_source):
    # Good colour contrast, sound structure. Whether a message is ANNOUNCED depends on how
    # it was inserted, not on how it looks.
    submit_empty_form(page, open_pitfall)
    page.get_by_text("Incorrect email or password").wait_for()
    page.evaluate(axe_source)
    assert page.evaluate("axe.run()")["violations"] == []
