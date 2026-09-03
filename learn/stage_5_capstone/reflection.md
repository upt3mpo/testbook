# Stage 5 Reflection: Job-Ready Capstone

These questions are about the capstone ticket you just worked - the
bookmarks feature (or whatever feature you substituted), delivered as one
bundle: a product requirement, a failing test, a performance threshold, and
a security requirement, all at once. If you can only answer these by
describing one stage at a time, you haven't finished the capstone yet -
finish [Part 2 and 3](README.md#part-2-the-capstone-ticket) first.

---

## Capstone Summary

**Feature built:**

**Link to the decision log:**

**p95 response time actually measured, at what concurrency:**

---

## Reflection Questions

These require judgment, not recall. Each one only makes sense once you've
actually worked the ticket - they're asking about decisions you made, not
facts you can look up.

### 1. You found a bug during E2E testing that was caused by a missing unit test. How do you decide where in the pyramid to add coverage, and what do you add?

Not "add a unit test and an E2E test" - that's not a decision, that's
covering yourself. What specifically tells you the unit-test layer was
the right layer to close the gap in, rather than, say, an integration
test at the API boundary? If you hit this exact situation while working
the bookmarks ticket, use it. If you didn't, construct the scenario from
what you know about where each layer catches (and misses) different
classes of bug.

### 2. Your k6 threshold and your IDOR security check both touch the same query. Which did you build first, and did satisfying one make the other harder or easier?

Point to the actual query. If you didn't notice a relationship between
the two, look again - a user-scoped bookmarks query is doing double duty
whether you designed it that way on purpose or not. Explain what you'd
tell a reviewer who asked "why does this query look the way it does?"

### 3. Imagine the ticket had shipped without the failing test attached - just the product requirement, the performance threshold, and the security requirement. What would you have built differently, and what would you have gotten wrong that the test would have caught?

This is asking you to notice what the given test actually pinned down
that you might not have thought to test yourself (the cross-user IDOR
case is the likely answer, but defend your own).

### 4. Which of the four requirements would you cut first if you had half the time, and which would you refuse to cut no matter what?

Defend both answers. A real answer names the actual risk of cutting each one - "the E2E test
is expensive and the integration tests already prove the API works" is a
defensible reason to cut E2E under time pressure; "ship without the auth
check" is not defensible under any time pressure, and you should be able
to say why the difference isn't just severity, it's blast radius.

### 5. Pick one specific decision in your implementation that you could only have made correctly because of something you learned in exactly one prior stage - not "I used pytest," a real decision. What would you have gotten wrong without that stage?

If you can't name one, that's worth sitting with: it may mean the four
requirements didn't actually interact as much as they could have for
the feature you chose, which is itself worth writing down as an honest
finding about your own capstone.

---

## Real-World Connection

The 2024 CrowdStrike outage - one of the largest IT outages in history -
wasn't a scale problem or a subtle logic bug; it was a testing/rollout-
process gap (no staged canary release before a global push, see
[Case Studies](../../docs/industry/CASE_STUDIES.md)). Across all five
stages of this curriculum, the pattern repeats: the most expensive real
failures are rarely caught by "more tests" in the abstract - they're
caught by testing at the *right layer* for that specific failure mode. As
you finish this capstone, which layer of your own test suite are you
least confident actually covers what it claims to?

---

## Interview Prep

Beyond questions about specific tools, expect these at the capstone/
portfolio-review level:

1. **"Walk me through your test suite design for the feature you built."**
   Be ready to explain not just what you tested, but why - what layer of
   the pyramid each test belongs to and why, and what you deliberately
   chose not to test and why that was a reasonable call.
2. **"You had four requirements land at once. Walk me through how you
   triaged them."** This is the actual capstone question. Your decision
   log is your answer - practice saying it out loud, not just having it
   written down.
3. **"What was the hardest bug or flaky test you ran into, and how did
   you actually fix it?"** Have a real, specific story ready - "I fixed a
   flaky test" is forgettable, "the test was racing a toast notification
   that auto-dismissed after 3 seconds, and I replaced a hardcoded wait
   with an assertion on the notification actually appearing" is not.
4. **"How would this test suite need to change if this app had 100x the
   users?"** A reasonable answer touches on what your current performance
   thresholds don't yet account for, and what your CI would need
   (parallelization, faster feedback) to stay useful at that scale.
5. **"Why should I trust that your tests actually catch regressions,
   instead of just padding a coverage number?"** Point to something
   concrete: a test you wrote that would have caught a real bug, or a
   case where you deliberately chose one meaningful assertion over five
   superficial ones.

---

## Portfolio Artifacts

- [ ] GitHub repository link: _______________
- [ ] `DECISION_LOG.md`: _______________
- [ ] Coverage report screenshot: _______________
- [ ] E2E test video or screenshot: _______________
- [ ] `TESTING.md` documentation: _______________

---

## Next Steps

- [ ] Update resume with a bullet describing the bookmarks ticket (or
      your substitute feature) - lead with the triage decision, not the
      tools
- [ ] Read [COMPLETION.md](../COMPLETION.md) - it closes out the full
      5-stage path and points you toward what to learn next

**You've got this.**
