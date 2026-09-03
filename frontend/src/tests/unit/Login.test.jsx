/**
 * Unit tests for the Login component.
 */

import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BrowserRouter } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { AuthContext } from '../../AuthContext';
import Login from '../../pages/Login';

const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  };
});

const renderLogin = (authValue) => {
  const mockAuth = authValue || { login: vi.fn() };
  return render(
    <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <AuthContext.Provider value={mockAuth}>
        <Login />
      </AuthContext.Provider>
    </BrowserRouter>
  );
};

describe('Login Component', () => {
  beforeEach(() => {
    mockNavigate.mockClear();
  });

  it('renders the login form', () => {
    renderLogin();

    expect(screen.getByPlaceholderText('Email')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Password')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Log In' })).toBeInTheDocument();
  });

  it('allows the user to type an email and password', async () => {
    const user = userEvent.setup();
    renderLogin();

    const emailInput = screen.getByPlaceholderText('Email');
    const passwordInput = screen.getByPlaceholderText('Password');

    await user.type(emailInput, 'sarah.johnson@testbook.com');
    await user.type(passwordInput, 'Sarah2024!');

    expect(emailInput.value).toBe('sarah.johnson@testbook.com');
    expect(passwordInput.value).toBe('Sarah2024!');
  });

  it('links to the registration page', () => {
    renderLogin();
    expect(screen.getByRole('link', { name: /create new account/i })).toHaveAttribute(
      'href',
      '/register'
    );
  });

  it('logs in and navigates to the feed on success', async () => {
    const user = userEvent.setup();
    const mockLogin = vi.fn().mockResolvedValue({ access_token: 'abc123' });
    renderLogin({ login: mockLogin });

    await user.type(screen.getByPlaceholderText('Email'), 'sarah.johnson@testbook.com');
    await user.type(screen.getByPlaceholderText('Password'), 'Sarah2024!');
    await user.click(screen.getByRole('button', { name: 'Log In' }));

    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalledWith('sarah.johnson@testbook.com', 'Sarah2024!');
    });
    expect(mockNavigate).toHaveBeenCalledWith('/');
  });

  it('shows the loading state while logging in', async () => {
    const user = userEvent.setup();
    // Resolved explicitly at the end of the test rather than via a real
    // timer, so the login promise doesn't settle (and call navigate)
    // after this test has already finished.
    let resolveLogin;
    const mockLogin = vi.fn().mockImplementation(
      () =>
        new Promise((resolve) => {
          resolveLogin = resolve;
        })
    );
    renderLogin({ login: mockLogin });

    await user.type(screen.getByPlaceholderText('Email'), 'sarah.johnson@testbook.com');
    await user.type(screen.getByPlaceholderText('Password'), 'Sarah2024!');
    await user.click(screen.getByRole('button', { name: 'Log In' }));

    expect(screen.getByRole('button', { name: 'Logging in...' })).toBeDisabled();

    resolveLogin({ access_token: 'abc123' });
    await waitFor(() => expect(mockNavigate).toHaveBeenCalled());
  });

  it('shows the backend error message on failed login', async () => {
    const user = userEvent.setup();
    const originalError = console.error;
    console.error = () => {};

    const mockLogin = vi.fn().mockRejectedValue({
      response: { data: { detail: 'Incorrect email or password' } },
    });
    renderLogin({ login: mockLogin });

    await user.type(screen.getByPlaceholderText('Email'), 'sarah.johnson@testbook.com');
    await user.type(screen.getByPlaceholderText('Password'), 'WrongPassword');
    await user.click(screen.getByRole('button', { name: 'Log In' }));

    expect(await screen.findByText('Incorrect email or password')).toBeInTheDocument();
    expect(mockNavigate).not.toHaveBeenCalled();

    console.error = originalError;
  });

  it('shows a generic error message when the backend gives no detail', async () => {
    const user = userEvent.setup();
    const originalError = console.error;
    console.error = () => {};

    const mockLogin = vi.fn().mockRejectedValue(new Error('Network error'));
    renderLogin({ login: mockLogin });

    await user.type(screen.getByPlaceholderText('Email'), 'sarah.johnson@testbook.com');
    await user.type(screen.getByPlaceholderText('Password'), 'Sarah2024!');
    await user.click(screen.getByRole('button', { name: 'Log In' }));

    expect(
      await screen.findByText('Invalid credentials. Please check your email and password.')
    ).toBeInTheDocument();

    console.error = originalError;
  });
});
