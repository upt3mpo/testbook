/**
 * MSW (Mock Service Worker) handlers for component testing
 *
 * These handlers provide realistic API mocking for testing components
 * without needing a running backend. Responses match the actual FastAPI
 * backend schema.
 *
 * Learn more in Lab 6B: Advanced Component Testing
 */

import { rest } from 'msw';

const API_BASE = 'http://localhost:8000/api';

export const handlers = [
  // GET /api/feed - Returns feed posts
  rest.get(`${API_BASE}/feed`, (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json([
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
      ])
    );
  }),

  // POST /api/posts/ - Create a post
  rest.post(`${API_BASE}/posts/`, async (req, res, ctx) => {
    const body = await req.json();

    return res(
      ctx.status(200),
      ctx.json({
        id: Date.now(),
        content: body.content,
        author: {
          id: 1,
          username: 'testuser',
          display_name: 'Test User',
        },
        created_at: new Date().toISOString(),
        reaction_counts: {},
        is_own_post: true,
      })
    );
  }),

  // GET /api/notifications - Returns notifications
  rest.get(`${API_BASE}/notifications`, (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json([
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
      ])
    );
  }),

  // GET /api/auth/me - Get current user
  rest.get(`${API_BASE}/auth/me`, (req, res, ctx) => {
    const authHeader = req.headers.get('Authorization');

    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res(
        ctx.status(401),
        ctx.json({ detail: 'Not authenticated' })
      );
    }

    return res(
      ctx.status(200),
      ctx.json({
        id: 1,
        email: 'test@testbook.com',
        username: 'testuser',
        display_name: 'Test User',
        bio: 'Test user bio',
      })
    );
  }),

  // GET /api/users/:username - Get user profile
  rest.get(`${API_BASE}/users/:username`, (req, res, ctx) => {
    const { username } = req.params;

    return res(
      ctx.status(200),
      ctx.json({
        id: 1,
        username,
        display_name: 'Test User',
        bio: 'Test bio',
        follower_count: 10,
        following_count: 5,
        is_following: false,
        is_blocked: false,
      })
    );
  }),

  // Error simulation endpoint
  rest.get(`${API_BASE}/error`, (req, res, ctx) => {
    return res(
      ctx.status(500),
      ctx.json({ detail: 'Internal server error' })
    );
  }),
];

