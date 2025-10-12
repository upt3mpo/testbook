"""Example tests combining API setup with UI verification

These examples demonstrate Python's unique advantage for full-stack testing.
Run with: pytest examples/test_api_ui_combined_example.py -v --headed
"""

import sys
from pathlib import Path

import pytest
import requests
from playwright.sync_api import Page

sys.path.insert(0, str(Path(__file__).parent.parent))

from pages.feed_page import FeedPage
from pages.profile_page import ProfilePage


@pytest.mark.examples
@pytest.mark.combined
class TestAPIPlusUIValidation:
    """Demonstrate combined API/UI testing patterns"""

    def test_api_created_posts_appear_in_ui(
        self, page: Page, login_as, api_url: str, fresh_database
    ):
        """Seed data via API, verify in UI - FAST setup!"""

        # 1. Login to get auth token
        login_response = requests.post(
            f"{api_url}/api/auth/login",
            json={"email": "sarah.johnson@testbook.com", "password": "Sarah2024!"},
        )
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 2. Create posts via API (FAST - no UI clicking!)
        for i in range(5):
            requests.post(
                f"{api_url}/api/posts/",
                json={"content": f"API created post {i + 1}"},
                headers=headers,
            )

        # 3. NOW verify in UI
        login_as("sarah")
        feed = FeedPage(page)
        feed.goto()

        # UI should show all API-created posts
        assert feed.post_count() >= 5
        assert feed.find_post_by_content("API created post 1").is_visible()

        print("✅ API-seeded posts verified in UI!")

    def test_api_follow_verified_in_ui(
        self, page: Page, login_as, api_url: str, test_users: dict, fresh_database
    ):
        """Use API for setup, UI for verification"""

        # 1. Login Sarah via API
        login_response = requests.post(
            f"{api_url}/api/auth/login",
            json={
                "email": test_users["sarah"]["email"],
                "password": test_users["sarah"]["password"],
            },
        )
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 2. Follow Mike via API
        requests.post(f"{api_url}/api/users/mikechen/follow", headers=headers)

        # 3. Verify follow relationship in UI
        login_as("sarah")

        profile = ProfilePage(page)
        profile.goto("mikechen")

        # UI should reflect API action
        assert profile.is_following() is True

        print("✅ API follow action verified in UI!")

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
            json={"email": "sarah.johnson@testbook.com", "password": "Sarah2024!"},
        )
        token = login_response.json()["access_token"]

        # Get feed via API
        feed_response = requests.get(
            f"{api_url}/api/feed", headers={"Authorization": f"Bearer {token}"}
        )
        posts = feed_response.json()

        # Verify post exists in API response
        post_contents = [p["content"] for p in posts]
        assert post_content in post_contents

        # Verify exact structure returned by API
        created_post = next(p for p in posts if p["content"] == post_content)
        assert created_post["author"]["username"] == "sarahjohnson"

        print("✅ UI action verified via API response!")
