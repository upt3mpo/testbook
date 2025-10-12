/**
 * K6 Smoke Test for Testbook API
 *
 * A smoke test verifies that the system can handle minimal load
 * and all critical endpoints are working.
 *
 * Run: k6 run smoke-test.js
 */

import { check, group, sleep } from 'k6';
import http from 'k6/http';
import { Rate } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');

// Test configuration
export const options = {
  vus: 1,                    // 1 virtual user
  duration: '1m',            // Run for 1 minute
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% of requests must complete below 500ms
    http_req_failed: ['rate<0.01'],    // Error rate must be below 1%
    errors: ['rate<0.01'],
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost:8000/api';

export function setup() {
  // Reset database before test
  http.post(`${BASE_URL}/dev/reset`);
  console.log('Database reset for smoke test');
  return {};
}

export default function () {
  let token;

  group('Health Check', () => {
    const res = http.get(`${BASE_URL}/health`);
    const success = check(res, {
      'health check returns 200': (r) => r.status === 200,
      'health check response time < 200ms': (r) => r.timings.duration < 200,
    });
    errorRate.add(!success);
  });

  group('Authentication', () => {
    // Login
    const loginRes = http.post(`${BASE_URL}/auth/login`, JSON.stringify({
      email: 'sarah.johnson@testbook.com',
      password: 'Sarah2024!'
    }), {
      headers: { 'Content-Type': 'application/json' },
    });

    const loginSuccess = check(loginRes, {
      'login successful': (r) => r.status === 200,
      'login returns token': (r) => r.json('access_token') !== undefined,
    });
    errorRate.add(!loginSuccess);

    if (loginSuccess) {
      token = loginRes.json('access_token');
    }
  });

  if (token) {
    const headers = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    };

    group('Feed Operations', () => {
      const feedRes = http.get(`${BASE_URL}/feed/all`, { headers });
      const success = check(feedRes, {
        'feed loads successfully': (r) => r.status === 200,
        'feed returns array': (r) => Array.isArray(r.json()),
        'feed response time < 500ms': (r) => r.timings.duration < 500,
      });
      errorRate.add(!success);
    });

    group('Post Operations', () => {
      // Get current user
      const meRes = http.get(`${BASE_URL}/auth/me`, { headers });
      check(meRes, {
        'get current user successful': (r) => r.status === 200,
      });

      // Get a post (assuming post ID 1 exists)
      const postRes = http.get(`${BASE_URL}/posts/1`, { headers });
      const success = check(postRes, {
        'get post successful or not found': (r) => r.status === 200 || r.status === 404,
      });
      errorRate.add(!success && postRes.status !== 404);
    });
  }

  sleep(1);
}

export function teardown(data) {
  console.log('Smoke test completed');
}

