# Testbook Backend Test Suite

Comprehensive test suite for the Testbook backend API built with pytest and FastAPI TestClient.

## Overview

This test suite demonstrates professional testing practices and serves as a learning resource for automation testing.

### Test Organization

- **`unit/`** - Unit tests (fast, isolated, test individual functions)
  - `test_auth.py` - Password hashing, JWT tokens
  - `test_models.py` - Database models, relationships
- **`integration/`** - Integration tests (test API endpoints and database)
  - `test_api_auth.py` - Authentication endpoints
  - `test_api_posts.py` - Posts endpoints
  - `test_api_users.py` - Users endpoints
  - `test_api_feed.py` - Feed endpoints
  - `test_api_contract.py` - API contract validation
  - `test_api_dev.py` - Development endpoints
  - `test_database.py` - Database constraints and transactions
- **`conftest.py`** - Shared fixtures and test configuration
- **`factories.py`** - Test data factories

## Running Tests

### Prerequisites

```bash
# Activate virtual environment
cd backend
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies including test packages
pip install -r requirements.txt
```

### Basic Commands

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v
# See [Quick Commands](docs/reference/QUICK_COMMANDS.md) for all pytest options

# Run specific test directory
pytest tests/unit/
pytest tests/integration/

# Run specific test file
pytest tests/unit/test_auth.py
pytest tests/integration/test_api_posts.py

# Run specific test
pytest tests/unit/test_auth.py::TestPasswordHashing::test_password_is_hashed

# Run tests by marker
pytest -m unit          # Only unit tests
pytest -m integration   # Only integration tests
pytest -m api           # Only API tests
pytest -m database      # Only database tests

# Run tests excluding slow tests
pytest -m "not slow"
```

### Coverage Reports

> **💡 When to Use Coverage:** Coverage is great for full test suite runs and CI/CD, but skip it when debugging individual tests to keep output clean.

```bash
# Run with coverage (explicit flags required)
pytest --cov=.

# Generate HTML coverage report
pytest --cov=. --cov-report=html
# See [Quick Commands](docs/reference/QUICK_COMMANDS.md) for all coverage options

# View HTML report
open htmlcov/index.html  # macOS
start htmlcov/index.html # Windows
```

### When to Use Coverage

**✅ Use Coverage For:**

- Full test suite runs (`make test-backend` or `just test-backend`)
- CI/CD pipelines
- Before committing code
- Quality assurance checks

**❌ Skip Coverage For:**

- Single test debugging (`pytest tests/unit/test_auth.py::test_password_is_hashed -v`)
- Quick test runs during development
- When you need clean, focused output

**Performance Impact:**
Coverage collection adds ~20-30% overhead to test execution time. For 166 tests, this means ~15-20 seconds additional time.

### Parallel Execution

```bash
# Run tests in parallel (faster)
pytest -n auto
```

## Test Structure

### Unit Tests (`tests/unit/`)

Test individual components in isolation:

- **`test_auth.py`** - Password hashing, JWT token creation
- **`test_models.py`** - Database models, relationships, cascades

### Integration Tests (`tests/integration/`)

Test API endpoints and multiple components together:

- **`test_api_auth.py`** - Registration, login, authentication
- **`test_api_posts.py`** - Post CRUD, comments, reactions, reposts
- **`test_api_users.py`** - User profiles, follow/unfollow, block/unblock
- **`test_api_feed.py`** - Feed generation, filtering, ordering
- **`test_api_contract.py`** - Property-based API contract validation (see below)
- **`test_api_dev.py`** - Development utilities
- **`test_database.py`** - Constraints, transactions, complex queries, cascades

#### About Contract Testing (`test_api_contract.py`)

This test uses **Schemathesis** for property-based contract testing - an advanced technique that automatically generates hundreds of test cases from your OpenAPI schema.

**What it does:**

- Reads the OpenAPI schema from FastAPI
- Automatically generates 500+ test cases for all endpoints
- Tests valid inputs, invalid inputs, edge cases, and security fuzzing
- Validates responses match the schema
- Finds bugs you'd never think to test manually

**Current Status:** ⚠️ **Skipped** (OpenAPI 3.1.0 compatibility)

FastAPI 0.115+ generates OpenAPI 3.1.0 schemas. Schemathesis 3.27.1 only has experimental 3.1.0 support. The test is skipped until full support is available.

**Educational Value:**
Even though skipped, studying this test teaches you about:

- Property-based testing (generates tests from properties/rules)
- Contract testing (validates implementation matches specification)
- API fuzzing (automated security testing)
- Advanced QA techniques used in production

**Learn more:** [Contract Testing Guide](../../docs/guides/CONTRACT_TESTING.md) - Complete explanation with examples

**Alternative:** Frontend contract testing works today! See [Lab 6C: Frontend Integration Testing](../../learn/stage_4_performance_security/exercises/LAB_06C_Frontend_Integration_Testing.md)

## Test Markers

Tests are organized with pytest markers:

- `@pytest.mark.unit` - Fast, isolated unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.api` - API endpoint tests
- `@pytest.mark.database` - Database-specific tests
- `@pytest.mark.auth` - Authentication/authorization tests
- `@pytest.mark.slow` - Tests that take longer to run
- `@pytest.mark.smoke` - Critical functionality tests

## Fixtures

Reusable test fixtures are defined in `conftest.py`:

### Database Fixtures

- `db_session` - Fresh database session for each test
- `client` - FastAPI TestClient with test database

### User Fixtures

- `test_user` - Primary test user
- `test_user_2` - Secondary test user
- `test_user_3` - Third test user for complex scenarios

### Auth Fixtures

- `auth_token` - Valid JWT token for test_user
- `auth_headers` - Authorization headers with token

### Content Fixtures

- `test_post` - Single test post
- `test_posts` - Multiple test posts from different users
- `test_comment` - Test comment
- `test_reaction` - Test reaction

## Writing New Tests

### Basic Test Example

```python
import pytest

@pytest.mark.unit
def test_something():
    """Test description."""
    # Arrange
    value = 42

    # Act
    result = value * 2

    # Assert
    assert result == 84
```

### API Test Example

```python
@pytest.mark.integration
@pytest.mark.api
def test_get_endpoint(client, auth_headers):
    """Test GET endpoint."""
    response = client.get("/api/endpoint", headers=auth_headers)

    assert response.status_code == 200
    assert "expected_key" in response.json()
```

### Database Test Example

```python
@pytest.mark.database
def test_database_operation(db_session, test_user):
    """Test database operation."""
    # Create record
    record = Model(user_id=test_user.id, data="test")
    db_session.add(record)
    db_session.commit()

    # Verify
    assert record.id is not None
```

## Best Practices

1. **[Arrange-Act-Assert](../../docs/concepts/TESTING_PATTERNS.md#arrange-act-assert-pattern)** - Structure tests clearly
2. **One assertion per test** - Keep tests focused (when possible)
3. **Use descriptive names** - Test name should describe what's being tested
4. **Add docstrings** - Explain what the test verifies
5. **Use fixtures** - Share common setup between tests
6. **Mark tests** - Use markers for organization
7. **Test edge cases** - Not just happy paths
8. **Clean up** - Fixtures handle cleanup automatically

## Test Coverage Goals

- **Unit Tests**: 80%+ coverage of core functions
- **Integration Tests**: All API endpoints covered
- **Database Tests**: All models and relationships covered
- **Edge Cases**: Error handling, validation, authorization

### Current Coverage: 84%

Generate a fresh coverage report instead of reading a static snapshot:

```bash
pytest --cov . --cov-report=html
# Open HTML: htmlcov/index.html
```

**Quick Coverage Check:**

```bash
pytest --cov --cov-report=term-missing
```

## Continuous Integration

Tests are automatically run on every commit via GitHub Actions. See `.github/workflows/backend-tests.yml`.

## Troubleshooting

### Common Issues

1. **Import errors**

   - Make sure you're in the backend directory
   - Activate virtual environment
   - Install all dependencies

2. **Database locked errors**

   - Delete `test_testbook.db` if it exists
   - Each test creates a fresh database

3. **Port already in use**

   - Tests use TestClient, no actual server needed
   - No port conflicts should occur

4. **Slow tests**
   - Use `pytest -n auto` for parallel execution
   - Skip slow tests with `pytest -m "not slow"`

## Learning Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Testing Best Practices](https://docs.pytest.org/en/latest/goodpractices.html)

## Test Data Factories

**NEW:** Professional test data factories available!

See [factories.py](factories.py) for creating test data easily:

```python
from tests.factories import UserFactory, PostFactory, create_user_with_posts

# Create a user
user = UserFactory.create(db_session)

# Create user with custom data
user = UserFactory.create(
    db_session,
    email="custom@test.com",
    username="customuser"
)

# Create user with 5 posts
user, posts = create_user_with_posts(db_session, num_posts=5)
```

See [LAB_05_Test_Data_Management.md](../../learn/stage_2_integration/exercises/LAB_05_Test_Data_Management.md) to learn more.

## Contributing

When adding new tests:

1. Follow existing patterns
2. Add appropriate markers
3. Use existing fixtures when possible
4. Consider using test factories for complex data
5. Update this README if needed
6. Ensure tests pass: `pytest -v`
7. Check coverage: `pytest --cov`
8. Maintain 80%+ coverage threshold
