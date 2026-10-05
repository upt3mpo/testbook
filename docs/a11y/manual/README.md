# Manual Accessibility Test Suite

Scripted manual tests for the parts of WCAG 2.2 AA that no tool can decide. Automation
([axe-core, Playwright behaviour tests, Lighthouse](../../guides/ACCESSIBILITY_TESTING.md))
catches roughly a third of accessibility problems. The rest need a person: what a screen
reader actually says, whether a focus order makes sense, whether an error message is
useful, whether the page is still usable at 400% zoom.

These scripts turn that person's judgement into a repeatable procedure with expected
results, so two testers get comparable answers.

## The scripts

| # | Script | Time | WCAG focus | What only a human can judge |
| --- | --- | --- | --- | --- |
| 01 | [Keyboard](01_KEYBOARD.md) | 25 min | 2.1.1, 2.1.2, 2.4.1, 2.4.3, 2.4.7, 2.4.11 | Is the order logical? Is focus ever lost or hidden? |
| 02 | [Screen reader: VoiceOver + Safari](02_SCREEN_READER_VOICEOVER.md) | 45 min | 1.3.1, 4.1.2, 4.1.3 | Do the announcements make sense? |
| 03 | [Screen reader: NVDA + Firefox](03_SCREEN_READER_NVDA.md) | 45 min | 1.3.1, 4.1.2, 4.1.3 | Same, on the most-used Windows reader |
| 04 | [Zoom, reflow and text spacing](04_ZOOM_REFLOW.md) | 20 min | 1.4.4, 1.4.10, 1.4.12 | Is it still usable, not just free of scrollbars? |
| 05 | [Contrast, colour and motion](05_CONTRAST_COLOR_MOTION.md) | 25 min | 1.4.1, 1.4.3, 1.4.11, 2.3.3 | Contrast of states a tool cannot reach |
| 06 | [Forms and errors](06_FORMS_ERRORS.md) | 25 min | 1.3.5, 3.3.1-3.3.4, 3.3.8 | Are errors understandable and recoverable? |
| 07 | [Content and cognitive](07_CONTENT_COGNITIVE.md) | 20 min | 2.4.2, 2.4.4, 2.4.6, 1.1.1, 3.1.1 | Is the wording and alt text meaningful? |
| 08 | [Pointer and target size](08_POINTER_TARGETS.md) | 15 min | 2.5.1, 2.5.7, 2.5.8 | Can it be used without precision or gestures? |

Also read [Screen reader comparison](SCREEN_READER_COMPARISON.md) before choosing which
reader to start with. Total for a full pass: about 3.5 hours.

## What the automated tests already cover

Do not re-test these by hand. They run in CI. Each script says where it overlaps.

- axe-core on every route, in default, interaction, dark-theme and 320 px states.
- Tab order of the login form; focus moving into and out of the post menu, edit box and
  comment box; the skip link; focus not hidden behind the sticky navbar.
- Page titles, announcements written to the live region (the *text*, not the speech).
- No horizontal scroll at 320 px; no controls under 24x24 px on the feed.

What automation **cannot** check, and these scripts do: whether the live region is
actually *spoken*, whether the spoken text is understandable, whether the order is
sensible rather than merely stable, and anything about colour that axe marks
"incomplete".

## Before you start

1. Start the app (`./start-dev.sh`, or `make start`) and open <http://localhost:3000>.
2. Reset to known data before **every** script:

   ```bash
   curl -X POST http://localhost:8000/api/dev/reset
   ```

3. Use the seed account `sarah.johnson@testbook.com` / `Sarah2024!` unless a script says
   otherwise. A second account (`mike.chen@testbook.com` / `MikeRocks88`) is useful for
   follow/block tests.
4. Copy [RUN_SHEET_TEMPLATE.md](RUN_SHEET_TEMPLATE.md) to `runs/YYYY-MM-DD-<tester>.md`
   and fill it in as you go. One run sheet per full pass.
5. Note your environment (OS, browser and version, screen reader and version). Results
   differ across them, and that is information, not noise.

## How to read a test case

Every case has an ID (for example `KB-07`), numbered steps, and an **Expected** result.
Mark it Pass, Fail, or N/A in the run sheet.

- **Pass:** every point under Expected is true.
- **Fail:** any point is false. Write down what actually happened, exactly.
- **Blocked:** you could not run it (for example the feature is missing). Say why.

Expected results describe the *information* that must be available, not exact wording.
Screen readers phrase things differently across products and versions. Judge: "did I get
the name, the role, and the state?" not "did it say precisely this sentence?".

## Severity

| Level | Meaning | Example |
| --- | --- | --- |
| **Blocker** | A user cannot complete a core task | Cannot reach Login's submit button by keyboard |
| **High** | The task is possible but needs a workaround or guessing | Error appears but is never announced |
| **Medium** | Degraded experience, task still clear | Page change not announced, title still tells you |
| **Low** | Polish or best practice | Link text could be more descriptive |

## Reporting a failure

A good accessibility bug report names the person who is blocked, not just the rule.
Use this shape:

```text
Title: <page> - <what is wrong> (<WCAG criterion>)
Environment: <OS / browser / screen reader + versions>
Steps: <numbered, from a reset database>
Expected: <what should happen>
Actual: <what happened, quoting the screen reader output if relevant>
Who it affects: <keyboard-only / screen reader / low vision / motor / cognitive users>
Severity: <Blocker | High | Medium | Low>
Suggested fix: <optional>
```

Add each confirmed failure to [../AUDIT_LOG.md](../AUDIT_LOG.md) with the next `A11Y-NNN`
ID, fix it, and add the test that guards it. A manual finding is not done until an
automated test exists for whatever part of it *can* be automated.

## Keeping these scripts honest

- When the UI changes, update the affected steps in the same pull request.
- If a manual check can be automated (it turned out to be deterministic), move it into
  `tests/e2e/accessibility-behavior.spec.js` and delete it here. Manual time is for what
  needs judgement.
- Record the date and the app version you last ran each script against in the run sheet.
