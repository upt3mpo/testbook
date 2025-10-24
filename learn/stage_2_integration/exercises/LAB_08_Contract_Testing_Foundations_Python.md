# 🧪 Lab 8: Contract Testing Foundations

**Estimated Time:** 90 minutes<br>
**Difficulty:** Intermediate<br>
**Language:** 🐍 Python<br>
**Prerequisites:** Lab 7 completed

**💡 Need JavaScript instead?** Try [Lab 8: Contract Testing Foundations (JavaScript)](LAB_08_Contract_Testing_Foundations_JavaScript.md)!

**What This Adds:** Contract testing ensures API compatibility between frontend and backend, preventing integration failures in production.

---

## 🎯 What You'll Learn

- **API contracts** - Define expected API behavior
- **Schema validation** - Ensure API responses match expected format
- **Contract testing** - Test API contracts without full integration
- **OpenAPI/Swagger** - Generate and validate API documentation
- **Consumer-driven contracts** - Frontend-driven API design
- **Breaking change detection** - Catch API changes that break clients

---

## 📋 Why Contract Testing Matters

**The Problem:**

- Frontend expects API to return `user.name`
- Backend changes API to return `user.fullName`
- Frontend breaks in production
- No tests caught this because they test in isolation

**The Solution:**
Contract testing ensures API changes don't break existing clients.

---

## 📋 Step-by-Step Instructions

### Part 1: Understanding API Contracts (20 minutes)

#### Step 1: What is an API Contract?

An API contract defines:

- **Request format** - What data the API expects
- **Response format** - What data the API returns
- **Status codes** - What each response means
- **Error formats** - How errors are communicated

#### Step 2: Example Contract

```python
"""
API Contract Definition for User Registration

This contract defines the expected behavior of the user registration endpoint.
It serves as a specification that both frontend and backend teams can agree on,
ensuring compatibility and preventing integration failures.
"""

# Example API contract for user registration
USER_REGISTRATION_CONTRACT = {
    "endpoint": "POST /api/auth/register",  # HTTP method and URL path

    "request": {
        # Required fields that the API expects
        "email": "string (required, valid email format)",           # Must be valid email
        "username": "string (required, 3-20 characters)",          # Username length constraint
        "display_name": "string (required, 1-50 characters)",      # Display name length constraint
        "password": "string (required, 8+ characters)"             # Password strength requirement
    },

    "response": {
        "success": {
            "status_code": 201,  # Created - user successfully registered
            "body": {
                "id": "integer",           # Auto-generated user ID
                "email": "string",         # User's email address
                "username": "string",      # User's chosen username
                "display_name": "string",  # User's display name
                "created_at": "datetime"   # Timestamp when user was created
            }
        },
        "error": {
            "status_code": 422,  # Unprocessable Entity - validation failed
            "body": {
                "detail": "array of validation errors"  # List of specific validation errors
            }
        }
    }
}
```

---

### Part 2: Schema Validation Testing (30 minutes)

#### Step 1: Install Schema Validation Library

```bash
cd backend
pip install jsonschema
```

#### Step 2: Create Schema Definitions

Create `backend/tests/schemas/user_schemas.py`:

```python
import jsonschema

# User registration request schema
USER_REGISTRATION_REQUEST_SCHEMA = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string",
            "format": "email",
            "minLength": 1
        },
        "username": {
            "type": "string",
            "minLength": 3,
            "maxLength": 20,
            "pattern": "^[a-zA-Z0-9_]+$"
        },
        "display_name": {
            "type": "string",
            "minLength": 1,
            "maxLength": 50
        },
        "password": {
            "type": "string",
            "minLength": 8
        }
    },
    "required": ["email", "username", "display_name", "password"],
    "additionalProperties": False
}

# User registration response schema
USER_REGISTRATION_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "email": {"type": "string"},
        "username": {"type": "string"},
        "display_name": {"type": "string"},
        "created_at": {"type": "string", "format": "date-time"}
    },
    "required": ["id", "email", "username", "display_name", "created_at"],
    "additionalProperties": False
}

# Error response schema
ERROR_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "detail": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "loc": {"type": "array"},
                    "msg": {"type": "string"},
                    "type": {"type": "string"}
                },
                "required": ["loc", "msg", "type"]
            }
        }
    },
    "required": ["detail"],
    "additionalProperties": False
}
```

#### Step 3: Create Schema Validation Tests

Create `backend/tests/contracts/test_user_contracts.py`:

```python
import pytest
import jsonschema
from fastapi.testclient import TestClient
from tests.schemas.user_schemas import (
    USER_REGISTRATION_REQUEST_SCHEMA,
    USER_REGISTRATION_RESPONSE_SCHEMA,
    ERROR_RESPONSE_SCHEMA
)

class TestUserRegistrationContract:
    """Test user registration API contract compliance."""

    def test_registration_request_schema_validation(self, client: TestClient):
        """Test that registration request matches expected schema."""
        # Valid request data
        valid_request = {
            "email": "test@example.com",
            "username": "testuser",
            "display_name": "Test User",
            "password": "password123"
        }

        # Validate request schema
        jsonschema.validate(valid_request, USER_REGISTRATION_REQUEST_SCHEMA)

        # Test with API
        response = client.post("/api/auth/register", json=valid_request)
        assert response.status_code == 201

    def test_registration_response_schema_validation(self, client: TestClient):
        """Test that registration response matches expected schema."""
        # Arrange
        request_data = {
            "email": "test@example.com",
            "username": "testuser",
            "display_name": "Test User",
            "password": "password123"
        }

        # Act
        response = client.post("/api/auth/register", json=request_data)

        # Assert
        assert response.status_code == 201
        response_data = response.json()

        # Validate response schema
        jsonschema.validate(response_data, USER_REGISTRATION_RESPONSE_SCHEMA)

        # Validate specific fields
        assert isinstance(response_data["id"], int)
        assert response_data["email"] == "test@example.com"
        assert response_data["username"] == "testuser"
        assert response_data["display_name"] == "Test User"
        assert "created_at" in response_data

    def test_registration_error_schema_validation(self, client: TestClient):
        """Test that registration error response matches expected schema."""
        # Arrange - Invalid request (missing required fields)
        invalid_request = {
            "email": "invalid-email",
            "username": "ab"  # Too short
        }

        # Act
        response = client.post("/api/auth/register", json=invalid_request)

        # Assert
        assert response.status_code == 422
        response_data = response.json()

        # Validate error response schema
        jsonschema.validate(response_data, ERROR_RESPONSE_SCHEMA)

        # Validate error structure
        assert "detail" in response_data
        assert isinstance(response_data["detail"], list)
        assert len(response_data["detail"]) > 0

        # Check error details
        for error in response_data["detail"]:
            assert "loc" in error
            assert "msg" in error
            assert "type" in error

    def test_registration_contract_breaking_changes(self, client: TestClient):
        """Test that API contract is stable (no breaking changes)."""
        # This test ensures the API doesn't change in ways that break clients

        # Arrange
        request_data = {
            "email": "test@example.com",
            "username": "testuser",
            "display_name": "Test User",
            "password": "password123"
        }

        # Act
        response = client.post("/api/auth/register", json=request_data)

        # Assert - Contract compliance
        assert response.status_code == 201
        response_data = response.json()

        # Required fields must be present
        required_fields = ["id", "email", "username", "display_name", "created_at"]
        for field in required_fields:
            assert field in response_data, f"Required field '{field}' missing from response"

        # Field types must be correct
        assert isinstance(response_data["id"], int)
        assert isinstance(response_data["email"], str)
        assert isinstance(response_data["username"], str)
        assert isinstance(response_data["display_name"], str)
        assert isinstance(response_data["created_at"], str)

        # No unexpected fields (additionalProperties: false)
        expected_fields = set(required_fields)
        actual_fields = set(response_data.keys())
        assert actual_fields == expected_fields, f"Unexpected fields: {actual_fields - expected_fields}"
```

---

### Part 3: OpenAPI Schema Testing (20 minutes)

#### Step 1: Generate OpenAPI Schema

```python
def test_openapi_schema_generation(self, client: TestClient):
    """Test that OpenAPI schema is generated correctly."""
    # Act
    response = client.get("/openapi.json")

    # Assert
    assert response.status_code == 200
    schema = response.json()

    # Validate OpenAPI structure
    assert "openapi" in schema
    assert "info" in schema
    assert "paths" in schema

    # Check specific endpoint
    assert "/api/auth/register" in schema["paths"]
    register_endpoint = schema["paths"]["/api/auth/register"]
    assert "post" in register_endpoint

    # Check request/response schemas
    post_spec = register_endpoint["post"]
    assert "requestBody" in post_spec
    assert "responses" in post_spec
    assert "201" in post_spec["responses"]
    assert "422" in post_spec["responses"]

def test_openapi_schema_validation(self, client: TestClient):
    """Test that OpenAPI schema is valid."""
    import jsonschema

    # Get OpenAPI schema
    response = client.get("/openapi.json")
    schema = response.json()

    # Validate against OpenAPI 3.0 schema
    openapi_schema = {
        "type": "object",
        "properties": {
            "openapi": {"type": "string"},
            "info": {"type": "object"},
            "paths": {"type": "object"}
        },
        "required": ["openapi", "info", "paths"]
    }

    jsonschema.validate(schema, openapi_schema)
```

---

### Part 4: Consumer-Driven Contract Testing (20 minutes)

#### Step 1: Create Consumer Contract

Create `backend/tests/contracts/consumer_contracts.py`:

```python
class ConsumerContract:
    """Defines what the frontend expects from the API."""

    @staticmethod
    def user_registration_contract():
        """Contract for user registration from frontend perspective."""
        return {
            "endpoint": "POST /api/auth/register",
            "expectations": {
                "request_format": {
                    "email": "string (email format)",
                    "username": "string (3-20 chars, alphanumeric + underscore)",
                    "display_name": "string (1-50 chars)",
                    "password": "string (8+ chars)"
                },
                "success_response": {
                    "status_code": 201,
                    "body": {
                        "id": "integer",
                        "email": "string",
                        "username": "string",
                        "display_name": "string",
                        "created_at": "string (ISO datetime)"
                    }
                },
                "error_response": {
                    "status_code": 422,
                    "body": {
                        "detail": "array of error objects"
                    }
                }
            }
        }

    @staticmethod
    def user_login_contract():
        """Contract for user login from frontend perspective."""
        return {
            "endpoint": "POST /api/auth/login",
            "expectations": {
                "request_format": {
                    "email": "string (email format)",
                    "password": "string"
                },
                "success_response": {
                    "status_code": 200,
                    "body": {
                        "access_token": "string",
                        "token_type": "string (bearer)",
                        "expires_in": "integer"
                    }
                },
                "error_response": {
                    "status_code": 401,
                    "body": {
                        "detail": "string (error message)"
                    }
                }
            }
        }
```

#### Step 2: Test Consumer Contracts

```python
def test_user_registration_consumer_contract(self, client: TestClient):
    """Test that API meets consumer expectations."""
    contract = ConsumerContract.user_registration_contract()

    # Test success case
    request_data = {
        "email": "test@example.com",
        "username": "testuser",
        "display_name": "Test User",
        "password": "password123"
    }

    response = client.post("/api/auth/register", json=request_data)

    # Validate against consumer contract
    assert response.status_code == 201
    response_data = response.json()

    # Check required fields exist
    expected_fields = ["id", "email", "username", "display_name", "created_at"]
    for field in expected_fields:
        assert field in response_data, f"Consumer expects field '{field}' in response"

    # Check field types match expectations
    assert isinstance(response_data["id"], int)
    assert isinstance(response_data["email"], str)
    assert isinstance(response_data["username"], str)
    assert isinstance(response_data["display_name"], str)
    assert isinstance(response_data["created_at"], str)

def test_user_login_consumer_contract(self, client: TestClient, db_session):
    """Test that login API meets consumer expectations."""
    # Arrange - Create user
    from models import User
    from auth import get_password_hash

    user = User(
        email="test@example.com",
        username="testuser",
        display_name="Test User",
        hashed_password=get_password_hash("password123")
    )
    db_session.add(user)
    db_session.commit()

    contract = ConsumerContract.user_login_contract()

    # Test success case
    request_data = {
        "email": "test@example.com",
        "password": "password123"
    }

    response = client.post("/api/auth/login", json=request_data)

    # Validate against consumer contract
    assert response.status_code == 200
    response_data = response.json()

    # Check required fields exist
    expected_fields = ["access_token", "token_type", "expires_in"]
    for field in expected_fields:
        assert field in response_data, f"Consumer expects field '{field}' in response"

    # Check field types and values
    assert isinstance(response_data["access_token"], str)
    assert response_data["token_type"] == "bearer"
    assert isinstance(response_data["expires_in"], int)
```

---

## 💪 Challenge Exercises

### Challenge 1: Test API Versioning

```python
def test_api_versioning_contract(self, client: TestClient):
    """Test that API versioning doesn't break contracts."""
    # TODO: Test that v1 API maintains backward compatibility
    # 1. Test that old API endpoints still work
    # 2. Test that response format hasn't changed
    # 3. Test that new fields are optional
    pass
```

### Challenge 2: Test Error Contract Consistency

```python
def test_error_contract_consistency(self, client: TestClient):
    """Test that all API errors follow the same contract."""
    # TODO: Test that all error responses follow the same format
    # 1. Test 400 errors
    # 2. Test 401 errors
    # 3. Test 404 errors
    # 4. Test 500 errors
    # All should follow the same error response schema
    pass
```

---

## 🎓 Advanced Patterns

### Contract Testing with Pytest Fixtures

```python
@pytest.fixture
def api_contract_validator():
    """Fixture for validating API contracts."""
    class ContractValidator:
        def __init__(self, client):
            self.client = client

        def validate_endpoint(self, method, endpoint, request_data, expected_status, expected_schema):
            """Validate an API endpoint against its contract."""
            response = getattr(self.client, method.lower())(endpoint, json=request_data)

            assert response.status_code == expected_status
            if expected_schema:
                jsonschema.validate(response.json(), expected_schema)

            return response

    return ContractValidator

def test_contract_validation_with_fixture(self, api_contract_validator, client):
    """Test contract validation using fixture."""
    validator = api_contract_validator(client)

    request_data = {
        "email": "test@example.com",
        "username": "testuser",
        "display_name": "Test User",
        "password": "password123"
    }

    response = validator.validate_endpoint(
        "POST", "/api/auth/register", request_data, 201, USER_REGISTRATION_RESPONSE_SCHEMA
    )

    assert response.json()["email"] == "test@example.com"
```

### Contract Testing with Test Data

```python
@pytest.mark.parametrize("test_case", [
    {
        "name": "valid_registration",
        "request": {
            "email": "test@example.com",
            "username": "testuser",
            "display_name": "Test User",
            "password": "password123"
        },
        "expected_status": 201,
        "expected_schema": USER_REGISTRATION_RESPONSE_SCHEMA
    },
    {
        "name": "invalid_email",
        "request": {
            "email": "invalid-email",
            "username": "testuser",
            "display_name": "Test User",
            "password": "password123"
        },
        "expected_status": 422,
        "expected_schema": ERROR_RESPONSE_SCHEMA
    }
])
def test_registration_contract_cases(self, client, test_case):
    """Test registration contract with multiple test cases."""
    response = client.post("/api/auth/register", json=test_case["request"])

    assert response.status_code == test_case["expected_status"]
    if test_case["expected_schema"]:
        jsonschema.validate(response.json(), test_case["expected_schema"])
```

---

## ✅ Completion Checklist

- [ ] Understand what API contracts are and why they matter
- [ ] Can validate API requests and responses against schemas
- [ ] Can test OpenAPI schema generation and validation
- [ ] Can write consumer-driven contract tests
- [ ] Can detect breaking changes in API contracts
- [ ] Completed all challenge exercises
- [ ] Understand the difference between contract and integration testing

---

## 💡 Pro Tips

1. **Start with consumer contracts** - Define what frontend needs first
2. **Validate schemas strictly** - Catch type mismatches early
3. **Test error contracts too** - Errors should follow consistent format
4. **Use OpenAPI for documentation** - Keep contracts and docs in sync
5. **Test breaking changes** - Ensure API changes don't break clients

---

## 📚 Next Steps

**Continue building your skills:**

- **[Lab 9: Basic E2E Testing (Python)](LAB_09_Basic_E2E_Testing_Python.md)** - End-to-end testing
- **[Lab 10: Advanced E2E Patterns (Python)](LAB_10_Advanced_E2E_Patterns_Python.md)** - Advanced E2E testing
- **[Lab 11: Cross-Browser Testing (Python)](LAB_11_Cross_Browser_Testing_Python.md)** - Multi-browser testing

---

**🎉 Congratulations!** You now understand contract testing and can ensure API compatibility between frontend and backend!

**Next Lab:** [Lab 9: Basic E2E Testing (Python)](LAB_09_Basic_E2E_Testing_Python.md)
