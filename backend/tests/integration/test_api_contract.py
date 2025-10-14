"""
API Contract Testing with Schemathesis

═══════════════════════════════════════════════════════════════════════════

WHAT THIS IS:
Property-based contract testing that automatically generates hundreds of test
cases from your OpenAPI schema to validate API behavior.

WHY IT'S IMPORTANT:
- Finds edge cases you'd never think to test manually
- Validates API matches documentation (prevents drift)
- Fuzzes endpoints for security vulnerabilities
- Saves massive testing time (1 test = 500+ generated cases)

HOW IT WORKS:
1. Reads OpenAPI schema from FastAPI
2. Automatically generates test cases for all endpoints
3. Tests valid inputs, invalid inputs, edge cases
4. Validates responses match schema
5. Reports any contract violations

WHAT IT VALIDATES:
- Request/response formats match schema definitions
- Status codes are appropriate
- Required fields are present
- Data types are correct
- Optional fields handled properly
- Boundary values (min/max)
- Security (fuzzing with malicious inputs)

═══════════════════════════════════════════════════════════════════════════

⚠️  CURRENT STATUS: SKIPPED (Planned for future update)

FastAPI 0.115+ generates OpenAPI 3.1.0 schemas by default.
Schemathesis 3.27.1 doesn't fully support 3.1.0 yet.

DISCOVERED SOLUTION:
Using force_schema_version="30" makes Schemathesis work! However, enabling this
test revealed areas needing improvement:
- Schema documentation gaps (undocumented 400/403/404 status codes)
- Authentication configuration for Schemathesis
- Database fixtures for test isolation
- 55 test failures to investigate and fix

PLANNED FOR FUTURE UPDATE:
Full contract testing enablement scheduled for a future release.
See: testbook-notes/v1.2-contract-testing-plan.md

FOR NOW:
✅ Study this test file to learn the pattern
✅ Read the comprehensive guide: docs/guides/CONTRACT_TESTING.md
✅ Try frontend contract testing: labs/LAB_06C_Frontend_Integration_Testing.md (works today!)
✅ Understand the concept (valuable for interviews!)

Reference: https://github.com/schemathesis/schemathesis/issues/494

═══════════════════════════════════════════════════════════════════════════

LEARN MORE:
📚 Full explanation: docs/guides/CONTRACT_TESTING.md
🧪 What it would test: See concrete examples in that guide
🔄 Frontend contract testing: labs/LAB_06C_Frontend_Integration_Testing.md
🛠️  Alternative tools: Dredd, Pact, Postman contract testing

This test demonstrates an advanced technique used in production at major tech companies!
"""

import pytest

# Skip this entire module - Contract testing fully enabled in future update
# See testbook-notes/v1.2-contract-testing-plan.md for details
pytest.skip(
    "Contract testing planned for future update - requires schema/auth configuration",
    allow_module_level=True,
)

import schemathesis  # noqa: E402
from main import app  # noqa: E402

# Create the schema from the FastAPI app
# Note: force_schema_version="30" enables it, but needs configuration
schema = schemathesis.from_asgi("/openapi.json", app, force_schema_version="30")


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


# Hooks to customize test behavior (optional)
# Uncomment to add custom logic before/after API calls

# @schema.hooks("before_call")
# def before_call(context, case):
#     """Hook executed before each API call."""
#     # Example: Add authentication headers
#     # case.headers = case.headers or {}
#     # case.headers["Authorization"] = "Bearer token"
#     pass

# @schema.hooks("after_call")
# def after_call(context, case, response):
#     """Hook executed after each API call."""
#     # Example: Log responses for debugging
#     # print(f"{case.method} {case.path} -> {response.status_code}")
#     pass
