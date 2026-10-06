# Exercise: the theme nobody scanned

**Goal:** write a test that **fails on the broken page** and **passes on the fixed page**.
Your starting file is `exercise/catch.spec.js` (JavaScript) or `exercise/test_catch.py`
(Python).

## Hints (use one at a time)

1. Scan the page with axe in its default state. Is it clean?
2. What can the user do on this page that changes how it looks?
3. Click the theme button in your test **before** you scan.
4. You only need axe's `color-contrast` rule. Playwright's axe builder has `withRules([...])`.

## Check yourself

- Your test fails on the broken page and the failure names a contrast ratio.
- It passes on the fixed page.
- Why does a default-theme scan pass on both?

The reference solution is in `solution/`.
