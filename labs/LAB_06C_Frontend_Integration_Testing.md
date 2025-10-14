# 🧪 Lab 6C: Frontend Integration & Contract Testing

**Estimated Time:** 90 minutes
**Difficulty:** Advanced
**Language:** 🟨 JavaScript
**Prerequisites:** Lab 6B (Advanced Component Testing), understanding of REST APIs, comfortable with JavaScript

**💡 JavaScript refresher needed?** Visit [learn-js.org](https://www.learn-js.org/) for interactive JavaScript practice

**What This Adds:** Bridge frontend testing with backend contract validation. Learn to test that your frontend components correctly integrate with the FastAPI backend schema using contract testing principles.

---

## 🎯 What You'll Learn

- **Contract testing** - Ensure frontend matches backend API contract
- **OpenAPI schema validation** - Validate against FastAPI's auto-generated schema
- **Integration testing** - Test frontend + backend together
- **MSW with real schemas** - Mock API responses that match actual backend
- **Type safety** - Generate TypeScript types from OpenAPI schema
- **API client testing** - Test your API wrapper functions

---

## 📋 Background: Why Contract Testing?

**The Problem:**

```javascript
// Frontend expects this:
const user = await api.getUser(1);
console.log(user.displayName);  // Error! Backend returns display_name

// Backend actually returns:
{
  "id": 1,
  "username": "sarah",
  "display_name": "Sarah Johnson",  // Snake case, not camelCase!
  "email": "sarah@testbook.com"
}
```

**The Solution: Contract Testing**

Contract testing ensures the frontend and backend agree on:
- Response structure
- Field names and types
- Status codes
- Error formats

**📚 Related:** This lab teaches **frontend contract testing** (validating backend responses). There's also **backend contract testing** with Schemathesis that validates the API itself. Learn more: [Contract Testing Guide](../docs/guides/CONTRACT_TESTING.md)

---

## Part 1: Setup OpenAPI Schema Validation (20 minutes)

### Step 1: Fetch Backend OpenAPI Schema

FastAPI auto-generates an OpenAPI schema at `/docs` and `/openapi.json`.

Create `frontend/scripts/fetch-schema.js`:

```javascript
#!/usr/bin/env node
const fs = require('fs');
const https = require('https');
const http = require('http');

const API_URL = process.env.API_URL || 'http://localhost:8000';
const OUTPUT_FILE = 'src/tests/openapi-schema.json';

console.log(`📥 Fetching OpenAPI schema from ${API_URL}/openapi.json...`);

const client = API_URL.startsWith('https') ? https : http;

client.get(`${API_URL}/openapi.json`, (res) => {
  let data = '';

  res.on('data', (chunk) => {
    data += chunk;
  });

  res.on('end', () => {
    try {
      const schema = JSON.parse(data);
      fs.writeFileSync(OUTPUT_FILE, JSON.stringify(schema, null, 2));
      console.log(`✅ Schema saved to ${OUTPUT_FILE}`);
      console.log(`📊 Found ${Object.keys(schema.paths || {}).length} API endpoints`);
    } catch (error) {
      console.error('❌ Failed to parse schema:', error.message);
      process.exit(1);
    }
  });
}).on('error', (error) => {
  console.error('❌ Failed to fetch schema:', error.message);
  console.error('💡 Make sure backend is running on', API_URL);
  process.exit(1);
});
```

Make it executable and run:

```bash
cd frontend
chmod +x scripts/fetch-schema.js
node scripts/fetch-schema.js
```

**✅ Checkpoint:** File `src/tests/openapi-schema.json` created with your API schema

### Step 2: Install Contract Testing Tools

```bash
npm install --save-dev openapi-validator-middleware jest-openapi
```

---

## Part 2: Validate API Client Against Schema (25 minutes)

### Step 1: Create Contract Test Helper

Create `frontend/src/tests/contract-helpers.js`:

```javascript
import jestOpenAPI from 'jest-openapi';
import schema from './openapi-schema.json';

// Load the OpenAPI schema
jestOpenAPI(schema);

/**
 * Validate that a response matches the OpenAPI schema
 * @param {object} response - Axios response object
 * @param {string} path - API path (e.g., '/api/users')
 * @param {string} method - HTTP method (e.g., 'get')
 * @param {number} status - Expected status code
 */
export function validateContract(response, path, method, status = 200) {
  expect(response.status).toBe(status);

  // Validate response matches schema
  expect(response).toSatisfyApiSpec();

  // Validate specific operation
  const operation = schema.paths[path]?.[method.toLowerCase()];
  if (!operation) {
    throw new Error(`No schema found for ${method.toUpperCase()} ${path}`);
  }

  return operation;
}

/**
 * Get expected response schema for an endpoint
 */
export function getResponseSchema(path, method, status = 200) {
  const operation = schema.paths[path]?.[method.toLowerCase()];
  const response = operation?.responses?.[status.toString()];
  return response?.content?.['application/json']?.schema;
}

/**
 * Validate object shape matches schema
 */
export function matchesSchema(data, schemaRef) {
  // Basic validation - in production, use a proper JSON Schema validator
  if (!schemaRef) return true;

  // Check required fields
  const schema = resolveSchemaRef(schemaRef);
  if (schema.required) {
    for (const field of schema.required) {
      if (!(field in data)) {
        throw new Error(`Missing required field: ${field}`);
      }
    }
  }

  return true;
}

function resolveSchemaRef(schemaRef) {
  if (schemaRef.$ref) {
    // Simple ref resolution - extend for full JSON Schema support
    const refPath = schemaRef.$ref.split('/').slice(2);
    let resolved = schema;
    for (const key of refPath) {
      resolved = resolved[key];
    }
    return resolved;
  }
  return schemaRef;
}
```

### Step 2: Test API Client

Create `frontend/src/tests/integration/api-client.test.js`:

```javascript
import { describe, it, expect, beforeAll } from 'vitest';
import axios from 'axios';
import { validateContract } from './contract-helpers';

const API_BASE = 'http://localhost:8000';

describe('API Client Contract Tests', () => {
  let authToken;

  beforeAll(async () => {
    // Login to get token
    const response = await axios.post(`${API_BASE}/api/auth/login`, {
      email: 'sarah.johnson@testbook.com',
      password: 'Sarah2024!',
    });
    authToken = response.data.access_token;
  });

  describe('GET /api/feed', () => {
    it('returns feed posts matching schema', async () => {
      const response = await axios.get(`${API_BASE}/api/feed`, {
        headers: { Authorization: `Bearer ${authToken}` },
      });

      // Validate against OpenAPI schema
      validateContract(response, '/api/feed', 'get', 200);

      // Validate response structure
      expect(Array.isArray(response.data)).toBe(true);

      if (response.data.length > 0) {
        const post = response.data[0];

        // Required fields per schema
        expect(post).toHaveProperty('id');
        expect(post).toHaveProperty('content');
        expect(post).toHaveProperty('author');
        expect(post).toHaveProperty('created_at');
        expect(post).toHaveProperty('reaction_counts');

        // Author object structure
        expect(post.author).toHaveProperty('id');
        expect(post.author).toHaveProperty('username');
        expect(post.author).toHaveProperty('display_name');
      }
    });
  });

  describe('POST /api/posts/', () => {
    it('creates post with schema-compliant request/response', async () => {
      const newPost = {
        content: 'Contract testing is awesome!',
      };

      const response = await axios.post(
        `${API_BASE}/api/posts/`,
        newPost,
        {
          headers: { Authorization: `Bearer ${authToken}` },
        }
      );

      // Validate response matches schema
      validateContract(response, '/api/posts/', 'post', 200);

      // Verify response structure
      expect(response.data).toHaveProperty('id');
      expect(response.data).toHaveProperty('content');
      expect(response.data.content).toBe(newPost.content);
    });
  });

  describe('GET /api/users/{username}', () => {
    it('returns user profile matching schema', async () => {
      const response = await axios.get(
        `${API_BASE}/api/users/sarahjohnson`,
        {
          headers: { Authorization: `Bearer ${authToken}` },
        }
      );

      validateContract(response, '/api/users/{username}', 'get', 200);

      const user = response.data;

      // Schema-defined fields
      expect(user).toHaveProperty('id');
      expect(user).toHaveProperty('username');
      expect(user).toHaveProperty('display_name');
      expect(user).toHaveProperty('bio');
      expect(user).toHaveProperty('follower_count');
      expect(user).toHaveProperty('following_count');
    });
  });
});
```

---

## Part 3: Integration Tests with MSW Contract Validation (30 minutes)

### Step 1: Create MSW Handlers from Schema

Create `frontend/src/tests/mocks/schema-based-handlers.js`:

```javascript
import { rest } from 'msw';
import schema from '../openapi-schema.json';

const API_BASE = 'http://localhost:8000';

/**
 * Generate MSW handlers that match OpenAPI schema
 */
export const schemaBasedHandlers = [
  // GET /api/feed - Returns array of posts
  rest.get(`${API_BASE}/api/feed`, (req, res, ctx) => {
    // Response matches schema structure
    return res(
      ctx.status(200),
      ctx.json([
        {
          id: 1,
          content: 'Schema-compliant post',
          author: {
            id: 1,
            username: 'testuser',
            display_name: 'Test User',
          },
          created_at: new Date().toISOString(),
          reaction_counts: { '👍': 5 },
          is_own_post: false,
        },
      ])
    );
  }),

  // POST /api/posts/ - Create post
  rest.post(`${API_BASE}/api/posts/`, async (req, res, ctx) => {
    const body = await req.json();

    // Validate request matches schema
    if (!body.content || typeof body.content !== 'string') {
      return res(
        ctx.status(422),
        ctx.json({ detail: 'Invalid request body' })
      );
    }

    // Return schema-compliant response
    return res(
      ctx.status(200),
      ctx.json({
        id: Date.now(),
        content: body.content,
        author: {
          id: 1,
          username: 'testuser',
          display_name: 'Test User',
        },
        created_at: new Date().toISOString(),
        reaction_counts: {},
        is_own_post: true,
      })
    );
  }),

  // GET /api/auth/me - Current user
  rest.get(`${API_BASE}/api/auth/me`, (req, res, ctx) => {
    const authHeader = req.headers.get('Authorization');

    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res(
        ctx.status(401),
        ctx.json({ detail: 'Not authenticated' })
      );
    }

    return res(
      ctx.status(200),
      ctx.json({
        id: 1,
        email: 'test@testbook.com',
        username: 'testuser',
        display_name: 'Test User',
        bio: 'Test user bio',
      })
    );
  }),
];
```

### Step 2: Test Components with Contract-Validated Mocks

Create `frontend/src/components/__tests__/FeedWithContracts.test.jsx`:

```javascript
import { render, screen, waitFor } from '@testing-library/react';
import { describe, it, expect, beforeAll, afterEach, afterAll } from 'vitest';
import { setupServer } from 'msw/node';
import { schemaBasedHandlers } from '../../test/mocks/schema-based-handlers';
import { BrowserRouter } from 'react-router-dom';
import { AuthContext } from '../../AuthContext';

// Setup MSW server with schema-based handlers
const server = setupServer(...schemaBasedHandlers);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

// Mock Feed component (simplified for testing)
function Feed() {
  const [posts, setPosts] = React.useState([]);
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    fetch('http://localhost:8000/api/feed')
      .then(res => res.json())
      .then(data => {
        setPosts(data);
        setLoading(false);
      });
  }, []);

  if (loading) return <div data-testid="loading">Loading...</div>;

  return (
    <div data-testid="feed">
      {posts.map(post => (
        <article key={post.id} data-testid={`post-${post.id}`}>
          <p>{post.content}</p>
          <span>{post.author.display_name}</span>
        </article>
      ))}
    </div>
  );
}

describe('Feed Integration with Contract Validation', () => {
  const renderFeed = () => {
    const mockAuth = {
      user: { id: 1, username: 'testuser', display_name: 'Test User' },
      login: vi.fn(),
      logout: vi.fn(),
    };

    return render(
      <BrowserRouter>
        <AuthContext.Provider value={mockAuth}>
          <Feed />
        </AuthContext.Provider>
      </BrowserRouter>
    );
  };

  it('displays posts with schema-compliant data', async () => {
    renderFeed();

    // Wait for loading to complete
    await waitFor(() => {
      expect(screen.queryByTestId('loading')).not.toBeInTheDocument();
    });

    // Verify feed loaded
    expect(screen.getByTestId('feed')).toBeInTheDocument();

    // Verify post data matches schema structure
    const post = screen.getByTestId('post-1');
    expect(post).toHaveTextContent('Schema-compliant post');
    expect(post).toHaveTextContent('Test User');
  });

  it('handles schema-compliant error responses', async () => {
    // Override handler to return error
    const { rest } = await import('msw');

    server.use(
      rest.get('http://localhost:8000/api/feed', (req, res, ctx) => {
        // FastAPI error format
        return res(
          ctx.status(500),
          ctx.json({ detail: 'Internal server error' })
        );
      })
    );

    renderFeed();

    // Component should handle error gracefully
    await waitFor(() => {
      expect(screen.queryByTestId('loading')).not.toBeInTheDocument();
    });
  });
});
```

---

## Part 4: Test API Wrapper Functions (20 minutes)

Create comprehensive tests for your API client.

Create `frontend/src/__tests__/api.contract.test.js`:

```javascript
import { describe, it, expect, beforeAll, afterEach, afterAll } from 'vitest';
import { setupServer } from 'msw/node';
import { schemaBasedHandlers } from '../test/mocks/schema-based-handlers';
import { postsAPI, authAPI, usersAPI } from '../api';

const server = setupServer(...schemaBasedHandlers);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('Posts API Contract Tests', () => {
  it('create() sends correct request and handles response', async () => {
    const postData = {
      content: 'Test post from contract test',
    };

    const result = await postsAPI.create(postData);

    // Verify response structure matches schema
    expect(result.data).toHaveProperty('id');
    expect(result.data).toHaveProperty('content');
    expect(result.data.content).toBe(postData.content);
    expect(result.data).toHaveProperty('author');
    expect(result.data.author).toHaveProperty('id');
    expect(result.data.author).toHaveProperty('username');
    expect(result.data.author).toHaveProperty('display_name');
  });

  it('list() returns schema-compliant feed', async () => {
    const result = await postsAPI.list();

    expect(Array.isArray(result.data)).toBe(true);

    if (result.data.length > 0) {
      const post = result.data[0];

      // Verify all required fields per schema
      expect(post).toHaveProperty('id');
      expect(post).toHaveProperty('content');
      expect(post).toHaveProperty('author');
      expect(post).toHaveProperty('created_at');
      expect(post).toHaveProperty('reaction_counts');

      // Verify types
      expect(typeof post.id).toBe('number');
      expect(typeof post.content).toBe('string');
      expect(typeof post.author).toBe('object');
      expect(typeof post.reaction_counts).toBe('object');
    }
  });
});

describe('Auth API Contract Tests', () => {
  it('getCurrentUser() returns schema-compliant user', async () => {
    const result = await authAPI.getCurrentUser();

    // Verify user object matches schema
    expect(result.data).toHaveProperty('id');
    expect(result.data).toHaveProperty('email');
    expect(result.data).toHaveProperty('username');
    expect(result.data).toHaveProperty('display_name');
    expect(result.data).toHaveProperty('bio');

    // Verify types
    expect(typeof result.data.id).toBe('number');
    expect(typeof result.data.email).toBe('string');
    expect(typeof result.data.username).toBe('string');
    expect(typeof result.data.display_name).toBe('string');
  });
});

describe('Users API Contract Tests', () => {
  it('getProfile() returns complete user profile', async () => {
    const result = await usersAPI.getProfile('testuser');

    // Verify profile matches schema
    expect(result.data).toHaveProperty('id');
    expect(result.data).toHaveProperty('username');
    expect(result.data).toHaveProperty('display_name');
    expect(result.data).toHaveProperty('bio');
    expect(result.data).toHaveProperty('follower_count');
    expect(result.data).toHaveProperty('following_count');

    // Verify types match schema
    expect(typeof result.data.follower_count).toBe('number');
    expect(typeof result.data.following_count).toBe('number');
  });
});
```

**Run the tests:**

```bash
npm test -- api.contract.test.js
```

---

## Part 5: Integration Test with Real Backend (15 minutes)

Test against the actual running backend to validate real contracts.

Create `frontend/src/test/integration/backend-integration.test.js`:

```javascript
import { describe, it, expect, beforeAll } from 'vitest';
import axios from 'axios';

const API_BASE = 'http://localhost:8000';

/**
 * These tests run against the REAL backend
 * Make sure backend is running: ./start-dev.sh
 */
describe('Backend Integration Tests', () => {
  let authToken;

  beforeAll(async () => {
    // Real login
    const response = await axios.post(`${API_BASE}/api/auth/login`, {
      email: 'sarah.johnson@testbook.com',
      password: 'Sarah2024!',
    });
    authToken = response.data.access_token;
  });

  it('GET /api/feed returns real data matching expected structure', async () => {
    const response = await axios.get(`${API_BASE}/api/feed`, {
      headers: { Authorization: `Bearer ${authToken}` },
    });

    expect(response.status).toBe(200);
    expect(Array.isArray(response.data)).toBe(true);

    // Validate structure matches what frontend expects
    if (response.data.length > 0) {
      const post = response.data[0];

      // These fields MUST exist for frontend to work
      expect(post).toHaveProperty('id');
      expect(post).toHaveProperty('content');
      expect(post).toHaveProperty('author');
      expect(post.author).toHaveProperty('username');
      expect(post.author).toHaveProperty('display_name');
    }
  });

  it('POST /api/posts/ creates post and returns correct structure', async () => {
    const postData = {
      content: 'Integration test post',
    };

    const response = await axios.post(
      `${API_BASE}/api/posts/`,
      postData,
      {
        headers: { Authorization: `Bearer ${authToken}` },
      }
    );

    expect(response.status).toBe(200);

    // Verify backend returns what frontend needs
    expect(response.data).toHaveProperty('id');
    expect(response.data.content).toBe(postData.content);
    expect(response.data).toHaveProperty('author');
    expect(response.data).toHaveProperty('created_at');
    expect(response.data).toHaveProperty('reaction_counts');
  });

  it('handles authentication errors with correct format', async () => {
    try {
      await axios.get(`${API_BASE}/api/auth/me`);
      // Should not reach here
      expect.fail('Should have thrown error');
    } catch (error) {
      expect(error.response.status).toBe(401);

      // FastAPI error format
      expect(error.response.data).toHaveProperty('detail');
    }
  });
});
```

**Run integration tests:**

```bash
# Make sure backend is running first!
# Then run:
npm test -- backend-integration.test.js
```

---

## Part 6: Practical Contract Testing Patterns (10 minutes)

### Pattern 1: Shared Type Definitions

Instead of duplicating types, generate TypeScript types from OpenAPI schema:

```bash
npm install --save-dev openapi-typescript
npx openapi-typescript src/test/openapi-schema.json -o src/types/api.d.ts
```

**Use in code:**

```typescript
import type { components } from './types/api';

type Post = components['schemas']['Post'];
type User = components['schemas']['User'];

// Now TypeScript ensures you use correct field names!
function displayPost(post: Post) {
  console.log(post.display_name);  // ❌ Error! Field doesn't exist
  console.log(post.author.display_name);  // ✅ Correct!
}
```

### Pattern 2: Schema Version Tracking

**Add to package.json:**

```json
{
  "scripts": {
    "test:contracts": "node scripts/fetch-schema.js && npm test -- contract",
    "validate:schema": "node scripts/fetch-schema.js && node scripts/validate-schema.js"
  }
}
```

### Pattern 3: Contract Test in CI

**Add to your CI workflow:**

```yaml
- name: Contract Tests
  run: |
    # Start backend
    cd backend && uvicorn main:app &
    sleep 5

    # Fetch latest schema
    cd ../frontend
    node scripts/fetch-schema.js

    # Run contract tests
    npm test -- contract
```

---

## 🎓 What You Learned

- ✅ **Contract testing** - Ensure frontend/backend agreement
- ✅ **OpenAPI validation** - Use FastAPI's auto-generated schema
- ✅ **Schema-based mocking** - MSW handlers that match real API
- ✅ **Integration testing** - Test against real backend
- ✅ **Type safety** - Generate types from schema
- ✅ **Professional patterns** - Used in production applications

---

## 💪 Practice Challenges

### Challenge 1: Add More Endpoints

Test contracts for:
- PUT /api/users/me (update profile)
- POST /api/posts/{id}/reactions
- DELETE /api/posts/{id}

### Challenge 2: Error Contract Testing

Test that error responses match FastAPI's error format:
- 400 (Validation error)
- 401 (Unauthorized)
- 403 (Forbidden)
- 404 (Not found)
- 422 (Unprocessable entity)

### Challenge 3: Schema Drift Detection

Create a test that compares the fetched schema with a baseline to detect API changes:

```javascript
it('API schema has not changed unexpectedly', () => {
  const currentSchema = require('../test/openapi-schema.json');
  const baselineSchema = require('../test/baseline-schema.json');

  // Compare endpoint counts
  expect(Object.keys(currentSchema.paths).length)
    .toBe(Object.keys(baselineSchema.paths).length);
});
```

### Challenge 4: Generate Test Cases from Schema

Write a script that reads the OpenAPI schema and generates basic contract tests automatically.

---

## 🎯 Pro Tips

**Tip 1: Keep Schema Updated**

```bash
# Run before tests
npm run test:contracts
```

**Tip 2: Use Schema in Development**

Mock your API during development with schema-compliant responses:

```javascript
// Development API client
if (import.meta.env.DEV && import.meta.env.VITE_MOCK_API) {
  // Use MSW with schema-based handlers
}
```

**Tip 3: Version Your Schema**

```bash
cp src/test/openapi-schema.json src/test/schemas/v1.0.0.json
```

**Tip 4: Combine with E2E Tests**

Contract tests ensure structure; E2E tests ensure behavior:

```javascript
// Contract test (fast)
it('response has correct structure', () => {
  expect(response.data).toMatchSchema();
});

// E2E test (realistic)
test('user can create post', async ({ page }) => {
  // Tests actual UI flow
});
```

---

## ✅ Lab Completion Checklist

- [ ] Fetched OpenAPI schema from backend
- [ ] Created schema-based MSW handlers
- [ ] Tested API client against contracts
- [ ] Created integration tests with real backend
- [ ] Understand contract testing principles
- [ ] Know when to use contract vs E2E tests

---

## 🆚 Contract Testing vs E2E Testing

| Aspect | Contract Testing | E2E Testing |
|--------|-----------------|-------------|
| **Speed** | Fast (< 1s) | Slower (5-30s) |
| **Scope** | API structure | Complete user flow |
| **Catches** | Schema mismatches | UI bugs, workflow issues |
| **Setup** | Schema + mocks | Full app running |
| **Best For** | API integration | User journeys |
| **When to Run** | Every commit | Before deploy |

**💡 Use Both:** Contract tests catch API breaking changes fast. E2E tests verify complete workflows work.

---

## 📚 Resources

**Working Helper Files (Ready to Use!):**
- **`frontend/scripts/fetch-schema.js`** - ⭐ Fetch OpenAPI schema from backend
  - Run: `node frontend/scripts/fetch-schema.js`
  - Creates: `src/test/openapi-schema.json`
- **`frontend/src/test/contract-helpers.js`** - Contract validation helpers
  - `validateContract()` - Validate responses
  - `hasRequiredFields()` - Check required fields
  - `TestbookSchemas` - Pre-defined schemas for common types
- **`frontend/src/test/openapi-schema.example.json`** - Example schema structure
- **`frontend/src/test/mocks/`** - MSW handlers from Lab 6B

**Prerequisites:**
- [Lab 6B: Advanced Component Testing](LAB_06B_Advanced_Component_Testing.md) - MSW basics
- [Testing Comparison Guide](../docs/guides/TESTING_COMPARISON_PYTHON_JS.md) - Backend testing context

**Next Steps:**
- [Section 8: Advanced E2E Patterns](../docs/course/SECTION_08_ADVANCED_E2E_PATTERNS.md) - Complete E2E patterns
- [CI/CD Guide](../docs/course/CI_CD_E2E_TESTING.md) - Automate contract tests

**External Documentation:**
- [OpenAPI Specification](https://swagger.io/specification/)
- [FastAPI OpenAPI](https://fastapi.tiangolo.com/tutorial/metadata/)
- [Contract Testing Guide](https://pactflow.io/blog/what-is-contract-testing/)

---

**🎉 You've mastered frontend integration testing with contract validation! This prevents countless API integration bugs!**

