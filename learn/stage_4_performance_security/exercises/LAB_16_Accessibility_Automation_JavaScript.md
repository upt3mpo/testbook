# Lab 16: Accessibility Automation (JavaScript)

**Estimated time:** 120 minutes (100 minutes core, 20 minutes optional stretch)
**Difficulty:** Intermediate
**Language:** JavaScript
**Prerequisites:** [Stage 0](../../stage_0_inclusion_first/README.md), Lab 10 (keyboard tests), Lab 12 (tags)

**Need Python instead?** Try [Lab 16: Accessibility Automation (Python)](LAB_16_Accessibility_Automation_Python.md). The two tracks are
compared in [JavaScript and Python accessibility testing compared](../../../docs/a11y/JS_VS_PYTHON_ACCESSIBILITY_TESTING.md).

**What this adds:** Stage 4 asks whether the system holds up under load and under attack. Accessibility is the third
non-functional question: does it work for everyone who needs to use it? In this lab you work with the real accessibility
suite, extend it, break the app on purpose to watch it fail, and learn exactly what automation can and cannot see.

---

## What you will learn

- How one helper can own the accessibility standard for a whole suite, and why that matters
- Why scanning a page is not enough, and how to scan the *states* of a page
- Why scans can flake, and how to make them reliable
- What failure looks like, and how to read an axe report
- Which defects automation catches, and which it never will

---

## Step-by-step instructions

Start the app with `./start-dev.sh` (or `make start`) and reset the data before each part:

```bash
curl -X POST http://localhost:8000/api/dev/reset
```

### Part 1: Read the suite (25 minutes)

Run the accessibility suite once, to see it pass:

```bash
cd tests
npm run test:a11y
```

You should see 50 tests pass in about two minutes. Now read how it is built.

**Open `tests/e2e/fixtures/a11y.js`.** It exports two things you will use: `AXE_TAGS` and
`expectNoA11yViolations(page, testInfo, options)`. Read the comment above `AXE_TAGS`. It says never to drop
`best-practice` or `wcag22aa`. Why?

**Open `tests/e2e/accessibility-axe.spec.js`** and find its four groups: every route, interaction states, phone width, and
dark theme. Notice that every test is one or two lines, because the helper does the work.

#### Experiment: what do the tags buy you?

The comment in the helper makes a claim: a WCAG-only tag list lets real bugs through. Test it.

1. Open `frontend/src/App.jsx`, find `PrivateLayout`, and change `<main id="main-content" tabIndex={-1}>` and its closing
   `</main>` to `<div id="main-content" tabIndex={-1}>` and `</div>`. The app looks identical, but the page no longer has a
   main landmark.
2. Run the feed scan:

   ```bash
   npx playwright test accessibility-axe -g "Feed page"
   ```

   It **fails**, reporting `landmark-one-main` and `region`. Those two rules carry the `best-practice` tag.
3. Now remove `"best-practice"` from `AXE_TAGS` in `tests/e2e/fixtures/a11y.js` and run it again. It **passes**. The bug is
   still there, but the narrowed standard cannot see it.
4. **Undo both changes:**

   ```bash
   git checkout frontend/src/App.jsx tests/e2e/fixtures/a11y.js
   ```

That is exactly how Testbook's original suite reported zero violations while real structural defects existed.

**Checkpoint:** you watched the same bug fail with all tags and pass without `best-practice`, then restored both files.

### Part 2: Extend the suite (25 minutes)

The suite scans many states, but not all. Add two.

**Create:** `tests/e2e/my_a11y.spec.js`

```javascript
import { test, expect } from "@playwright/test";
import { expectNoA11yViolations } from "./fixtures/a11y.js";

async function loginAsSarah(page) {
  await page.goto("/login");
  await page.getByLabel("Email").fill("sarah.johnson@testbook.com");
  await page.getByLabel("Password").fill("Sarah2024!");
  await page.getByRole("button", { name: "Log In" }).click();
  await expect(page.getByRole("navigation")).toBeVisible();
}

test.describe("My accessibility tests", { tag: "@a11y" }, () => {
  test("the feed with the Following tab selected", async ({ page }, testInfo) => {
    await loginAsSarah(page);
    await page.getByRole("button", { name: "Following" }).click();
    await expect(page.getByRole("button", { name: "Following" })).toHaveAttribute(
      "aria-pressed",
      "true"
    );
    await expectNoA11yViolations(page, testInfo, { name: "Following tab" });
  });

  // TODO: scan the feed in COMPACT text density. A user chooses it in Settings, so reach the state
  // the way a user does: open /settings, choose "Compact" in the Text Density field, save, wait
  // for the status message, go back to "/", and check the body has the class text-density-compact.
});
```

Write the second test yourself, then run both:

```bash
npx playwright test my_a11y --headed
```

Both should pass.

**Why this matters:** "Reach the state first, then scan it" is the rule that would have caught four of Testbook's real defects.
Text density, theme, the open menu, the error message: each is a different page as far as a scan is concerned.

#### Experiment: why does the helper wait?

Run your Following test a few times: it is reliable. Now find out why. Open `tests/e2e/fixtures/a11y.js` and find this
block at the top of `expectNoA11yViolations`:

```javascript
await page
  .waitForFunction(() => document.getAnimations().length === 0, null, { timeout: 3000 })
  .catch(() => {});
```

Comment it out and run your Following test again. It **fails** with `color-contrast`. The tabs use
`transition: all 0.2s`, so right after the click the active tab is half-way through a colour fade, and axe measures a colour
that never exists at rest. The failure is **not real**: wait 600 ms and the page is clean.

Restore the block (`git checkout tests/e2e/fixtures/a11y.js`).

> **Lesson:** a flaky accessibility test is worse than none, because people learn to ignore it. Scan after the page has
> settled. This is the accessibility version of the waiting lesson from Stage 3.

**Checkpoint:** both new tests pass, and you saw the scan fail when it measured a colour mid-fade.

### Part 3: Break it and read the failure (15 minutes)

A test you have never seen fail is a test you cannot trust. Break the app in a way axe catches.

1. In `frontend/src/components/Navbar.jsx`, find the avatar `<img>` and delete its `alt={user.display_name}` line.
2. Run the feed scan:

   ```bash
   npx playwright test accessibility-axe -g "Feed page"
   ```

3. Read the failure. The message lists each rule, its impact, and the first offending element:

   ```text
   image-alt [critical] x1 - Images must have alternative text
     <the selector of the offending image>
   ```

4. The full report is attached to the test. Open it:

   ```bash
   npx playwright show-report
   ```

   Click the failed test, find the **Feed-violations.json** attachment, and read the JSON: the rule, a link to its documentation,
   the HTML of the element, and a suggested fix.

5. **Undo:** `git checkout frontend/src/components/Navbar.jsx`.

**Checkpoint:** you read an axe failure message and its full JSON report.

### Part 4: Test what axe cannot see (20 minutes)

A scan sees one snapshot. Add two behaviour tests to `my_a11y.spec.js`.

```javascript
const ROUTES = [
  "/",
  "/post/1",
  "/profile/sarahjohnson",
  "/profile/sarahjohnson/followers",
  "/profile/sarahjohnson/following",
  "/settings",
];

test.describe("My behaviour tests", { tag: "@a11y" }, () => {
  test("no route scrolls sideways at 320px", async ({ page }) => {
    await page.setViewportSize({ width: 320, height: 700 });
    await loginAsSarah(page);
    for (const path of ROUTES) {
      await page.goto(path);
      await page.waitForLoadState("networkidle");
      const overflow = await page.evaluate(
        () => document.documentElement.scrollWidth - document.documentElement.clientWidth
      );
      expect(overflow, `${path} overflows by ${overflow}px`).toBeLessThanOrEqual(0);
    }
  });

  test("controls on the Settings page are at least 24x24 CSS px", async ({ page }) => {
    await loginAsSarah(page);
    await page.goto("/settings");
    const tooSmall = await page.evaluate(() =>
      [...document.querySelectorAll("button, a[href], input, textarea, select")]
        .map((el) => ({ el, r: el.getBoundingClientRect() }))
        .filter(({ r }) => r.width > 0 && r.height > 0 && (r.width < 24 || r.height < 24))
        .map(({ el, r }) => `${el.tagName} ${el.getAttribute("data-testid") || ""} ${Math.round(r.width)}x${Math.round(r.height)}`)
    );
    expect(tooSmall).toEqual([]);
  });
});
```

Run them: both pass. **Now break the first one.** In `frontend/src/components/Navbar.css`, find the `@media (max-width: 768px)`
block and delete the `flex-wrap: wrap;` line inside `.navbar-menu`. Run the test again. Every route now overflows by a few
pixels, because the navbar's links no longer wrap on a narrow screen, and your failure message names the route and the
amount. **Undo:** `git checkout frontend/src/components/Navbar.css`.

**Checkpoint:** your reflow test passes, and fails when the navbar's wrap rule is removed.

### Part 5: What does the suite still not catch? (15 minutes)

Testbook's audit found 20 defects (A11Y-001 to A11Y-020), and each is now guarded by a test. But a guard does not mean full coverage of the *kind*
of problem. Open the [audit log](../../../docs/a11y/AUDIT_LOG.md) and, for each defect, decide:

| Question | Your answer |
| --- | --- |
| Which test (scan or behaviour) guards it? | |
| Could the test pass while a real person still struggles? | |
| What would a human need to judge? | |

Then compare with the [coverage key](../../solutions/LAB_16_coverage_key.md). The pattern you should see: the suite proves
the **mechanism** (the label exists, the alert has the right role, focus moves) and cannot prove the **experience** (the label
makes sense, the announcement is useful, the order feels logical). That gap is Lab 17.

### Part 6: In CI, and Lighthouse (10 minutes)

Open `.github/workflows/accessibility.yml`. Find where it starts the servers, runs `npm run test:a11y`, and uploads the
Playwright report and the Lighthouse reports. Then run Lighthouse yourself, with the app running:

```bash
make lighthouse
```

Open one of the HTML reports from `tests/reports/lighthouse/`. Find the accessibility score and look at the list of audits.

**Question:** Lighthouse scores every page 100 on accessibility. Does that mean the pages are accessible? (It does not.
Lighthouse runs a subset of axe's rules, and several of the real defects passed it. Treat the score as a regression guard.)

**Checkpoint:** you can find the accessibility job in CI and explain what a Lighthouse score does and does not prove.

### Part 7: Optional stretch (20 minutes)

Pick two of the [Pitfalls](../../../pitfalls/README.md) and write the test that fails on the broken page and passes on the
fixed one, in JavaScript. Good choices here: *the theme nobody scanned* (it uses the same scan helper idea) and *lost focus*
(it uses the keyboard techniques from Lab 10). Each pitfall's `exercise.md` has a hint ladder.

---

## What you learned

- One helper owning the standard stops anyone narrowing it by accident
- A scan sees one snapshot: reach the state first, then scan it
- Scans can flake on animation, and a flaky test is a liability
- How to read an axe failure and its full report
- What the suite proves (mechanism) and what it cannot (experience)

## Lab completion checklist

- [ ] Ran `npm run test:a11y` and saw 50 tests pass
- [ ] Watched the `main` landmark removal fail with all tags and pass without `best-practice`
- [ ] Wrote scans for the Following tab and compact text density
- [ ] Saw a scan fail mid-fade when the animation wait was removed, and can explain why
- [ ] Read an axe failure message and the attached JSON report
- [ ] Wrote reflow and target-size tests, and broke the reflow one on purpose
- [ ] Filled in the coverage table and can say what automation cannot judge
- [ ] Ran Lighthouse and can say what a score of 100 does not prove
- [ ] Recorded how long each part took (the comparison page uses estimates, and your numbers are better)

## Reflection

1. Which of the 20 defects surprised you by being invisible to a scan?
2. Your Following test failed once for a reason that had nothing to do with accessibility. What would happen to a team if
   that kept happening?
3. If you could add one more test to the suite, what would it be, and which layer of the prevention ladder would it sit on?

**Next lab:** [Lab 17: Manual Accessibility Testing](LAB_17_Manual_Accessibility_Testing.md)
