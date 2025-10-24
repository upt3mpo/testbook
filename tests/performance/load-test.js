/**
 * K6 Load Test for Testbook API
 *
 * This file demonstrates comprehensive performance testing using k6.
 * It tests the system under sustained load to identify performance
 * characteristics, bottlenecks, and system limits.
 *
 * Key Testing Concepts Demonstrated:
 * - Load testing with realistic user scenarios
 * - Performance metrics collection and analysis
 * - Threshold-based pass/fail criteria
 * - Custom metrics for specific operations
 * - CI vs local testing configurations
 * - Error rate monitoring and analysis
 *
 * This file is referenced in Stage 4 learning materials as an example
 * of professional performance testing practices.
 *
 * Run: k6 run load-test.js
 */

import { check, group, sleep } from "k6";
import http from "k6/http";
import { Rate, Trend } from "k6/metrics";

// Custom metrics for detailed performance analysis
const errorRate = new Rate("errors");
const loginDuration = new Trend("login_duration");
const feedDuration = new Trend("feed_duration");
const postCreationDuration = new Trend("post_creation_duration");

// Load test configuration
// CI: Fast validation (2 min) | Local: Thorough testing (4 min)
const isCI = __ENV.CI === "true";

export const options = {
  stages: isCI
    ? [
        { duration: "20s", target: 5 }, // Ramp up to 5 users
        { duration: "40s", target: 5 }, // Stay at 5 users
        { duration: "20s", target: 10 }, // Ramp up to 10 users
        { duration: "30s", target: 10 }, // Stay at 10 users
        { duration: "10s", target: 0 }, // Ramp down (total: 2 min)
      ]
    : [
        { duration: "30s", target: 10 }, // Ramp up to 10 users
        { duration: "1m", target: 10 }, // Stay at 10 users
        { duration: "30s", target: 15 }, // Ramp up to 15 users
        { duration: "2m", target: 15 }, // Stay at 15 users
        { duration: "30s", target: 0 }, // Ramp down (total: 4.5 min)
      ],
  thresholds: {
    // Performance thresholds - these define what "good performance" means
    http_req_duration: ["p(95)<1000", "p(99)<2000"], // 95% < 1s, 99% < 2s
    http_req_failed: ["rate<0.05"], // Error rate < 5%
    errors: ["rate<0.05"], // Error rate < 5%
    login_duration: ["p(95)<500"], // Login should be fast
    feed_duration: ["p(95)<1000"], // Feed loading performance
    post_creation_duration: ["p(95)<600"], // Post creation performance
  },
};

const BASE_URL = __ENV.BASE_URL || "http://localhost:8000/api";

// Test data
const TEST_USERS = [
  { email: "sarah.johnson@testbook.com", password: "Sarah2024!" },
  { email: "mike.chen@testbook.com", password: "MikeRocks88" },
  { email: "emma.davis@testbook.com", password: "EmmaLovesPhotos" },
  { email: "alex.rodriguez@testbook.com", password: "Alex1234" },
];

export function setup() {
  // Reset and seed database
  http.post(`${BASE_URL}/dev/reset`);
  console.log("Database reset for load test");
  return { timestamp: Date.now() };
}

export default function (data) {
  // Select random user
  const user = TEST_USERS[Math.floor(Math.random() * TEST_USERS.length)];
  let token;

  group("User Login", () => {
    const startTime = Date.now();
    const loginRes = http.post(`${BASE_URL}/auth/login`, JSON.stringify(user), {
      headers: { "Content-Type": "application/json" },
    });
    loginDuration.add(Date.now() - startTime);

    const success = check(loginRes, {
      "login successful": (r) => r.status === 200,
      "token received": (r) => r.json("access_token") !== undefined,
    });
    errorRate.add(!success);

    if (success) {
      token = loginRes.json("access_token");
    }
  });

  if (token) {
    const headers = {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    };

    group("Browse Feed", () => {
      const startTime = Date.now();
      const feedRes = http.get(`${BASE_URL}/feed/all`, { headers });
      feedDuration.add(Date.now() - startTime);

      const success = check(feedRes, {
        "feed loaded": (r) => r.status === 200,
        "feed has posts": (r) => Array.isArray(r.json()) && r.json().length > 0,
      });
      errorRate.add(!success);
    });

    // 30% chance to create a post
    if (Math.random() < 0.3) {
      group("Create Post", () => {
        const postContent = `Load test post at ${new Date().toISOString()}`;
        const startTime = Date.now();
        const postRes = http.post(
          `${BASE_URL}/posts/`,
          JSON.stringify({
            content: postContent,
          }),
          { headers }
        );
        postCreationDuration.add(Date.now() - startTime);

        const success = check(postRes, {
          "post created": (r) => r.status === 201,
          "post has id": (r) => r.json("id") !== undefined,
        });
        errorRate.add(!success);
      });
    }

    // 50% chance to view following feed
    if (Math.random() < 0.5) {
      group("Browse Following Feed", () => {
        const followingRes = http.get(`${BASE_URL}/feed/following`, {
          headers,
        });
        check(followingRes, {
          "following feed loaded": (r) => r.status === 200,
        });
      });
    }

    // 20% chance to view profile
    if (Math.random() < 0.2) {
      group("View Profile", () => {
        const meRes = http.get(`${BASE_URL}/auth/me`, { headers });
        check(meRes, {
          "profile loaded": (r) => r.status === 200,
        });
      });
    }
  }

  sleep(Math.random() * 3 + 1); // Random sleep between 1-4 seconds
}

export function handleSummary(data) {
  return {
    "load-test-results.json": JSON.stringify(data, null, 2),
    stdout: textSummary(data, { indent: " ", enableColors: true }),
  };
}

function textSummary(data, options = {}) {
  const indent = options.indent || "";
  const enableColors = options.enableColors || false;

  let summary = `\n${indent}Load Test Summary\n${indent}${"=".repeat(50)}\n`;

  // Add key metrics
  if (data.metrics.http_req_duration) {
    summary += `${indent}HTTP Request Duration:\n`;
    summary += `${indent}  avg: ${data.metrics.http_req_duration.values.avg.toFixed(
      2
    )}ms\n`;
    summary += `${indent}  p95: ${data.metrics.http_req_duration.values[
      "p(95)"
    ].toFixed(2)}ms\n`;
    summary += `${indent}  p99: ${data.metrics.http_req_duration.values[
      "p(99)"
    ].toFixed(2)}ms\n`;
  }

  if (data.metrics.http_req_failed) {
    const failRate = (data.metrics.http_req_failed.values.rate * 100).toFixed(
      2
    );
    summary += `${indent}Error Rate: ${failRate}%\n`;
  }

  return summary;
}
