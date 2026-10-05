# 03 Screen reader testing: NVDA + Firefox (Windows)

**WCAG:** 1.1.1, 1.3.1, 2.4.2, 2.4.6, 3.3.1, 4.1.2, **4.1.3 Status Messages**
**Time:** about 45 minutes (add 20 if you have never used NVDA)
**Who this protects:** NVDA is a free, open-source Windows screen reader and consistently
among the most used in published screen reader surveys, so results here matter as much as
VoiceOver's. It behaves
differently from VoiceOver in ways that expose different bugs.

This script uses the **same case IDs and expected results** as
[02_SCREEN_READER_VOICEOVER.md](02_SCREEN_READER_VOICEOVER.md). Only the setup and the
keystrokes differ. Where NVDA behaves differently in a way that matters, it is called out.
See [SCREEN_READER_COMPARISON.md](SCREEN_READER_COMPARISON.md) for the full picture.

## Setup

- Windows 10 or 11. Install NVDA from <https://www.nvaccess.org> (free). Use Firefox
  (primary) or Chrome. Testing both is useful: NVDA's output differs slightly between them.
- Use a **standard, non-portable** NVDA install so the keyboard layout is predictable.
- Reset the data, open <http://localhost:3000/login> in a **new window**.
- Open *NVDA menu > Tools > Speech Viewer* to see the spoken text on screen. It is the
  easiest way to quote output in a bug report.

### NVDA keys you need

`NVDA` means the NVDA key: `Insert` (desktop layout) or `CapsLock` (default).

| Do this | Keys |
| --- | --- |
| Start / stop NVDA | `Ctrl+Alt+N` / `NVDA+Q` |
| Stop speaking | `Ctrl` |
| Read from here ("say all") | `NVDA+Down Arrow` |
| Next / previous item (browse mode) | `Down Arrow` / `Up Arrow` |
| Next heading / landmark / button / link / form field | `H` / `D` / `B` / `K` / `F` |
| Previous (any of the above) | the same key with `Shift` |
| **Elements list** (headings, links, buttons, landmarks) | `NVDA+F7` |
| Toggle browse mode and focus mode | `NVDA+Space` |
| Activate | `Enter` or `Space` |
| Read the page title | `NVDA+T` |

### The thing that trips everyone up: browse mode vs focus mode

NVDA has two modes on web pages:

- **Browse mode:** you read the page with the arrow keys and single-letter keys (`H`,
  `B`...). NVDA intercepts the keys.
- **Focus mode:** keys go straight to the page, which is what you need to type in a text
  box. NVDA switches automatically when you land on a form field and says so (a short
  "tone" or "focus mode").

If a case says "type something" and the keys seem to do nothing, you are in browse mode.
Press `NVDA+Space`. VoiceOver has no direct equivalent, which is why a custom widget can
work in one reader and fail in the other.

## How to judge

Same **name / role / state** test as the VoiceOver script. NVDA's wording is different
("button", "link", "edit", "toggle button", "pressed", "collapsed"), but the three pieces
of information must all be present.

## Cases

The case steps and expected results match
[the VoiceOver script](02_SCREEN_READER_VOICEOVER.md#cases). Use these NVDA translations of
the navigation, and note the differences below.

| VoiceOver step | NVDA equivalent |
| --- | --- |
| `VO+Right` to move to the next item | `Down Arrow` in browse mode |
| Web Rotor, Landmarks / Headings / Buttons | `NVDA+F7` (Elements list), or the `D` / `H` / `B` keys |
| `VO+Space` to activate | `Enter` (or `Space` on a button) |
| Caption panel | Speech Viewer |

### SR-01 Page title and landmarks

Press `NVDA+T` and listen on load. Elements list (`NVDA+F7`) > Landmarks / Headings.
**Expected** as in the VoiceOver script.

### SR-02 Login form

Use `F` to jump between fields, or `Tab`. **Expected** as before: names "Email" and
"Password", role edit / password edit, "required" announced.

> **NVDA difference:** NVDA announces `required` and `invalid entry` states reliably.
> Compare against VoiceOver, which sometimes phrases them differently.

### SR-03 Login error announced

Submit a wrong login with `Enter`. **Expected:** the error is spoken at once. `role="alert"`
messages are normally spoken by NVDA immediately and interrupt other speech.

> **Resolves A11Y-M01** for the login error on Windows.

### SR-04 Feed tabs

`B` to the "See All" and "Following" buttons. **Expected:** "toggle button" and
"pressed" / "not pressed" announced.

### SR-05 Landmarks and headings

`D` cycles landmarks (navigation, main). `H` cycles headings. Posts are articles named
"Post by <author>". **NVDA note:** articles are not always announced as a role in browse
mode. If NVDA does not speak "article" but does speak the name on entering the post, that is
acceptable; note it.

### SR-06 Post control names

`B` through the buttons, or `NVDA+F7 > Buttons`. **Expected:** React, Comment, Repost, "Post
options", and links named "View post by <author>". No blank or symbol-only entries.

### SR-07 Disclosure widgets

Listen for **"collapsed"** and **"expanded"** on React, Post options and Comment, before and
after activating. The reaction buttons are Like/Love/Haha/Wow/Sad/Angry and the chosen one is
**pressed**.

### SR-08 Announcements after actions

React, un-react, Repost and un-Repost, post a comment. **Expected:** "Reacted with like",
"Reaction removed", "Reposted", "Repost removed", "Comment posted".

> **NVDA note:** NVDA queues live-region messages and may speak them slightly after the
> action. Wait a couple of seconds before deciding something was not announced.

### SR-09 Edit mode and focus

Post options > Edit. **Expected:** focus is in "Edit post content". NVDA should switch to
focus mode automatically.

### SR-10 Delete

Confirm the dialog. **Expected:** the dialog text is read and "Post deleted" is spoken.

### SR-11 Navigating pages

Use the navbar. **Expected:** each page's title is announced. NVDA will often also read the
page's first heading; that is fine as long as the title is also available (`NVDA+T`).

### SR-12 Settings form and status messages

**Expected:** each field is named with its value; the success message is spoken. Check the
two `<select>` controls: NVDA reads the selected option when you land and when you change it
with the arrow keys.

## Findings specific to running both readers

If the same case passes in one reader and fails in the other, that is a **real** finding:

- Pass in VoiceOver, fail in NVDA, usually means the page relies on VoiceOver being
  forgiving of incomplete markup, or on a live region NVDA handles differently.
- Pass in NVDA, fail in VoiceOver is often a Safari specific gap (for example a missing
  `Tab` setting, or a role VoiceOver announces differently).

Do not average the two. Record both and look for the markup difference.
