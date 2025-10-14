"""Example tests using Page Object Model

These examples demonstrate the patterns taught in Lab 4B.
Run with: HEADLESS=false pytest examples/test_page_objects_example.py -v
"""

import sys
from pathlib import Path

import pytest
from playwright.sync_api import Page

sys.path.insert(0, str(Path(__file__).parent.parent))

from pages.feed_page import FeedPage
from pages.profile_page import ProfilePage


@pytest.mark.examples
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
