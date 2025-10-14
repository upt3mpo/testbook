# ⚡ Pytest Quick Reference

**One-page reference for pytest commands and patterns**

---

## 🚀 Essential Commands

### Running Tests

```bash
# Run all tests
pytest

# Verbose output (recommended)
pytest -v

# Very verbose (shows print statements)
pytest -vv -s

# Run specific directory
pytest tests/unit/
pytest tests/integration/

# Run specific file
pytest tests/unit/test_auth.py

# Run specific test
pytest tests/unit/test_auth.py::TestPasswordHashing::test_password_is_hashed

# Run specific class
pytest tests/unit/test_auth.py::TestPasswordHashing

# Run by pattern
pytest -k "password"  # Runs all tests with "password" in name
pytest -k "login or register"  # Multiple patterns
```

### By Marker

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run only API tests
pytest -m api

# Run everything except slow tests
pytest -m "not slow"

# Combine markers
pytest -m "unit and auth"
```

### Debugging

```bash
# Stop on first failure
pytest -x

# Drop into debugger on failure
pytest --pdb

# Drop into debugger on error AND failure
pytest --pdb --pdbcls=IPython.terminal.debugger:TerminalPdb

# Show local variables on failure
pytest -l

# Show why tests were skipped
pytest -rs
```

### Output Control

```bash
# Show print statements
pytest -s

# Quiet mode (less output)
pytest -q

# Show test durations
pytest --durations=10  # Slowest 10 tests

# No header/summary
pytest --no-header --no-summary
```

---

## 📊 Coverage

```bash
# Run with coverage
pytest --cov

# Coverage for specific module
pytest --cov=auth

# Show missing lines
pytest --cov=auth --cov-report=term-missing

# Generate HTML report
pytest --cov --cov-report=html

# Open coverage report
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
xdg-open htmlcov/index.html  # Linux

# Coverage with minimum threshold
pytest --cov --cov-fail-under=80
```

---

## ⚡ Performance

```bash
# Run tests in parallel (requires pytest-xdist)
pytest -n auto  # Uses all CPU cores
pytest -n 4     # Uses 4 workers

# Show slowest tests
pytest --durations=10

# Run only fast tests
pytest -m "not slow"
```

---

## 🔍 Finding Tests

```bash
# List all tests without running
pytest --collect-only

# List tests matching pattern
pytest --collect-only -k "login"

# Show available markers
pytest --markers

# Show available fixtures
pytest --fixtures
```

---

## 📝 Test Structure Patterns

### Basic Test

```python
def test_something():
    """Test description."""
    # Arrange
    value = 10

    # Act
    result = value * 2

    # Assert
    assert result == 20
```

### Using Fixtures

```python
def test_with_fixture(test_user):
    """Test using a fixture."""
    assert test_user.email == "testuser@example.com"
    assert test_user.id is not None
```

### Parameterized Test

```python
@pytest.mark.parametrize("input,expected", [
    (2, 4),
    (3, 9),
    (4, 16),
])
def test_square(input, expected):
    """Test with multiple inputs."""
    assert input ** 2 == expected
```

### Testing Exceptions

```python
def test_raises_error():
    """Test that function raises exception."""
    with pytest.raises(ValueError):
        some_function_that_raises()

    # Check error message
    with pytest.raises(ValueError, match="invalid"):
        some_function_that_raises()
```

### Setup and Teardown

```python
def test_with_setup_teardown(tmp_path):
    """Test with automatic cleanup."""
    # tmp_path is automatically created and cleaned up
    file = tmp_path / "test.txt"
    file.write_text("test data")

    assert file.read_text() == "test data"
    # tmp_path automatically deleted after test
```

---

## 🏷️ Markers

```python
# Mark as unit test
@pytest.mark.unit
def test_unit():
    pass

# Mark as slow
@pytest.mark.slow
def test_slow():
    pass

# Mark as skip
@pytest.mark.skip(reason="Not implemented yet")
def test_skip():
    pass

# Mark as expected failure
@pytest.mark.xfail(reason="Known bug")
def test_xfail():
    pass

# Multiple markers
@pytest.mark.unit
@pytest.mark.auth
def test_multiple():
    pass
```

---

## 🎯 Assertions

```python
# Equality
assert x == y
assert x != y

# Comparison
assert x > y
assert x >= y
assert x < y
assert x <= y

# Identity
assert x is y
assert x is None
assert x is not None

# Membership
assert x in [1, 2, 3]
assert x not in [1, 2, 3]

# Boolean
assert x
assert not x
assert x is True
assert x is False

# Type checking
assert isinstance(x, str)
assert isinstance(x, (str, int))

# String contains
assert "substring" in text
assert text.startswith("prefix")
assert text.endswith("suffix")

# Length
assert len(items) == 5
assert len(items) > 0

# Exception
with pytest.raises(ValueError):
    raise ValueError()
```

---

## 🔧 Common Fixtures

```python
# Database session
def test_db(db_session):
    user = User(email="test@test.com")
    db_session.add(user)
    db_session.commit()

# API client
def test_api(client):
    response = client.get("/api/endpoint")
    assert response.status_code == 200

# Authentication
def test_auth(auth_token, auth_headers):
    # Use auth_headers in requests
    response = client.get("/api/me", headers=auth_headers)

# Test data
def test_data(test_user, test_post):
    assert test_post.author_id == test_user.id
```

---

## 🐛 Debugging Tips

```python
# Print values during test
def test_debug():
    value = calculate_something()
    print(f"Value is: {value}")  # Run with: pytest -s
    assert value == expected

# Use breakpoint()
def test_breakpoint():
    value = calculate_something()
    breakpoint()  # Drops into debugger
    assert value == expected

# Show local variables
pytest -l  # Shows locals on failure
```

---

## 📋 Configuration (pytest.ini)

```ini
[pytest]
# Minimum pytest.ini
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Markers
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow tests

# Options
addopts =
    -v
    --strict-markers
    --tb=short
```

---

## 🚨 Common Issues

### Tests Not Found

```bash
# Issue: pytest doesn't find tests
# Fix: Make sure you're in the right directory
cd backend

# Fix: Check test file names start with test_
ls tests/test_*.py

# Fix: Check function names start with test_
grep "def test_" tests/test_file.py
```

### Import Errors

```bash
# Issue: ModuleNotFoundError
# Fix: Activate virtual environment
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Fix: Install dependencies
pip install -r requirements.txt
```

### Fixture Not Found

```bash
# Issue: "fixture 'test_user' not found"
# Fix: Check conftest.py exists
ls tests/conftest.py

# Fix: Check fixture is defined
grep "def test_user" tests/conftest.py
```

---

## 📚 Related Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [backend/tests/README.md](../../backend/tests/README.md) - Testbook test guide
- [TESTING_CHEATSHEET.md](TESTING_CHEATSHEET.md) - Testbook-specific testing

---

## 💡 Pro Tips

1. **Use `-v` always** - Verbose output shows exactly what's running
2. **Use `-x` when debugging** - Stop on first failure saves time
3. **Use `--pdb` for investigation** - Drop into debugger to explore
4. **Use `-k` for fast iteration** - Run only the test you're working on
5. **Use `--cov` regularly** - Track your test coverage
6. **Use `-n auto` for speed** - Parallel execution is much faster
7. **Name tests descriptively** - `test_login_with_wrong_password_fails` is better than `test_login_2`

---

**🎯 Most Common Usage:**

```bash
# While developing a specific test
pytest tests/test_file.py::test_function -v -s

# Before committing
pytest -v --cov

# Full verification
pytest -v --cov --cov-fail-under=80 -n auto
```

