from playwright.sync_api import Page, expect

PITFALL = "catch-it/hover-click-fight"


def test_a_real_mouse_click_opens_the_picker_and_aria_expanded_agrees(page: Page, open_pitfall, expect_bug_on_broken):
    expect_bug_on_broken("hover opens, the click then closes it: shown on screen but aria-expanded=false")
    open_pitfall(PITFALL)

    # click() moves the pointer onto the button first (hover), then clicks, like a real mouse.
    react = page.get_by_role("button", name="React")
    react.click()

    expect(react).to_have_attribute("aria-expanded", "true")
    expect(page.get_by_role("button", name="Like")).to_be_visible()


def test_moving_the_pointer_away_does_not_close_a_picker_opened_by_keyboard(
    page: Page, open_pitfall, expect_bug_on_broken
):
    expect_bug_on_broken("mouseleave writes the same state, so it closes the keyboard-opened picker")
    open_pitfall(PITFALL)

    react = page.get_by_role("button", name="React")
    react.focus()
    page.keyboard.press("Enter")
    expect(react).to_have_attribute("aria-expanded", "true")

    page.mouse.move(0, 0)
    react.hover()
    page.mouse.move(0, 0)

    expect(react).to_have_attribute("aria-expanded", "true")


def test_a_default_axe_scan_does_not_see_the_problem_that_is_the_lesson(page: Page, open_pitfall, axe_source):
    # The bug only exists in the transition between two inputs, which no single-snapshot
    # scan visits.
    open_pitfall(PITFALL)
    page.evaluate(axe_source)
    assert page.evaluate("axe.run()")["violations"] == []
