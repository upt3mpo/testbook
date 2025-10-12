import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import * as api from '../../api';
import { AuthContext } from '../../AuthContext';
import CreatePost from '../CreatePost';

// Mock the API
vi.mock('../../api', () => ({
  postsAPI: {
    createPost: vi.fn(),
    uploadMedia: vi.fn(),
  },
}));

const renderCreatePost = (props = {}) => {
  const mockAuth = {
    user: { id: 1, username: 'testuser', display_name: 'Test User' },
    login: vi.fn(),
    logout: vi.fn(),
  };

  const defaultProps = {
    onPostCreated: vi.fn(),
  };

  return render(
    <BrowserRouter>
      <AuthContext.Provider value={mockAuth}>
        <CreatePost {...defaultProps} {...props} />
      </AuthContext.Provider>
    </BrowserRouter>
  );
};

describe('CreatePost Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders the textarea input', () => {
    renderCreatePost();
    expect(screen.getByPlaceholderText("What's on your mind?")).toBeInTheDocument();
  });

  it('renders the Post button', () => {
    renderCreatePost();
    expect(screen.getByRole('button', { name: /post/i })).toBeInTheDocument();
  });

  it('allows user to type in the textarea', () => {
    renderCreatePost();
    const textarea = screen.getByPlaceholderText("What's on your mind?");

    fireEvent.change(textarea, { target: { value: 'Test post content' } });

    expect(textarea.value).toBe('Test post content');
  });

  it('disables Post button when textarea is empty', () => {
    renderCreatePost();
    const postButton = screen.getByRole('button', { name: /post/i });

    expect(postButton).toBeDisabled();
  });

  it('enables Post button when textarea has content', () => {
    renderCreatePost();
    const textarea = screen.getByPlaceholderText("What's on your mind?");
    const postButton = screen.getByRole('button', { name: /post/i });

    fireEvent.change(textarea, { target: { value: 'Test post' } });

    expect(postButton).not.toBeDisabled();
  });

  it('calls onPostCreated when post is submitted successfully', async () => {
    const mockOnPostCreated = vi.fn();
    const mockPost = { id: 1, content: 'Test post', author_id: 1 };

    api.postsAPI.createPost.mockResolvedValueOnce({ data: mockPost });

    renderCreatePost({ onPostCreated: mockOnPostCreated });

    const textarea = screen.getByPlaceholderText("What's on your mind?");
    const postButton = screen.getByRole('button', { name: /post/i });

    fireEvent.change(textarea, { target: { value: 'Test post' } });
    fireEvent.click(postButton);

    await waitFor(() => {
      expect(api.postsAPI.createPost).toHaveBeenCalledWith({
        content: 'Test post',
        image_url: null,
        video_url: null
      });
      expect(mockOnPostCreated).toHaveBeenCalledWith(mockPost);
    });
  });

  it('clears textarea after successful post submission', async () => {
    api.postsAPI.createPost.mockResolvedValueOnce({ data: { id: 1, content: 'Test' } });

    renderCreatePost();

    const textarea = screen.getByPlaceholderText("What's on your mind?");

    fireEvent.change(textarea, { target: { value: 'Test post' } });
    fireEvent.click(screen.getByRole('button', { name: /post/i }));

    await waitFor(() => {
      expect(textarea.value).toBe('');
    });
  });

  it('handles API errors gracefully', async () => {
    api.postsAPI.createPost.mockRejectedValueOnce(new Error('API Error'));

    renderCreatePost();

    const textarea = screen.getByPlaceholderText("What's on your mind?");

    fireEvent.change(textarea, { target: { value: 'Test post' } });
    fireEvent.click(screen.getByRole('button', { name: /post/i }));

    await waitFor(() => {
      expect(screen.getByText('Failed to create post')).toBeInTheDocument();
    });
  });
});

