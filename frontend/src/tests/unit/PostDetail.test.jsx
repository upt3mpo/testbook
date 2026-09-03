/**
 * Unit tests for the PostDetail page.
 */

import { render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import * as api from '../../api';
import { AuthContext } from '../../AuthContext';
import PostDetail from '../../pages/PostDetail';

const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  };
});

vi.mock('../../api', () => ({
  postsAPI: {
    getPost: vi.fn(),
    deletePost: vi.fn(),
  },
}));

const sarah = { id: 1, username: 'sarahjohnson', display_name: 'Sarah Johnson' };

const basePost = {
  id: 9,
  content: 'A detailed post',
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
  comments: [],
  reactions: [],
};

const renderPostDetail = (postId = '9') => {
  return render(
    <MemoryRouter initialEntries={[`/post/${postId}`]}>
      <AuthContext.Provider value={{ user: sarah }}>
        <Routes>
          <Route path="/post/:postId" element={<PostDetail />} />
        </Routes>
      </AuthContext.Provider>
    </MemoryRouter>
  );
};

describe('PostDetail Page', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    window.confirm = vi.fn(() => true);
  });

  it('renders the post via the real Post component', async () => {
    api.postsAPI.getPost.mockResolvedValueOnce({ data: basePost });

    renderPostDetail();

    expect(await screen.findByText('A detailed post')).toBeInTheDocument();
  });

  it('shows an error message when the post fails to load', async () => {
    api.postsAPI.getPost.mockRejectedValueOnce(new Error('Not found'));

    renderPostDetail();

    expect(await screen.findByText('Failed to load post')).toBeInTheDocument();
  });

  it('shows "no comments" when the post has none', async () => {
    api.postsAPI.getPost.mockResolvedValueOnce({ data: basePost });

    renderPostDetail();

    expect(await screen.findByText('No comments yet. Be the first to comment!')).toBeInTheDocument();
  });

  it('lists comments when the post has them', async () => {
    api.postsAPI.getPost.mockResolvedValueOnce({
      data: {
        ...basePost,
        comments: [
          {
            id: 1,
            content: 'Nice post!',
            author_username: 'mikechen',
            author_display_name: 'Mike Chen',
            author_profile_picture: '',
            created_at: '2026-01-15T11:00:00Z',
          },
        ],
      },
    });

    renderPostDetail();

    expect(await screen.findByText('Nice post!')).toBeInTheDocument();
    expect(screen.getByText('Mike Chen')).toBeInTheDocument();
  });

  it('shows "no reactions" when the post has none', async () => {
    api.postsAPI.getPost.mockResolvedValueOnce({ data: basePost });

    renderPostDetail();

    expect(await screen.findByText('No reactions yet.')).toBeInTheDocument();
  });

  it('lists reactions with the display name and emoji for the reaction type', async () => {
    api.postsAPI.getPost.mockResolvedValueOnce({
      data: {
        ...basePost,
        reactions: [
          { id: 1, reaction_type: 'love', username: 'mikechen', display_name: 'Mike Chen' },
        ],
      },
    });

    renderPostDetail();

    expect(await screen.findByText('Mike Chen')).toBeInTheDocument();
    // Post's own reaction dropdown also renders a ❤️ option, so scope
    // to the reactions summary list specifically.
    expect(within(screen.getByTestId('reactions-list')).getByText('❤️')).toBeInTheDocument();
  });

  it('navigates back to the feed after deleting the post', async () => {
    const user = userEvent.setup();
    api.postsAPI.getPost.mockResolvedValueOnce({ data: basePost });
    api.postsAPI.deletePost.mockResolvedValueOnce({});

    renderPostDetail();
    await screen.findByText('A detailed post');

    await user.click(screen.getByRole('button', { name: '⋯' }));
    await user.click(screen.getByRole('button', { name: /delete/i }));

    await waitFor(() => expect(mockNavigate).toHaveBeenCalledWith('/'));
  });
});
