# 🐛 Lab 4: Debugging and Error Handling

**Estimated Time:** 90 minutes<br>
**Difficulty:** Intermediate<br>
**Language:** 🟨 JavaScript<br>
**Prerequisites:** Lab 3 completed

**💡 Need Python instead?** Try [Lab 4: Debugging and Error Handling (Python)](LAB_04_Debugging_And_Error_Handling_Python.md)!

**What This Adds:** Master the art of debugging test failures - learn to read error messages, identify root causes, and fix broken tests systematically. This skill will save you hours of frustration.

---

## 🎯 What You'll Learn

By the end of this lab, you will:

- Read and understand Vitest error messages
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
- ✅ "The error says X is undefined on line 45, let me check that"

---

## Part 1: Reading Error Messages (30 minutes)

### Exercise 1: Simple Assertion Error

**Create this test:**

```javascript
// Create: frontend/src/tests/unit/test_errors.test.js

import { describe, it, expect } from "vitest";

describe("Error Reading Practice", () => {
  it("should demonstrate basic assertion error", () => {
    const result = 2 + 2;
    expect(result).toBe(5); // This will fail!
  });
});
```

**Run it:**

```bash
cd frontend
npm test test_errors.test.js
```

**You'll see:**

```text
❌ FAIL  test_errors.test.js > Error Reading Practice > should demonstrate basic assertion error
AssertionError: expected 4 to be 5

Expected: 5
Received: 4

  at Object.<anonymous> (test_errors.test.js:5:12)
```

**Let's break this down:**

```text
AssertionError: expected 4 to be 5
```

**Meaning:**

- `AssertionError` is the error type
- `expected 4 to be 5` shows what was expected vs received
- It's saying: "You expected 5 but got 4!"

```text
Expected: 5
Received: 4
```

**Meaning:**

- `Expected: 5` - What you thought it would be
- `Received: 4` - What it actually was

```text
at Object.<anonymous> (test_errors.test.js:5:12)
```

**Meaning:**

- File: `test_errors.test.js`
- Line: `5`
- Column: `12`

---

### Exercise 2: String Comparison Error

**Create this test:**

```javascript
it("should demonstrate string error", () => {
  const expected = "Hello World";
  const actual = "Hello world"; // Note: lowercase 'w'
  expect(expected).toBe(actual);
});
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
AssertionError: expected 'Hello World' to be 'Hello world'

Expected: "Hello world"
Received: "Hello World"
```

The error clearly shows the difference!

</details>

---

### Exercise 3: Type Errors

**Create this test:**

```javascript
it("should demonstrate type error", () => {
  const result = "42"; // String
  expect(result).toBe(42); // Number
});
```

**Run it and answer:**

1. What types are being compared?
2. Why doesn't JavaScript automatically convert them?

<details>
<summary>Click to see answers</summary>

1. String "42" vs Number 42
2. JavaScript is strict about types in comparisons with `toBe()`

**The Error Shows:**

```text
AssertionError: expected '42' to be 42

Expected: 42
Received: "42"
```

The quotes around "42" tell you it's a string!

</details>

---

## Part 2: Fixing Broken Tests (60 minutes)

**The Scenario:** A junior developer wrote these tests, but they all have bugs. Your job: fix them!

### Bug 1: Wrong Expected Value

**The Broken Test:**

```javascript
import { describe, it, expect } from "vitest";

describe("Broken Tests", () => {
  it("should test array length", () => {
    const items = ["apple", "banana", "cherry"];

    // 🐛 BUG: Wrong expected length
    expect(items.length).toBe(2);
  });
});
```

**Run it:**

```bash
npm test test_errors.test.js
```

**What happens:**

```text
AssertionError: expected 3 to be 2
```

**Your Task:**

1. How many items are actually in the array?
2. Fix the expected length

<details>
<summary>Click to see solution</summary>

```javascript
it("should test array length", () => {
  const items = ["apple", "banana", "cherry"];

  // Debug: See actual length
  console.log("Array length:", items.length);

  // ✅ FIXED: Array has 3 items, not 2
  expect(items.length).toBe(3);
});
```

</details>

---

### Bug 2: Wrong Object Property

**The Broken Test:**

```javascript
it("should test user object", () => {
  const user = {
    name: "John Doe",
    email: "john@example.com",
    age: 30,
  };

  // 🐛 BUG: Wrong property name
  expect(user.username).toBe("John Doe");
});
```

**Run it:**

```bash
npm test test_errors.test.js
```

**What happens:**

```text
AssertionError: expected undefined to be 'John Doe'
```

**Your Task:**

1. Why is `user.username` undefined?
2. What's the correct property name?

<details>
<summary>Click to see solution</summary>

```javascript
it("should test user object", () => {
  const user = {
    name: "John Doe",
    email: "john@example.com",
    age: 30,
  };

  // ✅ FIXED: It's 'name', not 'username'
  expect(user.name).toBe("John Doe");
});
```

</details>

---

### Bug 3: Wrong Array Method

**The Broken Test:**

```javascript
it("should test array includes", () => {
  const fruits = ["apple", "banana"];

  // 🐛 BUG: Wrong method
  expect(fruits.includes("orange")).toBe(true);
});
```

**Run it:**

```bash
npm test test_errors.test.js
```

**What happens:**

```text
AssertionError: expected false to be true
```

**Your Task:**

1. Does the array include "orange"?
2. What should the test actually verify?

<details>
<summary>Click to see solution</summary>

```javascript
it("should test array includes", () => {
  const fruits = ["apple", "banana"];

  // ✅ FIXED: Test what's actually in the array
  expect(fruits.includes("apple")).toBe(true);
  expect(fruits.includes("orange")).toBe(false);
});
```

</details>

---

### Bug 4: Wrong Function Call

**The Broken Test:**

```javascript
it("should test string methods", () => {
  const text = "Hello World";

  // 🐛 BUG: Wrong method
  const result = text.toUpperCase();
  expect(result).toBe("hello world");
});
```

**Run it:**

```bash
npm test test_errors.test.js
```

**What happens:**

```text
AssertionError: expected 'HELLO WORLD' to be 'hello world'
```

**Your Task:**

1. What does `toUpperCase()` actually return?
2. What method should you use for lowercase?

<details>
<summary>Click to see solution</summary>

```javascript
it("should test string methods", () => {
  const text = "Hello World";

  // ✅ FIXED: Use toLowerCase() for lowercase
  const result = text.toLowerCase();
  expect(result).toBe("hello world");
});
```

</details>

---

### Bug 5: Async/Await Missing

**The Broken Test:**

```javascript
it("should test async function", () => {
  // 🐛 BUG: Missing await
  const result = fetch("https://api.example.com/data");
  expect(result).toBeDefined();
});
```

**Run it:**

```bash
npm test test_errors.test.js
```

**What happens:**

```text
AssertionError: expected Promise {} to be defined
```

**Your Task:**

1. What type is `result`?
2. How do you handle async functions in tests?

<details>
<summary>Click to see solution</summary>

```javascript
it("should test async function", async () => {
  // ✅ FIXED: Added async/await
  const result = await fetch("https://api.example.com/data");
  expect(result).toBeDefined();
  expect(result.status).toBe(200);
});
```

**Key Learning:** Always use `async` and `await` with async functions!

</details>

---

## 💪 Your Challenge: Fix All At Once

**Now that you've seen the patterns, here are 3 more broken tests to fix on your own:**

```javascript
describe("Your Challenge", () => {
  it("challenge 1: fix this object test", () => {
    const config = {
      apiUrl: "https://api.test.com",
      timeout: 5000,
      retries: 3,
    };

    // Wrong property name
    expect(config.apiEndpoint).toBe("https://api.test.com");
  });

  it("challenge 2: fix this array test", () => {
    const numbers = [1, 2, 3, 4, 5];

    // Wrong array method
    expect(numbers.find((n) => n > 3)).toBe([4, 5]);
  });

  it("challenge 3: fix this string test", () => {
    const message = "Hello, World!";

    // Wrong string method
    const result = message.split(" ");
    expect(result).toBe("Hello");
  });
});
```

**Hints:**

1. Challenge 1: Check the object properties
2. Challenge 2: `find()` returns one item, not an array
3. Challenge 3: `split()` returns an array

<details>
<summary>Click to see solutions</summary>

```javascript
describe("Your Challenge", () => {
  it("challenge 1: fix this object test", () => {
    const config = {
      apiUrl: "https://api.test.com",
      timeout: 5000,
      retries: 3,
    };

    // Fixed: It's apiUrl, not apiEndpoint
    expect(config.apiUrl).toBe("https://api.test.com");
  });

  it("challenge 2: fix this array test", () => {
    const numbers = [1, 2, 3, 4, 5];

    // Fixed: find() returns one item, filter() returns array
    expect(numbers.filter((n) => n > 3)).toEqual([4, 5]);
  });

  it("challenge 3: fix this string test", () => {
    const message = "Hello, World!";

    // Fixed: split() returns array, check first element
    const result = message.split(" ");
    expect(result[0]).toBe("Hello");
  });
});
```

</details>

---

## 🎓 Debugging Strategy Checklist

When you encounter a failing test:

1. **Read the error message carefully**

   - [ ] What line failed?
   - [ ] What was expected?
   - [ ] What was received?

2. **Check the basics**

   - [ ] Are imports correct?
   - [ ] Are variable names spelled right?
   - [ ] Are you using the right method?

3. **Verify your assumptions**

   - [ ] Console.log values to see what you actually have
   - [ ] Check object properties and array contents
   - [ ] Verify function return types

4. **Test your fix**
   - [ ] Run the specific test
   - [ ] Make sure it passes for the right reason
   - [ ] Run all tests to ensure no new breaks

---

## 📊 Common Bug Patterns Summary

| Bug Type             | Symptom                   | Fix                                |
| -------------------- | ------------------------- | ---------------------------------- |
| **Wrong value**      | AssertionError: X to be Y | Check expected value               |
| **Wrong property**   | undefined to be X         | Check object property names        |
| **Wrong method**     | Wrong return type         | Use correct array/string method    |
| **Missing async**    | Promise {} to be X        | Add async/await                    |
| **Wrong comparison** | Array to be value         | Use toEqual() for arrays           |
| **Type mismatch**    | String to be Number       | Convert types or use right matcher |

---

## ✅ Completion Checklist

- [ ] Can identify which line failed in an error message
- [ ] Can tell the difference between expected and received values
- [ ] Understand what assertion errors mean
- [ ] Can read Vitest error messages
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
5. **Use console.log** - See what values you actually have

---

## 📚 Next Steps

**Continue building your skills:**

- **[Lab 5: API Endpoint Testing (JavaScript)](LAB_05_API_Endpoint_Testing_JavaScript.md)** - Write more complex tests
- **[Lab 9: Basic E2E Testing (JavaScript)](LAB_09_Basic_E2E_Testing_JavaScript.md)** - Debug browser tests
- **[DEBUGGING_GUIDE.md](../docs/reference/DEBUGGING_GUIDE.md)** - Advanced debugging

---

**🎉 Congratulations!** You're now a debugging expert. These skills will serve you throughout your entire testing career!

**Next Lab:** [Lab 5: API Endpoint Testing (JavaScript)](LAB_05_API_Endpoint_Testing_JavaScript.md)
