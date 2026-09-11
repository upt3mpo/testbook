# 🤔 Stage 2 Reflection: Integration Tests

Document your learning and insights from Stage 2.

---

## Reflection Questions

### 1. Why do integration tests need a database while unit tests don't?

*Your answer here...*

---

### 2. Pick one test from `tests/integration/test_api_posts.py`. What would break if you removed authentication?

**Test chosen:**

**What would break:**

*Your answer here...*

---

### 3. How do test factories make integration testing easier?

*Your answer here...*

---

### 4. What's the difference between a 401 and a 403 status code? Find an example of each in the tests

**401 Unauthorized:**

- **Meaning:**
- **Example test:**

**403 Forbidden:**

- **Meaning:**
- **Example test:**

---

### 5. What's one integration test you would add to improve test coverage?

**Test idea:**

**Why it matters:**

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

## Comparison: Unit vs Integration

**From my experience in Stage 1 vs Stage 2:**

| Aspect | Unit Tests | Integration Tests |
| -------- | ------------ | ------------------- |
| Speed | | |
| Complexity | | |
| Debugging | | |
| Value | | |

---

## Next Steps

**What I want to explore more in Stage 3:**

---

## Real-World Connection

A backend team can ship code where every unit test passes and still take the whole product down the first time real traffic hits it — because the database connection pool wasn't initialized correctly under production configuration, something no unit test in isolation would ever exercise (see the Black Friday outage scenario in [Case Studies](../../docs/industry/CASE_STUDIES.md)). Have you seen — or can you imagine — a case in an app you use where the individual pieces clearly work, but something about how they're wired together in the real environment doesn't?

---

## Interview Prep

1. **"What does an integration test actually verify that a unit test can't?"** Name a concrete failure mode: two functions that each work perfectly in isolation but disagree about the shape of the data passed between them — a unit test of each function alone would never catch that, only a test that runs them together (or against the real API) would.
2. **"How do you keep integration tests from becoming slow or flaky?"** Talk about test database fixtures scoped correctly (fresh state per test, not shared mutable state across tests), and why hitting a real external third-party service in a test suite is a different problem (and usually still gets mocked, even in an "integration" test) — the database is what you're really integrating with here.
3. **"What's contract testing, and why isn't 'the frontend and backend both pass their own tests' enough?"** Explain the gap: each side can be internally correct and still disagree about the response shape at the boundary between them, which is exactly what a schema change with no contract test would let through unnoticed until it broke in production.
4. **"When would you use a test factory instead of hand-writing test data in every test?"** When the same shape of realistic data (a user, a post) needs to exist across many tests — a factory keeps that setup in one place, so a schema change means updating one factory instead of every test that constructs that object by hand.

---

*These notes are gold for interviews when they ask "Tell me about integration testing"*
