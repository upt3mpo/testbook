# Exercise: the silent error

**Goal:** write a test that **fails on the broken page** and **passes on the fixed page**.
Your starting file is `exercise/catch.spec.js` (JavaScript) or `exercise/test_catch.py`
(Python).

## Hints (use one at a time)

1. A message that is announced to a screen reader has a particular **role**. Which one?
2. Playwright can find an element by role: `getByRole`.
3. Where is keyboard focus after the error appears? `document.activeElement` will tell you.
4. You will need to wait for the error to appear before you check anything.

## Check yourself

- You have **two** assertions that each fail on the broken page: one about the role, one
  about focus.
- Both pass on the fixed page.
- Why can no automated test tell you the message was actually *spoken*?

The reference solution is in `solution/`.
