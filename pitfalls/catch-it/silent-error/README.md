# The silent error

**Shelf:** Catch it.

## What you are looking at

A login form. Press **Log in** with the field empty. After a moment an error appears:
"Incorrect email or password". Both pages look identical.

With a screen reader, the **broken** page says nothing. On the **fixed** page the error is
announced as soon as it appears. Keyboard users are affected too: on the broken page,
focus is dropped on the page background after the submit.

## Why the tests miss it

Whether a message is announced depends on **how it was inserted into the page**, not on how
it looks. A plain `<div>` appearing is silent. The message has good contrast and the page is
structurally fine, so axe passes on both. And the submit button is disabled while the
request runs, which silently drops keyboard focus.

## Where it came from

A real Testbook bug on the login error. See
[A11Y-004 and A11Y-007](../../../docs/a11y/AUDIT_LOG.md) and
[Case 4 in the worked examples](../../../docs/a11y/WORKED_EXAMPLES.md).

## Who it affects

Screen reader users (WCAG 4.1.3 Status Messages) and keyboard users (2.4.3 Focus Order).

## The lesson

Test the **contract** (the message has the `alert` role, focus is somewhere sensible), since
you cannot test the spoken output directly. The actual speech needs a human with a screen
reader: that is what Lab 17 is for.

## Try it

```bash
npm install                         # once, in pitfalls/
npm run serve                       # open http://localhost:4100 and use the page by hand first
npm run exercise -- catch-it/silent-error   # run YOUR test (exercise/) against both pages
npm run red -- catch-it/silent-error        # watch the reference test fail on the broken page
npm test -- catch-it/silent-error           # the reference solution, as CI runs it
```

Python track: `pip install -r requirements.txt`, then
`python3 -m pytest --exercises --show-red catch-it/silent-error/exercise`.
