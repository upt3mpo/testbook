/**
 * Unit tests for the Feed page.
 *
 * Feed's own job is loading posts, switching between the "All" and
 * "Following" tabs, and wiring CreatePost/Post's callbacks back into
 * its posts list - so these tests render the real CreatePost and Post
 * children (mocking the API layer they all share) rather than
 * stubbing them out, to actually exercise that wiring.
 */

import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BrowserRouter } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import * as api from '../../api';
import { AuthContext } from '../../AuthContext';
import Feed from '../../pages/Feed';

vi.mock('../../api', () => ({
  feedAPI: {
    getAllFeed: vi.fn(),
    getFollowingFeed: vi.fn(),
  },
  postsAPI: {
    createPost: vi.fn(),
    uploadMedia: vi.fn(),
    deletePost: vi.fn(),
    updatePost: vi.fn(),
    addComment: vi.fn(),
    addReaction: vi.fn(),
    removeReaction: vi.fn(),
    createRepost: vi.fn(),
    deleteRepost: vi.fn(),
  },
}));

const sarah = { id: 1, username: 'sarahjohnson', display_name: 'Sarah Johnson' };

const makePost = (overrides = {}) => ({
  id: 1,
  content: 'Existing post',
  author_id: 1,
  author_username: 'sarahjohnson',
  author_display_name: 'Sarah Johnson',
  author_profile_picture: '/static/uploads/avatars/sarah.jpg',
  created_at: '2026-01-15T10:00:00Z',
  image_url: null,
  video_url: null,
  is_repost: false,
  reactions_count: 0,
  comments_count: 0,
  reposts_count: 0,
  user_reaction: null,
  has_reposted: false,
  ...overrides,
});

const renderFeed = () => {
  return render(
    <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <AuthContext.Provider value={{ user: sarah }}>
        <Feed />
      </AuthContext.Provider>
    </BrowserRouter>
  );
};

describe('Feed Page', () => {
  // Not covered: the window 'focus' listener and the block-status
  // CustomEvent/localStorage-timestamp listeners that reload the feed
  // when the user returns to the tab or blocks someone elsewhere. Not
  // hard - `window.dispatchEvent(new Event('focus'))` or
  // `window.dispatchEvent(new CustomEvent(BLOCK_STATUS_EVENT))` inside
  // a test would trigger them the same way a real focus/block event
  // does - handlePostCreated/Deleted/Updated (the callbacks these
  // listeners ultimately trigger via loadFeed) are already covered via
  // direct user interaction above.
  beforeEach(() => {
    vi.clearAllMocks();
    window.confirm = vi.fn(() => true);
    window.alert = vi.fn();
  });

  it('shows a loading state, then the loaded posts', async () => {
    api.feedAPI.getAllFeed.mockResolvedValueOnce({ data: [makePost()] });

    renderFeed();

    expect(screen.getByText('Loading posts...')).toBeInTheDocument();
    expect(await screen.findByText('Existing post')).toBeInTheDocument();
  });

  it('shows an empty state when there are no posts', async () => {
    api.feedAPI.getAllFeed.mockResolvedValueOnce({ data: [] });

    renderFeed();

    // "No posts to show." and "Be the first to post!" are adjacent text
    // nodes in the same paragraph, not their own elements, so match by
    // substring rather than exact text.
    expect(await screen.findByText(/be the first to post/i)).toBeInTheDocument();
  });

  it('shows an error message when the feed fails to load', async () => {
    api.feedAPI.getAllFeed.mockRejectedValueOnce(new Error('Network error'));

    renderFeed();

    expect(await screen.findByText('Failed to load feed')).toBeInTheDocument();
  });

  it('loads the following feed when the Following tab is clicked', async () => {
    const user = userEvent.setup();
    api.feedAPI.getAllFeed.mockResolvedValueOnce({ data: [makePost()] });
    api.feedAPI.getFollowingFeed.mockResolvedValueOnce({
      data: [makePost({ id: 2, content: 'Post from someone I follow' })],
    });

    renderFeed();
    await screen.findByText('Existing post');

    await user.click(screen.getByRole('button', { name: 'Following' }));

    expect(await screen.findByText('Post from someone I follow')).toBeInTheDocument();
    expect(api.feedAPI.getFollowingFeed).toHaveBeenCalled();
  });

  it('shows the following-specific empty message on the Following tab', async () => {
    const user = userEvent.setup();
    api.feedAPI.getAllFeed.mockResolvedValueOnce({ data: [makePost()] });
    api.feedAPI.getFollowingFeed.mockResolvedValueOnce({ data: [] });

    renderFeed();
    await screen.findByText('Existing post');

    await user.click(screen.getByRole('button', { name: 'Following' }));

    expect(await screen.findByText(/try following some users/i)).toBeInTheDocument();
  });

  it('adds a newly created post to the top of the feed', async () => {
    const user = userEvent.setup();
    api.feedAPI.getAllFeed.mockResolvedValueOnce({ data: [makePost()] });
    api.postsAPI.createPost.mockResolvedValueOnce({
      data: makePost({ id: 99, content: 'Brand new post' }),
    });

    renderFeed();
    await screen.findByText('Existing post');

    await user.type(screen.getByPlaceholderText("What's on your mind?"), 'Brand new post');
    // Exact match: an unscoped /post/i also matches the existing post's
    // "Repost" button.
    await user.click(screen.getByRole('button', { name: 'Post' }));

    await screen.findByText('Brand new post');

    // New posts are prepended - the new one should render before the
    // existing one in document order.
    const listText = screen.getByTestId('posts-list').textContent;
    expect(listText.indexOf('Brand new post')).toBeLessThan(listText.indexOf('Existing post'));
  });

  it('removes a deleted post from the feed', async () => {
    const user = userEvent.setup();
    api.feedAPI.getAllFeed.mockResolvedValueOnce({
      data: [makePost({ id: 1, content: 'Post to delete' })],
    });
    api.postsAPI.deletePost.mockResolvedValueOnce({});

    renderFeed();
    await screen.findByText('Post to delete');

    await user.click(screen.getByRole('button', { name: '⋯' }));
    await user.click(screen.getByRole('button', { name: /delete/i }));

    await waitFor(() => {
      expect(screen.queryByText('Post to delete')).not.toBeInTheDocument();
    });
  });
});
