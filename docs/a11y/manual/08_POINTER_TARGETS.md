# 08 Pointer, target size and gestures

**WCAG:** 2.5.1 Pointer Gestures, 2.5.2 Pointer Cancellation, 2.5.3 Label in Name,
**2.5.7 Dragging Movements (new in 2.2)**, **2.5.8 Target Size (Minimum, new in 2.2)**
**Time:** about 15 minutes
**Who this protects:** people with tremor or limited fine motor control, touch users with
large fingers, and users of head pointers, eye trackers and switch devices.

## Why this needs a human

axe checks the target size of each control (rule `target-size`). It has built-in
**exceptions** (a small control is fine if enough clear space surrounds it) and it cannot
tell whether a hit area *feels* too small or too close to a neighbour that does something
destructive.

*Automated overlap:* a test fails if any control on the feed is under 24x24 CSS px, and axe
runs `target-size` with the WCAG 2.2 tag. This script covers spacing, destructive
neighbours, and the touch experience.

## Setup

- Reset the data. Sign in as Sarah.
- A touch device is ideal (a phone on your local network at
  `http://<your-computer's-IP>:3000`, or the Chrome DevTools device toolbar with touch
  emulation). Otherwise use a mouse and apply the checks by measuring.
- To measure a target: DevTools > select the element > the box model shows its size in CSS
  pixels. 24 x 24 is the 2.2 minimum; **44 x 44** is the more comfortable target recommended
  for touch.

## Cases

### PT-01 Target size (2.5.8)

1. Measure each distinct control on the feed: React, Comment, Repost, View, "Post options",
   the reaction options, the navbar links and Logout, the Feed tabs, and the form
   controls.

**Expected:** every control is at least **24 x 24 CSS px**, or has enough empty space around
it that a 24 px circle centred on it would not overlap another target. Record any control
under 44 px as a Low finding for comfortable touch use.

### PT-02 Neighbours that do opposite things

1. In the post menu, look at **Edit** and **Delete**. On Profile, look at **Follow** and
   **Block**.

**Expected**

- Destructive actions (Delete, Block) are **not** so close to a harmless one that a slightly
  off tap triggers them.
- Both are behind a **confirmation**, which limits the damage (check that it appears).

### PT-03 Touch: tap carefully (2.5.2 Pointer Cancellation)

1. With touch (or a mouse): press **down** on Repost, drag the pointer **off** the button,
   and release.
2. Do the same on Delete in the menu (cancel the confirmation if it appears).

**Expected:** the action does **not** fire when you release outside the control. A user can
abort an accidental press by sliding away.

### PT-04 No dragging required (2.5.7, new in 2.2)

1. Find any feature that uses dragging: the composer's drop zone, any sliders, any
   reorderable list.

**Expected**

- Dragging is **never the only way**. The composer's drop zone has a clear alternative: the
  **Add Media** button opens the file picker, and the drop zone is also clickable.
- Nothing requires a path or multi-finger gesture (2.5.1). Testbook has none.

### PT-05 Label in name (2.5.3) and voice control

1. Use your OS voice control (macOS *Voice Control*, Windows *Voice Access*) and say "Click
   React", "Click Comment", "Click Repost", "Click Log In".

**Expected**

- Saying the **visible** label works. The accessible name **contains** the visible text, so
  a button that reads "Repost" can be triggered by saying "Repost".
- Controls whose accessible name differs from the visible text (for example the View link,
  named "View post by <author>") still work when you say the visible word "View". If there
  are several, voice control shows numbers; pick one. Record that behaviour.

## Record

Measure, do not guess. Write the **actual pixel size** of any control you flag.
