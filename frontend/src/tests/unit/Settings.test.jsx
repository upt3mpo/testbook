/**
 * Unit tests for the Settings page.
 */

import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BrowserRouter } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import * as api from '../../api';
import { AuthContext } from '../../AuthContext';
import Settings from '../../pages/Settings';

vi.mock('../../api', () => ({
  usersAPI: {
    updateProfile: vi.fn(),
    uploadAvatar: vi.fn(),
    clearAvatar: vi.fn(),
    deleteAccount: vi.fn(),
  },
}));

const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  };
});

const baseUser = {
  id: 1,
  email: 'sarah.johnson@testbook.com',
  username: 'sarahjohnson',
  display_name: 'Sarah Johnson',
  bio: 'Original bio',
  theme: 'light',
  text_density: 'normal',
  profile_picture: '/static/uploads/avatars/sarah.jpg',
};

const renderSettings = ({ updateUser = vi.fn(), logout = vi.fn(), user = baseUser } = {}) => {
  return render(
    <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <AuthContext.Provider value={{ user, updateUser, logout }}>
        <Settings />
      </AuthContext.Provider>
    </BrowserRouter>
  );
};

describe('Settings Page', () => {
  // Not covered: cancelling at the *second* delete-account confirm()
  // (the existing test below only cancels the first), and the visible
  // "Upload Photo"/drop-zone-style button's onClick, which just proxies
  // to fileInputRef.current?.click() - no branching logic of its own,
  // already effectively exercised by driving the hidden file input
  // directly in the upload test below. Neither is hard, just low
  // marginal value given what's already covered.
  beforeEach(() => {
    vi.clearAllMocks();
    window.confirm = vi.fn(() => true);
    window.alert = vi.fn();
    document.documentElement.removeAttribute('data-theme');
  });

  it("displays the user's email and username", () => {
    renderSettings();

    expect(screen.getByText('sarah.johnson@testbook.com')).toBeInTheDocument();
    expect(screen.getByText('@sarahjohnson')).toBeInTheDocument();
  });

  it('prefills the form with the current profile data', () => {
    renderSettings();

    expect(screen.getByLabelText('Display Name')).toHaveValue('Sarah Johnson');
    expect(screen.getByLabelText('Bio')).toHaveValue('Original bio');
  });

  it('saves an updated display name', async () => {
    const user = userEvent.setup();
    const updateUser = vi.fn();
    api.usersAPI.updateProfile.mockResolvedValueOnce({
      data: { ...baseUser, display_name: 'Sarah J.' },
    });
    renderSettings({ updateUser });

    await user.clear(screen.getByLabelText('Display Name'));
    await user.type(screen.getByLabelText('Display Name'), 'Sarah J.');
    await user.click(screen.getByRole('button', { name: 'Save Changes' }));

    await waitFor(() => {
      expect(api.usersAPI.updateProfile).toHaveBeenCalledWith(
        expect.objectContaining({ display_name: 'Sarah J.' })
      );
    });
    expect(updateUser).toHaveBeenCalledWith({ ...baseUser, display_name: 'Sarah J.' });
    expect(await screen.findByText('Settings updated successfully!')).toBeInTheDocument();
  });

  it('shows an error message when saving fails', async () => {
    const user = userEvent.setup();
    const originalError = console.error;
    console.error = () => {};
    api.usersAPI.updateProfile.mockRejectedValueOnce(new Error('Network error'));
    renderSettings();

    await user.click(screen.getByRole('button', { name: 'Save Changes' }));

    expect(await screen.findByText('Failed to update settings')).toBeInTheDocument();
    console.error = originalError;
  });

  it('applies the theme to the page as soon as it is selected', async () => {
    const user = userEvent.setup();
    renderSettings();

    await user.selectOptions(screen.getByLabelText('Theme'), 'dark');

    expect(document.documentElement).toHaveAttribute('data-theme', 'dark');
  });

  it('uploads a new avatar', async () => {
    const user = userEvent.setup();
    const updateUser = vi.fn();
    api.usersAPI.uploadAvatar.mockResolvedValueOnce({
      data: { url: '/static/uploads/avatars/new.jpg' },
    });
    renderSettings({ updateUser });

    const file = new File(['fake-image-bytes'], 'avatar.jpg', { type: 'image/jpeg' });
    const fileInput = document.querySelector('[data-testid="settings-avatar-input"]');
    await user.upload(fileInput, file);

    await waitFor(() => {
      expect(api.usersAPI.uploadAvatar).toHaveBeenCalledWith(file);
    });
    expect(updateUser).toHaveBeenCalledWith({
      ...baseUser,
      profile_picture: '/static/uploads/avatars/new.jpg',
    });
    expect(await screen.findByText('Profile picture updated successfully!')).toBeInTheDocument();
  });

  it('rejects a file that is not an accepted image type', async () => {
    renderSettings();

    // The input's accept attribute would normally stop a real browser's
    // file picker from offering a PDF, and userEvent.upload() mimics
    // that by refusing to attach a non-matching file - so this uses
    // fireEvent to simulate the file arriving anyway (e.g. via drag and
    // drop, which isn't filtered by accept), which is exactly the case
    // handleAvatarUpload's own type check exists to catch.
    const file = new File(['not-an-image'], 'document.pdf', { type: 'application/pdf' });
    const fileInput = document.querySelector('[data-testid="settings-avatar-input"]');
    fireEvent.change(fileInput, { target: { files: [file] } });

    expect(
      await screen.findByText('Please select a valid image file (JPG, PNG, GIF, WebP)')
    ).toBeInTheDocument();
    expect(api.usersAPI.uploadAvatar).not.toHaveBeenCalled();
  });

  it('clears the avatar after confirming', async () => {
    const user = userEvent.setup();
    const updateUser = vi.fn();
    api.usersAPI.clearAvatar.mockResolvedValueOnce({
      data: { profile_picture: '/static/images/default-avatar.jpg' },
    });
    renderSettings({ updateUser });

    await user.click(screen.getByRole('button', { name: /clear photo/i }));

    expect(window.confirm).toHaveBeenCalled();
    await waitFor(() => {
      expect(api.usersAPI.clearAvatar).toHaveBeenCalled();
    });
    expect(await screen.findByText(/using default avatar/i)).toBeInTheDocument();
  });

  it('does not clear the avatar if the user cancels the confirmation', async () => {
    const user = userEvent.setup();
    window.confirm = vi.fn(() => false);
    renderSettings();

    await user.click(screen.getByRole('button', { name: /clear photo/i }));

    expect(api.usersAPI.clearAvatar).not.toHaveBeenCalled();
  });

  it('deletes the account after both confirmations and redirects to login', async () => {
    const user = userEvent.setup();
    const logout = vi.fn();
    api.usersAPI.deleteAccount.mockResolvedValueOnce({});
    renderSettings({ logout });

    await user.click(screen.getByRole('button', { name: 'Delete Account' }));

    expect(window.confirm).toHaveBeenCalledTimes(2);
    await waitFor(() => {
      expect(api.usersAPI.deleteAccount).toHaveBeenCalled();
    });
    expect(logout).toHaveBeenCalled();

    // navigate('/') is deferred behind a short setTimeout in the real
    // component (to let the alert() dismiss first) - wait for it rather
    // than asserting immediately.
    await waitFor(() => expect(mockNavigate).toHaveBeenCalledWith('/'));
  });

  it('does not delete the account if the first confirmation is cancelled', async () => {
    const user = userEvent.setup();
    window.confirm = vi.fn(() => false);
    renderSettings();

    await user.click(screen.getByRole('button', { name: 'Delete Account' }));

    expect(api.usersAPI.deleteAccount).not.toHaveBeenCalled();
  });
});
