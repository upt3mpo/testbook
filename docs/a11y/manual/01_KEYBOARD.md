# 01 Keyboard-only testing

**WCAG:** 2.1.1 Keyboard, 2.1.2 No Keyboard Trap, 2.4.1 Bypass Blocks, 2.4.3 Focus Order,
2.4.7 Focus Visible, **2.4.11 Focus Not Obscured (Minimum, new in 2.2)**
**Time:** about 25 minutes
**Who this protects:** people who cannot use a mouse (motor disability, repetitive strain
injury, broken trackpad), switch and voice-control users, and every screen reader user.

## Setup

- Unplug or disable your mouse and trackpad if you can. If not, **do not touch them** for
  the whole script. Moving the pointer changes what you are testing.
- Use Chrome or Firefox at a normal window size (about 1280 px wide).
- Reset the data, then open <http://localhost:3000/login>.
- Keys: `Tab` next, `Shift+Tab` previous, `Enter` and `Space` activate, `Esc` close,
  arrow keys move within a control (for example a `<select>`).

> **Safari note:** Safari skips links and buttons when you press `Tab` unless you enable
> *Settings > Advanced > "Press Tab to highlight each item on a webpage"*. Use Chrome or
> Firefox for this script, or turn that option on. (Screen reader users in Safari use a
> different navigation, covered in script 02.)

## What to watch for throughout

Keep these three questions in your head for every case:

1. **Can I see where focus is?** (a clear ring, every time)
2. **Does Tab take me somewhere sensible next?** (visual order matches Tab order)
3. **Did focus ever vanish?** (nothing visibly focused after an action)

## Cases

### KB-01 Login form, by keyboard alone

1. Load `/login`. Press `Tab` once.
2. Continue pressing `Tab` until focus leaves the form.
3. Type `sarah.johnson@testbook.com` in Email, `Tab`, type the password, press `Enter`.

**Expected**

- Tab order is Email, Password, Log In, Create New Account.
- Every stop has a clearly visible focus indicator, including the two text fields.
- `Enter` in the password field submits. You land on the feed.

*Automated overlap:* the tab order and the keyboard-only login are covered by
`accessibility-behavior.spec.js`. Judge the **visibility** of the focus ring here, which a
test can only approximate.

### KB-02 Skip link

1. On the feed, reload the page (`F5`). Press `Tab` once.
2. Press `Enter`.
3. Press `Tab` once more.

**Expected**

- The first Tab stop is a link reading "Skip to main content". It is **visible** while
  focused (not just focusable).
- `Enter` moves focus to the page content. The next `Tab` goes to the first control
  *inside* the content (the Feed tabs), not back into the navbar.

### KB-03 Navbar

1. From the top of the feed, Tab through the navbar.

**Expected:** Testbook logo, Home, Profile, Settings, Logout, in that order, each with a
visible focus ring. No invisible stops.

### KB-04 Tab order down the feed (invisible stops)

1. Click nowhere. From the top, press `Tab` 40 times, noting what is focused each time.
2. Watch specifically between each post's "Repost" and the next post.

**Expected**

- Every Tab stop is **visible** when focused.
- Per post, the order is: author link, (menu button, if your own post), React, Comment,
  Repost, View. No stop where nothing visible has focus.
- You never press Tab and see nothing change on screen.

> **Why this case exists:** the reaction picker once left six invisible Tab stops on every
> post, and axe could not see it. See [Case 1 in the worked examples](../WORKED_EXAMPLES.md).
> If you ever press Tab and nothing appears focused, that is exactly this bug.

*Automated overlap:* a test asserts no reaction option is focused while the picker is
closed. This case catches the same class of bug in *any* new control.

### KB-05 Reaction picker

1. Tab to a post's **React** button. Press `Enter`.
2. Press `Tab`.
3. Press `Enter` on a reaction (for example Like).
4. Tab back to React, press `Enter` to reopen, then press `Esc`.

**Expected**

- `Enter` opens the picker. `Tab` moves into the first reaction (Like), which has a visible
  focus ring.
- Choosing a reaction applies it and closes the picker.
- `Esc` closes the picker and focus **returns to the React button**.

### KB-06 Post menu, edit and cancel (your own post)

1. On one of Sarah's own posts, Tab to the "..." menu button. Press `Enter`.
2. `Tab` to **Edit** and press `Enter`.
3. Type a few characters. `Tab` to **Cancel**, press `Enter`.
4. Reopen the menu and press `Esc`.

**Expected**

- The menu opens; `Tab` reaches Edit and Delete.
- After **Edit**, focus is **inside the edit box** (you can type at once).
- After **Cancel**, focus returns to the "..." button, not to the top of the page.
- `Esc` closes the menu and focus returns to the "..." button.

### KB-07 Comment box

1. Tab to **Comment** on a post. Press `Enter`.
2. Type "Testing". Press `Enter`.

**Expected**

- Pressing `Enter` on Comment puts focus **in the comment field**.
- Submitting posts the comment, closes the box, and focus returns to the **Comment**
  button.

### KB-08 Delete a post (focus after a destructive action)

1. On your own post, open the menu, choose **Delete**, confirm the browser prompt with
   `Enter`.

**Expected**

- The post disappears and focus is on the page content area (not lost, not on a removed
  element). Pressing `Tab` continues from the top of the content, so you are not sent back
  to the start of the document.

### KB-09 No keyboard traps

1. Open the post menu, the reaction picker, the comment box and the edit box in turn.
2. For each, try to leave using only `Tab`, `Shift+Tab` and `Esc`.

**Expected:** you can always leave. Focus never loops forever inside one widget with no way
out.

### KB-10 Focus Not Obscured (WCAG 2.2, 2.4.11)

This is new in 2.2. The navbar is **sticky**, so a focused element could hide behind it.

1. Make the window short (about 500 px tall) so the page scrolls a lot.
2. From the top of the feed, `Tab` repeatedly down at least 60 stops.
3. Then `Shift+Tab` back up 20 stops.

**Expected**

- The focused control is never **completely** hidden behind the navbar, in either direction.
- Ideally it is not hidden at all. Record any stop where it is partly covered.

*Automated overlap:* a test checks that the focused element's bottom edge stays below the
navbar. Do this by hand anyway at short heights, which the test does not cover.

### KB-11 Settings page and form controls

1. Go to Settings by keyboard (navbar link, `Enter`).
2. Tab through every control. Use the arrow keys to change **Theme** and **Text Density**.
3. Save with `Enter` on the Save button.

**Expected**

- Each field is reachable and operable. `<select>` changes with the arrow keys.
- A success message appears (this is checked for *speech* in script 02).
- The delete-account button is last in the order, clearly separated, and shows a
  confirmation before acting.

### KB-12 Follow, block and the lists

1. Open another user's profile (for example `mikechen`) by keyboard.
2. Tab to **Follow**, press `Enter`. Open the **Followers** list by keyboard.

**Expected:** Follow, Block, and the Followers/Following links are all reachable and
operable; list pages have a logical Tab order.

## Results to record

For each case, Pass/Fail. For every Fail, note the **exact stop** where it went wrong
("after pressing Enter on Edit, no visible focus"). That sentence is your bug report.
