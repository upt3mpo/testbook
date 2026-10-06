from playwright.sync_api import Page

PITFALL = "catch-it/invisible-tab-stops"

IS_HIDDEN_FROM_SIGHT = """
(el) => {
  for (let node = el; node; node = node.parentElement) {
    const s = getComputedStyle(node);
    if (s.display === 'none' || s.visibility === 'hidden' || Number(s.opacity) === 0) return true;
  }
  return false;
}
"""


def test_no_tab_stop_lands_on_a_control_the_user_cannot_see(page: Page, open_pitfall, expect_bug_on_broken):
    expect_bug_on_broken("the closed picker leaves 3 invisible controls in the Tab order")
    open_pitfall(PITFALL)

    # Press Tab through the whole page, noting every stop a sighted user could not see.
    invisible_stops = []
    for _ in range(8):
        page.keyboard.press("Tab")
        stop = page.evaluate(
            f"""() => {{
                const el = document.activeElement;
                const hidden = ({IS_HIDDEN_FROM_SIGHT})(el);
                return {{ label: el.getAttribute('aria-label') || el.textContent.trim(), hidden }};
            }}"""
        )
        if stop["hidden"]:
            invisible_stops.append(stop["label"])

    assert invisible_stops == []


def test_a_default_axe_scan_does_not_see_the_problem_that_is_the_lesson(
    page: Page, open_pitfall, axe_source
):
    # Same result on BOTH pages: axe inspects one snapshot of the DOM, and a transparent
    # control is not a rule violation. Only pressing Tab and watching focus reveals this bug.
    open_pitfall(PITFALL)
    page.evaluate(axe_source)
    results = page.evaluate("axe.run()")
    assert results["violations"] == []
