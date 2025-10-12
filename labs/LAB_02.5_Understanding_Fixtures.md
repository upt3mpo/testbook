# 🧪 Lab 2.5: Understanding Fixtures

**Estimated Time:** 45 minutes
**Difficulty:** Intermediate
**Prerequisites:** Labs 1 & 2 completed

---

## 🎯 What You'll Learn

By the end of this lab, you will:

- Understand what fixtures are and why they matter
- Use existing fixtures in your tests
- Create your own simple fixture
- Understand fixture scope (function, class, module)
- See how fixtures make tests cleaner and faster

---

## 💡 What Are Fixtures?

**Problem:** You need to set up test data repeatedly.

```python
def test_user_email():
    # Setup (repeated in every test)
    user = User(email="test@test.com", username="testuser")
    db.add(user)
    db.commit()

    # Test
    assert user.email == "test@test.com"

def test_user_username():
    # Same setup again!
    user = User(email="test@test.com", username="testuser")
    db.add(user)
    db.commit()

    # Test
    assert user.username == "testuser"
```

**Solution:** Fixtures provide reusable setup.

```python
@pytest.fixture
def test_user(db_session):
    """Create a test user (setup runs once per test)."""
    user = User(email="test@test.com", username="testuser")
    db_session.add(user)
    db_session.commit()
    return user

def test_user_email(test_user):
    """Use the fixture by name."""
    assert test_user.email == "test@test.com"

def test_user_username(test_user):
    """Fixture runs again for this test (fresh user)."""
    assert test_user.username == "testuser"
```

**Benefits:**

- ✅ No repeated setup code
- ✅ Consistent test data
- ✅ Automatic cleanup
- ✅ Clear dependencies

---

## 📋 Step-by-Step Instructions

### Step 1: Explore Existing Fixtures (10 minutes)

**Open:** `backend/tests/conftest.py`

**Find these fixtures:**

```python
@pytest.fixture
def test_user(db_session) -> User:
    """Create a test user in the database."""
    user = User(
        email="testuser@example.com",
        username="testuser",
        display_name="Test User",
        hashed_password=get_password_hash("TestPassword123!"),
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user
```

**Key parts:**

1. `@pytest.fixture` decorator - Marks function as a fixture
2. `test_user` name - How tests reference it
3. `db_session` parameter - Fixture can use other fixtures!
4. Returns `user` - This is what tests get
5. Automatic cleanup - Happens after test runs

✅ **Checkpoint:** List 5 fixtures you found in `conftest.py`

---

### Step 2: Use an Existing Fixture (10 minutes)

**Create:** `backend/tests/test_learn_fixtures.py`

```python
"""Learning about fixtures."""

import pytest


@pytest.mark.unit
class TestUsingFixtures:
    """Tests demonstrating fixture usage."""

    def test_fixture_provides_user(self, test_user):
        """Test that test_user fixture works."""
        # The fixture created a user for us
        assert test_user is not None
        assert test_user.id is not None
        assert test_user.email == "testuser@example.com"

    def test_fixture_user_has_password(self, test_user):
        """Test that user has hashed password."""
        # Each test gets a fresh user
        assert test_user.hashed_password is not None
        assert test_user.hashed_password.startswith("$2b$")

    def test_multiple_fixtures(self, test_user, test_user_2):
        """Test using multiple fixtures at once."""
        # test_user and test_user_2 are different users
        assert test_user.id != test_user_2.id
        assert test_user.email != test_user_2.email

```

**Run it:**

```bash
cd backend
pytest tests/test_learn_fixtures.py -v
```

✅ **Checkpoint:** All 3 tests should pass

---

### Step 3: Understanding Fixture Flow (10 minutes)

**Let's see what happens step-by-step:**

```python
def test_fixture_flow(test_user):
    """Demonstrates fixture execution flow."""
    print("\n📍 Inside test function")
    print(f"   User email: {test_user.email}")
    print(f"   User ID: {test_user.id}")


    assert test_user.email == "testuser@example.com"
```

**Run with output visible:**

```bash
pytest tests/test_learn_fixtures.py::TestUsingFixtures::test_fixture_flow -v -s
```

**You'll see:**

```
1. Fixture runs (creates user)
2. Test receives user
3. Test runs
4. Test completes
5. Fixture cleanup happens (automatic)
```

**Add this test to see the full flow:**

```python
def test_see_fixture_in_action(self, test_user):
    """See fixture data."""
    print(f"\n🔍 User ID: {test_user.id}")
    print(f"📧 Email: {test_user.email}")
    print(f"👤 Username: {test_user.username}")
    print(f"🏷️ Display Name: {test_user.display_name}")


    # Make some assertion
    assert test_user.display_name == "Test User"
```

**Run:**

```bash
pytest tests/test_learn_fixtures.py::TestUsingFixtures::test_see_fixture_in_action -v -s
```

✅ **Checkpoint:** You can see the user data printed

---

### Step 4: Create Your Own Simple Fixture (15 minutes)

**Add to the same file:**

```python
@pytest.fixture
def sample_post_data():
    """Fixture that returns test data (no database)."""
    return {
        "content": "This is a test post",
        "author_id": 1,
        "likes": 10,
        "comments": 5,
    }


class TestCustomFixtures:
    """Tests using our custom fixture."""

    def test_post_data_fixture(self, sample_post_data):
        """Test using our simple fixture."""
        assert sample_post_data["content"] == "This is a test post"
        assert sample_post_data["likes"] == 10

    def test_fixture_provides_all_fields(self, sample_post_data):
        """Test that fixture has all expected fields."""
        # Each test gets fresh copy of data
        expected_fields = ["content", "author_id", "likes", "comments"]

        for field in expected_fields:
            assert field in sample_post_data

    def test_modify_fixture_data(self, sample_post_data):
        """Test that modifications don't affect other tests."""
        # Modify the data

        sample_post_data["likes"] = 100

        # This won't affect other tests - they get fresh copy
        assert sample_post_data["likes"] == 100
```

**Run it:**

```bash
pytest tests/test_learn_fixtures.py::TestCustomFixtures -v
```

✅ **Checkpoint:** Your custom fixture tests pass

---

### Step 5: Fixtures Using Other Fixtures (Advanced) (10 minutes)

**Add this to demonstrate fixture chaining:**

```python
@pytest.fixture
def user_with_posts(test_user, db_session):
    """Fixture that uses test_user fixture."""
    # Create 3 posts for the test user
    posts = []
    for i in range(1, 4):
        post = Post(
            author_id=test_user.id,
            content=f"Test post number {i}",
        )
        db_session.add(post)
        posts.append(post)

    db_session.commit()

    for post in posts:
        db_session.refresh(post)

    return {"user": test_user, "posts": posts}


class TestComplexFixtures:
    """Tests using fixtures that depend on other fixtures."""

    def test_user_with_posts(self, user_with_posts):
        """Test fixture that creates user and posts."""
        user = user_with_posts["user"]
        posts = user_with_posts["posts"]

        assert user is not None
        assert len(posts) == 3
        assert all(post.author_id == user.id for post in posts)

    def test_posts_have_content(self, user_with_posts):
        """Test that posts have expected content."""
        posts = user_with_posts["posts"]


        # Check first post
        assert "Test post number 1" in posts[0].content

        # Check all have content
        assert all(len(post.content) > 0 for post in posts)
```

**Run it:**

```bash
pytest tests/test_learn_fixtures.py::TestComplexFixtures -v
```

✅ **Checkpoint:** Complex fixture tests pass

---

## 🎓 Understanding Fixture Scope

Fixtures can have different scopes:

```python
@pytest.fixture(scope="function")  # Default - runs for each test
def per_test_fixture():
    print("🔄 Runs for every test")
    return "test data"

@pytest.fixture(scope="class")  # Runs once per test class
def per_class_fixture():
    print("📦 Runs once for the class")
    return "class data"

@pytest.fixture(scope="module")  # Runs once per file
def per_module_fixture():
    print("📄 Runs once for the entire file")
    return "module data"

@pytest.fixture(scope="session")  # Runs once for entire test session
def per_session_fixture():
    print("🌍 Runs once for all tests")
    return "session data"
```

**Add this to see scopes in action:**

```python
@pytest.fixture(scope="class")
def class_scoped_counter():
    """Fixture that runs once per class."""
    print("\n🎯 Class fixture initialized!")
    return {"count": 0}


class TestFixtureScope:
    """Demonstrate fixture scope."""

    def test_scope_1(self, class_scoped_counter):
        """First test using class-scoped fixture."""
        class_scoped_counter["count"] += 1
        print(f"\n📊 Count in test 1: {class_scoped_counter['count']}")
        assert class_scoped_counter["count"] == 1

    def test_scope_2(self, class_scoped_counter):
        """Second test using same fixture instance."""
        class_scoped_counter["count"] += 1
        print(f"\n📊 Count in test 2: {class_scoped_counter['count']}")
        # Same fixture instance! Count is 2
        assert class_scoped_counter["count"] == 2


    def test_scope_3(self, class_scoped_counter):
        """Third test using same fixture instance."""
        class_scoped_counter["count"] += 1
        print(f"\n📊 Count in test 3: {class_scoped_counter['count']}")
        # Still same instance! Count is 3
        assert class_scoped_counter["count"] == 3
```

**Run with output:**

```bash
pytest tests/test_learn_fixtures.py::TestFixtureScope -v -s
```

You'll see the fixture initializes once, and all tests share it!

---

## 💪 Your Challenge

**Create a fixture for testing comments:**

```python
@pytest.fixture
def post_with_comments(test_user, test_user_2, test_post, db_session):
    """Create a post with multiple comments.

    TODO:
    1. Use test_post fixture
    2. Create 3 comments from test_user
    3. Create 2 comments from test_user_2
    4. Return dict with post and comments list
    """
    # Your code here!
    pass


class TestYourChallenge:
    """Test your fixture."""

    def test_post_has_comments(self, post_with_comments):
        """Test that post has 5 comments."""
        post = post_with_comments["post"]
        comments = post_with_comments["comments"]

        assert len(comments) == 5
        # Uncomment when you implement the fixture:
        # assert all(comment.post_id == post.id for comment in comments)

    def test_comments_from_two_users(self, post_with_comments):
        """Test that comments are from 2 different users."""

        comments = post_with_comments["comments"]

        # Get unique author IDs
        author_ids = {comment.author_id for comment in comments}

        # Should have exactly 2 different authors
        assert len(author_ids) == 2
```

**Hints:**

- Look at the `test_comment` fixture in `conftest.py` for an example
- Remember to `db_session.add()` and `db_session.commit()`
- Return a dictionary with `{"post": post, "comments": [...]}`

---

## 🚨 Common Mistakes

### Mistake 1: Forgetting to Return Value

```python
# ❌ BAD
@pytest.fixture
def my_data():
    data = {"value": 42}
    # Forgot to return!

# ✅ GOOD
@pytest.fixture
def my_data():
    data = {"value": 42}
    return data
```

### Mistake 2: Modifying Fixture in conftest.py

```python
# ❌ BAD - Don't edit conftest.py for learning exercises
# Edit your own test file instead

# ✅ GOOD - Create fixtures in your test file
@pytest.fixture
def my_custom_fixture():
    return "data"
```

### Mistake 3: Circular Dependencies

```python
# ❌ BAD - Fixtures can't depend on each other circularly
@pytest.fixture
def fixture_a(fixture_b):
    return "a"

@pytest.fixture
def fixture_b(fixture_a):  # Circular!
    return "b"

# ✅ GOOD - Clear dependency chain
@pytest.fixture
def fixture_a():
    return "a"

@pytest.fixture
def fixture_b(fixture_a):
    return f"b-uses-{fixture_a}"
```

### Mistake 4: Expecting Fixtures to Persist Between Tests

```python
@pytest.fixture
def counter():
    return {"count": 0}

# ❌ Tests expecting shared state
def test_1(counter):
    counter["count"] += 1
    assert counter["count"] == 1

def test_2(counter):
    # Gets FRESH counter, not the one from test_1
    assert counter["count"] == 1  # Not 2!
```

---

## 📝 Quiz

Test your understanding:

1. **What is a fixture?**
   - A) A test function
   - B) A reusable setup function
   - C) A bug
   - D) A Python class

2. **How do you use a fixture in a test?**
   - A) Call it like a function
   - B) Import it
   - C) Add it as a parameter
   - D) Use @fixture decorator

3. **What scope runs once per test?**
   - A) `scope="function"`
   - B) `scope="class"`
   - C) `scope="module"`
   - D) `scope="session"`

4. **Can fixtures use other fixtures?**
   - A) Yes
   - B) No

5. **Do fixtures automatically clean up?**
   - A) Yes
   - B) No

**Answers:** 1-B, 2-C, 3-A, 4-A, 5-A

---

## ✅ Completion Checklist

- [ ] Ran all test examples successfully
- [ ] Created your own simple fixture
- [ ] Completed the challenge (post_with_comments)
- [ ] Understand fixture scope differences
- [ ] Can explain why fixtures are useful

---

## 🎯 Key Takeaways

1. **Fixtures eliminate repeated setup** - Write once, use everywhere
2. **Fixtures can depend on other fixtures** - Build complex scenarios
3. **Fixtures run automatically** - Just add them as parameters
4. **Fixtures clean up automatically** - No manual cleanup needed
5. **Fixture scope controls when they run** - function, class, module, session

---

**Ready for more?**

- **[LAB_03_Testing_API_Endpoints.md](LAB_03_Testing_API_Endpoints.md)** - Use fixtures with API tests
- **[backend/tests/conftest.py](../backend/tests/conftest.py)** - Study professional fixtures
- **[Pytest Fixtures Documentation](https://docs.pytest.org/en/latest/fixture.html)** - Deep dive

---

**🎉 Congratulations!** You now understand one of the most powerful features of pytest!
