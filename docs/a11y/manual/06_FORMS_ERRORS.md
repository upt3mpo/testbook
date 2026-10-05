# 06 Forms, errors and authentication

**WCAG:** 1.3.5 Identify Input Purpose, 3.3.1 Error Identification, 3.3.2 Labels or
Instructions, 3.3.3 Error Suggestion, 3.3.4 Error Prevention, **3.3.7 Redundant Entry
(new in 2.2)**, **3.3.8 Accessible Authentication (Minimum, new in 2.2)**
**Time:** about 25 minutes
**Who this protects:** people with cognitive or memory disabilities, dyslexia, tremor or
motor difficulty, and screen reader users, plus everyone who uses a password manager.

## Why this needs a human

A test can confirm that a label exists and that an error has `role="alert"`. It cannot
tell you whether the error **makes sense**, whether it says **which field** is wrong, or
whether a person can **recover** from it without starting over.

*Automated overlap:* tests cover labels, `autocomplete` tokens, the error's role and focus,
that paste is not blocked, and axe on the error state. This script judges the *content*
and the *recovery*.

## Setup

- Reset the data. Use any browser. Have a password manager available (the browser's
  built-in one is fine).
- Pages: `/login`, `/register`, `/settings`.

## Cases

### FM-01 Every field says what it is for (3.3.2)

1. Look at Login, Register and Settings with **no text typed**. Then type one character in
   each field.

**Expected**

- Every field has a visible cue for its purpose **both** when empty and after you start
  typing. If the only cue is placeholder text that vanishes as you type, that is a failure
  (and was one, see Case 3 in the [worked examples](../WORKED_EXAMPLES.md)).
- Required fields are indicated. Format hints (for example "lowercase, no spaces" for
  username) are visible where they apply.

### FM-02 Login error: clear and recoverable (3.3.1, 3.3.3)

1. On Login, enter a real email with a wrong password. Submit.
2. Read the message. Correct only the password and submit again.

**Expected**

- The message says plainly that the email or password is incorrect. It does not blame the
  user or use jargon, and does not reveal which of the two was wrong (a security
  requirement, not a flaw).
- **What you typed is still there.** You do not have to retype the email.
- The message is not colour alone and stays on screen until you act.
- Keyboard focus is on or near the message (see script 01).

### FM-03 Register: duplicate email and username (3.3.1, 3.3.3)

1. On Register, use `sarah.johnson@testbook.com` as the email and any other valid values.
   Submit.
2. Change the email to a new one, but use the username `sarahjohnson`. Submit.

**Expected**

- Each message names **the field that is wrong** ("Email already registered", "Username
  already taken").
- After the error, the **other fields keep their values**. You are not asked to retype
  everything.
- Nothing about the form is cleared silently.

> **Judgement call to record:** the message identifies the field in words but is not
> attached to that field programmatically (`aria-describedby`). A screen reader user hears
> the message, then must find the field. Note whether you found that confusing. If so, it is
> a Low or Medium finding for field-level association.

### FM-04 Browser validation messages

1. On Login and Register, leave required fields empty and submit. Type an invalid email
   (for example `abc`) and submit.

**Expected**

- The browser's native validation message appears and names the problem (for example
  "Please fill out this field"). Keyboard focus moves to the first invalid field.
- With a screen reader on, the message is announced. (Native messages are generally
  accessible, but check in script 02/03 that the field you land on is named.)

### FM-05 Autofill and input purpose (1.3.5)

1. On Login, use your password manager to fill the form. Do the same on Register.
2. Look at which fields the browser offers to fill.

**Expected**

- The password manager offers the saved login on Login and offers to **create** a password
  on Register.
- Email, username and name are offered for the right fields. Nothing is mis-filled, for
  example a username placed in the email box.

### FM-06 Accessible Authentication (3.3.8, new in 2.2)

WCAG 2.2 says a login must not require a **cognitive function test** (remembering a
password counts) unless there is an alternative, such as a password manager or paste.

1. On Login, **paste** a password into the password field (copy it from a text editor).
2. Fill the form using only your password manager.
3. Look for any CAPTCHA, puzzle, "type the third character", or similar test.

**Expected**

- Paste works and the password manager can fill the field. There is no field that blocks
  either.
- There is **no** puzzle, transcription of characters, or image test.
- No time limit makes the user hurry to type a code (none exists today).

*Automated overlap:* a test verifies paste is not cancelled. The password-manager fill
(FM-05/06) is what only a human with a real manager can confirm.

### FM-07 Preventing mistakes (3.3.4) and redundant entry (3.3.7)

1. Delete a post, remove your profile picture, and (as a **throwaway account** you create on
   Register) start Delete Account in Settings, answering the prompts but stopping before the
   last confirmation.
2. Walk through Register and Settings looking for any place you are asked for something you
   already gave in the same session.

**Expected**

- Destructive actions ask for **confirmation** and can be cancelled. Deleting an account
  asks twice.
- You are never asked to re-enter information you already provided in the same process
  (3.3.7). Testbook's flows are short, so the expected answer is that this never happens;
  record it as N/A if you see no multi-step flow.

## Record

For every error message you see, copy the **exact text** into the run sheet. Writing down
what the user actually reads is the point of this script.
