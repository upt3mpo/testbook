# Exercise 0.2: Who is excluded

**Estimated time:** 30 minutes
**Difficulty:** Beginner
**Language:** None (no code)
**Prerequisites:** [Exercise 0.1](EXERCISE_0_1_Meet_The_Barriers.md) completed

**What this adds:** you turn each barrier into the people it excludes and the WCAG criterion it
breaks, so that "it is hard to use" becomes a precise, defensible statement.

---

## Why this exercise

A bug report that says "the page is hard to use" gets ignored. One that says "keyboard-only
users cannot see where focus is, which fails WCAG 2.4.7, and also affects anyone with a broken
trackpad" gets fixed. Naming **who** is affected, and **which requirement** is broken, is a core
skill for anyone who tests.

It also corrects a common mistake: assuming each barrier excludes only one small group. Almost
every barrier here also affects people with a temporary or situational limitation, which is why
fixing it helps so many people.

---

## What you will learn

- To express a barrier as who, what and which requirement
- To see the permanent, temporary and situational versions of the same barrier
- To find the right WCAG criterion by looking it up, not guessing

---

## Step 1: Gather your barrier log (2 minutes)

Open the log you made in Exercise 0.1. You will add three columns to it.

## Step 2: Look up the criteria (10 minutes)

The table below lists the WCAG 2.2 criteria that the eight barriers relate to. Use it as your
lookup. For any you are unsure about, open the W3C's "Understanding" page; the link is in the
last column.

| Criterion | Name | Level | Principle | Read more |
| --- | --- | --- | --- | --- |
| 1.3.1 | Info and Relationships | A | Perceivable | [Understanding 1.3.1](https://www.w3.org/WAI/WCAG22/Understanding/info-and-relationships.html) |
| 1.4.3 | Contrast (Minimum) | AA | Perceivable | [Understanding 1.4.3](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) |
| 2.1.1 | Keyboard | A | Operable | [Understanding 2.1.1](https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html) |
| 2.4.2 | Page Titled | A | Operable | [Understanding 2.4.2](https://www.w3.org/WAI/WCAG22/Understanding/page-titled.html) |
| 2.4.3 | Focus Order | A | Operable | [Understanding 2.4.3](https://www.w3.org/WAI/WCAG22/Understanding/focus-order.html) |
| 2.4.7 | Focus Visible | AA | Operable | [Understanding 2.4.7](https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html) |
| 3.3.2 | Labels or Instructions | A | Understandable | [Understanding 3.3.2](https://www.w3.org/WAI/WCAG22/Understanding/labels-or-instructions.html) |
| 4.1.2 | Name, Role, Value | A | Robust | [Understanding 4.1.2](https://www.w3.org/WAI/WCAG22/Understanding/name-role-value.html) |
| 4.1.3 | Status Messages | AA | Robust | [Understanding 4.1.3](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html) |

## Step 3: Map each barrier (15 minutes)

For each of the eight rows in your log, add three columns:

| Column | What to write |
| --- | --- |
| **People affected** | At least one **permanent**, one **temporary** and one **situational** example. Use the spectrum table in the [Stage 0 README](../README.md#not-a-fixed-group-permanent-temporary-situational) for ideas, and add your own |
| **POUR principle** | Perceivable, Operable, Understandable or Robust |
| **WCAG criterion** | The number and name, from the lookup table above. Pick the one that best fits; a barrier can break more than one, so list the main one first |

**Worked example for K1** (invisible Tab stops), so you can see the level of detail:

| People affected | POUR | WCAG criterion |
| --- | --- | --- |
| Permanent: a person who cannot use a mouse and navigates by switch. Temporary: someone with a broken wrist using the keyboard only. Situational: someone whose trackpad has stopped working, or who is using a keyboard-only kiosk | Operable | 2.4.7 Focus Visible |

Do the other seven yourself.

**Hints:**

- If you are unsure between two criteria, read both "Understanding" pages and choose the one
  that describes **what the user experienced**, not what the code did.
- Not every barrier has an obvious situational case. If you cannot think of one, say so and
  explain why. Honest gaps are better than invented examples.

## Step 4: Find the curb cut (3 minutes)

Pick **one** of the eight barriers. Write two or three sentences on who benefits from the **fix**
beyond the people you listed as the main group. This is the curb-cut effect applied to a single
bug: the fix helps people nobody was thinking of when the bug was reported.

---

## Checkpoint

You can:

- State each of the eight barriers as "who is affected, which principle, which criterion"
- Give permanent, temporary and situational examples for the same barrier
- Say why the situational examples matter when arguing for a fix

---

## What you produced

The completed mapping table. It feeds directly into
[Exercise 0.3](EXERCISE_0_3_Built_In_Then_Verified.md), where you decide which layer should
have prevented each defect.

**Suggested answers** are in the
[Stage 0 answer keys](../../solutions/stage_0_answer_keys.md#exercise-02-suggested-mapping).
There is more than one defensible answer for several rows, so read them as a comparison, not a
marking scheme.
