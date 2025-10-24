/**
 * K6 Stress Test for Testbook API
 *
 * Tests the system beyond normal operational capacity
 * to find the breaking point.
 *
 * Run: k6 run stress-test.js
 */

import { sleep } from 'k6';
import http from 'k6/http';

// CI: Quick stress test (2.5 min) | Local: Real stress test (5 min)
const isCI = __ENV.CI === 'true';

export const options = {
  stages: isCI ? [
    { duration: '20s', target: 10 },  // Ramp up to 10 users
    { duration: '40s', target: 15 },  // Stay at 15 users
    { duration: '20s', target: 25 },  // Spike to 25 users
    { duration: '50s', target: 25 },  // Stay at 25 users
    { duration: '20s', target: 0 },   // Ramp down (total: 2.5 min)
  ] : [
    { duration: '30s', target: 15 },  // Ramp up to 15 users
    { duration: '1m', target: 15 },   // Stay at 15 users
    { duration: '30s', target: 30 },  // Spike to 30 users
    { duration: '1m', target: 30 },   // Stay at 30 users
    { duration: '30s', target: 50 },  // Spike to 50 users
    { duration: '1m', target: 50 },   // Stay at 50 users
    { duration: '30s', target: 0 },   // Ramp down (total: 5 min)
  ],
  thresholds: {
    http_req_duration: ['p(99)<3000'],  // 99% < 3s even under stress
    http_req_failed: ['rate<0.10'],     // Error rate < 10% (more lenient under stress)
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost:8000/api';

export function setup() {
  http.post(`${BASE_URL}/dev/reset`);
  return {};
}

export default function () {
  const loginRes = http.post(`${BASE_URL}/auth/login`, JSON.stringify({
    email: 'sarah.johnson@testbook.com',
    password: 'Sarah2024!'
  }), {
    headers: { 'Content-Type': 'application/json' },
  });

  if (loginRes.status === 200) {
    const token = loginRes.json('access_token');
    const headers = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    };

    // Rapid-fire feed requests
    http.get(`${BASE_URL}/feed/all`, { headers });
    http.get(`${BASE_URL}/feed/following`, { headers });
    http.get(`${BASE_URL}/auth/me`, { headers });
  }

  sleep(0.5); // Shorter sleep for stress
}
