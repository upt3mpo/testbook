# 📦 Lab 7: Test Data Management (JavaScript)

**Estimated Time:** 45 minutes<br>
**Difficulty:** Intermediate<br>
**Language:** 🟨 JavaScript<br>
**Prerequisites:** Lab 6 completed

**💡 Need Python instead?** Try [Lab 7: Test Data Management (Python)](LAB_07_Test_Data_Management_Python.md)!

**What This Adds:** Master test data management with builder patterns and factories - learn to create reusable, maintainable test data that eliminates duplication and makes tests more reliable.

---

<h2 id="what-youll-learn">🎯 What You'll Learn</h2>

By the end of this lab, you will:

- Create reusable test data builders
- Use factory patterns for test data
- Manage test data lifecycle
- Avoid test data pollution
- Create realistic test scenarios efficiently

---

## 💡 Why Test Data Management Matters

**The Problem:**

```javascript
// Repeated setup in every test
describe("User Tests", () => {
  it("should test user post 1", () => {
    const user = {
      id: 1,
      email: "test@test.com",
      username: "testuser",
      displayName: "Test User",
    };
    const post = {
      id: 1,
      content: "Test post",
      authorId: user.id,
    };
    // Test code...
  });

  it("should test user post 2", () => {
    // Same setup again!
    const user = {
      id: 1,
      email: "test@test.com",
      username: "testuser",
      displayName: "Test User",
    };
    const post = {
      id: 1,
      content: "Test post",
      authorId: user.id,
    };
    // More duplication...
  });
});
```

**The Solution: Builder Pattern**

```javascript
function createUserWithPosts(numPosts = 3) {
  const user = createTestUser();
  const posts = Array.from({ length: numPosts }, (_, i) =>
    createTestPost(user.id, { content: `Post ${i + 1}` })
  );
  return { user, posts };
}

// Now tests are simple
describe("User Tests", () => {
  it("should test user posts", () => {
    const { user, posts } = createUserWithPosts(5);
    expect(posts).toHaveLength(5);
  });
});
```

---

<h2 id="step-by-step-instructions">📋 Step-by-Step Instructions</h2>

### Step 1: Create a Test Data Builder (15 minutes)

**Create:** `frontend/src/tests/unit/test_data_builders.test.js`

```javascript
/**
 * Test Data Builders and Factories
 *
 * This module provides builder patterns and factory functions for creating
 * test data in a clean, reusable way. This eliminates code duplication
 * and makes tests more maintainable.
 */

import { describe, it, expect } from "vitest";

/**
 * Builder pattern for creating test users with custom data.
 *
 * This class allows you to create user objects with specific attributes
 * using a fluent interface. This makes test data creation more readable
 * and maintainable.
 *
 * Example:
 *   const user = new UserBuilder().withEmail("custom@test.com").withUsername("custom").build();
 */
class UserBuilder {
  constructor() {
    // Initialize with default test user data
    this.email = "testuser@example.com"; // Default email for testing
    this.username = "testuser"; // Default username for testing
    this.displayName = "Test User"; // Default display name
    this.password = "TestPassword123!";
    this.bio = "Test bio";
  }

  withEmail(email) {
    this.email = email;
    return this;
  }

  withUsername(username) {
    this.username = username;
    return this;
  }

  withDisplayName(displayName) {
    this.displayName = displayName;
    return this;
  }

  build() {
    return {
      id: Math.random(),
      email: this.email,
      username: this.username,
      displayName: this.displayName,
      password: this.password,
      bio: this.bio,
      createdAt: new Date().toISOString(),
    };
  }
}

describe("UserBuilder", () => {
  it("should build user with defaults", () => {
    // Act
    const user = new UserBuilder().build();

    // Assert
    expect(user.id).toBeDefined();
    expect(user.email).toBe("testuser@example.com");
    expect(user.username).toBe("testuser");
    expect(user.displayName).toBe("Test User");
  });

  it("should build user with custom values", () => {
    // Act
    const user = new UserBuilder()
      .withEmail("custom@test.com")
      .withUsername("customuser")
      .withDisplayName("Custom Name")
      .build();

    // Assert
    expect(user.email).toBe("custom@test.com");
    expect(user.username).toBe("customuser");
    expect(user.displayName).toBe("Custom Name");
  });

  it("should build multiple different users", () => {
    // Act
    const user1 = new UserBuilder()
      .withEmail("user1@test.com")
      .withUsername("user1")
      .build();

    const user2 = new UserBuilder()
      .withEmail("user2@test.com")
      .withUsername("user2")
      .build();

    // Assert
    expect(user1.id).not.toBe(user2.id);
    expect(user1.email).not.toBe(user2.email);
  });
});
```

**Run it:**

```bash
cd frontend
npm test test_data_builders.test.js
```

✅ **Checkpoint:** All builder tests pass

---

### Step 2: Create a Post Builder (15 minutes)

**Add to the same file:**

```javascript
// Post Builder
class PostBuilder {
  constructor(author) {
    this.authorId = author.id;
    this.content = "Test post content";
    this.imageUrl = null;
    this.videoUrl = null;
  }

  withContent(content) {
    this.content = content;
    return this;
  }

  withImage(imageUrl) {
    this.imageUrl = imageUrl;
    return this;
  }

  withVideo(videoUrl) {
    this.videoUrl = videoUrl;
    return this;
  }

  build() {
    return {
      id: Math.random(),
      authorId: this.authorId,
      content: this.content,
      imageUrl: this.imageUrl,
      videoUrl: this.videoUrl,
      createdAt: new Date().toISOString(),
      reactionCounts: {},
    };
  }
}

describe("PostBuilder", () => {
  it("should build simple post", () => {
    // Arrange
    const user = new UserBuilder().build();

    // Act
    const post = new PostBuilder(user).build();

    // Assert
    expect(post.id).toBeDefined();
    expect(post.authorId).toBe(user.id);
    expect(post.content).toBe("Test post content");
  });

  it("should build post with image", () => {
    // Arrange
    const user = new UserBuilder().build();

    // Act
    const post = new PostBuilder(user)
      .withContent("Check out my image!")
      .withImage("/static/images/test.jpg")
      .build();

    // Assert
    expect(post.imageUrl).toBe("/static/images/test.jpg");
    expect(post.content).toBe("Check out my image!");
  });

  it("should build multiple posts for one user", () => {
    // Arrange
    const user = new UserBuilder().build();

    // Act
    const posts = Array.from({ length: 5 }, (_, i) =>
      new PostBuilder(user).withContent(`Post number ${i + 1}`).build()
    );

    // Assert
    expect(posts).toHaveLength(5);
    expect(posts.every((p) => p.authorId === user.id)).toBe(true);
    expect(posts[0].content).toBe("Post number 1");
    expect(posts[4].content).toBe("Post number 5");
  });
});
```

**Run it:**

```bash
npm test test_data_builders.test.js
```

✅ **Checkpoint:** Post builder tests pass

---

### Step 3: Create Helper Functions (15 minutes)

**Add helper functions:**

```javascript
// Helper functions for creating test scenarios
function createUserWithPosts(numPosts = 3, username = "testuser") {
  const user = new UserBuilder()
    .withUsername(username)
    .withEmail(`${username}@test.com`)
    .build();

  const posts = Array.from({ length: numPosts }, (_, i) =>
    new PostBuilder(user).withContent(`${username}'s post #${i + 1}`).build()
  );

  return { user, posts };
}

function createSocialNetwork() {
  // Create 3 users
  const { user: user1, posts: posts1 } = createUserWithPosts(2, "alice");
  const { user: user2, posts: posts2 } = createUserWithPosts(3, "bob");
  const { user: user3, posts: posts3 } = createUserWithPosts(1, "charlie");

  // Make them follow each other
  user1.following = [user2.id];
  user2.following = [user1.id, user3.id];

  return {
    users: [user1, user2, user3],
    posts: [...posts1, ...posts2, ...posts3],
  };
}

describe("Helper Functions", () => {
  it("should create user with posts", () => {
    // Act
    const { user, posts } = createUserWithPosts(5);

    // Assert
    expect(user.username).toBe("testuser");
    expect(posts).toHaveLength(5);
    expect(posts.every((p) => p.authorId === user.id)).toBe(true);
  });

  it("should create custom user with posts", () => {
    // Act
    const { user, posts } = createUserWithPosts(3, "custom");

    // Assert
    expect(user.username).toBe("custom");
    expect(posts).toHaveLength(3);
    expect(posts[0].content).toContain("custom");
  });

  it("should create social network", () => {
    // Act
    const network = createSocialNetwork();

    // Assert
    expect(network.users).toHaveLength(3);
    expect(network.posts).toHaveLength(6); // 2 + 3 + 1

    const [alice, bob, charlie] = network.users;

    // Check relationships
    expect(alice.following).toContain(bob.id);
    expect(bob.following).toContain(alice.id);
    expect(bob.following).toContain(charlie.id);
  });
});
```

**Run it:**

```bash
npm test test_data_builders.test.js
```

✅ **Checkpoint:** Helper function tests pass

---

### Step 4: Use Builders in Component Tests (15 minutes)

**Create:** `frontend/src/tests/unit/PostList.test.jsx`

```javascript
import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";

// PostList component for testing
function PostList({ posts, onPostClick }) {
  if (posts.length === 0) {
    return <div data-testid="no-posts">No posts available</div>;
  }

  return (
    <div data-testid="post-list">
      {posts.map((post) => (
        <div
          key={post.id}
          data-testid={`post-${post.id}`}
          onClick={() => onPostClick?.(post)}
        >
          <div data-testid="post-content">{post.content}</div>
          <div data-testid="post-author">By: {post.authorId}</div>
        </div>
      ))}
    </div>
  );
}

// Import builders (in real code, these would be in separate files)
class UserBuilder {
  constructor() {
    this.email = "test@example.com";
    this.username = "testuser";
    this.displayName = "Test User";
  }
  withUsername(username) {
    this.username = username;
    return this;
  }
  build() {
    return {
      id: Math.random(),
      username: this.username,
      email: this.email,
      displayName: this.displayName,
    };
  }
}

class PostBuilder {
  constructor(author) {
    this.authorId = author.id;
    this.content = "Test post";
  }
  withContent(content) {
    this.content = content;
    return this;
  }
  build() {
    return {
      id: Math.random(),
      authorId: this.authorId,
      content: this.content,
    };
  }
}

function createUserWithPosts(numPosts = 3) {
  const user = new UserBuilder().build();
  const posts = Array.from({ length: numPosts }, (_, i) =>
    new PostBuilder(user).withContent(`Post ${i + 1}`).build()
  );
  return { user, posts };
}

describe("PostList Component with Builders", () => {
  it("should render posts using builders", () => {
    // Arrange - Use builder to create test data
    const { user, posts } = createUserWithPosts(3);

    // Act
    render(<PostList posts={posts} />);

    // Assert
    expect(screen.getByTestId("post-list")).toBeInTheDocument();
    expect(screen.getAllByTestId(/post-\d+/)).toHaveLength(3);
    expect(screen.getByText("Post 1")).toBeInTheDocument();
    expect(screen.getByText("Post 2")).toBeInTheDocument();
    expect(screen.getByText("Post 3")).toBeInTheDocument();
  });

  it("should handle empty posts list", () => {
    // Arrange
    const posts = [];

    // Act
    render(<PostList posts={posts} />);

    // Assert
    expect(screen.getByTestId("no-posts")).toBeInTheDocument();
    expect(screen.getByText("No posts available")).toBeInTheDocument();
  });

  it("should call onPostClick when post is clicked", () => {
    // Arrange
    const { posts } = createUserWithPosts(2);
    const onPostClick = vi.fn();

    // Act
    render(<PostList posts={posts} onPostClick={onPostClick} />);
    fireEvent.click(screen.getByTestId(`post-${posts[0].id}`));

    // Assert
    expect(onPostClick).toHaveBeenCalledWith(posts[0]);
  });
});
```

**Run it:**

```bash
npm test PostList.test.jsx
```

✅ **Checkpoint:** Component tests with builders pass

---

## 💪 Your Challenge: Comment Builder

**Create a CommentBuilder:**

```javascript
class CommentBuilder {
  constructor(post, author) {
    // TODO: Set defaults
    this.postId = post.id;
    this.authorId = author.id;
    this.content = "Test comment";
  }

  withContent(content) {
    // TODO: Implement
    this.content = content;
    return this;
  }

  build() {
    // TODO: Create and return comment
    return {
      id: Math.random(),
      postId: this.postId,
      authorId: this.authorId,
      content: this.content,
      createdAt: new Date().toISOString(),
    };
  }
}

describe("Your CommentBuilder Challenge", () => {
  it("should build comment", () => {
    // Arrange
    const user = new UserBuilder().build();
    const post = new PostBuilder(user).build();
    const commenter = new UserBuilder()
      .withUsername("commenter")
      .withEmail("commenter@test.com")
      .build();

    // Act
    const comment = new CommentBuilder(post, commenter)
      .withContent("Great post!")
      .build();

    // Assert
    expect(comment.id).toBeDefined();
    expect(comment.postId).toBe(post.id);
    expect(comment.authorId).toBe(commenter.id);
    expect(comment.content).toBe("Great post!");
  });
});
```

**Hints:**

- Follow the same pattern as PostBuilder
- Remember to return `this` for method chaining
- Use `Math.random()` for unique IDs

---

<h2 id="best-practices-for-test-data">🎓 Best Practices for Test Data</h2>

### 1. Make Data Creation Easy

```javascript
// ❌ BAD - Lots of setup in each test
it("should test something", () => {
  const user = { id: 1, email: "test@test.com", username: "test" };
  const post = { id: 1, content: "test", authorId: 1 };
  // 10 more lines...
});

// ✅ GOOD - Simple helper function
it("should test something", () => {
  const { user, posts } = createUserWithPosts(5);
  // Test code
});
```

### 2. Use Meaningful Defaults

```javascript
// ✅ GOOD - Defaults make sense
class UserBuilder {
  constructor() {
    this.email = "test@example.com"; // Valid email
    this.username = "testuser"; // Valid username
    this.password = "ValidPass123!"; // Meets requirements
  }
}
```

### 3. Allow Customization

```javascript
// ✅ GOOD - Easy to customize
const user = new UserBuilder()
  .withEmail("custom@test.com")
  .withUsername("custom")
  .build();
```

### 4. Don't Share Mutable State

```javascript
// ❌ BAD - Global state
let SHARED_USER = null;

it("test 1", () => {
  SHARED_USER = createUser();
  SHARED_USER.username = "changed";
});

it("test 2", () => {
  // SHARED_USER was changed by test 1!
  expect(SHARED_USER.username).toBe("testuser"); // Fails!
});

// ✅ GOOD - Each test gets fresh data
it("test 1", () => {
  const user = createUser();
  user.username = "changed";
});

it("test 2", () => {
  const user = createUser(); // Fresh user
  expect(user.username).toBe("testuser"); // Pass!
});
```

---

<h2 id="when-to-use-each-approach">📊 When to Use Each Approach</h2>

| Approach              | Use When                   | Example                        |
| --------------------- | -------------------------- | ------------------------------ |
| **Builders**          | Need variations of data    | `UserBuilder().withEmail(...)` |
| **Factory Functions** | Creating complex scenarios | `createSocialNetwork()`        |
| **Inline Creation**   | Simple, one-off data       | `const value = 'test'`         |

---

## 🚨 Common Mistakes

### Mistake 1: Creating Too Much Data

```javascript
// ❌ BAD - Creates 1000 users for no reason
it("should test user count", () => {
  const users = Array.from({ length: 1000 }, (_, i) => createUser(`user${i}`));
  // Test only needs a few
});

// ✅ GOOD - Create what you need
it("should test user count", () => {
  const user1 = createUser("user1");
  const user2 = createUser("user2");
  expect(getUserCount()).toBe(2);
});
```

### Mistake 2: Hard-Coding IDs

```javascript
// ❌ BAD - Hard-coded ID
it("should get user", () => {
  const user = getUser(1);
  // User ID 1 might not exist!
});

// ✅ GOOD - Use created user's ID
it("should get user", () => {
  const user = createUser();
  const result = getUser(user.id);
});
```

### Mistake 3: Not Using Builders Consistently

```javascript
// ❌ BAD - Mixing approaches
it("should test user", () => {
  const user = { id: 1, email: "test@test.com" }; // Inline
  const post = new PostBuilder(user).build(); // Builder
});

// ✅ GOOD - Consistent approach
it("should test user", () => {
  const user = new UserBuilder().build();
  const post = new PostBuilder(user).build();
});
```

---

<h2 id="completion-checklist">✅ Completion Checklist</h2>

- [ ] Created UserBuilder and PostBuilder
- [ ] Created helper functions
- [ ] Completed CommentBuilder challenge
- [ ] Understand when to use builders vs inline creation
- [ ] Can create complex test scenarios easily

---

<h2 id="key-takeaways">🎯 Key Takeaways</h2>

1. **Builders make test data easy** - Fluent API with `.with*()` methods
2. **Factory functions create scenarios** - Complex data setups
3. **Clean data = reliable tests** - Fresh data for each test
4. **Don't hardcode data** - Create what you need
5. **Consistency matters** - Use the same approach throughout

---

<h2 id="next-steps">📚 Next Steps</h2>

**Apply your skills:**

- Use builders in your actual tests
- Create builders for other models
- Build complex test scenarios
- Read: [Test Data Patterns Guide](../docs/guides/TEST_DATA_PATTERNS.md) for more patterns

---

**🎉 Congratulations!** You can now manage test data like a professional!

**Next Lab:** [Lab 4B: Advanced E2E Testing (JavaScript)](LAB_04B_Advanced_E2E_JavaScript.md)
