/**
 * MSW (Mock Service Worker) handlers for component testing
 *
 * These handlers provide realistic API mocking for testing React components
 * without needing a running backend. All responses match the actual FastAPI
 * backend schema, ensuring tests accurately reflect real API behavior.
 *
 * Key Features:
 * - Network-level mocking (intercepts actual fetch/axios calls)
 * - Realistic response data matching backend schema
 * - Support for different HTTP methods and status codes
 * - Easy to override for specific test scenarios
 *
 * Usage:
 *   import { setupServer } from 'msw/node';
 *   import { handlers } from './handlers';
 *
 *   const server = setupServer(...handlers);
 *   beforeAll(() => server.listen());
 *   afterEach(() => server.resetHandlers());
 *   afterAll(() => server.close());
 *
 * Learn more: Lab 6B: Advanced Component Testing
 */

import { http, HttpResponse } from 'msw';

const API_BASE = 'http://localhost:8000/api';

export const handlers = [
  /**
   * GET /api/feed - Returns user's feed posts
   *
   * This handler mocks the feed endpoint that returns posts from users
   * the current user follows. Used for testing PostList, Feed, and
   * other components that display user feeds.
   */
  http.get(`${API_BASE}/feed`, () => {
    return HttpResponse.json([
      {
        id: 1,
        content: 'Mocked post from MSW',
        author: {
          id: 1,
          username: 'testuser',
          display_name: 'Test User',
        },
        created_at: new Date().toISOString(),
        reaction_counts: { '👍': 5, '❤️': 2 },
        is_own_post: false,
      },
      {
        id: 2,
        content: 'Another mocked post',
        author: {
          id: 2,
          username: 'anotheruser',
          display_name: 'Another User',
        },
        created_at: new Date().toISOString(),
        reaction_counts: {},
        is_own_post: false,
      },
    ]);
  }),

  /**
   * POST /api/posts/ - Create a new post
   *
   * This handler mocks post creation, simulating the backend's response
   * when a user creates a new post. Used for testing CreatePost component
   * and post creation workflows.
   *
   * Request body: { content: string, image_url?: string, video_url?: string }
   * Response: Post object with generated ID and author info
   */
  http.post(`${API_BASE}/posts/`, async ({ request }) => {
    const body = await request.json();

    return HttpResponse.json({
      id: Date.now(), // Simulate auto-generated ID
      content: body.content,
      author: {
        id: 1,
        username: 'testuser',
        display_name: 'Test User',
      },
      created_at: new Date().toISOString(),
      reaction_counts: {},
      is_own_post: true,
    });
  }),

  // GET /api/notifications - Returns notifications
  http.get(`${API_BASE}/notifications`, () => {
    return HttpResponse.json([
      {
        id: 1,
        message: 'New follower',
        type: 'follow',
        read: false,
        created_at: new Date().toISOString(),
      },
      {
        id: 2,
        message: 'Someone liked your post',
        type: 'like',
        read: true,
        created_at: new Date().toISOString(),
      },
    ]);
  }),

  // GET /api/auth/me - Get current user
  http.get(`${API_BASE}/auth/me`, ({ request }) => {
    const authHeader = request.headers.get('Authorization');

    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return HttpResponse.json({ detail: 'Not authenticated' }, { status: 401 });
    }

    return HttpResponse.json({
      id: 1,
      email: 'test@testbook.com',
      username: 'testuser',
      display_name: 'Test User',
      bio: 'Test user bio',
    });
  }),

  // GET /api/users/:username - Get user profile
  http.get(`${API_BASE}/users/:username`, ({ params }) => {
    const { username } = params;

    return HttpResponse.json({
      id: 1,
      username,
      display_name: 'Test User',
      bio: 'Test bio',
      follower_count: 10,
      following_count: 5,
      is_following: false,
      is_blocked: false,
    });
  }),

  // Error simulation endpoint
  http.get(`${API_BASE}/error`, () => {
    return HttpResponse.json({ detail: 'Internal server error' }, { status: 500 });
  }),
];
