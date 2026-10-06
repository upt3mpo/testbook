# Exercise: the hover and click fight

**Goal:** write a test that **fails on the broken page** and **passes on the fixed page**.
Your starting file is `exercise/catch.spec.js` (JavaScript) or `exercise/test_catch.py`
(Python).

Open the broken page and click **React** with the mouse. Look at the page, then inspect the
button's `aria-expanded` attribute in the developer tools.

## Hints (use one at a time)

1. Use a real click. Playwright's `click()` moves the pointer over the button first, exactly
   like a real mouse.
2. What does the screen show after the click? What does `aria-expanded` say?
3. The two should agree. Assert on `aria-expanded` and on the picker's visibility together.
4. There is a second way to expose the bug: open the picker with the **keyboard**, then move
   the pointer away and back.

## Check yourself

- Your test fails on the broken page, and the message points at `aria-expanded`.
- It passes on the fixed page.
- Why would a test that only used `focus()` and `Enter` never find the first problem?

The reference solution is in `solution/`.
