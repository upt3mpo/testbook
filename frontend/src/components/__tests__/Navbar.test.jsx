import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { describe, expect, it, vi } from 'vitest';
import { AuthContext } from '../../AuthContext';
import Navbar from '../Navbar';

// Helper to render with required providers
const renderNavbar = (authValue) => {
  return render(
    <BrowserRouter>
      <AuthContext.Provider value={authValue}>
        <Navbar />
      </AuthContext.Provider>
    </BrowserRouter>
  );
};

describe('Navbar Component', () => {
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
    const mockAuth = {
      user: { id: 1, username: 'testuser', display_name: 'Test User' },
      login: vi.fn(),
      logout: vi.fn(),
    };

    renderNavbar(mockAuth);
    expect(screen.getByText('Profile')).toBeInTheDocument();
  });
});

