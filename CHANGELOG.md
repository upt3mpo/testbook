# 📋 Changelog

All notable changes to the Testbook Testing Platform will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2025-10-12

### 🎉 Initial Release - Complete Dual-Stack Automation Testing Curriculum

**Testbook 1.0.0** is a comprehensive, self-paced automation testing learning platform offering complete Python, JavaScript, and Hybrid learning paths for aspiring QA automation engineers and developers.

---

## 🎓 What's Included

### Core Curriculum

**10+ Hands-On Labs (40-50 hours total):**
- Lab 1: Your First Test (Python, 30 min)
- Lab 2: Testing Real Functions (Python, 45 min)
- Lab 2.5: Understanding Fixtures (Python, 45 min)
- Lab 3: Testing API Endpoints (Python, 60 min)
- Lab 4: E2E Testing - Python & JavaScript versions (90 min each)
- Lab 4B: Advanced E2E Testing (Python) - Page objects, fixtures, mocking (120 min)
- Lab 5: Test Data Management (Python, 90 min)
- Lab 6: Testing with Rate Limits (Python, 60 min)
- Lab 6B: Advanced Component Testing (JavaScript) - MSW, async, accessibility (120 min)
- Lab 6C: Frontend Integration & Contract Testing (JavaScript) - OpenAPI validation (90 min)
- Debug Labs 1-2: Error interpretation and debugging practice

**8 Comprehensive Sections:**
- Section 1-5: Backend testing fundamentals (pytest, FastAPI TestClient, database)
- Section 6: Frontend component testing (Vitest, React Testing Library, axe-core)
- Section 7: E2E testing basics (Playwright - Python & JavaScript)
- Section 8: Advanced E2E Patterns (dual-stack comprehensive guide)
- Section 9: API testing (Postman, Newman, Python requests)
- Section 10: Performance testing (K6)
- Section 11: Security testing (OWASP)
- Section 12: CI/CD & Automation (GitHub Actions for both stacks)

**3 Advanced Guides:**
- Section 8: Advanced E2E Patterns (8-10 hours, dual-stack)
- Testing Comparison: Python vs JavaScript (45 min, side-by-side)
- CI/CD for E2E Testing (3-4 hours, production workflows)

### Learning Paths

**4 Validated Learning Personas:**
- **Path A-B:** Manual QA & Developers (50-60 hours, 25-35 hours)
- **Path C:** Complete Beginners (80-100 hours)
- **Path D:** Experienced SDETs (10-15 hours)
- **Path H:** Hybrid Track - Python backend + JavaScript frontend (30-40 hours) ⭐ **Most Common**

**3 Quick-Decision Scenarios:**
- Python-Only: Backend/API testing focus
- Hybrid (Recommended!): Python backend + React frontend
- Full-Stack: Complete mastery in both languages

### Technical Implementation

**Backend (Python/FastAPI):**
- 180 passing tests (pytest)
- 85.94% code coverage
- FastAPI application with authentication
- PostgreSQL database
- SQLAlchemy ORM
- JWT authentication
- Test factories and fixtures

**Frontend (React/Vite):**
- 30 passing tests (Vitest)
- Component tests with React Testing Library
- Contract tests with OpenAPI validation
- Accessibility tests with axe-core
- MSW for API mocking
- Modern React patterns

**Testing Infrastructure:**
- Playwright for E2E (Python & JavaScript)
- K6 for performance testing
- Postman/Newman for API testing
- pytest for backend testing
- Vitest for frontend testing
- Comprehensive CI/CD examples

### Documentation

**Entry Points:**
- START_HERE.md - Quick start guide
- QUICKSTART.md - Setup instructions
- README.md - Project overview
- WHICH_START_SCRIPT.md - Development vs production modes

**Guides (20+ files):**
- Running tests, debugging, logging
- Testing patterns and anti-patterns
- Common mistakes catalog
- Manual QA to automation transition
- Flaky tests guide
- Rate limiting guide
- Testing comparison (Python ↔ JavaScript)

**Reference Materials:**
- pytest quick reference
- Playwright quick reference
- Testing cheatsheet
- Debugging guide
- Project info

**Meta Documentation:**
- Learning paths (differentiated by background)
- Learning roadmap (visual progression)
- Course: Automation Testing 101 (structured curriculum)
- Persona walkthroughs (4 validated paths)
- Validation audit (quality assurance)

---

## 📊 Release Statistics

**Content:**
- 10+ detailed labs
- 8 comprehensive sections
- 3 advanced guides
- 20+ documentation guides
- 4 validated learning paths
- ~50 hours total curriculum

**Tests:**
- 210 passing tests (100% pass rate)
- 180 backend tests (pytest)
- 30 frontend tests (Vitest)
- 85.94% backend coverage

**Code:**
- Python backend (FastAPI, SQLAlchemy)
- React frontend (Vite, React Router)
- 20+ example files (page objects, mocks, helpers)
- Test factories and fixtures
- CI/CD workflows

---

## 🚀 Key Features

### Dual-Stack Support
- Complete Python track (backend, API, E2E)
- Complete JavaScript track (frontend, component, E2E)
- Explicit Hybrid path (Python + JavaScript)
- Cross-stack comparison guide

### Professional Patterns
- Page Object Model (both stacks)
- Advanced fixtures and factories
- Network mocking (MSW, Playwright)
- Contract testing (OpenAPI validation)
- Accessibility testing (WCAG compliance)
- CI/CD automation (GitHub Actions)

### Self-Paced Learning
- Choose your path (4 personas)
- Choose your stack (Python/JavaScript/Both)
- Choose your pace (15-100 hours depending on background)
- Real application to test
- Executable examples

---

## 📁 Repository Structure

**Application:**
- `backend/` - FastAPI application with 180 tests
- `frontend/` - React application with 30 tests
- `static/` - Shared static assets (21 real images included)

**Tests:**
- `backend/tests/` - 180 pytest tests (unit, integration, API, database)
- `frontend/src/test/` - Contract and component tests
- `tests/e2e/` - JavaScript E2E tests (Playwright)
- `tests/e2e-python/` - Python E2E tests with page object examples
- `tests/security/` - Security test suite
- `tests/performance/` - K6 performance tests
- `tests/api/` - API test examples

**Documentation:**
- `docs/course/` - Complete curriculum and guides
- `docs/guides/` - Practical how-to guides
- `docs/reference/` - Quick reference materials
- `labs/` - 10+ hands-on lab exercises

**Scripts:**
- `start-dev.sh/bat` - Development mode (port 3000, recommended)
- `start.sh/bat` - Production mode (Docker)
- `reset-database.sh/bat` - Database reset utility
- `run-all-tests.sh` - Complete test suite runner
- `setup_images.py` - Image generator (auto-runs if images missing)

**Configuration:**
- `docker-compose.yml` - Production deployment
- `Dockerfile` - Container definition
- `pytest.ini`, `vitest.config.js` - Test configuration
- `justfile`, `Makefile` - Task automation

---

## 🎯 Target Audience

**Perfect For:**
- Manual QA testers transitioning to automation
- Junior developers learning testing
- Bootcamp students building QA skills
- Self-learners exploring automation
- Staff engineers mentoring juniors

**Prerequisites:**
- Basic programming knowledge (Python or JavaScript)
- Command line familiarity (helpful)
- Willingness to learn

**No prior testing experience required!**

---

## 💡 Getting Started

**Quick Start:**
```bash
./start-dev.sh              # Start application
cd backend && pytest -v     # Run backend tests
cd frontend && npm test     # Run frontend tests
```

**Learn:**
- Read: [START_HERE.md](START_HERE.md)
- Follow: [labs/LAB_01_Your_First_Test.md](labs/LAB_01_Your_First_Test.md)
- Explore: [docs/course/COURSE_AUTOMATION_TESTING_101.md](docs/course/COURSE_AUTOMATION_TESTING_101.md)

---

## 🔮 Future Enhancements

Potential additions for future releases:

- Video walkthroughs for complex topics
- Interactive coding exercises
- Mobile testing module
- Visual regression testing examples
- More real-world scenarios
- Community-contributed labs

---

## 🙏 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- How to report bugs
- How to suggest enhancements
- How to contribute labs
- How to improve documentation

---

## ❓ Support

**Resources:**
- [FAQ.md](FAQ.md) - Common questions and issues
- [docs/course/COMMON_MISTAKES.md](docs/course/COMMON_MISTAKES.md) - Error catalog
- [docs/reference/DEBUGGING_GUIDE.md](docs/reference/DEBUGGING_GUIDE.md) - Troubleshooting

---

**🎓 Testbook 1.0.0 - Making automation testing education accessible to everyone! 🚀**

---

*For detailed version history and development journey, see [docs/VERSION_HISTORY.md](docs/VERSION_HISTORY.md)*
