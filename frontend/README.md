# Testbook Frontend

React frontend for the Testbook testing platform.

## Tech Stack

- **React 18** - UI framework
- **React Router v6** - Client-side routing
- **Vite** - Build tool and dev server
- **Axios** - HTTP client
- **Vitest** - Unit testing framework
- **React Testing Library** - Component testing

## Getting Started

### Development

```bash
# Install dependencies
npm install

# Start dev server (port 3000)
npm run dev
```

The frontend will be available at `http://localhost:3000`

### Building

```bash
# Production build
npm run build

# Preview production build
npm run preview
```

## Testing

### Run Tests

```bash
# Run all tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests with coverage
npm run test:coverage

# Run tests with UI
npm run test:ui
```

### Test Structure

```
src/
├── components/
│   ├── __tests__/          # Component tests
│   │   ├── Navbar.test.jsx
│   │   └── CreatePost.test.jsx
│   └── ...
└── test/
    └── setup.js            # Test configuration
```

### Writing Tests

Example component test:

```javascript
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import MyComponent from '../MyComponent';

describe('MyComponent', () => {
  it('renders correctly', () => {
    render(<MyComponent />);
    expect(screen.getByText('Hello')).toBeInTheDocument();
  });
});
```

### Testing Best Practices

1. **Test user behavior, not implementation**
   - Use `screen.getByRole()` instead of `getByTestId()`
   - Test what users see and do

2. **Mock external dependencies**
   - API calls
   - Browser APIs
   - Context providers

3. **Keep tests simple and focused**
   - One assertion per test when possible
   - Clear test names

4. **Use Testing Library queries properly**
   - Prefer `getByRole` > `getByLabelText` > `getByText` > `getByTestId`

## Component Testing vs E2E Testing

### Component Tests (Vitest + React Testing Library)
- **What:** Test individual React components in isolation
- **When:** Testing component logic, rendering, and user interactions
- **Speed:** Fast (milliseconds)
- **Examples:** Button clicks, form inputs, conditional rendering

### E2E Tests (Playwright)
- **What:** Test complete user flows through the app
- **When:** Testing full features with backend integration
- **Speed:** Slower (seconds)
- **Examples:** Login flow, creating posts, user interactions

**Both are important!** Component tests catch bugs early, E2E tests ensure everything works together.

## Project Structure

```
frontend/
├── public/           # Static assets
├── src/
│   ├── components/   # Reusable React components
│   ├── pages/        # Page components (routes)
│   ├── test/         # Test configuration
│   ├── api.js        # API client
│   ├── App.jsx       # Main app component
│   ├── AuthContext.jsx  # Authentication context
│   └── main.jsx      # Entry point
├── package.json
├── vite.config.js    # Vite configuration
└── vitest.config.js  # Test configuration
```

## Available Components

- **Navbar** - Navigation bar with auth state
- **CreatePost** - Post creation form
- **Post** - Individual post display with reactions/comments
- **Comment** - Comment display component

## Testing Coverage Goals

- **Components:** 70%+ coverage
- **Critical paths:** 90%+ coverage (Auth, Post creation)
- **UI interactions:** All major flows tested

## Learn More

- [Vite Documentation](https://vitejs.dev/)
- [React Testing Library](https://testing-library.com/react)
- [Vitest Documentation](https://vitest.dev/)
- [React Router](https://reactrouter.com/)

## Contributing

When adding new components:
1. Write the component
2. Write tests in `__tests__/` folder
3. Ensure tests pass: `npm test`
4. Check coverage: `npm run test:coverage`

---

*Part of the Testbook Testing Platform - Learn automation testing with a real application!*

