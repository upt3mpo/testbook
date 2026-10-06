# The hover and click fight

**Shelf:** Catch it.

## What you are looking at

A **React** button that reveals a picker, either when you hover over it or when you click
it. On both pages it looks fine with the mouse.

Click the button on the **broken** page and then ask what it reports: `aria-expanded` says
**false** while the picker is on screen. On the **fixed** page it says **true**.

## Why the tests miss it

A real mouse hovers *before* it clicks. Here both inputs write the same piece of state:
hover sets it open, then the click toggles it closed. The picker stays visible only because
a separate CSS rule also shows it on hover. So what the screen shows and what assistive
technology is told disagree.

Every static snapshot is internally consistent, so an axe scan passes on both pages. The bug
only exists in the **transition between two inputs**. Leaving the picker also closes one that
a keyboard user opened.

## Where it came from

A real Testbook bug, found when a keyboard test behaved inconsistently. See
[A11Y-014](../../../docs/a11y/AUDIT_LOG.md) and
[Case 2 in the worked examples](../../../docs/a11y/WORKED_EXAMPLES.md).

## Who it affects

Screen reader users (WCAG 4.1.2 Name, Role, Value) and keyboard users (2.1.1).

## The lesson

Two writers to one piece of state is a bug factory, and it is invisible to any test that
exercises one input at a time. When a control responds to both pointer and keyboard, test
both, and test them in combination.

## Try it

```bash
npm install                         # once, in pitfalls/
npm run serve                       # open http://localhost:4100 and use the page by hand first
npm run exercise -- catch-it/hover-click-fight   # run YOUR test (exercise/) against both pages
npm run red -- catch-it/hover-click-fight        # watch the reference test fail on the broken page
npm test -- catch-it/hover-click-fight           # the reference solution, as CI runs it
```

Python track: `pip install -r requirements.txt`, then
`python3 -m pytest --exercises --show-red catch-it/hover-click-fight/exercise`.
