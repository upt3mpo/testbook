# Glossary

Plain-language definitions for terms used throughout this repo's docs and labs. If you hit an unfamiliar word in a stage README or lab, check here first.

## Core testing concepts

**Test pyramid** — A model for how much of each test type you should have: lots of fast unit tests at the bottom, fewer integration tests in the middle, and a small number of slow end-to-end tests at the top. The shape matters because unit tests are cheap to write and run in milliseconds, while E2E tests are expensive to write and run in seconds-to-minutes — you want most of your bugs caught by the cheap layer.

**Unit test** — A test that exercises one function or one small unit of code in isolation, with no real database, network, or file system involved. If it needs any of those, it's not really a unit test anymore.

**Integration test** — A test that exercises two or more real components working together — most often, an API endpoint hitting a real (test) database. It answers "do these pieces actually work together," which a unit test testing each piece separately can't answer.

**End-to-end (E2E) test** — A test that drives the real application the way a user would: opening a browser, clicking buttons, typing into forms, reading what's on screen. Slower and more fragile than the layers below it, but it's the only layer that can catch a bug that only exists when the real frontend and backend are both running together.

**Fixture** — Reusable setup code that a test depends on, injected automatically by the test framework rather than repeated in every test. In pytest, a fixture is a function decorated with `@pytest.fixture` that a test requests as a parameter. In Vitest/JavaScript, `beforeEach`/`beforeAll` play a similar role, though without pytest's fixture-dependency-injection or scoping — see the note in [Stage 1's fixtures lab](../../learn/stage_1_unit/exercises/LAB_03_Fixtures_And_Test_Data_JavaScript.md) if you're comparing the two tracks.

**Mock** — A fake stand-in for a real dependency (an API call, a database, an external service) that you control in a test, so the test doesn't depend on that real thing actually being available or behaving a particular way. A mock lets you assert things like "was this function called, and with what arguments."

**Stub** — Similar to a mock, but narrower: a stub just returns a canned response when called, without the mock's ability to make assertions about how it was called. In practice, most testing frameworks blur the line between the two — don't lose sleep over the distinction.

**Test double** — The umbrella term covering mocks, stubs, fakes, and spies — anything that stands in for a real dependency in a test.

**Assertion** — A statement in a test that checks whether something is true, and fails the test if it isn't (`assert x == y` in Python, `expect(x).toBe(y)` in JavaScript). A test with zero assertions can pass without actually checking anything — a real anti-pattern, not a hypothetical one.

**AAA pattern (Arrange-Act-Assert)** — A way of structuring a test into three clear phases: set up the data and conditions you need (Arrange), do the thing being tested (Act), and check the result (Assert). Makes a test's intent readable at a glance.

**Flaky test** — A test that sometimes passes and sometimes fails with no code change in between, usually because of a timing assumption (waiting a fixed amount of time instead of waiting for a specific condition), shared state between tests, or a real race condition in the code under test. See [FLAKY_TESTS_GUIDE.md](../guides/FLAKY_TESTS_GUIDE.md).

**Test isolation / independence** — The property that a test can run on its own, in any order, alongside any other tests, and get the same result every time. A test that only passes if it runs after a different specific test is not isolated, and that's a bug in the test, not a quirk to work around.

**Parametrized test** — One test function run multiple times with different input values, instead of writing a near-identical copy of the test for each input. `@pytest.mark.parametrize` in Python, `test.each`/`it.each` in Vitest.

**Coverage** — The percentage of your application's code that gets executed by your test suite. Statement coverage counts lines executed; branch coverage additionally checks that both sides of every `if` were actually exercised (branch coverage is stricter and usually lower than statement coverage for the same test suite). High coverage doesn't guarantee good tests — you can execute a line without actually asserting anything meaningful about what it did.

## Patterns and roles

**Page Object Model (POM)** — An E2E testing pattern where you write one class per page (or major component) of your app, with methods like `login(email, password)` or `create_post(content)`, and your actual tests call those methods instead of repeating raw selectors everywhere. If a selector changes, you fix it in one place instead of in every test that touches that page.

**Contract testing** — Verifying that an API's actual response shape (fields, types) matches what the consumers of that API (usually a frontend) expect, so a backend change that would silently break the frontend gets caught before it ships. See [CONTRACT_TESTING.md](../guides/CONTRACT_TESTING.md).

**Chaos engineering** — Deliberately injecting failures (killing a server, adding network latency, cutting a connection) into a system to verify it degrades gracefully instead of cascading into a full outage. A different testing layer from the pyramid above — it tests resilience under failure, not correctness under normal operation.

**Canary rollout / staged rollout** — Deploying a change to a small subset of servers or users first, watching for problems, and only rolling out to everyone once the canary group looks healthy — instead of deploying to 100% of production at once. See the CrowdStrike case study in [CASE_STUDIES.md](../industry/CASE_STUDIES.md) for what skipping this costs.

**SDET (Software Development Engineer in Test)** — A QA role that writes code — test automation frameworks, tooling, CI/CD pipelines — rather than (or in addition to) manually testing an application. Distinct from a purely manual QA tester role.

## Non-functional testing

**Load testing** — Testing how a system behaves under an expected, realistic amount of traffic — does it stay fast and error-free at the volume you actually expect?

**Stress testing** — Testing how a system behaves *beyond* its expected capacity, deliberately pushing past normal load to find where and how it breaks.

**Smoke test** — A minimal, fast test run (often just a handful of critical checks) used to verify a build or deployment isn't fundamentally broken before running anything more thorough.

**OWASP Top 10** — A regularly updated list, published by the Open Web Application Security Project, of the ten most critical web application security risks (injection attacks, broken access control, etc.). A common reference point for what a security test suite should cover, though it's not exhaustive.

**Rate limiting** — Restricting how many requests a client can make in a given time window, to prevent abuse (brute-force login attempts, scraping, denial-of-service). See [RATE_LIMITING.md](../guides/RATE_LIMITING.md).

## CI/CD

**CI (Continuous Integration)** — Automatically building and testing every code change (usually on every push or pull request) so problems are caught immediately rather than discovered later.

**CD (Continuous Deployment/Delivery)** — Automatically deploying code that passes CI, either straight to production (Continuous Deployment) or to a stage where a human approves the final release (Continuous Delivery).

**Pre-commit hook** — A script that runs automatically before a git commit is allowed to complete, typically for formatting, linting, or quick checks — catching problems before they even reach CI.

**Branch protection** — GitHub repository settings that require certain conditions (passing CI, code review approval) before a branch can be merged, preventing broken or unreviewed code from landing on `main`.

---

Missing a term you had to look up? That's a real gap in this glossary — it should be added, not left for the next learner to hit the same wall.
