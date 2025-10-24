# 🐛 Lab 4: Debugging and Error Handling

**Estimated Time:** 90 minutes<br>
**Difficulty:** Intermediate<br>
**Language:** 🐍 Python<br>
**Prerequisites:** Lab 3 completed

**💡 Need JavaScript instead?** Try [Lab 4: Debugging and Error Handling (JavaScript)](LAB_04_Debugging_And_Error_Handling_JavaScript.md)!

**What This Adds:** Master the art of debugging test failures - learn to read error messages, identify root causes, and fix broken tests systematically. This skill will save you hours of frustration.

---

## 🎯 What You'll Learn

By the end of this lab, you will:

- Read and understand pytest error messages
- Identify the exact line where tests fail
- Debug and fix broken tests systematically
- Apply debugging strategies to real test failures
- Build confidence in fixing test failures

**Important:** This lab is about **learning to debug**, not avoiding errors. Errors are your friends - they tell you exactly what's wrong!

---

## 📋 Why This Matters

**Reality Check:**

- 80% of your testing time will be debugging
- Error messages tell you EXACTLY what's wrong
- Learning to debug makes you 10x faster
- Professional testers are expert debuggers

**What students say:**

- ❌ "I got an error, I don't know what to do"
- ✅ "The error says X is None on line 45, let me check that"

---

## Part 1: Reading Error Messages (30 minutes)

### Exercise 1: Simple Assertion Error

**Create this test:**

```python
# Create: backend/tests/test_learn_errors.py

def test_simple_math():
    """A test that will fail."""
    result = 2 + 2
    assert result == 5  # Wrong answer!
```

**Run it:**

```bash
cd backend
pytest tests/test_learn_errors.py::test_simple_math -v
```

**You'll see:**

```text
============================ FAILURES =============================
__________________ test_simple_math ___________________

    def test_simple_math():
        """A test that will fail."""
        result = 2 + 2
>       assert result == 5
E       AssertionError: assert 4 == 5

tests/test_learn_errors.py:4: AssertionError
========================= short test summary info =================
FAILED tests/test_learn_errors.py::test_simple_math - AssertionError: assert 4 == 5
```

**Let's break this down:**

```text
>       assert result == 5
```

**Meaning:** The `>` arrow points to the EXACT line that failed

```text
E       AssertionError: assert 4 == 5
```

**Meaning:**

- `E` means "Error"
- `AssertionError` is the error type
- `assert 4 == 5` shows what was asserted
- It's saying: "You said 4 equals 5, but it doesn't!"

---

### Exercise 2: String Comparison Error

**Create this test:**

```python
def test_string_comparison():
    """Practice reading string comparison errors."""
    expected = "Hello World"
    actual = "Hello world"  # Note: lowercase 'w'
    assert expected == actual
```

**Run it and answer:**

1. What was expected?
2. What was actual?
3. What's different between them?

<details>
<summary>Click to see answers</summary>

1. Expected: "Hello World" (capital W)
2. Actual: "Hello world" (lowercase w)
3. The 'W' vs 'w'

**The Error Shows:**

```text
E       AssertionError: assert 'Hello World' == 'Hello world'
E         - Hello world
E         + Hello World
E         ?       ^
```

The `^` points to the exact difference!

</details>

---

### Exercise 3: Type Errors

**Create this test:**

```python
def test_type_mismatch():
    """Practice reading type errors."""
    result = "42"  # String
    assert result == 42  # Integer
```

**Run it and answer:**

1. What types are being compared?
2. Why doesn't Python automatically convert them?

<details>
<summary>Click to see answers</summary>

1. String "42" vs Integer 42
2. Python is strict about types in comparisons

**The Error Shows:**

```text
E       AssertionError: assert '42' == 42
```

The quotes around '42' tell you it's a string!

</details>

---

## Part 2: Fixing Broken Tests (60 minutes)

**The Scenario:** A junior developer wrote these tests, but they all have bugs. Your job: fix them!

### Bug 1: Wrong Expected Value

**The Broken Test:**

```python
"""Tests with bugs to fix."""

import pytest
from auth import get_password_hash, verify_password

@pytest.mark.unit
class TestBrokenTests:
    """Tests that need fixing."""

    def test_password_hash_length(self):
        """Test password hash length."""
        password = "SecurePassword123!"
        hashed = get_password_hash(password)

        # 🐛 BUG: Wrong expected length
        assert len(hashed) > 10
```

**Run it:**

```bash
pytest tests/test_learn_errors.py::TestBrokenTests::test_password_hash_length -v
```

**What happens:**

- Test passes, but it's wrong!
- Bcrypt hashes are always 60 characters
- Test says "length > 10" which is too lenient

**Your Task:**

1. Add a print statement to see actual length
2. Fix the assertion to check for correct length (60)

<details>
<summary>Click to see solution</summary>

```python
def test_password_hash_length(self):
    """Test password hash length."""
    password = "SecurePassword123!"
    hashed = get_password_hash(password)

    # Debug: See actual length
    print(f"Hash length: {len(hashed)}")

    # ✅ FIXED: Bcrypt hashes are exactly 60 characters
    assert len(hashed) == 60
```

**Run with:** `pytest tests/test_learn_errors.py::TestBrokenTests::test_password_hash_length -v -s`

</details>

---

### Bug 2: Using Wrong Fixture

**The Broken Test:**

```python
def test_user_email(self, test_user_2):
    """Test user email."""
    # 🐛 BUG: Checking wrong user's email
    assert test_user_2.email == "testuser@example.com"
```

**Run it:**

```bash
pytest tests/test_learn_errors.py::TestBrokenTests::test_user_email -v
```

**What happens:**

```text
AssertionError: assert 'testuser2@example.com' == 'testuser@example.com'
```

**Your Task:**

1. Read the error - what email does `test_user_2` have?
2. Either use the correct fixture or fix the expected email

<details>
<summary>Click to see solution</summary>

**Solution 1: Use correct fixture**

```python
def test_user_email(self, test_user):
    """Test user email."""
    # ✅ FIXED: Using test_user instead of test_user_2
    assert test_user.email == "testuser@example.com"
```

**Solution 2: Fix expected email**

```python
def test_user_email(self, test_user_2):
    """Test user email."""
    # ✅ FIXED: Checking correct email for test_user_2
    assert test_user_2.email == "testuser2@example.com"
```

</details>

---

### Bug 3: Forgot to Commit Database Changes

**The Broken Test:**

```python
def test_create_user(self, db_session):
    """Test creating a user."""
    from models import User

    user = User(
        email="newuser@test.com",
        username="newuser",
        display_name="New User",
        hashed_password=get_password_hash("password")
    )
    db_session.add(user)
    # 🐛 BUG: Forgot db_session.commit()!

    # Try to query the user
    found_user = db_session.query(User).filter_by(email="newuser@test.com").first()
    assert found_user is not None
    assert found_user.username == "newuser"
```

**Run it:**

```bash
pytest tests/test_learn_errors.py::TestBrokenTests::test_create_user -v
```

**What happens:**

```text
AssertionError: assert None is not None
```

**Your Task:**

1. Why is `found_user` None?
2. What's missing between `add()` and the query?

<details>
<summary>Click to see solution</summary>

```python
def test_create_user(self, db_session):
    """Test creating a user."""
    from models import User

    user = User(
        email="newuser@test.com",
        username="newuser",
        display_name="New User",
        hashed_password=get_password_hash("password")
    )
    db_session.add(user)
    # ✅ FIXED: Added commit
    db_session.commit()
    db_session.refresh(user)  # Also refresh to get ID

    # Now query will work
    found_user = db_session.query(User).filter_by(email="newuser@test.com").first()
    assert found_user is not None
    assert found_user.username == "newuser"
```

**Key Learning:** Always commit after adding to database!

</details>

---

### Bug 4: Wrong API Endpoint

**The Broken Test:**

```python
def test_health_check(self, client):
    """Test health check endpoint."""
    # 🐛 BUG: Wrong endpoint URL
    response = client.get("/health")
    assert response.status_code == 200
```

**Run it:**

```bash
pytest tests/test_learn_errors.py::TestBrokenTests::test_health_check -v
```

**What happens:**

```text
AssertionError: assert 404 == 200
```

**Your Task:**

1. Why did we get 404?
2. Check `main.py` - what's the correct endpoint?
3. Fix the URL

<details>
<summary>Click to see solution</summary>

```python
def test_health_check(self, client):
    """Test health check endpoint."""
    # ✅ FIXED: Correct endpoint is /api/health
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

**Where to check:** Look in `backend/main.py` for the `@app.get()` decorator to find correct endpoints.

</details>

---

### Bug 5: Testing with Wrong Data Type

**The Broken Test:**

```python
def test_login(self, client, test_user):
    """Test login endpoint."""
    response = client.post(
        "/api/auth/login",
        # 🐛 BUG: Sending string instead of JSON
        data="email=testuser@example.com&password=TestPassword123!"
    )
    assert response.status_code == 200
```

**Run it:**

```bash
pytest tests/test_learn_errors.py::TestBrokenTests::test_login -v
```

**What happens:**

```text
AssertionError: assert 422 == 200
```

(422 = Validation Error)

**Your Task:**

1. Why did we get 422?
2. What format does the API expect?
3. Fix the request

<details>
<summary>Click to see solution</summary>

```python
def test_login(self, client, test_user):
    """Test login endpoint."""
    response = client.post(
        "/api/auth/login",
        # ✅ FIXED: Using json parameter instead of data
        json={
            "email": "testuser@example.com",
            "password": "TestPassword123!"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
```

**Key Learning:** FastAPI expects JSON (use `json=`), not form data (use `data=`).

</details>

---

## 💪 Your Challenge: Fix All At Once

**Now that you've seen the patterns, here are 3 more broken tests to fix on your own:**

```python
class TestYourChallenge:
    """Fix these tests without looking at solutions first!"""

    def test_challenge_1(self, client):
        """Challenge: Fix this API test."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "new@test.com",
                "password": "Pass123!"
                # Missing required fields!
            }
        )
        assert response.status_code == 200

    def test_challenge_2(self, test_post):
        """Challenge: Fix this attribute test."""
        # Wrong attribute name
        assert test_post.created_date is not None

    def test_challenge_3(self, db_session, test_user):
        """Challenge: Fix this query test."""
        from models import User

        # Wrong query method
        user = db_session.query(User).get(test_user.email)
        assert user is not None
```

**Hints:**

1. Challenge 1: Check schema requirements in `schemas.py`
2. Challenge 2: Check Post model in `models.py`
3. Challenge 3: `.get()` expects ID, not email

<details>
<summary>Click to see solutions</summary>

```python
class TestYourChallenge:
    """Fixed versions."""

    def test_challenge_1(self, client):
        """Challenge: Fix this API test."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "new@test.com",
                "username": "newuser",  # Added
                "display_name": "New User",  # Added
                "password": "Pass123!"
            }
        )
        assert response.status_code == 200

    def test_challenge_2(self, test_post):
        """Challenge: Fix this attribute test."""
        # Fixed: It's created_at, not created_date
        assert test_post.created_at is not None

    def test_challenge_3(self, db_session, test_user):
        """Challenge: Fix this query test."""
        from models import User

        # Fixed: Use filter_by for non-ID fields
        user = db_session.query(User).filter_by(email=test_user.email).first()
        # Or use .get() with ID:
        # user = db_session.query(User).get(test_user.id)
        assert user is not None
```

</details>

---

## 🎓 Debugging Strategy Checklist

When you encounter a failing test:

1. **Read the error message carefully**

   - [ ] What line failed?
   - [ ] What was expected?
   - [ ] What was actual?

2. **Check the basics**

   - [ ] Are imports correct?
   - [ ] Are variable names spelled right?
   - [ ] Are you using the right fixture?

3. **Verify your assumptions**

   - [ ] Print values to see what you actually have
   - [ ] Check model definitions for correct attributes
   - [ ] Verify API endpoint URLs

4. **Test your fix**
   - [ ] Run the specific test
   - [ ] Make sure it passes for the right reason
   - [ ] Run all tests to ensure no new breaks

---

## 📊 Common Bug Patterns Summary

| Bug Type              | Symptom                | Fix                             |
| --------------------- | ---------------------- | ------------------------------- |
| **Wrong value**       | AssertionError: X == Y | Check expected value            |
| **Missing commit**    | Query returns None     | Add `db_session.commit()`       |
| **Wrong endpoint**    | 404 error              | Check `main.py` for routes      |
| **Wrong data format** | 422 error              | Use `json=` not `data=`         |
| **Missing import**    | NameError              | Add import at top               |
| **Wrong attribute**   | AttributeError         | Check model definition          |
| **Off-by-one**        | Count mismatch         | Verify your counting            |
| **Wrong fixture**     | Wrong data             | Use correct fixture             |
| **Logic error**       | Test fails             | Think about what you're testing |

---

## ✅ Completion Checklist

- [ ] Can identify which line failed in an error message
- [ ] Can tell the difference between expected and actual values
- [ ] Understand what assertion errors mean
- [ ] Can read a stack trace (top to bottom)
- [ ] Know common error types and what they mean
- [ ] Fixed all 5 bugs successfully
- [ ] Completed the 3 challenge bugs
- [ ] Understand each type of error
- [ ] Can explain why each fix works
- [ ] Ran all tests and they pass

---

## 💡 Pro Tips

1. **Read before fixing** - Understand the error first
2. **Fix one at a time** - Don't change multiple things
3. **Verify your fix** - Make sure test passes for right reason
4. **Learn the pattern** - You'll see these errors again
5. **Use print statements** - See what values you actually have

---

## 📚 Next Steps

**Continue building your skills:**

- **[Lab 5: API Endpoint Testing (Python)](LAB_05_API_Endpoint_Testing_Python.md)** - Write more complex tests
- **[Lab 9: Basic E2E Testing (Python)](LAB_09_Basic_E2E_Testing_Python.md)** - Debug browser tests
- **[DEBUGGING_GUIDE.md](../docs/reference/DEBUGGING_GUIDE.md)** - Advanced debugging

---

**🎉 Congratulations!** You're now a debugging expert. These skills will serve you throughout your entire testing career!

**Next Lab:** [Lab 5: API Endpoint Testing (Python)](LAB_05_API_Endpoint_Testing_Python.md)
