# 📦 Lab 7: Test Data Management (Python)

**Estimated Time:** 45 minutes
**Difficulty:** Intermediate
**Language:** 🐍 Python
**Prerequisites:** Labs 1-6 completed

**💡 Need JavaScript instead?** Try [Lab 7: Test Data Management (JavaScript)](LAB_07_Test_Data_Management_JavaScript.md)!

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

```python
# Repeated setup in every test
def test_user_post_1():
    user = User(email="test@test.com", username="test"...)
    db.add(user)
    db.commit()
    post = Post(author_id=user.id, content="test")
    db.add(post)
    db.commit()
    # Test code...

def test_user_post_2():
    # Same setup again!
    user = User(email="test@test.com", username="test"...)
    db.add(user)
    db.commit()
    post = Post(author_id=user.id, content="test")
    # More duplication...
```

**The Solution: Builder Pattern**

```python
def create_user_with_posts(db, num_posts=3):
    """Reusable function to create test data."""
    user = User(email="test@test.com", username="test"...)
    db.add(user)
    db.commit()

    posts = [Post(author_id=user.id, content=f"Post {i}")
             for i in range(num_posts)]
    for post in posts:
        db.add(post)
    db.commit()

    return user, posts

# Now tests are simple
def test_user_posts():
    user, posts = create_user_with_posts(db, num_posts=5)
    assert len(posts) == 5
```

---

<h2 id="step-by-step-instructions">📋 Step-by-Step Instructions</h2>

### Step 1: Create a Test Data Builder (15 minutes)

**Create:** `backend/tests/test_data_builders.py`

````python
"""
Test Data Builders and Factories

This module provides builder patterns and factory functions for creating
test data in a clean, reusable way. This eliminates code duplication
and makes tests more maintainable.
"""

import pytest
from models import User, Post, Comment
from auth import get_password_hash

class UserBuilder:
```python
"""
Builder pattern for creating test users with custom data.

    This class allows you to create user objects with specific attributes
    using a fluent interface. This makes test data creation more readable
    and maintainable.

    Example:
        user = UserBuilder().with_email("custom@test.com").with_username("custom").build()
    """
    def __init__(self):
        """Initialize with default test user data."""
        self.email = "testuser@example.com"      # Default email for testing
        self.username = "testuser"               # Default username for testing
        self.display_name = "Test User"          # Default display name
        self.password = "TestPassword123!"       # Default password (will be hashed)
        self.bio = "Test bio"                    # Default bio text

    def with_email(self, email):
        """
        Set a custom email for the test user.

        Args:
            email (str): The email address to use

        Returns:
            UserBuilder: Self for method chaining
        """
        self.email = email
        return self

    def with_username(self, username):
        """Set custom username."""
        self.username = username
        return self

    def with_display_name(self, display_name):
        """Set custom display name."""
        self.display_name = display_name
        return self

    def build(self, db_session):
        """Create and save the user."""
        user = User(
            email=self.email,
            username=self.username,
            display_name=self.display_name,
            hashed_password=get_password_hash(self.password),
            bio=self.bio
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user

```python
@pytest.mark.unit
class TestUserBuilder:
    """Test the UserBuilder."""
    def test_build_default_user(self, db_session):
        """Test building user with defaults."""
        user = UserBuilder().build(db_session)

        assert user.id is not None
        assert user.email == "testuser@example.com"
        assert user.username == "testuser"

    def test_build_custom_user(self, db_session):
        """Test building user with custom values."""
        user = (UserBuilder()
                .with_email("custom@test.com")
                .with_username("customuser")
                .with_display_name("Custom Name")
                .build(db_session))

        assert user.email == "custom@test.com"
        assert user.username == "customuser"
        assert user.display_name == "Custom Name"

    def test_build_multiple_users(self, db_session):
        """Test building multiple different users."""
        user1 = (UserBuilder()
                 .with_email("user1@test.com")
                 .with_username("user1")
                 .build(db_session))

        user2 = (UserBuilder()
                 .with_email("user2@test.com")
                 .with_username("user2")
                 .build(db_session))

        assert user1.id != user2.id
        assert user1.email != user2.email

````

**Run it:**

```bash
cd backend
pytest tests/test_data_builders.py::TestUserBuilder -v
```

✅ **Checkpoint:** All builder tests pass

---

### Step 2: Create a Post Builder (15 minutes)

**Add to the same file:**

```python
class PostBuilder:
    """Builder for creating test posts."""

    def __init__(self, author):
        self.author_id = author.id
        self.content = "Test post content"
        self.image_url = None
        self.video_url = None

    def with_content(self, content):
        """Set custom content."""
        self.content = content
        return self

    def with_image(self, image_url):
        """Add image to post."""
        self.image_url = image_url
        return self

    def with_video(self, video_url):
        """Add video to post."""
        self.video_url = video_url
        return self

    def build(self, db_session):
        """Create and save the post."""
        post = Post(
            author_id=self.author_id,
            content=self.content,
            image_url=self.image_url,
            video_url=self.video_url
        )
        db_session.add(post)
        db_session.commit()
        db_session.refresh(post)
        return post


class TestPostBuilder:
    """Test the PostBuilder."""

    def test_build_simple_post(self, db_session):
        """Test building a simple text post."""
        user = UserBuilder().build(db_session)
        post = PostBuilder(user).build(db_session)

        assert post.id is not None
        assert post.author_id == user.id
        assert post.content == "Test post content"

    def test_build_post_with_image(self, db_session):
        """Test building post with image."""
        user = UserBuilder().build(db_session)
        post = (PostBuilder(user)
                .with_content("Check out my image!")
                .with_image("/static/images/test.jpg")
                .build(db_session))

        assert post.image_url == "/static/images/test.jpg"
        assert post.content == "Check out my image!"

    def test_build_multiple_posts(self, db_session):
        """Test building multiple posts for one user."""
        user = UserBuilder().build(db_session)

        posts = []
        for i in range(5):
            post = (PostBuilder(user)
                    .with_content(f"Post number {i}")
                    .build(db_session))
            posts.append(post)

        assert len(posts) == 5
        assert all(p.author_id == user.id for p in posts)
        assert posts[0].content == "Post number 0"
        assert posts[4].content == "Post number 4"
```

**Run it:**

```bash
pytest tests/test_data_builders.py::TestPostBuilder -v
```

✅ **Checkpoint:** Post builder tests pass

---

### Step 3: Create a Complete Scenario Builder (15 minutes)

**Add helper functions:**

```python
def create_user_with_posts(db_session, num_posts=3, username="testuser"):
    """Create a user with multiple posts."""
    user = (UserBuilder()
            .with_username(username)
            .with_email(f"{username}@test.com")
            .build(db_session))

    posts = []
    for i in range(num_posts):
        post = (PostBuilder(user)
                .with_content(f"{username}'s post #{i+1}")
                .build(db_session))
        posts.append(post)

    return user, posts


def create_social_network(db_session):
    """Create a small social network for testing.

    Returns:
        dict with 'users' and 'posts' keys
    """
    # Create 3 users
    user1, posts1 = create_user_with_posts(db_session, num_posts=2, username="alice")
    user2, posts2 = create_user_with_posts(db_session, num_posts=3, username="bob")
    user3, posts3 = create_user_with_posts(db_session, num_posts=1, username="charlie")

    # Make them follow each other
    user1.following.append(user2)
    user2.following.append(user1)
    user2.following.append(user3)
    db_session.commit()

    return {
        "users": [user1, user2, user3],
        "posts": posts1 + posts2 + posts3
    }


class TestScenarioBuilders:
    """Test complete scenario builders."""

    def test_user_with_posts(self, db_session):
        """Test creating user with posts."""
        user, posts = create_user_with_posts(db_session, num_posts=5)

        assert user.username == "testuser"
        assert len(posts) == 5
        assert all(p.author_id == user.id for p in posts)

    def test_custom_user_with_posts(self, db_session):
        """Test creating custom user with posts."""
        user, posts = create_user_with_posts(
            db_session,
            num_posts=3,
            username="custom"
        )

        assert user.username == "custom"
        assert len(posts) == 3
        assert "custom" in posts[0].content

    def test_social_network(self, db_session):
        """Test creating a complete social network."""
        network = create_social_network(db_session)

        assert len(network["users"]) == 3
        assert len(network["posts"]) == 6  # 2 + 3 + 1

        alice, bob, charlie = network["users"]

        # Check relationships
        assert bob in alice.following
        assert alice in bob.following
        assert charlie in bob.following
```

**Run it:**

```bash
pytest tests/test_data_builders.py::TestScenarioBuilders -v
```

✅ **Checkpoint:** Scenario tests pass

---

## 💪 Your Challenge: Comment Builder

**Create a CommentBuilder:**

```python
class CommentBuilder:
    """Builder for creating test comments.

    TODO: Implement this builder
    """

    def __init__(self, post, author):
        # TODO: Set defaults
        pass

    def with_content(self, content):
        # TODO: Implement
        pass

    def build(self, db_session):
        # TODO: Create and return comment
        pass


class TestYourCommentBuilder:
    """Test your CommentBuilder."""

    def test_build_comment(self, db_session):
        """Test building a comment."""
        user = UserBuilder().build(db_session)
        post = PostBuilder(user).build(db_session)

        commenter = (UserBuilder()
                     .with_username("commenter")
                     .with_email("commenter@test.com")
                     .build(db_session))

        comment = (CommentBuilder(post, commenter)
                   .with_content("Great post!")
                   .build(db_session))

        assert comment.id is not None
        assert comment.post_id == post.id
        assert comment.author_id == commenter.id
        assert comment.content == "Great post!"
```

**Hints:**

- Look at `models.py` to see Comment fields
- Follow the same pattern as PostBuilder
- Remember to commit and refresh

<details>
<summary>Click to see solution</summary>

```python
class CommentBuilder:
    """Builder for creating test comments."""

    def __init__(self, post, author):
        self.post_id = post.id
        self.author_id = author.id
        self.content = "Test comment"

    def with_content(self, content):
        """Set custom content."""
        self.content = content
        return self

    def build(self, db_session):
        """Create and save the comment."""
        comment = Comment(
            post_id=self.post_id,
            author_id=self.author_id,
            content=self.content
        )
        db_session.add(comment)
        db_session.commit()
        db_session.refresh(comment)
        return comment
```

</details>

---

<h2 id="best-practices-for-test-data">🎓 Best Practices for Test Data</h2>

### 1. Make Data Creation Easy

```python
# ❌ BAD - Lots of setup in each test
def test_something():
    user = User(...)
    db.add(user)
    db.commit()
    post = Post(...)
    db.add(post)
    # 10 more lines...

# ✅ GOOD - Simple helper function
def test_something():
    user, posts = create_user_with_posts(db, num_posts=5)
    # Test code
```

### 2. Use Meaningful Defaults

```python
# ✅ GOOD - Defaults make sense
class UserBuilder:
    def __init__(self):
        self.email = "test@example.com"  # Valid email
        self.username = "testuser"  # Valid username
        self.password = "ValidPass123!"  # Meets requirements
```

### 3. Allow Customization

```python
# ✅ GOOD - Easy to customize
user = (UserBuilder()
        .with_email("custom@test.com")
        .with_username("custom")
        .build(db))
```

### 4. Clean Up After Tests

```python
# ✅ GOOD - Fixtures handle cleanup automatically
@pytest.fixture
def clean_db(db_session):
    """Ensure clean database."""
    yield db_session
    # Automatic cleanup after test
```

### 5. Don't Share Mutable State

```python
# ❌ BAD - Global state
SHARED_USER = None

def test_1():
    global SHARED_USER
    SHARED_USER = create_user()
    SHARED_USER.username = "changed"

def test_2():
    # SHARED_USER was changed by test_1!
    assert SHARED_USER.username == "testuser"  # Fails!

# ✅ GOOD - Each test gets fresh data
def test_1():
    user = create_user()
    user.username = "changed"

def test_2():
    user = create_user()  # Fresh user
    assert user.username == "testuser"  # Pass!
```

---

<h2 id="when-to-use-each-approach">📊 When to Use Each Approach</h2>

| Approach              | Use When                   | Example                         |
| --------------------- | -------------------------- | ------------------------------- |
| **Fixtures**          | Data used by many tests    | `test_user`, `test_post`        |
| **Builders**          | Need variations of data    | `UserBuilder().with_email(...)` |
| **Factory Functions** | Creating complex scenarios | `create_social_network()`       |
| **Inline Creation**   | Simple, one-off data       | `value = "test"`                |

---

## 🚨 Common Mistakes

### Mistake 1: Creating Too Much Data

```python
# ❌ BAD - Creates 1000 users for no reason
def test_user_count():
    for i in range(1000):
        create_user(f"user{i}")
    # Test only needs a few

# ✅ GOOD - Create what you need
def test_user_count():
    create_user("user1")
    create_user("user2")
    assert User.count() == 2
```

### Mistake 2: Not Cleaning Up

```python
# ❌ BAD - Leaves test data in database
def test_without_cleanup():
    user = create_user()
    # User stays in database for next test!

# ✅ GOOD - Use fixtures for automatic cleanup
def test_with_cleanup(db_session):
    user = UserBuilder().build(db_session)
    # db_session fixture handles cleanup
```

### Mistake 3: Hard-Coding IDs

```python
# ❌ BAD - Hard-coded ID
def test_get_user():
    response = client.get("/api/users/1")
    # User ID 1 might not exist!

# ✅ GOOD - Use created user's ID
def test_get_user():
    user = create_user()
    response = client.get(f"/api/users/{user.id}")
```

---

<h2 id="completion-checklist">✅ Completion Checklist</h2>

- [ ] Created UserBuilder and PostBuilder
- [ ] Created scenario builder functions
- [ ] Completed CommentBuilder challenge
- [ ] Understand when to use builders vs fixtures
- [ ] Can create complex test scenarios easily

---

<h2 id="key-takeaways">🎯 Key Takeaways</h2>

1. **Builders make test data easy** - Fluent API with `.with_*()` methods
2. **Fixtures provide reusable setup** - Automatic cleanup
3. **Factory functions create scenarios** - Complex data setups
4. **Clean data = reliable tests** - Fresh data for each test
5. **Don't hardcode data** - Create what you need

---

<h2 id="next-steps">📚 Next Steps</h2>

**Apply your skills:**

- Use builders in your actual tests
- Create builders for Reaction model
- Build complex test scenarios
- Read: [Test Data Scenarios Guide](../docs/guides/TEST_DATA_SCENARIOS.md) for more patterns

---

**🎉 Congratulations!** You can now manage test data like a professional!

**Next Lab:** Move to [Stage 3: API & E2E Testing](../../stage_3_api_e2e/README.md) or explore other labs
