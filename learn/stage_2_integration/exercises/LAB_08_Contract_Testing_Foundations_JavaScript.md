# 🧪 Lab 8: Contract Testing Foundations

**Estimated Time:** 90 minutes<br>
**Difficulty:** Intermediate<br>
**Language:** 🟨 JavaScript<br>
**Prerequisites:** Lab 7 completed

**💡 Need Python instead?** Try [Lab 8: Contract Testing Foundations (Python)](LAB_08_Contract_Testing_Foundations_Python.md)!

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

```javascript
/**
 * API Contract Definition for User Registration
 *
 * This contract defines the expected behavior of the user registration endpoint.
 * It serves as a specification that both frontend and backend teams can agree on,
 * ensuring compatibility and preventing integration failures.
 */

// Example API contract for user registration
const USER_REGISTRATION_CONTRACT = {
  endpoint: "POST /api/auth/register", // HTTP method and URL path

  request: {
    // Required fields that the API expects
    email: "string (required, valid email format)", // Must be valid email
    username: "string (required, 3-20 characters)", // Username length constraint
    display_name: "string (required, 1-50 characters)", // Display name length constraint
    password: "string (required, 8+ characters)", // Password strength requirement
  },

  response: {
    success: {
      status_code: 201, // Created - user successfully registered
      body: {
        id: "integer", // Auto-generated user ID
        email: "string", // User's email address
        username: "string", // User's chosen username
        display_name: "string", // User's display name
        created_at: "datetime", // Timestamp when user was created
      },
    },
    error: {
      status_code: 422, // Unprocessable Entity - validation failed
      body: {
        detail: "array of validation errors", // List of specific validation errors
      },
    },
  },
};
```

---

### Part 2: Schema Validation Testing (30 minutes)

#### Step 1: Install Schema Validation Library

```bash
cd frontend
npm install --save-dev ajv
```

#### Step 2: Create Schema Definitions

Create `frontend/src/tests/schemas/userSchemas.js`:

```javascript
import Ajv from "ajv";

const ajv = new Ajv();

// User registration request schema
export const USER_REGISTRATION_REQUEST_SCHEMA = {
  type: "object",
  properties: {
    email: {
      type: "string",
      format: "email",
      minLength: 1,
    },
    username: {
      type: "string",
      minLength: 3,
      maxLength: 20,
      pattern: "^[a-zA-Z0-9_]+$",
    },
    display_name: {
      type: "string",
      minLength: 1,
      maxLength: 50,
    },
    password: {
      type: "string",
      minLength: 8,
    },
  },
  required: ["email", "username", "display_name", "password"],
  additionalProperties: false,
};

// User registration response schema
export const USER_REGISTRATION_RESPONSE_SCHEMA = {
  type: "object",
  properties: {
    id: { type: "integer" },
    email: { type: "string" },
    username: { type: "string" },
    display_name: { type: "string" },
    created_at: { type: "string", format: "date-time" },
  },
  required: ["id", "email", "username", "display_name", "created_at"],
  additionalProperties: false,
};

// Error response schema
export const ERROR_RESPONSE_SCHEMA = {
  type: "object",
  properties: {
    detail: {
      type: "array",
      items: {
        type: "object",
        properties: {
          loc: { type: "array" },
          msg: { type: "string" },
          type: { type: "string" },
        },
        required: ["loc", "msg", "type"],
      },
    },
  },
  required: ["detail"],
  additionalProperties: false,
};

// Schema validation functions
export const validateUserRegistrationRequest = ajv.compile(
  USER_REGISTRATION_REQUEST_SCHEMA
);
export const validateUserRegistrationResponse = ajv.compile(
  USER_REGISTRATION_RESPONSE_SCHEMA
);
export const validateErrorResponse = ajv.compile(ERROR_RESPONSE_SCHEMA);
```

#### Step 3: Create Schema Validation Tests

Create `frontend/src/tests/contracts/userContracts.test.js`:

```javascript
import { describe, it, expect, beforeEach } from "vitest";
import {
  validateUserRegistrationRequest,
  validateUserRegistrationResponse,
  validateErrorResponse,
} from "../schemas/userSchemas";

describe("User Registration Contract", () => {
  let mockFetch;

  beforeEach(() => {
    // Mock fetch for API calls
    mockFetch = vi.fn();
    global.fetch = mockFetch;
  });

  it("should validate registration request schema", () => {
    // Valid request data
    const validRequest = {
      email: "test@example.com",
      username: "testuser",
      display_name: "Test User",
      password: "password123",
    };

    // Validate request schema
    const isValid = validateUserRegistrationRequest(validRequest);
    expect(isValid).toBe(true);

    if (!isValid) {
      console.log(validateUserRegistrationRequest.errors);
    }
  });

  it("should validate registration response schema", async () => {
    // Mock successful API response
    const mockResponse = {
      id: 1,
      email: "test@example.com",
      username: "testuser",
      display_name: "Test User",
      created_at: "2024-01-01T00:00:00Z",
    };

    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 201,
      json: () => Promise.resolve(mockResponse),
    });

    // Make API call
    const response = await fetch("/api/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: "test@example.com",
        username: "testuser",
        display_name: "Test User",
        password: "password123",
      }),
    });

    const responseData = await response.json();

    // Validate response schema
    const isValid = validateUserRegistrationResponse(responseData);
    expect(isValid).toBe(true);

    if (!isValid) {
      console.log(validateUserRegistrationResponse.errors);
    }

    // Validate specific fields
    expect(responseData.id).toBeTypeOf("number");
    expect(responseData.email).toBe("test@example.com");
    expect(responseData.username).toBe("testuser");
    expect(responseData.display_name).toBe("Test User");
    expect(responseData.created_at).toBeTypeOf("string");
  });

  it("should validate error response schema", async () => {
    // Mock error API response
    const mockErrorResponse = {
      detail: [
        {
          loc: ["body", "email"],
          msg: "field required",
          type: "value_error.missing",
        },
        {
          loc: ["body", "username"],
          msg: "ensure this value has at least 3 characters",
          type: "value_error.any_str.min_length",
        },
      ],
    };

    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 422,
      json: () => Promise.resolve(mockErrorResponse),
    });

    // Make API call with invalid data
    const response = await fetch("/api/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: "invalid-email",
        username: "ab", // Too short
      }),
    });

    const responseData = await response.json();

    // Validate error response schema
    const isValid = validateErrorResponse(responseData);
    expect(isValid).toBe(true);

    if (!isValid) {
      console.log(validateErrorResponse.errors);
    }

    // Validate error structure
    expect(responseData.detail).toBeTypeOf("object");
    expect(Array.isArray(responseData.detail)).toBe(true);
    expect(responseData.detail.length).toBeGreaterThan(0);

    // Check error details
    responseData.detail.forEach((error) => {
      expect(error).toHaveProperty("loc");
      expect(error).toHaveProperty("msg");
      expect(error).toHaveProperty("type");
    });
  });

  it("should detect contract breaking changes", async () => {
    // This test ensures the API doesn't change in ways that break clients

    // Mock response with all required fields
    const mockResponse = {
      id: 1,
      email: "test@example.com",
      username: "testuser",
      display_name: "Test User",
      created_at: "2024-01-01T00:00:00Z",
    };

    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 201,
      json: () => Promise.resolve(mockResponse),
    });

    const response = await fetch("/api/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: "test@example.com",
        username: "testuser",
        display_name: "Test User",
        password: "password123",
      }),
    });

    const responseData = await response.json();

    // Contract compliance checks
    expect(response.status).toBe(201);

    // Required fields must be present
    const requiredFields = [
      "id",
      "email",
      "username",
      "display_name",
      "created_at",
    ];
    requiredFields.forEach((field) => {
      expect(responseData).toHaveProperty(field);
    });

    // Field types must be correct
    expect(responseData.id).toBeTypeOf("number");
    expect(responseData.email).toBeTypeOf("string");
    expect(responseData.username).toBeTypeOf("string");
    expect(responseData.display_name).toBeTypeOf("string");
    expect(responseData.created_at).toBeTypeOf("string");

    // No unexpected fields (additionalProperties: false)
    const expectedFields = new Set(requiredFields);
    const actualFields = new Set(Object.keys(responseData));
    const unexpectedFields = [...actualFields].filter(
      (field) => !expectedFields.has(field)
    );
    expect(unexpectedFields).toHaveLength(0);
  });
});
```

---

### Part 3: OpenAPI Schema Testing (20 minutes)

#### Step 1: Test OpenAPI Schema Generation

```javascript
it("should generate valid OpenAPI schema", async () => {
  // Mock OpenAPI schema response
  const mockOpenAPISchema = {
    openapi: "3.0.0",
    info: {
      title: "Testbook API",
      version: "1.0.0",
    },
    paths: {
      "/api/auth/register": {
        post: {
          requestBody: {
            content: {
              "application/json": {
                schema: {
                  type: "object",
                  properties: {
                    email: { type: "string" },
                    username: { type: "string" },
                    display_name: { type: "string" },
                    password: { type: "string" },
                  },
                },
              },
            },
          },
          responses: {
            201: {
              description: "User created successfully",
              content: {
                "application/json": {
                  schema: {
                    type: "object",
                    properties: {
                      id: { type: "integer" },
                      email: { type: "string" },
                      username: { type: "string" },
                      display_name: { type: "string" },
                      created_at: { type: "string" },
                    },
                  },
                },
              },
            },
            422: {
              description: "Validation error",
              content: {
                "application/json": {
                  schema: {
                    type: "object",
                    properties: {
                      detail: {
                        type: "array",
                        items: {
                          type: "object",
                          properties: {
                            loc: { type: "array" },
                            msg: { type: "string" },
                            type: { type: "string" },
                          },
                        },
                      },
                    },
                  },
                },
              },
            },
          },
        },
      },
    },
  };

  mockFetch.mockResolvedValueOnce({
    ok: true,
    json: () => Promise.resolve(mockOpenAPISchema),
  });

  const response = await fetch("/openapi.json");
  const schema = await response.json();

  // Validate OpenAPI structure
  expect(schema).toHaveProperty("openapi");
  expect(schema).toHaveProperty("info");
  expect(schema).toHaveProperty("paths");

  // Check specific endpoint
  expect(schema.paths).toHaveProperty("/api/auth/register");
  const registerEndpoint = schema.paths["/api/auth/register"];
  expect(registerEndpoint).toHaveProperty("post");

  // Check request/response schemas
  const postSpec = registerEndpoint.post;
  expect(postSpec).toHaveProperty("requestBody");
  expect(postSpec).toHaveProperty("responses");
  expect(postSpec.responses).toHaveProperty("201");
  expect(postSpec.responses).toHaveProperty("422");
});
```

---

### Part 4: Consumer-Driven Contract Testing (20 minutes)

#### Step 1: Create Consumer Contract

Create `frontend/src/tests/contracts/consumerContracts.js`:

```javascript
export class ConsumerContract {
  /**
   * Contract for user registration from frontend perspective.
   */
  static userRegistrationContract() {
    return {
      endpoint: "POST /api/auth/register",
      expectations: {
        requestFormat: {
          email: "string (email format)",
          username: "string (3-20 chars, alphanumeric + underscore)",
          display_name: "string (1-50 chars)",
          password: "string (8+ chars)",
        },
        successResponse: {
          statusCode: 201,
          body: {
            id: "integer",
            email: "string",
            username: "string",
            display_name: "string",
            created_at: "string (ISO datetime)",
          },
        },
        errorResponse: {
          statusCode: 422,
          body: {
            detail: "array of error objects",
          },
        },
      },
    };
  }

  /**
   * Contract for user login from frontend perspective.
   */
  static userLoginContract() {
    return {
      endpoint: "POST /api/auth/login",
      expectations: {
        requestFormat: {
          email: "string (email format)",
          password: "string",
        },
        successResponse: {
          statusCode: 200,
          body: {
            access_token: "string",
            token_type: "string (bearer)",
            expires_in: "integer",
          },
        },
        errorResponse: {
          statusCode: 401,
          body: {
            detail: "string (error message)",
          },
        },
      },
    };
  }
}
```

#### Step 2: Test Consumer Contracts

```javascript
describe("Consumer Contract Testing", () => {
  let mockFetch;

  beforeEach(() => {
    mockFetch = vi.fn();
    global.fetch = mockFetch;
  });

  it("should meet user registration consumer expectations", async () => {
    const contract = ConsumerContract.userRegistrationContract();

    // Mock successful response
    const mockResponse = {
      id: 1,
      email: "test@example.com",
      username: "testuser",
      display_name: "Test User",
      created_at: "2024-01-01T00:00:00Z",
    };

    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 201,
      json: () => Promise.resolve(mockResponse),
    });

    // Make API call
    const response = await fetch("/api/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: "test@example.com",
        username: "testuser",
        display_name: "Test User",
        password: "password123",
      }),
    });

    const responseData = await response.json();

    // Validate against consumer contract
    expect(response.status).toBe(201);

    // Check required fields exist
    const expectedFields = [
      "id",
      "email",
      "username",
      "display_name",
      "created_at",
    ];
    expectedFields.forEach((field) => {
      expect(responseData).toHaveProperty(field);
    });

    // Check field types match expectations
    expect(responseData.id).toBeTypeOf("number");
    expect(responseData.email).toBeTypeOf("string");
    expect(responseData.username).toBeTypeOf("string");
    expect(responseData.display_name).toBeTypeOf("string");
    expect(responseData.created_at).toBeTypeOf("string");
  });

  it("should meet user login consumer expectations", async () => {
    const contract = ConsumerContract.userLoginContract();

    // Mock successful login response
    const mockResponse = {
      access_token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      token_type: "bearer",
      expires_in: 3600,
    };

    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: () => Promise.resolve(mockResponse),
    });

    // Make API call
    const response = await fetch("/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: "test@example.com",
        password: "password123",
      }),
    });

    const responseData = await response.json();

    // Validate against consumer contract
    expect(response.status).toBe(200);

    // Check required fields exist
    const expectedFields = ["access_token", "token_type", "expires_in"];
    expectedFields.forEach((field) => {
      expect(responseData).toHaveProperty(field);
    });

    // Check field types and values
    expect(responseData.access_token).toBeTypeOf("string");
    expect(responseData.token_type).toBe("bearer");
    expect(responseData.expires_in).toBeTypeOf("number");
  });
});
```

---

## 💪 Challenge Exercises

### Challenge 1: Test API Versioning

```javascript
it("should maintain backward compatibility across API versions", async () => {
  // TODO: Test that v1 API maintains backward compatibility
  // 1. Test that old API endpoints still work
  // 2. Test that response format hasn't changed
  // 3. Test that new fields are optional
});
```

### Challenge 2: Test Error Contract Consistency

```javascript
it("should follow consistent error contract across all endpoints", async () => {
  // TODO: Test that all API errors follow the same format
  // 1. Test 400 errors
  // 2. Test 401 errors
  // 3. Test 404 errors
  // 4. Test 500 errors
  // All should follow the same error response schema
});
```

---

## 🎓 Advanced Patterns

### Contract Testing with Custom Matchers

```javascript
// Custom Vitest matchers for contract testing
expect.extend({
  toMatchContract(received, contract) {
    const { pass, message } = this.utils.matcherHint(
      "toMatchContract",
      received,
      contract
    );

    // Validate response structure
    const requiredFields = Object.keys(
      contract.expectations.successResponse.body
    );
    const missingFields = requiredFields.filter(
      (field) => !(field in received)
    );

    if (missingFields.length > 0) {
      return {
        pass: false,
        message: () =>
          `Expected response to have fields: ${missingFields.join(", ")}`,
      };
    }

    return { pass: true, message: () => "Response matches contract" };
  },
});

// Usage
it("should match user registration contract", async () => {
  const response = await fetch("/api/auth/register", {
    /* ... */
  });
  const data = await response.json();

  expect(data).toMatchContract(ConsumerContract.userRegistrationContract());
});
```

### Contract Testing with Test Data

```javascript
describe.each([
  {
    name: "valid_registration",
    request: {
      email: "test@example.com",
      username: "testuser",
      display_name: "Test User",
      password: "password123",
    },
    expectedStatus: 201,
    expectedSchema: USER_REGISTRATION_RESPONSE_SCHEMA,
  },
  {
    name: "invalid_email",
    request: {
      email: "invalid-email",
      username: "testuser",
      display_name: "Test User",
      password: "password123",
    },
    expectedStatus: 422,
    expectedSchema: ERROR_RESPONSE_SCHEMA,
  },
])(
  "Registration Contract Cases",
  ({ name, request, expectedStatus, expectedSchema }) => {
    it(`should handle ${name} case`, async () => {
      mockFetch.mockResolvedValueOnce({
        ok: expectedStatus < 400,
        status: expectedStatus,
        json: () =>
          Promise.resolve({
            /* mock response */
          }),
      });

      const response = await fetch("/api/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(request),
      });

      expect(response.status).toBe(expectedStatus);

      if (expectedSchema) {
        const responseData = await response.json();
        const isValid = validateUserRegistrationResponse(responseData);
        expect(isValid).toBe(true);
      }
    });
  }
);
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

- **[Lab 9: Basic E2E Testing (JavaScript)](LAB_09_Basic_E2E_Testing_JavaScript.md)** - End-to-end testing
- **[Lab 10: Advanced E2E Patterns (JavaScript)](LAB_10_Advanced_E2E_Patterns_JavaScript.md)** - Advanced E2E testing
- **[Lab 11: Cross-Browser Testing (JavaScript)](LAB_11_Cross_Browser_Testing_JavaScript.md)** - Multi-browser testing

---

**🎉 Congratulations!** You now understand contract testing and can ensure API compatibility between frontend and backend!

**Next Lab:** [Lab 9: Basic E2E Testing (JavaScript)](LAB_09_Basic_E2E_Testing_JavaScript.md)
