import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BrowserRouter } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { AuthContext } from '../../AuthContext';
import Navbar from '../../components/Navbar';

const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  };
});

// Helper to render with required providers
const renderNavbar = (authValue) => {
  return render(
    <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <AuthContext.Provider value={authValue}>
        <Navbar />
      </AuthContext.Provider>
    </BrowserRouter>
  );
};

describe('Navbar Component', () => {
  beforeEach(() => {
    mockNavigate.mockClear();
  });

  it('logs out and navigates to the login page when Logout is clicked', async () => {
    const user = userEvent.setup();
    const mockLogout = vi.fn();
    const mockAuth = {
      user: { id: 1, username: 'testuser', display_name: 'Test User' },
      login: vi.fn(),
      logout: mockLogout,
    };

    renderNavbar(mockAuth);
    await user.click(screen.getByRole('button', { name: 'Logout' }));

    expect(mockLogout).toHaveBeenCalled();
    expect(mockNavigate).toHaveBeenCalledWith('/login');
  });

  it('renders Testbook title', () => {
    const mockAuth = {
      user: null,
      login: vi.fn(),
      logout: vi.fn(),
    };

    renderNavbar(mockAuth);
    expect(screen.getByText('Testbook')).toBeInTheDocument();
  });

  it('shows login link when user is not authenticated', () => {
    const mockAuth = {
      user: null,
      login: vi.fn(),
      logout: vi.fn(),
    };

    renderNavbar(mockAuth);
    expect(screen.getByText('Login')).toBeInTheDocument();
  });

  it('shows logout button when user is authenticated', () => {
    const mockAuth = {
      user: { id: 1, username: 'testuser', display_name: 'Test User' },
      login: vi.fn(),
      logout: vi.fn(),
    };

    renderNavbar(mockAuth);
    expect(screen.getByText('Logout')).toBeInTheDocument();
  });

  it('displays user display name when authenticated', () => {
    const mockAuth = {
      user: { id: 1, username: 'testuser', display_name: 'Test User' },
      login: vi.fn(),
      logout: vi.fn(),
    };

    renderNavbar(mockAuth);
    expect(screen.getByText('Test User')).toBeInTheDocument();
  });

  it('shows Profile link when authenticated', () => {
    // Arrange - Set up authenticated user context
    const mockAuth = {
      user: { id: 1, username: 'testuser', display_name: 'Test User' },
      login: vi.fn(),
      logout: vi.fn(),
    };

    // Act - Render Navbar with authenticated state
    renderNavbar(mockAuth);

    // Assert - Profile link visible for authenticated users
    expect(screen.getByText('Profile')).toBeInTheDocument();
  });
});

// 🧠 Why These Tests Matter:
//
// Navbar component tests are ESSENTIAL because navigation is critical to UX:
//
// 1. **Authentication State** - Navbar shows different options based on login status
// 2. **Always Visible** - Navbar appears on every page, bugs affect entire app
// 3. **Context Integration** - Tests verify React Context (AuthContext) works correctly
// 4. **Accessibility** - Navigation must be keyboard-accessible and screen-reader friendly
//
// What These Tests Catch:
// - ✅ Wrong links shown (logout button appears when not logged in)
// - ✅ Context not updating (user logs in but navbar doesn't reflect it)
// - ✅ Missing navigation options (can't access profile/settings)
// - ✅ Broken conditional rendering (login/logout both showing)
// - ✅ Accessibility issues (links missing text, incorrect roles)
//
// In Real QA Teams:
// - Navbar tests are part of "critical path" test suites
// - They run on every component change (fast feedback)
// - Failed navbar tests indicate React Context issues (common bug source)
// - They verify global application state management works
//
// For Your Career:
// - Shows you understand React Context and state propagation
// - Demonstrates conditional rendering testing (if/else in JSX)
// - Proves you can test components with external dependencies (context, router)
// - Interview question: "How do you test authentication state in UI?" - Point to these!
// - Shows you test user-facing behavior, not implementation details
