# Accessibility Audit Log

**Target standard:** WCAG 2.2 Level AA
**Audit date:** 2026-10-04
**Status:** Phase 1 baseline. Every finding below is slated to be fixed, and each fix
gets a test that guards it. The columns **Fixed** and **Guarded by** are filled in as
the work lands.

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
| Defects found | 11 |
| Needs a human (manual script) | 3 |
| Checked and passing | 7 |

Why the existing suite was green: it scanned only 5 of 8 routes, only in their default
state, and none of the defects below that depend on state or on a human (focus loss,
reflow, titles, announcements) are things axe can see.

## Defects

| ID | Sev | WCAG | Where | Finding | Fixed | Guarded by |
| --- | --- | --- | --- | --- | --- | --- |
| A11Y-001 | High | 1.3.1, 3.3.2, 4.1.2 | Login, Register, CreatePost, comment input | Inputs have a placeholder and no `<label>` or `aria-label`. Placeholder disappears on input and is not a reliable name. axe accepts it, so this is invisible to automation. | | |
| A11Y-002 | High | 4.1.2, 1.3.1 | Post edit textarea | Edit-mode textarea has no accessible name at all. axe reports `label` (serious) once edit mode is open. | | |
| A11Y-003 | High | 1.3.5, 3.3.8 | Login, Register | No `autocomplete` tokens (`email`, `username`, `name`, `current-password`, `new-password`). Hurts password managers, which 3.3.8 relies on. | | |
| A11Y-004 | High | 4.1.3, 1.4.3 | Login error (and other `.error` blocks) | Error text is a plain `<div>`: not announced to screen readers. Its colour also fails contrast (axe `color-contrast`, serious). | | |
| A11Y-005 | High | 4.1.2, 2.1.1 | Post actions (25 on the feed) | A `<button>` nested inside an `<a>` for the "View" control: invalid interactive nesting, two tab stops per control. axe also flags it as `target-size` (the obscured inner button). | | |
| A11Y-006 | High | 4.1.2 | Post menu button, React/reaction buttons | Menu button is `⋯` with no name. `React ▼`/`😮 ▼` and the menu have no `aria-expanded`/`aria-haspopup`. Reaction buttons are emoji-only, so names depend on screen reader emoji dictionaries. | | |
| A11Y-007 | Med | 2.4.3, 3.2.1 | Post menu -> Edit; failed login | Focus drops to `<body>` when the menu closes after choosing Edit, and after a failed login (submit button disabled mid-request). Keyboard and screen reader users lose their place. | | |
| A11Y-008 | Med | 1.4.10 | All pages | Horizontal scroll at 320 px width (`scrollWidth` 396). | | |
| A11Y-009 | Med | 2.4.2 | All routes | Every route has the same `<title>`: "Testbook - Social Media for Testing". | | |
| A11Y-010 | Low | 2.4.1 | All authenticated pages | No skip link. A `<main>` landmark exists (so a technique is met), but there is a sticky 67 px navbar ahead of the content. | | |
| A11Y-011 | Low | 2.4.7, 1.4.11 | `.input:focus`, `.textarea:focus` | `outline: none`, leaving a 1 px border-colour change (#e0e0e0 -> #1264d0). Currently passes on contrast, but it is fragile and inconsistent with buttons, which keep the default ring. Use `:focus-visible` outline. | | |

## Needs manual verification

These are not failures yet. They need a human, so each has a script in `manual/`.

| ID | WCAG | Question |
| --- | --- | --- |
| A11Y-M01 | 4.1.3 | Are like/reaction counts, new comments and success/failure messages announced? No `aria-live`, `role=status` or `role=alert` exists anywhere in `frontend/src`, so the expectation is no. |
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
- **No `prefers-reduced-motion` rules.** The app's transitions are small colour
  changes. 2.3.3 is AAA, so this is out of scope. Noted as a possible future hardening.

## Tooling notes

- `frontend/` has axe-core 4.11 and `tests/` has 4.10.3. They should match.
- `frontend/package.json` lists `axe-playwright`, but the e2e suite uses
  `@axe-core/playwright`. The unused dependency should go.
