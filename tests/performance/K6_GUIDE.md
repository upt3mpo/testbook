# 📊 K6 Performance Testing Guide

**Load testing with thresholds and result interpretation**

---

## 🎯 What is K6?

K6 is a modern load testing tool that lets you test your application's performance under various load conditions.

**Official Docs:** https://k6.io/docs/

---

## 📦 Installation

```bash
# macOS
brew install k6

# Windows (Chocolatey)
choco install k6

# Windows (Scoop)
scoop install k6

# Linux
sudo gpg -k
sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt-get update
sudo apt-get install k6

# Verify
k6 version
```

---

## 🚀 Running Tests

### Basic Usage

```bash
# Run smoke test
k6 run tests/performance/smoke-test.js

# Run load test
k6 run tests/performance/load-test.js

# Run stress test
k6 run tests/performance/stress-test.js
```

---

## 📊 Understanding K6 Test Scripts

### Test Structure with Thresholds

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

// Define test options with thresholds
export const options = {
  // Number of virtual users
  vus: 10,

  // Test duration
  duration: '30s',

  // Thresholds (PASS/FAIL criteria)
  thresholds: {
    // HTTP errors should be less than 1%
    http_req_failed: ['rate<0.01'],

    // 95% of requests should be below 500ms
    http_req_duration: ['p(95)<500'],

    // 99% of requests should be below 1000ms
    http_req_duration: ['p(99)<1000'],

    // Average should be below 300ms
    http_req_duration: ['avg<300'],

    // Specific checks should pass 95%+ of the time
    checks: ['rate>0.95'],
  },
};

export default function() {
  // Your test scenario
  const res = http.get('http://localhost:8000/api/health');

  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 200ms': (r) => r.timings.duration < 200,
  });

  sleep(1);
}
```

---

## 🎯 Threshold Reference

### Common Threshold Patterns

```javascript
thresholds: {
  // Error Rate (should be very low)
  'http_req_failed': ['rate<0.01'],  // <1% errors

  // Response Time Percentiles
  'http_req_duration': [
    'p(50)<200',   // 50% under 200ms
    'p(90)<400',   // 90% under 400ms
    'p(95)<500',   // 95% under 500ms
    'p(99)<1000',  // 99% under 1000ms
  ],

  // Average Response Time
  'http_req_duration': ['avg<300'],

  // Maximum Response Time
  'http_req_duration': ['max<2000'],

  // Check Success Rate
  'checks': ['rate>0.95'],  // 95%+ checks pass

  // Iteration Duration
  'iteration_duration': ['avg<5000'],  // Avg iteration < 5s

  // HTTP Requests Per Second
  'http_reqs': ['rate>10'],  // At least 10 req/s
}
```

---

## 📈 Test Scenarios

### 1. Smoke Test (Sanity Check)

**Purpose:** Verify system handles minimal load
**VUs:** 1-5
**Duration:** 1-5 minutes

```javascript
// smoke-test.js
export const options = {
  vus: 2,
  duration: '2m',
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<500'],
  },
};
```

**Interpreting Results:**

- ✅ **Pass:** System handles minimal load, no errors
- ❌ **Fail:** Basic functionality broken, fix before scaling

---

### 2. Load Test (Normal Load)

**Purpose:** Test system under expected normal load
**VUs:** 10-50
**Duration:** 10-30 minutes

```javascript
// load-test.js with realistic thresholds
export const options = {
  stages: [
    { duration: '2m', target: 10 },   // Ramp up to 10 users
    { duration: '5m', target: 10 },   // Stay at 10 users
    { duration: '2m', target: 30 },   // Ramp up to 30 users
    { duration: '5m', target: 30 },   // Stay at 30 users
    { duration: '2m', target: 0 },    // Ramp down
  ],

  thresholds: {
    http_req_failed: ['rate<0.05'],      // <5% errors allowed
    http_req_duration: ['p(95)<800'],    // 95% under 800ms
    http_req_duration: ['p(99)<1500'],   // 99% under 1.5s
    http_req_duration: ['avg<400'],      // Average under 400ms
  },
};
```

**Interpreting Results:**

- ✅ **Pass:** System handles normal load within acceptable time
- ⚠️ **Warning:** Some thresholds close to limits, investigate
- ❌ **Fail:** Can't handle normal load, optimization needed

---

### 3. Stress Test (Breaking Point)

**Purpose:** Find when system breaks
**VUs:** Gradually increase until failure
**Duration:** 20-40 minutes

```javascript
// stress-test.js
export const options = {
  stages: [
    { duration: '2m', target: 10 },
    { duration: '5m', target: 10 },
    { duration: '2m', target: 50 },    // Increase
    { duration: '5m', target: 50 },
    { duration: '2m', target: 100 },   // Increase more
    { duration: '5m', target: 100 },
    { duration: '2m', target: 200 },   // Keep increasing
    { duration: '5m', target: 200 },
    { duration: '10m', target: 0 },    // Ramp down and recover
  ],

  thresholds: {
    // More lenient thresholds (expect degradation)
    http_req_failed: ['rate<0.10'],      // <10% errors
    http_req_duration: ['p(95)<2000'],   // 95% under 2s
    http_req_duration: ['p(99)<5000'],   // 99% under 5s
  },
};
```

**Interpreting Results:**

- ✅ Find breaking point (e.g., "System degrades at 150 VUs")
- ✅ Identify bottlenecks
- ✅ Plan capacity needs

---

## 📊 Interpreting K6 Metrics

### Key Metrics Explained

```
✓ http_req_duration
  avg=245ms  min=120ms  med=230ms  max=890ms  p(90)=350ms  p(95)=456ms
```

**What each means:**

- **avg (245ms):** Average response time - should be <300ms for good UX
- **min (120ms):** Fastest response - baseline performance
- **med (230ms):** Median (50th percentile) - typical user experience
- **max (890ms):** Slowest response - check for outliers
- **p(90) (350ms):** 90% of requests faster than this
- **p(95) (456ms):** 95% of requests faster than this (key metric!)
- **p(99):** 99% of requests faster than this

### Threshold Status

```
✓ http_req_duration.........: avg=245ms  p(95)=456ms
✗ http_req_failed...........: 2.3% ✗ 5.0%
```

- ✓ = Threshold passed
- ✗ = Threshold failed (with actual vs threshold)

---

## 🎯 Recommended Thresholds by Endpoint Type

### Fast Endpoints (Health, Static)

```javascript
thresholds: {
  'http_req_duration{endpoint:health}': ['p(95)<100'],
  'http_req_duration{endpoint:static}': ['p(95)<50'],
}
```

### API Endpoints (CRUD)

```javascript
thresholds: {
  'http_req_duration{endpoint:api}': [
    'p(95)<500',   // 95% under 500ms
    'avg<300',     // Average under 300ms
  ],
}
```

### Database-Heavy Endpoints

```javascript
thresholds: {
  'http_req_duration{endpoint:feed}': [
    'p(95)<800',   // 95% under 800ms
    'avg<500',     // Average under 500ms
  ],
}
```

### File Uploads

```javascript
thresholds: {
  'http_req_duration{endpoint:upload}': [
    'p(95)<2000',  // 95% under 2s
    'avg<1000',    // Average under 1s
  ],
}
```

---

## 🚨 When to Optimize

### Response Time Benchmarks

| User Experience | p(95) Response Time | Action |
|-----------------|---------------------|--------|
| **Excellent** | <200ms | 🎉 Great! |
| **Good** | 200-500ms | ✅ Acceptable |
| **Acceptable** | 500-1000ms | ⚠️ Consider optimizing |
| **Poor** | 1000-2000ms | 🔧 Optimize soon |
| **Unacceptable** | >2000ms | 🚨 Optimize immediately |

### Error Rate Benchmarks

| Error Rate | Status | Action |
|------------|--------|--------|
| **<0.1%** | 🎉 Excellent | Keep monitoring |
| **0.1-1%** | ✅ Good | Investigate errors |
| **1-5%** | ⚠️ Warning | Fix error sources |
| **>5%** | 🚨 Critical | Immediate fix needed |

---

## 💡 Performance Optimization Tips

### If Response Times Are High

1. **Check database queries** - Add indexes, optimize joins
2. **Enable caching** - Cache frequent queries
3. **Optimize algorithms** - Profile code, find bottlenecks
4. **Scale resources** - Add CPU/memory
5. **Use connection pooling** - Reuse database connections

### If Error Rate Is High

1. **Check logs** - What errors are occurring?
2. **Check resources** - Out of memory? Disk full?
3. **Check dependencies** - Database/external services down?
4. **Check rate limiting** - Hitting limits?
5. **Check concurrency** - Thread-safe issues?

---

## 📚 Sample K6 Test with Full Configuration

```javascript
import http from 'k6/http';
import { check, sleep, group } from 'k6';
import { Rate, Trend, Counter } from 'k6/metrics';

// Custom metrics
const loginErrors = new Rate('login_errors');
const feedLoadTime = new Trend('feed_load_time');
const postsCreated = new Counter('posts_created');

export const options = {
  stages: [
    { duration: '1m', target: 10 },
    { duration: '3m', target: 10 },
    { duration: '1m', target: 0 },
  ],

  thresholds: {
    // Overall metrics
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<500', 'p(99)<1000'],

    // Custom metrics
    login_errors: ['rate<0.05'],
    feed_load_time: ['p(95)<800'],
    posts_created: ['count>100'],

    // Per-endpoint thresholds
    'http_req_duration{endpoint:login}': ['p(95)<400'],
    'http_req_duration{endpoint:feed}': ['p(95)<600'],
  },
};

const BASE_URL = 'http://localhost:8000/api';

export default function() {
  let authToken;

  // Login
  group('Authentication', function() {
    const loginRes = http.post(`${BASE_URL}/auth/login`, JSON.stringify({
      email: 'sarah.johnson@testbook.com',
      password: 'Sarah2024!',
    }), {
      headers: { 'Content-Type': 'application/json' },
      tags: { endpoint: 'login' },
    });

    const loginSuccess = check(loginRes, {
      'login status is 200': (r) => r.status === 200,
      'has access token': (r) => r.json('access_token') !== undefined,
    });

    loginErrors.add(!loginSuccess);

    if (loginSuccess) {
      authToken = loginRes.json('access_token');
    }
  });

  if (authToken) {
    // Get Feed
    group('Feed', function() {
      const feedStart = new Date();
      const feedRes = http.get(`${BASE_URL}/feed/all`, {
        headers: { 'Authorization': `Bearer ${authToken}` },
        tags: { endpoint: 'feed' },
      });
      const feedDuration = new Date() - feedStart;

      check(feedRes, {
        'feed status is 200': (r) => r.status === 200,
        'feed has posts': (r) => r.json().length > 0,
      });

      feedLoadTime.add(feedDuration);
    });

    // Create Post
    group('Post Creation', function() {
      const postRes = http.post(`${BASE_URL}/posts/`, JSON.stringify({
        content: `Load test post ${Date.now()}`,
      }), {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authToken}`,
        },
        tags: { endpoint: 'posts' },
      });

      const postCreated = check(postRes, {
        'post created': (r) => r.status === 200,
      });

      if (postCreated) {
        postsCreated.add(1);
      }
    });
  }

  sleep(1);
}
```

---

## 📊 Interpreting Results

### Example Output

```
✓ http_req_failed.....................: 0.23%  ✓ 7   ✗ 3000
✓ http_req_duration...................: avg=285ms min=45ms med=245ms max=2.1s p(90)=420ms p(95)=556ms
  { expected_response:true }...........: avg=285ms min=45ms med=245ms max=2.1s p(90)=420ms p(95)=556ms
✓ http_reqs...........................: 3007   100.233/s

✓ checks.............................: 98.50% ✓ 8899 ✗ 135
✗ http_req_duration{endpoint:feed}...: avg=456ms min=120ms med=398ms max=2.1s p(90)=698ms p(95)=856ms
✓ http_req_duration{endpoint:login}..: avg=185ms min=45ms med=165ms max=450ms p(90)=289ms p(95)=345ms

✓ login_errors.......................: 0.11%  ✓ 3   ✗ 2700
✓ feed_load_time.....................: avg=461ms min=125ms med=405ms max=2.15s p(90)=705ms p(95)=865ms
✓ posts_created......................: 2800 counter
```

### What This Tells You

**Overall Health:** ✅ Good

- Error rate: 0.23% (excellent, <1%)
- Average response: 285ms (good, <300ms)
- 95th percentile: 556ms (acceptable, <600ms)

**Specific Findings:**

1. **Login Endpoint:** ✅ Excellent (p95: 345ms)
2. **Feed Endpoint:** ⚠️ Slower (p95: 856ms) - Investigate!
3. **Post Creation:** ✅ Working well (2800 created)

**Recommendations:**

- ✅ System handles 100 req/s with good performance
- ⚠️ Feed endpoint needs optimization (database queries?)
- ✅ Error rate very low
- ✅ Check rate acceptable (98.5%)

---

## 🔍 Analyzing Failed Thresholds

### When a Threshold Fails

```
✗ http_req_duration: avg=1250ms, p(95)=2340ms
  ✗ p(95)<500 - failed
```

**Steps to Debug:**

1. **Identify the endpoint:**

   ```javascript
   // Add tags to track specific endpoints
   http.get(url, { tags: { endpoint: 'feed' }});
   ```

2. **Check specific endpoint metrics:**

   ```
   http_req_duration{endpoint:feed}: avg=2100ms
   ```

   Found it! Feed is slow.

3. **Investigate why:**
   - Check database queries
   - Check N+1 query problems
   - Check missing indexes
   - Profile the code

4. **Fix and retest:**
   - Optimize queries
   - Add caching
   - Add indexes
   - Run k6 again

---

## 📊 Performance Report Template

After running tests, create a report:

```markdown
# Performance Test Results

**Date:** 2024-10-09
**Test:** Load Test (30 VUs, 10 min)
**Environment:** Development (local)

## Summary
- Total Requests: 5,432
- Error Rate: 0.18%
- Avg Response Time: 287ms
- P95 Response Time: 523ms

## Threshold Results
✅ Error rate < 1%
✅ P95 < 600ms
✅ Average < 400ms

## Findings
1. Login endpoint: Excellent (avg 145ms)
2. Feed endpoint: Acceptable (avg 456ms)
3. Post creation: Good (avg 234ms)

## Recommendations
- System ready for 50+ concurrent users
- Consider caching for feed queries
- Monitor error rate in production
```

---

## 🎯 Quick Reference

### Essential K6 Commands

```bash
# Run test
k6 run script.js

# Run with cloud reporting
k6 cloud script.js

# Run and save results
k6 run --out json=results.json script.js

# View summary only
k6 run --summary-export=summary.json script.js

# Set VUs and duration via CLI
k6 run --vus 20 --duration 5m script.js
```

### Environment Variables

```bash
# Set base URL
BASE_URL=http://localhost:8000 k6 run script.js

# In script, use:
const BASE_URL = __ENV.BASE_URL || 'http://localhost:8000';
```

---

## 📚 Related Resources

- [K6 Documentation](https://k6.io/docs/)
- [K6 Thresholds Guide](https://k6.io/docs/using-k6/thresholds/)
- [smoke-test.js](smoke-test.js) - Minimal load test
- [load-test.js](load-test.js) - Normal load test
- [stress-test.js](stress-test.js) - Breaking point test

---

**🎯 Pro Tip:** Start with smoke tests, then load tests, then stress tests. Always establish a performance baseline before making changes!
