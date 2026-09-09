# Testbook Full Audit — Report

**Date:** 2026-08-27
**Scope:** University curriculum audit (Part 1) + Principal QA engineering audit (Part 2) + consolidation (Part 3) + additions (Part 4), per the maintainer's audit brief.
**Audience:** the repo maintainer. This document is a record of the pass, not student-facing material.

This pass produced 28 commits on `develop`, none pushed (per the maintainer's instruction — local review first). All test-suite numbers below are from real runs against the live app during this session, not estimates.

---

## 1. Headline findings

The single most significant discovery was **not** a documentation-quality problem — it was a **fabrication problem**. `docs/industry/CASE_STUDIES.md` and `docs/industry/INDUSTRY_PRACTICES.md` presented invented company quotes, an incorrect root cause for a real incident (Knight Capital's $440M loss was attributed to a fabricated "missing else statement"; the real cause was a deployment failure reactivating dormant code), a wrong vulnerability type for another real incident (Equifax attributed to SQL injection; the real cause was an unpatched Apache Struts RCE), and three anonymous "major company" incidents with fabricated dollar figures presented as real, dated events. This was corrected — see §2.

The second most significant finding was that **test-count and coverage claims scattered across ~15 files had drifted from reality**, in both directions — some too high, some (my own early "fix," corrected later — see §7) too low. Every number in this report was verified by actually running the suite, not by editing prose.

## 2. Part 1 — Curriculum audit

### Orientation and accuracy (1A, 1F)
- Fixed a three-way contradiction in course-duration estimates: README.md, learn/README.md, and docs/INDEX.md each stated a different total (24-34h / 24-34h+14-20h / 12-18h) with different per-stage breakdowns. Standardized on 24-34h core + 14-23h optional (the figure the math actually supports), since README.md and learn/README.md already agreed with each other and docs/INDEX.md was the outlier.
- Removed a stale `docs/course/` reference and a "Recently Organized" changelog section from docs/INDEX.md — process artifacts with no teaching value, left over from a prior reorganization, contradicting other text on the same page.
- Removed a "Hands-On Exercises" section in docs/INDEX.md referencing fabricated lab names ("Lab 4B", "Lab 6B/6C") and a stale "planned Labs 7+" roadmap claiming topics (performance, security, CI/CD) weren't covered when they already are, in Stage 4/5.
- Full external-link audit: checked every URL in `docs/` and `learn/` (101 unique URLs) against real HTTP responses. Found and fixed 10 dead links (Ministry of Testing, Appium docs, Vitest guide ×2, Playwright JS docs, k6 Cloud — found later in a second sweep of `tests/`).
- A dedicated `markdown-link-check` run (using the repo's own `.markdown-link-check.json`) across all 91 markdown files in `docs/`, `learn/`, `tests/*/README.md`, and the top-level READMEs confirmed every internal link and anchor resolves after all edits.
- A leaked personal absolute path (the repo owner's actual home directory, in a Stage 4 lab and in the old MARKDOWN_VALIDATION.md) was found and removed.

### Language-choice guidance (1D)
Was missing entirely — the closest thing was a feature-comparison table with no actual decision guidance. Added real content to `learn/README.md`'s "Choose Your Track" section: what each language is actually used for in test automation specifically, an honest (non-fabricated, non-statistic-citing) take on job-market patterns, the real learning-curve difference (async/await is a genuine JS-specific hurdle, not just syntax), and a decision framework keyed to the student's stated goal.

### Python/JS path walkthrough and mirroring (1B, 1C, 1E)
Two parallel deep reviews (one per stage-pair, verified against the real backend/frontend source, not just read for style) found and fixed real defects, not just prose issues:

- **A lab that had Python-track students building files inside the JavaScript test directory** (`tests/e2e/` instead of `tests/e2e-python/`) throughout Stage 3's Lab 12 — every path reference was wrong.
- **A lab titled "Cross-Browser Testing" that never actually covered running against more than one browser** — added real content (the commented-out Firefox/WebKit projects in `tests/playwright.config.js` already existed; the lab just never told students to use them).
- Wrong API status codes and response shapes in two lab solution files (`learn/solutions/LAB_02_solution.py`, `LAB_03_solution.py`): asserted 200 where the API returns 201, 401 where FastAPI's `HTTPBearer` returns 403, a nonexistent `reaction_type` field instead of the real `user_reaction`/`reactions_count`, a test for a comment-deletion endpoint that doesn't exist in the API at all, and a hardcoded 30-minute token-expiry assumption where the real default is 1440 minutes. Verified all tests in both files now pass against the real backend.
- Quiz answer keys for Stage 3 and Stage 5 no longer matched their own stage's quiz questions (the quizzes had been edited since the keys were last updated) — rewritten to match.
- A fabricated k6 load-test payload field (`title`, which doesn't exist on the real `PostCreate` schema) and a missing trailing slash on the real `/api/posts/` route.
- Roughly a dozen broken/mislabeled "Next Lab" cross-references across Stage 2-4 labs.
- Three genuine Python/JS curriculum divergences (fixture dependency-injection has no Vitest equivalent; Stage 2 Lab 6 teaches entirely different material per track; a "Python advantage" framing for combined API+UI testing was actually just a JS-labs coverage gap, not a language limitation) were acknowledged explicitly in the affected files rather than left as silent asymmetry, per the audit's own "fill or explicitly acknowledge" rule.

### Voice / AI-tell pass (1G)
Applied to: both entry-point docs, all 5 stage READMEs, `docs/concepts/` (4 files), `docs/industry/` (4 files → now 3, see §4). Removed decorative header emoji, invented company quotes, fabricated case-study statistics, and repetitive bullet-list scaffolding that restated the same idea 3-4 times per section (most dramatically in `docs/concepts/TESTING_PHILOSOPHY.md`, condensed by ~150 lines without losing content).

**Not done exhaustively:** a full line-by-line voice rewrite of every file in `docs/guides/` and `docs/reference/` — several of these are very large (`WINDOWS_SETUP.md` is 2,264 lines, `TESTING_GUIDE.md` 1,348). Factual issues (stale counts, dead links, wrong API contracts) were fixed across all of them; a full prose-quality pass was not attempted given the size, and is the single largest remaining Part 1 item if this continues.

### Completeness (1H)
- Added explicit entry criteria to Stage 5's README (four concrete, checkable skills from Stages 1-4) — none existed before.
- Added a performance-test line item to the capstone's test-plan checklist — the capstone previously never required touching Stage 4's performance-testing side, only security.

---

## 3. Part 2 — Engineering audit

### Real numbers (verified by running the suites, not reading badges)

| Suite | Count | Notes |
|---|---|---|
| Backend (pytest) | **183 passed, 1 skipped** (184 collected) | Was 180 before this pass added 3 tests via splitting; see §7 for a self-correction along the way |
| Backend coverage | **85.98% statement**, 81.23% branch | Badge claim of 86% was already accurate (statement coverage) |
| Frontend (Vitest) | **40 passed** | Matches prior badge exactly |
| Frontend coverage | **41.19% lines** | Badge claim of 41% already accurate |
| E2E (JS, Playwright) | **59 passed** | |
| E2E (Python, Playwright) | **54 passed** (+ 6 in `examples/`, not counted in the headline figure, for consistency with how `backend/tests/examples/` is already excluded) | |
| Security | **18 passed, 5 skipped** (skips are rate-limit tests that don't trigger under test-mode limits) | Matches the documented "17-19/23" range exactly, once the suite is run against a freshly-reset database (see finding below) |
| Performance (k6) | Smoke and load tests run live: **0% error rate, all thresholds green** (p95 227ms smoke, 231ms load) | Full stress test not run (multi-minute, deliberately pushes past capacity) |
| **Total** | **359** (183 + 40 + 59 + 54 + 23) | |

### Real finding: E2E suites pollute security-test state
Running the JS and Python E2E suites and then the security suite back-to-back, without a reset in between, produces 2 failures and 3 errors that look like real security bugs (login returning 401 for a seed account) but are actually stale state — E2E tests mutate shared seed-account data (passwords, account deletions) and nothing warns a human running the full suite manually about this. Documented in `docs/guides/RUNNING_TESTS.md` as a troubleshooting step rather than left as a silent trap.

### Backend test quality (2A)
Found all 16 backend test functions with >3 assertions via AST parsing (not a naive grep, which would have missed several due to parametrization). Applied actual judgment rather than mechanically splitting everything — most were checking multiple fields of one freshly-created object, a genuinely single concern. Split the ones that mixed unrelated concerns: three tests bundled "does the functional response look right" with "is the password hash ever exposed," a security invariant that deserves its own always-checked test regardless of what else in the response shape changes.

**Real bug found in the process:** `test_register_sets_default_values` didn't actually assert on any default values — it duplicated the adjacent success test's assertions. Fixed to actually verify the claim in its own name (bio/theme/text_density defaults), which required fetching `/api/auth/me` after registering since the registration endpoint's own response schema doesn't include those fields.

**Not done:** the remaining parametrize-consolidation opportunity (only 4 `@pytest.mark.parametrize` uses exist across 183 tests) and a systematic assertion-message pass across the full suite. Time-boxed in favor of the higher-value items above; a reasonable next pass if this continues.

### Frontend test quality (2B)
`CreatePost.test.jsx` and `Register.test.jsx` used `fireEvent` exclusively despite `@testing-library/user-event` already being a declared dependency — a real Testing Library anti-pattern, not just a style preference. Converted every `fireEvent.change/click` call to `userEvent.type/click`. This wasn't cosmetic: the `fireEvent` version had a real unhandled-promise-rejection error in `Register.test.jsx` (a state update firing after the synchronous `fireEvent` dispatch had already let the test move on) that the `userEvent` version — which properly awaits interactions — resolved. Verified all 40 tests still pass.

### E2E test quality (2C)
- **Semantic locators**: converted 56 `.locator('[data-testid="X"]')` calls and 38 page-level shorthand calls (`page.click`/`page.fill` with the same raw CSS string) to `page.getByTestId('X')` across the full JS suite, and the equivalent 61+55 conversions across the Python suite, using Playwright's real semantic-locator API instead of reimplementing it via CSS attribute selectors. Deliberately left `data-testid-generic` and other custom-attribute selectors untouched — Playwright's `getByTestId` only matches the standard `data-testid` attribute by default, so those remain correct as CSS selectors, not an oversight. Verified with full suite runs after: 59/59 JS, 54/54 Python (+ 6/6 examples), no regressions.
- **Page Object Model consistency and hard-wait removal — attempted, failed safely, reverted.** Two background agents were dispatched to (a) build a matching POM structure for the JS suite (Python already has one, unused by the real tests) and retrofit both suites to use it, and (b) remove all 43 `waitForTimeout`/`wait_for_timeout` hard waits in favor of proper auto-waiting assertions. Both agents were cut off mid-work by a session usage-limit error. The JS suite was left in a broken state (3 failing tests, using a fabricated/misapplied locator combination) and the Python suite had only a small, incomplete change to one page-object file. **Both were reverted to the last known-good commit** rather than leaving broken test code in the repo, and verified back to fully passing before continuing.

  **This is the single largest piece of unfinished Part 2 work.** The recommendation stands as originally scoped: adopt POM consistently (Python's `pages/` classes should actually be used by `test_auth.py`/`test_posts.py`/`test_users.py`, not just the example files; JS needs an equivalent `BasePage`/`FeedPage`/`ProfilePage` structure), and replace all 43 hard waits with condition-specific assertions. Given the demonstrated risk of doing this via an unsupervised long-running agent, it should be done as a smaller, incrementally-verified pass — one spec file at a time, running the real suite after each file, not as one large batch.

### Performance tests (2D)
All three k6 scripts already had real, sensible thresholds and correctly staged ramp profiles (smoke intentionally flat, load/stress properly ramped). Added an explanation of *why* the specific numbers (500ms/1000ms/2000ms/3000ms, 1%/5%/10% error rates) were chosen — grounded in standard web-performance UX reference points, with an explicit note that they're a teaching default, not a number to defend in a real incident review.

### Security tests (2E)
Mapped real coverage against the OWASP Top 10 (2021) explicitly in `tests/security/README.md`. Confirmed gaps, documented rather than papered over: **A06 (Vulnerable/Outdated Components)**, **A08 (Software/Data Integrity Failures)**, and **A09 (Security Logging & Monitoring Failures)** have no coverage in this suite. Dependabot catches A06 at the PR level but nothing verifies it at test time.

### CI/CD (2F)
- Verified the existing action-version pins (`checkout@v7`, `setup-python@v7`, `setup-node@v7`, `upload-artifact@v7`) against GitHub's actual release API — **all genuinely current**, not fabricated or stale as initially suspected given how high the majors looked.
- Added Playwright browser caching (`actions/cache@v6`, keyed on the relevant lockfile) to both workflows that install browsers — every CI run was doing a full fresh download before this.
- Removed `.github/workflows/comprehensive-ci.yml.example` — zero references anywhere in the repo, duplicated coverage the active workflows already provide, and its unpinned tool versions confirmed nobody had touched it in a long time.
- Made both previously-`|| true`'d lint steps (backend ruff, frontend eslint) actually blocking — but only after verifying each one passes clean first (see next item), so this doesn't break CI on unrelated pre-existing issues.
- Added a real `[tool.ruff]` config to `backend/pyproject.toml` (E/F/I rules — pyflakes + import order; deliberately not ruff's stricter opt-in categories like bandit-style security checks, which produced 163 hits on a teaching codebase mostly unrelated to real bugs). Scoped and excluded `tests/examples/` (deliberately-illustrative, including an intentionally-bad file used to teach anti-patterns).
- Added a "Recommended Branch Protection Rules" section to `docs/guides/QUALITY_CHECKS.md` — none existed anywhere in the repo.

### Code quality infrastructure (2G)
- Replaced commented-out isort+flake8 pre-commit hooks with a single enabled `ruff` hook (using the new config above), verified to pass clean before enabling.
- Left `detect-secrets` commented out, but documented why rather than as unexplained dead config: `.secrets.baseline` is stale, and a fresh scan turns up ~1,200 new candidate matches (mostly CI env-var fixtures and seed test passwords, not real secrets) that need human triage before this can be enabled without blocking every future commit.
- Backend type-hint coverage (~22% of functions have explicit return-type annotations) was surveyed but not systematically improved — a large, low-urgency task, not attempted given everything else in scope.

---

## 4. Part 3 — Consolidation (executed, per approved decision log)

Presented the full inventory and decision log to the maintainer before any deletion, per the audit brief's own requirement. Approved actions, executed:

- **`docs/guides/MARKDOWN_VALIDATION.md`** (448 lines, fully orphaned from navigation) → absorbed into `docs/guides/QUALITY_CHECKS.md` as a new section, condensed to ~15 lines (kept: what's checked, how to run locally, config locations; cut: a fake "validation report example" and four redundant checklists).
- **`docs/industry/INDUSTRY_PRACTICES.md`** (32 lines after the fabrication rewrite in §2 — too thin to earn a 4th standalone file in `docs/industry/`) → absorbed into `CASE_STUDIES.md`'s introduction as a "Sourcing" note.
- Every inbound link to both removed files was repointed (`docs/INDEX.md`, `learn/README.md`, `docs/advanced/*`, `docs/concepts/*`, `docs/industry/*`), and `docs/INDEX.md`'s stale "Case Studies" content-highlights bullets (still referencing the fabricated incidents already corrected) were rewritten.

**Kept, with reasoning** (not just "left alone" — actually evaluated):
- `docs/reference/QUICK_REFERENCE_PYTEST.md` / `QUICK_REFERENCE_PLAYWRIGHT.md`: too large (467/657 lines) to be an appendix, each independently linked 4×.
- `docs/concepts/` (4 files): read in full — genuinely distinct altitudes (mindset / design principles / patterns / anti-patterns), not variations on one topic. Trimmed real redundancy between `TEST_DESIGN_PRINCIPLES.md` and `TESTING_ANTIPATTERNS.md` (see §2) rather than merging the files.
- `docs/advanced/` (2 files, not 3 — `ADVANCED_E2E_PATTERNS.md` doesn't exist, correcting an assumption in the original audit brief): different organizing principle (technique catalog vs. architecture-domain catalog), not redundant — though real overlap exists in their contract-testing/chaos-engineering sub-sections and with `docs/guides/CONTRACT_TESTING.md` (a third treatment). **Not trimmed** — flagged as a smaller follow-up, not executed this pass.
- `tests/*/README.md`, `backend/tests/README.md`: substantial, GitHub-navigation-relevant, well-linked.
- `docs/guides/RUNNING_TESTS.md`'s embedded troubleshooting section: verified (not assumed) to be complementary to `TROUBLESHOOTING.md`, not a duplicate — quick recovery commands vs. per-error-message reference. Kept both, added a cross-link.

Ran the repo's own `markdown-link-check` config against all 91 files after every consolidation and content change — zero broken internal links or anchors.

---

## 5. Part 4 — Additions

**Done:**
- A 7-question honest self-assessment ("Before You Start") in `learn/README.md`, with routing guidance based on the pattern of answers.
- `docs/reference/GLOSSARY.md` — plain-language definitions for every recurring term across the curriculum (fixture, mock/stub, flaky test, POM, contract testing, chaos engineering, canary rollout, coverage, CI/CD, etc.), cross-referenced from the docs it's most relevant to, linked from `docs/INDEX.md` and `learn/README.md`.
- Interview-prep sections (3-4 questions each, with what a strong answer touches on, not just the question) added to all 5 stage `reflection.md` files.
- Real-world-mapping prompts added to Stages 1, 2, 3, and 5's `reflection.md` (Stage 4 already had one from before this audit), each pointing at the actual corrected incident in `CASE_STUDIES.md` rather than a generic "companies care about this" statement.
- `CONTRIBUTING.md` was reviewed against the brief's checklist (how to submit an exercise, correct an error, run docs linting locally, what the standards are) — already substantively covers all of it. Only fix needed: a literal unfilled `(provide email here)` placeholder for security-issue reporting, replaced with GitHub's private security-advisory reporting.
- `docs/guides/PLAYWRIGHT_QUICKSTART.md` already existed and was already linked from README.md and docs/INDEX.md — verified content quality (accurate, no fixes needed), not created new.

**Evaluated, decided not to implement:**
- **Mutation testing** (mutmut for Python): attempted a real run against `backend/auth.py` to produce an actual example instead of a hypothetical one. Hit a pytest/mutmut integration incompatibility in this environment (a `BadTestExecutionCommandsException` from mutmut's own pytest-args wrapper) that would need real debugging time to resolve. Given the existing conceptual coverage in `docs/advanced/ADVANCED_TOPICS.md` is already reasonably solid (a worked hypothetical example, correct tool list for Python/JS/Java), and the environment friction encountered, decided not to force a hands-on addition this pass. Cleaned up the experiment (removed `setup.cfg`, uninstalled mutmut) — no residue left in the repo.
- **Visual regression testing** (Playwright's built-in `toHaveScreenshot()`): evaluated as lower-friction than mutation testing (no extra dependency needed), but declined to add given the audit's own emphasis this pass on *reducing* CI flakiness — screenshot tests are notoriously fragile across OS/font-rendering differences, and this repo has no existing baseline-management infrastructure for that. Adding one now, without that infrastructure, risks introducing exactly the kind of flaky-test problem this audit spent significant effort removing elsewhere (see §3, E2E hard-wait findings). A reasonable candidate for a future pass that specifically budgets time for CI baseline setup.

---

## 6. A note on Part 1 vs. Part 2 tension

None encountered that required an explicit tradeoff call. The closest case: splitting the three security-invariant assertions out of larger tests (§3) made those specific tests marginally less "tell a complete story in one read" (Part 1's readability lens) in exchange for a clearer, more isolated failure signal (Part 2's engineering lens) — resolved in favor of the engineering concern, since a security-invariant test failing for an unrelated reason (a display-name assertion breaking) is a worse outcome for a learner than a slightly longer test file.

## 7. A self-correction, documented transparently

Early in this pass, the backend test count was "corrected" from the original 180 down to 166, based on `grep -c "def test_"` across `tests/unit` and `tests/integration`. That grep undercounts: several tests are parametrized (`test_various_password_formats`, `test_create_reaction`, etc.), so one function definition expands into multiple collected test cases at run time — something only running the actual suite reveals. When the real suite was run (§3), the true number was 180 (181 collected, 1 skipped) — the original figure had been correct. Every file the incorrect 166 had been propagated to was found and fixed back to 180, and later to 183 after the legitimate test-splitting work in §3 added 3 net-new tests. The lesson applied going forward: run the real tool before "correcting" a number, don't trust a grep as a substitute for the thing that actually executes.

## 8. What was not touched, and why

- Full prose-voice rewrite of `docs/guides/*` and `docs/reference/*` beyond factual fixes (§2 — size).
- Backend parametrize consolidation and a systematic assertion-message pass (§3 — time-boxed in favor of higher-value splits).
- E2E Page Object Model adoption and `waitForTimeout`/`wait_for_timeout` removal (§3 — attempted, failed safely due to an agent session-limit interruption, reverted; documented as the top recommendation for a follow-up pass).
- `docs/advanced/ADVANCED_TOPICS.md` vs `ADVANCED_TESTING_STRATEGIES.md` vs `docs/guides/CONTRACT_TESTING.md` — a real, smaller three-way content-overlap trim on contract testing and chaos engineering specifically, identified but not executed.
- Mutation testing and visual regression testing hands-on additions (§5 — evaluated, declined for stated reasons, not silently skipped).
- Backend type-hint coverage improvement (§2G — surveyed, not systematically improved).

None of these were skipped silently — each is named here with a reason, per the audit brief's own instruction not to let "not done" be indistinguishable from "not found."

---

## 9. Follow-Up Pass: 2026-09-03

**Scope:** a 12-item follow-up addressing specific gaps named in the audit above (mainly §8's "what was not touched" list, plus items from §2's engineering findings that were surveyed but not executed: Ruff config triage, backend type hints, the ADVANCED_TOPICS/ADVANCED_TESTING_STRATEGIES/CONTRACT_TESTING overlap, mutation and visual regression testing).
**Audience:** the repo maintainer.

This pass produced 66 commits on `develop`, none pushed. Items were worked strictly in order, one at a time, each verified against the real test suite before moving on. All numbers below are from real runs at the end of this pass, not estimates or numbers carried over from earlier in the session.

### What this pass completed

**Items 1-2 (E2E hard waits/POM, monster-file voice pass):** replaced `waitForTimeout`/`wait_for_timeout` hard waits with auto-waiting assertions across the JS and Python E2E suites, then adopted a real Page Object Model in both (previously attempted in the original audit and reverted after a session interruption - this time completed and verified). Rewrote `docs/guides/WINDOWS_SETUP.md` and `docs/guides/TESTING_GUIDE.md` against real scenarios (real `EBADENGINE` output, real error text, real script behavior), fixing factual drift the originals had accumulated.

**Item 3 (frontend coverage):** raised frontend statement coverage from a verified 41.19% baseline to 83.36% (84.08% lines) by writing real tests for every file that had none, following this repo's established `vi.mock()` conventions - not by lowering the bar. Documented the handful of genuinely-hard-to-cover gaps (e.g. `Post.jsx`'s image-orientation logic, which depends on `naturalWidth`/`naturalHeight`, unsupported in jsdom) instead of leaving them silently uncovered.

**Item 4 (Stage 5 capstone redesign):** replaced the capstone's four-independent-tasks structure (each exercising exactly one prior stage) with one bundled ticket - a product requirement, a real failing integration test, a performance threshold, and a security requirement, delivered simultaneously - so a student has to triage across all four stages at once, the way the original audit brief's own model for this described. Rewrote the reflection questions to require synthesis instead of single-stage recall.

**Item 5 (OWASP gap scaffolding):** added `tests/security/test_owasp_gaps.py` - six fully-written, deliberately-skipped placeholder tests for A06 (vulnerable components), A08 (software/data integrity), and A09 (logging/monitoring), each explaining what it would assert, why it's skipped, how to implement it, and what production would actually do differently. Updated `tests/security/README.md`'s OWASP table from "not covered" to "partial, see test_owasp_gaps.py" for all three.

**Item 6 (detect-secrets baseline triage):** a fresh scan found 158 real candidate matches, not the ~1,200 the stale baseline's own comment had estimated. Triaged every one by hand: all 158 were false positives (seed/test account passwords, CI-only environment values, markdown showing example credentials). 148 handled by path exclusion in `.pre-commit-config.yaml` (whole trees that are entirely fixture/demo content); the remaining 10, in `backend/auth.py`'s dev-only SECRET_KEY fallback and `backend/seed.py`'s seed passwords, marked inline with `# pragma: allowlist secret` since those are real application files. The hook is enabled and passes clean.

**Item 7 (parametrize consolidation, assertion messages):** collapsed six clusters of near-duplicate backend test functions into parametrized tests (register/login invalid-input and bad-credentials cases, a display-preference update test, a JWT-expiration test), leaving the collected test count unchanged. Deliberately did *not* consolidate the "operation X requires auth" tests scattered across feature classes (create post, follow, block, etc.) - each has genuinely different fixtures and HTTP methods, and losing the locality of a feature's auth check living next to that feature's other tests wasn't worth the line-count reduction. Added assertion messages where a bare pytest failure wouldn't be self-explanatory (security-invariant checks, loop-based asserts, ambiguous multi-status-code outcomes) - not to every assert, since pytest's own introspection already explains simple comparisons.

**Item 8 (type hints):** this grew well beyond a straightforward annotation pass. Adding return types to the routers surfaced that `models.py`'s legacy `Column()`-style SQLAlchemy declarative models were fundamentally incompatible with clean mypy checking - the SQLAlchemy mypy plugin (tried first) silently failed to synthesize a working `__init__` for the mapped classes on this mypy/SQLAlchemy version pairing. The actual fix was migrating `models.py` to SQLAlchemy 2.0's native `Mapped[]`/`mapped_column()` style with a class-based `DeclarativeBase`, which mypy understands with no plugin at all. That migration caught real things along the way: two file-upload endpoints would crash with an unhandled `TypeError` on a filename-less upload (now a clean 400); a test's docstring claimed the default JWT expiration was 15 minutes when the real default is 1440, and the test only checked "sometime in the future," not the actual duration; five columns (`bio`, `profile_picture`, `theme`, `text_density`, `created_at` on `User`, similarly on `Post`) were nullable by omission despite every insert path populating them via a Python-side default, tightened to `nullable=False`. mypy is clean across the whole `backend/` tree and enabled in pre-commit as a local hook (not the mirror-mypy repo, since this codebase's type-checking correctness depends on real installed package versions).

**Item 9 (contract testing / chaos engineering overlap):** both topics were fully duplicated (identical Pact and chaos-monkey code examples) across `docs/advanced/ADVANCED_TOPICS.md`, `docs/advanced/ADVANCED_TESTING_STRATEGIES.md`, and `docs/guides/CONTRACT_TESTING.md`. Made `CONTRACT_TESTING.md` the sole authority for contract testing and `ADVANCED_TOPICS.md` the authority for chaos engineering within `docs/advanced/`; the non-authoritative locations now carry a one-sentence summary and a link.

**Item 10 (ruff config triage):** the previous pass enabled only E/F/I, avoiding roughly 163 hits without categorizing any of them. Ran `ruff check . --select=ALL` (1,596 hits), categorized every rule, and now has 24 categories enabled with 13 specific codes disabled (never whole families), each with a reason grounded in this codebase's actual hits - not guessed. This surfaced several real bugs, not just style noise: a `try/except/pass` in a test was silently swallowing a genuine `AssertionError` (meaning that test could never actually fail, regardless of what the delete-account endpoint did); two file-upload handlers caught bare `Exception` and mislabeled any internal bug as "upload failed" (narrowed to `OSError`); three `except`/`raise` sites weren't chaining causes; one endpoint had a dead unused `db` parameter. Also ran `ruff check --fix` for a mechanical modernization (112 fixes: `Optional[X]`/`List[X]` to `X | None`/`list[X]`, `datetime.timezone.utc` to `datetime.UTC`, matching the pinned `target-version = "py313"`).

**Item 11 (mutation testing worked example):** the prior audit's attempt failed with a `BadTestExecutionCommandsException` and declined to add hands-on content without a working example. Diagnosed the real cause: `pip install mutmut` installs 3.x by default, which has an entirely different CLI/config interface (`setup.cfg`-based `source_paths`, no `--paths-to-mutate`/`--runner` flags) than the 2.x the original command syntax assumed. Pinning `mutmut<3` resolved it. Ran a real mutation test against `backend/auth.py` scoped to `tests/unit/test_auth.py`: 47 mutants, 35 survived, all inside `get_current_user`/`get_optional_user` (no direct unit coverage, only indirect integration coverage). One surviving mutant inverted `if user is None: raise` to `if user is not None: raise` - a real, security-critical bug class (would reject valid users, accept invalid ones) that the unit suite didn't catch. Added two real unit tests that kill it (and 7 other mutants incidentally); re-ran to confirm: 27 survivors, down from 35. `docs/advanced/ADVANCED_TOPICS.md`'s mutation testing section now shows this real run instead of a hypothetical `calculate_discount()` example.

**Item 12 (visual regression testing + CI infrastructure):** built the infrastructure the prior audit correctly said should come first - `.github/workflows/visual-regression.yml` (weekly schedule + `workflow_dispatch` only, pinned to `ubuntu-22.04`, a `workflow_dispatch` input for regenerating baselines as a reviewable artifact rather than an auto-commit), a separate Playwright config, and three tests (login, feed, post detail) built on the existing page objects. Verifying these locally surfaced a real bug: `backend/seed.py` assigned repost timestamps with `timedelta(hours=random.randint(1, 24))`, so the feed's sort order genuinely differed between identical database resets - not a screenshot-tooling flake, a real nondeterminism bug the visual test happened to be the first thing to notice. Fixed (fixed offsets, matching how regular posts already work); three consecutive runs then produced byte-identical comparisons. `docs/guides/VISUAL_REGRESSION.md` documents the infrastructure decisions and uses this real failure as the "what a real visual regression failure looks like" worked example. **This repo does not ship committed baseline screenshots yet** - Playwright's snapshot naming is platform-specific (macOS-generated baselines would not match the pinned `ubuntu-22.04` CI runner), and this environment has no way to produce a real Linux baseline without either pushing to trigger the actual workflow or a local Linux container, neither available this pass. The doc's "Bootstrapping" section covers what a maintainer needs to do once (trigger `workflow_dispatch` with `update_baselines`, review the artifact, commit it) before the weekly schedule produces a meaningful signal instead of "no baseline found."

### Real final numbers (this pass)

Every number below is from an actual run at the end of this pass, not carried over from mid-pass or estimated.

| Suite | Result |
| --- | --- |
| Backend (`pytest --cov=.`) | 185 passed, 1 skipped, 85.68% statement coverage |
| Frontend (`npm test -- --coverage`) | 144 passed, 2 skipped, 83.36% statement / 84.08% line coverage |
| E2E JavaScript (`npx playwright test --project=chromium`) | 59 passed |
| E2E Python (`pytest e2e-python/`) | 60 passed |
| Security (`pytest security/`) | 18 passed, 9 skipped, 2 failed |
| k6 smoke (`k6 run tests/performance/smoke-test.js`) | 441/441 checks passed, all thresholds passed |
| Markdown links (113 real repo markdown files, excluding vendored `.venv`/`node_modules` content) | 1 broken link found and fixed (a dead Udemy course URL in `MANUAL_QA_TO_AUTOMATION.md`); 0 remaining |

The 2 security-suite failures are both rate-limiting-threshold tests (`test_login_attempts_should_be_rate_limited`, `test_registration_rate_limiting`) that assert against production-level rate limits while the test environment runs in `TESTING=true` mode with intentionally raised limits - a pre-existing, documented tension (see `tests/security/README.md`'s own "Why Some Tests May Fail" section) that predates this pass, not a regression introduced by it.

README.md's badges and every test-count/coverage reference found across the repo (`docs/guides/FAQ.md`, `docs/guides/RUNNING_TESTS.md`, `docs/guides/PORTFOLIO.md`, and a narrative anecdote in `LAB_15_Rate_Limiting_Production_Python.md`) were updated to match the numbers above. `CHANGELOG.md`'s historical entries were deliberately left alone - a changelog is a dated record of past states, not a live status document, and editing old entries to reflect current numbers would misrepresent what was true when they were written.

### Decisions the maintainer should be aware of

- **The visual regression baseline gap (Item 12)** is the one piece of this pass that isn't fully closed - see §9's Item 12 entry and `docs/guides/VISUAL_REGRESSION.md`'s "Bootstrapping" section for exactly what running `workflow_dispatch` with `update_baselines` once will finish.
- **The SQLAlchemy Mapped[] migration (Item 8)** touches every model in `models.py` and is a larger, riskier-looking diff than "add type hints" suggests at a glance. It was necessary (the classic-style models were not cleanly type-checkable at all), is fully backward-compatible at the SQL/runtime level (verified: 185 backend tests passing throughout, no migration needed), and is worth a specific look during review given its size.
- **The ruff config (Item 10)** now enables `S` (bandit-style security checks), which will flag new code the same way it flagged the `try/except/pass` and broad-`except` bugs found this pass - expected and intended, not a false-positive risk, given every current exclusion was individually checked against real hits rather than assumed.
- **`.mutmut-cache` is gitignored** (Item 11) - mutmut is not added to `backend/requirements.txt` as a standing dependency, since this pass treats it as an occasional diagnostic tool a contributor installs when they want to run it, not CI-gated infrastructure. Re-running the worked example in `docs/advanced/ADVANCED_TOPICS.md` requires `pip install "mutmut<3"` first.

---

## 10. Pre-Merge Hardening Pass: 2026-09-09

**Scope:** a 10-checkpoint pre-merge pass, run one checkpoint at a time with maintainer confirmation between each: fix the two failing security tests blocking CI, add CI job timeouts and verify Dependabot, review the SQLAlchemy migration, audit application accessibility, audit DevOps startup/devcontainer/Docker reliability, an instructional-designer pass on curriculum entry criteria, an application security review, a technical-writer pass on the two largest remaining docs, open-source community infrastructure, and this final verification.
**Audience:** the repo maintainer.

This pass produced 26 commits on `develop`, none pushed. All numbers below are from real runs at the end of this pass.

### What this pass completed

**Checkpoint 1 (failing security tests):** the two rate-limit tests weren't miscalibrated against production thresholds, as the checkpoint brief assumed - they already had correct skip-for-TESTING-mode logic, but it checked `os.getenv("TESTING")` on the *pytest process's own shell*, not the server actually being tested. Those are separate processes; exporting `TESTING=true` for one doesn't set it for the other. Replaced the check with a fixture that probes the server directly (`GET /api/dev/users`'s status code). Verified both directions live: against a `TESTING=true` server, both tests now skip regardless of the invoking shell's own env; against a production-mode server, both tests actually run and pass, proving real rate limiting works.

**Checkpoint 2 (CI timeouts, Dependabot):** none of 22 jobs across 11 workflows had a timeout except 3, which were tuned to values too tight for what they actually run. Added `timeout-minutes` to all 22, sized by reading what each job does (lint jobs 10 min, test jobs 15 min, E2E/visual-regression 30 min, the k6 job 20 min after checking its scripts run smoke+load+stress sequentially). `.github/dependabot.yml` already existed and already covered more than the checkpoint's own template (pip for three directories, npm for two, github-actions) - verified, not recreated.

**Checkpoint 3 (SQLAlchemy migration review):** reviewed the full `models.py` diff between `main` and `develop`. Confirmed the `Mapped[]` conversion itself is purely typing-layer (every column's arguments preserved exactly), and that the `backref`→`back_populates` relationship changes are behaviorally identical (verified the primary/secondary join swap matches what `backref` auto-generates). Found one genuinely non-cosmetic part: nine columns tightened from implicit `nullable=True` to explicit `nullable=False` is a real DDL change. Resolved rather than just flagged: confirmed no `*.db` file is ever committed (gitignored) and no raw SQL exists anywhere in `backend/` (every write goes through the ORM's own defaults), so the tightening can't actually be violated by any code path. Recorded that reasoning in the code comment itself.

**Checkpoint 4 (accessibility audit):** ran axe-core directly (`axe.run()`, full default rule set) against all 6 real pages, not just through the existing `accessibility-axe.spec.js` suite. Found 15 moderate-severity violations (missing `<main>` landmark app-wide, missing `<h1>` on Feed/Post Detail/Profile, a resulting heading-order skip) that the existing suite had been missing entirely - not because they aren't real, but because `landmark-one-main`, `region`, `page-has-heading-one`, and `heading-order` are all tagged `best-practice` in axe-core, not any WCAG tag, and the suite's `withTags()` only asked for WCAG tags. Fixed all 15 violations and closed the gap in the suite itself (added `'best-practice'` to its tag list) so this class of regression fails CI going forward instead of passing silently.

**Checkpoint 5 (DevOps reliability):** reproduced a real bug before fixing it: with ports already occupied, `start-dev.sh`/`start-dev.bat` used to warn and continue, but the readiness check that follows only polls a URL, not whether *this run's* process is answering it - so the script printed "Testbook is running!" while the actual freshly-started backend had crashed. Changed both scripts to exit with a clear error before starting anything. Fixed the devcontainer's `Dockerfile.dev`, which ran `npx playwright install chromium` with no `--with-deps` on a base image with zero Chromium system libraries - installed the dependencies at build time (as root, before the image drops to the non-root `vscode` user) instead of adding the flag at runtime, since that user has no `sudo`. With Docker made available partway through this checkpoint, re-verified everything for real rather than trusting the earlier static review: reproduced the devcontainer's build-context path bug empirically via `docker compose config` (it only worked because this clone happens to be in a folder named `testbook`), fixed it, then built the real image and launched a real headless Chromium browser inside it as proof. Also reproduced and fixed a real Docker production-mode bug: `docker-compose.yml` bind-mounts a gitignored `backend/testbook.db`, and Docker's behavior for a missing bind-mount *file* is to silently create an empty *directory* instead - confirmed by deliberately triggering the crash, then fixing `start.sh`/`start.bat` to create the file first (mirroring the pattern those scripts already used for `static/images`).

**Checkpoint 6 (instructional design):** the "Before You Start" self-assessment routed every low-experience student toward Python regardless of which track they'd end up choosing, with no JavaScript-equivalent resource, and the "already experienced" bucket had no real skip-ahead path. Fixed both. Added Entry Criteria sections to Stages 2, 3, and 4 (Stage 5 already had one) - sourced from each stage's own existing "Success Criteria" checklist rather than invented, so a student who actually completed the prior stage passes every criterion. Added a "Bridge" section to Stage 2 for the two concepts (the test client mechanism, access tokens) that Lab 5 uses without ever defining, after confirming via grep that no existing content already covered them.

**Checkpoint 7 (application security review):** documented JWT tradeoffs directly in `auth.py` (algorithm choice, the dev-mode secret fallback, the 24-hour expiration, the absence of revocation) - the 24-hour default had never been explained anywhere a student would see it. Reviewed both file-upload endpoints: the 10MB size limit and path-traversal safety were both already real, verified live against the running server; added a real second layer of type validation (checking actual file bytes against each image format's signature, not just the filename) after finding the existing check was extension-only. Found and fixed a real CORS misconfiguration: `allow_origins=["*"]` combined with `allow_credentials=True` - worse than a plain wildcard, since browsers reject that literal combination so CORS middleware reflects the actual requesting origin instead. Confirmed via full-codebase grep the app never uses cookies (bearer tokens only), so credentials mode was doing nothing useful; disabled it, verified as a genuine no-op via the full suite plus real cross-origin E2E requests. Added the seed-credential exposure warning to README.md and QUICK_START.md, and a new `docs/reference/SECURITY_NOTES.md` consolidating all of it as a teaching document.

**Checkpoint 8 (technical writer pass, WINDOWS_SETUP.md + TESTING_GUIDE.md):** verified nearly every command block and API example in both files against the real files they describe (package.json engine constraints, pyproject.toml's Python target, every backend endpoint's real status code and schema) rather than trusting the existing text - the prior follow-up pass's rewrite held up almost everywhere. Found and fixed the real drift that did exist: this pass's own Checkpoint 5 change to `start-dev.bat` added a new output line that two "Expected output" examples and a troubleshooting entry never got updated to match; two numbered lists of non-sequential tips that should have been bullets; a stale "138+ data-testid attributes" figure (real count: 151). Verified the specific seed-data numbers in TESTING_GUIDE.md by querying a freshly reset database - caught and corrected my own contaminated first count (from leftover session state) before concluding anything.

**Checkpoint 9 (community infrastructure):** issue templates and a PR template already existed from a prior pass, more thorough than this checkpoint's own suggested minimum - verified every doc link and command they reference rather than adding redundant ones. Confirmed via GitHub's public API that Discussions is already enabled and the repo's real scale matches this pass's own framing (5 stars, 1 fork). Zero issues currently carry `good first issue` (in fact zero non-PR issues exist at all - the 13 "open issues" the API counts are Dependabot PRs); listed 5 concrete, bounded candidates sourced from real findings elsewhere in this pass rather than inventing generic ones.

**Checkpoint 10 (this section):** full verification battery re-run for real, current numbers (below). While updating README.md's coverage badge, found the same staleness ran deeper than expected: `docs/guides/QUALITY_CHECKS.md` still described backend linting as "Black only, isort/Flake8 not yet enabled" and frontend coverage as "~41% (no gate)" - both several passes out of date. Fixing it surfaced a real, previously-undocumented inconsistency: `.pre-commit-config.yaml` runs Ruff for backend linting (migrated in the Item 10 follow-up pass), but `.github/workflows/testbook-ci.yml`'s `lint-backend` job and `scripts/quality-check.sh` were never migrated and still run isort and Flake8 directly. Both are real and currently enforced - they just aren't the same tool anymore, which means it's possible for pre-commit to pass locally while CI's separate isort/Flake8 run catches something different. Documented this in `QUALITY_CHECKS.md` rather than picking an answer unilaterally (migrate CI to Ruff too, or keep both deliberately) - see "Decisions the maintainer should be aware of" below. Also found `tests/security/README.md`'s own "Expected Results" section still documented the pre-Checkpoint-1 flaky range ("17-19 passed... 0-1 failed") instead of the now-deterministic result my own fix produces; rewrote it to match, including a stale "LAB_06" label pointing at the real LAB_15 file.

### Real final numbers (this pass)

Every number below is from an actual run at the end of this pass.

| Suite | Result |
| --- | --- |
| Backend (`pytest --cov=.`) | 185 passed, 1 skipped, 84.65% statement coverage |
| Frontend (`npm test -- --coverage`) | 144 passed, 2 skipped, 83.36% statement / 84.08% line coverage |
| E2E JavaScript (`npx playwright test --project=chromium`) | 59 passed |
| E2E Python (`pytest e2e-python/`) | 60 passed |
| Security (`pytest security/`, no `TESTING=true` on the pytest shell - proving Checkpoint 1's fix) | 18 passed, 11 skipped, 0 failed |
| k6 smoke (`k6 run tests/performance/smoke-test.js`) | 441/441 checks passed, all thresholds green |
| Markdown links (114 real repo markdown files, vendored `.venv`/`node_modules`/`htmlcov`/`.pytest_cache` excluded) | 701 links checked, 0 broken |

Backend statement coverage moved from 85.68% to 84.65% - a real, small drop, not an error. This pass added `backend/upload_validation.py` (Checkpoint 7's file-content-signature check) with no dedicated unit tests yet, only the live HTTP verification done at the time; that new file sits at 25% coverage and pulls the aggregate down. Worth a follow-up unit test, not urgent given it's already verified working end-to-end.

README.md's badges and every test-count/coverage reference found across the repo (`docs/guides/FAQ.md`, `docs/guides/RUNNING_TESTS.md`, `docs/guides/PORTFOLIO.md`, `docs/guides/QUALITY_CHECKS.md`, `tests/security/README.md`) were updated to match. `CHANGELOG.md` and the generic before/after example tables in `PORTFOLIO.md`/`learn/COMPLETION.md` were deliberately left alone - the former is a dated historical record, the latter are templates showing a student what *kind* of numbers to report for their own work, not claims about Testbook's own.

### Decisions the maintainer should be aware of

- **CI's isort/Flake8-vs-Ruff split (Checkpoint 10 finding) is now resolved**, per the maintainer's decision to migrate rather than keep both. `.github/workflows/testbook-ci.yml`'s `lint-backend` job, `scripts/quality-check.sh`, and `scripts/verify-release.sh` now all run `ruff check .` instead of installing and running isort/Flake8 separately - the same tool and the same config (`backend/pyproject.toml`'s `[tool.ruff]`) local pre-commit was already using. Removed the now-dead isort/Flake8 config as part of the migration: `backend/.flake8`, `backend/pyproject.toml`'s `[tool.isort]`, and the root `pyproject.toml`'s `[tool.isort]`/`[tool.flake8]` sections (the latter were never actually read by real flake8 invocations in this repo - flake8 needs the Flake8-pyproject plugin, not installed, to read config from a `pyproject.toml` at all). `backend/requirements.txt` and `backend/requirements.lock` updated to drop `flake8`/`isort` and add `ruff==0.16.4`, matching the version already pinned for pre-commit. Verified `ruff check .` and `black --check .` both pass clean, and the full backend suite (185 passed, 1 skipped) is unaffected.
- **A separate, smaller gap surfaced while doing this migration, left unfixed:** `mypy` is used by the local pre-commit hook (`backend/.venv/bin/mypy`) but isn't declared in `backend/requirements.txt` or `requirements.lock` at all - it works today only because it happened to get installed into this environment's venv at some point. A genuinely fresh clone's venv wouldn't have it, and the pre-commit mypy hook would fail with "command not found." Not part of what was asked for this pass; worth a maintainer's attention separately.
- **The visual regression baseline gap (from the prior follow-up pass, Item 12) is still open** - this pass didn't touch it. A maintainer still needs to trigger `workflow_dispatch` with `update_baselines` once, on a real push, to produce the first real Linux baseline; nothing in this environment can do that.
- **The devcontainer fixes in Checkpoint 5 were verified with real Docker** (installed partway through that checkpoint), including actually launching a headless browser inside the built image - stronger evidence than the static code review most of this pass otherwise relied on. Worth a real Codespaces rebuild to confirm end-to-end, since even a verified local Docker build can't rule out every Codespaces-specific difference.
- **Backend coverage's small drop (85.68% → 84.65%) is from a new, verified-but-not-unit-tested file** (`upload_validation.py`), not a regression in tested behavior - flagged above, not hidden in the number alone.
