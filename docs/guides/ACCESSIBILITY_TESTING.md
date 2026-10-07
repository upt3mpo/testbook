# Accessibility Testing Guide

**A reference for testing Testbook against WCAG 2.2 AA: what is automated, what needs a person, and where everything lives.**

This guide is the quick reference. To learn the ideas, start with [Stage 0: Inclusion First](../../learn/stage_0_inclusion_first/README.md) and the Stage 4 labs ([Lab 16](../../learn/stage_4_performance_security/exercises/LAB_16_Accessibility_Automation_JavaScript.md) for automation, [Lab 17](../../learn/stage_4_performance_security/exercises/LAB_17_Manual_Accessibility_Testing.md) for manual testing).

---

<h2 id="why-it-matters">Why It Matters</h2>

- About 1.3 billion people, roughly 1 in 6, live with a significant disability, according to the [World Health Organization](https://www.who.int/news-room/fact-sheets/detail/disability-and-health).
- Many people have a temporary or situational limitation too: a broken arm, a bright screen outside, a noisy train.
- Accessibility is often a legal or procurement requirement. Examples: the Americans with Disabilities Act and Section 508 in the United States, and the European Accessibility Act together with the EN 301 549 standard in Europe. Rules differ by country and sector, and they change. In the US, the Department of Justice's 2024 rule for state and local government websites points to WCAG 2.1 AA, and its compliance dates have already moved once, so check current dates. **This is not legal advice.**
- Features built for one group usually help everyone: captions, keyboard shortcuts and clear labels.

---

<h2 id="the-target">The Target</h2>

**WCAG 2.2 Level AA**, published by the W3C in October 2023. It adds criteria for focus visibility (2.4.11), dragging alternatives (2.5.7), target size (2.5.8) and accessible authentication (3.3.8), and it removes the obsolete 4.1.1 Parsing. Testbook's own status against all 55 A and AA criteria is in the [conformance report](../a11y/CONFORMANCE_REPORT.md).

---

<h2 id="automation-vs-people">Automation vs People</h2>

Automation proves a **mechanism**: this control has a name, this color pair passes, focus lands here. People judge the **experience**: is that name meaningful, is this flow usable, did the announcement make sense.

| Question | Automation can answer | A person must answer |
| --- | --- | --- |
| Does every input have an accessible name? | Yes | Whether the name is meaningful |
| Is text contrast at least 4.5:1? | Yes, for plain backgrounds | Text over images, gradients, hover and focus states |
| Can I reach and operate everything by keyboard? | Partly (Tab order, focus moves) | Whether the order makes sense, and whether anything is a trap |
| Is a status message announced? | That a live region exists and changed | What a screen reader actually says |
| Does the page work at 400% zoom? | Partly (320px viewport checks) | Whether it is still usable |
| Is the content understandable? | No | Yes |

Do not split the effort by a fixed percentage. Run the automated checks on every change, and schedule the manual scripts for each release and for any change to interaction patterns.

---

<h2 id="the-layers">The Layers in Testbook</h2>

| Layer | What it checks | Where it lives |
| --- | --- | --- |
| Lint | Obvious JSX problems while you type | `eslint-plugin-jsx-a11y` in the frontend |
| Component tests | axe on rendered components, plus a regression test for each fixed defect | `frontend/src/tests/accessibility/` |
| Token tests | Contrast of every design-token color pair, light and dark | `frontend/src/tests/accessibility/tokens.test.js` |
| E2E axe scans | Every route, key states, 320px width, dark mode | `tests/e2e/accessibility-axe.spec.js` |
| E2E behavior tests | Keyboard, focus, live regions, the accessibility tree | `tests/e2e/accessibility-behavior.spec.js` |
| Python mirror | The same E2E checks in pytest | `tests/e2e-python/test_accessibility.py` |
| Lighthouse CI | A score, including signed-in pages. A regression guard only. | `lighthouserc.js`, `tests/lighthouse/login.cjs` |
| Manual scripts | Keyboard, VoiceOver, NVDA, zoom, contrast, forms, content, pointer | [docs/a11y/manual/](../a11y/manual/README.md) |

Three more references:

- [Audit log](../a11y/AUDIT_LOG.md): the 20 defects found and fixed in Testbook, with the test that guards each one.
- [Worked examples](../a11y/WORKED_EXAMPLES.md): five defects walked through from symptom to guard test.
- [Pitfalls gallery](../../pitfalls/README.md): standalone pages showing how accessibility tests themselves go wrong.

---

<h2 id="running-tests">Running the Tests</h2>

```bash
# Component and token tests
cd frontend && npm run test:a11y

# E2E accessibility tests (app must be running: ./start-dev.sh)
cd tests && npm run test:a11y

# Both of the above
make test-a11y

# Lighthouse (app running, seeded data)
make lighthouse
```

```bash
# Python track (from tests/e2e-python, app running)
pytest -m a11y -v
```

For the JavaScript and Python differences in capability and workload, with measured numbers, see [JS vs Python accessibility testing](../a11y/JS_VS_PYTHON_ACCESSIBILITY_TESTING.md).

### In CI

- `frontend-tests.yml` runs the component and token tests.
- `accessibility.yml` runs the E2E suites and Lighthouse, and uploads the Playwright report (with the axe violation JSON) and the Lighthouse reports.
- `pitfalls.yml` runs the pitfalls gallery on its own, separate from the main suite.
- `markdown-validation.yml` runs a docs lint that fails on emoji, ASCII progress bars and vague link text, so the course docs stay readable with a screen reader.

---

<h2 id="axe-tags">Which axe Rules Run</h2>

The E2E scans use these tags: `wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa`, `wcag22aa` and `best-practice`. Keep `best-practice` in the list. Rules such as `landmark-one-main`, `region`, `page-has-heading-one` and `heading-order` carry only that tag, so a WCAG-only list silently skips them.

Two details that matter when you write your own:

- **Wait for animations to finish before scanning.** axe measures colors mid-fade during CSS transitions and reports false contrast failures. The shared helper waits until `document.getAnimations()` is empty.
- **Scan states, not only pages.** Open the menu, show the error, switch to dark mode, then scan.

---

<h2 id="common-fixes">Common axe Findings and Fixes</h2>

| Finding | Typical fix |
| --- | --- |
| Form elements must have labels | A visible `<label>` tied to the input. A placeholder is not a label. |
| Buttons must have discernible text | Visible text, or `aria-label` on an icon-only button. Hide decorative emoji with `aria-hidden="true"`. |
| Images must have alternative text | Meaningful `alt`, or `alt=""` for decorative images. |
| Insufficient color contrast | Adjust the color token, then confirm with the token test. Text needs 4.5:1, large text and UI components 3:1. |
| Heading levels should only increase by one | Fix the outline, and style headings with CSS rather than by level. |
| Page has no level-one heading or main landmark | One `<h1>` and one `<main>` per page. |

---

<h2 id="manual-checklist">Manual Checklist for a New Feature</h2>

Run the matching script from [docs/a11y/manual/](../a11y/manual/README.md) for anything beyond a trivial change.

- Operate every control with the keyboard alone, in a logical order, with a visible focus indicator.
- After opening, closing, saving or failing, focus goes somewhere sensible and is never lost.
- Errors and status changes are announced (live region or focus move).
- Zoom to 400% and check nothing is cut off or overlapping.
- Check both color themes, and check reduced-motion.
- Listen with a screen reader: VoiceOver on macOS and iOS, NVDA on Windows.
- Pointer targets are at least 24 by 24 CSS pixels, and dragging has an alternative.

Also add or update the component test and the E2E test, and add a regression test to the audit log if you fix a defect.

---

<h2 id="current-state">Current State</h2>

- **Automated:** 0 axe violations across the audited routes and states, and Lighthouse accessibility 100 on all six pages. A score of 100 does not mean accessible: several real defects passed Lighthouse before being found by other layers (see the audit log).
- **Fixed and guarded:** 20 defects, A11Y-001 to A11Y-020. Every guard test was confirmed to fail when its fix is reverted.
- **Not yet verified by a person:** the VoiceOver and NVDA scripts and a few other criteria. The conformance report lists these as "Not evaluated" rather than claiming them.

---

<h2 id="portfolio">For Your Portfolio</h2>

Describe what you proved and what you did not:

> "I added automated WCAG 2.2 AA testing to Testbook at three levels (component, browser, Lighthouse), fixed 20 real defects, and guarded each with a regression test I confirmed fails without the fix. I wrote scripted manual tests for the parts automation cannot judge, and an honest conformance report that marks unverified criteria as not evaluated."

See [PORTFOLIO.md](PORTFOLIO.md) and the Stage 5 conformance report artifact.

---

<h2 id="resources">Resources</h2>

- [WCAG 2.2 quick reference](https://www.w3.org/WAI/WCAG22/quickref/)
- [What's new in WCAG 2.2](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/)
- [axe-core](https://github.com/dequelabs/axe-core)
- [WebAIM](https://webaim.org/), including its [screen reader testing article](https://webaim.org/articles/screenreader_testing/)
- [The A11y Project](https://www.a11yproject.com/)
