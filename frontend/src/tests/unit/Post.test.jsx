/**
 * Unit tests for the Post component.
 *
 * Post is the most complex component in the app: it owns its own menu,
 * edit form, reaction dropdown, comment form, and repost toggle, and
 * calls postsAPI directly for each of those actions. These tests mock
 * postsAPI and check the same things a user would see - not the
 * component's internal state.
 */

import { render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BrowserRouter } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import * as api from '../../api';
import { AuthContext } from '../../AuthContext';
import Post from '../../components/Post';

vi.mock('../../api', () => ({
  postsAPI: {
    updatePost: vi.fn(),
    deletePost: vi.fn(),
    addComment: vi.fn(),
    addReaction: vi.fn(),
    removeReaction: vi.fn(),
    createRepost: vi.fn(),
    deleteRepost: vi.fn(),
  },
}));

const sarah = { id: 1, username: 'sarahjohnson', display_name: 'Sarah Johnson' };

const basePost = {
  id: 7,
  content: 'Hello Testbook!',
  author_id: 1,
  author_username: 'sarahjohnson',
  author_display_name: 'Sarah Johnson',
  author_profile_picture: '/static/uploads/avatars/sarah.jpg',
  created_at: '2026-01-15T10:00:00Z',
  image_url: null,
  video_url: null,
  is_repost: false,
  original_post_id: null,
  original_post: null,
  reactions_count: 0,
  comments_count: 0,
  reposts_count: 0,
  user_reaction: null,
  has_reposted: false,
};

const renderPost = (post, { currentUser = sarah, ...props } = {}) => {
  return render(
    <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <AuthContext.Provider value={{ user: currentUser }}>
        <Post post={post} onDelete={vi.fn()} onUpdate={vi.fn()} {...props} />
      </AuthContext.Provider>
    </BrowserRouter>
  );
};

describe('Post Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    window.confirm = vi.fn(() => true);
    window.alert = vi.fn();
  });

  it("displays the post's content and author", () => {
    renderPost(basePost);

    expect(screen.getByText('Hello Testbook!')).toBeInTheDocument();
    expect(screen.getByText('Sarah Johnson')).toBeInTheDocument();
    expect(screen.getByText('@sarahjohnson')).toBeInTheDocument();
  });

  it('displays reaction, comment, and repost counts', () => {
    renderPost({ ...basePost, reactions_count: 3, comments_count: 2, reposts_count: 1 });

    expect(screen.getByText('3 reactions')).toBeInTheDocument();
    expect(screen.getByText('2 comments')).toBeInTheDocument();
    expect(screen.getByText('1 reposts')).toBeInTheDocument();
  });

  it('shows a repost indicator when the post is a repost', () => {
    renderPost({ ...basePost, is_repost: true });
    expect(screen.getByText(/reposted$/)).toBeInTheDocument();
  });

  it('shows the menu button on your own post', () => {
    renderPost(basePost, { currentUser: sarah });
    expect(screen.getByRole('button', { name: '⋯' })).toBeInTheDocument();
  });

  it("does not show the menu button on another user's post", () => {
    renderPost(basePost, { currentUser: { id: 999, username: 'mikechen' } });
    expect(screen.queryByRole('button', { name: '⋯' })).not.toBeInTheDocument();
  });

  it('does not show a "View" link when rendered in detailed mode', () => {
    renderPost(basePost, { detailed: true });
    expect(screen.queryByRole('link', { name: 'View' })).not.toBeInTheDocument();
  });

  it('shows a "View" link to the post when not in detailed mode', () => {
    renderPost(basePost, { detailed: false });
    expect(screen.getByRole('link', { name: 'View' })).toHaveAttribute('href', '/post/7');
  });

  describe('Editing', () => {
    it('opens the edit form with the current content prefilled', async () => {
      const user = userEvent.setup();
      renderPost(basePost);

      await user.click(screen.getByRole('button', { name: '⋯' }));
      await user.click(screen.getByRole('button', { name: /edit/i }));

      expect(screen.getByDisplayValue('Hello Testbook!')).toBeInTheDocument();
    });

    it('discards changes when Cancel is clicked', async () => {
      const user = userEvent.setup();
      renderPost(basePost);

      await user.click(screen.getByRole('button', { name: '⋯' }));
      await user.click(screen.getByRole('button', { name: /edit/i }));
      await user.clear(screen.getByDisplayValue('Hello Testbook!'));
      await user.type(screen.getByRole('textbox'), 'Changed my mind');
      await user.click(screen.getByRole('button', { name: /cancel/i }));

      expect(screen.getByText('Hello Testbook!')).toBeInTheDocument();
      expect(api.postsAPI.updatePost).not.toHaveBeenCalled();
    });

    it('saves edited content via the API', async () => {
      const user = userEvent.setup();
      const onUpdate = vi.fn();
      api.postsAPI.updatePost.mockResolvedValueOnce({
        data: { ...basePost, content: 'Edited content' },
      });
      renderPost(basePost, { onUpdate });

      await user.click(screen.getByRole('button', { name: '⋯' }));
      await user.click(screen.getByRole('button', { name: /edit/i }));
      await user.clear(screen.getByDisplayValue('Hello Testbook!'));
      await user.type(screen.getByRole('textbox'), 'Edited content');
      await user.click(screen.getByRole('button', { name: /save/i }));

      await waitFor(() => {
        expect(api.postsAPI.updatePost).toHaveBeenCalledWith(7, {
          content: 'Edited content',
          image_url: null,
          video_url: null,
        });
      });
      expect(onUpdate).toHaveBeenCalledWith({ ...basePost, content: 'Edited content' });
    });

    it('rejects saving empty content without calling the API', async () => {
      const user = userEvent.setup();
      renderPost(basePost);

      await user.click(screen.getByRole('button', { name: '⋯' }));
      await user.click(screen.getByRole('button', { name: /edit/i }));
      await user.clear(screen.getByDisplayValue('Hello Testbook!'));
      await user.click(screen.getByRole('button', { name: /save/i }));

      expect(window.alert).toHaveBeenCalledWith('Post content cannot be empty');
      expect(api.postsAPI.updatePost).not.toHaveBeenCalled();
    });
  });

  describe('Deleting', () => {
    it('deletes the post after the user confirms', async () => {
      const user = userEvent.setup();
      const onDelete = vi.fn();
      api.postsAPI.deletePost.mockResolvedValueOnce({});
      renderPost(basePost, { onDelete });

      await user.click(screen.getByRole('button', { name: '⋯' }));
      await user.click(screen.getByRole('button', { name: /delete/i }));

      await waitFor(() => expect(onDelete).toHaveBeenCalledWith(7));
      expect(api.postsAPI.deletePost).toHaveBeenCalledWith(7);
    });

    it('does not delete the post if the user cancels the confirmation', async () => {
      const user = userEvent.setup();
      window.confirm = vi.fn(() => false);
      renderPost(basePost);

      await user.click(screen.getByRole('button', { name: '⋯' }));
      await user.click(screen.getByRole('button', { name: /delete/i }));

      expect(api.postsAPI.deletePost).not.toHaveBeenCalled();
    });
  });

  describe('Reactions', () => {
    it('adds a reaction when a reaction emoji is clicked', async () => {
      const user = userEvent.setup();
      const onUpdate = vi.fn();
      api.postsAPI.addReaction.mockResolvedValueOnce({
        data: { ...basePost, user_reaction: 'like', reactions_count: 1 },
      });
      renderPost(basePost, { onUpdate });

      await user.click(screen.getByRole('button', { name: /react/i }));
      // Reaction options are only identifiable by their `title` attribute -
      // their accessible name/text is just the emoji, which every other
      // reaction button also has some form of.
      await user.click(screen.getByTitle('like'));

      await waitFor(() => {
        expect(api.postsAPI.addReaction).toHaveBeenCalledWith(7, 'like');
      });
      expect(onUpdate).toHaveBeenCalledWith({
        ...basePost,
        user_reaction: 'like',
        reactions_count: 1,
      });
    });

    it('removes the reaction when the active reaction is clicked again', async () => {
      const user = userEvent.setup();
      api.postsAPI.removeReaction.mockResolvedValueOnce({
        data: { ...basePost, user_reaction: null },
      });
      renderPost({ ...basePost, user_reaction: 'like' });

      // The toggle button reads "👍 ▼" - distinct from the reaction
      // option below, which shows only the bare emoji.
      const reactButton = screen.getByRole('button', { name: '👍 ▼' });

      await user.click(reactButton);
      await user.click(screen.getByTitle('like'));

      await waitFor(() => {
        expect(api.postsAPI.removeReaction).toHaveBeenCalledWith(7);
      });
    });
  });

  describe('Comments', () => {
    it('reveals a comment form when the Comment button is clicked', async () => {
      const user = userEvent.setup();
      renderPost(basePost);

      expect(
        screen.queryByPlaceholderText('Write a comment...')
      ).not.toBeInTheDocument();

      await user.click(screen.getByRole('button', { name: 'Comment' }));

      expect(screen.getByPlaceholderText('Write a comment...')).toBeInTheDocument();
    });

    it('submits a comment and clears the form', async () => {
      const user = userEvent.setup();
      const onUpdate = vi.fn();
      api.postsAPI.addComment.mockResolvedValueOnce({ data: { id: 1, content: 'Nice!' } });
      renderPost(basePost, { onUpdate });

      await user.click(screen.getByRole('button', { name: 'Comment' }));
      const commentForm = screen.getByPlaceholderText('Write a comment...').closest('form');
      await user.type(within(commentForm).getByPlaceholderText('Write a comment...'), 'Nice!');
      // Scoped to the comment form: an unscoped /post/i also matches the
      // "Repost" button.
      await user.click(within(commentForm).getByRole('button', { name: 'Post' }));

      await waitFor(() => {
        expect(api.postsAPI.addComment).toHaveBeenCalledWith(7, 'Nice!');
      });
      expect(onUpdate).toHaveBeenCalledWith({ ...basePost, comments_count: 1 });
      expect(screen.queryByPlaceholderText('Write a comment...')).not.toBeInTheDocument();
    });

    it('does not submit an empty comment', async () => {
      const user = userEvent.setup();
      renderPost(basePost);

      await user.click(screen.getByRole('button', { name: 'Comment' }));
      const submitButton = within(
        screen.getByPlaceholderText('Write a comment...').closest('form')
      ).getByRole('button');

      expect(submitButton).toBeDisabled();
      expect(api.postsAPI.addComment).not.toHaveBeenCalled();
    });
  });

  describe('Reposting', () => {
    it('creates a repost when not already reposted', async () => {
      const user = userEvent.setup();
      api.postsAPI.createRepost.mockResolvedValueOnce({});
      renderPost(basePost);

      await user.click(screen.getByRole('button', { name: 'Repost' }));

      await waitFor(() => {
        expect(api.postsAPI.createRepost).toHaveBeenCalledWith({
          original_post_id: 7,
          content: '',
        });
      });
    });

    it('removes the repost when already reposted', async () => {
      const user = userEvent.setup();
      api.postsAPI.deleteRepost.mockResolvedValueOnce({});
      renderPost({ ...basePost, has_reposted: true });

      await user.click(screen.getByRole('button', { name: /reposted/i }));

      await waitFor(() => {
        expect(api.postsAPI.deleteRepost).toHaveBeenCalledWith(7);
      });
    });
  });
});
