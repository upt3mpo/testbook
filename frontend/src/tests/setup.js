import * as matchers from '@testing-library/jest-dom/matchers';
import { cleanup } from '@testing-library/react';
import { afterAll, afterEach, beforeAll, expect, vi } from 'vitest';
import { server } from './mocks/server';

// Extend Vitest's expect with jest-dom matchers
expect.extend(matchers);

// Display welcome banner
console.log(`
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║  ⚡ Welcome to Testbook Frontend Testing!                        ║
║                                                                  ║
║  ▶ Running 30+ component, integration & accessibility tests      ║
║  ▶ JavaScript Vitest | React Testing Library | MSW               ║
║                                                                  ║
║  💡 Tip: Use --watch for live reload, --ui for visual runner     ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
`);

// MSW Setup
beforeAll(() => server.listen({ onUnhandledRequest: 'warn' }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

// Cleanup after each test
afterEach(() => {
  cleanup();
});

// Mock window.matchMedia (for responsive components)
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation((query) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});

// Mock window.alert and window.confirm (used in some components)
global.alert = vi.fn();
global.confirm = vi.fn(() => true);
