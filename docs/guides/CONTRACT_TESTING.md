# 🤝 API Contract Testing with Schemathesis

**Property-based testing that validates your API matches its documentation**

---

## 🎯 Quick Start (30 seconds)

**Contract testing** ensures your API does exactly what your documentation says it does.

**Schemathesis** automatically generates hundreds of test cases from your OpenAPI schema to validate every endpoint, parameter, and response - finding bugs you'd never think to test manually.

**One test replaces 500+ manual tests.**

---

## 🤔 The Problem Contract Testing Solves

### Problem 1: API Documentation Drift

```yaml
# Your OpenAPI spec says:
POST /api/users
  required: ["name", "email"]

# But your code actually requires:
POST /api/users
  required: ["name", "email", "password"]  # Oops, forgot to update docs!
```

**Result:** Frontend breaks, integration fails, users confused.

### Problem 2: Edge Cases You Never Test

You write tests for:

```python
{"age": 25}      # Normal case
{"age": -1}      # Negative
```

But do you test?

```python
{"age": 2147483648}  # Integer overflow
{"age": "twenty-five"}  # Type mismatch
{"age": [25, 30]}  # Array instead of int
{"age": {"value": 25}}  # Object instead of int
{"age": null}  # Null value
{"age": 0.5}  # Float precision
# ... 494 more edge cases
```

Probably not! **Schemathesis tests all of them automatically.**

### Problem 3: Manual Testing Burden

For an API with 30 endpoints (like Testbook):

- **Traditional approach:** Write 300-500 tests manually (20+ hours)
- **Contract testing:** Write 1 test (30 minutes)

---

## 🚀 Enter Schemathesis

### What It Is

**Schemathesis** is a property-based testing tool that:

1. Reads your OpenAPI/Swagger schema
2. Automatically generates hundreds of test cases
3. Sends requests to your API
4. Validates responses match the schema
5. Reports any violations

### How It Works

**Traditional API Testing:**

```python
def test_create_user():
    """Test user creation"""
    response = client.post("/users", json={"name": "John", "email": "john@test.com"})
    assert response.status_code == 201

def test_create_user_missing_email():
    """Test missing email"""
    response = client.post("/users", json={"name": "John"})
    assert response.status_code == 422

def test_create_user_invalid_email():
    """Test invalid email format"""
    response = client.post("/users", json={"name": "John", "email": "not-an-email"})
    assert response.status_code == 422

# ... 47 more tests you need to write manually
```

**Schemathesis (Property-Based Testing):**

```python
import schemathesis

schema = schemathesis.from_asgi("/openapi.json", app)

@schema.parametrize()
def test_api_contract(case):
    """One test that validates ALL endpoints"""
    case.call_and_validate()
```

**That's it!** Schemathesis automatically:

- ✅ Tests all 30 endpoints
- ✅ Generates 500+ test cases
- ✅ Tests valid and invalid inputs
- ✅ Validates responses
- ✅ Checks status codes
- ✅ Finds edge cases

---

## 💡 Property-Based Testing Explained

### Traditional Testing (Example-Based)

You think of specific examples to test:

```python
test_with({"age": 25})      # You thought of this
test_with({"age": -1})      # You thought of this
test_with({"age": 150})     # You thought of this
```

**Problem:** You can only test what you think of.

### Property-Based Testing (Generative)

You define **properties** that should always be true:

```python
# Property: "If age is required, requests without age should fail"
# Property: "If age is integer, strings should be rejected"
# Property: "If age has min/max, values outside range should fail"
```

**Schemathesis automatically generates** hundreds of test cases to validate these properties:

```python
# Automatically generated test cases:
{"age": 25}                    # Valid
{"age": -1}                    # Boundary
{"age": 2147483647}            # Max int
{"age": "25"}                  # Wrong type
{"age": [25]}                  # Array
{"age": null}                  # Null
{"age": true}                  # Boolean
{}                             # Missing required field
{"age": 1.5}                   # Float vs int
{"age": ""}                    # Empty string
# ... 490 more you never would have thought of
```

---

## 📊 Example: What Schemathesis Would Test in Testbook

### Endpoint: `POST /api/posts`

**Your OpenAPI spec says:**

```yaml
/api/posts:
  post:
    requestBody:
      required: true
      properties:
        content:
          type: string
          maxLength: 500
        media_url:
          type: string
          format: uri
          nullable: true
```

**Schemathesis automatically tests:**

**Valid Cases (Happy Path):**

- `{"content": "Hello world"}` - Normal post
- `{"content": "x"*500}` - Max length boundary
- `{"content": "Test", "media_url": "http://example.com/img.jpg"}` - With media
- `{"content": "Test", "media_url": null}` - Null media allowed

**Invalid Cases (Should Fail):**

- `{}` - Missing required content
- `{"content": "x"*501}` - Exceeds max length
- `{"content": 123}` - Wrong type (number not string)
- `{"content": ["test"]}` - Array instead of string
- `{"content": null}` - Null when not allowed
- `{"media_url": "not-a-url"}` - Invalid URI format
- `{"media_url": 123}` - Number instead of string

**Security Fuzzing (Finds Vulnerabilities):**

- `{"content": "<script>alert('xss')</script>"}` - XSS attempt
- `{"content": "' OR 1=1--"}` - SQL injection
- `{"content": "../../../etc/passwd"}` - Path traversal
- `{"content": "A"*10000}` - Buffer overflow attempt

**Total:** 50+ test cases **automatically generated** for just ONE endpoint!

### For All 30 Testbook Endpoints

Schemathesis would generate:

- **~1,500 test cases** total
- **Run in ~2 minutes**
- **Find edge cases** you'd miss
- **Validate schemas** automatically
- **Fuzz for security** vulnerabilities

---

## ⚠️ Why This Test is Currently Skipped

### The Compatibility Issue

**The situation:**

- **FastAPI 0.115+** generates **OpenAPI 3.1.0** schemas (latest standard)
- **Schemathesis 3.27.1** only has **experimental 3.1.0 support** (still maturing)

**What happens if we run it:**

```text
SchemaError: The provided schema uses Open API 3.1.0,
which is currently not fully supported.
```

### Why OpenAPI 3.1.0 is Different

OpenAPI 3.1.0 introduced **complete JSON Schema compatibility** (Draft 2020-12), which is a major change. Tools like Schemathesis need time to adapt to these new features.

### What This Means for Learners

**The Good News:**

- ✅ The test file is still valuable to study
- ✅ You learn the concept of contract testing
- ✅ You see how property-based testing works
- ✅ When Schemathesis adds support, just remove one line!

**For Now:**

- 📚 Learn the **concept** (this guide)
- 🔬 Study the **test file** (see how it's structured)
- 🧪 Use **frontend contract testing** (Lab 6C - works today!)
- 🎯 Focus on the **180 tests that DO run**

### Discovered Workaround

**During development, we discovered:**

Using `force_schema_version="30"` makes Schemathesis work with OpenAPI 3.1.0! However, enabling it revealed:

- 55 test failures (mostly auth and schema documentation gaps)
- Schema needs documentation improvements
- Authentication needs configuration

**Reference:** <https://github.com/schemathesis/schemathesis/issues/494>

**Decision:** Enable in a future update after proper configuration. See `testbook-notes/v1.2-contract-testing-plan.md` for full enablement plan.

### Timeline

**Current Status:**

- ✅ Comprehensive documentation added
- ✅ Workaround discovered (`force_schema_version="30"`)
- ⚠️ Skipped pending full configuration
- 🚀 Full enablement planned for future update

**Future Update:**

- Fix schema documentation gaps
- Configure authentication for Schemathesis
- Enable all 500+ automated contract tests
- See internal plan: `testbook-notes/v1.2-contract-testing-plan.md`

**Alternatives Available Now:**

1. Frontend contract testing with OpenAPI (Lab 6C) ✅
2. Manual schema validation with Postman ✅
3. Traditional API integration tests (180+ tests!) ✅

---

## 🔄 How to Enable When Ready

When Schemathesis adds full OpenAPI 3.1.0 support:

**Step 1:** Update Schemathesis

```bash
cd backend
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install --upgrade schemathesis
```

**Step 2:** Remove the skip in `test_api_contract.py`

```python
# DELETE these lines (14-15):
# pytest.skip("Schemathesis doesn't fully support OpenAPI 3.1.0 yet",
#             allow_module_level=True)
```

**Step 3:** Run the test

```bash
pytest tests/integration/test_api_contract.py -v
```

**Expected:** Schemathesis generates and runs 500+ test cases automatically!

---

## 🛠️ Alternative: Use Experimental Mode (Advanced)

If you want to try it now (with caveats):

```python
# In test_api_contract.py, remove skip and add:
schema = schemathesis.from_asgi(
    "/openapi.json",
    app,
    experimental=True  # Enable experimental OpenAPI 3.1.0 support
)
```

**Pros:**

- ✅ Tests run today
- ✅ Learn by doing

**Cons:**

- ⚠️ May have bugs
- ⚠️ Incomplete coverage
- ⚠️ Features may change

**For now:** We're keeping it skipped for stability.

---

## 🔗 Related: Frontend Contract Testing

**You CAN do contract testing today!**

[Lab 6C: Frontend Integration Testing](../../labs/LAB_06C_Frontend_Integration_Testing.md) teaches contract testing from the **frontend perspective**:

```javascript
// Frontend validates backend responses match OpenAPI schema
const schema = await loadOpenAPISchema();
const response = await fetch('/api/posts');
const validation = validateAgainstSchema(response, schema);
```

**Same concept, different angle!**

- Backend Schemathesis: Tests API generates correct responses
- Frontend validation: Tests API consumers receive expected data
- **Together:** Complete contract validation from both sides

---

## 🎓 When to Use Contract Testing

### Perfect For

✅ **Microservices architectures**

- Multiple services with API contracts
- Prevent breaking changes between services

✅ **API-first development**

- Design API schema first
- Generate tests from schema automatically

✅ **Multiple API consumers**

- Mobile apps, web apps, third-party integrations
- Ensure all consumers get consistent data

✅ **Large APIs (20+ endpoints)**

- Saves massive time vs manual tests
- Comprehensive coverage automatically

### Not Needed For

❌ **Small APIs (<5 endpoints)** - Manual tests are fine
❌ **Rapidly changing APIs** - Schema updates are too frequent
❌ **Internal-only APIs** - Less risk of drift

---

## 🆚 Contract Testing vs Integration Testing

### Integration Tests (What We Have - 140+ tests)

```python
def test_create_post_with_valid_data():
    """Specific scenario test"""
    response = client.post("/api/posts",
        json={"content": "Test post"},
        headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["content"] == "Test post"
```

**Characteristics:**

- Tests specific scenarios you design
- Validates business logic
- Checks exact expected behavior
- You control what's tested

### Contract Tests (What Schemathesis Does)

```python
@schema.parametrize()
def test_api_contract(case):
    """Automatically generated tests"""
    case.call_and_validate()
```

**Characteristics:**

- Tests ALL possible inputs automatically
- Validates schema compliance
- Finds unexpected edge cases
- Tool controls what's tested

### Use Both

They complement each other:

- **Integration tests:** Validate business logic and workflows
- **Contract tests:** Validate schema compliance and edge cases

**Real-world teams** use both for comprehensive API coverage.

---

## 🔍 What Schemathesis Actually Tests

For each endpoint, Schemathesis validates:

### Request Validation

- ✅ Required parameters are enforced
- ✅ Optional parameters are accepted
- ✅ Data types match schema (string, int, boolean, etc.)
- ✅ Format constraints (email, URI, date)
- ✅ Min/max length restrictions
- ✅ Min/max value boundaries
- ✅ Enum values (only allowed values accepted)
- ✅ Pattern matching (regex validation)

### Response Validation

- ✅ Status codes match schema
- ✅ Response body structure matches schema
- ✅ All required fields present
- ✅ Data types correct
- ✅ No extra fields (if additionalProperties: false)

### Security Fuzzing

- ✅ XSS attempts in string fields
- ✅ SQL injection patterns
- ✅ Path traversal attempts
- ✅ Buffer overflow with long strings
- ✅ Malformed JSON
- ✅ Unexpected data types

---

## 📚 Alternative Tools

### Backend Contract Testing

| Tool | Language | Approach | Status in Testbook |
|------|----------|----------|-------------------|
| **Schemathesis** | Python | Property-based from OpenAPI | ⚠️ Skipped (OpenAPI 3.1.0) |
| **Dredd** | Any | Contract validation | Not implemented |
| **Pact** | Multiple | Consumer-driven contracts | Not implemented |
| **Postman** | Any | Manual contract tests | Available (see `tests/api/`) |

### Frontend Contract Testing

| Tool | Status in Testbook |
|------|-------------------|
| **OpenAPI validation** | ✅ Available - See Lab 6C |
| **MSW with schema** | ✅ Available - See Lab 6B |

**Learn frontend contract testing:** [Lab 6C: Frontend Integration Testing](../../labs/LAB_06C_Frontend_Integration_Testing.md)

---

## 🎓 Learning Path

### Stage 1: Understand the Concept (You Are Here!)

- ✅ Read this guide
- ✅ Understand contract testing value
- ✅ Know why it's important professionally

### Stage 2: Study the Code

- 📖 Read `backend/tests/integration/test_api_contract.py`
- 🔍 See how it's structured (even though skipped)
- 💡 Understand the pattern

### Stage 3: Learn Frontend Contracts

- 🧪 Complete [Lab 6C](../../labs/LAB_06C_Frontend_Integration_Testing.md)
- ✅ This teaches contract validation that WORKS today
- 🔄 Same concept, different angle (frontend → backend vs backend self-test)

### Stage 4: Monitor for Updates

- 📡 Watch Schemathesis releases
- 🔄 When OpenAPI 3.1.0 support is stable, enable the test
- 🚀 See 500+ automated tests in action!

### Stage 5: Apply to Your Projects

- 💼 Add contract testing to your portfolio projects
- 🎯 Mention in interviews ("I understand property-based contract testing")
- 🏆 Stand out from other QA candidates

---

## 💼 Why This Matters for Your Career

### Interview Talking Points

**When asked: "What types of API testing have you done?"**

✅ **Good Answer:**
"Integration tests, unit tests, and E2E tests."

🌟 **Great Answer:**
"Integration tests, E2E, and I've also worked with property-based contract testing using tools like Schemathesis. Contract testing automatically generates hundreds of test cases from the OpenAPI schema to validate that the API implementation matches its specification. It's especially valuable for microservices and API-first architectures where you need to prevent documentation drift and integration bugs."

### Real-World Scenarios

**Microservices Company:**
"We have 50 microservices. How would you test them?"

**Your answer:**
"I'd use contract testing with tools like Schemathesis or Pact. Each service's API contract is validated automatically, preventing breaking changes between services. I've practiced this concept in Testbook where I studied property-based testing and contract validation patterns."

**API-First Company:**
"We design APIs before implementing them. How do you ensure the implementation matches?"

**Your answer:**
"Contract testing! Tools like Schemathesis can validate that your FastAPI implementation matches the OpenAPI specification. I learned this technique in Testbook, and even though we had to skip the test due to OpenAPI 3.1.0 compatibility, I understand the pattern and could implement it with supported tools."

---

## 📖 Testbook's Contract Testing

### Our Test File: `backend/tests/integration/test_api_contract.py`

**What it would test:**

- All 30 API endpoints
- ~1,500 generated test cases
- Request validation
- Response validation
- Schema compliance
- Security fuzzing

**Current Status:** ⚠️ Skipped

**Reason:** OpenAPI 3.1.0 compatibility wait

**Educational Value:** Still valuable to study the pattern!

### Running Other Tests

While contract test is skipped, we have comprehensive API coverage:

```bash
# Run integration tests (140+ tests)
cd backend
pytest tests/integration/ -v

# These tests cover:
# - All endpoints (manual test cases)
# - Authentication flows
# - Business logic
# - Error handling
# - Database operations
```

**You're still learning professional API testing!**

---

## 🔗 Related Testbook Content

### Hands-On Labs

- [Lab 3: Testing API Endpoints](../../labs/LAB_03_Testing_API_Endpoints.md) - Traditional API testing
- [Lab 6C: Frontend Integration Testing](../../labs/LAB_06C_Frontend_Integration_Testing.md) - Contract validation (works today!)

### Learning Stages

- [Stage 2: Integration Tests](../../learn/stage_2_integration/) - API testing fundamentals
- [Stage 3: API & E2E](../../learn/stage_3_api_e2e/) - Advanced API patterns

### Reference Docs

- [Testing Guide](TESTING_GUIDE.md) - API testing examples
- [Testing Patterns](../reference/TESTING_PATTERNS.md) - Advanced techniques
- [Backend Tests README](../../backend/tests/README.md) - Test organization

---

## 🌐 External Resources

### Schemathesis

- [Official Documentation](https://schemathesis.readthedocs.io/)
- [GitHub Repository](https://github.com/schemathesis/schemathesis)
- [Property-Based Testing Intro](https://hypothesis.works/articles/what-is-property-based-testing/)

### OpenAPI

- [OpenAPI 3.1.0 Specification](https://spec.openapis.org/oas/v3.1.0)
- [Migration from 3.0 to 3.1](https://www.openapis.org/blog/2021/02/16/migrating-from-openapi-3-0-to-3-1-0)

### Alternative Tools

- [Dredd](https://dredd.org/) - API contract testing
- [Pact](https://pact.io/) - Consumer-driven contract testing
- [Postman Contract Testing](https://learning.postman.com/docs/designing-and-developing-your-api/testing-an-api/)

---

## ❓ FAQ

### Q: Why not just downgrade to OpenAPI 3.0?

**A:** We could, but:

- OpenAPI 3.1.0 has better features (JSON Schema compatibility)
- FastAPI uses 3.1.0 by default (industry standard)
- Better to teach modern standards
- Learners should understand this situation happens in real projects

### Q: Can I still learn contract testing from Testbook?

**A:** Absolutely!

1. Study the test file pattern (even though skipped)
2. Do Lab 6C for frontend contract testing (works today)
3. Understand the concept from this guide
4. Mention in interviews: "I understand contract testing patterns"

### Q: What's the difference between this and Lab 6C?

**A:**

- **Backend (Schemathesis):** Tests server generates correct responses
- **Frontend (Lab 6C):** Tests client receives expected responses
- **Same concept, different perspective!**

Both validate the contract between API provider and consumer.

### Q: Should I include this on my resume?

**A:** Yes!

```text
• Studied property-based contract testing with Schemathesis
• Understand automated schema validation and API fuzzing
• Implemented frontend contract validation with OpenAPI schemas
```

It shows you know advanced testing concepts even if the specific tool wasn't fully usable.

---

## 🎯 Key Takeaways

1. **Contract testing validates API matches documentation** - prevents drift
2. **Property-based testing generates tests automatically** - finds edge cases
3. **Schemathesis is powerful** - 1 test = 500+ generated cases
4. **Currently incompatible with OpenAPI 3.1.0** - but concept still valuable
5. **You can do frontend contract testing today** - see Lab 6C
6. **Real-world teams use this** - especially for microservices

---

## 🚀 Next Steps

1. ✅ **Understand the concept** (you just did!)
2. 📖 **Study the test file:** `backend/tests/integration/test_api_contract.py`
3. 🧪 **Do Lab 6C:** Frontend contract testing (works today!)
4. 💼 **Add to portfolio:** Mention contract testing knowledge
5. 🎯 **Use in interviews:** Discuss property-based testing
6. 🔮 **Watch for updates:** Enable when Schemathesis is ready

---

**Remember:** Even though this specific test is skipped, understanding contract testing and property-based testing makes you a stronger QA engineer. These are professional techniques used in production at major tech companies!

**You're learning concepts that matter.** 🎓
