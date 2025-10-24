# 🎯 Testbook Testing Cheat Sheet

Quick reference for testers and automation engineers.

> **📖 Testing Dynamic Content?** See [TESTING_PATTERNS.md](../concepts/TESTING_PATTERNS.md) for selecting posts/comments without hardcoded IDs!

## 🧰 Recommended Testing Tools

**New to testing?** Try these beginner-friendly tools:

- **[Playwright](https://playwright.dev/)** - UI testing (JavaScript, Python, Java, .NET)
- **[Postman](https://www.postman.com/)** - API testing (visual interface)
- **[PyTest](https://pytest.org/)** - Python testing framework

**More options**: See [README.md](../../README.md#-testing-frameworks-you-can-use) for a complete list

<h2 id="quick-start">🚀 Quick Start</h2>

```bash
# Start app (choose one)
./start-dev.sh        # macOS/Linux dev mode
start-dev.bat         # Windows dev mode
./start.sh            # macOS/Linux Docker
start.bat             # Windows Docker

# Reset database
./reset-database.sh   # macOS/Linux
reset-database.bat    # Windows
```

**URLs:**<ht<http://localhost:3000>
<http://localhost:8000/api>

- Frontend: <http://localhost:8000/docs>ev) or <http://localhost:8000> (Docker)
- Backend API: <http://localhost:8000/api>
- API Docs: <http://localhost:8000/docs>

## 🔐 Test Accounts

| <sarah.johnson@testbook.com> |
|-<mike.chen@testbook.com>-----|
| <emma.davis@testbook.com>.com> | Sarah2024! | Active, has followers |
| <newuser@testbook.com>com> | MikeRocks88 | Many posts |
| <emma.davis@testbook.com> | EmmaLovesPhotos | Photographer |
| <newuser@testbook.com> | NewUser123! | Clean account |

<h2 id="common-test-ids">🎯 Common Test IDs</h2>

### For Dynamic Content (When You Don't Know the ID)

```javascript
// Use generic selectors!
[data-testid-generic="post-item"]        // All posts
[data-testid-generic="comment-item"]     // All comments
[data-testid-generic="follower-item"]    // All followers
[data-testid-generic="following-item"]   // All following

// Then use .first(), .last(), .nth(n)
page.locator('[data-testid-generic="post-item"]').first()

// Or filter by attributes
[data-is-own-post="true"]                // Your posts only
[data-post-author="username"]            // Posts by user
[data-author="username"]                 // Comments by user
```

See **[TESTING_PATTERNS.md](../concepts/TESTING_PATTERNS.md)** for complete guide!

### Authentication

```text
login-email-input, login-password-input, login-submit-button
register-email-input, register-username-input, register-submit-button

```

### Navigation

```text
navbar, navbar-home-link, navbar-profile-link

navbar-settings-link, navbar-logout-button
```

### Posts (replace {id} with post ID)

```text
post-{id}                      # Post container
post-{id}-content              # Post text
post-{id}-react-button         # Reaction dropdown
post-{id}-reaction-like        # Like emoji button
post-{id}-comment-button       # Comment button
post-{id}-repost-button        # Repost/Unrepost toggle
post-{id}-menu-button          # 3-dot menu (own posts)

post-{id}-edit-button          # Edit option
post-{id}-delete-button        # Delete option
```

### Create Post

```text
create-post-textarea           # Text input

create-post-drop-zone          # Drag & drop area
create-post-media-button       # Upload button
create-post-submit-button      # Post button
```

### Profile

```text
profile-display-name           # User's name

profile-followers-link         # Click to see followers
profile-following-link         # Click to see following
profile-follow-button          # Follow/Unfollow
profile-edit-button            # Edit profile (own profile)
```

### Settings

```text
settings-avatar-input          # Avatar upload
settings-upload-avatar-button  # Upload photo button

settings-clear-avatar-button   # Clear photo button
settings-display-name-input    # Name field
settings-bio-input             # Bio field
settings-theme-select          # Theme dropdown
settings-save-button           # Save button
```

### Followers/Following

```text
followers-list                 # Followers container
follower-{id}-block-button     # Block follower
following-list                 # Following container
following-{id}-unfollow-button # Unfollow user
```

## 📡 Key API Endpoints

### Auth

```bash
POST /api/auth/register  # Auto-login on success
POST /api/auth/login     # Returns JWT token
GET  /api/auth/me        # Get current user
```

### Posts

```bash
POST   /api/posts/                    # Create post
POST   /api/posts/upload              # Upload media file

PUT    /api/posts/{id}                # Edit post
DELETE /api/posts/{id}                # Delete post
POST   /api/posts/repost              # Create repost
DELETE /api/posts/repost/{id}         # Remove repost
POST   /api/posts/{id}/reactions      # Add/change reaction
DELETE /api/posts/{id}/reactions      # Remove reaction
POST   /api/posts/{id}/comments       # Add comment
GET    /api/posts/{id}                # Get post details
```

### Users

```bash
GET    /api/users/{username}             # Get profile

GET    /api/users/{username}/followers   # Get followers list
GET    /api/users/{username}/following   # Get following list
GET    /api/users/{username}/posts       # Get user's posts
PUT    /api/users/me                     # Update profile
POST   /api/users/me/upload-avatar       # Upload avatar
POST   /api/users/{username}/follow      # Follow user

DELETE /api/users/{username}/follow      # Unfollow user
POST   /api/users/{username}/block       # Block user
DELETE /api/users/{username}/block       # Unblock user
```

### Feed

```bash
GET /api/feed/all        # All posts
GET /api/feed/following  # Following feed only
```

### Dev/Testing

```bash
POST /api/dev/reset        # Full database reset
POST /api/dev/seed         # Add more seed data
GET  /api/dev/users        # Get all users + passwords
POST /api/dev/create-post  # Create test post
```

<h2 id="quick-test-examples">🧪 Quick Test Examples</h2>

### Playwright

```javascript
// Login
await page.goto("http://localhost:3000");
await page.fill(
  '[data-testid="login-email-input"]',
  "sarah.johnson@testbook.com"
);
await page.fill('[data-testid="login-password-input"]', "Sarah2024!");
await page.click('[data-testid="login-submit-button"]');

// Create post
await page.fill('[data-testid="create-post-textarea"]', "Test post");
await page.click('[data-testid="create-post-submit-button"]');

// React to first post (most recent) - no hardcoded ID!
const firstPost = page.locator('[data-testid-generic="post-item"]').first();
await firstPost.locator('[data-testid$="-react-button"]').hover();
await firstPost.locator('[data-testid$="-reaction-like"]').click();

// Edit your own post
const ownPost = page.locator('[data-is-own-post="true"]').first();
await ownPost.locator('[data-testid$="-menu-button"]').click();
await ownPost.locator('[data-testid$="-edit-button"]').click();
await ownPost.locator('[data-testid$="-edit-textarea"]').fill("Edited");
await ownPost.locator('[data-testid$="-save-button"]').click();
```

### Python + Requests

```python
import requests

BASE_URL = "http://localhost:8000/api"

# Login
login_resp = requests.post(f"{BASE_URL}/auth/login", json={
    "email": "sarah.johnson@testbook.com",
    "password": "Sarah2024!"
})
token = login_resp.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Create post
post_resp = requests.post(f"{BASE_URL}/posts/",
    json={"content": "Test post"},
    headers=headers)

# Upload and post image
with open('test.jpg', 'rb') as f:
    upload_resp = requests.post(f"{BASE_URL}/posts/upload",
        files={'file': f}, headers=headers)

image_url = upload_resp.json()['url']
requests.post(f"{BASE_URL}/posts/",
    json={"content": "With image", "image_url": image_url},
    headers=headers)

# Follow user
requests.post(f"{BASE_URL}/users/mikechen/follow", headers=headers)
```

### Cypress

```javascript
describe("Testbook Tests", () => {
  beforeEach(() => {
    cy.request("POST", "http://localhost:8000/api/dev/reset");
    cy.visit("/");
  });

  it("should create post with file upload", () => {
    cy.get('[data-testid="login-email-input"]').type(
      "sarah.johnson@testbook.com"
    );
    cy.get('[data-testid="login-password-input"]').type("Sarah2024!");
    cy.get('[data-testid="login-submit-button"]').click();

    cy.get('[data-testid="create-post-textarea"]').type("Post with image");
    cy.get('[data-testid="create-post-file-input"]').attachFile(
      "test-image.jpg"
    );
    cy.get('[data-testid="create-post-submit-button"]').click();

    cy.get('[data-testid^="post-"]')
      .first()
      .should("contain", "Post with image");
  });
});
```

<h2 id="reset-commands">🔄 Reset Commands</h2>

| Platform    | Command                                            |
| ----------- | -------------------------------------------------- |
| macOS/Linux | `./reset-database.sh`                              |
| Windows CMD | `reset-database.bat`                               |
| Windows PS  | `.\reset-database.ps1`                             |
| API         | `curl -X POST http://localhost:8000/api/dev/reset` |

## 🔧 Backend Testing (PyTest)

### Setup

```bash
cd backend
pip install pytest pytest-asyncio httpx
pytest  # Run all tests
```

### Unit Test Example

```python
# Test password hashing
from auth import get_password_hash, verify_password

def test_password_hashing():
    password = "Test123!"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed) is True
```

### Integration Test Example

```python
# Test API endpoint
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_login():
    response = client.post("/api/auth/login", json={
        "email": "sarah.johnson@testbook.com",
        "password": "Sarah2024!"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
```

**Full backend testing guide**: [TESTING_GUIDE.md#backend-testing](../guides/TESTING_GUIDE.md#backend-testing)

## 📊 What Makes This Great for Testing

✅ **138+ unique test IDs** - Every element selectable
✅ **RESTful API** - All features accessible via HTTP
✅ **File uploads** - Te<http://localhost:8000/docs>
✅ **Toggle actions** - Test state changes (react, repost, follow)
✅ **Emoji reactions** - Test visual feedback
✅ **Edit functionality** - Test inline editing
✅ **Real-time updates** - Test feed refreshes
✅ **Authentication** - Test JWT flows
✅ **Authorization** - Test permission checks
✅ **Relationships** - Test complex user interactions
✅ **Easy reset** - Clean slate anytime
✅ **Pre-seeded data** - Consistent test scenarios
✅ **Cross-platform** - Test on any OS

## 🐛 Debugging Tips

1. **Check API docs**: <http://localhost:8000/docs>
2. **View network tab**: Monitor API calls in browser
3. **Check backend logs**: See request/response in terminal
4. **Reset database**: Clean state if data gets messy

## 📖 More Resources

- **[TESTING_PATTERNS.md](../concepts/TESTING_PATTERNS.md)** - ⭐ How to handle dynamic content (posts, comments, etc.)
- **[TESTING_GUIDE.md](../guides/TESTING_GUIDE.md)** - Detailed examples (UI, API, Backend)
  - [Backend Testing Section](../guides/TESTING_GUIDE.md#backend-testing) - Unit & integration tests
- **[TESTING_FEATURES.md](TESTING_FEATURES.md)** - Comprehensive testing capabilities
- **[README.md](../../README.md)** - Full feature documentation
- **API Docs** - Interactive API documentation at `/docs`

---

## ⚠️ CRITICAL: Essential Patterns (From Real Testbook Fixes)

### 1. Always Handle Browser Dialogs

**Problem:** `window.confirm()` and `window.alert()` block test execution!

**Solution:**

```javascript
// Add to test-helpers.js
function setupDialogHandler(page) {
  page.on("dialog", async (dialog) => {
    console.log(`Auto-accepting ${dialog.type()}: ${dialog.message()}`);
    await dialog.accept();
  });
}

// Call in every test file's beforeEach
test.beforeEach(async ({ page }) => {
  setupDialogHandler(page); // Essential!
  // ... rest of setup
});
```

**This fixed 5 Testbook tests** (block, unblock, delete account, edit post)

### 2. Verify Test IDs Match Code

Before writing tests, check the actual frontend code for test IDs:

```javascript
// ❌ BAD: Assuming test ID exists
await page.locator('[data-testid="followers-count"]').click();

// ✅ GOOD: Verify in code first
await page.locator('[data-testid="profile-followers-link"]').click();
```

### 3. Use Force Clicks for Dropdowns

For menus with click-outside handlers:

```javascript
await page.click('[data-testid="menu-button"]');
await page.locator('[data-testid="edit-button"]').click({ force: true });
```

### 4. Wait for State Changes, Not Time

```javascript
// ❌ BAD
await button.click();
await page.waitForTimeout(1000);

// ✅ GOOD
await button.click();
await expect(button).toContainText("Updated", { timeout: 10000 });
```

### 5. Retry Complex Interactions

For hover menus that are unreliable:

```javascript
let clicked = false;
for (let i = 0; i < 3 && !clicked; i++) {
  try {
    await reactButton.hover({ force: true });
    await page.waitForTimeout(500);
    await reactionBtn.click({ force: true });
    clicked = true;
  } catch (e) {
    if (i === 2) throw e;
  }
}
```

**These patterns took Testbook from 87% → 100% test pass rate!**

---

**Quick tip**: Read [TESTING_PATTERNS.md](../concepts/TESTING_PATTERNS.md) first if you're testing dynamic content! 🔖

**See also**: [docs/guides/FLAKY_TESTS_GUIDE.md](../guides/FLAKY_TESTS_GUIDE.md) for detailed examples and fixes
