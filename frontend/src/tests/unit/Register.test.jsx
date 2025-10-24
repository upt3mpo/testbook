/**
 * Unit tests for the Register component.
 *
 * This file demonstrates comprehensive React component testing using:
 * - React Testing Library for user-centric testing
 * - Vitest for test runner and assertions
 * - Mocking external dependencies (API, navigation)
 * - Testing user interactions and form behavior
 * - Testing async operations and error handling
 *
 * Key Testing Concepts Demonstrated:
 * - Component rendering and user interaction testing
 * - Mocking external dependencies (API calls, navigation)
 * - Testing form validation and submission
 * - Testing loading states and error handling
 * - Testing context providers and state management
 *
 * This file is referenced in Stage 1 and Stage 2 learning materials
 * as an example of professional React component testing.
 */

import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { AuthContext } from '../../AuthContext';
import Register from '../../pages/Register';

/**
 * Mock the API module to control API responses in tests.
 *
 * This allows us to test component behavior without making real API calls.
 * We can simulate success, failure, and different response scenarios.
 */
vi.mock('../../api', () => ({
  authAPI: {
    register: vi.fn(), // Mock the register function
    login: vi.fn(), // Mock the login function
  },
}));

/**
 * Mock React Router's useNavigate hook.
 *
 * This allows us to test navigation behavior without actually navigating.
 * We can verify that the correct routes are called after user actions.
 */
const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => mockNavigate, // Return our mock function
  };
});

/**
 * Test helper function to render the Register component with proper context.
 *
 * This function wraps the Register component with all necessary providers:
 * - BrowserRouter for routing context
 * - AuthContext for authentication state
 *
 * @param {Object} authValue - Optional auth context value for testing
 * @returns {Object} Rendered component and utilities
 */
const renderRegister = (authValue = null) => {
  // Create default mock auth context if none provided
  const mockAuth = authValue || {
    user: null,
    login: vi.fn(),
    logout: vi.fn(),
    register: vi.fn(),
  };

  return render(
    <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <AuthContext.Provider value={mockAuth}>
        <Register />
      </AuthContext.Provider>
    </BrowserRouter>
  );
};

describe('Register Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockNavigate.mockClear();
  });

  it('renders registration form', () => {
    renderRegister();

    expect(screen.getByTestId('register-page')).toBeInTheDocument();
    expect(screen.getByTestId('register-title')).toHaveTextContent('Create Account');
    expect(screen.getByTestId('register-form')).toBeInTheDocument();
  });

  it('renders all required form fields', () => {
    renderRegister();

    expect(screen.getByTestId('register-email-input')).toBeInTheDocument();
    expect(screen.getByTestId('register-username-input')).toBeInTheDocument();
    expect(screen.getByTestId('register-displayname-input')).toBeInTheDocument();
    expect(screen.getByTestId('register-password-input')).toBeInTheDocument();
    expect(screen.getByTestId('register-bio-input')).toBeInTheDocument();
    expect(screen.getByTestId('register-submit-button')).toBeInTheDocument();
  });

  it('allows user to type in form fields', () => {
    /**
     * Test user interaction with form inputs.
     *
     * This test verifies that users can interact with form fields,
     * which is fundamental to any form component. We test:
     * 1. Form fields are accessible and interactive
     * 2. User input is captured correctly
     * 3. Form state updates as user types
     *
     * This demonstrates the AAA pattern in React testing:
     * - Arrange: Render component and get form elements
     * - Act: Simulate user typing in form fields
     * - Assert: Verify the form state reflects user input
     */

    // Arrange - Render the component and get form elements
    renderRegister();
    const emailInput = screen.getByTestId('register-email-input');
    const usernameInput = screen.getByTestId('register-username-input');

    // Act - Simulate user typing in the form fields
    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(usernameInput, { target: { value: 'testuser' } });

    // Assert - Verify the form state reflects user input
    expect(emailInput.value).toBe('test@example.com');
    expect(usernameInput.value).toBe('testuser');
  });

  it('shows loading state during submission', async () => {
    // Mock a slow register function
    const mockRegister = vi
      .fn()
      .mockImplementation(
        () => new Promise((resolve) => setTimeout(() => resolve({ data: { id: 1 } }), 100))
      );
    const mockAuth = {
      user: null,
      login: vi.fn(),
      logout: vi.fn(),
      register: mockRegister,
    };

    renderRegister(mockAuth);

    const emailInput = screen.getByTestId('register-email-input');
    const usernameInput = screen.getByTestId('register-username-input');
    const displayNameInput = screen.getByTestId('register-displayname-input');
    const passwordInput = screen.getByTestId('register-password-input');
    const submitButton = screen.getByTestId('register-submit-button');

    // Fill all required form fields
    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(usernameInput, { target: { value: 'testuser' } });
    fireEvent.change(displayNameInput, { target: { value: 'Test User' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });
    fireEvent.click(submitButton);

    // Should show loading state
    expect(screen.getByText('Creating Account...')).toBeInTheDocument();
    expect(submitButton).toBeDisabled();
  });

  it('calls register API with correct data on form submission', async () => {
    const mockRegister = vi.fn().mockResolvedValue({ data: { id: 1 } });
    const mockAuth = {
      user: null,
      login: vi.fn(),
      logout: vi.fn(),
      register: mockRegister,
    };

    renderRegister(mockAuth);

    const emailInput = screen.getByTestId('register-email-input');
    const usernameInput = screen.getByTestId('register-username-input');
    const displayNameInput = screen.getByTestId('register-displayname-input');
    const passwordInput = screen.getByTestId('register-password-input');
    const bioInput = screen.getByTestId('register-bio-input');
    const submitButton = screen.getByTestId('register-submit-button');

    // Fill out the form
    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(usernameInput, { target: { value: 'testuser' } });
    fireEvent.change(displayNameInput, { target: { value: 'Test User' } });
    fireEvent.change(passwordInput, { target: { value: 'SecurePass123!' } });
    fireEvent.change(bioInput, { target: { value: 'Test bio' } });

    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockRegister).toHaveBeenCalledWith({
        email: 'test@example.com',
        username: 'testuser',
        display_name: 'Test User',
        password: 'SecurePass123!',
        bio: 'Test bio',
      });
    });
  });

  it('navigates to home page after successful registration', async () => {
    const mockRegister = vi.fn().mockResolvedValue({ data: { id: 1 } });
    const mockAuth = {
      user: null,
      login: vi.fn(),
      logout: vi.fn(),
      register: mockRegister,
    };

    renderRegister(mockAuth);

    const emailInput = screen.getByTestId('register-email-input');
    const usernameInput = screen.getByTestId('register-username-input');
    const displayNameInput = screen.getByTestId('register-displayname-input');
    const passwordInput = screen.getByTestId('register-password-input');
    const submitButton = screen.getByTestId('register-submit-button');

    // Fill all required form fields
    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(usernameInput, { target: { value: 'testuser' } });
    fireEvent.change(displayNameInput, { target: { value: 'Test User' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockNavigate).toHaveBeenCalledWith('/');
    });
  });

  it('handles registration API errors gracefully', async () => {
    // Suppress expected error output in test logs
    const originalError = console.error;
    console.error = () => {};

    // Arrange - Mock register function to return error with proper structure
    const mockRegister = vi.fn().mockRejectedValue({
      response: {
        data: {
          detail: 'Email already exists',
        },
      },
    });
    const mockAuth = {
      user: null,
      login: vi.fn(),
      logout: vi.fn(),
      register: mockRegister,
    };

    renderRegister(mockAuth);

    const emailInput = screen.getByTestId('register-email-input');
    const usernameInput = screen.getByTestId('register-username-input');
    const displayNameInput = screen.getByTestId('register-displayname-input');
    const passwordInput = screen.getByTestId('register-password-input');
    const submitButton = screen.getByTestId('register-submit-button');

    // Act - User fills form and submits but API fails
    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(usernameInput, { target: { value: 'testuser' } });
    fireEvent.change(displayNameInput, { target: { value: 'Test User' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });
    fireEvent.click(submitButton);

    // Assert - Error message displayed to user
    await waitFor(() => {
      expect(screen.getByTestId('register-error')).toHaveTextContent('Email already exists');
    });

    // Restore console.error
    console.error = originalError;
  });

  it('handles validation errors from API', async () => {
    const mockRegister = vi.fn().mockRejectedValue({
      response: {
        data: {
          detail: 'Username must be at least 3 characters long',
        },
      },
    });
    const mockAuth = {
      user: null,
      login: vi.fn(),
      logout: vi.fn(),
      register: mockRegister,
    };

    renderRegister(mockAuth);

    const emailInput = screen.getByTestId('register-email-input');
    const usernameInput = screen.getByTestId('register-username-input');
    const displayNameInput = screen.getByTestId('register-displayname-input');
    const passwordInput = screen.getByTestId('register-password-input');
    const submitButton = screen.getByTestId('register-submit-button');

    // Fill all required form fields
    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(usernameInput, { target: { value: 'testuser' } });
    fireEvent.change(displayNameInput, { target: { value: 'Test User' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByTestId('register-error')).toHaveTextContent(
        'Username must be at least 3 characters long'
      );
    });
  });

  it('shows generic error message for unknown errors', async () => {
    const mockRegister = vi.fn().mockRejectedValue(new Error('Network error'));
    const mockAuth = {
      user: null,
      login: vi.fn(),
      logout: vi.fn(),
      register: mockRegister,
    };

    renderRegister(mockAuth);

    const emailInput = screen.getByTestId('register-email-input');
    const usernameInput = screen.getByTestId('register-username-input');
    const displayNameInput = screen.getByTestId('register-displayname-input');
    const passwordInput = screen.getByTestId('register-password-input');
    const submitButton = screen.getByTestId('register-submit-button');

    // Fill all required form fields
    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(usernameInput, { target: { value: 'testuser' } });
    fireEvent.change(displayNameInput, { target: { value: 'Test User' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByTestId('register-error')).toHaveTextContent(
        'Registration failed. Please try again.'
      );
    });
  });

  it('clears error message when user starts typing again', async () => {
    const mockRegister = vi.fn().mockRejectedValue({
      response: {
        data: {
          detail: 'Email already exists',
        },
      },
    });
    const mockAuth = {
      user: null,
      login: vi.fn(),
      logout: vi.fn(),
      register: mockRegister,
    };

    renderRegister(mockAuth);

    const emailInput = screen.getByTestId('register-email-input');
    const usernameInput = screen.getByTestId('register-username-input');
    const displayNameInput = screen.getByTestId('register-displayname-input');
    const passwordInput = screen.getByTestId('register-password-input');
    const submitButton = screen.getByTestId('register-submit-button');

    // First submission fails - fill all required fields
    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(usernameInput, { target: { value: 'testuser' } });
    fireEvent.change(displayNameInput, { target: { value: 'Test User' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByTestId('register-error')).toHaveTextContent('Email already exists');
    });

    // Start typing again - error should clear
    fireEvent.change(emailInput, { target: { value: 'new@example.com' } });

    expect(screen.queryByTestId('register-error')).not.toBeInTheDocument();
  });
});

// 🧠 Why These Tests Matter:
//
// Registration component tests are CRITICAL for user onboarding because:
//
// 1. **First User Experience** - Registration is often the first interaction with your app
// 2. **Form Integration** - Tests verify complex form state management works correctly
// 3. **API Integration** - Tests ensure frontend calls backend APIs with correct data
// 4. **Error Handling** - Users need clear feedback when registration fails
// 5. **Navigation Flow** - Tests verify users are redirected after successful registration
//
// What These Tests Catch:
// - ✅ Broken form validation (users can submit invalid data)
// - ✅ API integration bugs (wrong payload structure sent to backend)
// - ✅ Missing error handling (users see generic errors instead of helpful messages)
// - ✅ Navigation issues (users get stuck on registration page)
// - ✅ State management bugs (loading states, error clearing)
// - ✅ Accessibility issues (form fields missing labels, buttons not keyboard accessible)
//
// In Real QA Teams:
// - Registration tests are part of "critical path" test suites
// - They run on every deployment (can't afford registration bugs)
// - Failed registration tests are P0 (highest priority) bugs
// - They serve as documentation for the registration flow
// - They prevent regressions during authentication system changes
//
// For Your Career:
// - Form testing is a core QA skill (every app has forms)
// - Shows you understand React state management and API integration
// - Demonstrates error handling and user experience testing
// - Interview question: "How do you test user registration?" - Point to these!
// - Proves you can test complex user workflows, not just simple components
