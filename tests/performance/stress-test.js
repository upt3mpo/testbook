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

export const options = {
  stages: [
    { duration: '2m', target: 20 },   // Ramp up to 20 users
    { duration: '5m', target: 20 },   // Stay at 20 users
    { duration: '2m', target: 50 },   // Spike to 50 users
    { duration: '5m', target: 50 },   // Stay at 50 users
    { duration: '2m', target: 100 },  // Spike to 100 users
    { duration: '5m', target: 100 },  // Stay at 100 users
    { duration: '5m', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(99)<3000'],  // 99% < 3s even under stress
    http_req_failed: ['rate<0.10'],     // Error rate < 10% (more lenient)
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

