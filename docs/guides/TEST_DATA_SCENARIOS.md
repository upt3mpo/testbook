# 🎭 Test Data Scenarios

Guide to using pre-configured test data scenarios for E2E and integration testing.

---

## Overview

Test data scenarios provide consistent, repeatable test data setups for different testing needs. This eliminates manual test data setup and ensures tests start with known states.

---

## Available Scenarios

### 1. `default` (Default)

**What it includes:**
- 8 pre-seeded users with known passwords
- Existing posts and interactions from seed data
- User relationships (followers, etc.)

**Use when:**
- Testing with realistic data
- Most general testing scenarios
- No special setup needed

**Example:**
```javascript
// JavaScript/Playwright
await seedDatabase(page, 'default');  // or just seedDatabase(page)
```

```python
# Python/Playwright
seed_test_data('default')  # or omit parameter
```

---

### 2. `empty`

**What it includes:**
- Clean database with no users
- No posts, no data
- Fresh slate

**Use when:**
- Testing registration flows
- Testing "no data" states
- Need complete control over all data

**Example:**
```javascript
// JavaScript/Playwright
await seedDatabase(page, 'empty');
// Now register your own test users
```

```python
# Python/Playwright
seed_test_data('empty')
# Database is completely empty
```

---

### 3. `minimal`

**What it includes:**
- Basic seeded users (same as default)
- No additional posts
- Clean feed state

**Use when:**
- Testing post creation from scratch
- Need users but not posts
- Testing empty feed states

**Example:**
```javascript
// JavaScript/Playwright
await seedDatabase(page, 'minimal');
// Users exist but feed is empty
```

```python
# Python/Playwright
seed_test_data('minimal')
```

---

### 4. `high_traffic`

**What it includes:**
- All default users
- 6+ additional posts across users
- More interactions and content

**Use when:**
- Testing with busy feeds
- Testing pagination or filtering
- Performance testing UI with data
- Testing "realistic" user experience

**Example:**
```javascript
// JavaScript/Playwright
await seedDatabase(page, 'high_traffic');
// Feed now has many posts
```

```python
# Python/Playwright
result = seed_test_data('high_traffic')
print(f"Created {result['posts_created']} additional posts")
```

---

## Pre-Seeded Users

All scenarios (except `empty`) include these users:

| User | Email | Password | Use For |
|------|-------|----------|---------|
| **Sarah Johnson** | sarah.johnson@testbook.com | Sarah2024! | Primary test user |
| **Mike Chen** | mike.chen@testbook.com | MikeRocks88 | Secondary user, interactions |
| **Emma Davis** | emma.davis@testbook.com | EmmaLovesPhotos | Third user, photo tests |
| **New User** | newuser@testbook.com | NewUser123! | Fresh user, no history |

---

## Usage Examples

### Example 1: Testing Empty States

```javascript
// Test what happens when feed is empty
test('displays empty state message', async ({ page }) => {
  await seedDatabase(page, 'empty');

  // Register a new user (feed will be empty)
  await registerUser(page, {
    email: 'test@example.com',
    username: 'testuser',
    displayName: 'Test User',
    password: 'Test123!'
  });

  // Verify empty state message shows
  await expect(page.locator('text=No posts yet')).toBeVisible();
});
```

### Example 2: Testing with High Traffic

```python
def test_feed_pagination(page, seed_test_data):
    """Test feed loads correctly with many posts"""
    # Seed high traffic scenario
    result = seed_test_data('high_traffic')
    assert result['posts_created'] >= 6

    # Login and check feed
    page.goto('http://localhost:3000')
    # ... test pagination logic
```

### Example 3: Testing Fresh Registration

```javascript
test('new user can register and post', async ({ page }) => {
  await seedDatabase(page, 'empty');

  // Register
  await registerUser(page, {
    email: 'brand.new@test.com',
    username: 'brandnew',
    displayName: 'Brand New',
    password: 'BrandNew123!'
  });

  // Create first post
  await createPost(page, 'My first post!');

  // Verify it appears
  await expect(page.locator('text=My first post!')).toBeVisible();
});
```

---

## Backend Support

### Dev API Endpoints (Require TESTING=true)

**Create Post:**
```bash
POST /api/dev/create-post?user_id=1&content=Hello
```

**Reset Database:**
```bash
POST /api/dev/reset
```

**Seed Database:**
```bash
POST /api/dev/seed
```

**⚠️ Important:** Set `TESTING=true` environment variable to enable these endpoints.

```bash
# Terminal 1: Start backend with test mode
cd backend
TESTING=true uvicorn main:app --reload

# Terminal 2: Run tests
pytest tests/e2e-python/ -v
```

---

## Creating Custom Scenarios

Want to add your own scenario? Here's how:

### JavaScript (test-helpers.js)

```javascript
async function seedDatabase(page, scenario = 'default') {
  await resetDatabase(page);

  if (scenario === 'my_custom_scenario') {
    // Create your custom test data
    await page.request.post(`${BACKEND_URL}/api/dev/create-post`, {
      params: { user_id: 1, content: 'Custom post' }
    });

    // Add more setup as needed
    return;
  }

  // ... existing scenarios
}
```

### Python (conftest.py)

```python
def _seed(scenario: str = "default"):
    if scenario == "my_custom_scenario":
        # Create custom test data
        response = requests.post(
            f"{api_url}/api/dev/create-post",
            params={"user_id": 1, "content": "Custom post"}
        )
        return {"scenario": "my_custom_scenario", "posts": 1}

    # ... existing scenarios
```

---

## Best Practices

### 1. **Choose the Right Scenario**
- Use `empty` for registration tests
- Use `default` for most tests
- Use `high_traffic` for feed/pagination tests
- Use `minimal` when you want to create posts from scratch

### 2. **Reset Between Tests**
- Use session-level reset for faster tests
- Use function-level reset when tests modify data
- Document which scenario each test needs

### 3. **Don't Rely on Order**
- Each test should be independent
- Don't assume data from previous tests
- Always seed the scenario you need

### 4. **Handle Timing**
- Wait for network idle after seeding
- Use proper waits for API calls
- Don't assume instant data availability

---

## Scenario Comparison

| Scenario | Users | Posts | Use Case | Setup Time |
|----------|-------|-------|----------|------------|
| `empty` | 0 | 0 | Registration, clean slate | Fast (~1s) |
| `minimal` | 8 | 0 | Post creation, empty feeds | Fast (~1s) |
| `default` | 8 | ~5 | General testing | Fast (~1s) |
| `high_traffic` | 8 | ~11+ | Feed testing, performance | Medium (~2s) |

---

## Troubleshooting

### Scenario not working?

**Check:**
1. Backend is running with `TESTING=true`
2. Dev endpoints are accessible
3. Network is stable
4. Wait for seeding to complete

**Debug:**
```javascript
// Log scenario result
const result = await seedDatabase(page, 'high_traffic');
console.log('Seeding complete:', result);
```

### Posts not appearing?

**Try:**
- Refresh the page after seeding
- Wait for network idle
- Check backend logs for errors
- Verify `TESTING=true` is set

---

## Learn More

- Backend Dev Endpoints: `backend/routers/dev.py`
- Test Helpers (JavaScript): See E2E test files in `tests/e2e/`
- Test Helpers (Python): `tests/e2e-python/conftest.py`
- [LAB 05: Test Data Management](../../labs/LAB_05_Test_Data_Management.md)

---

*Part of the Testbook Testing Platform*

