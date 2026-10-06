# Exercise: the test id that hides the bug

**Goal, part 1:** prove the suspect test cannot be trusted. **Part 2:** write one you can.

## Part 1: prove it

1. Run `suspect/suspect.spec.js` against both pages. Both green.
2. Open the broken page with a screen reader (or the browser's accessibility inspector) and
   look at the menu button. What is it called?
3. Which edit to the page would leave the suspect test green but make the page worse for a
   screen reader user?

## Part 2: write a trustworthy version

Your starting file is `exercise/trust.spec.js` (or `exercise/test_trust.py`). It must **fail on
the broken page** and **pass on the fixed page**.

### Hints (use one at a time)

1. How would you describe this button to a person over the phone?
2. Playwright's `getByRole` takes a `name` option.
3. Assert the button exists before you click it, so a missing button fails fast instead of
   timing out.

## Check yourself

- Yours is red on the broken page, green on the fixed page.
- You can explain why a default axe scan is silent on the broken page.

The reference solution is in `solution/`.
