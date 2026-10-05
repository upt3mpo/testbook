# 07 Content and cognitive accessibility

**WCAG:** 1.1.1 Non-text Content, 1.3.1 Info and Relationships, 2.4.2 Page Titled,
2.4.4 Link Purpose, 2.4.6 Headings and Labels, 3.1.1 Language of Page, 3.2.3 Consistent
Navigation, 3.2.4 Consistent Identification, **3.2.6 Consistent Help (new in 2.2)**
**Time:** about 20 minutes
**Who this protects:** screen reader users, people with cognitive, language or memory
disabilities, and everyone who scans a page quickly.

## Why this needs a human

Tools check that things **exist**: alt text is present, a title is present, headings
are in order. They cannot check that they are **meaningful**. An image with the alt text
"image" passes every scanner. So does a page titled "Page".

*Automated overlap:* tests confirm a distinct `<title>` per route, alt attributes exist,
heading order, landmarks, and `<html lang>`. This script judges **quality**.

## Setup

- Reset the data. Sign in as Sarah. Use any browser.
- To see what a screen reader would be told about an image, right-click it and choose
  *Inspect*, or use DevTools' accessibility pane (*Elements > Accessibility*).

## Cases

### CT-01 Page titles tell you where you are (2.4.2)

1. Visit Login, Register, Feed, a Post detail, a Profile, Followers, Following, Settings.
   Read each tab title.

**Expected**

- Every title is **different** and **describes the page**, with the specific part first
  ("Settings - Testbook", "Followers of @sarahjohnson - Testbook").
- The profile and post titles include who they are about.

### CT-02 Image alternatives are meaningful (1.1.1)

1. Inspect every kind of image: the navbar avatar, post-header avatars, comment avatars, a
   post's attached image, the profile avatar, the Settings avatar preview, and the
   composer's attachment preview.

**Expected**

- An avatar that sits **beside the person's name** can be named with that person's name or
  marked decorative; either is fine, but a user must not hear the same name twice in a row
  without reason. Record whether you hear a redundant double-read.
- A **post image** has alt text that says something useful about the picture.

> **Known limitation, recorded and not a bug:** user-uploaded post images all carry the
> generic alt text "Post content" because the app has no field where the author can describe
> an image. A tool cannot tell this is poor alt text; this case exists to record it. The fix
> is a product feature (an alt-text field when posting), not a CSS or markup change.

### CT-03 Headings describe their sections (2.4.6)

1. List the page's headings (DevTools, a heading-outline extension, or a screen reader's
   headings list) for Feed, Profile, Post detail and Settings.

**Expected**

- Each page has **one** top-level heading that names the page.
- Headings read in a sensible outline, with no skipped levels and no heading used only for
  styling.
- Some of these headings are visually hidden on purpose (for example the Feed's "Feed"). That
  is acceptable if the outline is still correct.

### CT-04 Links and buttons make sense out of context (2.4.4)

1. Open a screen reader's links list or buttons list (script 02/03) or scan the page's links
   in DevTools.

**Expected**

- No link reads only "click here", "more" or "View" with no further context. Post "View"
  links should say which post.
- Controls named only by an emoji or symbol are a failure unless they have a text name.
- Link text and destination agree.

### CT-05 Plain, consistent wording (cognitive)

1. Read every label, message and button on Login, Register, Feed and Settings.
2. Look for jargon, abbreviations, and inconsistent names for the same thing.

**Expected**

- The same action is called the same thing everywhere. (For example, "Log In" vs "Login" vs
  "Sign in" used for the same thing is a finding, even a minor one.)
- Error and success messages say what happened in everyday language.
- Nothing disappears before you can read it. Success messages stay long enough to read, or
  until dismissed.

### CT-06 Consistent navigation, identification and help (3.2.3, 3.2.4, 3.2.6)

1. Visit every signed-in page. Note where the navbar links are and what they are called.
2. Look for a help link, contact, or support mechanism.

**Expected**

- The navbar is in the **same place** with the **same order and names** on every signed-in
  page.
- A control that does the same thing has the same name everywhere (for example Follow).
- **3.2.6:** if a help mechanism exists, it appears in the same place on each page. Testbook
  has no help mechanism today, so record this as **N/A** and note that adding one would
  create a requirement.

## Record

For anything that is "technically present but unhelpful", log it as a finding even when no
WCAG rule is clearly broken. That judgement is the whole reason this script exists.
