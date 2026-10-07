# Exercise 0.3: Built in, then verified

**Estimated time:** 45 minutes
**Difficulty:** Beginner to intermediate
**Language:** None (no code)
**Prerequisites:** [Exercise 0.2](EXERCISE_0_2_Who_Is_Excluded.md) completed

**What this adds:** you trace Testbook's 19 real accessibility defects back to the layer that
should have prevented each one, and turn what you learn into acceptance criteria you will use
on the capstone ticket.

---

## Why this exercise

This is the heart of Stage 0. If you only remember one thing from it, it should be this:
**most accessibility defects are not found by testing because most are not testing problems.**
They are decisions made earlier. This exercise makes you see that with real evidence.

Testbook was audited against WCAG 2.2 AA and 19 defects were found and fixed. For every one of
them you can ask two questions:

1. **Where could it have been stopped earliest?**
2. **Which kind of test, if any, would have caught it?**

The gap between the answers is the lesson.

---

## What you will learn

- To classify a defect by the earliest layer that could have prevented it
- To see how few defects a default scan finds, and why
- To write acceptance criteria that prevent defects instead of reporting them

---

## Step 1: Read the layers (5 minutes)

Re-read the [prevention ladder](../README.md#the-prevention-ladder) in the Stage 0 README. The
seven layers are:

1. Requirements and design
2. Components and design system
3. Code review and lint
4. Unit and component tests
5. Automated end-to-end tests
6. Manual testing
7. Real users

Keep it open.

## Step 2: Gather your evidence (10 minutes)

For each defect you need to know what it was. Use, in this order:

1. The [audit log](../../../docs/a11y/AUDIT_LOG.md): one row per defect, with the WCAG criterion
   and a description.
2. The [worked examples](../../../docs/a11y/WORKED_EXAMPLES.md): five of the defects written up
   as case studies.
3. The [Pitfalls](../../../pitfalls/README.md) you used in Exercise 0.1: eight of the barriers
   in isolation.

You do not need to read every word. Skim each defect to understand what went wrong.

The audit log may list **more than 19** defects, because new ones are found over time. This exercise uses **A11Y-001 to A11Y-019**, the set known when the stage was written. Ignore any later ones.

## Step 3: Fill in the prevention matrix (20 minutes)

Copy this table. There is one row for each of the 19 defects. Fill in the last three columns.

| Audit ID | What went wrong (your own words) | Earliest layer that could have prevented it (1 to 7) | Would a default axe scan have caught it? (yes, no, partly) | Which layer would actually catch it? (1 to 7) |
| --- | --- | --- | --- | --- |
| A11Y-001 | | | | |
| A11Y-002 | | | | |
| A11Y-003 | | | | |
| A11Y-004 | | | | |
| A11Y-005 | | | | |
| A11Y-006 | | | | |
| A11Y-007 | | | | |
| A11Y-008 | | | | |
| A11Y-009 | | | | |
| A11Y-010 | | | | |
| A11Y-011 | | | | |
| A11Y-012 | | | | |
| A11Y-013 | | | | |
| A11Y-014 | | | | |
| A11Y-015 | | | | |
| A11Y-016 | | | | |
| A11Y-017 | | | | |
| A11Y-018 | | | | |
| A11Y-019 | | | | |

**Guidance:**

- "Earliest layer that could have prevented it" is a **judgement**. Several answers can be
  defensible. Write one sentence of justification for any you are unsure about.
- "Default axe scan" means a plain scan of each page in its default state, with the WCAG tags.
  Pitfalls often show you the answer: each pitfall page includes a test proving what a default
  scan does or does not see.
- If a defect was found by two different layers, write the cheaper one in the last column.

## Step 4: Add it up (5 minutes)

Count your answers.

| Question | Your count |
| --- | --- |
| How many defects could a default axe scan have caught on its own? | |
| How many could have been prevented at layers 1 to 3 (design, components, review and lint)? | |
| How many needed layers 5 to 7 (end-to-end, manual, real users) to find? | |

Write two or three sentences on what the numbers say. Then compare with the
[answer key](../../solutions/stage_0_answer_keys.md#exercise-03-the-prevention-matrix).

## Step 5: Write acceptance criteria (5 minutes)

Turn what you learned into something a team can use. Write **at least five acceptance criteria**
that you would attach to a ticket for a new feature, so that these defects cannot happen. They
should be **testable statements**, not wishes.

Weak: "The form is accessible."
Strong: "Every input has a visible label that stays visible while the user types."

Use this template, and keep the file: it is the starting point for the capstone ticket in
Stage 5.

```markdown
## Accessibility acceptance criteria: <feature name>

- [ ] Every control can be reached and operated with the keyboard alone.
- [ ] Focus is always visible, and moves to a sensible place when something opens or closes.
- [ ] Every input has a visible, persistent label.
- [ ] Every change that has no visible message of its own is announced to assistive technology.
- [ ] Errors say what went wrong and how to fix it, and are announced.
- [ ] The feature works in every theme and at 400% zoom.
- [ ] (add your own)
```

---

## Checkpoint

You can:

- Explain why a default scan found none of the 19 defects
- Say which layer you would invest in first, and why
- Write acceptance criteria that are specific enough to test

---

## What you produced

- A completed prevention matrix
- A set of accessibility acceptance criteria for a feature

Both come back in Stage 5, where accessibility is a requirement on the capstone ticket.

**Answer key** (read it after you have written your own):
[Stage 0 answer keys](../../solutions/stage_0_answer_keys.md#exercise-03-the-prevention-matrix).

## A last thought

Look at the "earliest layer" column. If most of your answers are in layers 1 to 3, you have
just seen why this stage comes before the testing stages. Testing is essential, and it is the
last line of defence, not the first.
