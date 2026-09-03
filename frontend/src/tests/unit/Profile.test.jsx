/**
 * Unit tests for the Profile page.
 */

import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Route, Routes, MemoryRouter } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import * as api from '../../api';
import { AuthContext } from '../../AuthContext';
import Profile from '../../pages/Profile';

vi.mock('../../api', () => ({
  usersAPI: {
    getProfile: vi.fn(),
    getUserPosts: vi.fn(),
    followUser: vi.fn(),
    unfollowUser: vi.fn(),
    blockUser: vi.fn(),
    unblockUser: vi.fn(),
  },
  postsAPI: {
    deletePost: vi.fn(),
  },
}));

const sarah = { id: 1, username: 'sarahjohnson', display_name: 'Sarah Johnson' };

const makeProfile = (overrides = {}) => ({
  username: 'mikechen',
  display_name: 'Mike Chen',
  bio: 'Photographer',
  profile_picture: '/static/uploads/avatars/mike.jpg',
  posts_count: 0,
  followers_count: 10,
  following_count: 5,
  is_following: false,
  is_blocked: false,
  ...overrides,
});

const renderProfile = (username = 'mikechen', currentUser = sarah) => {
  return render(
    <MemoryRouter initialEntries={[`/profile/${username}`]}>
      <AuthContext.Provider value={{ user: currentUser }}>
        <Routes>
          <Route path="/profile/:username" element={<Profile />} />
        </Routes>
      </AuthContext.Provider>
    </MemoryRouter>
  );
};

describe('Profile Page', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    window.confirm = vi.fn(() => true);
    window.alert = vi.fn();
    api.usersAPI.getUserPosts.mockResolvedValue({ data: [] });
  });

  it("displays the profile's name, username, and bio", async () => {
    api.usersAPI.getProfile.mockResolvedValueOnce({ data: makeProfile() });

    renderProfile();

    expect(await screen.findByText('Mike Chen')).toBeInTheDocument();
    expect(screen.getByText('@mikechen')).toBeInTheDocument();
    expect(screen.getByText('Photographer')).toBeInTheDocument();
  });

  it('shows an error message when the profile fails to load', async () => {
    api.usersAPI.getProfile.mockRejectedValueOnce(new Error('Not found'));

    renderProfile();

    expect(await screen.findByText('Failed to load profile')).toBeInTheDocument();
  });

  it("shows an Edit Profile button on the user's own profile", async () => {
    api.usersAPI.getProfile.mockResolvedValueOnce({
      data: makeProfile({ username: 'sarahjohnson', display_name: 'Sarah Johnson' }),
    });

    renderProfile('sarahjohnson');

    expect(await screen.findByRole('button', { name: /edit profile/i })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /^follow$/i })).not.toBeInTheDocument();
  });

  it('shows Follow and Block buttons on another user’s profile', async () => {
    api.usersAPI.getProfile.mockResolvedValueOnce({ data: makeProfile() });

    renderProfile();

    expect(await screen.findByRole('button', { name: 'Follow' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Block' })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /edit profile/i })).not.toBeInTheDocument();
  });

  it('shows the empty-posts message when the user has no posts', async () => {
    api.usersAPI.getProfile.mockResolvedValueOnce({ data: makeProfile() });

    renderProfile();

    expect(await screen.findByText('No posts yet.')).toBeInTheDocument();
  });

  it('follows the profile owner and updates the button and follower count', async () => {
    const user = userEvent.setup();
    api.usersAPI.getProfile.mockResolvedValueOnce({ data: makeProfile() });
    api.usersAPI.followUser.mockResolvedValueOnce({});

    renderProfile();

    await user.click(await screen.findByRole('button', { name: 'Follow' }));

    expect(api.usersAPI.followUser).toHaveBeenCalledWith('mikechen');
    expect(await screen.findByRole('button', { name: 'Unfollow' })).toBeInTheDocument();
    expect(screen.getByText('11')).toBeInTheDocument(); // followers_count went from 10 to 11
  });

  it('unfollows the profile owner', async () => {
    const user = userEvent.setup();
    api.usersAPI.getProfile.mockResolvedValueOnce({
      data: makeProfile({ is_following: true, followers_count: 10 }),
    });
    api.usersAPI.unfollowUser.mockResolvedValueOnce({});

    renderProfile();

    await user.click(await screen.findByRole('button', { name: 'Unfollow' }));

    expect(api.usersAPI.unfollowUser).toHaveBeenCalledWith('mikechen');
    expect(await screen.findByRole('button', { name: 'Follow' })).toBeInTheDocument();
  });

  it('blocks the profile owner after confirming', async () => {
    const user = userEvent.setup();
    api.usersAPI.getProfile.mockResolvedValueOnce({ data: makeProfile() });
    api.usersAPI.blockUser.mockResolvedValueOnce({});

    renderProfile();

    await user.click(await screen.findByRole('button', { name: 'Block' }));

    expect(window.confirm).toHaveBeenCalled();
    expect(api.usersAPI.blockUser).toHaveBeenCalledWith('mikechen');
    expect(await screen.findByRole('button', { name: 'Unblock' })).toBeInTheDocument();
  });

  it('does not block when the user cancels the confirmation', async () => {
    const user = userEvent.setup();
    window.confirm = vi.fn(() => false);
    api.usersAPI.getProfile.mockResolvedValueOnce({ data: makeProfile() });

    renderProfile();

    await user.click(await screen.findByRole('button', { name: 'Block' }));

    expect(api.usersAPI.blockUser).not.toHaveBeenCalled();
  });

  it('navigates own posts through the real Post component', async () => {
    api.usersAPI.getProfile.mockResolvedValueOnce({
      data: makeProfile({ username: 'sarahjohnson', display_name: 'Sarah Johnson' }),
    });
    api.usersAPI.getUserPosts.mockResolvedValueOnce({
      data: [
        {
          id: 5,
          content: "Sarah's post",
          author_id: 1,
          author_username: 'sarahjohnson',
          author_display_name: 'Sarah Johnson',
          author_profile_picture: '',
          created_at: '2026-01-15T10:00:00Z',
          image_url: null,
          video_url: null,
          is_repost: false,
          reactions_count: 0,
          comments_count: 0,
          reposts_count: 0,
          user_reaction: null,
          has_reposted: false,
        },
      ],
    });

    renderProfile('sarahjohnson');

    expect(await screen.findByText("Sarah's post")).toBeInTheDocument();
  });

  it('removes a post from the list when deleted via the real Post component', async () => {
    const user = userEvent.setup();
    window.confirm = vi.fn(() => true);
    api.usersAPI.getProfile.mockResolvedValueOnce({
      data: makeProfile({ username: 'sarahjohnson', display_name: 'Sarah Johnson' }),
    });
    api.usersAPI.getUserPosts.mockResolvedValueOnce({
      data: [
        {
          id: 5,
          content: 'Post to delete',
          author_id: 1,
          author_username: 'sarahjohnson',
          author_display_name: 'Sarah Johnson',
          author_profile_picture: '',
          created_at: '2026-01-15T10:00:00Z',
          image_url: null,
          video_url: null,
          is_repost: false,
          reactions_count: 0,
          comments_count: 0,
          reposts_count: 0,
          user_reaction: null,
          has_reposted: false,
        },
      ],
    });
    api.postsAPI.deletePost.mockResolvedValueOnce({});

    renderProfile('sarahjohnson');
    await screen.findByText('Post to delete');

    await user.click(screen.getByRole('button', { name: '⋯' }));
    await user.click(screen.getByRole('button', { name: /delete/i }));

    await waitFor(() => {
      expect(screen.queryByText('Post to delete')).not.toBeInTheDocument();
    });
  });
});
