/**
 * MSW server setup for Node.js tests
 *
 * This configures the Mock Service Worker for use in Vitest tests.
 * The server intercepts network requests and returns mocked responses.
 *
 * Learn more in Lab 6B: Advanced Component Testing
 */

import { setupServer } from 'msw/node';
import { handlers } from './handlers';

// Setup server with default handlers
export const server = setupServer(...handlers);
