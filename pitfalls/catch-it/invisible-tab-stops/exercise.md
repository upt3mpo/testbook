# Exercise: invisible Tab stops

**Goal:** write a test that **fails on the broken page** and **passes on the fixed page**.
Your starting file is `exercise/catch.spec.js` (JavaScript) or `exercise/test_catch.py`
(Python).

Open the broken page by hand first and press `Tab` until you see it happen.

## Hints (use one at a time)

1. A test has to do what you just did: press `Tab` several times.
2. After each press, ask the page what has focus: `document.activeElement`.
3. "Can the user see it?" is not the same as "is it in the page?". Playwright's own
   `isVisible()` treats `opacity: 0` as visible, so you will need to read the element's
   computed style yourself.
4. Check the element **and its ancestors**: `opacity`, `visibility` and `display` can each
   be set on a parent.

## Check yourself

- Your test fails on the broken page **for the right reason**: read the failure message. Does
  it name the invisible controls?
- It passes on the fixed page.
- Bonus: would a plain axe scan have caught it? (It would not. The reference solution has a
  test that proves it.)

The reference solution is in `solution/`. Compare after you have tried.
