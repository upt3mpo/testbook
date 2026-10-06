# The test id that hides the bug

**Shelf:** Trust it?

## What you are looking at

A post card with a menu button. On the **broken** page the button's only "name" is a `⋯`
symbol. On the **fixed** page it is named "Post options".

The suspect test finds the button by `data-testid`, clicks it, and checks the menu opens:

```bash
npm test -- trust-it/test-id-hides-bug/suspect
```

It is green on **both** pages.

## Why a test can lie

A test id is something only developers see. Users, and screen readers, never meet it. A test
that finds a control by test id can pass while a person has no idea what the control is for.
It is not wrong, just blind to the one thing that matters here.

axe cannot see this problem either: the `⋯` glyph counts as text, so the button *has* a name.
It is simply a useless one, and whether a name is meaningful is a human judgement.

## Where it came from

A real Testbook finding: the post menu was a bare `⋯` that every functional test could click
by test id. See [A11Y-006](../../../docs/a11y/AUDIT_LOG.md).

## The lesson

Prefer to find controls the way a user does: by **role and name**. That query fails when the
name is missing or useless, so the test can notice the problem. Keep test ids for things users
genuinely cannot see (and for the cases where there is no better handle).

## Try it

```bash
npm install                         # once, in pitfalls/
npm test -- trust-it/test-id-hides-bug/suspect   # the suspect test: green on BOTH pages
npm run exercise -- trust-it/test-id-hides-bug   # your improved test (exercise/) against both pages
npm run red -- trust-it/test-id-hides-bug        # the reference test failing on the broken page
```

Python track: `pip install -r requirements.txt`, then
`python3 -m pytest trust-it/test-id-hides-bug/suspect` and
`python3 -m pytest --exercises --show-red trust-it/test-id-hides-bug/exercise`.
