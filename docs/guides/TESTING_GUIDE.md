# 🧪 Testbook Testing Guide

This guide provides comprehensive examples and scenarios for testing Testbook with various automation frameworks.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Testing Frameworks](#testing-frameworks)
3. [Test Data](#test-data)
4. [Backend Testing](#backend-testing)
5. [API Testing](#api-testing)
6. [UI Testing](#ui-testing)
7. [Test Scenarios](#test-scenarios)

## Getting Started

### Prerequisites

1. **Start Testbook:**
   - macOS/Linux: `./start.sh` or `./start-dev.sh`
   - Windows: `start.bat` or `start-dev.bat`
2. Verify it's running: <http://localhost:8000>
3. Check API docs: <http://localhost:8000/docs>

## Testing Frameworks

Testbook works with any testing tool! Here are popular options:

### 🌐 UI Testing Tools

**[Playwright](https://playwright.dev/)** - Recommended for beginners

```bash
npm init playwright@latest

```

- Fast, reliable, cross-browser
- Great documentation
- Built-in test runner

**[Selenium](https://www.selenium.dev/)** - Industry standard

```bash
pip install selenium
```

- Works with all major languages

- Huge community support
- Extensive browser support

**[Cypress](https://www.cypress.io/)** - Developer-friendly

```bash
npm install cypress --save-dev
```

- Real-time reloads

- Time-travel debugging
- Beautiful UI

### 🔌 API Testing Tools

**[Postman](https://www.postman.com/)** - Visual & powerful

- No coding required (can add scripts)
- Collection runner for automation
- Export to Newman for CI/CD

**[REST Assured](https://rest-assured.io/)** - Java developers

```java
given().auth().basic("user", "pass")
  .when().get("/api/posts")
  .then().statusCode(200);
```

**[PyTest + Requests](https://docs.pytest.org/en/stable/getting-started.html)** - Python developers

```bash
pip install pytest requests
```

### 📚 Learning Resources

- **Playwright Tutorial**: <https://playwright.dev/docs/intro>
- **Selenium Guide**: <https://www.selenium.dev/documentation/>
- **Cypress Tutorial**: <https://docs.cypress.io/guides/getting-started/installing-cypress>
- **API Testing Guide**: <https://www.postman.com/api-platform/api-testing/>
- **PyTest Tutorial**: <https://docs.pytest.org/en/stable/getting-started.html>

### Reset Test Data

Before each test suite, reset the database:

```bash
# Easy way (recommended)
./reset-database.sh

# Or use API
curl -X POST http://localhost:8000/api/dev/reset
```

Or use the dev API in your tests:

```javascript
// JavaScript/Playwright
await fetch('http://localhost:8000/api/dev/reset', { method: 'POST' });

// Python/Requests
import requests
requests.post('http://localhost:8000/api/dev/reset')
```

## Test Data

### Available Test Accounts

| Email                        | Password        | Display Name  | Relationships                      |
| ---------------------------- | --------------- | ------------- | ---------------------------------- |
| <sarah.johnson@testbook.com> | Sarah2024!      | Sarah Johnson | Follows: Mike, Emma, Lisa          |
| <mike.chen@testbook.com>     | MikeRocks88     | Mike Chen     | Follows: Sarah, Emma, Alex, Daniel |
| <emma.davis@testbook.com>    | EmmaLovesPhotos | Emma Davis    | Follows: Sarah, Mike, Lisa, Olivia |
| <newuser@testbook.com>       | NewUser123!     | New User      | No followers/following             |

### Pre-seeded Content

- **9 test users** with different profiles and relationships
- **21 posts** with varied content (text, images, videos)
- **9 comments** on various posts
- **16 reactions** across different posts
- **2 reposts**
- **Established relationships** between users (follows, etc.)

### Key Testing Features

✅ **138+ data-testid attributes** - Every interactive element is easily selectable
✅ **File upload support** - Test drag-and-drop and file picker functionality
✅ **Toggle actions** - Reactions, reposts, follow/unfollow all toggleable
✅ **Edit functionality** - Posts and profiles are editable
✅ **Emoji reactions** - Visual feedback with 6 reaction types
✅ **Cross-platform scripts** - Reset database on macOS/Linux/Windows
✅ **Dev API endpoints** - Create custom test scenarios programmatically

## Backend Testing

Test the FastAPI backend with unit tests, integration tests, and database tests.

### Setup for Backend Tests

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install pytest pytest-asyncio httpx
```

### Unit Tests - Testing Models

Test individual database models and their methods:

```python
# test_models.py
import pytest
from models import User, Post
from database import SessionLocal
from auth import get_password_hash, verify_password

def test_user_password_hashing():
    """Test password hashing and verification"""
    password = "TestPassword123!"
    hashed = get_password_hash(password)

    # Password should be hashed
    assert hashed != password

    # Should verify correctly
    assert verify_password(password, hashed) is True

    # Should not verify incorrect password
    assert verify_password("WrongPassword", hashed) is False

def test_user_model_creation():
    """Test User model validation"""
    db = SessionLocal()

    user = User(
        email="test@example.com",
        username="testuser",
        display_name="Test User",
        hashed_password=get_password_hash("password123")
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.username == "testuser"

    db.close()

def test_post_model_relationships():
    """Test Post model relationships"""
    db = SessionLocal()

    # Get a test user
    user = db.query(User).first()

    # Create a post
    post = Post(
        author_id=user.id,
        content="Test post content"
    )

    db.add(post)
    db.commit()
    db.refresh(post)

    # Test relationship
    assert post.author.username == user.username
    assert post.author_id == user.id

    db.close()
```

### Integration Tests - Testing Routers

Test API endpoints with TestClient:

```python
# test_auth.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register_new_user():
    """Test user registration endpoint"""
    response = client.post(
        "/api/auth/register",
        json={
            "email": "newuser@test.com",
            "username": "newuser",
            "password": "SecurePass123!",
            "display_name": "New User"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@test.com"
    assert data["username"] == "newuser"
    assert "access_token" in data

def test_login_success():
    """Test successful login"""
    response = client.post(
        "/api/auth/login",
        json={
            "email": "sarah.johnson@testbook.com",
            "password": "Sarah2024!"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials():
    """Test login with wrong password"""
    response = client.post(
        "/api/auth/login",
        json={
            "email": "sarah.johnson@testbook.com",
            "password": "WrongPassword"
        }
    )

    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]

def test_get_current_user_authenticated():
    """Test getting current user with valid token"""
    # First login to get token
    login_response = client.post(
        "/api/auth/login",
        json={
            "email": "sarah.johnson@testbook.com",
            "password": "Sarah2024!"
        }
    )
    token = login_response.json()["access_token"]

    # Get current user
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "sarah.johnson@testbook.com"

def test_get_current_user_unauthorized():
    """Test accessing protected route without token"""
    response = client.get("/api/auth/me")

    assert response.status_code == 401
```

### Integration Tests - Testing Posts

```python
# test_posts.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture
def auth_token():
    """Fixture to get authentication token"""
    response = client.post(
        "/api/auth/login",
        json={
            "email": "sarah.johnson@testbook.com",
            "password": "Sarah2024!"
        }
    )
    return response.json()["access_token"]

def test_create_post(auth_token):
    """Test creating a new post"""
    response = client.post(
        "/api/posts/",
        json={
            "content": "This is a test post",
            "image_url": None,
            "video_url": None
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["content"] == "This is a test post"
    assert "id" in data
    assert "created_at" in data

def test_get_post_by_id(auth_token):
    """Test retrieving a specific post"""
    # First create a post
    create_response = client.post(
        "/api/posts/",
        json={"content": "Post to retrieve"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    post_id = create_response.json()["id"]

    # Get the post
    response = client.get(f"/api/posts/{post_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == post_id
    assert data["content"] == "Post to retrieve"

def test_update_own_post(auth_token):
    """Test updating your own post"""
    # Create a post
    create_response = client.post(
        "/api/posts/",
        json={"content": "Original content"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    post_id = create_response.json()["id"]

    # Update the post
    response = client.put(
        f"/api/posts/{post_id}",
        json={"content": "Updated content"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Updated content"

def test_cannot_update_other_users_post():
    """Test that users cannot update posts they don't own"""
    # Login as first user and create post
    token1 = client.post(
        "/api/auth/login",
        json={"email": "sarah.johnson@testbook.com", "password": "Sarah2024!"}
    ).json()["access_token"]

    post = client.post(
        "/api/posts/",
        json={"content": "Sarah's post"},
        headers={"Authorization": f"Bearer {token1}"}
    ).json()

    # Login as second user
    token2 = client.post(
        "/api/auth/login",
        json={"email": "mike.chen@testbook.com", "password": "MikeRocks88"}
    ).json()["access_token"]

    # Try to update first user's post
    response = client.put(
        f"/api/posts/{post['id']}",
        json={"content": "Mike trying to edit"},
        headers={"Authorization": f"Bearer {token2}"}
    )

    assert response.status_code == 403

def test_add_comment_to_post(auth_token):
    """Test adding a comment to a post"""
    # Get an existing post
    posts = client.get("/api/feed/all").json()
    post_id = posts[0]["id"]

    # Add comment
    response = client.post(
        f"/api/posts/{post_id}/comments",
        json={"content": "Great post!"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["content"] == "Great post!"
    assert data["post_id"] == post_id

def test_add_reaction_to_post(auth_token):
    """Test reacting to a post"""
    # Get an existing post
    posts = client.get("/api/feed/all").json()
    post_id = posts[0]["id"]

    # Add reaction
    response = client.post(
        f"/api/posts/{post_id}/reactions",
        json={"reaction_type": "like"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 201

    # Verify reaction was added
    post = client.get(f"/api/posts/{post_id}").json()
    assert post["user_reaction"] == "like"
```

### Database Tests

```python
# tests/integration/test_database.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from models import User, Post, Comment

# Create test database
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def test_db():
    """Create a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_database_user_crud(test_db):
    """Test Create, Read, Update, Delete for User"""
    # Create
    user = User(
        email="crud@test.com",
        username="cruduser",
        display_name="CRUD User",
        hashed_password="hashed"
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)

    # Read
    db_user = test_db.query(User).filter(User.email == "crud@test.com").first()
    assert db_user is not None
    assert db_user.username == "cruduser"

    # Update
    db_user.display_name = "Updated Name"
    test_db.commit()
    test_db.refresh(db_user)
    assert db_user.display_name == "Updated Name"

    # Delete
    test_db.delete(db_user)
    test_db.commit()
    assert test_db.query(User).filter(User.email == "crud@test.com").first() is None

def test_cascade_delete(test_db):
    """Test that deleting a user deletes their posts"""
    # Create user and post
    user = User(
        email="cascade@test.com",
        username="cascadeuser",
        display_name="Cascade User",
        hashed_password="hashed"
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)

    post = Post(
        author_id=user.id,
        content="Test post"
    )
    test_db.add(post)
    test_db.commit()

    # Delete user
    test_db.delete(user)
    test_db.commit()

    # Post should be deleted too (if cascade is configured)
    assert test_db.query(Post).filter(Post.author_id == user.id).first() is None
```

### Running Backend Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest test_auth.py

# Run specific test function
pytest test_auth.py::test_login_success

# Run with coverage
pytest --cov=. --cov-report=html

# Run tests in parallel (faster)
pytest -n auto
```

### Test Configuration

Create a `pytest.ini` file in the backend directory:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --tb=short
    --strict-markers
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow running tests
```

### Organizing Tests

```text
backend/
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Shared fixtures
│   ├── test_models.py       # Unit tests for models
│   ├── test_auth.py         # Integration tests for auth
│   ├── unit/
│   │   ├── test_auth.py     # Unit tests for auth
│   │   └── test_models.py   # Unit tests for models
│   ├── integration/
│   │   ├── test_api_auth.py # Integration tests for auth
│   │   ├── test_api_posts.py # Integration tests for posts
│   │   ├── test_api_users.py # Integration tests for users
│   │   └── test_database.py # Database tests
```

## API Testing

### Types of API Testing

**Integration Tests** (Manual test cases):

- Test specific scenarios you design
- Validate business logic
- Check exact expected behavior
- **In Testbook:** 140+ tests in `backend/tests/integration/`

**Contract Tests** (Automated from schema):

- Automatically generate test cases from OpenAPI schema
- Validate API matches documentation
- Find edge cases and security vulnerabilities
- **In Testbook:** See [Contract Testing Guide](CONTRACT_TESTING.md) for explanation (currently using experimental features)

### Authentication Flow

```python
# Python + Requests Example
import requests

BASE_URL = "http://localhost:8000/api"

# Login
response = requests.post(f"{BASE_URL}/auth/login", json={
    "email": "sarah.johnson@testbook.com",
    "password": "Sarah2024!"
})
token = response.json()["access_token"]

# Use token for authenticated requests
headers = {"Authorization": f"Bearer {token}"}
me = requests.get(f"{BASE_URL}/auth/me", headers=headers)
print(me.json())
```

```javascript
// JavaScript + Axios Example
const axios = require("axios");

const BASE_URL = "http://localhost:8000/api";

// Login
const loginResponse = await axios.post(`${BASE_URL}/auth/login`, {
  email: "sarah.johnson@testbook.com",
  password: "Sarah2024!",
});

const token = loginResponse.data.access_token;

// Use token
const me = await axios.get(`${BASE_URL}/auth/me`, {
  headers: { Authorization: `Bearer ${token}` },
});
console.log(me.data);
```

### API Test Scenarios

#### 1. User Registration

```python
def test_user_registration():
    response = requests.post(f"{BASE_URL}/auth/register", json={
        "email": "test@testbook.com",
        "username": "testuser",
        "display_name": "Test User",
        "password": "Test123!",
        "bio": "Testing account"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "test@testbook.com"
```

#### 2. Create Post

```python
def test_create_post():
    # Login first
    token = login("sarah.johnson@testbook.com", "Sarah2024!")

    # Create post
    response = requests.post(
        f"{BASE_URL}/posts/",
        json={"content": "Test post content"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "id" in response.json()
```

#### 3. Follow User

```python
def test_follow_user():
    token = login("sarah.johnson@testbook.com", "Sarah2024!")

    response = requests.post(
        f"{BASE_URL}/users/danielkim/follow",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "following" in response.json()["message"].lower()
```

#### 4. Upload Media File

```python
def test_upload_media():
    token = login("sarah.johnson@testbook.com", "Sarah2024!")

    # Upload file
    with open("test_image.jpg", "rb") as f:
        files = {"file": ("test_image.jpg", f, "image/jpeg")}
        response = requests.post(
            f"{BASE_URL}/posts/upload",
            files=files,
            headers={"Authorization": f"Bearer {token}"}
        )

    assert response.status_code == 200
    assert "url" in response.json()

    # Create post with uploaded image
    image_url = response.json()["url"]
    post_response = requests.post(
        f"{BASE_URL}/posts/",
        json={"content": "Check out my photo!", "image_url": image_url},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert post_response.status_code == 200
```

#### 5. Edit Post

```python
def test_edit_post():
    token = login("sarah.johnson@testbook.com", "Sarah2024!")

    # Create post
    post_response = requests.post(
        f"{BASE_URL}/posts/",
        json={"content": "Original content"},
        headers={"Authorization": f"Bearer {token}"}
    )
    post_id = post_response.json()["id"]

    # Edit post
    edit_response = requests.put(
        f"{BASE_URL}/posts/{post_id}",
        json={"content": "Edited content"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert edit_response.status_code == 200
    assert edit_response.json()["content"] == "Edited content"
```

#### 6. Toggle Repost

```python
def test_toggle_repost():
    token = login("sarah.johnson@testbook.com", "Sarah2024!")

    # Create repost
    repost_response = requests.post(
        f"{BASE_URL}/posts/repost",
        json={"original_post_id": 1, "content": ""},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert repost_response.status_code == 200

    # Remove repost
    unrepost_response = requests.delete(
        f"{BASE_URL}/posts/repost/1",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert unrepost_response.status_code == 200
```

#### 7. Get Followers/Following

```python
def test_get_followers_following():
    token = login("sarah.johnson@testbook.com", "Sarah2024!")

    # Get followers
    followers_response = requests.get(
        f"{BASE_URL}/users/sarahjohnson/followers",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert followers_response.status_code == 200
    assert isinstance(followers_response.json(), list)

    # Get following
    following_response = requests.get(
        f"{BASE_URL}/users/sarahjohnson/following",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert following_response.status_code == 200
    assert isinstance(following_response.json(), list)
```

## UI Testing

### Playwright Examples

#### Login Test

```javascript
const { test, expect } = require("@playwright/test");

test("user can login", async ({ page }) => {
  await page.goto("http://localhost:8000");

  await page.fill(
    '[data-testid="login-email-input"]',
    "sarah.johnson@testbook.com"
  );
  await page.fill('[data-testid="login-password-input"]', "Sarah2024!");
  await page.click('[data-testid="login-submit-button"]');

  await expect(page.locator('[data-testid="navbar"]')).toBeVisible();
  await expect(page.locator('[data-testid="navbar-username"]')).toContainText(
    "Sarah Johnson"
  );
});
```

#### Create Post Test

```javascript
test("user can create a post", async ({ page }) => {
  // Login first
  await loginAs(page, "sarah.johnson@testbook.com", "Sarah2024!");

  // Create post
  await page.fill('[data-testid="create-post-textarea"]', "My test post");
  await page.click('[data-testid="create-post-submit-button"]');

  // Verify post appears
  await expect(page.locator('[data-testid^="post-"]').first()).toContainText(
    "My test post"
  );
});
```

#### Upload Media Test

```javascript
test("user can create post with uploaded image", async ({ page }) => {
  await loginAs(page, "sarah.johnson@testbook.com", "Sarah2024!");

  // Fill in post content
  await page.fill('[data-testid="create-post-textarea"]', "Post with image");

  // Upload file via file picker
  await page.setInputFiles(
    '[data-testid="create-post-file-input"]',
    "path/to/test-image.jpg"
  );

  // Verify preview appears
  await expect(
    page.locator('[data-testid="create-post-preview"]')
  ).toBeVisible();

  // Submit post
  await page.click('[data-testid="create-post-submit-button"]');

  // Verify post appears with image
  await expect(page.locator('[data-testid^="post-"]').first()).toContainText(
    "Post with image"
  );
});
```

#### Edit Post Test

```javascript
test("user can edit their own post", async ({ page }) => {
  await loginAs(page, "sarah.johnson@testbook.com", "Sarah2024!");

  // Click 3-dot menu on first post
  await page.click('[data-testid="post-1-menu-button"]');

  // Click edit
  await page.click('[data-testid="post-1-edit-button"]');

  // Verify edit form appears
  await expect(page.locator('[data-testid="post-1-edit-form"]')).toBeVisible();

  // Edit content
  await page.fill('[data-testid="post-1-edit-textarea"]', "Updated content");
  await page.click('[data-testid="post-1-save-button"]');

  // Verify updated
  await expect(page.locator('[data-testid="post-1-content"]')).toContainText(
    "Updated content"
  );
});
```

#### Toggle Reaction Test

```javascript
test("user can toggle reactions", async ({ page }) => {
  await loginAs(page, "sarah.johnson@testbook.com", "Sarah2024!");

  // Hover over react button to show dropdown
  await page.hover('[data-testid="post-1-react-button"]');

  // Click like emoji
  await page.click('[data-testid="post-1-reaction-like"]');

  // Verify reaction is active
  await expect(
    page.locator('[data-testid="post-1-react-button"]')
  ).toContainText("👍");

  // Click again to remove
  await page.hover('[data-testid="post-1-react-button"]');
  await page.click('[data-testid="post-1-reaction-like"]');

  // Verify reaction removed
  await expect(
    page.locator('[data-testid="post-1-react-button"]')
  ).toContainText("React");
});
```

#### Followers/Following Pages Test

```javascript
test("user can view and manage followers", async ({ page }) => {
  await loginAs(page, "sarah.johnson@testbook.com", "Sarah2024!");

  // Go to own profile
  await page.click('[data-testid="navbar-profile-link"]');

  // Click followers count
  await page.click('[data-testid="profile-followers-link"]');

  // Verify on followers page
  await expect(page.locator('[data-testid="followers-page"]')).toBeVisible();

  // Block a follower (if any exist)
  const blockButton = page.locator('[data-testid$="-block-button"]').first();
  if (await blockButton.isVisible()) {
    await blockButton.click();
  }

  // Navigate to following page
  await page.click('[data-testid="navbar-profile-link"]');
  await page.click('[data-testid="profile-following-link"]');

  // Verify on following page
  await expect(page.locator('[data-testid="following-page"]')).toBeVisible();

  // Unfollow someone (if any exist)
  const unfollowButton = page
    .locator('[data-testid$="-unfollow-button"]')
    .first();
  if (await unfollowButton.isVisible()) {
    await unfollowButton.click();
  }
});
```

#### Profile Picture Upload Test

```javascript
test("user can upload profile picture", async ({ page }) => {
  await loginAs(page, "sarah.johnson@testbook.com", "Sarah2024!");

  // Go to settings
  await page.click('[data-testid="navbar-settings-link"]');

  // Upload avatar
  await page.setInputFiles(
    '[data-testid="settings-avatar-input"]',
    "path/to/avatar.jpg"
  );

  // Wait for upload to complete
  await page.waitForTimeout(1000);

  // Verify success message
  await expect(page.locator('[data-testid="settings-success"]')).toContainText(
    "updated successfully"
  );

  // Go to profile
  await page.click('[data-testid="navbar-profile-link"]');

  // Verify new avatar is shown
  await expect(page.locator('[data-testid="profile-avatar"]')).toBeVisible();
});
```

### Selenium Examples

#### Python + Selenium

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_login():
    driver = webdriver.Chrome()
    driver.get("http://localhost:8000")

    # Login
    email_input = driver.find_element(By.CSS_SELECTOR, '[data-testid="login-email-input"]')
    email_input.send_keys("sarah.johnson@testbook.com")

    password_input = driver.find_element(By.CSS_SELECTOR, '[data-testid="login-password-input"]')
    password_input.send_keys("Sarah2024!")

    submit_button = driver.find_element(By.CSS_SELECTOR, '[data-testid="login-submit-button"]')
    submit_button.click()

    # Wait for navigation
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="navbar"]'))
    )

    # Verify logged in
    username = driver.find_element(By.CSS_SELECTOR, '[data-testid="navbar-username"]')
    assert "Sarah Johnson" in username.text

    driver.quit()
```

### Cypress Examples

```javascript
describe("Testbook Tests", () => {
  beforeEach(() => {
    // Reset database
    cy.request("POST", "http://localhost:8000/api/dev/reset");
    cy.visit("/");
  });

  it("should login successfully", () => {
    cy.get('[data-testid="login-email-input"]').type(
      "sarah.johnson@testbook.com"
    );
    cy.get('[data-testid="login-password-input"]').type("Sarah2024!");
    cy.get('[data-testid="login-submit-button"]').click();

    cy.get('[data-testid="navbar"]').should("be.visible");
    cy.get('[data-testid="navbar-username"]').should(
      "contain",
      "Sarah Johnson"
    );
  });

  it("should create and interact with post", () => {
    // Login
    cy.login("sarah.johnson@testbook.com", "Sarah2024!");

    // Create post
    cy.get('[data-testid="create-post-textarea"]').type("Test post");
    cy.get('[data-testid="create-post-submit-button"]').click();

    // React to post
    cy.get('[data-testid^="post-"]')
      .first()
      .within(() => {
        cy.get('[data-testid$="-react-button"]').click();
        cy.get('[data-testid$="-reaction-like"]').click();
      });

    // Verify reaction
    cy.get('[data-testid^="post-"]').first().should("contain", "like");
  });
});
```

## Test Scenarios

### Scenario 1: Complete User Journey

**Goal:** Test full user lifecycle from registration to account deletion

```gherkin
Feature: User Lifecycle
  Scenario: New user complete journey
    Given I am on the registration page
    When I register with valid credentials
    And I login with my new account
    And I create a post
    And I follow another user
    And I view their profile
    And I go to settings
    And I change my theme to dark
    Then I should see dark mode applied
    When I delete my account
    Then I should be logged out
    And I cannot login with old credentials
```

### Scenario 2: Social Interactions

**Goal:** Test user interactions (follow, block, react, comment)

1. **Login as User A** (Sarah)
2. **Follow User B** (Mike)
3. **View User B's profile**
4. **React to User B's post** (like)
5. **Comment on User B's post**
6. **Block User C** (Alex)
7. **Verify User C's posts don't appear** in feed
8. **Unblock User C**
9. **Verify User C's posts reappear**

### Scenario 3: Feed Filtering

**Goal:** Test feed "See All" vs "Following" filtering

```python
def test_feed_filtering():
    # Login as user with specific following list
    token = login("sarah.johnson@testbook.com", "Sarah2024!")
    headers = {"Authorization": f"Bearer {token}"}

    # Get "See All" feed
    all_feed = requests.get(f"{BASE_URL}/feed/all", headers=headers)
    all_posts = all_feed.json()

    # Get "Following" feed
    following_feed = requests.get(f"{BASE_URL}/feed/following", headers=headers)
    following_posts = following_feed.json()

    # Assertions
    assert len(all_posts) > len(following_posts)

    # Verify following feed only contains posts from followed users
    sarah_following = ["mikechen", "emmadavis", "lisawilliams"]
    for post in following_posts:
        assert post["author_username"] in sarah_following
```

### Scenario 4: Post Interactions

**Goal:** Test complete post lifecycle

1. **Create post** with image
2. **Verify post appears** in feed
3. **Add multiple reactions** (like, love, wow)
4. **Add comments** from different users
5. **Repost the post**
6. **Verify repost appears** in feed
7. **Delete original post**
8. **Verify both post and repost are gone**

### Scenario 5: Theme & Settings

**Goal:** Test user preferences persistence

```javascript
test("theme persists across sessions", async ({ page, context }) => {
  // Login and change theme
  await loginAs(page, "sarah.johnson@testbook.com", "Sarah2024!");
  await page.goto("/settings");
  await page.selectOption('[data-testid="settings-theme-select"]', "dark");
  await page.click('[data-testid="settings-save-button"]');

  // Verify dark theme applied
  await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");

  // Logout and login again
  await page.click('[data-testid="navbar-logout-button"]');
  await loginAs(page, "sarah.johnson@testbook.com", "Sarah2024!");

  // Verify theme persisted
  await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
});
```

## Performance Testing

### Load Test Example (K6)

```javascript
import http from "k6/http";
import { check, sleep } from "k6";

export let options = {
  vus: 10,
  duration: "30s",
};

export default function () {
  // Login
  let loginRes = http.post(
    "http://localhost:8000/api/auth/login",
    JSON.stringify({
      email: "sarah.johnson@testbook.com",
      password: "Sarah2024!",
    }),
    { headers: { "Content-Type": "application/json" } }
  );

  check(loginRes, { "login successful": (r) => r.status === 200 });

  let token = loginRes.json("access_token");
  let headers = { Authorization: `Bearer ${token}` };

  // Get feed
  let feedRes = http.get("http://localhost:8000/api/feed/all", { headers });
  check(feedRes, { "feed loaded": (r) => r.status === 200 });

  sleep(1);
}
```

## Test Data Management

### Creating Custom Test Data

```python
# Use dev API to create specific scenarios
def setup_test_scenario():
    # Reset database
    requests.post(f"{BASE_URL}/dev/reset")

    # Get test users
    users = requests.get(f"{BASE_URL}/dev/users").json()
    sarah = next(u for u in users if u["username"] == "sarahjohnson")

    # Create specific test posts
    requests.post(f"{BASE_URL}/dev/create-post", json={
        "user_id": sarah["id"],
        "content": "Specific test post for scenario",
        "image_url": "/static/images/test-image.jpg"
    })
```

### Cleanup After Tests

```python
def teardown_tests():
    # Reset to clean state
    requests.post(f"{BASE_URL}/dev/reset")
```

## Tips & Best Practices

1. **Reset data between tests**: Use `./reset-database.sh` or `/api/dev/reset` endpoint
2. **Use data-testid attributes**: All elements have test IDs
3. **Wait for network requests**: Posts, comments may have slight delays
4. **Test with different users**: Verify permissions and visibility
5. **Check both UI and API**: Ensure consistency
6. **Test edge cases**: Empty feeds, blocked users, deleted content
7. **Verify error messages**: Test invalid inputs
8. **Test responsiveness**: Try different viewport sizes
9. **Check accessibility**: Use screen reader testing
10. **Monitor performance**: Check load times

## Common Test Patterns

### Page Object Model (POM)

```javascript
class LoginPage {
  constructor(page) {
    this.page = page;
    this.emailInput = '[data-testid="login-email-input"]';
    this.passwordInput = '[data-testid="login-password-input"]';
    this.submitButton = '[data-testid="login-submit-button"]';
  }

  async login(email, password) {
    await this.page.fill(this.emailInput, email);
    await this.page.fill(this.passwordInput, password);
    await this.page.click(this.submitButton);
  }
}
```

### API Helper Functions

```python
class TestbookAPI:
    def __init__(self, base_url="http://localhost:8000/api"):
        self.base_url = base_url
        self.token = None

    def login(self, email, password):
        response = requests.post(f"{self.base_url}/auth/login",
            json={"email": email, "password": password})
        self.token = response.json()["access_token"]
        return self.token

    def create_post(self, content, image_url=None):
        return requests.post(
            f"{self.base_url}/posts/",
            json={"content": content, "image_url": image_url},
            headers={"Authorization": f"Bearer {self.token}"}
        )
```

## Debugging Tips

1. **Check API responses**: <http://localhost:8000/docs>
2. **View browser console**: Look for errors
3. **Check network tab**: Monitor API calls
4. **Use verbose logging**: Enable in test framework
5. **Take screenshots**: On test failures
6. **Check database state**: Via dev endpoints

---

## 📚 More Resources

- **[README.md](../../README.md)** - Main documentation and project overview
- **[TESTING_PATTERNS.md](../reference/TESTING_PATTERNS.md)** - Testing dynamic content patterns
- **[TESTING_CHEATSHEET.md](../reference/TESTING_CHEATSHEET.md)** - Quick reference guide
- **[TESTING_FEATURES.md](../reference/TESTING_FEATURES.md)** - All testable features
- **[README.md](../../README.md#quick-start-5-minutes)** - Get started quickly

---

**Happy Testing! 🧪**
