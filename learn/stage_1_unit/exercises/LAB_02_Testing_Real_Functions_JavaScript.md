# 🧪 Lab 2: Testing Real Functions (JavaScript)

**Estimated Time:** 45 minutes<br>
**Difficulty:** Beginner<br>
**Language:** 🟨 JavaScript<br>
**Prerequisites:** Lab 1 completed

**💡 Need Python instead?** Try [Lab 2: Testing Real Functions (Python)](LAB_02_Testing_Real_Functions_Python.md)!

**What This Adds:** Move from testing simple examples to testing real production code - learn to test actual functions that handle API calls, component interactions, and other critical frontend logic.

---

<h2 id="what-youll-learn">🎯 What You'll Learn</h2>

- Test real Testbook frontend functions
- Test utility functions and helpers
- Use Vitest mocking
- Understand test coverage
- Test async functions

---

<h2 id="step-by-step-instructions">📋 Step-by-Step Instructions</h2>

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

✅ **Checkpoint:** You understand what these functions do

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

✅ **Checkpoint:** You understand the test structure

### Step 3: Run the Test (5 minutes)

```bash
cd frontend
npm test CreatePost.test.jsx
```

**You should see:**

```text
✓ CreatePost.test.jsx (7)
  ✓ CreatePost Component (7)
    ✓ calls onPostCreated when post is submitted successfully
```

**Try running all component tests:**

```bash
npm test -- --run
```

✅ **Checkpoint:** All component tests pass

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

// Mock the axios module so we can control its behavior in tests
vi.mock("axios");
const mockedAxios = vi.mocked(axios);

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

    // Arrange: Mock axios to simulate a failed API call
    const errorMessage = "Invalid credentials";
    mockedAxios.create.mockReturnValue({
      post: vi.fn().mockRejectedValue(new Error(errorMessage)),
    });

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

    // Arrange: Mock axios to simulate a successful API response
    const mockResponse = { data: { access_token: "fake-token" } };
    mockedAxios.create.mockReturnValue({
      post: vi.fn().mockResolvedValue(mockResponse),
    });

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

✅ **Checkpoint:** Your test passes!

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

    it("should handle invalid date", () => {
      // Arrange
      const invalidDate = "not-a-date";

      // Act & Assert
      expect(() => formatDate(invalidDate)).toThrow();
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

✅ **Checkpoint:** Your utility tests pass!

---

<h2 id="what-you-learned">🎓 What You Learned</h2>

- ✅ How to test real application functions
- ✅ How to mock external dependencies with `vi.mock()`
- ✅ How to test async functions with `async/await`
- ✅ How to test error handling
- ✅ How to navigate existing test code
- ✅ How to test utility functions

---

## 💪 Practice Exercises

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

<h2 id="troubleshooting">🐛 Troubleshooting</h2>

**Problem:** `ModuleNotFoundError: Cannot resolve module`
**Solution:** Make sure you're in the `frontend/` directory and using correct import paths

**Problem:** `Test not found`
**Solution:** Check file name ends with `.test.js` and functions use `it()` or `test()`

**Problem:** `Mock not working`
**Solution:** Make sure to call `vi.clearAllMocks()` in `beforeEach()`

---

<h2 id="lab-completion-checklist">✅ Lab Completion Checklist</h2>

Before moving to Lab 3, ensure you:

- [ ] Successfully ran existing component tests
- [ ] Wrote `api.test.js` and it passes
- [ ] Wrote `utils.test.js` and it passes
- [ ] Understand Arrange-Act-Assert pattern
- [ ] Can explain why testing utility functions matters

---

Answer these to solidify your learning:

1. **Why do we test utility functions separately from components?**
2. **What's the difference between `vi.fn()` and `vi.mock()`?**
3. **Why is it important to test error handling?**
4. **How do async tests differ from sync tests?**

---

**🎉 Great job! You're testing real frontend code!**

**Next Lab:** [Lab 2.5: Understanding Fixtures (JavaScript)](LAB_02.5_Understanding_Fixtures_JavaScript.md)
