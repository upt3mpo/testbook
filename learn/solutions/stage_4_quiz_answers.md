# Stage 4 Quiz Answers

## Performance, Security and Accessibility Testing Quiz Answers

### 1. What's the main purpose of performance testing?

**Answer: B) To ensure the app works under load**

- Performance testing verifies the app works under expected load
- It identifies bottlenecks and performance issues
- It ensures the app can handle real-world usage
- It's not just about finding bugs or testing individual functions

### 2. What does p95 response time mean?

**Answer: B) 95% of requests are faster than this time**

- p95 means 95th percentile
- 95% of requests complete in this time or faster
- It's more important than average because it shows worst-case performance
- It helps identify performance outliers

### 3. What is the OWASP Top 10?

**Answer: A) The 10 most common web vulnerabilities**

- OWASP Top 10 lists the most critical web application security risks
- It's updated regularly based on real-world data
- It helps prioritize security testing efforts
- It's not about testing tools or frameworks

### 4. Why is security testing important?

**Answer: B) It protects against attacks and data breaches**

- Security testing identifies vulnerabilities before attackers do
- It protects user data and company reputation
- It's required for compliance in many industries
- It's not about speed, user experience, or development time

### 5. What's the difference between load testing and stress testing?

**Answer: B) Load testing checks normal load, stress testing checks breaking point**

- Load testing verifies performance under expected load
- Stress testing finds the breaking point of the system
- Both are important for understanding system limits
- The difference is in the load level, not speed or users

### 6. An automated test confirms an error message has `role="alert"`. What can it NOT tell you?

**Answer: B) Whether the message is understandable and is actually spoken, in good time, by a screen reader**

- A test can prove the **mechanism**: the element exists, it has the right role, focus moved. Those are deterministic.
- It cannot prove the **experience**: whether the words help, whether the announcement arrives at a useful moment, whether a real
  screen reader speaks it as you expect. Only a person with a screen reader can judge that.
- That is why Lab 16 (automation) and Lab 17 (manual testing) come as a pair. Automate the mechanism, and keep a human for the
  experience.
- The other three options (existence, a correct role, a page title) are all things a test can check directly.

## How Did You Do?

- **6/6:** Excellent! You understand performance, security and accessibility testing
- **5/6:** Very good! You're ready for Stage 5
- **4/6:** Good! Review the concepts you missed
- **3/6 or less:** Consider reviewing Stage 4 materials before moving on

## Need More Practice?

- Re-read the [Stage 4 README](../stage_4_performance_security/README.md)
- Complete the [Stage 4 exercises](../stage_4_performance_security/exercises/)
- Try the [Performance Testing Guide](../../tests/performance/README.md)
- Practice with [Security Testing Guide](../../tests/security/README.md)

## Ready for Stage 5?

If you got 4/6 or better, you're ready to move on to [Stage 5: Capstone](../stage_5_capstone/README.md)!

---

_Remember: Performance and security testing are about protecting your application and users. Focus on real-world scenarios and actual threats._
