# 🧪 Lab 3: Fixtures And Test Data (JavaScript)

**Estimated Time:** 45 minutes<br>
**Difficulty:** Intermediate<br>
**Language:** 🟨 JavaScript<br>
**Prerequisites:** Labs 1 & 2 completed

**💡 Need Python instead?** Try [Lab 3: Fixtures And Test Data (Python)](LAB_03_Fixtures_And_Test_Data_Python.md)!

**What This Adds:** Master test data management with Vitest setup patterns - learn to create reusable test setup that eliminates code duplication and makes your tests more maintainable and reliable.

---

## 🎯 What You'll Learn

By the end of this lab, you will:

- Understand what setup/teardown patterns are and why they matter
- Use existing setup patterns in your tests
- Create your own simple setup functions
- Understand different setup scopes (beforeEach, beforeAll, etc.)
- See how setup patterns make tests cleaner and faster

---

## 💡 What Are Setup Patterns?

**Problem:** You need to set up test data repeatedly.

```javascript
describe("User Tests", () => {
  it("should test user email", () => {
    // Setup (repeated in every test)
    const user = { email: "test@test.com", username: "testuser" };
    // Test
    expect(user.email).toBe("test@test.com");
  });

  it("should test user username", () => {
    // Same setup again!
    const user = { email: "test@test.com", username: "testuser" };
    // Test
    expect(user.username).toBe("testuser");
  });
});
```

**Solution:** Setup patterns provide reusable setup.

```javascript
describe("User Tests", () => {
  let user;

  beforeEach(() => {
    // Setup runs before each test
    user = { email: "test@test.com", username: "testuser" };
  });

  it("should test user email", () => {
    expect(user.email).toBe("test@test.com");
  });

  it("should test user username", () => {
    expect(user.username).toBe("testuser");
  });
});
```

**Benefits:**

- ✅ No repeated setup code
- ✅ Consistent test data
- ✅ Automatic cleanup
- ✅ Clear dependencies

---

## 📋 Step-by-Step Instructions

### Step 1: Explore Existing Setup Patterns (10 minutes)

**Open:** `frontend/src/tests/setup.js`

**Find these patterns:**

```javascript
/**
 * Global test setup and teardown configuration
 *
 * This file configures MSW (Mock Service Worker) and React Testing Library
 * to run properly across all tests. These hooks run automatically.
 */

// MSW (Mock Service Worker) Setup
// Start the mock server before all tests run
beforeAll(() => {
  server.listen({
    onUnhandledRequest: "warn", // Warn about unhandled requests (helps catch missing mocks)
  });
});

// Reset MSW handlers after each test to ensure clean state
afterEach(() => {
  server.resetHandlers();
});

// Close the mock server after all tests complete
afterAll(() => {
  server.close();
});

// React Testing Library cleanup
// Clean up DOM after each test to prevent test interference
afterEach(() => {
  cleanup(); // Removes all mounted components from the DOM
});
```

**Key parts:**

1. `beforeAll()` - Runs once before all tests
2. `afterEach()` - Runs after each test
3. `afterAll()` - Runs once after all tests
4. `cleanup()` - Cleans up React components

✅ **Checkpoint:** List 3 setup patterns you found in `setup.js`

---

### Step 2: Use Existing Setup Patterns (10 minutes)

**Create:** `frontend/src/tests/unit/test_learn_setup.js`

```javascript
import {
  describe,
  it,
  expect,
  beforeEach,
  afterEach,
  beforeAll,
  afterAll,
} from "vitest";

describe("Learning Setup Patterns", () => {
  let testData;

  beforeAll(() => {
    console.log("🎯 Running once before all tests");
    testData = { initialized: true };
  });

  beforeEach(() => {
    console.log("🔄 Running before each test");
    testData = {
      initialized: true,
      testCount: (testData.testCount || 0) + 1,
    };
  });

  afterEach(() => {
    console.log("🧹 Running after each test");
    // Cleanup happens here
  });

  afterAll(() => {
    console.log("🏁 Running once after all tests");
  });

  it("should have setup data", () => {
    expect(testData.initialized).toBe(true);
    expect(testData.testCount).toBe(1);
  });

  it("should have fresh data for each test", () => {
    expect(testData.initialized).toBe(true);
    expect(testData.testCount).toBe(2);
  });
});
```

**Run it:**

```bash
cd frontend
npm test test_learn_setup.js
```

✅ **Checkpoint:** All tests should pass and you should see console logs

---

### Step 3: Understanding Setup Flow (10 minutes)

**Let's see what happens step-by-step:**

```javascript
describe("Setup Flow Demo", () => {
  let counter;

  beforeAll(() => {
    console.log("1. beforeAll: Initializing");
    counter = 0;
  });

  beforeEach(() => {
    console.log("2. beforeEach: Setting up test");
    counter += 1;
  });

  it("should demonstrate flow", () => {
    console.log("3. Inside test function");
    console.log(`   Counter value: ${counter}`);
    expect(counter).toBe(1);
  });

  it("should show fresh setup", () => {
    console.log("3. Inside second test");
    console.log(`   Counter value: ${counter}`);
    expect(counter).toBe(2);
  });

  afterEach(() => {
    console.log("4. afterEach: Cleaning up");
  });

  afterAll(() => {
    console.log("5. afterAll: Final cleanup");
  });
});
```

**Run with output visible:**

```bash
npm test test_learn_setup.js -- --reporter=verbose
```

**You'll see:**

```text
1. beforeAll: Initializing
2. beforeEach: Setting up test
3. Inside test function
   Counter value: 1
4. afterEach: Cleaning up
2. beforeEach: Setting up test
3. Inside second test
   Counter value: 2
4. afterEach: Cleaning up
5. afterAll: Final cleanup
```

✅ **Checkpoint:** You can see the setup flow in action

---

### Step 4: Create Your Own Setup Functions (15 minutes)

**Add to the same file:**

```javascript
// Helper function for creating test users
function createTestUser(overrides = {}) {
  return {
    id: 1,
    email: "test@example.com",
    username: "testuser",
    displayName: "Test User",
    ...overrides,
  };
}

// Helper function for creating test posts
function createTestPost(authorId, overrides = {}) {
  return {
    id: Math.random(),
    content: "Test post content",
    authorId,
    createdAt: new Date().toISOString(),
    ...overrides,
  };
}

describe("Custom Setup Functions", () => {
  let user;
  let posts;

  beforeEach(() => {
    // Use our helper functions
    user = createTestUser();
    posts = [
      createTestPost(user.id, { content: "First post" }),
      createTestPost(user.id, { content: "Second post" }),
    ];
  });

  it("should have user with default values", () => {
    expect(user.email).toBe("test@example.com");
    expect(user.username).toBe("testuser");
  });

  it("should have posts for the user", () => {
    expect(posts).toHaveLength(2);
    expect(posts[0].authorId).toBe(user.id);
    expect(posts[1].authorId).toBe(user.id);
  });

  it("should allow custom overrides", () => {
    const customUser = createTestUser({
      email: "custom@test.com",
      username: "customuser",
    });

    expect(customUser.email).toBe("custom@test.com");
    expect(customUser.username).toBe("customuser");
    expect(customUser.id).toBe(1); // Default value preserved
  });
});
```

**Run it:**

```bash
npm test test_learn_setup.js
```

✅ **Checkpoint:** Your custom setup functions work!

---

### Step 5: Advanced Setup Patterns (10 minutes)

**Add this to demonstrate complex setup:**

```javascript
describe("Advanced Setup Patterns", () => {
  let apiMock;
  let testServer;

  beforeAll(async () => {
    // Setup that takes time (like starting a server)
    console.log("🚀 Starting test server...");
    testServer = { running: true };
  });

  beforeEach(() => {
    // Fresh mock for each test
    apiMock = {
      get: vi.fn(),
      post: vi.fn(),
      put: vi.fn(),
      delete: vi.fn(),
    };
  });

  it("should use fresh mock", () => {
    apiMock.get.mockReturnValue({ data: "test" });
    expect(apiMock.get()).toEqual({ data: "test" });
  });

  it("should have fresh mock again", () => {
    // This test gets a fresh mock - no previous calls
    expect(apiMock.get).not.toHaveBeenCalled();
  });

  afterAll(async () => {
    // Cleanup that takes time
    console.log("🛑 Stopping test server...");
    testServer = { running: false };
  });
});
```

**Run it:**

```bash
npm test test_learn_setup.js
```

✅ **Checkpoint:** Advanced setup patterns work

---

## 🎓 Understanding Setup Scopes

Setup patterns can have different scopes:

```javascript
beforeAll(() => {
  // Runs once before all tests in describe block
  console.log("Runs once for all tests");
});

beforeEach(() => {
  // Runs before each test (default)
  console.log("Runs for every test");
});

afterEach(() => {
  // Runs after each test
  console.log("Runs after every test");
});

afterAll(() => {
  // Runs once after all tests in describe block
  console.log("Runs once after all tests");
});
```

**Add this to see scopes in action:**

```javascript
describe("Setup Scope Demo", () => {
  let classCounter = 0;

  beforeAll(() => {
    console.log("\n🎯 Class setup initialized!");
    classCounter = 0;
  });

  it("should increment class counter", () => {
    classCounter += 1;
    console.log(`\n📊 Counter in test 1: ${classCounter}`);
    expect(classCounter).toBe(1);
  });

  it("should increment class counter again", () => {
    classCounter += 1;
    console.log(`\n📊 Counter in test 2: ${classCounter}`);
    // Same counter instance! Counter is 2
    expect(classCounter).toBe(2);
  });

  it("should increment class counter third time", () => {
    classCounter += 1;
    console.log(`\n📊 Counter in test 3: ${classCounter}`);
    // Still same instance! Counter is 3
    expect(classCounter).toBe(3);
  });
});
```

**Run with output:**

```bash
npm test test_learn_setup.js -- --reporter=verbose
```

You'll see the setup initializes once, and all tests share it!

---

## 💪 Your Challenge: User with Posts Setup

**Create a setup function for testing users with posts:**

```javascript
function createUserWithPosts(userOverrides = {}, postCount = 3) {
  const user = createTestUser(userOverrides);
  const posts = [];

  for (let i = 0; i < postCount; i++) {
    posts.push(
      createTestPost(user.id, {
        content: `Post number ${i + 1}`,
        id: i + 1,
      })
    );
  }

  return { user, posts };
}

describe("Your Challenge", () => {
  it("should create user with posts", () => {
    const { user, posts } = createUserWithPosts({ username: "challenge" }, 5);

    expect(user.username).toBe("challenge");
    expect(posts).toHaveLength(5);
    expect(posts[0].authorId).toBe(user.id);
    expect(posts[0].content).toBe("Post number 1");
  });

  it("should create user with custom post count", () => {
    const { user, posts } = createUserWithPosts({}, 10);

    expect(posts).toHaveLength(10);
    expect(posts[9].content).toBe("Post number 10");
  });
});
```

**Hints:**

- Use the existing `createTestUser` and `createTestPost` functions
- Return an object with `{ user, posts }`
- Use a for loop to create multiple posts

---

## 🚨 Common Mistakes

### Mistake 1: Forgetting to Reset State

```javascript
// ❌ BAD - State persists between tests
let counter = 0;

it("should increment", () => {
  counter += 1;
  expect(counter).toBe(1);
});

it("should increment again", () => {
  counter += 1;
  expect(counter).toBe(2); // Depends on previous test!
});

// ✅ GOOD - Fresh state for each test
let counter;

beforeEach(() => {
  counter = 0; // Reset before each test
});
```

### Mistake 2: Using Wrong Scope

```javascript
// ❌ BAD - beforeAll for data that should be fresh
let user;

beforeAll(() => {
  user = createTestUser(); // Same user for all tests!
});

// ✅ GOOD - beforeEach for fresh data
beforeEach(() => {
  user = createTestUser(); // Fresh user for each test
});
```

### Mistake 3: Not Cleaning Up

```javascript
// ❌ BAD - No cleanup
it("should test something", () => {
  const element = document.createElement("div");
  // Element stays in DOM!
});

// ✅ GOOD - Cleanup after test
afterEach(() => {
  document.body.innerHTML = ""; // Clean up DOM
});
```

---

## 📝 Quiz

Test your understanding:

1. **What runs before each test?**

   - A) `beforeAll()`
   - B) `beforeEach()`
   - C) `afterEach()`
   - D) `afterAll()`

2. **What runs once before all tests?**

   - A) `beforeAll()`
   - B) `beforeEach()`
   - C) `afterEach()`
   - D) `afterAll()`

3. **When should you use `beforeEach()` vs `beforeAll()`?**

   - A) `beforeEach()` for fresh data, `beforeAll()` for setup that doesn't change
   - B) `beforeAll()` for fresh data, `beforeEach()` for setup that doesn't change
   - C) They're the same
   - D) Use `beforeEach()` always

4. **What's the main benefit of setup patterns?**

   - A) They make tests faster
   - B) They eliminate repeated setup code
   - C) They make tests more complex
   - D) They're required by Vitest

5. **When does cleanup happen?**
   - A) Never
   - B) In `afterEach()`
   - C) In `beforeEach()`
   - D) Automatically

**Answers:** 1-B, 2-A, 3-A, 4-B, 5-B

---

## ✅ Completion Checklist

- [ ] Ran all test examples successfully
- [ ] Created your own setup functions
- [ ] Completed the challenge (createUserWithPosts)
- [ ] Understand setup scope differences
- [ ] Can explain why setup patterns are useful

---

## 🎯 Key Takeaways

1. **Setup patterns eliminate repeated code** - Write once, use everywhere
2. **Different scopes for different needs** - `beforeEach` for fresh data, `beforeAll` for expensive setup
3. **Setup runs automatically** - Just add them to your describe blocks
4. **Cleanup prevents test interference** - Use `afterEach` for cleanup
5. **Helper functions make tests readable** - Create reusable setup functions

---

**Ready for more?**

- **[LAB_DEBUG_01_Reading_Errors_JavaScript.md](LAB_DEBUG_01_Reading_Errors_JavaScript.md)** - Learn to debug test failures
- **[frontend/src/tests/setup.js](../frontend/src/tests/setup.js)** - Study professional setup patterns
- **[Vitest Setup Documentation](https://vitest.dev/guide/setup.html)** - Deep dive

---

**🎉 Congratulations!** You now understand one of the most powerful features of Vitest!

**Next Lab:** [Lab DEBUG 01: Reading Errors (JavaScript)](LAB_DEBUG_01_Reading_Errors_JavaScript.md)
