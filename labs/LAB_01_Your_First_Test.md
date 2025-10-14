# 🧪 Lab 1: Your First Test

**Estimated Time:** 30 minutes
**Difficulty:** Beginner
**Prerequisites:** Testbook running

---

## 🎯 What You'll Learn

By the end of this lab, you will:
- Write your first automated test
- Run a test and see it pass
- Understand test structure
- Feel confident with testing basics

---

## 📋 Step-by-Step Instructions

### Step 1: Open Your Terminal (2 minutes)

**macOS/Linux:**
- Open Terminal app
- Navigate to Testbook: `cd /path/to/Testbook`

**Windows:**
- Open Command Prompt or PowerShell
- Navigate to Testbook: `cd C:\path\to\Testbook`

✅ **Checkpoint:** Run `ls` (or `dir` on Windows) and see `backend/` and `frontend/` folders

### Step 2: Activate Python Environment (2 minutes)

```bash
cd backend
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows
```

✅ **Checkpoint:** Your terminal prompt should now show `(venv)`

### Step 3: Create Your First Test File (5 minutes)

Create a new file: `backend/tests/test_my_first.py`

**Copy this code exactly:**
```python
"""My first test file!"""

def test_basic_math():
    """Test that 2 + 2 equals 4."""
    result = 2 + 2
    assert result == 4


def test_string_length():
    """Test string length."""
    text = "Hello"
    assert len(text) == 5


def test_list_contains():
    """Test list contains item."""
    fruits = ["apple", "banana", "orange"]
    assert "banana" in fruits
```

✅ **Checkpoint:** File saved in `backend/tests/test_my_first.py`

### Step 4: Run Your First Test (5 minutes)

```bash
pytest tests/test_my_first.py -v
```

**You should see:**
```
tests/test_my_first.py::test_basic_math PASSED ✓
tests/test_my_first.py::test_string_length PASSED ✓
tests/test_my_first.py::test_list_contains PASSED ✓

====================== 3 passed in 0.05s =======================
```

🎉 **Congratulations!** You just ran your first automated tests!

✅ **Checkpoint:** All 3 tests show PASSED with green checkmarks

### Step 5: Make a Test Fail (On Purpose!) (5 minutes)

**Change line 7 to:**
```python
assert result == 5  # Wrong answer!
```

**Run again:**
```bash
pytest tests/test_my_first.py -v
```

**You should see:**
```
tests/test_my_first.py::test_basic_math FAILED ✗

E   assert 4 == 5
```

**This is GOOD!** You now see how tests catch errors.

**Fix it back:**
```python
assert result == 4  # Correct answer
```

**Run again - should pass!**

✅ **Checkpoint:** You understand how failing tests help find bugs

### Step 6: Write Your Own Test (10 minutes)

**Add this function to the file:**
```python
def test_my_own_test():
    """Test something I wrote myself!"""
    # Test your name length
    my_name = "Your Name"
    assert len(my_name) > 0

    # Test your favorite number
    favorite_number = 42
    assert favorite_number > 0

    # Test a list you create
    my_list = ["item1", "item2", "item3"]
    assert len(my_list) == 3
```

**Customize it:**
- Change "Your Name" to your actual name
- Change favorite_number to your favorite number
- Add items to my_list

**Run it:**
```bash
pytest tests/test_my_first.py::test_my_own_test -v
```

✅ **Checkpoint:** Your custom test passes!

---

## 🎓 What You Learned

- ✅ How to run pytest
- ✅ How to write a test function
- ✅ How to use `assert` statements
- ✅ How failing tests help find bugs
- ✅ How to create your own tests

---

## 🚀 Next Steps

Now try:
1. Add 2 more test functions to your file
2. Run all your tests: `pytest tests/test_my_first.py`
3. Make one test fail on purpose and see the error
4. Fix it and verify it passes

---

## 💡 Key Takeaways

**Test Structure:**
```python
def test_something():           # Function starts with "test_"
    """What this test does."""  # Docstring explains it

    # Arrange: Set up test data
    value = 10

    # Act: Do something
    result = value * 2

    # Assert: Check result
    assert result == 20
```

**Assert Statements:**
- `assert x == y` - x equals y
- `assert x != y` - x not equals y
- `assert x > y` - x greater than y
- `assert x in list` - x is in list
- `assert x is True` - x is True

---

## 🎯 Challenge

Can you write a test that:
1. Creates a list of numbers
2. Calculates the sum
3. Asserts the sum is correct

**Hint:**
```python
def test_sum_numbers():
    numbers = [1, 2, 3, 4, 5]
    total = sum(numbers)
    assert total == ???  # You fill this in!
```

---

**🎉 Congratulations on completing Lab 1!**

**Next Lab:** [Lab 2: Testing Real Functions](LAB_02_Testing_Real_Functions.md)

