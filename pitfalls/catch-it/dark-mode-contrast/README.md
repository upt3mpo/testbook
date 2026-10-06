# The theme nobody scanned

**Shelf:** Catch it.

## What you are looking at

A settings page with a **Dark theme** toggle and a primary **Save settings** button. In the
default light theme both pages look fine and pass every check.

Switch to dark. On the **broken** page the white text on the blue button becomes hard to
read. A contrast checker measures it at 3.45:1, and WCAG needs 4.5:1. The **fixed** page uses
a darker blue behind white text in dark mode and passes.

## Why the tests miss it

Unlike the other pitfalls, **axe can catch this one**, but only if you ask in the right
state. The default scan runs in the default (light) theme, where there is nothing wrong. The
suite was green about a state the user can leave at any time.

The cause is a design-token mistake worth recognising: one colour variable did two jobs, as
text on the page background (wants a light blue on dark) and as a fill behind white text
(wants a dark blue). One variable cannot satisfy both.

## Where it came from

A real Testbook bug: dark mode had never been scanned and several buttons failed. See
[A11Y-016](../../../docs/a11y/AUDIT_LOG.md) and
[Case 5 in the worked examples](../../../docs/a11y/WORKED_EXAMPLES.md).

## Who it affects

People with low vision, and anyone reading in bright light. WCAG 1.4.3 Contrast (Minimum).

## The lesson

Every theme, mode or preference a user can switch is **another state to test**: dark mode,
high contrast, large text. Reach the state first, then scan it. And give distinct design
roles distinct tokens.

## Try it

```bash
npm install                         # once, in pitfalls/
npm run serve                       # open http://localhost:4100 and use the page by hand first
npm run exercise -- catch-it/dark-mode-contrast   # run YOUR test (exercise/) against both pages
npm run red -- catch-it/dark-mode-contrast        # watch the reference test fail on the broken page
npm test -- catch-it/dark-mode-contrast           # the reference solution, as CI runs it
```

Python track: `pip install -r requirements.txt`, then
`python3 -m pytest --exercises --show-red catch-it/dark-mode-contrast/exercise`.
