# Testbook API Testing

API testing examples and collections for Testbook.

## Contents

- **Testbook.postman_collection.json** - Postman/Newman collection
- **python_api_examples.py** - Python requests examples
- **README.md** - This file

## Postman Collection

### Prerequisites

- Install [Postman](https://www.postman.com/downloads/) (GUI) or
- Install [Newman](https://www.npmjs.com/package/newman) (CLI)

```bash
npm install -g newman
```

### Using Postman (GUI)

1. Open Postman
2. Click "Import"
3. Select `Testbook.postman_collection.json`
4. Start testing!

### Using Newman (CLI)

```bash
# Run entire collection
newman run Testbook.postman_collection.json

# Run with environment variables
newman run Testbook.postman_collection.json \
  --env-var "baseUrl=http://localhost:8000/api"

# Generate HTML report
newman run Testbook.postman_collection.json \
  --reporters cli,html \
  --reporter-html-export report.html

# Run specific folder
newman run Testbook.postman_collection.json \
  --folder "Authentication"
```

### Collection Structure

- **Authentication** - Register, login, get current user
- **Posts** - CRUD operations, comments, reactions
- **Feed** - All feed, following feed
- **Dev/Testing** - Reset database, seed data

### Environment Variables

The collection uses these variables:

- `{{baseUrl}}` - API base URL (default: http://localhost:8000/api)
- `{{token}}` - JWT token (auto-set after login)
- `{{postId}}` - Created post ID (auto-set)
- `{{userId}}` - Current user ID (auto-set)

## Python Examples

### Prerequisites

```bash
pip install requests
```

### Running Examples

```bash
# Run all examples
python python_api_examples.py

# Use as library
python -c "from python_api_examples import TestbookAPI; api = TestbookAPI(); print(api.get_all_feed())"
```

### Example Usage

```python
from python_api_examples import TestbookAPI

# Initialize API client
api = TestbookAPI()

# Reset database
api.reset_database()

# Login
api.login("sarah.johnson@testbook.com", "Sarah2024!")

# Create post
post = api.create_post("Hello from Python!")
print(f"Created post {post['id']}")

# Get feed
posts = api.get_all_feed()
print(f"Feed has {len(posts)} posts")

# Follow user
api.follow_user("mikechen")

# Add reaction
api.add_reaction(post['id'], 'like')
```

### Available Methods

**Authentication:**
- `register()` - Register new user
- `login()` - Login and get token
- `get_current_user()` - Get authenticated user

**Posts:**
- `create_post()` - Create new post
- `get_post()` - Get post by ID
- `update_post()` - Update post
- `delete_post()` - Delete post
- `add_comment()` - Add comment
- `add_reaction()` - Add/change reaction
- `remove_reaction()` - Remove reaction

**Feed:**
- `get_all_feed()` - Get all posts
- `get_following_feed()` - Get following posts

**Users:**
- `get_user_profile()` - Get user by username
- `update_profile()` - Update own profile
- `follow_user()` - Follow user
- `unfollow_user()` - Unfollow user
- `block_user()` - Block user
- `unblock_user()` - Unblock user

**Dev/Testing:**
- `reset_database()` - Reset to clean state

## Building Your Own Tests

### Using Pytest

```python
# test_testbook_api.py
import pytest
from python_api_examples import TestbookAPI

@pytest.fixture
def api():
    client = TestbookAPI()
    client.reset_database()
    client.login("sarah.johnson@testbook.com", "Sarah2024!")
    return client

def test_create_post(api):
    post = api.create_post("Test post")
    assert post['id'] is not None
    assert post['content'] == "Test post"

def test_follow_user(api):
    result = api.follow_user("mikechen")
    assert "following" in result['message'].lower()
```

Run with:
```bash
pytest test_testbook_api.py -v
```

### Using Requests Directly

```python
import requests

BASE_URL = "http://localhost:8000/api"

# Login
response = requests.post(f"{BASE_URL}/auth/login", json={
    "email": "sarah.johnson@testbook.com",
    "password": "Sarah2024!"
})
token = response.json()["access_token"]

# Authenticated request
headers = {"Authorization": f"Bearer {token}"}
posts = requests.get(f"{BASE_URL}/feed/all", headers=headers)
print(posts.json())
```

## Test Scenarios

### Scenario 1: User Registration Flow

```python
api = TestbookAPI()
api.reset_database()

# Register
user = api.register(
    email="test@example.com",
    username="testuser",
    display_name="Test User",
    password="Test123!"
)

# Should auto-login
me = api.get_current_user()
assert me['email'] == "test@example.com"
```

### Scenario 2: Post Interaction Flow

```python
api = TestbookAPI()
api.login("sarah.johnson@testbook.com", "Sarah2024!")

# Create post
post = api.create_post("Test post")

# React to post
api.add_reaction(post['id'], 'like')

# Add comment
comment = api.add_comment(post['id'], "Great!")

# Verify
retrieved = api.get_post(post['id'])
assert retrieved['reactions_count'] > 0
assert retrieved['comments_count'] > 0
```

### Scenario 3: Follow and Feed

```python
api = TestbookAPI()
api.login("sarah.johnson@testbook.com", "Sarah2024!")

# Get initial following feed
before = api.get_following_feed()

# Follow user
api.follow_user("mikechen")

# Get updated feed
after = api.get_following_feed()

# Should have more posts
assert len(after) >= len(before)
```

## Best Practices

1. **Reset database** before test suites
2. **Use fixtures** for common setup
3. **Check status codes** explicitly
4. **Validate response schemas**
5. **Test error cases** (401, 403, 404, etc.)
6. **Clean up test data** after tests
7. **Use meaningful assertions**

## Error Handling

```python
from python_api_examples import TestbookAPI
import requests

api = TestbookAPI()

try:
    # This will raise exception on error
    api.login("wrong@email.com", "wrongpass")
except requests.exceptions.HTTPError as e:
    print(f"Status code: {e.response.status_code}")
    print(f"Error: {e.response.json()}")
```

## CI/CD Integration

### GitHub Actions Example

```yaml
- name: Run API Tests
  run: |
    newman run tests/api/Testbook.postman_collection.json \
      --reporters cli,json \
      --reporter-json-export results.json
```

### Using in Python Tests

```python
# conftest.py
import pytest
from python_api_examples import TestbookAPI

@pytest.fixture(scope="session")
def api_client():
    client = TestbookAPI()
    client.reset_database()
    return client
```

## Troubleshooting

### Connection Refused

Make sure Testbook is running:
```bash
cd backend
uvicorn main:app --reload
```

### Authentication Errors

Reset database and try again:
```python
api = TestbookAPI()
api.reset_database()
```

### Import Errors

Make sure requests is installed:
```bash
pip install requests
```

## Additional Resources

- [API Documentation](http://localhost:8000/docs) - Interactive Swagger UI
- [ReDoc](http://localhost:8000/redoc) - Alternative API docs
- [Postman Learning](https://learning.postman.com/)
- [Requests Documentation](https://requests.readthedocs.io/)

