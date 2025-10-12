"""
Pytest fixtures for Playwright E2E tests
"""

import os

import pytest
import requests
from dotenv import load_dotenv
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

# Load environment variables from .env file
load_dotenv()


@pytest.fixture(scope="session")
def browser():
    """Launch browser for the entire test session"""
    headless = os.getenv("HEADLESS", "true").lower() == "true"
    slow_mo = int(os.getenv("SLOW_MO", "0"))

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless, slow_mo=slow_mo)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def context(browser: Browser):
    """Create a new browser context for each test"""
    # Set timeouts from environment
    timeout = int(os.getenv("DEFAULT_TIMEOUT", "30000"))

    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        record_video_dir="test-results/videos"
        if os.getenv("VIDEO_ON_FAILURE") == "true"
        else None,
    )
    context.set_default_timeout(timeout)
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext):
    """Create a new page for each test"""
    page = context.new_page()

    # Auto-accept all browser dialogs (alert, confirm, prompt)
    # This is essential for tests that trigger window.confirm() or window.alert()
    def handle_dialog(dialog):
        print(f"Auto-accepting {dialog.type}: {dialog.message}")
        dialog.accept()

    page.on("dialog", handle_dialog)

    # Log console errors for debugging
    def handle_console(msg):
        if msg.type == "error":
            print(f"Browser console error: {msg.text}")

    page.on("console", handle_console)

    yield page
    page.close()


@pytest.fixture(scope="session")
def base_url():
    """Base URL for the application (frontend)"""
    return os.getenv("FRONTEND_URL", "http://localhost:3000")


@pytest.fixture(scope="session")
def api_url():
    """Base URL for the API (backend)"""
    return os.getenv("BACKEND_URL", "http://localhost:8000")


# Test user credentials
@pytest.fixture(scope="session")
def test_users():
    """Pre-seeded test user credentials"""
    return {
        "sarah": {
            "email": "sarah.johnson@testbook.com",
            "password": "Sarah2024!",
            "name": "Sarah Johnson",
            "username": "sarahjohnson",
        },
        "mike": {
            "email": "mike.chen@testbook.com",
            "password": "MikeRocks88",
            "name": "Mike Chen",
            "username": "mikechen",
        },
        "emma": {
            "email": "emma.davis@testbook.com",
            "password": "EmmaLovesPhotos",
            "name": "Emma Davis",
            "username": "emmadavis",
        },
    }


@pytest.fixture(scope="session")
def reset_database(api_url: str):
    """
    Reset database to clean state before test session.

    This fixture runs once per session to ensure a clean state.
    Uses the /api/dev/reset endpoint to reset the database.
    """
    try:
        response = requests.post(f"{api_url}/api/dev/reset")
        if response.status_code == 200:
            print("\n✅ Database reset successful")
        else:
            print(f"\n⚠️  Database reset returned status {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"\n⚠️  Could not reset database: {e}")
        print("   Make sure the backend is running on", api_url)

    yield

    # Optional: Clean up after all tests
    # Uncomment if you want to reset after tests too
    # try:
    #     requests.post(f"{api_url}/api/dev/reset")
    # except:
    #     pass


@pytest.fixture(scope="function")
def fresh_database(api_url: str):
    """
    Reset database before each test function.

    Use this for tests that need a completely clean state.
    This is similar to JavaScript's beforeEach resetDatabase pattern.

    Example:
        def test_something(page, fresh_database):
            # Database is fresh for this test
    """
    try:
        response = requests.post(f"{api_url}/api/dev/reset")
        if response.status_code != 200:
            pytest.skip(f"Could not reset database: {response.status_code}")
    except requests.exceptions.RequestException as e:
        pytest.skip(f"Could not connect to API: {e}")


@pytest.fixture
def seed_test_data(api_url: str):
    """
    Seed database with test data.

    Returns a function to seed specific data based on scenario.

    Example:
        def test_something(page, seed_test_data):
            seed_test_data("high_traffic")
            # Now database has users with many posts
    """

    def _seed(scenario: str = "default"):
        """
        Seed data based on scenario.

        Scenarios:
        - "default": Standard seed (already done by reset)
        - "empty": Empty database (reset without seeding)
        - "minimal": Only basic users, no posts
        - "high_traffic": Many posts and interactions
        """
        if scenario == "empty":
            # Database already reset, no seeding needed
            return {"scenario": "empty", "users": 0, "posts": 0}

        elif scenario == "minimal":
            # Default seed includes users, this is same as default
            # Could be extended to create only 1-2 users
            return {"scenario": "minimal", "users": "default", "posts": 0}

        elif scenario == "high_traffic":
            # Create additional posts using dev API
            test_posts = [
                {"user_id": 1, "content": "Just had an amazing coffee! ☕"},
                {"user_id": 1, "content": "Working on a new project today!"},
                {"user_id": 2, "content": "Beautiful sunset tonight 🌅"},
                {"user_id": 2, "content": "Anyone want to grab lunch?"},
                {"user_id": 3, "content": "New photos uploaded! Check them out!"},
                {"user_id": 3, "content": "Feeling grateful today 💚"},
            ]

            created_posts = []
            for post_data in test_posts:
                try:
                    response = requests.post(
                        f"{api_url}/api/dev/create-post", params=post_data, timeout=5
                    )
                    if response.status_code == 200:
                        created_posts.append(response.json())
                except requests.exceptions.RequestException as e:
                    print(f"Warning: Failed to create test post: {e}")

            return {
                "scenario": "high_traffic",
                "posts_created": len(created_posts),
                "posts": created_posts,
            }

        # Default scenario uses standard seeded data
        return {"scenario": "default", "users": "default", "posts": "default"}

    return _seed


@pytest.fixture
def login_as(page: Page, base_url: str, test_users: dict):
    """Helper function to login as a specific user"""

    def _login(user_key: str = "sarah"):
        user = test_users[user_key]

        # Navigate to login page
        page.goto(base_url)

        # Fill in login form
        page.fill('[data-testid="login-email-input"]', user["email"])
        page.fill('[data-testid="login-password-input"]', user["password"])

        # Submit form
        page.click('[data-testid="login-submit-button"]')

        # Wait for navigation to complete
        page.wait_for_url(f"{base_url}/", timeout=10000)

        # Wait for navbar to be visible
        from playwright.sync_api import expect

        expect(page.locator('[data-testid="navbar"]')).to_be_visible(timeout=10000)

        # Wait for network to settle (with try-except to handle if it takes longer)
        try:
            page.wait_for_load_state("networkidle", timeout=5000)
        except:
            # If networkidle times out, just continue - the navbar is visible which is good enough
            pass

    return _login


@pytest.fixture(autouse=True, scope="session")
def setup_test_environment(api_url: str, reset_database):
    """
    Automatically set up test environment before any tests run.

    This fixture:
    - Ensures backend is accessible
    - Resets database to clean state
    - Runs once per test session
    """
    # Check if backend is available
    try:
        response = requests.get(f"{api_url}/docs", timeout=5)
        if response.status_code != 200:
            pytest.exit(f"Backend is not responding correctly on {api_url}")
    except requests.exceptions.RequestException:
        pytest.exit(
            f"Cannot connect to backend on {api_url}\nMake sure backend is running with: ./start-dev.sh"
        )

    print(f"\n✅ Backend is available at {api_url}")
    yield


# ============================================================================
# 🆕 Advanced Fixtures from Lab 4B
# ============================================================================


@pytest.fixture
def feed_page(page: Page):
    """Fixture that provides a FeedPage instance."""
    from pages.feed_page import FeedPage

    return FeedPage(page)


@pytest.fixture
def profile_page(page: Page):
    """Fixture that provides a ProfilePage instance."""
    from pages.profile_page import ProfilePage

    return ProfilePage(page)


@pytest.fixture
def authenticated_feed(page: Page, login_as):
    """Fixture that logs in and returns a FeedPage."""
    from pages.feed_page import FeedPage

    login_as("sarah")
    feed = FeedPage(page)
    feed.goto()
    return feed


@pytest.fixture
def create_test_posts(authenticated_feed):
    """Fixture that creates multiple test posts."""

    def _create_posts(count: int = 3, prefix: str = "Test post"):
        posts = []
        for i in range(count):
            content = f"{prefix} {i + 1}"
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
