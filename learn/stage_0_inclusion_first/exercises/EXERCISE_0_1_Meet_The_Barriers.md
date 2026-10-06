# Exercise 0.1: Meet the barriers

**Estimated time:** 45 minutes
**Difficulty:** Beginner
**Language:** None (no code)
**Prerequisites:** [Stage 0 README](../README.md), Parts 1 and 2

**What this adds:** you use eight small pages that each hide one real accessibility barrier,
describe what happened precisely, and compare each with its fixed version.

---

## Read this first

You are going to meet barriers in order to describe and fix them. You are **not** going to find
out what it is like to be a disabled person. A few minutes of using a keyboard or a screen
reader, with your habits and your eyesight, is a very different thing from daily life. Part 2
of the [Stage 0 README](../README.md#part-2-meeting-a-barrier-is-not-the-same-as-living-with-it)
explains why. Keep that framing as you work.

**Adapt this to your own needs.** If you already use a keyboard, a screen reader or another
assistive technology every day, use your own setup, and treat each task as "does this work with
what I normally use?". If a task would be difficult for you in the way described, skip it and
read the page's README instead. Nothing here is a test of you.

---

## What you will learn

- What a real barrier is like to meet, in words precise enough for a bug report
- How the same bug looks different from a keyboard, a screen reader, and a plain visual check
- That a "fixed" page is the result of specific, small decisions

---

## Step 1: Set up (5 minutes)

```bash
cd pitfalls
npm install        # once
npm run serve
```

Open <http://localhost:4100>. You will see the landing page with a **broken** and a **fixed**
link for each pitfall. Open the broken links in separate browser tabs as you reach them.

**Checkpoint:** the landing page loads and lists the pitfalls.

Also create your barrier log. Copy this table into a note or a file; you fill in one row per
task.

| Task | Page | What I did | What went wrong (exactly) | Who it affects | What the fixed page does differently |
| --- | --- | --- | --- | --- | --- |
| K1 | | | | | |
| K2 | | | | | |
| K3 | | | | | |
| S1 | | | | | |
| S2 | | | | | |
| V1 | | | | | |
| V2 | | | | | |
| M1 | | | | | |

---

## Step 2: Keyboard only (15 minutes)

**Put the mouse and trackpad out of reach and do not touch them.** Use `Tab` (next),
`Shift+Tab` (previous), `Enter` and `Space` (activate), and `Escape` (close). If your browser
is Safari, enable *Settings > Advanced > Press Tab to highlight each item on a webpage*, or use
Chrome or Firefox.

### K1: Invisible Tab stops

Open the **broken** page for *Invisible tab stops*.

1. Press `Tab` once. Focus lands on the **React** button.
2. Keep pressing `Tab` and count how many presses it takes to reach **Comment**.
3. Watch the screen on every press.

Write down: how many presses, and what you saw on the screen during the extra ones.

Now open the **fixed** page and repeat. How many presses now?

### K2: Lost focus

Open the **broken** page for *Lost focus*.

1. Press `Tab` until the **Post options** button (the three dots) is focused. Press `Enter`.
2. Press `Tab` to reach **Edit** and press `Enter`.
3. An edit box has appeared. **Without pressing anything else, start typing.**

Write down: where did your typing go? How would you know?

Repeat on the **fixed** page. Then, on both, press **Cancel** and type again.

### K3: A button inside a link

Open the **broken** page for *A button inside a link*.

1. From the top, press `Tab` repeatedly through the page.
2. Count the stops that say **View**.

Write down: how many stops for one control? Repeat on the **fixed** page.

---

## Step 3: Screen reader, or its stand-in (10 minutes)

If you have a screen reader, use it. Setup is in the manual testing scripts:
[VoiceOver on macOS](../../../docs/a11y/manual/02_SCREEN_READER_VOICEOVER.md#setup) or
[NVDA on Windows](../../../docs/a11y/manual/03_SCREEN_READER_NVDA.md#setup). **If you do not
have one**, use your browser's accessibility inspector instead: in Chrome, open the developer
tools, choose **Elements**, then the **Accessibility** pane; in Firefox, open the
**Accessibility** tab. It shows each element's name and role: the same information a screen
reader speaks, as text.

### S1: The silent error

Open the **broken** page for *The silent error*. Press **Log in** with the field empty.

- *With a screen reader:* listen. What do you hear when the error appears?
- *Without one:* in the accessibility inspector, find the error message. Does it have a role
  that would cause it to be announced (`alert`)?

Repeat on the **fixed** page. Write down the difference.

### S2: The test id that hides the bug

Open the **broken** page for *The test id that hides the bug*.

- Move to the menu button. *With a screen reader:* what does it say? *Without one:* what is its
  accessible **name** in the inspector?

Write down what a person who cannot see the screen would know about this button. Then do the
same on the **fixed** page.

---

## Step 4: Everything else (10 minutes)

Not every barrier is about a keyboard or a screen reader.

### V1: The theme nobody scanned

Open the **broken** page for *The theme nobody scanned* and press **Dark theme**.

1. Look at the **Save settings** button. Is the white text easy to read? Try lowering your
   screen brightness, or holding the screen at a distance.
2. Optional: measure it. In Chrome's developer tools, select the button and click the colour
   swatch in the Styles pane: it shows the **contrast ratio**. The target for this text is
   4.5:1.

Compare with the **fixed** page in dark mode.

### V2: A placeholder is not a label

Open the **broken** page for *A placeholder is not a label*.

1. Click into the email field and type a few characters.
2. Look away from the screen for ten seconds, then look back. What is the field for?

Imagine this was a long form and you had been interrupted. Compare with the **fixed** page.

### M1: Every page has the same title

Open the **broken** page for *Every page has the same title*.

1. Click **Settings**, then **Profile**. Look at the browser tab each time.
2. Imagine you have eight tabs of this app open, or you are reading your browser history.

Compare with the **fixed** page. If you are using a screen reader, listen after each click as
well.

---

## Step 5: Compare and reflect (5 minutes)

Finish the **What the fixed page does differently** column for every row. Look at the page
source if you want to see the exact change. Each fixed page differs from its broken twin in
only a line or two.

**Checkpoint questions:**

- Which barrier surprised you most? Why?
- Which one would you have **missed** if you had only looked at the screen with a mouse?
- Which fixes were a single line? What does that tell you about when they should have been
  made?

---

## What the fixed pages are not

A fixed page is not "fully accessible". Each one fixes the one bug it teaches. Real
conformance with WCAG 2.2 AA means every page, in every state, passing every criterion, and then
being used by real people. That is why the rest of the course exists.

---

## Optional stretch

Pick one pitfall and write the test that fails on the broken page and passes on the fixed one,
in your track's language. Its `exercise.md` has a hint ladder. You will do this properly in
Stage 3 and Lab 16, so skip it if you are short of time.

---

## What you produced

A completed barrier log. Keep it: you use it in
[Exercise 0.2](EXERCISE_0_2_Who_Is_Excluded.md) and refer to it in the Stage 0 reflection.

**Sample answers** for comparison are in the
[Stage 0 answer keys](../../solutions/stage_0_answer_keys.md#exercise-01-what-you-should-have-observed).
Read them after you have written your own.
