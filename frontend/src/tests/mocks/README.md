# 🎭 MSW (Mock Service Worker) Mocks

**Network mocking for component tests**

These files provide MSW configuration for testing React components without a running backend.

---

## 📁 Files

- `handlers.js` - API endpoint mock handlers
- `server.js` - MSW server setup for Node.js tests

---

## 🚀 Usage

### Basic Setup

The MSW server is configured in `setup.js` but commented out by default.

To enable MSW for all component tests, uncomment in `setup.js`:

```javascript
import { server } from './mocks/server';

beforeAll(() => server.listen({ onUnhandledRequest: 'warn' }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

### Use in Individual Tests

```javascript
import { render, screen, waitFor } from '@testing-library/react';
import { setupServer } from 'msw/node';
import { handlers } from '../test/mocks/handlers';

const server = setupServer(...handlers);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

test('component fetches data', async () => {
  render(<MyComponent />);

  await waitFor(() => {
    expect(screen.getByText('Mocked post from MSW')).toBeInTheDocument();
  });
});
```

### Override Handlers for Specific Tests

```javascript
import { rest } from 'msw';
import { server } from '../test/mocks/server';

test('handles error state', async () => {
  // Override default handler
  server.use(
    rest.get('http://localhost:8000/api/feed', (req, res, ctx) => {
      return res(ctx.status(500), ctx.json({ detail: 'Error' }));
    })
  );

  render(<MyComponent />);

  await waitFor(() => {
    expect(screen.getByText(/error/i)).toBeInTheDocument();
  });
});
```

---

## 🎓 Learn More

- [Lab 6B: Advanced Component Testing](../../../learn/stage_4_performance_security/exercises/LAB_06B_Advanced_Component_Testing.md) - Complete MSW tutorial
- [MSW Documentation](https://mswjs.io/docs/) - Official MSW docs
- [Testing Comparison Guide](../../../docs/guides/TESTING_COMPARISON_PYTHON_JS.md) - Compare with Python mocking

---

## 💡 Key Benefits

**Why use MSW instead of axios.mock?**

✅ **More realistic** - Intercepts at network level
✅ **Framework agnostic** - Works with any HTTP client
✅ **Reusable** - Same handlers for different tests
✅ **Better debugging** - See actual network requests
✅ **Development use** - Can use in dev mode too
