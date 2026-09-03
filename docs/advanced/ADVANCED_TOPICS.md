# Advanced Testing Topics: Beyond the Basics

## Introduction

Once you've mastered the fundamentals of testing, it's time to explore advanced topics that can take your testing skills to the next level. These topics are typically encountered in senior roles, complex projects, or specialized testing scenarios.

## Mutation Testing

### What is Mutation Testing?

Mutation testing is a technique for evaluating the quality of your test suite by introducing small changes (mutations) to your code and checking if your tests catch these changes.

**The Process:**

1. Create a copy of your code
2. Introduce a small change (mutation)
3. Run your tests
4. If tests fail, the mutation is "killed"
5. If tests pass, the mutation "survived"
6. High mutation score = good test quality

### Why Use Mutation Testing?

**Traditional Coverage Limitations:**

- 100% line coverage doesn't guarantee good tests
- Tests might not actually verify behavior
- Coverage metrics can be misleading

**Mutation Testing Benefits:**

- Tests the quality of your tests
- Identifies weak or ineffective tests
- Provides better confidence in test suite
- Helps improve test design

### A Worked Example: Mutating Testbook's Own Auth Code

The process above is the idea in outline. Here's what it looks like against
a real file in this repo, with real output, not a constructed scenario.

**The command:**

```bash
cd backend
pip install "mutmut<3"  # pinned - mutmut 3.x has a different CLI/config
                         # interface (setup.cfg-based source_paths instead
                         # of --paths-to-mutate); 2.x is what this example
                         # was run against
mutmut run --paths-to-mutate=auth.py \
  --runner="python -m pytest tests/unit/test_auth.py -x -q" \
  --test-time-multiplier=2.0
mutmut results
mutmut show <id>  # for any specific mutant
```

The `--runner` points at `tests/unit/test_auth.py` specifically, not the
whole backend suite - mutation testing reruns the test command once per
mutant, so scoping to a fast, self-contained file (no database, no HTTP
client) keeps a 47-mutant run down to about a minute instead of tying it
to the full suite's ~50-second runtime per mutant.

**Real output, first run:** 47 mutants generated, 35 survived, 12 killed.
Every one of the 35 survivors was inside `get_current_user` or
`get_optional_user` - both are FastAPI dependencies that need a request's
credentials and a database session to run, and `tests/unit/test_auth.py`
never called them directly. They're covered, but only indirectly, through
`tests/integration/test_api_auth.py` hitting real endpoints - coverage
that's real but invisible to a mutation run scoped to the unit suite for
speed.

**One real surviving mutant (id 40):**

```diff
     user = db.query(models.User).filter(models.User.email == email).first()
-    if user is None:
+    if user is not None:
         raise credentials_exception

     return user
```

This is `mutmut show 40`'s actual diff, not a constructed example. mutmut
flipped `is None` to `is not None` - and every test in the unit suite still
passed, because nothing in that file called `get_current_user` at all.

**What this mutant means:** if this were the real code, a request with a
valid token for a user who exists would be *rejected* (the found-user
branch now raises), and a token for a deleted or nonexistent user would
be silently *accepted* as authenticated (the not-found branch now returns
`user`, which is `None`, instead of raising). That's an inverted
authentication check landing in production undetected by the unit suite -
exactly the class of bug mutation testing exists to surface, and exactly
the kind that a coverage percentage alone would never reveal, since these
lines were "covered" by the integration suite the whole time.

**The test written to kill it**, added to `tests/unit/test_auth.py`:

```python
class TestGetCurrentUser:
    def test_returns_the_user_when_one_is_found(self):
        email = "test@example.com"
        token = create_access_token(data={"sub": email})
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)

        found_user = MagicMock()
        mock_db = MagicMock()
        mock_db.query.return_value.filter.return_value.first.return_value = found_user

        result = get_current_user(credentials=credentials, db=mock_db)

        assert result is found_user

    def test_raises_401_when_no_user_matches_the_token(self):
        token = create_access_token(data={"sub": "nonexistent@example.com"})
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)

        mock_db = MagicMock()
        mock_db.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            get_current_user(credentials=credentials, db=mock_db)

        assert exc_info.value.status_code == 401
```

No FastAPI app, no HTTP client, no real database - just the function
called directly with a mocked `Session` and a token built by the same
`create_access_token` the app itself uses. That's what makes it a unit
test rather than a slower integration test re-run.

**Real output, second run**, after adding those two tests: 47 mutants, 27
survived (down from 35), 20 killed (up from 12). Mutant 40 is no longer
in the survivors list - both new tests fail against it (the first because
it would raise where it should return; the second because it would
return `None` where it should raise), so either one alone would have
killed it.

**What's still unresolved:** the other 27 survivors are still inside
`get_current_user`/`get_optional_user` - things like mutating the string
`"Could not validate credentials"` or the `"sub"` dict key, which the
integration suite's status-code assertions don't distinguish from a
correctly-worded 401. Closing that gap fully would mean either writing
several more targeted unit tests like the two above, or accepting that
some of it is adequately covered by integration tests and not worth
duplicating at the unit level - a real trade-off, not laziness, and
exactly the kind of judgment call mutation testing is for surfacing in
the first place rather than resolving automatically.

### Tools for Mutation Testing

**Python:**

- `mutmut` - Simple and fast
- `cosmic-ray` - More features
- `mutpy` - Academic tool

**JavaScript:**

- `Stryker` - Comprehensive tool
- `mutant` - Simple tool

**Java:**

- `PIT` - Most popular
- `Major` - Academic tool

### When to Use Mutation Testing

**Good Use Cases:**

- Critical business logic
- Safety-critical systems
- When test quality is crucial
- Learning about test design

**Not Ideal For:**

- Simple CRUD operations
- Generated code
- Legacy code with poor tests
- Time-constrained projects

## Property-Based Testing

### What is Property-Based Testing?

Property-based testing generates random inputs and verifies that certain properties always hold true, rather than testing specific examples.

**Traditional Example-Based Testing:**

```python
def test_reverse_list():
    assert reverse([1, 2, 3]) == [3, 2, 1]
    assert reverse([1]) == [1]
    assert reverse([]) == []
```

**Property-Based Testing:**

```python
from hypothesis import given, strategies as st

@given(st.lists(st.integers()))
def test_reverse_properties(lst):
    # Property 1: Double reverse equals original
    assert reverse(reverse(lst)) == lst

    # Property 2: Length is preserved
    assert len(reverse(lst)) == len(lst)

    # Property 3: First element becomes last
    if lst:
        assert reverse(lst)[-1] == lst[0]
```

### Why Use Property-Based Testing?

**Benefits:**

- Tests many more cases than examples
- Discovers edge cases automatically
- Verifies mathematical properties
- Reduces test maintenance

**Example Discovery:**

```python
@given(st.lists(st.integers()))
def test_sort_properties(lst):
    sorted_lst = sort(lst)

    # Property 1: Result is sorted
    assert all(sorted_lst[i] <= sorted_lst[i+1]
              for i in range(len(sorted_lst)-1))

    # Property 2: Length is preserved
    assert len(sorted_lst) == len(lst)

    # Property 3: All elements are preserved
    assert set(sorted_lst) == set(lst)
```

### Tools for Property-Based Testing

**Python:**

- `hypothesis` - Most popular
- `fast-check` - Alternative

**JavaScript:**

- `fast-check` - Most popular
- `jsverify` - Alternative

**Java:**

- `jqwik` - Modern tool
- `quickcheck` - Original tool

### When to Use Property-Based Testing

**Good Use Cases:**

- Mathematical algorithms
- Data transformation functions
- Serialization/deserialization
- Complex business logic

**Not Ideal For:**

- Simple CRUD operations
- UI testing
- Integration testing
- Performance testing

## Fuzzing

### What is Fuzzing?

Fuzzing is a technique for finding bugs by providing random, invalid, or unexpected inputs to a program.

**Types of Fuzzing:**

- **Dumb Fuzzing:** Random data
- **Smart Fuzzing:** Structured data based on format
- **Coverage-Guided Fuzzing:** Uses coverage to guide input generation

### Why Use Fuzzing?

**Benefits:**

- Finds crashes and security vulnerabilities
- Tests with real-world data
- Discovers edge cases
- Automated bug finding

**Example: Fuzzing a Parser**

```python
import random
import string

def fuzz_parser():
    for _ in range(1000):
        # Generate random input
        input_data = ''.join(random.choices(
            string.ascii_letters + string.digits + ' \n\t',
            k=random.randint(0, 1000)
        ))

        try:
            result = parse(input_data)
            # Verify result is valid
            assert validate(result)
        except Exception as e:
            # Log interesting failures
            if "segmentation fault" in str(e):
                print(f"Crash found: {input_data[:100]}")
```

### Tools for Fuzzing

**General Purpose:**

- `AFL` (American Fuzzy Lop) - Most popular
- `libFuzzer` - Google's tool
- `honggfuzz` - High performance

**Language-Specific:**

- `python-afl` - Python fuzzing
- `go-fuzz` - Go fuzzing
- `cargo-fuzz` - Rust fuzzing

**Web Application:**

- `wfuzz` - Web fuzzer
- `ffuf` - Fast web fuzzer
- `Burp Suite` - Professional tool

### When to Use Fuzzing

**Good Use Cases:**

- Security testing
- Parser testing
- Protocol testing
- File format testing

**Not Ideal For:**

- Business logic testing
- UI testing
- Integration testing
- Performance testing

## Chaos Engineering

### What is Chaos Engineering?

Chaos engineering is the practice of intentionally introducing failures into a system to test its resilience and ability to recover.

**The Process:**

1. Define steady state
2. Form hypothesis
3. Introduce chaos
4. Verify system behavior
5. Learn and improve

### Why Use Chaos Engineering?

**Benefits:**

- Proves system resilience
- Identifies weak points
- Improves recovery procedures
- Builds confidence

**Example: Chaos Testing a Microservice**

```python
import random
import time
from concurrent.futures import ThreadPoolExecutor

def chaos_test_microservice():
    service = Microservice()

    def normal_operation():
        while True:
            try:
                response = service.handle_request()
                assert response.success
                time.sleep(0.1)
            except Exception as e:
                print(f"Normal operation failed: {e}")

    def chaos_monkey():
        while True:
            time.sleep(random.uniform(1, 5))
            # Randomly break things
            if random.random() < 0.1:
                service.simulate_network_failure()
            elif random.random() < 0.1:
                service.simulate_database_failure()
            elif random.random() < 0.1:
                service.simulate_memory_leak()

    # Run both operations concurrently
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(normal_operation)
        executor.submit(chaos_monkey)
```

### Tools for Chaos Engineering

**Kubernetes:**

- `Chaos Monkey` - Netflix's tool
- `Chaos Mesh` - CNCF project
- `Litmus` - Kubernetes-native

**AWS:**

- `AWS Fault Injection Simulator` - AWS service
- `Chaos Monkey for AWS` - Netflix's tool

**General:**

- `Chaos Toolkit` - Language-agnostic
- `Gremlin` - Commercial tool

### When to Use Chaos Engineering

**Good Use Cases:**

- Distributed systems
- Microservices
- High-availability systems
- Production systems

**Not Ideal For:**

- Simple applications
- Development environments
- Systems without monitoring
- Untested systems

## Contract Testing

Contract testing verifies that services can communicate correctly by checking the contracts between them (a consumer's expectations against a provider's actual API), commonly with tools like Pact or, for property-based contract checking against an OpenAPI spec, Schemathesis. See [Contract Testing Guide](../guides/CONTRACT_TESTING.md) for the full explanation, a worked Schemathesis example against this repo's own API, and a comparison against integration testing.

## Visual Testing

### What is Visual Testing?

Visual testing verifies that the visual appearance of an application is correct by comparing screenshots or visual elements.

**Types of Visual Testing:**

- **Screenshot Testing:** Compare full page screenshots
- **Element Testing:** Compare specific elements
- **Layout Testing:** Verify positioning and sizing

### Why Use Visual Testing?

**Benefits:**

- Catches visual regressions
- Tests across browsers and devices
- Validates design implementation
- Automated visual validation

**Example: Visual Testing with Playwright**

```python
def test_homepage_visual():
    page = browser.new_page()
    page.goto('http://localhost:3000')

    # Take screenshot
    page.screenshot(path='homepage.png')

    # Compare with baseline
    assert page.screenshot() == baseline_screenshot

    # Test specific element
    header = page.locator('header')
    assert header.screenshot() == header_baseline
```

### Tools for Visual Testing

**Popular Tools:**

- `Percy` - Most popular
- `Chromatic` - Storybook integration
- `Applitools` - AI-powered
- `Playwright` - Built-in visual testing

### When to Use Visual Testing

**Good Use Cases:**

- Design-heavy applications
- Marketing websites
- UI component libraries
- Cross-browser testing

**Not Ideal For:**

- API-only applications
- Backend services
- Data-heavy applications
- Prototype projects

## Performance Testing

### What is Performance Testing?

Performance testing verifies that an application meets performance requirements under various conditions.

**Types of Performance Testing:**

- **Load Testing:** Normal expected load
- **Stress Testing:** Beyond normal capacity
- **Spike Testing:** Sudden load increases
- **Volume Testing:** Large amounts of data

### Why Use Performance Testing?

**Benefits:**

- Identifies performance bottlenecks
- Validates performance requirements
- Prevents performance regressions
- Optimizes resource usage

**Example: Load Testing with k6**

```javascript
import http from "k6/http";
import { check } from "k6";

export let options = {
  stages: [
    { duration: "2m", target: 100 }, // Ramp up
    { duration: "5m", target: 100 }, // Stay at 100 users
    { duration: "2m", target: 200 }, // Ramp up to 200
    { duration: "5m", target: 200 }, // Stay at 200
    { duration: "2m", target: 0 }, // Ramp down
  ],
};

export default function () {
  let response = http.get("http://localhost:3000/api/users");

  check(response, {
    "status is 200": (r) => r.status === 200,
    "response time < 500ms": (r) => r.timings.duration < 500,
    "response time < 1000ms": (r) => r.timings.duration < 1000,
  });
}
```

### Tools for Performance Testing

**Popular Tools:**

- `k6` - Modern and developer-friendly
- `JMeter` - Mature and feature-rich
- `Gatling` - Scala-based
- `Artillery` - Node.js-based

### When to Use Performance Testing

**Good Use Cases:**

- High-traffic applications
- Real-time systems
- Resource-constrained environments
- Performance-critical features

**Not Ideal For:**

- Simple applications
- Prototype projects
- Internal tools
- Low-traffic applications

## Security Testing

### What is Security Testing?

Security testing identifies vulnerabilities and security weaknesses in an application.

**Types of Security Testing:**

- **Static Analysis:** Code analysis
- **Dynamic Analysis:** Runtime testing
- **Penetration Testing:** Manual testing
- **Vulnerability Scanning:** Automated scanning

### Why Use Security Testing?

**Benefits:**

- Identifies security vulnerabilities
- Prevents security breaches
- Ensures compliance
- Protects user data

**Example: Security Testing with OWASP ZAP**

```python
import requests
from zapv2 import ZAPv2

def test_security_vulnerabilities():
    zap = ZAPv2(proxies={'http': 'http://127.0.0.1:8080'})

    # Start scanning
    zap.urlopen('http://localhost:3000')
    zap.spider.scan('http://localhost:3000')

    # Wait for spider to complete
    while int(zap.spider.status()) < 100:
        time.sleep(2)

    # Start active scan
    zap.ascan.scan('http://localhost:3000')

    # Wait for scan to complete
    while int(zap.ascan.status()) < 100:
        time.sleep(2)

    # Get results
    alerts = zap.core.alerts()

    # Check for high-risk vulnerabilities
    high_risk = [alert for alert in alerts if alert['risk'] == 'High']
    assert len(high_risk) == 0, f"Found {len(high_risk)} high-risk vulnerabilities"
```

### Tools for Security Testing

**Popular Tools:**

- `OWASP ZAP` - Free and open source
- `Burp Suite` - Professional tool
- `Nessus` - Vulnerability scanner
- `SonarQube` - Code analysis

### When to Use Security Testing

**Good Use Cases:**

- Public-facing applications
- Financial applications
- Healthcare applications
- Applications handling sensitive data

**Not Ideal For:**

- Internal tools
- Prototype projects
- Simple applications
- Non-sensitive applications

## Conclusion

Advanced testing topics provide powerful tools for ensuring software quality in complex scenarios. While these techniques require more expertise and time to implement, they can significantly improve the reliability, security, and performance of your applications.

The key is to choose the right advanced techniques for your specific needs and gradually incorporate them into your testing strategy. Start with one technique, master it, and then move on to others.

Remember: advanced testing is not about using every technique, but about using the right techniques for your specific situation and requirements.

---

## Further Reading

- [Case Studies](../industry/CASE_STUDIES.md) - Real incidents and what's genuinely documented about industry practice
- [Case Studies](../industry/CASE_STUDIES.md) - Real-world examples of advanced testing
- [Tool Comparison](../industry/TOOL_COMPARISON.md) - Tools for advanced testing
- [Testing Philosophy](../concepts/TESTING_PHILOSOPHY.md) - The mindset behind advanced testing
