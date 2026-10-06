# Lost focus

**Shelf:** Catch it.

## What you are looking at

A post with a **Post options** menu. Open it with the keyboard and choose **Edit**: the menu
closes and an edit box appears. On both pages that is what you see.

On the **broken** page, look at where keyboard focus went. It disappeared: the Edit button
you just pressed no longer exists, so focus fell back to the top of the page. Press `Tab` and
you start from the beginning. On the **fixed** page focus is in the edit box, and closing the
editor puts focus back on the menu button.

## Why the tests miss it

Focus is something that **happens over time**. A snapshot of the page has no "where did focus
go after that click?", so no snapshot rule can see it. The page is structurally perfect in
every state.

## Where it came from

A real Testbook bug: focus fell to `<body>` when the post menu closed after Edit, and after a
failed login. See [A11Y-007](../../../docs/a11y/AUDIT_LOG.md).

## Who it affects

Keyboard and screen reader users, who lose their place and must navigate from the top.
WCAG 2.4.3 Focus Order.

## The lesson

The rule of thumb: **when a control opens something, move focus into it; when it closes,
return focus to the control that opened it.** If the element holding focus is removed, you
must place focus yourself.

## Try it

```bash
npm install                         # once, in pitfalls/
npm run serve                       # open http://localhost:4100 and use the page by hand first
npm run exercise -- catch-it/lost-focus   # run YOUR test (exercise/) against both pages
npm run red -- catch-it/lost-focus        # watch the reference test fail on the broken page
npm test -- catch-it/lost-focus           # the reference solution, as CI runs it
```

Python track: `pip install -r requirements.txt`, then
`python3 -m pytest --exercises --show-red catch-it/lost-focus/exercise`.
