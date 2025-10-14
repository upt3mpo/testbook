# 🚫 Testing Anti-Patterns

**Common testing mistakes and how to avoid them**

---

## 🎯 What Are Anti-Patterns?

Anti-patterns are common solutions that seem reasonable but cause problems. In testing, they lead to:

- Flaky tests (pass sometimes, fail sometimes)
- Slow test suites
- Hard-to-maintain tests
- False confidence

**This guide shows you what NOT to do, and what to do instead.**

---

## 📚 Table of Contents

1. [Hardcoded Data Anti-Patterns](#hardcoded-data-anti-patterns)
2. [Time and Sleep Anti-Patterns](#time-and-sleep-anti-patterns)
3. [Dependency Anti-Patterns](#dependency-anti-patterns)
4. [Assertion Anti-Patterns](#assertion-anti-patterns)
5. [Test Structure Anti-Patterns](#test-structure-anti-patterns)
6. [Database Anti-Patterns](#database-anti-patterns)
7. [E2E Testing Anti-Patterns](#e2e-testing-anti-patterns)

---

## 1. Hardcoded Data Anti-Patterns

### Anti-Pattern 1.1: Magic Numbers

**❌ BAD:**

```python
def test_get_user():
    """Test getting user by ID."""
    response = client.get("/api/users/1")  # Magic number!
    assert response.status_code == 200
```

**Why it's bad:**

- User ID 1 might not exist
- Test breaks if database is reset
- Brittle and unreliable

**✅ GOOD:**

```python
def test_get_user(client, test_user):
    """Test getting user by ID."""
    response = client.get(f"/api/users/{test_user.id}")
    assert response.status_code == 200
    assert response.json()["id"] == test_user.id
```

---

### Anti-Pattern 1.2: Hardcoded Timestamps

**❌ BAD:**

```python
def test_user_created_date():
    """Test user creation date."""
    user = create_user()
    # Hardcoded date - will fail tomorrow!
    assert user.created_at == "2024-01-15T10:30:00"
```

**Why it's bad:**

- Dates change, test breaks
- Timezone issues
- Not actually testing the logic

**✅ GOOD:**

```python
from datetime import datetime, timedelta

def test_user_created_date():
    """Test user creation date is recent."""
    before = datetime.utcnow()
    user = create_user()
    after = datetime.utcnow()

    # Check it's within our time window
    assert before <= user.created_at <= after
    # Or check it's recent (within last minute)
    assert datetime.utcnow() - user.created_at < timedelta(minutes=1)
```

---

### Anti-Pattern 1.3: Environment-Specific Data

**❌ BAD:**

```python
def test_api_connection():
    """Test API connection."""
    # Works on my machine only!
    response = requests.get("http://localhost:8000/api/health")
    assert response.status_code == 200
```

**Why it's bad:**

- Port might be different
- Hostname might be different
- CI/CD environment differs

**✅ GOOD:**

```python
import os

def test_api_connection():
    """Test API connection."""
    # Use environment variable with fallback
    base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
    response = requests.get(f"{base_url}/api/health")
    assert response.status_code == 200
```

---

## 2. Time and Sleep Anti-Patterns

### Anti-Pattern 2.1: Using sleep() for Waiting

**❌ BAD:**

```python
import time

def test_async_operation():
    """Test async operation."""
    trigger_async_task()
    time.sleep(5)  # Arbitrary wait!
    result = check_result()
    assert result.status == "complete"
```

**Why it's bad:**

- Might be too short (flaky test)
- Might be too long (slow test)
- Doesn't check actual condition

**✅ GOOD:**

```python
import time

def test_async_operation():
    """Test async operation."""
    trigger_async_task()

    # Wait for condition with timeout
    max_wait = 10
    start_time = time.time()

    while time.time() - start_time < max_wait:
        result = check_result()
        if result.status == "complete":
            break
        time.sleep(0.1)  # Small check interval

    assert result.status == "complete"
```

**✅ EVEN BETTER with pytest-timeout:**

```python
@pytest.mark.timeout(10)
def test_async_operation():
    """Test async operation."""
    trigger_async_task()

    # Poll until ready
    while True:
        result = check_result()
        if result.status == "complete":
            break
        time.sleep(0.1)

    assert result.status == "complete"
```

---

### Anti-Pattern 2.2: Playwright Timeouts

**❌ BAD:**

```javascript
test('wait for element', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await page.waitForTimeout(3000);  // Arbitrary wait!
  await page.click('[data-testid="button"]');
});
```

**Why it's bad:**

- Slows down tests unnecessarily
- Might not be long enough
- Doesn't wait for actual condition

**✅ GOOD:**

```javascript
test('wait for element', async ({ page }) => {
  await page.goto('http://localhost:3000');
  // Wait for specific element
  await page.waitForSelector('[data-testid="button"]', { state: 'visible' });
  await page.click('[data-testid="button"]');
});
```

**✅ EVEN BETTER (Playwright auto-waits):**

```javascript
test('wait for element', async ({ page }) => {
  await page.goto('http://localhost:3000');
  // Playwright automatically waits for element!
  await page.click('[data-testid="button"]');
});
```

---

## 3. Dependency Anti-Patterns

### Anti-Pattern 3.1: Tests Depending on Each Other

**❌ BAD:**

```python
created_user_id = None  # Global state!

def test_01_create_user():
    """Test creating user."""
    global created_user_id
    user = create_user()
    created_user_id = user.id
    assert user.id is not None

def test_02_update_user():
    """Test updating user."""
    # Depends on test_01 running first!
    update_user(created_user_id, name="Updated")
    user = get_user(created_user_id)
    assert user.name == "Updated"
```

**Why it's bad:**

- Tests must run in order
- Can't run tests in parallel
- If test_01 fails, test_02 fails too
- Hard to debug

**✅ GOOD:**

```python
def test_create_user():
    """Test creating user."""
    user = create_user()
    assert user.id is not None

def test_update_user():
    """Test updating user."""
    # Create its own user
    user = create_user()
    update_user(user.id, name="Updated")
    updated_user = get_user(user.id)
    assert updated_user.name == "Updated"
```

---

### Anti-Pattern 3.2: Testing Implementation, Not Behavior

**❌ BAD:**

```python
def test_password_hashing_implementation():
    """Test password hashing uses bcrypt."""
    password = "test123"
    hashed = get_password_hash(password)

    # Testing internal implementation
    assert "$2b$" in hashed
    assert hashed.count("$") == 3
    # What if we change hashing algorithm?
```

**Why it's bad:**

- Tests internal implementation details
- Breaks when implementation changes
- Doesn't test actual behavior

**✅ GOOD:**

```python
def test_password_hashing_behavior():
    """Test password hashing works correctly."""
    password = "test123"
    hashed = get_password_hash(password)

    # Test behavior: password is hashed
    assert hashed != password
    assert len(hashed) > len(password)

    # Test behavior: can verify correct password
    assert verify_password(password, hashed) is True

    # Test behavior: wrong password fails
    assert verify_password("wrong", hashed) is False
```

---

## 4. Assertion Anti-Patterns

### Anti-Pattern 4.1: No Assertions

**❌ BAD:**

```python
def test_user_creation():
    """Test user creation."""
    user = create_user()
    # No assertions! Test always passes
```

**Why it's bad:**

- Test doesn't verify anything
- Gives false confidence
- Useless test

**✅ GOOD:**

```python
def test_user_creation():
    """Test user creation."""
    user = create_user()

    assert user is not None
    assert user.id is not None
    assert user.email is not None
```

---

### Anti-Pattern 4.2: Too Many Assertions

**❌ BAD:**

```python
def test_everything():
    """Test all user functionality."""
    user = create_user()
    assert user.id is not None

    post = create_post(user)
    assert post.id is not None

    comment = create_comment(post)
    assert comment.id is not None

    user.follow(other_user)
    assert other_user in user.following

    # 50 more assertions...
```

**Why it's bad:**

- Hard to debug (which assertion failed?)
- Testing too much in one test
- Unclear what's being tested

**✅ GOOD:**

```python
def test_user_creation():
    """Test user creation."""
    user = create_user()
    assert user.id is not None

def test_post_creation():
    """Test post creation."""
    user = create_user()
    post = create_post(user)
    assert post.id is not None
    assert post.author_id == user.id

def test_comment_creation():
    """Test comment creation."""
    user = create_user()
    post = create_post(user)
    comment = create_comment(post)
    assert comment.id is not None
    assert comment.post_id == post.id

def test_user_follow():
    """Test user following."""
    user1 = create_user("user1")
    user2 = create_user("user2")
    user1.follow(user2)
    assert user2 in user1.following
```

---

### Anti-Pattern 4.3: Vague Assertions

**❌ BAD:**

```python
def test_api_response():
    """Test API response."""
    response = client.get("/api/posts")
    # Vague - what are we checking?
    assert response
    assert response.json()
```

**Why it's bad:**

- Unclear what's being verified
- Might pass for wrong reasons
- Hard to debug failures

**✅ GOOD:**

```python
def test_api_response():
    """Test API response returns posts."""
    response = client.get("/api/posts")

    # Specific assertions
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "id" in data[0]
    assert "content" in data[0]
```

---

## 5. Test Structure Anti-Patterns

### Anti-Pattern 5.1: Unclear Test Names

**❌ BAD:**

```python
def test_user():
    """Test user."""
    user = create_user()
    assert user.id

def test_user_2():
    """Test user again."""
    user = create_user()
    assert user.email
```

**Why it's bad:**

- Can't tell what's being tested
- Hard to find tests
- Meaningless failure messages

**✅ GOOD:**

```python
def test_user_has_id_after_creation():
    """Test that newly created user has an ID."""
    user = create_user()
    assert user.id is not None

def test_user_has_valid_email_format():
    """Test that user email follows valid format."""
    user = create_user(email="test@example.com")
    assert "@" in user.email
    assert "." in user.email
```

---

### Anti-Pattern 5.2: No Test Isolation

**❌ BAD:**

```python
# Shared state between tests
test_users = []

def test_create_user():
    """Test creating user."""
    user = create_user()
    test_users.append(user)  # Pollutes global state

def test_list_users():
    """Test listing users."""
    # Depends on test_create_user having run
    assert len(test_users) > 0
```

**Why it's bad:**

- Tests affect each other
- Can't run in parallel
- Hard to debug
- Order-dependent

**✅ GOOD:**

```python
def test_create_user():
    """Test creating user."""
    user = create_user()
    assert user.id is not None

def test_list_users():
    """Test listing users."""
    # Create its own data
    user1 = create_user("user1")
    user2 = create_user("user2")

    users = list_users()
    user_ids = [u.id for u in users]

    assert user1.id in user_ids
    assert user2.id in user_ids
```

---

## 6. Database Anti-Patterns

### Anti-Pattern 6.1: Not Cleaning Up Test Data

**❌ BAD:**

```python
def test_user_creation():
    """Test user creation."""
    user = User(email="test@test.com")
    db.add(user)
    db.commit()
    # User stays in database!

def test_another_user():
    """Test another user."""
    user = User(email="test@test.com")  # Duplicate email!
    db.add(user)
    db.commit()  # Fails! Email already exists
```

**Why it's bad:**

- Data pollution between tests
- Tests fail unexpectedly
- Hard to debug
- Can't run tests multiple times

**✅ GOOD:**

```python
@pytest.fixture
def clean_db(db_session):
    """Provide clean database for each test."""
    yield db_session
    # Cleanup after test
    db_session.rollback()

def test_user_creation(clean_db):
    """Test user creation."""
    user = User(email="test@test.com")
    clean_db.add(user)
    clean_db.commit()
    assert user.id is not None
    # Automatic cleanup via fixture

def test_another_user(clean_db):
    """Test another user."""
    user = User(email="test@test.com")
    clean_db.add(user)
    clean_db.commit()  # Works! Clean database
    assert user.id is not None
```

---

### Anti-Pattern 6.2: Testing with Production Database

**❌ BAD:**

```python
# Using production database URL
DATABASE_URL = "postgresql://prod:password@prod-server/prod_db"

def test_delete_user():
    """Test deleting user."""
    delete_user(user_id=1)  # DELETES PRODUCTION DATA!
```

**Why it's bad:**

- DESTROYS PRODUCTION DATA
- Catastrophic consequences
- Should NEVER happen

**✅ GOOD:**

```python
# Use test database
TEST_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture(scope="function")
def test_db():
    """Create fresh test database."""
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(engine)

    yield engine

    # Clean up
    Base.metadata.drop_all(engine)

def test_delete_user(test_db):
    """Test deleting user."""
    # Safe - using test database
    user = create_user()
    delete_user(user.id)
    assert get_user(user.id) is None
```

---

## 7. E2E Testing Anti-Patterns

### Anti-Pattern 7.1: Brittle Selectors

**❌ BAD:**

```javascript
test('click button', async ({ page }) => {
  // Fragile CSS selectors
  await page.click('.btn.btn-primary.submit-button.large');
  await page.click('div > div > button:nth-child(3)');
  await page.click('button[style="color: blue"]');
});
```

**Why it's bad:**

- Breaks when styles change
- Breaks when HTML structure changes
- Hard to maintain

**✅ GOOD:**

```javascript
test('click button', async ({ page }) => {
  // Stable selectors
  await page.click('[data-testid="submit-button"]');
  await page.click('[data-testid="cancel-button"]');
  await page.getByRole('button', { name: 'Submit' }).click();
});
```

---

### Anti-Pattern 7.2: Not Using Test IDs

**❌ BAD:**

```javascript
test('find element', async ({ page }) => {
  // Searching by text - breaks with typos or i18n
  await page.click('text=Submit Form');

  // Searching by class - breaks when styles change
  await page.click('.submit-btn');
});
```

**Why it's bad:**

- Text changes break tests
- Internationalization breaks tests
- Style changes break tests

**✅ GOOD:**

```javascript
test('find element', async ({ page }) => {
  // Use data-testid
  await page.click('[data-testid="submit-button"]');
});
```

**In your HTML:**

```html
<button data-testid="submit-button" class="btn btn-primary">
  Submit Form
</button>
```

---

### Anti-Pattern 7.3: Not Handling Browser Dialogs ⚠️ CRITICAL

**❌ BAD:**

```javascript
test('should delete account', async ({ page }) => {
  await page.click('[data-testid="delete-button"]');
  // Test hangs here! window.confirm() is blocking execution
  await expect(page).toHaveURL('/login');  // Never gets here
});
```

**Why it's bad:**

- `window.confirm()` blocks JavaScript execution
- Test waits forever for user input
- No error message - just timeout
- **This broke 5 tests in Testbook!**

**Real example from Testbook:**

When we had this in the frontend:

```javascript
// Profile.jsx
const handleBlock = async () => {
  if (!window.confirm('Are you sure you want to block this user?')) return;
  await blockUser();
};
```

Tests that clicked the block button would hang waiting for the dialog to be dismissed.

**✅ GOOD:**

```javascript
test('should delete account', async ({ page }) => {
  // Setup dialog handler BEFORE clicking
  page.on('dialog', dialog => dialog.accept());

  await page.click('[data-testid="delete-button"]');
  await expect(page).toHaveURL('/login');  // Works!
});
```

**✅ BETTER - Setup Once:**

```javascript
// In test-helpers.js
function setupDialogHandler(page) {
  page.on('dialog', async dialog => {
    console.log(`Auto-accepting ${dialog.type()}: ${dialog.message()}`);
    await dialog.accept();
  });
}

// In every test file
test.beforeEach(async ({ page }) => {
  setupDialogHandler(page);  // Handle all dialogs automatically
  // ... rest of setup
});
```

**Why it's better:**

- ✅ Handles confirms AND alerts
- ✅ Works for all tests automatically
- ✅ Logs what dialogs appear
- ✅ No need to remember for each test

**Note:** This fixed 5 Testbook E2E tests that were failing due to:

- Edit post alert: "Post updated successfully!"
- Block user confirm: "Are you sure you want to block?"
- Delete account confirms: Two separate confirmations
- Multiple other confirmation dialogs

---

### Anti-Pattern 7.4: Test ID Mismatches

**❌ BAD:**

```javascript
test('should show count', async ({ page }) => {
  // Looking for element that doesn't exist!
  await expect(page.locator('[data-testid="followers-count"]')).toBeVisible();
});
```

**Why it's bad:**

- Test fails with "element not found"
- Wastes time debugging
- Creates false failures

**Real example from Testbook:**

Tests were looking for `profile-followers-count` but frontend had:

```jsx
<Link data-testid="profile-followers-link">  {/* Different ID! */}
  <strong>{profile.followers_count}</strong> followers
</Link>
```

**✅ GOOD:**

```javascript
// Option 1: Match the actual test IDs
await expect(page.locator('[data-testid="profile-followers-link"]')).toBeVisible();

// Option 2: Add the missing test IDs to frontend
<strong data-testid="profile-followers-count">{count}</strong>
```

**Best Practice:**

- ✅ Keep a test ID reference document
- ✅ Verify test IDs exist before writing tests
- ✅ Use consistent naming conventions
- ✅ Add test IDs during component development, not later

---

### Anti-Pattern 7.5: Not Using Force Clicks When Needed

**❌ BAD:**

```javascript
test('should edit post', async ({ page }) => {
  await page.click('[data-testid="menu-button"]');
  await page.click('[data-testid="edit-button"]');  // Fails! Dropdown closing
});
```

**Why it's bad:**

- Dropdown menus can close due to click-outside handlers
- Timing is unreliable
- Tests become flaky

**Real example from Testbook:**

Our Post component has click-outside handler:

```javascript
useEffect(() => {
  const handleClickOutside = (event) => {
    setShowDropdown(false);  // Closes dropdown
  };
  document.addEventListener('mousedown', handleClickOutside);
}, [showDropdown]);
```

Tests would open the menu, but by the time they tried to click edit, the dropdown was closing!

**✅ GOOD:**

```javascript
test('should edit post', async ({ page }) => {
  await page.click('[data-testid="menu-button"]');

  // Force click to bypass visibility checks
  await page.locator('[data-testid="edit-button"]').click({ force: true });
});
```

**When to use `force: true`:**

- ✅ Elements with CSS transitions
- ✅ Dropdown menus with close handlers
- ✅ Elements that become hidden quickly
- ❌ Not for actually hidden elements
- ❌ Not as a first resort - debug the real issue first

**Note:** This fixed the final 2 failing Testbook tests (edit post, cancel edit)

---

## ✅ Quick Checklist: Avoid Anti-Patterns

Before committing your tests, check:

- [ ] No hardcoded IDs or magic numbers
- [ ] No `time.sleep()` or `waitForTimeout()` for synchronization
- [ ] Browser dialogs handled (confirm/alert/prompt) ⚠️ **CRITICAL**
- [ ] Test IDs match actual frontend code
- [ ] Tests are independent (no shared state)
- [ ] Each test has clear assertions
- [ ] Test names describe what's being tested
- [ ] Using test database, not production
- [ ] Tests clean up after themselves
- [ ] Using `data-testid` for E2E selectors
- [ ] Testing behavior, not implementation
- [ ] One concept per test

---

## 📚 Related Resources

- **[TESTING_PATTERNS.md](TESTING_PATTERNS.md)** - What TO do (now includes dialog handling & force clicks!)
- **[FLAKY_TESTS_GUIDE.md](../guides/FLAKY_TESTS_GUIDE.md)** ⭐ - Real fixes from this project
- **[TESTING_CHEATSHEET.md](TESTING_CHEATSHEET.md)** - Quick reference (updated with critical patterns)
- **[Common Mistakes](../course/COMMON_MISTAKES.md)** - Student errors
- **[Test Examples](../../backend/tests/examples/)** - Good vs bad tests
- **[Flaky Tests Guide](../guides/FLAKY_TESTS_GUIDE.md)** - How to fix unreliable tests

---

**Remember:** These anti-patterns are common. Even experienced developers make these mistakes. The key is to recognize them and fix them!

**Real-world impact:** Following these patterns helped us achieve **100% test pass rate (234/234 tests)** in Testbook!
