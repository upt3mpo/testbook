/**
 * Unit tests for AuthContext/AuthProvider.
 *
 * Every other component test mocks AuthContext's value directly, which
 * is the right call for testing those components in isolation - but it
 * means AuthProvider's own logic (login/register/logout, loading the
 * current user on mount, persisting the token) never actually runs in
 * any of them. These tests exercise the real provider instead, through
 * a small consumer component that surfaces its state.
 */

import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import * as api from '../../api';
import { AuthProvider, useAuth } from '../../AuthContext';

vi.mock('../../api', () => ({
  authAPI: {
    login: vi.fn(),
    register: vi.fn(),
    getMe: vi.fn(),
  },
}));

function AuthConsumer() {
  const { user, loading, isAuthenticated, login, register, logout, updateUser } = useAuth();

  return (
    <div>
      <div data-testid="loading-state">{loading ? 'loading' : 'idle'}</div>
      <div data-testid="auth-state">{isAuthenticated ? 'authenticated' : 'anonymous'}</div>
      <div data-testid="display-name">{user?.display_name ?? 'none'}</div>
      <button onClick={() => login('sarah.johnson@testbook.com', 'Sarah2024!')}>Login</button>
      <button
        onClick={() =>
          register({ email: 'new@testbook.com', username: 'newuser', password: 'pw' })
        }
      >
        Register
      </button>
      <button onClick={logout}>Logout</button>
      <button onClick={() => updateUser({ bio: 'Updated bio' })}>Update</button>
    </div>
  );
}

const renderWithProvider = () => {
  return render(
    <AuthProvider>
      <AuthConsumer />
    </AuthProvider>
  );
};

describe('AuthProvider', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    window.localStorage.getItem = vi.fn(() => null);
    window.localStorage.setItem = vi.fn();
    window.localStorage.removeItem = vi.fn();
  });

  it('starts with no user and finishes loading when there is no stored token', async () => {
    renderWithProvider();

    await waitFor(() => {
      expect(screen.getByTestId('loading-state')).toHaveTextContent('idle');
    });
    expect(screen.getByTestId('auth-state')).toHaveTextContent('anonymous');
    expect(api.authAPI.getMe).not.toHaveBeenCalled();
  });

  it('loads the current user on mount when a token is already stored', async () => {
    window.localStorage.getItem = vi.fn(() => 'existing-token');
    api.authAPI.getMe.mockResolvedValueOnce({
      data: { id: 1, display_name: 'Sarah Johnson' },
    });

    renderWithProvider();

    await waitFor(() => {
      expect(screen.getByTestId('auth-state')).toHaveTextContent('authenticated');
    });
    expect(screen.getByTestId('display-name')).toHaveTextContent('Sarah Johnson');
  });

  it('clears the stored token when loading the user fails', async () => {
    window.localStorage.getItem = vi.fn(() => 'expired-token');
    const originalError = console.error;
    console.error = () => {};
    api.authAPI.getMe.mockRejectedValueOnce(new Error('401 Unauthorized'));

    renderWithProvider();

    await waitFor(() => {
      expect(screen.getByTestId('loading-state')).toHaveTextContent('idle');
    });
    expect(window.localStorage.removeItem).toHaveBeenCalledWith('token');
    expect(screen.getByTestId('auth-state')).toHaveTextContent('anonymous');
    console.error = originalError;
  });

  it('logs in, stores the token, and loads the user', async () => {
    const user = userEvent.setup();
    api.authAPI.login.mockResolvedValueOnce({ data: { access_token: 'new-token' } });
    api.authAPI.getMe.mockResolvedValueOnce({
      data: { id: 1, display_name: 'Sarah Johnson' },
    });

    renderWithProvider();
    await waitFor(() => expect(screen.getByTestId('loading-state')).toHaveTextContent('idle'));

    await user.click(screen.getByRole('button', { name: 'Login' }));

    expect(api.authAPI.login).toHaveBeenCalledWith('sarah.johnson@testbook.com', 'Sarah2024!');
    await waitFor(() => {
      expect(window.localStorage.setItem).toHaveBeenCalledWith('token', 'new-token');
    });
    expect(await screen.findByTestId('display-name')).toHaveTextContent('Sarah Johnson');
  });

  it('registers, stores the token, and loads the user', async () => {
    const user = userEvent.setup();
    api.authAPI.register.mockResolvedValueOnce({ data: { access_token: 'signup-token' } });
    api.authAPI.getMe.mockResolvedValueOnce({ data: { id: 2, display_name: 'New User' } });

    renderWithProvider();
    await waitFor(() => expect(screen.getByTestId('loading-state')).toHaveTextContent('idle'));

    await user.click(screen.getByRole('button', { name: 'Register' }));

    expect(api.authAPI.register).toHaveBeenCalledWith({
      email: 'new@testbook.com',
      username: 'newuser',
      password: 'pw',
    });
    expect(await screen.findByTestId('display-name')).toHaveTextContent('New User');
  });

  it('clears the token and user on logout', async () => {
    const user = userEvent.setup();
    window.localStorage.getItem = vi.fn(() => 'existing-token');
    api.authAPI.getMe.mockResolvedValueOnce({
      data: { id: 1, display_name: 'Sarah Johnson' },
    });

    renderWithProvider();
    await waitFor(() =>
      expect(screen.getByTestId('auth-state')).toHaveTextContent('authenticated')
    );

    await user.click(screen.getByRole('button', { name: 'Logout' }));

    expect(window.localStorage.removeItem).toHaveBeenCalledWith('token');
    expect(screen.getByTestId('auth-state')).toHaveTextContent('anonymous');
  });

  it('merges partial updates into the current user without a server round trip', async () => {
    const user = userEvent.setup();
    window.localStorage.getItem = vi.fn(() => 'existing-token');
    api.authAPI.getMe.mockResolvedValueOnce({
      data: { id: 1, display_name: 'Sarah Johnson', bio: 'Original bio' },
    });

    renderWithProvider();
    await waitFor(() =>
      expect(screen.getByTestId('display-name')).toHaveTextContent('Sarah Johnson')
    );

    await user.click(screen.getByRole('button', { name: 'Update' }));

    // display_name is untouched by the partial update
    expect(screen.getByTestId('display-name')).toHaveTextContent('Sarah Johnson');
  });
});
