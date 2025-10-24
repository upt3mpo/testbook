# 🧪 Lab 13: Load Testing with k6

**Estimated Time:** 120 minutes<br>
**Difficulty:** Intermediate<br>
**Language:** 🟨 JavaScript (k6)<br>
**Prerequisites:** Lab 12 completed

**What This Adds:** Master load testing with k6 to ensure your application can handle real-world traffic. Learn to identify performance bottlenecks and optimize your application for production scale.

---

## 🎯 What You'll Learn

- **Load testing fundamentals** - Test application under various load conditions
- **k6 scripting** - Write performance test scripts in JavaScript
- **Performance metrics** - Understand response times, throughput, and error rates
- **Load patterns** - Test with different user loads and scenarios
- **Performance analysis** - Identify bottlenecks and optimization opportunities
- **CI/CD integration** - Run load tests in continuous integration

---

## 📋 Why Load Testing Matters

**The Problem:**

- Application works fine with 10 users
- Crashes with 1000 users
- No way to predict production performance
- Performance issues discovered too late

**The Solution:**
Load testing simulates real user traffic to identify performance limits and bottlenecks before production.

---

## 📋 Step-by-Step Instructions

### Part 1: k6 Setup and Basics (30 minutes)

#### Step 1: Install k6

**Windows (using Chocolatey):**

```bash
choco install k6
```

**macOS (using Homebrew):**

```bash
brew install k6
```

**Linux (using package manager):**

```bash
# Ubuntu/Debian
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
echo "deb https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt-get update
sudo apt-get install k6

# CentOS/RHEL
sudo dnf install https://dl.k6.io/rpm/repo.rpm
sudo dnf install k6
```

**Verify installation:**

```bash
k6 version
```

#### Step 2: Create Your First Load Test

Create `tests/performance/load-test-basic.js`:

```javascript
import http from "k6/http";
import { check, sleep } from "k6";

export let options = {
  vus: 10, // 10 virtual users
  duration: "30s", // for 30 seconds
};

export default function () {
  // Test the health endpoint
  let response = http.get("http://localhost:8000/api/health");

  // Check if the response is successful
  check(response, {
    "status is 200": (r) => r.status === 200,
    "response time < 200ms": (r) => r.timings.duration < 200,
    "response has status field": (r) => JSON.parse(r.body).status === "healthy",
  });

  sleep(1); // Wait 1 second between requests
}
```

#### Step 3: Run Your First Load Test

```bash
cd tests/performance
k6 run load-test-basic.js
```

**Expected output:**

```text
     ✓ status is 200
     ✓ response time < 200ms
     ✓ response has status field

     checks.........................: 100% ✓ 300      ✗ 0
     data_received..................: 15 kB 500 B/s
     data_sent......................: 2.1 kB 70 B/s
     http_req_duration..............: avg=45ms    min=12ms med=42ms max=156ms p(95)=89ms
     http_req_failed................: 0.00% ✓ 0        ✗ 300
     http_reqs......................: 300   10.0/s
     iteration_duration.............: avg=1.04s   min=1.01s med=1.03s max=1.16s p(95)=1.05s
     iterations.....................: 300   10.0/s
     vus............................: 10    min=10     max=10
     vus_max........................: 10    min=10     max=10
```

---

### Part 2: Advanced Load Testing Scenarios (30 minutes)

#### Step 1: Create User Authentication Load Test

Create `tests/performance/load-test-auth.js`:

```javascript
import http from "k6/http";
import { check, sleep } from "k6";
import { Rate } from "k6/metrics";

// Custom metric for tracking authentication success rate
let authSuccessRate = new Rate("auth_success_rate");

export let options = {
  stages: [
    { duration: "2m", target: 10 }, // Ramp up to 10 users over 2 minutes
    { duration: "5m", target: 10 }, // Stay at 10 users for 5 minutes
    { duration: "2m", target: 50 }, // Ramp up to 50 users over 2 minutes
    { duration: "5m", target: 50 }, // Stay at 50 users for 5 minutes
    { duration: "2m", target: 0 }, // Ramp down to 0 users over 2 minutes
  ],
  thresholds: {
    http_req_duration: ["p(95)<500"], // 95% of requests should be below 500ms
    http_req_failed: ["rate<0.1"], // Error rate should be less than 10%
    auth_success_rate: ["rate>0.9"], // Authentication success rate should be > 90%
  },
};

export default function () {
  // Test user registration
  let registerPayload = JSON.stringify({
    email: `test${__VU}${__ITER}@example.com`,
    username: `user${__VU}${__ITER}`,
    display_name: `Test User ${__VU}${__ITER}`,
    password: "password123",
  });

  let registerResponse = http.post(
    "http://localhost:8000/api/auth/register",
    registerPayload,
    {
      headers: { "Content-Type": "application/json" },
    }
  );

  let registerSuccess = check(registerResponse, {
    "registration status is 201": (r) => r.status === 201,
    "registration response time < 1000ms": (r) => r.timings.duration < 1000,
  });

  authSuccessRate.add(registerSuccess);

  if (registerSuccess) {
    // Test user login
    let loginPayload = JSON.stringify({
      email: `test${__VU}${__ITER}@example.com`,
      password: "password123",
    });

    let loginResponse = http.post(
      "http://localhost:8000/api/auth/login",
      loginPayload,
      {
        headers: { "Content-Type": "application/json" },
      }
    );

    let loginSuccess = check(loginResponse, {
      "login status is 200": (r) => r.status === 200,
      "login response time < 500ms": (r) => r.timings.duration < 500,
      "login returns access token": (r) =>
        JSON.parse(r.body).access_token !== undefined,
    });

    authSuccessRate.add(loginSuccess);

    if (loginSuccess) {
      // Test authenticated endpoint
      let token = JSON.parse(loginResponse.body).access_token;
      let profileResponse = http.get("http://localhost:8000/api/users/me", {
        headers: { Authorization: `Bearer ${token}` },
      });

      check(profileResponse, {
        "profile status is 200": (r) => r.status === 200,
        "profile response time < 300ms": (r) => r.timings.duration < 300,
      });
    }
  }

  sleep(1);
}
```

#### Step 2: Create API Endpoint Load Test

Create `tests/performance/load-test-api.js`:

```javascript
import http from "k6/http";
import { check, sleep } from "k6";
import { Counter, Rate, Trend } from "k6/metrics";

// Custom metrics
let postCreationRate = new Rate("post_creation_success_rate");
let postCreationCounter = new Counter("posts_created");
let postCreationDuration = new Trend("post_creation_duration");

export let options = {
  scenarios: {
    // Scenario 1: Normal load
    normal_load: {
      executor: "constant-vus",
      vus: 20,
      duration: "5m",
    },
    // Scenario 2: Spike test
    spike_test: {
      executor: "ramping-vus",
      startVUs: 0,
      stages: [
        { duration: "1m", target: 100 },
        { duration: "2m", target: 100 },
        { duration: "1m", target: 0 },
      ],
      startTime: "6m", // Start after normal load
    },
  },
  thresholds: {
    http_req_duration: ["p(95)<1000"],
    http_req_failed: ["rate<0.05"],
    post_creation_success_rate: ["rate>0.95"],
  },
};

export default function () {
  // First, authenticate to get a token
  let loginPayload = JSON.stringify({
    email: "test@example.com",
    password: "password123",
  });

  let loginResponse = http.post(
    "http://localhost:8000/api/auth/login",
    loginPayload,
    {
      headers: { "Content-Type": "application/json" },
    }
  );

  let loginSuccess = check(loginResponse, {
    "login successful": (r) => r.status === 200,
  });

  if (loginSuccess) {
    let token = JSON.parse(loginResponse.body).access_token;
    let headers = {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    };

    // Test creating a post
    let postPayload = JSON.stringify({
      title: `Load Test Post ${__VU}-${__ITER}`,
      content: `This is a load test post created by virtual user ${__VU} at iteration ${__ITER}`,
    });

    let startTime = Date.now();
    let postResponse = http.post(
      "http://localhost:8000/api/posts",
      postPayload,
      { headers }
    );
    let endTime = Date.now();

    let postSuccess = check(postResponse, {
      "post creation status is 201": (r) => r.status === 201,
      "post creation response time < 2000ms": (r) => r.timings.duration < 2000,
    });

    postCreationRate.add(postSuccess);
    if (postSuccess) {
      postCreationCounter.add(1);
    }
    postCreationDuration.add(endTime - startTime);

    // Test fetching posts
    let postsResponse = http.get("http://localhost:8000/api/feed", { headers });
    check(postsResponse, {
      "posts fetch status is 200": (r) => r.status === 200,
      "posts fetch response time < 1000ms": (r) => r.timings.duration < 1000,
    });

    // Test fetching user profile
    let profileResponse = http.get("http://localhost:8000/api/users/me", {
      headers,
    });
    check(profileResponse, {
      "profile fetch status is 200": (r) => r.status === 200,
      "profile fetch response time < 500ms": (r) => r.timings.duration < 500,
    });
  }

  sleep(1);
}
```

---

### Part 3: Performance Analysis and Reporting (30 minutes)

#### Step 1: Create Comprehensive Load Test

Create `tests/performance/load-test-comprehensive.js`:

```javascript
import http from "k6/http";
import { check, sleep } from "k6";
import { Rate, Trend, Counter } from "k6/metrics";

// Custom metrics for detailed analysis
let authSuccessRate = new Rate("auth_success_rate");
let postSuccessRate = new Rate("post_success_rate");
let apiResponseTime = new Trend("api_response_time");
let errorCounter = new Counter("error_count");

export let options = {
  stages: [
    { duration: "2m", target: 5 }, // Warm-up
    { duration: "5m", target: 20 }, // Normal load
    { duration: "3m", target: 50 }, // High load
    { duration: "2m", target: 100 }, // Peak load
    { duration: "5m", target: 100 }, // Sustained peak
    { duration: "2m", target: 0 }, // Cool down
  ],
  thresholds: {
    http_req_duration: ["p(95)<2000", "p(99)<5000"],
    http_req_failed: ["rate<0.1"],
    auth_success_rate: ["rate>0.95"],
    post_success_rate: ["rate>0.9"],
    api_response_time: ["p(95)<1500"],
  },
};

export default function () {
  let baseUrl = "http://localhost:8000/api";
  let headers = { "Content-Type": "application/json" };

  // Test 1: Health check
  let healthResponse = http.get(`${baseUrl}/health`);
  check(healthResponse, {
    "health check status is 200": (r) => r.status === 200,
    "health check response time < 100ms": (r) => r.timings.duration < 100,
  });

  // Test 2: User registration
  let registerPayload = JSON.stringify({
    email: `loadtest${__VU}${__ITER}@example.com`,
    username: `loaduser${__VU}${__ITER}`,
    display_name: `Load Test User ${__VU}`,
    password: "password123",
  });

  let registerResponse = http.post(
    `${baseUrl}/auth/register`,
    registerPayload,
    { headers }
  );
  let registerSuccess = check(registerResponse, {
    "registration status is 201": (r) => r.status === 201,
    "registration response time < 2000ms": (r) => r.timings.duration < 2000,
  });

  if (!registerSuccess) {
    errorCounter.add(1);
  }

  // Test 3: User login
  let loginPayload = JSON.stringify({
    email: `loadtest${__VU}${__ITER}@example.com`,
    password: "password123",
  });

  let loginResponse = http.post(`${baseUrl}/auth/login`, loginPayload, {
    headers,
  });
  let loginSuccess = check(loginResponse, {
    "login status is 200": (r) => r.status === 200,
    "login response time < 1000ms": (r) => r.timings.duration < 1000,
    "login returns token": (r) => JSON.parse(r.body).access_token !== undefined,
  });

  authSuccessRate.add(loginSuccess);

  if (loginSuccess) {
    let token = JSON.parse(loginResponse.body).access_token;
    let authHeaders = {
      ...headers,
      Authorization: `Bearer ${token}`,
    };

    // Test 4: Create post
    let postPayload = JSON.stringify({
      title: `Load Test Post ${__VU}-${__ITER}`,
      content: `This is a comprehensive load test post created by VU ${__VU} at iteration ${__ITER}. The content is designed to test the system under various load conditions.`,
    });

    let postResponse = http.post(`${baseUrl}/posts`, postPayload, {
      headers: authHeaders,
    });
    let postSuccess = check(postResponse, {
      "post creation status is 201": (r) => r.status === 201,
      "post creation response time < 2000ms": (r) => r.timings.duration < 2000,
    });

    postSuccessRate.add(postSuccess);
    apiResponseTime.add(postResponse.timings.duration);

    if (!postSuccess) {
      errorCounter.add(1);
    }

    // Test 5: Fetch posts
    let postsResponse = http.get(`${baseUrl}/feed`, { headers: authHeaders });
    check(postsResponse, {
      "posts fetch status is 200": (r) => r.status === 200,
      "posts fetch response time < 1500ms": (r) => r.timings.duration < 1500,
    });

    // Test 6: Fetch user profile
    let profileResponse = http.get(`${baseUrl}/users/me`, {
      headers: authHeaders,
    });
    check(profileResponse, {
      "profile fetch status is 200": (r) => r.status === 200,
      "profile fetch response time < 800ms": (r) => r.timings.duration < 800,
    });
  }

  sleep(1);
}
```

#### Step 2: Create Performance Test with Different Scenarios

Create `tests/performance/load-test-scenarios.js`:

```javascript
import http from "k6/http";
import { check, sleep } from "k6";

export let options = {
  scenarios: {
    // Scenario 1: Smoke test - minimal load
    smoke_test: {
      executor: "constant-vus",
      vus: 1,
      duration: "1m",
      tags: { test_type: "smoke" },
    },
    // Scenario 2: Load test - normal expected load
    load_test: {
      executor: "ramping-vus",
      startVUs: 0,
      stages: [
        { duration: "2m", target: 10 },
        { duration: "5m", target: 10 },
        { duration: "2m", target: 0 },
      ],
      tags: { test_type: "load" },
    },
    // Scenario 3: Stress test - beyond normal capacity
    stress_test: {
      executor: "ramping-vus",
      startVUs: 0,
      stages: [
        { duration: "2m", target: 20 },
        { duration: "5m", target: 20 },
        { duration: "2m", target: 50 },
        { duration: "5m", target: 50 },
        { duration: "2m", target: 0 },
      ],
      tags: { test_type: "stress" },
    },
    // Scenario 4: Spike test - sudden traffic spikes
    spike_test: {
      executor: "ramping-vus",
      startVUs: 0,
      stages: [
        { duration: "1m", target: 100 },
        { duration: "1m", target: 100 },
        { duration: "1m", target: 0 },
      ],
      tags: { test_type: "spike" },
    },
  },
  thresholds: {
    http_req_duration: ["p(95)<2000"],
    http_req_failed: ["rate<0.1"],
  },
};

export default function () {
  let baseUrl = "http://localhost:8000/api";
  let headers = { "Content-Type": "application/json" };

  // Health check
  let healthResponse = http.get(`${baseUrl}/health`);
  check(healthResponse, {
    "health check status is 200": (r) => r.status === 200,
  });

  // User registration
  let registerPayload = JSON.stringify({
    email: `scenario${__VU}${__ITER}@example.com`,
    username: `scenariouser${__VU}${__ITER}`,
    display_name: `Scenario User ${__VU}`,
    password: "password123",
  });

  let registerResponse = http.post(
    `${baseUrl}/auth/register`,
    registerPayload,
    { headers }
  );
  check(registerResponse, {
    "registration status is 201": (r) => r.status === 201,
  });

  // User login
  let loginPayload = JSON.stringify({
    email: `scenario${__VU}${__ITER}@example.com`,
    password: "password123",
  });

  let loginResponse = http.post(`${baseUrl}/auth/login`, loginPayload, {
    headers,
  });
  let loginSuccess = check(loginResponse, {
    "login status is 200": (r) => r.status === 200,
  });

  if (loginSuccess) {
    let token = JSON.parse(loginResponse.body).access_token;
    let authHeaders = {
      ...headers,
      Authorization: `Bearer ${token}`,
    };

    // Create post
    let postPayload = JSON.stringify({
      title: `Scenario Test Post ${__VU}-${__ITER}`,
      content: `This is a scenario test post for ${
        __ENV.TEST_TYPE || "unknown"
      } scenario.`,
    });

    let postResponse = http.post(`${baseUrl}/posts`, postPayload, {
      headers: authHeaders,
    });
    check(postResponse, {
      "post creation status is 201": (r) => r.status === 201,
    });

    // Fetch posts
    let postsResponse = http.get(`${baseUrl}/feed`, { headers: authHeaders });
    check(postsResponse, {
      "posts fetch status is 200": (r) => r.status === 200,
    });
  }

  sleep(1);
}
```

---

### Part 4: CI/CD Integration (30 minutes)

#### Step 1: Create GitHub Actions Workflow

Create `.github/workflows/load-tests.yml`:

```yaml
name: Load Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  schedule:
    - cron: "0 2 * * *" # Run daily at 2 AM

jobs:
  load-tests:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Install Python dependencies
        run: |
          cd backend
          pip install -r requirements.txt

      - name: Install k6
        run: |
          sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
          echo "deb https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
          sudo apt-get update
          sudo apt-get install k6

      - name: Start backend server
        run: |
          cd backend
          python -m uvicorn main:app --host 0.0.0.0 --port 8000 &
          sleep 10

      - name: Run smoke tests
        run: |
          cd tests/performance
          k6 run --env TEST_TYPE=smoke load-test-scenarios.js

      - name: Run load tests
        run: |
          cd tests/performance
          k6 run load-test-comprehensive.js --out json=results.json

      - name: Upload test results
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: load-test-results
          path: tests/performance/results.json
```

#### Step 2: Create Performance Monitoring Dashboard

Create `tests/performance/performance-dashboard.html`:

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Performance Test Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
      body {
        font-family: Arial, sans-serif;
        margin: 20px;
      }
      .chart-container {
        width: 800px;
        height: 400px;
        margin: 20px 0;
      }
      .metric {
        display: inline-block;
        margin: 10px;
        padding: 10px;
        border: 1px solid #ccc;
      }
    </style>
  </head>
  <body>
    <h1>Performance Test Dashboard</h1>

    <div class="metrics">
      <div class="metric">
        <h3>Response Time (95th percentile)</h3>
        <span id="response-time-95">-</span> ms
      </div>
      <div class="metric">
        <h3>Throughput</h3>
        <span id="throughput">-</span> requests/second
      </div>
      <div class="metric">
        <h3>Error Rate</h3>
        <span id="error-rate">-</span> %
      </div>
    </div>

    <div class="chart-container">
      <canvas id="responseTimeChart"></canvas>
    </div>

    <div class="chart-container">
      <canvas id="throughputChart"></canvas>
    </div>

    <script>
      // This would be populated with actual test results
      const testResults = {
        responseTime95: 1500,
        throughput: 25.5,
        errorRate: 2.1,
      };

      document.getElementById("response-time-95").textContent =
        testResults.responseTime95;
      document.getElementById("throughput").textContent =
        testResults.throughput;
      document.getElementById("error-rate").textContent = testResults.errorRate;

      // Response time chart
      const responseTimeCtx = document
        .getElementById("responseTimeChart")
        .getContext("2d");
      new Chart(responseTimeCtx, {
        type: "line",
        data: {
          labels: ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
          datasets: [
            {
              label: "Response Time (ms)",
              data: [100, 120, 150, 180, 200, 220, 250, 280, 300, 320, 350],
              borderColor: "rgb(75, 192, 192)",
              tension: 0.1,
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
            },
          },
        },
      });

      // Throughput chart
      const throughputCtx = document
        .getElementById("throughputChart")
        .getContext("2d");
      new Chart(throughputCtx, {
        type: "bar",
        data: {
          labels: ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
          datasets: [
            {
              label: "Throughput (req/s)",
              data: [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60],
              backgroundColor: "rgb(54, 162, 235)",
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
            },
          },
        },
      });
    </script>
  </body>
</html>
```

---

## 💪 Challenge Exercises

### Challenge 1: Create Custom Load Test Scenarios

```javascript
// Create tests/performance/load-test-custom.js
import http from "k6/http";
import { check, sleep } from "k6";

export let options = {
  scenarios: {
    // TODO: Create a custom scenario that:
    // 1. Simulates a typical user journey (register -> login -> create post -> view feed)
    // 2. Tests different user types (regular users, power users, admins)
    // 3. Includes realistic think time between actions
    // 4. Tests error scenarios (invalid data, network issues)
  },
};

export default function () {
  // TODO: Implement the custom scenario
  // Hint: Use different user types based on __VU % 3
  // 0-2: Regular user, 3-4: Power user, 5: Admin
}
```

### Challenge 2: Create Performance Regression Detection

```javascript
// Create tests/performance/performance-regression.js
import http from "k6/http";
import { check, sleep } from "k6";

export let options = {
  // TODO: Create a test that:
  // 1. Compares current performance with baseline
  // 2. Fails if performance degrades by more than 20%
  // 3. Generates a performance report
  // 4. Can be run in CI/CD pipeline
};

export default function () {
  // TODO: Implement performance regression detection
}
```

---

## ✅ Completion Checklist

- [ ] Can write basic k6 load test scripts
- [ ] Can create different load test scenarios (smoke, load, stress, spike)
- [ ] Can analyze performance metrics and identify bottlenecks
- [ ] Can integrate load tests into CI/CD pipeline
- [ ] Can create custom metrics and thresholds
- [ ] Completed all challenge exercises
- [ ] Understand how to scale load testing for production

---

## 💡 Pro Tips

1. **Start with smoke tests** - Verify basic functionality under minimal load
2. **Use realistic data** - Test with data similar to production
3. **Monitor key metrics** - Focus on response time, throughput, and error rate
4. **Test incrementally** - Gradually increase load to find breaking points
5. **Automate everything** - Run load tests in CI/CD for continuous monitoring

---

## 📚 Next Steps

**Continue building your skills:**

- **[Lab 14: Security Testing & OWASP (Python)](LAB_14_Security_Testing_OWASP_Python.md)** - Security testing
- **[Lab 15: Rate Limiting & Production Monitoring (Python)](LAB_15_Rate_Limiting_Production_Python.md)** - Production readiness
- **[Lab 16: Complete Test Suite Design (Python)](LAB_16_Complete_Test_Suite_Design_Python.md)** - Test strategy

---

**🎉 Congratulations!** You now understand load testing with k6 and can ensure your application performs well under production load!

**Next Lab:** [Lab 14: Security Testing & OWASP (Python)](LAB_14_Security_Testing_OWASP_Python.md)
