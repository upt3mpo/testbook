# 📝 Lab Solutions (Maintainers Only)

This directory contains a small set of reference implementations that demonstrate the expected outcomes for the introductory labs. These files are **not** intended for learners—they exist so maintainers can verify exercises quickly, prepare hints, or build automated checks.

---

## Available Reference Solutions

| Lab                            | File                 | Notes                                                     |
| ------------------------------ | -------------------- | --------------------------------------------------------- |
| Lab 1 – Your First Test        | `LAB_01_solution.py` | Demonstrates pytest basics and assertion patterns.        |
| Lab 2 – Testing Real Functions | `LAB_02_solution.py` | Shows password hashing tests that mirror the lab prompts. |
| Lab 5 – API Endpoint Testing   | `LAB_03_solution.py` | Covers TestClient usage and HTTP assertions (filename predates the Lab 5 renumbering). |

> Advanced labs (fixtures, E2E testing, debugging, rate limiting, etc.) encourage learners to compare their work against the production codebase and test suite. We intentionally avoid including end-to-end solutions to preserve the exploratory experience.

---

## Maintaining This Folder

- Keep solutions tightly aligned with the current lab wording; update them whenever exercises change.
- Follow the same linting standards as the main test suite so solutions double as exemplars.
- When adding a new solution, document it in the table above with a one-line summary.
- If a lab is retired or replaced, remove its solution to prevent confusion.

---

## Providing Feedback Without Spoilers

When learners are stuck:

1. Start with the hints already embedded in each lab.
2. Point them at related source files or existing tests (for example `backend/tests/integration/test_api_auth.py`).
3. Encourage running the relevant test suites to compare behaviour.
4. Use these solutions as a last resort, ideally during code review or mentoring.

The self-assessment checklists inside each lab and the progress trackers in `learn/README.md` should be your primary grading tools.

---

## Related Documentation

- `docs/reference/TROUBLESHOOTING.md` – Catalog of issues learners typically encounter.
- `docs/guides/RUNNING_TESTS.md` – How to execute the full test suite referenced by the labs.

Keep this directory lean so learners remain focused on discovery, while maintainers still have the guardrails they need.
