# 🧪 Lab 6B: Advanced Component Testing with Vitest

**Estimated Time:** 120 minutes
**Difficulty:** Advanced
**Language:** 🟨 JavaScript/React
**Prerequisites:** Basic understanding of React and Vitest, comfortable with async/await

**💡 Need JavaScript fundamentals?** Review async/await at [learn-js.org](https://www.learn-js.org/) (see "Async and Await" section)

**What This Adds:** Advanced component testing patterns including async data loading, network mocking with MSW, stateful components, and accessibility testing.

---

## 🎯 What You'll Learn

- **MSW (Mock Service Worker)** - Network mocking for components
- **Async data loading** - Test loading states and data fetching
- **Stateful components** - Test complex state management
- **Context & hooks** - Test components with context
- **Accessibility testing** - Automated a11y checks with axe
- **Visual regression basics** - Introduction to visual testing

---

## 📋 Step-by-Step Instructions

### Part 1: Setup MSW for Network Mocking (20 minutes)

Mock Service Worker intercepts network requests at the service worker level, making mocks more realistic.

#### Step 1: Install MSW

```bash
cd frontend
npm install --save-dev msw
```

#### Step 2: Create MSW Handlers

Create `frontend/src/test/mocks/handlers.js`:

```javascript
import { rest } from 'msw';

const API_BASE = 'http://localhost:8000/api';

export const handlers = [
  // Mock posts endpoint
  rest.get(`${API_BASE}/feed`, (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json([
        {
          id: 1,
          content: 'Mocked post from MSW',
          author: { id: 1, username: 'testuser', display_name: 'Test User' },
          created_at: new Date().toISOString(),
          reaction_counts: { '👍': 5, '❤️': 2 },
        },
        {
          id: 2,
          content: 'Another mocked post',
          author: { id: 2, username: 'anotheruser', display_name: 'Another User' },
          created_at: new Date().toISOString(),
          reaction_counts: {},
        },
      ])
    );
  }),

  // Mock post creation
  rest.post(`${API_BASE}/posts/`, (req, res, ctx) => {
    const { content } = req.body;

    return res(
      ctx.status(200),
      ctx.json({
        id: Date.now(),
        content,
        author: { id: 1, username: 'testuser', display_name: 'Test User' },
        created_at: new Date().toISOString(),
        reaction_counts: {},
      })
    );
  }),

  // Mock notifications
  rest.get(`${API_BASE}/notifications`, (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json([
        { id: 1, message: 'New follower', type: 'follow', read: false },
        { id: 2, message: 'Someone liked your post', type: 'like', read: true },
      ])
    );
  }),

  // Mock error scenario
  rest.get(`${API_BASE}/error`, (req, res, ctx) => {
    return res(
      ctx.status(500),
      ctx.json({ detail: 'Internal server error' })
    );
  }),
];
```

#### Step 3: Setup MSW Server for Tests

Create `frontend/src/test/mocks/server.js`:

```javascript
import { setupServer } from 'msw/node';
import { handlers } from './handlers';

// Setup server with default handlers
export const server = setupServer(...handlers);
```

#### Step 4: Configure Test Setup

Update `frontend/vitest.config.js` to include setup file:

```javascript
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.js', // Add this line
  },
});
```

Create `frontend/src/test/setup.js`:

```javascript
import '@testing-library/jest-dom';
import { server } from './mocks/server';

// Establish API mocking before all tests
beforeAll(() => server.listen({ onUnhandledRequest: 'warn' }));

// Reset any request handlers after each test
afterEach(() => server.resetHandlers());

// Clean up after all tests
afterAll(() => server.close());

// Mock window.alert and window.confirm
global.alert = vi.fn();
global.confirm = vi.fn(() => true);
```

---

### Part 2: Test Async Components with Loading States (30 minutes)

Create a component that fetches data and test all states.

#### Step 1: Create Async Component

Create `frontend/src/components/NotificationsList.jsx`:

```javascript
import { useEffect, useState } from 'react';
import axios from 'axios';

export default function NotificationsList() {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchNotifications();
  }, []);

  const fetchNotifications = async () => {
    try {
      setLoading(true);
      const response = await axios.get('http://localhost:8000/api/notifications');
      setNotifications(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load notifications');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div role="status" aria-live="polite" data-testid="notifications-loading">
        Loading notifications...
      </div>
    );
  }

  if (error) {
    return (
      <div role="alert" data-testid="notifications-error">
        {error}
      </div>
    );
  }

  if (notifications.length === 0) {
    return (
      <div data-testid="notifications-empty">
        No notifications yet
      </div>
    );
  }

  return (
    <div data-testid="notifications-list">
      <h2>Notifications</h2>
      <ul>
        {notifications.map((notif) => (
          <li
            key={notif.id}
            data-testid={`notification-${notif.id}`}
            className={notif.read ? 'read' : 'unread'}
          >
            {notif.message}
          </li>
        ))}
      </ul>
    </div>
  );
}
```

#### Step 2: Test All Component States

Create `frontend/src/components/__tests__/NotificationsList.test.jsx`:

```javascript
import { render, screen, waitFor } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { rest } from 'msw';
import { server } from '../../test/mocks/server';
import NotificationsList from '../NotificationsList';

describe('NotificationsList Component', () => {
  it('shows loading state initially', () => {
    render(<NotificationsList />);

    expect(screen.getByTestId('notifications-loading')).toBeInTheDocument();
    expect(screen.getByText(/loading notifications/i)).toBeInTheDocument();
  });

  it('displays notifications after loading', async () => {
    render(<NotificationsList />);

    // Wait for loading to complete
    await waitFor(() => {
      expect(screen.queryByTestId('notifications-loading')).not.toBeInTheDocument();
    });

    // Verify notifications are displayed
    expect(screen.getByTestId('notifications-list')).toBeInTheDocument();
    expect(screen.getByText('New follower')).toBeInTheDocument();
    expect(screen.getByText('Someone liked your post')).toBeInTheDocument();
  });

  it('handles error state correctly', async () => {
    // Override handler to return error
    server.use(
      rest.get('http://localhost:8000/api/notifications', (req, res, ctx) => {
        return res(ctx.status(500), ctx.json({ detail: 'Server error' }));
      })
    );

    render(<NotificationsList />);

    // Wait for error state
    await waitFor(() => {
      expect(screen.getByTestId('notifications-error')).toBeInTheDocument();
    });

    expect(screen.getByText(/failed to load notifications/i)).toBeInTheDocument();
  });

  it('handles empty notifications', async () => {
    // Override handler to return empty array
    server.use(
      rest.get('http://localhost:8000/api/notifications', (req, res, ctx) => {
        return res(ctx.status(200), ctx.json([]));
      })
    );

    render(<NotificationsList />);

    await waitFor(() => {
      expect(screen.getByTestId('notifications-empty')).toBeInTheDocument();
    });

    expect(screen.getByText(/no notifications yet/i)).toBeInTheDocument();
  });

  it('displays correct notification count', async () => {
    render(<NotificationsList />);

    await waitFor(() => {
      expect(screen.getByTestId('notifications-list')).toBeInTheDocument();
    });

    // Check that both notifications are rendered
    const notificationItems = screen.getAllByRole('listitem');
    expect(notificationItems).toHaveLength(2);
  });
});
```

---

### Part 3: Test Stateful Components (25 minutes)

Test components with complex state management.

Create `frontend/src/components/PostComposer.jsx`:

```javascript
import { useState } from 'react';

export default function PostComposer({ onSubmit, maxLength = 280 }) {
  const [content, setContent] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [charCount, setCharCount] = useState(0);

  const handleChange = (e) => {
    const newContent = e.target.value;
    setContent(newContent);
    setCharCount(newContent.length);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (content.trim().length === 0) return;
    if (charCount > maxLength) return;

    setIsSubmitting(true);

    try {
      await onSubmit(content);
      // Reset on success
      setContent('');
      setCharCount(0);
    } catch (error) {
      // Keep content on error so user doesn't lose work
      console.error('Failed to submit:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const isOverLimit = charCount > maxLength;
  const canSubmit = content.trim().length > 0 && !isOverLimit && !isSubmitting;

  return (
    <form onSubmit={handleSubmit} data-testid="post-composer">
      <textarea
        value={content}
        onChange={handleChange}
        placeholder="What's on your mind?"
        disabled={isSubmitting}
        data-testid="post-composer-textarea"
        aria-label="Post content"
        aria-invalid={isOverLimit}
      />

      <div className="composer-footer">
        <span
          className={isOverLimit ? 'char-count-over' : 'char-count'}
          data-testid="post-composer-char-count"
          aria-live="polite"
        >
          {charCount} / {maxLength}
        </span>

        <button
          type="submit"
          disabled={!canSubmit}
          data-testid="post-composer-submit"
        >
          {isSubmitting ? 'Posting...' : 'Post'}
        </button>
      </div>
    </form>
  );
}
```

Create test `frontend/src/components/__tests__/PostComposer.test.jsx`:

```javascript
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import PostComposer from '../PostComposer';

describe('PostComposer Component', () => {
  it('updates character count as user types', async () => {
    const user = userEvent.setup();
    render(<PostComposer onSubmit={vi.fn()} />);

    const textarea = screen.getByTestId('post-composer-textarea');
    const charCount = screen.getByTestId('post-composer-char-count');

    expect(charCount).toHaveTextContent('0 / 280');

    await user.type(textarea, 'Hello');

    expect(charCount).toHaveTextContent('5 / 280');
  });

  it('disables submit when content is empty', async () => {
    render(<PostComposer onSubmit={vi.fn()} />);

    const submitButton = screen.getByTestId('post-composer-submit');
    expect(submitButton).toBeDisabled();
  });

  it('enables submit when content is valid', async () => {
    const user = userEvent.setup();
    render(<PostComposer onSubmit={vi.fn()} />);

    const textarea = screen.getByTestId('post-composer-textarea');
    const submitButton = screen.getByTestId('post-composer-submit');

    await user.type(textarea, 'Valid post content');

    expect(submitButton).not.toBeDisabled();
  });

  it('disables submit when over character limit', async () => {
    const user = userEvent.setup();
    render(<PostComposer onSubmit={vi.fn()} maxLength={10} />);

    const textarea = screen.getByTestId('post-composer-textarea');
    const submitButton = screen.getByTestId('post-composer-submit');

    await user.type(textarea, 'This is way too long');

    expect(submitButton).toBeDisabled();
  });

  it('calls onSubmit with content when submitted', async () => {
    const user = userEvent.setup();
    const mockSubmit = vi.fn().mockResolvedValue({});

    render(<PostComposer onSubmit={mockSubmit} />);

    const textarea = screen.getByTestId('post-composer-textarea');
    const submitButton = screen.getByTestId('post-composer-submit');

    await user.type(textarea, 'Test post');
    await user.click(submitButton);

    expect(mockSubmit).toHaveBeenCalledWith('Test post');
  });

  it('clears content after successful submission', async () => {
    const user = userEvent.setup();
    const mockSubmit = vi.fn().mockResolvedValue({});

    render(<PostComposer onSubmit={mockSubmit} />);

    const textarea = screen.getByTestId('post-composer-textarea');

    await user.type(textarea, 'Test post');
    await user.click(screen.getByTestId('post-composer-submit'));

    await waitFor(() => {
      expect(textarea).toHaveValue('');
    });
  });

  it('shows submitting state during submission', async () => {
    const user = userEvent.setup();
    let resolveSubmit;
    const mockSubmit = vi.fn(() => new Promise(resolve => {
      resolveSubmit = resolve;
    }));

    render(<PostComposer onSubmit={mockSubmit} />);

    const textarea = screen.getByTestId('post-composer-textarea');
    const submitButton = screen.getByTestId('post-composer-submit');

    await user.type(textarea, 'Test post');
    await user.click(submitButton);

    // Should show submitting state
    expect(submitButton).toHaveTextContent('Posting...');
    expect(submitButton).toBeDisabled();
    expect(textarea).toBeDisabled();

    // Resolve submission
    resolveSubmit();

    await waitFor(() => {
      expect(submitButton).toHaveTextContent('Post');
    });
  });

  it('retains content when submission fails', async () => {
    const user = userEvent.setup();
    const mockSubmit = vi.fn().mockRejectedValue(new Error('Network error'));

    render(<PostComposer onSubmit={mockSubmit} />);

    const textarea = screen.getByTestId('post-composer-textarea');

    await user.type(textarea, 'Important post');
    await user.click(screen.getByTestId('post-composer-submit'));

    // Content should remain after failure
    await waitFor(() => {
      expect(textarea).toHaveValue('Important post');
    });
  });
});
```

---

### Part 4: Accessibility Testing (25 minutes)

Add automated accessibility testing to catch a11y issues.

#### Step 1: Install axe

```bash
npm install --save-dev vitest-axe
```

#### Step 2: Configure axe

Add to `frontend/src/test/setup.js`:

```javascript
import { expect } from 'vitest';
import { toHaveNoViolations } from 'vitest-axe';

expect.extend(toHaveNoViolations);
```

#### Step 3: Create Accessible Component

Create `frontend/src/components/SearchForm.jsx`:

```javascript
import { useState } from 'react';

export default function SearchForm({ onSearch }) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(query);
  };

  return (
    <form onSubmit={handleSubmit} role="search" aria-label="Search posts">
      <label htmlFor="search-input">
        Search
      </label>
      <input
        id="search-input"
        type="search"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search posts..."
        aria-describedby="search-help"
      />
      <span id="search-help" className="sr-only">
        Enter keywords to search posts
      </span>
      <button type="submit" aria-label="Submit search">
        🔍
      </button>
    </form>
  );
}
```

#### Step 4: Test Accessibility

Create `frontend/src/components/__tests__/SearchForm.test.jsx`:

```javascript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import { axe } from 'vitest-axe';
import SearchForm from '../SearchForm';

describe('SearchForm Accessibility', () => {
  it('has no accessibility violations', async () => {
    const { container } = render(<SearchForm onSearch={vi.fn()} />);

    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('has proper form role', () => {
    render(<SearchForm onSearch={vi.fn()} />);

    expect(screen.getByRole('search')).toBeInTheDocument();
  });

  it('has label associated with input', () => {
    render(<SearchForm onSearch={vi.fn()} />);

    const input = screen.getByLabelText('Search');
    expect(input).toBeInTheDocument();
    expect(input).toHaveAttribute('id', 'search-input');
  });

  it('has descriptive help text', () => {
    render(<SearchForm onSearch={vi.fn()} />);

    const input = screen.getByRole('searchbox');
    expect(input).toHaveAttribute('aria-describedby', 'search-help');

    const helpText = document.getElementById('search-help');
    expect(helpText).toHaveTextContent('Enter keywords to search posts');
  });

  it('button has accessible label', () => {
    render(<SearchForm onSearch={vi.fn()} />);

    const button = screen.getByRole('button', { name: /submit search/i });
    expect(button).toBeInTheDocument();
  });

  it('is keyboard accessible', async () => {
    const user = userEvent.setup();
    const mockSearch = vi.fn();

    render(<SearchForm onSearch={mockSearch} />);

    const input = screen.getByRole('searchbox');

    // Tab to input
    await user.tab();
    expect(input).toHaveFocus();

    // Type and submit with Enter
    await user.type(input, 'test query{Enter}');

    expect(mockSearch).toHaveBeenCalledWith('test query');
  });
});
```

---

### Part 5: Test Context & Hooks (20 minutes)

Test components that use React Context.

Create test for component using AuthContext:

`frontend/src/components/__tests__/UserProfile.test.jsx`:

```javascript
import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { AuthContext } from '../../AuthContext';

// Simple component that uses auth context
function UserProfile() {
  const { user } = React.useContext(AuthContext);

  if (!user) {
    return <div data-testid="not-logged-in">Please log in</div>;
  }

  return (
    <div data-testid="user-profile">
      <h1>{user.display_name}</h1>
      <p>@{user.username}</p>
    </div>
  );
}

describe('UserProfile with Context', () => {
  const renderWithAuth = (user = null) => {
    const mockAuth = {
      user,
      login: vi.fn(),
      logout: vi.fn(),
    };

    return render(
      <AuthContext.Provider value={mockAuth}>
        <UserProfile />
      </AuthContext.Provider>
    );
  };

  it('shows login prompt when not authenticated', () => {
    renderWithAuth(null);

    expect(screen.getByTestId('not-logged-in')).toBeInTheDocument();
    expect(screen.getByText('Please log in')).toBeInTheDocument();
  });

  it('displays user info when authenticated', () => {
    const mockUser = {
      id: 1,
      username: 'testuser',
      display_name: 'Test User',
    };

    renderWithAuth(mockUser);

    expect(screen.getByTestId('user-profile')).toBeInTheDocument();
    expect(screen.getByText('Test User')).toBeInTheDocument();
    expect(screen.getByText('@testuser')).toBeInTheDocument();
  });
});
```

---

## 🎓 What You Learned

- ✅ **MSW** - Professional network mocking for components
- ✅ **Async patterns** - Test loading, success, and error states
- ✅ **Stateful components** - Test complex state transitions
- ✅ **Accessibility** - Automated a11y testing with axe
- ✅ **Context testing** - Test components with React Context
- ✅ **User interactions** - Realistic user event simulation

---

## 💪 Practice Challenges

### Challenge 1: Test Suspense Components

Create a component using React Suspense and test it.

### Challenge 2: Test Custom Hooks

Extract logic into custom hooks and write tests for them.

### Challenge 3: Visual Regression Setup

Research and set up basic visual regression with Playwright component testing.

### Challenge 4: Test Performance

Add performance testing to ensure components render efficiently.

---

## ✅ Lab Completion Checklist

- [ ] MSW installed and configured
- [ ] Tested async component with all states
- [ ] Tested stateful component with state transitions
- [ ] Accessibility tests passing
- [ ] Context-based component tested
- [ ] All tests pass with good coverage

---

## 📚 Resources

**Working Examples:**
- **`frontend/src/test/mocks/`** - ⭐ MSW setup ready to use
  - `handlers.js` - API mock handlers
  - `server.js` - MSW server configuration
  - `examples.js` - Common handler patterns
  - `README.md` - Usage guide
- **`frontend/src/components/__tests__/examples/`** - Component test examples directory

**Existing Tests:**
- `frontend/src/components/__tests__/CreatePost.test.jsx` - Current component tests
- `frontend/src/components/__tests__/Navbar.test.jsx` - Navigation tests

**Official Documentation:**
- [MSW Documentation](https://mswjs.io/)
- [Vitest Documentation](https://vitest.dev/)
- [Testing Library](https://testing-library.com/)
- [axe-core](https://github.com/dequelabs/axe-core)

---

**🎉 You've mastered advanced component testing! These patterns are used in professional React applications!**

**Next:** [Lab 6C: Integration & Contract Testing](LAB_06C_Frontend_Integration_Testing.md) - Connect your components to backend contracts!

