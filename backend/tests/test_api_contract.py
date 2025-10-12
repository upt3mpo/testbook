"""
API Contract Testing with Schemathesis

Tests that all API endpoints conform to their OpenAPI schema specification.
Schemathesis generates test cases based on the OpenAPI schema and validates:
- Request/response formats match schema definitions
- Status codes are appropriate
- Required fields are present
- Data types are correct
"""

import schemathesis
from main import app

# Create the schema from the FastAPI app
schema = schemathesis.from_asgi("/openapi.json", app)


@schema.parametrize()
def test_api_contract(case):
    """
    Property-based contract test that validates all endpoints against OpenAPI spec.

    Schemathesis will:
    1. Generate test cases from the OpenAPI schema
    2. Send requests to the endpoints
    3. Validate responses match the schema
    4. Check status codes are appropriate
    """
    # Execute the test case
    response = case.call_asgi()

    # Validate the response conforms to the schema
    case.validate_response(response)


@schema.parametrize(endpoint="/api/health")
def test_health_endpoint_contract(case):
    """Specific contract test for health check endpoint"""
    response = case.call_asgi()
    case.validate_response(response)

    # Additional assertions beyond schema validation
    assert response.status_code == 200
    assert "status" in response.json()


@schema.parametrize(endpoint="/api")
def test_root_endpoint_contract(case):
    """Specific contract test for root endpoint"""
    response = case.call_asgi()
    case.validate_response(response)

    assert response.status_code == 200
    assert "message" in response.json()


# Hook to customize test behavior
@schema.hooks.apply("before_call")
def before_call(context, case):
    """
    Hook executed before each API call.
    Can be used to add authentication, headers, or modify requests.
    """
    # Example: Add common headers if needed
    # case.headers = case.headers or {}
    # case.headers["User-Agent"] = "Schemathesis/Test"
    pass


@schema.hooks.apply("after_call")
def after_call(context, case, response):
    """
    Hook executed after each API call.
    Can be used for additional logging or validation.
    """
    # Example: Log responses for debugging
    # print(f"Called {case.method} {case.path} -> {response.status_code}")
    pass
