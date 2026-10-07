# Lab 16 Coverage Key

Read this **after** you have filled in the coverage table in Lab 16, Part 5 (Part 6 in the Python version).

Each row shows the test that guards the defect, and what a person still has to judge. The "guard" is from the
[audit log](../../docs/a11y/AUDIT_LOG.md). File names are `tests/e2e/accessibility-axe.spec.js` (scans),
`tests/e2e/accessibility-behavior.spec.js` (behaviour) and `frontend/src/tests/accessibility/a11y-regressions.test.jsx` (unit).

| Audit ID | What guards it | Could it pass while a person struggles? | What a human judges |
| --- | --- | --- | --- |
| A11Y-001 | Locators by label throughout the suite, and unit tests | Yes: a label can exist and be unhelpful | Is the label's wording clear? |
| A11Y-002 | Axe scan with the edit box open | Less likely | Is "Edit post content" a good name? |
| A11Y-003 | Paste test and unit tests for the tokens | Yes: the tokens exist but a password manager may still misbehave | Does the password manager actually fill it? |
| A11Y-004 | Axe scan with the error showing, and the alert-and-focus test | Yes: the role is right, but is it spoken? | Is it announced, in good time, in words that help? |
| A11Y-005 | Unit test for nesting, and axe `target-size` | Unlikely | None |
| A11Y-006 | Keyboard test for the picker, and unit tests for names and state | Yes: a name exists | Is each name meaningful and not redundant? |
| A11Y-007 | Focus-management tests | Yes: focus moves, but to the right place? | Does focus feel sensible after each action? |
| A11Y-008 | The 320 px overflow test and the axe 320 px scans | Yes: no scrollbar is not the same as usable | Is it comfortable to use at 400% zoom? |
| A11Y-009 | The titles test | Yes: titles are distinct, but are they good? | Does each title say where you are? |
| A11Y-010 | The skip link test | Unlikely | None |
| A11Y-011 | The focus indicator test | Yes: the outline is thick, but is it noticeable? | Is the ring easy to see on every control? |
| A11Y-012 | The no-hidden-Tab-stops test | Unlikely | None |
| A11Y-013 | The announcement tests (the text) | **Yes**: the text is right, but is it spoken? | Is it heard, and does it make sense? |
| A11Y-014 | The real-pointer test | Unlikely | None |
| A11Y-015 | The aria-pressed test | Yes: the state exists | Is it announced in a way you understand? |
| A11Y-016 | The axe dark-theme scans and the token guard | Unlikely | Is dark mode comfortable, not just compliant? |
| A11Y-017 | The no-duplicate-ids test | Unlikely | None |
| A11Y-018 | The hover-and-Escape test | Unlikely | None |
| A11Y-019 | The unit tests and the browser test for the validation error | Yes: an alert appears, but is the message useful? | Does the message tell you what to fix? |
| A11Y-020 | The unit tests for names, and the browser test that reads the real accessibility tree of Feed, Settings and Profile | Unlikely | None |

## The pattern

Count the rows in the table above:

- **Eleven defects can pass their test while a person still struggles** (001, 003, 004, 006, 007, 008, 009, 011, 013, 015, 019).
  A test guards the *mechanism*, and only a person (or a real screen reader) can judge the *experience*. Most of these are about
  **names, announcements and focus**: the markup is right, and whether it is understandable is a human call.
- **Two are almost entirely mechanical**, with a small judgement left over (002 and 016).
- **Seven are fully mechanical** (005, 010, 012, 014, 017, 018, 020). A test owns them completely, and a human adds nothing.
- Eleven plus two plus seven is twenty.
- **Nothing here is caught by a scan alone.** The behaviour tests and the human pass fill what a snapshot cannot.

That gap is why Lab 17 exists.
