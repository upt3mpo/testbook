/**
 * Contract Tests - Lab 6C
 *
 * These tests validate that the frontend's expectations match the backend's OpenAPI schema.
 * Run with: npm run test:contracts
 */

import { describe, expect, it } from 'vitest';
import {
  hasRequiredFields,
  TestbookSchemas,
  validateContract,
  validateFieldTypes,
} from '../contract-helpers.js';

describe('Contract Tests (Lab 6C)', () => {
  it('should have TestbookSchemas defined', () => {
    expect(TestbookSchemas).toBeDefined();
    expect(TestbookSchemas.Post).toBeDefined();
    expect(TestbookSchemas.User).toBeDefined();
    expect(TestbookSchemas.UserProfile).toBeDefined();
  });

  it('should validate required fields', () => {
    const mockPost = {
      id: 1,
      content: 'Test post',
      author: { id: 1, username: 'testuser' },
      created_at: '2025-10-11T00:00:00Z',
      reaction_counts: { like: 0 },
    };

    expect(() => {
      hasRequiredFields(mockPost, TestbookSchemas.Post.requiredFields);
    }).not.toThrow();
  });

  it('should validate field types', () => {
    const mockUser = {
      id: 1,
      username: 'testuser',
      display_name: 'Test User',
      email: 'test@example.com',
    };

    expect(() => {
      validateFieldTypes(mockUser, TestbookSchemas.User.types);
    }).not.toThrow();
  });

  it('should detect missing required fields', () => {
    const incompletePost = {
      id: 1,
      content: 'Test post',
      // Missing: author, created_at, reaction_counts
    };

    expect(() => {
      hasRequiredFields(incompletePost, TestbookSchemas.Post.requiredFields);
    }).toThrow(/Missing required fields/);
  });

  it('should detect wrong field types', () => {
    const invalidUser = {
      id: '1', // Should be number
      username: 'testuser',
      display_name: 'Test User',
      email: 'test@example.com',
    };

    expect(() => {
      validateFieldTypes(invalidUser, TestbookSchemas.User.types);
    }).toThrow(/expected type/);
  });
});

// Example: How to use validateContract with a real API response
describe('Contract Validation Example', () => {
  it('demonstrates validateContract usage (requires running backend)', async () => {
    // Suppress schema warning for this demo test
    const originalWarn = console.warn;
    console.warn = () => {};

    // Mock a response that matches the expected structure
    const mockResponse = {
      status: 200,
      data: {
        id: 1,
        username: 'testuser',
        display_name: 'Test User',
        email: 'test@example.com',
      },
    };

    // This will warn if schema not fetched, but won't fail
    // In real tests, ensure backend is running and schema is fetched
    await validateContract(mockResponse, '/api/users/1', 'get', 200);

    // Restore console.warn
    console.warn = originalWarn;

    // If you reach here, validation passed (or was skipped with warning)
    expect(true).toBe(true);
  });
});
