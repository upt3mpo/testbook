/**
 * Unit tests for the Followers page.
 */

import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import * as api from '../../api';
import { AuthContext } from '../../AuthContext';
import Followers from '../../pages/Followers';

vi.mock('../../api', () => ({
  usersAPI: {
    getFollowers: vi.fn(),
    blockUser: vi.fn(),
    unblockUser: vi.fn(),
  },
}));

const sarah = { id: 1, username: 'sarahjohnson', display_name: 'Sarah Johnson' };

const makeFollower = (overrides = {}) => ({
  id: 2,
  username: 'mikechen',
  display_name: 'Mike Chen',
  bio: 'Photographer',
  profile_picture: '/static/uploads/avatars/mike.jpg',
  is_blocked: false,
  ...overrides,
});

const renderFollowers = (username = 'sarahjohnson', currentUser = sarah) => {
  return render(
    <MemoryRouter initialEntries={[`/profile/${username}/followers`]}>
      <AuthContext.Provider value={{ user: currentUser }}>
        <Routes>
          <Route path="/profile/:username/followers" element={<Followers />} />
        </Routes>
      </AuthContext.Provider>
    </MemoryRouter>
  );
};

describe('Followers Page', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('shows "Your Followers" on your own followers page', async () => {
    api.usersAPI.getFollowers.mockResolvedValueOnce({ data: [] });

    renderFollowers('sarahjohnson');

    expect(await screen.findByText('Your Followers')).toBeInTheDocument();
  });

  it("shows the owner's name on someone else's followers page", async () => {
    api.usersAPI.getFollowers.mockResolvedValueOnce({ data: [] });

    renderFollowers('mikechen');

    expect(await screen.findByText("mikechen's Followers")).toBeInTheDocument();
  });

  it('shows an error message when followers fail to load', async () => {
    api.usersAPI.getFollowers.mockRejectedValueOnce(new Error('Network error'));

    renderFollowers();

    expect(await screen.findByText('Failed to load followers')).toBeInTheDocument();
  });

  it('shows an empty message when there are no followers', async () => {
    api.usersAPI.getFollowers.mockResolvedValueOnce({ data: [] });

    renderFollowers();

    expect(await screen.findByText('No followers yet.')).toBeInTheDocument();
  });

  it('lists followers with their name and bio', async () => {
    api.usersAPI.getFollowers.mockResolvedValueOnce({ data: [makeFollower()] });

    renderFollowers();

    expect(await screen.findByText('Mike Chen')).toBeInTheDocument();
    expect(screen.getByText('@mikechen')).toBeInTheDocument();
    expect(screen.getByText('Photographer')).toBeInTheDocument();
  });

  it('does not show block controls on another user’s followers page', async () => {
    api.usersAPI.getFollowers.mockResolvedValueOnce({ data: [makeFollower()] });

    renderFollowers('mikechen');

    await screen.findByText('Mike Chen');
    expect(screen.queryByRole('button', { name: /block/i })).not.toBeInTheDocument();
  });

  it('blocks a follower from your own followers page', async () => {
    const user = userEvent.setup();
    api.usersAPI.getFollowers.mockResolvedValueOnce({ data: [makeFollower()] });
    api.usersAPI.blockUser.mockResolvedValueOnce({});
    api.usersAPI.getFollowers.mockResolvedValueOnce({
      data: [makeFollower({ is_blocked: true })],
    });

    renderFollowers();
    await screen.findByText('Mike Chen');

    await user.click(screen.getByRole('button', { name: 'Block' }));

    await waitFor(() => {
      expect(api.usersAPI.blockUser).toHaveBeenCalledWith('mikechen');
    });
    expect(await screen.findByRole('button', { name: 'Unblock' })).toBeInTheDocument();
  });

  it('unblocks an already-blocked follower', async () => {
    const user = userEvent.setup();
    api.usersAPI.getFollowers.mockResolvedValueOnce({
      data: [makeFollower({ is_blocked: true })],
    });
    api.usersAPI.unblockUser.mockResolvedValueOnce({});
    api.usersAPI.getFollowers.mockResolvedValueOnce({ data: [makeFollower()] });

    renderFollowers();
    await screen.findByText('Mike Chen');

    await user.click(screen.getByRole('button', { name: 'Unblock' }));

    await waitFor(() => {
      expect(api.usersAPI.unblockUser).toHaveBeenCalledWith('mikechen');
    });
    expect(await screen.findByRole('button', { name: 'Block' })).toBeInTheDocument();
  });
});
