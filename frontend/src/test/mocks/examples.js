/**
 * Example MSW handler patterns from Lab 6B
 *
 * These examples demonstrate common mocking scenarios for component testing.
 * Copy and adapt these patterns for your own tests.
 */

import { rest } from 'msw';

const API_BASE = 'http://localhost:8000/api';

/**
 * Example 1: Mock with delay (test loading states)
 */
export const slowResponseHandler = rest.get(`${API_BASE}/feed`, async (req, res, ctx) => {
  // Add 2 second delay
  await ctx.delay(2000);

  return res(
    ctx.status(200),
    ctx.json([
      { id: 1, content: 'Slow loading post', author: { id: 1, username: 'test', display_name: 'Test' } }
    ])
  );
});

/**
 * Example 2: Mock error responses
 */
export const errorHandler = rest.get(`${API_BASE}/feed`, (req, res, ctx) => {
  return res(
    ctx.status(500),
    ctx.json({ detail: 'Internal server error' })
  );
});

/**
 * Example 3: Mock empty state
 */
export const emptyFeedHandler = rest.get(`${API_BASE}/feed`, (req, res, ctx) => {
  return res(
    ctx.status(200),
    ctx.json([])
  );
});

/**
 * Example 4: Mock authentication check
 */
export const requiresAuthHandler = rest.get(`${API_BASE}/feed`, (req, res, ctx) => {
  const authHeader = req.headers.get('Authorization');

  if (!authHeader) {
    return res(
      ctx.status(401),
      ctx.json({ detail: 'Not authenticated' })
    );
  }

  return res(ctx.status(200), ctx.json([]));
});

/**
 * Example 5: Mock pagination
 */
export const paginatedHandler = rest.get(`${API_BASE}/posts`, (req, res, ctx) => {
  const page = req.url.searchParams.get('page') || '1';
  const limit = req.url.searchParams.get('limit') || '10';

  // Generate mock paginated data
  const posts = Array.from({ length: parseInt(limit) }, (_, i) => ({
    id: parseInt(page) * 100 + i,
    content: `Post ${i + 1} on page ${page}`,
    author: { id: 1, username: 'test', display_name: 'Test User' }
  }));

  return res(
    ctx.status(200),
    ctx.json({
      items: posts,
      total: 100,
      page: parseInt(page),
      pages: 10
    })
  );
});

/**
 * Usage in tests:
 *
 * import { server } from '../test/mocks/server';
 * import { errorHandler, emptyFeedHandler } from '../test/mocks/examples';
 *
 * test('handles empty feed', async () => {
 *   server.use(emptyFeedHandler);
 *   // Your test code...
 * });
 */

