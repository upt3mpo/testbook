# Frontend Tests

**Organized test structure for Testbook's React frontend**

---

## 📁 Directory Structure

```text
frontend/src/tests/
├── unit/                      # Component unit tests
│   ├── CreatePost.test.jsx    # Post creation component
│   ├── Navbar.test.jsx        # Navigation component
│   └── examples/              # Example test patterns
│
├── integration/               # API contract tests
│   └── contract.test.js       # OpenAPI schema validation
│
├── accessibility/             # Accessibility tests
│   └── accessibility.test.jsx # WCAG compliance checks
│
├── mocks/                     # Mock Service Worker (MSW)
│   ├── handlers.js           # API mock handlers
│   ├── server.js             # MSW server setup
│   ├── examples.js           # Example mock patterns
│   └── README.md             # MSW documentation
│
├── setup.js                   # Vitest configuration
├── contract-helpers.js        # Contract validation utilities
├── openapi-schema.json        # Backend API schema
└── openapi-schema.example.json # Example schema structure
```

---

## 🧪 Test Categories

### Unit Tests (`unit/`)

**Component-level tests** using Vitest and React Testing Library.

**What they test:**

- Component rendering
- User interactions (clicks, typing)
- State management
- Props handling
- Conditional rendering

**Tools:** Vitest, React Testing Library, MSW

**Run:**

```bash
npm test -- tests/unit/
```

---

### Integration Tests (`integration/`)

**API contract tests** ensuring frontend/backend agreement.

**What they test:**

- API response structure validation
- OpenAPI schema compliance
- Request/response data types
- Required fields presence

**Tools:** Vitest, OpenAPI validators

**Run:**

```bash
npm test -- tests/integration/
```

---

### Accessibility Tests (`accessibility/`)

**WCAG compliance checks** using axe-core.

**What they test:**

- Keyboard navigation
- ARIA labels and roles
- Form accessibility
- Semantic HTML
- Color contrast (where possible)

**Tools:** vitest-axe, axe-core

**Run:**

```bash
npm test -- tests/accessibility/
```

---

## 🎭 Mock Service Worker (MSW)

MSW intercepts network requests at the network level, providing realistic API mocking for component tests.

**Benefits:**

- ✅ More realistic than axios mocks
- ✅ Works with any HTTP client
- ✅ Reusable across tests
- ✅ Can be used in development mode

**Learn more:**

- [Lab 6B: Advanced Component Testing](../../../learn/stage_2_integration/exercises/LAB_06_Component_Testing_JavaScript.md)
- [MSW README](mocks/README.md)

---

## 🚀 Running Tests

### Run All Tests

```bash
npm test
```

### Run Specific Test Types

```bash
# Unit tests only
npm test -- tests/unit/

# Contract tests only
npm test -- tests/integration/

# Accessibility tests only
npm test -- tests/accessibility/

# Specific test file
npm test -- tests/unit/CreatePost.test.jsx
```

### Watch Mode

```bash
npm test -- --watch
```

### Coverage Report

```bash
npm test -- --coverage
```

---

## 📚 Learning Resources

### For Unit Testing (Stage 1)

- [Stage 1: Unit Tests](../../../learn/stage_1_unit/)
- Study: `tests/unit/CreatePost.test.jsx`, `tests/unit/Navbar.test.jsx`

### For Integration Testing (Stage 2)

- [Stage 2: Integration Tests](../../../learn/stage_2_integration/)
- Study: `tests/integration/contract.test.js`
- Study: `tests/mocks/handlers.js` for MSW patterns

### For Component Testing Labs

- [Lab 6B: Advanced Component Testing](../../../learn/stage_2_integration/exercises/LAB_06_Component_Testing_JavaScript.md)
- [Lab 6C: Frontend Integration Testing](../../../learn/stage_2_integration/exercises/LAB_08_Contract_Testing_Foundations_JavaScript.md)

---

## 🔧 Configuration

**Vitest Config:** `frontend/vitest.config.js`

**Setup File:** `tests/setup.js` (loaded before all tests)

**Coverage Excludes:**

- `node_modules/`
- `src/tests/` (test files themselves)
- `**/*.config.js`
- `**/main.jsx`

---

## ✅ Test Structure (AAA Pattern)

Our tests follow the **[Arrange-Act-Assert pattern](../../../docs/concepts/TESTING_PATTERNS.md#arrange-act-assert-pattern)**:

```jsx
it('should enable submit button when form is valid', () => {
  // Arrange - Set up test data and render component
  render(<CreatePost onPostCreated={mockCallback} />);

  // Act - Perform user actions
  fireEvent.change(screen.getByRole('textbox'), {
    target: { value: 'Test post content' },
  });

  // Assert - Verify expected outcomes
  expect(screen.getByRole('button', { name: /submit/i })).not.toBeDisabled();
});
```

---

## 💡 Key Testing Principles

1. **Test Behavior, Not Implementation**
   - Test what users see and do
   - Avoid testing internal state directly

2. **Use Semantic Queries**
   - Prefer `getByRole`, `getByLabelText` over `getByTestId`
   - Makes tests more robust and accessible

3. **Mock External Dependencies**
   - Use MSW for API calls
   - Mock browser APIs (localStorage, etc.)

4. **Test Error States**
   - Don't just test happy paths
   - Verify error messages and handling

---

## 🆚 Comparison with Backend Tests

| Aspect              | Frontend (JavaScript)               | Backend (Python)                    |
| ------------------- | ----------------------------------- | ----------------------------------- |
| **Framework**       | Vitest                              | pytest                              |
| **Structure**       | `tests/unit/`, `tests/integration/` | `tests/unit/`, `tests/integration/` |
| **Mocking**         | MSW (network level)                 | pytest fixtures                     |
| **Component Tests** | React Testing Library               | N/A                                 |
| **Contract Tests**  | OpenAPI validation                  | Schema validation                   |

**Both use the same test organization philosophy!**

---

## 📊 Coverage Goals

- **Unit Tests:** 80%+ coverage of components
- **Integration Tests:** All critical API contracts validated
- **Accessibility Tests:** Key user paths WCAG compliant

---

_For more details, see [Testing Guide](../../../docs/guides/TESTING_GUIDE.md)_
