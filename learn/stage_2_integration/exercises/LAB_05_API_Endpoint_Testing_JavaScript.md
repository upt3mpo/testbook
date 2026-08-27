# 🧪 Lab 5: API Endpoint Testing (JavaScript)

**Estimated Time:** 60 minutes<br>
**Difficulty:** Intermediate<br>
**Language:** 🟨 JavaScript<br>
**Prerequisites:** Labs 1-4 completed

**💡 Need Python instead?** Try [Lab 5: API Endpoint Testing (Python)](LAB_05_API_Endpoint_Testing_Python.md)!

**What This Adds:** Master API testing with MSW and Vitest - learn to test real HTTP endpoints, handle authentication, and verify JSON responses. This is essential for testing frontend-backend integration.

---

<h2 id="what-youll-learn">🎯 What You'll Learn</h2>

- Test real API endpoints with fetch/axios
- Use MSW (Mock Service Worker) for API mocking
- Test authentication flow
- Verify JSON responses
- Use Vitest for API testing

---

<h2 id="step-by-step-instructions">📋 Step-by-Step Instructions</h2>

### Step 1: Understand the API (10 minutes)

**What is an API endpoint?**

- URL that accepts requests: `/api/auth/login`
- Returns data: `{"access_token": "xxx"}`
- Like a function you call over HTTP

**Testbook's Login Endpoint:**

- **URL:** `POST /api/auth/login`
- **Input:** `{"email": "...", "password": "..."}`
- **Output:** `{"access_token": "...", "token_type": "bearer"}`

### Step 2: Look at Existing API Tests (10 minutes)

**Open:** `frontend/src/tests/unit/CreatePost.test.jsx`

**Find this test:**

```javascript
it("calls onPostCreated when post is submitted successfully", async () => {
  /**
   * Test that the CreatePost component properly handles successful post creation.
   *
   * This test verifies the complete post creation flow:
   * 1. User types content in the textarea
   * 2. User clicks the submit button
   * 3. Component calls the API with correct data
   * 4. Component triggers the success callback
   */

  // Arrange - Set up mocks and test data
  const mockOnPostCreated = vi.fn(); // Mock function to track callback calls
  const mockPost = {
    id: 1,
    content: "Test post",
    author_id: 1,
  };

  // Mock the API to return a successful response
  api.postsAPI.createPost.mockResolvedValueOnce({ data: mockPost });

  // Render the component with our mock callback
  renderCreatePost({ onPostCreated: mockOnPostCreated });

  // Get references to the form elements
  const textarea = screen.getByPlaceholderText("What's on your mind?");
  const postButton = screen.getByRole("button", { name: /post/i });

  // Act - Simulate user interaction
  // User types content in the textarea
  fireEvent.change(textarea, { target: { value: "Test post" } });

  // User clicks the submit button
  fireEvent.click(postButton);

  // Assert - Verify API was called correctly and callback was triggered
  await waitFor(() => {
    // Verify the API was called with the expected data structure
    expect(api.postsAPI.createPost).toHaveBeenCalledWith({
      content: "Test post", // User's input
      image_url: null, // No image uploaded
      video_url: null, // No video uploaded
    });

    // Verify the success callback was called with the returned post data
    expect(mockOnPostCreated).toHaveBeenCalledWith(mockPost);
  });
});
```

**Understand:**

- `api.postsAPI.createPost` - API function (mocked)
- `mockResolvedValueOnce()` - Mock successful response
- `toHaveBeenCalledWith()` - Verify API was called correctly
- `waitFor()` - Wait for async operations

✅ **Checkpoint:** You understand the test structure

### Step 3: Run the API Test (5 minutes)

```bash
cd frontend
npm test CreatePost.test.jsx
```

**Should see:**

```text
✓ CreatePost.test.jsx (8)
  ✓ CreatePost Component (8)
    ✓ calls onPostCreated when post is submitted successfully
```

✅ **Checkpoint:** Test passes!

### Step 4: Write Your Own API Test (20 minutes)

**Challenge:** Test that login API handles errors correctly

**Create:** `frontend/src/tests/unit/api_auth.test.js`

```javascript
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

describe("Auth API Tests", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should handle successful login", async () => {
    // Arrange - Mock successful response
    const mockResponse = {
      data: {
        access_token: "fake-token-123",
        token_type: "bearer",
      },
    };

    mockAxiosInstance.post.mockResolvedValue(mockResponse);

    // Act
    const result = await authAPI.login("test@test.com", "password123");

    // Assert
    expect(result).toEqual(mockResponse);
    expect(result.data.access_token).toBe("fake-token-123");
  });

  it("should handle login errors", async () => {
    // Arrange - Mock error response
    const errorMessage = "Invalid credentials";
    mockAxiosInstance.post.mockRejectedValue(new Error(errorMessage));

    // Act & Assert
    await expect(
      authAPI.login("test@test.com", "wrongpassword")
    ).rejects.toThrow(errorMessage);
  });

  it("should call login with correct data", async () => {
    // Arrange
    mockAxiosInstance.post.mockResolvedValue({
      data: { access_token: "token" },
    });

    // Act
    await authAPI.login("user@test.com", "password123");

    // Assert
    expect(mockAxiosInstance.post).toHaveBeenCalledWith("/auth/login", {
      email: "user@test.com",
      password: "password123",
    });
  });
});
```

**Run your test:**

```bash
npm test api_auth.test.js
```

✅ **Checkpoint:** Your test passes!

### Step 5: Test with MSW (Mock Service Worker) (30 minutes)

**MSW is already set up in Testbook! Let's use it.**

**Open:** `frontend/src/tests/mocks/handlers.js`

**Find these handlers:** (Testbook uses MSW v2's `http`/`HttpResponse` API, not the older `rest` API)

```javascript
import { http, HttpResponse } from "msw";

const API_BASE = "http://localhost:8000/api";

export const handlers = [
  // Mock feed endpoint
  http.get(`${API_BASE}/feed`, () => {
    return HttpResponse.json([
      {
        id: 1,
        content: "Mocked post from MSW",
        author: { id: 1, username: "testuser", display_name: "Test User" },
        created_at: new Date().toISOString(),
        reaction_counts: { "👍": 5, "❤️": 2 },
        is_own_post: false,
      },
    ]);
  }),
];
```

**Note:** Testbook's test setup (`frontend/src/tests/setup.js`) already starts a shared MSW server (imported from `frontend/src/tests/mocks/server.js`) before every test file runs, and closes it afterward. Because that server is already running, your own tests should reuse it with `server.use(...)` to add or override handlers for a single test, rather than creating and starting a second `setupServer()` instance (doing so registers two competing interceptors and produces confusing "unhandled request" warnings).

**Create:** `frontend/src/tests/unit/api_msw.test.js`

```javascript
import { describe, it, expect } from "vitest";
import { http, HttpResponse } from "msw";
import { server } from "../mocks/server";
import { authAPI } from "../../api";

describe("API Tests with MSW", () => {
  it("should login successfully with MSW", async () => {
    // Arrange - Override the login handler just for this test
    server.use(
      http.post("/api/auth/login", async ({ request }) => {
        const { email, password } = await request.json();

        if (email === "test@test.com" && password === "password123") {
          return HttpResponse.json({
            access_token: "fake-token-from-msw",
            token_type: "bearer",
          });
        }

        return HttpResponse.json(
          { detail: "Invalid credentials" },
          { status: 401 }
        );
      })
    );

    // Act
    const result = await authAPI.login("test@test.com", "password123");

    // Assert
    expect(result.data.access_token).toBe("fake-token-from-msw");
    expect(result.data.token_type).toBe("bearer");
  });

  it("should handle login failure with MSW", async () => {
    // Arrange - Override with a failure response
    server.use(
      http.post("/api/auth/login", async () => {
        return HttpResponse.json(
          { detail: "Invalid credentials" },
          { status: 401 }
        );
      })
    );

    // Act & Assert
    await expect(
      authAPI.login("wrong@test.com", "wrongpassword")
    ).rejects.toThrow();
  });

  it("should fetch feed data with MSW", async () => {
    // Arrange - Override the feed handler with test-specific data
    server.use(
      http.get("/api/feed", () => {
        return HttpResponse.json([
          {
            id: 1,
            content: "Test post from MSW",
            author: { id: 1, username: "testuser" },
            created_at: new Date().toISOString(),
          },
        ]);
      })
    );

    // Act
    const response = await fetch("/api/feed");
    const data = await response.json();

    // Assert
    expect(data).toHaveLength(1);
    expect(data[0].content).toBe("Test post from MSW");
    expect(data[0].author.username).toBe("testuser");
  });
});
```

**Run it:**

```bash
npm test api_msw.test.js
```

✅ **Checkpoint:** MSW tests pass!

---

<h2 id="what-you-learned">🎓 What You Learned</h2>

- ✅ How to test API endpoints with Vitest
- ✅ How to mock axios with `vi.mock()`
- ✅ How to use MSW for realistic API mocking
- ✅ How to verify API calls and responses
- ✅ How to test both success and failure cases

---

## 💪 Practice Challenges

### Challenge 1: Test Post Creation API

Write a test that:

1. Mocks the post creation API
2. Calls the API with test data
3. Verifies the response structure
4. Tests error handling

### Challenge 2: Test Authentication Flow

Write a test that:

1. Mocks successful login
2. Stores token in localStorage
3. Uses token for authenticated requests
4. Tests token expiration

### Challenge 3: Test API Error Handling

Write a test that:

1. Mocks different HTTP status codes (400, 401, 500)
2. Verifies error messages are handled correctly
3. Tests retry logic

---

<h2 id="common-mistakes">🐛 Common Mistakes</h2>

**Mistake 1:** Not waiting for async operations

```javascript
// ❌ Wrong
it("should call API", () => {
  authAPI.login("test@test.com", "password");
  expect(mockApi).toHaveBeenCalled(); // Fails! API call is async
});

// ✅ Correct
it("should call API", async () => {
  await authAPI.login("test@test.com", "password");
  expect(mockApi).toHaveBeenCalled();
});
```

**Mistake 2:** Not clearing mocks

```javascript
// ❌ Wrong - Mocks persist between tests
describe("API Tests", () => {
  const mockApi = vi.fn();

  it("test 1", () => {
    mockApi();
    expect(mockApi).toHaveBeenCalledTimes(1);
  });

  it("test 2", () => {
    expect(mockApi).toHaveBeenCalledTimes(0); // Fails!
  });
});

// ✅ Correct - Clear mocks between tests
describe("API Tests", () => {
  const mockApi = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("test 1", () => {
    mockApi();
    expect(mockApi).toHaveBeenCalledTimes(1);
  });

  it("test 2", () => {
    expect(mockApi).toHaveBeenCalledTimes(0); // Works!
  });
});
```

**Mistake 3:** Not testing error cases

```javascript
// ❌ Wrong - Only testing happy path
it("should login successfully", async () => {
  mockApi.mockResolvedValue({ data: { token: "abc" } });
  const result = await authAPI.login("test@test.com", "password");
  expect(result.data.token).toBe("abc");
});

// ✅ Correct - Test both success and failure
it("should login successfully", async () => {
  mockApi.mockResolvedValue({ data: { token: "abc" } });
  const result = await authAPI.login("test@test.com", "password");
  expect(result.data.token).toBe("abc");
});

it("should handle login failure", async () => {
  mockApi.mockRejectedValue(new Error("Invalid credentials"));
  await expect(authAPI.login("test@test.com", "wrongpassword")).rejects.toThrow(
    "Invalid credentials"
  );
});
```

---

<h2 id="lab-completion-checklist">✅ Lab Completion Checklist</h2>

- [ ] Ran existing API tests
- [ ] Wrote `api_auth.test.js` and it passes
- [ ] Wrote `api_msw.test.js` and it passes
- [ ] Understand how to mock APIs with Vitest
- [ ] Understand how to use MSW for realistic mocking
- [ ] Completed at least 1 practice challenge

---

<h2 id="quiz">🎯 Quiz</h2>

1. What does `vi.mock('axios')` do?
2. What's the difference between `mockResolvedValue()` and `mockRejectedValue()`?
3. Why use MSW instead of just mocking with Vitest?
4. What does `toHaveBeenCalledWith()` verify?
5. How is API testing different from unit testing?

**Answers:**

1. Mocks the axios module for testing
2. `mockResolvedValue()` mocks success, `mockRejectedValue()` mocks errors
3. MSW intercepts real network requests, making tests more realistic
4. Verifies that a function was called with specific arguments
5. API testing tests network calls, unit testing tests individual functions

---

<h2 id="further-reading">📚 Further Reading</h2>

- [MSW Documentation](https://mswjs.io/docs/)
- [Vitest Mocking Guide](https://vitest.dev/guide/mocking.html)
- Study: `frontend/src/tests/mocks/handlers.js` (MSW handlers)
- Study: `frontend/src/api.js` (API functions)

---

**🎉 You're now testing real APIs like a pro!**

**Next Lab:** [Lab 6: Component Testing (JavaScript)](LAB_06_Component_Testing_JavaScript.md)

---

## 🆚 JavaScript vs Python?

**Both versions of this lab teach the same concepts!**

| Aspect       | JavaScript (this lab)         | Python                           |
| ------------ | ----------------------------- | -------------------------------- |
| **Mocking**  | `vi.mock()` + MSW             | `@patch` decorator + fixtures    |
| **Best For** | Frontend teams, JS developers | Backend teams, Python developers |
| **Features** | Identical                     | Identical                        |
| **Realism**  | MSW intercepts real requests  | TestClient simulates requests    |

**Choose based on your comfort level!** Both are excellent.
