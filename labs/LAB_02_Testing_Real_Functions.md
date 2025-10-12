# 🧪 Lab 2: Testing Real Functions

**Estimated Time:** 45 minutes
**Difficulty:** Beginner
**Prerequisites:** Lab 1 completed

---

## 🎯 What You'll Learn

- Test real Testbook functions
- Test password hashing
- Test authentication
- Use pytest fixtures
- Understand test coverage

---

## 📋 Step-by-Step Instructions

### Step 1: Explore Real Functions (10 minutes)

**Open the file:** `backend/auth.py`

**Find these functions:**
```python
def get_password_hash(password):
    """Hash a password for storing."""
    # Uses bcrypt to securely hash passwords

def verify_password(plain_password, hashed_password):
    """Verify a password against a hash."""
    # Checks if password matches the hash
```

**Understand:** These are REAL functions used in Testbook!

✅ **Checkpoint:** You understand what these functions do

### Step 2: Look at Existing Tests (10 minutes)

**Open:** `backend/tests/test_unit_auth.py`

**Find this test:**
```python
def test_password_is_hashed(self):
    """Test that password hashing produces a different string."""
    # Arrange
    password = "TestPassword123!"

    # Act
    hashed = get_password_hash(password)

    # Assert
    assert hashed != password
    assert len(hashed) > len(password)
    assert hashed.startswith("$2b$")  # bcrypt format
```

**Notice:**
- Clear comments (Arrange, Act, Assert)
- Multiple assertions checking different things
- Tests what the function actually does

✅ **Checkpoint:** You understand the test structure

### Step 3: Run the Test (5 minutes)

```bash
cd backend
pytest tests/test_unit_auth.py::TestPasswordHashing::test_password_is_hashed -v
```

**You should see:**
```
tests/test_unit_auth.py::TestPasswordHashing::test_password_is_hashed PASSED ✓
```

**Try running all password tests:**
```bash
pytest tests/test_unit_auth.py::TestPasswordHashing -v
```

✅ **Checkpoint:** All password hashing tests pass

### Step 4: Write Your Own Password Test (15 minutes)

**Challenge:** Test that the same password produces different hashes

**Why?** Bcrypt uses a "salt" so the same password hashes differently each time (more secure!)

**Add this test to `test_unit_auth.py` in the `TestPasswordHashing` class:**

```python
def test_same_password_different_hashes(self):
    """Test that hashing the same password twice gives different results."""
    # Arrange
    password = "MyPassword123!"

    # Act
    hash1 = get_password_hash(password)
    hash2 = get_password_hash(password)

    # Assert
    assert hash1 != hash2  # Different hashes!
    # But both should verify correctly
    assert verify_password(password, hash1) is True
    assert verify_password(password, hash2) is True
```

**Run your test:**
```bash
pytest tests/test_unit_auth.py::TestPasswordHashing::test_same_password_different_hashes -v
```

✅ **Checkpoint:** Your test passes!

### Step 5: Test Password Verification (15 minutes)

**Challenge:** Test that wrong passwords are rejected

**Add this test:**
```python
def test_wrong_password_fails(self):
    """Test that wrong password doesn't verify."""
    # Arrange
    correct_password = "CorrectPassword123!"
    wrong_password = "WrongPassword456!"
    hashed = get_password_hash(correct_password)

    # Act & Assert
    assert verify_password(correct_password, hashed) is True
    assert verify_password(wrong_password, hashed) is False
```

**Run it:**
```bash
pytest tests/test_unit_auth.py::TestPasswordHashing::test_wrong_password_fails -v
```

✅ **Checkpoint:** Test passes and verifies security works!

---

## 🎓 What You Learned

- ✅ How to test real application functions
- ✅ How password hashing works
- ✅ Why security testing matters
- ✅ How to write tests that verify security
- ✅ How to navigate existing test code

---

## 💪 Practice Exercises

Try these on your own:

### Exercise 1: Edge Cases
Test password hashing with:
- Empty string
- Very long password (1000 characters)
- Password with special characters: `!@#$%^&*()`
- Unicode password: `密码123`

### Exercise 2: Multiple Assertions
Write one test that:
- Hashes a password
- Verifies hash is different than password
- Verifies hash length > 50 characters
- Verifies hash starts with "$2b$"
- Verifies the password verifies correctly

### Exercise 3: Explore More
Find and run tests for:
- JWT tokens (`test_unit_auth.py`)
- User models (`test_unit_models.py`)
- Try to understand what each test does

---

## 🐛 Troubleshooting

**Problem:** `ModuleNotFoundError: No module named 'auth'`
**Solution:** Make sure you're in the `backend/` directory and venv is activated

**Problem:** `Test not found`
**Solution:** Check file name starts with `test_` and function starts with `test_`

**Problem:** `Import errors`
**Solution:** Run `pip install -r requirements.txt`

---

## ✅ Lab Completion Checklist

Before moving to Lab 3, ensure you:
- [ ] Successfully ran existing password tests
- [ ] Wrote `test_same_password_different_hashes` and it passes
- [ ] Wrote `test_wrong_password_fails` and it passes
- [ ] Understand Arrange-Act-Assert pattern
- [ ] Can explain why password hashing matters

---

## 📝 Reflection Questions

Answer these to solidify your learning:

1. **Why do we hash passwords instead of storing them plainly?**
2. **Why does the same password produce different hashes?**
3. **What would happen if password verification was broken?**
4. **Why is it important to test security functions?**

---

**🎉 Great job! You're testing real security code!**

**Next Lab:** [Lab 3: Testing API Endpoints](labs/LAB_03_Testing_API_Endpoints.md)

