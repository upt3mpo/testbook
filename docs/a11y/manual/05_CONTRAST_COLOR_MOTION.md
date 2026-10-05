# 05 Contrast, colour and motion

**WCAG:** 1.4.1 Use of Color, 1.4.3 Contrast (Minimum), 1.4.11 Non-text Contrast,
2.3.3 Animation from Interactions (AAA; recommended), 2.2.2 Pause, Stop, Hide
**Time:** about 25 minutes
**Who this protects:** low-vision users, colour-blind users (about 1 in 12 men), and
anyone reading a screen in sunlight.

## Why this needs a human

axe computes contrast for most text, but it reports an element as **"incomplete"** when
it cannot decide: text over an image or gradient, text partly covered by another element,
and hover, focus, active and disabled states it never visits. It also checks only text,
not the colour of a focus ring against its surroundings. Those are the cases here.

*Automated overlap:* axe checks contrast on every route in light **and** dark themes and in
several open states. Do **not** re-measure ordinary text. Measure what axe flags as
incomplete, and the states below.

## Setup

- A contrast checker: the **Colour Contrast Analyser** (free, TPGi) or the browser's
  DevTools colour picker, which shows the ratio.
- Targets: **4.5:1** for normal text, **3:1** for large text (18 pt or 14 pt bold) and for
  UI component boundaries and focus indicators.
- Reset the data. Sign in as Sarah. Do each case in **light** and in **dark** (change it
  under Settings > Theme, then Save).
- The variables live in [`frontend/src/index.css`](../../../frontend/src/index.css).

## Cases

### CC-01 Items axe marks "incomplete"

1. Run an axe scan (browser extension, or the Playwright run) on the Feed and Profile and
   open the **Incomplete** results.
2. For each item, measure the foreground and background yourself.

**Expected:** each pair meets its threshold. Record the pair and the ratio.

Known incomplete items (as of the last audit) to settle by hand:

| Where | Why axe could not decide |
| --- | --- |
| Post composer textarea | Background partly obscured by another element |
| Post menu glyph | Non-text content (it is decorative and hidden from assistive technology; confirm the *button* boundary is visible) |
| Profile counts and secondary text | Text over a card background; confirm `text-secondary` on both backgrounds |

> This resolves the open item **A11Y-M02**.

### CC-02 Secondary text, both themes

1. Measure `--text-secondary` against `--bg-primary` **and** against `--bg-secondary`, in
   light and in dark.

**Expected:** at least 4.5:1 in all four combinations.

### CC-03 Interactive states

1. For each of: primary button, secondary button, danger button, feed tab, reaction
   option, navbar link, text link: measure the colours in the **default**, **hover**,
   **focus** and **disabled** states.

**Expected**

- Default, hover and focus text meet 4.5:1.
- **Disabled** controls are exempt from the ratio, but must still be recognisable as
  controls and not look like body text.

### CC-04 Focus indicator contrast (1.4.11)

1. Tab to a button, a text field, a link and a feed tab. Measure the focus ring against the
   background **and** against the control it surrounds.

**Expected:** the ring has at least **3:1** contrast against adjacent colours, and is at
least 2 px thick. Check the primary button specially, because the ring colour changes
there to stay visible against the blue.

### CC-05 Not by colour alone (1.4.1)

1. Find every place colour carries meaning: the active feed tab, the active reaction, the
   Reposted state, error text, success text, the Follow/Unfollow state.
2. Convert the screen to greyscale (macOS: *Accessibility > Display > Colour Filters >
   Greyscale*; Windows: *Colour filters > Greyscale*; or the Chrome DevTools *Rendering >
   Emulate vision deficiencies > Achromatopsia*).

**Expected**

- You can still tell the active tab from the inactive one, and a reacted post from an
  unreacted one.
- Errors still read as errors (they carry a message, not just a colour).
- Links inside body text are distinguishable without colour, or have 3:1 against the
  surrounding text.

### CC-06 Dark theme end to end

1. Switch to dark and visit every page and open the menu, picker, edit box and comment box.

**Expected:** no unreadable text, no invisible borders on inputs or cards, no white flash
or clipped dark text. Record any element that looks wrong even if you cannot name a ratio.

> Dark mode once failed contrast on primary buttons and the active tab (A11Y-016). If you
> ever add a colour, check it in both themes.

### CC-07 Motion

1. Turn on **Reduce motion** (macOS: *Accessibility > Display*; Windows: *Settings >
   Accessibility > Visual effects > Animation effects off*).
2. Reload. Open and close the reaction picker, menus, and hover the buttons.
3. Watch for anything that moves on its own: spinners, auto-updating content, anything
   that flashes.

**Expected**

- No content flashes more than three times in a second.
- Nothing moves, blinks or updates automatically for more than five seconds without a way
  to pause or stop it.
- The app's motion is limited to short fades. Note whether it honours the reduced-motion
  setting. (It currently does not, and that is a documented, AAA-level gap, not a failure.)

## Record

Write the **actual ratio** for every measurement, not just pass or fail. Ratios let the next
tester see whether a change moved a value toward the threshold.
