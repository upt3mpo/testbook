# Exercise: lost focus

**Goal:** write a test that **fails on the broken page** and **passes on the fixed page**.
Your starting file is `exercise/catch.spec.js` (JavaScript) or `exercise/test_catch.py`
(Python).

## Hints (use one at a time)

1. Do it by hand with the keyboard only: open the menu, choose Edit. Where is focus?
2. Use the keyboard in your test too: `focus()` the menu button, press `Enter`.
3. Check where focus is with `toBeFocused()` (or `to_be_focused()` in Python).
4. There are two moments to check: after choosing Edit, and after pressing Cancel.

## Check yourself

- You have two assertions that each fail on the broken page.
- Both pass on the fixed page.
- Why would clicking with the mouse hide the second bug?

The reference solution is in `solution/`.
