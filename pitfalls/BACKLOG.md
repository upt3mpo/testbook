# Pitfalls backlog

Ideas for future pitfalls, so they are not lost. **Nothing here is built.** The rule is to
build a pitfall when the lesson that needs it is written, not before: that way it is shaped
by the lesson, and the collection never fills with pitfalls nobody uses. When you build one,
move it into `README.md` and delete its row here.

How to read the table: **Shelf** is where it goes, **Needed by** is the lesson most likely
to want it, and **Source** says whether it is a real Testbook finding (preferred, link it) or
a common failure seen elsewhere.

## Accessibility

| Shelf | Slug | What it teaches | Needed by | Source |
| --- | --- | --- | --- | --- |
| Catch it | `sticky-header-covers-focus` | A fixed header can hide the focused control (WCAG 2.4.11); only tabbing the whole page shows it | Stage 3 keyboard lab, Lab 16 | Testbook: sticky navbar, fixed with `scroll-padding-top`; see the manual keyboard script (KB-10) |
| Catch it | `no-reflow-at-320` | A page that scrolls sideways at 320 px (WCAG 1.4.10); axe cannot see layout | Lab 16 | Testbook: A11Y-008 |
| Catch it | `emoji-only-names` | Controls named by an emoji are announced differently per platform, and axe accepts them | Stage 0 part 1, Lab 17 | Testbook: A11Y-006 (reaction buttons) |
| Catch it | `outline-none` | Removing the focus outline leaves keyboard users blind (WCAG 2.4.7); fragile replacements | Stage 0 part 1 | Testbook: A11Y-011 |
| Catch it | `error-not-tied-to-field` | An error message is shown but not associated with its field (`aria-describedby`, `aria-invalid`) | Lab 17 forms script | Testbook: judgement call in the forms script (FM-03) |
| Catch it | `crash-on-error-shape` | An API error shape the UI did not expect (a list instead of a string) blanks the whole page; a contract test on error shapes, and a boundary, are the defences | Stage 2 labs (error responses) | Testbook: A11Y-019 |
| Catch it | `tiny-targets` | Controls under 24x24 px (WCAG 2.5.8); axe has exceptions that need a human | Lab 16 | Testbook: target-size results and manual script PT-01 |
| Catch it | `skip-link-missing` | Repeated navigation with no way to bypass it (WCAG 2.4.1) | Stage 0 part 1 | Testbook: A11Y-010 |
| Catch it | `text-spacing-clips` | Text clipped when a user overrides line, letter and word spacing (WCAG 1.4.12) | Lab 17 zoom script | Common; manual script ZM-05 |
| Trust it? | `screenshot-passes-everything` | A visual-regression test is green while the page is unusable by keyboard | Stage 3 | Common |
| Trust it? | `green-axe-means-accessible` | A page that passes a default axe scan yet fails several of the other pitfalls | Stage 0 part 3 | Testbook: the original suite reported zero violations while 18 defects existed |

## Other test types (a separate, later project)

These belong to the other stages, not to the accessibility initiative. Listed so the
"how tests fail" idea has a home.

| Shelf | Slug | What it teaches | Needed by | Source |
| --- | --- | --- | --- | --- |
| Trust it? | `fixed-sleep-instead-of-wait` | A test that passes only because a sleep happens to be long enough | Stage 3 flaky tests | Common; see `docs/guides/FLAKY_TESTS_GUIDE.md` |
| Trust it? | `assertion-never-runs` | An assertion inside a callback or after a missing `await` that never executes | Stage 1 | Common |
| Trust it? | `mocked-away-the-bug` | Over-mocking: the test verifies the mock, not the code | Stage 2 | Common; see `docs/concepts/TESTING_ANTIPATTERNS.md` |
| Trust it? | `order-dependent-tests` | Two tests pass alone and fail together, or the reverse, because of shared state | Stage 1 | Common |
| Catch it | `contract-drift` | A backend renames a field and every unit test still passes | Stage 2 contract lab | Common |
| Catch it | `idor-on-saved-posts` | A user can read another user's private list by changing an id | Stage 4 security | Common; the capstone ticket's security requirement |
| Trust it? | `latency-threshold-on-the-average` | A performance threshold set on the mean hides a terrible tail | Stage 4 load testing | Common |

## Conventions to keep

- Keep the broken and fixed pages different in the **smallest** way that shows the lesson.
- Everything except the one bug must stay correct (the catalog test checks the basics).
- Measure what the usual tools say about the broken page **before** claiming what they miss.
  One earlier draft claimed axe catches a nameless button; it does not, and the README was
  wrong until it was measured.
- Write the JavaScript and Python solutions together, and the exercise skeletons with them.
