# Exercise: a button inside a link

**Goal:** write a test that **fails on the broken page** and **passes on the fixed page**.
Your starting file is `exercise/catch.spec.js` (JavaScript) or `exercise/test_catch.py`
(Python).

## Hints (use one at a time)

1. Open the broken page and press `Tab` until you notice the repeat.
2. A test can do the same: press `Tab` a few times and note what has focus each time.
3. `document.activeElement.textContent` tells you what each stop is.
4. Count the stops named "View". How many should there be?

## Check yourself

- Your test fails on the broken page and the failure shows two "View" stops.
- It passes on the fixed page.
- A plain axe scan is silent on both pages. Why?

The reference solution is in `solution/`.
