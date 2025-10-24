# 📚 Documentation Index

**Complete guide to all Testbook documentation**

---

<h2 id="start-here">🎯 Start Here</h2>

**🆕 Self-Guided Learning Path** → [../learn/](../learn/) ⭐ **RECOMMENDED**

**New to Testbook?** → [../README.md#learning-path](../README.md#learning-path)

**Want to run the app?** → [../README.md#quick-start-5-minutes](../README.md#quick-start-5-minutes)

**Want main overview?** → [../README.md](../README.md)

---

## 📁 Documentation Structure

```text
Testbook/
├── README.md                   📱 Project overview + quick start + learning paths
├── learn/                      🎓 Self-guided 5-stage curriculum (RECOMMENDED!)
│   ├── stage_1_unit/           🧪 Unit tests + exercises
│   ├── stage_2_integration/    🧱 Integration tests + exercises
│   ├── stage_3_api_e2e/        🌐 API & E2E testing + exercises
│   ├── stage_4_performance_security/ 🚀 Performance & security + exercises
│   ├── stage_5_capstone/       🎯 Job-ready capstone
│   └── solutions/              📝 Lab solutions
│
├── docs/
│   ├── course/                 👨‍🎓 Course materials
│   ├── guides/                 📖 How-to guides
│   ├── reference/              📚 Reference documentation
│   ├── concepts/               🧠 Deep conceptual understanding
│   ├── industry/               🏢 Real-world context & practices
│   ├── advanced/               🚀 Beyond the basics
│   └── INDEX.md               📑 This file
│
├── backend/tests/              🔬 Backend test suite
└── tests/                      🎭 E2E & other tests
```

---

<h2 id="self-guided-learning-path">🎓 Self-Guided Learning Path (`learn/`) **⭐ RECOMMENDED**</h2>

**The structured 5-stage journey to job-ready testing skills**

| Stage                                                                         | Focus             | Time      | Description                                        |
| ----------------------------------------------------------------------------- | ----------------- | --------- | -------------------------------------------------- |
| **[Stage 1: Unit Tests](../learn/stage_1_unit/)**                             | 🧪 Foundations    | 2-3 hours | Test individual functions, fixtures, AAA pattern   |
| **[Stage 2: Integration Tests](../learn/stage_2_integration/)**               | 🧱 Components     | 3-4 hours | API endpoints, database operations, test factories |
| **[Stage 3: API & E2E](../learn/stage_3_api_e2e/)**                           | 🌐 Full Stack     | 4-5 hours | Playwright, contracts, user workflows              |
| **[Stage 4: Performance & Security](../learn/stage_4_performance_security/)** | 🚀 Non-Functional | 2-3 hours | k6 load testing, OWASP security, rate limiting     |
| **[Stage 5: Capstone](../learn/stage_5_capstone/)**                           | 🎯 Portfolio      | 2-3 hours | Build test suite, documentation, job artifacts     |

**Total: 12-18 hours self-paced**

**What makes this path special:**

- ✅ Links directly to working test code
- ✅ Reflection questions for deep learning
- ✅ Success criteria at each stage
- ✅ Portfolio-ready artifacts
- ✅ Job interview preparation

**[Start Stage 1 →](../learn/stage_1_unit/)**

---

## 👨‍🎓 Course Materials (`docs/course/`)

| Resource                                                                        | Time Estimate | Experience Level          | Description                                   |
| ------------------------------------------------------------------------------- | ------------- | ------------------------- | --------------------------------------------- |
| **[COURSE_AUTOMATION_TESTING_101.md](course/COURSE_AUTOMATION_TESTING_101.md)** | 30-40 hours   | 🟢 Beginner → 🔴 Advanced | Self-paced curriculum with 12 sections        |
| **[Learning Paths](../learn/README.md#choose-your-track)**                      | 15 min        | 🟢 All levels             | Choose path based on your background          |
| **🆕 [SECTION_08_ADVANCED_E2E_PATTERNS.md](advanced/ADVANCED_E2E_PATTERNS.md)** | 8-10 hours    | 🔴 Advanced               | Advanced E2E patterns for Python & JavaScript |
| **🆕 [CI_CD_E2E_TESTING.md](course/CI_CD_E2E_TESTING.md)**                      | 3-4 hours     | 🔴 Advanced               | CI/CD automation for both stacks              |
| **[TROUBLESHOOTING.md](reference/TROUBLESHOOTING.md)**                          | 30 min        | 🟢 Beginner               | 24+ common errors and solutions               |
| **[Learning Roadmap](../learn/README.md#visual-learning-journey)**              | 10 min        | 🟢 All levels             | Visual skill progression guide                |

### Learning Path Details

**COURSE_AUTOMATION_TESTING_101.md:**

- 12 progressive sections (self-paced)
- Theory + hands-on practice
- Practice projects with solutions
- Self-assessment checkpoints
- Covers unit, integration, E2E, API, performance, security, CI/CD

**LEARNING_PATHS.md:**

- Complete beginner path
- Manual QA → Automation path
- Developer → Testing path
- Language-specific tracks (Python/JavaScript)

**TROUBLESHOOTING.md:**

- Setup & environment issues
- pytest common errors
- Playwright troubleshooting

- Quick reference for debugging

**LEARNING_ROADMAP.md:**

- Visual flowcharts
- Milestone tracking
- Skill matrix by experience level

---

<h2 id="how-to-guides">📖 How-To Guides (`docs/guides/`)</h2>

| Guide                                                                            | Time   | Level           | Purpose                                               |
| -------------------------------------------------------------------------------- | ------ | --------------- | ----------------------------------------------------- |
| **🆕 [QUICK_START.md](guides/QUICK_START.md)** ⭐                                | 15 min | 🟢 Beginner     | Complete setup guide for all platforms                |
| **🆕 [DEPLOYMENT_MODES.md](guides/DEPLOYMENT_MODES.md)** ⭐                      | 10 min | 🟢 Beginner     | Development vs Production mode explained              |
| **🆕 [FAQ.md](guides/FAQ.md)** ⭐                                                | 20 min | 🟢 All          | Frequently asked questions and answers                |
| **[RUNNING_TESTS.md](guides/RUNNING_TESTS.md)**                                  | 15 min | 🟢 Beginner     | How to run all test types                             |
| **[TESTING_GUIDE.md](guides/TESTING_GUIDE.md)**                                  | 45 min | 🟡 Intermediate | Comprehensive examples                                |
| **🆕 [TESTING_COMPARISON_PYTHON_JS.md](guides/TESTING_COMPARISON_PYTHON_JS.md)** | 45 min | 🟡 Intermediate | Side-by-side Python vs JavaScript testing             |
| **[FLAKY_TESTS_GUIDE.md](guides/FLAKY_TESTS_GUIDE.md)** ✨                       | 30 min | 🟡 Intermediate | Understanding & fixing flaky tests                    |
| **🆕 [PORTFOLIO.md](guides/PORTFOLIO.md)** ⭐                                    | 30 min | 🟢 All          | Build job-ready portfolio from your work              |
| **[TROUBLESHOOTING.md](reference/TROUBLESHOOTING.md)**                           | 20 min | 🟢 Beginner     | Technical errors with exact fixes                     |
| **🆕 [QUALITY_CHECKS.md](guides/QUALITY_CHECKS.md)** ⭐                          | 20 min | 🟡 Intermediate | Linting, formatting, coverage gates                   |
| **🆕 [ACCESSIBILITY_TESTING.md](guides/ACCESSIBILITY_TESTING.md)** ⭐            | 30 min | 🟡 Intermediate | WCAG 2.1, axe-core, Lighthouse                        |
| **🆕 [CONTRACT_TESTING.md](guides/CONTRACT_TESTING.md)** ⭐                      | 30 min | 🟡 Intermediate | Property-based API contract testing with Schemathesis |
| **[WINDOWS_SETUP.md](guides/WINDOWS_SETUP.md)**                                  | 30 min | 🟢 Beginner     | Windows-specific setup                                |
| **[ROADMAP.md](ROADMAP.md)**                                                     | 10 min | 🟡 Intermediate | Future improvements & maintenance                     |
| **[TASK_RUNNER.md](guides/TASK_RUNNER.md)** ✨                                   | 20 min | 🟢 Beginner     | Simplified commands (Make/just)                       |
| **[LOGGING.md](guides/LOGGING.md)** ✨                                           | 30 min | 🟡 Intermediate | Structured logging & observability                    |
| **[RATE_LIMITING.md](guides/RATE_LIMITING.md)** ✨                               | 25 min | 🟡 Intermediate | Rate limit tuning & config                            |
| **[MANUAL_QA_TO_AUTOMATION.md](guides/MANUAL_QA_TO_AUTOMATION.md)** ✨           | 60 min | 🟢 Beginner     | QA transition roadmap                                 |

### Guide Details

**RUNNING_TESTS.md:**

- Backend tests (pytest) - 166 tests
- E2E tests (Playwright - JS & Python)
- API tests (Postman/Newman)
- Performance tests (K6)

- Security tests
- Platform-specific commands (Windows/macOS/Linux)
- Troubleshooting common issues

**TESTING_GUIDE.md:**

- Complete testing scenarios

- All framework examples
- Real code snippets
- Best practices
- Anti-patterns to avoid

**FLAKY_TESTS_GUIDE.md:** ✨

- What flaky tests are and why they happen
- Real before/after code examples from this project
- Best practices for test stability
- Advanced retry logic techniques
- Fixed 10+ flaky tests in this project

**WINDOWS_SETUP.md:**

- Native Windows setup
- WSL (Windows Subsystem for Linux)
- Docker setup options
- Comparison table
- Windows-specific troubleshooting

**TASK_RUNNER.md:** ✨

- Make and just task runners
- Simplified development commands
- One-command setup and testing
- Cross-platform compatibility
- Self-documenting commands

**LOGGING.md:** ✨

- Structured logging implementation
- JSON and human-readable formats
- Request/response logging patterns
- Production observability

- Debugging with logs

**RATE_LIMITING.md:** ✨

- Environment-based configuration
- Per-endpoint customization
- Testing rate limits
- Production recommendations
- Monitoring and alerting

**MANUAL_QA_TO_AUTOMATION.md:** ✨

- Complete learning path for manual QA
- Side-by-side manual vs automated examples
- Month-by-month roadmap
- Career progression guidance
- Practical exercises from Testbook

### E2E Test Documentation

| Resource                                          | Framework           | Time   | Level           |
| ------------------------------------------------- | ------------------- | ------ | --------------- |
| [Python E2E Guide](../tests/e2e-python/README.md) | Playwright (Python) | 30 min | 🟡 Intermediate |
| [JavaScript E2E Guide](../tests/e2e/README.md)    | Playwright (JS)     | 30 min | 🟡 Intermediate |

Includes environment config, fixtures, test helpers, and patterns.

---

## 📚 Reference Documentation (`docs/reference/`)

### Quick References (⚡ 5-10 min each)

| Reference                                                                    | Type       | Best For                             |
| ---------------------------------------------------------------------------- | ---------- | ------------------------------------ |
| **[QUICK_REFERENCE_PYTEST.md](reference/QUICK_REFERENCE_PYTEST.md)**         | One-page   | pytest commands & patterns           |
| **[QUICK_REFERENCE_PLAYWRIGHT.md](reference/QUICK_REFERENCE_PLAYWRIGHT.md)** | One-page   | Playwright commands & locators       |
| **[TESTING_CHEATSHEET.md](reference/TESTING_CHEATSHEET.md)**                 | Cheatsheet | Common commands, test IDs, endpoints |

### In-Depth References (📖 15-45 min each)

| Reference                                                       | Time   | Level           | Purpose                           |
| --------------------------------------------------------------- | ------ | --------------- | --------------------------------- |
| **[DEBUGGING_GUIDE.md](reference/DEBUGGING_GUIDE.md)**          | 30 min | 🟡 Intermediate | Debug strategies & error patterns |
| **[TESTING_PATTERNS.md](concepts/TESTING_PATTERNS.md)**         | 20 min | 🟡 Intermediate | Patterns for dynamic content      |
| **[TESTING_ANTIPATTERNS.md](concepts/TESTING_ANTIPATTERNS.md)** | 25 min | 🟡 Intermediate | 16 mistakes to avoid              |
| **[TESTING_FEATURES.md](reference/TESTING_FEATURES.md)**        | 15 min | 🟢 Beginner     | All testable Testbook features    |
| **[PROJECT_INFO.md](reference/PROJECT_INFO.md)**                | 20 min | 🟡 Intermediate | Technical architecture details    |

### Content Highlights

**Quick References:**

- Instant command lookups
- Copy-paste snippets
- Pro tips included

**Debugging Guide:**

- Reading error messages
- Using pytest debugger

- Common patterns & solutions
- Advanced techniques

**Testing Patterns:**

- Dynamic content testing
- Selector strategies
- Real-world examples

**Anti-Patterns:**

- 16 documented mistakes
- Why they're bad
- How to fix them

**Project Info:**

- Complete API endpoints
- Database schema
- Tech stack overview

---

<h2 id="deep-conceptual-understanding">🧠 Deep Conceptual Understanding (`docs/concepts/`)</h2>

### Core Testing Philosophy

| Resource                                                            | Time   | Level           | Purpose                       |
| ------------------------------------------------------------------- | ------ | --------------- | ----------------------------- |
| **[TESTING_PHILOSOPHY.md](concepts/TESTING_PHILOSOPHY.md)**         | 30 min | 🟡 Intermediate | The "WHY" behind testing      |
| **[TEST_DESIGN_PRINCIPLES.md](concepts/TEST_DESIGN_PRINCIPLES.md)** | 25 min | 🟡 Intermediate | How to design effective tests |
| **[TESTING_PATTERNS.md](concepts/TESTING_PATTERNS.md)**             | 20 min | 🟡 Intermediate | Patterns for dynamic content  |
| **[TESTING_ANTIPATTERNS.md](concepts/TESTING_ANTIPATTERNS.md)**     | 25 min | 🟡 Intermediate | 16 mistakes to avoid          |

### Content Highlights

**Testing Philosophy:**

- Real-world impact stories
- Business case for testing
- Quality mindset development
- Industry standards

**Test Design Principles:**

- SOLID testing principles
- Test maintainability
- Readability best practices
- Documentation standards

---

## 🏢 Real-World Context & Practices (`docs/industry/`)

### Industry Insights

| Resource                                                    | Time   | Level           | Purpose                            |
| ----------------------------------------------------------- | ------ | --------------- | ---------------------------------- |
| **[CASE_STUDIES.md](industry/CASE_STUDIES.md)**             | 45 min | 🟡 Intermediate | Real testing disasters & successes |
| **[INDUSTRY_PRACTICES.md](industry/INDUSTRY_PRACTICES.md)** | 30 min | 🟡 Intermediate | How top companies test             |
| **[TOOL_COMPARISON.md](industry/TOOL_COMPARISON.md)**       | 25 min | 🟡 Intermediate | When to use what testing tool      |
| **[CAREER_GUIDE.md](industry/CAREER_GUIDE.md)**             | 20 min | 🟢 All levels   | QA career paths & salary data      |

### Content Highlights

**Case Studies:**

- Knight Capital $440M loss
- E-commerce platform outages
- Airline booking system bugs
- Video conferencing failures

**Industry Practices:**

- Google's testing culture
- Netflix's chaos engineering
- Amazon's testing strategies
- Microsoft's quality gates

---

<h2 id="beyond-the-basics">🚀 Beyond the Basics (`docs/advanced/`)</h2>

### Advanced Topics

| Resource                                                                      | Time   | Level       | Purpose                          |
| ----------------------------------------------------------------------------- | ------ | ----------- | -------------------------------- |
| **[ADVANCED_TOPICS.md](advanced/ADVANCED_TOPICS.md)**                         | 40 min | 🔴 Advanced | Mutation testing, property-based |
| **[ADVANCED_E2E_PATTERNS.md](advanced/ADVANCED_E2E_PATTERNS.md)**             | 35 min | 🔴 Advanced | Advanced E2E patterns            |
| **[ADVANCED_TESTING_STRATEGIES.md](advanced/ADVANCED_TESTING_STRATEGIES.md)** | 30 min | 🔴 Advanced | Enterprise testing strategies    |

### Content Highlights

**Advanced Topics:**

- Mutation testing techniques
- Property-based testing
- Test-driven development (TDD)
- Behavior-driven development (BDD)

**Advanced E2E Patterns:**

- Visual regression testing
- Cross-browser strategies
- Mobile testing patterns
- Performance testing integration

---

<h2 id="hands-on-exercises">🧪 Hands-On Exercises (`../learn/`)</h2>

**All lab exercises have been moved into the structured learning stages!**

**New Structure:**

- **Stage 1:** Unit test exercises in `learn/stage_1_unit/exercises/`
- **Stage 2:** Integration test exercises in `learn/stage_2_integration/exercises/`
- **Stage 3:** E2E test exercises in `learn/stage_3_api_e2e/exercises/`
- **Stage 4:** Performance & security exercises in `learn/stage_4_performance_security/exercises/`
- **Solutions:** All lab solutions in `learn/solutions/`

**Total time:** ~12-18 hours (same content, better organization)

**Recommended:** Start with the [Self-Guided Learning Path](../learn/) for the best experience!

**Choose your path:**

- 🐍 **Python-only:** Lab 4B
- ☕ **JavaScript-only:** Lab 6B → Lab 6C
- 🎯 **Hybrid (Python + JS):** Lab 4B + Lab 6B + Lab 6C
- 🌟 **Full-stack:** All three

### Future Labs - Roadmap

> **Status:** Additional advanced labs planned. Current focus: dual-stack coverage complete!

**Planned (Labs 7+):** Database Testing Deep Dive, Performance Testing, Security Testing Comprehensive, Full CI/CD Pipeline Setup

---

## 🔬 Test Suites

### Backend Tests (`../backend/tests/`)

**[backend/tests/README.md](../backend/tests/README.md)**
Backend testing guide

- 166 tests
- pytest usage
- Fixtures
- Coverage

### E2E Tests (`../tests/`)

**[tests/README.md](../tests/README.md)**
E2E testing guide

- Playwright tests
- Cross-browser
- Test helpers

### API Tests (`../tests/api/`)

**[tests/api/README.md](../tests/api/README.md)**
API testing guide

- Postman collection
- Python examples
- Newman CLI

### Performance Tests (`../tests/performance/`)

**[tests/performance/README.md](../tests/performance/README.md)**
Performance testing guide

- K6 scripts
- Load testing
- Analysis

### Security Tests (`../tests/security/`)

**[tests/security/README.md](../tests/security/README.md)**
Security testing guide

- 23+ security tests
- OWASP coverage
- Best practices

---

<h2 id="quick-navigation">🎯 Quick Navigation</h2>

### "I want to..."

**...learn testing** → [../README.md#choose-your-learning-path](../README.md#choose-your-learning-path)

**...run the app** → [../README.md#quick-start-5-minutes](../README.md#quick-start-5-minutes)

**...run tests** → [guides/RUNNING_TESTS.md](guides/RUNNING_TESTS.md)

**...write my first test** → [../learn/stage_1_unit/exercises/](../learn/stage_1_unit/exercises/)

**...understand fixtures** → [../learn/stage_1_unit/exercises/](../learn/stage_1_unit/exercises/)

**...debug failing tests** → [../learn/stage_1_unit/exercises/](../learn/stage_1_unit/exercises/)

**...avoid common mistakes** → [reference/TROUBLESHOOTING.md](reference/TROUBLESHOOTING.md)

**...look up pytest commands** → [reference/QUICK_REFERENCE_PYTEST.md](reference/QUICK_REFERENCE_PYTEST.md)

**...look up Playwright commands** → [reference/QUICK_REFERENCE_PLAYWRIGHT.md](reference/QUICK_REFERENCE_PLAYWRIGHT.md)

**...choose a learning path** → [../learn/README.md#choose-your-track](../learn/README.md#choose-your-track)

**...see the big picture** → [../learn/README.md#visual-learning-journey](../learn/README.md#visual-learning-journey)

**...look something up** → [reference/TESTING_CHEATSHEET.md](reference/TESTING_CHEATSHEET.md)

**...understand the project** → [../README.md](../README.md)

---

<h2 id="platform-specific-guides">🖥️ Platform-Specific Guides</h2>

### Windows Users

**Key differences:**

- Use `.bat` files instead of `.sh`
- Activate venv: `.venv\Scripts\activate`
- Path separator: `\` instead of `/`
- PowerShell or CMD

**Commands:**

```bat
start-dev.bat              :: Start app
reset-database.bat         :: Reset database
.venv\Scripts\activate      :: Activate Python

```

### macOS / Linux Users

**Commands:**

```bash

./start-dev.sh             # Start app (macOS/Linux)
start-dev.bat              # Start app (Windows)
./reset-database.sh        # Reset database (macOS/Linux)
source .venv/bin/activate  # Activate Python (macOS/Linux)
.venv\Scripts\activate     # Activate Python (Windows)
```

---

<h2 id="language-specific-guides">🐍☕ Language-Specific Guides</h2>

### Python Testing

**Resources:**

- Labs 1-3 (Python/pytest)

- Backend tests (166 tests)
- API examples (Python requests)
- Security tests (Python)

**Tools:**

- pytest
- requests
- FastAPI TestClient

### JavaScript Testing

**Resources:**

- Lab 4 (JavaScript/Playwright)
- E2E tests (60+ tests)
- Performance tests (K6)

**Tools:**

- Playwright

- Jest (optional)
- Newman

---

## 📊 By Topic

### Authentication Testing

- Unit tests: `backend/tests/unit/test_auth.py`
- API tests: `backend/tests/integration/test_api_auth.py`
- E2E tests: `tests/e2e/auth.spec.js`, `tests/e2e-python/test_auth.py`
- Guide: [guides/TESTING_GUIDE.md](guides/TESTING_GUIDE.md#authentication)

### API Testing

- Backend: [../backend/tests/](../backend/tests/)
- Examples: [../tests/api/python_api_examples.py](../tests/api/python_api_examples.py)

- Postman: [../tests/api/Testbook.postman_collection.json](../tests/api/Testbook.postman_collection.json)
- Guide: [../tests/api/README.md](../tests/api/README.md)

### E2E Testing

- Tests: [../tests/e2e/](../tests/e2e/)

- Config: [../tests/playwright.config.js](../tests/playwright.config.js)
- Guide: [../tests/README.md](../tests/README.md)

### Performance Testing

- Scripts: [../tests/performance/](../tests/performance/)
- Guide: [../tests/performance/README.md](../tests/performance/README.md)

### Security Testing

- Tests: [../tests/security/](../tests/security/)
- Guide: [../tests/security/README.md](../tests/security/README.md)

---

## 🔄 Recently Organized

**Moved to `docs/course/`:**

- COURSE_AUTOMATION_TESTING_101.md
- LEARNING_PATHS.md
- LEARNING_ROADMAP.md
- TROUBLESHOOTING.md

**Moved to `docs/guides/`:**

- RUNNING_TESTS.md
- TESTING_GUIDE.md

**Moved to `docs/reference/`:**

- TESTING_CHEATSHEET.md
- TESTING_PATTERNS.md
- TESTING_FEATURES.md
- PROJECT_INFO.md

**Removed (redundant summaries):**

- IMPLEMENTATION_COMPLETE.md
- TEST_VERIFICATION_REPORT.md

- TESTING_IMPLEMENTATION_SUMMARY.md
- TRANSFORMATION_SUMMARY.md
- FINAL_SUMMARY_FOR_USER.md
- QUICK_START_TESTING.md

**Removed (classroom-specific materials):**

- EDUCATOR_GUIDE.md
- GRADING_RUBRICS.md

- ASSESSMENT_CHECKPOINTS.md
- CLASSROOM_SETUP_CHECKLIST.md
- COURSE_PRESENTATION_GUIDE.md
- INSTRUCTOR_QUICK_START.md
- STUDENT_FEEDBACK_FORM.md

- STUDENT_PROGRESS_TRACKER.md

**Result:** Clean, organized, individual learner-focused documentation!

---

---

## 🎯 Recommended Reading Order

### Day 1

1. [../README.md#choose-your-learning-path](../README.md#choose-your-learning-path) - Choose path (2 min)
2. [../README.md](../README.md) - Project overview (10 min)
3. [../README.md#quick-start-5-minutes](../README.md#quick-start-5-minutes) - Get running (5 min)

### Day 2-7

4. [../learn/stage_1_unit/exercises/](../learn/stage_1_unit/exercises/) - First test exercises (30 min)
5. [../learn/stage_1_unit/exercises/](../learn/stage_1_unit/exercises/) - Unit testing exercises (45 min)
6. [../learn/stage_2_integration/exercises/](../learn/stage_2_integration/exercises/) - Integration test exercises (60 min)

### Week 2+

7. [course/COURSE_AUTOMATION_TESTING_101.md](course/COURSE_AUTOMATION_TESTING_101.md) - Self-paced curriculum
8. [guides/RUNNING_TESTS.md](guides/RUNNING_TESTS.md) - Reference
9. [reference/TESTING_CHEATSHEET.md](reference/TESTING_CHEATSHEET.md) - Quick lookups

---

## 📞 Need Help?

**Can't find something?**

- Check this index first
- Try [../README.md#choose-your-learning-path](../README.md#choose-your-learning-path)
- See [guides/RUNNING_TESTS.md](guides/RUNNING_TESTS.md) for troubleshooting

**Platform issues?**

- See platform-specific sections above
- Check [guides/RUNNING_TESTS.md](guides/RUNNING_TESTS.md)

**Language preference?**

- See language-specific sections above

---

**🎓 Everything organized - start learning! 🚀**
