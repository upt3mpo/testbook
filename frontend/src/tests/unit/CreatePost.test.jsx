/**
 * CreatePost Component Tests
 *
 * This file demonstrates comprehensive React component testing using Vitest
 * and React Testing Library. It tests the CreatePost component which allows
 * users to create new posts in the social media application.
 *
 * Key Testing Concepts Demonstrated:
 * - Component rendering and user interaction testing
 * - Mocking external dependencies (API calls, context providers)
 * - Testing form submission and validation
 * - Testing loading states and error handling
 * - Testing accessibility and user experience
 *
 * This file is referenced in Stage 2 learning materials as an example
 * of professional component testing practices.
 */

import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import * as api from '../../api';
import { AuthContext } from '../../AuthContext';
import CreatePost from '../../components/CreatePost';

// Mock the API module to control its behavior in tests
// This prevents real API calls during testing and allows us to
// simulate different response scenarios (success, error, loading)
vi.mock('../../api', () => ({
  postsAPI: {
    createPost: vi.fn(), // Mock function for creating posts
    uploadMedia: vi.fn(), // Mock function for uploading media
  },
}));

/**
 * Helper function to render CreatePost component with all required providers
 *
 * This function sets up the component with:
 * - Mock authentication context (simulates logged-in user)
 * - Browser router for navigation
 * - Default props for testing
 *
 * @param {Object} props - Additional props to pass to CreatePost component
 * @returns {Object} - Render result from React Testing Library
 */
const renderCreatePost = (props = {}) => {
  // Create mock authentication context
  // This simulates a logged-in user for testing
  const mockAuth = {
    user: {
      id: 1, // User ID for testing
      username: 'testuser', // Username for testing
      display_name: 'Test User', // Display name for testing
    },
    login: vi.fn(), // Mock login function
    logout: vi.fn(), // Mock logout function
  };

  // Default props that the component expects
  const defaultProps = {
    onPostCreated: vi.fn(), // Mock callback for when post is created
  };

  // Render the component wrapped in all required providers
  return render(
    <BrowserRouter
      future={{
        v7_startTransition: true, // Enable React 18 concurrent features
        v7_relativeSplatPath: true, // Enable new routing features
      }}
    >
      <AuthContext.Provider value={mockAuth}>
        <CreatePost {...defaultProps} {...props} />
      </AuthContext.Provider>
    </BrowserRouter>
  );
};

describe('CreatePost Component', () => {
  // Clear all mocks before each test to ensure clean state
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders the textarea input', () => {
    /**
     * Test that the textarea input is rendered correctly.
     *
     * This is a basic rendering test that verifies the component
     * displays the expected form element for user input.
     */
    renderCreatePost();
    expect(screen.getByPlaceholderText("What's on your mind?")).toBeInTheDocument();
  });

  it('renders the Post button', () => {
    /**
     * Test that the Post button is rendered correctly.
     *
     * This verifies that the submit button is present and accessible
     * for users to submit their posts.
     */
    renderCreatePost();
    expect(screen.getByRole('button', { name: /post/i })).toBeInTheDocument();
  });

  it('allows user to type in the textarea', () => {
    /**
     * Test that users can type content into the textarea.
     *
     * This verifies the basic user interaction functionality
     * and ensures the input field accepts user input correctly.
     */
    renderCreatePost();
    const textarea = screen.getByPlaceholderText("What's on your mind?");

    // Simulate user typing in the textarea
    fireEvent.change(textarea, { target: { value: 'Test post content' } });

    // Verify the textarea contains the typed content
    expect(textarea.value).toBe('Test post content');
  });

  it('disables Post button when textarea is empty', () => {
    /**
     * Test that the Post button is disabled when there's no content.
     *
     * This prevents users from submitting empty posts and provides
     * visual feedback about the form's state.
     */
    renderCreatePost();
    const postButton = screen.getByRole('button', { name: /post/i });

    // Verify the button is disabled when textarea is empty
    expect(postButton).toBeDisabled();
  });

  it('enables Post button when textarea has content', () => {
    /**
     * Test that the Post button is enabled when there's content.
     *
     * This ensures users can submit posts when they have content
     * and provides proper form validation feedback.
     */
    renderCreatePost();
    const textarea = screen.getByPlaceholderText("What's on your mind?");
    const postButton = screen.getByRole('button', { name: /post/i });

    // Simulate user typing content
    fireEvent.change(textarea, { target: { value: 'Test post' } });

    // Verify the button is enabled when there's content
    expect(postButton).not.toBeDisabled();
  });

  it('calls onPostCreated when post is submitted successfully', async () => {
    /**
     * Test the complete post creation flow with successful API response.
     *
     * This test verifies the entire user journey:
     * 1. User types content in the textarea
     * 2. User clicks the submit button
     * 3. Component calls the API with correct data
     * 4. Component triggers the success callback
     *
     * This is an integration test that verifies multiple components
     * work together correctly.
     */

    // Arrange - Set up mocks and test data
    const mockOnPostCreated = vi.fn(); // Mock function to track callback calls
    const mockPost = {
      id: 1,
      content: 'Test post',
      author_id: 1,
    };

    // Mock the API to return a successful response
    api.postsAPI.createPost.mockResolvedValueOnce({ data: mockPost });

    // Render the component with our mock callback
    renderCreatePost({ onPostCreated: mockOnPostCreated });

    // Get references to the form elements
    const textarea = screen.getByPlaceholderText("What's on your mind?");
    const postButton = screen.getByRole('button', { name: /post/i });

    // Act - Simulate user interaction
    // User types content in the textarea
    fireEvent.change(textarea, { target: { value: 'Test post' } });

    // User clicks the submit button
    fireEvent.click(postButton);

    // Assert - Verify API was called correctly and callback was triggered
    await waitFor(() => {
      // Verify the API was called with the expected data structure
      expect(api.postsAPI.createPost).toHaveBeenCalledWith({
        content: 'Test post', // User's input
        image_url: null, // Optional fields sent as null
        video_url: null, // Optional fields sent as null
      });

      // Verify the success callback was called with the returned post data
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
