# 🎓 Automation Testing 101

**A Self-Guided Learning Path Using Testbook**

Welcome to Automation Testing 101! This structured learning path teaches you professional test automation through hands-on practice with a real application.

Perfect for individual learners, junior developers exploring testing, or manual QA professionals transitioning to automation.

---

## 📖 Learning Path Overview

**Duration:** Self-paced (~30-40 hours total)
**Prerequisites:** Basic programming knowledge (Python or JavaScript)
**Format:** Hands-on labs, real code, practical exercises
**Outcome:** Professional automation testing skills

### What You'll Learn

By the end of this learning path, you will:

- ✅ Write automated tests that actually work
- ✅ Use industry-standard testing tools
- ✅ Test APIs, UIs, and databases
- ✅ Measure and improve test coverage
- ✅ Set up CI/CD pipelines
- ✅ Apply professional testing practices
- ✅ Build a portfolio of testing projects

### What Makes This Different

- **Real application** - Production-grade codebase
- **Executable tests** - Run and see results immediately
- **Multiple frameworks** - Learn what professionals use
- **Hands-on labs** - Practice, not just theory
- **Progressive difficulty** - Build skills gradually
- **Industry-relevant** - Tools used in real jobs
- **Self-paced** - Learn at your own speed

---

## 📚 Learning Path Structure

### Module 1: Foundations

**Goal:** Understand testing basics and set up environment

- [Section 1: Introduction to Testing](#section-1-introduction-to-testing)
- [Section 2: Environment Setup & First Tests](#section-2-environment-setup--first-tests)

**Time Estimate:** 4-6 hours

### Module 2: Backend Testing

**Goal:** Master backend testing with pytest

- [Section 3: Unit Testing](#section-3-unit-testing)
- [Section 4: Integration Testing](#section-4-integration-testing)
- [Section 5: Database Testing](#section-5-database-testing)

**Time Estimate:** 8-12 hours

### Module 3: Frontend Testing

**Goal:** Master frontend component and E2E testing

- [Section 6: Frontend Component Testing](#section-6-frontend-component-testing) ✨
- [Section 7: E2E Testing Basics](#section-7-e2e-testing-basics)
- [Section 8: Advanced E2E Patterns](#section-8-advanced-e2e-patterns)

**Time Estimate:** 8-12 hours

### Module 4: Specialized Testing

**Goal:** Learn API, contract, performance, and security testing

- [Section 9: API & Contract Testing](#section-9-api-contract-testing) ✨
- [Section 10: Performance Testing](#section-10-performance-testing)
- [Section 11: Security Testing](#section-11-security-testing)

**Time Estimate:** 10-14 hours

### Module 5: Professional Practices

**Goal:** CI/CD, observability, and real-world practices

- [Section 12: CI/CD & Automation](#section-12-cicd--automation) ✨
- [Section 13: Logging & Observability](#section-13-logging--observability) ✨
- [Section 14: Building Your Own Features](#section-14-building-your-own-features)

**Time Estimate:** 6-10 hours

---

## 📅 Detailed Curriculum

---

## Section 1: Introduction to Testing

### 🎯 Learning Objectives

- Understand why testing matters

- Learn types of testing
- Explore Testbook application
- Run your first test

### 📖 Theory (30 minutes)

**What is Software Testing?**

- Finding bugs before users do
- Ensuring quality
- Building confidence in code

**Types of Testing:**

- **Unit Testing** - Test individual functions

- **Integration Testing** - Test components together
- **E2E Testing** - Test complete user flows
- **API Testing** - Test backend endpoints
- **Performance Testing** - Test speed and load
- **Security Testing** - Test for vulnerabilities

### 🛠️ Hands-On Lab 1.1: Explore Testbook (45 minutes)

**Step 1: Start the Application**

```bash
cd Testbook
./start-dev.sh  # or start-dev.bat on Windows
```

**Step 2: Explore Features**

1. Open <http://localhost:3000> (development UI started by `start-dev` scripts)
   - If you launched with Docker (`start.sh` / `start.bat`), the UI will instead be available at <http://localhost:8000>.
2. Login with: `sarah.johnson@testbook.com` / `Sarah2024!`
3. Create a post
4. React to posts
5. Follow a user
6. Check your profile

**Step 3: Explore the API**

1. Open http://localhost:8000/docs
2. Try the `/api/auth/login` endpoint
3. Use the token to call `/api/auth/me`
4. Explore other endpoints

**✏️ Exercise:** Write down 5 things you could test in Testbook

### 🛠️ Hands-On Lab 1.2: Read Existing Code (30 minutes)

**Explore the codebase:**

1. **Backend Structure**

   ```bash
   ls backend/
   # Look at: main.py, models.py, routers/
   ```

2. **Frontend Structure**

   ```bash
   ls frontend/src/

   # Look at: App.jsx, pages/, components/
   ```

3. **Understanding the Flow**
   - User logs in → Token generated
   - Token sent with requests → API validates
   - Data from database → Returned as JSON

   - Frontend displays → User sees result

**✏️ Exercise:** Draw a diagram of how login works (User → Frontend → Backend → Database)

### 📝 Section 1 Self-Assessment

**Self-Check:**

Reflect on these questions to verify your understanding:

1. What are the 3 main types of testing?
2. What port does the backend run on?
3. What framework is the backend built with?
4. How do you reset the database?
5. Name 3 features in Testbook you could test

**Checkpoint:**

Document your progress:

- Diagram of login flow
- List of 5 testable features

### 📚 Resources

- [README.md](README.md) - Project overview
- [PROJECT_INFO.md](PROJECT_INFO.md) - Technical details
- [QUICKSTART.md](QUICKSTART.md) - Setup guide

---

## Section 2: Environment Setup & First Tests

### 🎯 Learning Objectives

- Set up testing tools
- Run existing tests
- Understand test structure

- Modify a simple test

### 📖 Theory (30 minutes)

**Test Anatomy:**

```python

def test_something():
    # Arrange - Set up test data
    password = "test123"

    # Act - Perform action
    result = hash_password(password)


    # Assert - Verify result
    assert result != password
```

**Why This Matters:**

- Arrange-Act-Assert is industry standard
- Makes tests readable
- Makes tests maintainable

### 🛠️ Hands-On Lab 2.1: Run Existing Tests (45 minutes)

**Step 1: Install Dependencies**

```bash

cd backend
source venv/bin/activate
pip install -r requirements.txt
```

**Step 2: Run Your First Test**

```bash
pytest tests/test_unit_auth.py::TestPasswordHashing::test_password_is_hashed -v
```

**Expected Output:**

```
tests/test_unit_auth.py::TestPasswordHashing::test_password_is_hashed PASSED ✓
```

**Step 3: Run All Tests**

```bash
pytest tests/ -v
```

**Expected Output:**

```
====================== 166 passed in 51s =======================
```

**Step 4: Generate Coverage Report**

```bash
pytest --cov --cov-report=html
open htmlcov/index.html
```

**✏️ Exercise:** Find a test with 100% coverage and one with <80% coverage

### 🛠️ Hands-On Lab 2.2: Understand Test Structure (60 minutes)

**Step 1: Read a Simple Test**

Open `backend/tests/test_unit_auth.py` and find this test:

```python
def test_password_is_hashed(self):
    """Test that password hashing produces a different string."""
    password = "TestPassword123!"
    hashed = get_password_hash(password)

    assert hashed != password
    assert len(hashed) > len(password)
    assert hashed.startswith("$2b$")
```

**Understand:**

- Line 1: Test function name (must start with `test_`)
- Line 2: Docstring explains what test does
- Lines 4-5: Arrange - Set up test data
- Line 7: Act - Call function being tested
- Lines 9-11: Assert - Verify results

**Step 2: Read Test Fixtures**

Open `backend/tests/conftest.py` and find:

```python
@pytest.fixture
def test_user(db_session: Session) -> User:
    """Create a test user in the database."""
    user = User(
        email="testuser@example.com",
        username="testuser",
        display_name="Test User",
        hashed_password=get_password_hash("TestPassword123!"),
    )

    db_session.add(user)
    db_session.commit()
    return user
```

**Understand:**

- `@pytest.fixture` - Reusable test setup
- Used by: `def test_something(test_user):`
- Automatically cleaned up after test

**✏️ Exercise:** Identify which tests use the `test_user` fixture

### 🛠️ Hands-On Lab 2.3: Modify a Test (45 minutes)

**Challenge:** Modify an existing test

**Step 1:** Find this test in `test_unit_auth.py`:

```python
def test_verify_correct_password(self):
    """Test that correct password verification succeeds."""
    password = "TestPassword123!"

    hashed = get_password_hash(password)

    assert verify_password(password, hashed) is True
```

**Step 2:** Add a new assertion:

```python
def test_verify_correct_password(self):
    """Test that correct password verification succeeds."""
    password = "TestPassword123!"
    hashed = get_password_hash(password)


    assert verify_password(password, hashed) is True
    # NEW: Verify hash looks like bcrypt format
    assert hashed.startswith("$2b$")  # ← Add this line
```

**Step 3:** Run your modified test:

```bash
pytest tests/test_unit_auth.py::TestPasswordHashing::test_verify_correct_password -v
```

**Step 4:** Verify it still passes!

**✏️ Exercise:** Add one more assertion to test that hash length > 50 characters

### 📝 Section 2 Self-Assessment

**Practical:**

1. Run all tests and show passing output
2. Generate coverage report

3. Modify a test and show it passing
4. Explain what a fixture does

**Self-Check:**

Reflect on these questions to verify your understanding:

1. What does `pytest` command do?
2. What is the Arrange-Act-Assert pattern?
3. What is a test fixture?
4. What does code coverage measure?

### 📚 Resources

- [backend/tests/README.md](backend/tests/README.md) - Backend testing guide
- [RUNNING_TESTS.md](RUNNING_TESTS.md) - How to run tests

---

## Section 3: Unit Testing

### 🎯 Learning Objectives

- Write your first unit test
- Test individual functions
- Use parameterized tests
- Achieve high coverage

### 📖 Theory (30 minutes)

**What is Unit Testing?**

- Tests ONE function or method
- Fast to run (no database, no network)
- Isolates bugs quickly
- Foundation of test pyramid

**Unit Test Best Practices:**

- Test one thing at a time
- Use descriptive names
- No external dependencies
- Fast execution (<10ms each)

### 🛠️ Hands-On Lab 3.1: Write Your First Unit Test (60 minutes)

**Challenge:** Test a new function

**Step 1:** Add a function to `backend/auth.py`:

```python
def is_valid_username(username: str) -> bool:
    """Check if username is valid (3-20 chars, alphanumeric)."""
    if len(username) < 3 or len(username) > 20:

        return False
    return username.isalnum()
```

**Step 2:** Create test file `backend/tests/test_unit_validation.py`:

```python
import pytest
from auth import is_valid_username


@pytest.mark.unit
class TestUsernameValidation:
    """Test username validation."""

    def test_valid_username(self):
        """Test that valid username is accepted."""
        assert is_valid_username("testuser") is True


    def test_username_too_short(self):
        """Test that short username is rejected."""
        assert is_valid_username("ab") is False

    def test_username_too_long(self):
        """Test that long username is rejected."""
        assert is_valid_username("a" * 21) is False

    def test_username_with_special_chars(self):
        """Test that special characters are rejected."""
        assert is_valid_username("test@user") is False
```

**Step 3:** Run your tests:

```bash
pytest tests/test_unit_validation.py -v
```

**Step 4:** Verify 4/4 tests pass!

**✏️ Exercise:** Add 3 more test cases:

- Empty username
- Username with spaces

- Username with numbers only

### 🛠️ Hands-On Lab 3.2: Parameterized Tests (45 minutes)

**Challenge:** Test multiple inputs efficiently

**Instead of writing separate tests:**

```python
def test_valid_username_1(self):
    assert is_valid_username("user1") is True

def test_valid_username_2(self):
    assert is_valid_username("user2") is True
```

**Use parameterization:**

```python
@pytest.mark.parametrize("username,expected", [
    ("user1", True),
    ("user2", True),
    ("ab", False),
    ("a" * 21, False),
    ("test@user", False),
])
def test_username_validation(self, username, expected):
    """Test various usernames."""
    assert is_valid_username(username) is expected
```

**Benefits:**

- Write once, test many cases
- Easy to add more cases

- Clear test data

**✏️ Exercise:** Add 5 more test cases to the parameterized test

### 🛠️ Hands-On Lab 3.3: Test Coverage Challenge (60 minutes)

**Challenge:** Improve coverage of a specific file

**Step 1:** Check current coverage:

```bash
pytest --cov=auth --cov-report=term-missing
```

**Step 2:** Find untested lines in `auth.py`

**Step 3:** Write tests to cover those lines

**Step 4:** Run coverage again and verify improvement

**Goal:** Get auth.py to 90%+ coverage

**✏️ Exercise:** Document which tests you added and why

### 📝 Section 3 Practice Project

**Project:** Test a New Feature

Add validation for email domains and write comprehensive tests:

```python
# In auth.py
def is_allowed_email_domain(email: str) -> bool:
    """Check if email domain is allowed."""
    allowed_domains = ["testbook.com", "example.com", "test.com"]
    domain = email.split("@")[-1]
    return domain in allowed_domains


# In tests/test_unit_validation.py
class TestEmailDomainValidation:
    # Write 5+ tests here
    pass
```

**Requirements:**

- 5+ test cases
- Test valid domains
- Test invalid domains
- Test edge cases (no @, multiple @, etc.)
- 100% coverage of the function

### 📚 Resources

- Study: `tests/test_unit_auth.py`
- Study: `tests/test_unit_models.py`
- Read: [Pytest Documentation](https://docs.pytest.org/)

---

## Section 4: Integration Testing

### 🎯 Learning Objectives

- Test API endpoints
- Use FastAPI TestClient
- Test authentication flows
- Test complete features

### 📖 Theory (30 minutes)

**What is Integration Testing?**

- Tests multiple components together
- Tests real API endpoints
- Uses TestClient (no real server needed)
- Verifies features work end-to-end

**Integration vs Unit:**

- Unit: `hash_password()` function
- Integration: `/api/auth/register` endpoint (uses hash_password, database, validation)

### 🛠️ Hands-On Lab 4.1: Test an API Endpoint (60 minutes)

**Challenge:** Write integration test for registration

**Step 1:** Study existing test:

```python
# From tests/test_api_auth.py
def test_register_new_user_success(self, client):
    """Test successful user registration."""
    response = client.post(
        "/api/auth/register",
        json={
            "email": "newuser@example.com",
            "username": "newuser",
            "display_name": "New User",
            "password": "SecurePass123!",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
```

**Step 2:** Understand the parts:

- `client` - FastAPI TestClient (from fixture)
- `client.post()` - Make API request
- `response.json()` - Parse response
- `assert` - Verify results

**Step 3:** Write similar test for login:

```python
def test_your_login_test(self, client):
    """Test login endpoint."""
    # Your code here
    pass

```

**✏️ Exercise:** Write the complete login test

### 🛠️ Hands-On Lab 4.2: Test Complete Flow (90 minutes)

**Challenge:** Test registration → login → create post flow

```python
def test_complete_user_journey(self, client):
    """Test full user journey from registration to posting."""
    # Step 1: Register
    register_response = client.post(
        "/api/auth/register",
        json={
            "email": "journey@test.com",
            "username": "journeyuser",
            "display_name": "Journey User",
            "password": "Test123!",
        }

    )
    assert register_response.status_code == 200
    token = register_response.json()["access_token"]

    # Step 2: Create post with token
    headers = {"Authorization": f"Bearer {token}"}
    post_response = client.post(
        "/api/posts/",

        json={"content": "My first post!"},
        headers=headers
    )
    assert post_response.status_code == 200

    # Step 3: Verify post exists

    post_id = post_response.json()["id"]
    get_response = client.get(f"/api/posts/{post_id}", headers=headers)
    assert get_response.status_code == 200
    assert get_response.json()["content"] == "My first post!"
```

**✏️ Exercise:** Extend this to add a comment and reaction

### 🛠️ Hands-On Lab 4.3: Test Error Cases (60 minutes)

**Challenge:** Test what happens when things go wrong

**Error Cases to Test:**

1. Register with duplicate email
2. Login with wrong password
3. Create post without authentication

4. Delete someone else's post

**Template:**

```python
def test_error_case_name(self, client):

    """Test [describe error scenario]."""
    # Trigger the error
    response = client.post(...)

    # Verify proper error response
    assert response.status_code == 400  # or 401, 403, 404
    assert "error message" in response.json()["detail"]
```

**✏️ Exercise:** Write 5 error case tests

### 📝 Section 4 Practice Project

**Project:** Test the Feed Feature

Create `backend/tests/test_api_feed_extended.py`:

**Requirements:**

- Test getting all feed
- Test getting following feed
- Test feed filtering (blocked users don't appear)
- Test feed ordering (newest first)
- Test empty feed (no posts)
- 10+ tests total

**Acceptance Criteria:**

- All tests pass
- Tests use fixtures from conftest.py
- Tests are well-documented
- Coverage of feed.py improves

### 📚 Resources

- Study: `tests/test_api_auth.py`
- Study: `tests/test_api_posts.py`
- Study: `tests/conftest.py` (fixtures)

---

## Section 5: Database Testing

### 🎯 Learning Objectives

- Test database models
- Test relationships

- Test constraints
- Test cascade deletes

### 📖 Theory (30 minutes)

**Why Test the Database?**

- Models define data structure
- Relationships can be complex
- Constraints prevent bad data
- Cascades affect data integrity

**What to Test:**

- Model creation
- Field validation
- Relationships (follow, block)
- Cascade deletes
- Unique constraints

### 🛠️ Hands-On Lab 5.1: Test Database Models (60 minutes)

**Challenge:** Test User model

**Study this example:**

```python
def test_create_user(self, db_session):
    """Test creating a user."""
    user = User(
        email="test@example.com",
        username="testuser",
        display_name="Test User",
        hashed_password=get_password_hash("password"),
    )
    db_session.add(user)

    db_session.commit()
    db_session.refresh(user)

    assert user.id is not None
    assert user.email == "test@example.com"
```

**✏️ Exercise:** Write a test for Post model creation

### 🛠️ Hands-On Lab 5.2: Test Relationships (90 minutes)

**Challenge:** Test follower/following relationships

```python
def test_follow_relationship(self, db_session, test_user, test_user_2):
    """Test following another user."""
    # Arrange
    test_user.following.append(test_user_2)

    db_session.commit()

    # Assert
    assert test_user_2 in test_user.following
    assert test_user in test_user_2.followers
```

**✏️ Exercise:** Write tests for:

- Block relationship
- Multiple followers
- Unfollow
- Mutual following

### 🛠️ Hands-On Lab 5.3: Test Cascade Deletes (60 minutes)

**Challenge:** Verify deleting user deletes their posts

```python
def test_delete_user_deletes_posts(self, db_session, test_user):
    """Test cascade delete."""
    # Arrange: Create post

    post = Post(author_id=test_user.id, content="Test")
    db_session.add(post)
    db_session.commit()
    post_id = post.id

    # Act: Delete user
    db_session.delete(test_user)

    db_session.commit()

    # Assert: Post should be gone
    deleted_post = db_session.query(Post).filter(Post.id == post_id).first()
    assert deleted_post is None
```

**✏️ Exercise:** Test that deleting a post deletes its comments and reactions

### 📝 Section 5 Practice Project

**Project:** Test Comment Model Completely

Create comprehensive tests for the Comment model:

**Requirements:**

- Test comment creation
- Test comment-post relationship
- Test comment-author relationship
- Test deleting post deletes comments
- Test deleting user deletes their comments
- 10+ tests total
- 100% coverage of Comment model

### 📚 Resources

- Study: `tests/test_unit_models.py`
- Study: `tests/test_database.py`
- Read: `backend/models.py`

---

## Section 6: Frontend Component Testing

> **🆕 Dual-Stack Note:** This section focuses on **JavaScript/React** component testing. If you're following the **Python-first track**, you can skip to [Section 7: E2E Testing](#section-7-e2e-testing-basics) which offers both Python and JavaScript options.

### 🎯 Learning Objectives ✨

- Understand component testing
- Use Vitest and React Testing Library
- Test React components in isolation
- Test accessibility with axe-core
- Test keyboard navigation
- **🆕 ADVANCED:** Network mocking, async data, stateful components

### 📊 Section 6 Content Overview

| Level | Content | Time | Description |
|-------|---------|------|-------------|
| **Beginner** | Lab 6.1-6.3 (inline) | 1-2 hours | Basic component testing patterns |
| **Advanced** | **🆕 [Lab 6B](../../labs/LAB_06B_Advanced_Component_Testing.md)** | 2 hours | MSW, async loading, accessibility testing |
| **Integration** | **🆕 [Lab 6C](../../labs/LAB_06C_Frontend_Integration_Testing.md)** | 90 min | OpenAPI contracts, integration tests |

**💡 For Python learners:** Section 6 is JavaScript-focused (React component testing). You can skip to [Section 7: E2E Testing](#section-7-e2e-testing-basics) which offers both Python and JavaScript options. If you want to understand frontend testing, consider learning Lab 4 JavaScript → Lab 6B for cross-stack awareness.

**For hybrid learners (Python backend + JS frontend):** Complete backend labs (1-5), then come here for Labs 6B → 6C to master frontend testing.

**📚 JavaScript Basics:** If you're new to JavaScript, try [learn-js.org](https://www.learn-js.org/) for free interactive tutorials before diving into component testing!

### 📖 Theory (20 minutes)

**What is Component Testing?**

- Tests individual React components
- Faster than E2E, more realistic than unit tests
- Tests user interactions without full browser
- Perfect for UI logic

**Testing Pyramid Position:**

- Below E2E (faster)
- Above unit tests (more realistic)
- Tests component behavior, not implementation

### 🛠️ Hands-On Lab 6.1: Run Component Tests (15 minutes)

**Step 1:** Run existing component tests:

```bash
cd frontend
npm test
```

**Step 2:** Run with coverage:

```bash
npm run test:coverage
```

**Step 3:** Run accessibility tests:

```bash
npm test -- accessibility
```

**✏️ Exercise:** Examine test output and identify what's being tested

### 🛠️ Hands-On Lab 6.2: Component Testing Patterns (45 minutes)

**Example:** Testing a button component

```javascript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import Button from '../components/Button';

describe('Button Component', () => {
  it('renders with correct text', () => {
    render(<Button>Click Me</Button>);
    expect(screen.getByText('Click Me')).toBeInTheDocument();
  });

  it('calls onClick when clicked', async () => {
    const handleClick = vi.fn();
    const user = userEvent.setup();

    render(<Button onClick={handleClick}>Click</Button>);
    await user.click(screen.getByText('Click'));

    expect(handleClick).toHaveBeenCalledOnce();
  });

  it('is keyboard accessible', async () => {
    const user = userEvent.setup();
    render(<Button>Click</Button>);

    const button = screen.getByText('Click');
    await user.tab();

    expect(button).toHaveFocus();
  });
});
```

**Key Patterns:**

- `screen` - Query rendered output
- `userEvent` - Simulate user interactions
- `vi.fn()` - Mock functions
- `toBeInTheDocument()` - Verify presence

**✏️ Exercise:** Write tests for a form input component

### 🛠️ Hands-On Lab 6.3: Accessibility Testing (45 minutes)

**Why Test Accessibility?**

- Legal requirements (ADA, WCAG)
- Better UX for everyone
- Catch issues early
- Automated compliance checking

**Example:** Using axe-core

```javascript
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'vitest-axe';
import LoginForm from '../components/LoginForm';

expect.extend(toHaveNoViolations);

it('has no accessibility violations', async () => {
  const { container } = render(<LoginForm />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});

it('has proper labels', () => {
  const { getByLabelText } = render(<LoginForm />);
  expect(getByLabelText(/username/i)).toBeInTheDocument();
  expect(getByLabelText(/password/i)).toBeInTheDocument();

});
```

**Common A11y Checks:**

- Form labels
- Button text
- Heading hierarchy
- Color contrast
- Keyboard navigation
- ARIA attributes

**✏️ Exercise:** Run accessibility tests on all components and fix violations

### 📝 Section 6 Practice Project

**Project:** Test the CreatePost Component

- Test rendering
- Test form submission
- Test input validation
- Test file upload
- Test accessibility
- 8+ tests total

**Study:** `frontend/src/tests/` for examples

### 🚀 Ready for Advanced Component Testing?

**Complete these beginner patterns first, then level up:**

**🆕 [Lab 6B: Advanced Component Testing](../../labs/LAB_06B_Advanced_Component_Testing.md)**

- Mock Service Worker (MSW) network mocking
- Testing async data loading states
- Testing stateful components
- React Context testing
- Comprehensive accessibility testing
- **Time:** 120 minutes

**Why Lab 6B matters:**

- Professional network mocking patterns
- Realistic async data scenarios
- Accessibility automation
- Used in production React apps

### 📚 Resources

**Basic Component Testing:**

- [Vitest Documentation](https://vitest.dev/)
- [React Testing Library](https://testing-library.com/react)
- [axe-core](https://github.com/dequelabs/axe-core)
- Study: `frontend/src/tests/`

**Advanced Patterns:**

- **🆕 [Lab 6B: Advanced Component Testing](../../labs/LAB_06B_Advanced_Component_Testing.md)** - MSW, async, accessibility
- **🆕 [Testing Comparison Guide](../guides/TESTING_COMPARISON_PYTHON_JS.md)** - See how component testing relates to Python testing

---

## Section 7: E2E Testing Basics

> **🆕 Choose Your Stack:** This section teaches E2E testing with **Playwright**, which works with both **Python and JavaScript**! Pick your preferred language and follow along. The concepts are identical across both stacks.

### 🎯 Learning Objectives

- Understand E2E testing
- Use Playwright (Python OR JavaScript)
- Test user interfaces
- Test complete user flows
- **🆕 Learn advanced patterns:** Page objects, fixtures, network mocking

### 📊 Section 7 Content Overview

| Level | Python Track | JavaScript Track | Time |
|-------|-------------|------------------|------|
| **Beginner** | [Lab 4: E2E Python](../../labs/LAB_04_E2E_Testing_Python.md) | [Lab 4: E2E JavaScript](../../labs/LAB_04_E2E_Testing_JavaScript.md) | 90 min |
| **Inline** | Lab 7.1-7.3 (below) | Lab 7.1-7.3 (below) | 2-3 hours |
| **Advanced** | **🆕 [Lab 4B: Advanced Python](../../labs/LAB_04B_Advanced_E2E_Python.md)** | **🆕 [Section 8 Advanced Patterns](SECTION_08_ADVANCED_E2E_PATTERNS.md)** | 2 hours |

**💡 Recommendation:**

- **New learners:** Start with [Lab 4](../../labs/LAB_04_E2E_Testing_Python.md) in your preferred language
- **Experienced:** Jump to the advanced content after completing basics below
- **Full-stack:** Complete both Lab 4 versions to see the differences!

**🔄 Hybrid Micro-Path (Python Backend + JavaScript Frontend):**

If you're working with a Python backend and JavaScript frontend stack (the most common real-world scenario), follow this recommended sequence:

1. **Backend foundation:** Complete Labs 1-5 (Python backend testing)
2. **E2E Python:** [Lab 4 Python](../../labs/LAB_04_E2E_Testing_Python.md) (test backend via Playwright)
3. **Component testing:** [Lab 6B](../../labs/LAB_06B_Advanced_Component_Testing.md) (test React components in isolation)
4. **Integration testing:** [Lab 6C](../../labs/LAB_06C_Frontend_Integration_Testing.md) (validate frontend-backend contracts)
5. **Advanced Python E2E:** [Lab 4B](../../labs/LAB_04B_Advanced_E2E_Python.md) (professional page objects, fixtures)
6. **Advanced patterns:** [Section 8](SECTION_08_ADVANCED_E2E_PATTERNS.md) (compare both stacks)

**Why this order?** You build from backend → E2E → component → integration → advanced, mirroring how full-stack features are developed and ensuring you understand contracts between layers.

### 📖 Theory (30 minutes)

**What is E2E Testing?**

- End-to-End testing
- Tests complete user journeys
- Tests real browser
- Slowest but most realistic

**When to Use E2E:**

- Critical user paths
- Cross-component features
- UI interactions
- Real browser behavior

### 🛠️ Hands-On Lab 7.1: Setup Playwright (30 minutes)

> **Choose your language:** Follow the setup for your chosen stack (Python OR JavaScript). Both teach the same concepts!

#### 🐍 Python Setup

**Step 1:** Install Playwright Python

```bash
cd tests/e2e-python
pip install -r requirements.txt
playwright install chromium
```

**Step 2:** Run example test:

```bash
pytest test_auth.py::TestAuthentication::test_login_success -v --headed
```

**Step 3:** Watch the test run in the browser!

**✏️ Exercise:** Run in slow motion: `pytest test_auth.py -v --headed --slowmo=1000`

---

#### ☕ JavaScript Setup

**Step 1:** Install Playwright JavaScript

```bash
cd tests
npm install
npx playwright install chromium
```

**Step 2:** Run example test:

```bash
npx playwright test auth.spec.js --headed
```

**Step 3:** Watch the test run in the browser!

**✏️ Exercise:** Run test in debug mode: `npx playwright test --debug`

### 🛠️ Hands-On Lab 7.2: Your First E2E Test (90 minutes)

**Challenge:** Write a login test in your chosen language

> **Quick Links:** Already completed Lab 4? This is a refresher. Advanced learners: Jump to [Lab 4B (Python)](../../labs/LAB_04B_Advanced_E2E_Python.md) or continue to Section 8.

#### 🐍 Python Version

**Step 1:** Create new file `tests/e2e-python/test_my_first.py`:

```python
from playwright.sync_api import Page, expect

def test_login_successfully(page: Page):
    """Test successful login."""
    # Navigate to app
    page.goto('http://localhost:3000')

    # Fill login form
    page.fill('[data-testid="login-email-input"]', 'sarah.johnson@testbook.com')
    page.fill('[data-testid="login-password-input"]', 'Sarah2024!')

    # Click login
    page.click('[data-testid="login-submit-button"]')

    # Verify logged in
    expect(page.locator('[data-testid="navbar"]')).to_be_visible()
```

**Step 2:** Run your test:

```bash
cd tests/e2e-python
pytest test_my_first.py -v --headed
```

**Step 3:** Watch it work!

**✏️ Exercise:** Add assertion to verify username appears in navbar

**Next:** [Lab 4: E2E Python](../../labs/LAB_04_E2E_Testing_Python.md) → [Lab 4B: Advanced](../../labs/LAB_04B_Advanced_E2E_Python.md)

---

#### ☕ JavaScript Version

**Step 1:** Create new file `tests/e2e/mytest.spec.js`:

```javascript
const { test, expect } = require('@playwright/test');

test('should login successfully', async ({ page }) => {
  // Navigate to app
  await page.goto('http://localhost:3000');

  // Fill login form
  await page.fill('[data-testid="login-email-input"]',
                  'sarah.johnson@testbook.com');
  await page.fill('[data-testid="login-password-input"]',
                  'Sarah2024!');

  // Click login
  await page.click('[data-testid="login-submit-button"]');

  // Verify logged in
  await expect(page.locator('[data-testid="navbar"]'))
    .toBeVisible();
});
```

**Step 2:** Run your test:

```bash
cd tests
npx playwright test mytest.spec.js --headed
```

**Step 3:** Watch it work!

**✏️ Exercise:** Add assertion to verify username appears in navbar

**Next:** [Lab 4: E2E JavaScript](../../labs/LAB_04_E2E_Testing_JavaScript.md) → [Lab 6B: Components](../../labs/LAB_06B_Advanced_Component_Testing.md) → [Lab 6C: Integration](../../labs/LAB_06C_Frontend_Integration_Testing.md)

### 🛠️ Hands-On Lab 7.3: Test User Actions (90 minutes)

**Challenge:** Test creating a post

```javascript
const { loginUser, createPost, getFirstPost } = require('./fixtures/test-helpers');

test('should create a post', async ({ page }) => {
  // Login

  await loginUser(page, 'sarah.johnson@testbook.com', 'Sarah2024!');

  // Create post
  await createPost(page, 'My test post!');

  // Verify post appears
  const firstPost = getFirstPost(page);
  await expect(firstPost).toContainText('My test post!');
  await expect(firstPost).toHaveAttribute('data-is-own-post', 'true');
});
```

**✏️ Exercise:** Add test for:

- Creating post with empty content (should fail)
- Creating post with very long content
- Creating multiple posts

### 📝 Section 7 Practice Project

**Project:** Test Complete Registration Flow

Write E2E test that:

1. Navigates to registration page
2. Fills all fields
3. Submits form
4. Verifies auto-login
5. Verifies redirect to feed
6. Creates first post
7. Verifies post appears

**Requirements:**

- Use test helpers
- Test passes consistently
- Well documented
- Takes screenshots on failure

**Complete in your preferred stack:**

- 🐍 **Python:** Use [Lab 4: E2E Python](../../labs/LAB_04_E2E_Testing_Python.md) as a guide
- ☕ **JavaScript:** Use [Lab 4: E2E JavaScript](../../labs/LAB_04_E2E_Testing_JavaScript.md) as a guide

### 🚀 Ready for Advanced E2E Patterns?

**Complete the basics above first, then dive deeper:**

#### 🐍 Python Track

**🆕 [Lab 4B: Advanced E2E Testing (Python)](../../labs/LAB_04B_Advanced_E2E_Python.md)**

- Page Object Model
- Advanced pytest fixtures
- Network interception
- Pytest markers (smoke/regression)
- Data builders
- **Time:** 120 minutes

#### ☕ JavaScript Track

**🆕 [Section 8: Advanced E2E Patterns](SECTION_08_ADVANCED_E2E_PATTERNS.md)**

- Advanced fixtures
- Network mocking
- Multi-browser testing
- **Time:** Continue to Section 8 below

#### 🔄 Both Stacks

**🆕 [Testing Comparison: Python vs JavaScript](../guides/TESTING_COMPARISON_PYTHON_JS.md)**

- See both implementations side-by-side
- Translate knowledge between stacks
- Understand equivalents

### 📚 Resources

**Beginner E2E:**

- Study: `tests/e2e/auth.spec.js` (JavaScript)
- Study: `tests/e2e-python/test_auth.py` (Python)
- Read: [Playwright Documentation](https://playwright.dev/)
- Read: [tests/README.md](tests/README.md)

**Advanced E2E:**

- **🆕 [Lab 4B: Advanced E2E Python](../../labs/LAB_04B_Advanced_E2E_Python.md)** - Professional Python patterns
- **🆕 [Section 8: Advanced Patterns](SECTION_08_ADVANCED_E2E_PATTERNS.md)** - Dual-stack comprehensive guide
- **🆕 [Testing Comparison Guide](../guides/TESTING_COMPARISON_PYTHON_JS.md)** - Python ↔ JavaScript translation

---

## Section 8: Advanced E2E Patterns

> **🆕 Complete Dual-Stack Section Available!** This inline content introduces advanced concepts. For comprehensive dual-stack coverage (Python AND JavaScript), see the **🆕 [dedicated Advanced E2E Patterns guide](SECTION_08_ADVANCED_E2E_PATTERNS.md)**.

> **🎯 Hybrid learners (Python + JavaScript):** After completing [Lab 6C](../../labs/LAB_06C_Frontend_Integration_Testing.md), you now understand how your React frontend integrates with your FastAPI backend through contracts. Section 8 teaches you advanced E2E patterns for testing the complete stack!

### 🎯 Learning Objectives

- Test dynamic content
- Handle async operations
- Use Page Object Model (both stacks)
- Test cross-browser
- **🆕 Advanced fixtures and network mocking**
- **🆕 CI/CD automation**

### 📊 Section 8 Complete Learning Path

| Content | Python | JavaScript | Description |
|---------|--------|------------|-------------|
| **Basics** | Inline (below) | Inline (below) | Dynamic content, basic POM |
| **Advanced Lab** | **🆕 [Lab 4B](../../labs/LAB_04B_Advanced_E2E_Python.md)** | Inline + Section guide | Page objects, fixtures, mocking |
| **Comprehensive** | **🆕 [Section 8 Guide](SECTION_08_ADVANCED_E2E_PATTERNS.md)** | **🆕 [Section 8 Guide](SECTION_08_ADVANCED_E2E_PATTERNS.md)** | Complete dual-stack coverage |
| **CI/CD** | **🆕 [CI/CD Guide](CI_CD_E2E_TESTING.md)** | **🆕 [CI/CD Guide](CI_CD_E2E_TESTING.md)** | Automate both stacks |

**🎯 Recommended Path:**

1. Complete basics below (2-3 hours)
2. Choose your track:
   - 🐍 **Python:** [Lab 4B: Advanced E2E](../../labs/LAB_04B_Advanced_E2E_Python.md) → [Section 8 Guide](SECTION_08_ADVANCED_E2E_PATTERNS.md)
   - ☕ **JavaScript:** [Section 8 Guide](SECTION_08_ADVANCED_E2E_PATTERNS.md) → JavaScript advanced patterns
   - 🔄 **Both:** Review [Testing Comparison](../guides/TESTING_COMPARISON_PYTHON_JS.md) first
3. Set up CI/CD: [CI/CD for E2E Testing](CI_CD_E2E_TESTING.md)

### 📖 Theory (30 minutes)

**Testing Dynamic Content:**

❌ **Bad:** Hardcode IDs

```javascript
await page.click('[data-testid="post-999-like"]');  // Might not exist!
```

✅ **Good:** Use dynamic selectors

```javascript
const firstPost = page.locator('[data-testid-generic="post-item"]').first();
await firstPost.locator('[data-testid$="-like-button"]').click();
```

### 🛠️ Hands-On Lab 8.1: Test Dynamic Content (90 minutes)

**Challenge:** Test interacting with posts without knowing IDs

**Study pattern:**

```javascript
test('should react to first post', async ({ page }) => {
  await loginUser(page, 'sarah.johnson@testbook.com', 'Sarah2024!');

  // Get first post (most recent)
  const firstPost = page.locator('[data-testid-generic="post-item"]').first();


  // Hover to show reactions
  await firstPost.locator('[data-testid$="-react-button"]').hover();

  // Click like
  await firstPost.locator('[data-testid$="-reaction-like"]').click();

  // Verify reaction added
  await expect(firstPost.locator('[data-testid$="-react-button"]'))
    .toContainText('👍');

});
```

**✏️ Exercise:** Write tests to:

- React to your own post
- React to a specific user's post
- Count all posts in feed

- Find post by content

### 🛠️ Hands-On Lab 8.2: Page Object Model (120 minutes)

**Challenge:** Create reusable page objects

**Create `tests/e2e/pages/FeedPage.js`:**

```javascript
class FeedPage {
  constructor(page) {
    this.page = page;
    this.createPostInput = '[data-testid="create-post-textarea"]';

    this.submitButton = '[data-testid="create-post-submit-button"]';
  }

  async goto() {
    await this.page.goto('http://localhost:3000');

  }

  async createPost(content) {
    await this.page.fill(this.createPostInput, content);
    await this.page.click(this.submitButton);

    await this.page.waitForTimeout(500);
  }

  getFirstPost() {
    return this.page.locator('[data-testid-generic="post-item"]').first();
  }
}

module.exports = { FeedPage };
```

**Use in tests:**

```javascript
const { FeedPage } = require('./pages/FeedPage');

test('should create post using POM', async ({ page }) => {
  const feedPage = new FeedPage(page);
  await loginUser(page, ...);

  await feedPage.createPost('Test post');
  const firstPost = feedPage.getFirstPost();
  await expect(firstPost).toContainText('Test post');
});

```

**✏️ Exercise:** Create `ProfilePage` class with methods for profile actions

### 📝 Section 8 Practice Project

**Project:** Complete Feature Test Suite

Test the entire "Follow User → View Their Posts" flow:

**Requirements:**

- Use Page Object Model
- Test across 2 browsers (Chrome + Firefox)
- Include negative tests (unfollow, block)
- 10+ test scenarios
- Screenshots on failure
- Comprehensive documentation

**Implement in your preferred stack - both are covered in the resources below!**

### 🚀 Deep Dive: Advanced E2E Patterns

**Ready to master professional E2E testing? We've got you covered with comprehensive resources:**

#### 🐍 Python Track - Complete Coverage

**🆕 [Lab 4B: Advanced E2E Testing (Python)](../../labs/LAB_04B_Advanced_E2E_Python.md)** ⭐

- **Page Object Model** - Reusable page classes
- **Advanced fixtures** - Parametrized, factory patterns
- **Network interception** - Mock API responses with Playwright
- **Pytest markers** - Organize tests (smoke, regression)
- **Data builders** - Clean test data creation
- **Time:** 120 minutes
- **Skill Level:** Advanced

**What you'll build:**

```python
# Professional page object
class FeedPage:
    def create_post(self, content: str) -> None:
        self.page.fill(self.textarea, content)
        self.page.click(self.submit)
        expect(self.first_post()).to_contain_text(content)

# Use in tests
def test_complete_workflow(page, login_as):
    login_as("sarah")
    feed = FeedPage(page)
    feed.create_post("Testing with POM!")
```

#### ☕ JavaScript Track - Complete Coverage

**Continue with inline examples above, then:**

**🆕 [Section 8: Advanced E2E Patterns (Dual-Stack)](SECTION_08_ADVANCED_E2E_PATTERNS.md)** ⭐

- **Both Python AND JavaScript implementations**
- Page Object Model in both languages
- Advanced Playwright fixtures
- Network interception examples
- Multi-browser testing setup
- **Time:** 8-10 hours comprehensive study

#### 🔄 Cross-Stack Understanding

**🆕 [Testing Comparison: Python vs JavaScript](../guides/TESTING_COMPARISON_PYTHON_JS.md)**

- Side-by-side syntax comparison
- Framework equivalents (pytest ↔ Vitest, etc.)
- When to use each stack
- Easy knowledge translation
- **Time:** 45 minutes

#### 🚀 CI/CD Automation

**🆕 [CI/CD for E2E Testing](CI_CD_E2E_TESTING.md)**

- GitHub Actions for Python tests
- GitHub Actions for JavaScript tests
- Caching strategies
- Parallel execution
- Artifact capture (screenshots, videos)
- **Both stacks fully covered**
- **Time:** 3-4 hours

### 🎓 Learning Path Summary

**Beginner → Advanced Progression:**

```
Section 7 Basics (inline)
    ↓
Choose Your Track:
    ├─ 🐍 Lab 4B (Python) → Section 8 Guide → CI/CD
    └─ ☕ Section 8 Guide → CI/CD

Optional: Testing Comparison Guide (any time)
```

### 📚 Resources

**Inline Examples (JavaScript Focus):**

- Study: [TESTING_PATTERNS.md](TESTING_PATTERNS.md)
- Study: `tests/e2e/users.spec.js`
- Read: [Playwright Best Practices](https://playwright.dev/docs/best-practices)

**🆕 Advanced Resources (Both Stacks):**

- **[Lab 4B: Advanced E2E Python](../../labs/LAB_04B_Advanced_E2E_Python.md)** - 120 min hands-on Python patterns
- **[Section 8: Advanced Patterns](SECTION_08_ADVANCED_E2E_PATTERNS.md)** - 8-10 hours dual-stack comprehensive
- **[Testing Comparison](../guides/TESTING_COMPARISON_PYTHON_JS.md)** - 45 min Python ↔ JavaScript translation
- **[CI/CD Guide](CI_CD_E2E_TESTING.md)** - 3-4 hours automation for both stacks

**Official Documentation:**

- [Playwright Python](https://playwright.dev/python/)
- [Playwright JavaScript](https://playwright.dev/)
- [pytest fixtures](https://docs.pytest.org/en/stable/fixture.html)

---

## Section 9: API Testing

### 🎯 Learning Objectives

- Test REST APIs directly
- Use Postman and Newman

- Build API test clients
- Automate API testing

### 📖 Theory (30 minutes)

**Why API Testing?**

- Faster than UI testing
- More stable than UI testing

- Tests business logic directly
- Essential for microservices

**API Testing Tools:**

- **Postman** - Visual, great for exploration
- **Newman** - CLI, great for automation
- **Python requests** - Code-based, flexible

### 🛠️ Hands-On Lab 9.1: Use Postman (60 minutes)

**Step 1:** Import collection

1. Open Postman

2. Import `tests/api/Testbook.postman_collection.json`
3. Explore requests

**Step 2:** Run collection

1. Click "Run collection"
2. Watch tests execute
3. View results

**Step 3:** Add new request

1. Add request to get user profile
2. Add tests to verify response
3. Save to collection

**✏️ Exercise:** Add 3 new requests to the collection with tests

### 🛠️ Hands-On Lab 9.2: Build API Client (120 minutes)

**Challenge:** Extend the Python API client

**Step 1:** Study existing client:

```python
# From tests/api/python_api_examples.py
class TestbookAPI:
    def login(self, email, password):
        response = self.session.post(
            f"{self.base_url}/auth/login",
            json={"email": email, "password": password}
        )
        self.token = response.json()["access_token"]
        return response.json()
```

**Step 2:** Add new methods:

```python
def get_followers(self, username):
    """Get user's followers list."""
    response = self.session.get(
        f"{self.base_url}/users/{username}/followers",
        headers=self._headers()
    )
    response.raise_for_status()
    return response.json()

def get_following(self, username):
    """Get user's following list."""
    # Your code here
    pass
```

**✏️ Exercise:** Add 5 new methods to the API client

### 📝 Section 8 Practice Project

**Project:** Complete API Test Suite

Create `tests/api/test_api_complete.py` using pytest + requests:

**Requirements:**

- Use your extended API client
- Test all major endpoints
- Include authentication
- Test error cases

- 20+ API tests
- Document test scenarios

### 📚 Resources

- Study: `tests/api/python_api_examples.py`
- Study: `tests/api/README.md`
- Run: `python tests/api/python_api_examples.py`

---

## Section 10: Performance Testing

### 🎯 Learning Objectives

- Understand load testing
- Use K6 tool
- Analyze performance metrics
- Identify bottlenecks

### 📖 Theory (30 minutes)

**Types of Performance Testing:**

- **Smoke Test** - Can it handle minimal load?
- **Load Test** - How does it perform under normal load?
- **Stress Test** - When does it break?
- **Spike Test** - How does it handle sudden load?

**Key Metrics:**

- Response time (avg, p95, p99)
- Error rate
- Throughput (requests/second)
- Resource usage

### 🛠️ Hands-On Lab 10.1: Run Load Tests (60 minutes)

**Step 1:** Install K6

```bash
brew install k6  # macOS
# or visit https://k6.io/docs/getting-started/installation/
```

**Step 2:** Run smoke test

```bash
k6 run tests/performance/smoke-test.js
```

**Step 3:** Analyze results

```
✓ health check returns 200
✓ login successful
✓ feed loads successfully

http_req_duration.........: avg=245ms  p(95)=456ms
http_req_failed...........: 0.23%
```

**✏️ Exercise:** Document what each metric means

### 🛠️ Hands-On Lab 10.2: Create Custom Load Test (120 minutes)

**Challenge:** Test a specific scenario

**Create `tests/performance/custom-test.js`:**

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 10,          // 10 virtual users
  duration: '2m',   // Run for 2 minutes
};

export default function() {

  // Your test scenario here
  // 1. Login
  // 2. Create post
  // 3. Get feed
  // 4. Sleep
}
```

**✏️ Exercise:** Complete the test scenario

### 📝 Section 10 Practice Project

**Project:** Performance Baseline Report

**Requirements:**

- Run smoke, load, and stress tests
- Document all metrics
- Identify slowest endpoints
- Suggest improvements
- Create performance requirements document

**Deliverables:**

- Test results (JSON exports)
- Analysis report
- Recommendations

### 📚 Resources

- Study: `tests/performance/*.js`
- Read: `tests/performance/README.md`
- Read: [K6 Documentation](https://k6.io/docs/)

---

## Section 11: Security Testing

### 🎯 Learning Objectives

- Test authentication security
- Test authorization

- Test input validation
- Find common vulnerabilities

### 📖 Theory (30 minutes)

**OWASP Top 10 (Common Vulnerabilities):**

1. Broken Access Control
2. Cryptographic Failures
3. Injection
4. Insecure Design
5. Security Misconfiguration
6. Vulnerable Components
7. Authentication Failures
8. Software/Data Integrity Failures
9. Logging/Monitoring Failures
10. Server-Side Request Forgery

### 🛠️ Hands-On Lab 11.1: Test Authentication (60 minutes)

**Challenge:** Verify auth is properly enforced

**Study example:**

```python
def test_cannot_access_without_auth(api_client):

    """Test protected endpoints require auth."""
    response = api_client.get(f"{BASE_URL}/auth/me")
    assert response.status_code in [401, 403]
```

**✏️ Exercise:** Test 5 protected endpoints without auth

### 🛠️ Hands-On Lab 11.2: Test Authorization (90 minutes)

**Challenge:** Verify users can only access their own data

**Example:**

```python
def test_cannot_edit_others_posts(api_client):
    """Test users can't edit posts they don't own."""
    # Login as user 1
    token1 = api_client.post(...).json()["access_token"]

    # Create post as user 1
    post = api_client.post(..., headers={"Authorization": f"Bearer {token1}"})


    # Login as user 2
    token2 = api_client.post(...).json()["access_token"]

    # Try to edit user 1's post as user 2
    response = api_client.put(
        f"/posts/{post['id']}",
        headers={"Authorization": f"Bearer {token2}"}
    )

    assert response.status_code == 403
```

**✏️ Exercise:** Write 5 authorization tests

### 📝 Section 10 Practice Project

**Project:** Security Audit Report

**Requirements:**

- Run all security tests
- Try manual penetration testing

- Document findings
- Categorize by severity
- Suggest fixes

**Tests to Run:**

- All tests in `tests/security/`
- Manual SQL injection attempts
- Manual XSS attempts
- Token manipulation attempts

### 📚 Resources

- Study: `tests/security/test_security.py`
- Read: `tests/security/README.md`
- Read: [OWASP Top 10](https://owasp.org/www-project-top-ten/)

---

## Section 12: CI/CD & Automation

> **🆕 Complete CI/CD Guide Available!** This section provides an introduction. For comprehensive GitHub Actions workflows, caching strategies, and production-ready CI/CD for both Python and JavaScript, see **🆕 [CI/CD for E2E Testing](CI_CD_E2E_TESTING.md)**.

### 🎯 Learning Objectives

- Understand CI/CD
- Configure GitHub Actions
- Automate test execution (Python & JavaScript)
- Generate test reports
- **🆕 Set up caching, parallelization, and artifacts**
- **🆕 Automate E2E, component, and backend tests**

### 📊 Section 12 Content Overview

| Level | Content | Description |
|-------|---------|-------------|
| **Beginner** | Inline (below) | Basic CI/CD concepts and simple workflow |
| **Production** | **🆕 [CI/CD Guide](CI_CD_E2E_TESTING.md)** | Complete automation for Python & JavaScript |

**💡 Quick Start:**

- Read basics below to understand CI/CD concepts
- Then jump to the **[CI/CD Guide](CI_CD_E2E_TESTING.md)** for production-ready workflows

### 📖 Theory (30 minutes)

**What is CI/CD?**

- **CI (Continuous Integration)** - Auto-test every code change
- **CD (Continuous Deployment)** - Auto-deploy if tests pass

**Why CI/CD?**

- Catch bugs early
- Fast feedback
- Consistent testing
- Professional practice
- **🆕 Run tests in parallel** - Faster results
- **🆕 Capture artifacts** - Screenshots, videos, reports

### 🛠️ Hands-On Lab 12.1: Understand GitHub Actions (60 minutes)

**Step 1:** Study basic workflow structure:

```yaml
# .github/workflows/backend-tests.yml
name: Backend Tests

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: pytest -v
```

**Step 2:** View workflow runs (if using GitHub)

**✏️ Exercise:** Explain what each section does

**🆕 Want Production-Ready Workflows?**

The example above is simplified for learning. For production use, see:

**🆕 [CI/CD for E2E Testing](CI_CD_E2E_TESTING.md)** - Includes:

- ✅ **Python E2E tests** - Full Playwright Python workflow
- ✅ **JavaScript E2E tests** - Full Playwright JavaScript workflow
- ✅ **Component tests** - Vitest with coverage
- ✅ **Backend tests** - pytest with coverage
- ✅ **Caching** - Speed up builds 3-5x
- ✅ **Parallel execution** - Run tests simultaneously
- ✅ **Artifacts** - Screenshots, videos, reports
- ✅ **Multiple browsers** - Chrome, Firefox, WebKit
- ✅ **GitLab CI examples** - Alternative to GitHub Actions

### 🛠️ Hands-On Lab 12.2: Local CI Simulation (90 minutes)

**Challenge:** Run tests like CI does

**Create `run-ci-locally.sh`:**

```bash
#!/bin/bash
echo "🚀 Running CI pipeline locally..."


# Backend tests
echo "📋 Running backend tests..."
cd backend
pytest -v --cov || exit 1

# API tests
echo "📋 Running API tests..."
python ../tests/api/python_api_examples.py || exit 1

# E2E tests (if frontend running)
echo "📋 Running E2E tests..."
cd ../tests
npm test || exit 1


echo "✅ All CI checks passed!"
```

**Run it:**

```bash
chmod +x run-ci-locally.sh
./run-ci-locally.sh
```

**✏️ Exercise:** Add security tests to the CI script

### 📝 Section 12 Practice Project

**Project:** Custom CI/CD Workflow

Create `.github/workflows/my-workflow.yml`:

**Requirements:**

- Run on every push
- Run backend tests
- Run security tests
- Upload coverage
- Fail if coverage < 80%
- Send notification on failure

**🆕 Use the Complete Guide:**

Instead of building from scratch, use the **[CI/CD for E2E Testing](CI_CD_E2E_TESTING.md)** guide which provides:

**Ready-to-use workflows for:**

- ✅ Python E2E tests (Playwright)
- ✅ JavaScript E2E tests (Playwright)
- ✅ Component tests (Vitest)
- ✅ Backend tests (pytest)
- ✅ Complete test suite (all above)

**Advanced features included:**

- Dependency caching
- Parallel test execution (sharding)
- Browser matrix (Chrome, Firefox, WebKit)
- Screenshot/video capture on failure
- Coverage upload to Codecov
- Retry strategies for flaky tests
- Slack/PR comment notifications

**Example from the guide:**

```yaml
# Complete E2E Python workflow with caching
name: E2E Python Tests

jobs:
  e2e-python:
    strategy:
      matrix:
        browser: [chromium, firefox]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          cache: 'pip'  # 3-5x faster builds
      - run: pip install -r tests/e2e-python/requirements.txt
      - run: playwright install --with-deps ${{ matrix.browser }}
      - run: pytest --browser=${{ matrix.browser }}
      - uses: actions/upload-artifact@v3  # Capture failures
        if: failure()
        with:
          name: screenshots
          path: tests/e2e-python/test-results/
```

**See the [CI/CD Guide](CI_CD_E2E_TESTING.md) for complete workflows!**

### 🚀 Production CI/CD Resources

**🆕 [CI/CD for E2E Testing](CI_CD_E2E_TESTING.md)** ⭐ **Start Here!**

- Complete GitHub Actions workflows (copy-paste ready)
- Python E2E automation
- JavaScript E2E automation
- Component test automation
- Backend test automation
- Caching strategies (3-5x speedup)
- Parallel execution patterns
- Artifact management
- GitLab CI examples
- **Time:** 3-4 hours to implement

**Additional Resources:**

- [Playwright CI Documentation](https://playwright.dev/docs/ci)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- Study: `.github/workflows/*.yml` (if available in repo)

### 💡 Pro Tips

**1. Start Simple, Then Optimize:**

```
Basic workflow → Add caching → Add parallel execution → Add artifacts
```

**2. Use the Guide's Templates:**
The CI/CD guide provides tested, production-ready workflows. Don't reinvent the wheel!

**3. Test Locally First:**

```bash
# Simulate CI locally
pytest -v --cov  # Backend
npm test -- --coverage  # Component
pytest tests/e2e-python/ # E2E Python
npx playwright test  # E2E JavaScript
```

**4. Monitor CI Performance:**

- Track build times
- Optimize slow tests
- Use caching effectively
- Consider parallel execution

---

## Section 14: Building Your Own Features

### 🎯 Final Project: Add Feature + Complete Test Suite

**Scenario:** Add "Post Bookmarks" feature to Testbook

**Requirements:**

1. **Backend Implementation:**
   - Add Bookmark model
   - Add bookmark endpoints
   - Add database migration

2. **Backend Tests:**
   - 5+ unit tests
   - 10+ integration tests
   - Database relationship tests
   - 80%+ coverage

3. **E2E Tests:**
   - Test bookmarking a post
   - Test viewing bookmarks
   - Test unbookmarking
   - Cross-browser tested

4. **API Tests:**
   - Postman collection updated
   - Python API client extended
   - 5+ API test scenarios

5. **Security Tests:**
   - Test authorization (only see own bookmarks)
   - Test permission checks

6. **Documentation:**
   - Feature documentation
   - API documentation
   - Test documentation

7. **CI/CD:**
   - All tests pass in CI
   - Coverage maintained

### Self-Assessment Checklist

Use this checklist to evaluate your final project:

**Backend Implementation (Must-Have):**

- [ ] Feature works correctly
- [ ] Follows project patterns
- [ ] Code is well-organized
- [ ] No linter errors

**Backend Tests (Must-Have):**

- [ ] 5+ unit tests written
- [ ] 10+ integration tests written
- [ ] All tests passing
- [ ] 80%+ code coverage

**E2E Tests (Must-Have):**

- [ ] User flows tested end-to-end
- [ ] Tests pass reliably
- [ ] Good test coverage

**Additional Testing (Nice-to-Have):**

- [ ] API tests documented
- [ ] Security/authorization tested
- [ ] Performance considerations

**Professional Practices (Nice-to-Have):**

- [ ] Clear documentation
- [ ] CI/CD pipeline configured
- [ ] Code is maintainable

### Portfolio Documentation

Document your work for future reference:

- Code repository (GitHub/GitLab)
- Video walkthrough or screenshots
- Test execution results
- Coverage reports
- Lessons learned notes

---

## 🎓 Learning Path Completion

### Completion Milestones

Track your progress through this self-paced journey:

**Beginner Milestone:**

- ✅ Complete Sections 1-5
- ✅ Write 20+ passing tests
- ✅ Understand test fundamentals

**Intermediate Milestone:**

- ✅ Complete Sections 6-9
- ✅ Write 50+ passing tests
- ✅ Test multiple layers (unit, integration, E2E)

**Advanced Milestone:**

- ✅ Complete Sections 10-12
- ✅ Write 100+ passing tests
- ✅ Implement CI/CD pipeline

**Professional Milestone:**

- ✅ Complete final project (Section 14)
- ✅ Build feature with full test coverage
- ✅ Portfolio-ready work

**📜 About Certificates:**
This is a self-guided learning resource - there are no certificates or grades. What you'll gain is better: **real skills** you can demonstrate with your GitHub portfolio. Employers care more about "show me your tests" than "show me your certificate."

Plus, you'll have that sense of accomplishment from building something real! 🎮

### Skills Gained

After completing this learning path, you can:

- ✅ Write unit, integration, and E2E tests
- ✅ Use pytest, Playwright, K6 professionally
- ✅ Test APIs with multiple tools
- ✅ Measure and improve code coverage
- ✅ Set up CI/CD pipelines
- ✅ Test for security vulnerabilities
- ✅ Test application performance
- ✅ Follow professional testing practices

### Portfolio Projects

You'll have built:

- 20+ unit tests
- 30+ integration tests
- 15+ E2E tests
- Complete API test suite
- Performance test suite
- CI/CD pipeline
- **Complete feature with full test coverage**

---

## 📚 Additional Resources

### Official Documentation

- [Pytest](https://docs.pytest.org/)
- [Playwright](https://playwright.dev/)
- [K6](https://k6.io/docs/)
- [FastAPI](https://fastapi.tiangolo.com/)

### Testbook Guides

- [RUNNING_TESTS.md](RUNNING_TESTS.md) - Run all tests
- [TESTING_GUIDE.md](TESTING_GUIDE.md) - Comprehensive guide
- [TESTING_PATTERNS.md](TESTING_PATTERNS.md) - Testing patterns
- [TESTING_CHEATSHEET.md](TESTING_CHEATSHEET.md) - Quick reference

### Learning Resources

- [Test Automation University](https://testautomationu.applitools.com/)
- [Playwright YouTube](https://www.youtube.com/@Playwrightdev)
- [K6 Learn](https://k6.io/docs/examples/)

---

## 💬 Getting Help

### Self-Guided Learning Tips

1. **Read documentation** - Check relevant README files
2. **Review examples** - Study working tests in the repo
3. **Run tests** - See what works
4. **Experiment** - Modify and learn by doing
5. **Research** - Search for solutions online
6. **Community** - Join testing communities for support

### Common Questions

**Q: Tests are failing, what do I do?**
A: Read the error message, check the troubleshooting guides, verify backend is running

**Q: How do I know what to test?**
A: Start with happy paths, then edge cases, then error cases

**Q: How much coverage is enough?**
A: Aim for 80% as a minimum, 100% for critical code

**Q: Which testing tool should I use?**
A: Use pytest for backend, Playwright for E2E, both are industry standards

**Q: Can I go at my own pace?**
A: Absolutely! This is self-paced learning. Take as much time as you need.

**Q: Do I need to complete every section?**
A: Focus on sections relevant to your goals. Core sections (1-5) are recommended for everyone.

---

## 🎯 Progress Tracker

Track your learning journey:

### Section-by-Section Checklist

- [ ] Section 1: Explored Testbook, understand testing types
- [ ] Section 2: Run all tests, modify a test
- [ ] Section 3: Write 10+ unit tests
- [ ] Section 4: Write 10+ integration tests
- [ ] Section 5: Test complete database model
- [ ] Section 6: Write component tests with Vitest
- [ ] Section 7: Write first E2E test
- [ ] Section 8: Implement Page Object Model
- [ ] Section 9: Build API test suite
- [ ] Section 10: Run performance tests
- [ ] Section 11: Complete security audit
- [ ] Section 12: Set up CI/CD
- [ ] Section 14: Build your own feature with tests

### Skill Level Milestones

**Beginner (Sections 1-4):**

- Can run existing tests
- Understands test structure
- Can modify simple tests
- Can write basic unit tests

**Intermediate (Sections 5-9):**

- Can write integration tests
- Can test APIs
- Can use fixtures effectively
- Can write E2E tests

**Advanced (Sections 10-12):**

- Can test performance
- Can test security
- Can set up CI/CD
- Can build complete test suites

**Professional (Section 14):**

- Can build features with complete test coverage
- Portfolio demonstrates all skills
- Ready for QA automation roles

---

## 🚀 Quick Start

Ready to begin? Start here:

```bash
# 1. Clone/setup Testbook
git clone https://github.com/upt3mpo/testbook.git
cd testbook

# 2. Start application
./start-dev.sh

# 3. Open course
# Read this file (COURSE_AUTOMATION_TESTING_101.md)

# 4. Start Section 1
# Follow Section 1 instructions above
```

---

**Welcome to Automation Testing 101! Let's build professional testing skills! 🎓🚀**

Next: [Section 1 Lab Instructions](#section-1-introduction-to-testing)
