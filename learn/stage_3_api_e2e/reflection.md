# 🤔 Stage 3 Reflection: API & E2E Testing

Document your insights from exploring browser automation and contract testing.

---

## Reflection Questions

### 1. Why are E2E tests slower than integration tests? Is it worth the trade-off?

**Why slower:**

**Trade-off analysis:**

*Your answer here...*

---

### 2. How does the Page Object Model make tests more maintainable?

*Your answer here...*

---

### 3. Pick one E2E test. List 3 things that could cause it to fail (even if the app works fine)

**Test chosen:**

**3 potential failure causes:**

1.
2.
3.

---

### 4. What's the difference between testing an API with integration tests vs contract tests?

**Integration tests:**

**Contract tests:**

**Key difference:**

*Your answer here...*

---

### 5. Imagine you're testing a shopping cart. What would you test with E2E vs integration tests?

### E2E tests (user workflows)

-

-

### Integration tests (API endpoints)

-

-

**Why this split:**

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

## Testing Strategy Insights

**Complete the testing pyramid for a feature you know well:**

```text
       /\      ← E2E tests: ____________________
      /  \
     /____\    ← Contract tests: ____________________
    /      \
   /________\  ← Integration tests: ____________________
  /          \
 /____________\ ← Unit tests: ____________________
```

---

## Page Object Model Practice

**Design a page object for a page you use often (e.g., Gmail, Twitter):**

**Page:** ____________________

### Key locators

-

-
-

### Key methods

-

-
-

---

## Next Steps

**What I want to explore more in Stage 4:**

---

## Real-World Connection

A booking or checkout flow can pass every unit and integration test and still be unusable — a JavaScript error on the submit button, invisible to any test that doesn't actually render the page in a real browser (see [Case Studies](../../docs/industry/CASE_STUDIES.md)). Have you ever hit a bug in a real app — a button that didn't respond, a form that silently failed — that you now realize was exactly this kind of gap: everything "worked" except the one thing a user actually needed?

---

## Interview Prep

1. **"Why are E2E tests slower and more fragile than the other layers, and how do you deal with that?"** Name the real cause (a real browser, real network timing, real rendering — none of which a unit or integration test touches), then the mitigation: Playwright's auto-waiting assertions instead of hardcoded sleeps, and reserving E2E tests for the workflows that actually need a real browser to verify.
2. **"What is the Page Object Model and what problem does it solve?"** It's not about "organization" in the abstract — it's that when a selector changes, you fix it in one page-object class instead of in every test file that happens to reference that element.
3. **"How do you decide what to E2E test versus leave to lower layers?"** Critical, high-value user workflows (login, checkout, the core action your app exists to let users do) — not every possible path through the UI, since that would make the suite too slow and flaky to be useful.
4. **"What's network mocking for in an E2E test, and doesn't that defeat the purpose of testing 'end to end'?"** It's for testing specific frontend states that are hard to trigger reliably otherwise (a slow API, an error response, an empty result) — you're still exercising the real UI, just controlling one variable at the boundary rather than the whole stack.

---

*E2E tests are your portfolio showpieces - capture videos of them for demos!*
