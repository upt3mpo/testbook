# Lab 17 Sample Bug Reports

Read these **after** you have written your own. They are examples of the format and the level of detail, not the only right
wording. Your environment line, and the words your screen reader actually spoke, will differ. Fill those in from your own run.

## Report 1: The silent error

```text
Title: Login form - failed sign-in is not announced to screen reader users (WCAG 4.1.3 Status Messages)

Environment: <your OS, browser, screen reader and versions>

Steps:
1. Open the broken "The silent error" pitfall page.
2. With the email field empty, activate "Log in".
3. Wait a moment for the message to appear on screen.

Expected: The message "Incorrect email or password" is announced as soon as it appears, and
keyboard focus moves to it or stays somewhere sensible.

Actual: The message appears visually but the screen reader says nothing. After the request,
keyboard focus is on the page background, not on the form or the message.
(Record what you actually heard, for example "silence".)

Who it affects: Screen reader users, who cannot tell whether the form submitted or what went
wrong. Also keyboard-only users, who lose their place when focus drops to the page background.

Severity: High. The task (signing in) cannot be completed with confidence, and a retry looks
identical to a failure.

Suggested fix: Give the message role="alert" so it is announced, and move focus to it when it
appears. The submit button is disabled while the request runs, which is what drops focus.
```

## Report 2: Lost focus

```text
Title: Post menu - choosing Edit loses keyboard focus (WCAG 2.4.3 Focus Order)

Environment: <your OS, browser, screen reader and versions>

Steps:
1. Open the broken "Lost focus" pitfall page.
2. Using only the keyboard, press Tab until "Post options" is focused, then press Enter.
3. Press Tab to reach "Edit" and press Enter.
4. Without pressing anything else, start typing.

Expected: Focus moves into the edit box, so typing goes there. After "Cancel", focus returns to
"Post options".

Actual: Typing goes nowhere. The "Edit" button disappeared when the menu closed, so focus fell
back to the top of the page. The same happens after "Cancel". (Record what a screen reader said,
if you used one.)

Who it affects: Keyboard-only and screen reader users, who must navigate from the top of the
page again after every use of the menu. Switch users, for whom that costs many extra presses.

Severity: Medium. The task is possible, but it takes much more effort and users may not realise
that their typing is going nowhere.

Suggested fix: Move focus into the edit box when it opens, and back to the menu button when it
closes. A rule of thumb: when a control opens something, focus moves in; when it closes, focus
returns to the control that opened it.
```

## What makes these good

- The **title** names the page, the problem and the criterion.
- The **steps** can be followed by someone who has never seen the page.
- **Actual** says exactly what happened, in plain words.
- **Who it affects** names people, not just rules, which is what gets a bug prioritised.
- **Severity** is justified in a sentence.
- The **fix** is a suggestion, not a demand.
