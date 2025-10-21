"""
Pytest configuration and fixtures for Testbook tests.

This module provides reusable test fixtures and configuration
that are available to all test files.
"""

import os
import sys
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# Add parent directory to path so we can import from backend
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth import create_access_token, get_password_hash
from database import Base, get_db
from main import app
from models import Comment, Post, Reaction, User

# ═══════════════════════════════════════════════════════════════════
# Welcome Banner & Completion Messages
# ═══════════════════════════════════════════════════════════════════


def pytest_configure(config):
    """Display welcome banner when pytest starts."""
    print("=" * 70)
    print("Welcome to Testbook Testing Platform!")
    print("Running 180+ backend tests (unit + integration + contract)")
    print("Python pytest | FastAPI | SQLAlchemy")
    print("Tip: Use -v for verbose output, -k to filter by name")
    print("=" * 70)

    # print(banner.encode('utf-8', errors='ignore').decode('utf-8'))  # Disabled for Windows encoding issues


def pytest_sessionfinish(session, exitstatus):
    """Display completion message after all tests run."""
    if exitstatus == 0:
        print("""
Congratulations! All Backend Tests Passed!

You're mastering automation testing! Your backend is working correctly.

Next steps:
  - Run coverage report: pytest --cov --cov-report=html
  - View coverage: open htmlcov/index.html
  - Run frontend tests: cd ../frontend && npm test
  - Run E2E tests: cd ../tests && npx playwright test

Keep up the great work!
""")
    else:
        print("""
Some Tests Failed

Debug tips:
  - Use pytest -v for more details
  - Use pytest -x to stop at first failure
  - Use pytest --lf to re-run last failed tests
  - Check docs/reference/TROUBLESHOOTING.md for technical errors with exact fixes
""")

    # print(message)  # Disabled for Windows encoding issues


# Test database configuration
TEST_DATABASE_URL = "sqlite:///./test_testbook.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """
    Create a fresh database session for each test.

    This fixture creates all tables before the test and drops them after,
    ensuring each test has a clean database state.

    Yields:
        Session: SQLAlchemy database session
    """
    # Create all tables
    Base.metadata.create_all(bind=test_engine)

    # Create session
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session: Session) -> TestClient:
    """
    Create a TestClient with overridden database dependency.

    This fixture provides a FastAPI TestClient that uses the test database
    instead of the production database.

    Args:
        db_session: Test database session

    Returns:
        TestClient: FastAPI test client
    """

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session: Session) -> User:
    """
    Create a test user in the database.

    Returns:
        User: Test user with known credentials
    """
    user = User(
        email="testuser@example.com",
        username="testuser",
        display_name="Test User",
        hashed_password=get_password_hash("TestPassword123!"),
        bio="Test user bio",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_user_2(db_session: Session) -> User:
    """
    Create a second test user for relationship testing.

    Returns:
        User: Second test user
    """
    user = User(
        email="testuser2@example.com",
        username="testuser2",
        display_name="Test User 2",
        hashed_password=get_password_hash("TestPassword456!"),
        bio="Second test user",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_user_3(db_session: Session) -> User:
    """
    Create a third test user for complex relationship testing.

    Returns:
        User: Third test user
    """
    user = User(
        email="testuser3@example.com",
        username="testuser3",
        display_name="Test User 3",
        hashed_password=get_password_hash("TestPassword789!"),
        bio="Third test user",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_token(test_user: User) -> str:
    """
    Create a valid JWT token for test user.

    Args:
        test_user: Test user to create token for

    Returns:
        str: JWT access token
    """
    return create_access_token(data={"sub": test_user.email})


@pytest.fixture
def auth_headers(auth_token: str) -> dict:
    """
    Create authorization headers with JWT token.

    Args:
        auth_token: JWT access token

    Returns:
        dict: Headers with authorization token
    """
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture
def test_post(db_session: Session, test_user: User) -> Post:
    """
    Create a test post in the database.

    Args:
        db_session: Database session
        test_user: User to create post for

    Returns:
        Post: Test post
    """
    post = Post(
        author_id=test_user.id,
        content="This is a test post",
    )
    db_session.add(post)
    db_session.commit()
    db_session.refresh(post)
    return post


@pytest.fixture
def test_posts(db_session: Session, test_user: User, test_user_2: User) -> list[Post]:
    """
    Create multiple test posts from different users.

    Args:
        db_session: Database session
        test_user: First user
        test_user_2: Second user

    Returns:
        list[Post]: List of test posts
    """
    posts = [
        Post(author_id=test_user.id, content=f"Test post {i} from user 1") for i in range(1, 4)
    ]
    posts.extend(
        [Post(author_id=test_user_2.id, content=f"Test post {i} from user 2") for i in range(1, 3)]
    )

    for post in posts:
        db_session.add(post)

    db_session.commit()

    for post in posts:
        db_session.refresh(post)

    return posts


@pytest.fixture
def test_comment(db_session: Session, test_post: Post, test_user_2: User) -> Comment:
    """
    Create a test comment on a post.

    Args:
        db_session: Database session
        test_post: Post to comment on
        test_user_2: User creating the comment

    Returns:
        Comment: Test comment
    """
    comment = Comment(
        post_id=test_post.id,
        author_id=test_user_2.id,
        content="This is a test comment",
    )
    db_session.add(comment)
    db_session.commit()
    db_session.refresh(comment)
    return comment


@pytest.fixture
def test_reaction(db_session: Session, test_post: Post, test_user_2: User) -> Reaction:
    """
    Create a test reaction on a post.

    Args:
        db_session: Database session
        test_post: Post to react to
        test_user_2: User creating the reaction

    Returns:
        Reaction: Test reaction
    """
    reaction = Reaction(
        post_id=test_post.id,
        user_id=test_user_2.id,
        reaction_type="like",
    )
    db_session.add(reaction)
    db_session.commit()
    db_session.refresh(reaction)
    return reaction


# Helper functions for tests


def login_user(client: TestClient, email: str, password: str) -> dict:
    """
    Helper function to login a user and return the token.

    Args:
        client: FastAPI TestClient
        email: User email
        password: User password

    Returns:
        dict: Response containing access_token
    """
    response = client.post("/api/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200
    return response.json()


def create_authenticated_headers(token: str) -> dict:
    """
    Create headers with authentication token.

    Args:
        token: JWT access token

    Returns:
        dict: Headers dictionary
    """
    return {"Authorization": f"Bearer {token}"}
