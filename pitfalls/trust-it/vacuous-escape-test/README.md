# The vacuous Escape test

**Shelf:** Trust it? A test is green. Should you believe it?

## What you are looking at

A menu that opens when you hover over it or click it, and should close when you press
`Escape`. On the **broken** page the Escape handler is missing. On the **fixed** page it works.

Run the suspect test:

```bash
npm test -- trust-it/vacuous-escape-test/suspect
```

It is **green on both pages**, including the one where Escape does nothing.

## Why a test can lie

The test clicks the button, presses Escape, and checks the menu is closed. But a real mouse
click hovers first (which opens the menu) and then clicks (which toggles it closed again).
So by the time Escape is pressed the menu is already shut. The test never gave Escape
anything to close, so it cannot tell whether Escape works.

## The experiment that exposes it

Delete the feature and see whether the test notices. This is the idea behind **mutation
testing**: if you can remove the behaviour a test claims to check and it still passes, the
test is not checking it. The broken page is that experiment, already done.

## Where it came from

This is a real mistake from building Testbook's accessibility tests: an Escape-key test that
passed, then turned out to pass even with the handler deleted.
See [Case 2 in the worked examples](../../../docs/a11y/WORKED_EXAMPLES.md).

## The lesson

Before pressing the key, **assert the precondition**: prove the menu is open. A test that
never checks its own setup can go green without exercising the feature.

## Try it

```bash
npm install                         # once, in pitfalls/
npm test -- trust-it/vacuous-escape-test/suspect   # the suspect test: green on BOTH pages
npm run exercise -- trust-it/vacuous-escape-test   # your improved test (exercise/) against both pages
npm run red -- trust-it/vacuous-escape-test        # the reference test failing on the broken page
```

Python track: `pip install -r requirements.txt`, then
`python3 -m pytest trust-it/vacuous-escape-test/suspect` and
`python3 -m pytest --exercises --show-red trust-it/vacuous-escape-test/exercise`.
