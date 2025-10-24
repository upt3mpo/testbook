# 🧪 Lab 1: Your First Test (JavaScript)

**Estimated Time:** 30 minutes<br>
**Difficulty:** Beginner<br>
**Language:** 🟨 JavaScript<br>
**Prerequisites:** Testbook running, Node.js installed, basic JavaScript knowledge

**💡 Need JavaScript basics?** Try [learn-js.org](https://www.learn-js.org/) for free interactive tutorials!

**💡 Need Python instead?** Try [Lab 1: Your First Test (Python)](LAB_01_Your_First_Test_Python.md)!

**What This Adds:** Your first step into automated testing - learn to write, run, and understand basic tests that catch bugs before they reach production.

---

<h2 id="what-youll-learn">🎯 What You'll Learn</h2>

By the end of this lab, you will:

- Write your first automated test with Vitest
- Run a test and see it pass
- Understand JavaScript test structure
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

### Step 2: Navigate to Frontend (2 minutes)

```bash
cd frontend
```

✅ **Checkpoint:** You should see `package.json` and `src/` folder

### Step 3: Create Your First Test File (5 minutes)

Create a new file: `frontend/src/tests/unit/test_my_first.test.js`

**Copy this code exactly:**

```javascript
/**
 * My first test file!
 *
 * This file demonstrates the basic structure of JavaScript tests using Vitest.
 * The describe() function groups related tests, and it() defines individual test cases.
 * Each test is automatically discovered and run by Vitest.
 */

import { describe, it, expect } from "vitest";

describe("My First Tests", () => {
  // Group all our basic tests together for better organization

  it("should add 2 + 2 equals 4", () => {
    /**
     * Test that basic arithmetic works correctly.
     *
     * This test verifies that JavaScript's addition operator works as expected.
     * It's a simple test to ensure our testing framework is working.
     */

    // Arrange: Set up the values we want to test
    const number1 = 2;
    const number2 = 2;

    // Act: Perform the operation we want to test
    const result = number1 + number2;

    // Assert: Verify the result is what we expect
    expect(result).toBe(4);
  });

  it("should check string length", () => {
    /**
     * Test that we can correctly measure string length.
     *
     * This test verifies that the .length property works correctly with strings.
     * String length is a fundamental operation we'll use in many tests.
     */

    // Arrange: Create a test string with known length
    const text = "Hello";

    // Act: Get the length of the string
    const length = text.length;

    // Assert: Verify the length is correct
    expect(length).toBe(5);
  });

  it("should check array contains item", () => {
    /**
     * Test that we can check if an item exists in an array.
     *
     * This test verifies the toContain() matcher works correctly with arrays.
     * Checking array membership is a common operation in testing.
     */

    // Arrange: Create an array of fruits for testing
    const fruits = ["apple", "banana", "orange"];

    // Act: Check if a specific fruit is in the array
    // (No separate act step needed - the assertion does the checking)

    // Assert: Verify the fruit is found in the array
    expect(fruits).toContain("banana");
  });
});
```

✅ **Checkpoint:** File saved in `frontend/src/tests/unit/test_my_first.test.js`

### Step 4: Run Your First Test (5 minutes)

```bash
npm test test_my_first.test.js
```

**You should see:**

```text
✓ test_my_first.test.js (3)
  ✓ My First Tests (3)
    ✓ should add 2 + 2 equals 4
    ✓ should check string length
    ✓ should check array contains item

Test Files  1 passed (1)
Tests  3 passed (3)
Start at 14:23:15
Duration  42ms
```

🎉 **Congratulations!** You just ran your first automated tests!

✅ **Checkpoint:** All 3 tests show ✓ with green checkmarks

### Step 5: Make a Test Fail (On Purpose!) (5 minutes)

**Change line 6 to:**

```javascript
expect(result).toBe(5); // Wrong answer!
```

**Run again:**

```bash
npm test test_my_first.test.js
```

**You should see:**

```text
✗ test_my_first.test.js (3)
  ✗ My First Tests (1)
    ✗ should add 2 + 2 equals 4

AssertionError: expected 4 to be 5
```

**This is GOOD!** You now see how tests catch errors.

**Fix it back:**

```javascript
expect(result).toBe(4); // Correct answer
```

**Run again - should pass!**

✅ **Checkpoint:** You understand how failing tests help find bugs

### Step 6: Write Your Own Test (10 minutes)

**Add this test to the file:**

```javascript
it("should test my own logic", () => {
  /**
   * Test something I wrote myself!
   *
   * This is your first custom test - you get to decide what to test!
   * This demonstrates how you can test any logic you write.
   */

  // Test your name length - names should not be empty
  const myName = "Your Name";
  expect(myName.length).toBeGreaterThan(0);

  // Test your favorite number - should be positive
  const favoriteNumber = 42;
  expect(favoriteNumber).toBeGreaterThan(0);

  // Test an array you create - verify it has the expected number of items
  const myList = ["item1", "item2", "item3"];
  expect(myList).toHaveLength(3);
});
```

**Customize it:**

- Change "Your Name" to your actual name
- Change favoriteNumber to your favorite number
- Add items to myList

**Run it:**

```bash
npm test test_my_first.test.js
```

✅ **Checkpoint:** Your custom test passes!

---

<h2 id="what-you-learned">🎓 What You Learned</h2>

- ✅ How to run Vitest
- ✅ How to write a test function with `it()`
- ✅ How to use `expect()` statements
- ✅ How failing tests help find bugs
- ✅ How to create your own tests

---

<h2 id="next-steps">🚀 Next Steps</h2>

Now try:

1. Add 2 more test functions to your file
2. Run all your tests: `npm test test_my_first.test.js`
3. Make one test fail on purpose and see the error
4. Fix it and verify it passes

---

## 💡 Key Takeaways

**Test Structure:**

```javascript
describe("Test Suite", () => {
  // Groups related tests
  it("should do something", () => {
    // Individual test
    // Arrange: Set up test data
    const value = 10;

    // Act: Do something
    const result = value * 2;

    // Assert: Check result
    expect(result).toBe(20);
  });
});
```

**Expect Statements:**

- `expect(x).toBe(y)` - x equals y
- `expect(x).not.toBe(y)` - x not equals y
- `expect(x).toBeGreaterThan(y)` - x greater than y
- `expect(array).toContain(item)` - array contains item
- `expect(x).toBeTruthy()` - x is truthy
- `expect(string).toHaveLength(n)` - string has length n

---

<h2 id="challenge">🎯 Challenge</h2>

Can you write a test that:

1. Creates an array of numbers
2. Calculates the sum
3. Asserts the sum is correct

**Hint:**

```javascript
it("should sum numbers", () => {
  /**
   * Test that we can correctly sum an array of numbers.
   *
   * This challenge tests your understanding of:
   * - Creating test data (the numbers array)
   * - Using array methods (reduce())
   * - Writing expectations with the correct expected value
   */

  // Arrange: Create an array of numbers to sum
  const numbers = [1, 2, 3, 4, 5];

  // Act: Calculate the sum using reduce()
  // reduce() starts with 0 and adds each number to the running total
  const total = numbers.reduce((sum, num) => sum + num, 0);

  // Assert: Verify the sum is correct
  // Hint: 1 + 2 + 3 + 4 + 5 = 15
  expect(total).toBe(15);
});
```

---

## 🆚 JavaScript vs Python?

**Both versions of this lab teach the same concepts!**

| Aspect       | JavaScript (this lab)         | Python                           |
| ------------ | ----------------------------- | -------------------------------- |
| **Syntax**   | `describe`/`it` blocks        | `def test_` functions            |
| **Best For** | JS developers, frontend teams | Python developers, backend teams |
| **Features** | Identical                     | Identical                        |
| **Speed**    | Same                          | Same                             |

**Choose based on your comfort level!** Both are excellent.

---

**🎉 Congratulations on completing Lab 1!**

**Next Lab:** [Lab 2: Testing Real Functions (JavaScript)](LAB_02_Testing_Real_Functions_JavaScript.md)
