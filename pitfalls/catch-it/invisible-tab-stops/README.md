# Invisible Tab stops

**Shelf:** Catch it. There is a bug, and your job is to write the test that fails on it.

## What you are looking at

A post card with a **React** button. Press it and a row of reaction buttons (Like, Love,
Haha) appears. Nothing looks wrong on either page.

Now put the mouse away and press `Tab` repeatedly on the **broken** page. Three times,
focus vanishes: it lands on a control you cannot see. Do the same on the **fixed** page and
every stop is visible.

## Why the tests miss it

The picker is hidden with `opacity: 0; pointer-events: none`. That makes it transparent and
unclickable, but it is still in the page, still in the accessibility tree, and still
reachable with `Tab`. A default axe scan passes on both pages: axe inspects one snapshot,
and a transparent control is not a rule violation. A screenshot test passes too.

Only a test that **presses Tab and watches where focus goes** can see it.

## Where it came from

This is a real bug from Testbook: the reaction picker left six invisible Tab stops on every
post. It was found by reading the CSS, not by any scan. See
[audit finding A11Y-012](../../../docs/a11y/AUDIT_LOG.md) and
[Case 1 in the worked examples](../../../docs/a11y/WORKED_EXAMPLES.md).

## Who it affects

Keyboard-only users, switch users, and screen reader users. WCAG 2.4.7 (Focus Visible).

## The lesson

`opacity: 0` hides something visually. `visibility: hidden` and `display: none` hide it
from the keyboard and assistive technology too. Pick the property for the one you mean.

## Try it

```bash
npm install                         # once, in pitfalls/
npm run serve                       # open http://localhost:4100 and use the page by hand first
npm run exercise -- catch-it/invisible-tab-stops   # run YOUR test (exercise/) against both pages
npm run red -- catch-it/invisible-tab-stops        # watch the reference test fail on the broken page
npm test -- catch-it/invisible-tab-stops           # the reference solution, as CI runs it
```

Python track: `pip install -r requirements.txt`, then
`python3 -m pytest --exercises --show-red catch-it/invisible-tab-stops/exercise`.
