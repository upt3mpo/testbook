/**
 * Unit tests for the Following page.
 */

import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import * as api from '../../api';
import { AuthContext } from '../../AuthContext';
import Following from '../../pages/Following';

vi.mock('../../api', () => ({
  usersAPI: {
    getFollowing: vi.fn(),
    unfollowUser: vi.fn(),
  },
}));

const sarah = { id: 1, username: 'sarahjohnson', display_name: 'Sarah Johnson' };

const makeFollowedUser = (overrides = {}) => ({
  id: 2,
  username: 'mikechen',
  display_name: 'Mike Chen',
  bio: 'Photographer',
  profile_picture: '/static/uploads/avatars/mike.jpg',
  is_following: true,
  ...overrides,
});

const renderFollowing = (username = 'sarahjohnson', currentUser = sarah) => {
  return render(
    <MemoryRouter initialEntries={[`/profile/${username}/following`]}>
      <AuthContext.Provider value={{ user: currentUser }}>
        <Routes>
          <Route path="/profile/:username/following" element={<Following />} />
        </Routes>
      </AuthContext.Provider>
    </MemoryRouter>
  );
};

describe('Following Page', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    window.alert = vi.fn();
  });

  it('shows "Following" on your own following page', async () => {
    api.usersAPI.getFollowing.mockResolvedValueOnce({ data: [] });

    renderFollowing('sarahjohnson');

    expect(await screen.findByText('Following')).toBeInTheDocument();
  });

  it("shows the owner's name on someone else's following page", async () => {
    api.usersAPI.getFollowing.mockResolvedValueOnce({ data: [] });

    renderFollowing('mikechen');

    expect(await screen.findByText('mikechen is Following')).toBeInTheDocument();
  });

  it('shows an error message when following list fails to load', async () => {
    api.usersAPI.getFollowing.mockRejectedValueOnce(new Error('Network error'));

    renderFollowing();

    expect(await screen.findByText('Failed to load following')).toBeInTheDocument();
  });

  it('shows an empty message when following no one', async () => {
    api.usersAPI.getFollowing.mockResolvedValueOnce({ data: [] });

    renderFollowing();

    expect(await screen.findByText('Not following anyone yet.')).toBeInTheDocument();
  });

  it('lists followed users with their name and bio', async () => {
    api.usersAPI.getFollowing.mockResolvedValueOnce({ data: [makeFollowedUser()] });

    renderFollowing();

    expect(await screen.findByText('Mike Chen')).toBeInTheDocument();
    expect(screen.getByText('@mikechen')).toBeInTheDocument();
    expect(screen.getByText('Photographer')).toBeInTheDocument();
  });

  it('does not show an unfollow button on another user’s following page', async () => {
    api.usersAPI.getFollowing.mockResolvedValueOnce({ data: [makeFollowedUser()] });

    renderFollowing('mikechen');

    await screen.findByText('Mike Chen');
    expect(screen.queryByRole('button', { name: /unfollow/i })).not.toBeInTheDocument();
  });

  it('unfollows a user from your own following page', async () => {
    const user = userEvent.setup();
    api.usersAPI.getFollowing.mockResolvedValueOnce({ data: [makeFollowedUser()] });
    api.usersAPI.unfollowUser.mockResolvedValueOnce({});
    api.usersAPI.getFollowing.mockResolvedValueOnce({ data: [] });

    renderFollowing();
    await screen.findByText('Mike Chen');

    await user.click(screen.getByRole('button', { name: 'Unfollow' }));

    await waitFor(() => {
      expect(api.usersAPI.unfollowUser).toHaveBeenCalledWith('mikechen');
    });
    expect(await screen.findByText('Not following anyone yet.')).toBeInTheDocument();
  });

  it('shows an alert if unfollowing fails', async () => {
    const user = userEvent.setup();
    const originalError = console.error;
    console.error = () => {};
    api.usersAPI.getFollowing.mockResolvedValueOnce({ data: [makeFollowedUser()] });
    api.usersAPI.unfollowUser.mockRejectedValueOnce(new Error('Network error'));

    renderFollowing();
    await screen.findByText('Mike Chen');

    await user.click(screen.getByRole('button', { name: 'Unfollow' }));

    await waitFor(() => {
      expect(window.alert).toHaveBeenCalledWith('Failed to unfollow user');
    });
    console.error = originalError;
  });
});
