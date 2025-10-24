# 🧪 Lab 1: Your First Test

**Estimated Time:** 30 minutes<br>
**Difficulty:** Beginner<br>
**Language:** 🐍 Python<br>
**Prerequisites:** Testbook running, Python installed, basic Python knowledge

**💡 Need Python basics?** Try [learnpython.org](https://www.learnpython.org/) for free interactive tutorials!

**💡 Need JavaScript instead?** Try [Lab 1: Your First Test (JavaScript)](LAB_01_Your_First_Test_JavaScript.md)!

**What This Adds:** Your first step into automated testing - learn to write, run, and understand basic tests that catch bugs before they reach production.

---

<h2 id="what-youll-learn">🎯 What You'll Learn</h2>

By the end of this lab, you will:

- Write your first automated test
- Run a test and see it pass
- Understand test structure
- Feel confident with testing basics

---

<h2 id="step-by-step-instructions">📋 Step-by-Step Instructions</h2>

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
# Linux/Mac
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\activate
```

✅ **Checkpoint:** Your terminal prompt should now show `(venv)`

### Step 3: Create Your First Test File (5 minutes)

Create a new file: `backend/tests/test_my_first.py`

**Copy this code exactly:**

```python
"""
My first test file!

This file demonstrates the basic structure of Python tests using pytest.
Each function that starts with 'test_' is automatically discovered and run by pytest.
"""

def test_basic_math():
    """
    Test that basic arithmetic works correctly.

    This test verifies that Python's addition operator works as expected.
    It's a simple test to ensure our testing framework is working.
    """
    # Arrange: Set up the values we want to test
    number1 = 2
    number2 = 2

    # Act: Perform the operation we want to test
    result = number1 + number2

    # Assert: Verify the result is what we expect
    assert result == 4, f"Expected 2 + 2 to equal 4, but got {result}"


def test_string_length():
    """
    Test that we can correctly measure string length.

    This test verifies that the len() function works correctly with strings.
    String length is a fundamental operation we'll use in many tests.
    """
    # Arrange: Create a test string with known length
    text = "Hello"

    # Act: Get the length of the string
    length = len(text)

    # Assert: Verify the length is correct
    assert length == 5, f"Expected 'Hello' to have length 5, but got {length}"


def test_list_contains():
    """
    Test that we can check if an item exists in a list.

    This test verifies the 'in' operator works correctly with lists.
    Checking list membership is a common operation in testing.
    """
    # Arrange: Create a list of fruits for testing
    fruits = ["apple", "banana", "orange"]

    # Act: Check if a specific fruit is in the list
    # (No separate act step needed - the assertion does the checking)

    # Assert: Verify the fruit is found in the list
    assert "banana" in fruits, "Expected 'banana' to be in the fruits list"
```

✅ **Checkpoint:** File saved in `backend/tests/test_my_first.py`

### Step 4: Run Your First Test (5 minutes)

```bash
pytest tests/test_my_first.py -v
```

**You should see:**

```text
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

```text
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
    """
    Test something I wrote myself!

    This is your first custom test - you get to decide what to test!
    This demonstrates how you can test any logic you write.
    """
    # Test your name length - names should not be empty
    my_name = "Your Name"
    assert len(my_name) > 0, "Name should not be empty"

    # Test your favorite number - should be positive
    favorite_number = 42
    assert favorite_number > 0, "Favorite number should be positive"

    # Test a list you create - verify it has the expected number of items
    my_list = ["item1", "item2", "item3"]
    assert len(my_list) == 3, f"Expected list to have 3 items, but got {len(my_list)}"
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

<h2 id="what-you-learned">🎓 What You Learned</h2>

- ✅ How to run pytest
- ✅ How to write a test function
- ✅ How to use `assert` statements
- ✅ How failing tests help find bugs
- ✅ How to create your own tests

---

<h2 id="next-steps">🚀 Next Steps</h2>

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

<h2 id="challenge">🎯 Challenge</h2>

Can you write a test that:

1. Creates a list of numbers
2. Calculates the sum
3. Asserts the sum is correct

**Hint:**

```python
def test_sum_numbers():
    """
    Test that we can correctly sum a list of numbers.

    This challenge tests your understanding of:
    - Creating test data (the numbers list)
    - Using built-in functions (sum())
    - Writing assertions with the correct expected value
    """
    # Arrange: Create a list of numbers to sum
    numbers = [1, 2, 3, 4, 5]

    # Act: Calculate the sum of all numbers
    total = sum(numbers)

    # Assert: Verify the sum is correct
    # Hint: 1 + 2 + 3 + 4 + 5 = 15
    assert total == 15, f"Expected sum to be 15, but got {total}"
```

---

**🎉 Congratulations on completing Lab 1!**

**Next Lab:** [Lab 2: Testing Real Functions (Python)](LAB_02_Testing_Real_Functions_Python.md)
