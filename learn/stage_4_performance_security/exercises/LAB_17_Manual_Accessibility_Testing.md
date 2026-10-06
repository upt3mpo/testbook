# Lab 17: Manual Accessibility Testing

**Estimated time:** 120 minutes (105 minutes core, 15 minutes optional)
**Difficulty:** Intermediate
**Language:** None (no code). The same lab for the Python, JavaScript and Hybrid tracks
**Prerequisites:** [Lab 16](LAB_16_Accessibility_Automation_JavaScript.md) (or its [Python version](LAB_16_Accessibility_Automation_Python.md)),
[Stage 0](../../stage_0_inclusion_first/README.md)

**What this adds:** Lab 16 proved what automation can see. This lab covers what it cannot: whether the experience makes sense.
You run scripted keyboard and screen reader tests, write professional bug reports, and decide which findings to automate.

---

## What you will learn

- How to run a scripted manual test and record results others can repeat
- How to use a screen reader well enough to test with it (and what to do if you do not have one)
- How to write an accessibility bug report that gets fixed
- How to decide what part of a manual finding can become an automated test

---

## Before you start

Do **not** skip the framing from [Stage 0, Part 2](../../stage_0_inclusion_first/README.md#part-2-meeting-a-barrier-is-not-the-same-as-living-with-it).
A scripted test with a screen reader is a way to **verify** that a product works with assistive technology. It is **not** a
substitute for testing with people who use assistive technology every day, and it does not tell you what that experience is
like. Say so in your reports.

**Adapt to your needs.** If you already use a keyboard-only setup, a screen reader or another assistive technology daily, use
yours. Nothing in this lab is a test of you.

**Pick your tools:**

| You have | Use |
| --- | --- |
| A Mac | VoiceOver with Safari ([setup](../../../docs/a11y/manual/02_SCREEN_READER_VOICEOVER.md#setup)) |
| Windows | NVDA with Firefox ([setup](../../../docs/a11y/manual/03_SCREEN_READER_NVDA.md#setup)) |
| Both | Do both, and compare in Part 6 |
| Neither | Use the alternative in Part 3 (the browser's accessibility inspector and a live-region watcher) |

Reset the data before each part: `curl -X POST http://localhost:8000/api/dev/reset`

---

## Step-by-step instructions

### Part 1: Set up your run sheet (10 minutes)

1. Read the [manual testing README](../../../docs/a11y/manual/README.md), especially "How to read a test case" and "Severity".
2. Copy the [run sheet template](../../../docs/a11y/manual/RUN_SHEET_TEMPLATE.md) to a file outside the repository, or inside it
   but **do not commit it**. Fill in the environment table (operating system, browser, screen reader, versions).

**Checkpoint:** your run sheet exists and the environment table is filled in.

### Part 2: The keyboard pass (25 minutes)

Run these cases from the [keyboard script](../../../docs/a11y/manual/01_KEYBOARD.md): **KB-01, KB-02, KB-04, KB-05, KB-06,
KB-07 and KB-10**.

**Why do this by hand when the suite already tests them?** Lab 16 tests the *mechanism*: focus moves, the order is stable,
nothing is hidden. It cannot judge the *experience*: is the focus ring easy to see? Does the order feel logical? How much effort
did that take? For each case, write down two things in the run sheet: **pass or fail**, and **anything the automated test would
not have noticed** (a ring that is hard to see, an order that is correct but odd, a step that took too many key presses).

**Checkpoint:** seven cases recorded, each with a judgement note.

### Part 3: The screen reader pass (40 minutes)

Run cases **SR-01 to SR-08** from the script for your reader:
[VoiceOver](../../../docs/a11y/manual/02_SCREEN_READER_VOICEOVER.md) or [NVDA](../../../docs/a11y/manual/03_SCREEN_READER_NVDA.md).

For every case, record the **exact words** the screen reader said, not just "pass". Use VoiceOver's caption panel or NVDA's Speech
Viewer to capture them. The test is name, role and state: did you hear all three?

**If you have no screen reader:**

1. **Names, roles and states.** Open the browser's accessibility inspector (Chrome: developer tools, **Elements**, then the
   **Accessibility** pane; Firefox: the **Accessibility** tab). Select each control the script mentions and record its **name**,
   **role** and **state**. This is the information a screen reader would speak.
2. **What would be announced.** Open the developer tools console and paste this to log every announcement the app makes:

   ```javascript
   const live = document.querySelector('[data-testid="live-region"]');
   new MutationObserver(() => {
     if (live.textContent) console.log("ANNOUNCED:", live.textContent);
   }).observe(live, { childList: true, characterData: true, subtree: true });
   ```

   Now react to a post, repost, comment, and move between pages. Each `ANNOUNCED:` line is something a screen reader will say.
   (Errors are different: they use `role="alert"`, which you check in the inspector.)
3. Say plainly in your run sheet that you used the inspector and not a screen reader. It tells you the markup is right. It does
   **not** tell you what it sounds like.

**Look out for these judgement items** that the scripts flag, because tools cannot decide them:

| Where | The question |
| --- | --- |
| Post header | The avatar is a link and the author's name is a link. Do you hear the author's name twice in a row? Is that a problem? |
| Post images | User-uploaded images all have the alternative text "Post content". Is that useful? What would be? |
| Register errors | "Email already registered" names the field in words but is not attached to the field. Did you find that confusing? |
| Reactions | Are the announcements ("Reacted with like") helpful, too chatty, or too late? |

**Checkpoint:** eight cases recorded with the actual words (or the inspector's output) and your answers to the four judgement
questions.

### Part 4: Write two bug reports (25 minutes)

Testbook itself is now accessible enough that a pass may find little. To practise writing reports you need something that is
actually broken, and the [Pitfalls](../../../pitfalls/README.md) are exactly that.

Start them with `cd pitfalls && npm install && npm run serve`, then open these **broken** pages and test them the way you tested
Testbook (keyboard, then screen reader or inspector):

1. [The silent error (broken)](http://localhost:4100/catch-it/silent-error/broken/)
2. [Lost focus (broken)](http://localhost:4100/catch-it/lost-focus/broken/)

Write one bug report for each, using the format from the
[manual testing README](../../../docs/a11y/manual/README.md#reporting-a-failure):

```text
Title: <page> - <what is wrong> (<WCAG criterion>)
Environment: <OS / browser / screen reader + versions>
Steps: <numbered, from a clean start>
Expected: <what should happen>
Actual: <what happened, quoting what you heard if relevant>
Who it affects: <keyboard-only / screen reader / low vision / motor / cognitive users>
Severity: <Blocker | High | Medium | Low>
Suggested fix: <optional>
```

**A good report names a person who is blocked, not just a rule.** "Fails 4.1.3" gets ignored. "A screen reader user who submits
the login form hears nothing and does not know it failed" gets fixed.

Compare with the [sample reports](../../solutions/LAB_17_sample_bug_reports.md) **after** you write yours.

**Checkpoint:** two complete bug reports, each naming who is affected and a severity.

### Part 5: Decide what to automate (15 minutes)

A manual finding is not finished until the part of it that **can** be automated **is** automated. For each of your two reports,
answer:

| Question | Report 1 | Report 2 |
| --- | --- | --- |
| Which part is deterministic (a role, a focus position, a name)? | | |
| Which part needs a human (is it understandable, is the wording useful)? | | |
| Which Lab 16 technique would test the deterministic part? | | |

Then write the test for **one** of them. The [pitfall's exercise](../../../pitfalls/catch-it/silent-error/exercise.md) has a hint
ladder, and Lab 16's helper is the pattern. The rule to remember: **automate the mechanism, keep a human for the experience.**

**Checkpoint:** you have split each finding into an automatable part and a human part, and written one test.

### Part 6: Compare two readers (optional, 15 minutes)

If you have both VoiceOver and NVDA, run SR-03 (the login error), SR-07 (expanded and collapsed) and SR-08 (announcements) in both.
Record where the speech differs. Read the [comparison](../../../docs/a11y/manual/SCREEN_READER_COMPARISON.md) and say whether any
difference is a **markup** problem or just a **wording** difference. The rule: if one reader passes and the other fails, look at
the markup. Do not average the two.

---

## What you learned

- How to run and record a scripted manual accessibility test
- That the useful part of a manual test is the judgement note, not the tick
- How to write a report that names who is affected
- How to split a finding into the part a test can own and the part a person must

## Lab completion checklist

- [ ] Filled in the environment table, including which tools I used (and said so if I had no screen reader)
- [ ] Recorded KB-01, KB-02, KB-04, KB-05, KB-06, KB-07 and KB-10, each with a judgement note
- [ ] Recorded SR-01 to SR-08 with the actual words spoken (or the inspector's output)
- [ ] Answered the four judgement questions about Testbook
- [ ] Wrote two bug reports that each name a person who is affected
- [ ] Split each finding into an automatable part and a human part, and wrote one test
- [ ] Can explain why a scripted screen reader test is not a substitute for testing with disabled users
- [ ] (Optional) Compared two screen readers and identified a markup difference or a wording difference

## Reflection

1. What did you notice during the manual pass that the automated suite could never have told you?
2. Which of your judgement items would you actually raise as a bug, and which would you leave? Why?
3. You are the only tester on a team that ships weekly. Which parts of this lab would you automate, which would you run before
   every release, and which would you ask real users to do?

**Next:** [Stage 5: Capstone](../../stage_5_capstone/README.md) (after the Stage 4 README's reflection and quiz).
