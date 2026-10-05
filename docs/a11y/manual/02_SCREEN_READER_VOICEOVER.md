# 02 Screen reader testing: VoiceOver + Safari (macOS)

**WCAG:** 1.1.1 Non-text Content, 1.3.1 Info and Relationships, 2.4.2 Page Titled,
2.4.6 Headings and Labels, 3.3.1 Error Identification, 4.1.2 Name, Role, Value,
**4.1.3 Status Messages**
**Time:** about 45 minutes (add 15 if you have never used VoiceOver)
**Who this protects:** blind and low-vision users. A screen reader turns the page into
speech, so it only reports what is in the **accessibility tree**: names, roles, states
and live-region messages. If it is not in the tree, it does not exist for this user.

Run [03_SCREEN_READER_NVDA.md](03_SCREEN_READER_NVDA.md) with the same case IDs on
Windows. Results are recorded side by side in the run sheet. Read
[SCREEN_READER_COMPARISON.md](SCREEN_READER_COMPARISON.md) first if you want to know why
two readers are used.

## Setup

- macOS with Safari. VoiceOver is built in (no install).
- **Turn VoiceOver on or off:** `Cmd+F5` (or hold Touch ID for 3 seconds on some Macs).
- **Quiet the speech while learning:** open *VoiceOver Utility > Verbosity* if it is too
  chatty. Do not change it between cases.
- **Important Safari setting:** *Safari > Settings > Advanced* and tick **"Press Tab to
  highlight each item on a webpage"**. Without it `Tab` skips links and buttons, and your
  results will be wrong.
- Reset the data, open <http://localhost:3000/login> in a **new Safari window**.
- Optional but helpful: *VoiceOver Utility > Visuals > Show caption panel* so you can read
  what is being spoken. It is also the easiest way to quote output in a bug report.

### VoiceOver keys you need

`VO` means `Control+Option` (held together).

| Do this | Keys |
| --- | --- |
| Move to next / previous item | `VO+Right` / `VO+Left` |
| Activate (click) | `VO+Space` |
| Read from here | `VO+A` |
| Stop speaking | `Control` |
| Open the **Web Rotor** (lists of headings, links, form controls, landmarks) | `VO+U`, then Left/Right to switch list, Up/Down to choose, `Enter` to go |
| Jump to next heading | `VO+Command+H` |
| Jump to next landmark | rotor, choose Landmarks |
| Interact with a control (enter a group) | `VO+Shift+Down`; leave with `VO+Shift+Up` |
| Hear the page title | Listen as the page loads; it is also the Safari window title |

> If you are new, run VoiceOver's built-in tutorial first: *System Settings > Accessibility
> > VoiceOver > Open VoiceOver Training*.

## How to judge

For each control, listen for three things. This is the **name / role / state** test:

- **Name:** what is it called? ("Email", not "edit text" with no name.)
- **Role:** what kind of thing is it? (button, link, text field, heading.)
- **State:** is it on, off, expanded, collapsed, selected, disabled, invalid?

If any of the three is missing or wrong, that is a failure, even if the screen *looks*
fine. Record what VoiceOver actually said (use the caption panel).

## Cases

### SR-01 Page title and landmarks (Login)

1. Open `/login`. Listen to the announcement on load.
2. Open the rotor (`VO+U`) and look at **Landmarks** and **Headings**.

**Expected**

- The page title is announced as **"Log In - Testbook"** (or the equivalent), not a generic
  title shared by every page.
- Landmarks include a **main** region.
- Headings include one **level 1** heading ("Testbook").

### SR-02 Login form: names, roles, placeholders

1. Move through the form with `VO+Right`.
2. Stop on each field and listen.

**Expected**

- Email field is announced as **"Email"**, role **text field** (or "edit text"), and says it
  is **required**.
- Password field is announced as **"Password"** and as a **secure** text field.
- The button is "Log In", role **button**.
- "Create New Account" is a **link** (not a button).

> **Why:** placeholders alone were once the only label. Listen for the *name* spoken as the
> field is focused, not as helper text read afterwards.

### SR-03 Login error is announced (4.1.3)

1. Enter a wrong email and password. Activate **Log In** (`VO+Space`, or `Enter` in the
   field).
2. Listen immediately, without moving.

**Expected**

- The error message ("Incorrect email or password" or similar) is **spoken automatically**,
  with no navigation.
- Focus lands on or near the message, so `VO+Right` continues from there.

*Automated overlap:* a test asserts the message has `role="alert"` and takes focus. It
cannot tell you whether it was *spoken*, which is what this case checks. This resolves
the open item **A11Y-M01** for the login error.

### SR-04 Feed tabs: state is announced

1. Sign in. On the feed, go to the "See All" and "Following" buttons.

**Expected**

- "See All" is announced as a **toggle button** (or "button, pressed" / "selected"), and its
  state is stated: it is **on/pressed**.
- "Following" is announced as **not pressed**.
- After activating "Following", the states swap and VoiceOver reflects it.

> Before this was fixed, the active tab was only coloured. See A11Y-015 in the
> [audit log](../AUDIT_LOG.md).

### SR-05 Landmarks and headings on the feed

1. Rotor > Landmarks. Rotor > Headings.

**Expected**

- Landmarks: **navigation** and **main**.
- The navbar's links are in the navigation landmark.
- There is a level-1 heading (it may be visually hidden: "Feed"). Headings do not skip
  levels in a confusing way.
- Each post is reachable as an **article** named **"Post by <author>"**.

### SR-06 Post controls: names that make sense out of context

1. Move to one post with `VO+Right`. Stop on each button.
2. Open the rotor and choose **Buttons** (or **Form Controls**) to hear the list.

**Expected**

- Buttons are named in words: **"React"**, **"Comment"**, **"Repost"**; the view link is
  **"View post by <author>"**.
- Your own posts have a button named **"Post options"** (not "ellipsis", not blank).
- In the rotor list, no entry is blank or just a symbol.

> Repeated names ("Comment" x 20) are acceptable here because each post is an article with
> a name. Note any place you cannot tell *which* post a control belongs to.

### SR-07 Disclosure widgets: expanded or collapsed

1. On "React", listen to its state. Activate it. Listen again.
2. On your own post's "Post options", do the same.
3. On "Comment", do the same.

**Expected**

- Each says **collapsed** before and **expanded** after (VoiceOver may say "expanded" or
  "collapsed" or use a pop-up button phrase).
- After opening React, the reactions are **Like, Love, Haha, Wow, Sad, Angry** (words, not
  just emoji), each a button. The one you chose is announced as **pressed/selected**.

### SR-08 Reaction announced after the action (4.1.3)

1. Open React, choose **Like**. Listen, without moving.
2. Choose Like again (to remove it). Listen.
3. Activate **Repost**, then again.
4. Open Comment, type "Testing", press `Enter`.

**Expected**

- You hear **"Reacted with like"**, then **"Reaction removed"**, then **"Reposted"** and
  **"Repost removed"**, then **"Comment posted"**.
- The announcements are **polite**: they do not cut off what you were already hearing
  mid-word, but they do arrive without navigating.

*Automated overlap:* the **text** of each announcement is tested. Only here do you learn
whether it is spoken, in a sensible order, and whether the wording helps. This resolves
**A11Y-M01** for dynamic changes.

### SR-09 Edit mode and focus

1. On your own post: Post options > Edit.
2. Listen to where focus lands.

**Expected**

- Focus is **in the edit box**, announced as **"Edit post content"**, with the current text
  read out.
- Cancel and Save are buttons. After Cancel, focus returns to "Post options".

### SR-10 Delete: focus and announcement

1. Post options > Delete. Confirm the native browser dialog.

**Expected**

- The dialog's message is read out.
- After confirming you hear **"Post deleted"**, and focus is somewhere sensible (the main
  content), not lost to the start of the document.

### SR-11 Navigating pages: title and announcement

1. Activate **Settings** in the navbar. Listen.
2. Use the navbar to go to **Profile**, then **Home**.

**Expected**

- Each navigation announces the **new page's title** (for example "Settings - Testbook").
  Because this is a single-page app, the browser does not announce a page load, so the app
  must do it.
- The title differs on every page.

### SR-12 Settings form and status messages

1. On Settings, move through the form. Change **Theme**, then **Save**.

**Expected**

- Each field has a spoken name (Display Name, Bio, Theme, Text Density) and the selects
  announce their **current value**.
- After saving, "Settings updated successfully!" is **spoken** without navigating.
- Images: avatars in the post header read the author's name, not "image" or a filename.

## Things to note even if every case passes

- Any control where you could not tell what it did.
- Any announcement that is too long, repeated, or arrives twice.
- Emoji read oddly (for example "red heart" vs "love"). Names should come from the labels,
  not emoji dictionaries.

## Record

Quote VoiceOver's actual output for every Fail. If you enabled the caption panel, paste its
text.
