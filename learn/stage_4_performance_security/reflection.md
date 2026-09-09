# 🤔 Stage 4 Reflection: Performance & Security

Document your learning about non-functional testing.

---

## Reflection Questions

### 1. Why might an application perform well in development but poorly in production?

*Your answer here...*

---

### 2. What's more important: average response time or p95 response time? Why?

**Average response time:**

**p95 response time:**

**My conclusion:**

*Your answer here...*

---

### 3. Pick one OWASP Top 10 vulnerability. Explain it in simple terms and how you'd test for it

**Vulnerability chosen:**

**Explanation (like I'm explaining to a friend):**

**How to test for it:**

*Your answer here...*

---

### 4. If you had to choose between performance testing OR security testing, which would you prioritize? Why?

**My choice:**

**Reasoning:**

*Your answer here...*

---

### 5. What's one security test you think every application should have?

**Test:**

**Why it's essential:**

*Your answer here...*

---

## My Key Takeaways

**Three things I learned:**

1.
2.
3.

---

## Performance Test Analysis

**From running k6 tests, my results:**

| Metric | Smoke Test | Load Test | Stress Test |
| -------- | ------------ | ----------- | ------------- |
| Avg response time | | | |
| p95 response time | | | |
| Error rate | | | |
| Max users | | | |

**Interpretation:**

---

## Security Vulnerability Hunt

**If I were attacking this app, I would try:**

1.
2.
3.

**Tests that prevent these attacks:**

1.
2.
3.

---

## Real-World Connections

**Performance or security issue I've experienced as a user:**

**How testing could have prevented it:**

---

## Next Steps

**What I want to include in my capstone project:**

---

## Interview Prep

1. **"Walk me through the difference between load testing and stress testing."** Load testing verifies the system handles *expected* traffic correctly; stress testing deliberately pushes past that to find where and how it actually breaks. Different goals, different thresholds — mixing them up in an interview answer is a common tell that you've only skimmed the topic.
2. **"How would you decide what performance thresholds to set for a new endpoint?"** There's no universal number — it depends on the actual user expectation for that action (a search should feel instant, a report generation can tolerate seconds) and your team's SLA. Reference that even this repo's own thresholds are explicitly a teaching default, not something to copy into a real production incident review.
3. **"What's the difference between testing for a SQL injection vulnerability and testing that your dependencies don't have known CVEs?"** One is about your own code's input handling (an application-layer test); the other is about supply-chain risk in code you didn't write (a dependency-scanning concern, tools like `pip-audit`/`npm audit`/Dependabot, not something a hand-written test easily catches).
4. **"Why does rate limiting sometimes cause your own tests to fail, and is that a bug?"** No — it's the rate limiter working. The real lesson is environment configuration: tests need a `TESTING` mode with relaxed limits, and a security suite that "fails" because production-strength rate limiting kicked in is evidence the feature works, not evidence of a broken test.

---

*Performance and security testing differentiate senior QA engineers from juniors!*
