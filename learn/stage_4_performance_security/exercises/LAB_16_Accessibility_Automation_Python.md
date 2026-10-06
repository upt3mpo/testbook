# Lab 16: Accessibility Automation (Python)

**Estimated time:** 135 minutes (115 minutes core, 20 minutes optional stretch)
**Difficulty:** Intermediate
**Language:** Python
**Prerequisites:** [Stage 0](../../stage_0_inclusion_first/README.md), Lab 10 (keyboard tests), Lab 12 (markers)

**Need JavaScript instead?** Try [Lab 16: Accessibility Automation (JavaScript)](LAB_16_Accessibility_Automation_JavaScript.md). The two
tracks are compared in [JavaScript and Python accessibility testing compared](../../../docs/a11y/JS_VS_PYTHON_ACCESSIBILITY_TESTING.md).

**What this adds:** Stage 4 asks whether the system holds up under load and under attack. Accessibility is the third
non-functional question: does it work for everyone who needs to use it? In this lab you work with the real accessibility
suite, **write the axe helper yourself** (the main difference from the JavaScript track, which has an official package),
extend the suite, break the app on purpose to watch it fail, and learn exactly what automation can and cannot see.

---

## What you will learn

- How to run axe-core from Python, with no official integration
- How one helper can own the accessibility standard for a whole suite, and why that matters
- Why scanning a page is not enough, and how to scan the *states* of a page
- Why scans can flake, and how to make them reliable
- Which defects automation catches, and which it never will

---

## Step-by-step instructions

Start the app with `./start-dev.sh` (or `make start`). The tests read axe-core from the frontend's dependencies, so make
sure `npm install` has been run in `frontend/` (it has if the app runs). Reset the data before each part:

```bash
curl -X POST http://localhost:8000/api/dev/reset
```

### Part 1: Read the suite (20 minutes)

Run the accessibility suite once, to see it pass:

```bash
cd tests/e2e-python
pytest -m a11y -v
```

You should see 50 tests pass in about two minutes. Now read how it is built.

**Open `tests/e2e-python/a11y.py`.** It exports `AXE_TAGS`, `run_axe`, `expect_no_a11y_violations` and `press_tab`. Read the
comment above `AXE_TAGS`. It says never to drop `best-practice` or `wcag22aa`. Why?

**Open `tests/e2e-python/test_accessibility.py`** and find its groups: `TestAxeRoutes`, `TestAxeInteractionStates`,
`TestAxePhoneWidth`, `TestAxeDarkTheme`, then the behaviour tests. Notice that each scan is one or two lines, because the helper
does the work.

#### Experiment: what do the tags buy you?

The comment in the helper makes a claim: a WCAG-only tag list lets real bugs through. Test it.

1. Open `frontend/src/App.jsx`, find `PrivateLayout`, and change `<main id="main-content" tabIndex={-1}>` and its closing
   `</main>` to `<div id="main-content" tabIndex={-1}>` and `</div>`. The app looks identical, but the page no longer has a
   main landmark.
2. Run the feed scan:

   ```bash
   pytest test_accessibility.py -k "TestAxeRoutes and Feed" -v
   ```

   It **fails**, reporting `landmark-one-main` and `region`. Those two rules carry the `best-practice` tag.
3. Now remove `"best-practice"` from `AXE_TAGS` in `tests/e2e-python/a11y.py` and run it again. It **passes**. The bug is
   still there, but the narrowed standard cannot see it.
4. **Undo both changes:**

   ```bash
   git checkout frontend/src/App.jsx tests/e2e-python/a11y.py
   ```

That is exactly how Testbook's original suite reported zero violations while real structural defects existed.

**Checkpoint:** you watched the same bug fail with all tags and pass without `best-practice`, then restored both files.

### Part 2: Write the axe helper yourself (20 minutes)

In JavaScript this is `npm install @axe-core/playwright` and a few lines. Python has no official integration, so you write the
glue. It is short, and writing it once means you understand exactly what the helper does.

**Create:** `tests/e2e-python/my_axe.py`

```python
from pathlib import Path

# The axe-core script lives in the frontend's dependencies, so the version always matches.
AXE_SCRIPT = Path(__file__).resolve().parents[2] / "frontend" / "node_modules" / "axe-core" / "axe.min.js"

TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa", "best-practice"]


def run_axe(page):
    """Scan the page as it is right now and return axe's list of violations."""
    # TODO 1: wait for CSS animations to finish, so you never scan a colour mid-fade
    #         (document.getAnimations().length === 0). Cap the wait at 3 seconds.
    # TODO 2: inject the axe script into the page if window.axe is not defined yet.
    #         A new page load is a new document, so check every time.
    # TODO 3: run axe.run(document, options) in the page and return the "violations" list.
    #         Options: {"runOnly": {"type": "tag", "values": TAGS}}
    raise NotImplementedError


def expect_no_violations(page, name="axe"):
    violations = run_axe(page)
    # TODO 4: assert there are none, with a message that lists each rule, its impact, and the
    #         first offending element's selector, so a failure is actionable without a debugger.
    raise NotImplementedError
```

**Hints** (use one at a time):

1. `page.wait_for_function("...", timeout=3000)` waits for a JavaScript condition. Wrap it in `try/except` so an endless
   animation cannot hang a test.
2. `page.evaluate("typeof window.axe !== 'undefined'")` tells you whether axe is already loaded. `page.evaluate(script_text)`
   runs a script in the page.
3. `page.evaluate("(options) => axe.run(document, options)", {...})` passes a Python dict into the page and returns the result
   as a dict.
4. A violation is a dict with `id`, `impact`, `help` and `nodes`. Each node has a `target` list of selectors.

**Test your helper.** Create `tests/e2e-python/test_my_axe.py`:

```python
import pytest
from my_axe import expect_no_violations
from pages.auth_page import AuthPage

pytestmark = pytest.mark.a11y


def test_the_login_page_has_no_violations(page, base_url, fresh_database):
    page.goto(f"{base_url}/login")
    page.get_by_label("Email").wait_for()
    expect_no_violations(page, "Login")
```

Run it: it should pass. Then break the app (delete the `alt` line from the navbar avatar in
`frontend/src/components/Navbar.jsx`, and scan the feed after logging in) and check **your helper** fails with a readable
message. Undo with `git checkout frontend/src/components/Navbar.jsx`.

**Compare** your version with the shipped `a11y.py`. Differences are fine. What did the shipped one add?

> **The workload difference.** Writing this helper is the main extra work in the Python track. It is about 15 lines, and you
> maintain them. In exchange, the axe version always matches the frontend's, and you know exactly what runs. See the
> [comparison](../../../docs/a11y/JS_VS_PYTHON_ACCESSIBILITY_TESTING.md).

**Checkpoint:** your helper passes on a clean page and fails readably on a broken one.

### Part 3: Extend the suite (25 minutes)

The suite scans many states, but not all. Add two. From here on, use the shipped `a11y.py` (or your own, if you prefer).

**Create:** `tests/e2e-python/test_my_a11y.py`

```python
import re

import pytest
from playwright.sync_api import Page, expect

from a11y import expect_no_a11y_violations
from pages.auth_page import AuthPage

pytestmark = pytest.mark.a11y


def login_as_sarah(page: Page) -> None:
    auth = AuthPage(page)
    auth.goto_login()
    auth.login("sarah.johnson@testbook.com", "Sarah2024!")
    auth.expect_logged_in()


def test_the_feed_with_the_following_tab_selected(page: Page, fresh_database):
    login_as_sarah(page)
    page.get_by_role("button", name="Following").click()
    expect(page.get_by_role("button", name="Following")).to_have_attribute("aria-pressed", "true")
    expect_no_a11y_violations(page, "Following tab")


# TODO: scan the feed in COMPACT text density. A user chooses it in Settings, so reach the state
# the way a user does: open /settings, choose "Compact" in the Text Density field, save, wait for
# the status message, go back to "/", and check the body has the class text-density-compact.
```

Write the second test yourself, then run both:

```bash
pytest test_my_a11y.py -v
```

Both should pass.

**Why this matters:** "Reach the state first, then scan it" is the rule that would have caught four of Testbook's real defects.
Text density, theme, the open menu, the error message: each is a different page as far as a scan is concerned.

#### Experiment: why does the helper wait?

Open `tests/e2e-python/a11y.py` and find this block in `run_axe`:

```python
try:
    page.wait_for_function("document.getAnimations().length === 0", timeout=3000)
except Exception:
    pass
```

Comment it out and run your Following test several times. It can **fail** with `color-contrast`. The tabs use
`transition: all 0.2s`, so right after the click the active tab is half-way through a colour fade, and axe measures a colour
that never exists at rest. The failure is **not real**: wait 600 ms and the page is clean. Restore the block
(`git checkout tests/e2e-python/a11y.py`).

> **Lesson:** a flaky accessibility test is worse than none, because people learn to ignore it. Scan after the page has
> settled. This is the accessibility version of the waiting lesson from Stage 3.

**Checkpoint:** both new tests pass, and you saw a scan fail mid-fade when the animation wait was removed.

### Part 4: Break it and read the failure (15 minutes)

A test you have never seen fail is a test you cannot trust. Break the app in a way axe catches.

1. In `frontend/src/components/Navbar.jsx`, find the avatar `<img>` and delete its `alt={user.display_name}` line.
2. Run the feed scan:

   ```bash
   pytest test_accessibility.py -k "TestAxeRoutes and Feed" -v
   ```

3. Read the failure. The message lists each rule, its impact, and the first offending element:

   ```text
   Feed:
     image-alt [critical] x1 - Images must have alternative text
       <the selector of the offending image>
   ```

4. The full report is saved too. Open `tests/e2e-python/test-results/a11y/feed-violations.json` and read it: the rule, a link to
   its documentation, the HTML of the element, and a suggested fix.
5. **Undo:** `git checkout frontend/src/components/Navbar.jsx`.

> **A difference from JavaScript:** the JavaScript helper attaches this JSON to the Playwright HTML report. Here it is a file on
> disk, because pytest has no built-in equivalent of an attachment.

**Checkpoint:** you read an axe failure message and its full JSON report.

### Part 5: Test what axe cannot see (20 minutes)

A scan sees one snapshot. Add two behaviour tests to `test_my_a11y.py`.

```python
ROUTES = [
    "/",
    "/post/1",
    "/profile/sarahjohnson",
    "/profile/sarahjohnson/followers",
    "/profile/sarahjohnson/following",
    "/settings",
]


def test_no_route_scrolls_sideways_at_320px(page: Page, fresh_database):
    page.set_viewport_size({"width": 320, "height": 700})
    login_as_sarah(page)
    for path in ROUTES:
        page.goto(f"http://localhost:3000{path}")
        page.wait_for_load_state("networkidle")
        overflow = page.evaluate(
            "document.documentElement.scrollWidth - document.documentElement.clientWidth"
        )
        assert overflow <= 0, f"{path} overflows by {overflow}px"


def test_controls_on_the_settings_page_are_at_least_24px(page: Page, fresh_database):
    login_as_sarah(page)
    page.goto("http://localhost:3000/settings")
    too_small = page.evaluate(
        """() => [...document.querySelectorAll('button, a[href], input, textarea, select')]
            .map(el => ({ el, r: el.getBoundingClientRect() }))
            .filter(({ r }) => r.width > 0 && r.height > 0 && (r.width < 24 || r.height < 24))
            .map(({ el, r }) => `${el.tagName} ${el.getAttribute('data-testid') || ''} ${Math.round(r.width)}x${Math.round(r.height)}`)"""
    )
    assert too_small == []
```

Run them: both pass. **Now break the first one.** In `frontend/src/components/Navbar.css`, find the `@media (max-width: 768px)`
block and delete the `flex-wrap: wrap;` line inside `.navbar-menu`. Run the test again. Every route now overflows by a few
pixels, because the navbar's links no longer wrap on a narrow screen, and your failure message names the route and the
amount. **Undo:** `git checkout frontend/src/components/Navbar.css`.

**Checkpoint:** your reflow test passes, and fails when the navbar's wrap rule is removed.

### Part 6: What does the suite still not catch? (15 minutes)

Testbook's audit found 19 defects, and each is now guarded by a test. But a guard does not mean full coverage of the *kind*
of problem. Open the [audit log](../../../docs/a11y/AUDIT_LOG.md) and, for each defect, decide:

| Question | Your answer |
| --- | --- |
| Which test (scan or behaviour) guards it? | |
| Could the test pass while a real person still struggles? | |
| What would a human need to judge? | |

Then compare with the [coverage key](../../solutions/LAB_16_coverage_key.md). The pattern you should see: the suite proves
the **mechanism** (the label exists, the alert has the right role, focus moves) and cannot prove the **experience** (the label
makes sense, the announcement is useful, the order feels logical). That gap is Lab 17.

### Part 7: In CI, and Lighthouse (10 minutes)

Open `.github/workflows/e2e-tests.yml` and find the Python job: it runs `pytest -v`, which now includes the accessibility tests.
Then open `.github/workflows/accessibility.yml`, which runs the JavaScript accessibility suite and Lighthouse on its own. Run
Lighthouse yourself, with the app running:

```bash
make lighthouse
```

Open one of the HTML reports from `tests/reports/lighthouse/` and find the accessibility score.

**Question:** Lighthouse scores every page 100 on accessibility. Does that mean the pages are accessible? (It does not.
Lighthouse runs a subset of axe's rules, and several of the 19 real defects passed it. Treat the score as a regression guard.)

**Checkpoint:** you can find where accessibility runs in CI and explain what a Lighthouse score does and does not prove.

### Part 8: Optional stretch (20 minutes)

Pick two of the [Pitfalls](../../../pitfalls/README.md) and write the test that fails on the broken page and passes on the fixed
one, in Python. Good choices here: *the theme nobody scanned* and *lost focus*. Each pitfall's `exercise.md` has a hint ladder.

---

## What you learned

- How to run axe-core from Python, and what an official integration would have saved you
- One helper owning the standard stops anyone narrowing it by accident
- A scan sees one snapshot: reach the state first, then scan it
- Scans can flake on animation, and a flaky test is a liability
- What the suite proves (mechanism) and what it cannot (experience)

## Lab completion checklist

- [ ] Ran `pytest -m a11y` and saw 50 tests pass
- [ ] Watched the `main` landmark removal fail with all tags and pass without `best-practice`
- [ ] Wrote my own axe helper that passes on a clean page and fails readably on a broken one
- [ ] Wrote scans for the Following tab and compact text density
- [ ] Saw a scan fail mid-fade when the animation wait was removed, and can explain why
- [ ] Read an axe failure message and the saved JSON report
- [ ] Wrote reflow and target-size tests, and broke the reflow one on purpose
- [ ] Filled in the coverage table and can say what automation cannot judge
- [ ] Ran Lighthouse and can say what a score of 100 does not prove
- [ ] Recorded how long each part took (the comparison page uses estimates, and your numbers are better)

## Reflection

1. What did writing the helper yourself teach you that using a package would not have?
2. Your Following test failed once for a reason that had nothing to do with accessibility. What would happen to a team if
   that kept happening?
3. If you could add one more test to the suite, what would it be, and which layer of the prevention ladder would it sit on?

**Next lab:** [Lab 17: Manual Accessibility Testing](LAB_17_Manual_Accessibility_Testing.md)
