# Lab 2: Testing Real Functions (JavaScript)

**Estimated Time:** 75 minutes (45 minutes of core steps and a 30 minute accessibility step)<br>
**Difficulty:** Beginner<br>
**Language:** JavaScript<br>
**Prerequisites:** Lab 1 completed

**Need Python instead?** Try [Lab 2: Testing Real Functions (Python)](LAB_02_Testing_Real_Functions_Python.md)!

**What This Adds:** Move from testing simple examples to testing real production code - learn to test actual functions that handle API calls, component interactions, and other critical frontend logic.

---

<h2 id="what-youll-learn">What You'll Learn</h2>

- Test real Testbook frontend functions
- Test utility functions and helpers
- Use Vitest mocking
- Understand test coverage
- Test async functions
- Test a pure function with boundary values, and why that matters for accessibility

---

<h2 id="step-by-step-instructions">Step-by-Step Instructions</h2>

### Step 1: Explore Real Functions (10 minutes)

**Open the file:** `frontend/src/api.js`

**Find these functions:**

```javascript
// Auth API functions
export const authAPI = {
  login: (email, password) => api.post("/auth/login", { email, password }),
  register: (userData) => api.post("/auth/register", userData),
  getMe: () => api.get("/auth/me"),
};
```

**Understand:** These are REAL functions used in Testbook frontend!

**Checkpoint:** You understand what these functions do

### Step 2: Look at Existing Tests (10 minutes)

**Open:** `frontend/src/tests/unit/CreatePost.test.jsx`

**Find this test:**

```javascript
it("calls onPostCreated when post is submitted successfully", async () => {
  // Arrange - Set up mocks and test data
  const mockOnPostCreated = vi.fn();
  const mockPost = { id: 1, content: "Test post", author_id: 1 };
  api.postsAPI.createPost.mockResolvedValueOnce({ data: mockPost });

  renderCreatePost({ onPostCreated: mockOnPostCreated });

  const textarea = screen.getByPlaceholderText("What's on your mind?");
  const postButton = screen.getByRole("button", { name: /post/i });

  // Act - User types and submits post
  fireEvent.change(textarea, { target: { value: "Test post" } });
  fireEvent.click(postButton);

  // Assert - Verify API called and callback triggered
  await waitFor(() => {
    expect(api.postsAPI.createPost).toHaveBeenCalledWith({
      content: "Test post",
      image_url: null,
      video_url: null,
    });
    expect(mockOnPostCreated).toHaveBeenCalledWith(mockPost);
  });
});
```

**Notice:**

- Clear comments (Arrange, Act, Assert)
- Multiple assertions checking different things
- Tests what the function actually does
- Uses `vi.fn()` for mocking

**Checkpoint:** You understand the test structure

### Step 3: Run the Test (5 minutes)

```bash
cd frontend
npm test CreatePost.test.jsx
```

**You should see:**

```text
✓ CreatePost.test.jsx (8)
  ✓ CreatePost Component (8)
    ✓ calls onPostCreated when post is submitted successfully
```

**Try running all component tests:**

```bash
npm test -- --run
```

**Checkpoint:** All component tests pass

### Step 4: Write Your Own API Test (15 minutes)

**Challenge:** Test that API functions handle errors correctly

**Create:** `frontend/src/tests/unit/api.test.js`

```javascript
/**
 * Test file for API functions
 *
 * This file demonstrates how to test real API functions using Vitest.
 * We use mocking to simulate API responses without making real network calls.
 */

import { describe, it, expect, vi, beforeEach } from "vitest";
import axios from "axios";
import { authAPI } from "../../api";

// Mock the axios module so we can control its behavior in tests.
// `api.js` calls axios.create() once, at module load time, so the
// factory below must return a working instance (including
// `interceptors`, which api.js configures immediately) *before*
// api.js's top-level code runs.
vi.mock("axios", () => {
  const mockAxiosInstance = {
    post: vi.fn(),
    get: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
    interceptors: {
      request: { use: vi.fn() },
      response: { use: vi.fn() },
    },
  };
  return {
    default: {
      create: vi.fn(() => mockAxiosInstance),
    },
  };
});

// Grab the same mocked instance that api.js received from axios.create()
const mockAxiosInstance = axios.create();

describe("API Functions", () => {
  // Clear all mocks before each test to ensure clean state
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should handle login API errors", async () => {
    /**
     * Test that API functions properly handle and propagate errors.
     *
     * This test ensures that when the API returns an error,
     * our function correctly throws that error to the caller.
     */

    // Arrange: Mock the axios instance to simulate a failed API call
    const errorMessage = "Invalid credentials";
    mockAxiosInstance.post.mockRejectedValue(new Error(errorMessage));

    // Act & Assert: Verify that the error is properly thrown
    await expect(
      authAPI.login("test@test.com", "wrongpassword")
    ).rejects.toThrow(errorMessage);
  });

  it("should handle successful login", async () => {
    /**
     * Test that API functions return data correctly on success.
     *
     * This test verifies that when the API call succeeds,
     * our function returns the expected data structure.
     */

    // Arrange: Mock the axios instance to simulate a successful API response
    const mockResponse = { data: { access_token: "fake-token" } };
    mockAxiosInstance.post.mockResolvedValue(mockResponse);

    // Act: Call the login function with test credentials
    const result = await authAPI.login("test@test.com", "password");

    // Assert: Verify the function returns the mocked response
    expect(result).toEqual(mockResponse);
  });
});
```

**Run your test:**

```bash
npm test api.test.js
```

**Checkpoint:** Your test passes!

### Step 5: Test Utility Functions (15 minutes)

**Challenge:** Test a utility function

**Create:** `frontend/src/utils/formatDate.js`

```javascript
/**
 * Format a date string for display
 * @param {string} dateString - ISO date string
 * @returns {string} Formatted date
 */
export function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

/**
 * Check if a string is a valid email
 * @param {string} email - Email to validate
 * @returns {boolean} True if valid email
 */
export function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}
```

**Create test:** `frontend/src/tests/unit/utils.test.js`

```javascript
import { describe, it, expect } from "vitest";
import { formatDate, isValidEmail } from "../../utils/formatDate";

describe("Utility Functions", () => {
  describe("formatDate", () => {
    it("should format date correctly", () => {
      // Arrange
      const dateString = "2024-01-15T10:30:00Z";

      // Act
      const result = formatDate(dateString);

      // Assert
      expect(result).toMatch(/Jan 15, 2024/);
    });

    it("should handle invalid date gracefully", () => {
      // Arrange
      const invalidDate = "not-a-date";

      // Act
      const result = formatDate(invalidDate);

      // Assert: Date.toLocaleDateString() does not throw for an invalid
      // date - it returns the literal string "Invalid Date"
      expect(result).toBe("Invalid Date");
    });
  });

  describe("isValidEmail", () => {
    it("should validate correct email", () => {
      // Arrange
      const validEmail = "test@example.com";

      // Act
      const result = isValidEmail(validEmail);

      // Assert
      expect(result).toBe(true);
    });

    it("should reject invalid email", () => {
      // Arrange
      const invalidEmail = "not-an-email";

      // Act
      const result = isValidEmail(invalidEmail);

      // Assert
      expect(result).toBe(false);
    });

    it("should handle edge cases", () => {
      expect(isValidEmail("")).toBe(false);
      expect(isValidEmail("test@")).toBe(false);
      expect(isValidEmail("@example.com")).toBe(false);
      expect(isValidEmail("test@example")).toBe(false);
    });
  });
});
```

**Run it:**

```bash
npm test utils.test.js
```

**Checkpoint:** Your utility tests pass!

---

### Step 6: A function that decides who can read your page (30 minutes)

**Accessibility thread.** Some of the most valuable functions to test are small and pure. One
of them decides whether people with low vision can read your text.

**Why it matters.** The *contrast ratio* between text and its background is a number. WCAG
requires at least **4.5:1** for normal text. Testbook's dark theme once failed this: white text
on the blue button was **3.46:1**, and nobody noticed because nobody had checked dark mode. A
unit test over the numbers would have caught it before a user ever saw it. You can read the
whole story in [Case 5 of the worked examples](../../../docs/a11y/WORKED_EXAMPLES.md).

**Open the function:** `frontend/src/tests/helpers/contrast.js`

```javascript
export function contrastRatio(colourA, colourB) { /* 1 to 21 */ }
export function passesAA(foreground, background, { largeText = false } = {}) { /* true or false */ }
```

Read it. It converts each colour to a *relative luminance* between 0 (black) and 1 (white) using
the formula in the WCAG definition, and returns `(lighter + 0.05) / (darker + 0.05)`. You do
not need to memorise the maths. You need to test that it gives the right answers.

> **Do not open `frontend/src/tests/unit/contrast.test.js` yet.** That is the maintainers'
> version of the tests you are about to write. Compare against it at the end.

**Create your own test file:** `frontend/src/tests/unit/contrast_lab.test.js`

**Start with this and complete it:**

```javascript
import { describe, expect, it } from "vitest";
import { contrastRatio, hexToRgb, passesAA } from "../helpers/contrast.js";

describe("contrastRatio", () => {
  it("is 21:1 for black on white", () => {
    // Arrange / Act / Assert: the WCAG definition says the maximum ratio is 21.
    expect(contrastRatio("#000000", "#ffffff")).toBeCloseTo(21, 5);
  });

  // TODO 1: a colour on itself is 1:1.

  // TODO 2: the answer must not depend on which colour is the foreground.
});
```

**Now write these tests yourself:**

1. **Known values.** Use `it.each` to check these real Testbook colour pairs. Compare with
   `toBeCloseTo(expected, 2)`, never `toBe`: floating-point maths is not exact.

   | Foreground | Background | Expected ratio |
   | --- | --- | --- |
   | `#ffffff` | `#2d88ff` | 3.46 (the dark-theme bug) |
   | `#ffffff` | `#1668d9` | 5.23 (the fix) |
   | `#ffffff` | `#1264d0` | 5.59 |

2. **The boundary.** Boundary values are where bugs live, and this function has a sharp one.
   Check that `#767676` on white **passes** AA and `#777777` on white **fails**. To your eye the
   two greys are identical. Their ratios are 4.54 and 4.48, on either side of 4.5. Also assert
   that the failing ratio is **less than 4.5 but more than 4.4**, to prove it is not being
   rounded: WCAG treats 4.499 as a fail, not as "close enough".

3. **Large text.** Check that the 3.46:1 pair fails for normal text and **passes** with
   `{ largeText: true }`, because large text only needs 3:1.

4. **Bad input.** `hexToRgb` should throw for `""`, `"#12"`, `"blue"` and `null`. Use
   `it.each` with `expect(() => ...).toThrow()`.

**Run your tests:**

```bash
cd frontend
npx vitest --run src/tests/unit/contrast_lab.test.js
```

**Checkpoint:** all your tests pass.

**Now compare** with `frontend/src/tests/unit/contrast.test.js`. Did you cover something it
does not, or miss something it covers?

### Step 7: Watch it guard the real app (10 minutes)

A function test is good. A test that applies the function to **your real design** is better.

**Open:** `frontend/src/tests/accessibility/tokens.test.js` and read the `PAIRS` list. It reads
the colour tokens from `frontend/src/index.css` and checks every text and background pair, in
**both** the light and dark themes, against 4.5:1.

**Run it:**

```bash
npx vitest --run src/tests/accessibility/tokens.test.js
```

**Now break the app on purpose.** In `frontend/src/index.css`, find the dark theme block
(`[data-theme='dark']`) and change this line:

```css
--accent-fill: #1668d9;
```

to the colour the bug used:

```css
--accent-fill: #2d88ff;
```

Run the test again. **It should fail**, with a message like:

```text
#ffffff (#ffffff) on --accent-fill (#2d88ff) is 3.46:1, needs 4.5:1
```

That message names the pair, the colours and the ratio, so the failure tells you exactly what to
fix. **Now undo your change:**

```bash
git checkout src/index.css
```

**Checkpoint:** the test failed with the contrast message, and passes again after you
reverted.

**What you just saw.** This is a *unit test*, layer 4 on the
[prevention ladder](../../stage_0_inclusion_first/README.md#the-prevention-ladder). It runs in
milliseconds, needs no browser, and would have caught a bug that a full browser test missed for
months. Cheap tests that apply a pure function to your real design are some of the best value in
accessibility testing.

<h2 id="what-you-learned">What You Learned</h2>

- How to test real application functions
- How to mock external dependencies with `vi.mock()`
- How to test async functions with `async/await`
- How to test error handling
- How to navigate existing test code
- How to test utility functions

---

## Practice Exercises

Try these on your own:

### Exercise 1: Edge Cases

Test utility functions with:

- Empty strings
- Null/undefined values
- Very long strings
- Special characters

### Exercise 2: Multiple Assertions

Write one test that:

- Tests multiple email formats
- Verifies all valid formats pass
- Verifies all invalid formats fail

### Exercise 3: Explore More

Find and run tests for:

- API functions (`frontend/src/tests/unit/`)
- Component tests (`frontend/src/tests/unit/`)
- Try to understand what each test does

---

<h2 id="troubleshooting">Troubleshooting</h2>

**Problem:** `ModuleNotFoundError: Cannot resolve module`
**Solution:** Make sure you're in the `frontend/` directory and using correct import paths

**Problem:** `Test not found`
**Solution:** Check file name ends with `.test.js` and functions use `it()` or `test()`

**Problem:** `Mock not working`
**Solution:** Make sure to call `vi.clearAllMocks()` in `beforeEach()`

---

<h2 id="lab-completion-checklist">Lab Completion Checklist</h2>

Before moving to Lab 3, ensure you:

- [ ] Successfully ran existing component tests
- [ ] Wrote `api.test.js` and it passes
- [ ] Wrote `utils.test.js` and it passes
- [ ] Understand Arrange-Act-Assert pattern
- [ ] Can explain why testing utility functions matters
- [ ] Wrote `contrast_lab.test.js`, including the `#767676` / `#777777` boundary test, and it passes
- [ ] Watched `tokens.test.js` fail when the dark accent colour was changed, then reverted
- [ ] Can explain why a 4.48:1 pair fails even though it looks the same as a 4.54:1 pair

---

Answer these to solidify your learning:

1. **Why do we test utility functions separately from components?**
2. **What's the difference between `vi.fn()` and `vi.mock()`?**
3. **Why is it important to test error handling?**
4. **How do async tests differ from sync tests?**

---

**Great job! You're testing real frontend code!**

**Next Lab:** [Lab 2.5: Understanding Fixtures (JavaScript)](LAB_03_Fixtures_And_Test_Data_JavaScript.md)
