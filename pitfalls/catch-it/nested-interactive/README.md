# A button inside a link

**Shelf:** Catch it.

## What you are looking at

A post card with **Comment** and **View** controls. They look identical on both pages.

Now press `Tab` on the **broken** page. It stops on **View**, and then stops on **View
again**. On the **fixed** page it stops once.

## Why the tests miss it

The broken page wraps a `<button>` in an `<a>`. Both are focusable, so one control became two
Tab stops (and two things to activate). It is invalid HTML, but axe has no rule that flags
this particular nesting: every element has a name and a role, so every snapshot check passes.
A screenshot looks the same.

Only a test that **walks the Tab order and counts** can see it.

## Where it came from

A real Testbook bug: every post's "View" control was a button inside a link, 25 times on the
feed. See [A11Y-005](../../../docs/a11y/AUDIT_LOG.md).

## Who it affects

Keyboard users (an extra, redundant stop on every post) and screen reader users (the control
is announced twice). WCAG 4.1.2 Name, Role, Value.

## The lesson

Pick **one** interactive element per control. A link that looks like a button should be a
link styled as a button, not a button wrapped in a link.

## Try it

```bash
npm install                         # once, in pitfalls/
npm run serve                       # open http://localhost:4100 and use the page by hand first
npm run exercise -- catch-it/nested-interactive   # run YOUR test (exercise/) against both pages
npm run red -- catch-it/nested-interactive        # watch the reference test fail on the broken page
npm test -- catch-it/nested-interactive           # the reference solution, as CI runs it
```

Python track: `pip install -r requirements.txt`, then
`python3 -m pytest --exercises --show-red catch-it/nested-interactive/exercise`.
