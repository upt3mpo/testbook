# Stage 0: Inclusion First

**Build it in, then verify it**

> **Language tracks:** this stage has no code and is the same for the Python, JavaScript and
> Hybrid tracks. You will use a browser, your keyboard, and (optionally) a screen reader.

## Your progress

You are at the start of the course. The order is Stage 0, then Stages 1 to 5.

- Stage 0: Inclusion First (you are here)
- Stage 1: Unit Tests
- Stage 2: Integration Tests
- Stage 3: API and E2E Testing
- Stage 4: Performance and Security
- Stage 5: Capstone

**Estimated time:** 2.5 hours of core content. There are no optional exercises in this stage.

## Entry criteria

You do not need to have run or tested anything yet. You need:

- A computer with a modern browser and a keyboard.
- Node.js 24 installed (the exercises serve a few small pages with it). If you have not set it
  up yet, follow the [Quick Start](../../docs/guides/QUICK_START.md) first.
- About 2.5 hours, ideally in two sittings. Part 3 is easier after a break.

A screen reader is helpful but not required. Every exercise that uses one has an alternative.

## Table of contents

- [Why this stage comes first](#why-this-stage-comes-first)
- [Part 1: What inclusion and accessibility mean](#part-1-what-inclusion-and-accessibility-mean)
- [Part 2: Meeting a barrier is not the same as living with it](#part-2-meeting-a-barrier-is-not-the-same-as-living-with-it)
- [Part 3: Built in, then verified](#part-3-built-in-then-verified)
- [The three exercises](#the-three-exercises)
- [Success criteria](#success-criteria)
- [Related resources](#related-resources)
- [Self-check quiz (optional)](#self-check-quiz-optional)
- [Reflection](#reflection)
- [Stage complete](#stage-complete)

---

## Why this stage comes first

Most testing courses treat accessibility as a late, specialist topic: write the app, test the
app, and near the end run an accessibility scan. This course puts it first, because that
order produces worse software and worse testers.

Think about a building. A ramp planned in the first drawings is a gentle slope that costs
almost nothing. A ramp added after the stairs are built is steep, awkward, expensive, and
often in the wrong place. And the inspector who visits at the end can only tell you the
building has no ramp. They cannot make one appear.

Testing works the same way. A tester can find a missing ramp. A tester cannot create the
inclusion that should have been designed in.

Testbook proves the point. It was built as a normal testing-course app, by people who cared
about quality, with a test suite that was green. When we audited it against WCAG 2.2 AA we
found **19 real defects**. The original accessibility tests had reported **zero violations**
the whole time, because they only looked at each page in its default state and most of the
problems were not the kind a snapshot can see.

Almost every one of those 19 defects was a decision made early: a design token, a component
without a required label, a CSS property chosen for the wrong reason. Testing could find
them. Only design, code and review could have **prevented** them.

So this stage asks you to change two habits:

1. **Treat accessibility as a requirement**, like correctness or security, from the first
   conversation about a feature.
2. **Treat testing as verification of inclusion, not the source of it.** Your job as a tester
   starts before the code exists.

### What you will be able to do

By the end of this stage you can:

- Explain who is excluded by common design choices, and why that is a design failure and not
  an edge case.
- Describe the difference between a defect that testing can find and one that only design can
  prevent.
- Meet a real barrier with a keyboard and assistive technology, and describe it precisely.
- Take any accessibility defect and say where in the lifecycle it should have been stopped.
- Write accessibility acceptance criteria for a ticket.

---

## Part 1: What inclusion and accessibility mean

### Two words, one idea

- **Accessibility** is whether people can actually use a thing: perceive it, operate it,
  understand it. It is usually measured against a standard.
- **Inclusion** is the wider intent: designing so that the people who will use something are
  not excluded by choices nobody examined. Accessibility is the part of inclusion you can
  test against a checklist. Inclusion also covers things a checklist cannot, such as whose
  needs were never asked about.

A note on language: some people prefer "people with disabilities" and others prefer "disabled
people". Both are in common use. Follow how the individuals and communities you work with
describe themselves. This course uses both.

### Two ways of seeing disability

| Model | Where it places the problem | What it leads to |
| --- | --- | --- |
| **Medical model** | In the person: they have an impairment that needs fixing or accommodating | Special requests, workarounds, separate "accessible versions" |
| **Social model** | In the environment: a barrier was designed into the world | Removing barriers for everyone, in the main product |

A flight of stairs does not disable anyone by itself. A building with only stairs does.
Accessibility work, and this course, uses the social model: **the barrier is a defect in the
design, so the defect is ours to fix.**

### Not a fixed group: permanent, temporary, situational

It is tempting to picture "users with disabilities" as a small, separate group. A more
accurate picture is a spectrum that every person moves along during their life.

| Ability | Permanent | Temporary | Situational |
| --- | --- | --- | --- |
| Touch | One arm | An arm in a cast | Holding a baby |
| See | Blind | A cataract, or dilated pupils at an eye test | Glare on a phone in the sun |
| Hear | Deaf | An ear infection | A loud room, or a silent office with no headphones |
| Speak | Nonverbal | Laryngitis | A heavy accent in a noisy place |

_Adapted from the Microsoft Inclusive Design toolkit's persona spectrum._

When something is designed for the permanent case, the temporary and situational cases usually
benefit too. That is the **curb-cut effect**: kerb cuts were demanded by wheelchair users and
are now used daily by parents with prams, travellers with luggage, delivery workers and
cyclists. Captions help deaf viewers, and also people on a train without sound. Keyboard
support helps screen reader users, and also a power user with a broken trackpad.

### The four principles, POUR

The Web Content Accessibility Guidelines (WCAG) organise everything under four principles. If
any one fails, people are excluded.

| Principle | The question | A Testbook example |
| --- | --- | --- |
| **Perceivable** | Can people perceive the content with the senses they have? | Text with too little contrast in dark mode |
| **Operable** | Can people operate every control with the input they have? | A keyboard user stuck on invisible controls |
| **Understandable** | Can people understand the content and how to use it? | A form field whose label vanishes as you type |
| **Robust** | Does it work with the assistive technology people use? | A button that is announced as just "button" |

### Standards and the law, briefly

- **WCAG 2.2** is the current version of the standard, published by the W3C in October 2023.
  It has three conformance levels: A, AA and AAA. **AA is the usual target**, and it is the
  target for Testbook.
- Laws and procurement rules refer to standards like WCAG. Examples include the Americans
  with Disabilities Act and Section 508 in the United States, and the European Accessibility
  Act and EN 301 549 in Europe.
- Requirements differ by country and sector and change over time. **This course is not legal
  advice.** If a project has a legal obligation, ask someone qualified.

Read the [official WCAG 2.2 quick reference](https://www.w3.org/WAI/WCAG22/quickref/) once to
see how the criteria are organised. You do not need to memorise it.

---

## Part 2: Meeting a barrier is not the same as living with it

Exercise 0.1 asks you to meet barriers: to use a page with only a keyboard, or listen to what
a screen reader says. This is useful, and it has limits that you should understand before you
start.

### What it is good for

- It makes an abstract rule concrete. "Focus must be visible" means something once you have
  pressed Tab and watched focus disappear.
- It gives you precise language for a bug report.

### What it cannot do

- **It does not tell you what it is like to be disabled.** Using a screen reader for twenty
  minutes, with your usual habits and a working pair of eyes, is nothing like using one fluently
  every day. Simulation exercises are widely criticised for leaving people with pity or fear
  instead of understanding, and for substituting a few minutes of inconvenience for a person's
  expertise.
- **It does not replace disabled people.** Disabled people are the experts on their own use
  of technology. The principle the disability rights movement has long used is "nothing about
  us without us". The gold standard for accessibility testing is testing with people who use
  assistive technology every day, paid for their expertise.

So the framing for this stage is: **you are experiencing a barrier in order to describe and fix
it, not to claim you understand a life.** Treat the experience as a way to take the work
seriously, and then go and learn from the people who do it every day. A few places to start
are in [Related resources](#related-resources).

---

## Part 3: Built in, then verified

This is the central idea of the stage, and of the whole accessibility thread through the
course.

### The prevention ladder

A defect can be stopped at several points. The earlier it is stopped, the cheaper and less
visible the fix.

| Layer | What happens here | What it can stop |
| --- | --- | --- |
| 1. Requirements and design | Someone decides what the feature must do and for whom | Missing keyboard path, no error design, no dark-mode contrast plan |
| 2. Components and design system | Shared pieces enforce good behaviour | A text field that cannot be created without a label |
| 3. Code review and lint | A person or a tool reads the code | A positive `tabindex`, missing alt text, an interactive element with no key handler |
| 4. Unit and component tests | Small tests check each piece | A missing accessible name, a wrong role |
| 5. Automated end-to-end tests | Tools drive a real browser | Contrast, nesting, tab order, focus after an action |
| 6. Manual testing | A person uses it by keyboard and screen reader | Whether the announcement makes sense, whether the order is logical |
| 7. Real users | People who use assistive technology do real tasks | Everything above missed, and things no checklist anticipated |

Testing sits in layers 4 to 7. Layers 1 to 3 are where prevention happens, and they are cheaper
than everything after them.

### What each layer can and cannot see

No single layer is enough. Automated tools are fast and repeatable, but a snapshot of a page
cannot see things that happen over time or depend on judgement.

- A scan can check that an element **has** a name. It cannot judge whether the name **means
  anything**.
- A scan sees one state. It cannot see what happens **after** you press a key, or what a
  **different theme** looks like unless you switch to it.
- A scan cannot tell you whether a message was **spoken**, or whether it was understandable.

You will see this with your own eyes in the exercises. The [Pitfalls](../../pitfalls/README.md)
you use are small pages that each hide exactly one bug a default scan misses.

### What it means for a tester

If prevention matters more than detection, then a tester's value starts earlier than the first
test:

- Ask "how does a keyboard user do this?" when a feature is first described.
- Write accessibility acceptance criteria into the ticket, so they are requirements and not an
  afterthought.
- Push for shared components that make the right thing the easy thing.
- Then verify, in layers, and know what each layer cannot see.

Stage 5 asks you to do exactly this on a real ticket.

---

## The three exercises

Do them in order. Each has a deliverable you keep, and each builds on the one before.

| Exercise | Time | What you do | What you produce |
| --- | --- | --- | --- |
| [0.1 Meet the barriers](exercises/EXERCISE_0_1_Meet_The_Barriers.md) | 45 minutes | Use eight small pages with a keyboard and assistive technology, and compare each with its fixed version | A barrier log |
| [0.2 Who is excluded](exercises/EXERCISE_0_2_Who_Is_Excluded.md) | 30 minutes | Map each barrier to the people affected and to a WCAG criterion | A completed mapping table |
| [0.3 Built in, then verified](exercises/EXERCISE_0_3_Built_In_Then_Verified.md) | 45 minutes | Trace 19 real defects back to the layer that should have prevented them | A prevention matrix and a set of acceptance criteria |

The reading in this README is the remaining half an hour.

---

## Success criteria

You are ready for Stage 1 when you can:

- [ ] Explain the social model of disability in your own words, with an example
- [ ] Give one permanent, one temporary and one situational example for the same ability
- [ ] Name the four POUR principles and give a web example of each
- [ ] Describe what it was like to use at least three of the broken pages, precisely enough to
      write a bug report
- [ ] Say why a default accessibility scan can pass while real barriers remain
- [ ] Place any accessibility defect on the prevention ladder and justify your choice
- [ ] Write five accessibility acceptance criteria for a feature
- [ ] Explain why testing with disabled people is the gold standard and what a few minutes of
      simulation cannot teach

---

## Related resources

### Hands-on

- [Exercise 0.1: Meet the barriers](exercises/EXERCISE_0_1_Meet_The_Barriers.md)
- [Exercise 0.2: Who is excluded](exercises/EXERCISE_0_2_Who_Is_Excluded.md)
- [Exercise 0.3: Built in, then verified](exercises/EXERCISE_0_3_Built_In_Then_Verified.md)
- [Pitfalls: the small pages used in the exercises](../../pitfalls/README.md)

### Testbook's own accessibility record

- [The audit log: every defect found, all fixed and tested](../../docs/a11y/AUDIT_LOG.md) (this stage uses the first 19)
- [Worked examples: the most instructive findings](../../docs/a11y/WORKED_EXAMPLES.md)
- [The manual testing scripts](../../docs/a11y/manual/README.md)

### Learn from the community

- [W3C Web Accessibility Initiative](https://www.w3.org/WAI/): the standards body's guides,
  including the "Understanding WCAG" documents for every criterion
- [WebAIM](https://webaim.org/): articles, and the annual survey of screen reader users
- [The A11y Project](https://www.a11yproject.com/): a community checklist and posts
- [Microsoft Inclusive Design](https://inclusive.microsoft.design/): the persona spectrum and
  the "solve for one, extend to many" approach

Prefer writing, talks and courses by disabled practitioners wherever you find them.

---

## Self-check quiz (optional)

1. **How should accessibility relate to testing?**

   - A) Testing makes a product accessible
   - B) Accessibility is a requirement designed in from the start, and testing verifies it
   - C) Accessibility is a separate task for a specialist after release
   - D) Accessibility only matters for products with a legal obligation

2. **In the social model of disability, where does the problem lie?**

   - A) In the person's impairment
   - B) In the person's choice of technology
   - C) In barriers designed into products and environments
   - D) In the lack of a medical diagnosis

3. **Which is an example of a situational limitation?**

   - A) A person who is permanently blind
   - B) A person with a broken arm
   - C) A person holding a baby in one arm
   - D) A person with low vision

4. **In Testbook's audit, how many of the 19 defects did the original default accessibility
   scan report?**

   - A) All 19
   - B) About half
   - C) None: it reported zero violations while all 19 existed
   - D) Exactly one

5. **What is true of `opacity: 0` compared with `visibility: hidden`?**
   - A) They are identical
   - B) `opacity: 0` hides an element visually but leaves it keyboard focusable;
     `visibility: hidden` also removes it from the Tab order
   - C) `visibility: hidden` leaves the element focusable
   - D) Only `opacity: 0` hides it from screen readers

**Answers:** [Check your answers here](../solutions/stage_0_quiz_answers.md)

---

## Reflection

Before moving to Stage 1, answer these:

1. **Think of a physical place you know well. Where was accessibility designed in, and where
   was it added afterwards? How could you tell?**

2. **Pick one of the broken pages from Exercise 0.1. Who, beyond people with permanent
   disabilities, would have been affected by it?**

3. **Why can a test suite be green while a product is inaccessible? Use one example from this
   stage.**

4. **What would you want to ask in a design meeting, before any code is written, to prevent one
   of the 19 defects?**

5. **What can a few minutes of using a barrier teach you, and what can it not? What would you
   need to do next to learn the rest?**

**Document your answers** in [reflection.md](reflection.md).

---

## Stage complete

You now start every other stage with the question that most courses leave to the end.

### [Continue to Stage 1: Unit Tests](../stage_1_unit/README.md)
