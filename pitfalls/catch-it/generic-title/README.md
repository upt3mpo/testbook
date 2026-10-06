# Every page has the same title

**Shelf:** Catch it.

## What you are looking at

A tiny single-page app with **Home**, **Settings** and **Profile** links. Click between them:
the heading and the text change on both pages.

Now look at the browser tab. On the **broken** page the title never changes. On the **fixed**
page it follows the content ("Settings - Testbook"), and a hidden status message announces
the new page.

## Why the tests miss it

axe checks that a `<title>` **exists**. It does not know your page is a single-page app, or
that the title should change as the content does. A single-page app never reloads, so the
browser gives a screen reader no "new page" cue unless you provide one. The page is
structurally fine at every moment.

## Where it came from

Real Testbook findings: every route had the same title, and moving between pages produced no
announcement. See [A11Y-009 and A11Y-013](../../../docs/a11y/AUDIT_LOG.md).

## Who it affects

Screen reader users (the title is the first thing read on a page load), and anyone with many
tabs or browsing history. WCAG 2.4.2 Page Titled and 4.1.3 Status Messages.

## The lesson

In a single-page app, **you** are responsible for what a page load normally does for free:
update the title, and announce the change.

## Try it

```bash
npm install                         # once, in pitfalls/
npm run serve                       # open http://localhost:4100 and use the page by hand first
npm run exercise -- catch-it/generic-title   # run YOUR test (exercise/) against both pages
npm run red -- catch-it/generic-title        # watch the reference test fail on the broken page
npm test -- catch-it/generic-title           # the reference solution, as CI runs it
```

Python track: `pip install -r requirements.txt`, then
`python3 -m pytest --exercises --show-red catch-it/generic-title/exercise`.
