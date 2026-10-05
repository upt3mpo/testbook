# Run: machine-executed preview (not a human pass)

> **This is not a completed manual run.** It records the measurements from the cases that
> can be executed by script, taken while the scripts were being written, so the scripts'
> expected results were checked against the real app. Every case that needs a human
> (screen readers, judgement of wording, voice control, touch) is **not run** and is marked
> so. A human pass on VoiceOver and NVDA is still to be done and should use a fresh copy of
> [the run sheet template](../RUN_SHEET_TEMPLATE.md).

| Field | Value |
| --- | --- |
| Date | 2026-10-04 |
| Executed by | Playwright / axe-core scripts (no human, no screen reader) |
| Browser | Chromium (Playwright), 1280x800 unless stated |
| App state | Database reset, signed in as `sarah.johnson@testbook.com` |

## Cases executed

| Case | Result | What was measured |
| --- | --- | --- |
| ZM-02 | Pass | No horizontal overflow at 320 px on Feed, Settings, Profile, Post detail |
| ZM-05 | Pass | With line-height 1.5, letter-spacing 0.12em, word-spacing 0.16em: nothing clipped on Feed, Settings, Profile, Login (the only "clipped" nodes were the intentionally hidden `.sr-only` labels) |
| PT-01 | Pass (2.5.8) | Every control on the feed is at least 24x24 px. Controls under the more comfortable 44 px are listed below (Low) |
| PT-03 | Pass | Pressing down on Repost, dragging off, and releasing elsewhere did **not** fire the action |
| CC-04 | Pass | Focus ring is 3 px with a 2 px offset on every control tested, **5.59:1** against the page in light and **5.09:1** in dark (needs 3:1) |
| CC-06 | Pass (axe) | Seven dark-theme axe scans pass (see the audit log, A11Y-016) |
| KB-04, KB-05, KB-06, KB-07, KB-08, KB-10 | Covered by automation | See `accessibility-behavior.spec.js`; still worth a human pass for focus *visibility* |

Controls under 44 px (Low, comfort only, not a WCAG 2.2 AA failure): navbar logo
120x42, Home 74x39, Profile 79x39, Settings 92x39, Logout 83x33, Feed tabs 337x37,
Add Media 130x41, Post 65x33, post author link 614x24, React 92x33, reaction options
42x35, Comment 101x39, Repost 83x39, View 67x39, post menu 47x31.

## Cases not run (need a human)

KB-01 to KB-03, KB-09, KB-11, KB-12 (visual judgement); SR-01 to SR-12 on both screen
readers; ZM-01, ZM-03, ZM-04, ZM-06 (by eye); CC-01 to CC-03, CC-05, CC-07; FM-01 to
FM-07; CT-01 to CT-06; PT-02, PT-04, PT-05.

## Findings

Executing these cases found two things worth logging, both already fixed and recorded in
the [audit log](../../AUDIT_LOG.md): **A11Y-016** (dark-theme contrast) and **A11Y-018**
(hover-revealed picker not dismissible with Escape). No other open findings.
