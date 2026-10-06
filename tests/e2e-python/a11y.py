"""Accessibility helpers for the Python Playwright tests.

The Python twin of tests/e2e/fixtures/a11y.js. One place owns the axe tag list and the
"scan the page and report" logic, so individual tests stay short and nobody narrows the standard
by accident.

How it differs from the JavaScript version (see docs/a11y/JS_VS_PYTHON_ACCESSIBILITY_TESTING.md):

- JavaScript has an official integration (@axe-core/playwright) with an AxeBuilder. Python has no
  official one, so this module injects the axe-core script into the page and calls axe.run()
  itself. That is only a few lines, but you maintain them.
- The axe-core script is read from frontend/node_modules, so Python learners need the frontend's
  dependencies installed (they already are if the app runs). The axe version therefore always
  matches the one the frontend tests use.
"""

import json
import re
from pathlib import Path

AXE_SCRIPT = Path(__file__).resolve().parents[2] / "frontend" / "node_modules" / "axe-core" / "axe.min.js"
REPORT_DIR = Path("test-results") / "a11y"

# Target standard: WCAG 2.2 Level AA, plus axe's best-practice rules.
#
# Do NOT drop 'best-practice'. landmark-one-main, region, page-has-heading-one, heading-order and
# several others carry no WCAG tag, so a WCAG-only list passes while real structural bugs ship.
# Do not drop 'wcag22aa' either: it is where target-size (2.5.8) lives.
AXE_TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa", "best-practice"]

_axe_source: str | None = None


def _source() -> str:
    global _axe_source
    if _axe_source is None:
        if not AXE_SCRIPT.exists():
            raise FileNotFoundError(
                f"axe-core not found at {AXE_SCRIPT}. Run `npm install` in frontend/ first."
            )
        _axe_source = AXE_SCRIPT.read_text(encoding="utf-8")
    return _axe_source


def run_axe(page, rules=None) -> list[dict]:
    """Scan the page as it is right now and return axe's list of violations.

    rules: run only these axe rules (for example ["color-contrast"]) instead of the whole tag set.
    """
    # CSS transitions animate colours. Scanning mid-fade measures colours that never exist at rest
    # and reports contrast failures that are not real (this happened on the Following tab). Wait
    # for running animations to finish first. Capped, so an endless animation cannot hang a test.
    try:
        page.wait_for_function("document.getAnimations().length === 0", timeout=3000)
    except Exception:
        pass

    # Every navigation creates a new document, so inject axe again whenever it is missing.
    if not page.evaluate("typeof window.axe !== 'undefined'"):
        page.evaluate(_source())
    run_only = {"type": "rule", "values": rules} if rules else {"type": "tag", "values": AXE_TAGS}
    result = page.evaluate("(options) => axe.run(document, options)", {"runOnly": run_only})
    return result["violations"]


def expect_no_a11y_violations(page, name: str = "axe", rules=None) -> None:
    """Fail on any axe violation. The full report is saved to test-results/a11y/ on failure,
    and the assertion message lists each rule, impact and the first offending node."""
    violations = run_axe(page, rules)
    if violations:
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
        (REPORT_DIR / f"{slug}-violations.json").write_text(json.dumps(violations, indent=2))

    summary = "\n  ".join(
        f"{v['id']} [{v['impact']}] x{len(v['nodes'])} - {v['help']}\n    {' '.join(v['nodes'][0]['target'])}"
        for v in violations
    )
    assert violations == [], f"{name}:\n  {summary}"


def press_tab(page) -> None:
    """Press the key that moves keyboard focus to the next control, in whichever engine is running.

    Safari (WebKit) by default only tabs through form fields, and needs Alt held to include links
    and buttons. Chromium and Firefox tab through everything.
    """
    engine = page.context.browser.browser_type.name
    page.keyboard.press("Alt+Tab" if engine == "webkit" else "Tab")
