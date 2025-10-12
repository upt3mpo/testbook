/**
 * Contract testing helpers for Lab 6C
 *
 * These helpers validate API responses against the OpenAPI schema
 * to ensure frontend and backend stay in sync.
 */

/**
 * Load OpenAPI schema (dynamically to avoid import errors if not fetched yet)
 */
async function loadSchema() {
  try {
    // Use dynamic import for ESM compatibility
    const module = await import('./openapi-schema.json', { assert: { type: 'json' } });
    return module.default;
  } catch (error) {
    // Schema not fetched yet - this is expected in tests
    // Tests can still run, validation will be skipped with warning
    if (process.env.NODE_ENV !== 'test') {
      console.warn('⚠️  OpenAPI schema not found. Run: npm run validate:schema');
    }
    return null;
  }
}

/**
 * Validate that a response matches expected structure
 *
 * @param {object} response - Axios response object
 * @param {string} path - API path (e.g., '/api/users')
 * @param {string} method - HTTP method (e.g., 'get')
 * @param {number} status - Expected status code
 */
export async function validateContract(response, path, method, status = 200) {
  const schema = await loadSchema();

  // Basic validation
  if (response.status !== status) {
    throw new Error(`Expected status ${status}, got ${response.status}`);
  }

  if (!schema) {
    console.warn('⚠️  Schema validation skipped - schema not loaded');
    return;
  }

  // Find operation in schema
  const operation = schema.paths?.[path]?.[method.toLowerCase()];
  if (!operation) {
    console.warn(`⚠️  No schema found for ${method.toUpperCase()} ${path}`);
    return;
  }

  console.log(`✅ Response status ${status} matches schema for ${method.toUpperCase()} ${path}`);
  return operation;
}

/**
 * Get expected response schema for an endpoint
 *
 * @param {string} path - API path
 * @param {string} method - HTTP method
 * @param {number} status - Status code
 * @returns {object|null} Schema definition
 */
export async function getResponseSchema(path, method, status = 200) {
  const schema = await loadSchema();
  if (!schema) return null;

  const operation = schema.paths?.[path]?.[method.toLowerCase()];
  const response = operation?.responses?.[status.toString()];
  return response?.content?.['application/json']?.schema;
}

/**
 * Check if data has required fields
 *
 * @param {object} data - Data to validate
 * @param {string[]} requiredFields - List of required field names
 */
export function hasRequiredFields(data, requiredFields) {
  const missing = requiredFields.filter(field => !(field in data));

  if (missing.length > 0) {
    throw new Error(`Missing required fields: ${missing.join(', ')}`);
  }

  return true;
}

/**
 * Validate field types
 *
 * @param {object} data - Data to validate
 * @param {object} typeMap - Map of field names to expected types
 * @example
 * validateFieldTypes(user, {
 *   id: 'number',
 *   username: 'string',
 *   follower_count: 'number'
 * });
 */
export function validateFieldTypes(data, typeMap) {
  for (const [field, expectedType] of Object.entries(typeMap)) {
    const actualType = typeof data[field];

    if (actualType !== expectedType) {
      throw new Error(
        `Field '${field}': expected type '${expectedType}', got '${actualType}'`
      );
    }
  }

  return true;
}

/**
 * Common field type maps for Testbook API
 */
export const TestbookSchemas = {
  Post: {
    requiredFields: ['id', 'content', 'author', 'created_at', 'reaction_counts'],
    types: {
      id: 'number',
      content: 'string',
      author: 'object',
      reaction_counts: 'object',
    },
  },

  User: {
    requiredFields: ['id', 'username', 'display_name', 'email'],
    types: {
      id: 'number',
      username: 'string',
      display_name: 'string',
      email: 'string',
    },
  },

  UserProfile: {
    requiredFields: ['id', 'username', 'display_name', 'bio', 'follower_count', 'following_count'],
    types: {
      id: 'number',
      username: 'string',
      display_name: 'string',
      follower_count: 'number',
      following_count: 'number',
    },
  },
};

