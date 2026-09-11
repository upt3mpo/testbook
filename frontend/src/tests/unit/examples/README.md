# 🧪 Component Test Examples

**Example tests demonstrating advanced patterns from Lab 6B**

These tests showcase the patterns taught in [Lab 6B: Advanced Component Testing](../../../../../learn/stage_2_integration/exercises/LAB_06_Component_Testing_JavaScript.md).

---

## 📁 Files

Place your example tests here following Lab 6B patterns:

- MSW network mocking examples
- Async data loading tests
- Stateful component tests
- Accessibility testing examples

---

## 🚀 Running Examples

```bash
cd frontend
npm test -- examples
```

---

## 📚 What to Test

### Component Testing Patterns

1. **Rendering** - Does component render correctly?
2. **User Interactions** - Clicks, typing, keyboard navigation
3. **State Management** - State updates, side effects
4. **API Integration** - Loading, success, error states
5. **Accessibility** - axe violations, ARIA, keyboard support

### Example Test Structure

```javascript
import { render, screen, waitFor } from '@testing-library/react';
import { setupServer } from 'msw/node';
import { handlers } from '../../mocks/handlers';

const server = setupServer(...handlers);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('MyComponent', () => {
  it('loads data from API', async () => {
    render(<MyComponent />);

    // Loading state
    expect(screen.getByText(/loading/i)).toBeInTheDocument();

    // Data loaded
    await waitFor(() => {
      expect(screen.getByText('Mocked post from MSW')).toBeInTheDocument();
    });
  });
});
```

---

## 🎓 Learn More

- [Lab 6B: Advanced Component Testing](../../../../../learn/stage_2_integration/exercises/LAB_06_Component_Testing_JavaScript.md)
- [Vitest Documentation](https://vitest.dev/)
- [Testing Library](https://testing-library.com/)
- [MSW Documentation](https://mswjs.io/)
