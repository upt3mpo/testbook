# Advanced Testing Strategies: Mastering Complex Scenarios

## Introduction

As you progress in your testing career, you'll encounter increasingly complex scenarios that require sophisticated testing strategies. This guide covers advanced strategies for handling complex systems, large-scale testing, and specialized testing scenarios.

## Testing Distributed Systems

### The Challenge

Distributed systems introduce unique testing challenges:

- Multiple services communicating
- Network failures and latency
- Data consistency across services
- Partial system failures
- Complex failure modes

### Strategy 1: Service Isolation Testing

**Principle:** Test each service in isolation with mocked dependencies.

**Benefits:**

- Fast test execution
- Reliable test results
- Easy debugging
- Independent development

**Implementation:**

```python
# Service A tests
def test_service_a_with_mocked_dependencies():
    # Mock service B
    with mock_service_b():
        response = service_a.process_request(request)
        assert response.success is True

# Service B tests
def test_service_b_with_mocked_dependencies():
    # Mock service A
    with mock_service_a():
        response = service_b.process_request(request)
        assert response.success is True
```

### Strategy 2: Contract Testing

**Principle:** Test the contracts between services to ensure compatibility.

**Benefits:**

- Prevents integration failures
- Enables independent deployment
- Reduces coupling
- Faster feedback

**Implementation:**

```python
# Consumer contract test
def test_user_service_contract():
    pact = Consumer('UserService').has_pact_with(Provider('UserAPI'))

    (pact
     .given('user exists')
     .upon_receiving('a request for user')
     .with_request('GET', '/users/123')
     .will_respond_with(200, body={
         'id': 123,
         'name': 'John Doe',
         'email': 'john@example.com'
     }))

    with pact:
        response = requests.get('http://localhost:8080/users/123')
        assert response.status_code == 200
```

### Strategy 3: Integration Testing

**Principle:** Test services together with real dependencies.

**Benefits:**

- Tests real interactions
- Catches integration bugs
- Validates end-to-end behavior
- Tests failure scenarios

**Implementation:**

```python
def test_user_registration_flow():
    # Test complete flow with real services
    with test_environment():
        # Register user
        response = register_user("test@example.com")
        assert response.success is True

        # Verify user in database
        user = get_user("test@example.com")
        assert user is not None

        # Verify email sent
        assert email_sent("test@example.com")
```

### Strategy 4: Chaos Engineering

**Principle:** Intentionally introduce failures to test system resilience.

**Benefits:**

- Proves system resilience
- Identifies weak points
- Improves recovery procedures
- Builds confidence

**Implementation:**

```python
def test_system_resilience():
    # Normal operation
    def normal_operation():
        while True:
            response = process_request()
            assert response.success is True
            time.sleep(0.1)

    # Chaos monkey
    def chaos_monkey():
        while True:
            time.sleep(random.uniform(1, 5))
            if random.random() < 0.1:
                simulate_network_failure()
            elif random.random() < 0.1:
                simulate_database_failure()

    # Run both concurrently
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(normal_operation)
        executor.submit(chaos_monkey)
```

## Testing Microservices

### The Challenge

Microservices introduce additional complexity:

- Service discovery
- Load balancing
- Circuit breakers
- Distributed tracing
- Event-driven architecture

### Strategy 1: Service Mesh Testing

**Principle:** Test the service mesh infrastructure and communication.

**Benefits:**

- Tests service discovery
- Validates load balancing
- Tests circuit breakers
- Tests distributed tracing

**Implementation:**

```python
def test_service_mesh():
    # Test service discovery
    service = discover_service('user-service')
    assert service is not None

    # Test load balancing
    responses = []
    for _ in range(10):
        response = service.handle_request()
        responses.append(response.instance_id)

    # Should hit multiple instances
    assert len(set(responses)) > 1

    # Test circuit breaker
    with simulate_service_failure('user-service'):
        response = service.handle_request()
        assert response.circuit_breaker_open is True
```

### Strategy 2: Event-Driven Testing

**Principle:** Test event-driven communication between services.

**Benefits:**

- Tests event publishing
- Tests event consumption
- Tests event ordering
- Tests event processing

**Implementation:**

```python
def test_event_driven_communication():
    # Publish event
    event = UserCreatedEvent(user_id=123, email="test@example.com")
    event_bus.publish(event)

    # Wait for event processing
    time.sleep(1)

    # Verify event was processed
    assert email_service.email_sent("test@example.com")
    assert notification_service.notification_sent(123)
    assert audit_service.event_logged(event)
```

### Strategy 3: Database Testing

**Principle:** Test database operations and data consistency.

**Benefits:**

- Tests data integrity
- Tests transactions
- Tests migrations
- Tests performance

**Implementation:**

```python
def test_database_operations():
    with database_transaction():
        # Create user
        user = create_user("test@example.com")
        assert user.id is not None

        # Create profile
        profile = create_profile(user.id, "John Doe")
        assert profile.user_id == user.id

        # Verify data consistency
        user_with_profile = get_user_with_profile(user.id)
        assert user_with_profile.profile is not None
        assert user_with_profile.profile.name == "John Doe"
```

## Testing Large-Scale Systems

### The Challenge

Large-scale systems present unique challenges:

- High traffic volumes
- Complex data flows
- Multiple failure modes
- Performance requirements
- Scalability concerns

### Strategy 1: Load Testing

**Principle:** Test system behavior under expected load.

**Benefits:**

- Identifies performance bottlenecks
- Validates performance requirements
- Tests scalability
- Prevents performance regressions

**Implementation:**

```javascript
// k6 load test
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

### Strategy 2: Stress Testing

**Principle:** Test system behavior beyond normal capacity.

**Benefits:**

- Identifies breaking points
- Tests failure handling
- Validates recovery procedures
- Tests resource limits

**Implementation:**

```python
def test_system_stress():
    # Gradually increase load until system breaks
    for load in range(100, 1000, 100):
        with simulate_load(load):
            response = process_request()
            if response.success is False:
                print(f"System broke at load: {load}")
                break

    # Test recovery
    with simulate_load(50):
        response = process_request()
        assert response.success is True
```

### Strategy 3: End-to-End Testing

**Principle:** Test complete user workflows across all services.

**Benefits:**

- Tests real user scenarios
- Validates system integration
- Tests business workflows
- Tests error handling

**Implementation:**

```python
def test_complete_user_journey():
    # User registration
    response = register_user("test@example.com")
    assert response.success is True
    user_id = response.user_id

    # User login
    response = login_user("test@example.com", "password")
    assert response.success is True
    token = response.token

    # Create post
    response = create_post(token, "Hello World")
    assert response.success is True
    post_id = response.post_id

    # View post
    response = get_post(post_id)
    assert response.success is True
    assert response.post.content == "Hello World"

    # Delete post
    response = delete_post(token, post_id)
    assert response.success is True
```

## Testing Real-Time Systems

### The Challenge

Real-time systems require special testing approaches:

- Timing constraints
- Concurrency issues
- Race conditions
- Performance requirements
- Reliability requirements

### Strategy 1: Timing Testing

**Principle:** Test that operations complete within required time limits.

**Benefits:**

- Validates timing requirements
- Identifies performance issues
- Tests real-time constraints
- Prevents timing bugs

**Implementation:**

```python
def test_timing_requirements():
    start_time = time.time()

    # Perform operation
    result = process_real_time_request()

    end_time = time.time()
    duration = end_time - start_time

    # Must complete within 100ms
    assert duration < 0.1
    assert result.success is True
```

### Strategy 2: Concurrency Testing

**Principle:** Test system behavior under concurrent access.

**Benefits:**

- Tests race conditions
- Tests thread safety
- Tests deadlock prevention
- Tests resource sharing

**Implementation:**

```python
def test_concurrency():
    results = []

    def worker():
        result = process_request()
        results.append(result)

    # Start 100 concurrent workers
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(worker) for _ in range(100)]

        # Wait for all to complete
        for future in futures:
            future.result()

    # All should succeed
    assert all(result.success for result in results)
    assert len(results) == 100
```

### Strategy 3: Race Condition Testing

**Principle:** Test for race conditions and timing-dependent bugs.

**Benefits:**

- Identifies race conditions
- Tests synchronization
- Tests atomic operations
- Prevents timing bugs

**Implementation:**

```python
def test_race_conditions():
    counter = 0

    def increment():
        nonlocal counter
        # Simulate race condition
        temp = counter
        time.sleep(0.001)  # Small delay
        counter = temp + 1

    # Start multiple threads
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(increment) for _ in range(10)]

        # Wait for all to complete
        for future in futures:
            future.result()

    # Counter should be 10 (no race condition)
    assert counter == 10
```

## Testing Machine Learning Systems

### The Challenge

Machine Learning systems introduce unique testing challenges:

- Non-deterministic behavior
- Data quality issues
- Model drift
- Performance degradation
- Bias and fairness

### Strategy 1: Data Quality Testing

**Principle:** Test the quality and consistency of training and test data.

**Benefits:**

- Prevents data quality issues
- Tests data preprocessing
- Validates data pipelines
- Ensures data consistency

**Implementation:**

```python
def test_data_quality():
    # Load training data
    data = load_training_data()

    # Test data completeness
    assert data.isnull().sum().sum() == 0

    # Test data types
    assert data.dtypes['age'] == 'int64'
    assert data.dtypes['name'] == 'object'

    # Test data ranges
    assert data['age'].min() >= 0
    assert data['age'].max() <= 120

    # Test data distribution
    assert data['age'].mean() > 0
    assert data['age'].std() > 0
```

### Strategy 2: Model Performance Testing

**Principle:** Test model performance and accuracy.

**Benefits:**

- Validates model accuracy
- Tests performance metrics
- Prevents model degradation
- Ensures model quality

**Implementation:**

```python
def test_model_performance():
    # Load test data
    X_test, y_test = load_test_data()

    # Load model
    model = load_model()

    # Make predictions
    y_pred = model.predict(X_test)

    # Test accuracy
    accuracy = accuracy_score(y_test, y_pred)
    assert accuracy > 0.9

    # Test precision
    precision = precision_score(y_test, y_pred)
    assert precision > 0.8

    # Test recall
    recall = recall_score(y_test, y_pred)
    assert recall > 0.8
```

### Strategy 3: Model Drift Testing

**Principle:** Test for model drift and performance degradation.

**Benefits:**

- Detects model drift
- Prevents performance degradation
- Tests model stability
- Ensures model reliability

**Implementation:**

```python
def test_model_drift():
    # Load current model
    current_model = load_current_model()

    # Load new data
    new_data = load_new_data()

    # Make predictions
    predictions = current_model.predict(new_data)

    # Test for drift
    drift_score = calculate_drift_score(predictions)
    assert drift_score < 0.1  # Threshold for drift

    # Test performance
    performance = calculate_performance(predictions)
    assert performance > 0.8  # Minimum performance
```

## Testing Security-Critical Systems

### The Challenge

Security-critical systems require specialized testing approaches:

- Security vulnerabilities
- Attack vectors
- Compliance requirements
- Data protection
- Access control

### Strategy 1: Vulnerability Testing

**Principle:** Test for common security vulnerabilities.

**Benefits:**

- Identifies security issues
- Tests attack vectors
- Validates security controls
- Prevents security breaches

**Implementation:**

```python
def test_security_vulnerabilities():
    # Test SQL injection
    response = requests.post('/api/users', json={
        'email': "'; DROP TABLE users; --"
    })
    assert response.status_code == 400

    # Test XSS
    response = requests.post('/api/posts', json={
        'content': '<script>alert("XSS")</script>'
    })
    assert '<script>' not in response.text

    # Test CSRF
    response = requests.post('/api/users', json={
        'email': 'test@example.com'
    })
    assert response.status_code == 403  # CSRF protection
```

### Strategy 2: Penetration Testing

**Principle:** Test system security through simulated attacks.

**Benefits:**

- Tests real attack scenarios
- Identifies security weaknesses
- Validates security controls
- Tests incident response

**Implementation:**

```python
def test_penetration_scenarios():
    # Test brute force attack
    for i in range(100):
        response = login_user("admin", f"password{i}")
        if response.success:
            assert i > 10  # Should require many attempts

    # Test privilege escalation
    response = get_admin_data(user_token="regular_user_token")
    assert response.status_code == 403

    # Test data exfiltration
    response = export_user_data(user_id="*")
    assert response.status_code == 403
```

### Strategy 3: Compliance Testing

**Principle:** Test compliance with security standards and regulations.

**Benefits:**

- Ensures compliance
- Tests security controls
- Validates data protection
- Prevents regulatory issues

**Implementation:**

```python
def test_gdpr_compliance():
    # Test data deletion
    response = delete_user_data(user_id=123)
    assert response.success is True

    # Verify data is deleted
    response = get_user_data(user_id=123)
    assert response.status_code == 404

    # Test data portability
    response = export_user_data(user_id=123)
    assert response.success is True
    assert 'email' in response.data
    assert 'name' in response.data
```

## Conclusion

Advanced testing strategies are essential for handling complex systems and scenarios. The key is to choose the right strategies for your specific needs and gradually incorporate them into your testing approach.

Remember: advanced testing is not about using every strategy, but about using the right strategies for your specific situation and requirements. Start with one strategy, master it, and then move on to others.

The most important thing is to continuously learn and adapt your testing strategies as your systems and requirements evolve.

---

## Further Reading

- [Advanced Topics](ADVANCED_TOPICS.md) - Advanced testing techniques
- [Industry Practices](../industry/INDUSTRY_PRACTICES.md) - How companies use advanced strategies
- [Case Studies](../industry/CASE_STUDIES.md) - Real-world examples of advanced testing
- [Testing Philosophy](../concepts/TESTING_PHILOSOPHY.md) - The mindset behind advanced testing
