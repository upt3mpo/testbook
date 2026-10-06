# A placeholder is not a label

**Shelf:** Catch it.

## What you are looking at

A login form. On the **broken** page each field shows only grey placeholder text ("Email",
"Password"). On the **fixed** page each field has a real label above it.

Type something into the broken page's email field: the word "Email" disappears. Anyone who
looks away and back no longer knows what the field is for.

## Why the tests miss it

axe-core accepts a non-empty placeholder as an accessible name, so a default scan passes on
both pages. The requirement (WCAG 3.3.2 Labels or Instructions) is **stronger than what a
tool can check**: a persistent label, not just a name that exists for a moment.

## Where it came from

A real Testbook bug on Login, Register, the post composer and the comment box. See
[A11Y-001](../../../docs/a11y/AUDIT_LOG.md) and
[Case 3 in the worked examples](../../../docs/a11y/WORKED_EXAMPLES.md).

## Who it affects

People with memory or cognitive disabilities, screen reader users, and anyone interrupted
mid-form.

## The lesson

Tools can only check that something exists. Whether it is *adequate* is a human judgement.
Your tests can still lean toward the right answer by finding fields by their label: that
query only works when a real label exists, so it fails on the broken page.

## Try it

```bash
npm install                         # once, in pitfalls/
npm run serve                       # open http://localhost:4100 and use the page by hand first
npm run exercise -- catch-it/placeholder-as-label   # run YOUR test (exercise/) against both pages
npm run red -- catch-it/placeholder-as-label        # watch the reference test fail on the broken page
npm test -- catch-it/placeholder-as-label           # the reference solution, as CI runs it
```

Python track: `pip install -r requirements.txt`, then
`python3 -m pytest --exercises --show-red catch-it/placeholder-as-label/exercise`.
