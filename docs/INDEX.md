# 📚 Documentation Index

**Complete guide to all Testbook documentation**

---

## 🎯 Start Here

**New to Testbook?** → [../START_HERE.md](../START_HERE.md) ⭐

**Want to run the app?** → [../QUICKSTART.md](../QUICKSTART.md)

**Want main overview?** → [../README.md](../README.md)

---

## 📁 Documentation Structure

```
Testbook/
├── START_HERE.md              ⭐ Choose your learning path
├── README.md                   📱 Project overview
├── QUICKSTART.md               🚀 Get running in 5 minutes
│
├── docs/
│   ├── course/                 👨‍🎓 Course materials
│   ├── guides/                 📖 How-to guides
│   ├── reference/              📚 Reference documentation
│   └── INDEX.md               📑 This file
│
├── labs/                       🧪 Hands-on tutorials
├── backend/tests/              🔬 Backend test suite
└── tests/                      🎭 E2E & other tests
```

---

## 👨‍🎓 Learning Materials (`docs/course/`)

| Resource | Time Estimate | Experience Level | Description |
|----------|---------------|------------------|-------------|
| **[COURSE_AUTOMATION_TESTING_101.md](course/COURSE_AUTOMATION_TESTING_101.md)** | 30-40 hours | 🟢 Beginner → 🔴 Advanced | Self-paced curriculum with 12 sections |
| **[LEARNING_PATHS.md](course/LEARNING_PATHS.md)** | 15 min | 🟢 All levels | Choose path based on your background |
| **🆕 [SECTION_08_ADVANCED_E2E_PATTERNS.md](course/SECTION_08_ADVANCED_E2E_PATTERNS.md)** | 8-10 hours | 🔴 Advanced | Advanced E2E patterns for Python & JavaScript |
| **🆕 [CI_CD_E2E_TESTING.md](course/CI_CD_E2E_TESTING.md)** | 3-4 hours | 🔴 Advanced | CI/CD automation for both stacks |
| **[COMMON_MISTAKES.md](course/COMMON_MISTAKES.md)** | 30 min | 🟢 Beginner | 24+ common errors and solutions |
| **[LEARNING_ROADMAP.md](course/LEARNING_ROADMAP.md)** | 10 min | 🟢 All levels | Visual skill progression guide |
| **🆕 [CURRICULUM_ENHANCEMENTS_PLAN.md](course/CURRICULUM_ENHANCEMENTS_PLAN.md)** | 5 min | 🟡 Educators | Dual-stack curriculum roadmap |

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

**COMMON_MISTAKES.md:**

- Setup & environment issues
- pytest common errors
- Playwright troubleshooting

- Quick reference for debugging

**LEARNING_ROADMAP.md:**

- Visual flowcharts
- Milestone tracking
- Skill matrix by experience level

---

## 📖 How-To Guides (`docs/guides/`)

| Guide | Time | Level | Purpose |
|-------|------|-------|---------|
| **[RUNNING_TESTS.md](guides/RUNNING_TESTS.md)** | 15 min | 🟢 Beginner | How to run all test types |
| **[TESTING_GUIDE.md](guides/TESTING_GUIDE.md)** | 45 min | 🟡 Intermediate | Comprehensive examples |
| **🆕 [TESTING_COMPARISON_PYTHON_JS.md](guides/TESTING_COMPARISON_PYTHON_JS.md)** | 45 min | 🟡 Intermediate | Side-by-side Python vs JavaScript testing |
| **[FLAKY_TESTS_GUIDE.md](guides/FLAKY_TESTS_GUIDE.md)** ✨ | 30 min | 🟡 Intermediate | Understanding & fixing flaky tests |
| **[WINDOWS_SETUP.md](guides/WINDOWS_SETUP.md)** | 30 min | 🟢 Beginner | Windows-specific setup |
| **[TASK_RUNNER.md](guides/TASK_RUNNER.md)** ✨ | 20 min | 🟢 Beginner | Simplified commands (Make/just) |
| **[LOGGING.md](guides/LOGGING.md)** ✨ | 30 min | 🟡 Intermediate | Structured logging & observability |
| **[RATE_LIMITING.md](guides/RATE_LIMITING.md)** ✨ | 25 min | 🟡 Intermediate | Rate limit tuning & config |
| **[MANUAL_QA_TO_AUTOMATION.md](guides/MANUAL_QA_TO_AUTOMATION.md)** ✨ | 60 min | 🟢 Beginner | QA transition roadmap |

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

| Resource | Framework | Time | Level |
|----------|-----------|------|-------|
| [Python E2E Guide](../tests/e2e-python/README.md) | Playwright (Python) | 30 min | 🟡 Intermediate |
| [JavaScript E2E Guide](../tests/e2e/README.md) | Playwright (JS) | 30 min | 🟡 Intermediate |

Includes environment config, fixtures, test helpers, and patterns.

---

## 📚 Reference Documentation (`docs/reference/`)

### Quick References (⚡ 5-10 min each)

| Reference | Type | Best For |
|-----------|------|----------|
| **[QUICK_REFERENCE_PYTEST.md](reference/QUICK_REFERENCE_PYTEST.md)** | One-page | pytest commands & patterns |
| **[QUICK_REFERENCE_PLAYWRIGHT.md](reference/QUICK_REFERENCE_PLAYWRIGHT.md)** | One-page | Playwright commands & locators |
| **[TESTING_CHEATSHEET.md](reference/TESTING_CHEATSHEET.md)** | Cheatsheet | Common commands, test IDs, endpoints |

### In-Depth References (📖 15-45 min each)

| Reference | Time | Level | Purpose |
|-----------|------|-------|---------|
| **[DEBUGGING_GUIDE.md](reference/DEBUGGING_GUIDE.md)** | 30 min | 🟡 Intermediate | Debug strategies & error patterns |
| **[TESTING_PATTERNS.md](reference/TESTING_PATTERNS.md)** | 20 min | 🟡 Intermediate | Patterns for dynamic content |

| **[TESTING_ANTIPATTERNS.md](reference/TESTING_ANTIPATTERNS.md)** | 25 min | 🟡 Intermediate | 16 mistakes to avoid |
| **[TESTING_FEATURES.md](reference/TESTING_FEATURES.md)** | 15 min | 🟢 Beginner | All testable Testbook features |
| **[PROJECT_INFO.md](reference/PROJECT_INFO.md)** | 20 min | 🟡 Intermediate | Technical architecture details |

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

## 🧪 Hands-On Labs (`../labs/`)

**[labs/README.md](../labs/README.md)**
Lab series overview | **Total: 🆕 12-18 hours** (includes advanced labs)

### Beginner Labs (Level: 🟢 Beginner)

| Lab | Time | Skills | Prerequisites |
|-----|------|--------|---------------|
| **[LAB_01](../labs/LAB_01_Your_First_Test.md)** | 30 min | First test, pytest basics | Testbook running |
| **[LAB_02](../labs/LAB_02_Testing_Real_Functions.md)** | 45 min | Unit testing, functions | Lab 1 |
| **[LAB_02.5](../labs/LAB_02.5_Understanding_Fixtures.md)** | 45 min | Fixtures, test setup | Lab 2 |
| **[LAB_03](../labs/LAB_03_Testing_API_Endpoints.md)** | 60 min | API testing, integration | Lab 2.5 |

**Total beginner time:** ~3 hours | **Experience level:** Complete beginner friendly

### Debugging Labs (Level: 🟡 Beginner/Intermediate)

| Lab | Time | Skills | Prerequisites |
|-----|------|--------|---------------|
| **[DEBUG-01](../labs/LAB_DEBUG_01_Reading_Errors.md)** | 30 min | Error messages, debugging | Labs 1-2 |
| **[DEBUG-02](../labs/LAB_DEBUG_02_Fixing_Broken_Tests.md)** | 60 min | Debugging practice, troubleshooting | DEBUG-01 |

**Total debug time:** ~1.5 hours | **Experience level:** Confidence with basic tests

### Intermediate Labs (Level: 🟡 Intermediate)

| Lab | Time | Skills | Prerequisites |
|-----|------|--------|---------------|
| **[LAB_04 (JS)](../labs/LAB_04_E2E_Testing_JavaScript.md)** | 90 min | Playwright, E2E, browser automation | Labs 1-3, JavaScript basics |
| **[LAB_04 (Py)](../labs/LAB_04_E2E_Testing_Python.md)** | 90 min | Playwright, E2E, browser automation | Labs 1-3, Python basics |
| **[LAB_05](../labs/LAB_05_Test_Data_Management.md)** | 45 min | Factories, test data, builder pattern | Labs 1-3 |
| **[LAB_06](../labs/LAB_06_Testing_With_Rate_Limits.md)** | 90 min | Rate limiting, security, env config | Labs 1-5 |

**Total intermediate time:** ~4-6 hours | **Experience level:** Comfortable with Python/JS testing

### Advanced Labs (Level: 🔴 Advanced) 🆕 **NOW AVAILABLE!**

| Lab | Time | Skills | Prerequisites |
|-----|------|--------|---------------|
| **🆕 [LAB_4B (Python)](../labs/LAB_04B_Advanced_E2E_Python.md)** | 120 min | Page Object Model, advanced fixtures, network mocking, API+UI validation | Lab 4 Python |
| **🆕 [LAB_6B (JavaScript)](../labs/LAB_06B_Advanced_Component_Testing.md)** | 120 min | MSW, async data, stateful components, accessibility | Basic React knowledge |
| **🆕 [LAB_6C (JavaScript)](../labs/LAB_06C_Frontend_Integration_Testing.md)** | 90 min | OpenAPI contracts, integration tests, schema validation | Lab 6B |

**Total advanced time:** ~5.5 hours | **Experience level:** Professional patterns

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

## 🎯 Quick Navigation

### "I want to..."

**...learn testing** → [../START_HERE.md](../START_HERE.md)
**...run the app** → [../QUICKSTART.md](../QUICKSTART.md)
**...run tests** → [guides/RUNNING_TESTS.md](guides/RUNNING_TESTS.md)
**...write my first test** → [../labs/LAB_01_Your_First_Test.md](../labs/LAB_01_Your_First_Test.md)
**...understand fixtures** → [../labs/LAB_02.5_Understanding_Fixtures.md](../labs/LAB_02.5_Understanding_Fixtures.md)

**...debug failing tests** → [../labs/LAB_DEBUG_01_Reading_Errors.md](../labs/LAB_DEBUG_01_Reading_Errors.md)
**...avoid common mistakes** → [course/COMMON_MISTAKES.md](course/COMMON_MISTAKES.md)
**...look up pytest commands** → [reference/QUICK_REFERENCE_PYTEST.md](reference/QUICK_REFERENCE_PYTEST.md)
**...look up Playwright commands** → [reference/QUICK_REFERENCE_PLAYWRIGHT.md](reference/QUICK_REFERENCE_PLAYWRIGHT.md)
**...choose a learning path** → [course/LEARNING_PATHS.md](course/LEARNING_PATHS.md)
**...see the big picture** → [course/LEARNING_ROADMAP.md](course/LEARNING_ROADMAP.md)
**...look something up** → [reference/TESTING_CHEATSHEET.md](reference/TESTING_CHEATSHEET.md)
**...understand the project** → [../README.md](../README.md)

---

## 🖥️ Platform-Specific Guides

### Windows Users

**Key differences:**

- Use `.bat` files instead of `.sh`
- Activate venv: `venv\Scripts\activate`
- Path separator: `\` instead of `/`
- PowerShell or CMD

**Commands:**

```cmd
start-dev.bat              :: Start app
reset-database.bat         :: Reset database
venv\Scripts\activate      :: Activate Python

```

### macOS / Linux Users

**Commands:**

```bash

./start-dev.sh             # Start app
./reset-database.sh        # Reset database
source venv/bin/activate   # Activate Python
```

---

## 🐍☕ Language-Specific Guides

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

- Unit tests: `backend/tests/test_unit_auth.py`
- API tests: `backend/tests/test_api_auth.py`
- E2E tests: `tests/e2e/auth.spec.js`
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
- COMMON_MISTAKES.md

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

## 🧭 Release Governance & Quality

- **[TESTBOOK_RELEASE_AUDIT.md](TESTBOOK_RELEASE_AUDIT.md)** – Current release readiness rubric, findings, and recommendations for maintainers.

---

## 🎯 Recommended Reading Order

### Day 1

1. [../START_HERE.md](../START_HERE.md) - Choose path (2 min)
2. [../README.md](../README.md) - Project overview (10 min)
3. [../QUICKSTART.md](../QUICKSTART.md) - Get running (5 min)

### Day 2-7

4. [../labs/LAB_01_Your_First_Test.md](../labs/LAB_01_Your_First_Test.md) (30 min)
5. [../labs/LAB_02_Testing_Real_Functions.md](../labs/LAB_02_Testing_Real_Functions.md) (45 min)
6. [../labs/LAB_03_Testing_API_Endpoints.md](../labs/LAB_03_Testing_API_Endpoints.md) (60 min)

### Week 2+

7. [course/COURSE_AUTOMATION_TESTING_101.md](course/COURSE_AUTOMATION_TESTING_101.md) - Self-paced curriculum
8. [guides/RUNNING_TESTS.md](guides/RUNNING_TESTS.md) - Reference
9. [reference/TESTING_CHEATSHEET.md](reference/TESTING_CHEATSHEET.md) - Quick lookups

---

## 📞 Need Help?

**Can't find something?**

- Check this index first
- Try [../START_HERE.md](../START_HERE.md)
- See [guides/RUNNING_TESTS.md](guides/RUNNING_TESTS.md) for troubleshooting

**Platform issues?**

- See platform-specific sections above
- Check [guides/RUNNING_TESTS.md](guides/RUNNING_TESTS.md)

**Language preference?**

- See language-specific sections above

---

**🎓 Everything organized - start learning! 🚀**
