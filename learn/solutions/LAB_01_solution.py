"""
Lab 1 Solution: Your First Test

This file contains complete solutions for all Lab 1 exercises.
Students may have variations that are also correct.
"""


def test_basic_math():
    """Test that 2 + 2 equals 4."""
    # Arrange
    # (No setup needed for this simple test)

    # Act
    result = 2 + 2

    # Assert
    assert result == 4


def test_string_length():
    """Test string length."""
    # Arrange
    text = "Hello"

    # Act
    length = len(text)

    # Assert
    assert length == 5
    # Alternative: assert len(text) == 5


def test_list_contains():
    """Test list contains item."""
    # Arrange
    fruits = ["apple", "banana", "orange"]

    # Act
    # (No action needed - checking membership)

    # Assert
    assert "banana" in fruits
    assert "grape" not in fruits  # Extra check


def test_my_own_test():
    """Test something I wrote myself!"""
    # Example solution - students will have different implementations

    # Test name length
    my_name = "Student Name"
    assert len(my_name) > 0
    assert isinstance(my_name, str)

    # Test favorite number
    favorite_number = 42
    assert favorite_number > 0
    assert favorite_number < 1000  # Extra check

    # Test a list
    my_list = ["item1", "item2", "item3"]
    assert len(my_list) == 3
    assert "item1" in my_list


# Challenge Exercise Solution
def test_sum_numbers():
    """Test sum of numbers."""
    # Arrange
    numbers = [1, 2, 3, 4, 5]

    # Act
    total = sum(numbers)

    # Assert
    assert total == 15
    # Alternative checks:
    assert total == 1 + 2 + 3 + 4 + 5
    assert total > 0


# Additional test examples students might create
def test_list_append():
    """Test appending to a list."""
    # Arrange
    items = []

    # Act
    items.append("first")
    items.append("second")

    # Assert
    assert len(items) == 2
    assert items[0] == "first"
    assert items[1] == "second"


def test_string_methods():
    """Test string methods."""
    # Arrange
    text = "hello world"

    # Act & Assert
    assert text.upper() == "HELLO WORLD"
    assert text.capitalize() == "Hello world"
    assert text.startswith("hello")
    assert text.endswith("world")


def test_dictionary_operations():
    """Test dictionary operations."""
    # Arrange
    person = {"name": "Alice", "age": 30}

    # Act & Assert
    assert person["name"] == "Alice"
    assert person["age"] == 30
    assert "name" in person
    assert "email" not in person

    # Add item
    person["email"] = "alice@example.com"
    assert person["email"] == "alice@example.com"


# Grading Notes for Instructors:
#
# FULL CREDIT (100%):
# - All required tests present and passing
# - Tests use assert statements correctly
# - Tests have descriptive names
# - Challenge exercise completed
#
# GOOD (85-99%):
# - Most tests present and passing
# - Minor issues with naming or structure
# - Challenge exercise attempted
#
# ACCEPTABLE (70-84%):
# - Basic tests work
# - Some tests missing or failing
# - Shows understanding of basics
#
# NEEDS IMPROVEMENT (<70%):
# - Many tests failing
# - Missing assert statements
# - Doesn't demonstrate understanding
#
# Common mistakes to watch for:
# 1. Using == instead of assert
# 2. Test names don't start with test_
# 3. Not running tests to verify they pass
# 4. Copy-paste errors
