# Test Design Principles: Building Effective Tests

## What Makes a Good Test?

A good test is more than just code that runs without errors. It's a piece of software that:

- **Verifies behavior** - Confirms the system works as expected
- **Documents intent** - Shows how the system should behave
- **Provides feedback** - Tells you when something breaks
- **Enables change** - Gives confidence to refactor and improve

## Core Design Principles

### 1. Clarity Over Cleverness

**The Principle:**
Tests should be easy to read and understand. Future developers (including yourself) should be able to understand what a test does without extensive documentation.

**Good Example:**

```python
def test_user_can_login_with_valid_credentials():
    # Clear what we're testing
    user = create_user(email="test@example.com", password="password123")

    # Clear what we're doing
    result = login_user("test@example.com", "password123")

    # Clear what we expect
    assert result.success is True
    assert result.user_id == user.id
```

**Bad Example:**

```python
def test_login():
    # What are we testing? What's the expected behavior?
    u = User(email="t@e.com", pwd="p123")
    r = login("t@e.com", "p123")
    assert r.s and r.uid == u.id
```

### 2. One Concept Per Test

**The Principle:**
Each test should verify one specific behavior. This makes tests easier to understand, debug, and maintain.

**Good Example:**

```python
def test_password_must_be_at_least_8_characters():
    result = validate_password("short")
    assert result.is_valid is False
    assert "at least 8 characters" in result.error_message

def test_password_must_contain_uppercase():
    result = validate_password("lowercase123")
    assert result.is_valid is False
    assert "uppercase letter" in result.error_message

def test_password_must_contain_number():
    result = validate_password("NoNumbers")
    assert result.is_valid is False
    assert "number" in result.error_message
```

**Bad Example:**

```python
def test_password_validation():
    # Testing multiple concepts in one test
    assert validate_password("short").is_valid is False
    assert validate_password("lowercase123").is_valid is False
    assert validate_password("NoNumbers").is_valid is False
    assert validate_password("ValidPass123").is_valid is True
```

### 3. Independent Tests

**The Principle:**
Tests should not depend on each other. Each test should be able to run in isolation and in any order.

**Why This Matters:**

- Tests can run in parallel
- Failures are easier to debug
- Tests are more reliable
- You can run individual tests

**How to Achieve:**

- Use fixtures for setup
- Clean up after each test
- Avoid shared state
- Use unique test data

### 4. Deterministic Results

**The Principle:**
Tests should produce the same result every time they run. No randomness, no external dependencies, no timing issues.

**Good Example:**

```python
def test_calculate_discount():
    # Always produces the same result
    price = 100.00
    discount_rate = 0.10

    result = calculate_discount(price, discount_rate)

    assert result == 10.00
```

**Bad Example:**

```python
def test_calculate_discount():
    # Random result - test is flaky
    price = random.uniform(50, 200)
    discount_rate = random.uniform(0.05, 0.20)

    result = calculate_discount(price, discount_rate)

    # This assertion might fail randomly
    assert result > 0
```

### 5. Fast Execution

**The Principle:**
Tests should run quickly to provide fast feedback. Slow tests discourage frequent running.

**How to Achieve:**

- Mock external dependencies
- Use in-memory databases
- Avoid file I/O
- Minimize network calls
- Use efficient assertions

### 6. Meaningful Assertions

**The Principle:**
Assertions should clearly express what you're verifying and provide helpful error messages when they fail.

**Good Example:**

```python
def test_user_registration():
    result = register_user("new@example.com", "password123")

    # Clear, specific assertions
    assert result.success is True, "User registration should succeed"
    assert result.user.email == "new@example.com", "Email should be set correctly"
    assert result.user.id is not None, "User should have an ID"
    assert len(result.user.password_hash) > 0, "Password should be hashed"
```

**Bad Example:**

```python
def test_user_registration():
    result = register_user("new@example.com", "password123")

    # Vague assertions
    assert result
    assert result.user
    assert result.user.email
```

## Test Structure Patterns

### The AAA Pattern

**Arrange** - Set up test data and conditions
**Act** - Execute the code being tested
**Assert** - Verify the expected outcome

```python
def test_calculate_total_price():
    # Arrange
    items = [
        {"name": "Apple", "price": 1.50, "quantity": 3},
        {"name": "Banana", "price": 0.75, "quantity": 2}
    ]

    # Act
    total = calculate_total_price(items)

    # Assert
    assert total == 6.00
```

### The Given-When-Then Pattern

**Given** - Initial state or context
**When** - Action or event
**Then** - Expected outcome

```python
def test_user_can_purchase_item():
    # Given
    user = create_user_with_balance(100.00)
    item = create_item(price=25.00)

    # When
    result = purchase_item(user, item)

    # Then
    assert result.success is True
    assert user.balance == 75.00
    assert item.owner == user
```

## Naming Conventions

### Test Function Names

**Pattern:** `test_[what]_[when]_[then]`

**Examples:**

```python
def test_user_login_when_credentials_are_valid():
    pass

def test_user_login_when_password_is_wrong():
    pass

def test_user_login_when_account_is_locked():
    pass
```

### Test Class Names

**Pattern:** `Test[WhatYoureTesting]`

**Examples:**

```python
class TestUserAuthentication:
    pass

class TestOrderProcessing:
    pass

class TestPaymentValidation:
    pass
```

## Data Management

### Test Data Principles

**1. Use Realistic Data**

```python
# Good - realistic data
user = User(
    email="john.doe@example.com",
    first_name="John",
    last_name="Doe",
    phone="+1-555-123-4567"
)

# Bad - unrealistic data
user = User(
    email="a@b.com",
    first_name="a",
    last_name="b",
    phone="123"
)
```

**2. Use Factories for Complex Data**

```python
def test_user_profile_completion():
    # Use factory to create realistic user
    user = UserFactory.create(
        email="test@example.com",
        profile_complete=False
    )

    # Test the specific behavior
    result = complete_profile(user, profile_data)
    assert result.success is True
    assert user.profile_complete is True
```

**3. Use Builders for Variations**

```python
def test_different_user_types():
    # Builder pattern for variations
    admin_user = UserBuilder().with_role("admin").build()
    regular_user = UserBuilder().with_role("user").build()

    # Test different behaviors
    assert admin_user.can_delete_users() is True
    assert regular_user.can_delete_users() is False
```

## Error Handling in Tests

### Testing Success Cases

```python
def test_successful_operation():
    result = perform_operation(valid_input)

    assert result.success is True
    assert result.data is not None
    assert result.error_message is None
```

### Testing Error Cases

```python
def test_operation_with_invalid_input():
    result = perform_operation(invalid_input)

    assert result.success is False
    assert result.data is None
    assert "Invalid input" in result.error_message
```

### Testing Edge Cases

```python
def test_operation_with_boundary_values():
    # Test minimum valid value
    result = perform_operation(minimum_valid_value)
    assert result.success is True

    # Test just below minimum
    result = perform_operation(minimum_valid_value - 1)
    assert result.success is False
```

## Test Organization

### Grouping Related Tests

```python
class TestUserRegistration:
    def test_successful_registration(self):
        pass

    def test_registration_with_duplicate_email(self):
        pass

    def test_registration_with_invalid_email(self):
        pass

    def test_registration_with_weak_password(self):
        pass
```

### Using Test Categories

```python
@pytest.mark.unit
def test_calculate_discount():
    pass

@pytest.mark.integration
def test_user_registration_flow():
    pass

@pytest.mark.slow
def test_large_dataset_processing():
    pass
```

## Common Anti-Patterns to Avoid

### 1. Testing Implementation Details

**Bad:**

```python
def test_user_creation():
    user = create_user("test@example.com")
    # Testing internal implementation
    assert user._password_hash is not None
    assert user._created_at is not None
```

**Good:**

```python
def test_user_creation():
    user = create_user("test@example.com")
    # Testing public behavior
    assert user.email == "test@example.com"
    assert user.can_login("password") is True
```

### 2. Overly Complex Test Setup

**Bad:**

```python
def test_simple_calculation():
    # 50 lines of setup for a simple test
    user = create_user_with_complex_profile()
    order = create_order_with_multiple_items()
    # ... more complex setup
    result = calculate_tax(order)
    assert result == 10.00
```

**Good:**

```python
def test_simple_calculation():
    # Simple, focused setup
    order = Order(total=100.00, tax_rate=0.10)
    result = calculate_tax(order)
    assert result == 10.00
```

### 3. Testing Multiple Things

**Bad:**

```python
def test_user_management():
    # Testing too many things
    user = create_user()
    user.update_profile()
    user.change_password()
    user.delete_account()
    # Multiple assertions for different behaviors
```

**Good:**

```python
def test_user_creation():
    user = create_user()
    assert user.email is not None

def test_profile_update():
    user = create_user()
    user.update_profile()
    assert user.profile_updated is True

def test_password_change():
    user = create_user()
    user.change_password()
    assert user.password_changed is True
```

## Measuring Test Quality

### Good Test Indicators

- **Fast** - Runs quickly
- **Independent** - Doesn't depend on other tests
- **Repeatable** - Same result every time
- **Self-validating** - Clear pass/fail result
- **Timely** - Written at the right time
- **Clear** - Easy to understand
- **Focused** - Tests one thing
- **Maintainable** - Easy to update

### Test Quality Checklist

- [ ] Does the test name clearly describe what it's testing?
- [ ] Is the test focused on one specific behavior?
- [ ] Are the setup, action, and assertion clear?
- [ ] Does the test use realistic data?
- [ ] Is the test independent of other tests?
- [ ] Does the test run quickly?
- [ ] Are the assertions meaningful and specific?
- [ ] Is the test easy to understand and maintain?

## Conclusion

Good test design is about creating tests that are:

- **Readable** - Easy to understand what they're testing
- **Reliable** - Consistent results every time
- **Maintainable** - Easy to update when code changes
- **Fast** - Quick feedback on code quality
- **Focused** - Testing one thing well

Remember: Tests are not just code—they're documentation, they're specifications, and they're your safety net. Invest in making them good, and they'll pay dividends in code quality and development velocity.

---

## Further Reading

- [Testing Philosophy](TESTING_PHILOSOPHY.md) - The mindset behind testing
- [Testing Patterns](TESTING_PATTERNS.md) - Common patterns and when to use them
- [Testing Anti-Patterns](TESTING_ANTIPATTERNS.md) - What to avoid
- [Industry Practices](../industry/INDUSTRY_PRACTICES.md) - How companies design tests
