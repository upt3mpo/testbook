"""
Examples of BAD tests - Anti-patterns to avoid.

DO NOT USE THESE IN PRODUCTION.
These are intentionally bad examples for educational purposes.
"""

import time


# ❌ ANTI-PATTERN 1: Hardcoded IDs
def test_get_user_bad():
    """BAD: Hardcoded user ID."""
    response = client.get("/api/users/1")  # What if user 1 doesn't exist?
    assert response.status_code == 200


# ❌ ANTI-PATTERN 2: Using sleep()
def test_async_bad():
    """BAD: Using arbitrary sleep."""
    trigger_task()
    time.sleep(5)  # Arbitrary wait - too long or too short?
    result = get_result()
    assert result == "done"


# ❌ ANTI-PATTERN 3: Dependent tests
test_data = {}  # Global state!


def test_step1_bad():
    """BAD: Stores data in global variable."""
    global test_data
    test_data["user"] = create_user()


def test_step2_bad():
    """BAD: Depends on test_step1_bad running first."""
    user = test_data["user"]  # Will fail if test_step1 didn't run
    assert user is not None


# ❌ ANTI-PATTERN 4: No assertions
def test_no_assertions_bad():
    """BAD: No assertions - test is useless."""
    user = create_user()
    # Forgot to assert anything!


# ❌ ANTI-PATTERN 5: Too many assertions (testing everything)
def test_everything_bad():
    """BAD: Testing too much in one test."""
    user = create_user()
    assert user.id is not None
    assert user.email is not None

    post = create_post(user)
    assert post.id is not None

    comment = create_comment(post)
    assert comment.id is not None

    # 50 more lines...


# ❌ ANTI-PATTERN 6: Vague test name
def test_user_bad():
    """BAD: Unclear what's being tested."""
    user = create_user()
    assert user


# ❌ ANTI-PATTERN 7: Testing implementation
def test_implementation_bad():
    """BAD: Testing internal implementation details."""
    password = "test"
    hashed = get_password_hash(password)

    # Testing bcrypt implementation details
    assert hashed.count("$") == 3
    assert "$2b$12$" in hashed
    # What if we change to a different hashing algorithm?


# ❌ ANTI-PATTERN 8: Not cleaning up
def test_no_cleanup_bad():
    """BAD: Leaves test data in database."""
    user = User(email="test@test.com")
    db.add(user)
    db.commit()
    # User stays in database for next test!


# ❌ ANTI-PATTERN 9: Brittle E2E selectors (JavaScript example in comments)
"""
// ❌ BAD - JavaScript example
test('bad selector', async ({ page }) => {
  await page.click('.btn.btn-primary.large');  // Breaks when CSS changes
  await page.click('div > div > div > button');  // Breaks when HTML changes
});
"""


# ❌ ANTI-PATTERN 10: Hardcoded timestamps
def test_timestamp_bad():
    """BAD: Hardcoded timestamp."""
    user = create_user()
    # Will fail tomorrow!
    assert str(user.created_at).startswith("2024-01-15")


# NOTE: See good_tests.py for correct implementations of all these examples.
