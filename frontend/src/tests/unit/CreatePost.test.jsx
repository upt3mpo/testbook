import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import * as api from '../../api';
import { AuthContext } from '../../AuthContext';
import CreatePost from '../../components/CreatePost';

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
    <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
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
    // Arrange - Set up mocks and test data
    const mockOnPostCreated = vi.fn();
    const mockPost = { id: 1, content: 'Test post', author_id: 1 };
    api.postsAPI.createPost.mockResolvedValueOnce({ data: mockPost });

    renderCreatePost({ onPostCreated: mockOnPostCreated });

    const textarea = screen.getByPlaceholderText("What's on your mind?");
    const postButton = screen.getByRole('button', { name: /post/i });

    // Act - User types and submits post
    fireEvent.change(textarea, { target: { value: 'Test post' } });
    fireEvent.click(postButton);

    // Assert - Verify API called and callback triggered
    await waitFor(() => {
      expect(api.postsAPI.createPost).toHaveBeenCalledWith({
        content: 'Test post',
        image_url: null, // Optional fields sent as null
        video_url: null,
      });
      expect(mockOnPostCreated).toHaveBeenCalledWith(mockPost); // Parent notified
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
    // Suppress expected error output in test logs
    const originalError = console.error;
    console.error = () => {};

    // Arrange - Mock API to return error
    api.postsAPI.createPost.mockRejectedValueOnce(new Error('API Error'));
    renderCreatePost();

    const textarea = screen.getByPlaceholderText("What's on your mind?");

    // Act - User submits post but API fails
    fireEvent.change(textarea, { target: { value: 'Test post' } });
    fireEvent.click(screen.getByRole('button', { name: /post/i }));

    // Assert - Error message displayed to user
    await waitFor(() => {
      expect(screen.getByText('Failed to create post')).toBeInTheDocument();
    });

    // Restore console.error
    console.error = originalError;
  });
});

// 🧠 Why These Tests Matter:
//
// Frontend component tests are CRITICAL for React applications because:
//
// 1. **User Interface Validation** - Components are what users interact with
// 2. **State Management** - Tests verify React state updates correctly (button enable/disable)
// 3. **API Integration** - Tests ensure components call backend APIs correctly
// 4. **Error Handling** - Users should see helpful messages, not broken UIs
//
// What These Tests Catch:
// - ✅ Broken user interactions (buttons don't respond)
// - ✅ State management bugs (button stays disabled)
// - ✅ API contract mismatches (wrong payload structure)
// - ✅ Missing error handling (app crashes on API failure)
// - ✅ Accessibility issues (missing aria labels, button roles)
//
// In Real QA Teams:
// - Component tests run on every PR before code review
// - They prevent UI regressions during refactoring
// - They serve as documentation for component behavior
// - They enable confident React development (change code, tests verify nothing broke)
//
// For Your Career:
// - React component testing is required for frontend QA roles
// - Shows you understand React hooks, state, and lifecycle
// - Demonstrates modern testing tools (Vitest, Testing Library, user-event)
// - Interview question: "How do you test React components?" - Point to these!
// - Proves you can test user interactions, not just implementation details
