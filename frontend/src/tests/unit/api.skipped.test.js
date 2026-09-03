/**
 * api.js coverage notes.
 *
 * Every other test file in this suite mocks this exact module
 * (`vi.mock('../../api', () => ({ ... }))`) so it can control what the
 * component under test receives without a real HTTP call. That's the
 * right call for testing components in isolation, but it means the
 * real body of api.js - the actual URL/method/payload each wrapper
 * sends to axios, and the request interceptor that attaches the auth
 * header - never itself runs in any of them.
 *
 * What *is* already covered, indirectly but extensively: that each
 * wrapper gets called with the right arguments. Every
 * `expect(api.usersAPI.followUser).toHaveBeenCalledWith('mikechen')`-
 * style assertion across Profile.test.jsx, Followers.test.jsx,
 * Settings.test.jsx, etc. is effectively a contract test against this
 * file's exported shape.
 *
 * What's below is skipped rather than removed, so the gap shows up in
 * test output instead of just being silently absent from this file.
 */

import { describe, it } from 'vitest';

describe('api.js (real network layer)', () => {
  it.skip(
    'attaches Authorization: Bearer <token> to requests when a token is stored',
    () => {
      // Not covered: mocking this module (as every other test does)
      // replaces the interceptor along with everything else, so it
      // never runs. Testing it honestly means observing a real
      // outgoing request rather than asserting against another mock of
      // this same file.
      //
      // Approach: this repo already has the tool for this -
      // src/tests/mocks/handlers.js and MSW (Mock Service Worker),
      // set up and documented ("Lab 6B: Advanced Component Testing")
      // but not currently wired into any real test. MSW intercepts
      // actual outgoing requests at the network level, so a test could
      // render a component with no token in localStorage, inspect the
      // Authorization header MSW observed (absent), then repeat with a
      // token set and assert the header appears only the second time.
      //
      // handlers.js needs one fix first: it hardcodes
      // `http://localhost:8000/api`, but api.js's baseURL is the
      // relative `/api`, which axios resolves against jsdom's default
      // test origin - `http://localhost:3000/api` in this project's
      // Vitest setup (confirmed by logging window.location.href in a
      // throwaway test). As written, handlers.js would never actually
      // intercept a request this file makes.
    }
  );

  it.skip('every authAPI/usersAPI/postsAPI/feedAPI/devAPI wrapper hits its real endpoint', () => {
    // Not covered directly for the same module-mocking reason above.
    // Low priority beyond the interceptor: these are one-line endpoint
    // mappings (e.g. `getProfile: (username) => api.get(\`/users/${username}\`)`)
    // with no conditional logic of their own, and every endpoint they
    // construct is already exercised indirectly by the
    // toHaveBeenCalledWith(...) assertions in the component tests that
    // mock this file.
    //
    // Approach if pursued anyway: same MSW-based technique as above -
    // call each wrapper directly (no component involved) and assert on
    // the method/URL/body MSW's request handler observed.
  });
});
