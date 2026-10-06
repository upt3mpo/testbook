# Accessibility testing: JavaScript and Python compared

The same accessibility suite exists in both tracks: 50 tests in each, covering the same routes,
states, themes, widths and behaviours, written from the same checklist. This page records what is
genuinely different between the two, so you can choose a track (or compare them) with facts.

Numbers marked **measured** come from this repository. Numbers marked **estimated** are judgement,
not measurement, and are labelled so.

## The two suites

| | JavaScript | Python |
| --- | --- | --- |
| Scans and behaviour tests | `tests/e2e/accessibility-axe.spec.js`, `tests/e2e/accessibility-behavior.spec.js` | `tests/e2e-python/test_accessibility.py` |
| Shared helper | `tests/e2e/fixtures/a11y.js` | `tests/e2e-python/a11y.py` |
| Number of tests (measured) | 50 | 50 |
| Lines of test code (measured) | 584 | 548 |
| Lines in the helper (measured) | 68 | 81 |
| Run time for all 50, serial (measured) | about 2.4 minutes | about 2.3 minutes |
| Run only these tests | `npm run test:a11y` or `--grep @a11y` | `pytest -m a11y` |

The two are close enough in size and speed that neither is a burden. The differences that matter
are in capability and in who maintains what.

## Capability differences

| Area | JavaScript | Python |
| --- | --- | --- |
| **axe integration** | An official package, `@axe-core/playwright`, with an `AxeBuilder`: choose tags and rules, include or exclude parts of the page, and it analyses iframes for you | No official integration. Community packages exist, but this repo injects the axe-core script and calls `axe.run()` directly: about 15 lines you own |
| **Where the axe version comes from** | The `axe-core` version pinned in `tests/package.json` | The copy in `frontend/node_modules`, so it always matches the frontend's own tests, but you need the frontend's dependencies installed |
| **iframes** | Handled by the integration | Not handled by a simple injection. A page with iframes needs extra work (injecting axe into each frame) |
| **Attaching the full report** | `testInfo.attach()` puts the axe JSON in the Playwright HTML report | The helper writes the JSON to `test-results/a11y/` instead. There is no HTML report attachment without adding a plugin |
| **Failure message** | A custom message on the `expect` | A custom message on the `assert`. Equivalent |
| **Selecting tests** | Tags: `{ tag: '@a11y' }`, `--grep @a11y` | Markers: `@pytest.mark.a11y`, `-m a11y` (registered in `pytest.ini`) |
| **Locators and web-first assertions** | `getByRole`, `getByLabel`, `expect(...).toBeFocused()` | `get_by_role`, `get_by_label`, `expect(...).to_be_focused()`. The same engine, the same retrying assertions |
| **Cross-browser** | Projects in `playwright.config.js`. Switching engine is a flag | The shared fixtures launch Chromium only. Other engines are launched from the shared `playwright_instance` fixture inside the test |
| **Waiting for animations before a scan** | `page.waitForFunction(...)` | `page.wait_for_function(...)`. Identical |

## Workload differences

| Task | JavaScript | Python |
| --- | --- | --- |
| Write the scanning helper | Install a package, write about 10 lines | Write about 15 lines to inject and run the script. This is the main extra work, and Lab 16 has Python learners do it |
| Add a scan of a new page or state | One line with the helper | One line with the helper |
| Write a keyboard test | Equal | Equal |
| Keep axe up to date | `npm update` | Update the frontend's copy. Nothing in Python to change |
| Get a readable failure report | Open the Playwright HTML report | Open the JSON file, or read the assertion message |

**Estimated** time for Lab 16: about 100 minutes in JavaScript and about 115 minutes in Python, the
difference being the helper that Python learners write themselves. These are estimates, not
measurements. Record your own times in the lab checklist.

## What is identical

- The checks themselves. A contrast failure, a missing landmark, a lost focus and a hidden Tab stop
  are caught the same way in both.
- The standard: WCAG 2.2 AA plus axe's best-practice rules, from one list in one helper.
- The speed, in practice.
- What neither can see. The same defects need a human in both tracks. See Lab 17.

## Which should you use?

- **Join a team already using one:** use theirs. The capability gap is small enough that this
  matters more than the language.
- **Starting fresh, accessibility-heavy, many pages with iframes or third-party widgets:** the
  JavaScript integration saves real work.
- **A Python shop with an existing pytest suite:** the Python helper is small, and keeping one
  language is worth more than the missing integration.

Either way, learn the *ideas* (one helper owns the standard, scan states and not just pages, wait
for the page to settle, pair scans with behaviour tests). They carry across.
