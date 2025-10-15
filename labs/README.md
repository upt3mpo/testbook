# 🧪 Hands-On Testing Labs

**Interactive, step-by-step labs for learning automation testing**

Self-paced, practical exercises that build testing skills progressively. Perfect for individual learners or staff engineers guiding junior developers and manual QA professionals into automation.

---

## 📚 Lab Series

### Beginner Labs

**Lab 1: Your First Test** ⭐ START HERE
*Write your first automated test and see it run*
→ [Start Lab 1](LAB_01_Your_First_Test.md)

**Lab 2: Testing Real Functions**
*Test actual Testbook functions (password hashing)*
→ [Start Lab 2](LAB_02_Testing_Real_Functions.md)

**Lab 2.5: Understanding Fixtures** ✨
*Master pytest fixtures - bridge the gap between Labs 2 and 3*
→ [Start Lab 2.5](LAB_02.5_Understanding_Fixtures.md)

**Lab 3: Testing API Endpoints**
*Test REST API endpoints with pytest*
→ [Start Lab 3](LAB_03_Testing_API_Endpoints.md)

### Debugging Labs 🐛

**Lab DEBUG-01: Reading Error Messages**
*Learn to read and understand test failures*
→ [Start DEBUG-01](LAB_DEBUG_01_Reading_Errors.md)

**Lab DEBUG-02: Fixing Broken Tests**
*Practice debugging with 10 intentionally broken tests*
→ [Start DEBUG-02](LAB_DEBUG_02_Fixing_Broken_Tests.md)

### Intermediate Labs

**Lab 4: End-to-End Testing - Choose Your Language!**
*Write UI tests with Playwright - Available in BOTH languages!*

🐍 **Python Version:** [LAB_04_E2E_Testing_Python.md](LAB_04_E2E_Testing_Python.md)
☕ **JavaScript Version:** [LAB_04_E2E_Testing_JavaScript.md](LAB_04_E2E_Testing_JavaScript.md)

**Recommendation:** Try BOTH to become a well-rounded tester!

**Lab 5: Test Data Management** ✨
*Master test data factories and builder patterns*
→ [Start Lab 5](LAB_05_Test_Data_Management.md)

**Lab 6: Testing with Rate Limiting & Security** ✨
*Handle rate limiting, test infrastructure, environment config*
→ [Start Lab 6](LAB_06_Testing_With_Rate_Limits.md)

### Advanced Labs 🔴

**🆕 Lab 4B: Advanced E2E Testing (Python)** 🐍
*Master Page Object Model, advanced fixtures, network mocking*
→ [Start Lab 4B](LAB_04B_Advanced_E2E_Python.md)

- Prerequisite: Lab 4 Python
- 120 minutes
- Page objects, pytest parametrization, data builders

**🆕 Lab 6B: Advanced Component Testing (JavaScript)** ☕
*MSW network mocking, async data loading, accessibility testing*
→ [Start Lab 6B](LAB_06B_Advanced_Component_Testing.md)

- Prerequisite: Basic React knowledge
- 120 minutes
- MSW, stateful components, axe accessibility

**🆕 Lab 6C: Frontend Integration & Contract Testing (JavaScript)** ☕
*OpenAPI contract validation, integration testing, schema-based mocking*
→ [Start Lab 6C](LAB_06C_Frontend_Integration_Testing.md)

- Prerequisite: Lab 6B
- 90 minutes
- Contract testing, OpenAPI validation, API client testing

### Future Labs (Roadmap)

> **Note:** Additional advanced labs are planned. Current focus is on dual-stack coverage (Python & JavaScript). Check back for updates or contribute ideas via GitHub Issues!

**Planned Future Labs:**

- **Lab 7:** Integration Testing with Contract Testing
- **Lab 8:** Database Testing Deep Dive
- **Lab 9:** API Testing with Postman Collections
- **Lab 10:** Performance Testing with K6
- **Lab 11:** Security Testing Comprehensive
- **Lab 12:** Full CI/CD Pipeline Setup

**Want to help?** These labs are open for community contribution! See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

---

## 🗺️ Choose Your Track

**Not sure which labs to do? Use this quick reference:**

### 🐍 Python-First Track

| Level | Labs | What You'll Learn |
|-------|------|-------------------|
| **Beginner** | 1, 2, 2.5, 3 | Basics, fixtures, API testing |
| **Intermediate** | 4 (Python), 5 | E2E with Playwright Python, test data |
| **Advanced** | **🆕 4B** | Page objects, advanced fixtures, network mocking |

**Total Time:** ~12-15 hours
**Best For:** Backend developers, Python developers, API testing focus

**🔄 Optional Cross-Stack:** Add [Lab 6B](LAB_06B_Advanced_Component_Testing.md) (JavaScript) to understand frontend component testing.

### ☕ JavaScript-First Track

| Level | Labs | What You'll Learn |
|-------|------|-------------------|
| **Beginner** | 1, 2, 2.5, 3 | Basics, fixtures, API testing (pytest) |
| **Intermediate** | 4 (JavaScript), 5 | E2E with Playwright JavaScript, test data |
| **Advanced** | **🆕 6B, 6C** | MSW, async data, accessibility, contract testing |

**Total Time:** ~14.5-17 hours (includes Lab 6C: 90 min)
**Best For:** Frontend developers, JavaScript developers, UI testing focus

**Progression:** Lab 4 JS → Lab 6B (components) → Lab 6C (integration/contracts) → Section 8

**🔄 Optional Cross-Stack:** Add [Lab 4B](LAB_04B_Advanced_E2E_Python.md) (Python) to see backend testing patterns.

### 🎯 Hybrid Track (Python Backend + JS Frontend) **Most Real-World**

| Level | Labs | What You'll Learn |
|-------|------|-------------------|
| **Beginner** | 1, 2, 2.5, 3 | Basics, fixtures, API testing (pytest) |
| **Intermediate** | 4 (Python), 5 | Backend E2E, test data |
| **Frontend** | 6B, 6C | React components, integration, contracts |
| **Advanced** | **🆕 4B** | Advanced Python E2E patterns |

**Total Time:** ~15.5-18 hours
**Best For:** Full-stack QA engineers, Python backend + React frontend teams

**Progression:** Backend (Python) → Frontend (JavaScript) → Integration (6C connects both!) → Advanced

### 🔄 Full-Stack Track (Everything) **Maximum Mastery**

| Level | Labs | What You'll Learn |
|-------|------|-------------------|
| **Beginner** | 1, 2, 2.5, 3 | Basics, fixtures, API testing |
| **Intermediate** | 4 (Both), 5, 6 | E2E in both languages, test data, rate limits |
| **Advanced** | **🆕 4B + 6B + 6C** | Advanced patterns in both stacks + contract testing |

**Total Time:** ~17.5-21 hours (includes all advanced labs)
**Best For:** Full-stack developers, maximum career flexibility, comprehensive learners

**Complete Progression:** Both Lab 4s → 4B (Python E2E) + 6B (Component) + 6C (Integration/Contracts) → Section 8

**💡 Use the [Testing Comparison Guide](../docs/guides/TESTING_COMPARISON_PYTHON_JS.md) to translate concepts between Python and JavaScript!**

---

## 🎯 How to Use These Labs

### 1. **Follow in Order**

Each lab builds on previous labs. Start with Lab 1!

### 2. **Do All Steps**

Don't skip steps - each teaches something important

### 3. **Type the Code**

Don't copy-paste! Typing helps you learn

### 4. **Experiment**

After completing each lab, try variations

### 5. **Take Notes**

Document what you learned

---

## ⏱️ Time Commitment

**Available Labs (Labs 1-6 + Debug Labs):**

- **Each lab:** 30-90 minutes
- **Total beginner labs (1-3):** ~2-3 hours
- **Debug labs (DEBUG-01, DEBUG-02):** ~1.5 hours
- **Total intermediate labs (4-6):** ~4-6 hours

**Complete all available labs:** ~8-11 hours

**Future labs (7-12):** Estimated 8-12 additional hours when released

---

## 🎓 Learning Outcomes

By completing available labs (1-6 + Debug), you will:

✅ **Write automated tests** in Python AND JavaScript
✅ **Test backends** with pytest (Python)
✅ **Test frontends** with Playwright (Python OR JavaScript)
✅ **Handle test data** with factories and fixtures
✅ **Debug tests** effectively
✅ **Test with security constraints** (rate limiting, auth)
✅ **Build portfolio** of testing projects

**With future labs (7-12), you'll also learn:**

- API testing with Postman/Newman
- Performance testing with K6
- Security testing best practices
- CI/CD pipeline setup

---

## 💡 Lab Format

Each lab includes:

- **Learning objectives** - What you'll learn
- **Step-by-step instructions** - Exactly what to do
- **Code examples** - Copy and try
- **Checkpoints** - Verify you're on track
- **Practice exercises** - Apply what you learned
- **Troubleshooting** - Fix common problems
- **Completion checklist** - Confirm you're ready for next lab

---

## 🚀 Getting Started

### Prerequisites

Before starting Lab 1:

- ✅ Testbook installed and running
- ✅ Basic Python or JavaScript knowledge
- ✅ Terminal/command prompt familiarity
- ✅ Code editor installed (VS Code recommended)

### Quick Setup

```bash
# 1. Clone Testbook
git clone https://github.com/upt3mpo/testbook.git
cd testbook

# 2. Start application
./start-dev.sh  # macOS/Linux
start-dev.bat   # Windows

# 3. Verify running
# Open http://localhost:3000

# 4. Start Lab 1!
# Open labs/LAB_01_Your_First_Test.md
```

---

## 🎯 Success Tips

1. **Go at your own pace** - These are self-paced
2. **Choose your stack wisely** - Pick based on your goals (see [track guide](#🗺️-choose-your-track) above)
3. **Ask questions** - Research when stuck
4. **Experiment** - Break things and fix them
5. **Review code** - Study working examples
6. **Practice** - Do the challenges
7. **Build** - Create your own tests
8. **Document** - Keep notes on what you learn
9. **Compare stacks** - Use the [Testing Comparison Guide](../docs/guides/TESTING_COMPARISON_PYTHON_JS.md) to see both approaches
10. **Go advanced** - Don't skip Labs 4B and 6B - they teach professional patterns!

---

## 🏆 Track Your Progress

Mark your accomplishments:

- [ ] 🥉 **Testing Novice** - Completed Labs 1-3
- [ ] 🥈 **Testing Practitioner** - Completed Labs 1-6 + Debug labs
- [ ] 🥇 **Advanced Specialist** - 🆕 Completed Lab 4B or 6B (professional patterns)
- [ ] 🏆 **Dual-Stack Master** - 🆕 Completed both Lab 4B AND 6B
- [ ] 🌟 **Testing Expert** - Contributed to the project or built advanced tests

**Current Lab Status:**

- ✅ Labs 1-6: Available
- ✅ Debug Labs: Available
- ✅ 🆕 **Advanced Labs (4B, 6B): Available!**
- 🔜 Labs 7-12: Planned (contributions welcome!)

**🎯 Skill Badges You Can Claim:**

After completing your track, you can claim expertise in:

- 🐍 **Python Testing** (Labs 1-6 + 4B)
- ☕ **JavaScript Testing** (Labs 1-6 + 6B)
- 🔄 **Full-Stack Testing** (All labs including 4B + 6B)
- 🧪 **Professional E2E Testing** (Lab 4B)
- ⚛️ **Component Testing** (Lab 6B)
- 🎭 **Playwright Mastery** (Lab 4 + 4B or Section 8)

---

## 📞 Getting Help

**Stuck on a lab?**

1. Re-read the instructions carefully
2. Check the troubleshooting section
3. Review similar examples in existing tests
4. Check [RUNNING_TESTS.md](../docs/guides/RUNNING_TESTS.md)
5. Check [COMMON_MISTAKES.md](../docs/course/COMMON_MISTAKES.md) - Your error is probably there!
6. Look at error messages - they usually tell you what's wrong!

**Common Solutions:**

- Backend not running? Start it: `cd backend && uvicorn main:app --reload`
- Tests failing? Reset database: `./reset-database.sh`
- Import errors? Install dependencies: `pip install -r requirements.txt`
- Need quick reference? See [QUICK_REFERENCE_PYTEST.md](../docs/reference/QUICK_REFERENCE_PYTEST.md)

---

## 🎓 Ready to Start?

**Begin your testing journey now:**

### → [Start Lab 1: Your First Test](LAB_01_Your_First_Test.md) ⭐

---

**Happy Testing! You're about to learn skills that are in high demand! 🚀**
