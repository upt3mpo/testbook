# Stage 5: Job-Ready Capstone

**Build Your Testing Portfolio**

> **💡 Language Selection**: This guide includes both Python and JavaScript examples. Both are expanded by default so you can see all approaches. Click the language tabs to collapse sections you don't need.

## Your Progress

[████████████████████████████] 100% complete

✅ Stage 1: Unit Tests (completed)<br>
✅ Stage 2: Integration Tests (completed)<br>
✅ Stage 3: API & E2E Testing (completed)<br>
✅ Stage 4: Performance & Security (completed)<br>
→ **Stage 5: Capstone** (you are here)

**Estimated time remaining:** 4-6 hours (core content) + 2-4 hours (optional exercises)

<h2 id="entry-criteria">Entry Criteria: What You Should Know Before Starting</h2>

Stage 5 doesn't teach new testing techniques - it asks you to combine everything from Stages 1-4 on a feature of your own choosing. Before starting, you should be able to:

- Write a unit test with the Arrange-Act-Assert pattern and explain what it isolates (Stage 1)
- Write an integration test that hits a real API endpoint with `TestClient` or an equivalent, including auth and database state (Stage 2)
- Write a Playwright E2E test that drives a full user workflow through the UI, using Page Object Model for at least one page (Stage 3)
- Explain what a k6 load test threshold measures and write at least one security test for input validation or authorization (Stage 4)

If any of those feel shaky, revisit that stage's exercises before starting the capstone - the project below assumes you can do all four without step-by-step guidance.

<h2 id="table-of-contents">Table of Contents</h2>

- [Entry Criteria](#entry-criteria)
- [Why a Testing Portfolio Matters: Your Gateway to Career Success](#why-a-testing-portfolio-matters-your-gateway-to-career-success)
- [Part 1: What Is a Testing Portfolio?](#part-1-what-is-a-testing-portfolio)
- [Part 2: The Capstone Ticket](#part-2-the-capstone-ticket)
- [Part 3: Working the Ticket](#part-3-working-the-ticket)
- [Part 4: Creating Portfolio Artifacts](#part-4-creating-portfolio-artifacts)
- [Part 5: Professional Presentation](#part-5-professional-presentation)
- [Part 6: Interview Preparation](#part-6-interview-preparation)
- [Part 7: Additional Patterns](#part-7-additional-patterns)
- [Success Criteria](#success-criteria)
- [Why This Matters](#why-this-matters)
- [Related Resources](#related-resources)
- [Self-Check Quiz (Optional)](#self-check-quiz-optional)
- [Reflection](#reflection)
- [Stage Complete](#stage-complete)

---

## Why a Testing Portfolio Matters: Your Gateway to Career Success

A resume can claim "experienced in test automation." A portfolio proves it: real test code an interviewer can open, a coverage report they can inspect, a video of an E2E suite actually running. That difference matters most exactly when it's hardest to show any other way - in an interview, when someone asks "can you show me something you've built?" and the honest answer needs to be yes.

What actually goes in one: working code that runs (not snippets), a couple of screenshots or a short video as visual proof, and documentation that explains your testing strategy in your own words - not just "here are 50 tests" but "here's why I tested it this way." The rest of this stage builds exactly that, using the feature you choose in Part 2.

---

<h2 id="part-1-what-is-a-testing-portfolio">Part 1: What Is a Testing Portfolio?</h2>

### The Job Interview Analogy

Imagine you're applying for a job as a chef. You could tell the interviewer "I know how to cook," or you could show them a portfolio of your best dishes, cooking techniques, and kitchen management skills. A testing portfolio works the same way.

A **testing portfolio** is a collection of your best testing work that demonstrates your skills to potential employers.

### Why Portfolios Matter

1. **Proof of skills**: Shows you can actually do the work
2. **Differentiation**: Sets you apart from other candidates
3. **Conversation starter**: Gives interviewers something specific to discuss
4. **Confidence**: Proves you're ready for the job

### What Makes a Great Testing Portfolio

**Essential Elements:**

- **Working code**: Real tests that actually run
- **Documentation**: Clear explanations of what you built
- **Visual proof**: Screenshots, videos, coverage reports
- **Professional presentation**: Clean, organized, easy to navigate

**Portfolio vs Resume:**

- **Resume**: Lists your skills and experience
- **Portfolio**: Shows your skills in action

### The Testing Portfolio Pyramid

```text
       /\      ← Visual Demos (videos, screenshots)
      /  \     ← Documentation (test plans, reports)
     /____\    ← Working Code (actual test suites)
    /      \   ← Test Results (coverage, metrics)
   /________\  ← Project Descriptions (what you built)
```

**Bottom to top:** Start with working code, add documentation, create visual proof, then package it professionally.

---

<h2 id="part-2-the-capstone-ticket">Part 2: The Capstone Ticket</h2>

### Why This Isn't Four Separate Assignments

In Stages 1 through 4, you practiced one layer of the pyramid at a time - unit tests in isolation in Stage 1, then integration, then E2E, then performance and security. That's the right way to *learn* each layer. It's not how a real ticket arrives.

A real ticket shows up as one bundle: a product requirement, a test someone already wrote against it, a performance budget it has to meet, and a security bar it can't ship without. Nobody hands them to you one at a time, waiting for you to finish the last one before showing you the next. You read all four before you decide what to do first - and that decision is the actual skill this stage is testing. Getting the code working is Stages 1-4. Deciding how to get there, in what order, and being able to explain why, is the capstone.

### The Ticket

You're picking up a real ticket for Testbook: **add post bookmarks.**

**Product requirement:**

> Users can bookmark any post they can see. A "Saved Posts" view (reachable from Settings) lists everything they've bookmarked, most recently bookmarked first. Users can un-bookmark. Bookmark state is private - Sarah can't see what Mike has bookmarked, and Mike can't see Sarah's list either.

**A test a teammate already wrote**, before the endpoint existed, so it currently fails with a 404 on every case. Drop it into `backend/tests/integration/test_api_bookmarks.py` and treat it as the contract your implementation has to satisfy, not a suggestion:

```python
"""Integration tests for post bookmarks - written against the spec,
before the endpoint exists. This file should fail until you build it."""

from auth import create_access_token


class TestBookmarks:
    def test_bookmark_a_post(self, client, auth_headers, test_post):
        response = client.post(f"/api/posts/{test_post.id}/bookmark", headers=auth_headers)
        assert response.status_code == 201

    def test_bookmarked_post_appears_in_saved_posts(self, client, auth_headers, test_post):
        client.post(f"/api/posts/{test_post.id}/bookmark", headers=auth_headers)

        response = client.get("/api/users/me/bookmarks", headers=auth_headers)

        assert response.status_code == 200
        post_ids = [p["id"] for p in response.json()]
        assert test_post.id in post_ids

    def test_unbookmark_removes_it_from_saved_posts(self, client, auth_headers, test_post):
        client.post(f"/api/posts/{test_post.id}/bookmark", headers=auth_headers)
        client.delete(f"/api/posts/{test_post.id}/bookmark", headers=auth_headers)

        response = client.get("/api/users/me/bookmarks", headers=auth_headers)

        post_ids = [p["id"] for p in response.json()]
        assert test_post.id not in post_ids

    def test_bookmarking_requires_authentication(self, client, test_post):
        response = client.post(f"/api/posts/{test_post.id}/bookmark")
        assert response.status_code == 401

    def test_cannot_see_another_users_bookmarks(self, client, auth_headers, test_user_2, test_post):
        """Sarah bookmarks a post. Mike's own /me/bookmarks must not include it."""
        client.post(f"/api/posts/{test_post.id}/bookmark", headers=auth_headers)

        mike_token = create_access_token(data={"sub": test_user_2.email})
        mike_headers = {"Authorization": f"Bearer {mike_token}"}

        response = client.get("/api/users/me/bookmarks", headers=mike_headers)

        post_ids = [p["id"] for p in response.json()]
        assert test_post.id not in post_ids
```

**Performance requirement**, from the same ticket:

> Saved Posts has to stay usable for a power user with hundreds of bookmarks. Load-test `GET /api/users/me/bookmarks` with k6 for a user who has 500 bookmarked posts, and hold p95 under 300ms at 20 concurrent users. Use `tests/performance/load-test.js` as your starting structure and pick a threshold you can defend in the decision log below.

**Security requirement**, from the same ticket:

> This ships with security sign-off attached, not bolted on after. At minimum: bookmarking must require authentication (the test file above already pins this), a user must not be able to read or modify another user's bookmark list under any input (the IDOR case above checks the direct route - now find at least one more way a typical implementation gets this wrong, and write a test for it), and the bookmark endpoints follow the same rate-limiting convention already used in `routers/auth.py` (`slowapi`, permissive under `TESTING=true`, conservative in production) rather than being left unlimited.

### Your Job

Build the feature until the test file above passes, meet the performance threshold, satisfy the security requirement, and add one Playwright E2E test (Python or JS, your choice, Page Object Model) that drives the real user workflow: log in, bookmark a post from the feed, navigate to Saved Posts, see it there, un-bookmark it, confirm it's gone.

Then write the [decision log](#part-3-working-the-ticket) - not a test plan you wrote in advance, a record of the order you actually worked in and why.

**Prefer a different feature?** The same four-artifact structure applies to anything with real state and real access control - "pin one post to your profile," or "mute a user without blocking them," work the same way. Write your own failing test first (that's the Stage 2 skill), and don't skip the performance or security artifact just because you changed the feature. Dropping either one is exactly the shortcut this stage exists to close off.

---

<h2 id="part-3-working-the-ticket">Part 3: Working the Ticket</h2>

### There Is No One Correct Order

Different reasonable engineers triage this ticket differently, and that's fine - what matters is that your order is a decision, not a default. A few real considerations that should shape it:

- The failing test file is your fastest feedback loop. Making it pass first tells you whether your data model and endpoints are shaped right, before you spend time on performance or the UI.
- The security requirement isn't a separate pass at the end. The IDOR check in the test file constrains your query design from the start - you can't query bookmarks by post alone without also filtering by the requesting user. Build it the naive way first and you'll be rewriting the query later, not patching it.
- The performance and security requirements pull in a related direction here: satisfying "don't leak other users' bookmarks" cheaply usually means an indexed, user-scoped query - which is also most of what "fast at 500 bookmarks" needs. Notice when a requirement from one stage does double duty for another; that's a real signal, not a coincidence to write off.
- The E2E test is your slowest feedback loop, and it depends on the backend being done. Writing it first would mean testing against a feature that doesn't exist yet.

None of that is a prescribed order. It's the kind of reasoning your decision log should contain.

### The Decision Log

Not a test plan - a short, honest account of what you actually did, written after the fact. Keep it to what a reviewer would actually want to know:

```markdown
# Decision Log: Post Bookmarks

## Order I worked in, and why

[What did you do first? Why - not "because Stage 2 comes before Stage 4,"
but because of something specific about *this* ticket. What did you learn
from that step that changed your plan for the next one?]

## Where the requirements pulled against each other

[Performance and security often trade off - stricter checks cost time,
looser ones cost risk. Did bookmarks actually force a tradeoff, or did
one requirement end up serving both (see the query-design note above)?
Be specific about what you'd do differently under a tighter deadline.]

## What I deliberately did not do, and why that's a reasonable call

[Every real ticket ships with some scope deliberately left out. Name
something you chose not to build or not to test, and defend the call -
not "I ran out of time," but "here's the actual risk of skipping this,
and here's why I judged it acceptable."]

## Where each stage's knowledge was actually load-bearing

[Not "I used pytest for backend tests and Playwright for E2E" - that's
just naming tools. Point to one specific decision in this feature you
could only have made correctly because you understood a specific prior
stage - a fixture-scope choice from Stage 1, an authorization pattern
from Stage 2, a locator strategy from Stage 3, a threshold number you
can defend from Stage 4.]
```

Save this alongside your tests as `DECISION_LOG.md` - it belongs in your portfolio (see [Part 4](#part-4-creating-portfolio-artifacts)) as much as the tests themselves do.

---

<h2 id="part-4-creating-portfolio-artifacts">Part 4: Creating Portfolio Artifacts</h2>

### The Showcase Analogy

Think of portfolio artifacts like a museum exhibit. You need:

- **The artwork** (your code) - The main attraction
- **The placard** (documentation) - Explains what it is
- **The video tour** (demos) - Shows it in action
- **The curator's notes** (test reports) - Professional analysis

### Essential Portfolio Artifacts

**Artifact 1: Test Coverage Report**

```bash
# Run these from the backend/ directory
cd backend

# Generate HTML coverage report
pytest --cov --cov-report=html

# Generate detailed coverage report with missing lines
pytest --cov --cov-report=html --cov-report=term-missing

# Generate coverage report for specific modules
pytest --cov=auth --cov=models --cov-report=html

# Screenshot the coverage report
# Open htmlcov/index.html and capture screenshot
```

**What to include in your portfolio:**

- Overall coverage percentage (aim for 80%+)
- File-by-file coverage breakdown
- Highlight: "Achieved 85% test coverage across 15 test files"
- Screenshot of the HTML coverage report

**Artifact 2: Test Execution Video**

```bash
# Run E2E test with recording
VIDEO_ON_FAILURE=true HEADLESS=false pytest tests/test_e2e_feature.py

# Run with slow motion for better video
VIDEO_ON_FAILURE=true HEADLESS=false pytest tests/test_e2e_feature.py --slowmo=1000

# Run specific test with video
VIDEO_ON_FAILURE=true HEADLESS=false pytest tests/e2e-python/test_auth.py::TestAuthentication::test_register_new_user_successfully -v

# Result: video of test running
```

**What to include in your portfolio:**

- 30-60 second clip showing test execution
- Clear view of browser automation
- Highlight: "E2E test demonstrating complete user registration workflow"
- Optional: Voiceover explaining what's being tested

**Artifact 3: Test Report**

```bash
pytest --html=test-report.html --self-contained-html
```

**What to include:**

- Pass/fail statistics
- Test execution time
- Any failures and how you fixed them

**Artifact 4: Test Documentation**

Create `TESTING.md` for your feature:

```markdown
# Testing Documentation: [Feature Name]

## Test Coverage

- **Unit Tests:** 15 tests, 100% function coverage
- **Integration Tests:** 12 tests, all endpoints covered
- **E2E Tests:** 5 tests, critical paths verified
- **Security Tests:** 3 tests, OWASP Top 10 addressed

## Test Strategy

[Explain your approach]

## Notable Test Cases

[Highlight interesting tests]

## Results

[Show metrics and outcomes]
```

---

<h2 id="part-5-professional-presentation">Part 5: Professional Presentation</h2>

### The Job Interview Analogy

Think of presenting your portfolio like giving a TED talk. You need:

- **A compelling story** (what you built and why)
- **Visual aids** (screenshots, videos, code)
- **Clear explanations** (what each part does)
- **Confident delivery** (you know your stuff)

### Resume & Portfolio Content

**Resume Bullet Points:**

Use these templates (fill in your specifics):

**For Testbook:**

- Built comprehensive test automation suite with pytest and Playwright, achieving 85%+ backend code coverage across 183 automated tests
- Implemented E2E testing framework using Page Object Model pattern, reducing test maintenance time by 40%
- Developed security test suite covering OWASP Top 10 vulnerabilities, identifying and documenting 3 critical issues
- Created performance testing strategy using k6, establishing baseline metrics for 500 concurrent users

**For Your Capstone:**

- Designed and implemented test automation for [feature] including unit, integration, E2E, and security tests
- Achieved 85%+ test coverage using pytest, FastAPI TestClient, and Playwright
- Documented testing strategy and created reusable test fixtures and factories
- Produced portfolio artifacts including coverage reports, test videos, and comprehensive documentation

### Portfolio README Template

Create `PORTFOLIO.md`:

```markdown
# Testing Portfolio - [Your Name]

## Overview

I completed Testbook's 5-stage learning path and built a comprehensive test suite demonstrating professional QA engineering skills.

## Skills Demonstrated

### Test Automation

- Pytest (unit and integration testing)
- Playwright (E2E browser automation)
- k6 (performance testing)
- Test fixture design
- Page Object Model pattern

### Testing Types

- ✅ Unit testing
- ✅ Integration testing
- ✅ API testing
- ✅ E2E testing
- ✅ Security testing
- ✅ Performance testing

## Projects

### 1. Testbook Learning Path

**Duration:** [Your timeframe]
**Description:** Completed 5-stage curriculum covering all aspects of test automation

**Achievements:**

- Wrote 50+ tests across all test types
- Achieved 85%+ coverage
- Implemented Page Object Model
- Created security test suite

### 2. Capstone: [Feature] - Built From a Bundled Ticket

**Description:** Given a product requirement, a failing integration test, a
performance threshold, and a security requirement simultaneously - built
[feature] to satisfy all four and documented the triage decisions in a
decision log.

**Test Coverage:**

- [N] integration tests (the given contract, extended with an IDOR test)
- 1 E2E test covering the full user workflow (Page Object Model)
- 1 k6 load test with a defended threshold
- [N] security tests (auth, IDOR, rate limiting)

**Results:**

- All four requirements satisfied, in an order documented in
  `DECISION_LOG.md`
- [p95 response time you actually hit] at [concurrency] concurrent users
- 0 production bugs in 30 days
```

---

<h2 id="part-6-interview-preparation">Part 6: Interview Preparation</h2>

### The Performance Analogy

Think of job interviews like performing in a play. You need:

- **Know your lines** (practice common questions)
- **Know your character** (understand your role as a QA engineer)
- **Rehearse your scenes** (practice explaining your work)
- **Bring your props** (have your portfolio ready)

### Common QA Interview Questions

**Technical Questions:**

**Q: "Explain the difference between unit, integration, and E2E tests."**
*Use the test pyramid. Give examples from Testbook.*

**Q: "How do you decide what to test?"**
*Talk about risk-based testing, critical paths, test strategy.*

**Q: "Walk me through how you'd test [feature]."**
*Show your test plan from this capstone.*

**Q: "How do you handle flaky tests?"**
*Discuss waits, retries, isolation, debugging techniques.*

**Q: "What's your approach to security testing?"**
*Reference OWASP Top 10, your security tests.*

**Behavioral Questions:**

**Q: "Tell me about a bug you found."**
*Prepare story: What was it? How'd you find it? Impact? How'd you document it?*

**Q: "Describe a time you had to learn a new testing tool."**
*Your Testbook journey! Playwright, pytest, k6.*

**Q: "How do you prioritize testing when time is limited?"**
*Risk-based testing, smoke tests, critical paths.*

### Show Your Work

**Bring to interviews:**

1. **Laptop with code ready** - Demo your tests running
2. **Coverage report screenshot** - Visual proof
3. **Test execution video** - Show E2E tests in action
4. **TESTING.md document** - Professional documentation
5. **GitHub repo link** - Clean, public portfolio

**Practice this demo:**
"Here's a test I wrote for [feature]. Let me show you how it runs..."
[Run test, explain each step, show passing result]

---

<h2 id="part-7-additional-patterns">Part 7: Additional Patterns</h2>

**📝 Note:** The patterns below are **additional enhancements** to your professional testing capabilities. All the **core concepts** needed to meet the Stage 5 success criteria are covered in Parts 1-6 above.

These patterns enhance your professional testing capabilities:

### CI/CD Integration

Set up automated testing in GitHub Actions:

```yaml
name: Test Suite
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - name: Set up Python
        uses: actions/setup-python@v7
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest --cov --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v7
```

### Test Data Management

Create realistic test data factories:

```python
from factory import Factory, Faker
from your_models import User, Post

class UserFactory(Factory):
    class Meta:
        model = User

    username = Faker('user_name')
    email = Faker('email')
    is_active = True

class PostFactory(Factory):
    class Meta:
        model = Post

    content = Faker('text', max_nb_chars=280)
    user = SubFactory(UserFactory)
```

### Performance Testing

Add k6 performance tests:

```javascript
import http from "k6/http";
import { check } from "k6";

export let options = {
  stages: [
    { duration: "2m", target: 10 },
    { duration: "5m", target: 10 },
    { duration: "2m", target: 0 },
  ],
};

export default function () {
  let response = http.get("http://localhost:8000/feature");
  check(response, {
    "status is 200": (r) => r.status === 200,
    "response time < 200ms": (r) => r.timings.duration < 200,
  });
}
```

---

<h2 id="success-criteria">Success Criteria</h2>

You're ready for QA engineering roles when you can:

**Portfolio Requirements:**

- [] Complete test suite with 80%+ coverage
- [] Professional documentation
- [] Visual artifacts (screenshots, videos)
- [] Clean, public GitHub repository
- [] Resume-ready project descriptions

**Technical Skills:**

- [] Made the given failing integration test pass, plus your own IDOR test
- [] Wrote one E2E test (Page Object Model) covering the full user workflow
- [] Met a k6 performance threshold you can defend, not just one you copied
- [] Implemented and tested the rate-limiting and authorization requirements
- [] Wrote a decision log explaining the order you worked in and why -
      not a test plan written in advance
- [] Debug failing tests

**Professional Skills:**

- [] Document your work clearly
- [] Present your portfolio confidently
- [] Answer technical questions
- [] Explain your testing approach
- [] Show continuous learning

---

<h2 id="why-this-matters">Why This Matters</h2>

### For Your Career

- **Portfolio differentiation** - Stand out from other candidates
- **Technical credibility** - Prove you can do the work
- **Interview confidence** - Have concrete examples to discuss
- **Career advancement** - Show growth and learning
- **Professional reputation** - Build your brand as a QA engineer

### In Real QA Teams

- **Portfolio thinking** - Always document your work
- **Continuous improvement** - Keep learning and growing
- **Knowledge sharing** - Help others learn from your work
- **Professional development** - Build skills systematically
- **Career planning** - Know where you want to go

---

<h2 id="related-resources">Related Resources</h2>

### Portfolio Development

- [Portfolio Guide](../../docs/guides/PORTFOLIO.md)
- [Interview Preparation](../../docs/industry/CAREER_GUIDE.md#interview-preparation)

### Technical Resources

- [Testing Best Practices](../../docs/guides/TESTING_GUIDE.md)
- [Running Tests & Coverage Reports](../../docs/guides/RUNNING_TESTS.md)

### Career Resources

- [QA Career Guide (paths, salary, interview prep)](../../docs/industry/CAREER_GUIDE.md)

---

<h2 id="self-check-quiz-optional">Self-Check Quiz (Optional)</h2>

Before considering yourself job-ready, can you answer these questions?

1. **What's the main purpose of a testing portfolio?**

   - A) To show off your coding skills
   - B) To demonstrate your testing abilities to employers
   - C) To replace your resume
   - D) To get more GitHub stars

2. **What should you include in your portfolio?**

   - A) Only passing tests
   - B) Test results, code samples, and documentation
   - C) Only code, no documentation
   - D) Only screenshots

3. **Why is documentation important in testing?**

   - A) It makes tests run faster
   - B) It helps others understand and maintain tests
   - C) It's required by law
   - D) It makes tests more fun

4. **What's the difference between a test plan and test cases?**

   - A) Test plan is faster
   - B) Test plan is high-level strategy, test cases are specific steps
   - C) Test cases are more important
   - D) There's no difference

5. **What makes a good QA engineer?**
   - A) Only technical skills
   - B) Only communication skills
   - C) Technical skills, communication, and problem-solving
   - D) Only problem-solving skills

**Answers:** [Check your answers here](../solutions/stage_5_quiz_answers.md)

---

<h2 id="reflection">Reflection</h2>

Before considering yourself job-ready, answer these:

1. **What was the most challenging part of building your test suite?**

2. **How did you decide what to test and what to skip?**

3. **What would you do differently if you started over?**

4. **How confident do you feel explaining your testing approach to others?**

5. **What's one area you want to improve before applying for jobs?**

**Document your answers** in [reflection.md](reflection.md).

---

<h2 id="stage-complete">Stage Complete</h2>

You now have a complete testing portfolio and are ready for QA engineering roles!

### [View Your Portfolio](../../docs/guides/PORTFOLIO.md)

Once you've finished the reflection above, read [COMPLETION.md](../COMPLETION.md) - it closes out the full 5-stage path and points you toward what to learn next.

---

*Your portfolio is never "done" - keep updating it as you learn new skills and complete new projects.*
