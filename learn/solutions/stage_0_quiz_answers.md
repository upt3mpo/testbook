# Stage 0 Quiz Answers

## Inclusion First Quiz Answers

### 1. How should accessibility relate to testing?

**Answer: B) Accessibility is a requirement designed in from the start, and testing verifies it**

- Testing can find a missing ramp. It cannot create the inclusion that should have been
  designed in.
- Testbook's audit found 18 defects, almost all of them early decisions (a component without a
  required label, a CSS property chosen for the wrong reason). Testing found them; only design,
  code and review could have prevented them.
- A specialist after release (C) is the pattern this stage argues against, because late fixes
  are costlier and the original suite had already reported zero violations.
- Accessibility matters whether or not a law applies (D). Laws vary; the barriers are real
  either way.

### 2. In the social model of disability, where does the problem lie?

**Answer: C) In barriers designed into products and environments**

- The medical model places the problem in the person. The social model places it in the world
  that was designed without them.
- A building with only stairs excludes a wheelchair user. The stairs are the defect.
- That is why accessibility defects are ours to fix: they are design defects.

### 3. Which is an example of a situational limitation?

**Answer: C) A person holding a baby in one arm**

- Permanent: a person who is blind, or has low vision (A, D).
- Temporary: a broken arm (B), which will heal.
- Situational: a limitation that comes from the circumstances, not the person, such as
  holding a baby, glare on a screen, or a loud room.
- The same design choice often affects all three, which is why fixing a barrier helps so many
  people.

### 4. In Testbook's audit, how many of the 18 defects did the original default accessibility scan report?

**Answer: C) None: it reported zero violations while all 18 existed**

- The original suite scanned five pages in their default state and reported zero violations the
  whole time.
- A scan sees one snapshot. Most of the defects depended on **state** (an open menu, an error),
  **time** (focus after an action), a **different theme**, or **judgement** (is a name
  meaningful?), which a default scan cannot see.
- See the [audit log](../../docs/a11y/AUDIT_LOG.md) and
  [worked examples](../../docs/a11y/WORKED_EXAMPLES.md).

### 5. What is true of `opacity: 0` compared with `visibility: hidden`?

**Answer: B) `opacity: 0` hides an element visually but leaves it keyboard focusable; `visibility: hidden` also removes it from the Tab order**

- `opacity: 0` makes an element transparent. It is still in the page, still reachable with Tab,
  and still in the accessibility tree.
- `visibility: hidden` and `display: none` hide the element from the keyboard and from
  assistive technology too.
- This was a real Testbook bug: the closed reaction picker left six invisible Tab stops on
  every post. See the
  [invisible tab stops pitfall](../../pitfalls/catch-it/invisible-tab-stops/README.md).

## How did you do?

- **5/5:** You have the foundation. Go and look for these ideas in every stage that follows.
- **3 to 4:** Good. Re-read Part 3 of the Stage 0 README before moving on, because the rest of
  the thread builds on it.
- **0 to 2:** Re-read the Stage 0 README and redo Exercise 0.1 with the broken pages. The
  experience is what makes the ideas stick.

## Need more practice?

- Re-read the [Stage 0 README](../stage_0_inclusion_first/README.md)
- Redo [Exercise 0.3](../stage_0_inclusion_first/exercises/EXERCISE_0_3_Built_In_Then_Verified.md)
- Read the [worked examples](../../docs/a11y/WORKED_EXAMPLES.md)

## Ready for Stage 1?

If you got 3/5 or better, continue to [Stage 1: Unit Tests](../stage_1_unit/README.md).
