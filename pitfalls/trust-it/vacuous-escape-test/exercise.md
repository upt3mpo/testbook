# Exercise: the vacuous Escape test

**Goal, part 1:** prove the suspect test cannot be trusted. **Part 2:** write one you can.

## Part 1: prove it

1. Run `suspect/suspect.spec.js` against both pages. Both green.
2. Without opening the page's source: which behaviour could you remove while keeping the test
   green? Now open the broken page's source and confirm.
3. Add a `console.log` or a screenshot just *before* the Escape key press in the suspect
   test. Is the menu open at that moment?

## Part 2: write a trustworthy version

Your starting file is `exercise/trust.spec.js` (or `exercise/test_trust.py`). It must **fail on
the broken page** and **pass on the fixed page**.

### Hints (use one at a time)

1. The click opens and then closes the menu. Is there another way to open it?
2. Use the keyboard: focus the button, press `Enter`.
3. Before pressing Escape, assert that the menu is visible. If the setup failed, you want to
   know *that*, not a confusing result later.

## Check yourself

- The suspect test is green on both pages. Yours is red on the broken page and green on the
  fixed page.
- You can say in one sentence what a precondition assertion buys you.

The reference solution is in `solution/`.
