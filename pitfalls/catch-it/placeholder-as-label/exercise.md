# Exercise: a placeholder is not a label

**Goal:** write a test that **fails on the broken page** and **passes on the fixed page**.
Your starting file is `exercise/catch.spec.js` (JavaScript) or `exercise/test_catch.py`
(Python).

## Hints (use one at a time)

1. How does a screen reader user find the email field? Not by its position on screen.
2. Playwright has a locator built for exactly this: `getByLabel` (`get_by_label` in Python).
3. Try the same test using `getByPlaceholder`. Does it pass on the broken page? That is why
   you should not use it here.
4. A second behaviour to assert: after typing, is the field's name still visible?

## Check yourself

- Your test fails on the broken page, passes on the fixed page.
- You can explain why a `getByTestId` or `getByPlaceholder` version would have kept passing.
- Bonus: the reference solution proves axe is silent on both pages. Why is it silent?

The reference solution is in `solution/`.
