# 🧪 Lab 4B: Advanced E2E Testing with Playwright (Python)

**Estimated Time:** 120 minutes
**Difficulty:** Advanced
**Language:** 🐍 Python
**Prerequisites:** Lab 4 (E2E Python) completed

**What This Adds:** This lab builds on Lab 4 by introducing professional patterns like Page Object Model, advanced fixtures, network stubbing, and pytest markers.

---

## 🎯 What You'll Learn

- **Page Object Model (POM)** - Reusable page helpers
- **Advanced pytest fixtures** - Custom test setup
- **Network interception** - Mock API responses
- **Pytest markers** - Organize test runs (smoke vs regression)
- **Screenshot assertions** - Visual verification
- **Selective waits** - Smart waiting strategies
- **Data builders** - Clean test data creation

---

## 📋 Step-by-Step Instructions

### Part 1: Page Object Model (45 minutes)

The Page Object Model organizes your test code by putting page-specific logic in reusable classes.

#### Step 1: Create Your First Page Object

Create `tests/e2e-python/pages/__init__.py` (empty file):

```bash
cd tests/e2e-python
mkdir -p pages
touch pages/__init__.py
```

Create `tests/e2e-python/pages/feed_page.py`:

```python
"""Page Object for the Feed page"""

from playwright.sync_api import Page, expect


class FeedPage:
    """Reusable helpers for interacting with the feed."""

    def __init__(self, page: Page) -> None:
        self.page = page

        # Selectors
        self.create_post_textarea = '[data-testid="create-post-textarea"]'
        self.create_post_submit = '[data-testid="create-post-submit"]'
        self.post_items = '[data-testid-generic="post-item"]'

    def goto(self) -> None:
        """Navigate to the feed page."""
        self.page.goto("http://localhost:3000")
        expect(self.page.locator('[data-testid="navbar"]')).to_be_visible()

    def create_post(self, content: str) -> None:
        """Create a new post."""
        self.page.fill(self.create_post_textarea, content)
        self.page.click(self.create_post_submit)

        # Wait for post to appear
        self.page.wait_for_timeout(500)
        expect(self.first_post()).to_contain_text(content)

    def first_post(self):
        """Get the first (most recent) post."""
        return self.page.locator(self.post_items).first

    def all_posts(self):
        """Get all posts."""
        return self.page.locator(self.post_items)

    def post_count(self) -> int:
        """Count visible posts."""
        return self.all_posts().count()

    def find_post_by_content(self, content: str):
        """Find a post by its content text."""
        return self.page.locator(self.post_items, has_text=content)

    def delete_first_post(self) -> None:
        """Delete the first post (must be your own)."""
        first = self.first_post()
        first.locator('[data-testid$="-delete-button"]').click()
        self.page.wait_for_timeout(500)
```

#### Step 2: Create Profile Page Object

Create `tests/e2e-python/pages/profile_page.py`:

```python
"""Page Object for the Profile page"""

from playwright.sync_api import Page, expect


class ProfilePage:
    """Reusable helpers for interacting with user profiles."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def goto(self, username: str) -> None:
        """Navigate to a user's profile."""
        self.page.goto(f"http://localhost:3000/profile/{username}")
        expect(self.page.locator('[data-testid="profile-username"]')).to_be_visible()

    def follow_user(self) -> None:
        """Click the follow button."""
        self.page.click('[data-testid="profile-follow-button"]')
        self.page.wait_for_timeout(300)

    def unfollow_user(self) -> None:
        """Click the unfollow button."""
        self.page.click('[data-testid="profile-unfollow-button"]')
        self.page.wait_for_timeout(300)

    def is_following(self) -> bool:
        """Check if currently following this user."""
        return self.page.locator('[data-testid="profile-unfollow-button"]').is_visible()

    def get_follower_count(self) -> int:
        """Get the number of followers."""
        text = self.page.locator('[data-testid="profile-followers-count"]').inner_text()
        return int(text)

    def get_following_count(self) -> int:
        """Get the number of following."""
        text = self.page.locator('[data-testid="profile-following-count"]').inner_text()
        return int(text)

    def get_post_count(self) -> int:
        """Get the number of posts on profile."""
        return self.page.locator('[data-testid-generic="post-item"]').count()
```

#### Step 3: Use Page Objects in Tests

Create `tests/e2e-python/test_page_objects.py`:

```python
"""Example tests using Page Object Model"""

import pytest
from playwright.sync_api import Page

from pages.feed_page import FeedPage
from pages.profile_page import ProfilePage


@pytest.mark.pom
class TestPageObjectExamples:
    """Tests demonstrating Page Object Model pattern"""

    def test_create_post_with_pom(self, page: Page, login_as, fresh_database):
        """Test creating a post using Page Object Model."""
        login_as("sarah")

        # Use FeedPage
        feed = FeedPage(page)
        feed.goto()

        post_content = "Testing with Page Objects!"
        feed.create_post(post_content)

        # Verify post exists
        assert feed.post_count() >= 1
        assert post_content in feed.first_post().inner_text()

    def test_follow_user_with_pom(self, page: Page, login_as, fresh_database):
        """Test following a user using Page Object Model."""
        login_as("sarah")

        # Go to Mike's profile
        profile = ProfilePage(page)
        profile.goto("mikechen")

        # Get initial counts
        initial_followers = profile.get_follower_count()

        # Follow user
        profile.follow_user()

        # Verify follow worked
        assert profile.is_following() is True
        assert profile.get_follower_count() == initial_followers + 1

    def test_complete_workflow_with_pom(self, page: Page, login_as, fresh_database):
        """Test complete workflow: create post → view profile → follow."""
        login_as("sarah")

        # Create a post
        feed = FeedPage(page)
        feed.goto()
        feed.create_post("Check out my profile!")

        # View own profile
        profile = ProfilePage(page)
        profile.goto("sarahjohnson")

        # Verify post appears on profile
        assert profile.get_post_count() >= 1
```

**🎯 Checkpoint:** Run `HEADLESS=false pytest test_page_objects.py -v -m pom`

---

### Part 2: Advanced Fixtures (30 minutes)

Create custom fixtures to simplify test setup.

Create `tests/e2e-python/advanced_conftest.py`:

```python
"""Advanced fixtures for E2E tests"""

import pytest
from playwright.sync_api import Page

from pages.feed_page import FeedPage
from pages.profile_page import ProfilePage


@pytest.fixture
def feed_page(page: Page) -> FeedPage:
    """Fixture that provides a FeedPage instance."""
    return FeedPage(page)


@pytest.fixture
def profile_page(page: Page) -> ProfilePage:
    """Fixture that provides a ProfilePage instance."""
    return ProfilePage(page)


@pytest.fixture
def authenticated_feed(page: Page, login_as) -> FeedPage:
    """Fixture that logs in and returns a FeedPage."""
    login_as("sarah")
    feed = FeedPage(page)
    feed.goto()
    return feed


@pytest.fixture
def create_test_posts(authenticated_feed: FeedPage):
    """Fixture that creates multiple test posts."""
    def _create_posts(count: int = 3, prefix: str = "Test post"):
        posts = []
        for i in range(count):
            content = f"{prefix} {i+1}"
            authenticated_feed.create_post(content)
            posts.append(content)
        return posts

    return _create_posts


@pytest.fixture(params=["sarah", "mike", "emma"])
def any_user(request, login_as):
    """Parametrized fixture that runs test with different users."""
    user_key = request.param
    login_as(user_key)
    return user_key
```

Add to `conftest.py`:

```python
# At the end of conftest.py
pytest_plugins = ["advanced_conftest"]
```

Create `tests/e2e-python/test_advanced_fixtures.py`:

```python
"""Tests using advanced fixtures"""

import pytest
from pages.feed_page import FeedPage


@pytest.mark.fixtures
class TestAdvancedFixtures:
    """Demonstrate advanced fixture patterns"""

    def test_with_feed_page_fixture(self, authenticated_feed: FeedPage, fresh_database):
        """Test using the authenticated_feed fixture."""
        # Already logged in and on feed page!
        authenticated_feed.create_post("Using fixture!")
        assert authenticated_feed.post_count() >= 1

    def test_with_multiple_posts(self, authenticated_feed: FeedPage, create_test_posts, fresh_database):
        """Test with multiple pre-created posts."""
        posts = create_test_posts(count=5, prefix="Fixture post")

        # Verify all posts created
        assert authenticated_feed.post_count() >= 5

        # Verify specific posts exist
        for post_content in posts:
            assert authenticated_feed.find_post_by_content(post_content).is_visible()

    def test_runs_with_each_user(self, any_user, feed_page: FeedPage, fresh_database):
        """This test runs 3 times - once for each user!"""
        feed_page.goto()
        feed_page.create_post(f"Posted by {any_user}")

        # Each user can create posts
        assert feed_page.post_count() >= 1
```

**🎯 Checkpoint:** Run `HEADLESS=false pytest test_advanced_fixtures.py -v -m fixtures`

---

### Part 3: Network Interception (20 minutes)

Mock API responses to test different scenarios.

Create `tests/e2e-python/test_network.py`:

```python
"""Tests using network interception"""

import json
import pytest
from playwright.sync_api import Page, Route


@pytest.mark.network
class TestNetworkInterception:
    """Demonstrate network mocking patterns"""

    def test_mock_empty_feed(self, page: Page, login_as, fresh_database):
        """Test with mocked empty feed response."""
        login_as("sarah")

        # Mock the feed API endpoint
        def handle_route(route: Route):
            route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps([])  # Empty feed
            )

        page.route("**/api/feed**", handle_route)

        # Navigate to feed
        page.goto("http://localhost:3000")

        # Should show empty state
        from playwright.sync_api import expect
        expect(page.locator("text=/no posts/i")).to_be_visible(timeout=5000)

    def test_mock_api_error(self, page: Page, login_as, fresh_database):
        """Test handling of API errors."""
        login_as("sarah")

        # Mock API to return error
        def handle_route(route: Route):
            route.fulfill(
                status=500,
                content_type="application/json",
                body=json.dumps({"detail": "Server error"})
            )

        page.route("**/api/posts/", handle_route)

        # Try to create post
        page.goto("http://localhost:3000")
        page.fill('[data-testid="create-post-textarea"]', "This will fail")
        page.click('[data-testid="create-post-submit"]')

        # Should show error message
        from playwright.sync_api import expect
        expect(page.locator("text=/error/i")).to_be_visible(timeout=5000)

    def test_slow_network_simulation(self, page: Page, login_as, fresh_database):
        """Test behavior with slow network."""
        login_as("sarah")

        # Add delay to API responses
        def handle_route(route: Route):
            import time
            time.sleep(2)  # Simulate 2 second delay
            route.continue_()

        page.route("**/api/feed**", handle_route)

        # Navigate and measure that loading indicator appears
        page.goto("http://localhost:3000")

        # Should show loading state (briefly)
        from playwright.sync_api import expect
        # Note: might timeout if feed loads too fast in test
        try:
            expect(page.locator('[role="status"]')).to_be_visible(timeout=1000)
        except:
            pass  # Loading was too fast
```

**🎯 Checkpoint:** Run `HEADLESS=false pytest test_network.py -v -m network`

---

### Part 4: Pytest Markers & Test Organization (15 minutes)

Organize tests with markers to run different test suites.

Create `pytest.ini` configuration (if not exists) or update it:

```ini
[pytest]
markers =
    smoke: Quick smoke tests that verify basic functionality
    regression: Full regression tests
    pom: Tests demonstrating Page Object Model
    fixtures: Tests demonstrating advanced fixtures
    network: Tests with network interception
    slow: Tests that take longer to run
```

Create `tests/e2e-python/test_markers.py`:

```python
"""Tests demonstrating pytest markers"""

import pytest
from playwright.sync_api import Page
from pages.feed_page import FeedPage


@pytest.mark.smoke
def test_smoke_app_loads(page: Page, base_url: str):
    """Smoke test: App loads successfully."""
    page.goto(base_url)
    from playwright.sync_api import expect
    expect(page.locator('[data-testid="login-email-input"]')).to_be_visible()


@pytest.mark.smoke
def test_smoke_login_works(page: Page, login_as, fresh_database):
    """Smoke test: Login functionality works."""
    login_as("sarah")
    from playwright.sync_api import expect
    expect(page.locator('[data-testid="navbar"]')).to_be_visible()


@pytest.mark.regression
@pytest.mark.slow
def test_regression_complete_user_journey(page: Page, test_users, fresh_database):
    """Full regression: Complete user journey."""
    # Register new user
    import time
    timestamp = int(time.time())

    page.goto("http://localhost:3000/register")
    page.fill('[data-testid="register-email-input"]', f"test{timestamp}@test.com")
    page.fill('[data-testid="register-username-input"]', f"test{timestamp}")
    page.fill('[data-testid="register-displayname-input"]', "Test User")
    page.fill('[data-testid="register-password-input"]', "Test123!")
    page.click('[data-testid="register-submit-button"]')

    page.wait_for_url("http://localhost:3000/", timeout=10000)

    # Create post
    feed = FeedPage(page)
    feed.create_post("My first post!")

    # View profile
    page.click('[data-testid="navbar-profile-link"]')

    # Logout
    page.click('[data-testid="navbar-logout-button"]')

    from playwright.sync_api import expect
    expect(page.locator('[data-testid="login-email-input"]')).to_be_visible()
```

**Run different marker combinations:**

```bash
# Run only smoke tests (fast)
pytest -m smoke -v

# Run regression tests
pytest -m regression -v

# Run everything except slow tests
pytest -m "not slow" -v

# Run smoke OR pom tests
pytest -m "smoke or pom" -v
```

---

### Part 5: Data Builders (10 minutes)

Create clean test data with builder pattern.

Create `tests/e2e-python/builders.py`:

```python
"""Test data builders for creating test data cleanly"""

import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class UserBuilder:
    """Builder for creating test user data."""

    email: Optional[str] = None
    username: Optional[str] = None
    display_name: Optional[str] = None
    password: str = "Test123!"

    def with_unique_email(self):
        """Generate unique email."""
        timestamp = int(time.time())
        self.email = f"test{timestamp}@testbook.com"
        return self

    def with_unique_username(self):
        """Generate unique username."""
        timestamp = int(time.time())
        self.username = f"test{timestamp}"
        return self

    def with_display_name(self, name: str):
        """Set display name."""
        self.display_name = name
        return self

    def with_password(self, password: str):
        """Set password."""
        self.password = password
        return self

    def build(self) -> dict:
        """Build the user dict."""
        if not self.email:
            self.with_unique_email()
        if not self.username:
            self.with_unique_username()
        if not self.display_name:
            self.display_name = f"Test User {self.username}"

        return {
            "email": self.email,
            "username": self.username,
            "displayName": self.display_name,
            "password": self.password
        }


@dataclass
class PostBuilder:
    """Builder for creating test post data."""

    content: str = "Test post content"

    def with_content(self, content: str):
        """Set post content."""
        self.content = content
        return self

    def with_long_content(self):
        """Create post with long content."""
        self.content = "This is a longer post. " * 20
        return self

    def build(self) -> dict:
        """Build the post dict."""
        return {"content": self.content}
```

Use in tests (`test_builders.py`):

```python
"""Tests using data builders"""

import pytest
from playwright.sync_api import Page

from builders import UserBuilder, PostBuilder
from pages.feed_page import FeedPage


@pytest.mark.builders
def test_with_user_builder(page: Page, fresh_database):
    """Test registration with UserBuilder."""
    # Build test user
    user = UserBuilder().with_display_name("Builder User").build()

    # Register
    page.goto("http://localhost:3000/register")
    page.fill('[data-testid="register-email-input"]', user["email"])
    page.fill('[data-testid="register-username-input"]', user["username"])
    page.fill('[data-testid="register-displayname-input"]', user["displayName"])
    page.fill('[data-testid="register-password-input"]', user["password"])
    page.click('[data-testid="register-submit-button"]')

    page.wait_for_url("http://localhost:3000/", timeout=10000)

    from playwright.sync_api import expect
    expect(page.locator('[data-testid="navbar"]')).to_be_visible()


@pytest.mark.builders
def test_with_post_builder(page: Page, login_as, fresh_database):
    """Test post creation with PostBuilder."""
    login_as("sarah")

    # Build test post
    post = PostBuilder().with_content("Built with builder pattern!").build()

    # Create post
    feed = FeedPage(page)
    feed.goto()
    feed.create_post(post["content"])

    # Verify
    assert feed.post_count() >= 1
```

---

### Part 6: Combined API + UI Validation (25 minutes)

One powerful Python advantage: Use the same language for backend API setup AND frontend UI verification!

#### Pattern 1: Seed Data via API, Verify via UI

Instead of clicking through the UI to set up test data, use the API directly:

Create `tests/e2e-python/test_api_ui_combined.py`:

```python
"""Tests combining API setup with UI verification"""

import pytest
import requests
from playwright.sync_api import Page, expect

from pages.feed_page import FeedPage
from pages.profile_page import ProfilePage


@pytest.mark.combined
class TestAPIPlusUIValidation:
    """Demonstrate combined API/UI testing patterns"""

    def test_api_created_post_appears_in_ui(
        self, page: Page, login_as, api_url: str, fresh_database
    ):
        """Seed data via API, verify in UI - FAST setup!"""

        # 1. Login to get auth token
        login_response = requests.post(
            f"{api_url}/api/auth/login",
            json={
                "email": "sarah.johnson@testbook.com",
                "password": "Sarah2024!"
            }
        )
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 2. Create posts via API (FAST - no UI clicking!)
        for i in range(5):
            requests.post(
                f"{api_url}/api/posts/",
                json={"content": f"API post {i+1}"},
                headers=headers
            )

        # 3. NOW verify in UI
        login_as("sarah")
        feed = FeedPage(page)
        feed.goto()

        # UI should show all API-created posts
        assert feed.post_count() >= 5
        assert feed.find_post_by_content("API post 1").is_visible()

    def test_api_follow_verified_in_ui(
        self, page: Page, login_as, api_url: str, test_users: dict, fresh_database
    ):
        """Use API for setup, UI for verification"""

        # 1. Login Sarah via API
        login_response = requests.post(
            f"{api_url}/api/auth/login",
            json={
                "email": test_users["sarah"]["email"],
                "password": test_users["sarah"]["password"]
            }
        )
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 2. Follow Mike via API
        requests.post(
            f"{api_url}/api/users/mikechen/follow",
            headers=headers
        )

        # 3. Verify follow relationship in UI
        login_as("sarah")

        profile = ProfilePage(page)
        profile.goto("mikechen")

        # UI should reflect API action
        assert profile.is_following() is True
        assert profile.get_follower_count() >= 1

    def test_ui_action_verified_via_api(
        self, page: Page, login_as, api_url: str, fresh_database
    ):
        """Reverse pattern: UI action, API verification"""

        # 1. Perform UI action
        login_as("sarah")
        feed = FeedPage(page)
        feed.goto()

        post_content = "UI created, API verified!"
        feed.create_post(post_content)

        # 2. Verify via API (more reliable for assertions)
        login_response = requests.post(
            f"{api_url}/api/auth/login",
            json={
                "email": "sarah.johnson@testbook.com",
                "password": "Sarah2024!"
            }
        )
        token = login_response.json()["access_token"]

        # Get feed via API
        feed_response = requests.get(
            f"{api_url}/api/feed",
            headers={"Authorization": f"Bearer {token}"}
        )
        posts = feed_response.json()

        # Verify post exists in API response
        post_contents = [p["content"] for p in posts]
        assert post_content in post_contents

        # Verify exact structure returned by API
        created_post = next(p for p in posts if p["content"] == post_content)
        assert created_post["author"]["username"] == "sarahjohnson"
```

#### Pattern 2: Complex Setup via API

For complex test scenarios, set up ALL data via API:

```python
@pytest.fixture
def complex_social_graph(api_url: str, test_users: dict, fresh_database):
    """Create complex social graph via API for testing."""

    def _setup():
        # Login all users and get tokens
        tokens = {}
        for key, user in test_users.items():
            response = requests.post(
                f"{api_url}/api/auth/login",
                json={"email": user["email"], "password": user["password"]}
            )
            tokens[key] = response.json()["access_token"]

        # Sarah follows Mike and Emma
        for target in ["mikechen", "emmadavis"]:
            requests.post(
                f"{api_url}/api/users/{target}/follow",
                headers={"Authorization": f"Bearer {tokens['sarah']}"}
            )

        # Mike follows Emma
        requests.post(
            f"{api_url}/api/users/emmadavis/follow",
            headers={"Authorization": f"Bearer {tokens['mike']}"}
        )

        # Create posts from all users
        for key, token in tokens.items():
            for i in range(3):
                requests.post(
                    f"{api_url}/api/posts/",
                    json={"content": f"{key} post {i+1}"},
                    headers={"Authorization": f"Bearer {token}"}
                )

        return tokens

    return _setup


def test_feed_shows_following_posts_only(
    page: Page, login_as, complex_social_graph
):
    """Test feed filtering with complex pre-seeded data."""

    # Setup entire social graph via API (FAST!)
    complex_social_graph()

    # Now test UI behavior
    login_as("sarah")

    feed = FeedPage(page)
    feed.goto()

    # Sarah should see posts from Mike and Emma (who she follows)
    assert feed.find_post_by_content("mike post 1").is_visible()
    assert feed.find_post_by_content("emma post 1").is_visible()
```

#### Pattern 3: API Verification of UI State

Test that UI changes are reflected in the database:

```python
def test_ui_update_persists_to_database(
    page: Page, login_as, api_url: str, fresh_database
):
    """Verify UI changes persist to backend."""

    # 1. Update profile via UI
    login_as("sarah")
    page.goto("http://localhost:3000/settings")

    page.fill('[data-testid="settings-bio"]', "Updated bio from UI test")
    page.click('[data-testid="settings-save"]')
    page.wait_for_timeout(500)

    # 2. Verify via API that change persisted
    login_response = requests.post(
        f"{api_url}/api/auth/login",
        json={
            "email": "sarah.johnson@testbook.com",
            "password": "Sarah2024!"
        }
    )
    token = login_response.json()["access_token"]

    me_response = requests.get(
        f"{api_url}/api/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    user = me_response.json()
    assert user["bio"] == "Updated bio from UI test"
```

**🎯 Checkpoint:** Run `HEADLESS=false pytest test_api_ui_combined.py -v -m combined`

---

## 🎓 What You Learned

- ✅ **Page Object Model** - Reusable, maintainable page helpers
- ✅ **Advanced fixtures** - Parametrized and custom fixtures
- ✅ **Network interception** - Mocking API responses
- ✅ **Pytest markers** - Organizing test runs (smoke/regression)
- ✅ **Data builders** - Clean test data creation
- ✅ **🆕 Combined API + UI validation** - Use Python for both backend and frontend testing
- ✅ **🆕 API-driven test setup** - Fast data seeding
- ✅ **🆕 Bidirectional verification** - API → UI and UI → API
- ✅ **Professional patterns** - Industry-standard E2E practices

---

## 💪 Practice Challenges

### Challenge 1: Add More Page Objects

Create page objects for:

- LoginPage
- RegistrationPage
- SettingsPage

### Challenge 2: Advanced Network Mocking

Create tests that mock:

- Partial responses (some posts load, others fail)
- Rate limit errors (429 status)
- Pagination responses

### Challenge 3: Complex Fixtures

Create a fixture that:

- Logs in as user A
- Creates 3 posts
- Logs in as user B
- Follows user A
- Returns both users

### Challenge 4: Screenshot Testing

Add screenshot capture on test failure:

```python
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            screenshot_path = f"test-results/failure-{item.name}.png"
            page.screenshot(path=screenshot_path)
            print(f"\n📸 Screenshot saved: {screenshot_path}")
```

### Challenge 5: Combined API + UI Testing

Create tests that:

- Use API to create 10 posts, reactions, and follows
- Verify all appear correctly in UI
- Measure time saved vs clicking through UI

---

## 🎯 Pro Tips

**Tip 1: Keep Page Objects Focused**

```python
# ❌ Bad: Too much logic in tests
def test_something(page):
    page.goto("...")
    page.fill('[data-testid="xyz"]', "...")
    page.click('[data-testid="abc"]')
    # 50 more lines...

# ✅ Good: Logic in page object
def test_something(page):
    profile = ProfilePage(page)
    profile.goto("sarah")
    profile.follow_user()
```

**Tip 2: Use Markers Strategically**

```bash
# Run before committing (fast)
pytest -m smoke

# Run nightly (comprehensive)
pytest -m regression

# Run specific feature
pytest -m "user_management"
```

**Tip 3: Combine Patterns**

```python
def test_advanced_pattern(authenticated_feed, create_test_posts):
    """Combines fixtures + page objects + builders"""
    posts = create_test_posts(count=5)

    # Now use page object methods
    assert authenticated_feed.post_count() == 5
```

**Tip 4: Python's Unique Advantage - Combined API/UI Testing**

```python
def test_fast_setup(page, login_as, api_url):
    """Use API for setup (FAST), UI for verification"""

    # Setup via API (no UI interaction needed!)
    token = get_auth_token(api_url, "sarah")
    create_posts_via_api(api_url, token, count=10)

    # Verify via UI
    login_as("sarah")
    feed = FeedPage(page)
    feed.goto()
    assert feed.post_count() == 10  # Instant setup!
```

This pattern is **10-100x faster** than clicking through UI for setup!

---

## ✅ Lab Completion Checklist

- [ ] Created FeedPage and ProfilePage objects
- [ ] Used page objects in tests successfully
- [ ] Created and used advanced fixtures
- [ ] Implemented network interception
- [ ] Used pytest markers to organize tests
- [ ] Created and used data builders
- [ ] 🆕 Implemented combined API + UI validation patterns
- [ ] 🆕 Understand Python's unique advantage for full-stack testing
- [ ] All tests pass

---

## 🆚 Compare with JavaScript

Both Python and JavaScript Playwright support these patterns!

| Feature | Python (this lab) | JavaScript |
|---------|------------------|------------|
| **Page Objects** | Classes | Classes or functions |
| **Fixtures** | pytest fixtures | Playwright fixtures |
| **Markers** | `@pytest.mark` | `test.describe` tags |
| **Network** | `page.route()` | `page.route()` |
| **Syntax** | Synchronous | Async/await |

The concepts transfer directly between languages!

---

## 📚 Resources

**Working Examples (Run These!):**

- **`tests/e2e-python/examples/`** - ⭐ Complete working examples from this lab
  - `test_page_objects_example.py` - Page Object Model in action
  - `test_api_ui_combined_example.py` - API + UI validation patterns
  - Run with: `HEADLESS=false pytest tests/e2e-python/examples/ -v -m examples`
- **`tests/e2e-python/pages/`** - Reusable page objects (base, feed, profile)
- **`tests/e2e-python/conftest.py`** - Advanced fixtures added at bottom

**Study Existing Tests:**

- `tests/e2e-python/test_auth.py` - Authentication examples
- `tests/e2e-python/test_posts.py` - Post management examples

**Official Documentation:**

- [Playwright Python Page Objects](https://playwright.dev/python/docs/pom)
- [pytest fixtures](https://docs.pytest.org/en/stable/fixture.html)
- [pytest markers](https://docs.pytest.org/en/stable/example/markers.html)

---

**🎉 You've mastered advanced E2E testing patterns in Python! These are professional-level skills used in production!**

**🐍 Python's Unique Advantage:** Unlike JavaScript, Python lets you use the same language for backend API manipulation AND frontend UI testing. This enables incredibly fast test setup by seeding data via API instead of clicking through UI!

**Next Steps:**

- Apply these patterns to the full test suite
- Explore [Section 8: Advanced E2E Patterns](../docs/course/SECTION_08_ADVANCED_E2E_PATTERNS.md) for more examples
- Compare with [JavaScript advanced patterns](../docs/guides/TESTING_COMPARISON_PYTHON_JS.md)
- Set up [CI/CD automation](../docs/course/CI_CD_E2E_TESTING.md)
