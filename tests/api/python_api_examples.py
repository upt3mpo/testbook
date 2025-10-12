"""
Python API Testing Examples for Testbook.

These examples demonstrate how to test the Testbook API using
the requests library. Great for learning API testing or building
your own test automation framework.

Usage:
    python python_api_examples.py
"""

from typing import Dict, Optional

import requests


class TestbookAPI:
    """
    API client for Testbook with built-in test examples.

    This class demonstrates professional API testing patterns and
    can be used as a foundation for building test automation suites.
    """

    def __init__(self, base_url: str = "http://localhost:8000/api"):
        self.base_url = base_url
        self.token: Optional[str] = None
        self.session = requests.Session()

    def _headers(self) -> Dict[str, str]:
        """Get headers with authentication token if available."""
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    # Authentication Methods

    def register(
        self, email: str, username: str, display_name: str, password: str, bio: str = ""
    ) -> Dict:
        """
        Register a new user.

        Example:
            >>> api = TestbookAPI()
            >>> response = api.register(
            ...     email="test@example.com",
            ...     username="testuser",
            ...     display_name="Test User",
            ...     password="Password123!"
            ... )
            >>> print(response["username"])
            testuser
        """
        response = self.session.post(
            f"{self.base_url}/auth/register",
            json={
                "email": email,
                "username": username,
                "display_name": display_name,
                "password": password,
                "bio": bio,
            },
        )
        response.raise_for_status()
        data = response.json()

        # Auto-set token from registration
        if "access_token" in data:
            self.token = data["access_token"]

        return data

    def login(self, email: str, password: str) -> Dict:
        """
        Login and store authentication token.

        Example:
            >>> api = TestbookAPI()
            >>> response = api.login("sarah.johnson@testbook.com", "Sarah2024!")
            >>> print("Logged in!")
        """
        response = self.session.post(
            f"{self.base_url}/auth/login", json={"email": email, "password": password}
        )
        response.raise_for_status()
        data = response.json()
        self.token = data["access_token"]
        return data

    def get_current_user(self) -> Dict:
        """
        Get current authenticated user.

        Example:
            >>> api = TestbookAPI()
            >>> api.login("sarah.johnson@testbook.com", "Sarah2024!")
            >>> user = api.get_current_user()
            >>> print(user["username"])
            sarahjohnson
        """
        response = self.session.get(f"{self.base_url}/auth/me", headers=self._headers())
        response.raise_for_status()
        return response.json()

    # Post Methods

    def create_post(
        self, content: str, image_url: str = None, video_url: str = None
    ) -> Dict:
        """
        Create a new post.

        Example:
            >>> api = TestbookAPI()
            >>> api.login("sarah.johnson@testbook.com", "Sarah2024!")
            >>> post = api.create_post("Hello from API!")
            >>> print(f"Created post {post['id']}")
        """
        response = self.session.post(
            f"{self.base_url}/posts/",
            json={"content": content, "image_url": image_url, "video_url": video_url},
            headers=self._headers(),
        )
        response.raise_for_status()
        return response.json()

    def get_post(self, post_id: int) -> Dict:
        """Get a specific post by ID."""
        response = self.session.get(f"{self.base_url}/posts/{post_id}")
        response.raise_for_status()
        return response.json()

    def update_post(self, post_id: int, content: str) -> Dict:
        """Update a post."""
        response = self.session.put(
            f"{self.base_url}/posts/{post_id}",
            json={"content": content},
            headers=self._headers(),
        )
        response.raise_for_status()
        return response.json()

    def delete_post(self, post_id: int) -> Dict:
        """Delete a post."""
        response = self.session.delete(
            f"{self.base_url}/posts/{post_id}", headers=self._headers()
        )
        response.raise_for_status()
        return response.json()

    def add_comment(self, post_id: int, content: str) -> Dict:
        """Add a comment to a post."""
        response = self.session.post(
            f"{self.base_url}/posts/{post_id}/comments",
            json={"content": content},
            headers=self._headers(),
        )
        response.raise_for_status()
        return response.json()

    def add_reaction(self, post_id: int, reaction_type: str) -> Dict:
        """
        Add or change reaction on a post.

        Args:
            post_id: Post ID
            reaction_type: One of: like, love, haha, wow, sad, angry
        """
        response = self.session.post(
            f"{self.base_url}/posts/{post_id}/reactions",
            json={"reaction_type": reaction_type},
            headers=self._headers(),
        )
        response.raise_for_status()
        return response.json()

    def remove_reaction(self, post_id: int) -> Dict:
        """Remove reaction from a post."""
        response = self.session.delete(
            f"{self.base_url}/posts/{post_id}/reactions", headers=self._headers()
        )
        response.raise_for_status()
        return response.json()

    # Feed Methods

    def get_all_feed(self) -> list:
        """Get all posts feed."""
        response = self.session.get(
            f"{self.base_url}/feed/all", headers=self._headers()
        )
        response.raise_for_status()
        return response.json()

    def get_following_feed(self) -> list:
        """Get following-only feed."""
        response = self.session.get(
            f"{self.base_url}/feed/following", headers=self._headers()
        )
        response.raise_for_status()
        return response.json()

    # User Methods

    def get_user_profile(self, username: str) -> Dict:
        """Get user profile by username."""
        response = self.session.get(
            f"{self.base_url}/users/{username}", headers=self._headers()
        )
        response.raise_for_status()
        return response.json()

    def update_profile(
        self,
        display_name: str = None,
        bio: str = None,
        theme: str = None,
        text_density: str = None,
    ) -> Dict:
        """Update own profile."""
        data = {}
        if display_name:
            data["display_name"] = display_name
        if bio is not None:
            data["bio"] = bio
        if theme:
            data["theme"] = theme
        if text_density:
            data["text_density"] = text_density

        response = self.session.put(
            f"{self.base_url}/users/me", json=data, headers=self._headers()
        )
        response.raise_for_status()
        return response.json()

    def follow_user(self, username: str) -> Dict:
        """Follow a user."""
        response = self.session.post(
            f"{self.base_url}/users/{username}/follow", headers=self._headers()
        )
        response.raise_for_status()
        return response.json()

    def unfollow_user(self, username: str) -> Dict:
        """Unfollow a user."""
        response = self.session.delete(
            f"{self.base_url}/users/{username}/follow", headers=self._headers()
        )
        response.raise_for_status()
        return response.json()

    def block_user(self, username: str) -> Dict:
        """Block a user."""
        response = self.session.post(
            f"{self.base_url}/users/{username}/block", headers=self._headers()
        )
        response.raise_for_status()
        return response.json()

    def unblock_user(self, username: str) -> Dict:
        """Unblock a user."""
        response = self.session.delete(
            f"{self.base_url}/users/{username}/block", headers=self._headers()
        )
        response.raise_for_status()
        return response.json()

    # Dev/Testing Methods

    def reset_database(self) -> Dict:
        """Reset database to initial state."""
        response = self.session.post(f"{self.base_url}/dev/reset")
        response.raise_for_status()
        return response.json()


# Example Test Scenarios


def example_auth_flow():
    """Example: Complete authentication flow."""
    print("\n=== Authentication Flow Example ===")

    api = TestbookAPI()

    # Reset database for clean state
    print("Resetting database...")
    api.reset_database()

    # Register new user (returns token, not user data)
    print("Registering new user...")
    result = api.register(
        email="example@test.com",
        username="exampleuser",
        display_name="Example User",
        password="Example123!",
    )
    print("✓ Registered and got token")

    # Get current user (should be auto-logged in)
    me = api.get_current_user()
    print(f"✓ Logged in as: {me['display_name']}")


def example_post_crud():
    """Example: Post CRUD operations."""
    print("\n=== Post CRUD Example ===")

    api = TestbookAPI()
    api.reset_database()

    # Login
    api.login("sarah.johnson@testbook.com", "Sarah2024!")
    print("✓ Logged in")

    # Create post (returns full post data)
    post = api.create_post("This is a test post from Python!")
    print(f"✓ Created post {post['id']}: {post['content'][:30]}...")

    # Update post
    updated = api.update_post(post["id"], "Updated content!")
    print(f"✓ Updated post: {updated['content']}")

    # Add comment
    comment = api.add_comment(post["id"], "Great post!")
    print(f"✓ Added comment: {comment['content']}")

    # Add reaction
    api.add_reaction(post["id"], "like")
    print("✓ Added like reaction")

    # Delete post
    api.delete_post(post["id"])
    print(f"✓ Deleted post {post['id']}")


def example_user_interactions():
    """Example: User follow/block interactions."""
    print("\n=== User Interactions Example ===")

    api = TestbookAPI()
    api.reset_database()

    # Login as Sarah
    api.login("sarah.johnson@testbook.com", "Sarah2024!")
    print("✓ Logged in as Sarah")

    # Get Mike's profile
    mike = api.get_user_profile("mikechen")
    print(f"✓ Mike has {mike['followers_count']} followers")

    # Try to follow Mike (may already be following)
    try:
        api.follow_user("mikechen")
        print("✓ Followed Mike")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            print("✓ Already following Mike")
        else:
            raise

    # Unfollow Mike
    try:
        api.unfollow_user("mikechen")
        print("✓ Unfollowed Mike")
    except requests.exceptions.HTTPError:
        print("✓ Not following Mike")

    # Block and unblock
    try:
        api.block_user("mikechen")
        print("✓ Blocked Mike")
        api.unblock_user("mikechen")
        print("✓ Unblocked Mike")
    except requests.exceptions.HTTPError as e:
        print(f"✓ Relationship action handled (status: {e.response.status_code})")


def example_feed_operations():
    """Example: Feed retrieval and filtering."""
    print("\n=== Feed Operations Example ===")

    api = TestbookAPI()
    api.reset_database()

    # Login
    api.login("sarah.johnson@testbook.com", "Sarah2024!")
    print("✓ Logged in")

    # Get all feed
    all_posts = api.get_all_feed()
    print(f"✓ All feed has {len(all_posts)} posts")

    # Get following feed
    following_posts = api.get_following_feed()
    print(f"✓ Following feed has {len(following_posts)} posts")

    print("✓ Feed operations completed successfully")


def example_profile_management():
    """Example: Profile updates."""
    print("\n=== Profile Management Example ===")

    api = TestbookAPI()
    api.reset_database()

    # Login
    api.login("sarah.johnson@testbook.com", "Sarah2024!")
    print("✓ Logged in")

    # Update profile
    updated = api.update_profile(
        display_name="Sarah J.", bio="Updated bio from API", theme="dark"
    )
    print(f"✓ Updated profile: {updated['display_name']}")
    print(f"✓ New theme: {updated['theme']}")


def run_all_examples():
    """Run all example scenarios."""
    print("╔═══════════════════════════════════════════╗")
    print("║  Testbook API Testing Examples (Python)  ║")
    print("╚═══════════════════════════════════════════╝")

    try:
        example_auth_flow()
        example_post_crud()
        example_user_interactions()
        example_feed_operations()
        example_profile_management()

        print("\n✓ All examples completed successfully!")

    except requests.exceptions.RequestException as e:
        print(f"\n✗ API Error: {e}")
        print("Make sure Testbook is running on http://localhost:8000")
    except Exception as e:
        print(f"\n✗ Error: {e}")


if __name__ == "__main__":
    run_all_examples()
