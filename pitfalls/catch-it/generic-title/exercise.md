# Exercise: every page has the same title

**Goal:** write a test that **fails on the broken page** and **passes on the fixed page**.
Your starting file is `exercise/catch.spec.js` (JavaScript) or `exercise/test_catch.py`
(Python).

## Hints (use one at a time)

1. Click between the links by hand and watch the browser tab.
2. Playwright can check the page title: `expect(page).toHaveTitle(...)`.
3. A second check: a screen reader needs a **status** region to announce the change.
4. Look for the region by its role, not by an id.

## Check yourself

- You have two assertions (title and announcement) that each fail on the broken page.
- Both pass on the fixed page.
- Why is a green axe scan no evidence that the titles are right?

The reference solution is in `solution/`.
