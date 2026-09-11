# Testbook Performance Tests

Performance testing suite using K6 for load, stress, and smoke testing.

## Prerequisites

### Install K6

**macOS:**

```bash
brew install k6
```

**Ubuntu/Debian:**

```bash
sudo gpg -k
sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt-get update
sudo apt-get install k6
```

**Windows:**

```bash
choco install k6
```

## Running Tests

### Smoke Test (Minimal Load)

Verifies that critical functionality works with minimal load.

```bash
k6 run smoke-test.js
```

**Configuration:**

- 1 virtual user
- 1 minute duration
- Tests: Health check, authentication, feed, basic operations

### Load Test (Normal Load)

Tests sustained load and identifies performance characteristics.

```bash
k6 run load-test.js
```

**Configuration:**

- Ramps from 0 → 10 → 15 users locally (0 → 5 → 10 in CI)
- ~4.5 minute total duration locally (~2 minutes in CI)
- Simulates realistic user behavior
- Creates posts, views feed, checks profiles

### Stress Test (Breaking Point)

Tests the system beyond normal capacity to find limits.

```bash
k6 run stress-test.js
```

**Configuration:**

- Ramps up to 50 users locally (25 users in CI)
- ~5 minute duration locally (~2.5 minutes in CI)
- More aggressive request patterns
- Identifies breaking point

## Understanding Results

### Key Metrics

**HTTP Request Duration:**

- `avg` - Average response time
- `p(95)` - 95th percentile (95% of requests faster than this)
- `p(99)` - 99th percentile
- `max` - Slowest request

**HTTP Request Failed:**

- `rate` - Percentage of failed requests
- Should be < 1% for smoke tests
- Should be < 5% for load tests
- Can be < 10% for stress tests

**Custom Metrics:**

- `login_duration` - Login endpoint performance
- `feed_duration` - Feed loading performance
- `post_creation_duration` - Post creation performance

### Example Output

```text
✓ health check returns 200
✓ login successful
✓ feed loads successfully

http_req_duration.........: avg=245.3ms  p(95)=456.2ms  p(99)=678.9ms
http_req_failed...........: 0.23%
errors....................: 0.23%
login_duration............: avg=189.4ms  p(95)=298.1ms
feed_duration.............: avg=312.8ms  p(95)=521.3ms
```

## Thresholds

Tests will fail if thresholds are not met:

**Smoke Test:**

- 95% of requests < 500ms
- Error rate < 1%

**Load Test:**

- 95% of requests < 1000ms
- 99% of requests < 2000ms
- Error rate < 5%

**Stress Test:**

- 99% of requests < 3000ms
- Error rate < 10%

### Why These Numbers

These aren't Testbook-specific research — they're standard reference points from web-performance/UX literature (Jakob Nielsen's classic response-time thresholds: under ~0.1s feels instant, under ~1s feels responsive with the user's flow of thought uninterrupted, beyond that the user notices they're waiting). The smoke test's 500ms threshold targets "feels responsive" for a single request under light load — it's meant to catch a regression on every run, so it stays strict. The load test's looser 1000ms/2000ms thresholds and higher error tolerance (5%) reflect that under realistic concurrent traffic, some tail latency is expected and acceptable — the goal is "still usable under load," not "as fast as an idle server." The stress test's 3000ms/10% thresholds mark the point past which the system is considered to be failing under load rather than just slower — stress testing intentionally pushes past normal capacity to find that breaking point, so its thresholds are a "this is too degraded" line, not a target.

If you're adapting these for a real production system, the right numbers depend on your actual users and SLA commitments, not on copying these — treat them as a reasonable teaching default, not a benchmark to defend in a real incident review.

## Custom Configuration

### Change Base URL

```bash
k6 run -e BASE_URL=http://production-server.com/api load-test.js
```

### Run with More VUs

```bash
k6 run --vus 50 --duration 10m load-test.js
```

### Save Results to File

```bash
k6 run --out json=results.json load-test.js
```

### Cloud Testing

```bash
k6 cloud load-test.js
```

## CI/CD Integration

Performance tests run automatically via `.github/workflows/performance-tests.yml`:

- On every push and pull request to `main`/`develop`
- Weekly on a schedule (Sundays at 4 AM UTC)

View results in GitHub Actions artifacts.

## Interpreting Results

### Good Performance

- p(95) < 500ms for most endpoints
- p(99) < 1000ms
- Error rate < 1%
- Consistent performance across load stages

### Performance Issues

- Increasing response times as load increases
- High p(99) values (> 2000ms)
- Error rate > 5%
- Timeouts or connection failures

### What to Test Next

If tests pass:

- Increase VUs (virtual users)
- Increase duration
- Add more complex scenarios

If tests fail:

- Identify bottleneck endpoints
- Check database performance
- Review backend logs
- Optimize slow queries
- Consider caching

## Common Scenarios

### Test Specific Endpoint

```javascript
import http from 'k6/http';

export default function() {
  // Login and get token first
  const loginRes = http.post('http://localhost:8000/api/auth/login', ...);
  const token = loginRes.json('access_token');

  // Test your endpoint
  const res = http.get('http://localhost:8000/api/your-endpoint', {
    headers: { 'Authorization': `Bearer ${token}` }
  });

  check(res, {
    'status is 200': (r) => r.status === 200,
    'duration < 300ms': (r) => r.timings.duration < 300,
  });
}
```

### Test POST Requests

```javascript
const payload = JSON.stringify({
  content: 'Test post'
});

const res = http.post('http://localhost:8000/api/posts/', payload, {
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  }
});
```

## Best Practices

1. **Start small** - Run smoke test before load test
2. **Reset database** - Use `/api/dev/reset` before tests
3. **Monitor backend** - Watch backend logs during tests
4. **Test incrementally** - Increase load gradually
5. **Set realistic thresholds** - Based on your requirements
6. **Test regularly** - Catch performance regressions early
7. **Test production-like environment** - Results differ across environments

## Troubleshooting

### High Error Rates

- Check if backend is running
- Verify database is accessible
- Check for port conflicts
- Review backend error logs

### Slow Response Times

- Check database query performance
- Look for N+1 query problems
- Consider adding indexes
- Review ORM query patterns
- Add caching where appropriate

### Connection Failures

- Increase backend timeout settings
- Check max connections limit
- Verify no firewall blocking
- Check system resources (CPU, RAM)

## Resources

- [K6 Documentation](https://k6.io/docs/)
- [Performance Testing Guide](https://k6.io/docs/testing-guides/api-load-testing/)
- [K6 Cloud](https://k6.io/docs/cloud/)
