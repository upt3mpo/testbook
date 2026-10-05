# 04 Zoom, reflow and text spacing

**WCAG:** 1.4.4 Resize Text, 1.4.10 Reflow, 1.4.12 Text Spacing, 1.4.13 Content on Hover
or Focus
**Time:** about 20 minutes
**Who this protects:** people with low vision who magnify the page, people on small
phones, and anyone who sets a larger default font. WCAG expects the page to remain
usable at **200%** text zoom and, with no sideways scrolling, at **400%** zoom (which is
the same as a 320 CSS pixel wide window).

> **Why this needs a human:** a test can check "no horizontal scrollbar". It cannot judge
> whether the page is still *usable*: a control pushed off-screen, overlapping text, or a
> button too far from its label passes the scrollbar check and still fails the user.

*Automated overlap:* tests assert no horizontal overflow at 320 px on four pages and run
axe at 320 px. This script covers usability, which they cannot.

## Setup

- Chrome or Firefox. Reset the data. Sign in as Sarah.
- Zoom with `Cmd/Ctrl +` and `Cmd/Ctrl -` (reset with `Cmd/Ctrl 0`). Browser zoom is what
  low-vision users use, and it also shrinks the CSS viewport, which is what triggers reflow.
- Note your window width at 100%. At **400%** zoom a 1280 px window behaves like 320 px.

## Cases

### ZM-01 200% zoom

1. Set the browser zoom to 200%. Visit Login, Feed, a Profile, a Post detail, Settings.

**Expected**

- All text is readable and not cut off or overlapping.
- Every control is still visible and usable.
- No *essential* information or function is lost.

### ZM-02 400% zoom / 320 px reflow

1. Set the zoom to 400%. Visit the same five pages.

**Expected**

- Content reflows into one column. **No horizontal scrolling** is needed to read (apart from
  genuinely two-dimensional content such as a data table; Testbook has none).
- The navbar wraps rather than running off the edge.
- Every action is still reachable, including the **Logout** button, which was once pushed
  off-screen.

### ZM-03 The post card at 400%

1. At 400%, find a post with an image and a post with a long comment.
2. Open React, Comment and the post menu.

**Expected**

- The reaction picker and the post menu **stay on-screen** and are not clipped by the
  window edge.
- Images scale down to fit. Long text wraps, including long usernames and email addresses
  (check Settings and Profile).

### ZM-04 Text-only zoom

1. Reset zoom. In Firefox: *Settings > General > Zoom > Zoom text only*, then zoom text to
   200%. (In Chrome, use *Settings > Appearance > Font size > Very large* instead.)

**Expected:** text grows, nothing overlaps, no text is clipped inside buttons or the navbar.

### ZM-05 Text spacing override (1.4.12)

1. Install a text-spacing bookmarklet or extension (for example "Text Spacing Editor"), or
   paste this into the browser console on each page:

   ```javascript
   const s = document.createElement('style');
   s.textContent = '* { line-height: 1.5 !important; letter-spacing: 0.12em !important; word-spacing: 0.16em !important; } p { margin-bottom: 2em !important; }';
   document.head.appendChild(s);
   ```

2. Visit Feed, Login and Settings.

**Expected**

- No text is clipped, truncated or overlapping. Buttons and the navbar grow to fit.
- Nothing disappears.

### ZM-06 Hover and focus content (1.4.13)

1. At 100% zoom, **hover** over React, then move the pointer slowly onto the reaction picker.
2. Move the pointer away, then **hover again** and press `Esc` while it is open.

**Expected**

- The picker stays open while the pointer is over it (it is **hoverable**).
- It remains until you move away or dismiss it (it is **persistent**).
- `Esc` closes it (it is **dismissible**) without moving the pointer.

## Record

For any failure, note the **zoom level and window width**, and attach a screenshot. A
failure that appears only at one zoom level is still a failure.
