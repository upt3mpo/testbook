# 🤔 Stage 1 Reflection: Unit Tests

Use this space to document your learning journey through Stage 1.

---

## Reflection Questions

### 1. What surprised you most about unit tests?

*Your answer here...*

---

### 2. Why do we use fixtures instead of just creating test data in each test?

*Your answer here...*

---

### 3. Pick one test from `tests/unit/test_auth.py`. What would happen if you removed the assertion?

**Test chosen:**

*Your answer here...*

---

### 4. How are unit tests different from just manually testing a function in the Python REPL?

*Your answer here...*

---

### 5. What's one thing you're still confused about?

*Your answer here...*

---

## My Key Takeaways

**Three things I learned:**

1.
2.
3.

---

## Challenges I Faced

**Problem:**

**How I solved it:**

---

## Next Steps

**What I want to explore more:**

---

## Real-World Connection

Knight Capital lost $440 million in 45 minutes in 2012 — not from a subtle logic bug, but from a deployment that left dormant, untested code paths reachable in production (see [Case Studies](../../docs/industry/CASE_STUDIES.md)). Unit tests don't directly prevent a deployment mistake like that one, but they build the habit this stage is really teaching: verifying a piece of code does exactly what you think it does, in isolation, before it ever gets the chance to surprise you in production. What's a time — in this app, a side project, or just reading about a bug like Knight Capital's — where a small, cheap check up front would have caught something expensive later?

---

## Interview Prep

Questions an interviewer might actually ask about what you just learned, and what a strong answer touches on:

1. **"Walk me through the AAA pattern and why you'd structure a test that way."** A strong answer names all three phases, explains that separating them makes a test's intent readable without running it, and gives a concrete example from this stage rather than reciting the definition.
2. **"What's the difference between a mock and the real thing you're testing, and why not just use real dependencies everywhere?"** Touch on speed (mocks run in milliseconds, real dependencies don't), determinism (a mock always behaves the way you told it to; a real API might not), and the tradeoff (mocking too much means you're not testing real integration — that's what Stage 2 covers).
3. **"If your test suite has 90% coverage, does that mean your code is well-tested?"** No — coverage tells you code was executed, not that anything meaningful was asserted about it. A good answer gives an example: a test that calls a function but doesn't check its return value adds to coverage without adding confidence.
4. **"How do you decide what to unit test versus what to leave for integration or E2E tests?"** Reference the testing pyramid: unit tests for pure logic and edge cases in isolation, integration tests for how pieces work together, E2E for full user workflows — and that most of your tests should be the cheap, fast layer.

---

*Keep these notes! They're great material for interviews and portfolio documentation.*
