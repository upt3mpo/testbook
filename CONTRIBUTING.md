# 🤝 Contributing to Testbook

Thank you for your interest in improving the Testbook Testing Platform! This document provides guidelines for contributing.

---

## 🎯 Ways to Contribute

### For Educators & Students

- **Report Issues** - Found a bug or unclear documentation? Let us know!
- **Suggest Improvements** - Have ideas for better labs or examples?
- **Share Feedback** - How can we make learning easier?

### For Developers

- **Fix Bugs** - Help improve stability
- **Add Tests** - Increase coverage
- **Improve Documentation** - Make guides clearer
- **Create Labs** - Design new learning exercises

---

## 📋 Before You Start

1. **Search existing issues** - Someone might already be working on it
2. **Read the docs** - Familiarize yourself with the project structure
3. **Run existing tests** - Make sure everything works on your machine

---

## 🔧 Development Setup

### Prerequisites

- Python 3.13+
- Node.js 20+
- Git

### Setup Steps

```bash
# 1. Fork and clone
git clone https://github.com/YOUR_USERNAME/testbook.git
cd testbook

# 2. Set up backend
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Set up frontend
cd ../frontend
npm install

# 4. Run tests to verify
cd ../backend
pytest -v

# 5. Start dev environment
cd ..
./start-dev.sh  # Or start-dev.bat on Windows
```

---

## 🌿 Branch Strategy

### Branch Naming

- `feature/` - New features or enhancements
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `lab/` - New lab content
- `test/` - Test improvements

**Examples:**

```text
feature/add-mutation-testing
fix/flaky-e2e-tests
docs/update-setup-guide
lab/add-contract-testing
test/increase-security-coverage
```

### Workflow

1. **Create a branch** from `main`:

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** with atomic commits

3. **Test your changes**:

   ```bash
   # Backend tests (with coverage for quality assurance)
   cd backend
   pytest -v --cov=. --cov-report=html --cov-report=term-missing

   # E2E tests
   cd ../tests
   npx playwright test
   ```

4. **Push and create PR**:

   ```bash
   git push origin feature/your-feature-name
   ```

---

## ✅ Testing Requirements

### All Contributions Must

1. **Pass existing tests** - Don't break what works
2. **Add new tests** - For new features
3. **Maintain coverage** - Keep coverage at 80%+
4. **Follow patterns** - Match existing code style

### Running Tests

```bash
# Backend tests (must pass)
cd backend
pytest -v

# Coverage check (must be 80%+) - explicit flags required
pytest --cov=. --cov-report=term-missing

# E2E tests (must pass)
cd ../tests
npx playwright test

# Security tests
pytest ../tests/security/ -v
```

---

## 📝 Code Style

### Python (Backend & Tests)

**Follow PEP 8** with these tools:

```bash
# Format code (we use black)
black backend/

# Sort imports
isort backend/

# Lint
flake8 backend/
```

**Standards:**

- Use type hints when helpful
- Write docstrings for all functions/classes
- Keep functions focused (one responsibility)
- Name tests descriptively: `test_user_can_login_with_valid_credentials`

**Example:**

```python
def test_user_creation_sets_default_values(db_session):
    """Test that user creation sets appropriate defaults."""
    user = User(email="test@test.com", username="test")
    db_session.add(user)
    db_session.commit()

    assert user.id is not None
    assert user.created_at is not None
```

### JavaScript (E2E Tests)

**Follow Airbnb style** with these tools:

```bash
# Format
npx prettier --write "tests/**/*.js"

# Lint
npx eslint tests/
```

**Standards:**

- Use `async/await` consistently
- Always use `data-testid` selectors
- Group tests with `describe()`
- Use descriptive test names

**Example:**

```javascript
test("user can login with valid credentials", async ({ page }) => {
  await page.goto("http://localhost:3000");
  await page.fill('[data-testid="login-email"]', "test@test.com");
  await page.fill('[data-testid="login-password"]', "password");
  await page.click('[data-testid="login-button"]');

  await expect(page.locator('[data-testid="navbar"]')).toBeVisible();
});
```

---

## 📚 Documentation Standards

### All Documentation Should

1. **Be clear and concise** - No jargon without explanation
2. **Include examples** - Show, don't just tell
3. **Be cross-platform** - Include Windows, macOS, Linux
4. **Have working links** - Verify all links work
5. **Follow markdown standards** - Enforced by markdownlint

### Markdown Validation

**Before committing documentation changes, run:**

```bash
# macOS/Linux
./scripts/check-markdown.sh

# Windows
scripts\check-markdown.bat
```

This validates:

- ✅ Markdown linting (formatting, style)
- ✅ Link checking (broken links, anchors)

**Auto-fix common issues:**

```bash
markdownlint --fix '**/*.md' --ignore node_modules --ignore venv
```

**CI/CD:** Markdown validation runs automatically on all pull requests

### Documentation Structure

```text
docs/
├── course/          # Course materials
│   ├── *.md         # Course content
│   └── README.md    # Course overview
├── guides/          # How-to guides
│   └── *.md         # Step-by-step guides
└── reference/       # Reference materials
    └── *.md         # Quick lookups

learn/
├── stage_*/exercises/LAB_*.md  # Lab files
└── solutions/       # Sample solutions
```

### Writing Labs

**Template:**

```markdown
# 🧪 Lab X: Title

**Estimated Time:** X minutes
**Difficulty:** Beginner/Intermediate/Advanced
**Prerequisites:** Lab Y completed

## 🎯 What You'll Learn

[Clear learning objectives]

## 📋 Step-by-Step Instructions

[Numbered steps with code examples]

## ✅ Completion Checklist

[Checkboxes for verification]
```

---

## 🔍 Pull Request Process

### PR Template

When creating a PR, include:

```markdown
## Description

[What does this PR do?]

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Lab content
- [ ] Test improvement

## Testing Done

- [ ] Backend tests pass
- [ ] E2E tests pass
- [ ] Coverage maintained/improved
- [ ] Manually tested

## Documentation Updated

- [ ] README updated (if needed)
- [ ] Lab content updated (if needed)
- [ ] Docstrings added/updated
- [ ] Markdown validation passed (if docs changed)

## Checklist

- [ ] Code follows style guidelines
- [ ] Self-reviewed code
- [ ] Added tests for new features
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Markdown linting passed (for doc changes)
```

### Review Process

1. **Automated checks run** - Tests, linting, coverage
2. **Maintainer reviews** - Code quality, design, tests
3. **Feedback addressed** - Make requested changes
4. **Approval & merge** - Once approved, we merge!

### Review Criteria

✅ **Approved if:**

- All tests pass
- Code quality is good
- Documentation is clear
- Follows contribution guidelines

❌ **Changes requested if:**

- Tests failing
- Coverage drops
- Unclear documentation
- Doesn't follow guidelines

---

## 🎓 Contributing Labs

### Lab Contribution Guidelines

1. **Clear learning objective** - What will students learn?
2. **Progressive difficulty** - Build on previous labs
3. **Complete examples** - Working code students can run
4. **Verification steps** - Checkpoints to confirm progress
5. **Common mistakes section** - What do students struggle with?
6. **Time estimate** - How long will this take?

### Lab Checklist

- [ ] Learning objectives stated
- [ ] Prerequisites listed
- [ ] Step-by-step instructions
- [ ] Code examples work
- [ ] Checkpoints included
- [ ] Troubleshooting section
- [ ] Completion checklist
- [ ] Estimated time provided
- [ ] Common mistakes documented
- [ ] Sample solution created (in `learn/solutions/`)

---

## 🐛 Reporting Issues

### Bug Reports

**Include:**

1. **Description** - What's wrong?
2. **Steps to reproduce** - How to see the bug?
3. **Expected behavior** - What should happen?
4. **Actual behavior** - What actually happens?
5. **Environment** - OS, Python version, Node version
6. **Screenshots** - If applicable

**Template:**

```markdown
**Bug Description:**
[Clear description]

**To Reproduce:**

1. Go to '...'
2. Click on '....'
3. See error

**Expected:** [What should happen]
**Actual:** [What actually happens]

**Environment:**

- OS: [e.g., macOS 13.0]
- Python: [e.g., 3.13]
- Node: [e.g., 20.0]

**Screenshots:** [If applicable]
```

### Feature Requests

**Include:**

1. **Problem** - What problem does this solve?
2. **Proposed solution** - How should it work?
3. **Alternatives** - Other ways to solve it?
4. **Context** - Why is this important?

---

## 📖 Documentation Contributions

### Types of Doc Contributions

1. **Fix typos/errors** - Quick fixes
2. **Clarify existing docs** - Make things clearer
3. **Add examples** - Show how things work
4. **Create new guides** - Fill documentation gaps
5. **Improve organization** - Better structure

### Documentation PRs

**Small fixes** (typos, broken links):

- Just create PR directly
- No issue needed

**Large changes** (new guides, restructuring):

- Create issue first
- Discuss approach
- Then create PR

---

## 🎯 Priority Areas

### High Priority

These contributions are especially valuable:

1. **Missing lab content** - Labs 6-12 marked "Coming soon"
2. **Test coverage gaps** - Increase backend coverage
3. **E2E test stability** - Reduce flaky tests
4. **Documentation improvements** - Make guides clearer
5. **Cross-platform fixes** - Windows compatibility

### Good First Issues

Look for issues tagged:

- `good-first-issue` - Perfect for beginners
- `documentation` - Doc improvements
- `help-wanted` - We need help!
- `lab-content` - Create/improve labs

---

## 💬 Communication

### Getting Help

- **GitHub Issues** - For bugs and features
- **GitHub Discussions** - For questions and ideas
- **Pull Request comments** - For code-specific discussions

### Be Respectful

- Be kind and professional
- Assume good intentions
- Provide constructive feedback
- Help newcomers

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## 🙏 Thank You

Every contribution makes Testbook better for learners worldwide. Whether you:

- Fix a typo
- Report a bug
- Create a lab
- Improve tests
- Update documentation

**You're helping people learn valuable skills. Thank you!** 🎉

---

## 📞 Questions?

- **General questions:** Create a GitHub Discussion
- **Bug reports:** Create a GitHub Issue
- **Security issues:** Email (provide email here)

---

**Happy Contributing! Let's make testing education better together! 🚀**
