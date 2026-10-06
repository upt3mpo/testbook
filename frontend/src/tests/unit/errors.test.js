/**
 * Unit tests for getErrorMessage (src/utils/errors.js).
 *
 * The API returns errors in two shapes: a plain string, or (for HTTP 422) a list of validation
 * issues. Rendering the list directly crashed the whole page (A11Y-019). These tests use the
 * real shapes captured from the running API.
 */

import { describe, expect, it } from 'vitest';
import { getErrorMessage } from '../../utils/errors.js';

const apiError = (detail) => ({ response: { data: { detail } } });
const FALLBACK = 'Something failed.';

describe('getErrorMessage: plain string errors', () => {
  it('returns the string as is', () => {
    expect(getErrorMessage(apiError('Email already registered'), FALLBACK)).toBe(
      'Email already registered'
    );
  });
});

describe('getErrorMessage: validation errors (HTTP 422)', () => {
  // Captured from POST /api/auth/register with the email "a@b".
  const invalidEmail = [
    {
      type: 'value_error',
      loc: ['body', 'email'],
      msg: 'value is not a valid email address: The part after the @-sign is not valid. It should have a period.',
      input: 'a@b',
      ctx: { reason: 'The part after the @-sign is not valid. It should have a period.' },
    },
  ];

  it('always returns a string, so it is always safe to render', () => {
    expect(typeof getErrorMessage(apiError(invalidEmail), FALLBACK)).toBe('string');
  });

  it('names the field and says how to fix it', () => {
    expect(getErrorMessage(apiError(invalidEmail), FALLBACK)).toBe(
      'Enter a valid email address, for example name@example.com.'
    );
  });

  it('says which required fields are missing, one sentence each', () => {
    const missing = [
      { type: 'missing', loc: ['body', 'username'], msg: 'Field required', input: {} },
      { type: 'missing', loc: ['body', 'display_name'], msg: 'Field required', input: {} },
    ];
    expect(getErrorMessage(apiError(missing), FALLBACK)).toBe(
      'Username is required. Display name is required.'
    );
  });

  it('keeps the framework message, prefixed by the field, for anything else', () => {
    const tooShort = [
      {
        type: 'string_too_short',
        loc: ['body', 'password'],
        msg: 'String should have at least 8 characters',
      },
    ];
    expect(getErrorMessage(apiError(tooShort), FALLBACK)).toBe(
      'Password: String should have at least 8 characters.'
    );
  });
});

describe('getErrorMessage: anything unexpected falls back to a safe string', () => {
  it.each([
    ['no response at all (network error)', new Error('Network Error')],
    ['an empty body', { response: { data: {} } }],
    ['an empty string detail', apiError('   ')],
    ['an empty list', apiError([])],
    ['a list of junk', apiError([null, 42, {}])],
    ['null', null],
    ['undefined', undefined],
  ])('%s', (_name, error) => {
    expect(getErrorMessage(error, FALLBACK)).toBe(FALLBACK);
  });

  it('uses a plain string inside a list', () => {
    expect(getErrorMessage(apiError(['password is too common']), FALLBACK)).toBe(
      'Password is too common.'
    );
  });
});
