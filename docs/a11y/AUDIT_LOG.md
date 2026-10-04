# Accessibility Audit Log

**Target standard:** WCAG 2.2 Level AA
**Audit date:** 2026-10-04
**Status:** All 13 defects fixed and guarded by tests (2026-10-04). Phase 2 manual
scripts cover what automation cannot (see "Needs manual verification").

## Method

The baseline was gathered against the running app (Chromium, 1280x800 unless noted,
seed data from `/api/dev/reset`, signed in as `sarah.johnson@testbook.com`):

1. axe-core 4.10 scans with tags `wcag2a, wcag2aa, wcag21a, wcag21aa, wcag22aa,
   best-practice` on all 8 routes in their default state.
2. axe scans of **interaction states** the existing suite never visits: post menu
   open, post edit mode, comment box open, reaction picker open, login error shown.
3. Scripted checks for criteria axe cannot decide: tab order and focus loss, focus
   obscured by the sticky navbar (120 consecutive Tab presses on the feed), target
   sizes, accessible names, 320 px reflow, page titles, live regions.

## Summary

| Result | Count |
| --- | --- |
| Defects found | 13 (11 from the scans, 2 found while fixing) |
| Needs a human (manual script) | 3 |
| Checked and passing | 7 |

Why the existing suite was green: it scanned only 5 of 8 routes, only in their default
state, and none of the defects below that depend on state or on a human (focus loss,
reflow, titles, announcements) are things axe can see.

## Defects

All 13 are fixed, each with a guarding test. "Guarded by" names the file; every
guard was confirmed to fail against the pre-fix code (22 of 26 new component tests
and 21 browser tests fail without the fixes; the remainder cover new components).

| ID | Sev | WCAG | Where | Finding | Fixed | Guarded by |
| --- | --- | --- | --- | --- | --- | --- |
| A11Y-001 | High | 1.3.1, 3.3.2, 4.1.2 | Login, Register, CreatePost, comment input | Inputs have a placeholder and no `<label>` or `aria-label`. Placeholder disappears on input and is not a reliable name. axe accepts it, so this is invisible to automation. | Yes: `<label class="sr-only">` on Login, Register and CreatePost; `aria-label` on the per-post comment input | a11y-regressions.test.jsx (A11Y-001); axe specs |
| A11Y-002 | High | 4.1.2, 1.3.1 | Post edit textarea | Edit-mode textarea has no accessible name at all. axe reports `label` (serious) once edit mode is open. | Yes: `aria-label="Edit post content"` | a11y-regressions.test.jsx (A11Y-002); axe "post in edit mode" |
| A11Y-003 | High | 1.3.5, 3.3.8 | Login, Register | No `autocomplete` tokens (`email`, `username`, `name`, `current-password`, `new-password`). Hurts password managers, which 3.3.8 relies on. | Yes: `autoComplete` tokens on all auth fields | a11y-regressions.test.jsx (A11Y-003); accessibility-behavior.spec.js (paste) |
| A11Y-004 | High | 4.1.3, 1.4.3 | Login error (and other `.error` blocks) | Error text is a plain `<div>`: not announced to screen readers. Its colour also fails contrast (axe `color-contrast`, serious). | Yes: New `Alert` component: `role=alert`/`status`, focus on form errors; error text colour darkened (`--error-text`) | a11y-regressions.test.jsx (A11Y-004); accessibility-behavior.spec.js; axe "login/register error" |
| A11Y-005 | High | 4.1.2, 2.1.1 | Post actions (25 on the feed) | A `<button>` nested inside an `<a>` for the "View" control: invalid interactive nesting, two tab stops per control. axe also flags it as `target-size` (the obscured inner button). | Yes: "View", "Create New Account" and "Log In" links are now single `<Link class="btn">` elements | a11y-regressions.test.jsx (A11Y-005); axe feed scans (`target-size`) |
| A11Y-006 | High | 4.1.2 | Post menu button, React/reaction buttons | Menu button is `⋯` with no name. `React ▼`/`😮 ▼` and the menu have no `aria-expanded`/`aria-haspopup`. Reaction buttons are emoji-only, so names depend on screen reader emoji dictionaries. | Yes: `aria-label`, `aria-expanded`, `aria-controls`, `aria-pressed` on menu, react and reaction buttons; Post is an `<article>` with a name | a11y-regressions.test.jsx (A11Y-006); accessibility-behavior.spec.js |
| A11Y-007 | Med | 2.4.3, 3.2.1 | Post menu -> Edit; failed login | Focus drops to `<body>` when the menu closes after choosing Edit, and after a failed login (submit button disabled mid-request). Keyboard and screen reader users lose their place. | Yes: Focus moves into edit/comment on open and back to the opener on close; Escape closes menus; delete parks focus on `<main>` | a11y-regressions.test.jsx (A11Y-007); accessibility-behavior.spec.js |
| A11Y-008 | Med | 1.4.10 | All pages | Horizontal scroll at 320 px width (`scrollWidth` 396). | Yes: Navbar menu wraps; long values wrap in Profile and Settings | accessibility-behavior.spec.js (A11Y-008); axe @320px |
| A11Y-009 | Med | 2.4.2 | All routes | Every route has the same `<title>`: "Testbook - Social Media for Testing". | Yes: `useDocumentTitle` hook on every page | a11y-regressions.test.jsx (A11Y-009); accessibility-behavior.spec.js (A11Y-009) |
| A11Y-010 | Low | 2.4.1 | All authenticated pages | No skip link. A `<main>` landmark exists (so a technique is met), but there is a sticky 67 px navbar ahead of the content. | Yes: Skip link in the authenticated layout; `<main id="main-content" tabindex="-1">` | accessibility-behavior.spec.js (A11Y-010) |
| A11Y-011 | Low | 2.4.7, 1.4.11 | `.input:focus`, `.textarea:focus` | `outline: none`, leaving a 1 px border-colour change (#e0e0e0 -> #1264d0). Currently passes on contrast, but it is fragile and inconsistent with buttons, which keep the default ring. Use `:focus-visible` outline. | Yes: Global `:focus-visible` 3px outline; removed `outline: none` from inputs | accessibility-behavior.spec.js (A11Y-011) |
| A11Y-012 | High | 2.4.7, 2.1.1 | Reaction picker (every post) | The closed picker was hidden with `opacity: 0; pointer-events: none`, so its 6 emoji buttons stayed in the Tab order while invisible: 6 invisible Tab stops per post. axe cannot see this. Found while reading `Post.css`, not by a scan. | Yes: `visibility: hidden` when closed | a11y-regressions.test.jsx (A11Y-012); accessibility-behavior.spec.js (A11Y-012) |
| A11Y-013 | Med | 4.1.3 | Whole app | No live region anywhere, so reactions, reposts, comments, deletions and client-side page changes produced no announcement. | Yes: `LiveRegion` + `announce()`, route announcer | a11y-regressions.test.jsx (A11Y-013); accessibility-behavior.spec.js (A11Y-013) |

## Needs manual verification

These are not failures yet. They need a human, so each has a script in `manual/`.

| ID | WCAG | Question |
| --- | --- | --- |
| A11Y-M01 | 4.1.3 | Do screen readers actually speak the announcements added for A11Y-013, and is the wording useful? The live region's text is tested; the spoken result is not testable without a screen reader. |
| A11Y-M02 | 1.4.3 | axe returns `color-contrast` as *incomplete* on the feed (5 nodes), register, settings and profile: the textarea background is partly obscured, and the `⋯` menu is non-text. A contrast tool must settle these. |
| A11Y-M03 | 2.5.8 | Spacing exceptions on small controls. axe's check has exceptions that need a human to confirm. |

## Checked and passing

| WCAG | Result |
| --- | --- |
| 2.4.11 Focus Not Obscured | 120 Tab presses on the feed with the sticky 67 px navbar: no focused element's centre was covered. Adding `scroll-padding-top` is hardening, with a regression test. |
| 2.5.7 Dragging Movements | N/A: no drag interactions. |
| 3.2.6 Consistent Help | N/A: no help mechanism. |
| 3.3.7 Redundant Entry | N/A: no multi-step flow re-asks for data. |
| 2.5.8 Target Size, other controls | No other control under 24x24 CSS px on the feed. |
| 3.1.1 Language | `<html lang="en">` present. |
| Landmarks, headings, `alt` text | 0 axe violations on all 8 routes' default states after the 2026-09 fixes. |

## Not defects (decisions)

- **Native `alert()` and `confirm()`.** Browsers expose these to assistive technology
  correctly, so they are not WCAG failures. Replacing them would also break existing
  tests that handle dialogs. Leave as is. Revisit only if the app grows a design
  system.
- **User-uploaded images have the generic alt text "Post content".** Fixing this needs
  a feature (an alt-text field when posting), not a bug fix. Left as is; the manual
  `alt` quality script covers it.
- **No `prefers-reduced-motion` rules.** The app's transitions are small colour
  changes. 2.3.3 is AAA, so this is out of scope. Noted as a possible future hardening.

## Tooling notes

- `frontend/` had axe-core 4.11 and `tests/` had 4.10.3. Both are now on 4.13.
- `frontend/package.json` listed `axe-playwright`, but nothing used it (the e2e suite
  uses `@axe-core/playwright`). Removed.
- `jsx-a11y/click-events-have-key-events` and `no-static-element-interactions` are now
  lint errors, not warnings. `media-has-caption` stays a warning: users upload the
  videos, so there are no captions to supply.
