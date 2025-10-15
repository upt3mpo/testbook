# 📅 Version History

Track major updates and improvements to the Testbook Testing Platform.

---

## [1.1.0] - 2025-10-14

### 🎓 "Full Journey Release" - Self-Guided Learning Path

**Major update transforming Testbook into a complete educational journey with structured learning paths, job readiness tools, and comprehensive quality gates.**

**Key Additions:**

- ✅ **5-Stage Self-Guided Learning Path** (12-18 hours curriculum)
  - Stage 1: Unit Tests → Stage 5: Job-Ready Capstone
  - Multi-track support: Python, JavaScript, Hybrid
  - Reflection prompts, success criteria, portfolio integration

- ✅ **Job Readiness Tools**
  - Complete CI/CD pipeline (8 automated jobs)
  - Portfolio guide with resume templates
  - Interview preparation materials
  - 6 status badges on README

- ✅ **Quality & Accessibility**
  - Linting enforced (Black, Flake8, ESLint, Prettier)
  - 80% coverage gate in CI
  - WCAG 2.1 AA accessibility tests
  - Lighthouse performance baselines

- ✅ **Educational Enhancements**
  - 9 test files enhanced with AAA comments
  - "Why This Matters" sections added
  - Career/interview talking points

- ✅ **Visual Assets**
  - 5 screenshots added to README
  - Application dashboard, test runs, coverage reports
  - E2E automation GIF

**Bug Fixes:**

- Fixed pytest-asyncio deprecation warnings
- Implemented python-dotenv for .env file support
- Fixed E2E test environment configuration (TESTING=true)
- Corrected Python Playwright documentation (--headed → HEADLESS=false)
- Added cross-platform support (Windows PowerShell/CMD syntax) to 15+ docs
- Fixed React Router v7 deprecation warnings
- Suppressed test console warnings for cleaner output

**Test Results:**

- 210+ tests passing (180 backend, 30+ frontend)
- 86% backend coverage, 95% frontend coverage
- 0 warnings, 0 linting errors

See [RELEASE_NOTES_v1.1.md](../RELEASE_NOTES_v1.1.md) and [CHANGELOG.md](../CHANGELOG.md) for complete details.

---

## [1.0.0] - 2025-10-12

### 🎉 Initial Release - Complete Dual-Stack Automation Testing Curriculum

**First public release of Testbook** - A comprehensive, self-paced automation testing learning platform.

**What's Included:**

- ✅ 10+ hands-on labs (40-50 hours total content)
- ✅ 8 comprehensive curriculum sections
- ✅ 4 validated learning paths (Python, JavaScript, Hybrid, Full-Stack)
- ✅ 210 passing tests (180 backend, 30 frontend)
- ✅ 85.94% backend code coverage
- ✅ Professional testing patterns and best practices
- ✅ Production-ready CI/CD examples
- ✅ Cross-platform support (Windows, macOS, Linux)

**Target Audience:**

- Manual QA testers transitioning to automation
- Junior developers learning testing
- Self-learners building QA automation skills
- Bootcamp students and career changers

**Key Features:**

- Real FastAPI + React application to test
- Dual-stack support (Python & JavaScript)
- Explicit Hybrid learning path (most common real-world scenario)
- Working examples and executable code
- Self-paced learning with no prerequisites

**Documentation:**

- 20+ guides and reference materials
- Clear learning paths for different backgrounds
- Common mistakes catalog
- Debugging guides
- Testing patterns and anti-patterns

See [CHANGELOG.md](../CHANGELOG.md) for complete feature list.

---

## 🔮 Future Releases

### Planned Enhancements (Post-1.0)

**Content:**

- Video walkthroughs for complex topics
- Interactive coding exercises
- Additional advanced labs
- More real-world scenarios

**Platform:**

- Enhanced CI/CD examples
- Additional testing frameworks
- Mobile testing module
- Visual regression testing

**Community:**

- User-contributed labs
- Example projects
- Best practices library

---

## 📊 Version Numbering

**Testbook uses Semantic Versioning (MAJOR.MINOR.PATCH):**

- **MAJOR (2.0.0):** Breaking changes to course structure or significant architecture changes
- **MINOR (1.1.0):** New labs, features, or substantial content additions
- **PATCH (1.0.1):** Bug fixes, typos, documentation improvements

**Current Version:** 1.1.0 (Full Journey Release)

---

## 📝 How to Stay Updated

**Track Changes:**

1. Watch this file for version updates
2. Check [CHANGELOG.md](../CHANGELOG.md) for detailed changes
3. Follow GitHub releases (when available)

**Contribute:**

- See [CONTRIBUTING.md](../CONTRIBUTING.md)
- Submit issues and feedback
- Contribute labs and examples

---

**🎓 Thank you for using Testbook! Let's make automation testing accessible to everyone! 🚀**

---

*Last Updated: October 14, 2025*
