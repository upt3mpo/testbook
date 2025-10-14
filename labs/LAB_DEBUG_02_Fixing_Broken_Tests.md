# 🔧 Lab DEBUG-02: Fixing Broken Tests

**Estimated Time:** 60 minutes
**Difficulty:** Intermediate
**Prerequisites:** Labs 1, 2, and DEBUG-01 completed

---

## 🎯 What You'll Learn

By the end of this lab, you will:
- Debug and fix broken tests
- Identify common test failures
- Use error messages to guide fixes
- Apply systematic debugging strategies
- Build confidence in fixing test failures

**The Scenario:** A junior developer wrote these tests, but they all have bugs. Your job: fix them!

---

## 📋 Setup

**Create:** `backend/tests/test_broken.py`

We'll add broken tests one at a time, fix them, then move to the next.

---

## 🐛 Bug 1: Wrong Expected Value

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
cd backend
pytest tests/test_broken.py::TestBrokenTests::test_password_hash_length -v
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

**Run with:** `pytest tests/test_broken.py::TestBrokenTests::test_password_hash_length -v -s`

</details>

---

## 🐛 Bug 2: Using Wrong Fixture

**The Broken Test:**

```python
def test_user_email(self, test_user_2):
    """Test user email."""
    # 🐛 BUG: Checking wrong user's email
    assert test_user_2.email == "testuser@example.com"
```

**Run it:**
```bash
pytest tests/test_broken.py::TestBrokenTests::test_user_email -v
```

**What happens:**
```
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

## 🐛 Bug 3: Forgot to Commit Database Changes

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
pytest tests/test_broken.py::TestBrokenTests::test_create_user -v
```

**What happens:**
```
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

## 🐛 Bug 4: Wrong API Endpoint

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
pytest tests/test_broken.py::TestBrokenTests::test_health_check -v
```

**What happens:**
```
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

## 🐛 Bug 5: Testing with Wrong Data Type

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
pytest tests/test_broken.py::TestBrokenTests::test_login -v
```

**What happens:**
```
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

## 🐛 Bug 6: Incorrect Assertion Logic

**The Broken Test:**

```python
def test_password_not_stored_plaintext(self, test_user):
    """Test that passwords are not stored as plaintext."""
    # 🐛 BUG: Logic is backwards!
    assert test_user.hashed_password == "TestPassword123!"
```

**Run it:**
```bash
pytest tests/test_broken.py::TestBrokenTests::test_password_not_stored_plaintext -v
```

**What happens:**
- Test fails (good!)
- But the assertion logic is backwards
- We WANT them to NOT be equal

**Your Task:**
1. What should we actually be testing?
2. Fix the assertion to test the right thing

<details>
<summary>Click to see solution</summary>

```python
def test_password_not_stored_plaintext(self, test_user):
    """Test that passwords are not stored as plaintext."""
    # ✅ FIXED: Use != to verify password IS NOT stored plaintext
    assert test_user.hashed_password != "TestPassword123!"
    # Additional checks to be thorough
    assert test_user.hashed_password.startswith("$2b$")
    assert len(test_user.hashed_password) == 60
```

**Key Learning:** Think about what you're actually testing. Use `!=` when you want to verify things are different.

</details>

---

## 🐛 Bug 7: Missing Import

**The Broken Test:**

```python
def test_post_creation(self, db_session, test_user):
    """Test creating a post."""
    # 🐛 BUG: Post not imported!
    post = Post(
        author_id=test_user.id,
        content="Test post"
    )
    db_session.add(post)
    db_session.commit()

    assert post.id is not None
```

**Run it:**
```bash
pytest tests/test_broken.py::TestBrokenTests::test_post_creation -v
```

**What happens:**
```
NameError: name 'Post' is not defined
```

**Your Task:**
1. What's missing?
2. Add the import at the top of the file

<details>
<summary>Click to see solution</summary>

**At the top of the file, add:**
```python
from models import User, Post  # Added Post
```

**Then the test works:**
```python
def test_post_creation(self, db_session, test_user):
    """Test creating a post."""
    # ✅ FIXED: Post is now imported
    post = Post(
        author_id=test_user.id,
        content="Test post"
    )
    db_session.add(post)
    db_session.commit()
    db_session.refresh(post)

    assert post.id is not None
    assert post.content == "Test post"
```

</details>

---

## 🐛 Bug 8: Accessing Non-Existent Attribute

**The Broken Test:**

```python
def test_user_full_name(self, test_user):
    """Test user full name."""
    # 🐛 BUG: full_name attribute doesn't exist!
    assert test_user.full_name == "Test User"
```

**Run it:**
```bash
pytest tests/test_broken.py::TestBrokenTests::test_user_full_name -v
```

**What happens:**
```
AttributeError: 'User' object has no attribute 'full_name'
```

**Your Task:**
1. Check `models.py` - what attributes does User have?
2. Use the correct attribute name

<details>
<summary>Click to see solution</summary>

```python
def test_user_full_name(self, test_user):
    """Test user display name."""
    # ✅ FIXED: It's called display_name, not full_name
    assert test_user.display_name == "Test User"
```

**Key Learning:** Check the model definition to see what attributes exist.

</details>

---

## 🐛 Bug 9: Off-by-One Error

**The Broken Test:**

```python
def test_multiple_users(self, db_session):
    """Test creating multiple users."""
    from models import User

    # Create 5 users
    for i in range(5):
        user = User(
            email=f"user{i}@test.com",
            username=f"user{i}",
            display_name=f"User {i}",
            hashed_password=get_password_hash("password")
        )
        db_session.add(user)
    db_session.commit()

    # 🐛 BUG: Wrong count!
    user_count = db_session.query(User).count()
    assert user_count == 6
```

**Run it:**
```bash
pytest tests/test_broken.py::TestBrokenTests::test_multiple_users -v
```

**What happens:**
```
AssertionError: assert 5 == 6
```

**Your Task:**
1. How many users did we create?
2. Why does the test expect 6?
3. Fix the expected count

<details>
<summary>Click to see solution</summary>

```python
def test_multiple_users(self, db_session):
    """Test creating multiple users."""
    from models import User

    # Create 5 users
    for i in range(5):
        user = User(
            email=f"user{i}@test.com",
            username=f"user{i}",
            display_name=f"User {i}",
            hashed_password=get_password_hash("password")
        )
        db_session.add(user)
    db_session.commit()

    # ✅ FIXED: We created 5 users, not 6
    user_count = db_session.query(User).count()
    assert user_count == 5
```

**Key Learning:** Double-check your counting logic. `range(5)` creates 0, 1, 2, 3, 4 (5 items).

</details>

---

## 🐛 Bug 10: Async/Timing Issue (Advanced)

**The Broken Test:**

```python
def test_verify_wrong_password(self):
    """Test that wrong password fails verification."""
    password = "correct_password"
    wrong_password = "wrong_password"

    hashed = get_password_hash(password)

    # 🐛 BUG: Logic error
    assert verify_password(wrong_password, hashed) is True
```

**Run it:**
```bash
pytest tests/test_broken.py::TestBrokenTests::test_verify_wrong_password -v
```

**What happens:**
```
AssertionError: assert False is True
```

**Your Task:**
1. What is the test trying to verify?
2. Should wrong password verification return True or False?
3. Fix the assertion

<details>
<summary>Click to see solution</summary>

```python
def test_verify_wrong_password(self):
    """Test that wrong password fails verification."""
    password = "correct_password"
    wrong_password = "wrong_password"

    hashed = get_password_hash(password)

    # ✅ FIXED: Wrong password should return False
    assert verify_password(wrong_password, hashed) is False
```

**Key Learning:** Think about what behavior you're testing. Wrong password should FAIL (return False).

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

## ✅ Completion Checklist

- [ ] Fixed all 10 bugs successfully
- [ ] Completed the 3 challenge bugs
- [ ] Understand each type of error
- [ ] Can explain why each fix works
- [ ] Ran all tests and they pass

---

## 📊 Common Bug Patterns Summary

| Bug Type | Symptom | Fix |
|----------|---------|-----|
| **Wrong value** | AssertionError: X == Y | Check expected value |
| **Missing commit** | Query returns None | Add `db_session.commit()` |
| **Wrong endpoint** | 404 error | Check `main.py` for routes |
| **Wrong data format** | 422 error | Use `json=` not `data=` |
| **Missing import** | NameError | Add import at top |
| **Wrong attribute** | AttributeError | Check model definition |
| **Off-by-one** | Count mismatch | Verify your counting |
| **Wrong fixture** | Wrong data | Use correct fixture |
| **Logic error** | Test fails | Think about what you're testing |

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
- **[LAB_03_Testing_API_Endpoints.md](LAB_03_Testing_API_Endpoints.md)** - Write more complex tests
- **[LAB_04_E2E_Testing_Python.md](LAB_04_E2E_Testing_Python.md)** or **[LAB_04_E2E_Testing_JavaScript.md](LAB_04_E2E_Testing_JavaScript.md)** - Debug browser tests
- **[DEBUGGING_GUIDE.md](../docs/reference/DEBUGGING_GUIDE.md)** - Advanced debugging

---

**🎉 Congratulations!** You're now a debugging expert. These skills will serve you throughout your entire testing career!

