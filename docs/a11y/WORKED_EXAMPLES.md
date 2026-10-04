# Accessibility Worked Examples

Real bugs from Testbook's own accessibility audit, written up as case studies. Each
one passed the automated scan that was supposed to catch it. They are the best
argument for pairing automation with behaviour tests and manual checks, and they
are the source material for Lab 16 and Lab 17.

Each case has the same shape: the bug, why the scans passed, how it was found, the
fix, and the test that now guards it. The **Plant it** line at the end of each is
for a future deliberately-broken version of the site (see
[Seeds for a broken site](#seeds-for-a-broken-site)).

Audit IDs refer to [AUDIT_LOG.md](AUDIT_LOG.md).

---

## Case 1: Six invisible Tab stops on every post (A11Y-012)

**The bug.** The reaction picker (the row of emoji that appears when you press
"React") was hidden like this:

```css
.reactions-dropdown {
  opacity: 0;
  pointer-events: none;
}
```

It looks hidden, and a mouse cannot touch it. But `opacity: 0` only makes an element
transparent. It is still in the DOM, still in the accessibility tree, and still
focusable. Every post therefore added six Tab stops that landed on nothing visible.
A keyboard user tabbing down the feed pressed Tab six extra times per post with no
sign of where focus had gone, which fails WCAG 2.4.7 (Focus Visible).

**Why the scans passed.** axe-core inspects a snapshot of the DOM and its computed
styles. An element that is transparent and unclickable is not a rule violation, and
axe has no concept of "you pressed Tab and focus vanished". Lighthouse is built on
axe, so it passed too.

**How it was found.** By reading `Post.css` during the fixes for other bugs, not by
any scan. That is the honest lesson: nothing flagged it.

**The fix.**

```css
.reactions-dropdown {
  opacity: 0;
  visibility: hidden; /* removes it from the tab order and the accessibility tree */
  pointer-events: none;
  transition: opacity 0.15s ease, transform 0.15s ease, visibility 0s linear 0.15s;
}
.reactions-dropdown.show {
  opacity: 1;
  visibility: visible;
  transition-delay: 0s;
}
```

The `visibility 0s linear 0.15s` transition delays the hide until the fade-out
finishes, so the animation still looks right. On show, the delay is reset to zero so
the picker becomes focusable immediately.

**The guards, at two layers.**

- *Component test.* `a11y-regressions.test.jsx` asserts that
  `queryByRole('button', { name: 'Like' })` is `null` while the picker is closed and
  present once it is opened. This works in jsdom because Vitest is configured with
  `css: true`, so jsdom applies the real stylesheet. Testing Library excludes
  `visibility: hidden` elements from role queries, which is exactly the property we
  care about.
- *Browser test.* `accessibility-behavior.spec.js` presses Tab 40 times down the feed
  and asserts that no focused element has a `-reaction-` test id while every picker
  is closed.

**Takeaway.** "Visually hidden" and "hidden from assistive technology and the
keyboard" are different things. Pick the CSS property for the one you mean:

| Property | Hidden visually | Out of tab order | Out of a11y tree |
| --- | --- | --- | --- |
| `opacity: 0` | Yes | No | No |
| `visibility: hidden` | Yes | Yes | Yes |
| `display: none` | Yes | Yes | Yes |
| `.sr-only` (clip) | Yes | No | No (this is the point) |

**Plant it.** Revert the two lines above to `opacity: 0; pointer-events: none` and
nothing in the existing scans changes. Only the behaviour tests notice.

---

## Case 2: Hover and click fight over the reaction picker (A11Y-014)

**The bug.** The same picker was driven by two inputs that both wrote the same React
state:

```jsx
<div
  className="reactions-container"
  onMouseEnter={() => setShowReactions(true)}
  onMouseLeave={() => setShowReactions(false)}
>
  <button onClick={() => setShowReactions(!showReactions)}>React</button>
```

With a real mouse the sequence is: pointer enters (state becomes open), the user
clicks (state toggles to closed). The picker stays visible only because a separate
CSS `:hover` rule also shows it. So the picker is on screen while the button reports
`aria-expanded="false"`: the visible state and the exposed state disagree. A second
failure: a keyboard user who opens the picker with Enter, then happens to have a
pointer resting on the page, can have it closed by a stray `mouseleave`.

**Why the scans passed.** Every static snapshot is internally consistent. The bug
only exists in the transition between two inputs.

**How it was found.** Twice, by tests that were wrong for an instructive reason:

1. A Playwright test that opened the picker with Enter and pressed Tab sometimes
   landed on the wrong element. The cause was a resting pointer producing synthetic
   `mouseenter`/`mouseleave` events as the page scrolled, closing the picker mid-test.
2. A Vitest test of the Escape key passed, then turned out to be **vacuous**. It
   opened the picker with `user.click()`, which hovers first (opening it) and then
   clicks (closing it). So the picker was already closed when Escape was pressed, and
   the assertion "picker is closed after Escape" held trivially. It would have passed
   even with the Escape handler deleted.

The second one is the more valuable lesson. A test can be green because it never
exercised the code it names. The fix for the test was to drive the keyboard path
explicitly. The fix for the app removed the cause.

**The fix.** Hover-to-reveal is CSS only (`.reactions-container:hover`). React state
is written only by an explicit click, tap or key press, plus a click-outside handler
so it still closes when you click away. One writer means the state cannot disagree
with itself.

**The guards.**

- A mouse `click()` leaves the picker open and `aria-expanded="true"`.
- Hovering and then un-hovering does not close a picker opened by keyboard.
- Clicking elsewhere closes it.
- The Playwright version uses a real pointer: click, move away, assert still open,
  click elsewhere, assert closed.

Two of the three unit guards fail against the old code, confirmed by temporarily
restoring it. The third (click elsewhere) passes both ways, which is expected: it
protects behaviour that was added alongside the fix.

**A related timing note.** Tab skips elements that are not yet visible. The picker
fades in over 150 ms, so a test that presses Tab the instant `aria-expanded` flips
can race the fade. The browser test therefore waits for the first option to be
visible before tabbing. A sighted keyboard user always sees the picker open before
pressing Tab, so waiting models the real flow rather than papering over a bug.

**Takeaway.** Two writers to one piece of state is a bug factory, and it is
invisible to any test that checks only one input at a time. When a control responds
to both pointer and keyboard, test both, and test them in combination.

**Plant it.** Restore the `onMouseEnter`/`onMouseLeave` handlers. The component still
works for a mouse user at a glance, which is what makes it a good hidden bug.

---

## Case 3: A placeholder is not a label (A11Y-001)

**The bug.** Login, Register, the post composer and the comment box had inputs with
a `placeholder` and no `<label>` or `aria-label`.

**Why the scans passed.** axe-core accepts a non-empty placeholder as an accessible
name, so the `label` rule is satisfied. But a placeholder vanishes as soon as you
type, so a sighted user with a memory problem loses the field's purpose, and screen
readers handle placeholders inconsistently. WCAG 3.3.2 (Labels or Instructions)
needs a persistent label. This is a bug a tool is *allowed* to miss, because the
check it can make is weaker than the requirement.

**The fix.** Real `<label>` elements, visually hidden with the `.sr-only` utility
where the design shows only a placeholder. The placeholder text stays for sighted
users.

**The guard.** Tests find the fields with `getByLabelText`, which only works when a
real label exists. The point of the guard is the *query*: `getByPlaceholderText`
would have kept passing.

**Takeaway.** Prefer role-and-label queries in your tests. They fail when the markup
is inaccessible; test-id queries keep passing no matter what.

**Plant it.** Remove the `<label>` and keep the placeholder. axe stays green.

---

## Case 4: The error nobody heard (A11Y-004, A11Y-007)

**The bug.** A failed login rendered `<div class="error">Incorrect email or
password</div>`. Three separate problems in one element:

1. It was not announced. A screen reader user pressed Enter and heard nothing.
2. Its text colour failed contrast. This one axe *did* catch, but only once the error
   was on screen, and the original suite never scanned that state.
3. The submit button is disabled during the request, which drops focus to `<body>`,
   so even a sighted keyboard user lost their place.

**The fix.** An `Alert` component that renders `role="alert"` for errors and
`role="status"` for confirmations, and moves focus to form errors. The error colour
was darkened.

**The guards.** A component test checks the role and that focus lands on the alert.
A browser test submits a bad login with the keyboard alone and asserts the alert is
focused. An axe scan runs *with the error showing*.

**Takeaway.** Scan states, not just pages. Several of the 14 defects only existed once
something was open, expanded or in error.

**Plant it.** Replace `<Alert>` with a plain `<div className="error">`.

---

## What these four have in common

| Case | Passed axe? | What catches it |
| --- | --- | --- |
| Invisible Tab stops | Yes | Behaviour test: press Tab, watch focus |
| Hover vs click | Yes | Behaviour test with a real pointer |
| Placeholder as label | Yes | Role/label queries; manual review |
| Silent error | Partly | Scan the error state; assert focus and role |

None of the four is exotic. Each is a normal, plausible piece of UI code, and each
looks fine in a screenshot.

---

## Seeds for a broken site

For the future deliberately-broken variant of Testbook (a version where tests of
several kinds fail and the bugs are not obvious), these are ready-made accessibility
seeds. Each is subtle, passes a default axe scan, and is caught only by the layer
named. Pair them with seeds from the other test types.

| Seed | The change | Default axe scan | Caught by |
| --- | --- | --- | --- |
| Invisible Tab stops | `opacity: 0` instead of `visibility: hidden` on the reaction picker | Passes | Tab-order behaviour test |
| Hover/click state fight | Restore `onMouseEnter`/`onMouseLeave` writing the same state as `onClick` | Passes | Real-pointer test; `aria-expanded` check |
| Placeholder as label | Delete `<label>`, keep `placeholder` | Passes | `getByLabelText`; manual |
| Silent error | Plain `<div className="error">` instead of `<Alert>` | Passes (until the state is scanned) | Error-state scan; role assertion |
| Lost focus on close | Drop the focus-restore effects in `Post.jsx` | Passes | Focus-management tests |
| Button in a link | `<Link><button>View</button></Link>` | Fails `target-size` only | Nested-interactive check |
| Generic page title | Remove `useDocumentTitle` | Passes | Title test |
| Sticky header covers focus | Remove `scroll-padding-top` and enlarge the navbar | Passes | Focus-not-obscured test |

Design notes for whoever builds it:

- Keep each seed to a one- or two-line change so the diff is small and the bug is
  hard to spot.
- Prefer seeds that look like normal, defensible code. `opacity: 0` is something
  developers write every day.
- Give learners the failing test *names* but not the cause, and let them work backward
  from "which layer should have caught this?".
