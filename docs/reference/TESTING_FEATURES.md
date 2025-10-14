# 🧪 Testbook Testing Features

## Overview

Testbook is purpose-built for QA automation testing practice. Every feature is designed with testability in mind.

## ✅ Test-Friendly Design

### 1. **Comprehensive Test IDs (138+ data-testid attributes)**

Every interactive element has a unique `data-testid` attribute for reliable element selection:

```javascript
// Easy element selection
await page.click('[data-testid="profile-edit-button"]');
await page.fill('[data-testid="create-post-textarea"]', 'Test content');
```

**For dynamic content** (posts, comments, followers), we provide **both specific and generic selectors**:

```javascript
// Generic - when you don't know the ID
await page.locator('[data-testid-generic="post-item"]').first();

// Specific - when you know the ID (e.g., from API response)
await page.click('[data-testid="post-1-react-button"]');

// Filter by attributes
await page.locator('[data-is-own-post="true"]').first();
```

📖 **See [TESTING_PATTERNS.md](TESTING_PATTERNS.md) for complete guide on testing dynamic content!**

### 2. **RESTful API Endpoints**

All features accessible via clean REST API:

- **Authentication**: Register, Login, Get current user
- **Users**: Profiles, Follow/Unfollow, Block/Unblock, Followers/Following lists
- **Posts**: Create, Edit, Delete, Upload media, Repost, Comment, React
- **Feed**: All posts, Following feed
- **Dev**: Reset, Seed, Get test users, Create test posts

### 3. **Dev API for Test Data Management**

```bash
# Reset to clean state
./reset-database.sh  # Works on all platforms

# Or via API
POST /api/dev/reset

# Get test users with passwords
GET /api/dev/users

# Create specific test posts
POST /api/dev/create-post
```

### 4. **Toggle Actions (Like Real Social Media)**

Many actions are toggleable for realistic testing:

- **Reactions**: Click to add, click again to remove (6 emoji types)
- **Reposts**: Click to repost, click again to unrepost
- **Follow**: Click to follow, click again to unfollow
- All actions update counts in real-time

### 5. **File Upload Testing**

Test file uploads with multiple methods:

- **Drag and drop**: Test HTML5 drag-and-drop functionality
- **File picker**: Test standard file input
- **Profile pictures**: Upload custom avatars
- **Post media**: Upload images and videos
- **Validation**: Test file type restrictions

### 6. **Edit Functionality**

Test CRUD operations completely:

- **Posts**: Create, Read, Update (edit), Delete
- **Profiles**: View, Edit, Update avatar
- **Comments**: Create, View
- **Reactions**: Create, Update, Delete

### 7. **Relationship Testing**

Complex user relationships to test:

- Follow/unfollow workflows
- Block/unblock workflows
- Followers and following lists
- Feed filtering based on relationships
- Visibility rules (blocked users hidden)

### 8. **Authentication & Authorization**

Test security and permissions:

- JWT token-based auth
- Protected routes
- Permission checks (can only edit own posts)
- Token expiration
- Auto-login on registration

### 9. **State Management**

Test state updates and persistence:

- Theme persistence (dark/light)
- Text density preference
- User preferences saved
- Logout clears state
- Feed updates after actions

### 10. **Cross-Platform Testing**

Scripts work on all platforms:

- **macOS/Linux**: `.sh` scripts
- **Windows**: `.bat` and `.ps1` scripts
- **Docker**: Universal containerization
- **Development mode**: Hot reload for rapid testing

## 📊 Testing Capabilities

### Frontend Testing

✅ **UI Automation Frameworks**
- Selenium WebDriver
- Playwright
- Cypress
- Puppeteer
- TestCafe

✅ **What You Can Test**
- User registration and login flows
- Post creation with text, images, videos
- File upload via drag-and-drop
- Edit posts inline
- Toggle reactions with emojis
- Add and view comments
- Repost and unrepost
- Follow/unfollow users
- Block/unblock users
- View followers and following
- Upload and change profile pictures
- Theme switching
- Navigation between pages
- Form validation
- Error handling

### Backend Testing

✅ **API Testing Frameworks**
- Postman/Newman
- REST Assured (Java)
- pytest + requests (Python)
- SuperTest (Node.js)
- RestSharp (.NET)

✅ **What You Can Test**
- All CRUD operations on posts
- File upload handling
- User authentication
- Authorization (can't edit others' posts)
- Relationship management
- Feed generation and filtering
- Data validation
- Error responses
- Status codes
- Response schemas

### Performance Testing

✅ **Load Testing Tools**
- K6
- JMeter
- Locust
- Artillery

✅ **What You Can Test**
- Concurrent user logins
- Feed loading performance
- File upload performance
- API response times
- Database query performance

### Security Testing

✅ **What You Can Test**
- JWT token validation
- Protected route access
- Permission checks
- XSS attempts (sanitization)
- SQL injection (ORM protection)
- File upload validation
- User isolation (can't access others' data)

## 🎯 Test Data

### Pre-seeded Data

- **9 test users** with varied profiles
- **21 posts** with different content types
- **Established relationships** (follows, blocks)
- **Comments and reactions** on posts
- **2 reposts** to test repost feature

### Test Accounts

All accounts have **known passwords** for easy testing:

| Email | Password | Use Case |
|-------|----------|----------|
| sarah.johnson@testbook.com | Sarah2024! | Active user with followers |
| mike.chen@testbook.com | MikeRocks88 | User with many posts |
| emma.davis@testbook.com | EmmaLovesPhotos | Photographer with images |
| newuser@testbook.com | NewUser123! | Fresh account, no activity |

### Dynamic Test Data

Create custom scenarios programmatically:

```python
# Reset to clean slate
requests.post(f"{BASE_URL}/dev/reset")

# Create specific test post
requests.post(f"{BASE_URL}/dev/create-post", json={
    "user_id": 1,
    "content": "Test post for scenario",
    "image_url": "/static/images/sunset.jpg"
})
```

## 🔍 Common Test Patterns

### Page Object Model (POM)

```javascript
class FeedPage {
  constructor(page) {
    this.page = page;
    this.createPostInput = '[data-testid="create-post-textarea"]';
    this.submitButton = '[data-testid="create-post-submit-button"]';
    this.allTab = '[data-testid="feed-tab-all"]';
    this.followingTab = '[data-testid="feed-tab-following"]';
  }

  async createPost(content) {
    await this.page.fill(this.createPostInput, content);
    await this.page.click(this.submitButton);
  }

  async switchToFollowing() {
    await this.page.click(this.followingTab);
  }
}
```

### API Test Helper

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

    def create_post(self, content, image_path=None):
        data = {"content": content}

        if image_path:
            # Upload image first
            with open(image_path, 'rb') as f:
                files = {'file': f}
                upload_resp = requests.post(
                    f"{self.base_url}/posts/upload",
                    files=files,
                    headers={"Authorization": f"Bearer {self.token}"}
                )
                data['image_url'] = upload_resp.json()['url']

        return requests.post(
            f"{self.base_url}/posts/",
            json=data,
            headers={"Authorization": f"Bearer {self.token}"}
        )

    def toggle_repost(self, post_id):
        # Check if already reposted
        post = requests.get(f"{self.base_url}/posts/{post_id}",
            headers={"Authorization": f"Bearer {self.token}"}).json()

        if post['has_reposted']:
            # Remove repost
            return requests.delete(f"{self.base_url}/posts/repost/{post_id}",
                headers={"Authorization": f"Bearer {self.token}"})
        else:
            # Create repost
            return requests.post(f"{self.base_url}/posts/repost",
                json={"original_post_id": post_id},
                headers={"Authorization": f"Bearer {self.token}"})
```

## 🎨 UI Testing Best Practices

### 1. Use Data Test IDs

```javascript
// Good - uses test ID
await page.click('[data-testid="login-submit-button"]');

// Bad - uses text or classes (fragile)
await page.click('button:has-text("Submit")');
```

### 2. Wait for Network Requests

```javascript
// Wait for API response
await Promise.all([
  page.waitForResponse(resp => resp.url().includes('/api/posts/')),
  page.click('[data-testid="create-post-submit-button"]')
]);
```

### 3. Test Error States

```javascript
// Test with invalid data
await page.fill('[data-testid="create-post-textarea"]', '');
await page.click('[data-testid="create-post-submit-button"]');
// Button should be disabled
```

### 4. Test File Uploads

```javascript
// Test drag and drop
const dropZone = await page.locator('[data-testid="create-post-drop-zone"]');
await dropZone.setInputFiles('test-image.jpg');
await expect(page.locator('[data-testid="create-post-preview"]')).toBeVisible();
```

## 📈 Test Coverage Recommendations

### Critical Paths (Must Test)
1. User registration → auto-login → create first post
2. Login → create post → logout → login again
3. Upload file → create post → verify media appears
4. React to post → toggle reaction → verify count updates
5. Follow user → verify following feed shows their posts
6. Block user → verify their posts disappear from feed

### Happy Paths
- All CRUD operations on posts
- All user relationship actions
- Profile updates and avatar changes
- Theme and preference changes
- Database reset and reseed

### Negative Tests
- Invalid login credentials
- Duplicate username/email registration
- Upload invalid file types
- Edit/delete others' posts (should fail)
- React without authentication

### Edge Cases
- Empty feeds (no followers, no posts)
- User with no avatar (uses default)
- Repost a repost
- Block someone you're following
- Delete account while logged in

## 🚀 Quick Start for Testers

1. **Start Testbook**:
   ```bash
   ./start-dev.sh    # macOS/Linux
   start-dev.bat     # Windows
   ```

2. **Reset to clean state**:
   ```bash
   ./reset-database.sh    # macOS/Linux
   reset-database.bat     # Windows
   ```

3. **Run your tests**:
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8000
   - API Docs: http://localhost:8000/docs

4. **Check test data**:
   ```bash
   curl http://localhost:8000/api/dev/users
   ```

## 📚 Documentation

- **TESTING_PATTERNS.md** - ⭐ Testing dynamic content (must read!)
- **TESTING_CHEATSHEET.md** - Quick reference card
- **README.md** - Complete feature list and setup
- **TESTING_GUIDE.md** - Detailed test examples
- **QUICKSTART.md** - Get started in 5 minutes
- **PROJECT_INFO.md** - Technical architecture
- **API Docs** - Interactive docs at `/docs` endpoint

## 💡 Why Testbook is Great for Testing

✅ **Realistic** - Behaves like real social media
✅ **Lightweight** - Starts in seconds, no heavy dependencies
✅ **Controllable** - Reset anytime, predictable test data
✅ **Well-documented** - Every endpoint and test ID documented
✅ **Feature-rich** - Real-world complexity without real-world problems
✅ **Test-friendly** - Built for automation from the ground up
✅ **Cross-platform** - Works on macOS, Linux, Windows
✅ **Modern stack** - Practice with current frameworks (FastAPI, React, Vite)

---

## 📚 More Resources

- **[README.md](../../README.md)** - Main documentation and project overview
- **[TESTING_GUIDE.md](../guides/TESTING_GUIDE.md)** - Complete testing examples
- **[TESTING_PATTERNS.md](TESTING_PATTERNS.md)** - Testing dynamic content patterns
- **[TESTING_CHEATSHEET.md](TESTING_CHEATSHEET.md)** - Quick reference guide
- **[QUICKSTART.md](../../QUICKSTART.md)** - Get started in 5 minutes

---

**Happy Testing! 🎉**

