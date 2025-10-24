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

### Example: Mutation Testing in Python

**Original Code:**

```python
def calculate_discount(price, discount_rate):
    if price > 0 and discount_rate > 0:
        return price * discount_rate
    return 0
```

**Test:**

```python
def test_calculate_discount():
    result = calculate_discount(100, 0.1)
    assert result == 10
```

**Mutation 1: Change `>` to `>=`**

```python
def calculate_discount(price, discount_rate):
    if price >= 0 and discount_rate > 0:  # Changed > to >=
        return price * discount_rate
    return 0
```

**Result:** Test still passes, but behavior changed! Mutation survived.

**Better Test:**

```python
def test_calculate_discount():
    result = calculate_discount(100, 0.1)
    assert result == 10

def test_calculate_discount_zero_price():
    result = calculate_discount(0, 0.1)
    assert result == 0

def test_calculate_discount_negative_rate():
    result = calculate_discount(100, -0.1)
    assert result == 0
```

**Result:** All mutations are killed. Test quality is high.

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

### What is Contract Testing?

Contract testing verifies that services can communicate correctly by checking the contracts between them.

**Types of Contracts:**

- **API Contracts:** Request/response formats
- **Message Contracts:** Event schemas
- **Database Contracts:** Data formats

### Why Use Contract Testing?

**Benefits:**

- Prevents integration failures
- Enables independent deployment
- Reduces coupling between services
- Faster feedback

**Example: API Contract Testing**

```python
from pact import Consumer, Provider

def test_user_service_contract():
    # Define the contract
    pact = Consumer('UserService').has_pact_with(Provider('UserAPI'))

    # Define expected interaction
    (pact
     .given('user exists')
     .upon_receiving('a request for user')
     .with_request('GET', '/users/123')
     .will_respond_with(200, body={
         'id': 123,
         'name': 'John Doe',
         'email': 'john@example.com'
     }))

    # Test the contract
    with pact:
        response = requests.get('http://localhost:8080/users/123')
        assert response.status_code == 200
        assert response.json()['id'] == 123
```

### Tools for Contract Testing

**Popular Tools:**

- `Pact` - Most popular
- `Spring Cloud Contract` - Java/Spring
- `Pacto` - Ruby
- `Pact-JS` - JavaScript

### When to Use Contract Testing

**Good Use Cases:**

- Microservices
- API-first development
- Service-oriented architecture
- Independent deployment

**Not Ideal For:**

- Monolithic applications
- Tightly coupled services
- Simple applications
- Prototype projects

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

- [Industry Practices](../industry/INDUSTRY_PRACTICES.md) - How companies use advanced techniques
- [Case Studies](../industry/CASE_STUDIES.md) - Real-world examples of advanced testing
- [Tool Comparison](../industry/TOOL_COMPARISON.md) - Tools for advanced testing
- [Testing Philosophy](../concepts/TESTING_PHILOSOPHY.md) - The mindset behind advanced testing
