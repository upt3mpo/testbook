# 🧪 Stage 1: Unit Tests

**Foundation of Test Automation**

Unit tests are the building blocks of test automation. They're fast, focused, and test individual functions in isolation. Master unit testing, and everything else becomes easier.

---

## 🎯 Learning Goals

By the end of this stage, you will:

- ✅ Understand what unit tests are and why they matter
- ✅ Read and understand existing unit tests
- ✅ Use pytest fixtures for test setup
- ✅ Apply the Arrange-Act-Assert (AAA) pattern
- ✅ Test edge cases and error conditions
- ✅ Mock external dependencies

**Duration:** 2-3 hours

---

## 📂 Where to Look

**Choose your track:** Unit testing works differently for backend vs frontend!

---

### 🐍 Python Track (Backend Focus)

**📁 Folder:** `/backend/tests/unit/`

1. **[`test_auth.py`](../../backend/tests/unit/test_auth.py)**
   - Password hashing and verification
   - JWT token creation and validation
   - Example of testing security functions

2. **[`test_models.py`](../../backend/tests/unit/test_models.py)**
   - Database model behavior
   - Relationships and cascades
   - Example of testing data structures

**Supporting Files:**

- [`backend/tests/conftest.py`](../../backend/tests/conftest.py) - pytest fixtures
- [`backend/tests/README.md`](../../backend/tests/README.md) - Testing docs

**Tools:** pytest, SQLAlchemy, FastAPI TestClient

---

### ☕ JavaScript Track (Frontend Focus)

**📁 Folder:** `/frontend/src/tests/unit/`

1. **[`CreatePost.test.jsx`](../../frontend/src/tests/unit/CreatePost.test.jsx)**
   - React component rendering
   - User interaction testing (typing, clicking)
   - API mocking with Vitest
   - State management validation

2. **[`Navbar.test.jsx`](../../frontend/src/tests/unit/Navbar.test.jsx)**
   - Conditional rendering based on auth state
   - React Context testing
   - Navigation component behavior

**Supporting Files:**

- [`frontend/src/tests/setup.js`](../../frontend/src/tests/setup.js) - Vitest configuration
- [`frontend/src/tests/mocks/`](../../frontend/src/tests/mocks/) - MSW handlers

**Tools:** Vitest, React Testing Library, Mock Service Worker (MSW)

---

### 🔄 Hybrid Track

**Study both!** Most real QA roles test backend AND frontend.

1. Start with Python backend tests (understand API contracts)
2. Then JavaScript frontend tests (see how UI consumes APIs)
3. Notice how they connect (API returns data, UI displays it)

**Time:** 3-4 hours (both tracks)

---

## 🔍 What to Look For

As you read each test file, pay attention to:

### 1. Test Structure (AAA Pattern)

```python
def test_example():
    # Arrange - Set up test data
    value = 42

    # Act - Execute the function being tested
    result = value * 2

    # Assert - Verify the result
    assert result == 84
```

**Find this pattern** in the test files. Can you identify Arrange, Act, and Assert in each test?

### 2. Fixtures

```python
@pytest.fixture
def test_user(db_session):
    user = User(username="testuser")
    db_session.add(user)
    db_session.commit()
    return user
```

**Notice how fixtures:**

- Provide reusable test data
- Keep tests DRY (Don't Repeat Yourself)
- Handle setup AND cleanup automatically

### 3. Test Markers

```python
@pytest.mark.unit
def test_something():
    pass
```

**Markers organize tests** by type, speed, or category. This helps run specific test groups.

### 4. Descriptive Names

```python
def test_password_is_hashed():
    """Verify that passwords are hashed, not stored as plain text."""
    # ...
```

**Good test names** tell you exactly what's being tested. You should be able to understand a test without reading its code.

### 5. Edge Cases

Look for tests that verify:

- ✅ Normal/happy path behavior
- ❌ Error conditions
- 🔄 Boundary conditions
- 🎯 Special cases

---

## 🏃 How to Practice

**Pick your track below:**

---

### 🐍 Python Track Practice

**Step 1: Run the Unit Tests**

```bash
cd backend
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Run all unit tests
pytest -m unit -v

# Run specific test file
pytest tests/unit/test_auth.py -v

# Run entire unit test directory
pytest tests/unit/ -v
```

**Expected output:** All tests should pass (green).

**Step 2: Study a Test**

Open `tests/unit/test_auth.py` and find `test_password_is_hashed`.

**Questions:**

- Can you identify Arrange, Act, Assert?
- Why does bcrypt hash start with "$2b$"?
- What would happen if password hashing was removed?

---

### ☕ JavaScript Track Practice

**Step 1: Run Component Tests**

```bash
cd frontend
npm test

# Run specific test file
npm test -- CreatePost.test.jsx

# Run in watch mode (reruns on changes)
npm test -- --watch
```

**Expected output:** All component tests should pass.

**Step 2: Study a Test**

Open `src/components/__tests__/CreatePost.test.jsx` and find the test for button enabling.

**Questions:**

- How does the test simulate user typing?
- What React state is being tested?
- Why mock the API instead of calling it?

---

### 🔄 Hybrid Track Practice

**Do both tracks!** Understanding both stacks makes you more valuable.

1. Run Python backend unit tests
2. Run JavaScript frontend component tests
3. Compare: How is testing similar? How is it different?
4. Notice: pytest fixtures vs Vitest mocks, database vs React state

---

## ✅ Success Criteria

You're ready for Stage 2 when you can:

**Core concepts (all tracks):**

- [ ] Explain what a unit test is
- [ ] Identify Arrange-Act-Assert in any test
- [ ] Understand what fixtures/mocks do
- [ ] Run unit tests from the command line
- [ ] Read a test and explain what it verifies
- [ ] Make a test fail intentionally and understand the output

**Python Track:**

- [ ] Use pytest fixtures (db_session, test_user)
- [ ] Write a simple pytest unit test from scratch
- [ ] Understand bcrypt password hashing

**JavaScript Track:**

- [ ] Use Vitest and React Testing Library
- [ ] Mock functions with `vi.fn()`
- [ ] Test React component rendering and state

**Hybrid Track:**

- [ ] Can explain how backend unit tests differ from frontend component tests
- [ ] Understand when to use each approach

---

## 🧠 Why This Matters

### In Real QA Teams

- **Unit tests run in seconds** - Developers run them constantly
- **Catch bugs early** - Before code reaches QA or production
- **Document behavior** - Tests show how code should work
- **Enable refactoring** - Change code safely when tests pass

### For Your Career

- **Foundational skill** - All test automation builds on unit testing
- **Interview topic** - You'll be asked to write unit tests
- **Code confidence** - Understanding tests means understanding code
- **Team collaboration** - Speak the same language as developers

---

## 💡 Key Concepts

### Unit Test Characteristics

**FIRST Principles:**

- **F**ast - Runs in milliseconds
- **I**ndependent - Doesn't depend on other tests
- **R**epeatable - Same result every time
- **S**elf-validating - Pass or fail, no manual checking
- **T**imely - Written alongside or before code

### What Makes a Good Unit Test?

✅ Tests one thing
✅ Has a clear name
✅ Follows AAA pattern
✅ Uses fixtures appropriately
✅ Tests edge cases
✅ Fails clearly when broken

❌ Tests multiple things
❌ Has vague names like `test_1`
❌ Mixes setup and assertions
❌ Duplicates setup code
❌ Only tests happy paths
❌ Gives cryptic error messages

---

## 🔗 Related Resources

### Hands-On Practice

- [Lab 1: Your First Test](../../labs/LAB_01_Your_First_Test.md)
- [Lab 2: Testing Real Functions](../../labs/LAB_02_Testing_Real_Functions.md)
- [Lab 2.5: Understanding Fixtures](../../labs/LAB_02.5_Understanding_Fixtures.md)

### Documentation

- [Pytest Documentation](https://docs.pytest.org/)
- [Testing Best Practices](../../docs/guides/TESTING_GUIDE.md)
- [Quick Reference](../../docs/reference/QUICK_REFERENCE_PYTEST.md)

### Code Examples

- [Good Test Examples](../../backend/tests/examples/good_tests.py)
- [Bad Test Examples](../../backend/tests/examples/bad_tests.py)

---

## 🤔 Reflection

Before moving to Stage 2, answer these questions:

1. **What surprised you most about unit tests?**

2. **Why do we use fixtures instead of just creating test data in each test?**

3. **Pick one test from `tests/unit/test_auth.py`. What would happen if you removed the assertion?**

4. **How are unit tests different from just manually testing a function in the Python REPL?**

5. **What's one thing you're still confused about?**

**Document your answers** in [reflection.md](reflection.md) or your own notes.

---

## 🎉 Stage Complete

Once you've met the success criteria and reflected on the questions:

### 👉 [Continue to Stage 2: Integration Tests](../stage_2_integration/README.md)

---

*Pro tip: Come back to this stage after completing later stages. You'll notice things you missed the first time! 🎯*
