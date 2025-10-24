# 🧪 Lab 6: Component Testing with Vitest

**Estimated Time:** 120 minutes<br>
**Difficulty:** Advanced<br>
**Language:** 🟨 JavaScript/React<br>
**Prerequisites:** Lab 5 completed

**💡 Need Python instead?** Try [Lab 6: Advanced API Testing (Python)](LAB_06_Advanced_API_Testing_Python.md)!

**What This Adds:** Master React component testing with Vitest and React Testing Library - learn to test user interactions, component state, and API integration. This bridges unit tests and E2E tests.

---

## 🎯 What You'll Learn

- Test React components with Vitest + React Testing Library
- Render components and query elements
- Simulate user interactions (clicks, typing, etc.)
- Test component state and props
- Test component integration with APIs
- Test accessibility and user experience

---

## 💡 Why Component Testing Matters

**The Problem:** Unit tests test individual functions, but users interact with components!

```javascript
// Unit test - tests the function
function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price, 0);
}

// Component test - tests the user experience
function ShoppingCart({ items }) {
  const total = calculateTotal(items);
  return <div>Total: ${total}</div>;
}
```

**The Solution:** Component tests verify the complete user experience!

---

## 📋 Step-by-Step Instructions

### Step 1: Explore Existing Component Tests (15 minutes)

**Open:** `frontend/src/tests/unit/CreatePost.test.jsx`

**This is a real component test! Let's understand it:**

```javascript
/**
 * Component Testing Setup - CreatePost Component
 *
 * This file demonstrates how to set up comprehensive component tests
 * using Vitest, React Testing Library, and proper mocking strategies.
 */

import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import { beforeEach, describe, expect, it, vi } from "vitest";
import * as api from "../../api";
import { AuthContext } from "../../AuthContext";
import CreatePost from "../../components/CreatePost";

// Mock the API module to control its behavior in tests
// This prevents real API calls during testing
vi.mock("../../api", () => ({
  postsAPI: {
    createPost: vi.fn(), // Mock function for creating posts
    uploadMedia: vi.fn(), // Mock function for uploading media
  },
}));

/**
 * Helper function to render CreatePost component with all required providers
 *
 * This function sets up the component with:
 * - Mock authentication context
 * - Browser router for navigation
 * - Default props for testing
 *
 * @param {Object} props - Additional props to pass to CreatePost component
 * @returns {Object} - Render result from React Testing Library
 */
const renderCreatePost = (props = {}) => {
  // Create mock authentication context
  // This simulates a logged-in user for testing
  const mockAuth = {
    user: {
      id: 1, // User ID for testing
      username: "testuser", // Username for testing
      display_name: "Test User", // Display name for testing
    },
    login: vi.fn(), // Mock login function
    logout: vi.fn(), // Mock logout function
  };

  // Default props that the component expects
  const defaultProps = {
    onPostCreated: vi.fn(), // Mock callback for when post is created
  };

  // Render the component wrapped in all required providers
  return render(
    <BrowserRouter
      future={{
        v7_startTransition: true, // Enable React 18 concurrent features
        v7_relativeSplatPath: true, // Enable new routing features
      }}
    >
      <AuthContext.Provider value={mockAuth}>
        <CreatePost {...defaultProps} {...props} />
      </AuthContext.Provider>
    </BrowserRouter>
  );
};
```

**Key concepts:**

1. **Mocking dependencies** - `vi.mock('../../api')`
2. **Test utilities** - `render`, `screen`, `fireEvent`
3. **Provider setup** - Wrapping with `AuthContext.Provider`
4. **Helper functions** - `renderCreatePost()` for consistent setup

✅ **Checkpoint:** You understand the component test structure

### Step 2: Run the Component Tests (10 minutes)

```bash
cd frontend
npm test CreatePost.test.jsx
```

**You should see:**

```text
✓ CreatePost.test.jsx (7)
  ✓ CreatePost Component (7)
    ✓ renders the textarea input
    ✓ renders the Post button
    ✓ allows user to type in the textarea
    ✓ disables Post button when textarea is empty
    ✓ enables Post button when textarea has content
    ✓ calls onPostCreated when post is submitted successfully
    ✓ clears textarea after successful post submission
```

✅ **Checkpoint:** All component tests pass!

### Step 3: Write Your First Component Test (20 minutes)

**Create:** `frontend/src/tests/unit/Button.test.jsx`

```javascript
import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";

// Simple Button component for testing
function Button({ children, onClick, disabled = false, variant = "primary" }) {
  const baseClasses = "px-4 py-2 rounded font-medium";
  const variantClasses = {
    primary: "bg-blue-500 text-white hover:bg-blue-600",
    secondary: "bg-gray-500 text-white hover:bg-gray-600",
    danger: "bg-red-500 text-white hover:bg-red-600",
  };

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`${baseClasses} ${variantClasses[variant]}`}
    >
      {children}
    </button>
  );
}

describe("Button Component", () => {
  it("should render button with text", () => {
    // Arrange & Act
    render(<Button>Click me</Button>);

    // Assert
    expect(
      screen.getByRole("button", { name: "Click me" })
    ).toBeInTheDocument();
  });

  it("should call onClick when clicked", () => {
    // Arrange
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click me</Button>);

    // Act
    fireEvent.click(screen.getByRole("button"));

    // Assert
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it("should be disabled when disabled prop is true", () => {
    // Arrange & Act
    render(<Button disabled>Click me</Button>);

    // Assert
    expect(screen.getByRole("button")).toBeDisabled();
  });

  it("should not call onClick when disabled", () => {
    // Arrange
    const handleClick = vi.fn();
    render(
      <Button onClick={handleClick} disabled>
        Click me
      </Button>
    );

    // Act
    fireEvent.click(screen.getByRole("button"));

    // Assert
    expect(handleClick).not.toHaveBeenCalled();
  });

  it("should apply correct variant classes", () => {
    // Arrange & Act
    render(<Button variant="danger">Delete</Button>);

    // Assert
    const button = screen.getByRole("button");
    expect(button).toHaveClass("bg-red-500");
  });
});
```

**Run your test:**

```bash
npm test Button.test.jsx
```

✅ **Checkpoint:** Your component test passes!

### Step 4: Test User Interactions (20 minutes)

**Create:** `frontend/src/tests/unit/Counter.test.jsx`

```javascript
import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { useState } from "react";

// Counter component for testing interactions
function Counter({ initialValue = 0, onCountChange }) {
  const [count, setCount] = useState(initialValue);

  const increment = () => {
    const newCount = count + 1;
    setCount(newCount);
    onCountChange?.(newCount);
  };

  const decrement = () => {
    const newCount = count - 1;
    setCount(newCount);
    onCountChange?.(newCount);
  };

  const reset = () => {
    setCount(initialValue);
    onCountChange?.(initialValue);
  };

  return (
    <div>
      <div data-testid="count-display">Count: {count}</div>
      <button onClick={increment} data-testid="increment-btn">
        +
      </button>
      <button onClick={decrement} data-testid="decrement-btn">
        -
      </button>
      <button onClick={reset} data-testid="reset-btn">
        Reset
      </button>
    </div>
  );
}

describe("Counter Component", () => {
  it("should display initial count", () => {
    // Arrange & Act
    render(<Counter initialValue={5} />);

    // Assert
    expect(screen.getByTestId("count-display")).toHaveTextContent("Count: 5");
  });

  it("should increment count when + button is clicked", () => {
    // Arrange
    render(<Counter initialValue={0} />);

    // Act
    fireEvent.click(screen.getByTestId("increment-btn"));

    // Assert
    expect(screen.getByTestId("count-display")).toHaveTextContent("Count: 1");
  });

  it("should decrement count when - button is clicked", () => {
    // Arrange
    render(<Counter initialValue={5} />);

    // Act
    fireEvent.click(screen.getByTestId("decrement-btn"));

    // Assert
    expect(screen.getByTestId("count-display")).toHaveTextContent("Count: 4");
  });

  it("should reset count when Reset button is clicked", () => {
    // Arrange
    render(<Counter initialValue={10} />);

    // Act - increment first, then reset
    fireEvent.click(screen.getByTestId("increment-btn"));
    fireEvent.click(screen.getByTestId("reset-btn"));

    // Assert
    expect(screen.getByTestId("count-display")).toHaveTextContent("Count: 10");
  });

  it("should call onCountChange when count changes", () => {
    // Arrange
    const onCountChange = vi.fn();
    render(<Counter onCountChange={onCountChange} />);

    // Act
    fireEvent.click(screen.getByTestId("increment-btn"));

    // Assert
    expect(onCountChange).toHaveBeenCalledWith(1);
  });

  it("should handle multiple interactions", () => {
    // Arrange
    render(<Counter initialValue={0} />);

    // Act - multiple clicks
    fireEvent.click(screen.getByTestId("increment-btn"));
    fireEvent.click(screen.getByTestId("increment-btn"));
    fireEvent.click(screen.getByTestId("decrement-btn"));

    // Assert
    expect(screen.getByTestId("count-display")).toHaveTextContent("Count: 1");
  });
});
```

**Run your test:**

```bash
npm test Counter.test.jsx
```

✅ **Checkpoint:** Your interaction tests pass!

### Step 5: Test Form Components (25 minutes)

**Create:** `frontend/src/tests/unit/LoginForm.test.jsx`

```javascript
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { useState } from "react";

// Login form component for testing
function LoginForm({ onSubmit, isLoading = false }) {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });
  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors((prev) => ({
        ...prev,
        [name]: "",
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Basic validation
    const newErrors = {};
    if (!formData.email) newErrors.email = "Email is required";
    if (!formData.password) newErrors.password = "Password is required";

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    try {
      await onSubmit(formData);
    } catch (error) {
      setErrors({ general: error.message });
    }
  };

  return (
    <form onSubmit={handleSubmit} data-testid="login-form">
      <div>
        <label htmlFor="email">Email:</label>
        <input
          id="email"
          name="email"
          type="email"
          value={formData.email}
          onChange={handleChange}
          data-testid="email-input"
        />
        {errors.email && <span data-testid="email-error">{errors.email}</span>}
      </div>

      <div>
        <label htmlFor="password">Password:</label>
        <input
          id="password"
          name="password"
          type="password"
          value={formData.password}
          onChange={handleChange}
          data-testid="password-input"
        />
        {errors.password && (
          <span data-testid="password-error">{errors.password}</span>
        )}
      </div>

      {errors.general && (
        <div data-testid="general-error">{errors.general}</div>
      )}

      <button type="submit" disabled={isLoading} data-testid="submit-btn">
        {isLoading ? "Logging in..." : "Login"}
      </button>
    </form>
  );
}

describe("LoginForm Component", () => {
  let mockOnSubmit;

  beforeEach(() => {
    mockOnSubmit = vi.fn();
  });

  it("should render form fields", () => {
    // Arrange & Act
    render(<LoginForm onSubmit={mockOnSubmit} />);

    // Assert
    expect(screen.getByTestId("email-input")).toBeInTheDocument();
    expect(screen.getByTestId("password-input")).toBeInTheDocument();
    expect(screen.getByTestId("submit-btn")).toBeInTheDocument();
  });

  it("should update input values when user types", () => {
    // Arrange
    render(<LoginForm onSubmit={mockOnSubmit} />);
    const emailInput = screen.getByTestId("email-input");
    const passwordInput = screen.getByTestId("password-input");

    // Act
    fireEvent.change(emailInput, { target: { value: "test@test.com" } });
    fireEvent.change(passwordInput, { target: { value: "password123" } });

    // Assert
    expect(emailInput.value).toBe("test@test.com");
    expect(passwordInput.value).toBe("password123");
  });

  it("should show validation errors for empty fields", async () => {
    // Arrange
    render(<LoginForm onSubmit={mockOnSubmit} />);

    // Act
    fireEvent.click(screen.getByTestId("submit-btn"));

    // Assert
    await waitFor(() => {
      expect(screen.getByTestId("email-error")).toHaveTextContent(
        "Email is required"
      );
      expect(screen.getByTestId("password-error")).toHaveTextContent(
        "Password is required"
      );
    });
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  it("should call onSubmit with form data when valid", async () => {
    // Arrange
    render(<LoginForm onSubmit={mockOnSubmit} />);
    const emailInput = screen.getByTestId("email-input");
    const passwordInput = screen.getByTestId("password-input");

    // Act
    fireEvent.change(emailInput, { target: { value: "test@test.com" } });
    fireEvent.change(passwordInput, { target: { value: "password123" } });
    fireEvent.click(screen.getByTestId("submit-btn"));

    // Assert
    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith({
        email: "test@test.com",
        password: "password123",
      });
    });
  });

  it("should clear errors when user starts typing", async () => {
    // Arrange
    render(<LoginForm onSubmit={mockOnSubmit} />);
    const emailInput = screen.getByTestId("email-input");

    // Act - submit with empty fields to trigger errors
    fireEvent.click(screen.getByTestId("submit-btn"));

    // Wait for errors to appear
    await waitFor(() => {
      expect(screen.getByTestId("email-error")).toBeInTheDocument();
    });

    // Start typing to clear error
    fireEvent.change(emailInput, { target: { value: "test@test.com" } });

    // Assert
    expect(screen.queryByTestId("email-error")).not.toBeInTheDocument();
  });

  it("should show loading state when isLoading is true", () => {
    // Arrange & Act
    render(<LoginForm onSubmit={mockOnSubmit} isLoading={true} />);

    // Assert
    expect(screen.getByTestId("submit-btn")).toBeDisabled();
    expect(screen.getByTestId("submit-btn")).toHaveTextContent("Logging in...");
  });

  it("should handle submit errors", async () => {
    // Arrange
    const errorMessage = "Invalid credentials";
    mockOnSubmit.mockRejectedValue(new Error(errorMessage));
    render(<LoginForm onSubmit={mockOnSubmit} />);

    // Act
    fireEvent.change(screen.getByTestId("email-input"), {
      target: { value: "test@test.com" },
    });
    fireEvent.change(screen.getByTestId("password-input"), {
      target: { value: "wrongpassword" },
    });
    fireEvent.click(screen.getByTestId("submit-btn"));

    // Assert
    await waitFor(() => {
      expect(screen.getByTestId("general-error")).toHaveTextContent(
        errorMessage
      );
    });
  });
});
```

**Run your test:**

```bash
npm test LoginForm.test.jsx
```

✅ **Checkpoint:** Your form tests pass!

---

## 🎓 What You Learned

- ✅ How to render React components in tests
- ✅ How to query elements with `screen` and `getByRole`
- ✅ How to simulate user interactions with `fireEvent`
- ✅ How to test component state and props
- ✅ How to test form validation and submission
- ✅ How to test loading states and error handling
- ✅ How to use `waitFor` for async operations

---

## 💪 Practice Challenges

### Challenge 1: Test a Todo Component

Create a Todo component with:

- Add new todos
- Mark todos as complete
- Delete todos
- Filter todos (all, active, completed)

Write tests for all functionality.

### Challenge 2: Test a Modal Component

Create a Modal component with:

- Open/close functionality
- Click outside to close
- Escape key to close
- Focus management

Write tests for all interactions.

### Challenge 3: Test a Search Component

Create a Search component with:

- Input field
- Search button
- Clear button
- Debounced search
- Loading state

Write tests for all features.

---

## 🚨 Common Mistakes

### Mistake 1: Testing Implementation Details

```javascript
// ❌ BAD - Testing how it works, not what it does
it("should call setState", () => {
  const setState = vi.fn();
  render(<Counter setState={setState} />);
  fireEvent.click(screen.getByText("+"));
  expect(setState).toHaveBeenCalled();
});

// ✅ GOOD - Testing the result, not the implementation
it("should increment count when + is clicked", () => {
  render(<Counter />);
  fireEvent.click(screen.getByText("+"));
  expect(screen.getByText("Count: 1")).toBeInTheDocument();
});
```

### Mistake 2: Not Waiting for Async Operations

```javascript
// ❌ BAD - Not waiting for async operation
it("should show success message", () => {
  render(<Form onSubmit={asyncSubmit} />);
  fireEvent.click(screen.getByText("Submit"));
  expect(screen.getByText("Success!")).toBeInTheDocument(); // Fails!
});

// ✅ GOOD - Wait for async operation
it("should show success message", async () => {
  render(<Form onSubmit={asyncSubmit} />);
  fireEvent.click(screen.getByText("Submit"));
  await waitFor(() => {
    expect(screen.getByText("Success!")).toBeInTheDocument();
  });
});
```

### Mistake 3: Not Testing User Experience

```javascript
// ❌ BAD - Testing internal state
it("should set loading to true", () => {
  render(<Button />);
  fireEvent.click(screen.getByText("Submit"));
  expect(component.state.loading).toBe(true);
});

// ✅ GOOD - Testing what user sees
it("should show loading state when clicked", () => {
  render(<Button />);
  fireEvent.click(screen.getByText("Submit"));
  expect(screen.getByText("Loading...")).toBeInTheDocument();
});
```

---

## 🎯 Pro Tips

### Tip 1: Use Semantic Queries

```javascript
// ❌ BAD - Fragile selectors
screen.getByTestId("submit-button");

// ✅ GOOD - Semantic queries
screen.getByRole("button", { name: "Submit" });
```

### Tip 2: Test User Flows, Not Individual Functions

```javascript
// ❌ BAD - Testing individual functions
it("should call validateEmail", () => {
  // Test implementation
});

// ✅ GOOD - Testing user flow
it("should show error for invalid email", () => {
  render(<LoginForm />);
  fireEvent.change(screen.getByLabelText("Email"), {
    target: { value: "invalid-email" },
  });
  fireEvent.click(screen.getByRole("button", { name: "Login" }));
  expect(screen.getByText("Invalid email")).toBeInTheDocument();
});
```

### Tip 3: Use Custom Render Functions

```javascript
// ✅ GOOD - Custom render with providers
const renderWithProviders = (ui, options = {}) => {
  const { user, ...renderOptions } = options;

  const Wrapper = ({ children }) => (
    <BrowserRouter>
      <AuthContext.Provider value={mockAuth}>{children}</AuthContext.Provider>
    </BrowserRouter>
  );

  return {
    user: userEvent.setup(),
    ...render(ui, { wrapper: Wrapper, ...renderOptions }),
  };
};
```

---

## ✅ Completion Checklist

- [ ] Ran existing component tests
- [ ] Wrote `Button.test.jsx` and it passes
- [ ] Wrote `Counter.test.jsx` and it passes
- [ ] Wrote `LoginForm.test.jsx` and it passes
- [ ] Understand how to test user interactions
- [ ] Understand how to test forms and validation
- [ ] Completed at least 1 practice challenge

---

## 🎯 Key Takeaways

1. **Test user experience, not implementation** - Focus on what users see and do
2. **Use semantic queries** - `getByRole`, `getByLabelText` are more reliable
3. **Test interactions, not state** - Test what happens when users click/type
4. **Wait for async operations** - Use `waitFor` for async updates
5. **Test error cases** - Users make mistakes, test error handling

---

**Ready for more?**

- **[LAB_05_Test_Data_Management_JavaScript.md](LAB_05_Test_Data_Management_JavaScript.md)** - Learn test data patterns
- **[React Testing Library Docs](https://testing-library.com/docs/react-testing-library/intro/)** - Official documentation
- **[Vitest Component Testing](https://vitest.dev/guide/testing.html#component-testing)** - Vitest component testing guide

---

**🎉 Congratulations!** You're now testing React components like a pro!

**Next Lab:** [Lab 5: Test Data Management (JavaScript)](LAB_05_Test_Data_Management_JavaScript.md)
